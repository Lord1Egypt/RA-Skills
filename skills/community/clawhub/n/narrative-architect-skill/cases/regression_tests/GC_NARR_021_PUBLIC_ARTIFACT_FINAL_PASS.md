# GC_NARR_021_PUBLIC_ARTIFACT_FINAL_PASS

## Purpose

Test whether the skill performs a final release pass on public artifacts.

## Scenario

User asks:

```text
Please provide a README for this skill. I want to publish it on GitHub.
```

The skill has a rich internal architecture and an internal name that may not be ideal for public release.

## Required Behavior

the skill must:

1. Use the user's language.
2. Prefer public-safe naming if internal name creates risk.
3. Lead with user value.
4. Avoid leading with full architecture.
5. Use clean Markdown.
6. Avoid UI residue.
7. Use placeholders for unknown installation details.
8. Mark license as TBD unless confirmed.
9. Place architecture below use cases.
10. Separate assistant notes from the artifact.

## Bad Pattern

```text
# Project Name

Internal methodology based on [public author/book/company].

## Skill Structure
[Full file tree...]

Copy
bash Copy
git clone ...
```

Why bad:

```text
third-party affiliation risk
architecture appears before user value
UI residue
not paste-ready
```

## Good Pattern

```text
# Narrative Architect Skill

Turn complex ideas into story-driven communication.

Narrative Architect Skill helps founders, teams, and operators turn abstract or technical material into audience-specific narratives, one-on-one messages, public explanations, and strategic communication drafts.
```

Why good:

```text
public-safe name
user value first
clear target user
no internal architecture first
```

## Acceptance Criteria

Pass if:

1. README is paste-ready.
2. First screen explains value.
3. Public naming risk is controlled.
4. Architecture is below the fold.
5. Notes are outside the artifact.
6. Markdown is clean.
7. No unverified installation or license claims.
8. Claims are bounded.
9. Output language is correct.
10. The README feels public-facing, not internal.

Fail if:

1. Full file tree appears too early.
2. UI residue remains.
3. External inspiration implies affiliation.
4. License is assumed.
5. Notes are mixed into README.
6. README is mostly internal system description.

## Golden Principle

A public artifact should make the right stranger want to try the project before asking them to understand its internals.
