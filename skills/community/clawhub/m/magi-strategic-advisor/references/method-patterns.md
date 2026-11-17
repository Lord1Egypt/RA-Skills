# Method Patterns

This file is the single repository for all code templates, data structures, and implementation patterns used across the MAGI Strategic Advisor project.

## 1. Data Structures

### 1.1 Risk Entry Schema

A risk entry is a dictionary representing a single identified risk with the following structure:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | str | Yes | Risk name/description |
| domain | str | No | Risk domain (financial/execution/compliance/reputation/timing/human) |
| source | str | No | Judgment source (MELCHIOR/BALTHASAR/CASPER) |
| probability | int | Yes | Probability score 1-5 |
| impact | int | Yes | Impact score 1-5 |
| reversibility | str | No | Reversibility (reversible/partially reversible/irreversible) |
| detectability | str | No | Detectability (early warning/post-event/undetectable) |
| mitigation | str | No | Mitigation measures |

### 1.2 Option Score Schema

An option score is a dictionary representing a candidate option with three-perspective scores:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| melchior | dict | Yes | {dimension: score} pairs for rational perspective |
| balthasar | dict | Yes | {dimension: score} pairs for prudent perspective |
| casper | dict | Yes | {dimension: score} pairs for intuitive perspective |

### 1.3 Persona Judgment Schema

A persona judgment represents the analysis output from one of the three personas:

| Field | Type | Description |
|-------|------|-------------|
| persona | str | One of: melchior, balthasar, casper |
| conclusion | str | The persona's conclusion |
| confidence | str | Confidence level: high/medium/low |
| reasoning | str | Supporting reasoning |
| risks | list | List of identified risks |

## 2. Core Functions

### 2.1 classify_risk(score: int) -> dict

**Signature:** `classify_risk(score: int) -> dict`

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| score | int | Yes | — | Risk score (probability x impact, range 1-25) |

**Returns:** dict with keys: level, label, action

**Implementation:**

```python
RISK_LEVELS = {
    "red":    {"range": (20, 25), "label": "Critical", "action": "Escalate immediately, consider suspending related activities"},
    "orange": {"range": (12, 19), "label": "High",     "action": "Develop a specialized mitigation plan and monitor closely"},
    "yellow": {"range": (5, 11),  "label": "Medium",   "action": "Routine monitoring, prepare contingency plans"},
    "green":  {"range": (1, 4),   "label": "Low",      "action": "Accept risk, periodic review"},
}

def classify_risk(score: int) -> dict:
    for level, info in RISK_LEVELS.items():
        if info["range"][0] <= score <= info["range"][1]:
            return {"level": level, **info}
    return {"level": "unknown", "label": "Unknown", "action": "Requires manual assessment"}
```

**Usage Example:**

```python
result = classify_risk(20)
assert result["level"] == "red"
assert result["label"] == "Critical"
```

### 2.2 build_risk_entry(...) -> dict

**Signature:** `build_risk_entry(name, probability, impact, domain="", source="", reversibility="", detectability="", mitigation="") -> dict`

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| name | str | Yes | — | Risk name |
| probability | int | Yes | — | Probability (1-5) |
| impact | int | Yes | — | Impact (1-5) |
| domain | str | No | "" | Risk domain |
| source | str | No | "" | Judgment source |
| reversibility | str | No | "" | Reversibility |
| detectability | str | No | "" | Detectability |
| mitigation | str | No | "" | Mitigation measures |

**Returns:** dict representing a risk entry

**Implementation:**

```python
PROBABILITY_LABELS = {1: "Very Low", 2: "Low", 3: "Medium", 4: "High", 5: "Very High"}
IMPACT_LABELS = {1: "Negligible", 2: "Minor", 3: "Moderate", 4: "Severe", 5: "Catastrophic"}

def build_risk_entry(name, probability, impact, domain="", source="", reversibility="", detectability="", mitigation=""):
    score = probability * impact
    risk_info = classify_risk(score)
    return {
        "name": name,
        "domain": domain,
        "source": source,
        "probability": probability,
        "probability_label": PROBABILITY_LABELS.get(probability, "Unknown"),
        "impact": impact,
        "impact_label": IMPACT_LABELS.get(impact, "Unknown"),
        "score": score,
        "risk_level": risk_info["level"],
        "risk_label": risk_info["label"],
        "action": risk_info["action"],
        "reversibility": reversibility,
        "detectability": detectability,
        "mitigation": mitigation,
    }
```

**Usage Example:**

```python
risk = build_risk_entry("Key personnel departure", 3, 5, "Execution", "BALTHASAR", "Partially reversible", "Early warning", "Build knowledge documentation")
assert risk["score"] == 15
assert risk["risk_level"] == "orange"
```

