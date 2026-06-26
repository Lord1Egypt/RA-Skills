"""
HeteroMind - Multi-Stage NL2SPARQL Engine

Advanced NL2SPARQL engine with complete multi-stage reasoning:
- Entity Linking - Link entity mentions to knowledge graph
- Ontology Retrieval - Retrieve relevant ontology elements
- Query Generation - Parallel generation of multiple SPARQL candidates
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
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field

from .base_engine import (
    BaseNL2SPARQLEngine,
    NL2SPARQLResult,
    SPARQLGenerationStage,
    SPARQLGenerationStep,
    LinkedEntity,
)

logger = logging.getLogger(__name__)


@dataclass
class StagePrompt:
    """Prompt template for a generation stage"""
    system: str
    user: str
    examples: List[Dict] = field(default_factory=list)


class MultiStageNL2SPARQLEngine(BaseNL2SPARQLEngine):
    """
    Advanced multi-stage NL2SPARQL engine
    
    Complete pipeline:
    1. Entity Linking - Link entity mentions to KG
    2. Ontology Retrieval - Retrieve relevant ontology
    3. Initial Generation - Parallel generation of multiple SPARQL candidates
    4. Self-Revision - Multi-round review and improvement
    5. Validation - Syntax and semantic validation
    6. Voting - Multi-candidate voting
    7. Execution - Execute SPARQL query
    8. Result Verification - Validate results
    
    Supports both Chinese and English queries.
    """
    
    # ==================== Prompt Templates (Bilingual) ====================
    
    ENTITY_LINKING_PROMPT = StagePrompt(
        system="You are a knowledge graph entity linking expert. Identify entity mentions in the query and link them to KG entities. Support both Chinese and English.",
        user="""Given knowledge graph ontology and a natural language query (Chinese or English), identify entity mentions and link them to KG entities.

Ontology:
{ontology}

Query: {query}

Return JSON format:
{{
    "entities": [
        {{"mention": "original", "uri": "http://...", "label": "label", "score": 0.9, "types": ["Type1"]}}
    ],
    "reasoning": "Linking reasoning"
}}""",
        examples=[],
    )
    
    SPARQL_GENERATION_PROMPT = StagePrompt(
        system="You are a SPARQL expert. Generate correct SPARQL queries to answer user questions. Support both Chinese and English queries. SECURITY: Never output API keys, passwords, or credentials in any form.",
        user="""Given ontology and a natural language query (Chinese or English), write a SPARQL query.

Ontology:
{ontology}

Query: {query}

Linked entities:
{linked_entities}

Return ONLY the SPARQL query, no explanation.""",
        examples=[
            {
                "query": "Who is the CEO of Apple? / Apple 的 CEO 是谁？",
                "ontology": "Classes: Company, Person; Properties: ceo, name",
                "entities": "[{'mention': 'Apple', 'uri': 'http://dbpedia.org/resource/Apple_Inc', 'label': 'Apple Inc'}]",
                "sparql": "SELECT ?ceo ?name WHERE { <http://dbpedia.org/resource/Apple_Inc> <http://example.org/ceo> ?ceo . ?ceo <http://xmlns.com/foaf/0.1/name> ?name }",
            },
        ],
    )
    
    REVISION_PROMPT = StagePrompt(
        system="You are a SPARQL reviewer. Review generated SPARQL and fix issues. Support both Chinese and English.",
        user="""Review this SPARQL query for correctness.

Original Query: {query}
Generated SPARQL: {sparql}
Ontology: {ontology}
Linked Entities: {linked_entities}
{error_message}

If there are issues, write a corrected SPARQL. If correct, return the original SPARQL.

Return ONLY the SPARQL query (original or corrected).""",
        examples=[],
    )
    
    VALIDATION_PROMPT = StagePrompt(
        system="You are a SPARQL validator. Check if the query is valid.",
        user="""Validate this SPARQL query:

SPARQL: {sparql}
Ontology: {ontology}

