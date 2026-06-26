"""
nl_query.py — Natural Language to SQL for pg-memory

Uses local Ollama LLM (configurable) to generate SQL from natural language
questions about the pg-memory database.
"""

import os
import re
import json
import time
import subprocess
from typing import List, Dict, Optional, Any, Union
from dataclasses import dataclass

@dataclass
class NLQueryConfig:
    """Configuration for natural language queries."""
    model: str = "ollama/mistral:latest"  # Default model
    max_results: int = 50
    timeout_seconds: int = 30
    temperature: float = 0.1
    
    @classmethod
    def from_env(cls) -> 'NLQueryConfig':
        """Load config from environment with OpenClaw-aware defaults."""
        # Detect OpenClaw's current default model
        openclaw_model = os.getenv('OPENCLAW_MODEL', 'ollama/mistral:latest')
        
        return cls(
            model=os.getenv('PG_MEMORY_NL_MODEL', openclaw_model),
            max_results=int(os.getenv('PG_MEMORY_NL_MAX_RESULTS', '50')),
            timeout_seconds=int(os.getenv('PG_MEMORY_NL_TIMEOUT', '30')),
            temperature=float(os.getenv('PG_MEMORY_NL_TEMP', '0.1'))
        )


@dataclass
class NLQueryResult:
    """Result from natural language query."""
    sql_query: str
    params: List[Any]
    result_count: int
    results: List[Dict]
    execution_time_ms: float
    interpretation: str


# Database schema for SQL generation context
DB_SCHEMA = """
TABLE: observations
- id (UUID, PRIMARY KEY): Unique observation ID
- title (TEXT): Optional title
- content (TEXT): Main observation text (full-text indexed)
- tags (TEXT[]): Array of tags
- importance_score (FLOAT): 0.0-1.0 importance rating
- created_at (TIMESTAMP): When created
- updated_at (TIMESTAMP): Last modified
- status (TEXT): 'active', 'ongoing', 'resolved', 'superseded'
- source (TEXT): Where it came from
- session_key (TEXT): Associated session
- related_observation_ids (UUID[]): Linked observations
- related_files (TEXT[]): Associated file paths
- related_urls (TEXT[]): Associated URLs

TABLE: summaries
- id (UUID): Summary ID
- source_observation_ids (UUID[]): Which observations summarized
- summary_type (TEXT): 'auto', 'manual', 'weekly', 'project'
- title (TEXT): Summary title
- content (TEXT): Summary text
- generated_by (TEXT): Who/what created it
- covers_from/to (TIMESTAMP): Time period

TABLE: observation_chains
- id (UUID): Chain ID
- chain_name (TEXT): Name of project/workflow
- chain_type (TEXT): 'project', 'decision', 'bugfix', 'workflow'
- status (TEXT): 'active', 'complete', 'abandoned'
- current_step (INT): Progress
- total_steps (INT): Total steps
- tags (TEXT[]): Chain tags

TABLE: observation_conflicts
- id (UUID): Conflict ID
- observation_1_id, observation_2_id (UUID): Related observations
- conflict_type (TEXT): 'contradiction', 'duplicate', 'outdated'
- conflict_score (FLOAT): 0.0-1.0 similarity

TABLE: follow_up_reminders
- id (UUID): Reminder ID
- observation_id (UUID): Related observation
- reminder_type (TEXT): 'follow_up', 'escalation', 'deadline'
- reminder_message (TEXT): What to do
- remind_at (TIMESTAMP): When to remind
- status (TEXT): 'pending', 'acknowledged', 'dismissed'
"""

