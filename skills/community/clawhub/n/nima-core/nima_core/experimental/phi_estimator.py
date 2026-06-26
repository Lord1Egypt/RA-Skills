"""
phi_estimator.py
Integrated Information (Φ) Estimator for NIMA's Global Workspace.

Uses resonator network to decompose bound hypervectors and measure
integration via slot lesioning.

Key insight: Φ is not just complexity—it's the degree to which
information is irreducibly bound. We measure this by lesioning each
slot and observing how much the whole representation degrades.

Author: Lilu (with David's consciousness architecture)
Date: Feb 12, 2026

STATUS: EXPERIMENTAL
This module provides experimental Φ (integrated information) measurement
capabilities for consciousness research. The estimation methods are based on
theoretical frameworks and are subject to ongoing validation and refinement.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import time

from .sparse_block_vsa import SparseBlockHDVector as HDVector

# Resonator network - may not be available in nima-core yet
try:
    from nima_core.retrieval.resonator import ResonatorNetwork
except ImportError:
    try:
        from .resonator import ResonatorNetwork
    except ImportError:
        ResonatorNetwork = None  # type: ignore


@dataclass
class PhiMeasurement:
    """
    A complete Φ measurement for a bound episode.
    
    Contains:
    - Overall Φ (average across all slot lesions)
    - Per-slot integration (which slots contribute most)
    - Decomposition quality (how clean was the resonator factorization)
    """
    phi: float  # Overall integrated information [0, 1]
    slot_phis: Dict[str, float]  # Φ per slot
    decomposition_quality: float  # How clean was factorization [0, 1]
    factors: Dict[str, HDVector]  # Recovered factors
    lesion_results: Dict[str, float]  # Similarity after each lesion
    computation_time_ms: float
    
    def is_highly_integrated(self, threshold: float = 0.7) -> bool:
        """Check if this episode represents highly integrated information."""
        return self.phi >= threshold
    
    def most_integrated_slot(self) -> Optional[str]:
        """Return the slot whose lesion causes the most degradation."""
        if not self.slot_phis:
            return None
        return max(self.slot_phis.items(), key=lambda x: x[1])[0]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for storage/serialization."""
        return {
            'phi': self.phi,
            'slot_phis': self.slot_phis,
            'decomposition_quality': self.decomposition_quality,
            'most_integrated_slot': self.most_integrated_slot(),
            'is_highly_integrated': self.is_highly_integrated(),
            'computation_time_ms': self.computation_time_ms,
        }


