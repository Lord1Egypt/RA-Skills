#!/usr/bin/env python3
"""
kb.biblio - LLM Integration Package

Provides Ollama/Gemma4 integration for Knowledge Base operations.
Includes file watcher and task scheduler for automated maintenance.
"""

# Use lazy imports to avoid circular dependency issues
# (kb.biblio.engine → kb.biblio.config → kb.biblio.__init__ → kb.biblio.engine)

def __getattr__(name):
    """Lazy import - only load submodules when accessed."""
    _lazy_map = {
        # Config
        "LLMConfig": "kb.biblio.config",
        "get_llm_config": "kb.biblio.config",
        # Engine
        "BaseLLMEngine": "kb.biblio.engine",
        "OllamaEngine": "kb.biblio.engine",
        "LLMResponse": "kb.biblio.engine.base",
        "LLMStreamChunk": "kb.biblio.engine.base",
        "LLMProvider": "kb.biblio.engine.base",
        # Content Manager
        "LLMContentManager": "kb.biblio.content_manager",
        "ContentManagerError": "kb.biblio.content_manager",
        "save_essence_async": "kb.biblio.content_manager",
        "save_report_async": "kb.biblio.content_manager",
        "list_essences_async": "kb.biblio.content_manager",
        "get_essence_by_topic_async": "kb.biblio.content_manager",
        # Generator - Essence
        "EssenzGenerator": "kb.biblio.generator",
        "EssenzGeneratorError": "kb.biblio.generator",
        "EssenzGenerationResult": "kb.biblio.generator",
        # Generator - Report
        "ReportGenerator": "kb.biblio.generator",
        "ReportGeneratorError": "kb.biblio.generator",
        "ReportGenerationResult": "kb.biblio.generator",
        # Watcher
        "FileWatcher": "kb.biblio.watcher",
        "FileWatcherError": "kb.biblio.watcher",
        "WatchedFile": "kb.biblio.watcher",
        "FileWatcherState": "kb.biblio.watcher",
        # Scheduler
        "TaskScheduler": "kb.biblio.scheduler",
        "TaskSchedulerError": "kb.biblio.scheduler",
        "ScheduledJob": "kb.biblio.scheduler",
        "JobResult": "kb.biblio.scheduler",
        "JobStatus": "kb.biblio.scheduler",
    }
    
    if name in _lazy_map:
        import importlib
        mod = importlib.import_module(_lazy_map[name])
        return getattr(mod, name)
    
    raise AttributeError(f"module 'kb.biblio' has no attribute {name!r}")


__all__ = [
    # Config
    "LLMConfig",
    "get_llm_config",
    # Engine
    "BaseLLMEngine",
    "OllamaEngine",
    # Models
    "LLMResponse",
    "LLMStreamChunk",
    "LLMProvider",
    # Content Manager
    "LLMContentManager",
    "ContentManagerError",
    "save_essence_async",
    "save_report_async",
    "list_essences_async",
    "get_essence_by_topic_async",
    # Generator - Essence
    "EssenzGenerator",
    "EssenzGeneratorError",
    "EssenzGenerationResult",
    # Generator - Report
    "ReportGenerator",
    "ReportGeneratorError",
    "ReportGenerationResult",
    # Watcher
    "FileWatcher",
    "FileWatcherError",
    "WatchedFile",
    "FileWatcherState",
    # Scheduler
    "TaskScheduler",
    "TaskSchedulerError",
    "ScheduledJob",
    "JobResult",
    "JobStatus",
]

__version__ = "1.0.0"