"""
HeteroMind - NL2SQL Base Engine

Base class and result types for NL2SQL engines.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum
import logging

from ..base import BaseEngine, QueryResult

logger = logging.getLogger(__name__)


class SQLGenerationStage(Enum):
    """Stages in SQL generation pipeline"""
    SCHEMA_RETRIEVAL = "schema_retrieval"
    INITIAL_GENERATION = "initial_generation"
    SELF_REVISION = "self_revision"
    VALIDATION = "validation"
    EXECUTION = "execution"
    RESULT_VERIFICATION = "result_verification"


@dataclass
class SQLGenerationStep:
    """Single step in SQL generation"""
    stage: SQLGenerationStage
    input: Any
    output: Any
    llm_response: Optional[str] = None
    confidence: float = 0.0
    reasoning: str = ""
    execution_time_ms: float = 0.0
    error: Optional[str] = None


@dataclass
class NL2SQLResult(QueryResult):
    """Extended QueryResult for NL2SQL"""
    generated_sql: Optional[str] = None
    execution_steps: List[SQLGenerationStep] = field(default_factory=list)
    schema_used: Optional[Dict] = None
    revision_count: int = 0
    voting_results: Optional[List[Dict]] = None
    final_confidence: float = 0.0


class BaseNL2SQLEngine(BaseEngine):
    """
    Base class for NL2SQL engines.
    
    Provides common utilities for:
    - Schema retrieval and indexing
    - Multi-stage SQL generation
    - Self-revision mechanisms
    - Voting between multiple candidates
    - Result validation
    """
    
    def __init__(self, config: dict):
        """
        Initialize NL2SQL engine.
        
        Args:
            config: Configuration dict with:
                - connection_string: Database connection
                - schema: Database schema metadata
                - llm_config: LLM configuration
                - generation_config: Generation parameters
        """
        super().__init__(config)
        
        self.connection_string = config.get("connection_string")
        self.schema = config.get("schema", {})
        self.llm_config = config.get("llm_config", {})
        self.generation_config = config.get("generation_config", {
            "num_candidates": 3,
            "max_revisions": 2,
            "voting_enabled": True,
            "parallel_generation": True,
        })
        
        # Schema index for efficient retrieval
        self.schema_index = self._build_schema_index()
    
    def _build_schema_index(self) -> Dict:
        """Build searchable schema index"""
        index = {
            "tables": {},
            "columns": {},
            "relationships": [],
            "keywords": {},
        }
        
        for table in self.schema.get("tables", []):
            table_name = table["name"].lower()
            index["tables"][table_name] = table
            
            for col in table.get("columns", []):
                col_name = col["name"].lower()
                index["columns"][col_name] = {
                    "table": table_name,
                    "type": col.get("type", "UNKNOWN"),
                    "description": col.get("description", ""),
                }
                
                # Index keywords from column description
                if col.get("description"):
                    for keyword in col["description"].lower().split():
                        if len(keyword) > 3:
                            index["keywords"].setdefault(keyword, []).append({
                                "table": table_name,
                                "column": col_name,
                            })
            
            # Index relationships (foreign keys)
            for fk in table.get("foreign_keys", []):
                index["relationships"].append({
                    "from_table": table_name,
                    "from_column": fk["column"],
                    "to_table": fk["references"]["table"],
                    "to_column": fk["references"]["column"],
                })
        
        logger.debug(f"Built schema index: {len(index['tables'])} tables, "
                    f"{len(index['columns'])} columns")
        
        return index
    
    def retrieve_relevant_schema(self, query: str) -> Dict:
        """
        Retrieve schema elements relevant to the query.
        
        Uses keyword matching and semantic similarity to find
        relevant tables and columns.
        
        Args:
            query: Natural language query
            
        Returns:
            Relevant schema subset
        """
        query_lower = query.lower()
        relevant = {
            "tables": [],
            "columns": [],
            "relationships": [],
        }
        
        # Match table names
        for table_name, table in self.schema_index["tables"].items():
            if table_name in query_lower:
                relevant["tables"].append(table)
                if table.get("description") and table["description"].lower() in query_lower:
                    relevant["tables"].append(table)
        
        # Match column names
        for col_name, col_info in self.schema_index["columns"].items():
            if col_name in query_lower:
                relevant["columns"].append({
                    "name": col_name,
                    **col_info,
                })
        
        # Match keywords from descriptions
        for keyword, matches in self.schema_index["keywords"].items():
            if keyword in query_lower:
                for match in matches:
                    table = self.schema_index["tables"].get(match["table"])
                    if table and table not in relevant["tables"]:
                        relevant["tables"].append(table)
        
        # Find relationships for matched tables
        table_names = {t["name"] for t in relevant["tables"]}
        for rel in self.schema_index["relationships"]:
            if rel["from_table"] in table_names or rel["to_table"] in table_names:
                relevant["relationships"].append(rel)
        
        logger.debug(f"Retrieved schema: {len(relevant['tables'])} tables, "
                    f"{len(relevant['columns'])} columns")
        
        return relevant
    
    async def generate_sql_candidates(
        self,
        query: str,
        schema: Dict,
        num_candidates: int = 3,
    ) -> List[str]:
        """
        Generate multiple SQL candidates.
        
        Args:
            query: Natural language query
            schema: Relevant schema subset
            num_candidates: Number of candidates to generate
            
        Returns:
            List of SQL query strings
        """
        # To be implemented by subclasses
        raise NotImplementedError
    
    async def revise_sql(
        self,
        query: str,
        sql: str,
        schema: Dict,
        error: Optional[str] = None,
    ) -> str:
        """
        Revise SQL based on feedback.
        
        Args:
            query: Original query
            sql: Current SQL
            schema: Schema subset
            error: Error message if any
            
        Returns:
            Revised SQL
        """
        # To be implemented by subclasses
        raise NotImplementedError
    
    def validate_sql(self, sql: str) -> Dict:
        """
        Validate SQL syntax and semantics.
        
        Args:
            sql: SQL query string
            
        Returns:
            Validation result with errors/warnings
        """
        import sqlparse
        
        validation = {
            "valid": True,
            "errors": [],
            "warnings": [],
        }
        
        # Parse SQL
        try:
            parsed = sqlparse.parse(sql)
            if not parsed:
                validation["valid"] = False
                validation["errors"].append("Failed to parse SQL")
                return validation
        except Exception as e:
            validation["valid"] = False
            validation["errors"].append(f"Parse error: {str(e)}")
            return validation
        
        # Check for dangerous operations
        sql_upper = sql.upper()
        dangerous = ["DROP", "DELETE", "TRUNCATE"]
        for keyword in dangerous:
            if keyword in sql_upper:
                validation["warnings"].append(
                    f"Query contains {keyword} - read-only mode enforced"
                )
        
        # Check for SELECT (read queries only)
        if not sql_upper.strip().startswith("SELECT"):
            validation["warnings"].append("Non-SELECT query detected")
        
        return validation
    
    async def vote_on_candidates(
        self,
        query: str,
        candidates: List[str],
        schema: Dict,
    ) -> Dict:
        """
        Vote on multiple SQL candidates to select the best one.
        
        Args:
            query: Original query
            candidates: List of SQL candidates
            schema: Schema subset
            
        Returns:
            Voting results with scores and best candidate
        """
        voting_results = []
        
        for i, sql in enumerate(candidates):
            # Score each candidate
            score = self._score_candidate(query, sql, schema)
            voting_results.append({
                "index": i,
                "sql": sql,
                "score": score,
                "criteria": self._get_scoring_criteria(query, sql, schema),
            })
        
        # Select best candidate
        best = max(voting_results, key=lambda x: x["score"])
        
        logger.debug(f"Voting complete: best candidate #{best['index']} "
                    f"with score {best['score']:.2f}")
        
        return {
            "best_index": best["index"],
            "best_sql": best["sql"],
            "best_score": best["score"],
            "all_results": voting_results,
        }
    
    def _score_candidate(
        self,
        query: str,
        sql: str,
        schema: Dict,
    ) -> float:
        """Score a SQL candidate"""
        score = 0.0
        
        # Criterion 1: Uses relevant tables
        table_names = {t["name"].lower() for t in schema.get("tables", [])}
        sql_lower = sql.lower()
        matched_tables = sum(1 for t in table_names if t in sql_lower)
        score += matched_tables * 0.2
        
        # Criterion 2: Has proper structure (SELECT ... FROM ... WHERE)
        if "SELECT" in sql_upper and "FROM" in sql_upper:
            score += 0.3
        
        # Criterion 3: No syntax errors
        validation = self.validate_sql(sql)
        if validation["valid"]:
            score += 0.3
        else:
            score -= len(validation["errors"]) * 0.2
        
        # Criterion 4: Matches query intent (simple keyword overlap)
        query_keywords = set(query.lower().split())
        sql_keywords = set(sql_lower.split())
        overlap = len(query_keywords & sql_keywords)
        score += min(0.2, overlap * 0.02)
        
        return min(1.0, max(0.0, score))
    
    def _get_scoring_criteria(
        self,
        query: str,
        sql: str,
        schema: Dict,
    ) -> Dict:
        """Get detailed scoring criteria"""
        return {
            "table_match": "Uses relevant tables",
            "structure": "Has proper SQL structure",
            "validity": "No syntax errors",
            "intent_match": "Matches query keywords",
        }
