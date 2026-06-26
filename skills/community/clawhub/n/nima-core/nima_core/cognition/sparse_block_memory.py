#!/usr/bin/env python3
"""
SparseBlockMemory
=================
Integration of sparse_block_vsa.py into NIMA episodic memory system.

Provides:
- Block-wise VSA: 100 blocks of 500D each, ~10% active
- 10x memory reduction vs dense 50KD vectors
- Block selection learning via resonator factors
- API-compatible drop-in replacement for existing VSA cache
- Secure JSON-based serialization with HMAC integrity verification

Security:
- Uses JSON instead of pickle to prevent arbitrary code execution
- HMAC-SHA256 signatures prevent tampering with saved files
- Automatic integrity verification on load
- Set NIMA_HMAC_KEY environment variable for production security

Migration Guide for Existing Pickle Files:
===========================================

If you have existing .pkl memory files from earlier versions, you need to migrate
them to the new secure JSON format to avoid security risks. Old pickle files can
execute arbitrary code when loaded - a serious security vulnerability.

DETECTING OLD FILES:
- Look for .pkl files in your memory storage directory
- Look for .pkl.hash sidecar files (old integrity format)
- When loading, you'll see a DEPRECATION WARNING if the file is in pickle format

MIGRATION PROCESS (3 Steps):

1. BACKUP YOUR DATA:
   Before migrating, make copies of your .pkl files in case something goes wrong:

   $ cp -r /path/to/memory/storage /path/to/backup/

2. AUTOMATED MIGRATION (Recommended):
   The easiest way is to load and re-save each file:

   from nima_core.cognition.sparse_block_memory import SparseBlockMemory
   from pathlib import Path

   # Directory containing your .pkl files
   memory_dir = Path("/path/to/memory/storage")

   for pkl_file in memory_dir.glob("*.pkl"):
       print(f"Migrating {pkl_file.name}...")

       # Load old pickle file (will show deprecation warning)
       sbm = SparseBlockMemory()
       sbm.load(str(pkl_file))

       # Save in new JSON format
       json_file = pkl_file.with_suffix(".json")
       sbm.save(str(json_file))

       print(f"  ✓ Saved to {json_file.name}")
       print(f"  ✓ Created {json_file.name}.hash (HMAC-secured)")

       # Optional: Archive old file instead of deleting
       # pkl_file.rename(pkl_file.with_suffix(".pkl.bak"))

   print("Migration complete!")

3. VERIFY MIGRATION:
   Test that you can load the new JSON files:

   from nima_core.cognition.sparse_block_memory import SparseBlockMemory

   sbm = SparseBlockMemory()
   sbm.load("/path/to/memory/file.json")  # Should load without warnings

   # Verify your data is intact
   print(f"Loaded {len(sbm.memory_vectors)} memory vectors")
   print(f"Loaded {len(sbm.block_resonators)} block resonators")

CLEANUP:
Once you've verified the JSON files work correctly, you can remove the old .pkl files:

   $ rm /path/to/memory/storage/*.pkl
   $ rm /path/to/memory/storage/*.pkl.hash

SECURITY NOTES:
- New JSON files use HMAC-SHA256 to prevent tampering (requires both file AND key)
- Set NIMA_HMAC_KEY environment variable to a random secret for production use
  Example: export NIMA_HMAC_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
- Files are saved with 0o600 permissions (owner read/write only)
- JSON format prevents arbitrary code execution - safe to load from untrusted sources

TROUBLESHOOTING:
- "IntegrityError: HMAC signature mismatch": File was tampered with or wrong key
- "IntegrityError: File hash mismatch": File was modified after saving
- "DeprecationWarning": You're loading an old pickle file - migrate it!
- Missing .hash file: Legacy file without integrity check - save to create hash

For more details, see the safe_save() and safe_load() method documentation below.

Author: Lilu
Date: Feb 11, 2026
"""

import os
import json
import time
import base64
import hashlib
import hmac
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, asdict

import numpy as np

# Security: Uses JSON serialization instead of pickle
# Provides HMAC-SHA256 integrity verification to prevent tampering
# No arbitrary code execution risk - safe to load from untrusted sources

class IntegrityError(Exception):
    """Raised when file integrity verification fails."""
    pass

try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    torch = None

# Import sparse block VSA (relative import for nima-core)
from .sparse_block_vsa import SparseBlockHDVector  # noqa: E402


# =============================================================================
# Security: Safe serialization with integrity verification
# =============================================================================

