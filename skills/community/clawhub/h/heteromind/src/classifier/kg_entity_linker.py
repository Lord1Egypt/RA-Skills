"""
HeteroMind - Layer 3b: KG Entity Linker

Links query entities to knowledge graph entities via SPARQL.
"""

import re
import logging
from typing import Dict, List

from .models import EntityLinking, KGEntity

logger = logging.getLogger(__name__)


class KGEntityLinker:
    """
    Layer 3b: KG entity linking.
    
    Extracts entity mentions from queries and links them to
    knowledge graph entities via SPARQL endpoints.
    """
    
    PREDICATE_PATTERNS = {
        "authorOf": r"(author|wrote|written by|published)",
        "worksAt": r"(works at|employed by|employee of)",
        "locatedIn": r"(located in|situated in|based in)",
        "partOf": r"(part of|member of|belongs to)",
        "bornIn": r"(born in|birthplace)",
        "founderOf": r"(founder of|founded|established)",
        "ceoOf": r"(ceo of|chief executive|head of)",
        "capitalOf": r"(capital of|capital city)",
    }
    
    def __init__(self, config: dict):
        """
        Initialize KG linker.
        
        Args:
            config: Configuration dict with:
                - endpoints: List of SPARQL endpoint configs
                - max_candidates: Max candidates per entity (default: 5)
                - min_similarity: Min similarity score (default: 0.7)
        """
        self.config = config
        self.endpoints = config.get("endpoints", [])
        self.max_candidates = config.get("max_candidates", 5)
        self.min_similarity = config.get("min_similarity", 0.7)
    
    def _extract_entities(self, query: str) -> List[str]:
        """Extract potential entity mentions from query"""
        entities = []
        
        # Quoted strings
        quoted = re.findall(r'"([^"]+)"|\'([^\']+)\'', query)
        entities.extend([q[0] or q[1] for q in quoted])
        
        # Capitalized phrases (simple NER heuristic)
        capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', query)
        entities.extend(capitalized)
        
        # Remove duplicates while preserving order
        seen = set()
        unique = []
        for e in entities:
            if e not in seen and len(e) > 1:
                seen.add(e)
                unique.append(e)
        
        return unique
    
    async def _search_kg(self, entity_mention: str, endpoint: dict) -> List[KGEntity]:
        """Search KG for entity mention via SPARQL"""
        sparql = f"""
        SELECT ?entity ?label ?desc WHERE {{
            ?entity rdfs:label ?label .
            FILTER(CONTAINS(LCASE(?label), "{entity_mention.lower()}"))
            OPTIONAL {{ ?entity rdfs:comment ?desc }}
        }}
        ORDER BY ?label
        LIMIT {self.max_candidates}
        """
        
        logger.debug(f"SPARQL query for '{entity_mention}': {sparql[:100]}...")
        
        # In real implementation, execute SPARQL here
        # For now, return empty list
        return []
    
    async def link_query(self, query: str) -> EntityLinking:
        """
        Link query entities to knowledge graph.
        
        Args:
            query: Natural language query string
            
        Returns:
            EntityLinking with linked entities
        """
        entity_mentions = self._extract_entities(query)
        
        if not entity_mentions:
            return EntityLinking(
                linked_entities=[],
                detected_predicates=[],
                confidence=0.0,
                is_kg_likely=False,
            )
        
        logger.debug(f"Extracted entities: {entity_mentions}")
        
        # Search each endpoint
        all_linked = []
        for endpoint in self.endpoints:
            if not endpoint.get("enabled", True):
                continue
            
            for mention in entity_mentions:
                results = await self._search_kg(mention, endpoint)
                all_linked.extend([
                    {
                        "mention": mention,
                        "entity": e.uri,
                        "label": e.label,
                        "score": e.score,
                    }
                    for e in results
                ])
        
        # Detect predicates from query verbs
        predicates = self._detect_predicates(query, all_linked)
        
        # Calculate confidence
        kg_confidence = len(all_linked) / max(len(entity_mentions), 1) * 0.5
        kg_confidence += len(predicates) * 0.1
        kg_confidence = min(1.0, kg_confidence)
        
        logger.debug(f"KG linking: {len(all_linked)} entities, {len(predicates)} predicates")
        
        return EntityLinking(
            linked_entities=all_linked,
            detected_predicates=predicates,
            confidence=kg_confidence,
            is_kg_likely=kg_confidence > 0.4,
        )
    
    def _detect_predicates(self, query: str, entities: List[Dict]) -> List[str]:
        """Detect predicates from query verbs/phrases"""
        predicates = []
        query_lower = query.lower()
        
        for pred, pattern in self.PREDICATE_PATTERNS.items():
            if re.search(pattern, query_lower):
                predicates.append(pred)
        
        return predicates
