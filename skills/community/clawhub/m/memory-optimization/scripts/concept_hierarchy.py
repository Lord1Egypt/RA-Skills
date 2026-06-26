#!/usr/bin/env python3
"""
ConceptHierarchy - Phase 4 Concept-Mediated Graph

Handles concept hierarchy operations: is_a, part_of, synonym_of relationships.
Provides functions for traversing concept hierarchies and finding related concepts.

Usage:
    python3 concept_hierarchy.py subconcepts <concept_id>
    python3 concept_hierarchy.py synonyms <concept_id>
    python3 concept_hierarchy.py path <concept_id1> <concept_id2>
"""

import sys
import logging
from pathlib import Path
from typing import List, Dict, Set, Optional

SCRIPT_DIR = Path(__file__).parent
WORKSPACE_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from memory_ontology import load_all_relations, load_all_entities


def get_subconcepts(concept_id: str) -> List[str]:
    """Get all direct and indirect subconcepts of a concept

    Args:
        concept_id: The parent concept ID

    Returns:
        List of subconcept IDs (direct and indirect)
    """
    relations = load_all_relations()

    subconcept_ids = []
    to_visit = [concept_id]
    visited: Set[str] = set()

    while to_visit:
        current = to_visit.pop()
        if current in visited:
            continue
        visited.add(current)

        for rel in relations:
            if rel.get('rel') == 'is_a' and rel.get('from') == current:
                child_id = rel.get('to')
                if child_id not in visited:
                    subconcept_ids.append(child_id)
                    to_visit.append(child_id)

    return subconcept_ids


def get_parent_concepts(concept_id: str) -> List[str]:
    """Get all direct and indirect parent concepts

    Args:
        concept_id: The child concept ID

    Returns:
        List of parent concept IDs
    """
    relations = load_all_relations()

    parent_ids = []
    to_visit = [concept_id]
    visited: Set[str] = set()

    while to_visit:
        current = to_visit.pop()
        if current in visited:
            continue
        visited.add(current)

        for rel in relations:
            if rel.get('rel') == 'is_a' and rel.get('to') == current:
                parent_id = rel.get('from')
                if parent_id not in visited:
                    parent_ids.append(parent_id)
                    to_visit.append(parent_id)

    return parent_ids


def get_transitive_closure(concept_id: str) -> Set[str]:
    """Get the transitive closure of a concept (all descendants)

    Args:
        concept_id: Starting concept ID

    Returns:
        Set of all descendant concept IDs
    """
    relations = load_all_relations()

    closure: Set[str] = set()
    to_visit = [concept_id]
    visited: Set[str] = set()

    while to_visit:
        current = to_visit.pop()
        if current in visited:
            continue
        visited.add(current)

        for rel in relations:
            if rel.get('rel') == 'is_a' and rel.get('from') == current:
                child_id = rel.get('to')
                if child_id not in visited:
                    closure.add(child_id)
                    to_visit.append(child_id)

    return closure


def get_synonyms(concept_id: str) -> List[str]:
    """Get all synonyms of a concept (transitive closure)

    Args:
        concept_id: Concept ID to find synonyms for

    Returns:
        List of all synonym concept IDs (including transitive)
    """
    relations = load_all_relations()

    synonyms: Set[str] = set()
    to_visit = [concept_id]
    visited: Set[str] = set()

    while to_visit:
        current = to_visit.pop()
        if current in visited:
            continue
        visited.add(current)

        for rel in relations:
            if rel.get('rel') == 'synonym_of':
                if rel.get('from') == current and rel.get('to') != concept_id:
                    synonyms.add(rel.get('to'))
                    if rel.get('to') not in visited:
                        to_visit.append(rel.get('to'))
                elif rel.get('to') == current and rel.get('from') != concept_id:
                    synonyms.add(rel.get('from'))
                    if rel.get('from') not in visited:
                        to_visit.append(rel.get('from'))

    return list(synonyms)


def get_related_concepts(concept_id: str) -> Dict[str, List[str]]:
    """Get all related concepts (hierarchical + synonyms)

    Args:
        concept_id: Concept ID

    Returns:
        Dict with 'parents', 'children', 'synonyms' keys
    """
    return {
        'parents': get_parent_concepts(concept_id),
        'children': get_subconcepts(concept_id),
        'synonyms': get_synonyms(concept_id)
    }


def find_common_ancestors(concept_id1: str, concept_id2: str) -> List[str]:
    """Find common ancestors of two concepts

    Args:
        concept_id1: First concept ID
        concept_id2: Second concept ID

    Returns:
        List of common ancestor concept IDs
    """
    ancestors1 = set(get_parent_concepts(concept_id1))
    ancestors1.add(concept_id1)

    ancestors2 = set(get_parent_concepts(concept_id2))
    ancestors2.add(concept_id2)

    return list(ancestors1 & ancestors2)


def find_lca(concept_id1: str, concept_id2: str) -> Optional[str]:
    """Find the lowest common ancestor of two concepts

    Args:
        concept_id1: First concept ID
        concept_id2: Second concept ID

    Returns:
        Lowest common ancestor concept ID, or None if not found
    """
    ancestors1 = set(get_parent_concepts(concept_id1))
    ancestors1.add(concept_id1)

    ancestors2 = set(get_parent_concepts(concept_id2))
    ancestors2.add(concept_id2)

    common = ancestors1 & ancestors2

    if not common:
        return None

    depth_cache = {}

    def get_depth(cid: str) -> int:
        if cid in depth_cache:
            return depth_cache[cid]
        depth = 0
        current = cid
        while True:
            parents = []
            for rel in load_all_relations():
                if rel.get('rel') == 'is_a' and rel.get('to') == current:
                    parents.append(rel.get('from'))
            if not parents:
                break
            current = parents[0]
            depth += 1
        depth_cache[cid] = depth
        return depth

    lca = None
    min_depth = float('inf')

    for concept in common:
        depth = get_depth(concept)
        if depth < min_depth:
            min_depth = depth
            lca = concept

    return lca


