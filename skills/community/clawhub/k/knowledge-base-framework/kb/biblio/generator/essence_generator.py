#!/usr/bin/env python3
"""
EssenzGenerator - LLM-powered Essence Extraction

Generates structured essences from Knowledge Base content using LLM.
Features:
- Single and batch essence generation
- Differential essence updates (update with new content)
- Prompt engineering with configurable templates
- Async methods with retry logic
- Hotspot scoring (how many existing essences are touched)
- Progress logging for batch operations
- Integration with LLMContentManager for persistence
"""

import asyncio
import json
import hashlib
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any

from kb.biblio.config import LLMConfig, get_llm_config
from kb.biblio.engine.base import LLMResponse, LLMProvider
from kb.biblio.engine import OllamaEngine, OllamaEngineError
from kb.biblio.engine.registry import EngineRegistry, EngineRegistryError, get_engine_registry
from kb.biblio.content_manager import LLMContentManager
from kb.biblio.generator.parallel_mixin import (
    ParallelMixin, ParallelResult, ParallelStrategy, DiffResult,
)
from kb.base.logger import KBLogger, get_logger

logger = get_logger("kb.llm.generator.essence")


class EssenzGeneratorError(Exception):
    """Error in essence generation operations."""
    pass


class EssenzGenerationResult:
    """
    Result of a single essence generation.
    
    Attributes:
        topic: The topic this essence covers
        success: Whether generation succeeded
        essence_path: Path to saved essence file (None if failed)
        essence_hash: Hash identifier for the essence
        source_files: List of source files used
        model_used: LLM model used for generation
        duration_ms: Generation time in milliseconds
        version: Essence version (incremented on updates)
        hotspot_score: How many other essences reference overlapping content
        error: Error message if generation failed
    """
    
    def __init__(
        self,
        topic: str,
        success: bool,
        *,
        essence_path: Optional[Path] = None,
        essence_hash: Optional[str] = None,
        source_files: Optional[List[str]] = None,
        model_used: Optional[str] = None,
        duration_ms: int = 0,
        version: int = 1,
        hotspot_score: int = 0,
        error: Optional[str] = None,
    ):
        self.topic = topic
        self.success = success
        self.essence_path = essence_path
        self.essence_hash = essence_hash
        self.source_files = source_files or []
        self.model_used = model_used
        self.duration_ms = duration_ms
        self.version = version
        self.hotspot_score = hotspot_score
        self.error = error
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "topic": self.topic,
            "success": self.success,
            "essence_path": str(self.essence_path) if self.essence_path else None,
            "essence_hash": self.essence_hash,
            "source_files": self.source_files,
            "model_used": self.model_used,
            "duration_ms": self.duration_ms,
            "version": self.version,
            "hotspot_score": self.hotspot_score,
            "error": self.error,
        }


