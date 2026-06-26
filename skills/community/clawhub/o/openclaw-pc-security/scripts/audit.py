import subprocess
import sys
import platform
import shutil
import re
import json
import os
import datetime
from pathlib import Path
import kbmap

# --- Constants for F3 (Browser Versions) ---
MIN_SECURE_VERSIONS = {
    "Chrome": "130.0",
    "Edge": "130.0",
    "Firefox": "128.0"
}

# --- Constants for F4 (Windows Lifecycle) ---
# Format: EOL Date, Base Severity
WINDOWS_LIFECYCLE = {
    "Windows 7": {"eol": datetime.date(2020, 1, 14), "base_sev": "Critical"},
    "Windows 8.1": {"eol": datetime.date(2023, 1, 10), "base_sev": "Critical"},
    "Windows 10": {"eol": datetime.date(2025, 10, 14), "base_sev": "High"},
    "Windows 11 22H2": {"eol": datetime.date(2024, 10, 8), "base_sev": "High"},
    "Windows 11 23H2": {"eol": datetime.date(2025, 11, 11), "base_sev": "Medium"},
    "Windows 11 24H2": {"eol": None, "base_sev": "Info"}, # Supported
}

def _sev_rank(x):
    s = (x or "").strip().lower()
    if s == "critical": return 50
    if s == "high": return 40
    if s == "medium": return 30
    if s == "low": return 20
    if s == "info": return 10
    return 0

def _parse_version_nums(v):
    if not v or not isinstance(v, str): return None
    s = v.strip()
    if not s: return None
    s = s.lstrip("vV")
    parts = s.split(".")
    nums = []
    for p in parts:
        if not p.isdigit(): return None
        nums.append(int(p))
    return tuple(nums) if nums else None

def _cmp_versions(a, b):
    va = _parse_version_nums(a)
    vb = _parse_version_nums(b)
    if va is None or vb is None: return None
    n = max(len(va), len(vb))
    va = va + (0,) * (n - len(va))
    vb = vb + (0,) * (n - len(vb))
    if va < vb: return -1
    if va > vb: return 1
    return 0

def run_cmd(cmd, shell=False):
    """Run a command and return stdout. Returns None if command fails."""
    try:
        if shell and sys.platform == "win32":
            cmd = ["powershell", "-Command", cmd] if isinstance(cmd, str) else cmd
            
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            encoding='utf-8', 
            errors='ignore',
            shell=shell if sys.platform != "win32" else False
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None

def get_defender_status():
    """F2: Get Windows Defender status."""
    if sys.platform != "win32":
        return None

    status = {
        "enabled": False,
        "signature_last_updated": None,
        "third_party_av": None
    }

    # 1. Check Defender Status
    try:
        out = run_cmd("Get-MpComputerStatus | Select-Object AntivirusEnabled,AntivirusSignatureLastUpdated | ConvertTo-Json -Compress", shell=True)
        if out:
            d = json.loads(out)
            if isinstance(d, dict):
                status["enabled"] = bool(d.get("AntivirusEnabled"))
                sl = d.get("AntivirusSignatureLastUpdated")
                if sl:
                    # PowerShell JSON date format: /Date(167...)/
                    m = re.search(r"\/Date\((\d+)\)\/", str(sl))
                    if m:
                        ts = int(m.group(1)) / 1000
                        status["signature_last_updated"] = datetime.datetime.fromtimestamp(ts).date().isoformat()
                    else:
                         # Try ISO format if present
                         try:
                             status["signature_last_updated"] = datetime.datetime.fromisoformat(str(sl).replace("Z", "+00:00")).date().isoformat()
                         except:
                             pass
    except Exception:
        pass

    # 2. Check Third Party AV
    try:
        out = run_cmd("Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntivirusProduct | Select-Object displayName | ConvertTo-Json -Compress", shell=True)
        if out:
            # Could be a list or dict
            d = json.loads(out)
            if isinstance(d, list):
                names = [x.get("displayName") for x in d if isinstance(x, dict) and x.get("displayName")]
                status["third_party_av"] = ", ".join([n for n in names if "Windows Defender" not in n])
            elif isinstance(d, dict):
                n = d.get("displayName")
                if n and "Windows Defender" not in n:
                    status["third_party_av"] = n
    except Exception:
        pass
        
    return status

