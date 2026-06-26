---
name: leanstral-formal-verification
description: >
  Formal verification using Lean 4 + Leanstral (labs-leanstral-2603) model.
  Use when: you need mathematical proof of code correctness, protocol verification,
  algorithm correctness, security property proofs, or any property that can be
  expressed as a logical theorem.
  Triggers: "formal proof", "formal verification", "Lean proof", "mathematical proof",
  "theorem proving", "Leanstral", "code verification", "correctness proof"
metadata: {"openclaw": {"requires": {"bins": ["lake"], "env": ["MISTRAL_API_KEY"]}, "primaryEnv": "MISTRAL_API_KEY"}}
---

# Leanstral Formal Verification

A skill for formal verification using Lean 4 + Mathlib + the **Leanstral** model
(`labs-leanstral-2603`) from Mistral AI to mathematically prove code properties.

> **🔑 Requires a Mistral API key.** Set via `MISTRAL_API_KEY` environment variable.
> The Leanstral model is available for **free** via Mistral's API as of 2026-05-17.
> Get a key at: https://console.mistral.ai/api-keys
>
> ```bash
> export MISTRAL_API_KEY="your-key-here"
> ```
>
> **⚠️ When using this skill:**
> - Theorem statements and code are sent to Mistral's API. Do not include
>   confidential code, secrets, or proprietary protocol details in prompts.
> - Generated `.lean` files are untrusted code — `verify.sh` rejects proof
>   holes (`sorry`/`admit`) and compiles in an isolated project directory.
> - Always review the generated theorem statements. Lean verifies that the
>   proof is valid, not that the theorem matches your intent.

## About the Model

Leanstral is Mistral AI's first open-source code agent for Lean 4 (released March 2026).
It is specialized for theorem proving — it generates proofs, and Lean 4 verifies them
mechanically. When a proof passes, correctness is a mathematical fact, not a probability.

| Spec | Value |
|---|---|
| Architecture | Mixture of Experts (128 experts, 4 active per token) |
| Total parameters | 119B |
| Active parameters | 6.5B per token |
| Context length | 256K tokens |
| License | Apache 2.0 (open weights) |
| API model ID | `labs-leanstral-2603` |
| API base URL | `https://api.mistral.ai/v1` |

### Why Leanstral beats general-purpose LLMs at proofs

General-purpose LLMs (GPT, Claude, etc.) write code and hope it works — they test
a few inputs but miss edge cases. Leanstral writes code and **proves it correct for
all inputs**. When Lean 4 accepts the proof, correctness is guaranteed mathematically.

### FLTEval Benchmarks

| Model | Cost ($) | Score |
|---|---|---|
| Claude Haiku | 184 | 23.0 |
| Claude Sonnet | 549 | 23.7 |
| Claude Opus 4.6 | 1,650 | 39.6 |
| **Leanstral pass@1** | **18** | **21.9** |
| **Leanstral pass@2** | **36** | **26.3** |
| **Leanstral pass@4** | **72** | **29.3** |
| **Leanstral pass@16** | **290** | **31.9** |

**Pass@16 beats Sonnet at 1/2 the cost, approaches Opus at 1/6 the cost.**

## Quick Start — Direct API Call

The primary way to use this skill: call the Mistral API directly.

```bash
curl -X POST "https://api.mistral.ai/v1/chat/completions" \
  -H "Authorization: Bearer $MISTRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "labs-leanstral-2603",
    "temperature": 1.0,
    "max_tokens": 32000,
    "messages": [{
      "role": "user",
      "content": "Prove the following theorem in Lean 4:\n\ntheorem add_comm (a b : Nat) : a + b = b + a := by\n  sorry"
    }]
  }'
```

Or with Python:

```python
from openai import OpenAI

client = OpenAI(
    api_key="***",
    base_url="https://api.mistral.ai/v1"
)

response = client.chat.completions.create(
    model="labs-leanstral-2603",
    temperature=1.0,
    max_tokens=32000,
    messages=[{"role": "user", "content": "Prove that..."}],
)
print(response.choices[0].message.content)
```

## Recommended API Parameters

