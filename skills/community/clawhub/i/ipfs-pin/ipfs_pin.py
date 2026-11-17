#!/usr/bin/env python3
"""ipfs-pin: OpenClaw plugin skill for IPFS content lifecycle.

Adds files to a local kubo IPFS node, pins them, and tracks them in a
ledger. Pinned content stays alive while referenced; `decay` unpins
entries whose TTL has elapsed since last reference and garbage-collects
the repo, so content decays naturally when no longer needed.

Security posture (mirrors jerithchain skill):
  - never invents CIDs: everything reported comes from the `ipfs` CLI
  - subprocess only with argv lists, shell=False, no eval/exec
  - ledger writes are atomic (tmp file + rename)
"""

import argparse
import fcntl
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.environ.get("IPFS_PIN_STATE_DIR",
                           os.path.expanduser("~/.openclaw/ipfs-pin"))
LEDGER_PATH = os.path.join(STATE_DIR, "ledger.json")
CONFIG_PATH = os.path.join(STATE_DIR, "config.json")
LOCK_PATH = os.path.join(STATE_DIR, "decay.lock")

LEDGER_VERSION = 1
DEFAULT_TTL_HOURS = 72


def _fail(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def _state_dir():
    os.makedirs(STATE_DIR, exist_ok=True)
    return STATE_DIR


def load_config():
    cfg = {"default_ttl_hours": DEFAULT_TTL_HOURS}
    try:
        with open(CONFIG_PATH) as f:
            cfg.update(json.load(f))
    except FileNotFoundError:
        pass
    except (json.JSONDecodeError, OSError) as e:
        _fail(f"config unreadable at {CONFIG_PATH}: {e}")
    return cfg


def load_ledger():
    try:
        with open(LEDGER_PATH) as f:
            ledger = json.load(f)
    except FileNotFoundError:
        return {"version": LEDGER_VERSION, "entries": {}}
    except (json.JSONDecodeError, OSError) as e:
        _fail(f"ledger unreadable at {LEDGER_PATH}: {e}")
    if ledger.get("version") != LEDGER_VERSION or not isinstance(ledger.get("entries"), dict):
        _fail(f"ledger format unrecognized at {LEDGER_PATH}")
    return ledger


def save_ledger(ledger):
    _state_dir()
    fd, tmp = tempfile.mkstemp(dir=STATE_DIR, prefix=".ledger-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(ledger, f, indent=2, sort_keys=True)
            f.write("\n")
        os.replace(tmp, LEDGER_PATH)
    except OSError as e:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        _fail(f"could not write ledger: {e}")


def run_ipfs(args, check=True):
    """Run `ipfs <args>`; returns CompletedProcess. argv list only, shell=False."""
    ipfs_bin = shutil.which("ipfs") or os.path.expanduser("~/bin/ipfs")
    if not (ipfs_bin and os.path.isfile(ipfs_bin) and os.access(ipfs_bin, os.X_OK)):
        _fail("`ipfs` binary not found in PATH or ~/bin/ipfs (required by this skill)")
    return subprocess.run([ipfs_bin] + args, capture_output=True, text=True,
                          check=False)


def ipfs_out(args):
    proc = run_ipfs(args)
    if proc.returncode != 0:
        _fail(f"`ipfs {' '.join(args)}` failed: {proc.stderr.strip() or proc.stdout.strip()}")
    return proc.stdout


def ipfs_alive():
    proc = run_ipfs(["id"])
    return proc.returncode == 0 and proc.stdout.strip() != ""


def cid_lookup(cid, ledger):
    """True if ledger already tracks this CID (existing pin gets refreshed)."""
    return cid in ledger["entries"]


def expires_at_of(entry):
    return entry["last_referenced"] + entry["ttl_hours"] * 3600


def now_iso(ts):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))


# ---------------------------------------------------------------- commands

def cmd_add(args):
    if not os.path.exists(args.path):
        _fail(f"path does not exist: {args.path}")
    if not ipfs_alive():
        _fail("IPFS daemon not reachable (systemctl --user status ipfs)")

    ttl = args.ttl if args.ttl is not None else load_config()["default_ttl_hours"]
    if ttl <= 0:
        _fail("--ttl must be positive")

    proc = run_ipfs(["add", "--pin", "-Q", "--", args.path])
    if proc.returncode != 0:
        _fail(f"ipfs add failed: {proc.stderr.strip() or proc.stdout.strip()}")
    cid = proc.stdout.strip().splitlines()[-1].strip()
    if not cid:
        _fail("ipfs add returned no CID")

    size = os.path.getsize(args.path)
    name = args.name or os.path.basename(args.path)
    now = time.time()

    ledger = load_ledger()
    entry = ledger["entries"].get(cid)
    if entry:
        # re-adding same content: refresh rather than duplicate
        entry["last_referenced"] = now
        entry["name"] = name
        entry["ttl_hours"] = ttl
    else:
        ledger["entries"][cid] = {
            "name": name,
            "path": os.path.abspath(args.path),
            "size": size,
            "added_at": now,
            "last_referenced": now,
            "ttl_hours": ttl,
        }
    save_ledger(ledger)

    out = {"cid": cid, "name": name, "ttl_hours": ttl,
           "expires_at": now_iso(expires_at_of(ledger["entries"][cid]))}
    print(json.dumps(out) if args.json else
          f"pinned {cid} ({name}, {size} bytes, decays after {out['expires_at']})")