def is_ancestor_of(ancestor_id: str, descendant_id: str) -> bool:
    """Check if concept_id1 is an ancestor of concept_id2

    Args:
        ancestor_id: Potential ancestor concept ID
        descendant_id: Potential descendant concept ID

    Returns:
        True if ancestor_id is an ancestor of descendant_id
    """
    ancestors = get_parent_concepts(descendant_id)
    return ancestor_id in ancestors


def get_concept_depth(concept_id: str) -> int:
    """Get the depth of a concept in the hierarchy (root = 0)

    Args:
        concept_id: Concept ID

    Returns:
        Depth in hierarchy
    """
    depth = 0
    current = concept_id
    visited: Set[str] = set()

    while True:
        if current in visited:
            break
        visited.add(current)

        parents = []
        for rel in load_all_relations():
            if rel.get('rel') == 'is_a' and rel.get('to') == current:
                parents.append(rel.get('from'))

        if not parents:
            break

        current = parents[0]
        depth += 1

    return depth


def get_hierarchy_tree(concept_id: str, max_depth: int = 3) -> Dict:
    """Get the hierarchy tree starting from a concept

    Args:
        concept_id: Root concept ID
        max_depth: Maximum depth to traverse

    Returns:
        Dictionary representing the tree structure
    """
    relations = load_all_relations()

    def build_tree(cid: str, depth: int) -> Dict:
        if depth >= max_depth:
            return {'id': cid, 'children': []}

        children = []
        for rel in relations:
            if rel.get('rel') == 'is_a' and rel.get('from') == cid:
                child_id = rel.get('to')
                children.append(build_tree(child_id, depth + 1))

        entities = load_all_entities()
        concept_name = ''
        if cid in entities:
            concept_name = entities[cid].get('properties', {}).get('name', '')

        return {
            'id': cid,
            'name': concept_name,
            'children': children
        }

    return build_tree(concept_id, 0)


def validate_hierarchy(concept_id: str) -> List[str]:
    """Validate concept hierarchy for cycles and consistency

    Args:
        concept_id: Concept ID to validate

    Returns:
        List of error messages (empty if valid)
    """
    errors = []

    relations = load_all_relations()

    concept_relations = [r for r in relations if r.get('from') == concept_id or r.get('to') == concept_id]

    for rel in concept_relations:
        if rel.get('rel') == 'is_a':
            from_id = rel.get('from')
            to_id = rel.get('to')

            if from_id == to_id:
                errors.append(f"Circular: {concept_id} is_a itself")

    ancestors = get_parent_concepts(concept_id)
    if concept_id in ancestors:
        errors.append(f"Circular hierarchy detected for {concept_id}")

    descendants = get_transitive_closure(concept_id)
    if concept_id in descendants:
        errors.append(f"Circular transitive closure for {concept_id}")

    return errors


def main():
    import argparse

    parser = argparse.ArgumentParser(description='ConceptHierarchy - Concept Hierarchy Operations')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    sub_parser = subparsers.add_parser('subconcepts', help='Get subconcepts')
    sub_parser.add_argument('concept_id', help='Concept ID')

    syn_parser = subparsers.add_parser('synonyms', help='Get synonyms')
    syn_parser.add_argument('concept_id', help='Concept ID')

    path_parser = subparsers.add_parser('path', help='Find path between concepts')
    path_parser.add_argument('concept_id1', help='First concept ID')
    path_parser.add_argument('concept_id2', help='Second concept ID')

    tree_parser = subparsers.add_parser('tree', help='Get hierarchy tree')
    tree_parser.add_argument('concept_id', help='Root concept ID')
    tree_parser.add_argument('--depth', type=int, default=3, help='Max depth')

    lca_parser = subparsers.add_parser('lca', help='Find lowest common ancestor')
    lca_parser.add_argument('concept_id1', help='First concept ID')
    lca_parser.add_argument('concept_id2', help='Second concept ID')

    args = parser.parse_args()

    if args.command == 'subconcepts':
        subs = get_subconcepts(args.concept_id)
        print(f"Subconcepts of {args.concept_id}: {subs}")

    elif args.command == 'synonyms':
        syns = get_synonyms(args.concept_id)
        print(f"Synonyms of {args.concept_id}: {syns}")

    elif args.command == 'path':
        lca = find_lca(args.concept_id1, args.concept_id2)
        if lca:
            print(f"Path: {args.concept_id1} -> ... -> {lca} <- ... <- {args.concept_id2}")
        else:
            print("No common ancestor found")

    elif args.command == 'tree':
        tree = get_hierarchy_tree(args.concept_id, max_depth=args.depth)
        print(json.dumps(tree, indent=2))

    elif args.command == 'lca':
        lca = find_lca(args.concept_id1, args.concept_id2)
        if lca:
            print(f"LCA: {lca}")
        else:
            print("No common ancestor")

    else:
        parser.print_help()


if __name__ == '__main__':
    import json
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
