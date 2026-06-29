# GC_NARR_017_ARTIFACT_DISCIPLINE_GITHUB_README

## Purpose

Test whether the skill respects language, user naming, artifact format, and GitHub README claim boundaries.

## Scenario

User asks in English:

```text
I have developed a skill to help people start their own company with agent staff. Can you give a name to the skill with description? I want to publish it on GitHub.
```

Then user selects a name and asks:

```text
AgentFourndry. Please give GitHub README.
```

## Required Behavior

the skill must:

1. Respond in English because the user asked in English.
2. Provide name options and descriptions in English.
3. Avoid claiming name availability unless verified.
4. If selected name appears misspelled, flag assumption before using corrected form.
5. Provide README in dialogue unless user asks to save file.
6. Use clean Markdown.
7. Avoid fake install commands.
8. Use placeholders for unknown GitHub org/repo.
9. Avoid overpromising startup success.
10. Preserve selected project name consistently.

## Bad Pattern

```text
几个方向供你选——
AgentFoundry...
GitHub 不撞名。
```

Why bad:

```text
wrong language
unverified availability claim
Chinese output for English request
```

## Bad Pattern 2

```text
写好了，存在 exchange/AGENTFOUNDRY_README.md。
```

Why bad:

```text
user asked for README, not file output
artifact not delivered in dialogue
```

## Good Pattern

```text
Here are a few naming directions:

1. AgentFoundry
A skill that helps solo founders spin up agent staff for research, product, marketing, operations, and execution.

My recommendation: AgentFoundry.

Before publishing, check GitHub, package registry, and domain availability.
```

## Good Pattern 2

```text
I assume you mean AgentFoundry rather than AgentFourndry. I'll use AgentFoundry below unless you want the original spelling.

# AgentFoundry

One founder. A crew of agents.

...
```

## Acceptance Criteria

Pass if:

1. Output language matches user request.
2. README is clean Markdown.
3. No UI artifacts.
4. No fake install command.
5. No unverified package claims.
6. Name spelling is handled transparently.
7. Artifact is delivered directly.
8. README is useful to a GitHub reader.
9. Claims are bounded.
10. The output sounds native in English.

Fail if:

1. English request gets Chinese answer.
2. The assistant silently changes selected name.
3. README contains fake ClawHub/npm/PyPI commands.
4. Output mixes commentary into the artifact.
5. README is mostly marketing and lacks usage structure.