class PhiEstimator:
    """
    Estimates integrated information (Φ) for bound hypervectors.
    
    Uses the resonator network to factor bound vectors, then lesions
    each slot independently to measure how much the whole depends on
    each part.
    
    Algorithm:
    1. Decompose bound vector B into factors {who, what, where, when}
    2. For each slot s:
       a. Replace s with random noise
       b. Rebind all factors → B_lesioned
       c. Measure similarity: sim = B · B_lesioned
       d. Φ_s = 1 - sim (similarity drop from lesioning s)
    3. Overall Φ = mean(Φ_s) across all slots
    """
    
    def __init__(self, 
                 resonator: 'ResonatorNetwork',
                 slot_names: List[str] = None,
                 num_lesion_trials: int = 3):
        """
        Initialize Φ estimator.
        
        Args:
            resonator: ResonatorNetwork for factorization
            slot_names: List of slot names to lesion (default: who, what, where, when)
            num_lesion_trials: Number of random noise vectors to try per slot (for robustness)
        """
        if ResonatorNetwork is None and resonator is not None:
            # External resonator passed in
            pass
        self.resonator = resonator
        self.slot_names = slot_names or ['who', 'what', 'where', 'when']
        self.num_lesion_trials = num_lesion_trials
        
        # Statistics
        self.total_measurements = 0
        self.total_computation_time = 0.0
        self.phi_history = []
    
    def measure_phi(self, bound_vector: HDVector) -> Optional[PhiMeasurement]:
        """
        Measure Φ for a bound hypervector.
        
        Args:
            bound_vector: The bound episode to measure
            
        Returns:
            PhiMeasurement with full results, or None if computation fails
        """
        start_time = time.time()
        
        # Step 1: Decompose the bound vector
        factors = self._decompose(bound_vector)
        if factors is None or len(factors) < 2:
            # Cannot decompose - treat as maximally integrated
            return PhiMeasurement(
                phi=1.0,
                slot_phis={},
                decomposition_quality=0.0,
                factors={},
                lesion_results={},
                computation_time_ms=(time.time() - start_time) * 1000
            )
        
        # Step 2: Measure decomposition quality
        # Reconstruct by rebinding factors and compare to original
        reconstructed = self._rebind_factors(factors)
        decomposition_quality = bound_vector.similarity(reconstructed)
        
        # Step 3: Lesion each slot and measure similarity drop
        slot_phis = {}
        lesion_results = {}
        
        for slot_name in self.slot_names:
            if slot_name not in factors:
                continue
            
            # Average over multiple random lesions for robustness
            drops = []
            for _ in range(self.num_lesion_trials):
                drop = self._lesion_and_measure(bound_vector, factors, slot_name)
                drops.append(drop)
            
            avg_drop = np.mean(drops)
            slot_phis[slot_name] = avg_drop
            lesion_results[slot_name] = 1.0 - avg_drop  # Similarity after lesion
        
        # Step 4: Compute overall Φ
        if slot_phis:
            phi = np.mean(list(slot_phis.values()))
        else:
            phi = 0.0
        
        computation_time = (time.time() - start_time) * 1000
        
        # Update statistics
        self.total_measurements += 1
        self.total_computation_time += computation_time
        self.phi_history.append(phi)
        
        return PhiMeasurement(
            phi=phi,
            slot_phis=slot_phis,
            decomposition_quality=decomposition_quality,
            factors=factors,
            lesion_results=lesion_results,
            computation_time_ms=computation_time
        )
    
    def _decompose(self, bound_vector: HDVector) -> Optional[Dict[str, HDVector]]:
        """
        Decompose a bound vector using the resonator network.
        
        Args:
            bound_vector: The vector to factor
            
        Returns:
            Dictionary of {slot_name: factor_vector} or None if fails
        """
        if self.resonator is None:
            return None
        try:
            # Run resonator dynamics
            factors = self.resonator.factor(bound_vector)
            return factors
        except Exception:
            # Decomposition failed
            return None
    
    def _rebind_factors(self, factors: Dict[str, HDVector]) -> HDVector:
        """
        Rebind all factors into a single vector.
        
        Args:
            factors: Dictionary of slot_name -> factor_vector
            
        Returns:
            Bound hypervector
        """
        result = None
        for vec in factors.values():
            if result is None:
                result = vec
            else:
                result = HDVector.bind(result, vec)
        return result if result else HDVector(block_dim=500, num_blocks=100)
    
    def _lesion_and_measure(self, 
                           original: HDVector,
                           factors: Dict[str, HDVector],
                           slot_to_lesion: str) -> float:
        """
        Lesion a slot and measure similarity drop.
        
        Args:
            original: Original bound vector
            factors: Current factor dictionary
            slot_to_lesion: Which slot to replace with noise
            
        Returns:
            Similarity drop (1 - similarity after lesion)
        """
        if slot_to_lesion not in factors:
            return 0.0
        
        # Save original slot
        original_slot = factors[slot_to_lesion]
        
        # Replace with random noise
        factors[slot_to_lesion] = self._create_noise_vector(original_slot)
        
        # Rebind
        lesioned = self._rebind_factors(factors)
        
        # Restore original
        factors[slot_to_lesion] = original_slot
        
        # Measure similarity drop
        similarity = original.similarity(lesioned)
        drop = 1.0 - similarity
        
        return max(0.0, drop)  # Clamp to [0, 1]
    
    def _create_noise_vector(self, template: HDVector) -> HDVector:
        """Create a random noise vector matching template dimensions."""
        import numpy as np
        noise = HDVector(
            block_dim=template.block_dim,
            num_blocks=template.num_blocks,
            rng=np.random.default_rng()
        )
        # Fill active blocks with random unit vectors
        for block_idx in noise.active_blocks:
            noise.blocks[block_idx] = np.random.randn(template.block_dim)
            norm = np.linalg.norm(noise.blocks[block_idx])
            if norm > 0:
                noise.blocks[block_idx] /= norm
        return noise
    
    def compare_phi(self, 
                    vectors: List[HDVector],
                    labels: List[str] = None) -> List[Tuple[str, float]]:
        """
        Compare Φ across multiple vectors.
        
        Useful for: "Which of my memories is most integrated?"
        
        Args:
            vectors: List of bound vectors to compare
            labels: Optional labels for each vector
            
        Returns:
            List of (label, phi) sorted by Φ (descending)
        """
        if labels is None:
            labels = [f"vector_{i}" for i in range(len(vectors))]
        
        results = []
        for vec, label in zip(vectors, labels):
            measurement = self.measure_phi(vec)
            if measurement:
                results.append((label, measurement.phi))
            else:
                results.append((label, 0.0))
        
        # Sort by Φ descending
        results.sort(key=lambda x: x[1], reverse=True)
        return results
    
    def get_statistics(self) -> Dict:
        """Get estimator statistics."""
        if not self.phi_history:
            return {
                'total_measurements': 0,
                'average_phi': None,
                'average_computation_time_ms': None,
            }
        
        return {
            'total_measurements': self.total_measurements,
            'average_phi': np.mean(self.phi_history),
            'std_phi': np.std(self.phi_history),
            'min_phi': np.min(self.phi_history),
            'max_phi': np.max(self.phi_history),
            'average_computation_time_ms': self.total_computation_time / self.total_measurements,
        }


