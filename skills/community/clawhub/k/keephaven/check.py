#!/usr/bin/env python3
"""Check a running Keephaven (a box, or the VM from the Keephaven VM script) and print a report an agent can share.

    python3 check.py                                      # the VM: dashboard :8080, settings :8888, Photos :2283
    python3 check.py --host keephaven-xxxx.local --web 80 # a box on your network
    python3 check.py --json

Read-only: signs in to nothing and changes nothing. Standard library only.
It reads the apps from the dashboard itself, so it checks exactly what that edition runs.
"""
import argparse
import json
import platform
import re
import urllib.error
import urllib.request


def get(url, timeout=6):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "keephaven-check/1"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(262144).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception:
        return 0, ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--web", type=int, default=8080, help="dashboard port: 80 on a box, 8080 on the VM")
    ap.add_argument("--settings", type=int, default=8888)
    ap.add_argument("--photos", type=int, default=2283, help="where Photos (Immich) answers, if forwarded elsewhere")
    ap.add_argument("--memory", type=int, default=8790)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    base = f"http://{a.host}"
    rep = {"check": "keephaven-check v1", "host": a.host, "checker_os": f"{platform.system()} {platform.machine()}"}

    s, page = get(f"{base}:{a.web}/")
    title = (re.search(r"<title>([^<]*)</title>", page) or [None, ""])[1]
    if s == 0:
        rep["stage"] = "no answer on the dashboard port"
    elif title == "Keephaven Setup":
        rep["stage"] = "waiting for setup (open the dashboard address and finish it)"
    elif "Initializing your cloud" in page:
        rep["stage"] = "starting up after setup"
    elif title == "Keephaven":
        rep["stage"] = "ready"
    else:
        rep["stage"] = f"unexpected page ({s}, title {title!r})"

    tiles = re.findall(r'name: "([^"]+)", desc: "([^"]+)", port: (\d+), health: "([^"]*)"', page)
    rep["edition_apps"] = [f"{n} ({d})" for n, d, _p, _h in tiles]
    apps = {}
    for name, desc, port, health in tiles:
        port = a.photos if port == "2283" else int(port)
        st, _ = get(f"{base}:{port}{health}")
        apps[f"{name} ({desc})"] = "up" if 200 <= st < 400 else ("not reachable from here" if st == 0 else f"HTTP {st}")
    rep["apps"] = apps

    s, body = get(f"{base}:{a.web}/update-status")
    try:
        rep["update_state"] = json.loads(body).get("state") if s == 200 and body.startswith("{") else None
    except ValueError:
        rep["update_state"] = None
    s, body = get(f"{base}:{a.settings}/")
    rep["settings"] = ("waiting for setup" if "Finish setting up first" in body else "up") if s in (200, 403) else "no answer"
    s, body = get(f"{base}:{a.photos}/api/server/version")
    try:
        v = json.loads(body) if s == 200 else None
        rep["immich_version"] = f"{v['major']}.{v['minor']}.{v['patch']}" if v else None
    except (ValueError, KeyError, TypeError):
        rep["immich_version"] = None
    s, _ = get(f"{base}:{a.memory}/v1/health")
    rep["agent_memory"] = "on" if s == 200 else "not on this box"

    if a.json:
        print(json.dumps(rep, indent=1))
        return
    print(f"Keephaven at {a.host}: {rep['stage']}")
    print(f"  settings: {rep['settings']}   update state: {rep['update_state']}")
    for n, st in apps.items():
        print(f"  {n}: {st}")
    print(f"  Immich version: {rep['immich_version']}   agent memory: {rep['agent_memory']}")
    up = sum(1 for st in apps.values() if st == "up")
    print(f"\nreport: {rep['check']} | {rep['checker_os']} | {rep['stage']} | apps up {up}/{len(apps)} "
          f"| immich {rep['immich_version']} | memory {rep['agent_memory']}")


if __name__ == "__main__":
    main()
