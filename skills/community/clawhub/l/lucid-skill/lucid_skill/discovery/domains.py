"""
Business domain clustering engine.
Agglomerative hierarchical clustering with average linkage.
Automatic k selection via silhouette score.
"""

from __future__ import annotations

import hashlib
import math
import re
import time
from typing import TYPE_CHECKING

import numpy as np

from lucid_skill.types import BusinessDomain

if TYPE_CHECKING:
    from lucid_skill.catalog.store import CatalogStore
    from lucid_skill.semantic.embedder import Embedder


def tokenize(name: str) -> list[str]:
    """Tokenize a name by splitting on camelCase, underscores, hyphens, and spaces."""
    result = re.sub(r"([a-z])([A-Z])", r"\1_\2", name)
    result = re.sub(r"[-\s]+", "_", result)
    return [t for t in result.lower().split("_") if len(t) > 1]


def build_tfidf_vector(
    tokens: list[str],
    vocabulary: dict[str, int],
    idf: dict[str, float],
) -> np.ndarray:
    """Build a TF-IDF feature vector from tokens, L2 normalized."""
    vec = np.zeros(len(vocabulary), dtype=np.float32)
    tf: dict[str, int] = {}
    for t in tokens:
        tf[t] = tf.get(t, 0) + 1
    for term, count in tf.items():
        idx = vocabulary.get(term)
        if idx is not None:
            vec[idx] = count * idf.get(term, 0.0)
    # L2 normalize
    norm = float(np.sqrt(np.dot(vec, vec)))
    if norm > 0:
        vec /= norm
    return vec


