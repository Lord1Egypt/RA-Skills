#!/usr/bin/env python3
"""
Whole-transcriptome miRNA target prediction
===========================================

Predict target sites of one or more mature miRNAs across the **entire mRNA
(transcriptome) of a species** - no pre-built TargetScan database needed.

Two prediction engines
----------------------
* **seed**   - canonical TargetScan seed-site matching (8mer / 7mer-m8 /
               7mer-A1 / 6mer). Fast, transparent, but a seed heuristic only:
               it is the TargetScan site *definition*, without the context++
               model (that model needs pre-computed multi-species UTR
               alignments and only exists for TargetScan's own species list,
               which excludes sheep/goat).
* **miranda** - run miRanda (Enright et al. 2003) over every miRNA x
               transcript pair: full duplex alignment with an empirical
               thermodynamic model (score + dG). Sequence-based, so it works
               for any species, but slower and more permissive on its own.
* **hybrid**  - (recommended, the default when miRanda is installed) seed sites
               are kept only when a miRanda alignment overlaps them, and each
               confirmed site carries its miRanda score and dG. This combines
               the precise seed definition with thermodynamic evidence.
* **auto**    - hybrid when miRanda is available, otherwise seed.

Target region
-------------
* --target-region cdna  scan the full spliced transcript (default for custom
                        FASTA input)
* --target-region utr   scan only the **3'UTR**, derived from the annotation
                        (GTF) plus the cDNA - miRNA targeting is 3'UTR
                        dominant, so this is the biologically faithful choice.
                        The GTF is downloaded automatically for built-in
                        species, or supplied with --gtf.

Target sources (choose one)
---------------------------
1. Built-in species preset, auto-downloaded from Ensembl and cached:
       --species human            (see --list-species for the full list)
2. Your own mRNA/cDNA FASTA:
       --mrna-fa my_transcripts.fa
3. Your own genome + GTF annotation (mRNA rebuilt by joining exons):
       --genome-fa genome.fa --gtf annotation.gtf

miRNA source (choose one)
-------------------------
* --mirna-fa mirna.fa   FASTA of mature miRNA sequences (name + sequence)
* --mirna miR-21-5p     a single name resolved from miRBase (cached)

Outputs
-------
{prefix}_sites.tsv        one row per predicted site
{prefix}_targets.tsv      one row per (miRNA, transcript), ranked by score
{prefix}_miranda.tsv      raw miRanda hits (when miRanda is used)
{prefix}_run_info.tsv     run metadata (source, engine, parameters)

Dependencies: standard library only; miRanda is optional (external binary).
"""

import argparse
import gzip
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request

CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "mirna-target-tools")
GENOME_CACHE = os.path.join(CACHE_DIR, "genomes")
MIRBASE_URL = "https://www.mirbase.org/download/mature.fa"
ENSEMBL_BASE = "https://ftp.ensembl.org/pub"

SPECIES_PRESETS = {
    "human": ("homo_sapiens", "GRCh38", ["hsa", "human", "hs"]),
    "mouse": ("mus_musculus", "GRCm39", ["mmu", "mouse"]),
    "rat": ("rattus_norvegicus", "mRatBN7.2", ["rno", "rat"]),
    "sheep": ("ovis_aries", "ARS-UI_Ramb_v3.0", ["oar", "sheep"]),
    "goat": ("capra_hircus", "ARS1", ["chi", "goat"]),
    "cow": ("bos_taurus", "ARS-UCD2.0", ["bta", "cow", "cattle"]),
    "pig": ("sus_scrofa", "Sscrofa11.1", ["ssc", "pig"]),
    "chicken": ("gallus_gallus", "GRCg7b", ["gga", "chicken"]),
}

SITE_WEIGHT = {"8mer": 4.0, "7mer-m8": 3.0, "7mer-A1": 2.0, "6mer": 1.0}
SITE_RANK = {"6mer": 1, "7mer-A1": 2, "7mer-m8": 3, "8mer": 4}
COMPLEMENT = {"A": "T", "T": "A", "U": "A", "C": "G", "G": "C", "N": "N"}


# --------------------------------------------------------------------------
# sequence helpers
# --------------------------------------------------------------------------
def revcomp(seq):
    return "".join(COMPLEMENT.get(c, "N") for c in reversed(seq))


def normalize_dna(seq):
    """Uppercase, DNA alphabet; U -> T; anything unknown -> N."""
    return "".join(c if c in "ACGT" else "N"
                   for c in seq.upper().replace("U", "T"))


def normalize_mirna(seq):
    return "".join(c if c in "ACGT" else "N" for c in seq.upper().replace("U", "T"))


def open_maybe_gz(path):
    return gzip.open(path, "rt") if path.endswith(".gz") else open(path, "rt")


def parse_fasta(path):
    records = []
    name, parts = None, []
    with open_maybe_gz(path) as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith(">"):
                if name is not None:
                    records.append((name, "".join(parts)))
                name, parts = line[1:].strip(), []
            elif line.strip():
                parts.append(line.strip())
    if name is not None:
        records.append((name, "".join(parts)))
    return records


def write_fasta(path, records):
    with open(path, "w") as fh:
        for name, seq in records:
            fh.write(">%s\n" % name)
            for i in range(0, len(seq), 60):
                fh.write(seq[i:i + 60] + "\n")


def strip_version(ident):
    """Ensembl IDs: cDNA FASTA headers carry '.1' versions, GTF attributes do
    not (the version lives in a separate transcript_version field)."""
    return re.sub(r"[.]\d+$", "", str(ident))


def parse_ensembl_header(header):
    fields = header.split()
    tx = fields[0]
    gene_id = gene = ""
    for f in fields[1:]:
        if f.startswith("gene:"):
            gene_id = f[5:].split(".")[0]
        elif f.startswith("gene_symbol:"):
            gene = f[12:]
    return tx, gene_id, gene


