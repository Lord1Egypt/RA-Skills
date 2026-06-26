"""
HeteroMind - Task Decomposer

Breaks complex queries into executable sub-tasks.
"""

import logging
from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum

from ..classifier import FinalDecision, KnowledgeSource

logger = logging.getLogger(__name__)


class TaskType(Enum):
    """Sub-task types"""
    QUERY = "query"           # Simple query
    AGGREGATE = "aggregate"    # Aggregation
    JOIN = "join"             # Join operation
    FILTER = "filter"         # Filter operation
    TRANSFORM = "transform"    # Transform/format
    FUSE = "fuse"             # Fuse results


@dataclass
class SubTask:
    """Represents a sub-task in the execution plan"""
    id: str
    query: str
    source: str
    task_type: TaskType
    depends_on: List[str]
    context: dict
    priority: int = 0


class TaskDecomposer:
    """
    Task decomposer for complex queries.
    
    Breaks down multi-hop queries into executable sub-tasks
    with dependency tracking for proper execution ordering.
    """
    
    def __init__(self, config: dict):
        """
        Initialize decomposer.
        
        Args:
            config: Configuration dict
        """
        self.config = config
        self.max_depth = config.get("max_depth", 5)
    
    async def decompose(
        self,
        query: str,
        source_decision: FinalDecision,
    ) -> List[SubTask]:
        """
        Decompose query into sub-tasks.
        
        Args:
            query: Natural language query
            source_decision: Source detection decision
            
        Returns:
            List of SubTask objects
        """
        logger.info(f"Decomposing query: {query}")
        
        # Simple queries: single task
        if not source_decision.layer2_output.requires_multi_hop:
            return await self._create_simple_tasks(query, source_decision)
        
        # Complex queries: multi-step decomposition
        return await self._create_complex_tasks(query, source_decision)
    
    async def _create_simple_tasks(
        self,
        query: str,
        source_decision: FinalDecision,
    ) -> List[SubTask]:
        """Create simple single-step tasks"""
        tasks = []
        
        for i, source in enumerate(source_decision.selected_sources):
            task = SubTask(
                id=f"task_{i}",
                query=query,
                source=source.value,
                task_type=TaskType.QUERY,
                depends_on=[],
                context={
                    "entities": source_decision.layer2_output.detected_entities,
                    "predicates": source_decision.layer2_output.detected_predicates,
                },
                priority=i,
            )
            tasks.append(task)
        
        return tasks
    
    async def _create_complex_tasks(
        self,
        query: str,
        source_decision: FinalDecision,
    ) -> List[SubTask]:
        """Create complex multi-step tasks"""
        # In real implementation, use LLM to decompose
        # For now, return placeholder
        
        tasks = []
        
        # Example decomposition for hybrid query
        if KnowledgeSource.HYBRID in source_decision.selected_sources:
            # Task 1: SQL query
            tasks.append(SubTask(
                id="task_sql_1",
                query=query,  # Would be refined
                source="sql_database",
                task_type=TaskType.QUERY,
                depends_on=[],
                context={},
                priority=1,
            ))
            
            # Task 2: KG query (depends on SQL results)
            tasks.append(SubTask(
                id="task_kg_2",
                query=query,  # Would be refined
                source="knowledge_graph",
                task_type=TaskType.QUERY,
                depends_on=["task_sql_1"],
                context={},
                priority=2,
            ))
            
            # Task 3: Fuse results
            tasks.append(SubTask(
                id="task_fuse_3",
                query="fuse",
                source="fusion",
                task_type=TaskType.FUSE,
                depends_on=["task_sql_1", "task_kg_2"],
                context={},
                priority=3,
            ))
        
        return tasks