| Parameter | Recommended | Why |
|---|---|---|
| `temperature` | **1.0** | Diverse proof strategies. Lower values produce repetitive attempts. |
| `max_tokens` | **32000** | Proofs are verbose. Generous output budget avoids truncation. |
| `reasoning_effort` | **"high"** (Mistral-specific) | Required for non-trivial proofs. Drop to `"medium"` only for simple boolean logic. |

### Pass@N Strategy

Leanstral improves significantly with multiple attempts. If a proof fails on the
first try, call the API again — the model explores different proof strategies each
time. **pass@2 adds +4.4 points to the score.** For automated workflows, loop
with retry logic:

```bash
for i in 1 2 3; do
  curl -s -X POST "https://api.mistral.ai/v1/chat/completions" \
    -H "Authorization: Bearer $MISTRAL_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"model\":\"labs-leanstral-2603\",\"temperature\":1.0,\"max_tokens\":32000,\"messages\":[{\"role\":\"user\",\"content\":\"$(cat proof_request.txt | jq -Rs .)\"}]}" \
    | jq -r '.choices[0].message.content' > proof_attempt_$i.lean
  # Verify with Lean 4
  bash verify.sh proof_attempt_$i.lean && break
done
```

## Prerequisites

Before using this skill, set up a Lean 4 project on your machine:

