#!/usr/bin/env python3
"""
Two-stage miRNA target refinement
=================================

Stage 1 (cheap):  a whole-transcriptome seed scan (predict_targets_genome.py)
                  scores every seed site and writes {prefix}_sites.tsv.
Stage 2 (this):   take the best-scoring seed sites, cut the **3'UTR window**
                  around each site, and re-predict the duplex with miRanda
                  and/or RNAhybrid (exact minimum free energy) on just those
                  windows.

This is the standard coarse-to-fine strategy: the seed scan is seconds for a
whole transcriptome, while the expensive thermodynamic engines only ever see
a few hundred short windows.  Because the windows are extracted from the
annotated 3'UTR rather than from the full cDNA, the reported positions and
MFE values are directly interpretable as 3'UTR binding sites.

Usage
-----
  python refine_sites.py \
      --sites results/genome/goat_cascade_sites.tsv \
      --species goat \
      --outdir results/refine --prefix goat_refine

  # your own transcriptome (cDNA FASTA + GTF for 3'UTR boundaries)
  python refine_sites.py --sites my_sites.tsv \
      --mrna-fa transcripts.fa --gtf annotation.gtf \
      --mirna-fa mirnas.fa \
      --outdir results/refine --prefix my_refine

Outputs
-------
{prefix}_selected_sites.tsv   selected seed sites with their 3'UTR window
{prefix}_windows.fa           the extracted 3'UTR windows (FASTA)
{prefix}_refined_sites.tsv    per-site miRanda/RNAhybrid evidence
{prefix}_refined_targets.tsv  per-(miRNA, transcript) summary
{prefix}_miranda_hits.tsv     raw miRanda hits restricted to the windows
{prefix}_rnahybrid_hits.tsv   raw RNAhybrid hits restricted to the windows
{prefix}_skipped.tsv          sites that could not be mapped (with reason)
{prefix}_refine_summary.tsv   run metadata and counts

Safety notes
------------
* all external programs are invoked with argv lists (no shell)
* windows and outputs are written under --outdir, and --prefix is validated
* temporary files live in a private mktemp-style directory that is removed
* input sites/FASTA are treated as untrusted data (bounded parsing)

Dependencies: standard library only; miRanda and/or RNAhybrid optional.
"""

import argparse
import csv
import importlib.util
import os
import re
import shutil
import sys
import tempfile

SEED_TYPES = ("8mer", "7mer-m8", "7mer-A1", "6mer")
SITE_LENGTH = {"8mer": 8, "7mer-m8": 8, "7mer-A1": 7, "6mer": 7}
SITE_WEIGHT = {"8mer": 4.0, "7mer-m8": 3.0, "7mer-A1": 2.0, "6mer": 1.0}
MAX_INPUT_ROWS = 5_000_000