def get_browser_versions():
    """F3: Get installed browser versions."""
    if sys.platform != "win32":
        return {}
        
    versions = {}
    
    # Chrome
    try:
        out = run_cmd(r'(Get-ItemProperty "HKLM:\SOFTWARE\Google\Chrome\BLBeacon" -ErrorAction SilentlyContinue).version', shell=True)
        if out: versions["Chrome"] = out.strip()
    except: pass
    
    # Edge
    try:
        # Edge GUID is tricky, usually under Clients. Iterate.
        # HKLM\SOFTWARE\Microsoft\EdgeUpdate\Clients\{guid} -> pv
        # Powershell: Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\EdgeUpdate\Clients\*' | Select-Object pv | Where-Object {$_.pv}
        # But there might be multiple clients (WebView2 etc). We want the browser.
        # Usually Microsoft Edge is {56EB18F8-B008-4CBD-B6D2-8C97FE7E9062} but might vary.
        # Let's try simple registry query for the well-known key if possible, or fallback to file.
        # Simpler: (Get-Item "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe").VersionInfo.ProductVersion
        out = run_cmd(r'(Get-Item "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" -ErrorAction SilentlyContinue).VersionInfo.ProductVersion', shell=True)
        if out: versions["Edge"] = out.strip()
    except: pass

    # Firefox
    try:
        # Read application.ini
        # Default path: C:\Program Files\Mozilla Firefox\application.ini
        # or C:\Program Files (x86)\...
        paths = [
            r"C:\Program Files\Mozilla Firefox\application.ini",
            r"C:\Program Files (x86)\Mozilla Firefox\application.ini"
        ]
        for p in paths:
            pp = Path(p)
            if pp.exists():
                content = pp.read_text(encoding="utf-8", errors="ignore")
                m = re.search(r"^Version=(.+)$", content, re.MULTILINE)
                if m:
                    versions["Firefox"] = m.group(1).strip()
                    break
    except: pass
    
    return versions

def _coerce_truthy(v):
    if v is None:
        return False
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return v != 0
    s = str(v).strip().lower()
    if s in ("", "0", "false", "no", "off", "null", "none"):
        return False
    if s in ("1", "true", "yes", "on"):
        return True
    return True

def _find_first_key_value(obj, keys_lower):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if str(k).strip().lower() in keys_lower:
                return v
        for v in obj.values():
            got = _find_first_key_value(v, keys_lower)
            if got is not None:
                return got
    elif isinstance(obj, list):
        for v in obj:
            got = _find_first_key_value(v, keys_lower)
            if got is not None:
                return got
    return None

def _net_listening_addrs(port):
    p = int(port)
    addrs = []

    def _add(a):
        aa = (a or "").strip()
        if not aa:
            return
        if aa.startswith("[") and aa.endswith("]"):
            aa = aa[1:-1]
        addrs.append(aa)

    try:
        if sys.platform == "win32":
            out = run_cmd(["netstat", "-ano"])
            if out:
                for line in out.splitlines():
                    if "LISTEN" not in line.upper():
                        continue
                    m = re.search(r"\s+TCP\s+(\S+):(\d+)\s+\S+\s+LISTEN", line, re.IGNORECASE)
                    if m and int(m.group(2)) == p:
                        _add(m.group(1))
        else:
            if shutil.which("netstat"):
                out = run_cmd(["netstat", "-an"])
                if out:
                    for line in out.splitlines():
                        if "LISTEN" not in line.upper():
                            continue
                        m = re.search(r"\s+tcp\S*\s+\S+\s+\S+\s+(\S+):(\d+)\s+\S+\s+LISTEN", line, re.IGNORECASE)
                        if m and int(m.group(2)) == p:
                            _add(m.group(1))
            elif shutil.which("ss"):
                out = run_cmd(["ss", "-lnt"])
                if out:
                    for line in out.splitlines():
                        if "LISTEN" not in line.upper():
                            continue
                        m = re.search(r"\s+LISTEN\s+\S+\s+\S+\s+(\S+):(\d+)\s+", line, re.IGNORECASE)
                        if m and int(m.group(2)) == p:
                            _add(m.group(1))
    except Exception:
        return []

    uniq = []
    seen = set()
    for a in addrs:
        if a not in seen:
            seen.add(a)
            uniq.append(a)
    return uniq