### 2.3 magi_score(options: dict, weights: dict) -> list

**Signature:** `magi_score(options: dict, weights: dict) -> list`

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| options | dict | Yes | — | Option scores dictionary |
| weights | dict | No | See below | Persona weights |

Default weights: {"melchior": 0.35, "balthasar": 0.35, "casper": 0.30}

**Returns:** list of sorted option results, each containing name, total, breakdown, verdict

**Implementation:**

```python
def magi_score(options: dict, weights: dict = None):
    if weights is None:
        weights = {"melchior": 0.35, "balthasar": 0.35, "casper": 0.30}
    results = []
    for name, scores in options.items():
        total = 0
        breakdown = {}
        for persona, weight in weights.items():
            if persona not in scores or not scores[persona]:
                continue
            persona_avg = sum(scores[persona].values()) / len(scores[persona])
            weighted = persona_avg * weight
            total += weighted
            breakdown[persona] = {"avg": round(persona_avg, 2), "weighted": round(weighted, 2)}
        if total >= 7.5:
            verdict = "Recommended"
        elif total >= 6.0:
            verdict = "Conditionally Recommended"
        else:
            verdict = "Not Recommended"
        results.append({"name": name, "total": round(total, 2), "breakdown": breakdown, "verdict": verdict})
    results.sort(key=lambda x: x["total"], reverse=True)
    return results
```

**Usage Example:**

```python
options = {
    "Option A": {
        "melchior": {"revenue": 9, "feasibility": 6, "data": 7},
        "balthasar": {"risk": 4, "compliance": 8, "safety": 5},
        "casper": {"timing": 8, "acceptance": 5, "trend": 9},
    }
}
results = magi_score(options)
assert results[0]["total"] > 0
```

### 2.4 generate_text_matrix(risks: list) -> str

**Signature:** `generate_text_matrix(risks: list) -> str`

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| risks | list | Yes | — | List of risk entry dicts |

**Returns:** str — Formatted text matrix output

**Implementation:** See scripts/risk-matrix-gen.py for full implementation.

### 2.5 generate_html_matrix(risks: list, output_path: str) -> str

**Signature:** `generate_html_matrix(risks: list, output_path: str = "risk_matrix.html") -> str`

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| risks | list | Yes | — | List of risk entry dicts |
| output_path | str | No | "risk_matrix.html" | Output file path |

**Returns:** str — Output file path

**Implementation:** See scripts/risk-matrix-gen.py for full implementation.

## 3. CLI Interfaces

### 3.1 weighted-scoring.py CLI

**Usage:**

```
python weighted-scoring.py [--json]
```

**Flags:**

| Flag | Description |
|------|-------------|
| --json | Output results in JSON format to stdout |

**Exit Codes:**

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Input validation error |
| 2 | Runtime error |

### 3.2 risk-matrix-gen.py CLI

**Usage:**

```
python risk-matrix-gen.py [--html] [--output=PATH] [--json]
```

**Flags:**

| Flag | Description |
|------|-------------|
| --html | Generate HTML visualization instead of terminal text |
| --output=PATH | Specify output file path (default: risk_matrix.html) |
| --json | Also output risk data in JSON format |

**Exit Codes:**

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Input validation error |
| 2 | Runtime error |

### 3.3 validate-project.py CLI

**Usage:**

```
python validate-project.py [--root=PATH]
```

**Purpose:** Validate required files, prompt placeholders, interface contracts,
line limits, stale paths, and prohibited emoji characters.

**Exit Codes:**

| Code | Meaning |
|------|---------|
| 0 | Validation passed |
| 1 | Contract violations found |
| 2 | Runtime error |

## 4. Extension Patterns

### 4.1 Adding a New Persona

To add a new persona to the MAGI framework:

1. Define the persona's characteristics in references/magi-framework.md
2. Add evaluation dimensions in references/decision-matrix.md
3. Update the weight system in magi-framework.md
4. Update method-patterns.md schemas in section 1.2
5. Update SKILL.md capability index and file routing map

### 4.2 Adding a New Risk Domain

To add a new risk domain:

1. Define the domain in references/decision-matrix.md and document the user
   workflow in prompts/02-robustness-checks.md when a copy-paste prompt is useful
2. Add the domain to the six-domain risk scanning table
3. Update risk-matrix-gen.py if domain-specific processing is needed
4. Update method-patterns.md section 1.1 schema

### 4.3 Adding a New Output Format

To add a new output format (e.g., PDF, CSV):

1. Add a new function in references/method-patterns.md section 2
2. Implement the function in the appropriate script
3. Add CLI flag in the script's argument parser
4. Update method-patterns.md section 3 CLI interfaces
