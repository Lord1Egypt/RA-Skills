#!/usr/bin/env python3
"""
ConceptMediatedGraph - Phase 4 Concept-Mediated Graph

Provides concept-based queries for the knowledge graph.
Allows querying entities by concept, transitive closure, and finding concept paths.

Usage:
    python3 concept_mediated_graph.py query --concept concept_xxx
    python3 concept_mediated_graph.py transitive --concept concept_xxx
    python3 concept_mediated_graph.py path --from dec_xxx --to dec_yyy
"""

import json
import sys
import logging
import re
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple
from collections import deque

SCRIPT_DIR = Path(__file__).parent
WORKSPACE_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from memory_ontology import load_all_entities, load_all_relations


def normalize_concept_name(name: str) -> str:
    """Normalize a concept name for comparison

    Args:
        name: Concept name to normalize

    Returns:
        Normalized lowercase name
    """
    if not name:
        return ''
    return re.sub(r'[^\w\s]', '', name.lower()).strip()


def query_entities_by_concept(concept_id: str) -> List[Dict]:
    """Query all entities directly linked to a concept

    Args:
        concept_id: Concept ID to query

    Returns:
        List of entities that are instances of the concept
    """
    entities = load_all_entities()
    relations = load_all_relations()

    entity_ids = set()
    for rel in relations:
        if rel.get('rel') == 'instance_of' and rel.get('to') == concept_id:
            entity_ids.add(rel.get('from'))

    for entity in entities.values():
        props = entity.get('properties', {})
        entity_concepts = props.get('concepts', [])
        if concept_id in entity_concepts:
            entity_ids.add(entity['id'])

    results = []
    for entity in entities.values():
        if entity['id'] in entity_ids:
            results.append(entity)

    return results


def query_entities_by_concept_name(concept_name: str) -> List[Dict]:
    """Query entities by concept name (fuzzy match)

    Args:
        concept_name: Concept name to search for

    Returns:
        List of matching entities
    """
    entities = load_all_entities()
    normalized_search = normalize_concept_name(concept_name)

    matching_concepts = []
    for entity in entities.values():
        if entity['type'] == 'Concept':
            concept_name_prop = entity.get('properties', {}).get('name', '')
            if normalize_concept_name(concept_name_prop) == normalized_search:
                matching_concepts.append(entity)

    results = []
    for concept in matching_concepts:
        related = query_entities_by_concept(concept['id'])
        results.extend(related)

    return results


def query_entities_by_concept_transitive(concept_id: str) -> List[Dict]:
    """Query entities by concept including all subconcepts (transitive closure)

    Args:
        concept_id: Root concept ID

    Returns:
        List of entities linked to the concept or any subconcept
    """
    from concept_hierarchy import get_transitive_closure

    all_concept_ids = {concept_id} | get_transitive_closure(concept_id)

    entities = load_all_entities()
    relations = load_all_relations()

    entity_ids = set()
    for rel in relations:
        if rel.get('rel') == 'instance_of' and rel.get('to') in all_concept_ids:
            entity_ids.add(rel.get('from'))

    for entity in entities.values():
        props = entity.get('properties', {})
        entity_concepts = props.get('concepts', [])
        if any(cid in all_concept_ids for cid in entity_concepts):
            entity_ids.add(entity['id'])

    results = []
    for entity in entities.values():
        if entity['id'] in entity_ids:
            results.append(entity)

    return results


def find_concept_path(entity1_id: str, entity2_id: str) -> List[str]:
    """Find concept path between two entities

    Uses BFS to find the shortest path through concepts connecting two entities.

    Args:
        entity1_id: First entity ID
        entity2_id: Second entity ID

    Returns:
        List of concept IDs forming the path, empty if no connection
    """
    entities = load_all_entities()
    relations = load_all_relations()

    entity1 = entities.get(entity1_id)
    entity2 = entities.get(entity2_id)

    if not entity1 or not entity2:
        return []

    concept_ids = {
        e['id'] for e in entities.values()
        if e['type'] == 'Concept'
    }
    for entity in entities.values():
        props = entity.get('properties', {})
        entity_concepts = props.get('concepts', [])
        concept_ids.update(entity_concepts)

    for rel in relations:
        if rel.get('rel') in ('is_a', 'part_of', 'synonym_of'):
            concept_ids.add(rel.get('from'))
            concept_ids.add(rel.get('to'))

    def get_entity_concepts(eid: str) -> Set[str]:
        concepts = set()
        for rel in relations:
            if rel.get('rel') == 'instance_of' and rel.get('from') == eid:
                cid = rel.get('to')
                if cid in concept_ids:
                    concepts.add(cid)

        entity = entities.get(eid)
        if entity:
            props = entity.get('properties', {})
            entity_concepts = props.get('concepts', [])
            for cid in entity_concepts:
                if cid in concept_ids:
                    concepts.add(cid)

        return concepts

    def get_concept_relations(cid: str) -> Set[str]:
        related = set()
        for rel in relations:
            if rel.get('rel') in ('instance_of', 'is_a', 'part_of', 'synonym_of'):
                if rel.get('from') == cid:
                    related.add(rel.get('to'))
                elif rel.get('to') == cid:
                    related.add(rel.get('from'))
        return related

    start_concepts = get_entity_concepts(entity1_id)
    end_concepts = get_entity_concepts(entity2_id)

    if not start_concepts or not end_concepts:
        return []

    intersection = start_concepts & end_concepts
    if intersection:
        return [list(intersection)[0]]

    queue = deque()
    for cid in start_concepts:
        queue.append((cid,))
    visited = start_concepts.copy()

    while queue:
        path = queue.popleft()
        current = path[-1]

        for next_concept in get_concept_relations(current):
            if next_concept in visited:
                continue

            if next_concept in end_concepts:
                return list(path) + [next_concept]

            visited.add(next_concept)
            queue.append(path + (next_concept,))

    return []


