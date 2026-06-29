# Public Positioning Mapper

## Purpose

Public Positioning Mapper converts an internal project description into a public-facing position.

It runs before public README, launch post, product page, marketplace listing, and open-source repo copy.

## Required Output

```yaml
public_positioning:
  public_name:
  naming_risk:
  one_line_value:
  target_user:
  user_problem:
  product_category:
  primary_use_cases:
  public_claim_boundary:
  internal_details_to_hide:
  public_details_to_show:
  first_screen_message:
```

## Field Definitions

### public_name

The name intended for public release.

If the name references a person, company, book, platform, or third-party brand, mark naming_risk.

### naming_risk

Options:

```text
none
low
medium
high
```

Risk reasons:

```text
third-party affiliation confusion
trademark risk
copyright association
too generic
too hard to search
too internal
too narrow
```

### one_line_value

A short public-facing value proposition.

Examples:

```text
Turn complex ideas into story-driven communication.
Write audience-specific narratives without losing your central judgment.
Structure one-on-one messages that move relationships forward.
```

### target_user

Who should use this?

Examples:

```text
founders
engineers
operators
writers
BD teams
investors
researchers
public communicators
technical teams
```

### user_problem

The user's real pain.

Examples:

```text
They know what they mean but cannot make others feel it.
They over-explain instead of telling a story.
Their messages are clear but not compelling.
Their communication loses personality when adapted to audiences.
```

### product_category

Examples:

```text
OpenClaw skill
writing skill
communication strategy skill
developer tool
narrative architecture framework
documentation generator
```

### primary_use_cases

List 3-6 practical uses.

### public_claim_boundary

What can be safely claimed?

Examples:

```text
helps structure messages
supports audience adaptation
provides narrative checks
generates reusable drafts
```

What cannot be safely claimed?

Examples:

```text
guarantees persuasion
works for all audiences
replaces human judgment
automates all communication
```

### internal_details_to_hide

Examples:

```text
full file list
all harness names
development history
private references
raw methodology notes
```

### public_details_to_show

Examples:

```text
runtime modes
example prompts
what it helps users produce
status
contributing
license
```

### first_screen_message

What should the reader understand immediately?

Format:

```text
[Project] helps [target user] do [valuable action] without [common failure].
```

## Failure Modes

Fail if:

1. Public copy is written from internal architecture outward.
2. Public name risk is ignored.
3. Use cases are vague.
4. Target user is unclear.
5. The project sounds like an internal research framework.
6. First-screen value is missing.

## Final Rule

Public positioning should make a stranger understand the project before they understand the architecture.
