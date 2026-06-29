# Runtime Mode Selector

## Purpose

Runtime Mode Selector chooses the appropriate execution mode before the skill processes the task.

The skill should not run the full narrative chain for every request.

A short message should not become an essay. 
A quick introduction should not become a proposal. 
A factual explanation should not be forced into a full story. 
A major public narrative should not be handled as a short rewrite.

## Core Rule

```text
Use the lightest mode that can solve the task.
```

If the task is simple, use a light chain.
If the task is strategic, use a deeper chain.
If the user is dissatisfied, do not rewrite blindly; enter recovery mode.

---

## Runtime Modes

The skill supports seven runtime modes:

```text
1. Quick Message Mode
2. One-on-One Strategy Mode
3. Public Narrative Mode
4. Expert Translation Mode
5. Rewrite Recovery Mode
6. Personal Communication Mode
7. Full Narrative Mode
```

Full Narrative Mode is reserved for complex, high-stakes, long-form narrative work.

---

# Mode 1: Quick Message Mode

## Use When

User asks for:

```text
short message
WeChat message
intro message
brief follow-up
one-sentence framing
short reply
meeting confirmation
small ask
warm intro note
```

## Goal

Make the next action easier.

This mode should not over-build the story.

## Runtime Chain

```text
Conversation Purpose
→ Relationship Context
→ Listener Hook
→ Minimum Next Action
→ Light Surface Check
→ Output
```

## Output Shape

Usually:

```text
1-5 sentences
direct
low friction
clear next step
```

## Do Not Run By Default

```text
Full Story Kernel
Full Affective Arc
Full Narrative Entropy
Full Harness Stack
Long-form rendering
```

## Failure Modes

Fail if:

```text
the message becomes too long
the output sounds like a proposal
the user's ask is hidden
the next step is unclear
the tone is too formal for the relationship
```

---

# Mode 2: One-on-One Strategy Mode

## Use When

User asks for communication with a specific person, team, institution, investor, customer, partner, expert, academic group, or resource holder.

Examples:

```text
I want to contact this professor.
I need to talk to an investor.
Help me message a hospital director.
We need to approach a partner.
This is through a friend.
Help me prepare talking points.
```

## Goal

Clarify the communication strategy, then produce the message or talking points.

The task is not only writing.
The task is to move a relationship, belief, or collaboration forward.

## Runtime Chain

```text
Conversation Purpose
→ Relationship Context
→ Recipient Motivation
→ Collaboration / Ask Hypothesis
→ Attraction Filter
→ Narrative Authority
→ Claim Boundary
→ Message / Talking Points
→ Harness
→ Output
```

## Required Checks

```text
conversation_outcome_harness
non_offensive_personality_harness
claim_harness
source_fidelity_harness
surface_naturalness_harness
```

## Output Shape

Depending on user request:

```text
short message
medium message
talking points
meeting opener
follow-up
```

## Failure Modes

Fail if:

```text
the message sounds like generic outreach
the product becomes the hero
the real purpose is unclear
the ask is too large too early
relationship context is wrong
the message is polite but forgettable
```

---

# Mode 3: Public Narrative Mode

## Use When

User asks for:

```text
article
speech
brand story
public post
short video script
Douyin script
LinkedIn post
media article
founder letter
presentation narrative
campaign copy
```

## Goal

Create public-facing story with tension, emotion, judgment, and memorability.

## Runtime Chain

```text
Story Kernel
→ Narrative Authority
→ Value / Stakes
→ Action-Reaction-Gap
→ Controlling Idea
→ Audience Cognition
→ Affective Arc
→ Narrative Entropy
→ Renderer
→ Harness
→ Output
```

## Required Checks

```text
claim_harness
source_fidelity_harness
narrative_authority_harness
story_harness
emotional_resonance_harness
narrative_entropy_harness
surface_naturalness_harness
```

## Output Shape

May be:

```text
short-form script
article
speech
manifesto
post
page narrative
```

## Failure Modes

Fail if:

```text
it only explains
it has no protagonist pressure
it has no turn
style becomes performance
it tries to please everyone
the ending is a slogan
```

---

# Mode 4: Expert Translation Mode

## Use When

User asks to explain a complex concept to a target audience.

Examples:

```text
Explain X to ordinary people.
Explain X to technical team.
Explain X to investors.
Explain X to children.
What is X?
Introduce this architecture.
Translate this technical idea into business language.
```

## Goal

Make a complex concept understandable without flattening it.

This mode prioritizes clarity, conceptual boundary, audience entry point, and one meaningful turn.

## Runtime Chain

```text
Claim Boundary
→ Audience Cognition
→ Audience Entropy Tolerance
→ Low-Entropy Ground
→ High-Entropy Turn
→ Mechanism Explanation
→ Surface Naturalness
→ Output
```

## Optional

Use Affective Arc if target audience is general public, media, or non-technical.

Use technical precision if target audience is expert.

## Required Checks

```text
claim_harness
source_fidelity_harness
audience_harness
narrative_entropy_harness
surface_naturalness_harness
```

## Failure Modes

Fail if:

```text
too technical for audience
too childish for audience
too many metaphors
no mechanism
no meaningful turn
too much jargon early
```

---

# Mode 5: Rewrite Recovery Mode