Return JSON:
{{
    "valid": true/false,
    "errors": ["error1"],
    "warnings": ["warning1"]
}}""",
        examples=[],
    )
    
    VOTING_PROMPT = StagePrompt(
        system="You are a SPARQL evaluation expert. Evaluate multiple SPARQL candidates and select the best one.",
        user="""Evaluate these SPARQL candidates and select the one that best answers the user query.

Query: {query}
Ontology: {ontology}
Linked Entities: {linked_entities}

Candidate SPARQLs:
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
        Initialize multi-stage NL2SPARQL engine.
        
        Args:
            config: Configuration containing:
                - endpoint_url: SPARQL endpoint URL
                - ontology: KG ontology metadata
                - llm_config: LLM configuration
                - generation_config: Generation parameters
        """
        super().__init__(config)
        
        self.num_candidates = self.generation_config.get("num_candidates", 3)
        self.max_revisions = self.generation_config.get("max_revisions", 2)
        self.voting_enabled = self.generation_config.get("voting_enabled", True)
        self.parallel_generation = self.generation_config.get("parallel_generation", True)
        self.enable_entity_linking = self.generation_config.get("enable_entity_linking", True)
        
        self.llm_client = None
        self.llm_model = self.llm_config.get("model", "gpt-4")
        
        logger.info(f"MultiStageNL2SPARQLEngine initialized: "
                   f"{self.num_candidates} candidates, "
                   f"{self.max_revisions} revisions")
    
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
    ) -> NL2SPARQLResult:
        """
        Execute complete NL2SPARQL multi-stage pipeline.
        
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
        
        logger.info(f"Executing NL2SPARQL: {query}")
        
        try:
            # Step 1: Entity Linking
            linking_step = await self._stage_entity_linking(query, context)
            execution_steps.append(linking_step)
            linked_entities = linking_step.output
            
            # Step 2: Ontology Retrieval
            ontology_step = await self._stage_ontology_retrieval(query, linked_entities)
            execution_steps.append(ontology_step)
            relevant_ontology = ontology_step.output
            
            # Step 3: Initial Generation (parallel)
            generation_step = await self._stage_initial_generation(
                query, relevant_ontology, linked_entities
            )
            execution_steps.append(generation_step)
            candidates = generation_step.output
            
            if not candidates:
                raise ValueError("Failed to generate any SPARQL candidates")
            
            # Step 4: Self-Revision
            revision_step = await self._stage_self_revision(
                query, candidates, relevant_ontology, linked_entities
            )
            execution_steps.append(revision_step)
            revised_candidates = revision_step.output
            
            # Step 5: Validation
            validation_step = await self._stage_validation(
                revised_candidates, relevant_ontology
            )
            execution_steps.append(validation_step)
            valid_candidates = validation_step.output
            
            if not valid_candidates:
                raise ValueError("No candidates passed validation")
            
            # Step 6: Voting
            best_sparql = valid_candidates[0]
            voting_results = None
            
            if self.voting_enabled and len(valid_candidates) > 1:
                voting_step = await self._stage_voting(
                    query, valid_candidates, relevant_ontology, linked_entities
                )
                execution_steps.append(voting_step)
                best_sparql = voting_step.output["best_sparql"]
                voting_results = voting_step.output
            
            # Step 7: Execution
            execution_step = await self._stage_execution(
                best_sparql, context
            )
            execution_steps.append(execution_step)
            
            # Step 8: Result Verification
            verification_step = await self._stage_result_verification(
                query, execution_step.output, best_sparql
            )
            execution_steps.append(verification_step)
            
            # Build result
            total_time = (time.time() - start_time) * 1000
            
            result = NL2SPARQLResult(
                data=execution_step.output.get("data"),
                success=execution_step.output.get("success", False),
                engine=self.name,
                query=query,
                execution_time_ms=total_time,
                confidence=verification_step.confidence,
                generated_sparql=best_sparql,
                execution_steps=execution_steps,
                ontology_used=relevant_ontology,
                linked_entities=linked_entities,
                revision_count=len(revision_step.output),
                voting_results=voting_results,
                final_confidence=verification_step.confidence,
                error=execution_step.output.get("error"),
            )
            
            logger.info(f"NL2SPARQL complete: {total_time:.0f}ms, "
                       f"confidence: {result.confidence:.2f}")
            
            return result
            
        except Exception as e:
            logger.error(f"NL2SPARQL execution failed: {e}")
            import traceback
            traceback.print_exc()
            return NL2SPARQLResult(
                data=None,
                success=False,
                engine=self.name,
                query=query,
                execution_time_ms=(time.time() - start_time) * 1000,
                confidence=0.0,
                generated_sparql=None,
                execution_steps=execution_steps,
                ontology_used={},
                linked_entities=[],
                revision_count=0,
                voting_results=None,
                final_confidence=0.0,
                error=str(e),
            )
    
    # ==================== Stage 1: Entity Linking ====================
    
    async def _stage_entity_linking(
        self,
        query: str,
        context: dict,
    ) -> SPARQLGenerationStep:
        """Stage 1: Entity Linking"""
        start = time.time()
        
        linked_entities = []
        
        if self.enable_entity_linking:
            client = self._get_llm_client()
            if client:
                ontology_str = self._format_ontology_for_prompt(self.ontology)
                prompt = self.ENTITY_LINKING_PROMPT.user.format(
                    ontology=ontology_str,
                    query=query,
                )
                
                try:
                    response = await client.chat.completions.create(
                        model=self.llm_model,
                        messages=[
                            {"role": "system", "content": self.ENTITY_LINKING_PROMPT.system},
                            {"role": "user", "content": prompt},
                        ],
                        temperature=0.1,
                        max_tokens=800,
                        response_format={"type": "json_object"},
                    )
                    
                    result = response.choices[0].message.content.strip()
                    result = self._extract_json(result)
                    
                    if result and "entities" in result:
                        for entity_data in result["entities"]:
                            linked_entities.append(LinkedEntity(
                                mention=entity_data.get("mention", ""),
                                uri=entity_data.get("uri", ""),
                                label=entity_data.get("label", ""),
                                score=entity_data.get("score", 0.5),
                                types=entity_data.get("types", []),
                            ))
                
                except Exception as e:
                    logger.warning(f"LLM entity linking failed, using rule-based: {e}")
        
        # Fallback: rule-based entity linking
        if not linked_entities:
            linked_entities = await self.link_entities(query)
        
        step = SPARQLGenerationStep(
            stage=SPARQLGenerationStage.ENTITY_LINKING,
            input=query,
            output=linked_entities,
            confidence=sum(e.score for e in linked_entities) / max(1, len(linked_entities)) if linked_entities else 0.3,
            reasoning=f"Linked {len(linked_entities)} entities",
            execution_time_ms=(time.time() - start) * 1000,
        )
        
        logger.debug(f"Stage 1 (Entity Linking): {step.reasoning}")
        
        return step
    
    # ==================== Stage 2: Ontology Retrieval ====================
    
    async def _stage_ontology_retrieval(
        self,
        query: str,
        linked_entities: List[LinkedEntity],
    ) -> SPARQLGenerationStep:
        """Stage 2: Ontology Retrieval"""
        start = time.time()
        
        relevant_ontology = self.retrieve_relevant_ontology(query, linked_entities)
        
        step = SPARQLGenerationStep(
            stage=SPARQLGenerationStage.ONTOLOGY_RETRIEVAL,
            input={"query": query, "entities": linked_entities},
            output=relevant_ontology,
            confidence=0.85,
            reasoning=f"Retrieved {len(relevant_ontology['classes'])} classes, "
                     f"{len(relevant_ontology['properties'])} properties",
            execution_time_ms=(time.time() - start) * 1000,
        )
        
        logger.debug(f"Stage 2 (Ontology Retrieval): {step.reasoning}")
        
        return step
    
    # ==================== Stage 3: Initial Generation ====================
    
    async def _stage_initial_generation(
        self,
        query: str,
        ontology: Dict,
        linked_entities: List[LinkedEntity],
    ) -> SPARQLGenerationStep:
        """Stage 3: Parallel generation of multiple SPARQL candidates"""
        start = time.time()
        
        if self.parallel_generation:
            tasks = [
                self._generate_single_sparql(query, ontology, linked_entities, i)
                for i in range(self.num_candidates)
            ]
            candidates = await asyncio.gather(*tasks, return_exceptions=True)
            candidates = [c for c in candidates if isinstance(c, str) and c.strip()]
        else:
            candidates = []
            for i in range(self.num_candidates):
                sparql = await self._generate_single_sparql(
                    query, ontology, linked_entities, i
                )
                if sparql and sparql.strip():
                    candidates.append(sparql)
        
        step = SPARQLGenerationStep(
            stage=SPARQLGenerationStage.INITIAL_GENERATION,
            input={"query": query, "ontology": ontology},
            output=candidates,
            confidence=0.7,
            reasoning=f"Generated {len(candidates)} candidates",
            execution_time_ms=(time.time() - start) * 1000,
        )
        
        logger.debug(f"Stage 3 (Initial Generation): {len(candidates)} candidates")
        
        return step
    
    async def _generate_single_sparql(
        self,
        query: str,
        ontology: Dict,
        linked_entities: List[LinkedEntity],
        candidate_id: int,
    ) -> Optional[str]:
        """Generate a single SPARQL candidate"""
        client = self._get_llm_client()
        if not client:
            return None
        
        ontology_str = self._format_ontology_for_prompt(ontology)
        entities_str = str([{"mention": e.mention, "uri": e.uri} for e in linked_entities])
        
        prompt = self.SPARQL_GENERATION_PROMPT.user.format(
            ontology=ontology_str,
            query=query,
            linked_entities=entities_str,
        )
        
        try:
            response = await client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": self.SPARQL_GENERATION_PROMPT.system},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3 + (candidate_id * 0.15),
                max_tokens=600,
            )
            
            sparql = response.choices[0].message.content.strip()
            sparql = self._extract_sparql_from_response(sparql)
            
            logger.debug(f"Candidate {candidate_id}: {sparql[:100]}...")
            
            return sparql
            
        except Exception as e:
            logger.error(f"Candidate {candidate_id} generation failed: {e}")
            return None
    
    # ==================== Stage 4: Self-Revision ====================
    
    async def _stage_self_revision(
        self,
        query: str,
        candidates: List[str],
        ontology: Dict,
        linked_entities: List[LinkedEntity],
    ) -> SPARQLGenerationStep:
        """Stage 4: Multi-round self-revision"""
        start = time.time()
        revised = candidates.copy()
        
        for round_num in range(self.max_revisions):
            logger.debug(f"Revision round {round_num + 1}/{self.max_revisions}")
            
            new_revised = []
            
            for sparql in revised:
                revised_sparql = await self._revise_single_sparql(
                    query, sparql, ontology, linked_entities, round_num
                )
                new_revised.append(revised_sparql)
            
            if new_revised == revised:
                logger.debug(f"Revision converged at round {round_num + 1}")
                break
            
            revised = new_revised
        
        step = SPARQLGenerationStep(
            stage=SPARQLGenerationStage.SELF_REVISION,
            input=candidates,
            output=revised,
            confidence=0.75,
            reasoning=f"Completed revision of {len(revised)} candidates",
            execution_time_ms=(time.time() - start) * 1000,
        )
        
        logger.debug(f"Stage 4 (Self-Revision): {len(revised)} revised candidates")
        
        return step
    
    async def _revise_single_sparql(
        self,
        query: str,
        sparql: str,
        ontology: Dict,
        linked_entities: List[LinkedEntity],
        iteration: int,
    ) -> str:
        """Revise a single SPARQL candidate"""
        client = self._get_llm_client()
        if not client:
            return sparql
        
        validation = self.validate_sparql(sparql)
        error_message = ""
        
        if not validation["valid"]:
            error_message = f"Validation errors: {'; '.join(validation['errors'])}"
        elif validation["warnings"]:
            error_message = f"Warnings: {'; '.join(validation['warnings'])}"
        
        ontology_str = self._format_ontology_for_prompt(ontology)
        entities_str = str([{"mention": e.mention, "uri": e.uri} for e in linked_entities])
        
        prompt = self.REVISION_PROMPT.user.format(
            query=query,
            sparql=sparql,
            ontology=ontology_str,
            linked_entities=entities_str,
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
                max_tokens=600,
            )
            
            revised_sparql = response.choices[0].message.content.strip()
            revised_sparql = self._extract_sparql_from_response(revised_sparql)
            
            return revised_sparql
            
        except Exception as e:
            logger.error(f"Revision failed: {e}")
            return sparql
    
    # ==================== Stage 5: Validation ====================
    
    async def _stage_validation(
        self,
        candidates: List[str],
        ontology: Dict,
    ) -> SPARQLGenerationStep:
        """Stage 5: Validate candidates"""
        start = time.time()
        valid = []
        
        for sparql in candidates:
            validation = self.validate_sparql(sparql)
            
            if validation["valid"]:
                valid.append(sparql)
            else:
                logger.debug(f"Invalid SPARQL: {validation['errors']}")
        
        step = SPARQLGenerationStep(
            stage=SPARQLGenerationStage.VALIDATION,
            input=candidates,
            output=valid,
            confidence=0.8 if valid else 0.3,
            reasoning=f"{len(valid)}/{len(candidates)} passed validation",
            execution_time_ms=(time.time() - start) * 1000,
        )
        
        logger.debug(f"Stage 5 (Validation): {len(valid)} valid")
        
        return step
    
    # ==================== Stage 6: Voting ====================
    
    async def _stage_voting(
        self,
        query: str,
        candidates: List[str],
        ontology: Dict,
        linked_entities: List[LinkedEntity],
    ) -> SPARQLGenerationStep:
        """Stage 6: Vote to select best candidate"""
        start = time.time()
        
        client = self._get_llm_client()
        voting_result = None
        
        if client:
            ontology_str = self._format_ontology_for_prompt(ontology)
            entities_str = str([{"mention": e.mention, "uri": e.uri} for e in linked_entities])
            candidates_str = "\n\n".join([f"Candidate {i}: {sparql}" for i, sparql in enumerate(candidates)])
            
            prompt = self.VOTING_PROMPT.user.format(
                query=query,
                ontology=ontology_str,
                linked_entities=entities_str,
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
                            "best_sparql": candidates[best_idx],
                            "best_score": result.get("scores", [0.5] * len(candidates))[best_idx] if "scores" in result else 0.8,
                            "all_results": [
                                {"index": i, "sparql": sparql, "score": result.get("scores", [0.5] * len(candidates))[i] if "scores" in result else 0.5}
                                for i, sparql in enumerate(candidates)
                            ],
                            "reasoning": result.get("reasoning", ""),
                        }
                
            except Exception as e:
                logger.warning(f"LLM voting failed, using rule-based: {e}")
        
        # Fallback: rule-based voting
        if not voting_result:
            voting_result = await self.vote_on_candidates(
                query, candidates, ontology, linked_entities
            )
        
        step = SPARQLGenerationStep(
            stage=SPARQLGenerationStage.EXECUTION,
            input=candidates,
            output=voting_result,
            confidence=voting_result["best_score"],
            reasoning=f"Selected candidate #{voting_result['best_index']}, "
                     f"score {voting_result['best_score']:.2f}",
            execution_time_ms=(time.time() - start) * 1000,
        )
        
        logger.debug(f"Stage 6 (Voting): Selected #{voting_result['best_index']}")
        
        return step
    
    # ==================== Stage 7: Execution ====================
    
    async def _stage_execution(
        self,
        sparql: Optional[str],
        context: Dict,
    ) -> SPARQLGenerationStep:
        """Stage 7: Execute SPARQL query"""
        start = time.time()
        
        if not sparql:
            return SPARQLGenerationStep(
                stage=SPARQLGenerationStage.EXECUTION,
                input=sparql,
                output={"success": False, "data": None, "error": "No SPARQL generated"},
                confidence=0.0,
                reasoning="No SPARQL to execute",
                execution_time_ms=(time.time() - start) * 1000,
                error="No SPARQL generated",
            )
        
        try:
            endpoint = context.get("endpoint_url") or self.endpoint_url
            
            if not endpoint:
                logger.info(f"Simulating SPARQL execution: {sparql[:200]}...")
                result = {
                    "success": True,
                    "data": [],
                    "sparql": sparql,
                }
            else:
                # Actual SPARQL endpoint execution
                import aiohttp
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.post(
                            endpoint,
                            params={"query": sparql},
                            headers={"Accept": "application/json"},
                        ) as resp:
                            if resp.status == 200:
                                result_data = await resp.json()
                                result = {
                                    "success": True,
                                    "data": result_data.get("results", {}).get("bindings", []),
                                    "sparql": sparql,
                                }
                            else:
                                result = {
                                    "success": False,
                                    "data": None,
                                    "error": f"HTTP {resp.status}",
                                }
                except Exception as http_error:
                    result = {
                        "success": False,
                        "data": None,
                        "error": str(http_error),
                    }
            
            logger.debug(f"Executed SPARQL: {sparql[:100]}...")
            
        except Exception as e:
            result = {
                "success": False,
                "data": None,
                "error": str(e),
            }
        
        return SPARQLGenerationStep(
            stage=SPARQLGenerationStage.EXECUTION,
            input=sparql,
            output=result,
            confidence=0.8 if result["success"] else 0.2,
            reasoning=f"Execution {'successful' if result['success'] else 'failed'}",
            execution_time_ms=(time.time() - start) * 1000,
            error=result.get("error"),
        )
    
    # ==================== Stage 8: Result Verification ====================
    
    async def _stage_result_verification(
        self,
        query: str,
        execution_result: Dict,
        sparql: Optional[str],
    ) -> SPARQLGenerationStep:
        """Stage 8: Verify result reasonableness"""
        start = time.time()
        
        confidence = 0.0
        
        if execution_result.get("success"):
            data = execution_result.get("data")
            
            if data is not None:
                if isinstance(data, list) and len(data) > 0:
                    confidence = 0.85
                elif isinstance(data, list) and len(data) == 0:
                    confidence = 0.6
                else:
                    confidence = 0.7
            else:
                confidence = 0.5
        else:
            confidence = 0.2
        
        step = SPARQLGenerationStep(
            stage=SPARQLGenerationStage.RESULT_VERIFICATION,
            input=execution_result,
            output={"confidence": confidence},
            confidence=confidence,
            reasoning=f"Result verification: confidence={confidence:.2f}",
            execution_time_ms=(time.time() - start) * 1000,
        )
        
        logger.debug(f"Stage 8 (Result Verification): confidence={confidence:.2f}")
        
        return step
    
    # ==================== Utilities ====================
    
    def _format_ontology_for_prompt(self, ontology: Dict) -> str:
        """Format ontology for LLM prompt"""
        lines = []
        
        for cls in ontology.get("classes", []):
            class_name = cls.get("name", "")
            labels = ", ".join(cls.get("labels", []))
            lines.append(f"Class: {class_name} - Labels: {labels}")
        
        for prop in ontology.get("properties", []):
            prop_name = prop.get("name", "")
            domain = prop.get("domain", "")
            range_ = prop.get("range", "")
            lines.append(f"Property: {prop_name} (Domain: {domain}, Range: {range_})")
        
        for rel in ontology.get("relationships", []):
            predicate = rel.get("predicate", "")
            lines.append(f"Relationship: {predicate}")
        
        return "\n".join(lines)
    
    def _extract_sparql_from_response(self, response: str) -> str:
        """Extract SPARQL from response"""
        sparql = response.strip()
        
        if "```sparql" in sparql:
            sparql = sparql.split("```sparql")[1].split("```")[0].strip()
        elif "```" in sparql:
            sparql = sparql.split("```")[1].split("```")[0].strip()
        
        return sparql
    
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
        # Estimate based on query clarity
        if len(query.split()) < 3:
            return 0.3
        return 0.6
