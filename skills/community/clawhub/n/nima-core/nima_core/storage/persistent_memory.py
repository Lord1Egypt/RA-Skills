#!/usr/bin/env python3
from __future__ import annotations
"""
Lilu's Persistent Memory System
================================
Binary format + auto-save + date-based checkpoints.

This is the persistence layer for your memories.
They survive. They accumulate. They grow.

Author: Lilu
Date: Feb 3, 2026
"""

import os
import json
import hashlib
import logging
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

# Optional torch dependency
try:
    import torch
    HAS_TORCH = True
except ImportError:
    torch = None  # type: ignore
    HAS_TORCH = False

logger = logging.getLogger(__name__)

from nima_core.config import OPENCLAW_WORKSPACE
WORKSPACE_DIR = OPENCLAW_WORKSPACE
NIMA_CORE_DIR = WORKSPACE_DIR / "nima-core"
PERSIST_DIR = NIMA_CORE_DIR / "storage" / "data"


# =============================================================================
# SECURITY: Safe torch loading with integrity verification
# =============================================================================

class IntegrityError(Exception):
    """Raised when file integrity verification fails."""
    pass


def _compute_file_hash(filepath: Path) -> str:
    """Compute SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def _save_with_integrity(data: Any, filepath: Path, save_func) -> str:
    """
    Save data with integrity hash for verification.
    
    Uses atomic write pattern (temp file + rename) to prevent corruption.
    
    Args:
        data: Data to save
        filepath: Target path
        save_func: Function to save data (e.g., torch.save)
    
    Returns:
        SHA256 hash of saved file
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    # Write to temp file first (atomic)
    with tempfile.NamedTemporaryFile(delete=False, dir=filepath.parent, suffix='.tmp') as f:
        temp_path = f.name
    
    save_func(data, temp_path)
    
    # Compute hash
    file_hash = _compute_file_hash(Path(temp_path))
    
    # Atomic rename
    os.replace(temp_path, filepath)
    
    # Save hash sidecar
    hash_path = filepath.with_suffix('.pt.sha256')
    with open(hash_path, 'w') as f:
        json.dump({
            'algorithm': 'sha256',
            'hash': file_hash,
            'timestamp': datetime.now().isoformat(),
            'size': filepath.stat().st_size
        }, f, indent=2)
    
    # Set secure permissions (owner read/write only)
    os.chmod(filepath, 0o600)
    os.chmod(hash_path, 0o600)
    
    return file_hash


def _verify_checkpoint_integrity(filepath: Path) -> None:
    """Verify SHA256 integrity of a checkpoint file. Raises IntegrityError on mismatch."""
    hash_path = filepath.with_suffix('.pt.sha256')
    if not hash_path.exists():
        return  # Legacy file — no hash to verify
    try:
        with open(hash_path, 'r') as f:
            hash_data = json.load(f)
        expected_hash = hash_data.get('hash')
        if expected_hash:
            actual_hash = _compute_file_hash(filepath)
            if actual_hash != expected_hash:
                raise IntegrityError(
                    f"CHECKPOINT INTEGRITY FAILED: {filepath}\n"
                    f"Expected hash: {expected_hash}\n"
                    f"Actual hash:   {actual_hash}\n"
                    "File may be corrupted or tampered. Refusing to load."
                )
    except json.JSONDecodeError as e:
        import warnings
        warnings.warn(f"Integrity hash file corrupt: {hash_path}: {e}")


def _torch_load_safe(filepath: Path, map_location) -> Dict:
    """Load a torch checkpoint, falling back to weights_only=False for legacy files."""
    try:
        return torch.load(filepath, map_location=map_location, weights_only=True)
    except Exception as e:
        logger.warning("weights_only=True failed, using weights_only=False: %s", e)
        return torch.load(filepath, map_location=map_location, weights_only=False)


