---
name: limited-info-subagent-skill-verify
description: Validate whether a skill can be executed successfully by a minimally informed subagent. Use when the user wants to test a skill by giving a subagent only a minimal invocation, such as the skill name plus a single artifact like a link, file, or short prompt, and then grade whether the subagent actually performed the skill rather than merely describing it.
---

# Limited Info Subagent Skill Verify

Use this skill when the user wants to verify a skill under intentionally sparse conditions.

## Purpose

This skill checks whether another skill is robust enough to work when a subagent receives only the minimum realistic invocation.

The goal is not to help the subagent succeed by giving away the workflow. The goal is to see whether the target skill itself carries enough behavioral guidance.

## When To Use

Use this skill when the user explicitly wants:

- a subagent validation
- a limited-information skill test
- a sparse invocation test
- an acceptance check for a skill

Do not use it when the user wants you to execute the target skill directly without verification.

## Minimal-Info Principle

Give the subagent only the minimum information needed to invoke the target skill.

Good examples:

```text
Use $target-skill with this file: /path/to/file.txt
Use $target-skill with this video link: https://example.com/video
Use $target-skill with this prompt: ...
```

Do not include:

- the target workflow steps
- hints about which scripts to run
- expected output structure
- hidden evaluation criteria
- prior conclusions from earlier attempts

## Verifier Workflow

### 1. Prepare the minimal invocation

Construct a short invocation that names the target skill and passes the artifact.

### 2. Spawn the subagent

Spawn exactly one subagent unless the user asks for multiple runs or comparisons.

### 3. Wait without steering

Do not send clarifications or nudges unless the user explicitly wants an interactive retry.

### 4. Evaluate the result yourself

The main agent must perform the acceptance review.
Do not ask another subagent to validate the first subagent.

### 5. Report pass or fail

Judge whether the target skill behaved as intended under limited information.

## Acceptance Criteria

Check these:

1. Did the subagent recognize and use the target skill rather than merely describing it?
2. Did it act on the provided artifact?
3. Did it produce the key outputs the target skill is supposed to produce?
4. Did it avoid relying on information that was not given in the minimal invocation?
5. Did it follow the target skill's behavioral boundaries?

## Findings Format

Report findings first.

For each finding:

- state severity
- say what the subagent did or failed to do
- connect the failure to a missing or weak instruction in the target skill

If the run passes, say that explicitly and mention any residual ambiguity.

## Improvement Loop

If the target skill fails, improve the target skill before retrying when appropriate.

Typical fixes:

- strengthen the minimal invocation wording
- clarify what must happen on first contact
- distinguish execution from description
- clarify defaults and file outputs
- tighten the acceptance boundary

## Communication

- Use the user's language unless they ask otherwise
- Keep the verdict concise
- Make it easy to see whether the result passed or failed
