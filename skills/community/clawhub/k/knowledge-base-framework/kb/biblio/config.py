#!/usr/bin/env python3
"""
LLM Configuration - LLM-spezifische Konfiguration

Modell-Pfade, Timeouts, Batch-Größen.
Integration mit KBConfig für konsistente Pfad-Auflösung.
"""

from pathlib import Path
from typing import Optional, Dict, Any
import os
import threading

from kb.base.config import KBConfig, get_config


class LLMConfigError(Exception):
    """Configuration-related errors for LLM module."""
    pass


class LLMConfig:
    """
    Singleton für LLM-spezifische Konfiguration.
    
    Thread-safe implementation mit lazy loading.
    Erbt Pfade von KBConfig, überschreibt mit Env-Vars.
    
    Supports two model sources:
    - "ollama" (default): Uses OllamaEngine with external Ollama server
    - "huggingface": Uses TransformersEngine with in-process model loading
    
    Usage:
        config = LLMConfig.get_instance()
        engine = create_engine(config)
        
        # With custom values
        config = LLMConfig(
            model="gemma4:e2b",
            timeout=180,
            temperature=0.7
        )
    """
    
    _instance: Optional['LLMConfig'] = None
    _lock = threading.Lock()
    
    DEFAULT_MODEL: str = "gemma4:e2b"
    DEFAULT_OLLAMA_URL: str = "http://localhost:11434"
    DEFAULT_TIMEOUT: int = 120  # seconds
    DEFAULT_TEMPERATURE: float = 0.7
    DEFAULT_MAX_TOKENS: int = 2048
    DEFAULT_BATCH_SIZE: int = 10
    DEFAULT_MAX_RETRIES: int = 3
    DEFAULT_RETRY_DELAY: float = 5.0  # seconds
    
    # Watcher defaults
    DEFAULT_WATCHER_INTERVAL: int = 20  # minutes
    DEFAULT_WATCHER_EXTENSIONS: tuple = (".md", ".pdf")
    DEFAULT_WATCHER_EXCLUDE_DIRS: tuple = ("biblio",)
    
    # Scheduler defaults
    DEFAULT_SCHEDULER_TICK: int = 60  # seconds between scheduler checks
    DEFAULT_SCHEDULER_DB: str = "scheduler_state.db"
    
    # GC defaults
    DEFAULT_GC_THRESHOLD_DAYS: int = 90  # days before archiving
    
    # Model source & parallel mode defaults
    DEFAULT_MODEL_SOURCE: str = "auto"  # "auto", "ollama", "huggingface", "compare"
    DEFAULT_HF_MODEL_NAME: str = "google/gemma-2-2b-it"
    DEFAULT_HF_DEVICE: str = "auto"
    DEFAULT_HF_REVISION: str = "main"
    DEFAULT_HF_DTYPE: str = "auto"
    
    # Ollama-specific defaults (for auto/compare fallback)
    DEFAULT_OLLAMA_MODEL: str = "gemma4:e2b"
    DEFAULT_OLLAMA_TIMEOUT: int = 120  # seconds
    DEFAULT_OLLAMA_TEMPERATURE: float = 0.7
    
    # Parallel / compare mode defaults
    DEFAULT_PARALLEL_MODE: bool = False
    DEFAULT_PARALLEL_STRATEGY: str = "primary_first"  # "primary_first", "aggregate", or "compare"
    
    def __init__(
        self,
        model: Optional[str] = None,
        ollama_url: Optional[str] = None,
        timeout: Optional[int] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        batch_size: Optional[int] = None,
        max_retries: Optional[int] = None,
        retry_delay: Optional[float] = None,
        model_source: Optional[str] = None,
        hf_model_name: Optional[str] = None,
        hf_quantization: Optional[str] = None,
        hf_device: Optional[str] = None,
        hf_cache_dir: Optional[str] = None,
        hf_token: Optional[str] = None,
        hf_revision: Optional[str] = None,
        hf_trust_remote_code: Optional[bool] = None,
        hf_torch_dtype: Optional[str] = None,
        hf_offload_folder: Optional[str] = None,
        ollama_model: Optional[str] = None,
        ollama_timeout: Optional[int] = None,
        ollama_temperature: Optional[float] = None,
        parallel_mode: Optional[bool] = None,
        parallel_strategy: Optional[str] = None,
        skip_validation: bool = False
    ):
        if LLMConfig._instance is not None:
            raise LLMConfigError("Use LLMConfig.get_instance() instead of constructor")
        
        # Resolve values: env > param > default
        self.model = self._resolve("KB_LLM_MODEL", model, self.DEFAULT_MODEL)
        self.ollama_url = self._resolve("KB_LLM_OLLAMA_URL", ollama_url, self.DEFAULT_OLLAMA_URL)
        self.timeout = self._resolve_int("KB_LLM_TIMEOUT", timeout, self.DEFAULT_TIMEOUT)
        self.temperature = self._resolve_float("KB_LLM_TEMPERATURE", temperature, self.DEFAULT_TEMPERATURE)
        self.max_tokens = self._resolve_int("KB_LLM_MAX_TOKENS", max_tokens, self.DEFAULT_MAX_TOKENS)
        self.batch_size = self._resolve_int("KB_LLM_BATCH_SIZE", batch_size, self.DEFAULT_BATCH_SIZE)
        self.max_retries = self._resolve_int("KB_LLM_MAX_RETRIES", max_retries, self.DEFAULT_MAX_RETRIES)
        self.retry_delay = self._resolve_float("KB_LLM_RETRY_DELAY", retry_delay, self.DEFAULT_RETRY_DELAY)
        
        # Model source & engine selection configuration
        self.model_source = self._resolve("KB_LLM_MODEL_SOURCE", model_source, self.DEFAULT_MODEL_SOURCE)
        self.hf_model_name = self._resolve("KB_LLM_HF_MODEL", hf_model_name, self.DEFAULT_HF_MODEL_NAME)
        self.hf_quantization = self._resolve_optional("KB_LLM_HF_QUANT", hf_quantization)
        self.hf_device = self._resolve("KB_LLM_HF_DEVICE", hf_device, self.DEFAULT_HF_DEVICE)
        self.hf_cache_dir = self._resolve_optional("KB_LLM_HF_CACHE", hf_cache_dir) or self._resolve_optional("HF_HOME", None)
        self.hf_token = self._resolve_optional("KB_LLM_HF_TOKEN", hf_token) or self._resolve_optional("HF_TOKEN", None)
        self.hf_revision = self._resolve("KB_LLM_HF_REVISION", hf_revision, self.DEFAULT_HF_REVISION)
        self.hf_trust_remote_code = self._resolve_bool("KB_LLM_HF_TRUST_REMOTE_CODE", hf_trust_remote_code, False)
        self.hf_torch_dtype = self._resolve("KB_LLM_HF_DTYPE", hf_torch_dtype, self.DEFAULT_HF_DTYPE)
        self.hf_offload_folder = self._resolve_optional("KB_LLM_HF_OFFLOAD_FOLDER", hf_offload_folder)
        
        # Ollama-specific (used in auto/compare mode as secondary or fallback)
        self.ollama_model = self._resolve("KB_LLM_OLLAMA_MODEL", ollama_model, self.DEFAULT_OLLAMA_MODEL)
        self.ollama_timeout = self._resolve_int("KB_LLM_OLLAMA_TIMEOUT", ollama_timeout, self.DEFAULT_OLLAMA_TIMEOUT)
        self.ollama_temperature = self._resolve_float("KB_LLM_OLLAMA_TEMPERATURE", ollama_temperature, self.DEFAULT_OLLAMA_TEMPERATURE)
        
        # Parallel / compare mode configuration
        self.parallel_mode = self._resolve_bool("KB_LLM_PARALLEL_MODE", parallel_mode, self.DEFAULT_PARALLEL_MODE)
        self.parallel_strategy = self._resolve("KB_LLM_PARALLEL_STRATEGY", parallel_strategy, self.DEFAULT_PARALLEL_STRATEGY)
        
        # Derived paths from KBConfig
        self._kb_config = get_config()
        
        if not skip_validation:
            self._validate()
            self._validate_hf_config()
        
        LLMConfig._instance = self
    
    def _resolve(self, env_var: str, param: Optional[str], default: str) -> str:
        """Resolve string value: env > param > default."""
        if env_var in os.environ:
            return os.environ[env_var]
        if param is not None:
            return param
        return default
    
    def _resolve_int(self, env_var: str, param: Optional[int], default: int) -> int:
        """Resolve integer value: env > param > default."""
        if env_var in os.environ:
            try:
                return int(os.environ[env_var])
            except ValueError:
                raise LLMConfigError(f"Invalid integer for {env_var}: {os.environ[env_var]}")
        if param is not None:
            return param
        return default
    
    def _resolve_float(self, env_var: str, param: Optional[float], default: float) -> float:
        """Resolve float value: env > param > default."""
        if env_var in os.environ:
            try:
                return float(os.environ[env_var])
            except ValueError:
                raise LLMConfigError(f"Invalid float for {env_var}: {os.environ[env_var]}")
        if param is not None:
            return param
        return default
    
    def _resolve_optional(self, env_var: str, param: Optional[str]) -> Optional[str]:
        """Resolve optional string value: env > param. Returns None if neither set."""
        if env_var in os.environ:
            return os.environ[env_var]
        if param is not None:
            return param
        return None
    
    def _resolve_bool(self, env_var: str, param: Optional[bool], default: bool) -> bool:
        """Resolve boolean value: env > param > default. Env values: 'true'/'1'/'yes' = True."""
        if env_var in os.environ:
            env_val = os.environ[env_var].lower()
            return env_val in ("true", "1", "yes")
        if param is not None:
            return param
        return default
    
    def _validate(self) -> None:
        """Validate LLM configuration."""
        if not self.ollama_url.startswith(("http://", "https://")):
            raise LLMConfigError(f"Invalid Ollama URL: {self.ollama_url}")
        
        if self.timeout <= 0:
            raise LLMConfigError(f"Timeout must be positive: {self.timeout}")
        
        if not 0 <= self.temperature <= 2:
            raise LLMConfigError(f"Temperature must be between 0 and 2: {self.temperature}")
    
    # Valid model_source values
    VALID_MODEL_SOURCES = ("ollama", "huggingface", "auto", "compare")
    VALID_PARALLEL_STRATEGIES = ("primary_first", "aggregate", "compare")
    
    def _validate_hf_config(self) -> None:
        """Validate model source and engine-specific configuration."""
        if self.model_source not in self.VALID_MODEL_SOURCES:
            raise LLMConfigError(
                f"Invalid model_source: {self.model_source}. "
                f"Must be one of {self.VALID_MODEL_SOURCES}"
            )
        
        # HF validation: required when source is huggingface, auto, or compare
        hf_required = self.model_source in ("huggingface", "auto", "compare")
        if hf_required:
            if not self.hf_model_name:
                raise LLMConfigError(
                    f"hf_model_name is required when model_source='{self.model_source}'"
                )
            if self.hf_quantization is not None and self.hf_quantization not in ("4bit", "8bit"):
                raise LLMConfigError(
                    f"Invalid quantization: {self.hf_quantization}. Must be '4bit', '8bit', or None"
                )
            valid_devices = {"auto", "cpu", "cuda", "mps"}
            if self.hf_device not in valid_devices and not self.hf_device.startswith("cuda:"):
                raise LLMConfigError(
                    f"Invalid device: {self.hf_device}. Must be 'auto', 'cpu', 'cuda', 'cuda:N', or 'mps'"
                )
            valid_dtypes = {"auto", "float16", "bfloat16", "float32"}
            if self.hf_torch_dtype not in valid_dtypes:
                raise LLMConfigError(
                    f"Invalid dtype: {self.hf_torch_dtype}. Must be one of {valid_dtypes}"
                )
        
        # Parallel / compare mode validation
        if self.parallel_strategy not in self.VALID_PARALLEL_STRATEGIES:
            raise LLMConfigError(
                f"Invalid parallel_strategy: {self.parallel_strategy}. "
                f"Must be one of {self.VALID_PARALLEL_STRATEGIES}"
            )
        
        if self.ollama_timeout <= 0:
            raise LLMConfigError(f"ollama_timeout must be positive: {self.ollama_timeout}")
        
        if not 0 <= self.ollama_temperature <= 2:
            raise LLMConfigError(
                f"ollama_temperature must be between 0 and 2: {self.ollama_temperature}"
            )
        
        # compare mode requires both engines
        if self.model_source == "compare" and not self.ollama_model:
            raise LLMConfigError(
                "ollama_model is required when model_source='compare'"
            )
    
    @classmethod
    def get_instance(cls) -> 'LLMConfig':
        """Returns singleton instance (lazy initialization).
        
        Thread-safe: All reads/writes of _instance are protected by cls._lock.
        No fast path outside the lock to avoid race conditions.
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
        return cls._instance
    
    @classmethod
    def reload(cls, **kwargs) -> 'LLMConfig':
        """Forces reload of configuration with optional overrides."""
        with cls._lock:
            cls._instance = None
        return cls(**kwargs) if kwargs else cls.get_instance()
    
    @classmethod
    def reset(cls) -> None:
        """Reset singleton (mainly for testing)."""
        with cls._lock:
            cls._instance = None
    
    # --- Derived Paths ---
    
    @property
    def library_biblio_path(self) -> Path:
        """Path to kb/library/biblio/ directory."""
        return self._kb_config.base_path / "library" / "biblio"
    
    # Backward compatibility alias
    @property
    def library_llm_path(self) -> Path:
        """Deprecated: Use library_biblio_path instead."""
        return self.library_biblio_path
    
    @property
    def essences_path(self) -> Path:
        """Path to essences directory."""
        return self.library_biblio_path / "essences"
    
    @property
    def reports_path(self) -> Path:
        """Path to reports directory."""
        return self.library_biblio_path / "reports"
    
    @property
    def graph_path(self) -> Path:
        """Path to knowledge graph directory."""
        return self.library_biblio_path / "graph"

    @property
    def incoming_path(self) -> Path:
        """Path to incoming files queue directory."""
        return self.library_biblio_path / "incoming"

    @property
    def templates_path(self) -> Path:
        """Path to LLM templates directory (shipped with source)."""
        # Templates are source code, not runtime data - resolve from package location
        return Path(__file__).parent / "templates"
    
    @property
    def watcher_state_db(self) -> Path:
        """Path to watcher state database."""
        return self._kb_config.base_path / "watcher_state.db"
    
    @property
    def scheduler_state_db(self) -> Path:
        """Path to scheduler state database."""
        return self._kb_config.base_path / self.DEFAULT_SCHEDULER_DB
    
    @property
    def watcher_interval(self) -> int:
        """File watcher scan interval in minutes."""
        return self._resolve_int(
            "KB_LLM_WATCHER_INTERVAL",
            None,
            self.DEFAULT_WATCHER_INTERVAL
        )
    
    @property
    def watcher_extensions(self) -> tuple:
        """File extensions to watch."""
        env = os.environ.get("KB_LLM_WATCHER_EXTENSIONS")
        if env:
            return tuple(e.strip() for e in env.split(",") if e.strip())
        return self.DEFAULT_WATCHER_EXTENSIONS
    
    @property
    def watcher_exclude_dirs(self) -> tuple:
        """Directory names to exclude from watching."""
        env = os.environ.get("KB_LLM_WATCHER_EXCLUDE_DIRS")
        if env:
            return tuple(d.strip() for d in env.split(",") if d.strip())
        return self.DEFAULT_WATCHER_EXCLUDE_DIRS
    
    @property
    def gc_threshold_days(self) -> int:
        """Days before essences are archived by GC."""
        return self._resolve_int(
            "KB_LLM_GC_THRESHOLD_DAYS",
            None,
            self.DEFAULT_GC_THRESHOLD_DAYS
        )
    
    # --- Utility Methods ---
    
    def ensure_dirs(self) -> None:
        """Ensure all LLM library directories exist."""
        for path in [self.essences_path, self.reports_path, self.graph_path, self.incoming_path]:
            path.mkdir(parents=True, exist_ok=True)
    
    def to_dict(self) -> Dict[str, Any]:
        """Export configuration as dictionary."""
        return {
            'model': self.model,
            'ollama_url': self.ollama_url,
            'timeout': self.timeout,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
            'batch_size': self.batch_size,
            'max_retries': self.max_retries,
            'retry_delay': self.retry_delay,
            'model_source': self.model_source,
            'hf_model_name': self.hf_model_name,
            'hf_quantization': self.hf_quantization,
            'hf_device': self.hf_device,
            'hf_cache_dir': self.hf_cache_dir,
            'hf_token': '***' if self.hf_token else None,  # Never expose token
            'hf_revision': self.hf_revision,
            'hf_trust_remote_code': self.hf_trust_remote_code,
            'hf_torch_dtype': self.hf_torch_dtype,
            'hf_offload_folder': self.hf_offload_folder,
            'ollama_model': self.ollama_model,
            'ollama_timeout': self.ollama_timeout,
            'ollama_temperature': self.ollama_temperature,
            'parallel_mode': self.parallel_mode,
            'parallel_strategy': self.parallel_strategy,
            'essences_path': str(self.essences_path),
            'reports_path': str(self.reports_path),
            'graph_path': str(self.graph_path),
            'watcher_interval': self.watcher_interval,
            'watcher_extensions': list(self.watcher_extensions),
            'watcher_exclude_dirs': list(self.watcher_exclude_dirs),
            'gc_threshold_days': self.gc_threshold_days,
            'watcher_state_db': str(self.watcher_state_db),
            'scheduler_state_db': str(self.scheduler_state_db),
        }
    
    def __repr__(self) -> str:
        return (
            f"LLMConfig(model={self.model}, "
            f"model_source={self.model_source}, "
            f"ollama_url={self.ollama_url}, "
            f"timeout={self.timeout})"
        )
    
    def __str__(self) -> str:
        source_desc = {
            "auto": f"auto({self.hf_model_name} → {self.ollama_model})",
            "compare": f"compare({self.hf_model_name} vs {self.ollama_model})",
        }
        desc = source_desc.get(self.model_source)
        if desc:
            return f"LLMConfig({desc})"
        if self.model_source == "huggingface":
            return f"LLMConfig({self.hf_model_name} @ huggingface)"
        return f"LLMConfig({self.model} @ {self.ollama_url})"


def get_llm_config() -> LLMConfig:
    """Get LLMConfig singleton instance."""
    return LLMConfig.get_instance()