#!/usr/bin/env python3
"""
miRNA conservation analysis (multi-species homolog alignment + conservation)

Extracts homologous mature miRNA sequences for a target miRNA across species from miRBase, aligns them,
computes per-position conservation (Shannon information content in bits + percent identity), and writes:
  - multiple sequence alignment FASTA (with gaps)
  - per-position conservation table (TSV)
  - summary statistics table (TSV)
  - publication-grade sequence logo (information content, 300 dpi PNG + optional SVG)
  - publication-grade multiple sequence alignment figure (300 dpi PNG + optional SVG)

Usage (mode 1: auto-extract homologs from miRBase):
  python conservation_analysis.py --mirna miR-21-5p \
      --reference-species hsa --outdir results/ --prefix miR-21

Usage (mode 2: user-supplied multiple sequence FASTA):
  python conservation_analysis.py --input-fa homologs.fa \
      --outdir results/ --prefix miR-21

Dependencies:
  Core (FASTA/MSA/conservation) uses only the standard library, with zero third-party dependencies.
  Plotting requires matplotlib (optional: if missing, figures are skipped and only TSVs are written).
"""

import argparse
import gzip
import math
import os
import shutil
import subprocess
import sys
import urllib.request

MIRBASE_URL = "https://www.mirbase.org/download/mature.fa"
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "mirna-target-tools")

# WebLogo standard base colors (RNA)
BASE_COLORS = {
    'A': '#2ecc71',  # green
    'C': '#3498db',  # blue
    'G': '#f39c12',  # orange
    'U': '#e74c3c',  # red
    'T': '#e74c3c',  # red (DNA T is merged into U)
}
VALID_BASES = set('ACGU')


# ---------------------------------------------------------------------------
# FASTA handling
# ---------------------------------------------------------------------------

def parse_fasta(path):
    """Parse FASTA (supports .gz). Returns [(header, seq), ...] where header includes '>'."""
    seqs = []
    name = None
    seq_parts = []
    opener = gzip.open if path.endswith('.gz') else open
    with opener(path, 'rt') as fh:
        for line in fh:
            line = line.rstrip('\n')
            if line.startswith('>'):
                if name is not None:
                    seqs.append((name, ''.join(seq_parts)))
                name = line[1:].strip()
                seq_parts = []
            else:
                if line.strip():
                    seq_parts.append(line.strip().upper())
        if name is not None:
            seqs.append((name, ''.join(seq_parts)))
    return seqs


def write_fasta(path, records):
    """records: [(header_without_>, seq), ...]"""
    with open(path, 'w') as fh:
        for header, seq in records:
            fh.write(f">{header}\n")
            for i in range(0, len(seq), 80):
                fh.write(seq[i:i + 80] + "\n")


def normalize_rna(seq):
    """Normalize to uppercase RNA, T -> U, keeping only ACGU (other characters become N)."""
    seq = seq.upper().replace('T', 'U')
    return ''.join(c if c in VALID_BASES else 'N' for c in seq)


# ---------------------------------------------------------------------------
# Sequence alignment (Needleman-Wunsch global alignment)
# ---------------------------------------------------------------------------

