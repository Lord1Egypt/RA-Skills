#!/usr/bin/env python3
"""
Entity Deduplication Engine — P2: Embedding-based duplicate detection and merging.

Uses embedding similarity to identify duplicate entities, merges them by:
- Keeping the entity with the earliest timestamp as the canonical
- Accumulating frequency across duplicates
- Marking merged entities with `merged_into` field

Usage:
    python3 entity_dedup.py run [--threshold 0.85] [--dry-run]
    python3 entity_dedup.py stats
"""

import json
import sys
import math
import hashlib
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field

SCRIPT_DIR = Path(__file__).parent
WORKSPACE_ROOT = SCRIPT_DIR.parent
ONTOLOGY_DIR = WORKSPACE_ROOT / "ontology"
GRAPH_FILE = ONTOLOGY_DIR / "graph.jsonl"
EMBED_CACHE_FILE = ONTOLOGY_DIR / "embed_cache.jsonl"

sys.path.insert(0, str(SCRIPT_DIR))
from utils.llm_client import LLMClient
from memory_ontology import load_all_entities, _write_to_graph


# Similarity threshold for deduplication
DEFAULT_SIMILARITY_THRESHOLD = 0.85


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    """Compute cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def _entity_text(entity: Dict) -> str:
    """Extract canonical text from an entity for embedding.

    Concatenates title + key content fields depending on entity type.
    """
    props = entity.get('properties', {})
    parts = []

    title = props.get('title', '')
    if title:
        parts.append(title)

    # Entity-type-specific content fields
    if entity['type'] == 'Decision':
        rationale = props.get('rationale', '')
        if rationale:
            parts.append(rationale)
    elif entity['type'] == 'Finding':
        content = props.get('content', '')
        if content:
            parts.append(content)
    elif entity['type'] == 'LessonLearned':
        lesson = props.get('lesson', '')
        if lesson:
            parts.append(lesson)
    elif entity['type'] == 'Commitment':
        desc = props.get('description', '')
        if desc:
            parts.append(desc)

    tags = props.get('tags', [])
    if tags:
        parts.append(' '.join(tags))

    return ' '.join(parts)


@dataclass
class MergeCandidate:
    """Represents a pair of entities flagged for merging."""
    entity1_id: str
    entity2_id: str
    similarity: float
    canonical_id: str  # which ID to keep


@dataclass
class DedupStats:
    """Statistics from a deduplication run."""
    pairs_found: int = 0
    entities_merged: int = 0
    canonical_entities: int = 0
    duplicates_marked: int = 0
    by_type: Dict[str, int] = field(default_factory=dict)


class EmbedCache:
    """Simple file-backed embedding cache with TTL."""

    TTL_HOURS = 24

    def __init__(self, cache_file: Path = EMBED_CACHE_FILE):
        self.cache_file = cache_file
        self._cache: Dict[str, Tuple[str, str, List[float]]] = {}  # text_hash -> (text, created_iso, embedding)
        self._load()

    def _load(self):
        if not self.cache_file.exists():
            return
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                        self._cache[entry['text_hash']] = (
                            entry['text'],
                            entry['created'],
                            entry['embedding']
                        )
                    except (json.JSONDecodeError, KeyError):
                        continue
        except Exception:
            pass

    def _save(self):
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            for text_hash, (text, created, embedding) in self._cache.items():
                f.write(json.dumps({
                    'text_hash': text_hash,
                    'text': text,
                    'created': created,
                    'embedding': embedding
                }, ensure_ascii=False) + '\n')

    def get(self, text: str) -> Optional[List[float]]:
        """Get cached embedding if still valid."""
        if not text:
            return None  # Empty text can collide on hash — skip cache
        # Note: MD5 is non-cryptographic here (text similarity cache, not security-critical).
        # Collision risk is negligible in practice. SHA-256 would be marginally safer.
        text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
        if text_hash not in self._cache:
            return None
        text_stored, created_str, embedding = self._cache[text_hash]
        if text_stored != text:
            return None
        try:
            created = datetime.fromisoformat(created_str.replace('Z', '+00:00'))
            age_hours = (datetime.now().astimezone() - created).total_seconds() / 3600
            if age_hours > self.TTL_HOURS:
                del self._cache[text_hash]
                return None
        except (ValueError, TypeError):
            return None
        return embedding

    def set(self, text: str, embedding: List[float]):
        """Cache an embedding."""
        text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
        self._cache[text_hash] = (
            text,
            datetime.now().astimezone().isoformat(),
            embedding
        )
        self._save()


class EntityDeduplicator:
    """Embedding-based entity deduplication engine."""

    # Entity types eligible for deduplication
    DEDUP_TYPES = {'Decision', 'Finding', 'LessonLearned', 'Commitment'}

    def __init__(self, client: LLMClient,
                 threshold: float = DEFAULT_SIMILARITY_THRESHOLD,
                 dry_run: bool = False):
        self.client = client
        self.threshold = threshold
        self.dry_run = dry_run
        self.embed_cache = EmbedCache()
        self.stats = DedupStats()

    def _get_embedding(self, text: str) -> Optional[List[float]]:
        """Get embedding with caching."""
        emb = self.embed_cache.get(text)
        if emb is not None:
            return emb
        emb = self.client.embed(text)
        if emb is not None:
            self.embed_cache.set(text, emb)
        return emb

    def _get_entity_text(self, entity: Dict) -> str:
        """Get text for an entity."""
        return _entity_text(entity)

    def _get_primary_timestamp(self, entity: Dict) -> str:
        """Get the earliest meaningful timestamp for an entity."""
        props = entity.get('properties', {})
        for field_name in ['made_at', 'discovered_at', 'learned_at', 'created_at', 'captured_at']:
            if field_name in props:
                return props[field_name]
        return entity.get('created', '1970-01-01T00:00:00+00:00')

    def find_candidates(self, entities: Dict[str, Dict]) -> List[MergeCandidate]:
        """Find all entity pairs above similarity threshold.

        Groups entities by type first, then compares within each group.
        Uses blocking on text length to reduce comparisons.
        """
        by_type: Dict[str, List[Tuple[str, Dict]]] = {}
        for eid, entity in entities.items():
            etype = entity['type']
            if etype not in self.DEDUP_TYPES:
                continue
            if 'merged_into' in entity.get('properties', {}):
                continue  # skip already-merged entities
            by_type.setdefault(etype, []).append((eid, entity))

        candidates: List[MergeCandidate] = []

        for etype, entity_list in by_type.items():
            if len(entity_list) < 2:
                continue

            # Pre-compute embeddings for all entities in this type group
            embeddings: Dict[str, List[float]] = {}

            for eid, entity in entity_list:
                text = self._get_entity_text(entity)
                emb = self._get_embedding(text)
                if emb is not None:
                    embeddings[eid] = emb

            # Compare all pairs (O(n²) but n is small per type)
            for i, (eid1, ent1) in enumerate(entity_list):
                if eid1 not in embeddings:
                    continue
                emb1 = embeddings[eid1]

                for eid2, ent2 in entity_list[i + 1:]:
                    if eid2 not in embeddings:
                        continue
                    emb2 = embeddings[eid2]

                    sim = _cosine_similarity(emb1, emb2)
                    if sim >= self.threshold:
                        # Keep the one with earliest timestamp as canonical
                        ts1 = self._get_primary_timestamp(ent1)
                        ts2 = self._get_primary_timestamp(ent2)
                        canonical = eid1 if ts1 <= ts2 else eid2

                        candidates.append(MergeCandidate(
                            entity1_id=eid1,
                            entity2_id=eid2,
                            similarity=sim,
                            canonical_id=canonical
                        ))
                        self.stats.pairs_found += 1
                        self.stats.by_type[etype] = self.stats.by_type.get(etype, 0) + 1

        return candidates

    def merge_pair(self, candidate: MergeCandidate, entities: Dict[str, Dict]) -> bool:
        """Merge two entities, keeping canonical.

        Returns True if merge was performed.
        """
        canonical_id = candidate.canonical_id
        dup_id = candidate.entity2_id if candidate.canonical_id == candidate.entity1_id else candidate.entity1_id

        canonical = entities.get(canonical_id)
        duplicate = entities.get(dup_id)

        if not canonical or not duplicate:
            return False

        now = datetime.now().astimezone().isoformat()

        # Get current frequency
        dup_props = duplicate.get('properties', {})
        freq = dup_props.get('frequency', 1)

        # Update canonical: accumulate frequency, merge tags
        can_props = canonical.get('properties', {})
        can_tags = set(can_props.get('tags', []))
        dup_tags = set(dup_props.get('tags', []))
        merged_tags = list(can_tags | dup_tags)

        # Merge provenance
        can_prov = can_props.get('provenance', [])
        dup_prov = dup_props.get('provenance', [])
        merged_prov = can_prov + [p for p in dup_prov if p not in can_prov]

        # Update canonical entity
        can_updates = {
            'frequency': can_props.get('frequency', 1) + freq,
            'tags': merged_tags,
            'provenance': merged_prov,
            'last_accessed': now
        }

        # If the canonical's title is generic and duplicate's is more specific, keep more specific
        if len(can_props.get('title', '')) < len(dup_props.get('title', '')):
            can_updates['title'] = dup_props['title']

        # Write canonical update (if not dry-run)
        if not self.dry_run:
            update_op = {
                'op': 'update',
                'entity': {
                    'id': canonical_id,
                    'properties': can_updates,
                    'updated': now
                },
                'timestamp': now
            }
            _write_to_graph(json.dumps(update_op, ensure_ascii=False) + '\n')

            # Mark duplicate as merged
            merge_op = {
                'op': 'update',
                'entity': {
                    'id': dup_id,
                    'properties': {
                        'merged_into': canonical_id,
                        'merge_similarity': candidate.similarity,
                        'merged_at': now
                    },
                    'updated': now
                },
                'timestamp': now
            }
            _write_to_graph(json.dumps(merge_op, ensure_ascii=False) + '\n')

        return not self.dry_run

    def run(self, entities: Dict[str, Dict]) -> DedupStats:
        """Run full deduplication pass."""
        candidates = self.find_candidates(entities)

        # Build reverse lookup: canonical -> duplicates
        canonical_map: Dict[str, List[MergeCandidate]] = {}
        for c in candidates:
            canonical_map.setdefault(c.canonical_id, []).append(c)

        # Track resolved canonical for each merged entity to flatten chains.
        # Key = entity that was merged (now a dup), Value = its ultimate canonical
        merged_to: Dict[str, str] = {}

        # Process each canonical entity
        for canonical_id, group in canonical_map.items():
            self.stats.canonical_entities += 1
            self.stats.entities_merged += len(group)

            for candidate in group:
                # Resolve canonical through the chain map (flatten e3->e2->e1 to e3->e1)
                resolved_canonical = merged_to.get(canonical_id, canonical_id)
                dup_id = candidate.entity2_id if candidate.canonical_id == candidate.entity1_id else candidate.entity1_id

                # Update the resolved canonical on the candidate for merge_pair to use
                resolved_candidate = MergeCandidate(
                    entity1_id=candidate.entity1_id,
                    entity2_id=candidate.entity2_id,
                    similarity=candidate.similarity,
                    canonical_id=resolved_canonical
                )

                # Track: this dup now maps to resolved_canonical
                merged_to[dup_id] = resolved_canonical

                if self.merge_pair(resolved_candidate, entities):
                    self.stats.duplicates_marked += 1

        return self.stats

    def dry_run_report(self, entities: Dict[str, Dict]) -> Tuple[List[MergeCandidate], DedupStats]:
        """Run without making changes, return candidates for review."""
        candidates = self.find_candidates(entities)
        stats = DedupStats(
            pairs_found=len(candidates),
            by_type=self.stats.by_type.copy()
        )
        return candidates, stats


def print_candidates(candidates: List[MergeCandidate], entities: Dict[str, Dict]):
    """Print dry-run merge candidates."""
    print("\n🔍 Merge Candidates (dry-run — no changes made):\n")
    for c in candidates:
        e1 = entities.get(c.entity1_id, {})
        e2 = entities.get(c.entity2_id, {})
        t1 = e1.get('properties', {}).get('title', c.entity1_id)
        t2 = e2.get('properties', {}).get('title', c.entity2_id)
        print(f"  [{c.similarity:.2f}] {e1.get('type', '?')}: {t1}")
        print(f"       ↕ MERGE → {c.canonical_id}")
        print(f"       {e2.get('type', '?')}: {t2}")
        print()


def cmd_run(args):
    """Run deduplication."""
    entities = load_all_entities()

    client = LLMClient(
        model=args.model,
        api_key=args.api_key,
        base_url=args.base_url
    )

    dedup = EntityDeduplicator(client, threshold=args.threshold, dry_run=args.dry_run)

    if args.dry_run:
        candidates, stats = dedup.dry_run_report(entities)
        print_candidates(candidates, entities)
        print(f"\n📊 Summary (dry-run):")
        print(f"  Pairs found: {stats.pairs_found}")
        print(f"  Duplicates would be marked: {stats.pairs_found}")
        for etype, count in sorted(stats.by_type.items()):
            print(f"    {etype}: {count}")
    else:
        stats = dedup.run(entities)
        print(f"\n✅ Deduplication complete:")
        print(f"  Pairs merged: {stats.pairs_found}")
        print(f"  Canonical entities updated: {stats.canonical_entities}")
        print(f"  Duplicates marked: {stats.duplicates_marked}")
        for etype, count in sorted(stats.by_type.items()):
            print(f"    {etype}: {count}")


def cmd_stats(_args):
    """Show deduplication statistics."""
    entities = load_all_entities()

    # Count entities already merged
    merged_count = 0
    by_type: Dict[str, int] = {}

    for entity in entities.values():
        if 'merged_into' in entity.get('properties', {}):
            merged_count += 1
        etype = entity['type']
        by_type[etype] = by_type.get(etype, 0) + 1

    print(f"\n📊 Deduplication Status:\n")
    print(f"  Total entities: {len(entities)}")
    print(f"  Already merged: {merged_count}")
    print(f"  Active: {len(entities) - merged_count}")
    print(f"\n  By type:")
    for etype, count in sorted(by_type.items()):
        print(f"    {etype}: {count}")


def main():
    parser = argparse.ArgumentParser(description='Entity Deduplication Engine')
    subparsers = parser.add_subparsers(dest='command', help='command')

    run_parser = subparsers.add_parser('run', help='Run deduplication')
    run_parser.add_argument('--threshold', '-t', type=float, default=DEFAULT_SIMILARITY_THRESHOLD,
                           help=f'Similarity threshold (default: {DEFAULT_SIMILARITY_THRESHOLD})')
    run_parser.add_argument('--dry-run', '-n', action='store_true',
                           help='Show what would be merged without making changes')
    run_parser.add_argument('--model', '-m', default=None)
    run_parser.add_argument('--api-key', '-k', default=None)
    run_parser.add_argument('--base-url', '-b', default=None)

    stats_parser = subparsers.add_parser('stats', help='Show deduplication stats')

    args = parser.parse_args()

    if args.command == 'run':
        cmd_run(args)
    elif args.command == 'stats':
        cmd_stats(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
