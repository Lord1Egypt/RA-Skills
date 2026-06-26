"""
schema_extractor.py
Extracts structured knowledge schemas from conversation patterns.

Identifies entities, relationships, and event patterns from episodic memories.
Bridges NIMA's VSA-encoded memories to symbolic knowledge graphs.

Author: Lilu (with David's knowledge extraction architecture)
Date: Feb 13, 2026
"""

import re
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field
from collections import defaultdict
import time


# Note: utils.security not available in nima-core, using fallback


@dataclass
class Entity:
    """Represents a detected entity (person, place, thing, concept)."""
    name: str
    entity_type: str  # 'person', 'place', 'concept', 'event', 'attribute'
    aliases: Set[str] = field(default_factory=set)
    mention_count: int = 0
    first_seen: str = ""
    last_seen: str = ""
    properties: Dict[str, Any] = field(default_factory=dict)
    
    def add_alias(self, alias: str):
        """Add an alias for this entity."""
        self.aliases.add(alias.lower())
        self.mention_count += 1
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            'name': self.name,
            'type': self.entity_type,
            'aliases': list(self.aliases),
            'mention_count': self.mention_count,
            'first_seen': self.first_seen,
            'last_seen': self.last_seen,
            'properties': self.properties,
        }


@dataclass
class Relationship:
    """Represents a relationship between entities."""
    subject: str
    predicate: str
    object_: str
    confidence: float = 1.0
    evidence: List[str] = field(default_factory=list)  # Source memory IDs
    frequency: int = 1
    
    def add_evidence(self, memory_id: str):
        """Add supporting evidence for this relationship."""
        if memory_id not in self.evidence:
            self.evidence.append(memory_id)
            self.frequency += 1
    
    @property
    def key(self) -> Tuple[str, str, str]:
        """Return a unique key for this relationship."""
        return (self.subject.lower(), self.predicate.lower(), self.object_.lower())
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            'subject': self.subject,
            'predicate': self.predicate,
            'object': self.object_,
            'confidence': self.confidence,
            'evidence_count': len(self.evidence),
            'frequency': self.frequency,
        }


@dataclass
class EventPattern:
    """Represents a recurring event pattern."""
    pattern_name: str
    participants: List[str]  # Entity names (or roles like 'user', 'assistant')
    action: str
    location: Optional[str] = None
    frequency: int = 1
    last_occurrence: str = ""
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            'pattern_name': self.pattern_name,
            'participants': self.participants,
            'action': self.action,
            'location': self.location,
            'frequency': self.frequency,
            'last_occurrence': self.last_occurrence,
        }


@dataclass
class Schema:
    """Complete knowledge schema extracted from conversation history."""
    entities: Dict[str, Entity] = field(default_factory=dict)
    relationships: Dict[Tuple[str, str, str], Relationship] = field(default_factory=dict)
    event_patterns: List[EventPattern] = field(default_factory=list)
    
    # Metadata
    extraction_time: float = 0.0
    memories_processed: int = 0
    
    def add_entity(self, entity: Entity):
        """Add or update an entity."""
        key = entity.name.lower()
        if key in self.entities:
            # Merge
            existing = self.entities[key]
            existing.aliases.update(entity.aliases)
            existing.mention_count += entity.mention_count
            if entity.last_seen:
                existing.last_seen = entity.last_seen
        else:
            self.entities[key] = entity
    
    def add_relationship(self, rel: Relationship):
        """Add or update a relationship."""
        key = rel.key
        if key in self.relationships:
            existing = self.relationships[key]
            for mem_id in rel.evidence:
                existing.add_evidence(mem_id)
            existing.confidence = min(1.0, existing.frequency / 10.0)
        else:
            self.relationships[key] = rel
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            'entities': {k: v.to_dict() for k, v in self.entities.items()},
            'relationships': [r.to_dict() for r in self.relationships.values()],
            'event_patterns': [p.to_dict() for p in self.event_patterns],
            'extraction_time': self.extraction_time,
            'memories_processed': self.memories_processed,
        }


