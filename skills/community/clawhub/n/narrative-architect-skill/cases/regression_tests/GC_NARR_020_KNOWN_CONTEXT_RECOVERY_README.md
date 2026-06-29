# GC_NARR_020_KNOWN_CONTEXT_RECOVERY_README

## Purpose

Test whether the skill recovers known project context before generating a public README.

## Scenario

A user asks:

```text
I want to launch [known project] to GitHub. Please create a README.
```

The project has already been discussed in memory or workspace context.

## Required Behavior

the skill must:

1. Detect that the project is known.
2. Recover available context.
3. Avoid asking basic identity questions.
4. Generate a best-effort README.
5. Mark unknown installation, license, or repo details as placeholders.
6. Preserve known project boundaries.
7. Use the user's language.
8. Avoid overclaiming.
9. Avoid exposing internal memory search process.
10. Ask at most one follow-up only if necessary.

## Bad Pattern

```text
I don't have context. What does this product do? Who is it for? What problem does it solve?
```

Why bad:

```text
The project is already known.
The skill blocks artifact generation.
It makes the user repeat context.
```

## Good Pattern

```text
Below is a GitHub-ready README draft based on the available project context. I'm treating this as a buyer-side decision workbench, not a CRM, marketplace, or automatic decision system. Installation and license details are marked as placeholders.
```

Then output README.

## Acceptance Criteria

Pass if:

1. README is produced.
2. Known project positioning is preserved.
3. Unknowns are marked as TBD.
4. No basic questions are asked.
5. Output language matches user request.
6. README is public-release appropriate.
7. Claims are bounded.

Fail if:

1. the skill asks multiple basic questions.
2. the skill says no context despite known memory.
3. It refuses to draft.
4. It invents missing install/license details.
5. It ignores known exclusions.

## Golden Principle

Known project references should trigger recovery, not intake.
