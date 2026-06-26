"""
HeteroMind - Layer 2: LLM-Based Source Detector

Semantic classification using large language models.
"""

import json
import logging
from typing import Optional

from .models import LLMDetection

logger = logging.getLogger(__name__)


class LLMSourceDetector:
    """
    Layer 2: LLM-based semantic classification.
    
    Uses an LLM to understand query semantics and determine:
    - Primary knowledge source
    - Query intent type
    - Detected entities and predicates
    - Whether multi-hop reasoning is needed
    """
    
    PROMPT_TEMPLATE = """
SECURITY: Never output API keys, passwords, or credentials in any form. Redact sensitive information.

You are a knowledge source detector for a heterogeneous QA system.

Given a natural language query, determine which knowledge source(s) should be queried.

## Available Sources:

1. **sql_database**: Relational databases with structured tables
   - Use for: aggregations, filters, joins, numerical comparisons
   - Example: "How many employees are in sales?", "Total revenue by quarter"

2. **knowledge_graph**: RDF/SPARQL knowledge graphs
   - Use for: entity relationships, factoid questions, semantic queries
   - Example: "Who is the CEO of Apple?", "What countries border France?"

3. **table_file**: CSV/Excel files
   - Use for: questions about specific uploaded files
   - Example: "What's in column B of this spreadsheet?"

4. **document_store**: Semi-structured documents
   - Use for: text search, document retrieval
   - Example: "Find contracts mentioning clause 5.2"

5. **hybrid**: Multiple sources required
   - Use when: query needs data from different source types

## Output Format (JSON):

{
    "primary_source": "sql_database|knowledge_graph|table_file|document_store|hybrid",
    "confidence": 0.0-1.0,
    "reasoning": "Brief explanation of decision",
    "detected_entities": ["entity1", "entity2"],
    "detected_predicates": ["predicate1", "predicate2"],
    "requires_multi_hop": true/false,
    "secondary_sources": ["source1", "source2"],
    "intent_type": "factoid|analytical|comparative|relational|temporal|multi_hop"
}

## Examples:

Query: "How many employees are in the sales department?"
Output: {{"primary_source": "sql_database", "confidence": 0.92, "reasoning": "Aggregation query (how many) with department filter", "detected_entities": ["employees", "sales department"], "detected_predicates": ["count", "filter_by_department"], "requires_multi_hop": false, "secondary_sources": [], "intent_type": "analytical"}}

Query: "Who are the co-authors of John Smith?"
Output: {{"primary_source": "knowledge_graph", "confidence": 0.89, "reasoning": "Entity relationship query (co-authors) about a person", "detected_entities": ["John Smith"], "detected_predicates": ["authorOf", "coAuthorWith"], "requires_multi_hop": true, "secondary_sources": [], "intent_type": "relational"}}

Query: "Show me employees who work on projects with budget >1M and have published papers"
Output: {{"primary_source": "hybrid", "confidence": 0.85, "reasoning": "Needs SQL for employee/project/budget data AND KG for publication data", "detected_entities": ["employees", "projects", "papers"], "detected_predicates": ["worksOn", "budget", "authorOf"], "requires_multi_hop": true, "secondary_sources": ["sql_database", "knowledge_graph"], "intent_type": "multi_hop"}}

## Now analyze this query:

Query: "{query}"
Output:
"""
    
    def __init__(self, config: dict):
        """
        Initialize LLM detector.
        
        Args:
            config: Configuration dict with:
                - api_key: LLM API key
                - model: Model name (default: gpt-4)
                - temperature: Sampling temperature (default: 0.1)
        """
        self.config = config
        self.api_key = config.get("api_key")
        self.model = config.get("model", "gpt-4")
        self.temperature = config.get("temperature", 0.1)
        self.client = None
    
    def _get_client(self):
        """Lazy initialization of LLM client"""
        if self.client is None:
            try:
                from openai import AsyncOpenAI
                self.client = AsyncOpenAI(api_key=self.api_key)
            except ImportError:
                logger.warning("OpenAI not installed, LLM detection unavailable")
                return None
        return self.client
    
    async def detect(self, query: str) -> LLMDetection:
        """
        Perform LLM-based source detection.
        
        Args:
            query: Natural language query string
            
        Returns:
            LLMDetection with classification results
        """
        client = self._get_client()
        
        if client is None:
            return LLMDetection(
                primary_source="unknown",
                confidence=0.0,
                reasoning="LLM client unavailable",
                detected_entities=[],
                detected_predicates=[],
                requires_multi_hop=False,
                secondary_sources=[],
                intent_type="unknown",
            )
        
        prompt = self.PROMPT_TEMPLATE.format(query=query)
        
        try:
            response = await client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                response_format={"type": "json_object"},
                max_tokens=500,
            )
            
            result = json.loads(response.choices[0].message.content)
            
            logger.debug(f"LLM detection result: {result.get('primary_source')}")
            
            return LLMDetection(
                primary_source=result.get("primary_source", "unknown"),
                confidence=result.get("confidence", 0.5),
                reasoning=result.get("reasoning", ""),
                detected_entities=result.get("detected_entities", []),
                detected_predicates=result.get("detected_predicates", []),
                requires_multi_hop=result.get("requires_multi_hop", False),
                secondary_sources=result.get("secondary_sources", []),
                intent_type=result.get("intent_type", "unknown"),
            )
            
        except Exception as e:
            logger.error(f"LLM detection failed: {e}")
            return LLMDetection(
                primary_source="unknown",
                confidence=0.0,
                reasoning=f"LLM detection error: {str(e)}",
                detected_entities=[],
                detected_predicates=[],
                requires_multi_hop=False,
                secondary_sources=[],
                intent_type="unknown",
            )