def cmd_ls(args):
    ledger = load_ledger()
    rows = []
    now = time.time()
    for cid, e in sorted(ledger["entries"].items(), key=lambda kv: kv[1]["last_referenced"]):
        rem_h = (expires_at_of(e) - now) / 3600
        rows.append({"cid": cid, "name": e["name"], "size": e["size"],
                     "ttl_hours": e["ttl_hours"],
                     "hours_remaining": round(rem_h, 2),
                     "expires_at": now_iso(expires_at_of(e))})
    if args.json:
        print(json.dumps(rows))
    elif not rows:
        print("(ledger empty)")
    else:
        for r in rows:
            mark = "EXPIRED" if r["hours_remaining"] <= 0 else f"{r['hours_remaining']}h left"
            print(f"{r['cid']}  {r['name']}  {r['size']}B  TTL {r['ttl_hours']}h  {mark}")


def cmd_touch(args):
    ledger = load_ledger()
    entry = ledger["entries"].get(args.cid)
    if not entry:
        _fail(f"CID not in ledger: {args.cid} (use `add` first)")
    entry["last_referenced"] = time.time()
    save_ledger(ledger)
    out = {"cid": args.cid, "expires_at": now_iso(expires_at_of(entry))}
    print(json.dumps(out) if args.json else
          f"refreshed {args.cid}, now decays after {out['expires_at']}")


def cmd_rm(args):
    ledger = load_ledger()
    if args.cid not in ledger["entries"]:
        _fail(f"CID not in ledger: {args.cid}")
    proc = run_ipfs(["pin", "rm", args.cid])
    # unpin failure is non-fatal for bookkeeping only if pin already gone;
    # otherwise surface it.
    if proc.returncode != 0 and "not pinned" not in (proc.stderr + proc.stdout):
        _fail(f"ipfs pin rm failed: {proc.stderr.strip() or proc.stdout.strip()}")
    if not args.no_gc:
        run_ipfs(["repo", "gc"])
    del ledger["entries"][args.cid]
    save_ledger(ledger)
    out = {"cid": args.cid, "removed": True}
    print(json.dumps(out) if args.json else f"unpinned and removed {args.cid}")