# System prompt for SQL generation
SQL_SYSTEM_PROMPT = """You are a PostgreSQL SQL generator. Convert natural language questions into valid SQL queries.

CRITICAL RULES:
1. Use ONLY the tables and columns described in the schema
2. Use PostgreSQL-specific syntax: to_tsvector(), to_tsquery(), plainto_tsquery(), && (array overlap)
3. For full-text search: to_tsvector('english', content) @@ plainto_tsquery('english', 'keyword')
4. For array operations: tags && ARRAY['tag1', 'tag2']
5. Use ::uuid for UUID casts when needed
6. Return ONLY valid SQL, no markdown, no explanations
7. Always include appropriate LIMIT clauses
8. For date ranges: created_at > NOW() - INTERVAL 'X days'

DATE PARSING:
- "last week" = created_at > NOW() - INTERVAL '7 days'
- "yesterday" = created_at > NOW() - INTERVAL '1 day'
- "this month" = created_at >= DATE_TRUNC('month', NOW())
- "today" = created_at::date = CURRENT_DATE

IMPORTANT SCORE INTERPRETATION:
- High importance: importance_score >= 0.7
- Medium importance: importance_score BETWEEN 0.4 AND 0.7
- Low importance: importance_score < 0.4

STATUS VALUES:
- 'active' = new observations
- 'ongoing' = in-progress work
- 'resolved' = completed
- 'superseded' = replaced by newer

Return ONLY the SQL query, no markdown formatting, no backticks."""


class NLQueryEngine:
    """Natural language to SQL query engine for pg-memory."""
    
    def __init__(self, config: Optional[NLQueryConfig] = None):
        self.config = config or NLQueryConfig.from_env()
    
    def set_model(self, model: str) -> None:
        """Change the model used for SQL generation."""
        self.config.model = model
        # Also update env for persistence
        os.environ['PG_MEMORY_NL_MODEL'] = model
    
    def _call_ollama(self, prompt: str) -> str:
        """Call local Ollama instance to generate SQL."""
        # Extract model name (remove 'ollama/' prefix if present)
        model = self.config.model
        if model.startswith('ollama/'):
            model = model[7:]  # Remove 'ollama/' prefix
        
        full_prompt = f"{SQL_SYSTEM_PROMPT}\n\nSCHEMA:\n{DB_SCHEMA}\n\nQUESTION: {prompt}\n\nSQL:"
        
        try:
            result = subprocess.run(
                ['ollama', 'run', model, full_prompt],
                capture_output=True,
                text=True,
                timeout=self.config.timeout_seconds
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"Ollama error: {result.stderr}")
            
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"Ollama timeout after {self.config.timeout_seconds}s")
        except FileNotFoundError:
            raise RuntimeError("Ollama not found. Install with: brew install ollama")
    
    def _extract_sql(self, response: str) -> str:
        """Extract clean SQL from LLM response."""
        # Remove markdown code blocks
        response = re.sub(r'```sql\s*', '', response)
        response = re.sub(r'```\s*', '', response)
        
        # Remove SQL comments
        response = re.sub(r'--.*$', '', response, flags=re.MULTILINE)
        response = re.sub(r'/\*.*?\*/', '', response, flags=re.DOTALL)
        
        # Find the SQL query (should start with SELECT)
        lines = response.strip().split('\n')
        sql_lines = []
        
        for line in lines:
            line = line.strip()
            # Skip empty lines and non-SQL
            if not line or line.lower().startswith(('here', 'the', 'this', 'note')):
                continue
            sql_lines.append(line)
        
        sql = ' '.join(sql_lines).strip()
        
        # Validate it looks like SQL
        if not sql.upper().startswith('SELECT'):
            raise ValueError(f"Generated text doesn't look like SQL: {sql[:100]}")
        
        # Add safety limit if not present
        if 'LIMIT' not in sql.upper():
            sql = sql.rstrip(';') + f" LIMIT {self.config.max_results}"
        
        return sql
    
    def _sanitize_sql(self, sql: str) -> str:
        """Additional SQL sanitization for safety."""
        # Block dangerous operations
        dangerous = ['DELETE', 'DROP', 'UPDATE', 'INSERT', 'TRUNCATE', 'ALTER', 'CREATE']
        sql_upper = sql.upper()
        
        for op in dangerous:
            if re.search(rf'\b{op}\b', sql_upper):
                raise ValueError(f"Dangerous operation detected: {op}")
        
        # Ensure only SELECT statements
        if not sql.strip().upper().startswith('SELECT'):
            raise ValueError("Only SELECT statements allowed")
        
        return sql
    
    def generate_sql(self, question: str) -> str:
        """Generate SQL from natural language question."""
        # Call LLM
        response = self._call_ollama(question)
        
        # Extract and clean SQL
        sql = self._extract_sql(response)
        
        # Safety check
        sql = self._sanitize_sql(sql)
        
        return sql
    
    def ask(self, db_connection, question: str) -> NLQueryResult:
        """
        Execute natural language query and return structured result.
        
        Args:
            db_connection: psycopg2 connection
            question: Natural language question
            
        Returns:
            NLQueryResult with SQL, params, results, and interpretation
        """
        from psycopg2.extras import RealDictCursor
        
        start_time = time.time()
        
        # Generate SQL
        sql = self.generate_sql(question)
        
        # Execute
        with db_connection.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            results = [dict(row) for row in rows]
        
        execution_time = (time.time() - start_time) * 1000
        
        # Build interpretation
        interpretation = f"Found {len(results)} observations matching your query"
        if 'importance' in question.lower():
            interpretation += " with specified importance criteria"
        if 'tag' in question.lower():
            interpretation += " and tag filters"
        if 'last' in question.lower() or 'week' in question.lower():
            interpretation += " within the time range"
        
        return NLQueryResult(
            sql_query=sql,
            params=[],  # Currently no parameterized queries
            result_count=len(results),
            results=results,
            execution_time_ms=execution_time,
            interpretation=interpretation
        )


