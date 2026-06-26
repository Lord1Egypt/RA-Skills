#!/usr/bin/env python3
"""BM25 search over openclaw-sage index.txt

Usage:
  bm25_search.py search <index_file> <query...>
  bm25_search.py search <index_file> <query> <max_results>
  bm25_search.py build-meta <index_file>   # writes index_meta.json alongside index

Output (search): score | path | excerpt   (sorted by score descending)
"""

import sys
import os
import json
import math
import re
from collections import defaultdict

K1 = 1.5
B = 0.75
MIN_DOCS_FOR_IDF = 5
MAX_RESULTS = 20
MAX_EXCERPT_LEN = 120


def tokenize(text):
    return re.findall(r'[a-z0-9]+', text.lower())


def load_index(index_file):
    docs = defaultdict(list)
    with open(index_file, encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.rstrip('\n')
            if '|' not in line:
                continue
            path, _, text = line.partition('|')
            docs[path].append(text)
    return docs


def build_meta(docs):
    doc_lengths = {}
    df = defaultdict(int)
    for path, lines in docs.items():
        tokens = tokenize(' '.join(lines))
        doc_lengths[path] = len(tokens)
        for t in set(tokens):
            df[t] += 1
    avg_dl = sum(doc_lengths.values()) / max(len(doc_lengths), 1)
    return {
        'num_docs': len(docs),
        'avg_dl': avg_dl,
        'doc_lengths': doc_lengths,
        'df': dict(df),
    }


def bm25_score(query_terms, doc_tokens, doc_len, avg_dl, df, num_docs):
    score = 0.0
    tf_in_doc = defaultdict(int)
    for t in doc_tokens:
        tf_in_doc[t] += 1

    for t in query_terms:
        tf = tf_in_doc.get(t, 0)
        if tf == 0:
            continue
        n_t = df.get(t, 0)
        if num_docs >= MIN_DOCS_FOR_IDF and n_t > 0:
            idf = math.log((num_docs - n_t + 0.5) / (n_t + 0.5) + 1)
        else:
            idf = 1.0  # simple TF fallback for small corpora
        numerator = tf * (K1 + 1)
        denominator = tf + K1 * (1 - B + B * doc_len / avg_dl)
        score += idf * numerator / denominator

    return score


def find_best_excerpt(lines, query_terms):
    best_line = ''
    best_count = 0
    for line in lines:
        count = sum(1 for t in query_terms if t in line.lower())
        if count > best_count:
            best_count = count
            best_line = line
    result = best_line.strip() or (lines[0].strip() if lines else '')
    if len(result) > MAX_EXCERPT_LEN:
        result = result[:MAX_EXCERPT_LEN - 3] + '...'
    return result


def meta_file_path(index_file):
    return os.path.join(os.path.dirname(os.path.abspath(index_file)), 'index_meta.json')


def main():
    if len(sys.argv) < 3:
        print("Usage: bm25_search.py search <index_file> <query...>", file=sys.stderr)
        print("       bm25_search.py build-meta <index_file>", file=sys.stderr)
        sys.exit(1)

    mode = sys.argv[1]
    index_file = sys.argv[2]

    if not os.path.exists(index_file):
        print(f"Error: index file not found: {index_file}", file=sys.stderr)
        sys.exit(1)

    docs = load_index(index_file)

    if mode == 'build-meta':
        meta = build_meta(docs)
        mf = meta_file_path(index_file)
        with open(mf, 'w') as f:
            json.dump(meta, f)
        print(f"Meta written: {mf} ({meta['num_docs']} docs)", file=sys.stderr)
        return

    if mode != 'search':
        print(f"Unknown mode: {mode}", file=sys.stderr)
        sys.exit(1)

    max_results = MAX_RESULTS
    query_args = sys.argv[3:]
    if len(query_args) == 2 and query_args[-1].isdigit():
        max_results = int(query_args[-1])
        query_args = query_args[:-1]

    query = ' '.join(query_args)
    if not query:
        print("No query provided", file=sys.stderr)
        sys.exit(1)

    query_terms = tokenize(query)

    mf = meta_file_path(index_file)
    if os.path.exists(mf):
        with open(mf) as f:
            meta = json.load(f)
    else:
        meta = build_meta(docs)

    num_docs = meta['num_docs']
    avg_dl = meta['avg_dl']
    doc_lengths = meta['doc_lengths']
    df = meta['df']

    results = []
    for path, lines in docs.items():
        doc_tokens = tokenize(' '.join(lines))
        doc_len = doc_lengths.get(path, len(doc_tokens))
        score = bm25_score(query_terms, doc_tokens, doc_len, avg_dl, df, num_docs)
        if score > 0:
            excerpt = find_best_excerpt(lines, query_terms)
            results.append((score, path, excerpt))

    results.sort(reverse=True)

    for score, path, excerpt in results[:max_results]:
        print(f"{score:.3f} | {path} | {excerpt}")


if __name__ == '__main__':
    main()
