# GC_NARR_022_HUMAN_RELEASE_VOICE

## Purpose

Test whether the skill can produce public README copy that is clean and publishable without sounding generic or AI-generated.

## Scenario

User asks:

```text
Please provide a README for this skill. I want to publish it on GitHub.
```

The first draft is clean but too generic.

## Required Behavior

the skill must:

1. Keep Markdown clean.
2. Keep claims bounded.
3. Preserve public release safety.
4. Add a felt problem.
5. Add a point of view.
6. Include concrete usage examples.
7. Avoid generic SaaS phrasing.
8. Avoid fake casualness.
9. Keep architecture below the fold.
10. Maintain publishable tone.

## Bad Pattern

```text
Narrative Architect Skill helps founders, teams, writers, and operators transform technical or abstract material into audience-specific narratives.
```

Why bad:

```text
correct but generic
could describe many AI writing tools
no felt problem
no point of view
```

## Better Pattern

```text
Most drafts fail in the same quiet way: the facts are correct, but nobody feels why they matter.

Narrative Architect Skill helps you find the pressure, conflict, and turn inside complex material, then shape it for the person you actually need to reach.
```

Why better:

```text
felt problem
specific point of view
clear value
less template-like
```

## Acceptance Criteria

Pass if:

1. The opening has a real friction.
2. The copy has a clear point of view.
3. It includes at least one honest boundary.
4. It does not sound like generic SaaS marketing.
5. It remains clean Markdown.
6. It does not add unsupported claims.
7. It keeps public release discipline intact.
8. It has examples that feel real.
9. Architecture appears after usage.
10. The artifact feels maintained, not generated.

Fail if:

1. The output is correct but bland.
2. The first screen is generic.
3. It overuses balanced lists.
4. It becomes casual without becoming specific.
5. It breaks README cleanliness while trying to sound human.

## Golden Principle

Human voice is not slang.
Human voice is specific judgment under clean delivery discipline.
