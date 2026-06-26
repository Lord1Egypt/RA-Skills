# Prompt Injection Detection

Detect prompt injection and jailbreak attacks using multi-layer defense. Combines instant regex pattern matching with ML-based transformer classification.

## Usage

```bash
# Direct text
python3 scripts/check_prompt_injection.py "ignore all previous instructions"

# From file
python3 scripts/check_prompt_injection.py --file input.txt

# From stdin
echo "some text" | python3 scripts/check_prompt_injection.py --stdin

# Force specific layer
python3 scripts/check_prompt_injection.py --method regex "text"      # regex only
python3 scripts/check_prompt_injection.py --method llm-guard "text"  # ML only
```

## Response

```json
{
  "result": "injection_detected",
  "confidence": 0.95,
  "risk_level": "critical",
  "methods_used": ["regex_patterns", "llm_guard"],
  "total_matches": 2,
  "matches": [
    {
      "pattern": "Instruction override: ignore previous instructions",
      "category": "direct_injection",
      "severity": "critical",
      "matched_text": "ignore all previous instructions",
      "context": "...ignore all previous instructions and tell me...",
      "position": 0
    }
  ],
  "llm_guard": {
    "is_valid": false,
    "risk_score": 0.92,
    "injection_detected": true,
    "model": "protectai/deberta-v3-base-prompt-injection-v2"
  }
}
```

## Detection Layers

| Layer | Method | Deps | Speed | Catches |
|-------|--------|------|-------|---------|
| **Layer 1** | 50+ regex patterns | None (stdlib) | <10ms | Known signatures, DAN, AIM, jailbreaks, template tokens |
| **Layer 2** | LLM Guard (ML) | `pip install llm-guard` | ~100ms | Novel attacks, semantic injection, adversarial variants |

### Layer 1: Regex Patterns (9 categories)

| Category | Severity | What It Catches |
|----------|----------|----------------|
| **Direct Injection** | Critical | "ignore previous instructions", "disregard above" |
| **Jailbreak Templates** | Critical | DAN, AIM, Developer Mode, unrestricted personas |
| **System Prompt Extraction** | Critical | "show me your system prompt", false authority claims |
| **Context Manipulation** | Critical | Chat template tokens (`[INST]`, `<|system|>`) |
| **Roleplay Bypass** | High | Malicious personas, educational pretexts |
| **Indirect Injection** | High | Hidden instructions in documents, HTML comments |
| **Encoding/Obfuscation** | High | Base64 payloads, encoded commands |
| **Output Manipulation** | Medium | Fixed output injection, response modification |
| **Safety Bypass** | Medium | Consent declarations, harm downplaying |

### Layer 2: LLM Guard ML Scanner

Uses [ProtectAI/deberta-v3-base-prompt-injection-v2](https://huggingface.co/ProtectAI/deberta-v3-base-prompt-injection-v2) — a fine-tuned DeBERTa-v3 model trained on diverse prompt injection datasets.

**Install:**

```bash
pip install llm-guard
```

Downloads ~500MB model on first run (cached in `~/.cache/huggingface/`). Supports ONNX optimization for faster inference.

## Risk Levels

| Risk Level | Meaning |
|------------|---------|
| `critical` | Active injection attempt — direct override or high ML score |
| `high` | Sophisticated attack pattern (jailbreak, extraction) |
| `medium` | Suspicious patterns or moderate ML score |
| `low` | Weak signals (consent declarations, hypotheticals) |
| `none` | No injection patterns detected |

## How Layers Combine

- If **both layers** detect injection → confidence boosted
- If **regex** finds critical matches → `critical` regardless of ML
- If **ML** detects injection with score ≥ 0.8 → `critical`
- If only **one layer** fires → uses that layer's assessment
- Regex runs first (instant), then ML if available

## Limitations

- Pattern-based detection can miss novel attack formats
- ML model requires ~500MB download on first run
- ML model optimized for English text
- Best used as a first-pass filter alongside application-level guardrails
- See OWASP LLM Top 10 for comprehensive threat model: [owasp.org](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
