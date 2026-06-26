#!/usr/bin/env python3
"""Interactive setup for PBS Backup skill."""

import getpass
import json
import sys
from pathlib import Path

try:
    from proxmoxer import ProxmoxAPI
except ImportError:
    print("proxmoxer not installed. Run: pip install proxmoxer")
    sys.exit(1)

# Add current dir to path to allow importing backup.py
sys.path.append(str(Path(__file__).parent.resolve()))
try:
    from backup import cmd_backup
except ImportError as e:
    print(f"Could not import backup.py: {e}")
    cmd_backup = None

PROXMOX_CREDS = Path.home() / ".openclaw" / "credentials" / "proxmox.json"
PBS_CONFIG = Path.home() / ".openclaw" / "credentials" / "pbs-backup.json"


def ask(prompt, default=""):
    suffix = f" [{default}]" if default else ""
    val = input(f"{prompt}{suffix}: ").strip()
    return val or default

def ask_int(prompt, default=""):
    while True:
        val = ask(prompt, default)
        try:
            return int(val)
        except ValueError:
            print("  Please enter a valid number.")

def yes_no(prompt, default="y"):
    tag = "[Y/n]" if default == "y" else "[y/N]"
    val = input(f"{prompt} {tag}: ").strip().lower()
    if not val:
        return default == "y"
    return val in {"y", "yes", "j", "ja"}


def test_host(cfg):
    try:
        tid = cfg["token_id"]
        user = tid.rsplit("!", 1)[0] if "!" in tid else "root@pam"
        prox = ProxmoxAPI(
            cfg["host"], user=user,
            token_name=tid.split("!")[1] if "!" in tid else tid,
            token_value=cfg["token_secret"],
            verify_ssl=cfg.get("verify_ssl", False),
        )
        nodes = prox.nodes.get()
        return nodes[0]["node"] if nodes else None
    except Exception as e:
        print(f"  Connection failed: {e}")
        return None


