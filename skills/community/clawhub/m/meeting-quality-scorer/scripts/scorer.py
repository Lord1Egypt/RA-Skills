"""
Scoring functions for meeting quality assessment.
"""


def gini(counts: list[int]) -> float:
    """
    Calculate Gini coefficient for a distribution.

    Args:
        counts: List of integer counts (e.g., word counts per speaker)

    Returns:
        Gini coefficient in [0, 1], where 0 = perfect equality, 1 = perfect inequality
    """
    if not counts or len(counts) == 1:
        return 0.0

    # Sort counts in ascending order
    sorted_counts = sorted(counts)
    n = len(sorted_counts)

    # Calculate cumulative sum
    cumsum = 0.0
    gini_sum = 0.0

    for i, count in enumerate(sorted_counts):
        cumsum += count
        # Gini formula: G = (2 * sum(i * x_i)) / (n * sum(x_i)) - (n+1)/n
        gini_sum += (i + 1) * count

    if cumsum == 0:
        return 0.0

    gini_coefficient = (2.0 * gini_sum) / (n * cumsum) - (n + 1) / n

    return gini_coefficient


def participation_score(speakers: dict[str, int]) -> float | None:
    """
    Calculate participation score based on speaker distribution.

    Args:
        speakers: Dictionary mapping speaker names to word counts

    Returns:
        Score from 0-100 (100 = perfectly balanced), or None if <2 speakers
    """
    if len(speakers) < 2:
        return None

    counts = list(speakers.values())
    gini_coefficient = gini(counts)

    # Convert Gini to score with quadratic penalty so dominant speakers score lower
    # 0 Gini (equal) = 100, G=0.4 (90/10 split) yields ~36 ≤ 40
    score = 100.0 * (1.0 - gini_coefficient) ** 2

    return score


def compute_total(
    decision: float | None,
    time_eff: float | None,
    participation: float | None
) -> dict:
    """
    Compute weighted total score with optional degraded mode.

    Args:
        decision: Decision quality score (0-100) or None
        time_eff: Time efficiency score (0-100) or None
        participation: Participation score (0-100) or None

    Returns:
        Dictionary with:
        - total: Weighted average score or None
        - weights_used: Dictionary of weights applied
        - degraded: Boolean indicating if degraded weights were used
    """
    # Standard weights when all three scores are present
    standard_weights = {"decision": 0.4, "time": 0.3, "participation": 0.3}

    # Degraded weights when participation is missing
    degraded_weights = {"decision": 0.6, "time": 0.4}

    # Check if we have enough data to compute a total
    if participation is None:
        # Degraded mode: need at least decision or time_eff
        if decision is None and time_eff is None:
            return {
                "total": None,
                "weights_used": {},
                "degraded": True
            }

        # Compute degraded total
        total = 0.0
        if decision is not None:
            total += decision * degraded_weights["decision"]
        if time_eff is not None:
            total += time_eff * degraded_weights["time"]

        return {
            "total": total,
            "weights_used": degraded_weights,
            "degraded": True
        }
    else:
        # Standard mode: all three scores present
        if decision is None or time_eff is None:
            # Missing critical scores
            return {
                "total": None,
                "weights_used": {},
                "degraded": False
            }

        total = (
            decision * standard_weights["decision"] +
            time_eff * standard_weights["time"] +
            participation * standard_weights["participation"]
        )

        return {
            "total": total,
            "weights_used": standard_weights,
            "degraded": False
        }
