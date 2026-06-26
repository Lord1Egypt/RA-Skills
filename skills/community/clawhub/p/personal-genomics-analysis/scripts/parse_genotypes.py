#!/usr/bin/env python3
"""
Universal genotype parser for consumer genetic testing data.
Supports: WeGene, 23andMe, AncestryDNA, VCF (compressed and uncompressed).
Outputs a unified genotype dictionary for downstream analysis.
"""

import gzip
import os
import sys
from collections import defaultdict


def detect_format(filepath):
    """Auto-detect genetic data file format."""
    ext = filepath.lower()
    if ext.endswith('.vcf') or ext.endswith('.vcf.gz'):
        return 'vcf'
    if ext.endswith('.cram'):
        return 'cram'
    if ext.endswith('.bam'):
        return 'bam'

    opener = gzip.open if filepath.endswith('.gz') else open
    try:
        with opener(filepath, 'rt', errors='replace') as f:
            lines = [f.readline() for _ in range(20)]
    except:
        return 'unknown'

    text = ''.join(lines)
    if '23andMe' in text:
        return '23andme'
    if 'AncestryDNA' in text:
        return 'ancestrydna'

    for line in lines:
        if line.startswith('#') or not line.strip():
            continue
        cols = line.strip().split('\t')
        if len(cols) == 5 and cols[0].startswith('rs'):
            return 'ancestrydna'
        if len(cols) == 4 and cols[0].startswith('rs'):
            return 'wegene'
        break

    return 'unknown'


def parse_wegene(filepath):
    """Parse WeGene TSV format: rsid \\t chromosome \\t position \\t genotype"""
    data = {}
    with open(filepath, 'r', errors='replace') as f:
        for line in f:
            if line.startswith('#') or line.startswith('rsid') or not line.strip():
                continue
            parts = line.strip().split('\t')
            if len(parts) >= 4 and parts[3] not in ('--', ''):
                data[parts[0]] = {
                    'chrom': parts[1], 'pos': parts[2], 'genotype': parts[3]
                }
    return data


def parse_23andme(filepath):
    """Parse 23andMe TSV format (same as WeGene but with # comment headers)."""
    data = {}
    with open(filepath, 'r', errors='replace') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.strip().split('\t')
            if len(parts) >= 4 and parts[3] not in ('--', ''):
                if parts[0].startswith('rs') or parts[0].startswith('i'):
                    data[parts[0]] = {
                        'chrom': parts[1], 'pos': parts[2], 'genotype': parts[3]
                    }
    return data


def parse_ancestrydna(filepath):
    """Parse AncestryDNA format: rsid \\t chromosome \\t position \\t allele1 \\t allele2"""
    data = {}
    with open(filepath, 'r', errors='replace') as f:
        for line in f:
            if line.startswith('#') or line.startswith('rsid') or not line.strip():
                continue
            parts = line.strip().split('\t')
            if len(parts) >= 5 and parts[3] != '0' and parts[4] != '0':
                data[parts[0]] = {
                    'chrom': parts[1], 'pos': parts[2],
                    'genotype': parts[3] + parts[4]
                }
    return data


