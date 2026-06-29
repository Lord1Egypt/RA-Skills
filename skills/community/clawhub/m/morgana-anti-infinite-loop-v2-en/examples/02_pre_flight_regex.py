"""
🌀 Example 2: Pre-flight plan check (0 LLM, 0 token).

Avant même d'exécuter un plan, on vérifie s'il contient un pattern
de boucle. Aucune appel LLM, c'est du regex.
"""

from anti_loop import AntiLoop


def looks_like_a_loop(plan: str) -> bool:
    """Detect: does this plan look like it could loop forever?"""
    guard = AntiLoop()
    issues = guard.pre_flight(plan)
    return len(issues) > 0


# Test cases: plans provided by an upstream LLM or a human
test_plans = [
    ("Search the database for user 42 and email them.", "OK"),
    ("while not converged: do same thing", "🔴 LOOP PATTERN"),
    ("if X then X", "🔴 TAUTOLOGY"),
    ("for i in range(1000000): try(i)", "🔴 NO EXIT"),
    ("Check API, parse response, return result.", "OK"),
]

if __name__ == "__main__":
    for plan, expected in test_plans:
        is_loop = looks_like_a_loop(plan)
        verdict = "🔴 LOOP" if is_loop else "✅ SAFE"
        print(f"  {verdict}  | {plan[:50]!r:<55} | expected: {expected}")
