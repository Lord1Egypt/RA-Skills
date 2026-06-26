"""
HeteroMind - Result Fusion

Fuses results from multiple knowledge sources.
"""

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..classifier import FinalDecision, KnowledgeSource
from ..engines.base import QueryResult

logger = logging.getLogger(__name__)


@dataclass
class FusedResult:
    """Fused result from multiple sources"""
    data: Any
    success: bool
    sources: List[str]
    confidence: float
    conflicts: List[Dict]
    fusion_method: str


class ResultFusion:
    """
    Result fusion for multi-source queries.
    
    Combines results from multiple knowledge sources,
    handles conflicts, and produces unified output.
    """
    
    def __init__(self, config: dict):
        """
        Initialize fusion module.
        
        Args:
            config: Configuration dict
        """
        self.config = config
        self.conflict_strategy = config.get("conflict_strategy", "weighted")
    
    async def fuse(
        self,
        results: List[QueryResult],
        source_decision: FinalDecision,
    ) -> FusedResult:
        """
        Fuse results from multiple sources.
        
        Args:
            results: List of QueryResult from engines
            source_decision: Source detection decision
            
        Returns:
            FusedResult
        """
        logger.info(f"Fusing {len(results)} results")
        
        if not results:
            return FusedResult(
                data=None,
                success=False,
                sources=[],
                confidence=0.0,
                conflicts=[],
                fusion_method="none",
            )
        
        # Single source: no fusion needed
        if len(results) == 1:
            return FusedResult(
                data=results[0].data,
                success=results[0].success,
                sources=[results[0].engine],
                confidence=results[0].confidence,
                conflicts=[],
                fusion_method="single",
            )
        
        # Multiple sources: fuse results
        fused_data = self._combine_data(results)
        conflicts = self._detect_conflicts(results)
        confidence = self._calculate_confidence(results)
        
        sources = list(set(r.engine for r in results))
        
        return FusedResult(
            data=fused_data,
            success=True,
            sources=sources,
            confidence=confidence,
            conflicts=conflicts,
            fusion_method=self.conflict_strategy,
        )
    
    def _combine_data(self, results: List[QueryResult]) -> Any:
        """Combine data from multiple results"""
        # Simple concatenation for now
        # In real implementation, implement smart fusion logic
        
        combined = []
        for result in results:
            if result.data:
                if isinstance(result.data, list):
                    combined.extend(result.data)
                else:
                    combined.append(result.data)
        
        return combined
    
    def _detect_conflicts(self, results: List[QueryResult]) -> List[Dict]:
        """Detect conflicts between results"""
        conflicts = []
        
        # Simple conflict detection
        # In real implementation, implement sophisticated conflict detection
        
        return conflicts
    
    def _calculate_confidence(self, results: List[QueryResult]) -> float:
        """Calculate combined confidence score"""
        if not results:
            return 0.0
        
        # Average confidence
        total = sum(r.confidence for r in results)
        return total / len(results)
