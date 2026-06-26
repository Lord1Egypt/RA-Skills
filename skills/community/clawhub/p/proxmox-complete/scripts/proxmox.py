#!/usr/bin/env python3
"""
Proxmox Complete Skill - Python API
Merged from robnew/proxmox-skill with enhancements
"""

import os
import sys
import json
from proxmoxer import ProxmoxAPI

def jprint(obj, code=0):
    print(json.dumps(obj, indent=2))
    sys.exit(code)

def env(name: str) -> str:
    v = os.getenv(name)
    if not v:
        jprint({"ok": False, "error": f"Missing env var: {name}"}, 2)
    return v

def load_config():
    """Load config from OpenClaw credentials or env vars"""
    config_file = os.path.expanduser("~/.openclaw/credentials/proxmox.json")
    
    if os.path.exists(config_file):
        with open(config_file) as f:
            cfg = json.load(f)
        host = cfg.get("host", "").replace("https://", "").replace("http://", "")
        token_id = cfg.get("token_id", "")
        token_secret = cfg.get("token_secret", "")
        verify_ssl = cfg.get("verify_ssl", False)
    else:
        # Fall back to env vars
        host = env("PVE_HOST").replace("https://", "").replace("http://", "")
        token_id = env("PVE_TOKEN_ID")
        token_secret = env("PVE_TOKEN_SECRET")
        verify_ssl = os.getenv("PVE_VERIFY_SSL", "false").lower() in ("true", "1", "yes")
    
    if "!" not in token_id:
        jprint({"ok": False, "error": "Token ID must be user@realm!tokenname"}, 2)
    
    return host, token_id, token_secret, verify_ssl

def connect() -> ProxmoxAPI:
    host, token_id, token_secret, verify_ssl = load_config()
    user, token_name = token_id.split("!", 1)
    
    return ProxmoxAPI(
        host,
        user=user,
        token_name=token_name,
        token_value=token_secret,
        verify_ssl=verify_ssl,
    )

def list_nodes(p: ProxmoxAPI):
    return p.nodes.get()

def node_health(p: ProxmoxAPI, node: str):
    return p.nodes(node).status.get()

def list_vms(p: ProxmoxAPI):
    return p.cluster.resources.get(type="vm")

def status_current(p: ProxmoxAPI, node: str, kind: str, vmid: str):
    endpoint = getattr(p.nodes(node), kind)
    return endpoint(vmid).status.current.get()

def action_vm(p: ProxmoxAPI, node: str, kind: str, vmid: str, action: str):
    endpoint = getattr(p.nodes(node), kind)
    return getattr(endpoint(vmid).status, action).post()

def snapshot_vm(p: ProxmoxAPI, node: str, kind: str, vmid: str, snapname: str, vmstate: bool = False):
    endpoint = getattr(p.nodes(node), kind)
    return endpoint(vmid).snapshot.post(snapname=snapname, vmstate=1 if vmstate else 0)

def list_snapshots(p: ProxmoxAPI, node: str, kind: str, vmid: str):
    endpoint = getattr(p.nodes(node), kind)
    return endpoint(vmid).snapshot.get()

def delete_snapshot(p: ProxmoxAPI, node: str, kind: str, vmid: str, snapname: str):
    endpoint = getattr(p.nodes(node), kind)
    return endpoint(vmid).snapshot(snapname).delete()

def rollback_snapshot(p: ProxmoxAPI, node: str, kind: str, vmid: str, snapname: str):
    endpoint = getattr(p.nodes(node), kind)
    return endpoint(vmid).snapshot(snapname).rollback.post()

def list_storage(p: ProxmoxAPI, node: str):
    return p.nodes(node).storage.get()

def list_tasks(p: ProxmoxAPI, node: str, limit: int = 10):
    return p.nodes(node).tasks.get(limit=limit)

def list_backups(p: ProxmoxAPI, node: str, storage: str = "local"):
    return p.nodes(node).storage(storage).content.get(content="backup")

