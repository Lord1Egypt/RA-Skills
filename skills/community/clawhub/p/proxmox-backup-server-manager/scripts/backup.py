#!/usr/bin/env python3
"""PBS Backup — create, list, check, and manage Proxmox Backup Server backups."""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    from proxmoxer import ProxmoxAPI
    import urllib.request
    import ssl
except ImportError:
    print(json.dumps({"ok": False, "error": "proxmoxer not installed", "hint": "pip install proxmoxer"}))
    sys.exit(1)

PBS_CONFIG = Path.home() / ".openclaw" / "credentials" / "pbs-backup.json"
PROXMOX_CREDS = Path.home() / ".openclaw" / "credentials" / "proxmox.json"


def load_config():
    if not PBS_CONFIG.exists():
        print(json.dumps({
            "ok": False,
            "error": "PBS not configured",
            "setup_needed": True,
            "hint": "Run setup.py or follow references/setup-guide.md"
        }))
        sys.exit(1)
    try:
        return json.loads(PBS_CONFIG.read_text())
    except json.JSONDecodeError as e:
        print(json.dumps({"ok": False, "error": f"Invalid config file: {e}"}))
        sys.exit(1)


def resolve_hosts(config):
    """Merge hosts from PBS config and optional proxmox.json."""
    hosts = dict(config.get("proxmox_hosts", {}))
    if not hosts and PROXMOX_CREDS.exists():
        try:
            creds = json.loads(PROXMOX_CREDS.read_text())
            hosts.update(creds.get("hosts", {}))
        except json.JSONDecodeError as e:
            print(json.dumps({"ok": False, "error": f"Invalid proxmox.json file: {e}"}))
            sys.exit(1)
    return hosts


def connect(hosts, host_name):
    if host_name not in hosts:
        print(json.dumps({
            "ok": False,
            "error": f"Unknown host: {host_name}",
            "available": list(hosts.keys())
        }))
        sys.exit(1)
    try:
        h = hosts[host_name]
        tid = h.get("token_id", "")
        user = tid.rsplit("!", 1)[0] if "!" in tid else "root@pam"
        return ProxmoxAPI(
            h["host"], user=user,
            token_name=tid.split("!")[1] if "!" in tid else tid,
            token_value=h["token_secret"],
            verify_ssl=h.get("verify_ssl", False)
        )
    except KeyError as e:
        print(json.dumps({"ok": False, "error": f"Missing config key for host {host_name}: {e}"}))
        sys.exit(1)


def get_target(config, vmid):
    """Resolve a VMID to its full target config."""
    targets = config.get("targets", config.get("containers", {}))
    defaults = config.get("defaults", {})
    key = str(vmid)

    if key in targets:
        ct = targets[key].copy()
        for k, v in defaults.items():
            ct.setdefault(k, v)
        if "node" not in ct:
            print(json.dumps({
                "ok": False,
                "error": f"Target {vmid} has no 'node' defined",
                "hint": "Add 'node' to the target config in pbs-backup.json"
            }))
            sys.exit(1)
        return ct

    # Not registered
    print(json.dumps({
        "ok": False,
        "error": f"VMID {vmid} is not registered",
        "registered": [
            {"vmid": v, "name": c.get("name", "?")} 
            for v, c in targets.items()
        ],
        "hint": "Add this target to pbs-backup.json or run setup.py"
    }))
    sys.exit(1)


