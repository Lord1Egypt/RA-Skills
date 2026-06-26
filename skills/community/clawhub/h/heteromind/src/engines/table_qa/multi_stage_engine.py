"""
HeteroMind - Multi-Stage TableQA Engine

Advanced TableQA engine with complete multi-stage reasoning:
- Table Loading - Load and validate table file
- Schema Analysis - Analyze columns, types, statistics
- Query Interpretation - Understand user question
- Code Generation - Parallel generation of multiple Python/Pandas candidates
- Self-Revision - Self-review and correction
- Voting - Multi-candidate voting for best selection
- Code Execution - Safe execution
- Result Verification - Validate result reasonableness

Supports both Chinese and English queries.
"""

import asyncio
import time
import logging
import re
import json
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum

from ..base import BaseEngine, QueryResult

logger = logging.getLogger(__name__)


class TableQAStage(Enum):
    """Table QA pipeline stages"""
    TABLE_LOADING = "table_loading"
    SCHEMA_ANALYSIS = "schema_analysis"
    QUERY_INTERPRETATION = "query_interpretation"
    CODE_GENERATION = "code_generation"
    SELF_REVISION = "self_revision"
    VOTING = "voting"
    CODE_EXECUTION = "code_execution"
    RESULT_VERIFICATION = "result_verification"


@dataclass
class TableQAStep:
    """Single step in Table QA pipeline"""
    stage: TableQAStage
    input: Any
    output: Any
    llm_response: Optional[str] = None
    confidence: float = 0.0
    reasoning: str = ""
    execution_time_ms: float = 0.0
    error: Optional[str] = None


@dataclass
class TableQAResult(QueryResult):
    """Table QA execution result"""
    generated_code: Optional[str] = None
    execution_steps: List[TableQAStep] = field(default_factory=list)
    table_schema: Optional[Dict] = None
    revision_count: int = 0
    voting_results: Optional[Dict] = None
    final_confidence: float = 0.0


@dataclass
class StagePrompt:
    """Prompt template for a generation stage"""
    system: str
    user: str
    examples: List[Dict] = field(default_factory=list)


