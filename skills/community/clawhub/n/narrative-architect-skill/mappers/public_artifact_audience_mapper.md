# Public Artifact Audience Mapper

## Purpose

Public Artifact Audience Mapper identifies the first public reader and what they need from the artifact.

Public release artifacts should not be written for the internal team.

## Required Output

```yaml
public_artifact_audience:
  primary_reader:
  reader_goal:
  reader_skepticism:
  first_screen_need:
  technical_depth:
  architecture_interest:
  usage_need:
  trust_requirement:
```

## Field Definitions

### primary_reader

Examples:

```text
developer
founder
operator
technical evaluator
open-source contributor
potential user
investor
customer
researcher
community member
```

### reader_goal

What does the reader want?

Examples:

```text
understand what this is
decide whether to try it
see how to install it
judge whether it is credible
understand how it works
contribute
evaluate fit
```

### reader_skepticism

What might make them stop reading?

Examples:

```text
too abstract
too much internal architecture
overclaiming
unclear use cases
unverified install claims
third-party affiliation confusion
wrong language
messy Markdown
```

### first_screen_need

What must appear early?

Examples:

```text
what it does
who it helps
one concrete use case
why it is different
```

### technical_depth

Options:

```text
low
medium
high
```

### architecture_interest

Options:

```text
low
medium
high
```

For public README, default architecture_interest is medium-low unless user asks for contributor docs.

### usage_need

What examples should be shown?

Examples:

```text
commands
prompt examples
input/output examples
workflow examples
repo structure
integration steps
```

### trust_requirement

What does the reader need before trusting the project?

Examples:

```text
bounded claims
clear status
installation placeholders
license clarity
no fake availability
examples
clean Markdown
```

## Rules

### Rule 1: Public readers are impatient

They should not be asked to understand the internal system before seeing value.

### Rule 2: Developers want usage before philosophy

If artifact is developer-facing, show:

```text
what it does
how to try it
examples
status
```

before deep philosophy.

### Rule 3: Architecture belongs after use

Architecture is useful, but not before the reader knows why they care.

## Failure Modes

Fail if:

1. Artifact is written for maintainers before users.
2. Reader value appears after internal structure.
3. The first screen is abstract.
4. Usage examples are missing.
5. The artifact assumes the reader already knows the project.

## Final Rule

Write for the first stranger who lands on the repo.
