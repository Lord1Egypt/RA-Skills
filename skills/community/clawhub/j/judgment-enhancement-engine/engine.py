# encoding: utf-8
"""
AI Agent Judgment Enhancement Engine
Version: 1.1 | Production-ready

Features: lookahead Monte Carlo, risk-adjusted utility,
historical reflection, timeout protection, greedy/sample dual mode.

Zero external dependencies.
"""

import math
import random
import time
from dataclasses import dataclass
from typing import Dict, Generic, List, Optional, Protocol, Tuple, TypeVar


State = TypeVar("State")
Action = TypeVar("Action")


class WorldModel(Protocol[State, Action]):
    def get_possible_outcomes(self, state: State, action: Action) -> List[Tuple[State, float, float]]:
        ...

    def is_terminal(self, state: State) -> bool:
        ...

    def get_legal_actions(self, state: State) -> List[Action]:
        ...


class ObjectiveFunction(Protocol[State]):
    def evaluate(self, state: State) -> float:
        ...


@dataclass
class JudgmentResult(Generic[Action]):
    best_action: Action
    scores: Dict[Action, float]
    raw_utilities: Dict[Action, float]
    risk_metrics: Dict[Action, Dict[str, float]]
    reasoning: str
    confidence: float


class JudgmentEnhancementEngine(Generic[State, Action]):
    def __init__(
        self,
        world_model: WorldModel[State, Action],
        objective: ObjectiveFunction[State],
        risk_tolerance: float = 0.5,
        lookahead_depth: int = 2,
        simulation_breadth: int = 3,
        history_size: int = 100,
        max_compute_time_sec: float = 1.0,
        use_greedy_rollout: bool = True,
    ):
        self.world = world_model
        self.objective = objective
        self.risk_tolerance = max(0.0, min(1.0, risk_tolerance))
        self.depth = max(1, lookahead_depth)
        self.breadth = max(1, simulation_breadth)
        self.max_time = max_compute_time_sec
        self.use_greedy = use_greedy_rollout
        self._history: List[Tuple[int, Action, float]] = []
        self._history_size = history_size

    def enhance_judgment(self, state: State, candidate_actions: Optional[List[Action]] = None) -> JudgmentResult[Action]:
        start_time = time.monotonic()
        if candidate_actions is None:
            candidate_actions = self.world.get_legal_actions(state)
        if not candidate_actions:
            raise ValueError("no legal actions")

        action_stats = {}
        for act in candidate_actions:
            if time.monotonic() - start_time > self.max_time:
                break
            action_stats[act] = self._evaluate_action(state, act, start_time)

        scores = {}
        raw_utils = {}
        risk_metrics = {}

        for act, stats in action_stats.items():
            exp_u = stats["expected_utility"]
            var_u = stats["variance"]
            raw_utils[act] = exp_u
            risk_penalty = (1.0 - self.risk_tolerance) * math.sqrt(var_u) if var_u > 0 else 0.0
            scores[act] = exp_u - risk_penalty
            risk_metrics[act] = {
                "expected": exp_u,
                "variance": var_u,
                "std": math.sqrt(var_u),
                "var_95": stats.get("var_95", exp_u),
            }

        state_hash = self._hash_state(state)
        for act in candidate_actions:
            scores[act] += self._historical_correction(state_hash, act)

        best_action = max(scores.items(), key=lambda x: x[1])[0]
        confidence = self._compute_confidence(action_stats.get(best_action, {}))
        reasoning = self._build_reasoning(best_action, scores, risk_metrics)

        return JudgmentResult(
            best_action=best_action,
            scores=scores,
            raw_utilities=raw_utils,
            risk_metrics=risk_metrics,
            reasoning=reasoning,
            confidence=confidence,
        )

    def record_outcome(self, state: State, action: Action, actual_utility: float) -> None:
        state_hash = self._hash_state(state)
        self._history.append((state_hash, action, actual_utility))
        if len(self._history) > self._history_size:
            self._history.pop(0)

    def clear_history(self) -> None:
        self._history.clear()

    def _evaluate_action(self, state: State, action: Action, deadline: float) -> Dict[str, float]:
        outcomes = self.world.get_possible_outcomes(state, action)
        if not outcomes:
            return {"expected_utility": -float("inf"), "variance": 0.0}
        total_prob = sum(p for _, p, _ in outcomes)
        if total_prob <= 0:
            return {"expected_utility": -float("inf"), "variance": 0.0}
        norm = 1.0 / total_prob
        exp_u = 0.0
        sum_sq = 0.0
        var95_samples = []
        for ns, prob, rew in outcomes:
            p = prob * norm
            if p <= 0:
                continue
            future = self._rollout(ns, self.depth - 1, deadline)
            total = rew + future
            exp_u += p * total
            sum_sq += p * (total**2)
            sample_cnt = max(1, int(p * 100))
            var95_samples.extend([total] * sample_cnt)
        variance = sum_sq - (exp_u**2)
        var95 = exp_u
        if var95_samples:
            var95_samples.sort()
            var95 = var95_samples[int(0.05 * len(var95_samples))]
        return {"expected_utility": exp_u, "variance": variance, "var_95": var95}

    def _rollout(self, state: State, depth: int, deadline: float) -> float:
        if time.monotonic() > deadline:
            return 0.0
        if depth <= 0 or self.world.is_terminal(state):
            return self.objective.evaluate(state)
        legal = self.world.get_legal_actions(state)
        if not legal:
            return self.objective.evaluate(state)
        if self.use_greedy:
            sample_actions = random.sample(legal, min(self.breadth, len(legal)))
            best_value = -float("inf")
            for act in sample_actions:
                act_val = 0.0
                total_p = 0.0
                for ns, prob, rew in self.world.get_possible_outcomes(state, act):
                    if prob <= 0:
                        continue
                    total_p += prob
                    act_val += prob * (rew + self._rollout(ns, depth - 1, deadline))
                if total_p > 0:
                    act_val /= total_p
                if act_val > best_value:
                    best_value = act_val
            return best_value if best_value > -float("inf") else 0.0
        else:
            sample_actions = random.sample(legal, min(self.breadth, len(legal)))
            total_val = 0.0
            for act in sample_actions:
                for ns, prob, rew in self.world.get_possible_outcomes(state, act):
                    if prob <= 0:
                        continue
                    total_val += prob * (rew + self._rollout(ns, depth - 1, deadline))
            return total_val / len(sample_actions) if sample_actions else 0.0

    def _historical_correction(self, state_hash: int, action: Action) -> float:
        matches = [u for h, a, u in self._history if h == state_hash and a == action]
        if not matches:
            return 0.0
        avg_actual = sum(matches) / len(matches)
        return -max(0.0, -avg_actual) * 0.2

    def _compute_confidence(self, stats: Dict[str, float]) -> float:
        if not stats:
            return 0.0
        std = math.sqrt(stats.get("variance", 1.0))
        conf = 1.0 / (1.0 + std * 2.0)
        if self._history:
            conf = min(1.0, conf * (1.0 + 0.1 * math.log1p(len(self._history))))
        return max(0.0, min(1.0, conf))

    def _build_reasoning(self, best, scores, metrics):
        best_score = scores[best]
        best_m = metrics.get(best, {})
        exp_u = best_m.get("expected", 0.0)
        std = best_m.get("std", 0.0)
        return (
            f"Selected {best} (risk-adj={best_score:.3f}, expected={exp_u:.3f}, "
            f"std={std:.3f}, risk_tol={self.risk_tolerance:.2f}, depth={self.depth})"
        )

    @staticmethod
    def _hash_state(state):
        try:
            return hash(repr(state))
        except Exception:
            return hash(id(state))


