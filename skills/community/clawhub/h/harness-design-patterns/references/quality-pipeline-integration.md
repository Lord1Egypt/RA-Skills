# Integration with Skill Quality Pipeline

How execution-harness patterns integrate with the improvement-* skill family.

## 1. improvement-evaluator + Ralph

**Problem:** Evaluation tasks that require multi-turn interaction may time out or stop prematurely, producing false negatives.

**Integration:** For interactive evaluator runs (not headless `-p` mode), initialize Ralph before starting the evaluation session:

```bash
# 1. Initialize Ralph persistent execution
bash ralph-init.sh eval-skill-xyz 10

# 2. Start Claude Code with the evaluation task (interactive mode)
claude --permission-mode bypassPermissions

# Ralph stop hook (configured in settings.json) will block premature stops
```

For headless mode, use `--max-turns 200` (Claude Code built-in). Ralph is not needed for headless.

## 2. autoloop-controller + Handoff Documents

**Problem:** When autoloop runs 5+ improvement iterations, context gets compressed and the loop loses track of which improvements were tried, accepted, or rejected.

**Integration:** Each autoloop iteration should write a handoff document before the iteration ends:

```
~/.openclaw/shared-context/sessions/<session-id>/handoffs/iteration-<N>.md
```

Content: Decided (what was changed), Rejected (what was tried but reverted), Scores (before/after), Remaining (what to try next).

The next iteration's UserPromptSubmit hook injects the latest handoff as context.

## 3. improvement-gate + Agent-Type Verification Hook

**Problem:** improvement-gate's 6 layers (Schema → Compile → Lint → Regression → Review → HumanReview) are all mechanical/code-level. They can't judge whether a SKILL.md change semantically improves the skill.

**Integration:** Add an agent-type hook to the gate's verification:

```json
{
  "hooks": [{
    "type": "agent",
    "agent": "Read the original and modified SKILL.md. Judge: does the change genuinely improve clarity, actionability, or coverage? Or is it cosmetic/harmful? Return verdict: accept/reject with reason."
  }]
}
```

This adds a semantic layer on top of the mechanical checks.

## 4. improvement-learner + Compaction Memory Extraction

**Problem:** During long self-improvement loops, the learner accumulates evaluation patterns in its HOT memory but loses them during context compression.

**Integration:** PreCompact hook extracts the learner's current scoring patterns and writes them to session state before compaction:

```
~/.openclaw/shared-context/sessions/<session-id>/learner-patterns.json
```

## 5. skill-forge + task_suite.yaml from Execution Patterns

**Problem:** skill-forge generates task suites from SKILL.md, but doesn't know about execution-harness patterns that could become test cases.

**Integration:** When forging a task suite for a skill that uses execution-harness patterns (detected by `triggers:` containing "ralph", "handoff", etc.), inject test tasks that verify:
- Ralph state file is correctly created
- Handoff documents follow the 5-section structure
- Cancel signals expire correctly

## Summary Table

| Quality Skill | Harness Pattern | Integration Type |
|--------------|-----------------|-----------------|
| improvement-evaluator | Ralph + dispatch | Use --ralph for interactive eval runs |
| autoloop-controller | Handoff documents | Write iteration handoffs for context survival |
| improvement-gate | Agent-type hook | Semantic verification layer on top of mechanical checks |
| improvement-learner | Compaction extraction | PreCompact saves scoring patterns to session state |
| skill-forge | Pattern-aware test gen | Auto-generate harness-specific test tasks |
