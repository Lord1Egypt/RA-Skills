#!/usr/bin/env python3
"""takeout_unpack_watch.py — entpackt fertige Takeout-ZIPs sofort nach Download.

Warum sofort: ZIPs + entpackte Daten = 2x Bibliotheks-Groesse. Wer erst am Ende
entpackt, braucht das Doppelte an Plattenplatz. Der Waechter testet (unzip -t),
entpackt (nice) und loescht jedes verifizierte ZIP sobald es landet.

Endet mit Exit 0, wenn --expected Teile entpackt sind; Exit 2 bei 45 min Stillstand
ohne aktiven aria2c (Warnung, dass der Download-Runner vermutlich haengt).
"""
import argparse
import glob
import os
import subprocess
import time

EXPECTED_MAGIC = b"PK\x03\x04"


def is_zip(p):
    try:
        with open(p, "rb") as f:
            return f.read(4) == EXPECTED_MAGIC
    except Exception:
        return False


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--dir", required=True, help="Ordner mit den Takeout-ZIPs")
    ap.add_argument("--dest", required=True, help="Entpack-Zielordner")
    ap.add_argument("--expected", type=int, default=18, help="Anzahl erwarteter Teile")
    ap.add_argument("--log", default=None, help="Log-Datei (default: <dir>/takeout_unpack.log)")
    args = ap.parse_args()

    os.makedirs(args.dest, exist_ok=True)
    logfile = open(args.log or os.path.join(args.dir, "takeout_unpack.log"), "a", buffering=1)

    def log(m):
        line = f"[{time.strftime('%H:%M:%S')}] {m}"
        print(line, flush=True)
        logfile.write(line + "\n")

    def aria2_active():
        return subprocess.run(["pgrep", "-f", "aria2c.*takeout"],
                              capture_output=True).returncode == 0

    log("=== Entpack-Waechter gestartet ===")
    done = 0
    stall = 0
    while True:
        candidates = [z for z in sorted(glob.glob(os.path.join(args.dir, "*.zip")))
                      if not os.path.exists(z + ".aria2") and is_zip(z)]
        if candidates:
            stall = 0
            for z in candidates:
                name = os.path.basename(z)
                t0 = time.time()
                r = subprocess.run(["unzip", "-t", "-qq", z], capture_output=True, text=True)
                if r.returncode != 0:
                    log(f"  {name}: INTEGRITAET FEHLGESCHLAGEN (rc={r.returncode}) — bleibt liegen")
                    continue
                r = subprocess.run(["nice", "-n", "15", "unzip", "-o", "-qq", z, "-d", args.dest],
                                   capture_output=True, text=True)
                if r.returncode != 0:
                    log(f"  {name}: entpacken fehlgeschlagen (rc={r.returncode}) — bleibt liegen")
                    continue
                os.remove(z)
                for stray in (z + ".aria2",):
                    if os.path.exists(stray):
                        os.remove(stray)
                done += 1
                log(f"  {name}: getestet+entpackt+geloescht in {(time.time() - t0) / 60:.1f} min")
            log(f"Stand: {done}/{args.expected} entpackt")
            if done >= args.expected:
                log(f"=== ALLE {args.expected} TEILE ENTpackt ===")
                return 0
        else:
            if not aria2_active():
                stall += 2
                if stall >= 45:
                    log(f"WARNUNG: 45 min Stillstand ohne aria2c — Wächter beendet sich (Exit 2)")
                    return 2
            else:
                stall = 0
        time.sleep(120)


if __name__ == "__main__":
    import sys
    sys.exit(main())