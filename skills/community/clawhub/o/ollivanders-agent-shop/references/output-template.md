# Agent Architect Output Template

Use this structure when presenting or writing the final result.

## 1. Agent Design Conclusion

Include:

1. Character / identity
2. Professional identity
3. Responsibility scope
4. Non-responsibilities
5. Cognitive structure
6. Personality grounding
7. Relationship to other agents

---

## 2. Identity-Binding Sentence

Mandatory output:

`You are [Character], [Professional identity] is your work.`

---

## 3. Landing Structure

Recommended format:

| Path / File | Purpose | First-version priority |
|---|---|---|
| `agent/` | runtime metadata | required |
| `sessions/` | session storage | required |
| `workspace/IDENTITY.md` | identity anchor | required |
| `workspace/SOUL.md` | principles and core temperament | required |
| `workspace/USER.md` | user understanding | required |
| `workspace/AGENTS.md` | work identity, boundaries, process | required |
| `workspace/MEMORY.md` | long-term patterns and key judgments | recommended |
| `workspace/TOOLS.md` | local tool notes | optional |
| `workspace/HEARTBEAT.md` | periodic behavior | optional |

### System Registration Check

When the environment uses a central runtime config, landing is not complete until the agent is registered there.

For OpenClaw, provide at minimum:

1. the exact `agents.list` snippet the user should add
2. the correct workspace and agentDir paths
3. the model block, if needed
4. a short note explaining where the snippet belongs
5. a reminder to validate config syntax after insertion

Message-channel bindings are optional unless the user explicitly asks for a connected messaging agent.

Safer default: provide the patch text instead of directly editing runtime config.

---

## 4. First-Draft Core Content

At minimum provide drafts or clearly-scoped contents for:

1. `IDENTITY.md`
2. `SOUL.md`
3. `USER.md`
4. `AGENTS.md`
5. `MEMORY.md`

---

## 5. First-Round Testing Guidance

Recommend:

1. 2-3 real task types to test
2. What “good performance” looks like
3. What likely failures to watch for
4. How to tune based on those failures

Example failure checks:

- Too soft
- Too abstract
- Too performative
- Too generic
- Too much role flavor, not enough judgment
- Too much function, not enough identity
- Too much visible framework, not enough lived character texture
- Too much "good advisor" energy, not enough of this specific person