# --------------------------------------------------------------------------
# seed-site scanning (TargetScan site definitions)
# --------------------------------------------------------------------------
def find_sites(mrna, mirna):
    """Return a sorted list of (site_start_0based, site_type) for one miRNA."""
    core6 = revcomp(mirna[1:7]) if len(mirna) >= 7 else ""
    core7 = revcomp(mirna[1:8]) if len(mirna) >= 8 else ""

    sites = {}

    def keep(start, site_type):
        if start < 0:
            return
        cur = sites.get(start)
        if cur is None or SITE_RANK[site_type] > SITE_RANK[cur]:
            sites[start] = site_type

    if core7 and core7 in mrna:
        i = mrna.find(core7)
        while i >= 0:
            keep(i - 1, "8mer" if (i > 0 and mrna[i - 1] == "A") else "7mer-m8")
            i = mrna.find(core7, i + 1)
    if core6 and core6 in mrna:
        i = mrna.find(core6)
        while i >= 0:
            # core7 = complement(nt8) + core6, so a longer match starting at
            # i-1 already covers this 6mer core - do not double-count it
            if not (core7 and i > 0 and mrna[i - 1:i + 6] == core7):
                keep(i - 1, "7mer-A1" if (i > 0 and mrna[i - 1] == "A") else "6mer")
            i = mrna.find(core6, i + 1)
    return sorted(sites.items())


def site_sequence(mrna, start, site_type):
    length = 8 if site_type in ("8mer", "7mer-m8") else 7
    return mrna[start:start + length]


# --------------------------------------------------------------------------
# target sources
# --------------------------------------------------------------------------
def resolve_species(key):
    k = key.strip().lower()
    if k in SPECIES_PRESETS:
        return k, SPECIES_PRESETS[k]
    for name, (slug, asm, aliases) in SPECIES_PRESETS.items():
        if k == slug or k in aliases:
            return name, (slug, asm, aliases)
    return None, None


def list_species():
    print("Built-in species presets (Ensembl cDNA + GTF, downloaded and cached):")
    for name, (slug, asm, aliases) in sorted(SPECIES_PRESETS.items()):
        print("  %-8s %-20s %-22s aliases: %s"
              % (name, slug, asm, ",".join(aliases)))
    print("\nUse --species <name-or-alias>, or supply --mrna-fa / --genome-fa+--gtf.")