def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity between two vectors."""
    if len(a) != len(b):
        return 0.0
    dot = float(np.dot(a, b))
    norm_a = float(np.sqrt(np.dot(a, a)))
    norm_b = float(np.sqrt(np.dot(b, b)))
    denom = norm_a * norm_b
    return 0.0 if denom == 0 else dot / denom


def compute_distance_matrix(vectors: list[np.ndarray]) -> list[list[float]]:
    """Compute pairwise distance matrix: dist[i][j] = 1 - cosine_similarity."""
    n = len(vectors)
    dist = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d = 1.0 - cosine_sim(vectors[i], vectors[j])
            dist[i][j] = d
            dist[j][i] = d
    return dist


def agglomerative_clustering(
    dist: list[list[float]], n: int
) -> list[dict]:
    """
    Run agglomerative clustering with average linkage.
    Returns the full merge history so we can cut at any k.
    Each entry is {'a': int, 'b': int, 'distance': float}.
    """
    # Each item starts as its own cluster
    cluster_members: dict[int, list[int]] = {i: [i] for i in range(n)}

    # Active cluster IDs
    active: set[int] = set(range(n))

    # Inter-cluster distance cache (average linkage)
    inter_dist: dict[str, float] = {}

    def dist_key(a: int, b: int) -> str:
        return f"{min(a, b)}|{max(a, b)}"

    for i in active:
        for j in active:
            if i < j:
                inter_dist[dist_key(i, j)] = dist[i][j]

    merge_history: list[dict] = []
    next_cluster_id = n

    while len(active) > 1:
        # Find closest pair
        min_dist = float("inf")
        best_a = -1
        best_b = -1
        for i in active:
            for j in active:
                if i >= j:
                    continue
                d = inter_dist.get(dist_key(i, j), float("inf"))
                if d < min_dist:
                    min_dist = d
                    best_a = i
                    best_b = j

        if best_a == -1:
            break

        merge_history.append({"a": best_a, "b": best_b, "distance": min_dist})

        # Merge into a new cluster
        new_id = next_cluster_id
        next_cluster_id += 1
        members_a = cluster_members[best_a]
        members_b = cluster_members[best_b]
        new_members = members_a + members_b
        cluster_members[new_id] = new_members
        del cluster_members[best_a]
        del cluster_members[best_b]
        active.discard(best_a)
        active.discard(best_b)

        # Compute average linkage distance to all remaining clusters
        for other in active:
            other_members = cluster_members[other]
            sum_dist = 0.0
            for mi in new_members:
                for mj in other_members:
                    sum_dist += dist[mi][mj]
            avg_dist = sum_dist / (len(new_members) * len(other_members))
            inter_dist[dist_key(new_id, other)] = avg_dist

        active.add(new_id)

    return merge_history


def cut_at_k(merge_history: list[dict], n: int, k: int) -> list[int]:
    """Cut the dendrogram at k clusters. Returns cluster labels for each item."""
    # Start: each item is its own cluster
    parent: dict[int, int] = {i: i for i in range(n)}

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    # Apply merges until we have k clusters
    num_clusters = n
    next_id = n
    for merge in merge_history:
        if num_clusters <= k:
            break
        root_a = find(merge["a"])
        root_b = find(merge["b"])
        if root_a != root_b:
            parent[root_a] = next_id
            parent[root_b] = next_id
            parent[next_id] = next_id
            next_id += 1
            num_clusters -= 1

    # Assign labels
    labels = [0] * n
    label_map: dict[int, int] = {}
    label_counter = 0
    for i in range(n):
        root = find(i)
        if root not in label_map:
            label_map[root] = label_counter
            label_counter += 1
        labels[i] = label_map[root]
    return labels


def silhouette_score(dist: list[list[float]], labels: list[int], k: int) -> float:
    """Compute silhouette score for a given labeling."""
    n = len(labels)
    if k <= 1 or k >= n:
        return -1.0

    total_sil = 0.0
    for i in range(n):
        my_cluster = labels[i]

        # a(i) = average distance to same-cluster members
        sum_a = 0.0
        count_a = 0
        for j in range(n):
            if j != i and labels[j] == my_cluster:
                sum_a += dist[i][j]
                count_a += 1
        a = sum_a / count_a if count_a > 0 else 0.0

        # b(i) = min average distance to other clusters
        min_b = float("inf")
        for c in range(k):
            if c == my_cluster:
                continue
            sum_b = 0.0
            count_b = 0
            for j in range(n):
                if labels[j] == c:
                    sum_b += dist[i][j]
                    count_b += 1
            if count_b > 0:
                min_b = min(min_b, sum_b / count_b)
        if min_b == float("inf"):
            min_b = 0.0

        denom = max(a, min_b)
        sil = 0.0 if denom == 0 else (min_b - a) / denom
        total_sil += sil

    return total_sil / n


def generate_domain_name(
    domain_indices: list[int],
    all_token_sets: list[list[str]],
    total_domains: int,
    all_domain_indices: list[list[int]],
) -> str:
    """Generate domain name from table+column tokens using TF-IDF top-3 words."""
    # Collect tokens for this domain
    domain_tokens: list[str] = []
    for idx in domain_indices:
        domain_tokens.extend(all_token_sets[idx])

    # TF: count in this domain
    tf: dict[str, int] = {}
    for t in domain_tokens:
        tf[t] = tf.get(t, 0) + 1

    # IDF: log(totalDomains / domainsContainingTerm)
    idf: dict[str, float] = {}
    for term in tf:
        domains_with_term = 0
        for indices in all_domain_indices:
            domain_token_set: set[str] = set()
            for idx in indices:
                for t in all_token_sets[idx]:
                    domain_token_set.add(t)
            if term in domain_token_set:
                domains_with_term += 1
        idf[term] = math.log((total_domains + 1) / (domains_with_term + 1))

    # Score = TF * IDF
    scored = [(term, count * idf.get(term, 0.0)) for term, count in tf.items()]
    scored.sort(key=lambda x: x[1], reverse=True)

    top_terms = [s[0] for s in scored[:3]]
    return "_".join(top_terms) if top_terms else "default"


def make_single_domain(
    all_tables: list[dict],
    all_token_sets: list[list[str]],
) -> BusinessDomain:
    """Create a single 'default' domain containing all tables."""
    table_names = [t["table_name"] for t in all_tables]

    # Top keywords across all tables
    all_tokens: list[str] = []
    for ts in all_token_sets:
        all_tokens.extend(ts)
    freq: dict[str, int] = {}
    for t in all_tokens:
        freq[t] = freq.get(t, 0) + 1
    keywords = [
        t
        for t, _ in sorted(freq.items(), key=lambda x: x[1], reverse=True)[:5]
    ]

    domain_id = hashlib.sha256(
        "|".join(sorted(table_names)).encode()
    ).hexdigest()[:16]

    return BusinessDomain(
        domain_id=domain_id,
        domain_name="_".join(keywords[:3]) if keywords else "default",
        table_names=table_names,
        keywords=keywords,
        created_at=int(time.time() * 1000),
        version=1,
    )


def discover_business_domains(
    catalog: CatalogStore,
    embedder: Embedder | None = None,
) -> list[BusinessDomain]:
    """
    Discover business domains by clustering tables.
    Uses embeddings if available, otherwise falls back to TF-IDF on table/column names.
    """
    all_tables = catalog.get_tables()
    if len(all_tables) == 0:
        return []

    n = len(all_tables)

    # Collect tokens for each table (for domain naming and TF-IDF fallback)
    all_token_sets: list[list[str]] = []
    for t in all_tables:
        cols = catalog.get_columns(t["source_id"], t["table_name"])
        tokens = tokenize(t["table_name"]) + [
            tok for c in cols for tok in tokenize(c["column_name"])
        ]
        all_token_sets.append(tokens)

    # Build feature vectors
    vectors: list[np.ndarray]
    use_embeddings = False

    # Try embeddings first
    if embedder and embedder.is_ready():
        emb_vectors: list[np.ndarray | None] = []
        for t in all_tables:
            emb = catalog.get_embedding(t["source_id"], t["table_name"])
            if emb:
                emb_vectors.append(
                    np.frombuffer(emb["vector"], dtype=np.float32).copy()
                )
            else:
                emb_vectors.append(None)
        if all(v is not None for v in emb_vectors):
            vectors = emb_vectors  # type: ignore[assignment]
            use_embeddings = True

    if not use_embeddings:
        # Fallback: TF-IDF vectors from table+column names
        all_tokens_set: set[str] = set()
        for ts in all_token_sets:
            for t in ts:
                all_tokens_set.add(t)
        vocabulary: dict[str, int] = {}
        idx = 0
        for t in all_tokens_set:
            vocabulary[t] = idx
            idx += 1

        # Compute document frequency
        df: dict[str, int] = {}
        for ts in all_token_sets:
            unique = set(ts)
            for t in unique:
                df[t] = df.get(t, 0) + 1

        # IDF
        idf: dict[str, float] = {}
        for term, count in df.items():
            idf[term] = math.log((n + 1) / (count + 1))

        vectors = [build_tfidf_vector(ts, vocabulary, idf) for ts in all_token_sets]

    # Single domain fallback for < 5 tables
    if n < 5:
        return [make_single_domain(all_tables, all_token_sets)]

    # Compute distance matrix
    dist = compute_distance_matrix(vectors)

    # Agglomerative clustering
    merge_history = agglomerative_clustering(dist, n)

    # Find optimal k via silhouette score
    max_k = min(n // 2, 20)
    best_k = 1
    best_sil = -1.0

    for k in range(2, max_k + 1):
        labels = cut_at_k(merge_history, n, k)
        sil = silhouette_score(dist, labels, k)
        if sil > best_sil:
            best_sil = sil
            best_k = k

    # If silhouette is too low, fallback to single domain
    if best_sil < 0.25:
        return [make_single_domain(all_tables, all_token_sets)]

    # Cut at best k
    labels = cut_at_k(merge_history, n, best_k)

    # Group tables by cluster
    clusters: dict[int, list[int]] = {}
    for i in range(n):
        if labels[i] not in clusters:
            clusters[labels[i]] = []
        clusters[labels[i]].append(i)

    all_domain_indices = list(clusters.values())

    # Build domains
    domains: list[BusinessDomain] = []
    for _label, indices in clusters.items():
        table_names = [all_tables[i]["table_name"] for i in indices]
        domain_name = generate_domain_name(
            indices, all_token_sets, best_k, all_domain_indices
        )

        # Keywords: top tokens from domain
        domain_tokens: list[str] = []
        for i in indices:
            domain_tokens.extend(all_token_sets[i])
        freq: dict[str, int] = {}
        for t in domain_tokens:
            freq[t] = freq.get(t, 0) + 1
        keywords = [
            t
            for t, _ in sorted(freq.items(), key=lambda x: x[1], reverse=True)[:5]
        ]

        domain_id = hashlib.sha256(
            "|".join(sorted(table_names)).encode()
        ).hexdigest()[:16]

        domains.append(
            BusinessDomain(
                domain_id=domain_id,
                domain_name=domain_name,
                table_names=table_names,
                keywords=keywords,
                created_at=int(time.time() * 1000),
                version=1,
            )
        )

    return domains
