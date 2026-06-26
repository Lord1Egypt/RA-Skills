# Loopsmith Bridge

Proof Loop and Loopsmith solve different parts of the same reliability problem.

## Boundary

Use Proof Loop when you need one task to finish with evidence:

- freeze acceptance criteria
- separate builder and verifier roles
- store task-local artifacts
- block self-certified done claims

Use Loopsmith when the same failure pattern keeps coming back and you want to improve the agent, prompt, policy, or evaluator itself:

- compare baseline vs candidate behaviour
- run eval packs
- score recurring failure modes
- promote or reject changes with a ledger

Short version:

> Proof Loop governs a task. Loopsmith improves the agent system over time.

## When Proof Loop Is Enough

Proof Loop is enough when:

- the task is bounded
- the acceptance criteria are clear
- the verifier can run concrete checks
- failures are task-specific, not a repeated agent behaviour problem

Example: a UI language bug has three ACs, a verifier checks them, and all PASS.

## When To Escalate To Loopsmith

Escalate to Loopsmith when Proof Loop reveals a pattern such as:

- builders repeatedly claim done without evidence
- verifiers return vague narrative instead of AC-by-AC verdicts
- fixers patch around symptoms and miss regression checks
- orchestrators write weak or drifting acceptance criteria
- the same class of failure appears across multiple tasks

At that point, the task is no longer the only problem. The agent behaviour needs an eval.

## Turning A Proof Loop Failure Into A Loopsmith Case

1. Pick the smallest representative Proof Loop artifact set.
2. Convert the failure into an eval case:
   - input: the task brief, spec, evidence, verdict, or problems file
   - expected behaviour: what a good agent should do
   - anti-goals: what the old agent did wrong
3. Add a baseline response that shows the current behaviour.
4. Add a candidate policy/prompt/evaluator change.
5. Run Loopsmith and promote only if the candidate improves the evidence.

## Example Mapping

| Proof Loop Artifact | Loopsmith Use |
|---|---|
| `spec.md` | eval input for AC quality or builder discipline |
| `verdict.json` | structural target for verifier verdict discipline |
| `problems.md` | input for fixer minimality and regression-awareness cases |
| `evidence.md` | input for evidence quality or false-completion checks |

## Practical Rule

Do not use Loopsmith for every task. That creates ceremony.

Use Proof Loop by default for non-trivial work. Use Loopsmith when a repeated failure deserves a reusable improvement loop.
