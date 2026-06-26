"""
HeteroMind - Answer Generator

Generates natural language answers from fused results.
"""

import logging
from typing import Dict, Optional

from ..classifier import FinalDecision
from ..fusion.result_fusion import FusedResult

logger = logging.getLogger(__name__)


class AnswerGenerator:
    """
    Answer generator for query results.
    
    Converts structured fused results into natural language responses
    with proper citations and uncertainty handling.
    """
    
    def __init__(self, config: dict):
        """
        Initialize generator.
        
        Args:
            config: Configuration dict with:
                - model: LLM model for generation
                - include_citations: Whether to include source citations
                - handle_uncertainty: How to handle uncertain results
        """
        self.config = config
        self.model = config.get("model", "gpt-4")
        self.include_citations = config.get("include_citations", True)
        self.handle_uncertainty = config.get("handle_uncertainty", "transparent")
    
    async def generate(
        self,
        fused_result: FusedResult,
        query: str,
        source_decision: FinalDecision,
    ) -> str:
        """
        Generate natural language answer.
        
        Args:
            fused_result: Fused result from multiple sources
            query: Original query
            source_decision: Source detection decision
            
        Returns:
            Natural language answer
        """
        logger.info("Generating answer")
        
        if not fused_result.success or fused_result.data is None:
            return self._generate_error_response(query, source_decision)
        
        # Generate answer based on result type
        if isinstance(fused_result.data, (list, tuple)):
            answer = self._generate_list_answer(fused_result, query)
        elif isinstance(fused_result.data, dict):
            answer = self._generate_dict_answer(fused_result, query)
        else:
            answer = self._generate_scalar_answer(fused_result, query)
        
        # Add citations if enabled
        if self.include_citations and source_decision.selected_sources:
            answer += self._generate_citations(source_decision)
        
        return answer
    
    def _generate_list_answer(self, result: FusedResult, query: str) -> str:
        """Generate answer for list results"""
        data = result.data
        
        if not data:
            return "No results found."
        
        # Format as list
        items = "\n".join(f"- {item}" for item in data[:10])  # Limit to 10
        
        answer = f"Found {len(data)} results:\n{items}"
        
        return answer
    
    def _generate_dict_answer(self, result: FusedResult, query: str) -> str:
        """Generate answer for dictionary results"""
        data = result.data
        
        # Format key-value pairs
        items = "\n".join(f"- {k}: {v}" for k, v in data.items())
        
        answer = f"Results:\n{items}"
        
        return answer
    
    def _generate_scalar_answer(self, result: FusedResult, query: str) -> str:
        """Generate answer for scalar results"""
        data = result.data
        
        answer = f"Answer: {data}"
        
        return answer
    
    def _generate_error_response(self, query: str, decision: FinalDecision) -> str:
        """Generate error response"""
        return (
            "I wasn't able to find an answer to your question. "
            "This could be because:\n"
            "- The data doesn't exist in the available sources\n"
            "- The query needs clarification\n"
            "- There was a technical issue\n\n"
            "Please try rephrasing your question or providing more context."
        )
    
    def _generate_citations(self, decision: FinalDecision) -> str:
        """Generate source citations"""
        sources = [s.value for s in decision.selected_sources]
        
        if not sources:
            return ""
        
        citations = "\n\nSources:\n"
        for source in sources:
            citations += f"- {source}\n"
        
        return citations