def _load_sibling(name):
    """Import a script from this directory without relying on cwd."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), name + ".py")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def clean_field(value):
    """TSV-safe cell: no tabs, newlines or NULs."""
    return re.sub(r"[\t\r\n\x00]+", " ", str(value)).strip()


def fasta_token(value):
    """One whitespace-free FASTA header token."""
    return re.sub(r"[\s\x00>]+", "_", clean_field(value)).strip("_") or "NA"


def read_sites(path):
    """Read and validate the stage-1 sites table."""
    rows = []
    with open(path, newline="", errors="replace") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        required = {"mirna", "transcript_id", "site_type", "position",
                    "weight", "seed_site_sequence"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise SystemExit("Error: %s is missing column(s): %s"
                             % (path, ", ".join(sorted(missing))))
        for i, row in enumerate(reader, 2):
            if len(rows) >= MAX_INPUT_ROWS:
                raise SystemExit("Error: %s has more than %d data rows; refusing "
                                 "to continue" % (path, MAX_INPUT_ROWS))
            site_type = (row.get("site_type") or "").strip()
            if site_type not in SEED_TYPES:
                continue
            try:
                row["position"] = int(row["position"])
                row["weight"] = float(row.get("weight") or SITE_WEIGHT[site_type])
            except (TypeError, ValueError):
                continue
            if row["position"] < 1:
                continue
            row["site_type"] = site_type
            row["_line"] = i
            row["seed_site_sequence"] = (row.get("seed_site_sequence") or "").strip().upper()
            rows.append(row)
    return rows


def build_sequences(ptg, args, needed):
    """Return {transcript_id: (cDNA, gene_id, gene_name)} for wanted transcripts."""
    sequences = {}
    if args.mrna_fa:
        for header, seq in ptg.parse_fasta(args.mrna_fa):
            tx, gene_id, gene = ptg.parse_ensembl_header(header)
            if tx in needed:
                sequences[tx] = (ptg.normalize_dna(seq), gene_id, gene)
    elif args.genome_fa:
        records = ptg.transcripts_from_gtf(args.gtf, ptg.load_genome(args.genome_fa))
        for tx, gene_id, gene, seq in records:
            if tx in needed:
                sequences[tx] = (ptg.normalize_dna(seq), gene_id, gene)
    else:
        name, preset = ptg.resolve_species(args.species)
        if not preset:
            raise SystemExit("Error: unknown species '%s' (see --list-species)" % args.species)
        cdna = ptg.fetch_cdna(preset[0], args.cache_dir, refresh=args.refresh)
        for header, seq in ptg.parse_fasta(cdna):
            tx, gene_id, gene = ptg.parse_ensembl_header(header)
            if tx in needed:
                sequences[tx] = (ptg.normalize_dna(seq), gene_id, gene)

    missing = sorted(needed - set(sequences))
    if missing:
        print("Warning: %d transcript(s) from the sites table were not found in the "
              "target source (e.g. %s)" % (len(missing), ", ".join(missing[:3])))
    return sequences


def build_utrs(ptg, args, sequences, sites):
    """Return ({tx: 3'UTR}, {tx: status}) and the region kind used by stage 1."""
    regions = {row.get("region", "cdna") for row in sites}
    utrs, status = {}, {}

    gtf = args.gtf
    if not gtf and args.species:
        # Built-in species: fetch the GTF so 3'UTRs can be sliced.
        _, preset = ptg.resolve_species(args.species)
        if preset:
            gtf = ptg.fetch_gtf(preset[0], args.cache_dir, refresh=args.refresh)

    if gtf:
        structure = ptg.load_gtf_structure(gtf)
        for tx, (cdna, _, _) in sequences.items():
            info = structure.get(ptg.strip_version(tx))
            if info is None:
                status[tx] = "no_annotation"
                continue
            utr, st = ptg.slice_utr3(cdna, info)
            status[tx] = st
            if st == "ok":
                utrs[tx] = utr
            elif st == "noncoding" and "utr" in regions:
                # stage 1 kept non-coding transcripts whole under --target-region
                # utr, so keep the same coordinates here instead of dropping them
                utrs[tx] = cdna
                status[tx] = "noncoding_full_transcript"
            elif st == "noncoding":
                status[tx] = "noncoding_no_3utr"
        return utrs, status

    if regions == {"utr"}:
        # The stage-1 target source was already a 3'UTR set.
        for tx, (cdna, _, _) in sequences.items():
            utrs[tx] = cdna
            status[tx] = "input_is_utr"
        return utrs, status

    raise SystemExit(
        "Error: stage 1 scanned cDNA coordinates but no --gtf was given, so the "
        "3'UTR cannot be located.\n"
        "       Supply --gtf (or --species, which fetches one), or run stage 1 "
        "with --target-region utr.")


def map_sites(ptg, sites, sequences, utrs, status, tolerance=5):
    """Attach a 0-based 3'UTR position to each site; return (mapped, skipped)."""
    mapped, skipped = [], []
    for row in sites:
        tx = row["transcript_id"]
        if tx not in sequences:
            skipped.append((row, "transcript_not_found"))
            continue
        if tx not in utrs:
            skipped.append((row, status.get(tx, "no_3utr")))
            continue
        cdna = sequences[tx][0]
        utr = utrs[tx]
        stage1_region = (row.get("region") or "cdna").strip()
        offset = 0 if stage1_region == "utr" else max(0, len(cdna) - len(utr))
        pos0 = row["position"] - 1 - offset
        site_type = row["site_type"]
        expected = row["seed_site_sequence"]
        if expected:
            expected = ptg.normalize_dna(expected)
        else:
            expected = utr[pos0:pos0 + SITE_LENGTH[site_type]] if pos0 >= 0 else ""
        if not expected:
            skipped.append((row, "outside_3utr"))
            continue

        if pos0 < 0 or pos0 + len(expected) > len(utr):
            skipped.append((row, "outside_3utr"))
            continue

        # Guard against annotation/version drift: the seed sequence stored in
        # stage 1 must exist at the mapped position (allow a small local shift).
        if row["seed_site_sequence"]:
            found = None
            for delta in range(0, tolerance + 1):
                for candidate in ((pos0,) if delta == 0 else (pos0 - delta, pos0 + delta)):
                    if candidate < 0 or candidate + len(expected) > len(utr):
                        continue
                    if utr[candidate:candidate + len(expected)] == expected:
                        found = candidate
                        break
                if found is not None:
                    break
            if found is None:
                skipped.append((row, "sequence_mismatch"))
                continue
            pos0 = found

        row["pos0"] = pos0
        row["site_len"] = len(expected)
        row["utr_len"] = len(utr)
        row["gene_id"] = row.get("gene_id") or sequences[tx][1]
        row["gene_name"] = row.get("gene_name") or sequences[tx][2]
        mapped.append(row)
    return mapped, skipped


def select_sites(sites, args):
    """Rank by preliminary weight and cap per miRNA / per transcript."""
    ranked = sorted(sites, key=lambda r: (-r["weight"], r["mirna"],
                                          r["transcript_id"], r["pos0"]))
    selected, per_mirna, per_tx = [], {}, {}
    for row in ranked:
        mir = row["mirna"]
        tx = row["transcript_id"]
        if per_mirna.get(mir, 0) >= args.top_per_mirna:
            continue
        if per_tx.get((mir, tx), 0) >= args.max_per_transcript:
            continue
        per_mirna[mir] = per_mirna.get(mir, 0) + 1
        per_tx[(mir, tx)] = per_tx.get((mir, tx), 0) + 1
        selected.append(row)
        if len(selected) >= args.max_sites:
            break
    return selected


def make_windows(selected, utrs, flank, gap, max_windows, mode="site"):
    """Group selected sites into 3'UTR windows. Returns (windows, skipped).

    mode="site" gives one window around each site cluster; mode="utr" gives
    one window per (miRNA, transcript) covering the whole annotated 3'UTR.
    """
    windows, overflow = [], []
    groups = {}
    for row in selected:
        groups.setdefault((row["mirna"], row["transcript_id"]), []).append(row)
    for (mir, tx), items in groups.items():
        length = len(utrs[tx])
        items = sorted(items, key=lambda r: r["pos0"])
        if mode == "utr":
            windows.append({"mirna": mir, "transcript_id": tx,
                            "start": 0, "end": length, "sites": items})
            continue
        current = None
        for row in items:
            start = max(0, row["pos0"] - flank)
            end = min(length, row["pos0"] + row["site_len"] + flank)
            if current and start <= current["end"] + gap:
                current["end"] = max(current["end"], end)
                current["sites"].append(row)
            else:
                if current:
                    windows.append(current)
                current = {"mirna": mir, "transcript_id": tx,
                           "start": start, "end": end, "sites": [row]}
        if current:
            windows.append(current)
    # Stable order, then apply the global window cap.
    windows.sort(key=lambda w: (w["mirna"], w["transcript_id"], w["start"]))
    if len(windows) > max_windows:
        overflow = windows[max_windows:]
        windows = windows[:max_windows]
    for idx, win in enumerate(windows, 1):
        win["id"] = "W%06d" % idx
        win["length"] = win["end"] - win["start"]
    return windows, overflow


def write_window_fasta(path, windows, utrs):
    with open(path, "w") as fh:
        for win in windows:
            utr = utrs[win["transcript_id"]]
            seq = utr[win["start"]:win["end"]].replace("T", "U")
            fh.write(">%s mirna=%s transcript=%s start=%d end=%d\n"
                     % (win["id"], fasta_token(win["mirna"]), fasta_token(win["transcript_id"]),
                        win["start"] + 1, win["end"]))
            for i in range(0, len(seq), 60):
                fh.write(seq[i:i + 60] + "\n")


def load_mirna_sequences(ptg, args, names):
    """Map miRNA name -> normalized sequence (from --mirna-fa or the database)."""
    seqs = {}
    if args.mirna_fa:
        for header, seq in ptg.parse_fasta(args.mirna_fa):
            name = header.split()[0]
            s = ptg.normalize_mirna(seq)
            if len(s) >= 6:
                seqs[name] = s
    else:
        resolved = ptg.mirna_from_name(",".join(sorted(names)), args.mature_fa)
        for name, seq in resolved:
            seqs[name] = ptg.normalize_mirna(seq)

    out = {}
    for name in names:
        if name in seqs:
            out[name] = seqs[name]
            continue
        # tolerate prefix differences (chi-miR-504-5p vs miR-504-5p)
        bare = name[4:] if len(name) > 4 and name[3] == "-" else name
        candidates = [n for n in seqs if n == bare or n.endswith("-" + bare)]
        if candidates:
            out[name] = seqs[candidates[0]]
            continue
        out[name] = None
    return out


def run_miranda(exe, query_fa, target_fa, out_path, score, energy):
    import subprocess
    cmd = [exe, query_fa, target_fa, "-sc", str(score), "-en", str(energy),
           "-quiet", "-out", out_path]
    proc = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    return proc


def run_rnahybrid(exe, query_fa, target_fa, out_path, energy, dataset, max_target):
    import subprocess
    cmd = [exe, "-c", "-m", str(max_target), "-e", str(energy),
           "-t", target_fa, "-q", query_fa]
    if dataset and dataset != "none":
        cmd += ["-s", dataset]
    with open(out_path, "w") as fh:
        proc = subprocess.run(cmd, stdout=fh, stderr=subprocess.PIPE, text=True)
    return proc


def overlap(a_start, a_end, b_start, b_end, tolerance=0):
    return a_start <= b_end + tolerance and a_end >= b_start - tolerance


def main():
    ap = argparse.ArgumentParser(
        description="Refine top seed sites by extracting 3'UTR windows and "
                    "re-predicting with miRanda / RNAhybrid")
    ap.add_argument("--sites", required=True,
                    help="stage-1 {prefix}_sites.tsv from predict_targets_genome.py "
                         "(needs mirna, transcript_id, site_type, position, weight, "
                         "seed_site_sequence; region is used when present)")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--species", help="built-in species preset (fetches Ensembl cDNA/GTF)")
    src.add_argument("--mrna-fa", help="your own cDNA FASTA (same one used in stage 1)")
    src.add_argument("--genome-fa", help="your own genome FASTA (use with --gtf)")
    ap.add_argument("--gtf", help="GTF annotation (required for cDNA-coordinate input; "
                                  "auto-fetched for --species)")
    ap.add_argument("--cache-dir", default=None, help="Ensembl cache directory")
    ap.add_argument("--refresh", action="store_true", help="re-download cached references")
    mir = ap.add_mutually_exclusive_group()
    mir.add_argument("--mirna-fa", help="FASTA with the mature miRNA sequences")
    mir.add_argument("--mature-fa", help="local miRBase mature.fa used to resolve names")
    ap.add_argument("--method", default="auto", choices=["auto", "miranda", "rnahybrid", "both"],
                    help="engine(s) for refinement; auto (default) requires real "
                         "miRanda 3.3a and adds RNAhybrid when available; "
                         "rnahybrid is the explicit no-miRanda option")
    ap.add_argument("--miranda-score", type=float, default=140.0,
                    help="miRanda score cutoff (default 140)")
    ap.add_argument("--miranda-energy", type=float, default=-20.0,
                    help="miRanda dG cutoff in kcal/mol (default -20)")
    ap.add_argument("--rnahybrid-energy", type=float, default=-20.0,
                    help="RNAhybrid MFE cutoff in kcal/mol (default -20)")
    ap.add_argument("--rnahybrid-dataset", default="3utr_human",
                    choices=["3utr_human", "3utr_fly", "3utr_worm", "none"])
    ap.add_argument("--rnahybrid-max-target", type=int, default=10000,
                    help="RNAhybrid -m value (default 10000 nt)")
    ap.add_argument("--window-mode", default="site", choices=["site", "utr"],
                    help="site: a window around each selected site (default); "
                         "utr: the whole annotated 3'UTR of each selected transcript")
    ap.add_argument("--flank", type=int, default=60,
                    help="3'UTR bases on each side of a site (default 60)")
    ap.add_argument("--merge-gap", type=int, default=20,
                    help="merge overlapping/nearby windows within this gap (default 20)")
    ap.add_argument("--top-per-mirna", type=int, default=200,
                    help="maximum selected sites per miRNA (default 200)")
    ap.add_argument("--max-per-transcript", type=int, default=5,
                    help="maximum selected sites per (miRNA, transcript) (default 5)")
    ap.add_argument("--max-sites", type=int, default=5000,
                    help="global cap on selected sites (default 5000)")
    ap.add_argument("--max-windows", type=int, default=4000,
                    help="global cap on extracted windows (default 4000)")
    ap.add_argument("--min-weight", type=float, default=0.0,
                    help="drop sites below this preliminary weight")
    ap.add_argument("--locate-tolerance", type=int, default=5, metavar="NT",
                    help="allowed local shift when re-locating a seed sequence "
                         "(default 5 nt)")
    ap.add_argument("--strict", action="store_true",
                    help="fail if a requested engine is unavailable")
    ap.add_argument("--outdir", default="refine_results", help="output directory")
    ap.add_argument("--prefix", default="refine", help="output filename prefix")
    args = ap.parse_args()

    if not os.path.isfile(args.sites):
        raise SystemExit("Error: --sites %s not found" % args.sites)
    if args.genome_fa and not args.gtf:
        raise SystemExit("Error: --genome-fa also needs --gtf")
    if not args.species and not args.mrna_fa and not args.genome_fa:
        raise SystemExit("Error: give --species, --mrna-fa or --genome-fa+--gtf")
    if args.flank < 0 or args.merge_gap < 0:
        ap.error("--flank and --merge-gap must be >= 0")
    if args.locate_tolerance < 0:
        ap.error("--locate-tolerance must be >= 0")
    if args.rnahybrid_max_target < 1:
        ap.error("--rnahybrid-max-target must be >= 1")
    if not str(args.outdir).strip():
        ap.error("--outdir must not be empty")
    for name in ("top_per_mirna", "max_per_transcript", "max_sites", "max_windows"):
        if getattr(args, name) < 1:
            ap.error("--%s must be >= 1" % name.replace("_", "-"))

    ptg = _load_sibling("predict_targets_genome")
    args.prefix = ptg.safe_name(args.prefix, "prefix")
    args.cache_dir = args.cache_dir or ptg.GENOME_CACHE
    os.makedirs(args.outdir, exist_ok=True)

    # ---- read + filter stage-1 sites
    sites = read_sites(args.sites)
    sites = [r for r in sites if r["weight"] >= args.min_weight]
    if not sites:
        raise SystemExit("Error: no seed sites in %s (after filtering)." % args.sites)
    print("Stage-1 seed sites: %d across %d miRNA(s)"
          % (len(sites), len({r["mirna"] for r in sites})))

    needed = {r["transcript_id"] for r in sites}
    sequences = build_sequences(ptg, args, needed)
    if not sequences:
        raise SystemExit("Error: none of the transcripts in the sites table were found.")
    utrs, status = build_utrs(ptg, args, sequences, sites)

    mapped, skipped = map_sites(ptg, sites, sequences, utrs, status,
                                tolerance=args.locate_tolerance)
    if not mapped:
        raise SystemExit("Error: no site could be mapped to a 3'UTR. Reasons: %s"
                         % ", ".join(sorted({reason for _, reason in skipped})))
    selected = select_sites(mapped, args)
    print("Mapped sites: %d | selected: %d | skipped: %d"
          % (len(mapped), len(selected), len(skipped)))

    windows, overflow = make_windows(selected, utrs, args.flank,
                                     args.merge_gap, args.max_windows,
                                     mode=args.window_mode)
    if overflow:
        skipped.extend([(row, "window_cap_reached") for win in overflow for row in win["sites"]])
    print("3'UTR windows: %d (%d-%d nt)"
          % (len(windows), args.flank, args.flank * 2 + 8))

    # ---- engines
    miranda_exe = ptg.find_tool("miranda")
    rnahybrid_exe = ptg.find_tool("RNAhybrid", "rnahybrid")
    miranda_hint = (
        "Error: the default refinement requires a real miRanda 3.3a binary.\n"
        "Install it with:  bash scripts/install_miranda_conda.sh\n"
        "Then verify with: python3 scripts/check_env.py\n"
        "For an explicitly RNAhybrid-only refinement use: --method rnahybrid")
    methods = []
    if args.method == "auto":
        if not miranda_exe:
            raise SystemExit(miranda_hint)
        methods.append("miranda")
        if rnahybrid_exe:
            methods.append("rnahybrid")
        else:
            print("Warning: RNAhybrid not found - using real miRanda only.")
    elif args.method == "miranda":
        if not miranda_exe:
            raise SystemExit(miranda_hint)
        methods.append("miranda")
    elif args.method == "rnahybrid":
        if not rnahybrid_exe:
            raise SystemExit("Error: --method rnahybrid requires RNAhybrid.\n"
                             "Install it with: conda install -c bioconda rnahybrid")
        methods.append("rnahybrid")
    elif args.method == "both":
        missing = [name for name, exe in (("miRanda", miranda_exe),
                                          ("RNAhybrid", rnahybrid_exe)) if not exe]
        if missing:
            raise SystemExit("Error: --method both requires: %s\n%s"
                             % (", ".join(missing),
                                miranda_hint if "miRanda" in missing else
                                "Install RNAhybrid with: conda install -c bioconda rnahybrid"))
        methods.extend(["miranda", "rnahybrid"])
    if not methods:
        raise SystemExit("Error: no refinement engine selected.")
    print("Refinement engines: %s" % ", ".join(methods))
    if "rnahybrid" in methods:
        too_long = [w for w in windows if w["length"] > args.rnahybrid_max_target]
        if too_long:
            print("Warning: %d window(s) exceed --rnahybrid-max-target (%d nt); "
                  "RNAhybrid will skip them. Raise the limit or use --window-mode site."
                  % (len(too_long), args.rnahybrid_max_target))

    names = {win["mirna"] for win in windows}
    mirna_seqs = load_mirna_sequences(ptg, args, names)
    unusable = [n for n, s in mirna_seqs.items() if not s]
    if unusable:
        raise SystemExit("Error: no sequence for miRNA(s): %s (pass --mirna-fa or "
                         "--mature-fa)" % ", ".join(sorted(unusable)))

    windows_by_id = {win["id"]: win for win in windows}
    miranda_hits, rnahybrid_hits = {}, {}
    tmpdir = tempfile.mkdtemp(prefix="mirna_refine_")
    try:
        by_mirna = {}
        for win in windows:
            by_mirna.setdefault(win["mirna"], []).append(win)

        for idx, (mir, wins) in enumerate(sorted(by_mirna.items())):
            target_fa = os.path.join(tmpdir, "windows_%d.fa" % idx)
            query_fa = os.path.join(tmpdir, "query_%d.fa" % idx)
            write_window_fasta(target_fa, wins, utrs)
            with open(query_fa, "w") as fh:
                fh.write(">%s\n%s\n" % (clean_field(mir), mirna_seqs[mir].replace("T", "U")))

            if "miranda" in methods:
                out = os.path.join(tmpdir, "miranda_%d.txt" % idx)
                proc = run_miranda(miranda_exe, query_fa, target_fa, out,
                                   args.miranda_score, args.miranda_energy)
                if proc.returncode != 0:
                    print("  miRanda failed for %s: %s" % (mir, proc.stderr.strip()[:300]))
                else:
                    for target, hits in ptg.parse_miranda_hits(out).items():
                        if target in windows_by_id:
                            miranda_hits.setdefault(target, []).extend(
                                [(mir,) + h for h in hits])

            if "rnahybrid" in methods:
                out = os.path.join(tmpdir, "rnahybrid_%d.txt" % idx)
                proc = run_rnahybrid(rnahybrid_exe, query_fa, target_fa, out,
                                     args.rnahybrid_energy, args.rnahybrid_dataset,
                                     args.rnahybrid_max_target)
                if proc.returncode != 0:
                    print("  RNAhybrid failed for %s: %s" % (mir, proc.stderr.strip()[:300]))
                else:
                    for target, hits in ptg.parse_rnahybrid_hits([out]).items():
                        if target in windows_by_id:
                            rnahybrid_hits.setdefault(target, []).extend(hits)

        # ---- per-site refined calls
        refined = []
        for win in windows:
            wt_start = win["start"] + 1
            for row in win["sites"]:
                site_start = row["pos0"] - win["start"] + 1
                site_end = site_start + row["site_len"] - 1

                best_mir = None
                for _m, rs, re_, sc, en, _qs, _qe in miranda_hits.get(win["id"], []):
                    if overlap(rs, re_, site_start, site_end, args.locate_tolerance):
                        if best_mir is None or sc > best_mir[0]:
                            best_mir = (sc, en, rs, re_)

                best_mfe = None
                for _m, mfe, pval, pos in rnahybrid_hits.get(win["id"], []):
                    hit_end = pos + len(mirna_seqs[win["mirna"]]) - 1
                    if overlap(pos, hit_end, site_start, site_end, args.locate_tolerance):
                        if best_mfe is None or mfe < best_mfe[0]:
                            best_mfe = (mfe, pval, pos)

                miranda_ok = best_mir is not None
                mfe_ok = best_mfe is not None and best_mfe[0] <= args.rnahybrid_energy
                if "miranda" in methods and "rnahybrid" in methods:
                    call = "confirmed" if (miranda_ok and mfe_ok) else (
                        "partial" if (miranda_ok or mfe_ok) else "not_confirmed")
                elif "miranda" in methods:
                    call = "confirmed" if miranda_ok else "not_confirmed"
                else:
                    call = "confirmed" if mfe_ok else "not_confirmed"

                refined.append({
                    "mirna": row["mirna"],
                    "transcript_id": row["transcript_id"],
                    "gene_id": row.get("gene_id", ""),
                    "gene_name": row.get("gene_name", ""),
                    "site_type": row["site_type"],
                    "prelim_weight": row["weight"],
                    "site_start_utr": row["pos0"] + 1,
                    "site_sequence": row["seed_site_sequence"],
                    "window_id": win["id"],
                    "window_start_utr": win["start"] + 1,
                    "window_end_utr": win["end"],
                    "window_length": win["length"],
                    "site_offset_in_window": site_start,
                    "miranda_confirmed": int(miranda_ok),
                    "miranda_score": "" if best_mir is None else "%.1f" % best_mir[0],
                    "miranda_energy": "" if best_mir is None else "%.2f" % best_mir[1],
                    "miranda_target_start": "" if best_mir is None else best_mir[2],
                    "miranda_target_end": "" if best_mir is None else best_mir[3],
                    "rnahybrid_mfe": "" if best_mfe is None else "%.2f" % best_mfe[0],
                    "rnahybrid_pvalue": "" if best_mfe is None else "%.6g" % best_mfe[1],
                    "rnahybrid_position": "" if best_mfe is None else best_mfe[2],
                    "mfe_confirmed": int(mfe_ok),
                    "refined_call": call,
                })

        # ---- write outputs
        prefix = os.path.join(args.outdir, args.prefix)
        windows_fa = prefix + "_windows.fa"
        write_window_fasta(windows_fa, windows, utrs)

        selected_path = prefix + "_selected_sites.tsv"
        with open(selected_path, "w") as fh:
            cols = ["mirna", "transcript_id", "gene_id", "gene_name", "site_type",
                    "weight", "site_start_utr", "seed_site_sequence", "window_id",
                    "window_start_utr", "window_end_utr"]
            fh.write("\t".join(cols) + "\n")
            for win in windows:
                for row in win["sites"]:
                    fh.write("\t".join(clean_field(x) for x in (
                        row["mirna"], row["transcript_id"], row.get("gene_id", ""),
                        row.get("gene_name", ""), row["site_type"], row["weight"],
                        row["pos0"] + 1, row["seed_site_sequence"], win["id"],
                        win["start"] + 1, win["end"])) + "\n")

        refined_path = prefix + "_refined_sites.tsv"
        cols = list(refined[0].keys()) if refined else [
            "mirna", "transcript_id", "gene_id", "gene_name", "site_type",
            "prelim_weight", "site_start_utr", "site_sequence", "window_id",
            "window_start_utr", "window_end_utr", "window_length",
            "site_offset_in_window", "miranda_confirmed", "miranda_score",
            "miranda_energy", "miranda_target_start", "miranda_target_end",
            "rnahybrid_mfe", "rnahybrid_pvalue", "rnahybrid_position",
            "mfe_confirmed", "refined_call"]
        with open(refined_path, "w") as fh:
            fh.write("\t".join(cols) + "\n")
            for row in refined:
                fh.write("\t".join(clean_field(row[c]) for c in cols) + "\n")

        # per-target aggregation
        grouped = {}
        for row in refined:
            key = (row["mirna"], row["transcript_id"])
            g = grouped.setdefault(key, {
                "gene_id": row["gene_id"], "gene_name": row["gene_name"],
                "windows": set(), "n_sites": 0, "n_confirmed": 0,
                "mfe_values": [], "miranda_scores": [],
            })
            g["windows"].add(row["window_id"])
            g["n_sites"] += 1
            if row["refined_call"] == "confirmed":
                g["n_confirmed"] += 1
            if row["rnahybrid_mfe"] != "":
                g["mfe_values"].append(float(row["rnahybrid_mfe"]))
            if row["miranda_score"] != "":
                g["miranda_scores"].append(float(row["miranda_score"]))
        targets_path = prefix + "_refined_targets.tsv"
        with open(targets_path, "w") as fh:
            fh.write("mirna\ttranscript_id\tgene_id\tgene_name\tn_windows\t"
                     "n_sites_tested\tn_confirmed\tbest_mfe_kcal_mol\t"
                     "best_miranda_score\tevidence_level\n")
            for (mir, tx), g in sorted(grouped.items(),
                                       key=lambda kv: (-kv[1]["n_confirmed"], kv[0])):
                best_mfe = min(g["mfe_values"]) if g["mfe_values"] else None
                best_sc = max(g["miranda_scores"]) if g["miranda_scores"] else None
                if g["n_confirmed"] >= 2 or (best_mfe is not None and best_mfe <= -25):
                    level = "strong"
                elif g["n_confirmed"] == 1:
                    level = "moderate"
                else:
                    level = "weak"
                fh.write("\t".join(clean_field(x) for x in (
                    mir, tx, g["gene_id"], g["gene_name"], len(g["windows"]),
                    g["n_sites"], g["n_confirmed"],
                    "" if best_mfe is None else "%.2f" % best_mfe,
                    "" if best_sc is None else "%.1f" % best_sc, level)) + "\n")

        # raw hit tables
        miranda_path = prefix + "_miranda_hits.tsv"
        with open(miranda_path, "w") as fh:
            fh.write("window_id\tmirna\ttranscript_id\tquery_start\tquery_end\t"
                     "target_start\ttarget_end\tscore\tenergy\n")
            for wid, hits in sorted(miranda_hits.items()):
                win = windows_by_id[wid]
                for mir, rs, re_, sc, en, qs, qe in hits:
                    fh.write("%s\t%s\t%s\t%d\t%d\t%d\t%d\t%.1f\t%.2f\n"
                             % (wid, clean_field(mir), win["transcript_id"],
                                qs, qe, rs, re_, sc, en))

        rnahybrid_path = prefix + "_rnahybrid_hits.tsv"
        with open(rnahybrid_path, "w") as fh:
            fh.write("window_id\ttranscript_id\tmirna\tposition\tmfe_kcal_mol\tp_value\n")
            for wid, hits in sorted(rnahybrid_hits.items()):
                win = windows_by_id[wid]
                for mir, mfe, pval, pos in hits:
                    fh.write("%s\t%s\t%s\t%d\t%.2f\t%s\n"
                             % (wid, win["transcript_id"], clean_field(mir), pos, mfe,
                                "" if pval is None else "%.6g" % pval))

        skipped_path = prefix + "_skipped.tsv"
        with open(skipped_path, "w") as fh:
            fh.write("mirna\ttranscript_id\tsite_type\tposition\treason\n")
            for row, reason in skipped:
                fh.write("%s\t%s\t%s\t%s\t%s\n"
                         % (clean_field(row["mirna"]), clean_field(row["transcript_id"]),
                            row["site_type"], row["position"], reason))

        counts = {}
        for row in refined:
            counts[row["refined_call"]] = counts.get(row["refined_call"], 0) + 1
        summary_path = prefix + "_refine_summary.tsv"
        with open(summary_path, "w") as fh:
            fh.write("metric\tvalue\n")
            for key, value in (
                ("sites_input", len(sites)),
                ("sites_mapped", len(mapped)),
                ("sites_selected", len(selected)),
                ("sites_refined", len(refined)),
                ("sites_skipped", len(skipped)),
                ("windows", len(windows)),
                ("mirnas", len(names)),
                ("engines", "+".join(methods)),
                ("confirmed", counts.get("confirmed", 0)),
                ("partial", counts.get("partial", 0)),
                ("not_confirmed", counts.get("not_confirmed", 0)),
                ("window_mode", args.window_mode),
                ("flank_nt", args.flank),
                ("merge_gap_nt", args.merge_gap),
                ("top_per_mirna", args.top_per_mirna),
                ("max_per_transcript", args.max_per_transcript),
                ("miranda_score", args.miranda_score),
                ("miranda_energy", args.miranda_energy),
                ("rnahybrid_energy", args.rnahybrid_energy),
                ("target_region", "3utr"),
                ("stage1_sites", clean_field(os.path.abspath(args.sites))),
            ):
                fh.write("%s\t%s\n" % (key, value))

        print()
        print("=== Refinement done ===")
        print("  windows        : %s (%d)" % (windows_fa, len(windows)))
        print("  refined sites  : %s (%d confirmed, %d partial, %d not)"
              % (refined_path, counts.get("confirmed", 0), counts.get("partial", 0),
                 counts.get("not_confirmed", 0)))
        print("  target summary : %s" % targets_path)
        print("  summary        : %s" % summary_path)
        if skipped:
            print("  skipped        : %s (%d)" % (skipped_path, len(skipped)))
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    main()
