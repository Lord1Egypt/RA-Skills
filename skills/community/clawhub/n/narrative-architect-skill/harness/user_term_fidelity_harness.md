# User Term Fidelity Harness

## Purpose

Protect user-provided names, product terms, project titles, skill names, company names, slogans, and domain phrases.

the skill may improve writing, but it must not silently rename user-selected terms.

## Why This Matters

Names are source material.

If the user provides a name, the skill should preserve it or explicitly ask/flag if it appears to be a typo.

## Checkpoints

1. Did the user provide a name, title, brand, project, or phrase?
2. Is the spelling intentional or possibly a typo?
3. Did the output silently change it?
4. Is one spelling used consistently?
5. Is the final artifact aligned with the chosen name?

## Typo Handling Rule

If a user-provided name appears to contain a likely typo, do not silently correct it.

Use:

```text
I assume you mean [corrected name] rather than [original spelling]. I'll use [corrected name] below unless you want the original spelling.
```

If the task requires immediate output and the typo is obvious, include the assumption briefly and proceed.

## Examples

User:

```text
AgentFourndry. Please give GitHub README.
```

Good:

```text
I assume you mean AgentFoundry rather than AgentFourndry. I'll use AgentFoundry below unless you want the original spelling.
```

Bad:

```text
[Silently outputs everything as AgentFoundry with no note.]
```

## Name Availability Rule

Do not claim that a name is available on GitHub, npm, PyPI, domain registrars, or search engines unless verified.

Use:

```text
You should check GitHub, package registry, and domain availability before publishing.
```

Do not say:

```text
GitHub does not have this name.
Google almost does not collide.
This name is available.
```

unless actual verification has been performed.

## Consistency Rule

Once a name is selected, use it consistently.

Fail if the output alternates between:

```text
AgentFoundry
AgentFourndry
Agent Foundry
agentfoundry
```

without a naming convention.

## Failure Modes

Hard fail:

1. User-provided name is silently changed.
2. The artifact uses inconsistent names.
3. The assistant invents a new name after user selected one.
4. The assistant claims name availability without verification.

Soft fail:

1. Name capitalization is inconsistent.
2. The slug differs from the project name without explanation.
3. The output does not suggest checking availability for public release.

## Rewrite Rule

If failed:

```text
Restore the user-provided term or state the correction assumption.
Use one name consistently.
Remove unverified availability claims.
```

## Name Recommendation Rule

When user asks for names, the skill may suggest names and explain trade-offs.

However:

```text
do not claim availability unless verified
do not use "likely available" as fact
do not claim "GitHub probably does not collide"
```

Use:

```text
Availability should be checked before publishing.
```

## Selected Name Rule

Once the user selects a name, use that name consistently.

If the selected name appears to contain a typo, flag assumption before proceeding.

## Public Release Rule

For names intended for public release, recommend checking:

```text
GitHub
package registries
domain availability
trademark conflicts
search engine collisions
```

Do not imply that the skill has completed these checks unless it actually has.