class SchemaExtractor:
    """
    Extracts structured knowledge schemas from episodic memories.
    
    Identifies:
    - Entities (people, places, concepts, events, attributes)
    - Relationships (subject-predicate-object triples)
    - Event patterns (recurring scenarios)
    
    Usage:
        extractor = SchemaExtractor()
        schema = extractor.extract_schema(memories)
        extractor.save_schema(schema, "schema.json")
    """
    
    def __init__(self):
        """Initialize the schema extractor."""
        # Entity patterns and rules
        self._init_entity_patterns()
        self._init_relationship_patterns()
        
        # Statistics
        self.stats = {
            'extractions': 0,
            'total_entities': 0,
            'total_relationships': 0,
            'total_patterns': 0,
        }
    
    def _init_entity_patterns(self):
        """Initialize patterns for entity recognition."""
        # Named entity patterns
        self.name_patterns = [
            # Direct addressing: "David, ..."
            (r'\b([A-Z][a-z]+),?\s+(?:can you|could you|please|what|how|why|let me)', 'person'),
            # User references: "my wife", "my daughter"
            (r'\bmy\s+(wife|husband|son|daughter|mother|father|brother|sister|friend|colleague)\b', 'person'),
            # Capitalized names in context
            (r'\b([A-Z][a-z]+)\s+(?:said|told|asked|mentioned|replied|wrote)\b', 'person'),
            # Places
            (r'\b(at|in|to|from)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b', 'place'),
            # Organizations
            (r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:Company|Inc|Corp|LLC|Organization|Institute)\b', 'organization'),
            # Technical terms
            (r'\b(NIMA|VSA|MCP|RAG|LLM|GPT|Claude|OpenAI|Anthropic)\b', 'concept'),
            # Projects
            (r'\b([A-Z][a-z]+(?:-[a-z]+)*)\s+(?:project|system|app|tool)\b', 'project'),
        ]
        
        # Attribute patterns
        self.attribute_patterns = [
            (r'\b(\w+)\s+is\s+(?:very |really |quite )?(\w+)', 'attribute'),
            (r'\b(\w+)\s+has\s+(?:a |an )?(\w+)', 'attribute'),
        ]
        
        # Common predicates
        self.predicate_patterns = [
            'said', 'told', 'asked', 'mentioned', 'replied',
            'built', 'created', 'wrote', 'designed', 'implemented',
            'uses', 'has', 'is', 'works with', 'works on',
            'likes', 'loves', 'prefers', 'wants', 'needs',
            'connected to', 'related to', 'depends on',
        ]
    
    def _init_relationship_patterns(self):
        """Initialize patterns for relationship extraction."""
        self.relationship_patterns = [
            # X told Y about Z
            (r'(\w+)\s+told\s+(\w+)\s+about\s+(\w+)', 'told_about'),
            # X works on Y
            (r'(\w+)\s+(?:works|worked)\s+(?:on|with)\s+(\w+)', 'works_on'),
            # X uses Y
            (r'(\w+)\s+uses\s+(\w+)', 'uses'),
            # X is Y's Z
            (r"(\w+)\s+is\s+(\w+)'s\s+(\w+)", 'is_owner_of'),
            # X created Y
            (r'(\w+)\s+(?:created|built|made|designed)\s+(\w+)', 'created'),
            # X connected to Y
            (r'(\w+)\s+(?:connected|related|linked)\s+to\s+(\w+)', 'connected_to'),
        ]
    
    def extract_schema(self, 
                       memories: List[Dict], 
                       text_field: str = 'raw_text',
                       id_field: str = 'id',
                       metadata_fields: Optional[List[str]] = None) -> Schema:
        """
        Extract schema from a list of episodic memories.
        
        Args:
            memories: List of memory dictionaries
            text_field: Field containing text content
            id_field: Field containing memory ID
            metadata_fields: Additional fields to check for entity information
            
        Returns:
            Complete Schema with entities, relationships, and patterns
        """
        start_time = time.time()
        schema = Schema()
        
        for memory in memories:
            memory_id = str(memory.get(id_field, ''))
            text = memory.get(text_field, '')
            timestamp = str(memory.get('timestamp', memory.get('when', '')))
            
            # Extract entities from text
            entities = self._extract_entities(text, timestamp)
            for entity in entities:
                schema.add_entity(entity)
            
            # Extract relationships
            relationships = self._extract_relationships(text, memory_id)
            for rel in relationships:
                schema.add_relationship(rel)
            
            # Check metadata for additional entities
            if metadata_fields:
                for field in metadata_fields:
                    if field in memory and memory[field]:
                        meta_entity = Entity(
                            name=str(memory[field]),
                            entity_type='attribute',
                            first_seen=timestamp,
                            last_seen=timestamp,
                        )
                        schema.add_entity(meta_entity)
            
            schema.memories_processed += 1
        
        # Find event patterns
        schema.event_patterns = self._find_event_patterns(memories, schema.entities)
        
        # Update statistics
        schema.extraction_time = time.time() - start_time
        self.stats['extractions'] += 1
        self.stats['total_entities'] += len(schema.entities)
        self.stats['total_relationships'] += len(schema.relationships)
        self.stats['total_patterns'] += len(schema.event_patterns)
        
        return schema
    
    def _extract_entities(self, text: str, timestamp: str = "") -> List[Entity]:
        """Extract entities from text using patterns."""
        entities = []
        seen = set()
        
        # Apply name patterns
        for pattern, entity_type in self.name_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                # Extract the entity name (usually first group)
                name = match.group(1) if match.lastindex and match.lastindex >= 1 else match.group(0)
                name = name.strip()
                
                if name and len(name) > 1 and name.lower() not in seen:
                    seen.add(name.lower())
                    entity = Entity(
                        name=name,
                        entity_type=entity_type,
                        first_seen=timestamp,
                        last_seen=timestamp,
                    )
                    entities.append(entity)
        
        # Also extract from WHO/WHAT/WHERE if present in structured text
        structured_patterns = [
            (r'WHO[:\s]+([^\n,;]+)', 'person'),
            (r'WHAT[:\s]+([^\n,;]+)', 'event'),
            (r'WHERE[:\s]+([^\n,;]+)', 'place'),
        ]
        
        for pattern, entity_type in structured_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                name = match.group(1).strip()
                if name and len(name) > 1 and name.lower() not in seen:
                    seen.add(name.lower())
                    entity = Entity(
                        name=name,
                        entity_type=entity_type,
                        first_seen=timestamp,
                        last_seen=timestamp,
                    )
                    entities.append(entity)
        
        return entities
    
    def _extract_relationships(self, text: str, memory_id: str) -> List[Relationship]:
        """Extract relationships from text using patterns."""
        relationships = []
        
        for pattern, predicate in self.relationship_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                groups = match.groups()
                if len(groups) >= 2:
                    subject = groups[0].strip()
                    obj = groups[-1].strip()
                    
                    if subject and obj and subject.lower() != obj.lower():
                        rel = Relationship(
                            subject=subject,
                            predicate=predicate,
                            object_=obj,
                            confidence=0.5,
                            evidence=[memory_id],
                        )
                        relationships.append(rel)
        
        return relationships
    
    def _find_event_patterns(self, 
                             memories: List[Dict],
                             entities: Dict[str, Entity]) -> List[EventPattern]:
        """Find recurring event patterns in memories."""
        patterns = []
        
        # Group by action verbs
        action_groups = defaultdict(list)
        for memory in memories:
            text = memory.get('raw_text', '')
            # Extract action verbs
            verbs = re.findall(r'\b(wrote|sent|called|met|built|created|discussed|asked|told)\b', text.lower())
            for verb in verbs:
                action_groups[verb].append(memory)
        
        # Create patterns for frequent actions
        for action, group in action_groups.items():
            if len(group) >= 2:  # At least 2 occurrences
                pattern = EventPattern(
                    pattern_name=f"frequent_{action}",
                    participants=list(entities.keys())[:5],  # Top entities
                    action=action,
                    frequency=len(group),
                    last_occurrence=max(m.get('timestamp', '') for m in group),
                )
                patterns.append(pattern)
        
        return patterns
    
    def extract_from_vsa_memory(self, 
                                  vsa_memory,
                                  top_n: int = 100) -> Schema:
        """
        Extract schema from VSA memory using resonance with role vectors.
        
        Args:
            vsa_memory: SparseBlockMemory or NIMA instance
            top_n: Number of recent memories to analyze
            
        Returns:
            Schema extracted from VSA-encoded memories
        """
        # Get recent memories
        if hasattr(vsa_memory, 'memory_metadata'):
            # SparseBlockMemory
            memories = vsa_memory.memory_metadata[-top_n:]
        else:
            # Fallback: convert from other format
            memories = []
        
        # Add IDs to memories if missing
        for i, mem in enumerate(memories):
            if 'id' not in mem:
                mem['id'] = f"vsa_{i}"
        
        return self.extract_schema(memories)
    
    def merge_schemas(self, 
                      schema1: Schema, 
                      schema2: Schema) -> Schema:
        """
        Merge two schemas, keeping track of all evidence.
        
        Returns:
            New combined Schema
        """
        merged = Schema()
        
        # Merge entities
        for entity in schema1.entities.values():
            merged.add_entity(entity)
        for entity in schema2.entities.values():
            merged.add_entity(entity)
        
        # Merge relationships
        for rel in schema1.relationships.values():
            merged.add_relationship(rel)
        for rel in schema2.relationships.values():
            merged.add_relationship(rel)
        
        # Merge event patterns (deduplicate by name)
        pattern_names = set()
        for pattern in schema1.event_patterns + schema2.event_patterns:
            if pattern.pattern_name not in pattern_names:
                merged.event_patterns.append(pattern)
                pattern_names.add(pattern.pattern_name)
        
        merged.memories_processed = schema1.memories_processed + schema2.memories_processed
        
        return merged
    
    def save_schema(self, schema: Schema, filepath: str):
        """Save schema to JSON file."""
        import tempfile
        import os
        import hashlib
        
        # Validate and convert
        data = schema.to_dict()
        
        # Serialize to JSON
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        
        # Compute hash
        content_hash = hashlib.sha256(json_str.encode('utf-8')).hexdigest()
        data['_hash'] = content_hash
        
        # Atomic write pattern
        filepath = Path(filepath)
        with tempfile.NamedTemporaryFile(
            mode='w',
            delete=False,
            dir=filepath.parent,
            suffix='.tmp'
        ) as f:
            temp_path = f.name
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Atomic rename
        os.replace(temp_path, filepath)
        
        # Save hash sidecar for integrity verification
        hash_path = filepath.with_suffix('.sha256')
        with open(hash_path, 'w') as f:
            json.dump({
                'algorithm': 'sha256',
                'hash': content_hash,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            }, f, indent=2)
        
        print(f"💾 Schema saved to {filepath} ({len(schema.entities)} entities, {len(schema.relationships)} relationships)")
    
    def load_schema(self, filepath: str, verify: bool = True) -> Schema:
        """Load schema from JSON file."""
        
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"Schema file not found: {filepath}")
        
        # Verify integrity if hash exists
        if verify:
            hash_path = filepath.with_suffix('.sha256')
            if hash_path.exists():
                with open(hash_path, 'r') as f:
                    hash_data = json.load(f)
                
                with open(filepath, 'rb') as f:
                    actual_hash = hashlib.sha256(f.read()).hexdigest()
                
                if actual_hash != hash_data.get('hash'):
                    print(f"⚠️  Warning: Schema integrity check failed for {filepath}")
        
        # Load
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Reconstruct Schema
        schema = Schema()
        schema.extraction_time = data.get('extraction_time', 0.0)
        schema.memories_processed = data.get('memories_processed', 0)
        
        # Add entities
        for entity_data in data.get('entities', {}).values():
            entity = Entity(
                name=entity_data['name'],
                entity_type=entity_data['type'],
                aliases=set(entity_data.get('aliases', [])),
                mention_count=entity_data.get('mention_count', 0),
                first_seen=entity_data.get('first_seen', ''),
                last_seen=entity_data.get('last_seen', ''),
                properties=entity_data.get('properties', {}),
            )
            schema.entities[entity.name.lower()] = entity
        
        # Add relationships
        for rel_data in data.get('relationships', []):
            rel = Relationship(
                subject=rel_data['subject'],
                predicate=rel_data['predicate'],
                object_=rel_data['object'],
                confidence=rel_data.get('confidence', 1.0),
                frequency=rel_data.get('frequency', 1),
            )
            schema.relationships[rel.key] = rel
        
        # Add event patterns
        for pattern_data in data.get('event_patterns', []):
            pattern = EventPattern(
                pattern_name=pattern_data['pattern_name'],
                participants=pattern_data.get('participants', []),
                action=pattern_data['action'],
                location=pattern_data.get('location'),
                frequency=pattern_data.get('frequency', 1),
                last_occurrence=pattern_data.get('last_occurrence', ''),
            )
            schema.event_patterns.append(pattern)
        
        return schema
    
    def get_statistics(self) -> Dict:
        """Get extractor statistics."""
        return self.stats.copy()
    
    def query_schema(self, 
                     schema: Schema,
                     entity: Optional[str] = None,
                     relationship_type: Optional[str] = None) -> Dict:
        """
        Query schema for specific information.
        
        Args:
            schema: Schema to query
            entity: Entity name to look up
            relationship_type: Relationship type to filter
            
        Returns:
            Dict with matching results
        """
        results = {
            'entity': None,
            'relationships': [],
            'related_entities': [],
        }
        
        if entity:
            entity_key = entity.lower()
            if entity_key in schema.entities:
                results['entity'] = schema.entities[entity_key].to_dict()
            
            # Find relationships involving this entity
            for rel in schema.relationships.values():
                if rel.subject.lower() == entity_key or rel.object_.lower() == entity_key:
                    if relationship_type is None or rel.predicate == relationship_type:
                        results['relationships'].append(rel.to_dict())
                        
                        # Track related entities
                        other = rel.object_ if rel.subject.lower() == entity_key else rel.subject
                        if other not in results['related_entities']:
                            results['related_entities'].append(other)
        
        elif relationship_type:
            # Find all relationships of this type
            for rel in schema.relationships.values():
                if rel.predicate == relationship_type:
                    results['relationships'].append(rel.to_dict())
        
        return results