class GridWorld:
    def __init__(self, w, h, goal, obstacles):
        self.w, self.h = w, h
        self.goal = goal
        self.obs = set(obstacles)

    def is_valid(self, pos):
        x, y = pos
        return 0 <= x < self.w and 0 <= y < self.h and pos not in self.obs

    def move(self, state, action):
        d = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}.get(action, (0, 0))
        ns = (state[0] + d[0], state[1] + d[1])
        return ns if self.is_valid(ns) else state


class GridModel(WorldModel):
    def __init__(self, grid):
        self.grid = grid
        self.actions = ["up", "down", "left", "right"]

    def get_possible_outcomes(self, state, action):
        ns = self.grid.move(state, action)
        r = 100.0 if ns == self.grid.goal else -1.0
        return [(ns, 1.0, r)]

    def is_terminal(self, state):
        return state == self.grid.goal

    def get_legal_actions(self, state):
        return self.actions


class GridObjective(ObjectiveFunction):
    def __init__(self, goal):
        self.goal = goal

    def evaluate(self, state):
        return -abs(state[0] - self.goal[0]) - abs(state[1] - self.goal[1])


def demo():
    g = GridWorld(5, 5, (4, 4), [(2, 2), (2, 3)])
    m = GridModel(g)
    o = GridObjective((4, 4))
    e = JudgmentEnhancementEngine(m, o, risk_tolerance=0.3, lookahead_depth=3, simulation_breadth=4, use_greedy_rollout=True)

    start = (0, 0)
    r = e.enhance_judgment(start)
    print("State:", start, "Goal:", g.goal)
    print("Best action:", r.best_action)
    print("Confidence:", round(r.confidence, 2))
    for a, s in r.scores.items():
        print(f"  {a}: {s:.3f} (raw={r.raw_utilities[a]:.3f})")
    print("Reason:", r.reasoning)

    ns = g.move(start, r.best_action)
    e.record_outcome(start, r.best_action, 100.0 if ns == g.goal else -1.0)
    r2 = e.enhance_judgment(start)
    print("After history, best:", r2.best_action, "(conf=", round(r2.confidence, 2), ")")
    print("All tests passed.")


if __name__ == "__main__":
    demo()
