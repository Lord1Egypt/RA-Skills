"""
HeteroMind - Engine Base Classes

Abstract base classes for knowledge source engines.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class QueryResult:
    """Result from engine query execution"""
    data: Any
    success: bool
    engine: str
    query: str
    execution_time_ms: float
    confidence: float
    error: Optional[str] = None
    metadata: Dict[str, Any] = None


class BaseEngine(ABC):
    """
    Abstract base class for all knowledge source engines.
    
    All engine implementations (SQL, SPARQL, Table QA) must inherit
    from this class and implement the required methods.
    """
    
    def __init__(self, config: dict):
        """
        Initialize engine.
        
        Args:
            config: Engine-specific configuration
                - name: Engine name
                - enabled: Whether engine is enabled
                - llm_config: LLM configuration (optional, can be overridden per-call)
                    - model: Model name (e.g., "gpt-4", "deepseek-chat", "claude-3")
                    - api_key: API key for LLM provider
                    - base_url: API base URL (optional, for custom endpoints)
        """
        self.config = config
        self.name = config.get("name", "unknown")
        self.enabled = config.get("enabled", True)
        
        # Default LLM configuration (can be overridden per-call)
        self.llm_config = config.get("llm_config", {})
    
    @abstractmethod
    async def execute(
        self,
        query: str,
        context: dict,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> QueryResult:
        """
        Execute a query.
        
        Args:
            query: Query string (SQL, SPARQL, or natural language)
            context: Execution context (connection, schema, etc.)
            model: Model name to use (overrides config, e.g., "gpt-4", "deepseek-chat", "claude-3")
            api_key: API key to use (overrides config)
            
        Returns:
            QueryResult with data and metadata
        """
        pass
    
    @abstractmethod
    def get_confidence(self, query: str, context: dict) -> float:
        """
        Get confidence score for executing this query.
        
        Args:
            query: Query string
            context: Execution context
            
        Returns:
            Confidence score 0.0-1.0
        """
        pass
    
    def validate_result(self, result: QueryResult) -> bool:
        """
        Validate query result.
        
        Args:
            result: QueryResult to validate
            
        Returns:
            True if result is valid
        """
        if not result.success:
            return False
        
        if result.data is None:
            return False
        
        return True
    
    async def execute_with_retry(
        self,
        query: str,
        context: dict,
        max_retries: int = 2,
    ) -> QueryResult:
        """
        Execute query with retry logic.
        
        Args:
            query: Query string
            context: Execution context
            max_retries: Maximum retry attempts
            
        Returns:
            QueryResult
        """
        last_error = None
        
        for attempt in range(max_retries + 1):
            try:
                result = await self.execute(query, context)
                
                if self.validate_result(result):
                    return result
                
                last_error = result.error or "Invalid result"
                
            except Exception as e:
                last_error = str(e)
                logger.warning(f"Engine execution failed (attempt {attempt + 1}): {e}")
        
        # All retries failed
        return QueryResult(
            data=None,
            success=False,
            engine=self.name,
            query=query,
            execution_time_ms=0,
            confidence=0.0,
            error=f"All retries failed: {last_error}",
        )


class BaseSQLEngine(BaseEngine):
    """
    Base class for SQL engines.
    
    Provides SQL-specific utilities and validation.
    """
    
    def __init__(self, config: dict):
        super().__init__(config)
        self.connection_string = config.get("connection_string")
        self.schema = config.get("schema", {})
    
    @abstractmethod
    async def generate_sql(self, natural_query: str, schema: dict) -> str:
        """
        Generate SQL from natural language query.
        
        Args:
            natural_query: Natural language query
            schema: Database schema
            
        Returns:
            SQL query string
        """
        pass
    
    async def execute_sql(self, sql: str, connection: Any) -> List[Dict]:
        """
        Execute SQL query.
        
        Args:
            sql: SQL query string
            connection: Database connection
            
        Returns:
            List of row dictionaries
        """
        # In real implementation, execute SQL
        pass
    
    def validate_sql(self, sql: str) -> bool:
        """Validate SQL syntax"""
        # Basic SQL validation
        sql_upper = sql.upper().strip()
        
        # Must start with SELECT (for read queries)
        if not sql_upper.startswith("SELECT"):
            return False
        
        # Must not contain dangerous operations
        dangerous = ["DROP", "DELETE", "TRUNCATE", "ALTER"]
        for keyword in dangerous:
            if keyword in sql_upper:
                return False
        
        return True


class BaseSPARQLEngine(BaseEngine):
    """
    Base class for SPARQL engines.
    
    Provides SPARQL-specific utilities and validation.
    """
    
    def __init__(self, config: dict):
        super().__init__(config)
        self.endpoint_url = config.get("endpoint_url")
        self.graph = config.get("graph")
    
    @abstractmethod
    async def generate_sparql(self, natural_query: str, ontology: dict) -> str:
        """
        Generate SPARQL from natural language query.
        
        Args:
            natural_query: Natural language query
            ontology: KG ontology/schema
            
        Returns:
            SPARQL query string
        """
        pass
    
    async def execute_sparql(self, sparql: str, endpoint: str) -> List[Dict]:
        """
        Execute SPARQL query.
        
        Args:
            sparql: SPARQL query string
            endpoint: SPARQL endpoint URL
            
        Returns:
            List of result bindings
        """
        # In real implementation, execute SPARQL
        pass
    
    def validate_sparql(self, sparql: str) -> bool:
        """Validate SPARQL syntax"""
        sparql_upper = sparql.upper().strip()
        
        # Must contain SELECT or ASK
        if not ("SELECT" in sparql_upper or "ASK" in sparql_upper):
            return False
        
        # Must contain WHERE clause
        if "WHERE" not in sparql_upper:
            return False
        
        return True


class BaseTableQAEngine(BaseEngine):
    """
    Base class for Table QA engines.
    
    Provides table-specific utilities and validation.
    """
    
    def __init__(self, config: dict):
        super().__init__(config)
        self.table_path = config.get("table_path")
        self.table_format = config.get("format", "csv")
    
    @abstractmethod
    async def answer(self, query: str, table: Any) -> Any:
        """
        Answer question about table.
        
        Args:
            query: Natural language query
            table: Loaded table (DataFrame, etc.)
            
        Returns:
            Answer (value, list, or DataFrame)
        """
        pass
    
    def load_table(self, path: str) -> Any:
        """
        Load table from file.
        
        Args:
            path: File path
            
        Returns:
            Loaded table
        """
        import pandas as pd
        
        if path.endswith('.csv'):
            return pd.read_csv(path)
        elif path.endswith('.xlsx'):
            return pd.read_excel(path)
        else:
            raise ValueError(f"Unsupported table format: {path}")