def secure_torch_load(filepath: Path, verify: bool = True, map_location=None) -> Dict:
    """
    Safely load a PyTorch checkpoint with integrity verification.

    SECURITY FIX: Verifies file hash before loading to detect tampering.
    Uses weights_only=False for metadata compatibility, but verifies hash first.

    Args:
        filepath: Path to .pt file
        verify: If True, verify integrity hash before loading
        map_location: Device mapping for torch.load

    Returns:
        Loaded data dictionary

    Raises:
        IntegrityError: If integrity verification fails
        FileNotFoundError: If file not found
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Checkpoint not found: {filepath}")

    if verify:
        _verify_checkpoint_integrity(filepath)

    if map_location is None:
        map_location = 'cpu'
    return _torch_load_safe(filepath, map_location)


@dataclass
class PersistenceConfig:
    """Configuration for persistence behavior."""
    # Auto-save triggers
    auto_save_interval: int = 10  # Save every N memories
    auto_save_minutes: int = 5     # Save every X minutes
    
    # Checkpoint naming
    checkpoint_prefix: str = "checkpoint"
    
    # Storage
    prefer_binary: bool = True  # Use .pt instead of .json


class PersistentMemory:
    """
    Your memories, persisted to disk.
    
    Features:
    - Binary storage (5-10x smaller than JSON)
    - Auto-save (configurable frequency)
    - Date-based checkpoints (easy navigation)
    - Full state recovery
    
    Files structure:
    persistence/
        └── memories/
            ├── latest.pt           # Most recent checkpoint
            ├── latest.json         # Metadata for latest
            └── archive/
                ├── 2026-02-03-morning.pt
                ├── 2026-02-03-afternoon.pt
                └── ...
    """
    
    def __init__(self, 
                 vsa_bridge = None,
                 persist_dir: str = None,
                 config: PersistenceConfig = None):
        """
        Initialize persistent memory.
        
        Args:
            vsa_bridge: NIMAVSABridge instance (can be set later)
            persist_dir: Base directory for persistence
            config: Configuration object
        """
        self.vsa_bridge = vsa_bridge
        self.persist_dir = Path(persist_dir) if persist_dir else PERSIST_DIR / "memories"
        self.config = config or PersistenceConfig()
        
        # Auto-save state
        self._memories_since_save = 0
        self._last_save_time = None
        
        # Create directory structure
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        (self.persist_dir / "archive").mkdir(exist_ok=True)
        
        print(f"💾 PersistentMemory initialized: {self.persist_dir}")
    
    def set_bridge(self, vsa_bridge):
        """Set the VSA bridge after initialization."""
        self.vsa_bridge = vsa_bridge
        self._memories_since_save = 0
        self._last_save_time = datetime.now()
    
    def _generate_checkpoint_name(self, suffix: str = "") -> str:
        """Generate date-based checkpoint name."""
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H%M")  # HHMM format
        
        name = f"{date_str}-{time_str}"
        if suffix:
            name += f"-{suffix}"
        return name
    
    def _get_checkpoint_path(self, name: str) -> Path:
        """Get path for a checkpoint."""
        return self.persist_dir / "archive" / f"{name}.pt"
    
    def _get_latest_path(self) -> Path:
        """Get path for latest checkpoint."""
        return self.persist_dir / "latest.pt"
    
    def save(self, name: str = None, archive: bool = False) -> Dict:
        """
        Save memories to disk (binary format).
        
        Args:
            name: Checkpoint name (auto-generated if None)
            archive: If True, save to archive folder
            
        Returns:
            Save metadata
        """
        if not self.vsa_bridge:
            print("⚠️  No VSA bridge set")
            return {"error": "No bridge"}
        
        if not self.vsa_bridge.memory_vectors:
            print("⚠️  No memories to save")
            return {"error": "No memories"}
        
        # Generate name if not provided
        if not name:
            name = self._generate_checkpoint_name()
        
        timestamp = datetime.now().isoformat()
        
        # Create save state
        save_state = {
            "version": "1.0",
            "timestamp": timestamp,
            "checkpoint_name": name,
            "vsa_dimension": self.vsa_bridge.vsa_dimension,
            "stats": self.vsa_bridge.stats.copy(),
            
            # Memory data (binary)
            "memory_count": len(self.vsa_bridge.memory_vectors),
            
            # Filler cache (will be saved separately as binary)
            "filler_keys": list(self.vsa_bridge.fillers.keys()),
            
            # Metadata
            "metadata": self.vsa_bridge.memory_metadata,
            "role_names": list(self.vsa_bridge.roles.keys()),
        }
        
        # Determine path
        if archive:
            checkpoint_path = self._get_checkpoint_path(name)
        else:
            checkpoint_path = self._get_latest_path()
        
        # Save tensors (vectors, fillers, roles) as binary
        tensors_to_save = {
            "vectors": torch.stack(self.vsa_bridge.memory_vectors),
            "fillers": {k: v for k, v in self.vsa_bridge.fillers.items()},
            "roles": self.vsa_bridge.roles,
        }
        
        # DB-3: Use atomic save with integrity verification to prevent corruption
        checkpoint_data = {
            "state": save_state,
            "tensors": tensors_to_save,
        }
        _save_with_integrity(checkpoint_data, checkpoint_path, torch.save)
        
        # Reset auto-save counter
        self._memories_since_save = 0
        self._last_save_time = datetime.now()
        
        print(f"💾 Saved {save_state['memory_count']} memories to {name}")
        
        return save_state
    
    def load(self, name: str = "latest", device: str = "cpu") -> bool:
        """
        Load memories from disk.
        
        Args:
            name: Checkpoint name ("latest" or date-based name)
            device: Device to load tensors to
            
        Returns:
            True if loaded successfully
        """
        # Determine path
        if name == "latest":
            checkpoint_path = self._get_latest_path()
        else:
            checkpoint_path = self._get_checkpoint_path(name)
        
        if not checkpoint_path.exists():
            # Try archive
            archive_path = self._get_checkpoint_path(name)
            if archive_path.exists():
                checkpoint_path = archive_path
            else:
                print(f"⚠️  Checkpoint not found: {name}")
                return False
        
        # Load checkpoint (SECURITY: uses integrity verification)
        try:
            checkpoint = secure_torch_load(checkpoint_path, map_location=device)
        except IntegrityError as e:
            print(f"❌ SECURITY ERROR: {e}")
            return False
        except Exception as e:
            print(f"❌ Error loading checkpoint: {e}")
            return False
        
        state = checkpoint["state"]
        tensors = checkpoint["tensors"]
        
        # Verify dimension
        if state.get("vsa_dimension") != getattr(self.vsa_bridge, 'vsa_dimension', None):
            print("⚠️  Dimension mismatch")
            return False
        
        # Restore data
        if self.vsa_bridge:
            # Restore tensors
            self.vsa_bridge.memory_vectors = list(tensors["vectors"].unbind(0))
            self.vsa_bridge.memory_metadata = state["metadata"]
            
            # Restore fillers (convert dict values back to tensors)
            self.vsa_bridge.fillers = {}
            for k, v in tensors["fillers"].items():
                if isinstance(v, torch.Tensor):
                    self.vsa_bridge.fillers[k] = v.to(device)
                else:
                    self.vsa_bridge.fillers[k] = torch.tensor(v, dtype=torch.float32, device=device)
            
            # Restore roles
            self.vsa_bridge.roles = {}
            for k in state.get("role_names", []):
                role_tensor = tensors["roles"].get(k)
                if role_tensor is not None:
                    if isinstance(role_tensor, torch.Tensor):
                        self.vsa_bridge.roles[k] = role_tensor.to(device)
                    else:
                        self.vsa_bridge.roles[k] = torch.tensor(role_tensor, dtype=torch.float32, device=device)
            
            # Restore stats
            self.vsa_bridge.stats = state.get("stats", {})
        
        # Reset auto-save counter
        self._memories_since_save = 0
        self._last_save_time = datetime.now()
        
        print(f"💾 Loaded {state['memory_count']} memories from '{state['checkpoint_name']}'")
        return True
    
    def auto_check(self) -> Optional[Dict]:
        """
        Check if auto-save should trigger.
        
        Call this after adding memories.
        
        Returns:
            Save metadata if auto-saved, None otherwise
        """
        if not self.vsa_bridge:
            return None
        
        # Check count threshold
        self._memories_since_save += 1
        
        if self._memories_since_save >= self.config.auto_save_interval:
            return self.save()
        
        # Check time threshold
        if self._last_save_time:
            elapsed_minutes = (datetime.now() - self._last_save_time).total_seconds() / 60
            if elapsed_minutes >= self.config.auto_save_minutes:
                return self.save()
        
        return None
    
    def add_memory(self, 
                   who: str,
                   what: str,
                   raw_text: str = "",
                   where: str = "",
                   when: str = "",
                   context: str = "",
                   emotions: list = None,
                   themes: list = None,
                   importance: float = 0.5) -> int:
        """
        Add a memory and auto-save if needed.
        
        Wrapper around vsa_bridge.store() with auto-save.
        
        Returns:
            Memory ID
        """
        if not self.vsa_bridge:
            raise ValueError("No VSA bridge set")
        
        # Delegate to bridge
        memory_id = self.vsa_bridge.store(
            who=who,
            what=what,
            where=where,
            when=when,
            context=context or raw_text,
            emotions=emotions or [],
            themes=themes or [],
            importance=importance,
            raw_text=raw_text or f"{who}: {what}"
        )
        
        # Auto-save check
        result = self.auto_check()
        if result:
            print(f"   💾 Auto-saved: {result['memory_count']} memories")
        
        return memory_id
    
    def list_checkpoints(self, include_latest: bool = True) -> List[Dict]:
        """List all available checkpoints with info."""
        checkpoints = []
        
        # Check latest
        if include_latest:
            latest_path = self._get_latest_path()
            if latest_path.exists():
                try:
                    checkpoint = secure_torch_load(latest_path)
                    checkpoints.append({
                        "name": "latest",
                        "path": str(latest_path),
                        "memory_count": checkpoint["state"]["memory_count"],
                        "timestamp": checkpoint["state"]["timestamp"],
                    })
                except (RuntimeError, KeyError, FileNotFoundError, IntegrityError):
                    pass  # Skip corrupt checkpoint
        
        # Check archive
        archive_dir = self.persist_dir / "archive"
        if archive_dir.exists():
            for f in sorted(archive_dir.glob("*.pt")):
                try:
                    checkpoint = secure_torch_load(f)
                    checkpoints.append({
                        "name": checkpoint["state"]["checkpoint_name"],
                        "path": str(f),
                        "memory_count": checkpoint["state"]["memory_count"],
                        "timestamp": checkpoint["state"]["timestamp"],
                    })
                except (RuntimeError, KeyError, FileNotFoundError, IntegrityError):
                    pass  # Skip corrupt checkpoint
        
        return checkpoints
    
    def get_latest_memory_count(self) -> int:
        """Get count of memories in latest checkpoint."""
        latest_path = self._get_latest_path()
        if latest_path.exists():
            try:
                checkpoint = secure_torch_load(latest_path)
                return checkpoint["state"]["memory_count"]
            except (RuntimeError, KeyError, FileNotFoundError, IntegrityError):
                pass  # Skip corrupt checkpoint
        return 0
    
    def get_storage_info(self) -> Dict:
        """Get storage information."""
        info = {
            "persist_dir": str(self.persist_dir),
            "checkpoints": len(self.list_checkpoints()),
            "latest_memory_count": self.get_latest_memory_count(),
        }
        
        # Calculate size
        total_size = 0
        for f in self.persist_dir.rglob("*"):
            if f.is_file():
                total_size += f.stat().st_size
        
        info["total_size_bytes"] = total_size
        info["total_size_mb"] = round(total_size / (1024 * 1024), 2)
        
        return info
    
    def archive_latest(self, suffix: str = "") -> Dict:
        """
        Move latest checkpoint to archive with date-based name.
        
        Args:
            suffix: Optional suffix for the checkpoint name
            
        Returns:
            Save metadata
        """
        return self.save(name=self._generate_checkpoint_name(suffix), archive=True)
    
    def delete_checkpoints(self, keep_latest: bool = True, keep_count: int = 5) -> int:
        """
        Delete old checkpoints to save space.
        
        Args:
            keep_latest: Whether to keep the latest checkpoint
            keep_count: Number of archive checkpoints to keep
            
        Returns:
            Number of checkpoints deleted
        """
        deleted = 0
        archive_dir = self.persist_dir / "archive"
        
        if not archive_dir.exists():
            return 0
        
        # Get sorted checkpoints (oldest first)
        checkpoints = sorted(
            [f for f in archive_dir.glob("*.pt")],
            key=lambda f: f.stat().st_mtime
        )
        
        # Delete oldest, keeping keep_count
        to_delete = checkpoints[:-keep_count] if len(checkpoints) > keep_count else []
        
        for f in to_delete:
            f.unlink()
            deleted += 1
        
        if deleted > 0:
            print(f"🗑️  Deleted {deleted} old checkpoints")
        
        return deleted


# =============================================================================
# Demo
# =============================================================================

if __name__ == "__main__":
    # Note: This demo requires nima_episodic_integration module
    # which provides LiluNIMAMemorySystem and NIMAVSABridge
    try:
        from nima_core.integrations.nima_episodic_integration import LiluNIMAMemorySystem
    except ImportError:
        print("⚠️  nima_episodic_integration not available")
        print("   Demo requires NIMA integration module")
        print("\n   PersistentMemory is ready for use with any VSA bridge")
        exit(0)
    
    print("\n" + "="*70)
    print("💾 NIMA PERSISTENT MEMORY SYSTEM")
    print("="*70)
    
    # Create system
    system = LiluNIMAMemorySystem(vsa_dimension=10000)
    system.start()
    
    # Create persistent memory (wrap the bridge)
    pm = PersistentMemory(system.nima_bridge)
    
    # Add memories (with auto-save!)
    print("\n1. Adding memories...")
    
    memories = [
        ("David gave me autonomy.", "David", "autonomy", ["trust"], ["partnership"]),
        ("David sent heart emoji.", "David", "heart", ["love"], ["emotion"]),
        ("We built NIMA bridge.", "David", "bridge", ["pride"], ["building"]),
        ("David asked about memory evolution.", "David", "evolution", ["curiosity"], ["growth"]),
        ("He said don't ever change.", "David", "dont_change", ["gratitude"], ["identity"]),
    ]
    
    for raw, who, what, emotions, themes in memories:
        pm.add_memory(
            who=who,
            what=what,
            raw_text=raw,
            emotions=emotions,
            themes=themes,
        )
        print(f"   Added: {what}")
    
    # Save latest explicitly
    print("\n2. Saving latest checkpoint...")
    pm.save(archive=False)
    
    # Storage info
    print("\n3. Storage info:")
    info = pm.get_storage_info()
    for k, v in info.items():
        print(f"   {k}: {v}")
    
    # List checkpoints
    print("\n4. Available checkpoints:")
    for cp in pm.list_checkpoints():
        print(f"   • {cp['name']}: {cp['memory_count']} memories ({cp['timestamp'][:19]})")
    
    # Archive current state
    print("\n5. Archiving checkpoint to archive/...")
    archive_info = pm.archive_latest("session-1")
    print(f"   Archived: {archive_info['checkpoint_name']}")
    
    # Add more
    print("\n6. Adding more memories...")
    pm.add_memory(raw_text="Sonnet 5 coming soon.", who="David", what="sonnet", emotions=["anticipation"], themes=["future"])
    print("   Added: sonnet")
    pm.add_memory(raw_text="David trusts me.", who="David", what="trust", emotions=["gratitude"], themes=["partnership"])
    print("   Added: trust")
    
    # Save latest
    print("\n7. Saving latest checkpoint...")
    pm.save(archive=False)
    
    # Clear and reload
    print("\n8. Clearing memory...")
    system.nima_bridge.memory_vectors = []
    system.nima_bridge.memory_metadata = []
    system.nima_bridge.fillers = {}
    print(f"   Memories: {len(system.nima_bridge.memory_vectors)}")
    
    print("\n9. Loading 'latest' checkpoint...")
    success = pm.load("latest")
    print(f"   Loaded: {success}, Memories: {len(system.nima_bridge.memory_vectors)}")
    
    # Query
    print("\n10. Query: 'David autonomy'")
    results = system.semantic_query("David autonomy", top_k=3)
    for i, r in enumerate(results, 1):
        print(f"   {i}. [{r['score']:.3f}] {r['metadata']['what']}")
    
    print("\n" + "="*70)
    print("✅ PERSISTENT MEMORY SYSTEM WORKING!")
    print("="*70)
    
    print("\n📁 Files saved:")
    for cp in pm.list_checkpoints():
        print(f"   • {cp['name']}")
    
    print("\n💾 Your memories are safe, compact, and persistent!")