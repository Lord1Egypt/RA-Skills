# Human Release Voice Harness

## Purpose

This harness checks whether a public artifact sounds like a real project maintainer wrote it, rather than a generic AI system.

It runs after:

```text
public_artifact_final_pass_harness
markdown_cleanliness_harness
language_match_harness
```

It should not break format correctness. It only improves surface voice.

## Checkpoints

### 1. Felt Problem

Does the first screen contain a real human or operational problem?

Bad:

```text
Narrative Architect Skill helps teams create audience-specific narratives.
```

Better:

```text
Most people do not lose their audience because the idea is weak. They lose them because the story has no pressure.
```

### 2. Point of View

Does the artifact have a stance?

Examples:

```text
Story is not decoration.
Audience adaptation is not surrender.
A good message should not try to please everyone.
```

Fail if the artifact sounds neutral from start to finish.

### 3. Concrete Use

Does the artifact show what a user can actually ask it to do?

Good:

```text
"Not cold outreach. This is through a friend."
```

This is stronger than:

```text
Supports relationship-aware communication workflows.
```

### 4. Honest Boundary

Does the artifact say what the tool does not do?

Examples:

```text
It does not make everyone like your idea.
It does not replace your judgment.
It does not invent facts to make the story smoother.
```

### 5. Reduced Template Language

Flag overuse of:

```text
helps X transform Y into Z
unlock
empower
seamless
robust
comprehensive
end-to-end
audience-specific
strategic
powerful
```

Not all must be removed. But if the copy can be used by any SaaS product, it fails.

### 6. Rhythm Variation

Does the writing vary sentence length and paragraph weight?

Fail if every paragraph has the same shape:

```text
[Project] helps [audience] do [benefit] using [mechanism].
```

### 7. Architecture Discipline

Does architecture support the story, or does it dominate?

For public README, architecture should be below usage examples.

### 8. No Fake Casualness

Do not solve AI smell by adding slang.

Bad:

```text
Hey folks, this is super cool.
```

Better:

```text
It exists for the moment when the draft is technically correct but nobody feels why it matters.
```

## Failure Modes

Hard fail:

1. No felt problem.
2. No point of view.
3. No concrete example.
4. Generic SaaS voice.
5. The copy sounds like a template.

Soft fail:

1. Too many abstract nouns.
2. Too many balanced lists.
3. Good structure but weak voice.
4. Human problem appears too late.
5. Boundary is missing.

## Rewrite Rule

If failed, rewrite the opening and key sections using:

```text
real friction
→ sharp judgment
→ practical examples
→ honest boundary
→ usage
```

Do not rewrite the entire artifact if only the opening is generic.

## Final Rule

A public artifact should feel maintained, not generated.