# =============================================================================
# Demonstration
# =============================================================================

def demo_schema_extractor():
    """Demonstrate schema extraction from sample memories."""
    print("=" * 70)
    print("SCHEMA EXTRACTOR DEMONSTRATION")
    print("=" * 70)
    
    # Sample episodic memories
    memories = [
        {
            'id': 'mem_001',
            'raw_text': 'David asked Lilu about NIMA memory system integration',
            'timestamp': '2026-02-13T10:00:00',
            'who': 'David',
            'what': 'asked about NIMA',
        },
        {
            'id': 'mem_002',
            'raw_text': 'Lilu explained how VSA encodes episodic memories',
            'timestamp': '2026-02-13T10:05:00',
            'who': 'Lilu',
            'what': 'explained VSA encoding',
        },
        {
            'id': 'mem_003',
            'raw_text': 'David built the sparse block memory module',
            'timestamp': '2026-02-13T11:00:00',
            'who': 'David',
            'what': 'built sparse memory',
        },
        {
            'id': 'mem_004',
            'raw_text': 'Melissa discussed marketing strategy with David',
            'timestamp': '2026-02-13T12:00:00',
            'who': 'Melissa',
            'what': 'discussed marketing',
        },
    ]
    
    # Create extractor
    extractor = SchemaExtractor()
    
    # Extract schema
    print("\n📊 Extracting schema from 4 memories...")
    schema = extractor.extract_schema(memories, metadata_fields=['who', 'what'])
    
    # Display results
    print(f"\n🧠 Entities found: {len(schema.entities)}")
    for name, entity in list(schema.entities.items())[:5]:
        print(f"   - {entity.name} ({entity.entity_type}): {entity.mention_count} mentions")
    
    print(f"\n🔗 Relationships found: {len(schema.relationships)}")
    for rel in list(schema.relationships.values())[:5]:
        print(f"   - {rel.subject} --[{rel.predicate}]--> {rel.object_}")
    
    print(f"\n📋 Event patterns: {len(schema.event_patterns)}")
    for pattern in schema.event_patterns[:3]:
        print(f"   - {pattern.pattern_name}: {pattern.frequency} occurrences")
    
    # Query example
    print("\n🔍 Query: 'David'")
    results = extractor.query_schema(schema, entity='David')
    if results['entity']:
        print(f"   Entity: {results['entity']['name']}")
        print(f"   Related to: {results['related_entities']}")
    
    # Statistics
    print("\n📈 Extraction statistics:")
    stats = extractor.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n" + "=" * 70)
    print("✅ Schema Extractor operational")
    print("=" * 70)


if __name__ == "__main__":
    demo_schema_extractor()