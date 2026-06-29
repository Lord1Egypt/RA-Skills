# Collaboration Intent Mapper

## Purpose

Collaboration Intent Mapper turns vague cooperation language into specific collaboration hypotheses.

Users often say "we want to discuss cooperation" or "we want to explore collaboration." That is too vague for effective communication.

the skill should help the user clarify what kind of collaboration is being proposed, what value each side brings, and what the first conversation should test.

## Required Output

Internally produce:

```yaml
collaboration_intent:
 collaboration_type:
 shared_problem:
 user's_contribution:
 recipient_contribution:
 possible_joint_question:
 evidence_or_testbed:
 first_meeting_goal:
 not_yet_asking_for:
```

## Collaboration Types

Examples:

```text
methodology validation
research collaboration
case study collaboration
data partnership
pilot project
expert consultation
strategic alliance
co-authored paper
customer discovery
institutional introduction
commercial partnership
```

## Shared Problem

The problem both sides could care about.

Examples:

```text
How to prioritize resources under uncertain and heterogeneous data.
How to translate a theory from one scale to another.
How to evaluate adoption pathways before full investment.
How to make complex decisions when evidence quality varies.
```

## User's Contribution

What the user brings.

Examples:

```text
real cases
operational data
market context
domain problem
implementation environment
software system
decision workflow
commercial scenario
```

## Recipient Contribution

What the other side may bring.

Examples:

```text
methodology
theoretical framework
research credibility
domain expertise
validation approach
data science method
policy perspective
clinical perspective
```

## Possible Joint Question

A concrete question for discussion.

Weak:

```text
Can we cooperate?
```

Strong:

```text
Can a resource allocation method developed for regional planning be tested in a cross-market adoption scenario?
```

## Evidence or Testbed

What makes the collaboration real rather than abstract?

Examples:

```text
running cases
pilot sites
existing datasets
planned country rollout
customer pipeline
field interviews
historical decisions
prototype system
```

## First Meeting Goal

The first meeting should not try to complete the entire collaboration.

It should test:

```text
is the problem valid?
is there methodological overlap?
is the testbed useful?
is the other side interested?
what next material should be prepared?
```

## Not Yet Asking For

Clarify what the user is not asking too early.

Examples:

```text
formal partnership
funding
endorsement
data access
paper authorship
commercial commitment
exclusive support
```

## Failure Modes

Fail if:

1. "Collaboration" remains abstract.
2. The message does not explain why this recipient is relevant.
3. The user over-asks before trust exists.
4. The user's contribution is unclear.
5. The recipient's value is treated as generic.
6. Too many cooperation directions are listed at once.
7. The first meeting has no clear purpose.

## Final Rule

A good collaboration message should make the other side think:

"This is not a random request. This is a real problem where my method, experience, or position may matter."