def cmd_backup(config, vmid, note=None, timeout=600):
    ct = get_target(config, vmid)
    hosts = resolve_hosts(config)
    prox = connect(hosts, ct["host"])

    storage = ct.get("storage", config.get("defaults", {}).get("storage", ""))
    if not storage:
        print(json.dumps({
            "ok": False,
            "error": "No storage configured",
            "hint": "Set defaults.storage in pbs-backup.json"
        }))
        sys.exit(1)

    params = {
        "vmid": int(vmid),
        "storage": storage,
        "mode": ct.get("mode", "snapshot"),
        "compress": ct.get("compress", "zstd"),
    }
    if note:
        params["notes-template"] = note

    try:
        upid = str(prox.nodes(ct["node"]).vzdump.post(**params))
    except Exception as e:
        print(json.dumps({"ok": False, "error": f"Failed to start backup: {e}"}))
        sys.exit(1)

    print(json.dumps({
        "ok": True, "status": "triggered",
        "vmid": vmid, "name": ct.get("name", f"VM {vmid}"),
        "storage": storage, "mode": params["mode"],
        "host": ct["host"], "upid": upid
    }))

    # Poll for completion
    last_error = None
    for i in range(timeout // 5):
        time.sleep(5)
        try:
            st = prox.nodes(ct["node"]).tasks(upid).status.get()
            if st.get("status") == "stopped":
                ok = st.get("exitstatus", "") == "OK"
                print(json.dumps({
                    "ok": ok, "action": "backup_finished",
                    "vmid": vmid, "name": ct.get("name", f"VM {vmid}"),
                    "status": st.get("exitstatus", "?"),
                    "storage": storage,
                    "duration_seconds": (i + 1) * 5
                }))
                sys.exit(0 if ok else 1)
        except Exception as e:
            last_error = str(e)
            pass

    timeout_message = f"Timeout ({timeout // 60} min)"
    if last_error:
        timeout_message += f" (Last error: {last_error})"
    print(json.dumps({"ok": False, "error": timeout_message, "upid": upid}))
    sys.exit(1)


def cmd_status(config, vmid):
    ct = get_target(config, vmid)
    hosts = resolve_hosts(config)
    prox = connect(hosts, ct["host"])

    try:
        tasks = prox.nodes(ct["node"]).tasks.get(
            typefilter="vzdump", vmid=int(vmid), limit=1
        )
    except Exception as e:
        print(json.dumps({"ok": False, "error": f"API error fetching status: {e}"}))
        sys.exit(1)

    if not tasks:
        print(json.dumps({"ok": True, "vmid": vmid, "status": "no backups found"}))
        return

    t = tasks[0]
    print(json.dumps({
        "ok": True, "vmid": vmid,
        "name": ct.get("name", f"VM {vmid}"),
        "last_backup": datetime.fromtimestamp(t.get("starttime", 0)).strftime("%Y-%m-%d %H:%M"),
        "status": t.get("exitstatus", t.get("status", "?")),
        "storage": ct.get("storage", "?")
    }))


def cmd_list(config, vmid):
    ct = get_target(config, vmid)
    hosts = resolve_hosts(config)
    prox = connect(hosts, ct["host"])

    try:
        tasks = prox.nodes(ct["node"]).tasks.get(
            typefilter="vzdump", vmid=int(vmid), limit=10
        )
    except Exception as e:
        print(json.dumps({"ok": False, "error": f"API error fetching list: {e}"}))
        sys.exit(1)
        
    backups = [{
        "time": datetime.fromtimestamp(t.get("starttime", 0)).strftime("%Y-%m-%d %H:%M"),
        "status": t.get("exitstatus", t.get("status", "?"))
    } for t in tasks]

    print(json.dumps({"ok": True, "vmid": vmid, "name": ct.get("name", f"VM {vmid}"), "backups": backups}))


def cmd_check(config):
    hosts = resolve_hosts(config)
    results = []

    for name, h in hosts.items():
        try:
            prox = connect(hosts, name)
            nodes = [n["node"] for n in prox.nodes.get()]
            storage = config.get("defaults", {}).get("storage", "")
            storage_ok = False
            storage_error = None
            if storage and nodes:
                try:
                    ss = prox.nodes(nodes[0]).storage.get()
                    storage_ok = any(s["storage"] == storage for s in ss)
                except Exception as e:
                    storage_ok = False
                    storage_error = str(e)
            
            res = {"host": name, "ip": h.get("host", "?"), "status": "ok",
                   "nodes": nodes, "storage": storage, "storage_ok": storage_ok}
            if storage_error:
                res["storage_error"] = storage_error
            results.append(res)
        except Exception as e:
            results.append({"host": name, "ip": h.get("host", "?"), "status": "error", "error": str(e)})

    containers = config.get("targets", config.get("containers", {}))
    pbs_config = config.get("pbs", {})
    pbs_status = "not configured"
    if pbs_config.get("host"):
        try:
            url = f"https://{pbs_config['host']}:{pbs_config.get('port', 8007)}/api2/json/version"
            ctx = ssl.create_default_context()
            if not pbs_config.get("verify_ssl", False):
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
            with urllib.request.urlopen(url, context=ctx, timeout=5) as resp:
                if resp.status == 200:
                    pbs_status = "ok"
                else:
                    pbs_status = f"error (HTTP {resp.status})"
        except Exception as e:
            pbs_status = f"error ({e})"

    print(json.dumps({
        "ok": all(r["status"] == "ok" for r in results) and pbs_status == "ok",
        "hosts": results,
        "targets": len(containers),
        "pbs": {"host": pbs_config.get("host", "not configured"), "status": pbs_status}
    }))


def cmd_targets(config):
    targets = config.get("targets", config.get("containers", {}))
    result = [{"vmid": v, "name": c.get("name", "?"), "host": c.get("host", "?"),
               "type": c.get("type", "?"), "storage": c.get("storage", "?")}
              for v, c in targets.items()]
    print(json.dumps({"ok": True, "targets": result}))


def main():
    p = argparse.ArgumentParser(description="PBS Backup Manager")
    p.add_argument("vmid", nargs="?", help="VM/CT ID")
    p.add_argument("--note", "-n", help="Backup note")
    p.add_argument("--list", "-l", action="store_true", help="List recent backups")
    p.add_argument("--status", "-s", action="store_true", help="Last backup status")
    p.add_argument("--check", action="store_true", help="Health check")
    p.add_argument("--targets", "-t", action="store_true", help="List targets")
    p.add_argument("--timeout", type=int, default=600, help="Backup timeout in seconds (default: 600)")
    args = p.parse_args()

    config = load_config()

    if args.check:
        return cmd_check(config)
    if args.targets:
        return cmd_targets(config)
    if not args.vmid:
        # No VMID — back up all targets
        targets = config.get("targets", config.get("containers", {}))
        if not targets:
            print(json.dumps({"ok": False, "error": "No targets configured", "setup_needed": True}))
            return
        results = []
        for vmid in targets:
            try:
                cmd_backup(config, vmid, args.note, args.timeout)
                results.append({"vmid": vmid, "name": targets[vmid].get("name", "?"), "ok": True})
            except SystemExit as e:
                results.append({"vmid": vmid, "name": targets[vmid].get("name", "?"), "ok": e.code == 0})
        if len(targets) > 1:
            print(json.dumps({"ok": all(r["ok"] for r in results), "action": "batch_complete", "results": results}))
        return

    if args.list:
        cmd_list(config, args.vmid)
    elif args.status:
        cmd_status(config, args.vmid)
    else:
        cmd_backup(config, args.vmid, args.note, args.timeout)


if __name__ == "__main__":
    main()
