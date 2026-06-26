"""
HeteroMind - Layer 3c: Entity Retrieval Verifier

Verifies if entities mentioned in query actually exist in knowledge sources.
"""

import os
import logging
from typing import Dict, List

from .models import EntityVerification

logger = logging.getLogger(__name__)


class EntityRetrievalVerifier:
    """
    Layer 3c: Entity retrieval verification.
    
    Critical validation step - verifies if entities mentioned in the query
    actually exist in each knowledge source. If entities don't exist in
    a source, that source is unlikely to provide useful results.
    
    Verification methods:
    - SQL: Search across tables for entity mentions
    - KG: SPARQL ASK queries for entity existence
    - Tables: Scan CSV/Excel files for entity matches
    """
    
    def __init__(self, config: dict):
        """
        Initialize verifier.
        
        Args:
            config: Configuration dict with:
                - sql_connection: SQL connection string
                - kg_endpoints: KG endpoint configs
                - table_paths: Paths to table files
        """
        self.config = config
        self.sql_connection = config.get("sql_connection")
        self.kg_endpoints = config.get("kg_endpoints", [])
        self.table_paths = config.get("table_paths", [])
    
    async def verify_entities(
        self,
        entities: List[str],
        predicates: List[str],
    ) -> EntityVerification:
        """
        Verify if entities exist in each knowledge source.
        
        Args:
            entities: List of entity mentions from query
            predicates: List of detected predicates
            
        Returns:
            EntityVerification with verification results
        """
        logger.debug(f"Verifying {len(entities)} entities across sources")
        
        sql_results = await self._verify_in_sql(entities)
        kg_results = await self._verify_in_kg(entities)
        table_results = await self._verify_in_tables(entities)
        
        sql_score = len(sql_results) / max(len(entities), 1)
        kg_score = len(kg_results) / max(len(entities), 1)
        table_score = len(table_results) / max(len(entities), 1)
        
        logger.debug(
            f"Verification scores: SQL={sql_score:.2f}, "
            f"KG={kg_score:.2f}, Table={table_score:.2f}"
        )
        
        return EntityVerification(
            entities_found_in_sql=sql_results,
            entities_found_in_kg=kg_results,
            entities_found_in_tables=table_results,
            sql_verification_score=sql_score,
            kg_verification_score=kg_score,
            table_verification_score=table_score,
        )
    
    async def _verify_in_sql(self, entities: List[str]) -> List[Dict]:
        """Verify entities exist in SQL database"""
        found = []
        
        if not self.sql_connection:
            logger.debug("SQL connection not configured, skipping SQL verification")
            return found
        
        # For each entity, search across all tables
        for entity in entities:
            # In real implementation, execute SQL like:
            # SELECT TABLE_NAME, COLUMN_NAME, COUNT(*) as match_count
            # FROM INFORMATION_SCHEMA.COLUMNS
            # WHERE EXISTS (
            #     SELECT 1 FROM table_name 
            #     WHERE LOWER(column_name) LIKE LOWER('%entity%')
            # )
            
            logger.debug(f"Would verify in SQL: {entity}")
            # Placeholder: add mock result for testing
            # found.append({
            #     "entity": entity,
            #     "table": "placeholder",
            #     "column": "name",
            #     "match_count": 1,
            # })
        
        return found
    
    async def _verify_in_kg(self, entities: List[str]) -> List[Dict]:
        """Verify entities exist in knowledge graph"""
        found = []
        
        for endpoint in self.kg_endpoints:
            if not endpoint.get("enabled", True):
                continue
            
            for entity in entities:
                sparql = f"""
                ASK WHERE {{
                    ?entity rdfs:label ?label .
                    FILTER(CONTAINS(LCASE(?label), "{entity.lower()}"))
                }}
                """
                
                logger.debug(f"Would verify in KG ({endpoint['name']}): {entity}")
                # In real implementation, execute SPARQL ASK query
        
        return found
    
    async def _verify_in_tables(self, entities: List[str]) -> List[Dict]:
        """Verify entities exist in table files"""
        found = []
        
        for table_path in self.table_paths:
            if not os.path.exists(table_path):
                continue
            
            try:
                import pandas as pd
                
                if table_path.endswith('.csv'):
                    df = pd.read_csv(table_path)
                elif table_path.endswith('.xlsx'):
                    df = pd.read_excel(table_path)
                else:
                    continue
                
                for entity in entities:
                    for col in df.columns:
                        matches = df[col].astype(str).str.contains(
                            entity, case=False, na=False
                        )
                        if matches.any():
                            found.append({
                                "entity": entity,
                                "table": table_path,
                                "column": col,
                                "match_count": int(matches.sum()),
                            })
                            logger.debug(
                                f"Found '{entity}' in {table_path}:{col} "
                                f"({matches.sum()} matches)"
                            )
            except Exception as e:
                logger.error(f"Error verifying in table {table_path}: {e}")
        
        return found