def needleman_wunsch(seq1, seq2, match=2, mismatch=-1, gap=-2):
    """Global alignment with free end gaps (suited to miRNA: conserved 5' seed, isomiR variation at the 3' end).

    The first row/column is initialized to 0 (no end-gap penalty), and traceback starts from the
    global maximum of the last row/column, keeping both sequences whole and pushing gaps to the ends.
    Returns (aligned1, aligned2), using '-' for gaps.
    """
    m, n = len(seq1), len(seq2)
    score = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            diag = score[i - 1][j - 1] + (match if seq1[i - 1] == seq2[j - 1] else mismatch)
            up = score[i - 1][j] + gap
            left = score[i][j - 1] + gap
            score[i][j] = max(diag, up, left)

    # Traceback start: global maximum of the last row/column (free end gaps)
    best = -1e9
    bi, bj = m, n
    for i in range(m + 1):
        if score[i][n] > best:
            best, bi, bj = score[i][n], i, n
    for j in range(n + 1):
        if score[m][j] > best:
            best, bi, bj = score[m][j], m, j

    # Trace back to (0, 0)
    mid1, mid2 = [], []
    i, j = bi, bj
    while i > 0 and j > 0:
        if score[i][j] == score[i - 1][j - 1] + \
                (match if seq1[i - 1] == seq2[j - 1] else mismatch):
            mid1.append(seq1[i - 1]); mid2.append(seq2[j - 1]); i -= 1; j -= 1
        elif score[i][j] == score[i - 1][j] + gap:
            mid1.append(seq1[i - 1]); mid2.append('-'); i -= 1
        else:
            mid1.append('-'); mid2.append(seq2[j - 1]); j -= 1
    # leading end gaps (free)
    while i > 0:
        mid1.append(seq1[i - 1]); mid2.append('-'); i -= 1
    while j > 0:
        mid1.append('-'); mid2.append(seq2[j - 1]); j -= 1
    mid1.reverse(); mid2.reverse()

    # trailing end gaps (free)
    tail1 = seq1[bi:]
    tail2 = seq2[bj:]
    L = max(len(tail1), len(tail2))
    tail1 = tail1 + '-' * (L - len(tail1))
    tail2 = tail2 + '-' * (L - len(tail2))
    return ''.join(mid1) + tail1, ''.join(mid2) + tail2


# ---------------------------------------------------------------------------
# Progressive multiple sequence alignment (star alignment)
#
# Model: an alignment = anchors (reference positions 0..L-1) + insertion slots (slot k lies
# between anchor k-1 and anchor k; k=0 is the start and k=L is the end). Each sequence has one
# character (or gap) at each anchor and some inserted characters in each slot. All sequences share
# the same set of insertion columns (max insert count for the slot, left-aligned, padded with '-').
# ---------------------------------------------------------------------------

def progressive_msa(seqs, names, ref_idx=0):
    """Returns dict: name -> aligned string (with gaps, all the same length)."""
    ref = seqs[ref_idx]
    L = len(ref)
    n = len(seqs)

    # Per-sequence anchor characters (list of L chars) and insertions (list of L+1 slots)
    anchor = {}
    insert = {}
    anchor[names[ref_idx]] = list(ref)
    insert[names[ref_idx]] = [[] for _ in range(L + 1)]

    for i in range(n):
        if i == ref_idx:
            continue
        name = names[i]
        s = seqs[i]
        a_ref, a_s = needleman_wunsch(ref, s)

        s_anchor = ['-'] * L
        s_insert = [[] for _ in range(L + 1)]
        ref_pos = 0
        for rc, sc in zip(a_ref, a_s):
            if rc == '-':
                # ref is a gap here => s inserts character sc "before anchor ref_pos"
                # belonging to insertion slot ref_pos (slot k = after anchor k-1, before anchor k)
                s_insert[ref_pos].append(sc)
            else:
                s_anchor[ref_pos] = sc
                ref_pos += 1
        anchor[name] = s_anchor
        insert[name] = s_insert

    # Merge insertion slots: each slot's width is the max insert count across sequences
    slot_len = [0] * (L + 1)
    for name in names:
        for k in range(L + 1):
            slot_len[k] = max(slot_len[k], len(insert[name][k]))

    # Render each sequence's final aligned string (insertions left-aligned, right-padded with '-')
    result = {}
    for name in names:
        chars = []
        for k in range(L + 1):
            ins = insert[name][k]
            chars.extend(ins)
            chars.extend(['-'] * (slot_len[k] - len(ins)))
            if k < L:
                chars.append(anchor[name][k])
        result[name] = ''.join(chars)
    return result


# ---------------------------------------------------------------------------
# Conservation computation
# ---------------------------------------------------------------------------