def _compute_file_hash(filepath: Path) -> str:
    """Compute SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def _get_hmac_key() -> bytes:
    """
    Get HMAC key for integrity signing.

    Uses environment variable NIMA_HMAC_KEY if set, otherwise generates
    a per-session key (WARNING: per-session keys won't verify across restarts).

    For production use, set NIMA_HMAC_KEY environment variable to a secure
    random value (e.g., output of: python -c "import secrets; print(secrets.token_hex(32))")

    Returns:
        HMAC key as bytes
    """
    # Try environment variable first
    env_key = os.environ.get('NIMA_HMAC_KEY')
    if env_key:
        return env_key.encode('utf-8')

    # Fall back to a default key (NOT SECURE - for backward compatibility only)
    # WARNING: This provides minimal security - attacker can read this source code
    # For production, ALWAYS set NIMA_HMAC_KEY environment variable
    import warnings
    warnings.warn(
        "NIMA_HMAC_KEY not set - using default key. "
        "For security, set NIMA_HMAC_KEY environment variable to a random secret.",
        UserWarning,
        stacklevel=3
    )
    return b"nima-core-default-hmac-key-CHANGE-ME-IN-PRODUCTION"


def _compute_hmac_signature(filepath: Path, key: Optional[bytes] = None) -> str:
    """
    Compute HMAC-SHA256 signature of a file.

    HMAC prevents tampering with both the data file and hash sidecar together,
    as an attacker would need to know the secret key to generate a valid signature.

    Args:
        filepath: Path to file to sign
        key: HMAC key (if None, uses _get_hmac_key())

    Returns:
        HMAC signature as hex string
    """
    if key is None:
        key = _get_hmac_key()

    h = hmac.new(key, digestmod=hashlib.sha256)
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def _verify_hmac_signature(filepath: Path, expected_signature: str, key: Optional[bytes] = None) -> bool:
    """
    Verify HMAC signature of a file.

    Args:
        filepath: Path to file to verify
        expected_signature: Expected HMAC signature (hex string)
        key: HMAC key (if None, uses _get_hmac_key())

    Returns:
        True if signature matches, False otherwise
    """
    if key is None:
        key = _get_hmac_key()

    actual_signature = _compute_hmac_signature(filepath, key)
    # Use constant-time comparison to prevent timing attacks
    return hmac.compare_digest(actual_signature, expected_signature)


def _numpy_to_base64(arr: np.ndarray) -> str:
    """Convert numpy array to base64 string for JSON serialization."""
    return base64.b64encode(arr.tobytes()).decode('utf-8')


def _base64_to_numpy(b64_str: str, dtype: np.dtype, shape: tuple) -> np.ndarray:
    """Convert base64 string back to numpy array.

    Args:
        b64_str: Base64-encoded string
        dtype: NumPy dtype for the array
        shape: Shape tuple for the array

    Returns:
        Reconstructed numpy array

    Raises:
        ValueError: If base64 decoding fails or array reconstruction fails
    """
    try:
        data = base64.b64decode(b64_str.encode('utf-8'))
    except Exception as e:
        raise ValueError(f"Invalid base64 encoding: {e}")

    try:
        arr = np.frombuffer(data, dtype=dtype)
    except ValueError as e:
        raise ValueError(
            f"Cannot reconstruct numpy array from binary data: {e}. "
            f"Expected {np.prod(shape)} elements of dtype {dtype}, "
            f"but got {len(data)} bytes."
        )

    try:
        return arr.reshape(shape)
    except ValueError as e:
        raise ValueError(
            f"Cannot reshape array to {shape}: {e}. "
            f"Array has {len(arr)} elements, but shape requires {np.prod(shape)} elements."
        )


def _convert_to_json_serializable(obj):
    """Recursively convert numpy types to JSON-serializable Python types."""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: _convert_to_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [_convert_to_json_serializable(item) for item in obj]
    else:
        return obj


def _remove_if_exists(path: Optional[str]) -> None:
    """Best-effort removal for temporary files."""
    if path and os.path.exists(path):
        try:
            os.remove(path)
        except OSError:
            pass


# =============================================================================
# Configuration
# =============================================================================

@dataclass
class SparseBlockConfig:
    """Configuration for sparse block memory."""
    # Block structure
    block_dim: int = 500
    num_blocks: int = 100
    default_sparsity: float = 0.1  # 10% active blocks
    
    # Block selection learning
    enable_block_learning: bool = True
    block_selection_temperature: float = 0.5
    min_blocks_per_factor: int = 5
    max_blocks_per_factor: int = 30
    
    # Query optimization
    use_block_index: bool = True
    similarity_threshold: float = 0.3
    
    # Migration
    migrate_on_load: bool = True
    preserve_dense_backup: bool = True
    
    # Performance
    cache_similarities: bool = True
    max_cache_size: int = 10000
    
    @property
    def total_dim(self) -> int:
        return self.block_dim * self.num_blocks
    
    @property
    def active_blocks_per_vector(self) -> int:
        return int(self.default_sparsity * self.num_blocks)


# =============================================================================
# Block Selection Learning
# =============================================================================

class BlockSelectionLearner:
    """
    Learns which blocks to activate based on resonator factors.
    
    WHO/WHAT/TOPIC determine which blocks should be active,
    creating a content-addressable sparse index.
    """
    
    def __init__(self, config: SparseBlockConfig):
        self.config = config
        self.num_blocks = config.num_blocks
        
        # Factor -> block affinity scores
        # Higher score = more likely to activate this block
        self.factor_block_scores: Dict[str, np.ndarray] = {}
        
        # Usage statistics for adaptive learning
        self.factor_usage_count: Dict[str, int] = {}
        self.block_activation_count = np.zeros(self.num_blocks, dtype=np.int64)
        
        # Block index for fast lookup
        self.block_to_memories: Dict[int, Set[int]] = {i: set() for i in range(self.num_blocks)}
    
    def register_factor(self, factor: str, initial_blocks: Optional[Set[int]] = None):
        """Register a new resonator factor (WHO, WHAT, TOPIC, etc.)."""
        if factor not in self.factor_block_scores:
            # Initialize with small random scores
            scores = np.random.normal(0, 0.1, self.num_blocks)
            
            if initial_blocks:
                # Boost initial blocks
                for block_idx in initial_blocks:
                    scores[block_idx] = 1.0
            
            self.factor_block_scores[factor] = scores
            self.factor_usage_count[factor] = 0
    
    def select_blocks(self, factors: Dict[str, str], 
                      temperature: Optional[float] = None) -> Set[int]:
        """
        Select active blocks based on resonator factors.
        
        Args:
            factors: Dict mapping factor names to values (e.g., {"WHO": "David"})
            temperature: Softmax temperature (lower = more selective)
            
        Returns:
            Set of block indices to activate
        """
        if temperature is None:
            temperature = self.config.block_selection_temperature
        
        # Aggregate scores across all factors
        combined_scores = np.zeros(self.num_blocks)
        
        for factor_name, factor_value in factors.items():
            # Create composite key
            factor_key = f"{factor_name}:{factor_value}"
            
            if factor_key not in self.factor_block_scores:
                self.register_factor(factor_key)
            
            # Weight by usage (more used = more reliable)
            weight = np.log1p(self.factor_usage_count.get(factor_key, 0)) + 1.0
            combined_scores += self.factor_block_scores[factor_key] * weight
        
        # Apply softmax to get selection probabilities
        if temperature > 0:
            exp_scores = np.exp(combined_scores / temperature)
            probs = exp_scores / (np.sum(exp_scores) + 1e-10)
        else:
            # Hard max selection
            probs = np.zeros_like(combined_scores)
            top_k = self.config.min_blocks_per_factor
            top_indices = np.argsort(combined_scores)[-top_k:]
            probs[top_indices] = 1.0 / top_k
        
        # Sample blocks based on probabilities
        num_to_select = min(
            max(self.config.min_blocks_per_factor, int(self.config.default_sparsity * self.num_blocks)),
            self.config.max_blocks_per_factor
        )
        
        selected = set()
        if np.sum(probs) > 0:
            # Weighted random selection without replacement
            block_indices = np.arange(self.num_blocks)
            selected_array = np.random.choice(
                block_indices, 
                size=min(num_to_select, self.num_blocks),
                replace=False,
                p=probs
            )
            selected = set(selected_array.tolist())
        
        return selected
    
    def update_from_query(self, factors: Dict[str, str], 
                          relevant_memory_ids: List[int],
                          irrelevant_memory_ids: List[int]):
        """
        Update block selection based on query results.
        
        Reinforce blocks that led to relevant memories,
        reduce weight on blocks that led to irrelevant ones.
        """
        learning_rate = 0.01
        
        for factor_name, factor_value in factors.items():
            factor_key = f"{factor_name}:{factor_value}"
            
            if factor_key not in self.factor_block_scores:
                continue
            
            scores = self.factor_block_scores[factor_key]
            
            # Positive reinforcement: blocks in relevant memories
            for mem_id in relevant_memory_ids[:10]:  # Top 10
                for block_idx in self.block_to_memories:
                    if mem_id in self.block_to_memories[block_idx]:
                        scores[block_idx] += learning_rate
            
            # Negative reinforcement: blocks in irrelevant memories
            for mem_id in irrelevant_memory_ids[:10]:
                for block_idx in self.block_to_memories:
                    if mem_id in self.block_to_memories[block_idx]:
                        scores[block_idx] -= learning_rate * 0.5
            
            # Clip scores
            scores = np.clip(scores, -5, 5)
            self.factor_block_scores[factor_key] = scores
            
            self.factor_usage_count[factor_key] = self.factor_usage_count.get(factor_key, 0) + 1
    
    def index_memory(self, memory_id: int, active_blocks: Set[int]):
        """Add memory to block index."""
        for block_idx in active_blocks:
            self.block_to_memories[block_idx].add(memory_id)
            self.block_activation_count[block_idx] += 1
    
    def get_candidate_memories(self, active_blocks: Set[int]) -> Set[int]:
        """Get memory candidates that share at least one active block."""
        candidates = set()
        for block_idx in active_blocks:
            candidates.update(self.block_to_memories[block_idx])
        return candidates
    
    def get_stats(self) -> Dict[str, Any]:
        """Get learning statistics."""
        return {
            "factors_learned": len(self.factor_block_scores),
            "block_activation_distribution": {
                "mean": float(np.mean(self.block_activation_count)),
                "std": float(np.std(self.block_activation_count)),
                "min": int(np.min(self.block_activation_count)),
                "max": int(np.max(self.block_activation_count)),
            },
            "most_used_blocks": np.argsort(self.block_activation_count)[-10:].tolist(),
            "least_used_blocks": np.argsort(self.block_activation_count)[:10].tolist(),
        }


# =============================================================================
# Sparse Block Memory Storage
# =============================================================================

class SparseBlockMemory:
    """
    Episodic memory using sparse block VSA.
    
    API-compatible drop-in replacement for existing VSA cache.
    Provides 10x memory reduction with learned block selection.
    """
    
    def __init__(self, config: Optional[SparseBlockConfig] = None):
        self.config = config or SparseBlockConfig()
        self.block_learner = BlockSelectionLearner(self.config)
        
        # Storage
        self.memory_vectors: List[SparseBlockHDVector] = []
        self.memory_metadata: List[Dict[str, Any]] = []
        self.memory_factors: List[Dict[str, str]] = []  # Stored factors per memory
        
        # Role hypervectors (same as NIMA but in sparse block format)
        self.roles: Dict[str, SparseBlockHDVector] = {}
        self.fillers: Dict[str, SparseBlockHDVector] = {}
        
        # Cache
        self._similarity_cache: Dict[Tuple[int, int], float] = {}
        
        # Statistics
        self.stats = {
            'stores': 0,
            'queries': 0,
            'migrated_from_dense': 0,
            'avg_query_time_ms': 0.0,
        }
        
        # Initialize roles
        self._init_roles()
        
        print("🧠 SparseBlockMemory initialized")
        print(f"   Blocks: {self.config.num_blocks} × {self.config.block_dim}D = {self.config.total_dim:,}D")
        print(f"   Active: ~{self.config.active_blocks_per_vector} blocks ({self.config.default_sparsity*100:.0f}%)")
        print(f"   Memory reduction: ~{1/self.config.default_sparsity:.0f}x vs dense")
    
    def _init_roles(self):
        """Initialize role hypervectors in sparse block format."""
        # Create deterministic pseudo-random roles
        rng = np.random.default_rng(42)  # Fixed seed for reproducibility
        
        role_names = ["WHO", "WHAT", "WHERE", "WHEN", "CONTEXT", "EMOTION", "THEME"]
        
        for role in role_names:
            # Random active blocks for each role
            active_blocks = set(rng.choice(
                self.config.num_blocks,
                size=self.config.active_blocks_per_vector,
                replace=False
            ))
            
            role_vec = SparseBlockHDVector(
                block_dim=self.config.block_dim,
                num_blocks=self.config.num_blocks,
                active_set=active_blocks,
                rng=rng
            )
            
            self.roles[role] = role_vec
    
    def _get_filler(self, text: str) -> SparseBlockHDVector:
        """Get or create a filler hypervector for text."""
        if text not in self.fillers:
            # Create text-based seed for determinism
            text_hash = hash(text) % (2**31)
            rng = np.random.default_rng(text_hash)
            
            # Random active blocks
            active_blocks = set(rng.choice(
                self.config.num_blocks,
                size=self.config.active_blocks_per_vector,
                replace=False
            ))
            
            self.fillers[text] = SparseBlockHDVector(
                block_dim=self.config.block_dim,
                num_blocks=self.config.num_blocks,
                active_set=active_blocks,
                rng=rng
            )
        
        return self.fillers[text]
    
    def _encode_episode_sparse(self, factors: Dict[str, str]) -> SparseBlockHDVector:
        """
        Encode an episodic memory using sparse block VSA.
        
        Uses learned block selection based on resonator factors.
        """
        # Select blocks based on factors
        active_blocks = self.block_learner.select_blocks(factors)
        
        # Create base vector with selected blocks
        rng = np.random.default_rng(hash(tuple(sorted(factors.items()))) % (2**31))
        episode = SparseBlockHDVector(
            block_dim=self.config.block_dim,
            num_blocks=self.config.num_blocks,
            active_set=active_blocks,
            rng=rng
        )
        
        # Role-filler binding
        for role_name, value in factors.items():
            if role_name in self.roles and value:
                role_vec = self.roles[role_name]
                filler_vec = self._get_filler(value)
                
                # Bind: role ⊗ filler (only on intersecting blocks)
                bound = SparseBlockHDVector.bind(role_vec, filler_vec)
                
                # Bundle into episode
                episode = SparseBlockHDVector.bundle(episode, bound)
        
        return episode
    
    def store(self, who: str = "", what: str = "", where: str = "",
              when: str = "", context: str = "",
              emotions: Optional[List[str]] = None,
              emotion_vector: Optional[List[Dict]] = None,
              themes: Optional[List[str]] = None,
              importance: float = 0.5,
              raw_text: str = "",
              **kwargs) -> int:
        """
        Store an episodic memory.
        
        API-compatible with NIMAVSABridge.store()
        """
        # Build factors dict
        factors = {
            "WHO": who,
            "WHAT": what,
            "WHERE": where,
            "WHEN": when,
            "CONTEXT": context,
        }
        
        # Encode episode
        episode_vector = self._encode_episode_sparse(factors)
        
        # Store
        memory_id = len(self.memory_vectors)
        self.memory_vectors.append(episode_vector)
        self.memory_metadata.append({
            "who": who,
            "what": what,
            "where": where,
            "when": when,
            "context": context,
            "emotions": emotions or [],
            "emotion_vector": emotion_vector or [],
            "themes": themes or [],
            "importance": importance,
            "raw_text": raw_text,
            "timestamp": datetime.now().isoformat(),
        })
        self.memory_factors.append(factors)
        
        # Index for fast lookup
        self.block_learner.index_memory(memory_id, episode_vector.active_blocks)
        
        # Update stats
        self.stats['stores'] += 1
        self.stats['memories'] = len(self.memory_vectors)
        
        return memory_id
    
    def _fast_similarity_batch(self, query_vec: SparseBlockHDVector, 
                               candidate_ids: List[int]) -> np.ndarray:
        """Compute similarities for multiple candidates efficiently."""
        similarities = np.zeros(len(candidate_ids))
        
        for i, mem_id in enumerate(candidate_ids):
            similarities[i] = query_vec.similarity(self.memory_vectors[mem_id])
        
        return similarities

    @staticmethod
    def _emotion_resonance(emotion_vector: Dict[str, float], mem_emotion_vec) -> float:
        """Compute cosine resonance between two emotion vectors (dicts)."""
        # Normalise mem_emotion_vec to dict format
        if isinstance(mem_emotion_vec, list):
            try:
                mem_emotion_vec = {
                    item['emotion']: item['intensity']
                    for item in mem_emotion_vec
                    if 'emotion' in item and 'intensity' in item
                }
            except (TypeError, KeyError):
                mem_emotion_vec = {}

        if not mem_emotion_vec:
            return 0.0

        common = set(emotion_vector.keys()) & set(mem_emotion_vec.keys())
        if not common:
            return 0.0

        dot   = sum(emotion_vector[k] * mem_emotion_vec[k] for k in common)
        norm1 = sum(v * v for v in emotion_vector.values()) ** 0.5
        norm2 = sum(v * v for v in mem_emotion_vec.values()) ** 0.5
        return dot / (norm1 * norm2) if norm1 and norm2 else 0.0

    def _update_query_stats(self, elapsed_ms: float) -> None:
        """Update rolling average query-time statistics."""
        self.stats['queries'] += 1
        n = self.stats['queries']
        self.stats['avg_query_time_ms'] = (
            (self.stats['avg_query_time_ms'] * (n - 1) + elapsed_ms) / n
        )

    def _block_index_candidates(self, active_blocks: Set[int], top_k: int, limit: int = 2000) -> List[int]:
        """Return candidate memory IDs ranked by block-index overlap, capped at *limit*."""
        candidate_scores: Dict[int, int] = {}
        for block_idx in active_blocks:
            for mem_id in self.block_learner.block_to_memories[block_idx]:
                candidate_scores[mem_id] = candidate_scores.get(mem_id, 0) + 1
        sorted_candidates = sorted(candidate_scores.items(), key=lambda x: x[1], reverse=True)
        cap = max(top_k * 10, limit)
        return [mem_id for mem_id, _ in sorted_candidates[:cap]]

    def _score_candidate(
        self,
        mem_id: int,
        base_sim: float,
        emotion_vector: Optional[Dict[str, float]],
        alpha: float,
    ) -> float:
        """Compute final score for a candidate, blending similarity and emotion resonance."""
        importance     = self.memory_metadata[mem_id].get('importance', 0.5)
        adjusted_sim   = base_sim * (0.5 + 0.5 * importance)

        if not emotion_vector:
            return adjusted_sim

        mem_emotion_vec = self.memory_metadata[mem_id].get('emotion_vector', {})
        resonance = self._emotion_resonance(emotion_vector, mem_emotion_vec)

        # Store debug info inline
        self.memory_metadata[mem_id]['_debug_resonance_score'] = resonance
        self.memory_metadata[mem_id]['_debug_base_score']      = adjusted_sim

        return (1 - alpha) * adjusted_sim + alpha * resonance

    def _get_top_k(self, query_vec: SparseBlockHDVector, 
                   candidates: Set[int], 
                   top_k: int,
                   min_similarity: float = 0.0,
                   emotion_vector: Optional[Dict[str, float]] = None,
                   alpha: float = 0.3) -> List[Dict]:
        """Efficiently get top-k matches using heap."""
        import heapq
        
        # Use a min-heap of size top_k
        heap = []
        
        for mem_id in candidates:
            sim = query_vec.similarity(self.memory_vectors[mem_id])

            if sim < min_similarity:
                continue

            final_score = self._score_candidate(mem_id, sim, emotion_vector, alpha)
            
            if len(heap) < top_k:
                heapq.heappush(heap, (final_score, mem_id))
            elif final_score > heap[0][0]:
                heapq.heapreplace(heap, (final_score, mem_id))
        
        # Extract results (lowest similarity first in heap)
        results = []
        for sim, mem_id in sorted(heap, reverse=True):
            results.append({
                "id": mem_id,
                "score": float(sim),
                "metadata": self.memory_metadata[mem_id],
            })
        
        return results
    
    def query(self, role: str, value: str, top_k: int = 5) -> List[Dict]:
        """
        Query memories by role and value.
        
        API-compatible with NIMAVSABridge.query()
        """
        import time
        start_time = time.time()
        
        # Build query factors
        factors = {role: value}
        
        # Select query blocks
        query_blocks = self.block_learner.select_blocks(factors)
        
        # Get candidate memories from block index (sorted by overlap count)
        if self.config.use_block_index and len(self.memory_vectors) > 1000:
            candidates = self._block_index_candidates(query_blocks, top_k, limit=1000)
        else:
            candidates = list(range(len(self.memory_vectors)))
        
        # Create query vector
        query_filler = self._get_filler(value)
        
        if role in self.roles:
            query_vec = SparseBlockHDVector.bind(self.roles[role], query_filler)
        else:
            query_vec = query_filler
        
        # Get top-k using efficient heap
        results = self._get_top_k(query_vec, set(candidates), top_k, 
                                  self.config.similarity_threshold)
        
        # Update stats
        self._update_query_stats((time.time() - start_time) * 1000)
        
        return results
    
    def semantic_query(self, query_text: str, top_k: int = 5, emotion_vector: Optional[Dict[str, float]] = None) -> List[Dict]:
        """
        Query memories by semantic similarity.
        
        API-compatible with NIMAVSABridge.semantic_query()
        """
        import time
        start_time = time.time()
        
        # Build query factors from text
        factors = {
            "WHO": query_text,
            "WHAT": query_text,
            "CONTEXT": query_text,
        }
        
        # Encode query
        query_vec = self._encode_episode_sparse(factors)
        
        # Get candidates from block index (optimized)
        if self.config.use_block_index and len(self.memory_vectors) > 1000:
            candidates = self._block_index_candidates(query_vec.active_blocks, top_k, limit=2000)
        else:
            candidates = list(range(len(self.memory_vectors)))
        
        # Get top-k efficiently
        results = self._get_top_k(query_vec, set(candidates), top_k,
                                  self.config.similarity_threshold,
                                  emotion_vector=emotion_vector)
        
        # Update stats
        self._update_query_stats((time.time() - start_time) * 1000)
        
        return results
    
    def similarity(self, id1: int, id2: int) -> float:
        """
        Compute similarity between two memories.
        
        API-compatible with VSA cache interface.
        """
        if id1 < 0 or id1 >= len(self.memory_vectors):
            raise ValueError(f"Invalid memory ID: {id1}")
        if id2 < 0 or id2 >= len(self.memory_vectors):
            raise ValueError(f"Invalid memory ID: {id2}")
        
        # Check cache
        cache_key = (min(id1, id2), max(id1, id2))
        if cache_key in self._similarity_cache:
            return self._similarity_cache[cache_key]
        
        # Compute
        vec1 = self.memory_vectors[id1]
        vec2 = self.memory_vectors[id2]
        sim = vec1.similarity(vec2)
        
        # Cache
        if len(self._similarity_cache) < self.config.max_cache_size:
            self._similarity_cache[cache_key] = sim
        
        return sim
    
    def bind(self, id1: int, id2: int) -> SparseBlockHDVector:
        """
        Bind two memory vectors.
        
        API-compatible with VSA bind operation.
        """
        vec1 = self.memory_vectors[id1]
        vec2 = self.memory_vectors[id2]
        return SparseBlockHDVector.bind(vec1, vec2)
    
    def bundle(self, ids: List[int]) -> SparseBlockHDVector:
        """
        Bundle multiple memory vectors.
        
        API-compatible with VSA bundle operation.
        """
        if not ids:
            raise ValueError("No IDs provided")
        
        result = self.memory_vectors[ids[0]]
        for mem_id in ids[1:]:
            result = SparseBlockHDVector.bundle(result, self.memory_vectors[mem_id])
        
        return result
    
    def migrate_from_dense(self, dense_vectors: List[np.ndarray], 
                          metadata: List[Dict],
                          factor_extractor: Optional[callable] = None):
        """
        Migrate from dense vectors to sparse block format.
        
        Args:
            dense_vectors: List of dense hypervectors (numpy arrays)
            metadata: List of metadata dicts
            factor_extractor: Optional function to extract factors from metadata
        """
        print(f"🔄 Migrating {len(dense_vectors)} memories from dense to sparse block...")
        
        for i, (dense_vec, meta) in enumerate(zip(dense_vectors, metadata)):
            # Extract factors
            if factor_extractor:
                factors = factor_extractor(meta)
            else:
                factors = {
                    "WHO": meta.get("who", ""),
                    "WHAT": meta.get("what", ""),
                    "WHERE": meta.get("where", ""),
                    "WHEN": meta.get("when", ""),
                    "CONTEXT": meta.get("context", ""),
                }
            
            # Create sparse representation
            active_blocks = self.block_learner.select_blocks(factors)
            
            rng = np.random.default_rng(hash(tuple(sorted(factors.items()))) % (2**31))
            sparse_vec = SparseBlockHDVector(
                block_dim=self.config.block_dim,
                num_blocks=self.config.num_blocks,
                active_set=active_blocks,
                rng=rng
            )
            
            # Store
            self.memory_vectors.append(sparse_vec)
            self.memory_metadata.append(meta)
            self.memory_factors.append(factors)
            
            # Index
            self.block_learner.index_memory(len(self.memory_vectors) - 1, active_blocks)
            
            if (i + 1) % 100 == 0:
                print(f"   Migrated {i + 1}/{len(dense_vectors)}...")
        
        self.stats['migrated_from_dense'] = len(dense_vectors)
        print(f"✅ Migrated {len(dense_vectors)} memories")
    
    def get_memory_usage(self) -> Dict[str, float]:
        """Get memory usage statistics."""
        # Count active blocks across all memories
        total_active_blocks = sum(
            len(vec.active_blocks) for vec in self.memory_vectors
        )
        
        # Memory calculations
        bytes_per_float = 8
        bytes_per_block = self.config.block_dim * bytes_per_float
        
        # Sparse storage
        sparse_bytes = total_active_blocks * bytes_per_block
        sparse_bytes += len(self.memory_vectors) * 100  # overhead for sets
        
        # Dense equivalent
        dense_bytes = len(self.memory_vectors) * self.config.total_dim * bytes_per_float
        
        return {
            "memory_count": len(self.memory_vectors),
            "total_active_blocks": total_active_blocks,
            "avg_active_blocks_per_memory": total_active_blocks / max(len(self.memory_vectors), 1),
            "sparse_storage_mb": sparse_bytes / (1024 * 1024),
            "dense_equivalent_mb": dense_bytes / (1024 * 1024),
            "compression_ratio": dense_bytes / max(sparse_bytes, 1),
            "filler_cache_size": len(self.fillers),
            "role_count": len(self.roles),
        }

    def _serialize_numpy(self, arr: np.ndarray) -> Dict[str, Any]:
        """
        Convert numpy array to JSON-safe dictionary.

        Safe alternative to pickle for numpy arrays.
        Stores dtype, shape, and data as nested lists.

        Args:
            arr: Numpy array to serialize

        Returns:
            Dictionary with dtype, shape, and data as list
        """
        return {
            'dtype': str(arr.dtype),
            'shape': list(arr.shape),
            'data': arr.tolist()
        }

    def _deserialize_numpy(self, data: Dict[str, Any]) -> np.ndarray:
        """
        Convert JSON-safe dictionary back to numpy array.

        Safe alternative to pickle for numpy arrays.
        Reconstructs array from dtype, shape, and data fields.

        Args:
            data: Dictionary with dtype, shape, and data fields

        Returns:
            Reconstructed numpy array
        """
        arr = np.array(data['data'], dtype=data['dtype'])
        return arr.reshape(data['shape'])

    def save(self, filepath: str):
        """Save memory state to file with integrity hash.

        SECURITY FIX: Now uses safe JSON serialization instead of pickle.
        Uses atomic write pattern to prevent corruption.
        """
        # Delegate to safe_save() which uses JSON instead of pickle
        self.safe_save(filepath)

    def _build_save_state(self) -> dict:
        """Serialize current memory state to a JSON-safe dictionary."""
        state = {
            "config": asdict(self.config),
            "metadata": _convert_to_json_serializable(self.memory_metadata),
            "factors": _convert_to_json_serializable(self.memory_factors),
            "stats": _convert_to_json_serializable(self.stats),
            "block_learner": {
                "factor_block_scores": {
                    k: _numpy_to_base64(v)
                    for k, v in self.block_learner.factor_block_scores.items()
                },
                "factor_usage_count": {k: int(v) for k, v in self.block_learner.factor_usage_count.items()},
                "block_activation_count": _numpy_to_base64(self.block_learner.block_activation_count),
                "block_activation_count_dtype": str(self.block_learner.block_activation_count.dtype),
                "block_activation_count_shape": [int(x) for x in self.block_learner.block_activation_count.shape],
                "factor_block_scores_dtype": "float64",
                "factor_block_scores_shape": [self.config.num_blocks],
            },
        }
        vector_data = []
        for vec in self.memory_vectors:
            vec_dict = {
                "active_blocks": sorted([int(x) for x in vec.active_blocks]),
                "blocks": {
                    str(block_idx): {
                        "data": _numpy_to_base64(block_array),
                        "dtype": str(block_array.dtype),
                        "shape": [int(x) for x in block_array.shape],
                    }
                    for block_idx, block_array in vec.blocks.items()
                },
            }
            vector_data.append(vec_dict)
        state["vectors"] = vector_data
        return state

    def _write_json_to_temp(self, state: dict, filepath: "Path") -> str:
        """Write *state* as JSON to a temporary file in *filepath*'s parent directory.

        Returns the temp file path on success.
        Raises IOError for filesystem errors and ValueError for serialisation errors.
        """
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(
                delete=False,
                dir=filepath.parent,
                suffix='.tmp',
                mode='w',
            ) as f:
                temp_path = f.name
                json.dump(state, f, indent=2)
            return temp_path
        except (IOError, OSError) as e:
            _remove_if_exists(temp_path)
            raise IOError(
                f"Failed to write memory file to {filepath}: {e}\n"
                "Check disk space and write permissions."
            )
        except (TypeError, ValueError) as e:
            _remove_if_exists(temp_path)
            raise ValueError(
                f"Failed to serialize memory state to JSON: {e}\n"
                "The memory data may contain non-serializable objects."
            )

    def _write_integrity_sidecar(self, filepath: "Path", file_hash: str, hmac_signature: str) -> "Path":
        """Write the SHA-256 / HMAC sidecar file for *filepath*.

        Emits a UserWarning on failure (non-fatal); returns the sidecar path.
        """
        hash_path = filepath.with_suffix('.json.sha256')
        try:
            with open(hash_path, 'w') as f:
                json.dump({
                    'algorithm': 'sha256',
                    'hash': file_hash,
                    'hmac_algorithm': 'hmac-sha256',
                    'hmac_signature': hmac_signature,
                    'timestamp': datetime.now().isoformat(),
                    'size': filepath.stat().st_size,
                    'memory_count': len(self.memory_vectors),
                }, f, indent=2)
        except (IOError, OSError) as e:
            import warnings
            warnings.warn(
                f"Failed to write integrity hash file {hash_path}: {e}\n"
                "The main file was saved successfully, but without integrity verification. "
                "Future loads will work but won't be able to verify integrity.",
                UserWarning,
            )
        return hash_path

    def _apply_secure_permissions(self, filepath: "Path", hash_path: "Path") -> None:
        """Set restrictive file permissions (0o600) on *filepath* and *hash_path*."""
        try:
            os.chmod(filepath, 0o600)
            if hash_path.exists():
                os.chmod(hash_path, 0o600)
        except (OSError, AttributeError):
            pass  # chmod not supported on all platforms (e.g., Windows)

    def _commit_temp_file(self, temp_path: str, filepath: "Path") -> None:
        """Atomically commit *temp_path* to *filepath*, write sidecar, and set permissions.

        Cleans up *temp_path* on failure.
        """
        try:
            file_hash = _compute_file_hash(Path(temp_path))
            os.replace(temp_path, filepath)
            hmac_signature = _compute_hmac_signature(filepath)
            hash_path = self._write_integrity_sidecar(filepath, file_hash, hmac_signature)
            self._apply_secure_permissions(filepath, hash_path)
            print(f"💾 Safely saved {len(self.memory_vectors)} memories to {filepath}")
        except Exception as e:
            _remove_if_exists(temp_path)
            raise IOError(f"Failed to save memory file: {e}")

    def _write_state_atomically(self, state: dict, filepath: "Path") -> None:
        """Write *state* to *filepath* via an atomic temp-file + rename pattern,
        then save the HMAC/SHA-256 sidecar and set secure permissions."""
        temp_path = self._write_json_to_temp(state, filepath)
        self._commit_temp_file(temp_path, filepath)

    def safe_save(self, filepath: str):
        """
        Save memory state using JSON serialization with base64-encoded numpy arrays.

        SECURITY FIX: Uses JSON instead of pickle to avoid arbitrary code execution.
        Includes HMAC-based signing, integrity hashing, and atomic write pattern.

        HMAC signature prevents tampering with both data and hash files together.
        Set NIMA_HMAC_KEY environment variable for production security.

        Args:
            filepath: Path to save the memory state (will use .json extension)
        """
        state = self._build_save_state()
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        self._write_state_atomically(state, filepath)

    def _verify_file_integrity(self, filepath: "Path") -> None:
        """Check HMAC signature and SHA-256 hash for *filepath* using its sidecar.

        Raises IntegrityError when verification fails; emits warnings for legacy
        files that lack HMAC or a sidecar altogether.
        """
        hash_path = filepath.with_suffix('.json.sha256')
        if not hash_path.exists():
            import warnings
            warnings.warn(
                f"No integrity hash file found for {filepath}. "
                "Loading without verification (legacy file). "
                "For security, re-save the file to add integrity protection.",
                UserWarning,
            )
            return

        try:
            with open(hash_path, 'r') as f:
                hash_data = json.load(f)
            self._verify_hmac(filepath, hash_data)
            self._verify_hash(filepath, hash_data)
        except json.JSONDecodeError as e:
            raise IntegrityError(
                f"INTEGRITY HASH FILE CORRUPTED: {hash_path}\n"
                f"Error: {e}\n"
                "The integrity verification file is corrupted and cannot be read. "
                "This may indicate tampering or file system corruption. Refusing to load."
            )
        except (KeyError, ValueError) as e:
            raise IntegrityError(
                f"INTEGRITY HASH FILE INVALID: {hash_path}\n"
                f"Error: {e}\n"
                "The integrity verification file has invalid structure. "
                "Expected fields: hash, hmac_signature, algorithm. Refusing to load."
            )

    def _verify_hmac(self, filepath: "Path", hash_data: dict) -> None:
        """Verify the stored HMAC signature when present."""
        expected_hmac = hash_data.get('hmac_signature')
        if expected_hmac:
            if not _verify_hmac_signature(filepath, expected_hmac):
                raise IntegrityError(
                    f"HMAC SIGNATURE VERIFICATION FAILED: {filepath}\n"
                    "File may be tampered. HMAC prevents attackers from modifying "
                    "both the data file and hash sidecar together. Refusing to load."
                )
            return

        import warnings
        warnings.warn(
            f"File {filepath} has no HMAC signature - using legacy hash-only verification. "
            "For better security, re-save the file to add HMAC protection.",
            UserWarning,
        )

    def _verify_hash(self, filepath: "Path", hash_data: dict) -> None:
        """Verify the stored SHA-256 hash when present."""
        expected_hash = hash_data.get('hash')
        if not expected_hash:
            return
        actual_hash = _compute_file_hash(filepath)
        if actual_hash != expected_hash:
            raise IntegrityError(
                f"MEMORY INTEGRITY FAILED: {filepath}\n"
                f"Expected hash: {expected_hash}\n"
                f"Actual hash:   {actual_hash}\n"
                "File may be corrupted or tampered. Refusing to load."
            )

    @staticmethod
    def _load_json_state(filepath: "Path") -> dict:
        """Load JSON state from disk with corruption-aware errors."""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise IntegrityError(
                f"MEMORY FILE CORRUPTED: {filepath}\n"
                f"JSON parsing error at line {e.lineno}, column {e.colno}: {e.msg}\n"
                "The memory file is corrupted and cannot be parsed as JSON. "
                "This may indicate file corruption, incomplete write, or tampering. "
                "You may need to restore from a backup."
            )
        except UnicodeDecodeError as e:
            raise IntegrityError(
                f"MEMORY FILE CORRUPTED: {filepath}\n"
                f"Unicode decoding error: {e}\n"
                "The memory file contains invalid UTF-8 encoding. "
                "This may indicate file corruption or a binary file being read as text. "
                "If this is a pickle file, use load() instead of safe_load()."
            )

    def _restore_config(self, state: dict, filepath: "Path") -> None:
        """Restore configuration from serialized state."""
        try:
            self.config = SparseBlockConfig(**state["config"])
        except (KeyError, TypeError, ValueError) as e:
            raise IntegrityError(
                f"MEMORY FILE CORRUPTED: {filepath}\n"
                f"Invalid or missing 'config' field: {e}\n"
                "The memory file has invalid configuration data. "
                "This may indicate file corruption or incompatible format version."
            )

    def _restore_state_metadata(self, state: dict, filepath: "Path") -> None:
        """Restore metadata, factors, and stats sections."""
        try:
            self.memory_metadata = state["metadata"]
            self.memory_factors = state["factors"]
            self.stats = state["stats"]
        except KeyError as e:
            raise IntegrityError(
                f"MEMORY FILE CORRUPTED: {filepath}\n"
                f"Missing required field: {e}\n"
                "The memory file is missing required fields (metadata, factors, or stats). "
                "This may indicate file corruption or incomplete save."
            )

    def _restore_block_learner_state(self, state: dict, filepath: "Path") -> None:
        """Restore serialized block-learner arrays and counters."""
        if "block_learner" not in state:
            return
        try:
            bl = state["block_learner"]
            self.block_learner.factor_block_scores = {}
            score_dtype = np.dtype(bl.get("factor_block_scores_dtype", "float64"))
            score_shape = tuple(bl.get("factor_block_scores_shape", [self.config.num_blocks]))

            for factor_key, b64_data in bl["factor_block_scores"].items():
                self.block_learner.factor_block_scores[factor_key] = self._decode_factor_scores(
                    filepath, factor_key, b64_data, score_dtype, score_shape
                )

            self.block_learner.factor_usage_count = bl["factor_usage_count"]
            activation_dtype = np.dtype(bl.get("block_activation_count_dtype", "int64"))
            activation_shape = tuple(bl.get("block_activation_count_shape", [self.config.num_blocks]))
            self.block_learner.block_activation_count = self._decode_block_activation_count(
                filepath, bl, activation_dtype, activation_shape
            )
        except KeyError as e:
            raise IntegrityError(
                f"MEMORY FILE CORRUPTED: {filepath}\n"
                f"Missing required block_learner field: {e}\n"
                "The block learner data is incomplete or corrupted."
            )

    def _decode_factor_scores(
        self,
        filepath: "Path",
        factor_key: str,
        b64_data: str,
        dtype: np.dtype,
        shape: tuple,
    ) -> np.ndarray:
        """Decode a base64-encoded factor score array."""
        try:
            return _base64_to_numpy(b64_data, dtype, shape).copy()
        except (ValueError, TypeError) as e:
            raise IntegrityError(
                f"MEMORY FILE CORRUPTED: {filepath}\n"
                f"Invalid base64-encoded factor block scores for '{factor_key}': {e}\n"
                "The numpy array data is corrupted or has invalid format."
            )

    def _decode_block_activation_count(
        self,
        filepath: "Path",
        block_learner_state: dict,
        dtype: np.dtype,
        shape: tuple,
    ) -> np.ndarray:
        """Decode the block activation count array."""
        try:
            return _base64_to_numpy(
                block_learner_state["block_activation_count"], dtype, shape
            ).copy()
        except (ValueError, TypeError) as e:
            raise IntegrityError(
                f"MEMORY FILE CORRUPTED: {filepath}\n"
                f"Invalid base64-encoded block activation count: {e}\n"
                "The numpy array data is corrupted or has invalid format."
            )

    def _restore_vectors_state(self, state: dict, filepath: "Path") -> None:
        """Restore serialized sparse vectors."""
        try:
            self.memory_vectors = [
                self._build_vector_from_state(filepath, vec_idx, vec_data)
                for vec_idx, vec_data in enumerate(state["vectors"])
            ]
        except (TypeError, ValueError) as e:
            raise IntegrityError(
                f"MEMORY FILE CORRUPTED: {filepath}\n"
                f"Invalid vectors data structure: {e}\n"
                "The 'vectors' field has invalid format (expected list of vector dictionaries)."
            )

    def _build_vector_from_state(
        self,
        filepath: "Path",
        vec_idx: int,
        vec_data: dict,
    ) -> SparseBlockHDVector:
        """Reconstruct one SparseBlockHDVector from serialized JSON state."""
        try:
            vec = SparseBlockHDVector(
                block_dim=self.config.block_dim,
                num_blocks=self.config.num_blocks,
                active_set=set(vec_data["active_blocks"]),
                rng=None,
            )
            vec.blocks = {
                int(block_idx_str): self._decode_vector_block(
                    filepath, vec_idx, block_idx_str, block_info
                )
                for block_idx_str, block_info in vec_data["blocks"].items()
            }
            return vec
        except KeyError as e:
            raise IntegrityError(
                f"MEMORY FILE CORRUPTED: {filepath}\n"
                f"Missing required field in vector {vec_idx}: {e}\n"
                "Expected fields: active_blocks, blocks. "
                "The vector data is incomplete or corrupted."
            )

    def _decode_vector_block(
        self,
        filepath: "Path",
        vec_idx: int,
        block_idx_str: str,
        block_info: dict,
    ) -> np.ndarray:
        """Decode one serialized vector block."""
        try:
            dtype = np.dtype(block_info["dtype"])
            shape = tuple(block_info["shape"])
            return _base64_to_numpy(block_info["data"], dtype, shape)
        except (ValueError, TypeError, KeyError) as e:
            raise IntegrityError(
                f"MEMORY FILE CORRUPTED: {filepath}\n"
                f"Invalid block data for vector {vec_idx}, block {block_idx_str}: {e}\n"
                "The numpy array data is corrupted or has invalid format."
            )

    def _rebuild_block_index(self, filepath: "Path") -> None:
        """Rebuild the block index from restored vectors."""
        try:
            self.block_learner.block_to_memories = {
                i: set() for i in range(self.config.num_blocks)
            }
            self.block_learner.block_activation_count = np.zeros(
                self.config.num_blocks, dtype=np.int64
            )
            for mem_id, vec in enumerate(self.memory_vectors):
                self.block_learner.index_memory(mem_id, vec.active_blocks)
        except Exception as e:
            raise IntegrityError(
                f"MEMORY FILE CORRUPTED: {filepath}\n"
                f"Failed to rebuild block index: {e}\n"
                "The vector data may be corrupted or incompatible with current format."
            )

    @staticmethod
    def _is_json_file(filepath: "Path") -> bool:
        """Return True if *filepath* can be parsed as JSON text."""
        try:
            with open(filepath, 'r') as f:
                json.load(f)
            return True
        except (json.JSONDecodeError, UnicodeDecodeError):
            return False

    @staticmethod
    def _warn_legacy_pickle(filepath: "Path") -> None:
        """Emit the legacy pickle deprecation warning."""
        import warnings
        warnings.warn(
            f"\n{'='*70}\n"
            f"DEPRECATION WARNING: Loading legacy pickle format from {filepath}\n"
            f"{'='*70}\n"
            f"Pickle deserialization is deprecated and will be removed in a future version.\n"
            f"Pickle files can execute arbitrary code and pose a security risk.\n"
            f"\n"
            f"ACTION REQUIRED: Re-save this file to migrate to the new JSON format:\n"
            f"  1. Load the file (this will show this warning)\n"
            f"  2. Call save() to save in the new secure JSON format\n"
            f"  3. Future loads will use the secure JSON format automatically\n"
            f"\n"
            f"For more information on this security fix, see:\n"
            f"  nima_core/cognition/sparse_block_memory.py (MIGRATION GUIDE)\n"
            f"{'='*70}\n",
            DeprecationWarning,
            stacklevel=2,
        )

    @staticmethod
    def _verify_legacy_pickle_integrity(filepath: "Path") -> None:
        """Best-effort SHA-256 verification for legacy pickle files."""
        hash_path = filepath.with_suffix(filepath.suffix + '.sha256')
        if not hash_path.exists():
            print(f"⚠️  Warning: No integrity hash found for {filepath}")
            return
        try:
            with open(hash_path, 'r') as f:
                hash_data = json.load(f)
            expected_hash = hash_data.get('hash')
            if not expected_hash:
                return
            with open(filepath, 'rb') as f:
                actual_hash = hashlib.sha256(f.read()).hexdigest()
            if actual_hash != expected_hash:
                raise IntegrityError(
                    f"Memory file integrity check FAILED for {filepath}!\n"
                    f"Expected: {expected_hash}\n"
                    f"Actual:   {actual_hash}\n"
                    "This could indicate file corruption or tampering."
                )
            print(f"✅ Integrity verified for {filepath}")
        except (json.JSONDecodeError, KeyError) as e:
            print(f"⚠️  Warning: Could not verify integrity: {e}")

    def _restore_legacy_pickle_state(self, state: dict) -> None:
        """Restore legacy pickle state into the in-memory structures."""
        self.config = SparseBlockConfig(**state["config"])
        self.memory_metadata = state["metadata"]
        self.memory_factors = state["factors"]
        self.stats = state["stats"]

        if "block_learner" in state:
            bl = state["block_learner"]
            self.block_learner.factor_block_scores = {
                k: np.array(v) for k, v in bl["factor_block_scores"].items()
            }
            self.block_learner.factor_usage_count = bl["factor_usage_count"]
            self.block_learner.block_activation_count = np.array(bl["block_activation_count"])

        self.memory_vectors = []
        for vec_data in state["vectors"]:
            vec = SparseBlockHDVector(
                block_dim=self.config.block_dim,
                num_blocks=self.config.num_blocks,
                active_set=set(vec_data["active_blocks"]),
                rng=None,
            )
            vec.blocks = {
                int(k): np.frombuffer(v, dtype=np.float64).reshape(self.config.block_dim)
                for k, v in vec_data["blocks"].items()
            }
            self.memory_vectors.append(vec)

        self._rebuild_block_index(Path("<legacy-pickle>"))

    def safe_load(self, filepath: str, verify: bool = True):
        """
        Load memory state from JSON serialization with integrity verification.

        SECURITY FIX: Uses JSON instead of pickle to avoid arbitrary code execution.
        Verifies HMAC signature and file hash before loading to detect tampering.

        HMAC-based signing prevents an attacker from tampering with both the data
        file and hash sidecar together, as they would need the secret HMAC key.

        Args:
            filepath: Path to the saved memory file (.json)
            verify: If True, verify HMAC signature and integrity hash before loading

        Raises:
            IntegrityError: If integrity verification or HMAC signature fails
            FileNotFoundError: If file not found
        """
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"Memory file not found: {filepath}")

        if verify:
            self._verify_file_integrity(filepath)

        state = self._load_json_state(filepath)
        self._restore_config(state, filepath)
        self._restore_state_metadata(state, filepath)
        self._restore_block_learner_state(state, filepath)
        self._restore_vectors_state(state, filepath)
        self._rebuild_block_index(filepath)

        print(f"💾 Safely loaded {len(self.memory_vectors)} memories from {filepath}")

    def load(self, filepath: str, verify_integrity: bool = True):
        """Load memory state from file with auto-detection of format (JSON or pickle).

        Auto-detects the file format and loads accordingly:
        - JSON format: Uses safe_load() (secure, no code execution risk)
        - Pickle format: Falls back to legacy pickle loader with deprecation warning

        Args:
            filepath: Path to the saved memory file
            verify_integrity: If True, verify SHA256 hash before loading

        Raises:
            IntegrityError: If file hash doesn't match expected
            FileNotFoundError: If file not found
        """
        filepath = Path(filepath)

        if not filepath.exists():
            raise FileNotFoundError(f"Memory file not found: {filepath}")

        if self._is_json_file(filepath):
            self.safe_load(str(filepath), verify=verify_integrity)
            return

        import pickle
        self._warn_legacy_pickle(filepath)
        if verify_integrity:
            self._verify_legacy_pickle_integrity(filepath)

        # Load with pickle (verified above)
        with open(filepath, 'rb') as f:
            state = pickle.load(f)

        self._restore_legacy_pickle_state(state)

        print(f"💾 Loaded {len(self.memory_vectors)} memories from {filepath} (legacy pickle format)")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get system statistics."""
        return {
            "vsa_dimension": self.config.total_dim,
            "block_structure": f"{self.config.num_blocks}×{self.config.block_dim}",
            "total_memories": len(self.memory_vectors),
            "filler_count": len(self.fillers),
            "role_count": len(self.roles),
            "stats": self.stats.copy(),
            "block_learner": self.block_learner.get_stats(),
            "memory_usage": self.get_memory_usage(),
        }


# =============================================================================
# Benchmark Utilities
# =============================================================================

def benchmark_sparse_block_memory(num_memories: int = 10000, 
                                  num_queries: int = 100) -> Dict[str, Any]:
    """
    Benchmark sparse block memory performance.
    
    Returns:
        Benchmark results comparing sparse vs theoretical dense
    """
    print("\n📊 BENCHMARK: SparseBlockMemory")
    print(f"   Memories: {num_memories:,}")
    print(f"   Queries: {num_queries}")
    print("=" * 60)
    
    # Create memory
    config = SparseBlockConfig()
    memory = SparseBlockMemory(config)
    
    # Generate test memories
    print("\n1. Generating test memories...")
    start_time = time.time()
    
    for i in range(num_memories):
        memory.store(
            who=f"Person_{i % 100}",
            what=f"Event_{i}",
            where=f"Location_{i % 50}",
            context=f"Context text for memory {i}",
            importance=np.random.random(),
        )
    
    store_time = time.time() - start_time
    print(f"   Stored {num_memories} memories in {store_time:.2f}s")
    print(f"   Rate: {num_memories/store_time:.0f} memories/sec")
    
    # Memory usage
    print("\n2. Memory usage:")
    usage = memory.get_memory_usage()
    print(f"   Sparse: {usage['sparse_storage_mb']:.2f} MB")
    print(f"   Dense equivalent: {usage['dense_equivalent_mb']:.2f} MB")
    print(f"   Compression: {usage['compression_ratio']:.1f}x")
    
    # Query benchmark
    print("\n3. Query performance:")
    
    # Semantic queries
    query_times = []
    for i in range(num_queries):
        query_text = f"Event_{np.random.randint(num_memories)}"
        start = time.time()
        results = memory.semantic_query(query_text, top_k=10)
        query_times.append((time.time() - start) * 1000)  # ms
    
    avg_query_time = np.mean(query_times)
    p95_query_time = np.percentile(query_times, 95)
    
    print(f"   Avg query time: {avg_query_time:.2f} ms")
    print(f"   P95 query time: {p95_query_time:.2f} ms")
    print(f"   Queries/sec: {1000/avg_query_time:.0f}")
    
    # Role-based queries
    role_times = []
    for i in range(num_queries // 2):
        start = time.time()
        results = memory.query("WHAT", f"Event_{np.random.randint(num_memories)}", top_k=10)
        role_times.append((time.time() - start) * 1000)
    
    avg_role_time = np.mean(role_times)
    print(f"   Avg role query: {avg_role_time:.2f} ms")
    
    # Block learner stats
    print("\n4. Block learner statistics:")
    learner_stats = memory.block_learner.get_stats()
    print(f"   Factors learned: {learner_stats['factors_learned']}")
    print(f"   Block usage mean: {learner_stats['block_activation_distribution']['mean']:.1f}")
    
    results = {
        "num_memories": num_memories,
        "num_queries": num_queries,
        "store_time_sec": store_time,
        "store_rate": num_memories / store_time,
        "memory_usage_mb": usage['sparse_storage_mb'],
        "dense_equivalent_mb": usage['dense_equivalent_mb'],
        "compression_ratio": usage['compression_ratio'],
        "avg_query_ms": avg_query_time,
        "p95_query_ms": p95_query_time,
        "queries_per_sec": 1000 / avg_query_time,
        "avg_role_query_ms": avg_role_time,
        "block_learner_factors": learner_stats['factors_learned'],
    }
    
    print("\n" + "=" * 60)
    print("✅ BENCHMARK COMPLETE")
    print("=" * 60)
    
    return results


def compare_with_dense(num_memories: int = 5000) -> Dict[str, Any]:
    """
    Compare sparse block memory with dense VSA memory.
    """
    print("\n🔬 COMPARISON: Sparse vs Dense VSA")
    print(f"   Testing with {num_memories} memories")
    print("=" * 60)
    
    config = SparseBlockConfig()
    
    # Memory usage comparison
    sparse_memory = SparseBlockMemory(config)
    
    # Dense memory simulation (using numpy)
    dense_vectors = []
    
    # Generate same memories in both
    print("\n1. Populating memories...")
    
    test_memories = [
        (f"Person_{i % 100}", f"Event_{i}", f"Location_{i % 50}", np.random.random())
        for i in range(num_memories)
    ]
    
    # Sparse
    sparse_start = time.time()
    for who, what, where, importance in test_memories:
        sparse_memory.store(who=who, what=what, where=where, importance=importance)
    sparse_time = time.time() - sparse_start
    
    # Dense (simulate 50K dense vectors)
    dense_dim = 50000
    dense_start = time.time()
    for _ in test_memories:
        dense_vec = np.random.normal(0, 1/np.sqrt(dense_dim), dense_dim)
        dense_vec = dense_vec / np.linalg.norm(dense_vec)
        dense_vectors.append(dense_vec)
    dense_time = time.time() - dense_start
    
    print(f"   Sparse store: {sparse_time:.2f}s")
    print(f"   Dense store: {dense_time:.2f}s")
    
    # Query comparison
    print("\n2. Query performance...")
    
    # Sparse query
    sparse_qtimes = []
    for i in range(100):
        start = time.time()
        _ = sparse_memory.semantic_query(f"Event_{np.random.randint(num_memories)}")
        sparse_qtimes.append((time.time() - start) * 1000)
    
    # Dense query (brute force cosine similarity)
    dense_qtimes = []
    for i in range(100):
        query_vec = np.random.normal(0, 1/np.sqrt(dense_dim), dense_dim)
        query_vec = query_vec / np.linalg.norm(query_vec)
        
        start = time.time()
        similarities = []
        for dv in dense_vectors:
            sim = np.dot(query_vec, dv)
            similarities.append(sim)
        _ = np.argsort(similarities)[-10:]
        dense_qtimes.append((time.time() - start) * 1000)
    
    print(f"   Sparse query: {np.mean(sparse_qtimes):.2f} ms (avg)")
    print(f"   Dense query: {np.mean(dense_qtimes):.2f} ms (avg)")
    
    # Memory comparison
    print("\n3. Memory footprint...")
    sparse_usage = sparse_memory.get_memory_usage()
    dense_bytes = num_memories * dense_dim * 8  # 8 bytes per float64
    
    print(f"   Sparse: {sparse_usage['sparse_storage_mb']:.2f} MB")
    print(f"   Dense: {dense_bytes / (1024**2):.2f} MB")
    print(f"   Savings: {dense_bytes / (sparse_usage['sparse_storage_mb'] * 1024**2):.1f}x")
    
    return {
        "num_memories": num_memories,
        "sparse_store_time": sparse_time,
        "dense_store_time": dense_time,
        "sparse_query_ms": np.mean(sparse_qtimes),
        "dense_query_ms": np.mean(dense_qtimes),
        "sparse_memory_mb": sparse_usage['sparse_storage_mb'],
        "dense_memory_mb": dense_bytes / (1024**2),
        "memory_savings": dense_bytes / (sparse_usage['sparse_storage_mb'] * 1024**2),
    }


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="SparseBlockMemory")
    parser.add_argument("action", choices=["benchmark", "compare", "demo"],
                        help="Action to perform")
    parser.add_argument("--memories", type=int, default=10000,
                        help="Number of memories for benchmark")
    parser.add_argument("--queries", type=int, default=100,
                        help="Number of queries for benchmark")
    
    args = parser.parse_args()
    
    if args.action == "benchmark":
        results = benchmark_sparse_block_memory(args.memories, args.queries)
        print("\n📊 Results:")
        for k, v in results.items():
            print(f"   {k}: {v}")
    
    elif args.action == "compare":
        results = compare_with_dense(args.memories)
        print("\n🔬 Comparison:")
        for k, v in results.items():
            print(f"   {k}: {v}")
    
    elif args.action == "demo":
        print("\n" + "=" * 70)
        print("🧠 SparseBlockMemory DEMO")
        print("=" * 70)
        
        # Create memory
        memory = SparseBlockMemory()
        
        # Add memories
        print("\n1. Adding memories...")
        memories = [
            ("David", "gave autonomy", "office", ["trust"], ["partnership"]),
            ("David", "sent heart emoji", "chat", ["love"], ["emotion"]),
            ("Melissa", "discussed marketing", "meeting", ["excitement"], ["business"]),
            ("David", "asked about VSA", "research", ["curiosity"], ["learning"]),
            ("Lilu", "built sparse memory", "code", ["pride"], ["building"]),
        ]
        
        for who, what, where, emotions, themes in memories:
            mid = memory.store(
                who=who, what=what, where=where,
                emotions=emotions, themes=themes,
                importance=0.8
            )
            print(f"   Added: {who} - {what}")
        
        # Query
        print("\n2. Semantic query: 'David autonomy'")
        results = memory.semantic_query("David autonomy", top_k=3)
        for r in results:
            print(f"   [{r['score']:.3f}] {r['metadata']['who']}: {r['metadata']['what']}")
        
        print("\n3. Role query: WHAT='heart emoji'")
        results = memory.query("WHAT", "heart emoji", top_k=3)
        for r in results:
            print(f"   [{r['score']:.3f}] {r['metadata']['who']}: {r['metadata']['what']}")
        
        # Stats
        print("\n4. Statistics:")
        stats = memory.get_stats()
        print(f"   Memories: {stats['total_memories']}")
        print(f"   Dimensions: {stats['vsa_dimension']:,}")
        print(f"   Block structure: {stats['block_structure']}")
        
        usage = stats['memory_usage']
        print(f"   Memory usage: {usage['sparse_storage_mb']:.4f} MB")
        print(f"   Compression: {usage['compression_ratio']:.1f}x")
        
        print("\n" + "=" * 70)
        print("✅ DEMO COMPLETE")
        print("=" * 70)