def cmd_decay(args):
    _state_dir()
    lock = open(LOCK_PATH, "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        if not args.quiet:
            print("decay already running elsewhere; skipping")
        return
    try:
        _decay_locked(args)
    finally:
        fcntl.flock(lock, fcntl.LOCK_UN)
        lock.close()


def _decay_locked(args):
    ledger = load_ledger()
    now = time.time()
    expired = {cid: e for cid, e in ledger["entries"].items()
               if expires_at_of(e) <= now}
    if args.dry_run:
        rows = [{"cid": cid, "name": e["name"], "expired_at": now_iso(expires_at_of(e))}
                for cid, e in expired.items()]
        print(json.dumps(rows) if args.json else
              ("(dry-run) would decay:\n" + "\n".join(
                  f"  {r['cid']}  {r['name']}" for r in rows) if rows else "(dry-run) nothing to decay"))
        return
    decayed = []
    for cid, e in expired.items():
        proc = run_ipfs(["pin", "rm", cid])
        err = (proc.stderr + proc.stdout).lower()
        # tolerate: already-unpinned, or CID not on this node at all —
        # both mean there is nothing left to protect; delete bookkeeping.
        if proc.returncode != 0 and not ("not pinned" in err or "path does not" in err):
            _fail(f"ipfs pin rm {cid} failed: {proc.stderr.strip() or proc.stdout.strip()}")
        del ledger["entries"][cid]
        decayed.append({"cid": cid, "name": e["name"]})
    if decayed:
        save_ledger(ledger)
        gc = run_ipfs(["repo", "gc"])
        if gc.returncode != 0:
            _fail(f"ipfs repo gc failed: {gc.stderr.strip()}")
    if args.json:
        print(json.dumps({"decayed": decayed, "count": len(decayed)}))
    elif not args.quiet:
        if decayed:
            for d in decayed:
                print(f"decayed {d['cid']} ({d['name']})")
        else:
            print("nothing to decay")
        print(f"pinned entries remaining: {len(ledger['entries'])}")


def cmd_get(args):
    if not ipfs_alive():
        _fail("IPFS daemon not reachable (get via local node)")
    if args.out:
        proc = run_ipfs(["get", args.cid, "-o", args.out])
        if proc.returncode != 0:
            _fail(f"ipfs get failed: {proc.stderr.strip() or proc.stdout.strip()}")
        if not args.json:
            print(f"wrote {args.out}")
        return
    proc = run_ipfs(["cat", args.cid])
    if proc.returncode != 0:
        _fail(f"ipfs cat failed (block may be garbage-collected locally): "
              f"{proc.stderr.strip() or proc.stdout.strip()}")
    sys.stdout.write(proc.stdout)


def _repo_stat_fields(text):
    """Parse `ipfs repo stat` human-format output into a dict."""
    fields = {}
    for line in text.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            k = k.strip()
            try:
                fields[k] = int(v.strip())
            except ValueError:
                fields[k] = v.strip()
    return fields


def cmd_status(args):
    if not ipfs_alive():
        out = {"daemon": "down"}
        print(json.dumps(out) if args.json else "IPFS daemon: DOWN (systemctl --user status ipfs)")
        return
    repo = _repo_stat_fields(ipfs_out(["repo", "stat"]))
    pins_raw = ipfs_out(["pin", "ls", "--quiet"])
    pins = [l.strip() for l in pins_raw.splitlines() if l.strip()]
    ledger = load_ledger()
    fed = [p for p in pins if p in ledger["entries"]]
    untracked = [p for p in pins if p not in ledger["entries"]]
    out = {
        "daemon": "up",
        "repo_size_bytes": repo.get("RepoSize"),
        "storage_max_bytes": repo.get("StorageMax"),
        "ipfs_pins": len(pins),
        "ledger_entries": len(ledger["entries"]),
        "ledger_untracked_pins": len(untracked),
    }
    if args.json:
        print(json.dumps(out))
    else:
        gb = out["repo_size_bytes"] / 1e9
        maxgb = out["storage_max_bytes"] / 1e9
        print(f"daemon: up | repo: {gb:.3f}GB / {maxgb:.0f}GB | "
              f"pins: {out['ipfs_pins']} (ledger-tracked {len(fed)}, untracked {len(untracked)})")
        if untracked:
            print("untracked pins (pinned on node but not in ledger, e.g. manual `ipfs add`):")
            for p in untracked[:10]:
                print(f"  {p}")


def cmd_config_show(args):
    print(json.dumps(load_config()) if args.json else
          f"default_ttl_hours: {load_config()['default_ttl_hours']}")
def cmd_config_set(args):
    if args.default_ttl_hours is not None:
        if args.default_ttl_hours <= 0:
            _fail("default_ttl_hours must be positive")
        _state_dir()
        cfg = load_config()
        cfg["default_ttl_hours"] = args.default_ttl_hours
        tmp = CONFIG_PATH + ".tmp"
        with open(tmp, "w") as f:
            json.dump(cfg, f, indent=2, sort_keys=True)
            f.write("\n")
        os.replace(tmp, CONFIG_PATH)
    out = load_config()
    print(json.dumps(out) if args.json else
          f"default_ttl_hours: {out['default_ttl_hours']}")


# ---------------------------------------------------------------- argparse

def build_parser():
    p = argparse.ArgumentParser(prog="ipfs_pin", description=__doc__)
    p.add_argument("--json", action="store_true", help="structured output")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="add+pin a file (starts or refreshes its TTL)")
    a.add_argument("path")
    a.add_argument("--name")
    a.add_argument("--ttl", type=float, help="hours until decay, overrides default")
    a.set_defaults(fn=cmd_add)

    sub.add_parser("ls", help="list ledger entries").set_defaults(fn=cmd_ls)

    t = sub.add_parser("touch", help="refresh last_referenced (content survives)")
    t.add_argument("cid")
    t.set_defaults(fn=cmd_touch)

    r = sub.add_parser("rm", help="unpin now and remove from ledger")
    r.add_argument("cid")
    r.add_argument("--no-gc", action="store_true")
    r.set_defaults(fn=cmd_rm)

    d = sub.add_parser("decay", help="unpin entries past TTL, then repo gc")
    d.add_argument("--dry-run", action="store_true")
    d.add_argument("--quiet", action="store_true")
    d.set_defaults(fn=cmd_decay)

    g = sub.add_parser("get", help="retrieve content by CID from local node")
    g.add_argument("cid")
    g.add_argument("-o", "--out", help="write to path instead of stdout")
    g.set_defaults(fn=cmd_get)

    sub.add_parser("status", help="daemon/repo/ledger overview").set_defaults(fn=cmd_status)

    cs = sub.add_parser("config", help="show/set skill config")
    cs.add_argument("--default-ttl-hours", type=float)
    cs.set_defaults(fn=cmd_config_show, set_fn=cmd_config_set)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    # `config --default-ttl-hours 24` mutates; plain `config` shows
    if getattr(args, "set_fn", None) is not None and getattr(args, "default_ttl_hours", None) is not None:
        args.set_fn(args)
    else:
        args.fn(args)


if __name__ == "__main__":
    main()