def usage():
    jprint({
        "ok": False,
        "error": "usage",
        "examples": [
            "proxmox.py nodes",
            "proxmox.py node_health <node>",
            "proxmox.py vms",
            "proxmox.py status <node> <qemu|lxc> <vmid>",
            "proxmox.py list_snapshots <node> <qemu|lxc> <vmid>",
            "proxmox.py snapshot <node> <qemu|lxc> <vmid> <snapname> [vmstate=0|1]",
            "proxmox.py delete_snapshot <node> <qemu|lxc> <vmid> <snapname>",
            "proxmox.py rollback <node> <qemu|lxc> <vmid> <snapname>",
            "proxmox.py <start|stop|reboot|shutdown> <node> <qemu|lxc> <vmid>",
            "proxmox.py storage <node>",
            "proxmox.py backups <node> [storage]",
            "proxmox.py tasks <node> [limit]"
        ]
    }, 2)

def main():
    if len(sys.argv) < 2:
        usage()

    p = connect()
    cmd = sys.argv[1].strip().lower()

    try:
        if cmd == "nodes":
            jprint({"ok": True, "data": list_nodes(p)})
        
        elif cmd == "node_health":
            node = sys.argv[2]
            jprint({"ok": True, "data": node_health(p, node)})
        
        elif cmd == "vms":
            jprint({"ok": True, "data": list_vms(p)})
        
        elif cmd == "status":
            node, kind, vmid = sys.argv[2:5]
            jprint({"ok": True, "data": status_current(p, node, kind, vmid)})
        
        elif cmd == "start":
            node, kind, vmid = sys.argv[2:5]
            jprint({"ok": True, "data": action_vm(p, node, kind, vmid, "start")})
        
        elif cmd == "stop":
            node, kind, vmid = sys.argv[2:5]
            jprint({"ok": True, "data": action_vm(p, node, kind, vmid, "stop")})
        
        elif cmd == "shutdown":
            node, kind, vmid = sys.argv[2:5]
            jprint({"ok": True, "data": action_vm(p, node, kind, vmid, "shutdown")})
        
        elif cmd == "reboot":
            node, kind, vmid = sys.argv[2:5]
            jprint({"ok": True, "data": action_vm(p, node, kind, vmid, "reboot")})
        
        elif cmd == "snapshot":
            node, kind, vmid, snapname = sys.argv[2:6]
            vmstate = sys.argv[6].lower() in ("1", "true", "yes") if len(sys.argv) > 6 else False
            jprint({"ok": True, "data": snapshot_vm(p, node, kind, vmid, snapname, vmstate)})
        
        elif cmd == "list_snapshots":
            node, kind, vmid = sys.argv[2:5]
            jprint({"ok": True, "data": list_snapshots(p, node, kind, vmid)})
        
        elif cmd == "delete_snapshot":
            node, kind, vmid, snapname = sys.argv[2:6]
            jprint({"ok": True, "data": delete_snapshot(p, node, kind, vmid, snapname)})
        
        elif cmd == "rollback":
            node, kind, vmid, snapname = sys.argv[2:6]
            jprint({"ok": True, "data": rollback_snapshot(p, node, kind, vmid, snapname)})
        
        elif cmd == "storage":
            node = sys.argv[2]
            jprint({"ok": True, "data": list_storage(p, node)})
        
        elif cmd == "backups":
            node = sys.argv[2]
            storage = sys.argv[3] if len(sys.argv) > 3 else "local"
            jprint({"ok": True, "data": list_backups(p, node, storage)})
        
        elif cmd == "tasks":
            node = sys.argv[2]
            limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
            jprint({"ok": True, "data": list_tasks(p, node, limit)})
        
        else:
            usage()
    
    except Exception as e:
        jprint({"ok": False, "error": str(e)}, 1)

if __name__ == "__main__":
    main()