def parse_vcf(filepath, target_rsids=None, target_positions=None):
    """
    Parse VCF file. If targets are specified, only extract those variants.
    target_rsids: set of rsid strings to look for
    target_positions: dict of "chr:pos" -> rsid for position-based lookup
    Returns: (genotype_dict, quality_stats)
    """
    data = {}
    stats = {
        'total_variants': 0, 'pass_variants': 0,
        'ti': 0, 'tv': 0, 'depth_sum': 0, 'depth_count': 0,
        'chrom_counts': defaultdict(int), 'het_count': 0, 'hom_count': 0
    }

    transitions = {('A', 'G'), ('G', 'A'), ('C', 'T'), ('T', 'C')}
    opener = gzip.open if filepath.endswith('.gz') else open

    with opener(filepath, 'rt') as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split('\t', 10)
            if len(parts) < 10:
                continue

            chrom, pos, rsid_col, ref, alt = parts[0:5]
            filt = parts[6]
            stats['total_variants'] += 1
            stats['chrom_counts'][chrom] += 1

            if filt == 'PASS' or filt == '.':
                stats['pass_variants'] += 1

            # Ti/Tv calculation (SNPs only)
            if len(ref) == 1 and len(alt) == 1 and alt != '.':
                if (ref, alt) in transitions:
                    stats['ti'] += 1
                else:
                    stats['tv'] += 1

            # Parse sample fields
            fmt_fields = parts[8].split(':')
            sample_fields = parts[9].split(':')
            sample_dict = dict(zip(fmt_fields, sample_fields))

            gt = sample_dict.get('GT', '.')
            dp = sample_dict.get('DP', '.')

            if dp != '.' and dp.isdigit():
                stats['depth_sum'] += int(dp)
                stats['depth_count'] += 1

            # Determine genotype
            alleles_list = [ref] + alt.split(',')
            gt_indices = gt.replace('|', '/').split('/')
            try:
                geno_alleles = [alleles_list[int(g)] for g in gt_indices if g != '.']
            except (ValueError, IndexError):
                geno_alleles = []

            genotype_str = ''.join(geno_alleles)

            if len(geno_alleles) == 2:
                if geno_alleles[0] != geno_alleles[1]:
                    stats['het_count'] += 1
                else:
                    stats['hom_count'] += 1

            # Check if this is a target variant
            matched_id = None
            if target_rsids and rsid_col in target_rsids:
                matched_id = rsid_col
            elif target_positions and f"{chrom}:{pos}" in target_positions:
                matched_id = target_positions[f"{chrom}:{pos}"]

            if matched_id or (target_rsids is None and target_positions is None):
                store_id = matched_id or rsid_col
                data[store_id] = {
                    'chrom': chrom, 'pos': pos, 'ref': ref, 'alt': alt,
                    'filter': filt, 'genotype': genotype_str,
                    'dp': dp, 'gq': sample_dict.get('GQ', '.'),
                    'ad': sample_dict.get('AD', '.'),
                    'gt_raw': gt, 'vcf_rsid': rsid_col
                }

    return data, stats


def build_unified_dict(*sources):
    """Merge multiple genotype sources into unified {rsid: genotype} dict.
    First source takes priority (typically chip data, faster lookup)."""
    unified = {}
    for source in sources:
        for rsid, info in source.items():
            if rsid not in unified:
                geno = info.get('genotype', '')
                if isinstance(geno, str) and '/' in geno:
                    geno = geno.replace('/', '')
                unified[rsid] = geno
    return unified


def print_summary(fmt, data, stats=None):
    """Print parsing summary."""
    print(f"  Format: {fmt}")
    print(f"  Variants loaded: {len(data):,}")
    if stats:
        print(f"  Total variants in file: {stats['total_variants']:,}")
        print(f"  PASS variants: {stats['pass_variants']:,}")
        if stats['tv'] > 0:
            print(f"  Ti/Tv ratio: {stats['ti']/stats['tv']:.2f}")
        if stats['depth_count'] > 0:
            print(f"  Average depth: {stats['depth_sum']/stats['depth_count']:.1f}x")
        if stats['hom_count'] > 0:
            print(f"  Het/Hom ratio: {stats['het_count']/stats['hom_count']:.2f}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python parse_genotypes.py <file1> [file2] ...")
        sys.exit(1)

    all_data = {}
    for filepath in sys.argv[1:]:
        print(f"\nParsing: {filepath}")
        fmt = detect_format(filepath)

        if fmt == 'wegene':
            data = parse_wegene(filepath)
            print_summary(fmt, data)
            all_data.update({k: v['genotype'] for k, v in data.items()})
        elif fmt == '23andme':
            data = parse_23andme(filepath)
            print_summary(fmt, data)
            all_data.update({k: v['genotype'] for k, v in data.items()})
        elif fmt == 'ancestrydna':
            data = parse_ancestrydna(filepath)
            print_summary(fmt, data)
            all_data.update({k: v['genotype'] for k, v in data.items()})
        elif fmt == 'vcf':
            data, stats = parse_vcf(filepath)
            print_summary(fmt, data, stats)
            all_data.update({k: v['genotype'] for k, v in data.items()})
        else:
            print(f"  WARNING: Unknown format for {filepath}")

    print(f"\nTotal unified variants: {len(all_data):,}")