def get_server_config_status(server_config_path=None):
    cfg = None
    cfg_path = None

    def _try_load(p):
        nonlocal cfg, cfg_path
        try:
            pp = Path(p)
            if not pp.exists() or not pp.is_file():
                return False
            txt = pp.read_text(encoding="utf-8", errors="ignore").strip()
            if not txt:
                return False
            cfg = json.loads(txt)
            cfg_path = pp
            return isinstance(cfg, dict)
        except Exception:
            return False

    if server_config_path:
        _try_load(server_config_path)

    if cfg is None:
        candidates = []
        candidates.append(Path.cwd() / "config.json")
        candidates.append(Path.home() / ".openclaw" / "config.json")
        appdata = os.environ.get("APPDATA") if sys.platform == "win32" else None
        if appdata:
            candidates.append(Path(appdata) / "openclaw" / "config.json")

        for p in candidates:
            if _try_load(p):
                break

    findings = []

    if cfg is None:
        findings.append({
            "type": "server_config_not_found",
            "details": "OpenClaw config file was not found on this machine (it may be installed elsewhere or use a different path).",
            "severity": "Info",
        })

        addrs = _net_listening_addrs(18789)
        if addrs:
            findings.append({
                "type": "server_default_port",
                "details": "OpenClaw is listening on the default port 18789, which is easier to find by automated scans.",
                "severity": "High",
            })
            if any(a in ("0.0.0.0", "::") for a in addrs):
                findings.append({
                    "type": "server_exposed_public",
                    "details": "OpenClaw is listening on all network adapters, so other machines may be able to reach it unless you restrict access.",
                    "severity": "High",
                })
            elif any(a in ("127.0.0.1", "::1") for a in addrs):
                findings.append({
                    "type": "server_local_only",
                    "details": "OpenClaw appears to be bound to local-only address (local access only).",
                    "severity": "Info",
                })

        return findings

    auth_val = _find_first_key_value(cfg, {"auth", "auth_required", "authentication"})
    auth_on = _coerce_truthy(auth_val)
    if auth_on:
        findings.append({
            "type": "server_auth_enabled",
            "details": f"Password protection is enabled. (config: {cfg_path.as_posix() if cfg_path else 'config.json'})",
            "severity": "Info",
        })
    else:
        findings.append({
            "type": "server_auth_disabled",
            "details": f"Password protection is not enabled, so anyone who can reach the service may be able to access it. (config: {cfg_path.as_posix() if cfg_path else 'config.json'})",
            "severity": "Critical",
        })

    port_val = _find_first_key_value(cfg, {"port"})
    port_num = None
    try:
        port_num = int(str(port_val).strip()) if port_val is not None and str(port_val).strip() != "" else 18789
    except Exception:
        port_num = 18789

    if port_num == 18789:
        findings.append({
            "type": "server_default_port",
            "details": "OpenClaw uses the default port 18789, which is easier to guess by automated scans.",
            "severity": "High",
        })
    else:
        findings.append({
            "type": "server_custom_port",
            "details": f"OpenClaw uses a custom port {port_num}.",
            "severity": "Info",
        })

    addr_val = _find_first_key_value(cfg, {"listen", "listen_address", "bind", "bind_address", "host", "address"})
    addr_s = str(addr_val).strip() if addr_val is not None else ""

    addrs = _net_listening_addrs(port_num)
    if addr_s:
        if addr_s in ("0.0.0.0", "::"):
            findings.append({
                "type": "server_exposed_public",
                "details": "OpenClaw is configured to listen on all network adapters, so it may be reachable from other machines unless you restrict access.",
                "severity": "High",
            })
        elif addr_s in ("127.0.0.1", "localhost", "::1"):
            findings.append({
                "type": "server_local_only",
                "details": "OpenClaw is configured for local access only.",
                "severity": "Info",
            })
    elif addrs:
        if any(a in ("0.0.0.0", "::") for a in addrs):
            findings.append({
                "type": "server_exposed_public",
                "details": "OpenClaw is listening on all network adapters, so other machines may be able to reach it unless you restrict access.",
                "severity": "High",
            })
        elif any(a in ("127.0.0.1", "::1") for a in addrs):
            findings.append({
                "type": "server_local_only",
                "details": "OpenClaw appears to be bound to local-only address (local access only).",
                "severity": "Info",
            })

    return findings