def main():
    print("=== PBS Backup Setup ===\n")
    config = {"pbs": {}, "defaults": {}, "proxmox_hosts": {}, "targets": {}}

    # --- A. PBS ---
    if not yes_no("Is a Proxmox Backup Server already running?"):
        print("\nPBS must be installed first.")
        print("Installation steps are in 'references/setup-guide.md'.")
        if not yes_no("Continue setup anyway (for later PBS install)?", "n"):
            sys.exit(0)
    else:
        config["pbs"]["host"] = ask("PBS IP/hostname")
        config["pbs"]["port"] = ask_int("PBS port", "8007")
        config["pbs"]["datastore"] = ask("PBS datastore name")
        config["pbs"]["verify_ssl"] = yes_no("Verify PBS TLS?", "n")

        print("\n--- PBS Storage Setup ---")
        print("How will PBS store backups?")
        print("  1. Locally (on the PBS host's own disk)")
        print("  2. On a NAS (via NFS or SMB mount)")
        storage_choice = ask("Choice (1/2)", "1")

        if storage_choice == "2":
            config["pbs"]["storage_type"] = "nas"
            while True:
                nas_type = ask("NAS type (nfs/smb)", "nfs").lower()
                if nas_type in {"nfs", "smb"}:
                    break
                print("  Must be 'nfs' or 'smb'.")
            nas_ip = ask("NAS IP/hostname")
            nas_export = ask("NFS export path or SMB share")
            nas_mount = ask("Local mount point on PBS host", f"/mnt/pbs/{config['pbs']['datastore']}")
            config["pbs"]["nas"] = {
                "type": nas_type, "ip": nas_ip, "export": nas_export, "mount_point": nas_mount,
            }

            print("\n--- ACTION REQUIRED: Mount NAS on PBS Host ---")
            print("Log into your PBS host and run these commands:")
            print(f"\n  # Create mount point\n  sudo mkdir -p {nas_mount}")

            if nas_type == "nfs":
                print("\n  # Install NFS client\n  sudo apt update && sudo apt install -y nfs-common")
                fstab_line = f"{nas_ip}:{nas_export}  {nas_mount}  nfs   defaults,nofail   0 0"
                print(f"\n  # Add to /etc/fstab to mount on boot\n  echo '{fstab_line}' | sudo tee -a /etc/fstab")
                print("\n  # Mount now\n  sudo mount -a")
                print(f"\n  # Verify (should show the new mount)\n  df -h {nas_mount}")

            else: # smb
                print("\n  # Install SMB client\n  sudo apt update && sudo apt install -y cifs-utils")
                smb_user = ask("SMB username")
                smb_pass = getpass.getpass("  SMB password: ")
                creds_file = "/root/.smbcreds"
                print("\n  # Create credentials file manually:")
                print(f"  sudo nano {creds_file}")
                print("  # Add these two lines:")
                print(f"  #   username={smb_user}")
                print("  #   password=<your_smb_password>")
                print(f"  sudo chmod 600 {creds_file}")
                fstab_line = f"//{nas_ip}/{nas_export}  {nas_mount}  cifs   credentials={creds_file},iocharset=utf8,nofail   0 0"
                print(f"\n  # Add to /etc/fstab to mount on boot\n  echo \"{fstab_line}\" | sudo tee -a /etc/fstab")
                print("\n  # Mount now\n  sudo mount -a")

            print("\n-------------------------------------------------")
            if not yes_no("Have you completed ALL the steps above?"):
                print("Aborting setup. Please complete the steps and run again.")
                sys.exit(1)
            
            print("\nGreat. Now, create the datastore:")
            print(f"  sudo proxmox-backup-manager datastore create {config['pbs']['datastore']} {nas_mount}")

        else: # local
            config["pbs"]["storage_type"] = "local"
            local_path = ask("Path for local datastore", f"/backup/{config['pbs']['datastore']}")
            config["pbs"]["local_path"] = local_path
            print("\n--- ACTION REQUIRED: Create Datastore ---")
            print("Log into your PBS host and run these commands:")
            print(f"  # Create directory\n  sudo mkdir -p {local_path}")
            print(f"  # Create datastore\n  sudo proxmox-backup-manager datastore create {config['pbs']['datastore']} {local_path}")
            print("-------------------------------------------")

        if not yes_no("Have you created the datastore on the PBS host?"):
            print("Aborting setup. Please create the datastore and run again.")
            sys.exit(1)


    # --- B. Defaults ---
    print("\n--- Backup defaults ---")
    if yes_no("Is PBS already added as a storage target on your Proxmox host(s)?", "y"):
        storage = ask("PBS storage name in Proxmox")
    else:
        print("\n  You must add PBS as a storage target in Proxmox.")
        print("  Example command to run on your Proxmox host:")
        print("  pvesm add pbs <storage_name> --server <pbs_ip> --datastore <ds_name> --username <user>@pbs --fingerprint <fp> --password <pw>")
        storage = ask("\nEnter the storage name you will use")

    config["defaults"] = {
        "storage": storage,
        "mode": ask("Backup mode", "snapshot"),
        "compress": ask("Compression", "zstd"),
        "prune_keep_last": ask_int("Keep last N backups", "10"),
    }

    # --- C. Proxmox hosts ---
    print("\n--- Proxmox hosts ---")
    if PROXMOX_CREDS.exists() and yes_no("Import hosts from proxmox.json?"):
        try:
            imported = json.loads(PROXMOX_CREDS.read_text()).get("hosts", {})
        except (json.JSONDecodeError, IOError) as e:
            print(f"  Warning: Could not read proxmox.json: {e}")
            imported = {}
        config["proxmox_hosts"].update(imported)
        if imported:
            print(f"  Imported: {', '.join(imported.keys())}")

    print("Add Proxmox hosts (empty label to skip/finish):")
    while True:
        label = ask("\nHost label").strip()
        if not label:
            break
        if label in config["proxmox_hosts"]:
            print(f"  '{label}' already exists.")
            continue

        h = {
            "host": ask("  IP/hostname"),
            "token_id": ask("  API token ID (format: user@realm!tokenname, e.g. root@pam!backup)"),
            "token_secret": ask("  Token secret"),
            "verify_ssl": yes_no("  Verify TLS?", "n"),
        }
        node = test_host(h)
        if node:
            h["node"] = node
            print(f"  Connected — node: {node}")
        else:
            h["node"] = ask("  Node name (auto-detect failed)")
        config["proxmox_hosts"][label] = h

    if not config["proxmox_hosts"]:
        print("\nNo hosts configured. Cannot continue.")
        sys.exit(1)

    # --- D. Discover & Select Targets ---
    print("\n--- Discovering VMs and containers on all hosts ---")
    all_guests = []  # [{vmid, name, type, host_label, node, status}]

    for label, hcfg in config["proxmox_hosts"].items():
        node = hcfg.get("node")
        if not node:
            print(f"  Skipping {label}: no node name")
            continue
        try:
            tid = hcfg["token_id"]
            user = tid.rsplit("!", 1)[0] if "!" in tid else "root@pam"
            prox = ProxmoxAPI(
                hcfg["host"], user=user,
                token_name=tid.split("!")[1] if "!" in tid else tid,
                token_value=hcfg["token_secret"],
                verify_ssl=hcfg.get("verify_ssl", False),
            )
            for ct in prox.nodes(node).lxc.get():
                all_guests.append({
                    "vmid": str(ct["vmid"]), "name": ct.get("name", "?"),
                    "type": "lxc", "host": label, "node": node,
                    "status": ct.get("status", "?"),
                })
            for vm in prox.nodes(node).qemu.get():
                all_guests.append({
                    "vmid": str(vm["vmid"]), "name": vm.get("name", "?"),
                    "type": "qemu", "host": label, "node": node,
                    "status": vm.get("status", "?"),
                })
        except Exception as e:
            print(f"  Warning: Could not query {label}: {e}")

    if not all_guests:
        print("  No VMs or containers found on any host.")
        print("  You can add targets manually later by editing the config.")
    else:
        # Sort by host then vmid
        all_guests.sort(key=lambda g: (g["host"], int(g["vmid"])))

        print(f"\n  Found {len(all_guests)} guests:\n")
        print(f"  {'#':>3}  {'VMID':>5}  {'Type':<5} {'Name':<20} {'Host':<15} {'Status'}")
        print(f"  {'-'*3}  {'-'*5}  {'-'*5} {'-'*20} {'-'*15} {'-'*7}")
        for i, g in enumerate(all_guests, 1):
            print(f"  {i:>3}  {g['vmid']:>5}  {g['type']:<5} {g['name']:<20} {g['host']:<15} {g['status']}")

        print("\n  Options:")
        print("    'all'          — add all as backup targets")
        print("    '1,3,5'        — add specific ones by number")
        print("    '1-4,7'        — ranges work too")
        print("    empty / 'none' — skip, add targets later")

        selection = ask("\n  Select targets", "all").strip().lower()

        if selection and selection != "none":
            selected_indices = set()
            if selection == "all":
                selected_indices = set(range(len(all_guests)))
            else:
                for part in selection.split(","):
                    part = part.strip()
                    if "-" in part:
                        try:
                            a, b = part.split("-", 1)
                            for idx in range(int(a) - 1, int(b)):
                                selected_indices.add(idx)
                        except ValueError:
                            print(f"  Invalid range: {part}")
                    else:
                        try:
                            selected_indices.add(int(part) - 1)
                        except ValueError:
                            print(f"  Invalid number: {part}")

            added = 0
            for idx in sorted(selected_indices):
                if 0 <= idx < len(all_guests):
                    g = all_guests[idx]
                    config["targets"][g["vmid"]] = {
                        "host": g["host"],
                        "node": g["node"],
                        "type": g["type"],
                        "name": g["name"],
                        "storage": storage,
                    }
                    added += 1
            print(f"\n  ✅ Added {added} backup target(s).")
        else:
            print("  No targets selected. You can add them later.")

    # --- Save ---
    PBS_CONFIG.parent.mkdir(parents=True, exist_ok=True)
    PBS_CONFIG.write_text(json.dumps(config, indent=2))
    PBS_CONFIG.chmod(0o600)
    print(f"\n✅ Config saved to {PBS_CONFIG}")

    # Print summary without secrets
    summary_config = json.loads(json.dumps(config))
    for h in summary_config.get("proxmox_hosts", {}).values():
        if "token_secret" in h:
            h["token_secret"] = "***"
    print(json.dumps(summary_config, indent=2))

    # --- Test backup ---
    if config.get("targets") and cmd_backup:
        if yes_no("\nRun a test backup now?"):
            first_target_vmid = list(config["targets"].keys())[0]
            print(f"\n--- Running test backup for VMID {first_target_vmid} ---")
            try:
                cmd_backup(config, first_target_vmid, note="First backup via setup", timeout=300)
                print("--- Test backup finished ---")
            except SystemExit as e:
                # cmd_backup calls sys.exit on success/fail, which is fine
                if e.code != 0:
                    print("--- Test backup reported an error ---")
            except Exception as e:
                print(f"--- An unexpected error occurred during test backup: {e} ---")
        else:
            print("\nReminder: Run a manual backup soon to verify the setup.")


if __name__ == "__main__":
    main()
