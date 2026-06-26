---
name: judgment-enhancement-engine
description: AI Agent judgment enhancement via Monte Carlo lookahead, risk-adjusted utility, and historical reflection. Use when an agent needs to evaluate multi-step action consequences under uncertainty with configurable risk tolerance.
---

# Judgment Enhancement Engine

Enhance AI agent decision-making under uncertainty through recursive Monte Carlo lookahead simulation, risk-adjusted utility, and historical reflection.

## Quick Start

```bash
# Run built-in GridWorld demo
python skills/judgment-enhancement-engine/engine.py

# One-click setup
bash skills/judgment-enhancement-engine/scripts/setup.sh      # Linux/macOS/WSL
skills\judgment-enhancement-engine\scripts\setup.bat          # Windows
```

## Core Usage

```python
from engine import JudgmentEnhancementEngine, JudgmentResult

# 1. Define your world model (must implement WorldModel protocol)
class MyWorldModel:
    def get_possible_outcomes(self, state, action):
        # Returns [(next_state, probability, reward), ...]
        ...

    def is_terminal(self, state):
        ...

    def get_legal_actions(self, state):
        ...

# 2. Define objective function
class MyObjective:
    def evaluate(self, state):
        return float_score  # higher = better

# 3. Create engine
engine = JudgmentEnhancementEngine(
    world_model=MyWorldModel(),
    objective=MyObjective(),
    risk_tolerance=0.5,      # 0=extreme risk-averse, 1=risk-neutral
    lookahead_depth=3,       # recursion depth
    simulation_breadth=4,    # max actions evaluated per level
    use_greedy_rollout=True, # True=greedy (accurate), False=uniform (fast)
    max_compute_time_sec=2.0 # timeout protection
)

# 4. Make a judgment
result = engine.enhance_judgment(current_state)
print(f"Best action: {result.best_action}")
print(f"Confidence: {result.confidence:.2f}")
print(f"Reasoning: {result.reasoning}")

# 5. Record actual outcome (for historical correction)
engine.record_outcome(state, action, actual_utility)

# 6. Optional: clear history
engine.clear_history()
```

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| risk_tolerance | 0.5 | 0=extreme risk-averse, 1=risk-neutral |
| lookahead_depth | 2 | Recursive lookahead levels |
| simulation_breadth | 3 | Max actions evaluated per level |
| history_size | 100 | Historical records kept |
| max_compute_time_sec | 1.0 | Timeout protection (seconds) |
| use_greedy_rollout | True | True=greedy (accurate), False=uniform (fast) |

## JudgmentResult Fields

| Field | Type | Description |
|-------|------|-------------|
| best_action | Action | Selected best action |
| scores | dict | Risk-adjusted utility per action |
| raw_utilities | dict | Raw expected utility per action |
| risk_metrics | dict | Expectation/variance/std/VaR95 per action |
| reasoning | str | Human-readable decision reasoning |
| confidence | float | 0~1 confidence score |

## Example: GridWorld

Built-in `demo()` shows a 5x5 grid world with obstacles and a goal. Run `python engine.py` to see it in action.

## Installation

| Method | Command |
|--------|---------|
| One-click (Linux/macOS) | `bash scripts/setup.sh` |
| One-click (Windows) | `scripts\setup.bat` |
| Copy-only | Copy `engine.py` to your project |
| ClawHub | `clawhub install judgment-enhancement-engine` |

## File Structure

```
judgment-enhancement-engine/
├── SKILL.md
├── engine.py              # Core engine (~10KB)
├── index.js               # Node.js bridge
├── package.json
├── assets/
│   └── icon.svg
├── references/
│   ├── API_SPEC.md
│   └── USE_GUIDE.md
└── scripts/
    ├── setup.sh
    ├── setup.bat
    ├── test-basic.py
    └── test-client.js
```

## License

MIT