def position_conservation(column_chars):
    """Given a column of characters (including gap/N), compute conservation metrics.

    Returns dict: consensus, identity(%), bits, counts, gap_count, valid_count
    - bits: Shannon information content = log2(4) - H, from the ACGU distribution excluding gap/N
    - identity: percentage of non-gap/N sequences matching the most common base (%)
    """
    counts = {'A': 0, 'C': 0, 'G': 0, 'U': 0}
    gap_count = 0
    for ch in column_chars:
        if ch == '-':
            gap_count += 1
        elif ch in counts:
            counts[ch] += 1
        else:
            # 'N' or anything else: treated as missing, not counted
            gap_count += 1
    valid = sum(counts.values())
    total = len(column_chars)

    total = len(column_chars)
    coverage = (valid / total * 100.0) if total > 0 else 0.0
    gap_percent = (gap_count / total * 100.0) if total > 0 else 0.0

    if valid == 0:
        return {
            'consensus': '-', 'identity': 0.0, 'bits': 0.0,
            'counts': counts, 'gap_count': gap_count, 'valid_count': 0,
            'gap_percent': gap_percent, 'coverage': coverage, 'total': total,
        }

    # Information content (bits, from the ACGU distribution excluding gaps)
    H = 0.0
    for b in 'ACGU':
        c = counts[b]
        if c > 0:
            p = c / valid
            H -= p * math.log2(p)
    bits = 2.0 - H  # log2(4) = 2 for RNA

    consensus = max('ACGU', key=lambda b: counts[b])
    identity = counts[consensus] / valid * 100.0

    return {
        'consensus': consensus, 'identity': identity, 'bits': bits,
        'counts': counts, 'gap_count': gap_count, 'valid_count': valid,
        'gap_percent': gap_percent, 'coverage': coverage, 'total': total,
    }


def pairwise_identity(aligned1, aligned2):
    """Pairwise identity (%) between two sequences (equal length, with gaps; only non-gap sites)."""
    match = 0
    total = 0
    for a, b in zip(aligned1, aligned2):
        if a == '-' or b == '-':
            continue
        total += 1
        if a == b:
            match += 1
    return (match / total * 100.0) if total > 0 else 0.0


# ---------------------------------------------------------------------------
# Visualization
# ---------------------------------------------------------------------------

# Shared journal-friendly look (matches plot_enrichment.py):
# white background, no top/right spines, muted ticks, left-aligned title,
# soft amber wash for the seed region, editable text in SVG output.
INK = '#222222'
MUTED = '#6b7280'
GRID = '#e9e9e9'
SEED_TINT = '#FBF0D5'
GAP_COLOR = '#E4E7EB'


def _setup_matplotlib():
    """Import matplotlib lazily and apply the shared plotting style."""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        return None
    matplotlib.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica', 'sans-serif'],
        'axes.unicode_minus': False,
        'svg.fonttype': 'none',
    })
    return plt


def _style_axes(ax, grid_axis=None):
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    for side in ('left', 'bottom'):
        ax.spines[side].set_color('#c9ccd1')
        ax.spines[side].set_linewidth(0.9)
    ax.tick_params(colors=MUTED, length=3, width=0.9)
    ax.tick_params(axis='y', length=0)
    ax.set_axisbelow(True)
    if grid_axis:
        ax.grid(axis=grid_axis, color=GRID, linewidth=0.8)
    else:
        ax.grid(False)


