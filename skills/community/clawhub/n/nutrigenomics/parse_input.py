"""
parse_input.py — Multi-format genetic data parser
Supports: 23andMe .txt, AncestryDNA .csv, standard VCF
Returns: dict mapping rsid -> genotype string (e.g. "AT", "TT")
"""

import csv
import re
from pathlib import Path

from path_safety import (
    MAX_HEADER_LINES,
    MAX_LINE_BYTES,
    MAX_VARIANTS,
    validate_input_file,
)


# Genotype calls are read from a user-supplied file and later rendered into a
# Markdown report, so they are untrusted text until proven otherwise. Only
# nucleotide calls are accepted: A/C/G/T plus D and I, which 23andMe uses for
# deletions and insertions. A run is allowed because a VCF call joins REF/ALT
# alleles and an indel can be several bases. Anything else is discarded rather
# than scored -- a "genotype" that is not a genotype cannot be biologically
# meaningful, and must never reach the report.
_VALID_GENOTYPE = re.compile(r"^[ACGTDI]{1,32}$")


def clean_genotype(value: str):
    """Return an uppercased genotype call, or None if it is not a valid call."""
    if not isinstance(value, str):
        return None
    cleaned = value.strip().upper().replace("-", "")
    if not cleaned or not _VALID_GENOTYPE.match(cleaned):
        return None
    return cleaned


def _bounded(lines, genotypes):
    """
    Yield lines, stopping cleanly once the variant cap is reached and skipping
    absurdly long lines.

    Streaming bounds how much of the FILE is held at once; it does not bound the
    genotype table, which grows with the number of variants. A crafted file with
    tens of millions of rows would still exhaust memory, so parsing stops at
    MAX_VARIANTS and over-long lines are discarded rather than buffered.
    """
    for line in lines:
        if len(genotypes) >= MAX_VARIANTS:
            break
        if len(line) > MAX_LINE_BYTES:
            continue
        yield line


def detect_format(filepath: str) -> str:
    """Auto-detect genetic file format from header."""
    with open(filepath, encoding="utf-8", errors="replace") as f:
        # Only the header region is informative. Reading the whole file to sniff
        # a format lets a crafted file of pure comment lines stall detection.
        for _n, line in enumerate(f):
            if _n >= MAX_HEADER_LINES:
                break
            if len(line) > MAX_LINE_BYTES:
                continue
            if line.startswith("##fileformat=VCF"):
                return "vcf"
            if "rsid" in line.lower() and "chromosome" in line.lower() and "genotype" in line.lower():
                return "23andme"
            if "rsid" in line.lower() and "allele1" in line.lower():
                return "ancestry"
            if not line.startswith("#"):
                break
    # Fallback: infer from extension
    ext = Path(filepath).suffix.lower()
    if ext == ".vcf":
        return "vcf"
    if ext == ".csv":
        return "ancestry"
    return "23andme"


def parse_23andme(filepath: str) -> dict:
    """Parse 23andMe raw data file. Returns {rsid: genotype}."""
    genotypes = {}
    with open(filepath, encoding="utf-8", errors="replace") as f:
        for line in _bounded(f, genotypes):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 4:
                continue
            rsid, chrom, pos, genotype = parts[0], parts[1], parts[2], parts[3]
            if rsid.startswith("rs"):
                call = clean_genotype(genotype)
                if call:
                    genotypes[rsid] = call
    return genotypes


def parse_ancestry(filepath: str) -> dict:
    """
    Parse an AncestryDNA raw data file. Returns {rsid: genotype}.

    The file is streamed. csv.DictReader accepts any iterable of strings, so
    comment lines are filtered by a generator rather than by building a list of
    every line first — a consumer genetic file is large, and materialising it
    made memory use scale with input size (ClawHub audit T09, memory exhaustion).
    """
    genotypes = {}
    with open(filepath, encoding="utf-8", errors="replace") as f:
        rows = (line for line in _bounded(f, genotypes) if not line.startswith("#"))
        for row in csv.DictReader(rows, delimiter="\t"):
            rsid = row.get("rsid", "").strip()
            allele1 = row.get("allele1", "").strip()
            allele2 = row.get("allele2", "").strip()
            if rsid.startswith("rs"):
                call = clean_genotype(allele1 + allele2)
                if call:
                    genotypes[rsid] = call
    return genotypes


def parse_vcf(filepath: str) -> dict:
    """Parse VCF file, extracting GT field. Returns {rsid: genotype_bases}."""
    genotypes = {}
    chrom_col, pos_col, id_col, ref_col, alt_col, gt_col = 0, 1, 2, 3, 4, 9

    with open(filepath, encoding="utf-8", errors="replace") as f:
        for line in _bounded(f, genotypes):
            line = line.strip()
            if line.startswith("##"):
                continue
            if line.startswith("#CHROM"):
                continue
            parts = line.split("\t")
            if len(parts) < 10:
                continue
            rsid = parts[id_col]
            if not rsid.startswith("rs"):
                continue
            ref = parts[ref_col]
            alts = parts[alt_col].split(",")
            alleles = [ref] + alts

            fmt = parts[8].split(":")
            gt_idx = fmt.index("GT") if "GT" in fmt else 0
            sample = parts[gt_col].split(":")[gt_idx]
            # Handle phased (|) or unphased (/)
            indices = re.split(r"[|/]", sample)
            try:
                called = "".join(alleles[int(i)] for i in indices if i != ".")
                call = clean_genotype(called)
                if call:
                    genotypes[rsid] = call
            except (IndexError, ValueError):
                pass
    return genotypes


def parse_genetic_file(filepath: str, fmt: str = "auto") -> dict:
    """Parse genetic data file in any supported format."""
    filepath = str(validate_input_file(filepath))

    if fmt == "auto":
        fmt = detect_format(filepath)
    
    parsers = {
        "23andme": parse_23andme,
        "ancestry": parse_ancestry,
        "vcf": parse_vcf,
    }
    
    if fmt not in parsers:
        raise ValueError(f"Unknown format: {fmt}. Choose from: {list(parsers.keys())}")
    
    return parsers[fmt](filepath)
