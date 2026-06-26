"""
HeteroMind - Main Orchestrator

Unified heterogeneous knowledge QA system orchestrator.
Coordinates source detection, task decomposition, engine execution,
result fusion, and answer generation.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from .classifier import (
    SourceDetectorOrchestrator,
    FinalDecision,
    KnowledgeSource,
)
from .decomposer.task_decomposer import TaskDecomposer, SubTask
from .engines.base import BaseEngine, QueryResult
from .fusion.result_fusion import ResultFusion, FusedResult
from .generator.answer_generator import AnswerGenerator

logger = logging.getLogger(__name__)


@dataclass
class QueryContext:
    """Context for a query execution"""
    query: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Dict[str, Any] = None


@dataclass
class QueryResponse:
    """Final query response"""
    answer: str
    sources: List[str]
    confidence: float
    execution_plan: List[Dict]
    raw_results: List[QueryResult]


class HeteroMindOrchestrator:
    """
    Main HeteroMind orchestrator.
    
    Provides unified natural language QA interface over heterogeneous
    knowledge sources (SQL databases, knowledge graphs, table files, documents).
    
    Workflow:
    1. Source Detection - Determine which knowledge source(s) to query
    2. Task Decomposition - Break complex queries into sub-tasks
    3. Engine Execution - Execute sub-tasks on appropriate engines
    4. Result Fusion - Combine results from multiple sources
    5. Answer Generation - Generate natural language response
    """
    
    def __init__(self, config: dict):
        """
        Initialize HeteroMind orchestrator.
        
        Args:
            config: Configuration dict with:
                - source_detection: Source detector config
                - engines: Engine configurations (sql, sparql, table_qa)
                - fusion: Result fusion config
                - generator: Answer generator config
        """
        self.config = config
        
        # Initialize source detector
        self.source_detector = SourceDetectorOrchestrator(
            config.get("source_detection", {})
        )
        
        # Initialize task decomposer
        self.task_decomposer = TaskDecomposer(
            config.get("decomposer", {})
        )
        
        # Initialize engine registry
        self.engines = self._initialize_engines(config.get("engines", {}))
        
        # Initialize result fusion
        self.result_fusion = ResultFusion(
            config.get("fusion", {})
        )
        
        # Initialize answer generator
        self.answer_generator = AnswerGenerator(
            config.get("generator", {})
        )
        
        logger.info("HeteroMind orchestrator initialized")
    
    def _initialize_engines(self, engine_config: dict) -> Dict[str, List[BaseEngine]]:
        """Initialize engine registry from config"""
        engines = {
            "sql_database": [],
            "knowledge_graph": [],
            "table_file": [],
            "document_store": [],
        }
        
        # SQL engines
        for sql_engine_config in engine_config.get("sql", []):
            if sql_engine_config.get("enabled", True):
                engine = self._load_engine("sql", sql_engine_config)
                if engine:
                    engines["sql_database"].append(engine)
        
        # SPARQL engines
        for sparql_engine_config in engine_config.get("sparql", []):
            if sparql_engine_config.get("enabled", True):
                engine = self._load_engine("sparql", sparql_engine_config)
                if engine:
                    engines["knowledge_graph"].append(engine)
        
        # Table QA engines
        for table_engine_config in engine_config.get("table_qa", []):
            if table_engine_config.get("enabled", True):
                engine = self._load_engine("table_qa", table_engine_config)
                if engine:
                    engines["table_file"].append(engine)
        
        logger.info(
            f"Initialized engines: "
            f"SQL={len(engines['sql_database'])}, "
            f"SPARQL={len(engines['knowledge_graph'])}, "
            f"Table={len(engines['table_file'])}"
        )
        
        return engines
    
    def _load_engine(self, engine_type: str, config: dict) -> Optional[BaseEngine]:
        """Load a single engine from config"""
        # Dynamic engine loading based on type
        # In real implementation, this would import and instantiate engine classes
        
        logger.debug(f"Loading engine: {engine_type}/{config.get('name')}")
        
        # Placeholder - in real implementation:
        # if engine_type == "sql" and config["name"] == "deepeye":
        #     from .engines.sql.deepeye import DeepEyeEngine
        #     return DeepEyeEngine(config)
        
        return None
    
    async def query(self, query: str, context: Optional[QueryContext] = None) -> QueryResponse:
        """
        Process a natural language query.
        
        Main entry point for HeteroMind QA system.
        
        Args:
            query: Natural language query string
            context: Optional query context (user_id, session_id, metadata)
            
        Returns:
            QueryResponse with answer and metadata
        """
        logger.info(f"Processing query: {query}")
        
        if context is None:
            context = QueryContext(query=query)
        
        # Step 1: Source Detection
        logger.info("Step 1: Detecting knowledge sources")
        source_decision = await self.source_detector.detect(query)
        
        if source_decision.primary_source == KnowledgeSource.UNKNOWN:
            return await self._handle_unknown_source(query)
        
        # Step 2: Task Decomposition
        logger.info("Step 2: Decomposing task")
        subtasks = await self.task_decomposer.decompose(
            query=query,
            source_decision=source_decision,
        )
        
        # Step 3: Engine Execution
        logger.info("Step 3: Executing subtasks")
        results = await self._execute_subtasks(subtasks, source_decision)
        
        # Step 4: Result Fusion
        logger.info("Step 4: Fusing results")
        fused_result = await self.result_fusion.fuse(
            results=results,
            source_decision=source_decision,
        )
        
        # Step 5: Answer Generation
        logger.info("Step 5: Generating answer")
        answer = await self.answer_generator.generate(
            fused_result=fused_result,
            query=query,
            source_decision=source_decision,
        )
        
        # Build response
        response = QueryResponse(
            answer=answer,
            sources=[s.value for s in source_decision.selected_sources],
            confidence=source_decision.confidence,
            execution_plan=source_decision.execution_plan,
            raw_results=results,
        )
        
        logger.info(f"Query complete: {answer[:100]}...")
        
        return response
    
    async def _execute_subtasks(
        self,
        subtasks: List[SubTask],
        source_decision: FinalDecision,
    ) -> List[QueryResult]:
        """Execute subtasks on appropriate engines"""
        results = []
        
        # Group subtasks by source for parallel execution
        by_source = {}
        for subtask in subtasks:
            source = subtask.source
            by_source.setdefault(source, []).append(subtask)
        
        # Execute subtasks for each source
        tasks = []
        for source, source_subtasks in by_source.items():
            engines = self.engines.get(source, [])
            
            if not engines:
                logger.warning(f"No engines available for source: {source}")
                continue
            
            # Select best engine for this subtask
            engine = self._select_engine(engines, source_subtasks[0])
            
            # Execute subtask
            for subtask in source_subtasks:
                task = asyncio.create_task(engine.execute(
                    query=subtask.query,
                    context=subtask.context,
                ))
                tasks.append(task)
        
        # Wait for all tasks
        if tasks:
            completed = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in completed:
                if isinstance(result, Exception):
                    logger.error(f"Subtask execution failed: {result}")
                else:
                    results.append(result)
        
        return results
    
    def _select_engine(
        self,
        engines: List[BaseEngine],
        subtask: SubTask,
    ) -> BaseEngine:
        """Select best engine for a subtask"""
        if not engines:
            raise ValueError("No engines available")
        
        if len(engines) == 1:
            return engines[0]
        
        # Select engine with highest confidence for this subtask
        best_engine = max(engines, key=lambda e: e.get_confidence(
            subtask.query,
            subtask.context,
        ))
        
        logger.debug(f"Selected engine: {best_engine.__class__.__name__}")
        
        return best_engine
    
    async def _handle_unknown_source(self, query: str) -> QueryResponse:
        """Handle case where source detection fails"""
        answer = (
            "I'm not sure which data source to query for this question. "
            "Could you please clarify if you're asking about:\n"
            "- Database records (employees, projects, sales, etc.)\n"
            "- Knowledge graph (entities, relationships, facts)\n"
            "- A specific table/file (CSV, Excel)\n"
            "- Documents (reports, contracts, articles)"
        )
        
        return QueryResponse(
            answer=answer,
            sources=[],
            confidence=0.0,
            execution_plan=[],
            raw_results=[],
        )
    
    async def health_check(self) -> Dict[str, Any]:
        """Check health of all components"""
        health = {
            "status": "healthy",
            "components": {
                "source_detector": "ok",
                "task_decomposer": "ok",
                "engines": {},
                "result_fusion": "ok",
                "answer_generator": "ok",
            },
        }
        
        # Check engines
        for source, engines in self.engines.items():
            health["components"]["engines"][source] = len(engines)
        
        return health


# =============================================================================
# Convenience Functions
# =============================================================================

async def ask(query: str, config: Optional[dict] = None) -> str:
    """
    Simple convenience function to ask a question.
    
    Args:
        query: Natural language query
        config: Optional configuration dict
        
    Returns:
        Natural language answer
    """
    if config is None:
        config = {}
    
    orchestrator = HeteroMindOrchestrator(config)
    response = await orchestrator.query(query)
    
    return response.answer


# =============================================================================
# Example Usage
# =============================================================================

if __name__ == "__main__":
    # Example configuration
    config = {
        "source_detection": {
            "layer2": {
                "api_key": "your-api-key",
                "model": "gpt-4",
            },
            "layer3": {
                "kg_endpoints": [
                    {"name": "dbpedia", "url": "https://dbpedia.org/sparql"}
                ],
            },
            "layer4": {
                "weights": {
                    "rule_based": 0.15,
                    "llm_based": 0.35,
                    "schema_based": 0.25,
                    "verification": 0.25,
                },
            },
        },
        "engines": {
            "sql": [
                {"name": "deepeye", "enabled": True},
                {"name": "din_sql", "enabled": True},
            ],
            "sparql": [
                {"name": "gpt_sparql", "enabled": True},
            ],
            "table_qa": [
                {"name": "pandasai", "enabled": True},
            ],
        },
    }
    
    # Run query
    async def main():
        orchestrator = HeteroMindOrchestrator(config)
        
        query = "How many employees are in the sales department?"
        response = await orchestrator.query(query)
        
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}")
        print(f"Answer: {response.answer}")
        print(f"\nSources: {response.sources}")
        print(f"Confidence: {response.confidence:.2f}")
    
    asyncio.run(main())
