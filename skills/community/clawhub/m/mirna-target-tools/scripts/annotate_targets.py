#!/usr/bin/env python3
"""
Annotate miRNA target genes and run functional enrichment analysis.

Two capabilities:
  1. Gene annotation  - convert gene symbols to Entrez/Ensembl IDs and fetch
     gene descriptions via MyGene.info (online API, no local DB required).
  2. Functional enrichment - GO (BP/CC/MF) and KEGG pathway enrichment via the
     g:Profiler REST API (standard-library only, no third-party dependency),
     supporting human/mouse/rat/sheep/goat/cow. Every tested term is reported
     with both its raw p-value and a Benjamini-Hochberg FDR q-value (BH is
     applied within each source over the full tested family).

Usage examples:
  # From merged targets TSV (column "TargetGene")
  python annotate_targets.py --input merged_high_confidence.txt --gene-col TargetGene \
      --species goat --output-dir results/annotation

  # From a plain gene list (one symbol per line)
  python annotate_targets.py --input gene_list.txt --plain-list \
      --species human --output-dir results/annotation

Dependencies:
  pip install pandas mygene      # mygene is optional (only for gene annotation)
"""

import argparse
import json
import math
import os
import sys
import urllib.request

import numpy as np
import pandas as pd


# Common name / alias -> (taxid for MyGene.info, organism for g:Profiler)
SPECIES_MAP = {
    'human':       (9606, 'hsapiens'),
    'hsapiens':    (9606, 'hsapiens'),
    'mouse':       (10090, 'mmusculus'),
    'mmusculus':   (10090, 'mmusculus'),
    'rat':         (10116, 'rnorvegicus'),
    'rnorvegicus': (10116, 'rnorvegicus'),
    'sheep':       (9940, 'oarambouillet'),
    'ovis':        (9940, 'oarambouillet'),
    'goat':        (9925, 'chircus'),
    'capra':       (9925, 'chircus'),
    'cow':         (9913, 'btaurus'),
    'btaurus':     (9913, 'btaurus'),
}

# g:Profiler REST endpoint (no auth required)
GPROFILER_URL = 'https://biit.cs.ut.ee/gprofiler/api/gost/profile/'


def resolve_species(species):
    """Map a species name/alias to (taxid, g:Profiler organism)."""
    key = str(species).strip().lower()
    if key in SPECIES_MAP:
        return SPECIES_MAP[key]
    if key.isdigit():
        # numeric taxid works for MyGene.info but not g:Profiler
        return (int(key), None)
    print(f"Error: unknown species '{species}'.")
    print(f"Supported: {', '.join(sorted(set(SPECIES_MAP)))}")
    sys.exit(1)


def load_gene_list(input_file, gene_col, plain_list):
    """Return a sorted, deduplicated list of gene symbols."""
    if plain_list:
        with open(input_file) as f:
            genes = [ln.strip() for ln in f if ln.strip() and not ln.startswith('#')]
    else:
        df = pd.read_csv(input_file, sep='\t')
        if gene_col is None:
            candidates = [c for c in df.columns if c.lower() in
                          ('targetgene', 'target_gene', 'gene', 'genes',
                           'symbol', 'genesymbol', 'gene_symbol', 'target')]
            if not candidates:
                print(f"Error: cannot auto-detect gene column. Found columns: {list(df.columns)}")
                print("Use --gene-col to specify the column name.")
                sys.exit(1)
            gene_col = candidates[0]
            print(f"Auto-detected gene column: '{gene_col}'")
        if gene_col not in df.columns:
            print(f"Error: column '{gene_col}' not found. Available: {list(df.columns)}")
            sys.exit(1)
        genes = df[gene_col].dropna().astype(str).str.strip()
    genes = sorted({g for g in genes if g})
    return genes


def annotate_genes(genes, taxid):
    """Annotate gene symbols using MyGene.info. Returns DataFrame or None."""
    try:
        import mygene
    except ImportError:
        print("Warning: 'mygene' not installed. Skipping gene annotation.")
        print("         Install with: pip install mygene")
        return None

    mg = mygene.MyGeneInfo()
    try:
        res = mg.querymany(genes, scopes='symbol',
                           fields='entrezgene,ensembl.gene,symbol,name,summary,type_of_gene,taxid',
                           species=taxid, verbose=False)
    except Exception as e:
        print(f"Warning: MyGene.info query failed: {e}")
        return None

    rows = []
    for r in res:
        if r.get('notfound'):
            rows.append({'query': r.get('query'), 'symbol': r.get('query'),
                         'entrez': None, 'ensembl': None, 'description': None,
                         'gene_type': None, 'taxid': None, 'status': 'not_found'})
            continue
        ens = r.get('ensembl', {})
        ens_id = None
        if isinstance(ens, dict):
            ens_id = ens.get('gene')
        elif isinstance(ens, list) and ens:
            ens_id = ens[0].get('gene')
        rows.append({
            'query': r.get('query'),
            'symbol': r.get('symbol'),
            'entrez': r.get('entrezgene'),
            'ensembl': ens_id,
            'description': r.get('summary') or r.get('name'),
            'gene_type': r.get('type_of_gene'),
            'taxid': r.get('taxid'),
            'status': 'ok',
        })
    return pd.DataFrame(rows)