class EssenzGenerator(ParallelMixin):
    """
    LLM-powered Essence Generator with parallel engine support.
    
    Generates structured essences (summaries, key points, cross-references,
    open questions) from Knowledge Base content.
    
    Supports parallel generation strategies when parallel_mode is enabled:
    - primary_first: Primary engine runs; secondary on failure (fallback)
    - aggregate: Both engines generate; results are combined (union)
    - compare: Both engines generate; diff-view + merge if complementary
    
    Usage:
        generator = EssenzGenerator()
        
        # Single essence
        result = await generator.generate_essence(
            topic="Machine Learning",
            source_files=["/path/to/ml_notes.pdf", "/path/to/ml_intro.md"]
        )
        
        # Parallel essence (when parallel_mode=True in config)
        result = await generator.generate_essence_parallel(
            topic="Machine Learning",
            source_files=["/path/to/ml_notes.pdf"],
            strategy="compare",  # or "primary_first", "aggregate"
        )
        
        # Batch
        results = await generator.generate_essences_batch([
            ("ML Basics", ["ml_intro.pdf"]),
            ("Neural Networks", ["nn_chapter.pdf", "nn_notes.md"]),
        ])
        
        # Differential update
        result = await generator.update_essence_with_new_content(
            essence_id="abc123",
            new_files=["new_ml_research.pdf"]
        )
    """
    
    def __init__(
        self,
        llm_config: Optional[LLMConfig] = None,
        engine: Optional[OllamaEngine] = None,
        content_manager: Optional[LLMContentManager] = None,
        registry: Optional[EngineRegistry] = None,
    ):
        self._config = llm_config or get_llm_config()
        self._engine = engine or OllamaEngine.get_instance()
        self._content_manager = content_manager or LLMContentManager()
        self._template = self._load_template()
        
        # Initialize parallel mixin support
        self.__init_parallel__(llm_config)
        if registry is not None:
            self._parallel_registry = registry
        
        logger.info(
            "EssenzGenerator initialized",
            extra={
                "model": self._config.model,
                "parallel_mode": self._config.parallel_mode,
                "parallel_strategy": self._config.parallel_strategy,
            }
        )
    
    # --- Template Loading ---
    
    def _load_template(self) -> str:
        """Load the essence prompt template."""
        template_path = self._config.templates_path / "essence_template.md"
        
        if template_path.exists():
            return template_path.read_text(encoding="utf-8")
        
        logger.warning(
            f"Essence template not found at {template_path}, using default"
        )
        return self._default_template()
    
    @staticmethod
    def _default_template() -> str:
        """Fallback template if file is missing."""
        return """# {{ title }}

## Zusammenfassung

{{ summary }}

## Kernpunkte

{% for point in key_points %}
- {{ point }}
{% endfor %}

## Entitäten

{% for entity in entities %}
- {{ entity }}
{% endfor %}

## Beziehungen

{% for rel in relationships %}
- **{{ rel.from }}** → {{ rel.type }} → **{{ rel.to }}**
{% endfor %}

## Keywords

{{ keywords | join(", ") }}

---

*Extracted: {{ extracted_at }} | Model: {{ model }}*"""
    
    # --- Content Reading ---
    
    def _read_source_files(self, source_files: List[str]) -> str:
        """
        Read content from source files.
        
        Args:
            source_files: List of file paths to read
            
        Returns:
            Concatenated content from all files
        """
        contents = []
        total_bytes = 0
        max_total_bytes = 500_000  # ~500KB limit to avoid overwhelming context
        
        for file_path_str in source_files:
            file_path = Path(file_path_str)
            
            if not file_path.exists():
                logger.warning(f"Source file not found: {file_path}")
                contents.append(f"[FEHLER: Datei nicht gefunden: {file_path_str}]")
                continue
            
            if not file_path.is_file():
                logger.warning(f"Not a file: {file_path}")
                continue
            
            try:
                content = file_path.read_text(encoding="utf-8", errors="replace")
                file_size = len(content.encode("utf-8"))
                
                if total_bytes + file_size > max_total_bytes:
                    # Truncate to fit
                    remaining = max_total_bytes - total_bytes
                    content = content[:remaining] + "\n... [abgeschnitten wegen Größenlimit]"
                    logger.warning(
                        f"Truncated source file: {file_path}",
                        extra={"original_size": file_size, "remaining": remaining}
                    )
                
                contents.append(f"--- Quelle: {file_path.name} ---\n{content}")
                total_bytes += len(content.encode("utf-8"))
                
            except Exception as e:
                logger.warning(f"Failed to read source file {file_path}: {e}")
                contents.append(f"[FEHLER beim Lesen: {file_path_str}: {e}]")
        
        return "\n\n".join(contents)
    
    # --- Prompt Building ---
    
    def _build_essence_prompt(
        self,
        topic: str,
        source_content: str,
        existing_essence: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Build the LLM prompt for essence generation.
        
        Args:
            topic: The topic to generate essence for
            source_content: Concatenated content from source files
            existing_essence: If provided, includes previous essence for differential update
            
        Returns:
            Formatted prompt string
        """
        prompt_parts = [
            "Du bist ein Wissensmanagement-Assistent. Deine Aufgabe ist es, "
            "eine strukturierte Essenz aus den folgenden Quellen zu einem "
            "bestimmten Thema zu extrahieren.\n",
            f"## Thema: {topic}\n",
            "## Anforderungen an die Essenz:\n",
            "1. **Zusammenfassung**: Eine prägnante Zusammenfassung des Themas (2-3 Sätze)\n",
            "2. **Kernpunkte**: Die wichtigsten Erkenntnisse/Thesen als Bullet-Points (5-10 Punkte)\n",
            "3. **Verknüpfungen**: Querverbindungen zu anderen Konzepten oder Domänen\n",
            "4. **Widersprüche**: Identifizierte Widersprüche oder Spannungen zwischen Quellen\n",
            "5. **Offene Fragen**: Ungeklärte Fragen, die weitere Recherche erfordern\n",
            "6. **Entitäten**: Benannte Entitäten (Personen, Orte, Konzepte, Organisationen)\n",
            "7. **Beziehungen**: Beziehungen zwischen Entitäten (from → type → to)\n",
            "8. **Keywords**: Suchbegriffe für die Indexierung\n\n",
            "## Ausgabeformat (JSON):\n",
            "```json\n",
            '{\n',
            '  "summary": "...",\n',
            '  "key_points": ["...", "..."],\n',
            '  "connections": ["...", "..."],\n',
            '  "contradictions": ["...", "..."],\n',
            '  "open_questions": ["...", "..."],\n',
            '  "entities": ["...", "..."],\n',
            '  "relationships": [{"from": "...", "type": "...", "to": "..."}],\n',
            '  "keywords": ["...", "..."]\n',
            '}\n',
            "```\n\n",
            "Antworte AUSSCHLIESSLICH mit gültigem JSON. Kein Markdown, kein Text davor oder danach.\n\n",
        ]
        
        if existing_essence:
            prompt_parts.append(
                "## Bestehende Essenz (aktualisieren):\n"
                f"Version: {existing_essence.get('version', 1)}\n"
                f"Zusammenfassung: {existing_essence.get('summary', '')}\n"
                f"Kernpunkte: {json.dumps(existing_essence.get('key_points', []), ensure_ascii=False)}\n\n"
                "Integriere die neuen Informationen in die bestehende Essenz. "
                "Aktualisiere Zusammenfassung und Kernpunkte, füge neue Erkenntnisse hinzu, "
                "und markiere Widersprüche zwischen alter und neuer Essenz.\n\n"
            )
        
        prompt_parts.append(
            f"## Quellinhalt:\n\n{source_content}\n\n"
            "Generiere nun die Essenz als JSON."
        )
        
        return "".join(prompt_parts)
    
    # --- LLM Response Parsing ---
    
    def _parse_essence_json(self, raw_response: str) -> Dict[str, Any]:
        """
        Parse JSON from LLM response.
        
        Handles cases where the model wraps JSON in markdown code blocks
        or adds extra text.
        
        Args:
            raw_response: Raw LLM response text
            
        Returns:
            Parsed essence dictionary
            
        Raises:
            EssenzGeneratorError: If JSON cannot be parsed
        """
        # Strip whitespace
        text = raw_response.strip()
        
        # Try to extract JSON from code blocks
        if "```json" in text:
            start = text.index("```json") + 7
            end = text.find("```", start)
            if end > start:
                text = text[start:end].strip()
        elif "```" in text:
            start = text.index("```") + 3
            end = text.find("```", start)
            if end > start:
                text = text[start:end].strip()
        
        # Try to find JSON object boundaries
        if "{" in text:
            start = text.index("{")
            # Find matching closing brace
            depth = 0
            for i in range(start, len(text)):
                if text[i] == "{":
                    depth += 1
                elif text[i] == "}":
                    depth -= 1
                    if depth == 0:
                        text = text[start:i + 1]
                        break
        
        try:
            data = json.loads(text)
            return self._validate_essence_data(data)
        except json.JSONDecodeError as e:
            raise EssenzGeneratorError(
                f"Failed to parse LLM response as JSON: {e}\n"
                f"Raw response (first 500 chars): {raw_response[:500]}"
            )
    
    def _validate_essence_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and normalize essence data.
        
        Ensures all required fields exist with sensible defaults.
        """
        defaults = {
            "summary": "",
            "key_points": [],
            "connections": [],
            "contradictions": [],
            "open_questions": [],
            "entities": [],
            "relationships": [],
            "keywords": [],
        }
        
        result = {}
        for key, default in defaults.items():
            value = data.get(key, default)
            # Ensure lists are actually lists
            if isinstance(default, list) and not isinstance(value, list):
                if isinstance(value, str):
                    value = [value]
                else:
                    value = default
            result[key] = value
        
        return result
    
    # --- Hotspot Scoring ---
    
    async def _compute_hotspot_score(
        self,
        source_files: List[str],
    ) -> int:
        """
        Compute hotspot score: how many existing essences reference
        overlapping source files.
        
        Args:
            source_files: List of source file paths
            
        Returns:
            Number of existing essences with overlapping sources
        """
        existing_essences = await self._content_manager.list_essences(limit=1000)
        
        if not existing_essences:
            return 0
        
        source_set = set(Path(f).resolve() for f in source_files if Path(f).exists())
        
        if not source_set:
            return 0
        
        score = 0
        
        for essence_info in existing_essences:
            essence_hash = essence_info.get("hash")
            if not essence_hash:
                continue
            
            json_path = self._config.essences_path / essence_hash / "essence.json"
            if not json_path.exists():
                continue
            
            try:
                data = json.loads(json_path.read_text(encoding="utf-8"))
                essence_source = data.get("source_path")
                
                if essence_source:
                    resolved = Path(essence_source).resolve()
                    if resolved in source_set:
                        score += 1
                        
            except (json.JSONDecodeError, IOError):
                continue
        
        return score
    
    # --- Retry Logic ---
    
    async def _generate_with_retry(
        self,
        prompt: str,
        max_retries: Optional[int] = None,
    ) -> LLMResponse:
        """
        Generate LLM response with retry logic and exponential backoff.
        
        Args:
            prompt: The prompt to send
            max_retries: Override config max_retries
            
        Returns:
            LLMResponse on success
            
        Raises:
            EssenzGeneratorError: After all retries exhausted
        """
        retries = max_retries if max_retries is not None else self._config.max_retries
        last_error = None
        
        for attempt in range(retries):
            try:
                response = await self._engine.generate_async(prompt)
                
                if response.success and response.content:
                    return response
                
                # Empty response - treat as transient
                last_error = EssenzGeneratorError(
                    f"Empty LLM response (attempt {attempt + 1}/{retries})"
                )
                logger.warning(
                    f"Empty LLM response, retrying",
                    extra={"attempt": attempt + 1, "retries": retries}
                )
                
            except OllamaEngineError as e:
                last_error = EssenzGeneratorError(f"LLM engine error: {e}")
                logger.warning(
                    f"LLM engine error, retrying",
                    extra={
                        "attempt": attempt + 1,
                        "retries": retries,
                        "error": str(e)
                    }
                )
            
            except Exception as e:
                last_error = EssenzGeneratorError(f"Unexpected error: {e}")
                logger.error(
                    f"Unexpected error during generation",
                    extra={
                        "attempt": attempt + 1,
                        "error": str(e)
                    }
                )
            
            # Exponential backoff
            if attempt < retries - 1:
                delay = self._config.retry_delay * (2 ** attempt)
                logger.info(f"Retrying in {delay:.1f}s", extra={"attempt": attempt + 1})
                await asyncio.sleep(delay)
        
        raise EssenzGeneratorError(
            f"All {retries} retries exhausted. Last error: {last_error}"
        )
    
    # --- Core Generation Methods ---
    
    async def generate_essence(
        self,
        topic: str,
        source_files: List[str],
        *,
        tags: Optional[List[str]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> EssenzGenerationResult:
        """
        Generate an essence for a topic from source files.
        
        Reads KB content from the provided source files, sends to LLM
        for structured extraction, and saves the result via ContentManager.
        
        Args:
            topic: The topic to generate an essence for
            source_files: List of file paths to read as source content
            tags: Optional tags for categorization
            temperature: Override LLM temperature
            max_tokens: Override max tokens
            
        Returns:
            EssenzGenerationResult with success status and details
        """
        start_time = time.time()
        
        logger.info(
            f"Generating essence for topic: {topic}",
            extra={
                "topic": topic,
                "source_count": len(source_files),
                "source_files": source_files[:5],  # Limit log size
            }
        )
        
        try:
            # 1. Read source content
            source_content = self._read_source_files(source_files)
            
            if not source_content.strip() or source_content.strip().startswith("[FEHLER"):
                raise EssenzGeneratorError(
                    f"No valid content found in source files: {source_files}"
                )
            
            # 2. Compute hotspot score
            hotspot_score = await self._compute_hotspot_score(source_files)
            
            # 3. Build prompt
            prompt = self._build_essence_prompt(topic, source_content)
            
            # 4. Generate with retry
            response = await self._generate_with_retry(prompt)
            
            # 5. Parse response
            essence_data = self._parse_essence_json(response.content)
            
            # 6. Save via ContentManager
            essence_path = await self._content_manager.save_essence(
                title=topic,
                summary=essence_data.get("summary", ""),
                key_points=essence_data.get("key_points", []),
                content=self._format_essence_body(essence_data),
                source_file=Path(source_files[0]) if source_files else None,
                entities=essence_data.get("entities", []),
                relationships=essence_data.get("relationships", []),
                keywords=essence_data.get("keywords", []),
                model_used=response.model,
                tags=tags or [],
                confidence=0.8,
            )
            
            # 7. Extract hash from path
            essence_hash = essence_path.parent.name if essence_path else None
            
            duration_ms = int((time.time() - start_time) * 1000)
            
            logger.info(
                f"Essence generated successfully",
                extra={
                    "topic": topic,
                    "essence_hash": essence_hash,
                    "duration_ms": duration_ms,
                    "hotspot_score": hotspot_score,
                }
            )
            
            return EssenzGenerationResult(
                topic=topic,
                success=True,
                essence_path=essence_path,
                essence_hash=essence_hash,
                source_files=source_files,
                model_used=response.model,
                duration_ms=duration_ms,
                version=1,
                hotspot_score=hotspot_score,
            )
            
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            
            logger.error(
                f"Failed to generate essence",
                extra={
                    "topic": topic,
                    "duration_ms": duration_ms,
                    "error": str(e),
                }
            )
            
            return EssenzGenerationResult(
                topic=topic,
                success=False,
                source_files=source_files,
                model_used=self._config.model,
                duration_ms=duration_ms,
                error=str(e),
            )
    
    # --- Parallel Generation ---
    
    def _init_parallel(
        self,
        llm_config: Optional[LLMConfig] = None,
    ):
        """Initialize ParallelMixin fields for EssenzGenerator."""
        self.__init_parallel__(llm_config)
    
    async def generate_essence_parallel(
        self,
        topic: str,
        source_files: List[str],
        *,
        strategy: Optional[str] = None,
        tags: Optional[List[str]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> EssenzGenerationResult:
        """
        Generate an essence using parallel engine strategies.
        
        When parallel_mode is enabled and a secondary engine is available,
        uses the specified strategy:
        - "primary_first": Try primary, fallback to secondary on failure
        - "aggregate": Both engines generate, results are merged (union)
        - "compare": Both generate, diff-view created, merge if complementary
        
        Falls back to single-engine generation if parallel mode is disabled.
        
        Args:
            topic: The topic to generate an essence for
            source_files: List of file paths to read as source content
            strategy: Override strategy ("primary_first", "aggregate", "compare")
            tags: Optional tags for categorization
            temperature: Override LLM temperature
            max_tokens: Override max tokens
            
        Returns:
            EssenzGenerationResult with success status and details
        """
        start_time = time.time()
        
        # Resolve strategy
        if strategy is not None:
            effective_strategy = ParallelStrategy(strategy)
        else:
            effective_strategy = self._parallel_strategy
        
        logger.info(
            f"Generating parallel essence for topic: {topic}",
            extra={
                "topic": topic,
                "strategy": effective_strategy.value,
                "source_count": len(source_files),
            }
        )
        
        # If not in parallel mode or no secondary engine, fall back to standard
        if not self._should_use_parallel():
            logger.info("Parallel mode disabled or no secondary engine, using standard generation")
            return await self.generate_essence(
                topic=topic,
                source_files=source_files,
                tags=tags,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        
        try:
            # 1. Read source content
            source_content = self._read_source_files(source_files)
            
            if not source_content.strip() or source_content.strip().startswith("[FEHLER"):
                raise EssenzGeneratorError(
                    f"No valid content found in source files: {source_files}"
                )
            
            # 2. Compute hotspot score
            hotspot_score = await self._compute_hotspot_score(source_files)
            
            # 3. Build prompt
            prompt = self._build_essence_prompt(topic, source_content)
            
            # 4. Generate with strategy
            parallel_result = await self._generate_with_strategy(
                prompt, effective_strategy
            )
            
            # 5. Process result based on strategy
            if effective_strategy == ParallelStrategy.PRIMARY_FIRST:
                return await self._process_primary_first_result(
                    parallel_result, topic, source_files, tags, hotspot_score
                )
            elif effective_strategy == ParallelStrategy.AGGREGATE:
                return await self._process_aggregate_result(
                    parallel_result, topic, source_files, tags, hotspot_score, temperature, max_tokens
                )
            elif effective_strategy == ParallelStrategy.COMPARE:
                return await self._process_compare_result(
                    parallel_result, topic, source_files, tags, hotspot_score, temperature, max_tokens
                )
            else:
                # Should not reach here
                raise EssenzGeneratorError(f"Unknown strategy: {effective_strategy}")
                
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            logger.error(
                f"Failed parallel essence generation",
                extra={"topic": topic, "duration_ms": duration_ms, "error": str(e)}
            )
            return EssenzGenerationResult(
                topic=topic,
                success=False,
                source_files=source_files,
                model_used=self._config.model,
                duration_ms=duration_ms,
                error=str(e),
            )
    
    async def _process_primary_first_result(
        self,
        parallel_result: ParallelResult,
        topic: str,
        source_files: List[str],
        tags: Optional[List[str]],
        hotspot_score: int,
    ) -> EssenzGenerationResult:
        """Process a primary_first parallel result."""
        start_time = time.time()
        
        response = parallel_result.primary_result or parallel_result.secondary_result
        
        if response is None:
            return EssenzGenerationResult(
                topic=topic,
                success=False,
                source_files=source_files,
                model_used=parallel_result.primary_model,
                duration_ms=parallel_result.primary_duration_ms,
                error=parallel_result.error or "Both engines failed",
            )
        
        if not response.success or not response.content:
            return EssenzGenerationResult(
                topic=topic,
                success=False,
                source_files=source_files,
                model_used=response.model,
                duration_ms=parallel_result.primary_duration_ms,
                error=f"LLM response failed: {response.error or 'empty content'}",
            )
        
        # Parse and save
        essence_data = self._parse_essence_json(response.content)
        model_used = response.model
        used_secondary = parallel_result.secondary_result is not None and parallel_result.primary_result is None
        
        essence_path = await self._content_manager.save_essence(
            title=topic,
            summary=essence_data.get("summary", ""),
            key_points=essence_data.get("key_points", []),
            content=self._format_essence_body(essence_data),
            source_file=Path(source_files[0]) if source_files else None,
            entities=essence_data.get("entities", []),
            relationships=essence_data.get("relationships", []),
            keywords=essence_data.get("keywords", []),
            model_used=model_used,
            tags=tags or [],
            confidence=0.8,
        )
        
        essence_hash = essence_path.parent.name if essence_path else None
        duration_ms = int((time.time() - start_time) * 1000)
        
        logger.info(
            f"Essence generated via primary_first strategy"
            f" ({'secondary' if used_secondary else 'primary'})",
            extra={"topic": topic, "essence_hash": essence_hash, "used_secondary": used_secondary}
        )
        
        return EssenzGenerationResult(
            topic=topic,
            success=True,
            essence_path=essence_path,
            essence_hash=essence_hash,
            source_files=source_files,
            model_used=model_used,
            duration_ms=duration_ms,
            version=1,
            hotspot_score=hotspot_score,
        )
    
    async def _process_aggregate_result(
        self,
        parallel_result: ParallelResult,
        topic: str,
        source_files: List[str],
        tags: Optional[List[str]],
        hotspot_score: int,
        temperature: Optional[float],
        max_tokens: Optional[int],
    ) -> EssenzGenerationResult:
        """Process an aggregate parallel result: merge both outputs."""
        start_time = time.time()
        
        primary_response = parallel_result.primary_result
        secondary_response = parallel_result.secondary_result
        
        if primary_response is None and secondary_response is None:
            return EssenzGenerationResult(
                topic=topic,
                success=False,
                source_files=source_files,
                model_used=parallel_result.primary_model,
                duration_ms=parallel_result.primary_duration_ms,
                error=parallel_result.error or "Both engines failed",
            )
        
        # Parse both if available
        essence_a = None
        essence_b = None
        
        if primary_response and primary_response.success and primary_response.content:
            try:
                essence_a = self._parse_essence_json(primary_response.content)
            except EssenzGeneratorError:
                logger.warning("Failed to parse primary engine essence in aggregate mode")
        
        if secondary_response and secondary_response.success and secondary_response.content:
            try:
                essence_b = self._parse_essence_json(secondary_response.content)
            except EssenzGeneratorError:
                logger.warning("Failed to parse secondary engine essence in aggregate mode")
        
        # Merge if both available
        if essence_a and essence_b:
            merged = self.merge_essences(essence_a, essence_b)
            model_used = f"{parallel_result.primary_model}+{parallel_result.secondary_model}"
        elif essence_a:
            merged = essence_a
            model_used = parallel_result.primary_model
        elif essence_b:
            merged = essence_b
            model_used = parallel_result.secondary_model
        else:
            return EssenzGenerationResult(
                topic=topic,
                success=False,
                source_files=source_files,
                model_used=parallel_result.primary_model,
                duration_ms=int((time.time() - start_time) * 1000),
                error="Both engines produced unparsable results",
            )
        
        # Save merged essence
        essence_path = await self._content_manager.save_essence(
            title=topic,
            summary=merged.get("summary", ""),
            key_points=merged.get("key_points", []),
            content=self._format_essence_body(merged),
            source_file=Path(source_files[0]) if source_files else None,
            entities=merged.get("entities", []),
            relationships=merged.get("relationships", []),
            keywords=merged.get("keywords", []),
            model_used=model_used,
            tags=tags or [],
            confidence=0.85,  # Higher confidence from aggregation
        )
        
        essence_hash = essence_path.parent.name if essence_path else None
        duration_ms = int((time.time() - start_time) * 1000)
        
        logger.info(
            f"Essence generated via aggregate strategy",
            extra={"topic": topic, "essence_hash": essence_hash, "model_used": model_used}
        )
        
        return EssenzGenerationResult(
            topic=topic,
            success=True,
            essence_path=essence_path,
            essence_hash=essence_hash,
            source_files=source_files,
            model_used=model_used,
            duration_ms=duration_ms,
            version=1,
            hotspot_score=hotspot_score,
        )
    
    async def _process_compare_result(
        self,
        parallel_result: ParallelResult,
        topic: str,
        source_files: List[str],
        tags: Optional[List[str]],
        hotspot_score: int,
        temperature: Optional[float],
        max_tokens: Optional[int],
    ) -> EssenzGenerationResult:
        """Process a compare parallel result: diff-view and conditional merge."""
        start_time = time.time()
        
        primary_response = parallel_result.primary_result
        secondary_response = parallel_result.secondary_result
        
        if primary_response is None and secondary_response is None:
            return EssenzGenerationResult(
                topic=topic,
                success=False,
                source_files=source_files,
                model_used=parallel_result.primary_model,
                duration_ms=parallel_result.primary_duration_ms,
                error=parallel_result.error or "Both engines failed",
            )
        
        # Parse both
        essence_a = None
        essence_b = None
        
        if primary_response and primary_response.success and primary_response.content:
            try:
                essence_a = self._parse_essence_json(primary_response.content)
            except EssenzGeneratorError:
                logger.warning("Failed to parse primary engine essence in compare mode")
        
        if secondary_response and secondary_response.success and secondary_response.content:
            try:
                essence_b = self._parse_essence_json(secondary_response.content)
            except EssenzGeneratorError:
                logger.warning("Failed to parse secondary engine essence in compare mode")
        
        # Determine result
        if essence_a and essence_b:
            # Compute diff
            diff_result = self.diff_essences(essence_a, essence_b)
            parallel_result.diff_result = diff_result
            
            if diff_result.can_merge:
                # Merge complementary results
                merged = self.merge_essences(essence_a, essence_b, diff_result)
                model_used = f"{parallel_result.primary_model}+{parallel_result.secondary_model} (merged)"
                logger.info(
                    f"Compare mode: results merged ("
                    f"{diff_result.complement_count} complementary, "
                    f"{diff_result.conflict_count} conflicts)",
                    extra={"topic": topic}
                )
            else:
                # Conflicts exist - use primary result
                merged = essence_a
                model_used = f"{parallel_result.primary_model} (conflicts: use primary)"
                logger.info(
                    f"Compare mode: conflicts detected ("
                    f"{diff_result.conflict_count} conflicts, "
                    f"{diff_result.complement_count} complementary), "
                    f"using primary result",
                    extra={"topic": topic}
                )
            
            # Save diff metadata alongside essence
            essence_data = merged
        elif essence_a:
            merged = essence_a
            model_used = parallel_result.primary_model
        elif essence_b:
            merged = essence_b
            model_used = parallel_result.secondary_model
        else:
            return EssenzGenerationResult(
                topic=topic,
                success=False,
                source_files=source_files,
                model_used=parallel_result.primary_model,
                duration_ms=int((time.time() - start_time) * 1000),
                error="Both engines produced unparsable results",
            )
        
        # Save
        essence_path = await self._content_manager.save_essence(
            title=topic,
            summary=merged.get("summary", ""),
            key_points=merged.get("key_points", []),
            content=self._format_essence_body(merged),
            source_file=Path(source_files[0]) if source_files else None,
            entities=merged.get("entities", []),
            relationships=merged.get("relationships", []),
            keywords=merged.get("keywords", []),
            model_used=model_used,
            tags=tags or [],
            confidence=0.85 if parallel_result.diff_result and parallel_result.diff_result.can_merge else 0.8,
        )
        
        # If we have a diff_result, save it alongside
        if parallel_result.diff_result:
            diff_path = essence_path.parent / "diff.json" if essence_path else None
            if diff_path:
                diff_path.write_text(
                    json.dumps(parallel_result.diff_result.to_dict(), indent=2, ensure_ascii=False),
                    encoding="utf-8"
                )
        
        essence_hash = essence_path.parent.name if essence_path else None
        duration_ms = int((time.time() - start_time) * 1000)
        
        logger.info(
            f"Essence generated via compare strategy",
            extra={"topic": topic, "essence_hash": essence_hash, "model_used": model_used}
        )
        
        return EssenzGenerationResult(
            topic=topic,
            success=True,
            essence_path=essence_path,
            essence_hash=essence_hash,
            source_files=source_files,
            model_used=model_used,
            duration_ms=duration_ms,
            version=1,
            hotspot_score=hotspot_score,
        )
    
    async def generate_essences_batch(
        self,
        topics: List[str],
        source_files_map: Optional[Dict[str, List[str]]] = None,
        *,
        concurrency: int = 3,
        tags: Optional[List[str]] = None,
        on_progress: Optional[callable] = None,
        parallel_strategy: Optional[str] = None,
    ) -> List[EssenzGenerationResult]:
        """
        Generate essences for multiple topics in batch.
        
        Processes topics concurrently with configurable concurrency limit.
        Supports parallel engine strategies when enabled.
        
        Args:
            topics: List of topics to generate essences for
            source_files_map: Optional mapping of topic → source files
            concurrency: Max concurrent generations (default: 3)
            tags: Tags to apply to all generated essences
            on_progress: Optional callback(topic, index, total) for progress
            parallel_strategy: Optional strategy override for parallel mode
            
        Returns:
            List of EssenzGenerationResult objects
        """
        total = len(topics)
        results: List[EssenzGenerationResult] = []
        semaphore = asyncio.Semaphore(concurrency)
        
        logger.info(
            f"Starting batch essence generation",
            extra={"total_topics": total, "concurrency": concurrency}
        )
        
        use_parallel = self._should_use_parallel()
        
        async def _generate_one(topic: str, index: int) -> EssenzGenerationResult:
            async with semaphore:
                if on_progress:
                    try:
                        on_progress(topic, index, total)
                    except Exception:
                        pass
                
                files = source_files_map.get(topic, []) if source_files_map else []
                
                if use_parallel:
                    return await self.generate_essence_parallel(
                        topic=topic,
                        source_files=files,
                        strategy=parallel_strategy,
                        tags=tags,
                    )
                else:
                    return await self.generate_essence(
                        topic=topic,
                        source_files=files,
                        tags=tags,
                    )
        
        # Schedule all tasks
        tasks = [
            _generate_one(topic, i)
            for i, topic in enumerate(topics)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=False)
        
        # Log summary
        successes = sum(1 for r in results if r.success)
        failures = sum(1 for r in results if not r.success)
        
        logger.info(
            f"Batch generation complete",
            extra={
                "total": total,
                "successes": successes,
                "failures": failures,
                "parallel": use_parallel,
            }
        )
        
        return list(results)
        concurrency: int = 3,
        tags: Optional[List[str]] = None,
        on_progress: Optional[callable] = None,
    
    async def update_essence_with_new_content(
        self,
        essence_id: str,
        new_files: List[str],
        *,
        temperature: Optional[float] = None,
    ) -> EssenzGenerationResult:
        """
        Update an existing essence with new content (differential essence).
        
        Loads the existing essence, reads new files, and asks the LLM
        to integrate the new information into the existing structure.
        
        Args:
            essence_id: Hash of the existing essence to update
            new_files: List of new file paths to integrate
            temperature: Optional temperature override
            
        Returns:
            EssenzGenerationResult with updated version info
        """
        start_time = time.time()
        
        logger.info(
            f"Updating essence with new content",
            extra={"essence_id": essence_id, "new_files_count": len(new_files)}
        )
        
        try:
            # 1. Load existing essence
            essence_dir = self._config.essences_path / essence_id
            if not essence_dir.exists():
                raise EssenzGeneratorError(
                    f"Essence not found: {essence_id}"
                )
            
            json_path = essence_dir / "essence.json"
            md_path = essence_dir / "essence.md"
            
            if not json_path.exists():
                raise EssenzGeneratorError(
                    f"Essence JSON not found: {json_path}"
                )
            
            existing_data = json.loads(json_path.read_text(encoding="utf-8"))
            existing_essence = existing_data.get("essence", {})
            existing_version = existing_data.get("version", 1)
            existing_source = existing_data.get("source_path")
            
            # 2. Read new content
            new_content = self._read_source_files(new_files)
            
            if not new_content.strip() or new_content.strip().startswith("[FEHLER"):
                raise EssenzGeneratorError(
                    f"No valid content in new files: {new_files}"
                )
            
            # 3. Build differential prompt
            prompt = self._build_essence_prompt(
                topic=existing_essence.get("title", essence_id),
                source_content=new_content,
                existing_essence={
                    "version": existing_version,
                    "summary": existing_essence.get("summary", ""),
                    "key_points": existing_essence.get("key_points", []),
                }
            )
            
            # 4. Generate updated essence
            response = await self._generate_with_retry(prompt)
            
            # 5. Parse
            updated_data = self._parse_essence_json(response.content)
            
            # 6. Compute hotspot score
            all_sources = []
            if existing_source:
                all_sources.append(existing_source)
            all_sources.extend(new_files)
            hotspot_score = await self._compute_hotspot_score(all_sources)
            
            # 7. Save updated essence (creates new version in same directory)
            new_version = existing_version + 1
            
            # Update the existing essence files
            essence_path = await self._content_manager.save_essence(
                title=existing_essence.get("title", essence_id),
                summary=updated_data.get("summary", existing_essence.get("summary", "")),
                key_points=updated_data.get("key_points", existing_essence.get("key_points", [])),
                content=self._format_essence_body(updated_data),
                source_file=Path(new_files[0]) if new_files else None,
                entities=updated_data.get("entities", existing_essence.get("entities", [])),
                relationships=updated_data.get("relationships", existing_essence.get("relationships", [])),
                keywords=updated_data.get("keywords", existing_essence.get("keywords", [])),
                model_used=response.model,
                tags=existing_data.get("tags", []),
                confidence=0.85,  # Slightly higher for differential updates
            )
            
            # Update metadata in the existing essence directory
            updated_metadata = {
                **existing_data,
                "version": new_version,
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "previous_source_hash": existing_data.get("source_hash"),
                "new_source_files": new_files,
                "model": response.model,
            }
            json_path.write_text(
                json.dumps(updated_metadata, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )
            
            new_hash = essence_path.parent.name if essence_path else None
            duration_ms = int((time.time() - start_time) * 1000)
            
            logger.info(
                f"Essence updated successfully",
                extra={
                    "essence_id": essence_id,
                    "new_hash": new_hash,
                    "version": new_version,
                    "duration_ms": duration_ms,
                }
            )
            
            return EssenzGenerationResult(
                topic=existing_essence.get("title", essence_id),
                success=True,
                essence_path=essence_path,
                essence_hash=new_hash,
                source_files=all_sources,
                model_used=response.model,
                duration_ms=duration_ms,
                version=new_version,
                hotspot_score=hotspot_score,
            )
            
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            
            logger.error(
                f"Failed to update essence",
                extra={
                    "essence_id": essence_id,
                    "duration_ms": duration_ms,
                    "error": str(e),
                }
            )
            
            return EssenzGenerationResult(
                topic=essence_id,
                success=False,
                source_files=new_files,
                model_used=self._config.model,
                duration_ms=duration_ms,
                version=existing_version if 'existing_version' in dir() else 0,
                error=str(e),
            )
    
    # --- Formatting Helpers ---
    
    def _format_essence_body(self, essence_data: Dict[str, Any]) -> str:
        """
        Format essence data into a detailed markdown body.
        
        Args:
            essence_data: Parsed essence dictionary
            
        Returns:
            Formatted markdown string
        """
        parts = []
        
        # Connections
        connections = essence_data.get("connections", [])
        if connections:
            parts.append("## Verknüpfungen\n")
            for conn in connections:
                parts.append(f"- {conn}")
            parts.append("")
        
        # Contradictions
        contradictions = essence_data.get("contradictions", [])
        if contradictions:
            parts.append("## Widersprüche\n")
            for contra in contradictions:
                parts.append(f"- ⚠️ {contra}")
            parts.append("")
        
        # Open questions
        open_questions = essence_data.get("open_questions", [])
        if open_questions:
            parts.append("## Offene Fragen\n")
            for q in open_questions:
                parts.append(f"- ❓ {q}")
            parts.append("")
        
        return "\n".join(parts) if parts else "Keine zusätzlichen Analysen verfügbar."