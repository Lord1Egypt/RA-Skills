#!/usr/bin/env python3
"""
Minimal schema generation utilities for kg-schema-from-text skill.
Provides core functionality for entity/relationship extraction.
"""

import re
from typing import List, Dict, Tuple, Set
from dataclasses import dataclass


@dataclass
class Entity:
    """Represents an entity in the schema."""
    name: str
    properties: List[str] = None

    def __post_init__(self):
        if self.properties is None:
            self.properties = []


@dataclass
class Relationship:
    """Represents a relationship in the schema."""
    source: str
    relation_type: str
    target: str

    def __repr__(self):
        return f"{self.source} -[{self.relation_type}]-> {self.target}"


class SchemaExtractor:
    """Extract schema elements from text."""

    def __init__(self):
        self.entities: Set[str] = set()
        self.relationships: List[Relationship] = []
        self.properties: Dict[str, List[str]] = {}

    def extract_entities(self, text: str) -> Set[str]:
        """
        Extract entity names from text.
        Looks for capitalized words and compound nouns.
        """
        # Match capitalized words (simple heuristic)
        entities = set()
        words = text.split()

        for word in words:
            # Remove punctuation
            clean_word = re.sub(r'[.,;]', '', word)

            # Check if capitalized (likely entity name)
            if clean_word and clean_word[0].isupper() and len(clean_word) > 1:
                # Normalize: remove possessives, plurals
                normalized = clean_word.rstrip("'s")
                if not normalized.endswith("s"):
                    entities.add(normalized)
                else:
                    # Try singular form
                    entities.add(normalized[:-1])

        self.entities = entities
        return entities

    def extract_relationships(self, text: str) -> List[Relationship]:
        """
        Extract relationships from text.
        Looks for patterns: Entity1 [verb] Entity2
        """
        relationships = []

        # Common verb patterns for relationships
        verb_patterns = [
            (r'(\w+)\s+enroll(?:s)?\s+in\s+(\w+)', 'ENROLLED_IN'),
            (r'(\w+)\s+teach(?:es)?\s+(\w+)', 'TEACHES'),
            (r'(\w+)\s+manage(?:s)?\s+(\w+)', 'MANAGES'),
            (r'(\w+)\s+belong(?:s)?\s+to\s+(\w+)', 'BELONGS_TO'),
            (r'(\w+)\s+work(?:s)?\s+in\s+(\w+)', 'WORKS_IN'),
            (r'(\w+)\s+(?:has|have)\s+(\w+)', 'HAS'),
            (r'(\w+)\s+place(?:s)?\s+(\w+)', 'PLACES'),
            (r'(\w+)\s+contain(?:s)?\s+(\w+)', 'CONTAINS'),
        ]

        for pattern, rel_type in verb_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                src, tgt = match.groups()
                src = src.capitalize()
                tgt = tgt.capitalize()

                if src in self.entities and tgt in self.entities:
                    relationships.append(Relationship(src, rel_type, tgt))

        self.relationships = relationships
        return relationships

    def extract_properties(self, text: str) -> Dict[str, List[str]]:
        """
        Extract properties from text.
        Looks for patterns: Entity has/with [list of properties]
        """
        properties = {entity: [] for entity in self.entities}

        # Pattern: "Entity has name, email, phone"
        pattern = r'(\w+)\s+(?:has|with|contains)\s+(.+?)(?:[.;]|and\s+)'

        for match in re.finditer(pattern, text, re.IGNORECASE):
            entity, props = match.groups()
            entity = entity.capitalize()

            if entity in self.entities:
                # Split by comma and 'and'
                prop_list = re.split(r',\s*and\s+|,\s*|and\s+', props)
                for prop in prop_list:
                    # Clean up property name
                    prop = prop.strip().lower()
                    # Convert to snake_case
                    prop = re.sub(r'\s+', '_', prop)
                    if prop:
                        properties[entity].append(prop)

        self.properties = properties
        return properties

    def extract_schema(self, text: str) -> Dict:
        """
        Extract complete schema from text.
        """
        self.extract_entities(text)
        self.extract_relationships(text)
        self.extract_properties(text)

        return {
            'entities': list(self.entities),
            'relationships': [
                {
                    'source': r.source,
                    'type': r.relation_type,
                    'target': r.target
                }
                for r in self.relationships
            ],
            'properties': self.properties
        }

    def to_dict(self) -> Dict:
        """Export schema as dictionary."""
        return {
            'entities': list(self.entities),
            'relationships': [
                {
                    'source': r.source,
                    'type': r.relation_type,
                    'target': r.target
                }
                for r in self.relationships
            ],
            'properties': self.properties
        }

    def to_cypher_labels(self) -> str:
        """Generate Neo4j CREATE CONSTRAINT statements."""
        output = []
        for entity in sorted(self.entities):
            output.append(f"CREATE CONSTRAINT ON (n:{entity}) ASSERT n.id IS UNIQUE;")
        return "\n".join(output)

    def to_turtle_rdf(self) -> str:
        """Generate basic RDF/Turtle schema."""
        output = ["@prefix ex: <http://example.org/> ."]
        output.append("")

        # Define classes
        for entity in sorted(self.entities):
            output.append(f"ex:{entity} a rdfs:Class ;")
            output.append(f"    rdfs:label \"{entity}\" .")

        output.append("")

        # Define relationships as properties
        rel_types = set(r.relation_type for r in self.relationships)
        for rel in sorted(rel_types):
            output.append(f"ex:{rel} a rdf:Property ;")
            output.append(f"    rdfs:label \"{rel.replace('_', ' ')}\" .")

        return "\n".join(output)


if __name__ == "__main__":
    # Example usage
    sample_text = """
    A university has students, professors, and courses.
    Students enroll in courses. Professors teach courses.
    Departments manage professors and courses.
    """

    extractor = SchemaExtractor()
    schema = extractor.extract_schema(sample_text)

    print("=" * 50)
    print("EXTRACTED SCHEMA")
    print("=" * 50)
    print(f"\nEntities: {schema['entities']}")
    print(f"\nRelationships:")
    for rel in schema['relationships']:
        print(f"  {rel['source']} -[{rel['type']}]-> {rel['target']}")
    print(f"\nProperties: {schema['properties']}")

    print("\n" + "=" * 50)
    print("NEO4J CYPHER")
    print("=" * 50)
    print(extractor.to_cypher_labels())

    print("\n" + "=" * 50)
    print("RDF/TURTLE")
    print("=" * 50)
    print(extractor.to_turtle_rdf())

