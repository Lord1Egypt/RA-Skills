import argparse
import scanner
import analyzer
import audit
import kbmap
import msrc
import json
import sys
import os
from pathlib import Path
import subprocess
import re
import html as _html
import datetime
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed

def _h(x):
    return _html.escape("" if x is None else str(x), quote=True)

def _is_pcish_target(target: str) -> bool:
    t = (target or "").strip().lower()
    if t in ("localhost",):
        return True
    try:
        ip = ipaddress.ip_address(t)
        return bool(ip.is_loopback or ip.is_private or ip.is_link_local)
    except Exception:
        return False

def main():
    parser = argparse.ArgumentParser(description="OpenClaw Vulnerability Scanner")
    parser.add_argument("target", nargs="?", help="IP address or hostname of the target")
    parser.add_argument("--targets-file", help="File containing targets, one per line", default=None)
    parser.add_argument("--port", type=int, help="Port to scan (optional, otherwise default ports)", default=None)
    parser.add_argument("--ports", help="Comma-separated ports to scan", default=None)
    parser.add_argument("--max-workers", type=int, default=64)
    parser.add_argument("--port-timeout", type=float, default=0.5)
    parser.add_argument("--http-timeout", type=float, default=2.0)
    parser.add_argument("--assume-version", default=None)
    parser.add_argument("--enable-cred-check", action="store_true", help="Enable active default-credential check (disabled by default)")
    parser.add_argument("--enable-leak-check", action="store_true", help="Enable active exposure check on OpenClaw endpoints (disabled by default)")
    parser.add_argument("--skip-cred-check", action="store_true", help="Disable credential check (compat)")
    parser.add_argument("--skip-leak-check", action="store_true", help="Disable exposure check (compat)")
    parser.add_argument("--insecure", action="store_true", help="Allow insecure HTTPS (skip TLS certificate verification) for probing")
    parser.add_argument("--audit", action="store_true", help="Perform local OS/Node.js audit (requires local execution)")
    parser.add_argument("--latest-openclaw-version", default=None, help="Latest OpenClaw version string for local CLI comparison (e.g. v2026.3.2)")
    parser.add_argument("--npm-view-latest-openclaw", action="store_true", help="Fetch latest OpenClaw version from npm registry via `npm view openclaw version`")
    parser.add_argument("--kb-map-path", default=None, help="Path to Windows CVE↔KB mapping CSV (default: papar/windows_cve_kb_map.csv)")
    parser.add_argument("--windows-cves", default=None, help="Comma-separated CVEs to check against Windows KB mapping")
    parser.add_argument("--windows-cves-file", default=None, help="File containing CVEs (one per line) to check against Windows KB mapping")
    parser.add_argument("--msrc-cvrf-id", default=None, help="MSRC CVRF ID to fetch (e.g. 2026-Mar)")
    parser.add_argument("--msrc-cvrf-ids", default=None, help="Comma-separated MSRC CVRF IDs to fetch and merge (e.g. 2026-Jan,2026-Feb,2026-Mar)")
    parser.add_argument("--msrc-cvrf-from", default=None, help="Start MSRC CVRF ID (inclusive) for month range (e.g. 2016-Jan)")
    parser.add_argument("--msrc-cvrf-to", default=None, help="End MSRC CVRF ID (inclusive) for month range (e.g. 2026-Mar)")
    parser.add_argument("--msrc-cvrf-cache-dir", default=None, help="Directory to cache downloaded CVRF JSON (default: papar/msrc_cvrf_cache)")
    parser.add_argument("--msrc-cvrf-rate-limit", type=float, default=0.6, help="Seconds to wait between CVRF requests (default: 0.6)")
    parser.add_argument("--msrc-cvrf-retries", type=int, default=4, help="Retry count for CVRF requests (default: 4)")
    parser.add_argument("--merge-existing-kb-map", action="store_true", help="Merge with existing windows_cve_kb_map.csv instead of overwriting")
    parser.add_argument("--update-windows-kb-map", action="store_true", help="Fetch MSRC CVRF and generate/update local Windows CVE↔KB mapping CSV")
    parser.add_argument("--watchlist-path", default=None, help="Path to CVE watchlist CSV (default: papar/cve_analysis_result.csv)")
    parser.add_argument("--check-watchlist-all", action="store_true", help="Check all CVEs from watchlist CSV against Windows KB mapping")
    parser.add_argument("--msrc-api-key", default=None, help="MSRC SUG API key for CVE->KB lookup (optional; can also use env MSRC_API_KEY)")
    parser.add_argument("--update-windows-kb-map-from-watchlist", action="store_true", help="Use MSRC SUG API to map all watchlist CVEs to KBs and update mapping CSV")
    parser.add_argument("--out-dir", default="output")
    parser.add_argument("--no-html", action="store_true")
    args = parser.parse_args()

    # Allow running just audit without target
    if not args.target and not args.targets_file and not args.audit:
        parser.print_help()
        sys.exit(2)

    targets = []
    if args.target:
        targets.append(args.target.strip())
    if args.targets_file:
        p = Path(args.targets_file)
        if p.exists():
            for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
                t = line.strip()
                if t and not t.startswith("#"):
                    targets.append(t)
    
    # If no targets but audit is requested, just do audit
    if not targets and args.audit:
        print("[*] No network targets provided, performing local audit only.")

    targets = [t for i, t in enumerate(targets) if t and t not in targets[:i]]
    
    def _validate_port(p):
        return isinstance(p, int) and 1 <= p <= 65535

    ports = None
    if args.ports:
        try:
            ports = [int(x.strip()) for x in args.ports.split(",") if x.strip()]
        except ValueError:
            parser.error("--ports must be a comma-separated list of integers")
        bad = [p for p in ports if not _validate_port(p)]
        if bad:
            parser.error(f"Invalid port(s) in --ports: {', '.join(str(x) for x in bad)} (valid range: 1-65535)")
    elif args.port:
        if not _validate_port(args.port):
            parser.error("--port must be in range 1-65535")
        ports = [args.port]

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    report_base = "scan_report"
    run_id = "latest"

    def get_local_bindings(ports_to_check):
        if not ports_to_check:
            return {}
        if sys.platform != "win32":
            return {}
        try:
            out = subprocess.check_output(["netstat", "-ano", "-p", "tcp"], text=True, encoding="utf-8", errors="ignore")
        except Exception:
            return {}
        bindings = {int(p): [] for p in ports_to_check}
        pat = re.compile(r"^\s*TCP\s+(\S+):(\d+)\s+\S+\s+LISTENING\s+(\d+)\s*$", re.IGNORECASE)
        for line in out.splitlines():
            m = pat.match(line)
            if not m:
                continue
            addr, port_s, pid_s = m.group(1), m.group(2), m.group(3)
            try:
                port_i = int(port_s)
            except ValueError:
                continue
            if port_i not in bindings:
                continue
            bindings[port_i].append({"local_address": addr, "pid": int(pid_s)})
        return bindings
    
    local_audit_results = None
    if args.audit:
        try:
            raw_audit = audit.audit_local_system()
            raw_audit.setdefault("policy", {})
            if isinstance(raw_audit.get("policy"), dict):
                base = Path(__file__).resolve().parent.parent
                pol = raw_audit["policy"]

                kb_map_path = Path(args.kb_map_path) if args.kb_map_path else (base / "papar" / "windows_cve_kb_map.csv")
                pol["windows_kb_map_path"] = str(kb_map_path)
                watchlist_path = Path(args.watchlist_path) if args.watchlist_path else (base / "papar" / "cve_analysis_result.csv")
                pol["watchlist_path"] = str(watchlist_path)

                if args.windows_cves or args.windows_cves_file:
                    cves = []
                    if args.windows_cves:
                        cves.extend([x.strip() for x in str(args.windows_cves).split(",") if x.strip()])
                    if args.windows_cves_file:
                        p = Path(args.windows_cves_file)
                        if p.exists():
                            for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
                                t = line.strip()
                                if t and not t.startswith("#"):
                                    cves.append(t)
                    cves = [x.upper() for x in cves]
                    cves = [x for i, x in enumerate(cves) if x and x not in cves[:i]]
                    if cves:
                        pol["windows_cves"] = cves
                elif args.check_watchlist_all:
                    pol["windows_cves"] = kbmap.load_cves_from_csv(watchlist_path)

                if args.update_windows_kb_map:
                    ids = []
                    if args.msrc_cvrf_id:
                        ids.append(str(args.msrc_cvrf_id).strip())
                    if args.msrc_cvrf_ids:
                        ids.extend([x.strip() for x in str(args.msrc_cvrf_ids).split(",") if x.strip()])
                    if args.msrc_cvrf_from or args.msrc_cvrf_to:
                        if not (args.msrc_cvrf_from and args.msrc_cvrf_to):
                            parser.error("--msrc-cvrf-from and --msrc-cvrf-to must be used together")
                        ids.extend(msrc.generate_cvrf_ids(args.msrc_cvrf_from, args.msrc_cvrf_to))
                    ids = [x for i, x in enumerate(ids) if x and x not in ids[:i]]
                    if not ids:
                        parser.error("--update-windows-kb-map requires --msrc-cvrf-id, --msrc-cvrf-ids, or --msrc-cvrf-from/--msrc-cvrf-to")

                    base_map = {}
                    if args.merge_existing_kb_map:
                        base_map = kbmap.load_cve_kb_map_csv(kb_map_path)

                    merged = {k: set(v) for k, v in (base_map or {}).items()}
                    cache_dir = Path(args.msrc_cvrf_cache_dir) if args.msrc_cvrf_cache_dir else (base / "papar" / "msrc_cvrf_cache")
                    cvrf_failed = []
                    for cid in ids:
                        try:
                            doc = msrc.fetch_cvrf_document_cached(
                                cid,
                                cache_dir=cache_dir,
                                timeout_s=15,
                                rate_limit_s=float(args.msrc_cvrf_rate_limit),
                                retries=int(args.msrc_cvrf_retries),
                            )
                        except Exception:
                            if len(cvrf_failed) < 50:
                                cvrf_failed.append(cid)
                            continue
                        mapping = kbmap.extract_cve_kb_map_from_cvrf(doc)
                        for cve, kbs in (mapping or {}).items():
                            merged.setdefault(cve, set()).update(set(kbs or set()))

                    source = "msrc_cvrf:" + ",".join(ids)
                    kbmap.save_cve_kb_map_csv(kb_map_path, merged, source=source)
                    pol["msrc_cvrf_ids"] = ids
                    pol["msrc_cvrf_cache_dir"] = str(cache_dir)
                    pol["msrc_cvrf_rate_limit"] = float(args.msrc_cvrf_rate_limit)
                    pol["windows_kb_map_count"] = len(merged)
                    if cvrf_failed:
                        pol["msrc_cvrf_failed_count"] = len(cvrf_failed)
                        pol["msrc_cvrf_failed_sample"] = cvrf_failed[:20]

                if args.update_windows_kb_map_from_watchlist:
                    key = (args.msrc_api_key or os.environ.get("MSRC_API_KEY") or "").strip()
                    if not key:
                        parser.error("--update-windows-kb-map-from-watchlist requires --msrc-api-key or env MSRC_API_KEY")
                    all_cves = kbmap.load_cves_from_csv(watchlist_path)
                    base_map = kbmap.load_cve_kb_map_csv(kb_map_path) if args.merge_existing_kb_map else {}
                    merged = {k: set(v) for k, v in (base_map or {}).items()}
                    updated = 0
                    missing = [c for c in all_cves if c and not (c in merged and merged.get(c))]
                    chunk = 25
                    for i in range(0, len(missing), chunk):
                        group = missing[i:i+chunk]
                        try:
                            m = msrc.fetch_kbs_by_cves_sug(group, key)
                        except Exception:
                            m = {}
                        for cve, kbs in (m or {}).items():
                            if kbs:
                                if not merged.get(cve):
                                    updated += 1
                                merged.setdefault(cve, set()).update(set(kbs))
                    kbmap.save_cve_kb_map_csv(kb_map_path, merged, source="msrc_sug")
                    pol["windows_kb_map_count"] = len(merged)
                    pol["windows_kb_map_updated_from_watchlist"] = updated

                if args.latest_openclaw_version:
                    pol["latest_openclaw_version"] = args.latest_openclaw_version
                elif args.npm_view_latest_openclaw:
                    latest = audit.get_openclaw_latest_version_from_npm()
                    if latest:
                        pol["latest_openclaw_version"] = latest
            local_audit_results = {
                "raw": raw_audit,
                "findings": audit.analyze_audit_data(raw_audit)
            }
        except Exception as e:
            print(f"[-] Local audit failed: {e}")

    print(f"[*] Starting OpenClaw Scan for {len(targets)} target(s)...")
    results = []

    def scan_one(t):
        scan_res = scanner.run_scan(
            t,
            ports=ports,
            port_timeout_s=args.port_timeout,
            http_timeout_s=args.http_timeout,
            max_workers=args.max_workers,
            insecure=args.insecure,
        )
        services = scan_res.get("services", [])
        findings = []
        enable_cred_check = bool(args.enable_cred_check) and (not args.skip_cred_check)
        enable_leak_check = bool(args.enable_leak_check) and (not args.skip_leak_check)
        for s in services:
            findings.append(
                analyzer.run_analysis(
                    s,
                    assume_version=args.assume_version,
                    enable_cred_check=enable_cred_check,
                    enable_exposure_check=enable_leak_check,
                    timeout_s=args.http_timeout,
                )
            )
        local_bindings = {}
        if t in ("127.0.0.1", "localhost", "::1"):
            local_bindings = get_local_bindings(scan_res.get("open_ports", []))
        return {
            "target": t,
            "open_ports": scan_res.get("open_ports", []),
            "services": services,
            "findings": findings,
            "local_bindings": local_bindings,
        }

    if targets:
        with ThreadPoolExecutor(max_workers=min(len(targets), max(1, args.max_workers))) as executor:
            future_map = {executor.submit(scan_one, t): t for t in targets}
            for fut in as_completed(future_map):
                t = future_map[fut]
                try:
                    results.append(fut.result())
                except Exception as e:
                    results.append(
                        {
                            "target": t,
                            "open_ports": [],
                            "services": [],
                            "findings": [],
                            "local_bindings": {},
                            "error": str(e),
                        }
                    )

        results.sort(key=lambda x: x.get("target", ""))

    print("\n" + "=" * 40)
    print(" SCAN REPORT ")
    print("=" * 40)

    severities = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0, "unknown": 0}
    for r in results:
        print(f"Target: {r['target']}")
        if r.get("error"):
            print(f"  Scan error: {r.get('error')}")
            continue
        if not r.get("open_ports"):
            print("  No open ports found.")
            continue
        print(f"  Open ports: {r['open_ports']}")
        if r.get("local_bindings"):
            for p, binds in r["local_bindings"].items():
                if binds:
                    addrs = ", ".join(sorted({b.get('local_address', '') for b in binds if b.get('local_address')}))
                    print(f"  Local bindings for {p}: {addrs}")
        if not r.get("findings"):
            print("  No OpenClaw services identified.")
            continue
        for f in r["findings"]:
            vlist = f.get("vulnerabilities", [])
            if not vlist:
                print(f"  Service: {f.get('target')} - No vulnerabilities found.")
                continue
            print(f"  Service: {f.get('target')}")
            for v in vlist:
                sev = (v.get("severity") or "Unknown").lower()
                sev_key = sev if sev in severities else "unknown"
                severities[sev_key] += 1
                print(f"    [{v.get('severity','Unknown')}] {v.get('type','')}")

    if local_audit_results:
        print(f"Local Audit Findings:")
        for f in local_audit_results["findings"]:
            print(f"    [{f.get('severity')}] {f.get('type')}: {f.get('details')}")

    json_path = out_dir / f"{report_base}.json"
    try:
        report_data = {
            "results": results
        }
        if local_audit_results:
            report_data["local_audit"] = local_audit_results
            
        json_path.write_text(json.dumps(report_data, indent=4, ensure_ascii=False), encoding="utf-8")
        print(f"\n[+] Detailed report saved to {json_path.as_posix()}")
    except Exception as e:
        print(f"[-] Failed to save report: {e}")

    if not args.no_html:
        html_path = out_dir / f"{report_base}.html"
        try:
            total_targets = len(results)
            total_services = sum(len(r.get("findings", [])) for r in results)
            total_open_ports = sum(len(r.get("open_ports", [])) for r in results)
            
            # Add audit findings to severities
            if local_audit_results:
                for f in local_audit_results["findings"]:
                    sev = (f.get("severity") or "Unknown").lower()
                    sev_key = sev if sev in severities else "unknown"
                    severities[sev_key] += 1
            
            def _is_private_or_local(host):
                h = (host or "").strip().lower()
                if h in ("127.0.0.1", "localhost", "::1"):
                    return True
                parts = h.split(".")
                if len(parts) == 4 and all(p.isdigit() for p in parts):
                    a, b, c, d = [int(x) for x in parts]
                    if a == 10:
                        return True
                    if a == 192 and b == 168:
                        return True
                    if a == 172 and 16 <= b <= 31:
                        return True
                    if a == 127:
                        return True
                return False

            def _default_lang():
                if results:
                    return "zh" if _is_private_or_local(results[0].get("target")) else "en"
                return "zh"

            def _health_level():
                if severities.get("critical", 0) > 0 or severities.get("high", 0) > 0:
                    return "red"
                if severities.get("medium", 0) > 0:
                    return "yellow"
                return "green"

            local_cli_version = None
            if local_audit_results and isinstance(local_audit_results, dict):
                raw = local_audit_results.get("raw") or {}
                if isinstance(raw, dict):
                    oc = raw.get("openclaw") or {}
                    if isinstance(oc, dict):
                        local_cli_version = oc.get("version") or None

            sev_kpis = [
                ("critical", severities.get("critical", 0)),
                ("high", severities.get("high", 0)),
                ("medium", severities.get("medium", 0)),
                ("low", severities.get("low", 0)),
                ("info", severities.get("info", 0)),
                ("unknown", severities.get("unknown", 0)),
            ]
            kpi_html = "".join([f"<div class='kpi'><div class='k' data-k='sev_{k}'></div><div class='v'>{v}</div></div>" for k, v in sev_kpis])

            recos = []
            def _add_reco(k, zh, en):
                recos.append({"k": k, "zh": zh, "en": en})
            red_types = []
            red_seen = set()
            def _is_red(sev):
                s = str(sev or "").strip().lower()
                return s in ("critical", "high")
            def _add_red_type(t):
                tt = str(t or "").strip()
                if not tt:
                    return
                if tt in red_seen:
                    return
                red_seen.add(tt)
                red_types.append(tt)
            for r in results:
                for f in r.get("findings", []) or []:
                    for v in f.get("vulnerabilities", []) or []:
                        if _is_red(v.get("severity")):
                            _add_red_type(v.get("type"))
            if local_audit_results:
                for f in local_audit_results.get("findings", []) or []:
                    if _is_red(f.get("severity")):
                        _add_red_type(f.get("type"))

            for t in red_types:
                if t == "weak_credentials":
                    _add_reco("weak_credentials", "立刻修改默认口令，禁用弱口令/默认账号，并开启 MFA（如支持）。", "Change default credentials immediately, disable default accounts, and enable MFA if available.")
                elif t in ("openclaw_outdated", "openclaw_version_mismatch"):
                    _add_reco("openclaw_outdated", "升级 OpenClaw 到最新稳定版本并谨慎验证：升级后部分或全部功能可能不可用，请结合自身情况判断。", "Upgrade OpenClaw to the latest stable release and validate carefully: after upgrading, some or all functions may be unavailable; assess carefully.")
                elif t == "windows_support_status":
                    _add_reco("windows_support_status", "你的 Windows 已停止获得安全更新。步骤：1) 打开“设置”→“Windows 更新”，看是否能升级到 Windows 11；2) 如果不能升级，了解 ESU 延伸支持方案并评估是否需要；3) 升级/开通后，再运行一次本工具确认状态。", "Your Windows version is no longer receiving security updates. Steps: 1) Open Settings → Windows Update and check if you can upgrade; 2) If you cannot upgrade, learn about ESU extended support and decide if you need it; 3) After upgrading/enrolling, rerun this tool to confirm.")
                elif t == "windows_cve_unpatched":
                    _add_reco("windows_cve_unpatched", "按报告列出的 KB 安装系统更新，并在安装后重新审计验证。", "Install the missing Windows updates (KBs) and rerun the audit to verify.")
                elif t == "windows_kb_map_missing":
                    _add_reco("windows_kb_map_missing", "先生成 CVE↔KB 映射文件（MSRC CVRF），再做补丁核验。", "Generate a CVE↔KB mapping from MSRC CVRF first, then validate patch status.")
                elif t == "unknown_version":
                    _add_reco("unknown_version", "让服务暴露版本信息（如 X-OpenClaw-Version 或 /api/status），便于自动化风控。", "Expose service version (e.g., X-OpenClaw-Version or /api/status) to enable automated risk checks.")
                elif t == "defender_status":
                    _add_reco("defender_status", "你的电脑防病毒保护已关闭或过期。步骤：1) 打开“Windows 安全中心”→“病毒和威胁防护”→“管理设置”，开启“实时保护”；2) 回到“病毒和威胁防护”，点击“检查更新/更新病毒库”；3) 如果你用的是第三方杀软：确认它处于启用并已更新。", "Antivirus protection is turned off or out of date. Steps: 1) Open Windows Security → Virus & threat protection → Manage settings, turn on Real-time protection; 2) Go back and check for updates to refresh signatures; 3) If you use a third-party antivirus, make sure it is enabled and updated.")
                elif t == "browser_outdated":
                    _add_reco("browser_outdated", "你的浏览器版本有已知安全漏洞。步骤：1) 打开浏览器，点右上角菜单；2) 进入“帮助/关于”，点击“检查更新”并等待安装完成；3) 重启浏览器，并打开“自动更新”（如有）。", "Your browser is out of date and may have known security issues. Steps: 1) Open the browser menu (top-right); 2) Go to Help/About and check for updates until it finishes; 3) Restart the browser and enable auto-update if available.")
                elif t == "server_auth_disabled":
                    _add_reco("server_auth_disabled", "任何人都能直接访问你的 OpenClaw，需要立即开启密码保护。步骤：1) 找到配置文件（Windows：%APPDATA%\\openclaw\\config.json；macOS：~/.openclaw/config.json）；2) 在配置里开启“auth/认证”相关开关，并设置访问密码（如支持）；3) 重启 OpenClaw 服务后再检查一次。", "Anyone who can reach your OpenClaw may be able to access it. Enable password protection now. Steps: 1) Find the config file (Windows: %APPDATA%\\openclaw\\config.json; macOS: ~/.openclaw/config.json); 2) Turn on the auth/password protection option and set a password if supported; 3) Restart OpenClaw and rerun this tool to confirm.")
                elif t == "server_default_port":
                    _add_reco("server_default_port", "你在用默认端口，容易被自动化扫描工具发现。步骤：1) 打开配置文件（Windows：%APPDATA%\\openclaw\\config.json；macOS：~/.openclaw/config.json）；2) 把端口改成别的数字（不要用 18789）；3) 重启服务，并同步更新防火墙/安全组放行的新端口。", "You are using the default port, which is easier to find by automated scans. Steps: 1) Open the config file (Windows: %APPDATA%\\openclaw\\config.json; macOS: ~/.openclaw/config.json); 2) Change the port to a different number (avoid 18789); 3) Restart the service and update firewall/security-group rules to match.")
                elif t == "server_exposed_public":
                    _add_reco("server_exposed_public", "你的服务对所有网络开放，建议限制访问来源。步骤：1) 在防火墙/云平台安全组里，只允许你自己的 IP 访问；2) 或把监听地址改成 127.0.0.1（只允许本机访问）；3) 重启服务后再检查一次。", "Your service is reachable from other networks. Restrict who can access it. Steps: 1) In your firewall/security-group, allow only your own IP; 2) Or bind/listen on 127.0.0.1 for local-only access; 3) Restart the service and rerun this tool to confirm.")
                else:
                    _add_reco(t, f"发现高风险项：{t}。请参考报告详情，尽快采取缓解/修复措施并复核。", f"High-risk finding detected: {t}. Refer to report details, remediate, and re-verify.")
            if not recos:
                _add_reco("ok", "当前未发现高风险项，建议保持系统与 OpenClaw 定期更新，并持续最小暴露面。", "No high-risk issues detected. Keep OS/OpenClaw updated and continue minimizing exposure.")

            cards = []

            if local_audit_results:
                items = []
                for f in local_audit_results["findings"]:
                    sev = f.get("severity", "Unknown")
                    sev_cls = str(sev).lower()
                    det = f.get("details", "")
                    items.append(
                        f"<li>"
                        f"<div class='row'>"
                        f"<span class='sev sev-{_h(sev_cls)}' data-sev='{_h(sev_cls)}'>{_h(sev)}</span>"
                        f"<span class='type'>{_h(f.get('type',''))}</span>"
                        f"</div>"
                        f"<div class='details'>{_h(det)}</div>"
                        f"</li>"
                    )
                meta_parts = [f"<span data-k='local_host'></span>: {_h(audit.get_os_info().get('system'))}"]
                if local_cli_version:
                    meta_parts.append(f"<span data-k='local_openclaw_cli'></span>: {_h(local_cli_version)}")
                cards.append(
                    f"<div class='card'>"
                    f"<div class='card-head'>"
                    f"<div class='card-title' data-k='local_audit_title'></div>"
                    f"<div class='card-meta'>{' · '.join(meta_parts)}</div>"
                    f"</div>"
                    f"<div class='section'>"
                    f"<div class='label' data-k='audit_findings'></div>"
                    f"<ul class='vuln'>{''.join(items)}</ul>"
                    f"</div>"
                    f"</div>"
                )

            for r in results:
                binds_html = ""
                if r.get("local_bindings"):
                    parts = []
                    for p, binds in r["local_bindings"].items():
                        if not binds:
                            continue
                        addrs = ", ".join(sorted({b.get("local_address", "") for b in binds if b.get("local_address")}))
                        parts.append(f"<div class='sub'><span data-k='port'></span> {_h(p)}: {_h(addrs)}</div>")
                    if parts:
                        binds_html = "<div class='section'><div class='label' data-k='local_bindings'></div>" + "".join(parts) + "</div>"

                open_ports_html = ", ".join(str(p) for p in r.get("open_ports", [])) or "-"
                err = r.get("error")
                err_html = f"<div class='err'>{_h(err)}</div>" if err else ""
                findings = r.get("findings", [])
                if err:
                    vuln_html = "<div class='ok' data-k='no_results'></div>"
                elif not findings:
                    vuln_html = "<div class='ok' data-k='no_openclaw'></div>"
                else:
                    items = []
                    for f in findings:
                        vlist = f.get("vulnerabilities", [])
                        svc = f.get("service", "") or ""
                        svc_target = f.get("target", "") or ""
                        svc_version = f.get("version", "") or ""
                        svc_version_norm = str(svc_version).strip()
                        if svc_version_norm.lower() in ("unknown", "none", ""):
                            svc_version_html = f"<span class='muted' data-k='version_not_exposed'></span>"
                        else:
                            svc_version_html = _h(svc_version_norm)

                        extra_meta = ""
                        if _is_private_or_local(r.get("target")) and local_cli_version:
                            if svc_version_norm.lower() in ("unknown", "none", ""):
                                extra_meta = f"<div class='svc-sub'><span data-k='local_openclaw_cli'></span>: {_h(local_cli_version)}</div>"

                        header = (
                            f"<div class='svc'>"
                            f"<div class='svc-left'>"
                            f"<div class='svc-title'>{_h(svc)}</div>"
                            f"<div class='svc-meta'>{_h(svc_target)}</div>"
                            f"{extra_meta}"
                            f"</div>"
                            f"<div class='svc-right'>"
                            f"<div class='svc-k' data-k='service_version'></div>"
                            f"<div class='svc-v'>{svc_version_html}</div>"
                            f"</div>"
                            f"</div>"
                        )
                        if not vlist:
                            items.append(header + "<div class='ok' data-k='no_vulns'></div>")
                            continue
                        li = []
                        for v in vlist:
                            sev = v.get("severity", "Unknown")
                            sev_cls = str(sev).lower()
                            det = v.get("details", "")
                            cves = ", ".join(v.get("cves", [])) if v.get("cves") else ""
                            hits = ""
                            if v.get("hits"):
                                hit_lines = []
                                for h in v["hits"]:
                                    kw_list = h.get("keywords", [])
                                    kw_list = kw_list if isinstance(kw_list, list) else [str(kw_list)]
                                    hit_lines.append(f"<div class='hit'><span class='path'>{_h(h.get('path',''))}</span><span class='kw'>{_h(', '.join([str(x) for x in kw_list]))}</span></div>")
                                hits = "<div class='hits'>" + "".join(hit_lines) + "</div>"
                            cve_html = f"<div class='cves'>{_h(cves)}</div>" if cves else ""
                            det_html = f"<div class='details'>{_h(det)}</div>" if det else ""
                            li.append(
                                f"<li>"
                                f"<div class='row'>"
                                f"<span class='sev sev-{_h(sev_cls)}' data-sev='{_h(sev_cls)}'>{_h(sev)}</span>"
                                f"<span class='type'>{_h(v.get('type',''))}</span>"
                                f"</div>"
                                f"{det_html}{cve_html}{hits}"
                                f"</li>"
                            )
                        items.append(header + "<ul class='vuln'>" + "".join(li) + "</ul>")
                    vuln_html = "".join(items)

                cards.append(
                    f"<div class='card'>"
                    f"<div class='card-head'>"
                    f"<div class='card-title'>{_h(r.get('target',''))}</div>"
                    f"<div class='card-meta'><span data-k='open_ports'></span>: {_h(open_ports_html)}</div>"
                    f"</div>"
                    f"{err_html}"
                    f"{binds_html}"
                    f"<div class='section'><div class='label' data-k='findings'></div>{vuln_html}</div>"
                    f"</div>"
                )

            lang = _default_lang()
            health = _health_level()
            reco_json = json.dumps(recos, ensure_ascii=False)
            scan_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            html_report_data = {"results": results}
            if local_audit_results:
                html_report_data["local_audit"] = local_audit_results
            report_json = json.dumps(html_report_data, ensure_ascii=False).replace("</", "<\\/")
            counts_json = json.dumps(severities, ensure_ascii=False)
            report_targets = [r.get("target") for r in (results or []) if isinstance(r, dict) and r.get("target")]
            report_kind = "pc" if report_targets and all(_is_pcish_target(t) for t in report_targets) else "server"

            html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>OpenClaw Scan Report</title>
  <style>
    :root {{
      --bg1:#f5f7ff;
      --bg2:#f7f8fa;
      --card:#ffffffcc;
      --border:#e7e9ee;
      --text:#0b0f19;
      --muted:#6b7280;
      --shadow:0 10px 30px rgba(12, 20, 40, .08);
      --shadow2:0 1px 2px rgba(12, 20, 40, .06);
      --r:18px;
      --red:#ff3b30;
      --yellow:#ffcc00;
      --green:#34c759;
      --blue:#0a84ff;
    }}
    html,body{{height:100%}}
    body{{
      margin:0;
      padding:28px;
      color:var(--text);
      background:radial-gradient(1200px 600px at 20% 0%, var(--bg1), transparent),
                 radial-gradient(1200px 600px at 90% 10%, #fdf2ff, transparent),
                 linear-gradient(180deg, var(--bg2), #ffffff);
      font-family:-apple-system,BlinkMacSystemFont,"SF Pro Display","SF Pro Text","Segoe UI",Roboto,Helvetica,Arial,"Apple Color Emoji","Segoe UI Emoji";
    }}
    .wrap{{max-width:1100px;margin:0 auto}}
    .topbar{{display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;margin-bottom:18px}}
    .title h1{{margin:0;font-size:22px;letter-spacing:-.02em}}
    .sub{{color:var(--muted);font-size:12px}}
    .actions{{display:flex;gap:10px;align-items:center}}
    .btn{{
      border:1px solid var(--border);
      background:rgba(255,255,255,.9);
      border-radius:999px;
      padding:8px 12px;
      font-size:12px;
      cursor:pointer;
      box-shadow:var(--shadow2);
    }}
    .btn .btn-ico{{display:inline-block;margin-right:6px}}
    .btn .btn-txt{{display:inline-block}}
    @media (max-width:480px){{
      .btn{{padding:8px 10px}}
      .btn .btn-ico{{margin-right:0}}
      .btn .btn-txt{{display:none}}
    }}
    .summary{{display:grid;grid-template-columns:1.3fr 1fr;gap:14px;align-items:stretch;margin-bottom:18px}}
    @media (max-width:900px){{.summary{{grid-template-columns:1fr}}}}
    .panel{{
      background:var(--card);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
      border:1px solid var(--border);
      border-radius:var(--r);
      box-shadow:var(--shadow);
      padding:16px;
    }}
    .dot{{width:12px;height:12px;border-radius:50%}}
    .dot.red{{background:var(--red);box-shadow:0 0 0 6px rgba(255,59,48,.14)}}
    .dot.yellow{{background:var(--yellow);box-shadow:0 0 0 6px rgba(255,204,0,.14)}}
    .dot.green{{background:var(--green);box-shadow:0 0 0 6px rgba(52,199,89,.14)}}
    .hero-title{{font-weight:900;font-size:22px;letter-spacing:-.02em;line-height:1.2}}
    .hero-sub{{color:var(--muted);font-size:12px;margin-top:6px}}
    .eol-banner{{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:12px;
      margin-top:12px;
      padding:12px 14px;
      border-radius:var(--r);
      border:1px solid rgba(255,59,48,.28);
      border-left:5px solid var(--red);
      background:rgba(255,59,48,.08);
    }}
    .eol-left{{display:flex;align-items:flex-start;gap:10px}}
    .eol-ico{{font-size:18px;line-height:1}}
    .eol-title{{font-weight:900}}
    .eol-sub{{color:var(--muted);font-size:12px;margin-top:2px}}
    .eol-link{{
      border:1px solid rgba(255,59,48,.25);
      background:rgba(255,255,255,.8);
      border-radius:999px;
      padding:8px 12px;
      font-size:12px;
      font-weight:800;
      text-decoration:none;
      color:#7a1a14;
      white-space:nowrap;
    }}
    .kpis{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}}
    @media (max-width:520px){{.kpis{{grid-template-columns:repeat(2,1fr)}}}}
    .kpi{{background:rgba(255,255,255,.7);border:1px solid var(--border);border-radius:14px;padding:10px 12px}}
    .kpi .k{{color:var(--muted);font-size:12px}}
    .kpi .v{{font-size:20px;font-weight:800;letter-spacing:-.02em}}
    .cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(360px,1fr));gap:14px}}
    .card{{
      background:var(--card);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
      border:1px solid var(--border);
      border-radius:var(--r);
      padding:16px;
      box-shadow:var(--shadow);
    }}
    .card-head{{display:flex;justify-content:space-between;gap:12px;align-items:flex-start;margin-bottom:10px}}
    .card-title{{font-weight:800;color:#0b2540;word-break:break-all}}
    .card-meta{{color:var(--muted);font-size:12px;word-break:break-all}}
    .label{{font-weight:800;margin:14px 0 8px 0}}
    .section{{margin-top:8px}}
    .err{{color:#b42318;background:rgba(255,59,48,.08);border:1px solid rgba(255,59,48,.18);padding:10px 12px;border-radius:14px;font-size:12px;font-weight:700;word-break:break-all}}
    .ok{{color:#1f7a3d;font-weight:800}}
    .muted{{color:var(--muted)}}
    ul.vuln{{margin:0;padding-left:18px}}
    ul.vuln li{{margin:10px 0}}
    .row{{display:flex;align-items:center;gap:8px;flex-wrap:wrap}}
    .sev{{display:inline-flex;align-items:center;justify-content:center;min-width:64px;padding:2px 10px;border-radius:999px;font-size:12px;color:#fff;font-weight:800}}
    .sev-critical{{background:var(--red)}}
    .sev-high{{background:#ff9500}}
    .sev-medium{{background:var(--blue)}}
    .sev-low{{background:var(--green)}}
    .sev-info{{background:#64748b}}
    .sev-unknown{{background:#8e8e93}}
    .type{{font-weight:800}}
    .details{{font-size:12px;color:var(--muted);margin-top:4px;word-break:break-word}}
    .cves{{font-size:12px;color:#111827;margin-top:4px;word-break:break-word}}
    .svc{{display:flex;gap:12px;justify-content:space-between;align-items:flex-start;padding:12px 12px;border:1px solid var(--border);border-radius:16px;background:rgba(255,255,255,.65);margin:12px 0 10px 0}}
    .svc-title{{font-weight:900}}
    .svc-meta{{font-size:12px;color:var(--muted);word-break:break-all}}
    .svc-sub{{font-size:12px;color:var(--muted);margin-top:2px}}
    .svc-right{{text-align:right;min-width:160px}}
    .svc-k{{font-size:12px;color:var(--muted)}}
    .svc-v{{font-size:14px;font-weight:900}}
    .svc-right{{text-align:right;min-width:160px}}
    .hits{{margin-top:8px;border-left:3px solid rgba(107,114,128,.25);padding-left:10px}}
    .hit{{font-size:12px;color:#111827;margin:3px 0}}
    .hit .path{{display:inline-block;min-width:110px;color:#0a66c2}}
    .hit .kw{{color:var(--muted)}}
    .reco li{{margin:8px 0}}
    .fgrid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:14px}}
    .fcard{{position:relative}}
    .fcard.f-sev-critical{{background:rgba(255,59,48,.08);border-color:rgba(255,59,48,.22)}}
    .fcard.f-sev-high{{background:rgba(255,149,0,.08);border-color:rgba(255,149,0,.18)}}
    .fmeta{{color:var(--muted);font-size:12px;margin-top:6px;word-break:break-all}}
    .fbody{{margin-top:10px}}
    .freco{{margin-top:10px;font-size:12px;font-weight:800}}
    .freco .rk{{color:var(--muted);font-weight:700}}
    .defender-line{{margin-top:8px;font-size:12px;color:#111827;display:flex;gap:8px;align-items:center;flex-wrap:wrap}}
    .browser-line{{margin-top:8px;font-size:12px;color:#111827;display:flex;gap:8px;align-items:center;flex-wrap:wrap}}
    .pulse-dot{{
      position:absolute;
      top:12px;
      right:12px;
      width:10px;
      height:10px;
      border-radius:50%;
      background:var(--red);
      box-shadow:0 0 0 6px rgba(255,59,48,.14);
      animation:pulse 1.2s infinite;
    }}
    @keyframes pulse {{
      0% {{ transform:scale(1); opacity:1; }}
      70% {{ transform:scale(1.6); opacity:.25; }}
      100% {{ transform:scale(1); opacity:1; }}
    }}
    details.tech summary{{cursor:pointer;list-style:none;font-weight:900}}
    details.tech summary::-webkit-details-marker{{display:none}}
    pre.tech{{margin:10px 0 0 0;padding:12px;border-radius:14px;border:1px solid var(--border);background:rgba(255,255,255,.7);overflow:auto;font-size:12px;line-height:1.45}}
    .footer{{margin:18px 0 10px 0;color:var(--muted);font-size:12px;text-align:center}}
    body.mode-simple #techDetails{{display:none}}
    body.mode-simple .fcard[data-sev="medium"],body.mode-simple .fcard[data-sev="low"],body.mode-simple .fcard[data-sev="info"],body.mode-simple .fcard[data-sev="unknown"]{{display:none}}
    body.mode-simple .details{{display:none}}
    body.mode-simple .browser-line,body.mode-simple .defender-line{{display:none}}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="topbar">
      <div class="title">
        <h1 data-k="title"></h1>
        <div class="sub" id="scanTime"></div>
        <div class="sub" id="reportKind"></div>
      </div>
      <div class="actions">
        <button class="btn" id="langBtn"><span class="btn-ico">🌐</span><span class="btn-txt"></span></button>
        <button class="btn" id="modeBtn"><span class="btn-ico">🔍</span><span class="btn-txt"></span></button>
      </div>
    </div>

    <div class="summary">
      <div class="panel">
        <div class="hero-title" id="heroTitle"></div>
        <div class="hero-sub" id="heroSub"></div>
        <div id="eolBanner"></div>
      </div>
      <div class="panel">
        <div class="label" data-k="overall_counts"></div>
        <div class="kpis" id="kpiRow"></div>
      </div>
    </div>

    <div class="panel" style="margin-bottom:14px">
      <div class="label" data-k="next_steps"></div>
      <ul class="reco" id="recoList"></ul>
    </div>

    <div class="fgrid" id="findingGrid"></div>

    <details class="panel tech" id="techDetails" style="margin-top:14px">
      <summary data-k="tech_details"></summary>
      <pre class="tech" id="techJson"></pre>
    </details>

    <div class="footer" id="footerText"></div>
  </div>

  <script>
    const DEFAULT_LANG = "{lang}";
    const HEALTH = "{health}";
    const COUNTS = {counts_json};
    const RECO = {reco_json};
    const SCAN_TIME = "{_h(scan_time)}";
    const REPORT = {report_json};
    const REPORT_KIND = "{_h(report_kind)}";
    const I18N = {{
      zh: {{
        title: "OpenClaw 扫描报告",
        overall_counts: "总体统计",
        next_steps: "下一步建议",
        tech_details: "技术详情",
        run: "运行",
        targets: "目标",
        services: "服务",
        open_ports: "开放端口",
        sev_critical: "严重",
        sev_high: "高",
        sev_medium: "中",
        sev_low: "低",
        sev_info: "信息",
        sev_unknown: "未知",
        scan_time: "扫描时间",
        lang_btn: "English",
        mode_show_details: "查看详情",
        mode_simple_view: "简洁视图",
        reco_label: "建议",
        footer: "由 OpenClaw PC Security 生成 · 报告仅供参考，请勿上传至公开平台",
        hero_red: "你的电脑有 {{n}} 个问题需要处理",
        hero_yellow: "你的电脑有 {{n}} 个问题建议关注",
        hero_green: "你的电脑目前状态良好",
        hero_meta: "目标 {{t}} · 服务 {{s}} · 开放端口 {{p}}",
        eol_title: "Windows 已停止支持",
        eol_sub: "EOL 日期：{{d}}",
        eol_btn: "了解 ESU 方案",
        defender_line: "🛡️ Defender：{{s}} · 病毒库：{{d}}",
        min_required: "最低要求",
        report_kind_label: "对象",
        report_kind_pc: "PC/内网目标",
        report_kind_server: "服务器/公网目标",
        type_map: {{
          defender_status: "防病毒保护状态",
          browser_outdated: "浏览器版本过旧",
          browser_info: "浏览器版本信息",
          server_config_not_found: "服务器配置文件未找到",
          server_auth_disabled: "未开启访问保护",
          server_auth_enabled: "已开启访问保护",
          server_default_port: "使用默认端口",
          server_custom_port: "使用自定义端口",
          server_exposed_public: "对外网络暴露",
          server_local_only: "仅本机可访问",
          windows_support_status: "Windows 支持状态",
          openclaw_outdated: "OpenClaw 版本落后",
          openclaw_version_mismatch: "OpenClaw 版本不一致",
          windows_patch_lag: "Windows 补丁滞后",
          windows_last_security_update: "最近安全更新",
          weak_credentials: "默认/弱口令风险"
        }}
      }},
      en: {{
        title: "OpenClaw Scan Report",
        overall_counts: "Overall counts",
        next_steps: "Next steps",
        tech_details: "Technical details",
        run: "Run",
        targets: "Targets",
        services: "Services",
        open_ports: "Open ports",
        sev_critical: "Critical",
        sev_high: "High",
        sev_medium: "Medium",
        sev_low: "Low",
        sev_info: "Info",
        sev_unknown: "Unknown",
        scan_time: "Scan time",
        lang_btn: "中文",
        mode_show_details: "Show Details",
        mode_simple_view: "Simple View",
        reco_label: "Recommendation",
        footer: "Generated by OpenClaw PC Security · For reference only. Do not upload publicly.",
        hero_red: "You have {{n}} issues to fix",
        hero_yellow: "You have {{n}} issues to review",
        hero_green: "Your system looks healthy",
        hero_meta: "Target {{t}} · Service {{s}} · Open ports {{p}}",
        eol_title: "Windows is out of support",
        eol_sub: "EOL date: {{d}}",
        eol_btn: "Learn about ESU",
        defender_line: "🛡️ Defender: {{s}} · Signatures: {{d}}",
        min_required: "Minimum",
        report_kind_label: "Scope",
        report_kind_pc: "PC/Internal target",
        report_kind_server: "Server/Public target",
        type_map: {{
          defender_status: "Antivirus Protection",
          browser_outdated: "Browser Out of Date",
          browser_info: "Browser Version",
          server_config_not_found: "Server Config Not Found",
          server_auth_disabled: "Password Protection Off",
          server_auth_enabled: "Password Protection On",
          server_default_port: "Default Port In Use",
          server_custom_port: "Custom Port In Use",
          server_exposed_public: "Publicly Exposed",
          server_local_only: "Local Access Only",
          windows_support_status: "Windows Support Status",
          openclaw_outdated: "OpenClaw Outdated",
          openclaw_version_mismatch: "OpenClaw Version Mismatch",
          windows_patch_lag: "Windows Patch Lag",
          windows_last_security_update: "Last Security Update",
          weak_credentials: "Weak/Default Credentials"
        }}
      }}
    }};

    let lang = DEFAULT_LANG;
    let mode = "simple";

    function t(key) {{
      const v = (I18N[lang] || {{}})[key];
      return typeof v === "string" ? v : "";
    }}

    function fmt(template, vars) {{
      return String(template || "").replace(/\{{(\w+)\}}/g, (_, k) => (vars && vars[k] != null ? String(vars[k]) : ""));
    }}

    function esc(s) {{
      return String(s || "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
    }}

    function sevLabel(s) {{
      const k = "sev_" + (["critical","high","medium","low","info","unknown"].includes(s) ? s : "unknown");
      return t(k) || s;
    }}

    function typeLabel(type) {{
      const m = (I18N[lang] || {{}}).type_map || {{}};
      return m[type] || type || "";
    }}

    function recoText(type) {{
      const key = type === "openclaw_version_mismatch" ? "openclaw_outdated" : type;
      const r = (RECO || []).find(x => x && x.k === key);
      if (!r) return "";
      return (lang === "zh" ? r.zh : r.en) || "";
    }}

    function healthTitle() {{
      const c = Number(COUNTS.critical || 0);
      const h = Number(COUNTS.high || 0);
      const m = Number(COUNTS.medium || 0);
      if (HEALTH === "red") return fmt(t("hero_red"), {{ n: c + h }});
      if (HEALTH === "yellow") return fmt(t("hero_yellow"), {{ n: m }});
      return t("hero_green");
    }}

    function flattenFindings() {{
      const out = [];
      const la = REPORT && REPORT.local_audit ? REPORT.local_audit : null;
      if (la && Array.isArray(la.findings)) {{
        for (const f of la.findings) {{
          out.push({{
            source: "local",
            type: (f && f.type) || "",
            severity: String((f && f.severity) || "unknown").toLowerCase(),
            details: (f && f.details) || "",
            cves: f && f.cves ? f.cves : null,
            target: "local",
            service: "local",
            ports: ""
          }});
        }}
      }}
      const rs = REPORT && Array.isArray(REPORT.results) ? REPORT.results : [];
      for (const r of rs) {{
        const tgt = (r && r.target) || "";
        const openPorts = Array.isArray(r && r.open_ports) ? r.open_ports.join(",") : "";
        const fs = r && Array.isArray(r.findings) ? r.findings : [];
        for (const f of fs) {{
          const svc = (f && f.service) || "";
          const vlist = f && Array.isArray(f.vulnerabilities) ? f.vulnerabilities : [];
          for (const v of vlist) {{
            out.push({{
              source: "remote",
              type: (v && v.type) || "",
              severity: String((v && v.severity) || "unknown").toLowerCase(),
              details: (v && v.details) || "",
              cves: v && v.cves ? v.cves : null,
              hits: v && v.hits ? v.hits : null,
              target: tgt,
              service: svc,
              ports: openPorts
            }});
          }}
        }}
      }}
      const rank = {{ critical: 50, high: 40, medium: 30, low: 20, info: 10, unknown: 0 }};
      out.sort((a, b) => (rank[b.severity] || 0) - (rank[a.severity] || 0));
      return out;
    }}

    function findEolDate(findings) {{
      for (const f of findings) {{
        if (f.type === "windows_support_status" && (f.severity === "high" || f.severity === "critical")) {{
          const m = String(f.details || "").match(/EOL\\s*(\\d{{4}}-\\d{{2}}-\\d{{2}})/i);
          if (m) return m[1];
          return "";
        }}
      }}
      return null;
    }}

    function renderEolBanner(findings) {{
      const host = document.getElementById("eolBanner");
      host.innerHTML = "";
      const d = findEolDate(findings);
      if (!d) return;
      const el = document.createElement("div");
      el.className = "eol-banner";
      const left = document.createElement("div");
      left.className = "eol-left";
      const ico = document.createElement("div");
      ico.className = "eol-ico";
      ico.textContent = "⚠️";
      const txt = document.createElement("div");
      const title = document.createElement("div");
      title.className = "eol-title";
      title.textContent = t("eol_title");
      const sub = document.createElement("div");
      sub.className = "eol-sub";
      sub.textContent = fmt(t("eol_sub"), {{ d }});
      txt.appendChild(title);
      txt.appendChild(sub);
      left.appendChild(ico);
      left.appendChild(txt);
      const link = document.createElement("a");
      link.className = "eol-link";
      link.href = "https://learn.microsoft.com/zh-cn/lifecycle/faq/windows";
      link.target = "_blank";
      link.rel = "noreferrer";
      link.textContent = t("eol_btn");
      el.appendChild(left);
      el.appendChild(link);
      host.appendChild(el);
    }}

    function renderKPIs() {{
      const host = document.getElementById("kpiRow");
      host.innerHTML = "";
      const items = mode === "simple"
        ? [["critical", COUNTS.critical || 0], ["high", COUNTS.high || 0]]
        : [["critical", COUNTS.critical || 0], ["high", COUNTS.high || 0], ["medium", COUNTS.medium || 0], ["low", COUNTS.low || 0], ["info", COUNTS.info || 0], ["unknown", COUNTS.unknown || 0]];
      for (const [k, v] of items) {{
        const div = document.createElement("div");
        div.className = "kpi";
        const kk = document.createElement("div");
        kk.className = "k";
        kk.textContent = sevLabel(k);
        const vv = document.createElement("div");
        vv.className = "v";
        vv.textContent = String(Number(v));
        div.appendChild(kk);
        div.appendChild(vv);
        host.appendChild(div);
      }}
    }}

    function renderRecoList() {{
      const recoList = document.getElementById("recoList");
      recoList.innerHTML = "";
      for (const r of (RECO || [])) {{
        const li = document.createElement("li");
        li.textContent = (lang === "zh" ? r.zh : r.en) || "";
        recoList.appendChild(li);
      }}
    }}

    function renderTech() {{
      const pre = document.getElementById("techJson");
      pre.textContent = JSON.stringify(REPORT, null, 2);
    }}

    function renderFindings(findings) {{
      const host = document.getElementById("findingGrid");
      host.innerHTML = "";
      const laRaw = REPORT && REPORT.local_audit ? (REPORT.local_audit.raw || {{}}) : {{}};
      const defender = laRaw && typeof laRaw === "object" ? laRaw.defender : null;

      for (const f of findings) {{
        const card = document.createElement("div");
        card.className = "card fcard f-sev-" + esc(f.severity);
        card.setAttribute("data-sev", f.severity);
        card.setAttribute("data-type", f.type);

        const showPulse = f.type === "defender_status" && (f.severity === "high" || f.severity === "critical");
        if (showPulse) {{
          const pd = document.createElement("div");
          pd.className = "pulse-dot";
          card.appendChild(pd);
        }}

        const meta = f.source === "remote"
          ? fmt(t("hero_meta"), {{ t: f.target || "-", s: f.service || "-", p: f.ports || "-" }})
          : "";

        let detailText = String(f.details || "");
        const reco = recoText(f.type);
        
        const row = document.createElement("div");
        row.className = "row";
        const sev = document.createElement("span");
        sev.className = "sev sev-" + esc(f.severity);
        sev.setAttribute("data-sev", f.severity);
        sev.textContent = sevLabel(f.severity);
        const typ = document.createElement("span");
        typ.className = "type";
        typ.textContent = typeLabel(f.type);
        row.appendChild(sev);
        row.appendChild(typ);
        card.appendChild(row);

        if (meta) {{
          const m = document.createElement("div");
          m.className = "fmeta";
          m.textContent = meta;
          card.appendChild(m);
        }}

        const body = document.createElement("div");
        body.className = "fbody";

        if (detailText) {{
          const det = document.createElement("div");
          det.className = "details";
          det.textContent = detailText;
          body.appendChild(det);
        }}

        if (f.type === "browser_outdated") {{
          const mm = detailText.match(/^(Chrome|Edge|Firefox)\\s+version\\s+([0-9.]+).*?(?:minimum|min|>=)\\s*(?:secure\\s*)?(?:version\\s*)?([0-9.]+)/i);
          const name = mm ? mm[1] : "";
          const cur = mm ? mm[2] : "";
          const min = mm ? mm[3] : "";
          const icon = name.toLowerCase() === "chrome" ? "🌐" : (name.toLowerCase() === "edge" ? "🔷" : (name.toLowerCase() === "firefox" ? "🦊" : "🌐"));
          const bl = document.createElement("div");
          bl.className = "browser-line";
          bl.textContent = icon + " " + name + " " + cur + " → " + t("min_required") + " " + min;
          body.appendChild(bl);
        }}

        if (f.type === "defender_status" && defender) {{
          const enabled = defender.enabled === true ? (lang === "zh" ? "已开启" : "Enabled") : (lang === "zh" ? "已关闭" : "Disabled");
          const sig = defender.signature_last_updated ? String(defender.signature_last_updated) : (lang === "zh" ? "未知" : "Unknown");
          const dl = document.createElement("div");
          dl.className = "defender-line";
          dl.textContent = fmt(t("defender_line"), {{ s: enabled, d: sig }});
          body.appendChild(dl);
        }}

        if (reco) {{
          const rr = document.createElement("div");
          rr.className = "freco";
          const rk = document.createElement("span");
          rk.className = "rk";
          rk.textContent = t("reco_label") + ": ";
          rr.appendChild(rk);
          const rt = document.createElement("span");
          rt.textContent = reco;
          rr.appendChild(rt);
          body.appendChild(rr);
        }}

        card.appendChild(body);

        host.appendChild(card);
      }}
    }}

    function applyLangAndMode() {{
      document.querySelectorAll("[data-k]").forEach(el => {{
        const k = el.getAttribute("data-k");
        const v = (I18N[lang] || {{}})[k];
        if (typeof v === "string") el.textContent = v;
      }});

      document.getElementById("scanTime").textContent = t("scan_time") + ": " + SCAN_TIME;
      const rk = document.getElementById("reportKind");
      if (rk) rk.textContent = t("report_kind_label") + ": " + (REPORT_KIND === "pc" ? t("report_kind_pc") : t("report_kind_server"));

      const langBtnTxt = document.querySelector("#langBtn .btn-txt");
      if (langBtnTxt) langBtnTxt.textContent = t("lang_btn");

      const modeBtnTxt = document.querySelector("#modeBtn .btn-txt");
      if (modeBtnTxt) modeBtnTxt.textContent = (mode === "simple" ? t("mode_show_details") : t("mode_simple_view"));

      document.getElementById("heroTitle").textContent = healthTitle();
      document.getElementById("heroSub").textContent = t("run") + ": {_h(run_id)} · " + t("targets") + ": {total_targets} · " + t("services") + ": {total_services} · " + t("open_ports") + ": {total_open_ports}";

      document.body.classList.toggle("mode-simple", mode === "simple");

      const findings = flattenFindings();
      renderEolBanner(findings);
      renderKPIs();
      renderRecoList();
      renderFindings(findings);
      renderTech();

      const ft = document.getElementById("footerText");
      ft.textContent = t("footer");
    }}

    document.getElementById("langBtn").addEventListener("click", () => {{
      lang = (lang === "zh" ? "en" : "zh");
      applyLangAndMode();
    }});

    document.getElementById("modeBtn").addEventListener("click", () => {{
      mode = (mode === "simple" ? "detail" : "simple");
      applyLangAndMode();
    }});

    applyLangAndMode();
  </script>
</body>
</html>"""
            html_path.write_text(html, encoding="utf-8")
            print(f"[+] HTML report saved to {html_path.as_posix()}")
        except Exception as e:
            print(f"[-] Failed to save HTML report: {e}")

    exit_code = 0
    if severities["critical"] > 0 or severities["high"] > 0:
        exit_code = 1
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
