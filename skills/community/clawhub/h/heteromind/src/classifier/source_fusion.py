"""
HeteroMind - Layer 4: Multi-Source Fusion

Fuses all detection layers with entity verification for final decision.
"""

import logging
from typing import Dict, List, Optional

from .models import (
    KnowledgeSource,
    RuleBasedScore,
    LLMDetection,
    SchemaMatch,
    EntityLinking,
    EntityVerification,
    FinalDecision,
)

logger = logging.getLogger(__name__)


class SourceFusion:
    """
    Layer 4: Multi-source fusion with entity verification.
    
    Combines outputs from all previous layers:
    - Layer 1: Rule-based scores (15% weight)
    - Layer 2: LLM classification (35% weight)
    - Layer 3a/3b: Schema matching (25% weight)
    - Layer 3c: Entity verification (25% weight + 30% boost)
    
    Outputs final decision with execution plan.
    """
    
    def __init__(self, config: dict):
        """
        Initialize fusion module.
        
        Args:
            config: Configuration dict with:
                - weights: Layer weights (rule, llm, schema, verification)
                - thresholds: Confidence thresholds
                - verification_boost: Score boost for verified entities
        """
        self.config = config
        
        self.weights = config.get("weights", {
            "rule_based": 0.15,
            "llm_based": 0.35,
            "schema_based": 0.25,
            "verification": 0.25,
        })
        
        self.thresholds = config.get("thresholds", {
            "high_confidence": 0.8,
            "medium_confidence": 0.5,
            "low_confidence": 0.3,
        })
        
        self.verification_boost = config.get("verification_boost", 0.3)
    
    def fuse(
        self,
        rule_scores: RuleBasedScore,
        llm_detection: LLMDetection,
        sql_match: Optional[SchemaMatch],
        kg_linking: Optional[EntityLinking],
        entity_verification: Optional[EntityVerification],
    ) -> FinalDecision:
        """
        Fuse all detection layers into final decision.
        
        Args:
            rule_scores: Layer 1 output
            llm_detection: Layer 2 output
            sql_match: Layer 3a output
            kg_linking: Layer 3b output
            entity_verification: Layer 3c output
            
        Returns:
            FinalDecision with fused results
        """
        aggregated = {}
        reasoning_parts = []
        
        for source in ["sql_database", "knowledge_graph", "table_file", "document_store"]:
            scores = []
            weights = []
            
            # Layer 1: Rule-based score
            if source in rule_scores.source_scores:
                scores.append(rule_scores.source_scores[source])
                weights.append(self.weights["rule_based"])
            
            # Layer 2: LLM score
            llm_score = self._calculate_llm_score(llm_detection, source)
            if llm_score > 0:
                scores.append(llm_score)
                weights.append(self.weights["llm_based"])
            
            # Layer 3a/3b: Schema-based score
            schema_score = self._calculate_schema_score(
                source, sql_match, kg_linking
            )
            if schema_score > 0:
                scores.append(schema_score)
                weights.append(self.weights["schema_based"])
            
            # Layer 3c: Verification score (critical!)
            verification_score = self._calculate_verification_score(
                source, entity_verification
            )
            if verification_score > 0:
                boosted_score = min(1.0, verification_score * (1 + self.verification_boost))
                scores.append(boosted_score)
                weights.append(self.weights["verification"])
                reasoning_parts.append(
                    f"{source}: verification={verification_score:.2f}"
                )
            
            if scores:
                total_weight = sum(weights)
                aggregated[source] = sum(s * w for s, w in zip(scores, weights)) / total_weight
            else:
                aggregated[source] = 0.0
        
        max_score = max(aggregated.values()) if aggregated else 0
        threshold = self.thresholds["low_confidence"]
        
        selected_sources = [
            KnowledgeSource(src) for src, score in aggregated.items()
            if score >= threshold
        ]
        
        if len(selected_sources) > 1:
            final_source = KnowledgeSource.HYBRID
        elif selected_sources:
            final_source = selected_sources[0]
        else:
            final_source = KnowledgeSource.UNKNOWN
        
        execution_plan = self._generate_execution_plan(
            selected_sources, llm_detection, entity_verification
        )
        
        reasoning = self._generate_reasoning(
            aggregated, llm_detection, entity_verification, reasoning_parts
        )
        
        logger.info(f"Fusion decision: {final_source.value} (confidence: {max_score:.2f})")
        
        return FinalDecision(
            primary_source=final_source,
            confidence=max_score,
            all_scores=aggregated,
            selected_sources=selected_sources,
            reasoning=reasoning,
            layer1_output=rule_scores,
            layer2_output=llm_detection,
            layer3_sql_output=sql_match,
            layer3_kg_output=kg_linking,
            layer3_verification=entity_verification,
            execution_plan=execution_plan,
        )
    
    def _calculate_llm_score(self, llm: LLMDetection, source: str) -> float:
        """Calculate LLM-based score for a source"""
        if llm.primary_source == source:
            return llm.confidence
        elif source in llm.secondary_sources:
            return llm.confidence * 0.7
        return 0.0
    
    def _calculate_schema_score(
        self,
        source: str,
        sql_match: Optional[SchemaMatch],
        kg_linking: Optional[EntityLinking],
    ) -> float:
        """Calculate schema-based score for a source"""
        if source == "sql_database" and sql_match:
            return sql_match.confidence
        elif source == "knowledge_graph" and kg_linking:
            return kg_linking.confidence
        return 0.0
    
    def _calculate_verification_score(
        self,
        source: str,
        verification: Optional[EntityVerification],
    ) -> float:
        """Calculate verification-based score for a source"""
        if verification is None:
            return 0.0
        
        if source == "sql_database":
            return verification.sql_verification_score
        elif source == "knowledge_graph":
            return verification.kg_verification_score
        elif source == "table_file":
            return verification.table_verification_score
        return 0.0
    
    def _generate_execution_plan(
        self,
        sources: List[KnowledgeSource],
        llm: LLMDetection,
        verification: Optional[EntityVerification],
    ) -> List[Dict]:
        """Generate execution plan based on selected sources"""
        plan = []
        
        for i, source in enumerate(sources):
            step = {
                "step": i + 1,
                "source": source.value,
                "is_parallel": len(sources) > 1,
                "depends_on": [],
                "entities": llm.detected_entities,
                "predicates": llm.detected_predicates,
            }
            
            if verification:
                if source == KnowledgeSource.SQL_DATABASE:
                    step["verified_entities"] = verification.entities_found_in_sql
                elif source == KnowledgeSource.KNOWLEDGE_GRAPH:
                    step["verified_entities"] = verification.entities_found_in_kg
                elif source == KnowledgeSource.TABLE_FILE:
                    step["verified_entities"] = verification.entities_found_in_tables
            
            plan.append(step)
        
        return plan
    
    def _generate_reasoning(
        self,
        aggregated: Dict[str, float],
        llm: LLMDetection,
        verification: Optional[EntityVerification],
        reasoning_parts: List[str],
    ) -> str:
        """Generate human-readable reasoning"""
        parts = []
        
        sorted_sources = sorted(aggregated.items(), key=lambda x: x[1], reverse=True)
        if sorted_sources:
            top = sorted_sources[0]
            parts.append(f"Primary: {top[0]} ({top[1]:.2f})")
            if len(sorted_sources) > 1 and sorted_sources[1][1] > 0.3:
                parts.append(f"Secondary: {sorted_sources[1][0]} ({sorted_sources[1][1]:.2f})")
        
        if llm.reasoning:
            parts.append(f"LLM: {llm.reasoning}")
        
        if verification:
            verified_count = (
                len(verification.entities_found_in_sql) +
                len(verification.entities_found_in_kg) +
                len(verification.entities_found_in_tables)
            )
            parts.append(f"Verified: {verified_count} entities")
        
        parts.extend(reasoning_parts)
        
        return " | ".join(parts)