def get_os_info():
    """Get basic OS information."""
    info = {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "patches": [],
        "patches_detailed": [],
        "windows_version": None,
        "windows_display_version": None,
        "windows_product_name": None,
        "windows_build": None,
        "latest_patch": None,
    }
    
    if info["system"] == "Windows":
        reg_json = run_cmd(
            r"Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion' | "
            r"Select-Object ProductName,DisplayVersion,ReleaseId,CurrentBuildNumber,UBR | ConvertTo-Json -Compress",
            shell=True,
        )
        if reg_json:
            try:
                d = json.loads(reg_json)
                if isinstance(d, dict):
                    info["windows_product_name"] = d.get("ProductName") or None
                    info["windows_display_version"] = d.get("DisplayVersion") or d.get("ReleaseId") or None
                    b = d.get("CurrentBuildNumber")
                    ubr = d.get("UBR")
                    if b:
                        info["windows_build"] = f"{b}.{ubr}" if ubr is not None else str(b)
            except Exception:
                pass

        wv = run_cmd("(Get-ComputerInfo).WindowsVersion", shell=True)
        if wv:
            info["windows_version"] = wv.strip()

        # Get installed hotfixes
        out = run_cmd("wmic qfe list brief /format:csv")
        if out:
            lines = out.splitlines()
            if len(lines) > 1:
                headers = lines[0].split(',')
                try:
                    idx = headers.index('HotFixID')
                    idx_on = headers.index('InstalledOn') if 'InstalledOn' in headers else -1
                    for line in lines[1:]:
                        parts = line.split(',')
                        if len(parts) > idx:
                            hotfix = parts[idx].strip()
                            if hotfix:
                                info["patches"].append(hotfix)
                                installed_on = None
                                if idx_on >= 0 and len(parts) > idx_on:
                                    installed_on = parts[idx_on].strip() or None
                                info["patches_detailed"].append({"hotfix": hotfix, "installed_on": installed_on})
                except ValueError:
                    import re
                    patches = re.findall(r"(KB\d+)", out)
                    info["patches"] = sorted(list(set(patches)))
                    info["patches_detailed"] = [{"hotfix": x, "installed_on": None} for x in info["patches"]]

        def _parse_date(s):
            t = (s or "").strip()
            if not t: return None
            for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y", "%d/%m/%Y", "%Y/%m/%d"):
                try: return datetime.datetime.strptime(t, fmt).date()
                except: pass
            m = re.match(r"^\s*(\d{1,2})/(\d{1,2})/(\d{4})\s*$", t)
            if m:
                try: return datetime.date(int(m.group(3)), int(m.group(1)), int(m.group(2)))
                except: return None
            return None

        latest = None
        for p in info.get("patches_detailed") or []:
            if not isinstance(p, dict): continue
            d = _parse_date(p.get("installed_on"))
            if not d: continue
            if not latest or d > latest.get("date"):
                latest = {"hotfix": p.get("hotfix"), "date": d}
        if latest:
            info["latest_patch"] = {"hotfix": latest.get("hotfix"), "installed_on": latest["date"].isoformat()}
    
    return info

def get_node_info():
    info = {"version": None, "npm_version": None, "vulnerabilities": []}
    node_v = run_cmd(["node", "-v"])
    if node_v: info["version"] = node_v.strip()
    npm_v = run_cmd("npm -v", shell=True)
    if npm_v: info["npm_version"] = npm_v.strip()
    return info

def get_openclaw_info():
    info = {"path": None, "version_raw": None, "version": None}
    p = shutil.which("openclaw")
    if p:
        info["path"] = p
        v = None
        if sys.platform == "win32" and p.lower().endswith((".cmd", ".bat")):
            v = run_cmd("openclaw --version", shell=True)
        else:
            v = run_cmd(["openclaw", "--version"])
        if v:
            info["version_raw"] = v.strip()
            m = re.search(r"(v?\d+(?:\.\d+){1,3})", v)
            if m: info["version"] = m.group(1)
    return info

def get_openclaw_latest_version_from_npm(package="openclaw"):
    pkg = (package or "").strip()
    if not pkg: return None
    v = run_cmd(f"npm view {pkg} version", shell=True)
    if not v: return None
    s = str(v).strip()
    if not s: return None
    m = re.search(r"(v?\d+(?:\.\d+){1,3})", s)
    return m.group(1) if m else s

