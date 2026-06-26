"""
HeteroMind - NL2SPARQL Base Engine

Base class and result types for NL2SPARQL engines.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum
import logging

from ..base import BaseEngine, QueryResult

logger = logging.getLogger(__name__)


class SPARQLGenerationStage(Enum):
    """Stages in SPARQL generation pipeline"""
    ENTITY_LINKING = "entity_linking"
    ONTOLOGY_RETRIEVAL = "ontology_retrieval"
    INITIAL_GENERATION = "initial_generation"
    SELF_REVISION = "self_revision"
    VALIDATION = "validation"
    EXECUTION = "execution"
    RESULT_VERIFICATION = "result_verification"


@dataclass
class SPARQLGenerationStep:
    """Single step in SPARQL generation"""
    stage: SPARQLGenerationStage
    input: Any
    output: Any
    llm_response: Optional[str] = None
    confidence: float = 0.0
    reasoning: str = ""
    execution_time_ms: float = 0.0
    error: Optional[str] = None


@dataclass
class LinkedEntity:
    """Entity linked to knowledge graph"""
    mention: str
    uri: str
    label: str
    score: float
    types: List[str] = field(default_factory=list)


@dataclass
class NL2SPARQLResult(QueryResult):
    """Extended QueryResult for NL2SPARQL"""
    generated_sparql: Optional[str] = None
    execution_steps: List[SPARQLGenerationStep] = field(default_factory=list)
    linked_entities: List[LinkedEntity] = field(default_factory=list)
    ontology_used: Optional[Dict] = None
    revision_count: int = 0
    voting_results: Optional[List[Dict]] = None
    final_confidence: float = 0.0


class BaseNL2SPARQLEngine(BaseEngine):
    """
    Base class for NL2SPARQL engines.
    
    Provides common utilities for:
    - Entity linking to KG
    - Ontology retrieval
    - Multi-stage SPARQL generation
    - Self-revision mechanisms
    - Voting between candidates
    - Result validation
    """
    
    def __init__(self, config: dict):
        """
        Initialize NL2SPARQL engine.
        
        Args:
            config: Configuration dict with:
                - endpoint_url: SPARQL endpoint URL
                - ontology: KG ontology metadata
                - llm_config: LLM configuration
                - generation_config: Generation parameters
        """
        super().__init__(config)
        
        self.endpoint_url = config.get("endpoint_url")
        self.ontology = config.get("ontology", {})
        self.llm_config = config.get("llm_config", {})
        self.generation_config = config.get("generation_config", {
            "num_candidates": 3,
            "max_revisions": 2,
            "voting_enabled": True,
            "parallel_generation": True,
            "entity_linking_threshold": 0.7,
        })
        
        # Ontology index for efficient retrieval
        self.ontology_index = self._build_ontology_index()
    
    def _build_ontology_index(self) -> Dict:
        """Build searchable ontology index"""
        index = {
            "classes": {},
            "properties": {},
            "instances": {},
            "relationships": [],
        }
        
        # Index classes
        for cls in self.ontology.get("classes", []):
            class_name = cls["name"].lower()
            index["classes"][class_name] = cls
            
            # Index labels and synonyms
            for label in cls.get("labels", []):
                index["classes"][label.lower()] = cls
            
            for synonym in cls.get("synonyms", []):
                index["classes"][synonym.lower()] = cls
        
        # Index properties
        for prop in self.ontology.get("properties", []):
            prop_name = prop["name"].lower()
            index["properties"][prop_name] = prop
            
            # Index labels
            for label in prop.get("labels", []):
                index["properties"][label.lower()] = prop
        
        # Index relationships (object properties)
        for rel in self.ontology.get("relationships", []):
            index["relationships"].append(rel)
            
            # Index by predicate name
            predicate = rel.get("predicate", "").lower()
            if predicate:
                index["properties"][predicate] = rel
        
        logger.debug(f"Built ontology index: {len(index['classes'])} classes, "
                    f"{len(index['properties'])} properties")
        
        return index
    
    async def link_entities(self, query: str) -> List[LinkedEntity]:
        """
        Link entity mentions in query to knowledge graph.
        
        Args:
            query: Natural language query
            
        Returns:
            List of linked entities
        """
        # Extract entity mentions (simple NER)
        mentions = self._extract_entity_mentions(query)
        
        linked = []
        threshold = self.generation_config.get("entity_linking_threshold", 0.7)
        
        for mention in mentions:
            # Search ontology for match
            best_match = self._find_best_entity_match(mention)
            
            if best_match and best_match["score"] >= threshold:
                linked.append(LinkedEntity(
                    mention=mention,
                    uri=best_match["uri"],
                    label=best_match["label"],
                    score=best_match["score"],
                    types=best_match.get("types", []),
                ))
        
        logger.debug(f"Linked {len(linked)}/{len(mentions)} entities")
        
        return linked
    
    def _extract_entity_mentions(self, query: str) -> List[str]:
        """Extract potential entity mentions from query"""
        import re
        
        mentions = []
        
        # Quoted strings
        quoted = re.findall(r'"([^"]+)"|\'([^\']+)\'', query)
        mentions.extend([q[0] or q[1] for q in quoted if q[0] or q[1]])
        
        # Capitalized phrases (simple NER)
        capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', query)
        mentions.extend(capitalized)
        
        # Remove duplicates
        seen = set()
        unique = []
        for m in mentions:
            if m not in seen and len(m) > 1:
                seen.add(m)
                unique.append(m)
        
        return unique
    
    def _find_best_entity_match(self, mention: str) -> Optional[Dict]:
        """Find best ontology match for entity mention"""
        mention_lower = mention.lower()
        best_match = None
        best_score = 0.0
        
        # Check classes
        for class_name, cls in self.ontology_index["classes"].items():
            if mention_lower == class_name:
                return {
                    "uri": cls.get("uri", f"http://example.org/{class_name}"),
                    "label": cls.get("label", mention),
                    "score": 1.0,
                    "types": [cls.get("name")],
                }
            elif mention_lower in class_name or class_name in mention_lower:
                score = 0.8
                if score > best_score:
                    best_score = score
                    best_match = {
                        "uri": cls.get("uri"),
                        "label": cls.get("label", mention),
                        "score": score,
                        "types": [cls.get("name")],
                    }
        
        # Check properties
        for prop_name, prop in self.ontology_index["properties"].items():
            if mention_lower == prop_name:
                return {
                    "uri": prop.get("uri"),
                    "label": prop.get("label", mention),
                    "score": 1.0,
                    "types": ["Property"],
                }
        
        return best_match if best_score >= 0.5 else None
    
    def retrieve_relevant_ontology(
        self,
        query: str,
        linked_entities: List[LinkedEntity],
    ) -> Dict:
        """
        Retrieve ontology elements relevant to the query.
        
        Args:
            query: Natural language query
            linked_entities: Linked entity mentions
            
        Returns:
            Relevant ontology subset
        """
        relevant = {
            "classes": [],
            "properties": [],
            "relationships": [],
        }
        
        # Add types of linked entities
        for entity in linked_entities:
            for type_uri in entity.types:
                cls = self.ontology_index["classes"].get(type_uri.lower())
                if cls and cls not in relevant["classes"]:
                    relevant["classes"].append(cls)
        
        # Find properties based on query keywords
        query_lower = query.lower()
        for prop_name, prop in self.ontology_index["properties"].items():
            if prop_name in query_lower:
                relevant["properties"].append(prop)
        
        # Find relationships for matched classes
        class_uris = {c.get("uri") for c in relevant["classes"]}
        for rel in self.ontology_index["relationships"]:
            domain = rel.get("domain", "")
            range_ = rel.get("range", "")
            if domain in class_uris or range_ in class_uris:
                relevant["relationships"].append(rel)
        
        logger.debug(f"Retrieved ontology: {len(relevant['classes'])} classes, "
                    f"{len(relevant['properties'])} properties")
        
        return relevant
    
    async def generate_sparql_candidates(
        self,
        query: str,
        ontology: Dict,
        linked_entities: List[LinkedEntity],
        num_candidates: int = 3,
    ) -> List[str]:
        """
        Generate multiple SPARQL candidates.
        
        Args:
            query: Natural language query
            ontology: Relevant ontology subset
            linked_entities: Linked entities
            num_candidates: Number of candidates
            
        Returns:
            List of SPARQL query strings
        """
        raise NotImplementedError
    
    async def revise_sparql(
        self,
        query: str,
        sparql: str,
        ontology: Dict,
        error: Optional[str] = None,
    ) -> str:
        """
        Revise SPARQL based on feedback.
        
        Args:
            query: Original query
            sparql: Current SPARQL
            ontology: Ontology subset
            error: Error message if any
            
        Returns:
            Revised SPARQL
        """
        raise NotImplementedError
    
    def validate_sparql(self, sparql: str) -> Dict:
        """
        Validate SPARQL syntax and semantics.
        
        Args:
            sparql: SPARQL query string
            
        Returns:
            Validation result with errors/warnings
        """
        validation = {
            "valid": True,
            "errors": [],
            "warnings": [],
        }
        
        # Basic syntax checks
        sparql_upper = sparql.upper().strip()
        
        # Must contain SELECT or ASK
        if "SELECT" not in sparql_upper and "ASK" not in sparql_upper:
            validation["valid"] = False
            validation["errors"].append("Missing SELECT or ASK clause")
        
        # Must contain WHERE
        if "WHERE" not in sparql_upper:
            validation["valid"] = False
            validation["errors"].append("Missing WHERE clause")
        
        # Check for balanced braces
        if sparql.count("{") != sparql.count("}"):
            validation["valid"] = False
            validation["errors"].append("Unbalanced braces")
        
        # Check for PREFIX declarations (warning only)
        if "PREFIX" not in sparql_upper and "http://" in sparql.lower():
            validation["warnings"].append("Consider adding PREFIX declarations")
        
        return validation
    
    async def vote_on_candidates(
        self,
        query: str,
        candidates: List[str],
        ontology: Dict,
        linked_entities: List[LinkedEntity],
    ) -> Dict:
        """
        Vote on multiple SPARQL candidates.
        
        Args:
            query: Original query
            candidates: SPARQL candidates
            ontology: Ontology subset
            linked_entities: Linked entities
            
        Returns:
            Voting results
        """
        voting_results = []
        
        for i, sparql in enumerate(candidates):
            score = self._score_candidate(
                query, sparql, ontology, linked_entities
            )
            voting_results.append({
                "index": i,
                "sparql": sparql,
                "score": score,
                "criteria": self._get_scoring_criteria(),
            })
        
        best = max(voting_results, key=lambda x: x["score"])
        
        return {
            "best_index": best["index"],
            "best_sparql": best["sparql"],
            "best_score": best["score"],
            "all_results": voting_results,
        }
    
    def _score_candidate(
        self,
        query: str,
        sparql: str,
        ontology: Dict,
        linked_entities: List[LinkedEntity],
    ) -> float:
        """Score a SPARQL candidate"""
        score = 0.0
        sparql_lower = sparql.lower()
        
        # Criterion 1: Uses linked entities
        for entity in linked_entities:
            if entity.uri.lower() in sparql_lower or \
               entity.label.lower() in sparql_lower:
                score += 0.2
        
        # Criterion 2: Has proper structure
        if "SELECT" in sparql.upper() and "WHERE" in sparql.upper():
            score += 0.3
        
        # Criterion 3: Valid syntax
        validation = self.validate_sparql(sparql)
        if validation["valid"]:
            score += 0.3
        else:
            score -= len(validation["errors"]) * 0.2
        
        # Criterion 4: Uses ontology properties
        for prop in ontology.get("properties", []):
            if prop.get("name", "").lower() in sparql_lower:
                score += 0.1
        
        return min(1.0, max(0.0, score))
    
    def _get_scoring_criteria(self) -> Dict:
        """Get scoring criteria descriptions"""
        return {
            "entity_use": "Uses linked entities",
            "structure": "Has proper SPARQL structure",
            "validity": "No syntax errors",
            "ontology_use": "Uses ontology properties",
        }