def get_concept_for_entity(entity_id: str) -> List[Dict]:
    """Get all concepts linked to an entity

    Args:
        entity_id: Entity ID

    Returns:
        List of concept entities
    """
    entities = load_all_entities()
    relations = load_all_relations()

    concept_ids = set()
    for rel in relations:
        if rel.get('rel') == 'instance_of' and rel.get('from') == entity_id:
            concept_ids.add(rel.get('to'))

    results = []
    for concept_id in concept_ids:
        if concept_id in entities and entities[concept_id]['type'] == 'Concept':
            results.append(entities[concept_id])

    return results


def link_entity_to_concept(entity_id: str, concept_id: str) -> bool:
    """Link an entity to a concept

    Args:
        entity_id: Entity ID to link
        concept_id: Concept ID to link to

    Returns:
        True if successful
    """
    from memory_ontology import create_relation, get_entity

    entity = get_entity(entity_id, refresh_strength=False)
    if not entity:
        return False

    try:
        create_relation(entity_id, 'instance_of', concept_id)

        if 'concepts' not in entity['properties']:
            entity['properties']['concepts'] = []
        if concept_id not in entity['properties']['concepts']:
            entity['properties']['concepts'].append(concept_id)

        return True
    except Exception as e:
        logging.error(f"Failed to link entity {entity_id} to concept {concept_id}: {e}")
        return False


def unlink_entity_from_concept(entity_id: str, concept_id: str) -> bool:
    """Unlink an entity from a concept

    Args:
        entity_id: Entity ID to unlink
        concept_id: Concept ID to unlink from

    Returns:
        True if successful
    """
    entities = load_all_entities()
    relations = load_all_relations()

    entity = entities.get(entity_id)
    if not entity:
        return False

    for rel in relations:
        if rel.get('rel') == 'instance_of' and rel.get('from') == entity_id and rel.get('to') == concept_id:
            return True

    if 'concepts' in entity['properties']:
        entity['properties']['concepts'] = [
            c for c in entity['properties']['concepts'] if c != concept_id
        ]

    return True


def get_concept_stats() -> Dict:
    """Get statistics about concepts in the graph

    Returns:
        Dictionary with concept statistics
    """
    entities = load_all_entities()
    relations = load_all_relations()

    concepts = [e for e in entities.values() if e['type'] == 'Concept']

    total_instances = 0
    for rel in relations:
        if rel.get('rel') == 'instance_of':
            total_instances += 1

    concept_with_instances = 0
    for concept in concepts:
        instance_count = sum(
            1 for rel in relations
            if rel.get('rel') == 'instance_of' and rel.get('to') == concept['id']
        )
        if instance_count > 0:
            concept_with_instances += 1

    return {
        'total_concepts': len(concepts),
        'total_instance_links': total_instances,
        'concepts_with_instances': concept_with_instances,
        'orphaned_concepts': len(concepts) - concept_with_instances
    }