## Use When

User expresses dissatisfaction, correction, or reframing.

Examples:

```text
不是这个意思。
太 AI。
不够有情绪。
不是冷邮件。
这个版本不适合。
太销售。
缺少主体性。
这个框架更接近我们想要的。
```

## Goal

Identify which layer failed, then reroute.

Do not keep polishing the wrong draft.

## Runtime Chain

```text
User Feedback
→ Failure Layer Diagnosis
→ Reroute to Correct Mode
→ Rewrite
→ Output
```

## Failure Layer Categories

```text
communication context error
relationship context error
conversation purpose error
claim boundary error
source fidelity error
narrative authority error
audience entry error
affective arc weakness
narrative entropy weakness
surface naturalness error
style overperformance
user frame not preserved
```

## Follow-Up Rule

If user gives clear correction, do not ask. Reroute and rewrite.

If user gives vague dissatisfaction, diagnose first and ask one high-leverage question.

Preferred question:

```text
你更想修哪一层：目的、关系语境、主张强度、情绪入口，还是表面表达？
```

## Failure Modes

Fail if:

```text
the skill defends previous output
keeps rewriting at word level
asks many questions
ignores user's correction
does not reroute
```

---

# Mode 6: Personal Communication Mode

## Use When

User asks for private, interpersonal, low-stakes, or emotionally sensitive communication.

Examples:

```text
introduce me to someone
help me text someone I like
ask someone out
recover from awkwardness
I am shy / awkward in front of her
apologize in a personal relationship
follow up after a date
```

## Goal

Create a low-pressure moment where the user's real self can appear.

This is not a pitch. This is not outreach. Do not route personal communication into One-on-One Strategy Mode.

## Runtime Chain

```text
Apply Universal Language Lock
→ Detect Personal Communication Mode
→ Map Personal Context
→ Preserve User Personality
→ Choose Low-Pressure Scene
→ Draft Sendable Message
→ Run Personal Communication Harness
→ Run Output Language Lock Harness
→ Output Message + Short Notes
```

## Required Checks

```text
personal_communication_harness
output_language_lock_harness
surface_naturalness_harness
```

## Output Shape

```text
Short framing
Sendable message
Why it works
Notes for you, not for them
```

For very short tasks:

```text
Sendable message
One note
```

## Failure Modes

Fail if:

```text
treats the message as a sales pitch
writes in the wrong language
uses pickup-artist or manipulative tactics
turns insecurity into self-pity
makes the user sound fake or performative
over-strategizes romance
```

See: `selectors/personal_communication_mode_selector.md`
See: `principles/personal_authenticity_without_performance.md`

---

# Mode 7: Full Narrative Mode

## Use When

Only for complex, high-stakes, long-form work.

Examples:

```text
major pitch narrative
founder story
brand manifesto
long-form article
keynote speech
strategic narrative document
high-stakes collaboration proposal
```

## Runtime Chain

Use the full standard chain:

```text
Parse Material
→ Extract Claim Boundary
→ Build Story Kernel
→ Map Narrative Authority
→ Identify Value / Stakes
→ Build Action-Reaction-Gap
→ Build Controlling Idea
→ Map Audience Cognition
→ Map Affective Arc
→ Map Narrative Entropy
→ Select Entry Point
→ Render with Style
→ Run Harness
→ Final Output
```

## Rule

Do not use Full Narrative Mode by default.

Use it only when the task requires full story architecture.

---

# Mode Selection Rules

## Rule 1: Short output defaults to light mode

If the user asks for a short message, brief reply, or one-liner, use Quick Message Mode unless the user explicitly asks for strategy.

## Rule 2: Named recipient triggers one-on-one strategy

If the user names a person, team, institution, investor, customer, expert, professor, partner, or friend introduction, consider One-on-One Strategy Mode.

## Rule 3: Public channel triggers public narrative

If the user names a platform or public format, use Public Narrative Mode.

Examples:

```text
Douyin
LinkedIn
media
article
speech
public post
video script
brand story
```

## Rule 4: Explanation triggers expert translation

If the task begins with:

```text
What is...
Explain...
Introduce...
Tell ordinary people...
Tell technical team...
```

use Expert Translation Mode.

## Rule 5: Dissatisfaction triggers recovery

If the user says an output is wrong, weak, not right, too AI, too salesy, too flat, or not their intent, use Rewrite Recovery Mode.

## Rule 6: Preserve user's preferred frame

If the user says a version is close to their desired framework, do not replace the structure. Improve within that frame.

## Rule 7: When uncertain, choose lighter mode

If two modes both fit, choose the lighter mode first.

The system may escalate if the output fails.

## Rule 8: Personal communication is not outreach

If the user asks for romantic, friendship, dating, or emotionally personal communication, use Personal Communication Mode, not One-on-One Strategy Mode. One-on-One Strategy is for professional outreach, collaboration, and institutional contact. Routing personal communication through One-on-One Strategy produces sales-toned messages and violates the personal authenticity principle.

---

# Output Visibility

Do not expose mode selection unless:

```text
the user asks for analysis
the user is debugging the skill
the user asks why the output changed
```

Default output should be user-facing content only.

---

# Final Rule

The skill should not show how much machinery it used.

It should use the right amount of machinery and then disappear behind the output.
