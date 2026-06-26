#!/usr/bin/env python3
"""
kb.llm - Backward Compatibility Alias
======================================

DEPRECATED: Use kb.biblio instead.
This module re-exports everything from kb.biblio for backward compatibility.
"""

import warnings

warnings.warn(
    "kb.llm is deprecated, use kb.biblio instead",
    DeprecationWarning,
    stacklevel=2
)


def __getattr__(name):
    """Lazy redirect to kb.biblio."""
    import kb.biblio
    return getattr(kb.biblio, name)


__all__ = [
    "LLMConfig",
    "get_llm_config",
    "BaseLLMEngine",
    "OllamaEngine",
    "LLMResponse",
    "LLMStreamChunk",
    "LLMProvider",
    "LLMContentManager",
    "ContentManagerError",
    "save_essence_async",
    "save_report_async",
    "list_essences_async",
    "get_essence_by_topic_async",
    "EssenzGenerator",
    "EssenzGeneratorError",
    "EssenzGenerationResult",
    "ReportGenerator",
    "ReportGeneratorError",
    "ReportGenerationResult",
    "FileWatcher",
    "FileWatcherError",
    "WatchedFile",
    "FileWatcherState",
    "TaskScheduler",
    "TaskSchedulerError",
    "ScheduledJob",
    "JobResult",
    "JobStatus",
]

__version__ = "1.0.0"