1. Install [elan](https://github.com/leanprover/elan) (Lean version manager)
2. Create a Lean project: `lake new formal-verification`
3. Add Mathlib as a dependency in `lakefile.lean`
4. Run `lake build` once to build the Mathlib cache (~500MB, one-time cost)
5. Create a `verify.sh` script in the project root (see below)

### verify.sh template

```bash
#!/bin/bash
# verify.sh — compile and check a Lean 4 proof file
# Usage: bash verify.sh /path/to/proof.lean
set -e
export PATH="$HOME/.elan/bin:$PATH"
PROJECT_DIR="<your-lean-project-dir>"
cp "$1" "$PROJECT_DIR/Proof.lean"
cd "$PROJECT_DIR"
lake build
```

## When to use

**Use cases:**
- Proving that a code fix satisfies the intended properties
- Formal verification of security properties
- Proving the correctness of algorithms
- Verifying the safety of protocols
- Proving that multiple conditional branches are exhaustive
- Providing formal assurance that "this change does not break existing behavior"

**Do not use:**
- When simple unit tests are sufficient
- When you want to check runtime behavior (test by actually running it)
- For unprovable subjective properties (UX, design, etc.)
- For I/O-heavy code (file systems, network, databases — Lean 4 is for pure functions)
- For entire large codebases — focus on the critical core, not 100% coverage

## Workflow Patterns

### Pattern 1: Verify an existing code fix
```
1. Write the code + specification in Lean 4
2. Call Leanstral API: "Prove this implementation satisfies the specification"
3. Compile the returned proof with verify.sh
4. Pass → correctness guaranteed. Fail → failure point is the bug location.
```

### Pattern 2: Spec-driven development
```
1. Write the specification in Lean 4 first (what "correct" means)
2. Call Leanstral to generate both implementation AND proof
3. Compile — when the proof passes, development is complete. No tests needed.
```

### Pattern 3: Root-cause a bug
```
1. Observe the bug's symptoms
2. Write the "correct behavior" specification in Lean 4
3. Call Leanstral to prove the current implementation satisfies it
4. The point where the proof fails = the bug's root cause
5. Fix, then re-prove to confirm
```

### Pattern 4: Safe refactoring
```
1. Write the pre- and post-refactoring code
2. Define equivalence as a specification
3. Call Leanstral to prove they are equivalent
4. Proof passes → refactoring is mathematically safe
```

### Pattern 5: State machine / concurrency verification
```
1. Model the state machine as an inductive proposition in Lean 4
2. Formulate properties: "no deadlocks", "no unreachable states", etc.
3. Call Leanstral to prove them
→ Catches concurrency bugs exhaustively, not probabilistically
```

## Verification Flow

### Step 1: Identify the properties to be verified

Clearly state the properties to be proven in natural language. For example, when
verifying a code change that adds a new boolean guard condition:

- "When the user cancels, the side effect does not fire."
- "During system-generated timeouts, the side effect fires as before (unchanged)."
- "The guard flag only becomes true on user-initiated operations."

### Step 2: Build a formal model

Convert the natural language properties into Lean 4 types and theorems:

```lean
-- Model the relevant boolean conditions as variables
variable (timedOut compactDuring timeExecuting userAborted : Bool)

-- Condition BEFORE the change
def triggerOld : Bool := timedOut && !compactDuring && !timeExecuting

-- Condition AFTER the change (adds userAborted guard)
def triggerNew : Bool := timedOut && !compactDuring && !timeExecuting && !userAborted
```

### Step 3: Call Leanstral to generate proofs

Send the model + theorems to the Leanstral API with a prompt like:

```
Prove the following theorems in Lean 4 using Mathlib.
Use only the tactics: simp, tauto, rw, cases, rfl, constructor.

[paste your model + theorems here]
```

### Step 4: Save output and compile

```bash
# Save Leanstral's response to a .lean file
echo "$LEANSTRAL_OUTPUT" > FormalVerification.lean

# Compile and verify
bash <lean-project-dir>/verify.sh FormalVerification.lean
```

- **Success**: `Build completed successfully` → Proof completed
- **Failure**: Read the error message → Send the error back to Leanstral → Retry

### Step 5: Report the results

- List of proven theorems
- Compilation output (success message)
- Which real-world properties each theorem corresponds to

## Prompt Strategy

When instructing Leanstral via the API, always provide:

```
[Context]
- Lean 4 version in use
- Dependencies (Mathlib, specific modules)
- The code/specification to verify

[Instruction]
- What property to prove
- Optional: suggested tactics or approach
- Any constraints (e.g., "only use simp and tauto")
```

### Concrete Example: Algorithm Correctness

```lean
-- Define the specification FIRST
def sorted_correct (arr : Array Nat) : Prop :=
  ∀ i j, i < j → j < arr.size → arr[i]! ≤ arr[j]!

-- Send to Leanstral: "Prove that bubbleSort satisfies sorted_correct"
def bubbleSort (arr : Array Nat) : Array Nat := by
  sorry -- implementation

theorem bubbleSort_correct (arr : Array Nat) :
  sorted_correct (bubbleSort arr) := by
  sorry -- Leanstral generates this proof
```

## Using as an OpenClaw Sub-Agent (Optional)

If you have already configured a Leanstral sub-agent in your OpenClaw gateway
(this is separate setup — see the gateway's agent configuration), you can
delegate proof generation to it:

```
sessions_spawn:
  agentId: <your-leanstral-agent-id>
  task: |
    You are a Lean 4 formal verification expert.

    ## Context
    [Description of the verification target and properties to prove]

    ## Environment
    Lean 4 is available on the HOST. To compile:
    ```bash
    export PATH="$HOME/.elan/bin:$PATH"
    bash <lean-project-dir>/verify.sh /workspace/your-file.lean
    ```

    ## Task
    1. Identify the properties to be verified
    2. Build a formal model in Lean 4
    3. Write and prove theorems
    4. Verify compilation using verify.sh (mandatory)
    5. If it fails, read the error, fix the proof, and recompile
    6. Report the final compilation output

    Save to: /workspace/FormalVerification.lean
```

Recommended sub-agent parameters (if configuring one):

| Setting | Recommended |
|---|---|
| Model | `labs-leanstral-2603` (Mistral) |
| Temperature | 1.0 |
| Max tokens | 32000 |
| Thinking / reasoning | high |
| Timeout | 600–1200 seconds |
| Fallback models | Any capable reasoning models |

## Best Practices

### ✅ DO

1. **Write the specification first.** Define "correct" before implementing.
2. **Prove in small steps.** Break large theorems into lemmas.
3. **Set reasoning_effort="high".** Essential for non-trivial proofs.
4. **Use pass@N.** If the first API call fails, retry — each attempt explores different strategies.
5. **Feed Lean errors back to Leanstral.** The error message tells exactly what failed.
6. **Leverage Mathlib.** Use existing proven lemmas — don't re-prove everything from scratch.
7. **Keep proofs small and focused.** One property per verification task.

### ❌ DON'T

1. **Use for I/O-heavy code.** Lean 4 is for pure functions. File I/O, networking, databases are impractical to formalize.
2. **Formalize an entire large codebase.** Pick the critical 5% — the core logic that must never be wrong.
3. **Confuse "proof passes" with "spec is correct."** Lean verifies that the implementation matches the spec. The spec's correctness is a human judgment.
4. **Use Leanstral for general tasks.** It's specialized for Lean 4 proofs — not for Python web apps, general chat, or code generation in other languages.
5. **Trust proofs blindly.** Lean's verification is trustworthy, but rare hallucinations (non-existent theorems/tactics) are caught by the compiler.

## Important Notes

### Lean on the host

Lean 4 with Mathlib requires ~500MB of cached dependencies. Run it directly on
your machine — containerizing it is impractical. The `verify.sh` script compiles
`.lean` files using the host's Lean installation.

### Timeout management

The Leanstral model can take minutes to generate proofs. Countermeasures:
- Set generous API timeouts (600–1200s)
- Use pass@N: retry with fresh API calls if the first proof fails
- Divide complex proofs into smaller lemmas

## Applications in Other Fields

| Field | Example |
|---|---|
| **Algorithms** | Correctness of sorting/searching, proof of computational complexity |
| **Security** | Safety of authentication protocols, access control properties |
| **Business logic** | Consistency of fee calculations, exhaustiveness of discount rules |
| **Data integrity** | Satisfaction of DB constraints, safety of schema migrations |
| **Protocols** | Deadlock-free state transitions, message ordering guarantees |
| **Mathematics** | Correctness of statistical calculations, equivalence of formula transformations |
| **State machines** | No unreachable states, all transitions defined, invariant preservation |
| **Refactoring** | Pre/post equivalence proofs, behavioral preservation guarantees |

### Application procedure

1. **Define the property in natural language** — "If X, then Y must always hold"
2. **Build a formal model** — Variables, types, functions that model the system
3. **Write theorems** — Express properties using `theorem`
4. **Call Leanstral API** — Send the model + theorems and request proofs
5. **Compile and verify** — `lake build` checks the proofs

### Basic proof tactics

| Tactic | Use |
|---|---|
| `simp` | Expand definitions and simplify |
| `tauto` | Automatic proof of propositional logic |
| `rw [h]` | Rewrite using assumption `h` |
| `cases` | Case analysis |
| `intro h` | Introduce implication |
| `rfl` | Trivial equality |
| `constructor` | Split a conjunction |

## Limitations

| Limitation | Detail |
|---|---|
| **Lean 4 only** | Does not support Coq, Isabelle, Agda, or other proof assistants |
| **I/O-poor** | File systems, networking, databases cannot be formalized practically |
| **Learning curve** | Requires understanding of Lean 4's tactic language |
| **Not for full codebases** | Formalizing an entire project is impractical — focus on critical core |
| **Proof length** | Complex proofs can be very long and may exceed context |
| **Hallucinations** | Rarely generates non-existent theorems/tactics — Lean catches these |

## Error Handling

### Compilation errors

```
error: unknown identifier 'foo'
```
→ The definition does not exist. Define it with `def` or add an `import`.

```
error: type mismatch
```
→ Type mismatch. Check the variable type declaration.

```
error: tactic 'simp' failed
```
→ `simp` cannot prove it. Use more specific tactics (`cases`, `rw`).

### Pass@N retry loop

```bash
# Basic retry loop: try up to 3 times, stop on first success
for i in 1 2 3; do
  echo "Attempt $i..."
  curl -s ... | python3 -c "import sys,json; print(json.load(sys.stdin)['choices'][0]['message']['content'])" > proof.lean
  if bash verify.sh proof.lean 2>/dev/null; then
    echo "✅ Proof verified on attempt $i"
    break
  fi
  echo "❌ Attempt $i failed, retrying..."
done
```

## Reference Links

- **Leanstral blog**: https://mistral.ai/news/leanstral
- **Model (HuggingFace)**: https://huggingface.co/mistralai/Leanstral-2603
- **API docs**: https://docs.mistral.ai/models/leanstral-26-03
- **Lean 4**: https://github.com/leanprover/lean4
- **Mathlib**: https://github.com/leanprover-community/mathlib4
- **Lean AI leaderboard**: https://lean-lang.org/eval/
