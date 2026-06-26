"""
HeteroMind - Layer 3a: SQL Schema Matcher

Matches query mentions against database schema metadata.
"""

import logging
from typing import Dict, List, Optional, Tuple

from .models import SchemaMatch, ColumnInfo, TableInfo, DatabaseSchema

logger = logging.getLogger(__name__)


class SQLSchemaMatcher:
    """
    Layer 3a: SQL schema matching.
    
    Matches query mentions against database schema to determine:
    - Which tables are referenced
    - Which columns are referenced
    - What joins are required
    - Confidence score for SQL source
    """
    
    def __init__(self, schemas: List):
        """
        Initialize with database schemas.
        
        Args:
            schemas: List of DatabaseSchema objects OR dict schemas (JSON format)
        """
        # Convert dict schemas to DatabaseSchema objects if needed
        self.schemas = []
        for schema in schemas:
            if isinstance(schema, dict):
                self.schemas.append(self._dict_to_schema(schema))
            else:
                self.schemas.append(schema)
        
        self.column_index = self._build_column_index()
        self.table_index = self._build_table_index()
    
    def _dict_to_schema(self, data: dict) -> DatabaseSchema:
        """Convert dictionary schema to DatabaseSchema object"""
        tables = []
        for table_data in data.get("tables", []):
            columns = []
            for col_data in table_data.get("columns", []):
                col = ColumnInfo(
                    name=col_data.get("name", ""),
                    table=table_data.get("name", ""),
                    data_type=col_data.get("type", "VARCHAR"),
                    alias=col_data.get("alias"),
                )
                columns.append(col)
            
            table = TableInfo(
                name=table_data.get("name", ""),
                schema=data.get("database", "public"),
                columns=columns,
                description=table_data.get("description"),
            )
            tables.append(table)
        
        return DatabaseSchema(
            name=data.get("database", "unknown"),
            tables=tables,
        )
    
    def _build_column_index(self) -> Dict[str, List[ColumnInfo]]:
        """Build inverted index: column_name -> [ColumnInfo]"""
        index = {}
        for schema in self.schemas:
            for table in schema.tables:
                for col in table.columns:
                    key = col.name.lower()
                    index.setdefault(key, []).append(col)
                    if col.alias:
                        index.setdefault(col.alias.lower(), []).append(col)
        return index
    
    def _build_table_index(self) -> Dict[str, List[TableInfo]]:
        """Build inverted index: table_name -> [TableInfo]"""
        index = {}
        for schema in self.schemas:
            for table in schema.tables:
                key = table.name.lower()
                index.setdefault(key, []).append(table)
                if table.description:
                    for word in table.description.lower().split():
                        if len(word) > 3:
                            index.setdefault(word, []).append(table)
        return index
    
    def match_query(self, query: str) -> SchemaMatch:
        """
        Match query against SQL schema.
        
        Args:
            query: Natural language query string
            
        Returns:
            SchemaMatch with matched tables/columns
        """
        query_lower = query.lower()
        
        mentioned_columns = []
        for col_name, cols in self.column_index.items():
            if col_name in query_lower or f" {col_name}" in query_lower:
                mentioned_columns.extend([c.name for c in cols])
        
        mentioned_tables = []
        for table_name, tables in self.table_index.items():
            if table_name in query_lower or f" {table_name}" in query_lower:
                mentioned_tables.extend([t.name for t in tables])
        
        required_joins = self._infer_joins(list(set(mentioned_tables)))
        confidence = self._calculate_confidence(mentioned_columns, mentioned_tables)
        
        logger.debug(f"SQL schema match: tables={mentioned_tables}, cols={mentioned_columns}")
        
        return SchemaMatch(
            mentioned_tables=list(set(mentioned_tables)),
            mentioned_columns=list(set(mentioned_columns)),
            required_joins=required_joins,
            confidence=confidence,
            is_sql_likely=confidence > 0.3,
        )
    
    def _infer_joins(self, tables: List[str]) -> List[Tuple[str, str]]:
        """Infer required joins between tables"""
        joins = []
        if len(tables) > 1:
            for i, t1 in enumerate(tables):
                for t2 in tables[i+1:]:
                    joins.append((t1, t2))
        return joins
    
    def _calculate_confidence(self, columns: List[str], tables: List[str]) -> float:
        """Calculate confidence score based on matches"""
        if not columns and not tables:
            return 0.0
        
        score = (len(tables) * 0.4 + len(columns) * 0.2)
        score = min(1.0, score)
        
        return score
