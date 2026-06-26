#!/usr/bin/env python3
"""
ConceptExtractor - Phase 4 Concept-Mediated Graph

Extracts concepts from existing entities using LLM analysis.
Concepts represent high-level semantic groupings that connect related entities.

Usage:
    python3 concept_extractor.py extract --dry-run
    python3 concept_extractor.py extract
    python3 concept_extractor.py stats
"""

import json
import sys
import logging
from pathlib import Path
from typing import List, Dict, Optional, Any, Set
from datetime import datetime

from utils.llm_client import LLMClient

SCRIPT_DIR = Path(__file__).parent
WORKSPACE_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from memory_ontology import (
    load_all_entities, create_entity, create_relation,
    generate_entity_id, get_entity, ensure_ontology_dir
)

CONCEPT_EXTRACTION_PROMPT = """You are a concept extraction expert. Analyze the given entities and identify high-level semantic concepts that connect them.

Entities to analyze:
{entities}

Your task:
1. Identify 1-5 key concepts that emerge from these entities
2. Each concept should be a high-level semantic category (e.g., "Performance Optimization", "Security", "User Experience")
3. Concepts should help connect related entities together

Output format (only JSON, no other text):
{{
  "concepts": [
    {{
      "name": "Concept Name",
      "description": "Brief description of this concept",
      "confidence": 0.0-1.0,
      "related_entity_ids": ["entity_id1", "entity_id2"]
    }}
  ]
}}

Guidelines:
- Focus on actionable, high-level concepts
- Confidence reflects how strongly the concept unites the entities
- A concept should have at least 2 related entities to be meaningful"""


class ConceptExtractor:
    """Extracts concepts from entities using LLM analysis"""

    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm_client = llm_client or LLMClient()
        self._created_concepts: Set[str] = set()

    def _entities_to_text(self, entities: List[Dict]) -> str:
        """Convert entities to text for LLM prompt"""
        lines = []
        for entity in entities:
            props = entity.get('properties', {})
            title = props.get('title', props.get('name', ''))
            content = props.get('content', props.get('rationale', props.get('lesson', '')))
            entity_type = entity.get('type', 'Unknown')
            entity_id = entity.get('id', '')

            lines.append(f"- [{entity_type}] {entity_id}: {title}")
            if content:
                lines.append(f"  Content: {content[:200]}")

        return '\n'.join(lines)

    def extract_concepts(self, entities: List[Dict], dry_run: bool = False) -> List[Dict]:
        """Extract concepts from a list of entities

        Args:
            entities: List of entities to analyze
            dry_run: If True, don't actually create entities

        Returns:
            List of extracted concept dictionaries
        """
        if not entities:
            return []

        if len(entities) < 2:
            logging.warning("Need at least 2 entities to extract concepts")
            return []

        entities_text = self._entities_to_text(entities)

        prompt = CONCEPT_EXTRACTION_PROMPT.format(entities=entities_text)

        messages = [
            {"role": "system", "content": "You are a concept extraction expert. Output only JSON."},
            {"role": "user", "content": prompt}
        ]

        response = self.llm_client.call(messages)
        if not response:
            logging.error("LLM call failed for concept extraction")
            return []

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                data = json.loads(json_str)
                concepts = data.get('concepts', [])
            else:
                logging.error(f"No JSON found in LLM response: {response}")
                return []
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse LLM response: {e}")
            return []

        if dry_run:
            return concepts

        created_concepts = []
        for concept_data in concepts:
            concept = self._create_concept_entity(concept_data)
            if concept:
                created_concepts.append(concept)

        return created_concepts

    def _create_concept_entity(self, concept_data: Dict) -> Optional[Dict]:
        """Create a Concept entity from extracted data

        Args:
            concept_data: Concept data from LLM extraction

        Returns:
            Created Concept entity or None
        """
        name = concept_data.get('name')
        if not name:
            return None

        description = concept_data.get('description', '')
        related_entity_ids = concept_data.get('related_entity_ids', [])
        confidence = concept_data.get('confidence', 0.5)

        now = datetime.now().astimezone().isoformat()

        props = {
            'name': name,
            'description': description,
            'related_concepts': [],
            'instance_count': len(related_entity_ids),
            'created_at': now,
            'tags': ['#concept', '#extracted'],
            'confidence': confidence,
            'provenance': ['concept_extractor:phase4']
        }

        try:
            concept = create_entity('Concept', props)
            self._created_concepts.add(concept['id'])

            for entity_id in related_entity_ids:
                self._link_entity_to_concept(concept['id'], entity_id)

            return concept
        except Exception as e:
            logging.error(f"Failed to create concept {name}: {e}")
            return None

    def _link_entity_to_concept(self, concept_id: str, entity_id: str):
        """Link an entity to a concept

        Args:
            concept_id: Concept entity ID
            entity_id: Entity ID to link
        """
        try:
            create_relation(entity_id, 'instance_of', concept_id)

            entity = get_entity(entity_id, refresh_strength=False)
            if entity:
                props = entity.get('properties', {})
                concepts = props.get('concepts', [])
                if concept_id not in concepts:
                    concepts.append(concept_id)
                    props['concepts'] = concepts

        except Exception as e:
            logging.warning(f"Failed to link entity {entity_id} to concept {concept_id}: {e}")

    def run_extraction(self, dry_run: bool = False, max_entities: int = 100) -> Dict:
        """Run concept extraction on all eligible entities

        Args:
            dry_run: If True, don't create entities
            max_entities: Maximum entities to process

        Returns:
            Statistics dictionary
        """
        ensure_ontology_dir()

        print(f"\n{'='*60}")
        print(f"Concept Extractor - {'DRY RUN' if dry_run else 'LIVE RUN'}")
        print(f"{'='*60}\n")

        entities = load_all_entities()
        eligible_types = {'Decision', 'Finding', 'LessonLearned', 'Commitment'}

        eligible_entities = [
            e for e in entities.values()
            if e['type'] in eligible_types
            and not e.get('properties', {}).get('consolidated_into')
            and not e.get('properties', {}).get('is_archived')
        ]

        eligible_entities = eligible_entities[:max_entities]

        print(f"Found {len(eligible_entities)} eligible entities")

        if not eligible_entities:
            print("No eligible entities to process")
            return {'concepts_extracted': 0, 'entities_processed': 0}

        concepts = self.extract_concepts(eligible_entities, dry_run=dry_run)

        stats = {
            'concepts_extracted': len(concepts),
            'entities_processed': len(eligible_entities)
        }

        print(f"\nExtracted {len(concepts)} concepts from {len(eligible_entities)} entities")

        return stats


def main():
    import argparse

    parser = argparse.ArgumentParser(description='ConceptExtractor - Phase 4 Concept Extraction')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    extract_parser = subparsers.add_parser('extract', help='Extract concepts from entities')
    extract_parser.add_argument('--dry-run', action='store_true', help='Dry run mode')

    stats_parser = subparsers.add_parser('stats', help='Show concept statistics')

    args = parser.parse_args()

    if args.command == 'extract':
        extractor = ConceptExtractor()
        extractor.run_extraction(dry_run=args.dry_run)

    elif args.command == 'stats':
        from memory_ontology import get_entities_by_type

        concepts = get_entities_by_type('Concept')
        print(f"\nTotal Concepts: {len(concepts)}")

        if concepts:
            total_instances = sum(c.get('properties', {}).get('instance_count', 0) for c in concepts)
            print(f"Total Instance Links: {total_instances}")

    else:
        parser.print_help()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