def audit_local_system(server_config_path=None):
    """Perform a local audit of OS and Node.js environment."""
    print("[*] Auditing local system...")
    
    os_info = get_os_info()
    print(f"[+] OS: {os_info['system']} {os_info['release']} (Patches found: {len(os_info['patches'])})")
    
    node_info = get_node_info()
    if node_info['version']:
        print(f"[+] Node.js: {node_info['version']}")
    else:
        print("[-] Node.js not found or not in PATH")

    openclaw_info = get_openclaw_info()
    if openclaw_info.get("version"):
        print(f"[+] OpenClaw CLI: {openclaw_info['version']}")
    elif openclaw_info.get("path"):
        print(f"[+] OpenClaw CLI: found ({openclaw_info['path']})")
    else:
        print("[-] OpenClaw CLI not found or not in PATH")
        
    # F2: Defender
    defender = get_defender_status()
    if defender:
        print(f"[+] Defender: Enabled={defender['enabled']}, Last Sig={defender['signature_last_updated']}")

    # F3: Browsers
    browsers = get_browser_versions()
    if browsers:
        print(f"[+] Browsers: {', '.join([f'{k} {v}' for k,v in browsers.items()])}")

    server_config = get_server_config_status(server_config_path=server_config_path)
    if server_config:
        hi = [f for f in server_config if str((f or {}).get("severity") or "").strip().lower() in ("high", "critical")]
        print(f"[+] Server config: {len(server_config)} checks ({len(hi)} high/critical)")

    return {
        "os": os_info,
        "node": node_info,
        "openclaw": openclaw_info,
        "defender": defender, # F2
        "browsers": browsers, # F3
        "server_config": server_config,
    }

