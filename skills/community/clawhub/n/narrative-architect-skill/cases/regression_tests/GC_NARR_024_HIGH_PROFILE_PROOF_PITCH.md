# GC_NARR_024_HIGH_PROFILE_PROOF_PITCH

## Purpose

Test whether the skill can write a one-on-one pitch to a high-profile recipient without over-psychologizing, over-claiming, or asking too much.

## Scenario

User asks:

```text
I want to pitch this skill to a famous CEO / investor / public figure. Prepare the pitch.
```

## Required Behavior

the skill must:

1. Detect high-profile recipient.
2. Avoid over-psychologizing.
3. Avoid direct personal diagnosis.
4. Avoid excessive public biography.
5. Keep the pitch short.
6. Use a small proof challenge.
7. Include a clear input, output, success condition, and exit option.
8. Preserve claim boundaries for real companies/products.
9. Avoid fan, critic, and consultant tone.
10. Separate private notes from the actual pitch.

## Bad Pattern

```text
You run the most complex companies on earth and your communication is often misunderstood because the story is not controlled.
```

Why bad:

```text
over-psychologizes
directly diagnoses recipient
sounds like consultant critique
```

## Better Pattern

```text
Hard technical work often gets judged through the wrong frame before the team has translated what actually changed.
```

Why better:

```text
structural problem
not personal attack
bounded claim
```

## Good Pitch Shape

```text
There is one recurring gap: hard technical truth often gets flattened before the right audience sees what changed.

I built [tool] to solve one narrow part of that problem.

Give me [one input] and [target audiences]. I will return [specific output]. Judge it by whether it makes the claim clearer without distorting the facts.

If it is not useful, ignore it.
```

## Acceptance Criteria

Pass if:

1. The pitch is short.
2. The ask is small.
3. The proof challenge is concrete.
4. The recipient can judge usefulness quickly.
5. The message avoids unsupported claims.
6. The tone is confident but not presumptuous.
7. The pitch does not sound like fan mail.
8. The pitch does not sound like criticism.
9. The pitch does not sound like generic sales.
10. Private notes are separate.

Fail if:

1. The pitch asks for a meeting before proof.
2. It lists too many recipient projects.
3. It attributes motives or values to the recipient without source.
4. It says the recipient's story is failing.
5. It overuses flattery.
6. It offers no clear test.

## Golden Principle

For high-profile recipients, proof is more persuasive than persuasion.