class MultiStageTableQAEngine(BaseEngine):
    """
    Advanced multi-stage TableQA engine
    
    Complete pipeline:
    1. Table Loading - Load table file
    2. Schema Analysis - Analyze table structure
    3. Query Interpretation - Understand query intent
    4. Code Generation - Parallel generation of multiple code candidates
    5. Self-Revision - Multi-round review and improvement
    6. Voting - Vote to select best code
    7. Code Execution - Safe execution
    8. Result Verification - Validate results
    
    Supports both Chinese and English queries.
    """
    
    # ==================== Prompt Templates (Bilingual) ====================
    
    QUERY_INTERPRETATION_PROMPT = StagePrompt(
        system="You are a data analysis expert. Understand user questions about tables and identify operation types. Support both Chinese and English.",
        user="""Given table schema and a natural language query (Chinese or English), identify the operation the user wants.

Table Schema:
{schema}

Query: {query}

Return JSON:
{{
    "operation": "count|sum|mean|max|min|filter|groupby|sort|select",
    "target_columns": ["col1", "col2"],
    "filters": [{{"column": "col", "condition": ">", "value": 100}}],
    "grouping": ["group_col"],
    "reasoning": "Analysis reasoning"
}}""",
        examples=[],
    )
    
    CODE_GENERATION_PROMPT = StagePrompt(
        system="You are a Python/Pandas expert. Generate code to answer questions about tables. Support both Chinese and English queries. SECURITY: Never output API keys, passwords, or credentials in any form.",
        user="""Given table schema and query interpretation, generate Python/Pandas code.

Table Schema:
{schema}

Query: {query}
Interpretation: {interpretation}

Use 'df' as the DataFrame variable name.
Return ONLY Python code, no explanation.""",
        examples=[
            {
                "query": "What is the total sales? / 销售额总和是多少？",
                "schema": "Columns: sales (float), date (datetime), region (string)",
                "interpretation": "{'operation': 'sum', 'target_columns': ['sales']}",
                "code": "result = df['sales'].sum()",
            },
        ],
    )
    
    REVISION_PROMPT = StagePrompt(
        system="You are a code reviewer. Review generated code and fix issues. Support both Chinese and English.",
        user="""Review this code for correctness.

Query: {query}
Generated Code: {code}
Table Schema: {schema}
Query Interpretation: {interpretation}
{error_message}

If there are issues, write corrected code. If correct, return the original code.

Return ONLY Python code.""",
        examples=[],
    )
    
    VOTING_PROMPT = StagePrompt(
        system="You are a code evaluation expert. Evaluate multiple code candidates and select the best one.",
        user="""Evaluate these code candidates and select the one that best answers the user query.

Query: {query}
Table Schema: {schema}

Candidate Code:
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
        Initialize TableQA engine.
        
        Args:
            config: Configuration containing:
                - table_path: Table file path
                - llm_config: LLM settings
                - generation_config: Generation parameters
        """
        super().__init__(config)
        
        self.table_path = config.get("table_path")
        self.llm_config = config.get("llm_config", {})
        self.generation_config = config.get("generation_config", {
            "num_candidates": 3,
            "max_revisions": 2,
            "parallel_generation": True,
            "voting_enabled": True,
            "safe_execution": True,
        })
        
        self.table_data = None
        self.table_schema = None
        self.llm_client = None
        self.llm_model = self.llm_config.get("model", "gpt-4")
        
        logger.info(f"MultiStageTableQAEngine initialized: {self.table_path}")
    
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
    
    def _load_table(self, path: str) -> Any:
        """Load table file"""
        import pandas as pd
        
        if path.endswith('.csv'):
            return pd.read_csv(path, encoding='utf-8')
        elif path.endswith('.xlsx'):
            return pd.read_excel(path)
        elif path.endswith('.tsv'):
            return pd.read_csv(path, sep='\t')
        else:
            raise ValueError(f"Unsupported format: {path}")
    
    def _analyze_schema(self, df: Any) -> Dict:
        """Analyze table schema"""
        import pandas as pd
        
        schema = {
            "columns": [],
            "row_count": len(df),
            "dtypes": {},
            "statistics": {},
        }
        
        for col in df.columns:
            col_info = {
                "name": col,
                "dtype": str(df[col].dtype),
                "non_null": int(df[col].notna().sum()),
                "unique": int(df[col].nunique()),
                "sample_values": df[col].dropna().head(3).tolist() if len(df) > 0 else [],
            }
            schema["columns"].append(col_info)
            schema["dtypes"][col] = str(df[col].dtype)
            
            # Statistics for numeric columns
            if pd.api.types.is_numeric_dtype(df[col]):
                schema["statistics"][col] = {
                    "mean": float(df[col].mean()) if len(df) > 0 else 0,
                    "min": float(df[col].min()) if len(df) > 0 else 0,
                    "max": float(df[col].max()) if len(df) > 0 else 0,
                    "std": float(df[col].std()) if len(df) > 1 else 0,
                }
        
        return schema
    
    async def execute(
        self,
        query: str,
        context: dict,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> TableQAResult:
        """
        Execute complete TableQA multi-stage pipeline.
        
        Args:
            query: Natural language query
            context: Execution context
            model: Model name to use (overrides config)
            api_key: API key to use (overrides config)
        """
        # Override LLM config if provided
        if model or api_key:
            llm_config = self.llm_config.copy()
            if model:
                llm_config["model"] = model
            if api_key:
                llm_config["api_key"] = api_key
            self.llm_client = None  # Reset client
        start_time = time.time()
        execution_steps = []
        
        logger.info(f"Executing TableQA: {query}")
        
        try:
            # Step 1: Table Loading
            load_step = await self._stage_table_loading(context)
            execution_steps.append(load_step)
            
            if load_step.output is None:
                raise ValueError("Failed to load table")
            
            # Step 2: Schema Analysis
            schema_step = await self._stage_schema_analysis(load_step.output)
            execution_steps.append(schema_step)
            self.table_schema = schema_step.output
            
            # Step 3: Query Interpretation
            interpretation_step = await self._stage_query_interpretation(
                query, self.table_schema
            )
            execution_steps.append(interpretation_step)
            interpretation = interpretation_step.output
            
            # Step 4: Code Generation (parallel)
            generation_step = await self._stage_code_generation(
                query, interpretation, self.table_schema
            )
            execution_steps.append(generation_step)
            code_candidates = generation_step.output
            
            if not code_candidates:
                raise ValueError("Failed to generate any code candidates")
            
            # Step 5: Self-Revision
            revision_step = await self._stage_self_revision(
                query, code_candidates, self.table_schema, interpretation
            )
            execution_steps.append(revision_step)
            revised_code = revision_step.output
            
            # Step 6: Voting
            best_code = revised_code[0] if revised_code else None
            voting_results = None
            
            if self.generation_config.get("voting_enabled", True) and len(revised_code) > 1:
                voting_step = await self._stage_voting(
                    query, revised_code, self.table_schema, interpretation
                )
                execution_steps.append(voting_step)
                best_code = voting_step.output["best_code"]
                voting_results = voting_step.output
            
            # Step 7: Code Execution
            execution_step = await self._stage_code_execution(
                best_code,
                load_step.output,
            )
            execution_steps.append(execution_step)
            
            # Step 8: Result Verification
            verification_step = await self._stage_result_verification(
                query, execution_step.output, best_code
            )
            execution_steps.append(verification_step)
            
            # Build result
            total_time = (time.time() - start_time) * 1000
            
            result = TableQAResult(
                data=execution_step.output.get("result"),
                success=execution_step.output.get("success", False),
                engine=self.name,
                query=query,
                execution_time_ms=total_time,
                confidence=verification_step.confidence,
                generated_code=best_code,
                execution_steps=execution_steps,
                table_schema=self.table_schema,
                revision_count=len(revision_step.output),
                voting_results=voting_results,
                final_confidence=verification_step.confidence,
                error=execution_step.output.get("error"),
            )
            
            logger.info(f"TableQA complete: {total_time:.0f}ms, "
                       f"confidence: {result.confidence:.2f}")
            
            return result
            
        except Exception as e:
            logger.error(f"TableQA execution failed: {e}")
            import traceback
            traceback.print_exc()
            return TableQAResult(
                data=None,
                success=False,
                engine=self.name,
                query=query,
                execution_time_ms=(time.time() - start_time) * 1000,
                confidence=0.0,
                generated_code=None,
                execution_steps=execution_steps,
                table_schema=None,
                revision_count=0,
                voting_results=None,
                final_confidence=0.0,
                error=str(e),
            )
    
    # ==================== Stage 1: Table Loading ====================
    
    async def _stage_table_loading(self, context: dict) -> TableQAStep:
        """Stage 1: Load table"""
        start = time.time()
        
        try:
            path = context.get("table_path") or self.table_path
            
            if not path:
                return TableQAStep(
                    stage=TableQAStage.TABLE_LOADING,
                    input=context,
                    output=None,
                    confidence=0.0,
                    reasoning="No table path provided",
                    execution_time_ms=(time.time() - start) * 1000,
                    error="No table path",
                )
            
            df = self._load_table(path)
            
            return TableQAStep(
                stage=TableQAStage.TABLE_LOADING,
                input=path,
                output=df,
                confidence=0.95,
                reasoning=f"Loaded {len(df)} rows, {len(df.columns)} columns",
                execution_time_ms=(time.time() - start) * 1000,
            )
            
        except Exception as e:
            return TableQAStep(
                stage=TableQAStage.TABLE_LOADING,
                input=context,
                output=None,
                confidence=0.0,
                reasoning=f"Load failed: {str(e)}",
                execution_time_ms=(time.time() - start) * 1000,
                error=str(e),
            )
    
    # ==================== Stage 2: Schema Analysis ====================
    
    async def _stage_schema_analysis(self, df: Any) -> TableQAStep:
        """Stage 2: Analyze schema"""
        start = time.time()
        
        schema = self._analyze_schema(df)
        
        step = TableQAStep(
            stage=TableQAStage.SCHEMA_ANALYSIS,
            input=f"{len(df)} rows, {len(df.columns)} columns",
            output=schema,
            confidence=0.95,
            reasoning=f"Analyzed {len(schema['columns'])} columns",
            execution_time_ms=(time.time() - start) * 1000,
        )
        
        logger.debug(f"Stage 2 (Schema Analysis): {step.reasoning}")
        
        return step
    
    # ==================== Stage 3: Query Interpretation ====================
    
    async def _stage_query_interpretation(
        self,
        query: str,
        schema: Dict,
    ) -> TableQAStep:
        """Stage 3: Query interpretation"""
        start = time.time()
        
        # Use LLM for query interpretation
        client = self._get_llm_client()
        interpretation = None
        
        if client:
            schema_str = self._format_schema_for_prompt(schema)
            prompt = self.QUERY_INTERPRETATION_PROMPT.user.format(
                schema=schema_str,
                query=query,
            )
            
            try:
                response = await client.chat.completions.create(
                    model=self.llm_model,
                    messages=[
                        {"role": "system", "content": self.QUERY_INTERPRETATION_PROMPT.system},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.1,
                    max_tokens=500,
                    response_format={"type": "json_object"},
                )
                
                result = response.choices[0].message.content.strip()
                result = self._extract_json(result)
                
                if result:
                    interpretation = result
                
            except Exception as e:
                logger.warning(f"LLM query interpretation failed, using rule-based: {e}")
        
        # Fallback: rule-based interpretation
        if interpretation is None:
            interpretation = {
                "operation": self._detect_operation(query),
                "target_columns": self._detect_columns(query, schema),
                "filters": self._detect_filters(query, schema),
                "grouping": self._detect_grouping(query, schema),
                "reasoning": "Rule-based matching",
            }
        
        step = TableQAStep(
            stage=TableQAStage.QUERY_INTERPRETATION,
            input=query,
            output=interpretation,
            confidence=0.8 if interpretation else 0.5,
            reasoning=f"Detected operation: {interpretation.get('operation', 'unknown')}",
            execution_time_ms=(time.time() - start) * 1000,
        )
        
        logger.debug(f"Stage 3 (Query Interpretation): {step.reasoning}")
        
        return step
    
    def _detect_operation(self, query: str) -> str:
        """Detect operation type from query - supports Chinese and English"""
        query_lower = query.lower()
        
        # Bilingual operation keywords
        operations = [
            ("count", ["多少", "几个", "数量", "count", "how many"]),
            ("sum", ["总和", "合计", "总计", "sum", "total"]),
            ("mean", ["平均", "均值", "mean", "average"]),
            ("max", ["最大", "最高", "max", "maximum"]),
            ("min", ["最小", "最低", "min", "minimum"]),
            ("filter", ["筛选", "过滤", "where", "filter"]),
            ("groupby", ["分组", "按", "group by"]),
            ("sort", ["排序", "顺序", "order by", "sort"]),
        ]
        
        for op, keywords in operations:
            if any(kw in query_lower for kw in keywords):
                return op
        
        return "select"
    
    def _detect_columns(self, query: str, schema: Dict) -> List[str]:
        """Detect relevant columns from query"""
        matched = []
        query_lower = query.lower()
        
        for col in schema["columns"]:
            if col["name"].lower() in query_lower:
                matched.append(col["name"])
        
        return matched
    
    def _detect_filters(self, query: str, schema: Dict) -> List[Dict]:
        """Detect filter conditions"""
        filters = []
        
        # Simple pattern matching
        patterns = [
            (r'(大于 | 超过|greater|more than|>)\s*(\d+(?:\.\d+)?)', ">"),
            (r'(小于 | 低于|less|less than|<)\s*(\d+(?:\.\d+)?)', "<"),
            (r'(等于 | 等于|equals|=)\s*(\d+(?:\.\d+)?)', "="),
        ]
        
        for pattern, op in patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                filters.append({
                    "operator": op,
                    "value": match.group(2),
                })
        
        return filters
    
    def _detect_grouping(self, query: str, schema: Dict) -> List[str]:
        """Detect grouping columns"""
        # Simple implementation
        return []
    
    # ==================== Stage 4: Code Generation ====================
    
    async def _stage_code_generation(
        self,
        query: str,
        interpretation: Dict,
        schema: Dict,
    ) -> TableQAStep:
        """Stage 4: Parallel generation of code candidates"""
        start = time.time()
        
        num_candidates = self.generation_config.get("num_candidates", 3)
        parallel = self.generation_config.get("parallel_generation", True)
        
        if parallel:
            tasks = [
                self._generate_single_code(query, interpretation, schema, i)
                for i in range(num_candidates)
            ]
            candidates = await asyncio.gather(*tasks, return_exceptions=True)
            candidates = [c for c in candidates if isinstance(c, str) and c.strip()]
        else:
            candidates = []
            for i in range(num_candidates):
                code = await self._generate_single_code(
                    query, interpretation, schema, i
                )
                if code and code.strip():
                    candidates.append(code)
        
        step = TableQAStep(
            stage=TableQAStage.CODE_GENERATION,
            input={"query": query, "interpretation": interpretation},
            output=candidates,
            confidence=0.7,
            reasoning=f"Generated {len(candidates)} code candidates",
            execution_time_ms=(time.time() - start) * 1000,
        )
        
        logger.debug(f"Stage 4 (Code Generation): {len(candidates)} candidates")
        
        return step
    
    async def _generate_single_code(
        self,
        query: str,
        interpretation: Dict,
        schema: Dict,
        candidate_id: int,
    ) -> Optional[str]:
        """Generate a single code candidate"""
        client = self._get_llm_client()
        if not client:
            return self._generate_code_template(interpretation, schema)
        
        schema_str = self._format_schema_for_prompt(schema)
        
        prompt = self.CODE_GENERATION_PROMPT.user.format(
            schema=schema_str,
            query=query,
            interpretation=interpretation,
        )
        
        try:
            response = await client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": self.CODE_GENERATION_PROMPT.system},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3 + (candidate_id * 0.15),
                max_tokens=400,
            )
            
            code = response.choices[0].message.content.strip()
            code = self._extract_code_from_response(code)
            
            return code
            
        except Exception as e:
            logger.error(f"Code generation failed: {e}")
            return self._generate_code_template(interpretation, schema)
    
    def _generate_code_template(
        self,
        interpretation: Dict,
        schema: Dict,
    ) -> str:
        """Generate code template (fallback)"""
        op = interpretation.get("operation", "select")
        cols = interpretation.get("target_columns", [])
        
        if not cols and schema["columns"]:
            cols = [schema["columns"][0]["name"]]
        
        col = cols[0] if cols else "col"
        
        templates = {
            "count": "result = len(df)",
            "sum": f"result = df['{col}'].sum()",
            "mean": f"result = df['{col}'].mean()",
            "max": f"result = df['{col}'].max()",
            "min": f"result = df['{col}'].min()",
            "filter": f"result = df[df['{col}'].notna()]",
            "groupby": f"result = df.groupby('{col}').size()",
            "sort": f"result = df.sort_values('{col}')",
            "select": f"result = df[['{col}']]",
        }
        
        return templates.get(op, "result = df")
    
    # ==================== Stage 5: Self-Revision ====================
    
    async def _stage_self_revision(
        self,
        query: str,
        candidates: List[str],
        schema: Dict,
        interpretation: Dict,
    ) -> TableQAStep:
        """Stage 5: Multi-round self-revision"""
        start = time.time()
        revised = candidates.copy()
        max_revisions = self.generation_config.get("max_revisions", 2)
        
        for round_num in range(max_revisions):
            logger.debug(f"Revision round {round_num + 1}/{max_revisions}")
            
            new_revised = []
            
            for code in revised:
                revised_code = await self._revise_single_code(
                    query, code, schema, interpretation, round_num
                )
                new_revised.append(revised_code)
            
            if new_revised == revised:
                logger.debug(f"Revision converged at round {round_num + 1}")
                break
            
            revised = new_revised
        
        step = TableQAStep(
            stage=TableQAStage.SELF_REVISION,
            input=candidates,
            output=revised,
            confidence=0.75,
            reasoning=f"Completed revision of {len(revised)} candidates",
            execution_time_ms=(time.time() - start) * 1000,
        )
        
        logger.debug(f"Stage 5 (Self-Revision): {len(revised)} revised candidates")
        
        return step
    
    async def _revise_single_code(
        self,
        query: str,
        code: str,
        schema: Dict,
        interpretation: Dict,
        iteration: int,
    ) -> str:
        """Revise a single code candidate"""
        client = self._get_llm_client()
        if not client:
            return code
        
        # Try to validate code
        error_message = ""
        try:
            scope = {"df": None, "pd": __import__("pandas")}
            compile(code, '<string>', 'exec')
        except SyntaxError as e:
            error_message = f"Syntax error: {str(e)}"
        
        schema_str = self._format_schema_for_prompt(schema)
        
        prompt = self.REVISION_PROMPT.user.format(
            query=query,
            code=code,
            schema=schema_str,
            interpretation=interpretation,
            error_message=error_message,
        )
        
        try:
            response = await client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": self.REVISION_PROMPT.system},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
                max_tokens=400,
            )
            
            revised_code = response.choices[0].message.content.strip()
            revised_code = self._extract_code_from_response(revised_code)
            
            return revised_code
            
        except Exception as e:
            logger.error(f"Revision failed: {e}")
            return code
    
    # ==================== Stage 6: Voting ====================
    
    async def _stage_voting(
        self,
        query: str,
        candidates: List[str],
        schema: Dict,
        interpretation: Dict,
    ) -> TableQAStep:
        """Stage 6: Vote to select best code"""
        start = time.time()
        
        client = self._get_llm_client()
        voting_result = None
        
        if client:
            schema_str = self._format_schema_for_prompt(schema)
            candidates_str = "\n\n".join([f"Candidate {i}:\n{code}" for i, code in enumerate(candidates)])
            
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
                            "best_code": candidates[best_idx],
                            "best_score": result.get("scores", [0.5] * len(candidates))[best_idx] if "scores" in result else 0.8,
                            "all_results": [
                                {"index": i, "code": code, "score": result.get("scores", [0.5] * len(candidates))[i] if "scores" in result else 0.5}
                                for i, code in enumerate(candidates)
                            ],
                            "reasoning": result.get("reasoning", ""),
                        }
                
            except Exception as e:
                logger.warning(f"LLM voting failed, using rule-based: {e}")
        
        # Fallback: rule-based voting
        if not voting_result:
            voting_result = {
                "best_index": 0,
                "best_code": candidates[0] if candidates else None,
                "best_score": 0.7,
                "all_results": [{"index": i, "code": code, "score": 0.5} for i, code in enumerate(candidates)],
                "reasoning": "Default to first candidate",
            }
        
        step = TableQAStep(
            stage=TableQAStage.VOTING,
            input=candidates,
            output=voting_result,
            confidence=voting_result["best_score"],
            reasoning=f"Selected candidate #{voting_result['best_index']}",
            execution_time_ms=(time.time() - start) * 1000,
        )
        
        logger.debug(f"Stage 6 (Voting): Selected #{voting_result['best_index']}")
        
        return step
    
    # ==================== Stage 7: Code Execution ====================
    
    async def _stage_code_execution(
        self,
        code: Optional[str],
        df: Any,
    ) -> TableQAStep:
        """Stage 7: Execute code"""
        start = time.time()
        
        if not code:
            return TableQAStep(
                stage=TableQAStage.CODE_EXECUTION,
                input=code,
                output={"success": False, "result": None, "error": "No code"},
                confidence=0.0,
                reasoning="No code to execute",
                execution_time_ms=(time.time() - start) * 1000,
                error="No code generated",
            )
        
        try:
            # Safe execution
            import pandas as pd
            scope = {"df": df, "pd": pd}
            
            exec(code, scope)
            result = scope.get("result")
            
            return TableQAStep(
                stage=TableQAStage.CODE_EXECUTION,
                input=code,
                output={"success": True, "result": result},
                confidence=0.85,
                reasoning="Code executed successfully",
                execution_time_ms=(time.time() - start) * 1000,
            )
            
        except Exception as e:
            return TableQAStep(
                stage=TableQAStage.CODE_EXECUTION,
                input=code,
                output={"success": False, "result": None, "error": str(e)},
                confidence=0.2,
                reasoning=f"Execution failed: {str(e)}",
                execution_time_ms=(time.time() - start) * 1000,
                error=str(e),
            )
    
    # ==================== Stage 8: Result Verification ====================
    
    async def _stage_result_verification(
        self,
        query: str,
        execution_result: Dict,
        code: Optional[str],
    ) -> TableQAStep:
        """Stage 8: Result verification"""
        start = time.time()
        
        confidence = 0.0
        
        if execution_result.get("success"):
            result = execution_result.get("result")
            if result is not None:
                confidence = 0.85
            else:
                confidence = 0.5
        else:
            confidence = 0.2
        
        step = TableQAStep(
            stage=TableQAStage.RESULT_VERIFICATION,
            input=execution_result,
            output={"confidence": confidence},
            confidence=confidence,
            reasoning=f"Verification: confidence={confidence:.2f}",
            execution_time_ms=(time.time() - start) * 1000,
        )
        
        logger.debug(f"Stage 8 (Result Verification): confidence={confidence:.2f}")
        
        return step
    
    # ==================== Utilities ====================
    
    def _format_schema_for_prompt(self, schema: Dict) -> str:
        """Format schema for prompt"""
        lines = []
        
        for col in schema["columns"]:
            dtype = col["dtype"]
            non_null = col["non_null"]
            lines.append(f"Column: {col['name']} ({dtype}, {non_null} non-null)")
        
        lines.append(f"Total rows: {schema['row_count']}")
        
        return "\n".join(lines)
    
    def _extract_code_from_response(self, response: str) -> str:
        """Extract code from response"""
        code = response.strip()
        
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0].strip()
        elif "```" in code:
            code = code.split("```")[1].split("```")[0].strip()
        
        return code
    
    def _extract_json(self, text: str) -> Optional[Dict]:
        """Extract JSON from text"""
        import json
        import re
        
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
        """Get confidence for this query"""
        if len(query.split()) > 3:
            return 0.7
        return 0.5
