#!/usr/bin/env python3
"""
Fetch mature miRNA sequences from public databases
==================================================

Gives the toolkit the ability to pull miRNA sequences itself instead of
requiring a hand-made FASTA.

Sources, tried in order (first success wins)
--------------------------------------------
1. --mature-fa            a local miRBase mature.fa you already have
2. cache                  ~/.cache/mirna-target-tools/mature.fa (from an earlier run)
3. miRBase download       https://www.mirbase.org/download/mature.fa (+ mirrors)
4. RNAcentral             https://rnacentral.org/api/v1/rna (name search fallback)

Usage
-----
  # all mature miRNAs of a species (species name or miRBase prefix both work)
  python fetch_mirnas.py --species goat --out goat_mirnas.fa
  python fetch_mirnas.py --species chi  --list            # just list them

  # a few specific miRNAs by name (species prefix optional)
  python fetch_mirnas.py --names miR-21-5p,chi-miR-504-5p --out picked.fa

  # refresh / pre-seed the cached miRBase release
  python fetch_mirnas.py --update

Notes
-----
* The bulk miRBase file needs network access to mirbase.org. If that is blocked,
  supply --mature-fa (a mature.fa you downloaded elsewhere) or --names with
  --source rnacentral; both are cached locally afterwards.
* Sequences are written as RNA (U, not T). The predictor normalises them itself.

Dependencies: standard library only.
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "mirna-target-tools")
MATURE_CACHE = os.path.join(CACHE_DIR, "mature.fa")

MIRBASE_URLS = [
    "https://www.mirbase.org/download/mature.fa",
    "https://mirbase.org/download/mature.fa",
    "https://www.mirbase.org/ftp/CURRENT/mature.fa",
    "ftp://mirbase.org/pub/mirbase/CURRENT/mature.fa",
]
RNACENTRAL_API = "https://rnacentral.org/api/v1/rna/"

# species name <-> miRBase (and genome) prefix
SPECIES_PREFIXES = {
    "human": "hsa", "mouse": "mmu", "rat": "rno", "sheep": "oar",
    "goat": "chi", "cow": "bta", "pig": "ssc", "chicken": "gga",
}


def species_prefix(name):
    """Accept 'goat', 'chi', 'Chi-miR-504' -> 'chi'."""
    key = str(name).strip().lower()
    if key in SPECIES_PREFIXES:
        return SPECIES_PREFIXES[key]
    if key in SPECIES_PREFIXES.values():
        return key
    if len(key) == 3:
        return key
    raise SystemExit("Error: unknown species '%s' (known: %s)"
                     % (name, ", ".join(sorted(SPECIES_PREFIXES))))


# --------------------------------------------------------------------------
# getting a mature.fa
# --------------------------------------------------------------------------
def download_mature(force=False, verbose=True):
    """Download miRBase mature.fa into the cache. Returns path or None."""
    if os.path.exists(MATURE_CACHE) and not force:
        if verbose:
            print("Using cached miRBase file: %s (%.1f MB)"
                  % (MATURE_CACHE, os.path.getsize(MATURE_CACHE) / 1e6))
        return MATURE_CACHE
    os.makedirs(CACHE_DIR, exist_ok=True)
    for url in MIRBASE_URLS:
        try:
            if verbose:
                print("Trying %s ..." % url)
            req = urllib.request.Request(url, headers={"User-Agent": "mirna-target-tools/3.0"})
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = resp.read()
            if len(data) < 100000:
                raise RuntimeError("suspiciously small file (%d bytes)" % len(data))
            tmp = MATURE_CACHE + ".part"
            with open(tmp, "wb") as fh:
                fh.write(data)
            os.replace(tmp, MATURE_CACHE)
            if verbose:
                print("Saved %s (%.1f MB)" % (MATURE_CACHE, len(data) / 1e6))
            return MATURE_CACHE
        except Exception as exc:
            if verbose:
                print("  failed: %s" % exc)
    return None


def mature_path(local=None, allow_download=True, verbose=True):
    """Resolve a mature.fa: explicit path > cache > download."""
    if local:
        if not os.path.exists(local):
            raise SystemExit("Error: --mature-fa %s not found" % local)
        return local
    if os.path.exists(MATURE_CACHE):
        if verbose:
            print("Using cached miRBase file: %s" % MATURE_CACHE)
        return MATURE_CACHE
    if allow_download:
        return download_mature(verbose=verbose)
    return None


# --------------------------------------------------------------------------
# parsing / selecting
# --------------------------------------------------------------------------
def parse_mature(path):
    """[(name, sequence)] from a miRBase mature.fa (name = first header token)."""
    out, name = [], None
    with open(path, errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith(">"):
                name = line[1:].split()[0]
            elif line.strip() and name:
                seq = line.strip().upper().replace("T", "U")
                if 15 <= len(seq) <= 30 and re.fullmatch(r"[ACGU]+", seq):
                    out.append((name, seq))
    return out


def split_name(name):
    """'chi-miR-504-5p' -> ('chi', 'miR-504-5p'); 'miR-21-5p' -> (None, ...)."""
    if "-" in name:
        prefix, rest = name.split("-", 1)
        if prefix in SPECIES_PREFIXES.values():
            return prefix, rest
        return None, name
    return None, name


def select(entries, names=None, species=None):
    """Filter (name, seq) entries. Returns (hits, notes)."""
    notes = []
    if species:
        pre = species_prefix(species)
        hits = [e for e in entries if e[0].startswith(pre + "-")]
        notes.append("%s (%s): %d mature miRNAs" % (species, pre, len(hits)))
        return hits, notes
    hits, missing = [], []
    for want in names or []:
        want = want.strip()
        if not want:
            continue
        pre, rest = split_name(want)
        matched = []
        for nm, sq in entries:
            epre, erest = split_name(nm)
            if erest != rest:
                continue
            if pre and epre != pre:
                continue
            matched.append((nm, sq))
        if matched:
            # prefer the requested species when a bare name matched several
            if pre:
                matched = [m for m in matched if split_name(m[0])[0] == pre]
            hits.extend(matched)
            notes.append("%s -> %s" % (want, ", ".join(m[0] for m in matched)))
        else:
            missing.append(want)
    if missing:
        notes.append("MISSING: %s" % ", ".join(missing))
    return hits, notes


def fetch_from_rnacentral(names):
    """Best-effort fallback: look a miRNA up in RNAcentral by name."""
    hits = []
    for want in names:
        url = "%s?q=%s&format=json&rna_type=miRNA" % (RNACENTRAL_API, urllib.parse.quote(want))
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "mirna-target-tools/3.0"})
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except Exception as exc:
            print("  RNAcentral lookup of %s failed: %s" % (want, exc))
            continue
        for item in data.get("results", []):
            seq = (item.get("sequence") or "").upper().replace("T", "U")
            desc = str(item.get("description") or "")
            if 15 <= len(seq) <= 30 and re.fullmatch(r"[ACGU]+", seq):
                hits.append((desc.split()[0] if desc else want, seq))
                break
    return hits


def write_fasta(path, entries):
    with open(path, "w") as fh:
        for name, seq in entries:
            fh.write(">%s\n%s\n" % (name, seq))


def main():
    ap = argparse.ArgumentParser(
        description="Fetch mature miRNA sequences from public databases")
    ap.add_argument("--species", help="all mature miRNAs of a species (name or prefix, e.g. goat/chi)")
    ap.add_argument("--names", help="comma-separated miRNA names (species prefix optional)")
    ap.add_argument("--names-file", help="file with one miRNA name per line")
    ap.add_argument("--out", help="write a FASTA here (default: stdout summary only)")
    ap.add_argument("--list", action="store_true", help="list the selected miRNAs")
    ap.add_argument("--mature-fa", help="local miRBase mature.fa to use")
    ap.add_argument("--source", default="auto", choices=["auto", "mirbase", "rnacentral"],
                    help="auto (local/cache/miRBase, RNAcentral as fallback), mirbase, rnacentral")
    ap.add_argument("--update", action="store_true", help="re-download the cached miRBase file")
    args = ap.parse_args()

    if not args.species and not args.names and not args.names_file:
        ap.error("give --species, --names or --names-file")

    names = []
    if args.names:
        names += [n for n in args.names.split(",") if n.strip()]
    if args.names_file:
        with open(args.names_file) as fh:
            names += [l.strip() for l in fh if l.strip()]

    path = None
    if args.source in ("auto", "mirbase"):
        if args.update:
            path = download_mature(force=True)
        else:
            path = mature_path(args.mature_fa, allow_download=True)

    if path:
        entries = parse_mature(path)
        print("miRBase entries: %d (%s)" % (len(entries), path))
        hits, notes = select(entries, names, args.species)
        for n in notes:
            print("  " + n)
    else:
        hits, notes = [], []
        print("miRBase is unavailable (no local file, download failed).")

    if not hits and args.source in ("auto", "rnacentral") and names:
        print("Falling back to RNAcentral name lookups ...")
        hits = fetch_from_rnacentral(names)
        if hits:
            hits, _ = select(hits, names, None)

    if not hits:
        print("\nNo miRNA sequences obtained.")
        print("How to fix:")
        print("  * put a miRBase mature.fa somewhere and pass --mature-fa /path/to/mature.fa")
        print("  * or give your own FASTA directly to the predictor (--mirna-fa)")
        return 1

    print("\nSelected %d sequence(s):" % len(hits))
    for nm, sq in (hits if args.list else hits[:10]):
        print("  %-24s %2d nt  %s" % (nm, len(sq), sq[:40]))
    if not args.list and len(hits) > 10:
        print("  ... (%d more)" % (len(hits) - 10))

    if args.out:
        write_fasta(args.out, hits)
        print("\nFASTA written to %s" % args.out)
    return 0


if __name__ == "__main__":
    import urllib.parse
    sys.exit(main())
