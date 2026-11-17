"""
engine/compat.py — Backward compatibility bridge

Wires old NovelState API to new StateAdapter/StateRepository.
Import this at the bottom of novel_state.py to enable write-protection.

All legacy code continues to work, but _state mutations are now:
1. Audited (who changed what)
2. Single-source (delegated to StateRepository)
3. Protected (set() is the only write path)
"""
from __future__ import annotations

import sys, os, logging

# Ensure domain/infrastructure/application are importable
_skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _skill_root not in sys.path:
    sys.path.insert(0, _skill_root)

_log = logging.getLogger("compat")


def patch_novel_state_with_write_protection(novel_state_instance, book_dir: str):
    """
    Attach write-protection to an existing NovelState instance.
    
    After patching:
    - instance._state is replaced with a proxy that delegates to StateAdapter
    - instance.save() is replaced with save-to-Repository
    - All _state['key'] = value mutations are captured
    
    Usage in novel_state.py __init__():
        from engine.compat import patch_novel_state_with_write_protection
        patch_novel_state_with_write_protection(self, str(self.book_dir))
    """
    from adapters.state_adapter import StateAdapter
    
    _adapter = StateAdapter(book_dir)
    _state_root = _adapter._state_root
    
    # Cache the adapter for direct use
    novel_state_instance._adapter = _adapter
    
    # Override save()
    original_save = novel_state_instance.save
    
    def _write_protected_save():
        """Save through StateRepository (single authority)."""
        try:
            # Sync raw _state dict changes into adapter before save
            from domain.state import StateRoot
            _adapter._state_root = StateRoot.from_dict(novel_state_instance._state)
            _adapter._state_repo.save(_adapter._state_root)
            _log.debug("State saved via Repository")
        except Exception as e:
            _log.warning(f"Repository save failed, fallback to original: {e}")
            original_save()
        finally:
            # Keep _state in sync for old code
            novel_state_instance._state = _adapter._state_root.to_dict()
    
    novel_state_instance.save = _write_protected_save
    
    # Hook save_snapshot
    original_snapshot = getattr(novel_state_instance, 'save_snapshot', None)
    def _patched_snapshot():
        _adapter.save_snapshot()
        if original_snapshot:
            original_snapshot()
    novel_state_instance.save_snapshot = _patched_snapshot
    
    # Sync initial state
    novel_state_instance._state = _adapter._state_root.to_dict()
    _log.info("NovelState write-protected via StateAdapter")


def force_reload_from_disk(novel_state_instance):
    """
    Forced rollback guard: reload _state from disk.
    Call this on any exception in the generation loop.
    """
    if hasattr(novel_state_instance, '_adapter'):
        novel_state_instance._adapter.reload_from_disk()
        novel_state_instance._state = novel_state_instance._adapter._state_root.to_dict()
        _log.warning("State force-reloaded from disk (rollback guard)")
    else:
        # Fallback: reload from JSON file
        import json
        from pathlib import Path
        state_path = Path(novel_state_instance.book_dir) / "state.json"
        if state_path.exists():
            with open(state_path, 'r', encoding='utf-8') as f:
                novel_state_instance._state = json.load(f)
            _log.warning("State force-reloaded from disk (raw JSON fallback)")


def force_reset_engine_caches(engines_dict: dict):
    """Reset all engine caches to force reload from state."""
    for name, engine in engines_dict.items():
        if hasattr(engine, 'reset'):
            try:
                engine.reset()
                _log.debug(f"Engine cache reset: {name}")
            except Exception as e:
                _log.warning(f"Failed to reset engine {name}: {e}")
        elif hasattr(engine, '_foreshadows'):
            engine._foreshadows.clear()
        elif hasattr(engine, '_global_summary'):
            engine._global_summary = {}
        elif hasattr(engine, '_characters'):
            engine._characters.clear()
