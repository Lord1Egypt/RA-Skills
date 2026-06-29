# Recipient Power Context Mapper

## Purpose

Recipient Power Context Mapper identifies whether the target recipient requires high-power communication discipline.

This mapper runs inside One-on-One Strategy Mode when the user names or implies a specific person, investor, expert, CEO, public figure, institution, regulator, or senior decision-maker.

## Required Output

```yaml
recipient_power_context:
  recipient_type:
  power_level:
  public_visibility:
  likely_attention_constraint:
  relationship_distance:
  acceptable_claim_style:
  acceptable_ask_size:
  recipient_risk:
  recommended_pitch_shape:
```

## Field Definitions

### recipient_type

Examples:

```text
public_figure
major_ceo
investor
senior_academic
regulator
institutional_leader
celebrity
technical_leader
expert_practitioner
customer_executive
artist
creator
performer
designer
persona_based_professional
```

### power_level

Options:

```text
low
medium
high
very_high
```

### public_visibility

Options:

```text
private
semi_public
public
highly_public
```

### likely_attention_constraint

How much time and patience the recipient likely has.

Examples:

```text
very_low
low
medium
unknown
```

High-profile recipients usually have low attention tolerance.

### relationship_distance

Examples:

```text
cold
warm_intro
known_but_not_close
existing_relationship
trusted_relationship
```

### acceptable_claim_style

For high-power recipients, preferred style:

```text
specific
bounded
testable
non-flattering
non-diagnostic
non-performative
```

Avoid:

```text
grand claims
psychological assumptions
public biography summary
excessive praise
direct criticism
```

### acceptable_ask_size

For first contact, use small asks.

Examples:

```text
15-minute test
review one output
send one hard example
permission to show a sample
reply if useful
```

Avoid:

```text
buy the product
adopt the system
schedule long meeting
strategic partnership
formal collaboration
public endorsement
```

### recipient_risk

Risks when addressing this person.

Examples:

```text
sounds like fan mail
sounds like a consultant diagnosis
sounds like a cold sales pitch
makes unsupported claims about their beliefs
overuses public company names
attacks their communication
asks for too much
```

### recommended_pitch_shape

Options:

```text
proof_challenge
sharp_problem_frame
warm_intro_request
technical_demo_offer
one_specific_use_case
```

## Detection Rules

Use this mapper when the user says:

```text
sell to [specific famous person]
pitch to [CEO / investor / professor / regulator]
message [public figure]
reach out to [senior leader]
convince [high-status recipient]
```

## High-Power Communication Rule

For high-power recipients:

```text
specific > broad
testable > persuasive
bounded > grand
challenge > pitch
structural problem > personal diagnosis
```

## Artist / Creator Rule

For artists, creators, performers, and persona-based professionals:

```text
do not enter through their craft
enter through where craft loses control
do not critique their output
do not use narrative theory language unless they do
the skill serves the infrastructure around the art, not the art itself
```

## Failure Modes

Fail if:

1. The message over-psychologizes the recipient.
2. The message summarizes the recipient's public identity too much.
3. The message claims what the recipient values without evidence.
4. The message directly diagnoses the recipient's failure.
5. The ask is too large.
6. The message sounds like admiration or criticism rather than a useful challenge.
7. The message name-drops too many of the recipient's projects.

## Final Rule

High-profile recipients do not need more flattery, biography, or persuasion.

They need a sharp reason to test whether you are useful.