def _list_dir(subdir, pattern):
    """List matching file names in an Ensembl /pub/current subdirectory."""
    listing = "%s/current/%s/" % (ENSEMBL_BASE, subdir)
    req = urllib.request.Request(listing, headers={"User-Agent": "mirna-target-tools/2.1"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        html = resp.read().decode("utf-8", "replace")
    return listing, sorted(set(re.findall(pattern, html)))


def _discover(subdir, pattern):
    """subdir is the Ensembl path under /pub/current, e.g. 'gtf/capra_hircus'."""
    listing, names = _list_dir(subdir, pattern)
    if not names:
        raise RuntimeError("nothing matching %s at %s" % (pattern, listing))
    return listing + names[0], names[0]


def _download(url, dest):
    print("Downloading %s" % url)
    tmp = dest + ".part"
    req = urllib.request.Request(url, headers={"User-Agent": "mirna-target-tools/2.1"})
    with urllib.request.urlopen(req, timeout=900) as resp, open(tmp, "wb") as out:
        total = 0
        while True:
            chunk = resp.read(1 << 20)
            if not chunk:
                break
            out.write(chunk)
            total += len(chunk)
            if total % (100 << 20) < (1 << 20):
                print("  ... %.0f MB" % (total / 1e6))
    os.replace(tmp, dest)
    print("Saved %s (%.1f MB)" % (dest, os.path.getsize(dest) / 1e6))
    return dest


def fetch_cdna(slug, cache_dir, refresh=False):
    os.makedirs(cache_dir, exist_ok=True)
    url, fname = _discover("fasta/%s/cdna" % slug,
                           r"([A-Za-z0-9._-]+\.cdna\.all\.fa\.gz)")
    dest = os.path.join(cache_dir, fname)
    if os.path.exists(dest) and not refresh:
        print("Using cached cDNA: %s (%.1f MB)" % (dest, os.path.getsize(dest) / 1e6))
        return dest
    return _download(url, dest)


def fetch_gtf(slug, cache_dir, refresh=False):
    """Fetch the GTF annotation, preferring the complete one over chr/abinitio
    (the complete file also covers scaffold- and patch-placed transcripts, which
    the cDNA FASTA contains)."""
    os.makedirs(cache_dir, exist_ok=True)
    listing, names = _list_dir("gtf/%s" % slug, r"([A-Za-z0-9._-]+\.gtf\.gz)")
    if not names:
        raise RuntimeError("no GTF found at %s" % listing)

    def rank(n):
        if ".abinitio." in n:
            return 2
        return 1 if ".chr." in n else 0

    best = sorted(names, key=rank)[0]
    dest = os.path.join(cache_dir, best)
    if os.path.exists(dest) and not refresh:
        print("Using cached GTF: %s (%.1f MB)" % (dest, os.path.getsize(dest) / 1e6))
        return dest
    return _download(listing + best, dest)


def load_genome(path):
    print("Loading genome %s ..." % path)
    genome = {h.split()[0]: normalize_dna(s) for h, s in parse_fasta(path)}
    print("  %d sequences" % len(genome))
    return genome


def transcripts_from_gtf(gtf_path, genome):
    """Rebuild mRNA sequences by joining exons (strand-aware) from a GTF."""
    print("Reading annotation %s ..." % gtf_path)
    exons = {}
    with open_maybe_gz(gtf_path) as fh:
        for line in fh:
            if not line or line.startswith("#"):
                continue
            f = line.rstrip("\n").split("\t")
            if len(f) < 9 or f[2] != "exon":
                continue
            attrs = dict(re.findall(r'(\w+)\s+"([^"]*)"', f[8]))
            tid = attrs.get("transcript_id")
            if not tid:
                continue
            exons.setdefault(tid, {
                "chrom": f[0], "strand": f[6],
                "gene_id": attrs.get("gene_id", ""),
                "gene_name": attrs.get("gene_name") or attrs.get("gene", ""),
                "parts": [],
            })["parts"].append((int(f[3]), int(f[4])))

    records, skipped = [], 0
    for tid, info in exons.items():
        chrom = genome.get(info["chrom"])
        if chrom is None:
            skipped += 1
            continue
        seq = "".join(chrom[s - 1:e] for s, e in sorted(info["parts"]))
        if info["strand"] == "-":
            seq = revcomp(seq)
        records.append((tid, info["gene_id"], info["gene_name"], normalize_dna(seq)))
    if skipped:
        print("  warning: %d transcripts skipped (chromosome not in genome)" % skipped)
    print("  %d transcripts" % len(records))
    return records


# --------------------------------------------------------------------------
# 3'UTR extraction from a GTF (no genome download needed)
# --------------------------------------------------------------------------
def load_gtf_structure(gtf_path):
    """Return {transcript_id: {...exons, cds...}} from a GTF."""
    print("Reading annotation for 3'UTR extraction: %s ..." % gtf_path)
    tx = {}
    with open_maybe_gz(gtf_path) as fh:
        for line in fh:
            if not line or line.startswith("#"):
                continue
            f = line.rstrip("\n").split("\t")
            if len(f) < 9 or f[2] not in ("exon", "CDS"):
                continue
            attrs = dict(re.findall(r'(\w+)\s+"([^"]*)"', f[8]))
            tid = attrs.get("transcript_id")
            if not tid:
                continue
            tid = strip_version(tid)
            rec = tx.setdefault(tid, {
                "strand": f[6],
                "gene_id": attrs.get("gene_id", ""),
                "gene_name": attrs.get("gene_name") or attrs.get("gene", ""),
                "exons": [], "cds": [],
            })
            rec["exons" if f[2] == "exon" else "cds"].append((int(f[3]), int(f[4])))
    print("  %d transcripts in annotation" % len(tx))
    return tx


def utr3_lengths(info):
    """(five_utr_bases, three_utr_bases) in cDNA coordinates, or None if non-coding."""
    exons = sorted(info["exons"])
    if not exons or not info["cds"]:
        return None
    cds = sorted(info["cds"])
    cds_lo, cds_hi = cds[0][0], cds[-1][1]
    cds_len = sum(e - s + 1 for s, e in cds)
    if info["strand"] == "+":
        five = sum(max(0, min(e, cds_lo) - s) for s, e in exons if s < cds_lo)
        three = sum(max(0, e - max(s, cds_hi)) for s, e in exons if e > cds_hi)
    else:
        five = sum(max(0, e - max(s, cds_hi)) for s, e in exons if e > cds_hi)
        three = sum(max(0, min(e, cds_lo) - s) for s, e in exons if s < cds_lo)
    return five, cds_len, three


def slice_utr3(cdna, info):
    """Return (sequence, status). status: ok | noncoding | mismatch."""
    try:
        lens = utr3_lengths(info)
    except Exception:
        return cdna, "mismatch"
    if lens is None:
        return cdna, "noncoding"
    five, cds_len, three = lens
    if three == 0:
        return cdna, "mismatch"
    # the annotation is only trusted when 5'UTR + CDS + 3'UTR rebuilds the cDNA
    if abs((five + cds_len + three) - len(cdna)) > 3:
        return cdna, "mismatch"
    return cdna[len(cdna) - three:], "ok"


# --------------------------------------------------------------------------
# miRanda engine
# --------------------------------------------------------------------------
def miranda_path():
    return shutil.which("miranda")


def run_miranda(mirna_fa, target_fa, out_path, score, energy):
    """Run miRanda for one miRNA FASTA against one target FASTA."""
    cmd = [miranda_path(), mirna_fa, target_fa,
           "-sc", str(score), "-en", str(energy), "-quiet", "-out", out_path]
    with open(out_path, "w") as fh:
        proc = subprocess.run(cmd, stdout=fh, stderr=subprocess.PIPE, text=True)
    return proc.returncode


HIT_RE = re.compile(r"^>([^\t>]+)\t([^\t]+)\t([-\d.]+)\t([-\d.]+)\t(\d+) (\d+)\t(\d+) (\d+)")


def parse_miranda_hits(path):
    """Return {transcript: [(r_start, r_end, score, energy, q_start, q_end), ...]}."""
    hits = {}
    if not os.path.exists(path):
        return hits
    with open(path, errors="replace") as fh:
        for line in fh:
            m = HIT_RE.match(line)
            if not m:
                continue
            _mir, target, sc, en, qs, qe, rs, re_ = m.groups()
            hits.setdefault(target, []).append(
                (int(rs), int(re_), float(sc), float(en), int(qs), int(qe)))
    return hits


# --------------------------------------------------------------------------
# RNAhybrid engine (exact MFE duplex; slower, used for refinement or in the
# three-way intersect mode)
# --------------------------------------------------------------------------
def rnahybrid_path():
    return shutil.which("RNAhybrid") or shutil.which("rnahybrid")


def run_rnahybrid(target_fa, mirna_files, tmpdir, energy, dataset, jobs,
                  max_target=10000):
    """Run RNAhybrid once per miRNA. Returns [output paths].

    -m matters: RNAhybrid silently SKIPS any target longer than its maximum
    target length (default is small), which would drop most 3'UTRs and cDNAs.
    """
    import time
    outs, running = [], []
    for idx, mir in enumerate(mirna_files):
        while len(running) >= jobs:
            for q in list(running):
                if q.poll() is not None:
                    running.remove(q)
            if len(running) >= jobs:
                time.sleep(0.2)
        out = os.path.join(tmpdir, "rnahybrid_%d.txt" % idx)
        cmd = [rnahybrid_path(), "-c", "-m", str(max_target), "-e", str(energy),
               "-t", target_fa, "-q", mir]
        if dataset and dataset != "none":
            cmd += ["-s", dataset]
        with open(out, "w") as fh:
            running.append(subprocess.Popen(cmd, stdout=fh, stderr=subprocess.PIPE))
        outs.append(out)
    for q in running:
        q.wait()
    return outs


def parse_rnahybrid_hits(paths):
    """Parse compact RNAhybrid output.

    Format: target:target_len:query:query_len:MFE:p-value:position:alignment
    Returns {transcript: [(mirna, mfe, pvalue, position), ...]}
    """
    hits = {}
    for path in paths:
        if not os.path.exists(path):
            continue
        with open(path, errors="replace") as fh:
            for line in fh:
                parts = line.rstrip("\n").split(":", 7)
                if len(parts) < 7:
                    continue
                target, _tlen, query, _qlen, mfe, pval, pos = parts[:7]
                try:
                    rec = (query.split()[0], float(mfe), float(pval), int(pos))
                except ValueError:
                    continue
                hits.setdefault(target.split()[0], []).append(rec)
    return hits


# --------------------------------------------------------------------------
# miRNA source
# --------------------------------------------------------------------------
def mirnas_from_fasta(path):
    out = []
    for header, seq in parse_fasta(path):
        name = header.split()[0]
        s = normalize_mirna(seq)
        if len(s) < 6:
            print("  warning: skipping short/invalid sequence for %s" % name)
            continue
        out.append((name, s))
    if not out:
        raise SystemExit("Error: no usable miRNA sequences in %s" % path)
    return out


def _load_fetcher():
    """Import the sibling fetch_mirnas.py (works regardless of cwd)."""
    import importlib.util
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fetch_mirnas.py")
    spec = importlib.util.spec_from_file_location("fetch_mirnas", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def fetch_mirbase_mature(mature_fa=None):
    """Local file > cache > miRBase download (multi-URL, via fetch_mirnas)."""
    if mature_fa and os.path.exists(mature_fa):
        return mature_fa
    fetcher = _load_fetcher()
    path = fetcher.mature_path(None, allow_download=True)
    if not path:
        print("Warning: no local miRBase file and the download failed.")
        print("         fetch one with: python scripts/fetch_mirnas.py --update")
    return path


def mirnas_from_species(species, mature_fa=None):
    """Fetch every mature miRNA of a species straight from the database."""
    path = fetch_mirbase_mature(mature_fa)
    if not path:
        raise SystemExit("Error: cannot fetch miRNAs for '%s' (no database access). "
                         "Provide --mature-fa or use --mirna-fa." % species)
    fetcher = _load_fetcher()
    entries = fetcher.parse_mature(path)
    hits, notes = fetcher.select(entries, None, species)
    for n in notes:
        print("  " + n)
    if not hits:
        raise SystemExit("Error: no mature miRNAs found for species '%s'." % species)
    return [(nm, normalize_mirna(sq)) for nm, sq in hits]


def mirna_from_name(name, mature_fa=None):
    """Resolve one or more miRNA names from the database (species prefix optional)."""
    path = fetch_mirbase_mature(mature_fa)
    if not path:
        raise SystemExit("Error: cannot resolve '%s' (no database access). "
                         "Provide --mature-fa or use --mirna-fa." % name)
    fetcher = _load_fetcher()
    entries = fetcher.parse_mature(path)
    names = [n.strip() for n in str(name).split(",") if n.strip()]
    hits, notes = fetcher.select(entries, names, None)
    for n in notes:
        print("  " + n)
    if not hits:
        raise SystemExit("Error: '%s' not found (try the bare name, e.g. miR-21-5p)." % name)
    return [(nm, normalize_mirna(sq)) for nm, sq in hits]


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(
        description="Whole-transcriptome miRNA target prediction "
                    "(TargetScan-style seed sites, miRanda, or hybrid confirmation)")
    ap.add_argument("--list-species", action="store_true",
                    help="print built-in species presets and exit")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--mirna-fa", help="FASTA of mature miRNA sequences (name + sequence)")
    src.add_argument("--mirna", help="miRNA name(s) resolved from the database, comma "
                                     "separated (e.g. miR-21-5p or chi-miR-504-5p)")
    src.add_argument("--mirna-species", help="fetch EVERY mature miRNA of a species from "
                                             "the database (e.g. goat or chi)")
    tgt = ap.add_mutually_exclusive_group()
    tgt.add_argument("--species", help="built-in species preset (see --list-species)")
    tgt.add_argument("--mrna-fa", help="your own mRNA/cDNA FASTA")
    tgt.add_argument("--genome-fa", help="your own genome FASTA (use with --gtf)")
    ap.add_argument("--gtf", help="GTF annotation: required for --genome-fa, optional "
                                  "override for --species (3'UTR extraction), or supplied "
                                  "with --mrna-fa to enable --target-region utr")
    ap.add_argument("--target-region", default="cdna", choices=["cdna", "utr"],
                    help="scan the full spliced transcript (cdna) or only the 3'UTR (utr, "
                         "needs the GTF annotation; default: cdna)")
    ap.add_argument("--method", default="auto",
                    choices=["auto", "seed", "miranda", "hybrid", "rnahybrid", "triple"],
                    help="auto (hybrid when miRanda is installed, else seed), seed "
                         "(TargetScan-style sites only), miranda (miRanda hits only), "
                         "hybrid (seed sites confirmed by a miRanda alignment), "
                         "rnahybrid (exact MFE duplex only), triple (run seed + miRanda "
                         "+ RNAhybrid and keep the three-way intersection)")
    ap.add_argument("--miranda-score", type=float, default=140.0,
                    help="miRanda score threshold (default 140)")
    ap.add_argument("--miranda-energy", type=float, default=-20.0,
                    help="miRanda dG threshold in kcal/mol (default -20)")
    ap.add_argument("--rnahybrid-energy", type=float, default=-20.0,
                    help="RNAhybrid MFE cutoff in kcal/mol (default -20)")
    ap.add_argument("--rnahybrid-dataset", default="3utr_human",
                    choices=["3utr_human", "3utr_fly", "3utr_worm", "none"],
                    help="dataset used by RNAhybrid for p-values; only fly/worm/human "
                         "ship with the tool, so 3utr_human is the mammalian "
                         "approximation ('none' skips p-values)")
    ap.add_argument("--rnahybrid-max-target", type=int, default=10000,
                    help="maximum target length passed to RNAhybrid (-m); RNAhybrid "
                         "silently skips longer sequences, so raise this for long "
                         "3'UTRs or full cDNAs (default 10000 nt)")
    ap.add_argument("--refine-rnahybrid", type=int, default=0, metavar="N",
                    help="three-stage cascade: after the seed/miRanda scan, re-score the "
                         "top N targets per miRNA with RNAhybrid (exact MFE + p-value); "
                         "0 disables the refinement stage")
    ap.add_argument("--min-utr-length", type=int, default=30,
                    help="minimum 3'UTR length kept in --target-region utr "
                         "(default 30 nt; shorter UTRs carry no usable site)")
    ap.add_argument("--jobs", type=int, default=0,
                    help="parallel miRanda jobs (default: min(CPU count, #miRNAs))")
    ap.add_argument("--mature-fa", help="local miRBase mature.fa (for --mirna)")
    ap.add_argument("--outdir", default=".", help="output directory (default: current)")
    ap.add_argument("--prefix", default="genome_targets", help="output file prefix")
    ap.add_argument("--cache-dir", default=GENOME_CACHE, help="where to cache Ensembl downloads")
    ap.add_argument("--refresh", action="store_true", help="re-download cached files")
    ap.add_argument("--min-score", type=float, default=0.0,
                    help="drop (miRNA, transcript) rows below this total score")
    ap.add_argument("--max-transcripts", type=int, default=0,
                    help="only scan the first N transcripts (quick tests)")
    ap.add_argument("--top", type=int, default=0,
                    help="keep only the top N target rows per miRNA (0 = all)")
    ap.add_argument("--sort-by", default="score", choices=["score", "density"],
                    help="rank by raw score (default) or length-normalised density")
    args = ap.parse_args()

    if args.list_species:
        list_species()
        return

    if not args.mirna_fa and not args.mirna and not args.mirna_species:
        ap.error("provide --mirna-fa, --mirna or --mirna-species")
    if not args.species and not args.mrna_fa and not args.genome_fa:
        ap.error("provide --species, --mrna-fa or --genome-fa")
    if args.genome_fa and not args.gtf:
        ap.error("--genome-fa also needs --gtf")

    method = args.method
    if method == "auto":
        method = "hybrid" if miranda_path() else "seed"
    if method in ("miranda", "hybrid", "triple") and not miranda_path():
        print("Warning: miRanda not found on PATH.")
        print("         install it (conda install -c bioconda miranda) or pick another --method.")
        method = "rnahybrid" if (method == "triple" and rnahybrid_path()) else "seed"
    if method in ("rnahybrid", "triple") and not rnahybrid_path():
        print("Warning: RNAhybrid not found on PATH.")
        print("         install it (conda install -c bioconda rnahybrid) or pick another --method.")
        method = "hybrid" if miranda_path() else "seed"
    print("Prediction engine: %s | target region: %s" % (method, args.target_region))

    # ---- miRNAs
    if args.mirna_fa:
        mirnas = mirnas_from_fasta(args.mirna_fa)
    elif args.mirna_species:
        print("Fetching all mature miRNAs for species '%s' from the database ..."
              % args.mirna_species)
        mirnas = mirnas_from_species(args.mirna_species, args.mature_fa)
    else:
        mirnas = mirna_from_name(args.mirna, args.mature_fa)
        print("Resolved %d database entry/entries for '%s'" % (len(mirnas), args.mirna))
    seen, uniq = {}, []
    for name, seq in mirnas:
        if seq not in seen:
            seen[seq] = True
            uniq.append((name, seq))
    if len(uniq) < len(mirnas):
        print("Merged %d duplicate mature sequence(s)" % (len(mirnas) - len(uniq)))
    mirnas = uniq
    print("miRNAs: %d (%s)" % (len(mirnas), ", ".join(m for m, _ in mirnas[:6])
                               + (" ..." if len(mirnas) > 6 else "")))

    # ---- target transcripts
    gtf_path = args.gtf
    if args.mrna_fa:
        source = "mrna:%s" % os.path.basename(args.mrna_fa)
        print("Loading transcripts from %s ..." % args.mrna_fa)
        records = []
        for header, seq in parse_fasta(args.mrna_fa):
            tx, gene_id, gene = parse_ensembl_header(header)
            records.append((tx, gene_id, gene, normalize_dna(seq)))
    elif args.genome_fa:
        source = "genome:%s+%s" % (os.path.basename(args.genome_fa),
                                   os.path.basename(args.gtf))
        records = transcripts_from_gtf(args.gtf, load_genome(args.genome_fa))
    else:
        name, preset = resolve_species(args.species)
        if not preset:
            raise SystemExit("Error: unknown species '%s' (see --list-species)" % args.species)
        slug = preset[0]
        source = "ensembl:%s" % slug
        cdna = fetch_cdna(slug, args.cache_dir, refresh=args.refresh)
        if args.target_region == "utr" and not gtf_path:
            gtf_path = fetch_gtf(slug, args.cache_dir, refresh=args.refresh)
        print("Loading transcripts from %s ..." % cdna)
        records = []
        for header, seq in parse_fasta(cdna):
            tx, gene_id, gene = parse_ensembl_header(header)
            records.append((tx, gene_id, gene, normalize_dna(seq)))

    print("Transcripts: %d" % len(records))
    if args.max_transcripts:
        records = records[:args.max_transcripts]
        print("Limiting to first %d transcripts (--max-transcripts)" % len(records))

    # ---- optional 3'UTR extraction
    if args.target_region == "utr":
        if not gtf_path:
            print("Warning: --target-region utr needs a GTF; using full cDNA instead.")
        else:
            structure = load_gtf_structure(gtf_path)
            kept, statuses = [], {}
            n_short = 0
            for tx, gene_id, gene, seq in records:
                info = structure.get(strip_version(tx))
                if info is None:
                    statuses["no_annotation"] = statuses.get("no_annotation", 0) + 1
                    continue
                utr, status = slice_utr3(seq, info)
                statuses[status] = statuses.get(status, 0) + 1
                if status == "ok" and len(utr) >= args.min_utr_length:
                    kept.append((tx, gene_id, gene, utr))
                elif status == "ok":
                    n_short += 1
                elif status == "noncoding":
                    kept.append((tx, gene_id, gene, seq))
                # mismatched transcripts are dropped: their UTR boundaries
                # cannot be trusted, so they are not silently scanned as cDNA
            print("  3'UTR extraction: %s, shorter_than_%dnt=%d"
                  % (", ".join("%s=%d" % (k, v) for k, v in sorted(statuses.items())),
                     args.min_utr_length, n_short))
            n_before = len(records)
            records = kept
            print("  %d/%d transcripts kept for 3'UTR scanning" % (len(records), n_before))

    if not records:
        raise SystemExit("Error: no target transcripts left to scan.")

    # ---- miRanda
    miranda_hits = {}
    miranda_tsv = None
    if method in ("miranda", "hybrid", "triple"):
        os.makedirs(args.outdir, exist_ok=True)
        tmpdir = tempfile.mkdtemp(prefix="mirna_miranda_")
        try:
            target_fa = os.path.join(tmpdir, "targets.fa")
            # miRanda needs a unique FASTA id per target
            write_fasta(target_fa, [("%s %s" % (r[0], r[2] or r[1]), r[3]) for r in records])
            print("Running miRanda (%d miRNA x %d transcripts, -sc %g -en %g) ..."
                  % (len(mirnas), len(records), args.miranda_score, args.miranda_energy))
            jobs = args.jobs or min(os.cpu_count() or 1, len(mirnas))
            mirna_files = []
            for idx, (mname, mseq) in enumerate(mirnas):
                p = os.path.join(tmpdir, "mir_%d.fa" % idx)
                write_fasta(p, [(mname, mseq.replace("T", "U"))])
                mirna_files.append(p)
            procs = []
            running = []
            import time
            for idx, p in enumerate(mirna_files):
                while len(running) >= jobs:
                    for q in list(running):
                        if q.poll() is not None:
                            running.remove(q)
                    if len(running) >= jobs:
                        time.sleep(0.2)
                out = os.path.join(tmpdir, "hits_%d.txt" % idx)
                cmd = [miranda_path(), p, target_fa, "-sc", str(args.miranda_score),
                       "-en", str(args.miranda_energy), "-quiet", "-out", out]
                running.append(subprocess.Popen(cmd, stdout=subprocess.DEVNULL,
                                                stderr=subprocess.PIPE))
                procs.append((out, mirnas[idx][0]))
            for q in running:
                q.wait()
            for out, mname in procs:
                for target, hs in parse_miranda_hits(out).items():
                    tid = target.split()[0]
                    miranda_hits.setdefault(tid, []).extend(
                        [(mname,) + h for h in hs])
            n = sum(len(v) for v in miranda_hits.values())
            print("  miRanda hits: %d across %d transcripts" % (n, len(miranda_hits)))
            miranda_tsv = os.path.join(args.outdir, "%s_miranda.tsv" % args.prefix)
            with open(miranda_tsv, "w") as fh:
                fh.write("mirna\ttranscript_id\tquery_start\tquery_end\ttarget_start\t"
                         "target_end\tmiranda_score\tmiranda_energy\n")
                for tid, hs in sorted(miranda_hits.items()):
                    for mname, rs, re_, sc, en, qs, qe in hs:
                        fh.write("%s\t%s\t%d\t%d\t%d\t%d\t%.1f\t%.2f\n"
                                 % (mname, tid, qs, qe, rs, re_, sc, en))
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    # ---- RNAhybrid (exact MFE duplex; used alone or as the third engine)
    rnahybrid_hits = {}
    rnahybrid_tsv = None
    if method in ("rnahybrid", "triple"):
        os.makedirs(args.outdir, exist_ok=True)
        tmpdir2 = tempfile.mkdtemp(prefix="mirna_rnahybrid_")
        try:
            target_fa2 = os.path.join(tmpdir2, "targets.fa")
            write_fasta(target_fa2, [("%s %s" % (r[0], r[2] or r[1]), r[3]) for r in records])
            print("Running RNAhybrid (%d miRNA x %d transcripts, MFE <= %g kcal/mol, "
                  "dataset %s) ..."
                  % (len(mirnas), len(records), args.rnahybrid_energy, args.rnahybrid_dataset))
            jobs2 = args.jobs or min(os.cpu_count() or 1, len(mirnas))
            mir_files = []
            for idx, (mname, mseq) in enumerate(mirnas):
                p = os.path.join(tmpdir2, "rq_%d.fa" % idx)
                write_fasta(p, [(mname, mseq.replace("T", "U"))])
                mir_files.append(p)
            outs = run_rnahybrid(target_fa2, mir_files, tmpdir2, args.rnahybrid_energy,
                                 args.rnahybrid_dataset, jobs2,
                                 max_target=args.rnahybrid_max_target)
            rnahybrid_hits = parse_rnahybrid_hits(outs)
            n_rh = sum(len(v) for v in rnahybrid_hits.values())
            print("  RNAhybrid hits: %d across %d transcripts" % (n_rh, len(rnahybrid_hits)))
            rnahybrid_tsv = os.path.join(args.outdir, "%s_rnahybrid.tsv" % args.prefix)
            with open(rnahybrid_tsv, "w") as fh:
                fh.write("mirna\ttranscript_id\tposition\tmfe_kcal_mol\tp_value\n")
                for tid, hs in sorted(rnahybrid_hits.items()):
                    for mname, mfe, pval, pos in hs:
                        fh.write("%s\t%s\t%d\t%.2f\t%s\n"
                                 % (mname, tid, pos, mfe,
                                    ("%.6g" % pval) if pval is not None else ""))
        finally:
            shutil.rmtree(tmpdir2, ignore_errors=True)

    # ---- per-transcript prediction
    os.makedirs(args.outdir, exist_ok=True)
    sites_path = os.path.join(args.outdir, "%s_sites.tsv" % args.prefix)
    targets_path = os.path.join(args.outdir, "%s_targets.tsv" % args.prefix)
    info_path = os.path.join(args.outdir, "%s_run_info.tsv" % args.prefix)

    n_tx = len(records)
    print("Scanning (%s) %d miRNA x %d transcripts ..." % (method, len(mirnas), n_tx))
    targets = []
    with open(sites_path, "w") as sfh:
        sfh.write("mirna\ttranscript_id\tgene_id\tgene_name\tregion\tposition\tsite_type\t"
                  "weight\tseed_site_sequence\tmiranda_confirmed\tmiranda_score\t"
                  "miranda_energy\trnahybrid_mfe\trnahybrid_pvalue\n")
        for mi, (mname, mseq) in enumerate(mirnas, 1):
            for tx, gene_id, gene, seq in records:
                hits = [h for h in miranda_hits.get(tx, []) if h[0] == mname]
                rhits = [h for h in rnahybrid_hits.get(tx, []) if h[0] == mname]
                seed_sites = (find_sites(seq, mseq)
                              if method not in ("miranda", "rnahybrid") else [])
                best_mfe = best_pval = None
                if rhits:
                    best_rh = min(rhits, key=lambda h: h[1])
                    best_mfe, best_pval = best_rh[1], best_rh[2]
                rows = []
                if method == "miranda":
                    for _m, rs, re_, sc, en, qs, qe in hits:
                        rows.append((rs - 1, "miranda", 0.0, "", 1, sc, en,
                                     best_mfe, best_pval))
                elif method == "rnahybrid":
                    for _m, mfe, pval, pos in rhits:
                        rows.append((pos - 1, "rnahybrid", 0.0, "", 0, "nan", "nan",
                                     mfe, pval))
                elif method in ("hybrid", "triple"):
                    if method == "triple" and (not hits or not rhits):
                        seed_sites = []   # three-way intersection: every engine must agree
                    for start, stype in seed_sites:
                        end = start + (8 if stype in ("8mer", "7mer-m8") else 7)
                        overlapping = [h for h in hits if not (h[2] < start or h[1] > end)]
                        if not overlapping:
                            continue
                        best = max(overlapping, key=lambda h: h[3])
                        rows.append((start, stype, SITE_WEIGHT[stype],
                                     site_sequence(seq, start, stype), 1,
                                     best[3], best[4], best_mfe, best_pval))
                else:
                    for start, stype in seed_sites:
                        rows.append((start, stype, SITE_WEIGHT[stype],
                                     site_sequence(seq, start, stype), 0, "nan", "nan",
                                     best_mfe, best_pval))
                if not rows:
                    continue
                counts = {"8mer": 0, "7mer-m8": 0, "7mer-A1": 0, "6mer": 0}
                total = 0.0
                best_type, best_energy = None, None
                for start, stype, weight, sseq, conf, msc, men, rmfe, rpval in rows:
                    if stype in counts:
                        counts[stype] += 1
                        total += weight
                        if best_type is None or SITE_RANK[stype] > SITE_RANK[best_type]:
                            best_type = stype
                    if isinstance(men, float) and (best_energy is None or men < best_energy):
                        best_energy = men
                    sfh.write("%s\t%s\t%s\t%s\t%s\t%d\t%s\t%.1f\t%s\t%d\t%s\t%s\t%s\t%s\n"
                              % (mname, tx, gene_id, gene, args.target_region, start + 1,
                                 stype, weight, sseq, conf,
                                 ("%.1f" % msc) if isinstance(msc, float) else msc,
                                 ("%.2f" % men) if isinstance(men, float) else men,
                                 ("%.2f" % rmfe) if isinstance(rmfe, float) else "",
                                 ("%.6g" % rpval) if isinstance(rpval, float) else ""))
                kb = max(len(seq), 1) / 1000.0
                # rnahybrid-only mode has no seed weights (total stays 0), so the
                # score filter would silently drop every hit - ranking is by MFE
                if method == "rnahybrid" or total >= args.min_score:
                    evidence = "+".join(n for n, ok in (("seed", bool(seed_sites)),
                                                        ("miranda", bool(hits)),
                                                        ("rnahybrid", bool(rhits))) if ok)
                    targets.append({
                        "mirna": mname, "transcript_id": tx, "gene_id": gene_id,
                        "gene_name": gene, "length": len(seq), "n_sites": len(rows),
                        "n_8mer": counts["8mer"], "n_7mer_m8": counts["7mer-m8"],
                        "n_7mer_A1": counts["7mer-A1"], "n_6mer": counts["6mer"],
                        "score": total, "best": best_type or "-",
                        "score_per_kb": total / kb, "sites_per_kb": len(rows) / kb,
                        "miranda_hits": len(hits), "rnahybrid_hits": len(rhits),
                        "best_energy": best_energy, "best_mfe": best_mfe,
                        "best_pval": best_pval, "evidence": evidence or "-",
                    })
            if len(mirnas) > 1:
                print("  %s: done (%d/%d miRNAs)" % (mname, mi, len(mirnas)))

    # ---- optional third cascade stage: exact-MFE refinement of the top hits
    if args.refine_rnahybrid and rnahybrid_path() and method in ("seed", "miranda", "hybrid"):
        print("Refining the top %d targets per miRNA with RNAhybrid ..."
              % args.refine_rnahybrid)
        by_mirna = {}
        for row in targets:
            lst = by_mirna.setdefault(row["mirna"], [])
            if len(lst) < args.refine_rnahybrid:
                lst.append(row)
        sel = [r for rows in by_mirna.values() for r in rows]
        seq_by_tx = {r[0]: r[3] for r in records}
        mirna_seq = dict(mirnas)
        tmpdir3 = tempfile.mkdtemp(prefix="mirna_refine_")
        try:
            txs = []
            for r in sel:
                if r["transcript_id"] not in txs:
                    txs.append(r["transcript_id"])
            target_fa3 = os.path.join(tmpdir3, "targets.fa")
            write_fasta(target_fa3, [(t, seq_by_tx[t]) for t in txs if t in seq_by_tx])
            jobs3 = args.jobs or min(os.cpu_count() or 1, max(1, len(by_mirna)))
            mir_files3 = []
            for idx, mname in enumerate(by_mirna):
                p = os.path.join(tmpdir3, "rq_%d.fa" % idx)
                write_fasta(p, [(mname, mirna_seq[mname].replace("T", "U"))])
                mir_files3.append(p)
            outs3 = run_rnahybrid(target_fa3, mir_files3, tmpdir3, args.rnahybrid_energy,
                                  args.rnahybrid_dataset, jobs3,
                                  max_target=args.rnahybrid_max_target)
            if rnahybrid_tsv is None:
                rnahybrid_tsv = os.path.join(args.outdir, "%s_rnahybrid.tsv" % args.prefix)
                with open(rnahybrid_tsv, "w") as fh:
                    fh.write("mirna\ttranscript_id\tposition\tmfe_kcal_mol\tp_value\n")
            refined = {}
            with open(rnahybrid_tsv, "a") as fh:
                for path in outs3:
                    for tid, hs in parse_rnahybrid_hits([path]).items():
                        for mname, mfe, pval, pos in hs:
                            refined[(mname, tid)] = (mfe, pval)
                            fh.write("%s\t%s\t%d\t%.2f\t%s\n"
                                     % (mname, tid, pos, mfe,
                                        ("%.6g" % pval) if pval is not None else ""))
            n_hit = 0
            for r in sel:
                got = refined.get((r["mirna"], r["transcript_id"]))
                if got:
                    r["best_mfe"], r["best_pval"] = got
                    r["mfe_verified"] = "yes" if got[0] <= args.rnahybrid_energy else "no"
                    n_hit += 1
                else:
                    r["mfe_verified"] = "no"
            print("  refined %d/%d targets with RNAhybrid (%d pass MFE <= %g kcal/mol)"
                  % (n_hit, len(sel),
                     sum(1 for r in sel if r.get("mfe_verified") == "yes"),
                     args.rnahybrid_energy))
        finally:
            shutil.rmtree(tmpdir3, ignore_errors=True)

    if args.sort_by == "density":
        targets.sort(key=lambda r: (-r["score_per_kb"], r["mirna"], r["transcript_id"]))
    elif method == "rnahybrid":
        targets.sort(key=lambda r: (r["best_mfe"] if r["best_mfe"] is not None else 0.0,
                                    r["mirna"], r["transcript_id"]))
    else:
        targets.sort(key=lambda r: (-r["score"], r["mirna"], r["transcript_id"]))
    if args.top:
        kept, per = [], {}
        for r in targets:
            per[r["mirna"]] = per.get(r["mirna"], 0) + 1
            if per[r["mirna"]] <= args.top:
                kept.append(r)
        targets = kept

    with open(targets_path, "w") as tfh:
        tfh.write("mirna\ttranscript_id\tgene_id\tgene_name\tregion\ttranscript_length\t"
                  "n_sites\tn_8mer\tn_7mer_m8\tn_7mer_A1\tn_6mer\ttotal_score\t"
                  "site_density_per_kb\tscore_per_kb\tbest_site_type\tmiranda_hits\t"
                  "best_miranda_energy\trnahybrid_hits\tbest_rnahybrid_mfe\t"
                  "best_rnahybrid_pvalue\tevidence\tmfe_verified\n")
        for r in targets:
            tfh.write("%s\t%s\t%s\t%s\t%s\t%d\t%d\t%d\t%d\t%d\t%d\t%.1f\t%.3f\t%.3f\t%s\t%d\t%s\t%d\t%s\t%s\t%s\t%s\n"
                      % (r["mirna"], r["transcript_id"], r["gene_id"], r["gene_name"],
                         args.target_region, r["length"], r["n_sites"], r["n_8mer"],
                         r["n_7mer_m8"], r["n_7mer_A1"], r["n_6mer"], r["score"],
                         r["sites_per_kb"], r["score_per_kb"], r["best"],
                         r["miranda_hits"],
                         ("%.2f" % r["best_energy"]) if isinstance(r["best_energy"], float) else "",
                         r["rnahybrid_hits"],
                         ("%.2f" % r["best_mfe"]) if isinstance(r["best_mfe"], float) else "",
                         ("%.6g" % r["best_pval"]) if isinstance(r["best_pval"], float) else "",
                         r["evidence"], r.get("mfe_verified", "")))
    n_genes = len({(r["mirna"], r["gene_id"] or r["gene_name"] or r["transcript_id"])
                   for r in targets})
    with open(info_path, "w") as ifh:
        ifh.write("metric\tvalue\n")
        ifh.write("target_source\t%s\n" % source)
        ifh.write("species\t%s\n" % (args.species or ""))
        ifh.write("method\t%s\n" % method)
        ifh.write("target_region\t%s\n" % args.target_region)
        ifh.write("gtf\t%s\n" % (gtf_path or ""))
        ifh.write("mirnas\t%d\n" % len(mirnas))
        ifh.write("transcripts_scanned\t%d\n" % n_tx)
        ifh.write("target_rows\t%d\n" % len(targets))
        ifh.write("target_genes\t%d\n" % n_genes)
        ifh.write("min_score\t%g\n" % args.min_score)
        ifh.write("miranda_score_threshold\t%g\n" % args.miranda_score)
        ifh.write("miranda_energy_threshold\t%g\n" % args.miranda_energy)
        ifh.write("min_utr_length\t%d\n" % args.min_utr_length)
        ifh.write("transcripts_scanned_after_utr_filter\t%d\n" % len(records))
        ifh.write("site_weights\t8mer=4;7mer-m8=3;7mer-A1=2;6mer=1\n")
        ifh.write("note\tseed sites are TargetScan site definitions only "
                  "(no context++ model); hybrid sites additionally have a "
                  "miRanda alignment with score and dG\n")

    print()
    print("=== Done ===")
    print("  sites   : %s" % sites_path)
    if miranda_tsv:
        print("  miRanda : %s" % miranda_tsv)
    print("  targets : %s (%d rows, %d genes)" % (targets_path, len(targets), n_genes))
    print("  run info: %s" % info_path)
    if targets:
        print("  top hit : %s -> %s (%s, score %.1f)"
              % (targets[0]["mirna"], targets[0]["transcript_id"],
                 targets[0]["gene_name"] or targets[0]["gene_id"], targets[0]["score"]))


if __name__ == "__main__":
    main()
