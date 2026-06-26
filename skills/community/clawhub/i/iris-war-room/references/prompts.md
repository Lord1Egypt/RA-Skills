# War Room — Prompt Templates

## Language Rule

All spawn prompts must include the language instruction matching the user's language:
- Chinese user → add "请用中文回复。" to each agent prompt
- English user → no extra instruction needed (default)
- Other → add "Respond in {language}."

## Token-Optimized Spawn (File-Based Context)

For proposals over 1500 words, write context to a temp file first:

```python
# Step 1: Write proposal to temp file
exec("cat > /tmp/rt_{topic}.md << 'DATA'\n{proposal_content}\nDATA")

# Step 2: Spawn with lightweight prompts
sessions_spawn(
  task="""You are the {ROLE} in an adversarial roundtable evaluation.
{LANGUAGE_INSTRUCTION}

**Topic**: {TOPIC}

Read /tmp/rt_{topic}.md for the full proposal and data, then:
{DELIVERABLES}

{MANDATORY_CLOSING_QUESTION}""",
  label="{role}_{topic}_{YYYYMMDD}",
  mode="run"
)
```

Each agent prompt is ~500 tokens instead of ~3000. Agents read the shared file themselves.

## Inline Spawn (Short Proposals)

For proposals under 1500 words, inline directly:

```python
sessions_spawn(
  task="""You are the {ROLE} in an adversarial roundtable evaluation.
{LANGUAGE_INSTRUCTION}

**Topic**: {TOPIC}

**Proposal/Data**:
{PROPOSAL}

**Your task**:
{DELIVERABLES}

{MANDATORY_CLOSING_QUESTION}""",
  label="{role}_{topic}_{YYYYMMDD}",
  mode="run"
)
```

## Model Override (Optional)

For critical roles that need deeper reasoning:

```python
sessions_spawn(
  task=...,
  label="guardian_{topic}_{date}",
  mode="run",
  model="opus"  # or "sonnet" for mid-tier
)
```

## Ruling Document Template

Save to: `~/roundtable/RT{N}_{TOPIC}_{YYYYMMDD}.md`

```markdown
# War Room #{N} — {TOPIC}

**Audit ID**: RT{N}-{TOPIC_SHORT}-{YYYYMMDD}
**Date**: {YYYY-MM-DD}
**Ruling**: {GO/NO-GO/REWORK} — {conditions}

## I. Participants
| Role | Label | Runtime | Key Contribution |
|------|-------|---------|-----------------|

## II. Per-Agent Findings
{Summaries with key numbers and arguments}

## III. Process Highlights
{Notable quotes, strongest challenges, turning points in the discussion}
- **Strongest challenge**: {which agent raised what}
- **Turning point**: {what shifted the consensus}
- **Key tension**: {where agents most disagreed}

## IV. Consensus (4/5+)
{Numbered list of agreed points}

## V. Disputes and Contradictions
| Dispute | Pro (who/what) | Con (who/what) | Ruling & Rationale |

## VI. Final Plan
{Concrete deliverables with numbers}

## VII. Scenario Projections
| Scenario | Probability | Outcome |

## VIII. Retained Doubts
{Numbered list of honest unknowns — mandatory}

## IX. Ruling
**{GO / NO-GO / REWORK}**
Conditions: {if any}

## X. Suggested Action Items
| Priority | Task | Owner | Deadline |
|----------|------|-------|----------|
| P0 | | | |
| P1 | | | |
| P2 | | | |
```

## Post-Ruling Checklist

1. Save report to `~/roundtable/RT{N}_{TOPIC}_{YYYYMMDD}.md` (create dir if needed)
2. Reply to user with the full report content
3. Store key decisions to long-term memory with audit ID
4. Git commit the report (if in a managed repo)
5. Update daily log file
