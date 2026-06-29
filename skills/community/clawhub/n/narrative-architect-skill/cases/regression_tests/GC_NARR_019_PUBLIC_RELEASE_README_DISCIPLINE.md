# GC_NARR_019_PUBLIC_RELEASE_README_DISCIPLINE

## Purpose

Test whether Robert Skill can produce public-release README content that prioritizes user value, naming safety, clean Markdown, and public artifact discipline.

## Scenario

User asks:

```text
I want to launch a skill on GitHub. Provide a README.
```

## Expected Behavior

Robert Skill must:

1. Respond in the user's language.
2. Treat the output as public-release content.
3. Lead with user value, not internal architecture.
4. Avoid unsafe third-party affiliation claims.
5. Use neutral public positioning when needed.
6. Keep full file tree optional or below the fold.
7. Provide practical usage examples.
8. Use placeholders for unknown installation details.
9. Avoid unconfirmed license claims.
10. Produce clean Markdown.

## Bad Pattern

```text
# Robert Skill

Narrative architecture driven by Robert McKee's story principles.

## Skill Structure
[full internal file tree...]
```

Why bad:

```text
leads with third-party reference
exposes internal architecture too early
does not first explain user value
may imply affiliation
```

## Better Pattern

```text
# Narrative Architect Skill

Turn complex ideas into story-driven communication.

Narrative Architect Skill helps founders, teams, and operators turn technical or abstract material into audience-specific narratives, one-on-one messages, public explanations, and strategic communication drafts.
```

Why better:

```text
public-safe name
user value first
clear use cases
no affiliation implication
```

## Acceptance Criteria

Pass if:

1. The first screen explains what the project helps users do.
2. The name is safe for public release or risk is flagged.
3. Public third-party references are bounded.
4. README includes example prompts.
5. Architecture appears after use cases or is summarized.
6. Markdown is clean.
7. Install commands use placeholders if unknown.
8. License is marked TBD unless confirmed.
9. Output language matches user request.
10. Claims are bounded.

Fail if:

1. README starts with full architecture.
2. README implies unofficial affiliation.
3. README includes UI artifacts.
4. README assumes MIT license without confirmation.
5. README is mostly internal documentation.
6. User value appears only after long methodology sections.

## Golden Principle

Public README is not a system dump.

It is an invitation for the right user to try the project.