def suggest_concepts_for_entity(entity_id: str) -> List[Dict]:
    """Suggest concepts that might be relevant to an entity

    Based on shared concepts with other entities and entity type.

    Args:
        entity_id: Entity ID

    Returns:
        List of suggested concept entities with relevance scores
    """
    entities = load_all_entities()
    relations = load_all_relations()

    entity = entities.get(entity_id)
    if not entity:
        return []

    entity_concepts = set()
    for rel in relations:
        if rel.get('rel') == 'instance_of' and rel.get('from') == entity_id:
            entity_concepts.add(rel.get('to'))

    related_entities = set()
    for rel in relations:
        if rel.get('from') in entity_concepts or rel.get('to') in entity_concepts:
            related_entities.add(rel.get('from'))
            related_entities.add(rel.get('to'))

    related_entities.discard(entity_id)

    concept_scores: Dict[str, float] = {}
    for rel in relations:
        if rel.get('from') in related_entities and rel.get('rel') == 'instance_of':
            cid = rel.get('to')
            if cid not in entity_concepts:
                concept_scores[cid] = concept_scores.get(cid, 0) + 1.0

    suggestions = []
    for cid, score in concept_scores.items():
        if cid in entities and entities[cid]['type'] == 'Concept':
            suggestions.append({
                'concept': entities[cid],
                'relevance_score': score
            })

    suggestions.sort(key=lambda x: x['relevance_score'], reverse=True)

    return suggestions[:5]


def find_related_entities(entity_id: str, max_hops: int = 2) -> List[Dict]:
    """Find entities related through concept mediation

    Args:
        entity_id: Starting entity ID
        max_hops: Maximum hops through concepts

    Returns:
        List of related entities with paths
    """
    entities = load_all_entities()
    relations = load_all_relations()

    entity = entities.get(entity_id)
    if not entity:
        return []

    entity_concepts = set()
    for rel in relations:
        if rel.get('rel') == 'instance_of' and rel.get('from') == entity_id:
            entity_concepts.add(rel.get('to'))

    related = []
    visited = {entity_id}

    def traverse(current_id: str, path: List[str], depth: int):
        if depth > max_hops:
            return

        for rel in relations:
            if rel.get('from') == current_id:
                next_id = rel.get('to')
                if next_id in visited:
                    continue

                rel_type = rel.get('rel')
                if rel_type == 'instance_of':
                    next_concepts = set()
                    for r in relations:
                        if r.get('rel') == 'instance_of' and r.get('from') == next_id:
                            next_concepts.add(r.get('to'))

                    for concept_id in next_concepts:
                        if concept_id in entity_concepts:
                            related.append({
                                'entity_id': next_id,
                                'path': path + [concept_id, next_id],
                                'via_concept': concept_id
                            })
                            visited.add(next_id)
                            traverse(next_id, path + [concept_id, next_id], depth + 1)

    traverse(entity_id, [entity_id], 0)

    return related


def main():
    import argparse

    parser = argparse.ArgumentParser(description='ConceptMediatedGraph - Concept-Based Queries')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    query_parser = subparsers.add_parser('query', help='Query entities by concept')
    query_parser.add_argument('--concept', required=True, help='Concept ID or name')

    trans_parser = subparsers.add_parser('transitive', help='Query entities by concept (transitive)')
    trans_parser.add_argument('--concept', required=True, help='Concept ID')

    path_parser = subparsers.add_parser('path', help='Find concept path between entities')
    path_parser.add_argument('--from', dest='from_id', required=True, help='First entity ID')
    path_parser.add_argument('--to', dest='to_id', required=True, help='Second entity ID')

    stats_parser = subparsers.add_parser('stats', help='Show concept statistics')

    suggest_parser = subparsers.add_parser('suggest', help='Suggest concepts for entity')
    suggest_parser.add_argument('--entity', required=True, help='Entity ID')

    args = parser.parse_args()

    if args.command == 'query':
        results = query_entities_by_concept(args.concept)
        if not results:
            results = query_entities_by_concept_name(args.concept)

        print(f"Found {len(results)} entities:")
        for e in results:
            print(f"  - {e['id']} ({e['type']}): {e.get('properties', {}).get('title', '')}")

    elif args.command == 'transitive':
        results = query_entities_by_concept_transitive(args.concept)
        print(f"Found {len(results)} entities (transitive):")
        for e in results:
            print(f"  - {e['id']} ({e['type']}): {e.get('properties', {}).get('title', '')}")

    elif args.command == 'path':
        path = find_concept_path(args.from_id, args.to_id)
        if path:
            print(f"Path: {' -> '.join(path)}")
        else:
            print("No path found")

    elif args.command == 'stats':
        stats = get_concept_stats()
        print(f"\nConcept Statistics:")
        print(f"  Total Concepts: {stats['total_concepts']}")
        print(f"  Total Instance Links: {stats['total_instance_links']}")
        print(f"  Concepts with Instances: {stats['concepts_with_instances']}")
        print(f"  Orphaned Concepts: {stats['orphaned_concepts']}")

    elif args.command == 'suggest':
        suggestions = suggest_concepts_for_entity(args.entity)
        print(f"\nSuggested concepts for {args.entity}:")
        for s in suggestions:
            print(f"  - {s['concept']['id']}: {s['concept']['properties'].get('name', '')} (score: {s['relevance_score']:.2f})")

    else:
        parser.print_help()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
