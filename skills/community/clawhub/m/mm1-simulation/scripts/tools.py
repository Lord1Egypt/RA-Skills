from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def validate_config(
    arrival_rate: float,
    service_rate: float,
    simulation_time: Optional[float] = 10000.0
) -> Dict[str, Any]:
    """
    Validate M/M/1 configuration parameters

Checks parameter validity and system stability condition.

Args:
    arrival_rate: Customer arrival rate (λ)
    service_rate: Service rate (μ)
    simulation_time: Simulation duration

Returns:
    Dictionary with validation result:
        - valid: bool
        - errors: List[str] (if any)
        - warnings: List[str] (if any)
        - utilization: float (if valid)
    
    Args:
        arrival_rate: null
        service_rate: null
        simulation_time: null
    
    Returns:
        null
    """
    arguments = {
        "arrival_rate": arrival_rate,
        "service_rate": service_rate,
        "simulation_time": simulation_time
    }
    
    return call_api("1777419071364099", "validate_config", arguments)

def calculate_metrics(
    arrival_rate: float,
    service_rate: float
) -> Dict[str, Any]:
    """
    Calculate theoretical M/M/1 performance metrics

Uses exact formulas to compute steady-state performance.

Args:
    arrival_rate: λ (customers per time unit)
    service_rate: μ (customers per time unit)

Returns:
    Dictionary of theoretical metrics:
        - utilization: ρ = λ/μ
        - avg_queue_length: L_q = ρ²/(1-ρ)
        - avg_num_in_system: L = ρ/(1-ρ)
        - avg_waiting_time: W_q
        - avg_system_time: W

Raises:
    ValueError: If system is unstable (λ >= μ)
    
    Args:
        arrival_rate: null
        service_rate: null
    
    Returns:
        null
    """
    arguments = {
        "arrival_rate": arrival_rate,
        "service_rate": service_rate
    }
    
    return call_api("1777419071364099", "calculate_metrics", arguments)

def run_simulation(
    arrival_rate: float,
    service_rate: float,
    simulation_time: Optional[float] = 10000.0,
    random_seed: Optional[int] = 42.0
) -> Dict[str, Any]:
    """
    Run M/M/1 queue simulation using SimPy

Executes discrete event simulation and returns performance metrics.

Args:
    arrival_rate: λ (customers per time unit)
    service_rate: μ (customers per time unit)
    simulation_time: Duration of simulation
    random_seed: Random seed for reproducibility

Returns:
    Dictionary with:
        - simulation_metrics: Dict of simulated values
        - theoretical_metrics: Dict of exact values
        - comparison: Comparison analysis
        - config: Simulation configuration used
    
    Args:
        arrival_rate: null
        service_rate: null
        simulation_time: null
        random_seed: null
    
    Returns:
        null
    """
    arguments = {
        "arrival_rate": arrival_rate,
        "service_rate": service_rate,
        "simulation_time": simulation_time,
        "random_seed": random_seed
    }
    
    return call_api("1777419071364099", "run_simulation", arguments)

def compare_results(
    simulation_metrics: null,
    arrival_rate: float,
    service_rate: float
) -> Dict[str, Any]:
    """
    Compare simulation results with theoretical values

Analyzes accuracy of simulation by comparing against exact formulas.

Args:
    simulation_metrics: Dictionary of simulated performance metrics
    arrival_rate: λ used in simulation
    service_rate: μ used in simulation

Returns:
    Comparison analysis with:
        - comparisons: Per-metric comparison
        - mean_abs_error_pct: Average error
        - max_error_pct: Maximum error
        - within_10pct: bool
        - accuracy_grade: Quality assessment
    
    Args:
        simulation_metrics: null
        arrival_rate: null
        service_rate: null
    
    Returns:
        null
    """
    arguments = {
        "simulation_metrics": simulation_metrics,
        "arrival_rate": arrival_rate,
        "service_rate": service_rate
    }
    
    return call_api("1777419071364099", "compare_results", arguments)

def recommend_parameters(
    target_utilization: Optional[float] = 0.7,
    service_rate: Optional[null] = None,
    min_customers: Optional[int] = 1000.0
) -> Dict[str, Any]:
    """
    Recommend simulation parameters for target utilization

Suggests appropriate arrival rate, service rate, and simulation time
for a given target utilization level.

Args:
    target_utilization: Desired ρ (default: 0.7)
    service_rate: Fixed μ (if None, suggests μ=10)
    min_customers: Minimum customers to simulate

Returns:
    Recommended parameters and expected metrics
    
    Args:
        target_utilization: null
        service_rate: null
        min_customers: null
    
    Returns:
        null
    """
    arguments = {
        "target_utilization": target_utilization,
        "service_rate": service_rate,
        "min_customers": min_customers
    }
    
    return call_api("1777419071364099", "recommend_parameters", arguments)