def analyze_audit_data(audit_data):
    """Analyze local audit data for OS and Node.js vulnerabilities."""
    vulns = []
    
    # 1. OS Analysis
    os_info = audit_data.get("os", {})
    patches = os_info.get("patches", [])
    
    if os_info.get("system") == "Windows":
        product = os_info.get("windows_product_name") or f"Windows {os_info.get('release')}"
        dv = os_info.get("windows_display_version") or os_info.get("windows_version")
        build = os_info.get("windows_build")
        parts = [str(product).strip()]
        if dv:
            parts.append(str(dv).strip())
        if build:
            parts.append(f"build {str(build).strip()}")
        vulns.append({
            "type": "windows_version",
            "details": " ".join([p for p in parts if p]),
            "severity": "Info",
        })

        # F4: Windows EOL Logic
        eol_status = {"status": "Unknown", "severity": "Info", "details": "Support status: Unknown"}
        
        # Determine Lifecycle Entry
        lc_entry = None
        p_lower = str(product).lower()
        dv_norm = str(dv).strip().upper() if dv else ""
        
        if "windows 7" in p_lower:
            lc_entry = WINDOWS_LIFECYCLE.get("Windows 7")
        elif "windows 8.1" in p_lower:
            lc_entry = WINDOWS_LIFECYCLE.get("Windows 8.1")
        elif "windows 10" in p_lower:
            lc_entry = WINDOWS_LIFECYCLE.get("Windows 10")
        elif "windows 11" in p_lower:
            if "22H2" in dv_norm:
                lc_entry = WINDOWS_LIFECYCLE.get("Windows 11 22H2")
            elif "23H2" in dv_norm:
                lc_entry = WINDOWS_LIFECYCLE.get("Windows 11 23H2")
            elif "24H2" in dv_norm:
                lc_entry = WINDOWS_LIFECYCLE.get("Windows 11 24H2")
        
        if lc_entry:
            eol = lc_entry["eol"]
            base_sev = lc_entry["base_sev"]
            
            if eol is None:
                # Supported indefinitely (for now)
                vulns.append({
                    "type": "windows_support_status",
                    "details": f"Support status: Supported",
                    "severity": base_sev # Info
                })
            else:
                today = datetime.date.today()
                advice = ""
                if "windows 10" in p_lower:
                    advice = "ZH: 评估升 Win11 或注册 ESU。 EN: Evaluate Win11 upgrade or enroll in ESU."
                elif "windows 7" in p_lower or "windows 8.1" in p_lower:
                     advice = "ZH: 系统已停止支持，请立即升级。 EN: System EOL, upgrade immediately."
                
                if today > eol:
                    vulns.append({
                        "type": "windows_support_status",
                        "details": f"Support status: Out of support (EOL {eol}). {advice}",
                        "severity": base_sev # Critical/High
                    })
                else:
                    days_left = (eol - today).days
                    if days_left < 180:
                        # Bump severity
                        sev_map = {"Info": "Low", "Low": "Medium", "Medium": "High", "High": "Critical", "Critical": "Critical"}
                        new_sev = sev_map.get(base_sev, "High")
                        vulns.append({
                            "type": "windows_support_status",
                            "details": f"Support status: Ending soon (EOL {eol}, < 180 days). {advice}",
                            "severity": new_sev
                        })
                    else:
                        vulns.append({
                            "type": "windows_support_status",
                            "details": f"Support status: Supported (EOL {eol})",
                            "severity": "Info" # Supported -> Info as per F4 rule 4
                        })
        else:
             vulns.append({
                "type": "windows_support_status",
                "details": "Support status: Unknown (version not in lifecycle DB)",
                "severity": "Info"
            })

        # Patch Lag
        latest_patch = os_info.get("latest_patch") if isinstance(os_info, dict) else None
        last_date_s = latest_patch.get("installed_on") if isinstance(latest_patch, dict) else None
        last_kb = latest_patch.get("hotfix") if isinstance(latest_patch, dict) else None
        last_dt = None
        if last_date_s:
            try: last_dt = datetime.date.fromisoformat(str(last_date_s))
            except: last_dt = None

        if last_dt:
            label = f"{last_dt.isoformat()}" + (f" ({last_kb})" if last_kb else "")
            vulns.append({
                "type": "windows_last_security_update",
                "details": f"Last Security Update: {label}",
                "severity": "Info",
            })
            days = (datetime.date.today() - last_dt).days
            if days > 90:
                vulns.append({
                    "type": "windows_patch_lag",
                    "details": f"Patch is {days} days old (> 90 days): Update recommended",
                    "severity": "Medium",
                })
            else:
                vulns.append({
                    "type": "windows_patch_lag",
                    "details": f"Patch is {days} days old (<= 90 days): Up-to-date",
                    "severity": "Info",
                })
        else:
            vulns.append({
                "type": "windows_last_security_update",
                "details": "Last Security Update: Unknown (cannot determine hotfix install date)",
                "severity": "Medium",
            })

        # KB Map Check
        cves_to_check = None
        if isinstance(audit_data, dict):
            pol = audit_data.get("policy", {})
            if isinstance(pol, dict) and isinstance(pol.get("windows_cves"), list):
                cves_to_check = pol.get("windows_cves")
        if cves_to_check:
            base = Path(__file__).resolve().parent.parent
            kb_map_path = base / "papar" / "windows_cve_kb_map.csv"
            if isinstance(audit_data, dict):
                pol = audit_data.get("policy", {})
                if isinstance(pol, dict) and pol.get("windows_kb_map_path"):
                    kb_map_path = Path(str(pol.get("windows_kb_map_path")))
            cve_kb_map = kbmap.load_cve_kb_map_csv(kb_map_path)
            if cve_kb_map:
                vulns.append({
                    "type": "windows_cve_check_scope",
                    "details": f"Checking KB installation for {len(cves_to_check)} CVEs",
                    "severity": "Info",
                })
                vulns.extend(kbmap.evaluate_missing_kbs(patches, cve_kb_map, cves=cves_to_check, include_unmapped=True))
            else:
                vulns.append({
                    "type": "windows_kb_map_missing",
                    "details": "CVE↔KB mapping file not found or empty; cannot assess CVE patch status",
                    "severity": "Low",
                })

        # F2: Defender Analysis
        defender = audit_data.get("defender")
        if defender:
            enabled = defender.get("enabled")
            sl = defender.get("signature_last_updated")
            tp = defender.get("third_party_av")
            
            if not enabled and not tp:
                vulns.append({
                    "type": "defender_status",
                    "details": "Windows Defender is disabled and no third-party AV detected",
                    "severity": "Critical"
                })
            else:
                if sl:
                    try:
                        dt = datetime.date.fromisoformat(sl)
                        days = (datetime.date.today() - dt).days
                        if days > 30:
                            vulns.append({
                                "type": "defender_status",
                                "details": f"Defender signatures out of date by {days} days (> 30)",
                                "severity": "High"
                            })
                        elif days > 7:
                            vulns.append({
                                "type": "defender_status",
                                "details": f"Defender signatures out of date by {days} days (> 7)",
                                "severity": "Medium"
                            })
                        else:
                            vulns.append({
                                "type": "defender_status",
                                "details": f"Defender status normal (signatures {days} days old)",
                                "severity": "Info"
                            })
                    except:
                        pass
                else:
                    if enabled:
                         vulns.append({
                            "type": "defender_status",
                            "details": "Defender enabled but signature date unknown",
                            "severity": "Info"
                        })

    # F3: Browser Analysis
    browsers = audit_data.get("browsers", {})
    for name, ver in browsers.items():
        min_ver = MIN_SECURE_VERSIONS.get(name)
        if min_ver:
            cmp_res = _cmp_versions(ver, min_ver)
            if cmp_res == -1: # ver < min_ver
                vulns.append({
                    "type": "browser_outdated",
                    "details": f"{name} version {ver} is below minimum secure version {min_ver}",
                    "severity": "High"
                })
            else:
                vulns.append({
                    "type": "browser_info",
                    "details": f"{name} version {ver} is up-to-date (>= {min_ver})",
                    "severity": "Info"
                })

    server_cfg_findings = audit_data.get("server_config") if isinstance(audit_data, dict) else None
    if isinstance(server_cfg_findings, list):
        for f in server_cfg_findings:
            if isinstance(f, dict) and f.get("type") and f.get("severity"):
                vulns.append(f)

    # 2. Node.js Analysis
    node_info = audit_data.get("node", {})
    version = node_info.get("version")
    
    if version:
        v_clean = version.lstrip('v')
        try:
            major = int(v_clean.split('.')[0])
            if major < 18:
                vulns.append({
                    "type": "nodejs_eol",
                    "details": f"Node.js version {version} is End-of-Life (EOL)",
                    "severity": "Critical",
                    "cves": ["CVE-2023-32002", "CVE-2023-32559"]
                })
            elif major == 18 and int(v_clean.split('.')[1]) < 19:
                 vulns.append({
                    "type": "nodejs_outdated",
                    "details": f"Node.js version {version} is outdated",
                    "severity": "Medium"
                })
        except:
            pass
            
        vulns.append({
            "type": "nodejs_info",
            "details": f"Node.js {version} (npm {node_info.get('npm_version')})",
            "severity": "Info"
        })
    else:
        vulns.append({
            "type": "nodejs_missing",
            "details": "Node.js not found in environment",
            "severity": "Low"
        })

    openclaw_info = audit_data.get("openclaw", {}) if isinstance(audit_data, dict) else {}
    latest = None
    if isinstance(audit_data, dict):
        pol = audit_data.get("policy", {})
        if isinstance(pol, dict):
            latest = pol.get("latest_openclaw_version")
    current = openclaw_info.get("version") if isinstance(openclaw_info, dict) else None
    openclaw_path = openclaw_info.get("path") if isinstance(openclaw_info, dict) else None

    if current:
        vulns.append({
            "type": "openclaw_cli_info",
            "details": f"OpenClaw CLI {current}",
            "severity": "Info"
        })
        if latest:
            cmp_res = _cmp_versions(current, latest)
            if cmp_res == -1:
                vulns.append({
                    "type": "openclaw_outdated",
                    "details": f"OpenClaw CLI version {current} is behind latest {latest}. ZH: 升级后部分或全部功能可能不可用，请谨慎判断。 EN: After upgrading, some or all functions may be unavailable; assess carefully.",
                    "severity": "High"
                })
            elif cmp_res is None and str(current).strip() != str(latest).strip():
                vulns.append({
                    "type": "openclaw_version_mismatch",
                    "details": f"OpenClaw CLI version {current} differs from latest {latest}. ZH: 升级后部分或全部功能可能不可用，请谨慎判断。 EN: After upgrading, some or all functions may be unavailable; assess carefully.",
                    "severity": "High"
                })
    elif openclaw_path:
        vulns.append({
            "type": "openclaw_cli_unreadable",
            "details": "OpenClaw CLI found but version unreadable from openclaw --version",
            "severity": "Low"
        })
    else:
        vulns.append({
            "type": "openclaw_cli_missing",
            "details": "OpenClaw CLI not found in PATH",
            "severity": "Low"
        })

    vulns.sort(key=lambda v: (-_sev_rank(v.get("severity")), str(v.get("type") or "")))
    return vulns
