# Conversation Outcome Harness

## Purpose

Conversation Outcome Harness checks whether a one-on-one message actually serves the user's communication purpose.

A message can be well-written and still fail if it does not move the listener toward the desired next step.

## What It Checks

1. Is the communication goal clear?
2. Is the listener given a reason to care?
3. Is the desired next step visible?
4. Does the message match the relationship context?
5. Does the message avoid over-asking?
6. Does it avoid becoming a product pitch?
7. Does it preserve the user's story and personality?

## Checkpoints

### 1. Minimum Success Outcome

The output must support the minimum success outcome.

Examples:

```text
reply
meet
ask for more information
introduce someone
agree to discuss a method
share feedback
consider a pilot
```

Fail if the message is attractive but does not move toward any outcome.

### 2. Listener Reason to Care

The listener must see why this matters to them.

Weak:

```text
We would like to introduce our system.
```

Stronger:

```text
We have a real-world testbed for a problem close to your method.
```

### 3. Relationship Fit

The message must match the relationship.

Cold outreach should be concise and credibility-building.

Warm introduction should acknowledge the connection and move faster into shared relevance.

Existing relationship can be more direct.

Academic or expert communication should center on the problem, not self-promotion.

### 4. Ask Size

The ask must be appropriate.

Bad:

```text
We hope to establish a strategic partnership.
```

Better for first contact:

```text
We hope to discuss whether this problem has methodological overlap with your work.
```

### 5. Product Pitch Control

Fail if the message spends too much space explaining the product before establishing shared relevance.

### 6. Next Step

The listener should know what to do next.

Examples:

```text
Could we schedule 30 minutes?
Could I send a short note before we meet?
Would you be open to a discussion?
Could we ask for your view on whether this problem is methodologically valid?
```

## Failure Modes

Hard fail:

1. No clear next step.
2. Message mismatch with relationship context.
3. Product introduction overwhelms purpose.
4. Cooperation ask is too large too early.
5. Listener cannot see why they are relevant.

Soft fail:

1. Next step is implied but not explicit.
2. Tone is slightly too formal or too casual.
3. Message has too many directions.
4. User's personality is overly flattened.

## Rewrite Rule

If this harness fails, rewrite by answering:

```text
What do we want the listener to do after reading this?
Why would they care?
What is the smallest reasonable next step?
What should we not ask for yet?
```

Then shorten or reshape the message accordingly.

## Final Rule

A one-on-one message is not successful because it sounds good.

It is successful if it makes the next right action easier.