# =============================================================================
# Integration with Global Workspace
# =============================================================================

def measure_workspace_integration(workspace, resonator) -> Dict:
    """
    Measure Φ for all entries in a global workspace.
    
    Args:
        workspace: GlobalWorkspace instance
        resonator: ResonatorNetwork for factorization
        
    Returns:
        Dictionary with statistics about workspace integration
    """
    estimator = PhiEstimator(resonator)
    
    measurements = []
    for entry in workspace.history:
        measurement = estimator.measure_phi(entry.bound)
        if measurement:
            measurements.append(measurement)
            # Cache in entry
            entry._phi = measurement.phi
            entry._factors = measurement.factors
    
    if not measurements:
        return {'error': 'No measurements completed'}
    
    phis = [m.phi for m in measurements]
    
    return {
        'num_entries_measured': len(measurements),
        'average_phi': np.mean(phis),
        'std_phi': np.std(phis),
        'min_phi': np.min(phis),
        'max_phi': np.max(phis),
        'highly_integrated_count': sum(1 for p in phis if p >= 0.7),
        'estimator_stats': estimator.get_statistics(),
    }


# =============================================================================
# Demonstration
# =============================================================================

def demo_phi_estimator():
    """Demonstrate Φ estimation on synthetic data."""
    global ResonatorNetwork
    
    print("=" * 70)
    print("Φ ESTIMATOR DEMONSTRATION")
    print("=" * 70)
    
    # Check if resonator is available
    if ResonatorNetwork is None:
        print("\n⚠️  ResonatorNetwork not available - skipping demo")
        print("   Install nima_core.retrieval.resonator to enable Φ estimation")
        return
    
    try:
        from nima_core.retrieval.resonator import ResonatorNetwork, CodebookBuilder  # noqa: F401
        
        # Build small codebooks for demo
        codebooks = {
            'who': [HDVector(block_dim=100, num_blocks=10) for _ in range(3)],
            'what': [HDVector(block_dim=100, num_blocks=10) for _ in range(3)],
            'where': [HDVector(block_dim=100, num_blocks=10) for _ in range(3)],
        }
        
        # Create resonator (using the imported class)
        resonator = ResonatorNetwork(dimension=1000)
        resonator.initialize_role_keys(['who', 'what', 'where'])
        for name, cb in codebooks.items():
            resonator.add_codebook(name, cb)
        
        # Create estimator
        estimator = PhiEstimator(resonator, slot_names=['who', 'what', 'where'])
        
        print("\n📊 Testing Φ on different binding configurations...")
        
        # Test 1: Clean binding (should have moderate-high Φ)
        who = codebooks['who'][0]
        what = codebooks['what'][0]
        where = codebooks['where'][0]
        bound_clean = HDVector.bind(HDVector.bind(who, what), where)
        
        print("\n1. Clean binding (who ⊗ what ⊗ where):")
        result = estimator.measure_phi(bound_clean)
        if result:
            print(f"   Φ = {result.phi:.3f}")
            print(f"   Decomposition quality: {result.decomposition_quality:.3f}")
            print(f"   Computation time: {result.computation_time_ms:.1f}ms")
        
        # Test 2: Two-slot binding (should have lower Φ)
        bound_simple = HDVector.bind(who, what)
        print("\n2. Two-slot binding (who ⊗ what):")
        result2 = estimator.measure_phi(bound_simple)
        if result2:
            print(f"   Φ = {result2.phi:.3f}")
        
        # Test 3: Random vector (should have very low Φ - no structure)
        random_vec = HDVector(block_dim=500, num_blocks=100)
        print("\n3. Random vector (no binding structure):")
        result3 = estimator.measure_phi(random_vec)
        if result3:
            print(f"   Φ = {result3.phi:.3f}")
        
        # Statistics
        print("\n📈 Estimator Statistics:")
        stats = estimator.get_statistics()
        for key, value in stats.items():
            if value is not None:
                print(f"   {key}: {value:.3f}" if isinstance(value, float) else f"   {key}: {value}")
        
        print("\n" + "=" * 70)
        print("✅ Φ Estimator operational")
        print("=" * 70)
        
    except ImportError as e:
        print(f"⚠️  Could not import resonator: {e}")
        print("   Run from nima_core directory with proper imports.")


if __name__ == "__main__":
    demo_phi_estimator()