def run_enrichment(genes, organism):
    """Run GO + KEGG enrichment via the g:Profiler REST API. Returns DataFrame or None."""
    if organism is None:
        print("Warning: numeric taxid given, but g:Profiler needs an organism name.")
        print("         Use a common name (human/mouse/rat/sheep/goat/cow) for enrichment.")
        return None

    payload = {
        'organism': organism,
        'query': genes,
        'sources': ['GO:BP', 'GO:CC', 'GO:MF', 'KEGG'],
        # ask for the FULL tested family (no pre-filtering) so the
        # Benjamini-Hochberg correction below is computed over every term
        # g:Profiler tested, not just the ones that already looked significant
        'user_threshold': 1.0,
        'no_evidences': True,
        'no_iea': False,
        'domain_scope': 'annotated',
    }

    print(f"Querying g:Profiler ({organism}) with {len(genes)} genes ...")
    try:
        req = urllib.request.Request(
            GPROFILER_URL,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json', 'User-Agent': 'mirna-target-tools/1.0'},
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"Warning: g:Profiler query failed: {e}")
        return None

    result = data.get('result', [])
    if not result:
        print("Warning: no enriched terms returned (possibly no significant hits).")
        return None

    rows = []
    for r in result:
        rows.append({
            'source': r.get('source'),
            'native': r.get('native'),
            'name': r.get('name'),
            'p_value': r.get('p_value'),
            'term_size': r.get('term_size'),
            'query_size': r.get('query_size'),
            'intersection_size': r.get('intersection_size'),
            'intersections': ','.join(r.get('intersections', [])),
            'description': r.get('description'),
        })

    df = pd.DataFrame(rows)
    if df.empty:
        return None

    # Benjamini-Hochberg FDR, computed within each source over *every* term the
    # API tested (the full family, not just the significant subset) so the
    # correction stays statistically valid. g:Profiler's own correction
    # (g:SCS) is deliberately conservative; BH is reported alongside the raw p.
    df['q_value'] = np.nan
    for src, idx in df.groupby('source').groups.items():
        p = df.loc[idx, 'p_value'].to_numpy(dtype=float)
        m = len(p)
        order = np.argsort(p)
        q = p[order] * m / np.arange(1, m + 1)
        q = np.minimum.accumulate(q[::-1])[::-1]
        out = np.empty(m)
        out[order] = q
        df.loc[idx, 'q_value'] = np.clip(out, 0.0, 1.0)

    df['neg_log10_p'] = df['p_value'].apply(lambda p: -math.log10(p) if p > 0 else float('nan'))
    df['neg_log10_q'] = df['q_value'].apply(lambda q: -math.log10(q) if q and q > 0 else float('nan'))
    df['significant'] = (df['p_value'] < 0.05) & (df['q_value'] < 0.05)
    df = df.sort_values('p_value').reset_index(drop=True)
    return df


def main():
    parser = argparse.ArgumentParser(
        description='Annotate miRNA target genes and run GO/KEGG enrichment analysis')
    parser.add_argument('--input', required=True,
                        help='Input file: merged targets TSV, or a plain gene list')
    parser.add_argument('--gene-col', default=None,
                        help='Column name holding gene symbols (for TSV input; auto-detected if omitted)')
    parser.add_argument('--plain-list', action='store_true',
                        help='Treat input as a plain list (one gene symbol per line)')
    parser.add_argument('--species', default='human',
                        help='Species: human/mouse/rat/sheep/goat/cow (default: human)')
    parser.add_argument('--output-dir', default='annotation_results',
                        help='Output directory (default: annotation_results)')
    parser.add_argument('--prefix', default=None,
                        help='Output filename prefix (default: derived from input basename)')
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: input file '{args.input}' not found!")
        sys.exit(1)

    taxid, organism = resolve_species(args.species)
    os.makedirs(args.output_dir, exist_ok=True)
    prefix = args.prefix or os.path.splitext(os.path.basename(args.input))[0]

    genes = load_gene_list(args.input, args.gene_col, args.plain_list)
    print(f"Loaded {len(genes)} unique target genes.")

    # 1) Gene annotation
    ann_df = annotate_genes(genes, taxid)
    if ann_df is not None:
        ann_path = os.path.join(args.output_dir, f"{prefix}_gene_annotation.tsv")
        ann_df.to_csv(ann_path, sep='\t', index=False)
        print(f"Gene annotation written to {ann_path}")
        if 'status' in ann_df.columns:
            n_ok = (ann_df['status'] == 'ok').sum()
            print(f"  Annotated {n_ok}/{len(genes)} genes.")

    # 2) Functional enrichment
    enrich_df = run_enrichment(genes, organism)
    if enrich_df is not None:
        full_path = os.path.join(args.output_dir, f"{prefix}_enrichment_all.tsv")
        enrich_df.to_csv(full_path, sep='\t', index=False)
        print(f"Enrichment results written to {full_path}")
        if 'source' in enrich_df.columns:
            for src, name in [('GO:BP', 'GO_BP'), ('GO:CC', 'GO_CC'),
                              ('GO:MF', 'GO_MF'), ('KEGG', 'KEGG')]:
                sub = enrich_df[(enrich_df['source'] == src) & enrich_df['significant']]
                if len(sub):
                    p = os.path.join(args.output_dir, f"{prefix}_{name}.tsv")
                    sub.to_csv(p, sep='\t', index=False)
                    print(f"  {src}: {len(sub)} significant terms -> {os.path.basename(p)}")
        n_p = int((enrich_df['p_value'] < 0.05).sum())
        n_q = int(enrich_df['significant'].sum())
        print(f"  Terms tested: {len(enrich_df)} | p < 0.05: {n_p} | BH q < 0.05: {n_q}")
        print("  (the *_all.tsv keeps every tested term with its q_value)")

    print("Done!")


if __name__ == '__main__':
    main()