def _save(fig, plt, out_png, out_svg=None, dpi=300):
    fig.savefig(out_png, dpi=dpi, bbox_inches='tight', facecolor='white')
    if out_svg:
        fig.savefig(out_svg, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def _position_ticks(ax, width, fontsize=7.5):
    if width <= 30:
        step = 1
    elif width <= 60:
        step = 2
    else:
        step = 5
    ticks = list(range(1, width + 1, step))
    ax.set_xticks(ticks)
    ax.set_xticklabels([str(t) for t in ticks], fontsize=fontsize)
    ax.set_xlim(0.5, width + 0.5)


def draw_sequence_logo(msa, names, seed_start, seed_end, out_png, out_svg=None):
    """Draw the information-content sequence logo. msa: dict name -> aligned string."""
    plt = _setup_matplotlib()
    if plt is None:
        print("Warning: matplotlib is not installed; skipping the sequence logo plot.")
        return False
    from matplotlib.patches import Rectangle

    aligned = [msa[n] for n in names]
    width = len(aligned[0])
    cols = [[aligned[r][c] for r in range(len(aligned))] for c in range(width)]
    stats = [position_conservation(col) for col in cols]

    fig, ax = plt.subplots(figsize=(max(6.5, width * 0.46), 3.0))
    fig.patch.set_facecolor('white')

    # seed-region background wash (drawn first, keeps bubbles crisp)
    if seed_start and seed_end:
        ax.axvspan(seed_start - 0.5, seed_end + 0.5, color=SEED_TINT, zorder=0)
        ax.text((seed_start + seed_end) / 2.0, 2.10,
                'seed (nt %d-%d)' % (seed_start, seed_end),
                ha='center', va='bottom', fontsize=8, color='#9a7b3f',
                style='italic', zorder=5)

    for c in range(width):
        st = stats[c]
        x = c + 1
        if st['valid_count'] == 0:
            ax.add_patch(Rectangle((x - 0.45, 0), 0.9, 2.0, facecolor=GAP_COLOR,
                                   edgecolor='none', zorder=2))
            continue
        coverage = st['coverage']
        bits = st['bits']
        # scale by coverage below 50% so sparse columns do not look over-confident
        eff_bits = bits if coverage >= 50.0 else bits * (coverage / 100.0)
        bottom = 0.0
        for b in sorted('ACGU', key=lambda b: st['counts'][b], reverse=True):
            cnt = st['counts'][b]
            if cnt == 0:
                continue
            h = (cnt / st['valid_count']) * eff_bits
            if h <= 0.001:
                continue
            ax.add_patch(Rectangle((x - 0.45, bottom), 0.9, h,
                                   facecolor=BASE_COLORS[b], edgecolor='white',
                                   linewidth=0.5, zorder=3))
            if h >= 0.22:
                ax.text(x, bottom + h / 2.0, b, ha='center', va='center',
                        fontsize=9.5, fontweight='bold', color='white', zorder=4)
            bottom += h
        if coverage < 50.0:
            ax.text(x, 2.04, '%d%%' % round(coverage), ha='center', va='bottom',
                    fontsize=6.5, color=MUTED, zorder=5)

    _position_ticks(ax, width)
    ax.set_ylim(0, 2.18)
    ax.set_yticks([0, 0.5, 1.0, 1.5, 2.0])
    ax.set_xlabel('Position (nt, 5\u2032 \u2192 3\u2032)', fontsize=10, color=INK, labelpad=6)
    ax.set_ylabel('Information content (bits)', fontsize=10, color=INK, labelpad=6)
    ax.set_title('miRNA sequence conservation', loc='left', fontsize=12.5,
                 color=INK, pad=14)
    _style_axes(ax)

    _save(fig, plt, out_png, out_svg)
    return True


def draw_alignment(msa, names, seed_start, seed_end, out_png, out_svg=None):
    """Draw the multiple sequence alignment figure."""
    plt = _setup_matplotlib()
    if plt is None:
        print("Warning: matplotlib is not installed; skipping the alignment plot.")
        return False
    from matplotlib.patches import Rectangle

    aligned = [msa[n] for n in names]
    n_rows = len(aligned)
    width = len(aligned[0])

    fig, ax = plt.subplots(figsize=(max(6.5, width * 0.40), max(2.4, n_rows * 0.42)))
    fig.patch.set_facecolor('white')

    if seed_start and seed_end:
        ax.axvspan(seed_start - 0.5, seed_end + 0.5, color=SEED_TINT, zorder=0)

    for r, name in enumerate(names):
        seq = aligned[r]
        y = n_rows - r  # reference on top
        for c, ch in enumerate(seq):
            if ch == '-':
                face = GAP_COLOR
            elif ch in BASE_COLORS:
                face = BASE_COLORS[ch]
            else:
                face = '#B8BDC4'
            ax.add_patch(Rectangle((c + 0.5, y - 0.36), 1.0, 0.72,
                                   facecolor=face, edgecolor='white',
                                   linewidth=0.3, zorder=2))
            if ch != '-':
                ax.text(c + 1.0, y, ch, ha='center', va='center', fontsize=8.5,
                        fontweight='bold', color='white', zorder=3)
        if r:
            ax.axhline(y + 0.5, color='#F1F3F5', linewidth=0.8, zorder=1)

    _position_ticks(ax, width, fontsize=7.0)
    ax.set_ylim(0.5, n_rows + 0.5)
    ax.set_yticks(range(1, n_rows + 1))
    ax.set_yticklabels(names, fontsize=8.5, color=INK)
    ax.set_xlabel('Position (nt, 5\u2032 \u2192 3\u2032)', fontsize=10, color=INK, labelpad=6)
    title = 'Multiple sequence alignment'
    if seed_start and seed_end:
        title += '  (seed nt %d-%d highlighted)' % (seed_start, seed_end)
    ax.set_title(title, loc='left', fontsize=12.5, color=INK, pad=14)
    _style_axes(ax)

    _save(fig, plt, out_png, out_svg)
    return True


# ---------------------------------------------------------------------------
# Main flow
# ---------------------------------------------------------------------------

def fetch_mature_fa(mature_fa=None):
    """Return the mature.fa path (local file or download cache)."""
    if mature_fa and os.path.exists(mature_fa):
        return mature_fa

    cache_path = os.path.join(CACHE_DIR, "mature.fa")
    if os.path.exists(cache_path):
        return cache_path

    os.makedirs(CACHE_DIR, exist_ok=True)
    print(f"Downloading miRBase mature.fa ... ({MIRBASE_URL})")
    try:
        req = urllib.request.Request(MIRBASE_URL, headers={'User-Agent': 'mirna-target-tools/1.0'})
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = resp.read()
        with open(cache_path, 'wb') as fh:
            fh.write(data)
        print(f"Cached to {cache_path} ({len(data)} bytes)")
        return cache_path
    except Exception as e:
        print(f"Error: failed to download miRBase mature.fa: {e}")
        print("Please download it manually and pass: --mature-fa /path/to/mature.fa")
        sys.exit(1)


def extract_homologs(mature_fa, mirna_id, species_filter=None):
    """Extract all homologs of mirna_id from mature.fa.

    mirna_id looks like 'miR-21-5p' (without the species prefix).
    Returns [(species_prefix, mirna_id, accession, species_name, seq), ...]
    """
    records = parse_fasta(mature_fa)
    hits = []
    for header, seq in records:
        # header: 'hsa-miR-21-5p MIMAT0000076 Homo sapiens miR-21-5p'
        fields = header.split()
        if not fields:
            continue
        name_field = fields[0]  # 'hsa-miR-21-5p'
        if '-' not in name_field:
            continue
        prefix, rest = name_field.split('-', 1)
        # Exact mirbase-id match (rest == mirna_id) to avoid prefix collisions such as miR-21 vs miR-210
        if rest != mirna_id:
            continue
        accession = fields[1] if len(fields) > 1 else ''
        # Species name = middle fields (drop name_field, accession, and the trailing mirna-id)
        if len(fields) >= 4:
            species_name = ' '.join(fields[2:-1])
        else:
            species_name = prefix
        if species_filter and prefix not in species_filter:
            continue
        hits.append((prefix, mirna_id, accession, species_name, normalize_rna(seq)))
    return hits


SKILL_SCRIPTS = os.path.dirname(os.path.abspath(__file__))
R_CONSERVATION_SCRIPT = os.path.join(SKILL_SCRIPTS, 'plot_conservation.R')
R_PLOT_PKGS = ('ggplot2', 'dplyr')


def r_engine_status():
    """Return (ok, message) for the R plotting engine (Rscript + packages)."""
    if shutil.which('Rscript') is None:
        return False, 'Rscript not found on PATH'
    check = ' && '.join('requireNamespace("%s", quietly=TRUE)' % p for p in R_PLOT_PKGS)
    try:
        proc = subprocess.run(['Rscript', '-e', 'cat(%s)' % check],
                              capture_output=True, text=True, timeout=180)
    except Exception as exc:                      # pragma: no cover
        return False, 'Rscript failed: %s' % exc
    if proc.stdout.strip().upper().startswith('TRUE'):
        return True, 'R + ' + '/'.join(R_PLOT_PKGS)
    return False, 'missing R packages: %s' % ', '.join(R_PLOT_PKGS)


def draw_with_r(outdir, prefix, seed_start, seed_end):
    """Draw the logo + alignment with the ggplot2 script. True on success."""
    if not os.path.exists(R_CONSERVATION_SCRIPT):
        print("  R plotting script not found: %s" % R_CONSERVATION_SCRIPT)
        return False
    cmd = ['Rscript', R_CONSERVATION_SCRIPT,
           '--outdir', outdir, '--prefix', prefix,
           '--seed-start', str(seed_start), '--seed-end', str(seed_end)]
    print("  drawing figures with R (ggplot2) ...")
    return subprocess.call(cmd) == 0


def run_conservation(records, names, seed_start, seed_end, outdir, prefix,
                     ref_idx=0, make_plots=True, engine='auto'):
    """records: [(seq, ...)] parallel to names, already normalized. Runs alignment + conservation + output."""
    os.makedirs(outdir, exist_ok=True)
    seqs = [r[4] for r in records]
    full_names = [f"{r[0]}-{r[1]}" for r in records]  # 'hsa-miR-21-5p'

    # MSA
    msa = progressive_msa(seqs, full_names, ref_idx=ref_idx)
    # Preserve input order
    aligned_seqs = [msa[n] for n in full_names]

    # 1) Alignment FASTA
    fasta_path = os.path.join(outdir, f"{prefix}_aligned.fa")
    write_fasta(fasta_path, [
        (f"{r[0]}-{r[1]} {r[2]} {r[3]}", aligned_seqs[i])
        for i, r in enumerate(records)
    ])

    # 2) Per-position conservation table
    width = len(aligned_seqs[0])
    cols = [[aligned_seqs[r][c] for r in range(len(aligned_seqs))] for c in range(width)]
    cons_path = os.path.join(outdir, f"{prefix}_conservation.tsv")
    with open(cons_path, 'w') as fh:
        fh.write("position\tconsensus\tidentity_percent\tbits\tA\tC\tG\tU\tgap\tvalid_count\tcoverage_percent\tis_seed\n")
        for c in range(width):
            st = position_conservation(cols[c])
            is_seed = 'yes' if (seed_start and seed_end and
                                (seed_start <= c + 1 <= seed_end)) else 'no'
            fh.write(
                f"{c + 1}\t{st['consensus']}\t{st['identity']:.2f}\t{st['bits']:.3f}\t"
                f"{st['counts']['A']}\t{st['counts']['C']}\t{st['counts']['G']}\t{st['counts']['U']}\t"
                f"{st['gap_count']}\t{st['valid_count']}\t{st['coverage']:.1f}\t{is_seed}\n"
            )

    # 3) Summary statistics
    stats = [position_conservation(col) for col in cols]
    seed_bits = []
    seed_identity = []
    all_bits = [s['bits'] for s in stats]
    all_identity = [s['identity'] for s in stats]
    for c in range(width):
        if seed_start and seed_end and (seed_start <= c + 1 <= seed_end):
            seed_bits.append(stats[c]['bits'])
            seed_identity.append(stats[c]['identity'])

    # Core region (coverage >= 50%) statistics
    core_bits = [s['bits'] for s in stats if s['coverage'] >= 50.0]
    core_identity = [s['identity'] for s in stats if s['coverage'] >= 50.0]

    # Mean pairwise identity
    pw = []
    for i in range(len(aligned_seqs)):
        for j in range(i + 1, len(aligned_seqs)):
            pw.append(pairwise_identity(aligned_seqs[i], aligned_seqs[j]))
    avg_pw = sum(pw) / len(pw) if pw else 0.0

    summary_path = os.path.join(outdir, f"{prefix}_summary.tsv")
    with open(summary_path, 'w') as fh:
        fh.write("metric\tvalue\n")
        fh.write(f"mirna\t{records[0][1]}\n")
        fh.write(f"num_species\t{len(records)}\n")
        fh.write(f"species_list\t{','.join(r[0] for r in records)}\n")
        fh.write(f"alignment_length\t{width}\n")
        fh.write(f"mean_bits_all\t{sum(all_bits) / width:.3f}\n")
        fh.write(f"mean_identity_all_percent\t{sum(all_identity) / width:.2f}\n")
        if seed_bits:
            fh.write(f"mean_bits_seed\t{sum(seed_bits) / len(seed_bits):.3f}\n")
            fh.write(f"mean_identity_seed_percent\t{sum(seed_identity) / len(seed_identity):.2f}\n")
        if core_bits:
            fh.write(f"core_region_length\t{len(core_bits)}\n")
            fh.write(f"mean_bits_core\t{sum(core_bits) / len(core_bits):.3f}\n")
            fh.write(f"mean_identity_core_percent\t{sum(core_identity) / len(core_identity):.2f}\n")
        fh.write(f"mean_pairwise_identity_percent\t{avg_pw:.2f}\n")
        fully_conserved = sum(1 for s in stats if s['identity'] >= 100.0 and s['valid_count'] > 0)
        fh.write(f"fully_conserved_positions\t{fully_conserved}\n")

    # 4) Figures - R (ggplot2) by default, matplotlib as the fallback
    ok_logo = ok_aln = False
    if make_plots:
        if engine in ('auto', 'r'):
            ok, why = r_engine_status()
            if ok:
                ok_logo = ok_aln = draw_with_r(outdir, prefix, seed_start, seed_end)
                if not ok_logo:
                    print("  R plotting failed%s" % ("" if engine == 'auto' else ""))
            else:
                print("  R plotting engine unavailable: %s" % why)
                print("  install it with: bash %s"
                      % os.path.join(SKILL_SCRIPTS, 'install_r_deps.sh'))
            if not ok_logo and engine == 'r':
                raise SystemExit("Error: R plotting was requested but is unavailable.")
        if not ok_logo:
            if engine == 'auto':
                print("  falling back to the Python (matplotlib) engine")
            logo_png = os.path.join(outdir, f"{prefix}_sequence_logo.png")
            logo_svg = os.path.join(outdir, f"{prefix}_sequence_logo.svg")
            aln_png = os.path.join(outdir, f"{prefix}_alignment.png")
            aln_svg = os.path.join(outdir, f"{prefix}_alignment.svg")
            ok_logo = draw_sequence_logo(msa, full_names, seed_start, seed_end, logo_png, logo_svg)
            ok_aln = draw_alignment(msa, full_names, seed_start, seed_end, aln_png, aln_svg)

    return {
        'fasta': fasta_path,
        'conservation': cons_path,
        'summary': summary_path,
        'num_species': len(records),
        'width': width,
    }


def main():
    parser = argparse.ArgumentParser(
        description='miRNA conservation analysis (multi-species homolog alignment + conservation plots)')
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument('--mirna', help='target miRNA (e.g. miR-21-5p); homologs are extracted from miRBase')
    src.add_argument('--input-fa', help='user-supplied multiple sequence FASTA file')
    parser.add_argument('--mature-fa', help='path to a local miRBase mature.fa (optional)')
    parser.add_argument('--reference-species', default=None,
                        help='reference species prefix (e.g. chi/hsa) used as the alignment anchor; defaults to the first sequence')
    parser.add_argument('--species', default=None,
                        help='comma-separated allow-list of species prefixes (e.g. hsa,chi,bta,mmu); defaults to all')
    parser.add_argument('--seed-start', type=int, default=2, help='seed region start nt (default 2)')
    parser.add_argument('--seed-end', type=int, default=8, help='seed region end nt (default 8)')
    parser.add_argument('--outdir', default='.', help='output directory (default: current)')
    parser.add_argument('--prefix', default='mirna_conservation', help='prefix for output files')
    parser.add_argument('--no-plot', action='store_true', help='skip plotting (TSV output only)')
    parser.add_argument('--engine', default='auto', choices=['auto', 'r', 'python'],
                        help='Plotting engine: auto (R when available, else Python), '
                             'r (ggplot2, default choice), python (matplotlib fallback)')
    args = parser.parse_args()

    if args.seed_start < 1 or args.seed_end < args.seed_start:
        print("Error: invalid seed region (required: 1 <= seed-start <= seed-end).")
        sys.exit(1)

    # Obtain sequences
    if args.mirna:
        mature_fa = fetch_mature_fa(args.mature_fa)
        species_filter = set(s.strip() for s in args.species.split(',')) \
            if args.species else None
        records = extract_homologs(mature_fa, args.mirna, species_filter)
        if not records:
            print(f"Error: no homologs found for '{args.mirna}' in miRBase.")
            print("Please check the name (e.g. miR-21-5p, without a species prefix).")
            sys.exit(1)
        print(f"Found homologs in {len(records)} species:")
        for r in records:
            print(f"  {r[0]:>5}  {r[4]}")
    else:
        # User-supplied FASTA
        raw = parse_fasta(args.input_fa)
        records = []
        for header, seq in raw:
            name_field = header.split()[0]
            if '-' in name_field:
                prefix, mirna_id = name_field.split('-', 1)
            else:
                prefix, mirna_id = name_field, 'unknown'
            records.append((prefix, mirna_id, '', '', normalize_rna(seq)))
        if len(records) < 2:
            print("Error: --input-fa requires at least 2 sequences.")
            sys.exit(1)
        print(f"Read {len(records)} sequences.")

    # Determine the reference sequence
    ref_idx = 0
    if args.reference_species:
        for i, r in enumerate(records):
            if r[0] == args.reference_species:
                ref_idx = i
                break
        else:
            print(f"Warning: reference species '{args.reference_species}' not found; using the first sequence.")

    result = run_conservation(
        records, [r[0] for r in records], args.seed_start, args.seed_end,
        args.outdir, args.prefix, ref_idx=ref_idx, make_plots=not args.no_plot,
        engine=args.engine)

    print()
    print("=== Output files ===")
    print(f"  alignment FASTA     : {result['fasta']}")
    print(f"  per-position table  : {result['conservation']}")
    print(f"  summary table       : {result['summary']}")
    if not args.no_plot:
        print(f"  sequence logo (PNG) : {os.path.join(args.outdir, args.prefix + '_sequence_logo.png')}")
        print(f"  sequence logo (SVG) : {os.path.join(args.outdir, args.prefix + '_sequence_logo.svg')}")
        print(f"  alignment (PNG)     : {os.path.join(args.outdir, args.prefix + '_alignment.png')}")
        print(f"  alignment (SVG)     : {os.path.join(args.outdir, args.prefix + '_alignment.svg')}")
    print(f"\n{result['num_species']} species, alignment length {result['width']} nt.")
    print("Done!")


if __name__ == '__main__':
    main()
