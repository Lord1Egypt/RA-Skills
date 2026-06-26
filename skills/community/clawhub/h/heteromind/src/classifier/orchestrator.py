"""
HeteroMind - Source Detector Orchestrator

Main orchestrator that coordinates all 4 layers of source detection.
"""

import logging
from typing import Optional

from .models import (
    FinalDecision,
    SchemaMatch,
    EntityLinking,
    EntityVerification,
    DatabaseSchema,
)
from .rule_detector import RuleBasedDetector
from .llm_detector import LLMSourceDetector
from .sql_schema_matcher import SQLSchemaMatcher
from .kg_entity_linker import KGEntityLinker
from .entity_verifier import EntityRetrievalVerifier
from .source_fusion import SourceFusion

logger = logging.getLogger(__name__)


class SourceDetectorOrchestrator:
    """
    Main orchestrator for knowledge source detection.
    
    Coordinates all 4 layers:
    1. Rule-based pre-filter (fast keyword/pattern matching)
    2. LLM-based semantic classification
    3. Schema-aware detection (SQL schema + KG entity linking + verification)
    4. Multi-source fusion with entity verification
    
    Provides unified async interface for source detection.
    """
    
    def __init__(self, config: dict):
        """
        Initialize orchestrator.
        
        Args:
            config: Configuration dict with:
                - layer1: Rule-based config (optional, uses defaults)
                - layer2: LLM config (api_key, model, temperature)
                - layer3: Schema/KG config (schemas, kg_endpoints, table_paths)
                - layer4: Fusion config (weights, thresholds, verification_boost)
        """
        self.config = config
        
        # Layer 1: Rule-based (always available)
        self.layer1 = RuleBasedDetector()
        
        # Layer 2: LLM-based
        self.layer2 = LLMSourceDetector(config.get("layer2", {}))
        
        # Layer 3: Schema/KG/Verification
        self.layer3_sql: Optional[SQLSchemaMatcher] = None
        self.layer3_kg: Optional[KGEntityLinker] = None
        self.layer3_verification: Optional[EntityRetrievalVerifier] = None
        
        layer3_config = config.get("layer3", {})
        
        if "schemas" in layer3_config:
            self.layer3_sql = SQLSchemaMatcher(layer3_config["schemas"])
        
        if "kg_endpoints" in layer3_config:
            self.layer3_kg = KGEntityLinker(layer3_config)
            self.layer3_verification = EntityRetrievalVerifier(layer3_config)
        
        # Layer 4: Fusion
        self.layer4 = SourceFusion(config.get("layer4", {}))
    
    async def detect(self, query: str) -> FinalDecision:
        """
        Detect knowledge source(s) for a query.
        
        Executes all 4 layers in sequence and returns fused decision.
        
        Args:
            query: Natural language query string
            
        Returns:
            FinalDecision with complete detection results
        """
        logger.info(f"Detecting source for query: {query}")
        
        # Layer 1: Rule-based (fast, synchronous)
        rule_scores = self.layer1.detect(query)
        logger.debug(
            f"Layer 1 complete: {rule_scores.source_scores}"
        )
        
        # Layer 2: LLM-based (async)
        llm_detection = await self.layer2.detect(query)
        logger.debug(f"Layer 2 complete: {llm_detection.primary_source}")
        
        # Layer 3: Schema/KG/Verification (async)
        sql_match: Optional[SchemaMatch] = None
        kg_linking: Optional[EntityLinking] = None
        entity_verification: Optional[EntityVerification] = None
        
        if self.layer3_sql:
            sql_match = self.layer3_sql.match_query(query)
            logger.debug(f"Layer 3a (SQL) complete: {sql_match.confidence:.2f}")
        
        if self.layer3_kg:
            kg_linking = await self.layer3_kg.link_query(query)
            logger.debug(f"Layer 3b (KG) complete: {kg_linking.confidence:.2f}")
        
        if self.layer3_verification:
            entity_verification = await self.layer3_verification.verify_entities(
                llm_detection.detected_entities,
                llm_detection.detected_predicates,
            )
            logger.debug(f"Layer 3c (Verification) complete")
        
        # Layer 4: Fusion
        final_decision = self.layer4.fuse(
            rule_scores=rule_scores,
            llm_detection=llm_detection,
            sql_match=sql_match,
            kg_linking=kg_linking,
            entity_verification=entity_verification,
        )
        
        logger.info(
            f"Final decision: {final_decision.primary_source.value} "
            f"(confidence: {final_decision.confidence:.2f})"
        )
        
        return final_decision
    
    async def detect_with_fallback(self, query: str) -> FinalDecision:
        """
        Detect with fallback for missing layers.
        
        If LLM is unavailable, relies more heavily on rule-based detection.
        If schema/KG not configured, skips those layers.
        
        Args:
            query: Natural language query string
            
        Returns:
            FinalDecision with available layer outputs
        """
        return await self.detect(query)
