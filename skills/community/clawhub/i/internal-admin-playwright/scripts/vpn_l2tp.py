#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
import yaml


def sh(cmd: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, shell=True, text=True, capture_output=True, check=check)


def load_cfg(skill_root: Path) -> dict:
    p = skill_root / "references" / "vpn_config.yaml"
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def write_configs(cfg: dict):
    server = cfg.get("server", "").strip()
    username = cfg.get("username", "").strip()
    password = cfg.get("password", "").strip()
    psk = cfg.get("psk", "").strip()
    local_port = int(cfg.get("xl2tpd_local_port", 0) or 0)

    if not all([server, username, password, psk]):
        raise SystemExit("vpn_config.yaml 缺少 server/username/password/psk")

    Path("/etc/ipsec.conf").write_text(
        f'''config setup\n  uniqueids=no\n\nconn l2tp-psk\n  keyexchange=ikev1\n  authby=psk\n  type=transport\n  left=%defaultroute\n  leftprotoport=17/1701\n  right={server}\n  rightprotoport=17/1701\n  rightid=%any\n  forceencaps=yes\n  auto=add\n''',
        encoding="utf-8",
    )
    Path("/etc/ipsec.secrets").write_text(f'%any {server} : PSK "{psk}"\n', encoding="utf-8")
    sh("chmod 600 /etc/ipsec.secrets")

    Path("/etc/xl2tpd/xl2tpd.conf").write_text(
        f'''[global]\naccess control = no\nport = {local_port}\n\n[lac myvpn]\nlns = {server}\npppoptfile = /etc/ppp/options.xl2tpd\nlength bit = yes\nredial = yes\nredial timeout = 15\nmax redials = 3\nautodial = no\n''',
        encoding="utf-8",
    )

    Path("/etc/ppp/options.xl2tpd").write_text(
        f'''ipcp-accept-local\nipcp-accept-remote\nrefuse-eap\nrequire-mschap-v2\nnoccp\nnoauth\nmtu 1410\nmru 1410\nnoipdefault\ndefaultroute\nusepeerdns\nconnect-delay 5000\nname "{username}"\npassword "{password}"\n''',
        encoding="utf-8",
    )
    sh("chmod 600 /etc/ppp/options.xl2tpd")


def up(skill_root: Path):
    cfg = load_cfg(skill_root)
    write_configs(cfg)
    server = cfg["server"]

    sh("/sbin/modprobe l2tp_ppp", check=False)
    sh("/usr/sbin/ipsec restart")
    sh("/usr/sbin/ipsec up l2tp-psk", check=False)
    sh("pkill xl2tpd", check=False)
    sh("nohup /usr/sbin/xl2tpd -D >/var/log/xl2tpd-manual.log 2>&1 &")
    sh("sleep 2 && echo 'c myvpn' > /var/run/xl2tpd/l2tp-control", check=False)
    sh("sleep 3", check=False)

    if cfg.get("route_all_traffic", True):
        gw = sh("ip route | awk '/default via/ {print $3; exit}'", check=False).stdout.strip()
        if gw:
            sh(f"ip route replace {server} via {gw} dev eth0", check=False)
            sh("ip route replace default dev ppp0", check=False)

    print("VPN up done")


def down(skill_root: Path):
    sh("poff -a", check=False)
    sh("pkill pppd", check=False)
    sh("pkill xl2tpd", check=False)
    sh("/usr/sbin/ipsec down l2tp-psk", check=False)
    sh("/usr/sbin/ipsec stop", check=False)
    print("VPN down done")


def status():
    sh1 = sh("ip -brief a | grep -E 'ppp0|eth0|lo' || true", check=False).stdout
    sh2 = sh("/usr/sbin/ipsec status || true", check=False).stdout
    print(sh1)
    print(sh2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["up", "down", "status"])
    args = parser.parse_args()
    skill_root = Path(__file__).resolve().parents[1]

    if args.action == "up":
        up(skill_root)
    elif args.action == "down":
        down(skill_root)
    else:
        status()


if __name__ == "__main__":
    main()
