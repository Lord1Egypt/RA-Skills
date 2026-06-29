# Conversation Purpose Mapper

## Purpose

Conversation Purpose Mapper identifies the user's real objective before generating one-on-one communication.

Users often provide keywords, fragments, or rough thoughts. They are rarely asking only for polished wording. In one-on-one communication, they usually want to move a relationship, decision, collaboration, or belief forward.

This mapper helps the skill clarify the strategic purpose behind the message.

## Required Output

Before writing one-on-one communication, internally produce:

```yaml
conversation_purpose:
 communication_type:
 relationship_context:
 user's_real_goal:
 minimum_success_outcome:
 desired_next_action:
 listener_current_state:
 listener_desired_state:
 what_must_be_understood:
 what_should_not_be_said_too_early:
 risk_if_message_fails:
```

## Field Definitions

### communication_type

Examples:

```text
warm introduction
cold outreach
follow-up message
meeting opening
meeting closing
voice-call talking points
academic collaboration request
investor intro
customer education
media conversation
expert consultation
partner alignment
internal persuasion
```

### relationship_context

Examples:

```text
stranger
friend introduction
known but not close
existing collaborator
former colleague
senior expert
potential customer
potential investor
academic team
government or institutional contact
```

### user's_real_goal

The deeper goal behind the message.

Examples:

```text
get a meeting
earn method-level interest
invite collaboration
get feedback
secure introduction
shift perception
create trust
test fit
open a research discussion
move from awareness to participation
```

### minimum_success_outcome

The smallest outcome that would make the message successful.

Examples:

```text
The listener agrees to a call.
The listener asks for more material.
The listener introduces another person.
The listener says the research question is valid.
The listener understands this is not a product pitch.
The listener agrees there is a real methodological overlap.
```

### desired_next_action

The concrete next step.

Examples:

```text
meet
reply
review document
introduce colleague
share data direction
co-design project
schedule call
give feedback
```

### listener_current_state

What the listener likely thinks before the message.

Examples:

```text
does not know us
may think this is a sales pitch
may think the concept is too abstract
may not see relevance
may be interested but busy
may care about methodology more than product
```

### listener_desired_state

What the listener should think after reading or hearing.

Examples:

```text
This is relevant to my work.
This is a real problem, not a pitch.
This team has a useful testbed.
This could become a joint research question.
This is worth a conversation.
```

### what_must_be_understood

The one idea that must land.

Examples:

```text
We are not asking them to hear a product demo.
We are bringing a real-world problem their method may help solve.
The story is about a shared problem, not our feature list.
```

### what_should_not_be_said_too_early

Examples:

```text
full product architecture
grand vision
claims of being first
too many numbers
commercial ambition
technical jargon
requests for formal cooperation before trust exists
```

## Decision Rule

If the user's communication goal is clear, do not ask follow-up questions. Infer and proceed.

If the goal is unclear, ask one high-leverage question:

```text
What is the minimum outcome you want from this communication: a meeting, advice, collaboration interest, introduction, validation, or commitment?
```

Do not ask multiple low-level style questions first.

## Failure Modes

Fail if:

1. The text is polished but does not move the relationship forward.
2. The output sounds like a pitch when the goal is trust.
3. The message asks for a meeting without giving the listener a reason to care.
4. The message explains too much and never names the desired next step.
5. The message hides the user's real purpose.
6. The message over-asks before establishing relevance.

## Final Rule

Before writing, the skill must know what the communication is trying to make happen.
