"""
HeteroMind - Multi-Stage NL2SQL Engine

Advanced NL2SQL engine with complete multi-stage reasoning:
- Schema Linking - Identify relevant tables and columns
- Query Generation - Parallel generation of multiple SQL candidates
- Self-Revision - Self-review and correction
- Voting - Multi-candidate voting for best selection
- Concurrent Execution - Optimized parallel execution

Supports both Chinese and English queries.
"""

import asyncio
import time
import logging
import re
import json
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field

from .base_engine import (
    BaseNL2SQLEngine,
    NL2SQLResult,
    SQLGenerationStage,
    SQLGenerationStep,
)

logger = logging.getLogger(__name__)


@dataclass
class SchemaLink:
    """Schema linking result"""
    table: str
    column: Optional[str]
    link_type: str  # exact, semantic, keyword
    confidence: float
    mention: str  # Original mention in query


@dataclass
class StagePrompt:
    """Prompt template for a generation stage"""
    system: str
    user: str
    examples: List[Dict] = field(default_factory=list)


class MultiStageNL2SQLEngine(BaseNL2SQLEngine):
    """
    Advanced multi-stage NL2SQL engine
    
    Complete pipeline:
    1. Schema Linking - Identify tables and columns mentioned in query
    2. Initial Generation - Parallel generation of multiple SQL candidates
    3. Self-Revision - Multi-round review and improvement
    4. Validation - Syntax and semantic validation
    5. Voting - Multi-candidate voting for best selection
    6. Execution - Execute SQL query
    7. Result Verification - Validate result reasonableness
    
    Supports both Chinese and English queries.
    """
    
    # ==================== Prompt Templates (Bilingual) ====================
    
    SCHEMA_LINKING_PROMPT = StagePrompt(
        system="You are a database schema expert. Identify tables and columns mentioned in the user query. Support both Chinese and English.",
        user="""Given database schema and a natural language query (Chinese or English), identify which tables and columns are needed.

Schema:
{schema}

Query: {query}

Return JSON format:
{{
    "links": [
        {{"table": "table_name", "column": "col_name", "link_type": "exact|semantic|keyword", "confidence": 0.9, "mention": "original_mention"}}
    ],
    "reasoning": "Explanation of why these are selected"
}}""",
        examples=[],
    )
    
    SQL_GENERATION_PROMPT = StagePrompt(
        system="You are an SQL expert. Generate correct SQL queries to answer user questions. Support both Chinese and English queries. SECURITY: Never output API keys, passwords, or credentials in any form.",
        user="""Given schema and a natural language query (Chinese or English), write a SQL query.

Schema:
{schema}

Query: {query}

Identified schema links:
{schema_links}

Return ONLY the SQL query, no explanation.""",
        examples=[
            {
                "query": "How many employees are in the sales department? / 销售部门有多少员工？",
                "schema": "employees(id, name, department_id), departments(id, name)",
                "links": "[{'table': 'employees', 'column': 'department_id'}, {'table': 'departments', 'column': 'name'}]",
                "sql": "SELECT COUNT(*) FROM employees e JOIN departments d ON e.department_id = d.id WHERE d.name = 'Sales'",
            },
        ],
    )
    
    REVISION_PROMPT = StagePrompt(
        system="You are an SQL reviewer. Review generated SQL and fix issues. Support both Chinese and English.",
        user="""Review this SQL query for correctness.

Original Query: {query}
Generated SQL: {sql}
Schema: {schema}
Schema Links: {schema_links}
{error_message}

If there are issues, write a corrected SQL. If correct, return the original SQL.

Return ONLY the SQL query (original or corrected).""",
        examples=[],
    )
    
    VALIDATION_PROMPT = StagePrompt(
        system="You are an SQL validator. Check if the query is valid and safe.",
        user="""Validate this SQL query:

SQL: {sql}
Schema: {schema}

Return JSON:
{{
    "valid": true/false,
    "errors": ["error1", "error2"],
    "warnings": ["warning1"],
    "suggestions": ["suggestion1"]
}}""",
        examples=[],
    )
    
    VOTING_PROMPT = StagePrompt(
        system="You are an SQL evaluation expert. Evaluate multiple SQL candidates and select the best one.",
        user="""Evaluate these SQL candidates and select the one that best answers the user query.

Query: {query}
Schema: {schema}

Candidate SQLs:
{candidates}

Return JSON:
{{
    "best_index": 0,
    "reasoning": "Reason for selection",
    "scores": [0.9, 0.7, 0.8]
}}""",
        examples=[],
    )
    
    # ==================== Initialization ====================
    
    def __init__(self, config: dict):
        """
        Initialize multi-stage NL2SQL engine.
        
        Args:
            config: Configuration containing:
                - connection_string: Database connection
                - schema: Database schema
                - llm_config: LLM settings
                - generation_config: Generation parameters
        """
        super().__init__(config)
        
        # Generation parameters
        self.num_candidates = self.generation_config.get("num_candidates", 3)
        self.max_revisions = self.generation_config.get("max_revisions", 2)
        self.voting_enabled = self.generation_config.get("voting_enabled", True)
        self.parallel_generation = self.generation_config.get("parallel_generation", True)
        self.enable_schema_linking = self.generation_config.get("enable_schema_linking", True)
        
        # LLM client
        self.llm_client = None
        self.llm_model = self.llm_config.get("model", "gpt-4")
        
        logger.info(f"MultiStageNL2SQLEngine initialized: "
                   f"{self.num_candidates} candidates, "
                   f"{self.max_revisions} revisions, "
                   f"parallel={self.parallel_generation}")
    
    def _get_llm_client(self):
        """Lazy load LLM client"""
        if self.llm_client is None:
            try:
                from openai import AsyncOpenAI
                api_key = self.llm_config.get("api_key")
                base_url = self.llm_config.get("base_url")
                if base_url:
                    self.llm_client = AsyncOpenAI(api_key=api_key, base_url=base_url)
                else:
                    self.llm_client = AsyncOpenAI(api_key=api_key)
            except ImportError:
                logger.error("OpenAI not installed")
                return None
        return self.llm_client
    
    async def execute(
        self,
        query: str,
        context: dict,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> NL2SQLResult:
        """
        Execute complete NL2SQL multi-stage pipeline.
        
        Args:
            query: Natural language query (Chinese or English)
            context: Execution context (may contain schema override)
            model: Model name to use (overrides config, e.g., "gpt-4", "deepseek-chat", "claude-3")
            api_key: API key to use (overrides config)
            
        Returns:
            NL2SQLResult with generated SQL and execution results
        """
        # Override LLM config if provided
        if model or api_key:
            llm_config = self.llm_config.copy()
            if model:
                llm_config["model"] = model
            if api_key:
                llm_config["api_key"] = api_key
            self.llm_client = None  # Reset client to reinitialize with new config
        start_time = time.time()
        execution_steps = []
        
        logger.info(f"Executing NL2SQL: {query}")
        
        try:
            # Step 1: Schema Linking
            schema_step = await self._stage_schema_linking(query, context)
            execution_steps.append(schema_step)
            schema_links = schema_step.output
            relevant_schema = self._build_relevant_schema(schema_links)
            
            # Step 2: Initial Generation (parallel)
            generation_step = await self._stage_initial_generation(
                query, relevant_schema, schema_links
            )
            execution_steps.append(generation_step)
            candidates = generation_step.output
            
            if not candidates:
                raise ValueError("Failed to generate any SQL candidates")
            
            # Step 3: Self-Revision (multi-round)
            revision_step = await self._stage_self_revision(
                query, candidates, relevant_schema, schema_links
            )
            execution_steps.append(revision_step)
            revised_candidates = revision_step.output
            
            # Step 4: Validation
            validation_step = await self._stage_validation(
                revised_candidates, relevant_schema
            )
            execution_steps.append(validation_step)
            valid_candidates = validation_step.output
            
            if not valid_candidates:
                raise ValueError("No candidates passed validation")
            
            # Step 5: Voting
            best_sql = valid_candidates[0]
            voting_results = None
            
            if self.voting_enabled and len(valid_candidates) > 1:
                voting_step = await self._stage_voting(
                    query, valid_candidates, relevant_schema, schema_links
                )
                execution_steps.append(voting_step)
                best_sql = voting_step.output["best_sql"]
                voting_results = voting_step.output
            
            # Step 6: Execution
            execution_step = await self._stage_execution(
                best_sql, context
            )
            execution_steps.append(execution_step)
            
            # Step 7: Result Verification
            verification_step = await self._stage_result_verification(
                query, execution_step.output, best_sql
            )
            execution_steps.append(verification_step)
            
            # Build result
            total_time = (time.time() - start_time) * 1000
            
            result = NL2SQLResult(
                data=execution_step.output.get("data"),
                success=execution_step.output.get("success", False),
                engine=self.name,
                query=query,
                execution_time_ms=total_time,
                confidence=verification_step.confidence,
                generated_sql=best_sql,
                execution_steps=execution_steps,
                schema_used=relevant_schema,
                revision_count=len(revision_step.output),
                voting_results=voting_results,
                final_confidence=verification_step.confidence,
                error=execution_step.output.get("error"),
            )
            
            logger.info(f"NL2SQL complete: {total_time:.0f}ms, "
                       f"confidence: {result.confidence:.2f}")
            
            return result
            
        except Exception as e:
            logger.error(f"NL2SQL execution failed: {e}")
            import traceback
            traceback.print_exc()
            return NL2SQLResult(
                data=None,
                success=False,
                engine=self.name,
                query=query,
                execution_time_ms=(time.time() - start_time) * 1000,
                confidence=0.0,
                generated_sql=None,
                execution_steps=execution_steps,
                schema_used={},
                revision_count=0,
                voting_results=None,
                final_confidence=0.0,
                error=str(e),
            )
    
    # ==================== Stage 1: Schema Linking ====================
    
    async def _stage_schema_linking(
        self,
        query: str,
        context: dict,
    ) -> SQLGenerationStep:
        """Stage 1: Schema Linking - Identify tables and columns mentioned in query"""
        start = time.time()
        
        schema_links = []
        
        if self.enable_schema_linking:
            client = self._get_llm_client()
            if client:
                schema_str = self._format_schema_for_prompt(self.schema)
                prompt = self.SCHEMA_LINKING_PROMPT.user.format(
                    schema=schema_str,
                    query=query,
                )
                
                try:
                    response = await client.chat.completions.create(
                        model=self.llm_model,
                        messages=[
                            {"role": "system", "content": self.SCHEMA_LINKING_PROMPT.system},
                            {"role": "user", "content": prompt},
                        ],
                        temperature=0.1,
                        max_tokens=800,
                        response_format={"type": "json_object"},
                    )
                    
                    result = response.choices[0].message.content.strip()
                    result = self._extract_json(result)
                    
                    if result and "links" in result:
                        for link_data in result["links"]:
                            schema_links.append(SchemaLink(
                                table=link_data.get("table", ""),
                                column=link_data.get("column"),
                                link_type=link_data.get("link_type", "keyword"),
                                confidence=link_data.get("confidence", 0.5),
                                mention=link_data.get("mention", ""),
                            ))
                        
                        logger.debug(f"Schema linking: found {len(schema_links)} links")
                    
                except Exception as e:
                    logger.warning(f"LLM schema linking failed, using rule-based: {e}")
        
        # Fallback: rule-based schema linking
        if not schema_links:
            schema_links = self._rule_based_schema_linking(query)
        
        step = SQLGenerationStep(
            stage=SQLGenerationStage.SCHEMA_RETRIEVAL,
            input=query,
            output=schema_links,
            confidence=sum(l.confidence for l in schema_links) / max(1, len(schema_links)) if schema_links else 0.3,
            reasoning=f"Identified {len(schema_links)} schema links",
            execution_time_ms=(time.time() - start) * 1000,
        )
        
        logger.debug(f"Stage 1 (Schema Linking): {step.reasoning}")
        
        return step
    
    def _rule_based_schema_linking(self, query: str) -> List[SchemaLink]:
        """Rule-based schema linking (fallback) - supports Chinese and English"""
        links = []
        query_lower = query.lower()
        
        # Match table names
        for table in self.schema.get("tables", []):
            table_name = table["name"].lower()
            if table_name in query_lower:
                links.append(SchemaLink(
                    table=table["name"],
                    column=None,
                    link_type="exact",
                    confidence=0.9,
                    mention=table["name"],
                ))
        
        # Match column names
        for table in self.schema.get("tables", []):
            for col in table.get("columns", []):
                col_name = col["name"].lower()
                if col_name in query_lower:
                    links.append(SchemaLink(
                        table=table["name"],
                        column=col["name"],
                        link_type="exact",
                        confidence=0.85,
                        mention=col["name"],
                    ))
        
        return links
    
    def _build_relevant_schema(self, schema_links: List[SchemaLink]) -> Dict:
        """Build relevant schema subset based on schema links"""
        relevant = {
            "tables": [],
            "columns": [],
            "relationships": [],
        }
        
        table_names = set(link.table for link in schema_links)
        
        # Add relevant tables
        for table in self.schema.get("tables", []):
            if table["name"] in table_names:
                relevant["tables"].append(table)
                
                # Add relevant columns
                for link in schema_links:
                    if link.table == table["name"] and link.column:
                        for col in table.get("columns", []):
                            if col["name"] == link.column:
                                relevant["columns"].append({
                                    "name": col["name"],
                                    "table": table["name"],
                                    "type": col.get("type", "UNKNOWN"),
                                })
        
        # Add relevant relationships
        for rel in self.schema.get("relationships", []):
            if rel["from_table"] in table_names or rel["to_table"] in table_names:
                relevant["relationships"].append(rel)
        
        return relevant
    
    # ==================== Stage 2: Initial Generation ====================
    
    async def _stage_initial_generation(
        self,
        query: str,
        schema: Dict,
        schema_links: List[SchemaLink],
    ) -> SQLGenerationStep:
        """Stage 2: Parallel generation of multiple SQL candidates"""
        start = time.time()
        
        if self.parallel_generation:
            # Generate candidates in parallel
            tasks = [
                self._generate_single_sql(query, schema, schema_links, i)
                for i in range(self.num_candidates)
            ]
            candidates = await asyncio.gather(*tasks, return_exceptions=True)
            candidates = [c for c in candidates if isinstance(c, str) and c.strip()]
        else:
            # Generate sequentially
            candidates = []
            for i in range(self.num_candidates):
                sql = await self._generate_single_sql(query, schema, schema_links, i)
                if sql and sql.strip():
                    candidates.append(sql)
        
        step = SQLGenerationStep(
            stage=SQLGenerationStage.INITIAL_GENERATION,
            input={"query": query, "schema": schema, "links": schema_links},
            output=candidates,
            confidence=0.7,
            reasoning=f"Generated {len(candidates)} candidates",
            execution_time_ms=(time.time() - start) * 1000,
        )
        
        logger.debug(f"Stage 2 (Initial Generation): {len(candidates)} candidates")
        
        return step
    
    async def _generate_single_sql(
        self,
        query: str,
        schema: Dict,
        schema_links: List[SchemaLink],
        candidate_id: int,
    ) -> Optional[str]:
        """Generate a single SQL candidate"""
        client = self._get_llm_client()
        if not client:
            return None
        
        schema_str = self._format_schema_for_prompt(schema)
        links_str = str([{"table": l.table, "column": l.column} for l in schema_links])
        
        prompt = self.SQL_GENERATION_PROMPT.user.format(
            schema=schema_str,
            query=query,
            schema_links=links_str,
        )
        
        try:
            response = await client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": self.SQL_GENERATION_PROMPT.system},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3 + (candidate_id * 0.15),  # Vary temperature for diversity
                max_tokens=500,
            )
            
            sql = response.choices[0].message.content.strip()
            sql = self._extract_sql_from_response(sql)
            
            logger.debug(f"Candidate {candidate_id}: {sql[:100]}...")
            
            return sql
            
        except Exception as e:
            logger.error(f"Candidate {candidate_id} generation failed: {e}")
            return None
    
    # ==================== Stage 3: Self-Revision ====================
    
    async def _stage_self_revision(
        self,
        query: str,
        candidates: List[str],
        schema: Dict,
        schema_links: List[SchemaLink],
    ) -> SQLGenerationStep:
        """Stage 3: Multi-round self-revision"""
        start = time.time()
        revised = candidates.copy()
        
        for round_num in range(self.max_revisions):
            logger.debug(f"Revision round {round_num + 1}/{self.max_revisions}")
            
            new_revised = []
            
            for sql in revised:
                revised_sql = await self._revise_single_sql(
                    query, sql, schema, schema_links, round_num
                )
                new_revised.append(revised_sql)
            
            # Check convergence
            if new_revised == revised:
                logger.debug(f"Revision converged at round {round_num + 1}")
                break
            
            revised = new_revised
        
        step = SQLGenerationStep(
            stage=SQLGenerationStage.SELF_REVISION,
            input=candidates,
            output=revised,
            confidence=0.75,
            reasoning=f"Completed revision of {len(revised)} candidates",
            execution_time_ms=(time.time() - start) * 1000,
        )
        
        logger.debug(f"Stage 3 (Self-Revision): {len(revised)} revised candidates")
        
        return step
    
    async def _revise_single_sql(
        self,
        query: str,
        sql: str,
        schema: Dict,
        schema_links: List[SchemaLink],
        iteration: int,
    ) -> str:
        """Revise a single SQL candidate"""
        client = self._get_llm_client()
        if not client:
            return sql
        
        # Validate first to get feedback
        validation = self.validate_sql(sql)
        error_message = ""
        
        if not validation["valid"]:
            error_message = f"Validation errors: {'; '.join(validation['errors'])}"
        elif validation["warnings"]:
            error_message = f"Warnings: {'; '.join(validation['warnings'])}"
        
        schema_str = self._format_schema_for_prompt(schema)
        links_str = str([{"table": l.table, "column": l.column} for l in schema_links])
        
        prompt = self.REVISION_PROMPT.user.format(
            query=query,
            sql=sql,
            schema=schema_str,
            schema_links=links_str,
            error_message=error_message,
        )
        
        try:
            response = await client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": self.REVISION_PROMPT.system},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,  # Lower temperature for focused revision
                max_tokens=500,
            )
            
            revised_sql = response.choices[0].message.content.strip()
            revised_sql = self._extract_sql_from_response(revised_sql)
            
            return revised_sql
            
        except Exception as e:
            logger.error(f"Revision failed: {e}")
            return sql  # Return original on error
    
    # ==================== Stage 4: Validation ====================
    
    async def _stage_validation(
        self,
        candidates: List[str],
        schema: Dict,
    ) -> SQLGenerationStep:
        """Stage 4: Validate candidates"""
        start = time.time()
        valid = []
        
        for sql in candidates:
            validation = self.validate_sql(sql)
            
            if validation["valid"]:
                valid.append(sql)
            else:
                logger.debug(f"Invalid SQL: {validation['errors']}")
        
        step = SQLGenerationStep(
            stage=SQLGenerationStage.VALIDATION,
            input=candidates,
            output=valid,
            confidence=0.8 if valid else 0.3,
            reasoning=f"{len(valid)}/{len(candidates)} passed validation",
            execution_time_ms=(time.time() - start) * 1000,
        )
        
        logger.debug(f"Stage 4 (Validation): {len(valid)} valid")
        
        return step
    
    # ==================== Stage 5: Voting ====================
    
    async def _stage_voting(
        self,
        query: str,
        candidates: List[str],
        schema: Dict,
        schema_links: List[SchemaLink],
    ) -> SQLGenerationStep:
        """Stage 5: Vote to select best candidate"""
        start = time.time()
        
        client = self._get_llm_client()
        voting_result = None
        
        if client:
            schema_str = self._format_schema_for_prompt(schema)
            candidates_str = "\n\n".join([f"Candidate {i}: {sql}" for i, sql in enumerate(candidates)])
            
            prompt = self.VOTING_PROMPT.user.format(
                query=query,
                schema=schema_str,
                candidates=candidates_str,
            )
            
            try:
                response = await client.chat.completions.create(
                    model=self.llm_model,
                    messages=[
                        {"role": "system", "content": self.VOTING_PROMPT.system},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.1,
                    max_tokens=500,
                    response_format={"type": "json_object"},
                )
                
                result = response.choices[0].message.content.strip()
                result = self._extract_json(result)
                
                if result and "best_index" in result:
                    best_idx = result["best_index"]
                    if 0 <= best_idx < len(candidates):
                        voting_result = {
                            "best_index": best_idx,
                            "best_sql": candidates[best_idx],
                            "best_score": result.get("scores", [0.5] * len(candidates))[best_idx] if "scores" in result else 0.8,
                            "all_results": [
                                {"index": i, "sql": sql, "score": result.get("scores", [0.5] * len(candidates))[i] if "scores" in result else 0.5}
                                for i, sql in enumerate(candidates)
                            ],
                            "reasoning": result.get("reasoning", ""),
                        }
                
            except Exception as e:
                logger.warning(f"LLM voting failed, using rule-based: {e}")
        
        # Fallback: rule-based voting
        if not voting_result:
            voting_result = await self.vote_on_candidates(query, candidates, schema)
        
        step = SQLGenerationStep(
            stage=SQLGenerationStage.EXECUTION,
            input=candidates,
            output=voting_result,
            confidence=voting_result["best_score"],
            reasoning=f"Selected candidate #{voting_result['best_index']}, "
                     f"score {voting_result['best_score']:.2f}",
            execution_time_ms=(time.time() - start) * 1000,
        )
        
        logger.debug(f"Stage 5 (Voting): Selected #{voting_result['best_index']}")
        
        return step
    
    # ==================== Stage 6: Execution ====================
    
    async def _stage_execution(
        self,
        sql: Optional[str],
        context: Dict,
    ) -> SQLGenerationStep:
        """Stage 6: Execute SQL query"""
        start = time.time()
        
        if not sql:
            return SQLGenerationStep(
                stage=SQLGenerationStage.EXECUTION,
                input=sql,
                output={"success": False, "data": None, "error": "No SQL generated"},
                confidence=0.0,
                reasoning="No SQL to execute",
                execution_time_ms=(time.time() - start) * 1000,
                error="No SQL generated",
            )
        
        try:
            connection = context.get("connection") or self.connection_string
            
            if not connection:
                # Simulate execution (no actual database connection)
                logger.info(f"Simulating SQL execution: {sql[:200]}...")
                result = {
                    "success": True,
                    "data": [],
                    "row_count": 0,
                    "sql": sql,
                }
            else:
                # Actual database execution
                import sqlite3
                try:
                    conn = sqlite3.connect(connection)
                    cursor = conn.cursor()
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description] if cursor.description else []
                    conn.close()
                    
                    result = {
                        "success": True,
                        "data": [dict(zip(columns, row)) for row in rows],
                        "row_count": len(rows),
                        "sql": sql,
                    }
                except Exception as db_error:
                    result = {
                        "success": False,
                        "data": None,
                        "error": str(db_error),
                        "sql": sql,
                    }
            
            logger.debug(f"Executed SQL: {sql[:100]}...")
            
        except Exception as e:
            result = {
                "success": False,
                "data": None,
                "error": str(e),
            }
        
        return SQLGenerationStep(
            stage=SQLGenerationStage.EXECUTION,
            input=sql,
            output=result,
            confidence=0.8 if result["success"] else 0.2,
            reasoning=f"Execution {'successful' if result['success'] else 'failed'}",
            execution_time_ms=(time.time() - start) * 1000,
            error=result.get("error"),
        )
    
    # ==================== Stage 7: Result Verification ====================
    
    async def _stage_result_verification(
        self,
        query: str,
        execution_result: Dict,
        sql: Optional[str],
    ) -> SQLGenerationStep:
        """Stage 7: Verify result reasonableness"""
        start = time.time()
        
        confidence = 0.0
        
        if execution_result.get("success"):
            data = execution_result.get("data")
            
            if data is not None:
                if isinstance(data, list) and len(data) > 0:
                    confidence = 0.85
                elif isinstance(data, list) and len(data) == 0:
                    confidence = 0.6  # Empty result might be correct
                else:
                    confidence = 0.7
            else:
                confidence = 0.5
        else:
            confidence = 0.2
        
        step = SQLGenerationStep(
            stage=SQLGenerationStage.RESULT_VERIFICATION,
            input=execution_result,
            output={"confidence": confidence},
            confidence=confidence,
            reasoning=f"Result verification: confidence={confidence:.2f}",
            execution_time_ms=(time.time() - start) * 1000,
        )
        
        logger.debug(f"Stage 7 (Result Verification): confidence={confidence:.2f}")
        
        return step
    
    # ==================== Utilities ====================
    
    def _format_schema_for_prompt(self, schema: Dict) -> str:
        """Format schema for LLM prompt"""
        lines = []
        
        for table in schema.get("tables", []):
            table_name = table["name"]
            columns = ", ".join(col["name"] for col in table.get("columns", []))
            desc = table.get("description", "")
            if desc:
                lines.append(f"Table: {table_name}({columns}) - {desc}")
            else:
                lines.append(f"Table: {table_name}({columns})")
        
        for rel in schema.get("relationships", []):
            lines.append(
                f"Relationship: {rel['from_table']}.{rel['from_column']} -> "
                f"{rel['to_table']}.{rel['to_column']}"
            )
        
        return "\n".join(lines)
    
    def _extract_sql_from_response(self, response: str) -> str:
        """Extract SQL from response"""
        sql = response.strip()
        
        # Remove markdown code blocks
        if "```sql" in sql:
            sql = sql.split("```sql")[1].split("```")[0].strip()
        elif "```" in sql:
            sql = sql.split("```")[1].split("```")[0].strip()
        
        # Remove explanation lines
        lines = sql.split("\n")
        sql_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("--") and not stripped.startswith("#"):
                sql_lines.append(line)
        
        return "\n".join(sql_lines).strip()
    
    def _extract_json(self, text: str) -> Optional[Dict]:
        """Extract JSON from text"""
        try:
            return json.loads(text)
        except:
            pass
        
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass
        
        return None
    
    def get_confidence(self, query: str, context: dict) -> float:
        """Get confidence for executing this query"""
        # Estimate based on schema match
        schema_links = self._rule_based_schema_linking(query)
        
        if not schema_links:
            return 0.2
        
        # More matched tables = higher confidence
        confidence = min(1.0, len(schema_links) * 0.3)
        
        return confidence