# Convenience functions for CLI/Python API
_query_engine: Optional[NLQueryEngine] = None

def get_query_engine() -> NLQueryEngine:
    """Get or create singleton query engine."""
    global _query_engine
    if _query_engine is None:
        _query_engine = NLQueryEngine()
    return _query_engine

def ask(question: str, db_connection=None) -> Union[NLQueryResult, str]:
    """
    Quick natural language query.
    
    Either provide db_connection or pg_memory will create one.
    Returns NLQueryResult on success, error string on failure.
    """
    engine = get_query_engine()
    
    try:
        if db_connection is None:
            # Import here to avoid circular
            from pg_memory import get_memory
            mem = get_memory()
            with mem._get_connection() as conn:
                return engine.ask(conn, question)
        
        return engine.ask(db_connection, question)
    except Exception as e:
        return f"Error: {str(e)}"

def set_model(model: str) -> str:
    """Change the NL query model."""
    engine = get_query_engine()
    engine.set_model(model)
    return f"NL query model changed to: {model}"

def get_model() -> str:
    """Get current NL query model."""
    engine = get_query_engine()
    return engine.config.model

def preview_sql(question: str) -> str:
    """Generate SQL without executing (for testing)."""
    engine = get_query_engine()
    try:
        return engine.generate_sql(question)
    except Exception as e:
        return f"Error generating SQL: {str(e)}"


def query_nl(question: str, db_connection=None) -> Union[NLQueryResult, str]:
    """
    Alias for ask(). Maintains API consistency with pg_memory.query_nl().
    """
    return ask(question, db_connection)


if __name__ == "__main__":
    # Test
    print("Testing nl_query...")
    
    try:
        engine = NLQueryEngine()
        
        # Test SQL generation
        test_q = "Show me high importance observations from last week"
        print(f"\nQuestion: {test_q}")
        
        sql = engine.generate_sql(test_q)
        print(f"Generated SQL: {sql}")
        print(f"\nSQL type: {type(sql)}")
        print(f"SQL content: {sql[:200]}...")
        
    except Exception as e:
        print(f"Error: {e}")
