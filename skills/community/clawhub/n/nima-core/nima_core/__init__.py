"""NIMA Core — Dynamic Affect System for AI agents."""

__version__ = "2.3.0"

from .cognition.dynamic_affect import DynamicAffectSystem, AffectVector, get_affect_system
from .cognition.personality_profiles import PersonalityManager, get_profile, list_profiles
from .cognition.emotion_detection import map_emotions_to_affects, detect_affect_from_text
from .cognition.response_modulator_v2 import GenericResponseModulator, ResponseGuidance, modulate_response
from .cognition.archetypes import (
    ARCHETYPES,
    get_archetype,
    list_archetypes,
    baseline_from_archetype,
    baseline_from_description
)

# Infrastructure modules
from .logging_config import get_logger
from .metrics import get_metrics, Timer, RECALL_QUERY_MS, RECALL_CACHE_HITS, AFFECT_UPDATE_MS, MEMORY_STORE_MS
from .connection_pool import get_pool

__all__ = [
    "DynamicAffectSystem",
    "AffectVector",
    "get_affect_system",
    "PersonalityManager",
    "get_profile",
    "list_profiles",
    "map_emotions_to_affects",
    "detect_affect_from_text",
    "GenericResponseModulator",
    "ResponseGuidance",
    "modulate_response",
    "ARCHETYPES",
    "get_archetype",
    "list_archetypes",
    "baseline_from_archetype",
    "baseline_from_description",
    "__version__",
    # Infrastructure
    "get_logger",
    "get_metrics",
    "Timer",
    "RECALL_QUERY_MS",
    "RECALL_CACHE_HITS",
    "AFFECT_UPDATE_MS",
    "MEMORY_STORE_MS",
    "get_pool",
]
# Memory pruner (optional - may fail if ladybug not available)
try:
    from .memory_pruner import run_pruner, status as pruner_status
    __all__.extend(["run_pruner", "pruner_status"])
except ImportError:
    pass


def main():
    """CLI entry point — runs setup wizard."""
    import subprocess, sys
    # Find and run install.sh from package directory
    import os
    pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    install_script = os.path.join(pkg_dir, 'install.sh')
    if os.path.exists(install_script):
        subprocess.run(['bash', install_script], cwd=pkg_dir)
    else:
        print("NIMA Core v" + __version__)
        print("Run ./install.sh from the nima-core directory to set up hooks.")
        print("Or manually copy hooks: cp -r openclaw_hooks/* ~/.openclaw/extensions/")
        print("Docs: https://nima-core.ai")
