# Public Release Policy

## Purpose

Public Release Policy governs how Robert Skill writes content intended for public distribution.

Use this policy when the user asks for:

```text
GitHub README
open-source launch
public repo copy
website copy
landing page
product page
public announcement
launch post
public skill description
marketplace listing
developer documentation
press-facing copy
```

## Core Rule

Public release content must prioritize:

```text
user value
use cases
clarity
truthfulness
ease of adoption
public naming safety
```

over:

```text
internal architecture
private inspiration
implementation detail
theory exposition
long file tree
internal harness names
private workflow terminology
```

## Public vs Internal Content

### Internal Content May Include

```text
full runtime chain
mappers
harnesses
private methodology notes
raw references
internal skill name
implementation details
development history
```

### Public Content Should Lead With

```text
one-line value proposition
who it is for
what problem it solves
what it helps users do
how to start
examples
status
license
contributing guidance
```

## Public Naming Rule

If the public name references a real person, copyrighted work, trademark, organization, platform, or identifiable proprietary method, Robert Skill must flag potential public-release risk.

Examples:

```text
Robert Skill
McKee Skill
Palantir-style Skill
OpenAI-native Skill
```

Risk types:

```text
confusion with official affiliation
trademark risk
copyright/provenance risk
unwanted dependency on another brand
unclear public positioning
```

Recommended action:

```text
Use neutral public branding unless affiliation is official or permission is clear.
```

Examples:

```text
Narrative Architect Skill
StoryKernel
NarrativeOS
StoryForge
Communication Architect
```

## Inspiration Disclosure Rule

Private inspiration does not need to become public branding.

Instead of:

```text
Built on Robert McKee's Story.
```

Prefer:

```text
Inspired by classic story design, audience cognition, and communication strategy.
```

If a real author or copyrighted work is mentioned, use careful language:

```text
Inspired by story design principles. Not affiliated with [person / organization].
```

## Public README Priority

A public README should follow this order:

```text
1. Project name
2. One-line description
3. What it is
4. Why it exists
5. Who it is for
6. Use cases
7. Quick start / example usage
8. How it works
9. Project structure
10. Status
11. Contributing
12. License
```

Do not lead with:

```text
full internal file tree
full runtime chain
long philosophy section
private methodology
all harnesses
all mappers
```

unless the repository is specifically for developers extending the skill and the user requests architecture-first documentation.

## Internal Architecture Exposure Rule

Architecture can appear in public docs, but only after user value and usage are clear.

For README:

```text
User value first.
Architecture second.
Full file tree optional.
```

If architecture is too long, move it to:

```text
docs/architecture.md
docs/runtime.md
docs/contributing.md
```

## Claim Boundary Rule

Do not overclaim public capability.

Avoid:

```text
guarantees better storytelling
turns any idea into a successful narrative
works for all audiences
fully automates communication
replaces human judgment
```

Prefer:

```text
helps structure communication
supports story-driven explanation
provides reusable narrative checks
assists with audience-specific drafts
helps reduce common writing failures
```

## Public Tone Rule

Public release copy should be:

```text
clear
confident
bounded
developer-friendly when technical
non-defensive
non-grandiose
```

Avoid:

```text
internal jargon
AI buzzwords
empty slogans
excessive manifesto language
overly academic explanation
unnecessary self-praise
```

## Failure Modes

Hard fail:

1. Public README starts with internal architecture before user value.
2. Public copy claims unofficial affiliation.
3. Public release uses a risky name without flagging it.
4. README includes internal-only methodology as public positioning.
5. Public artifact contains UI residue or mixed-language notes.
6. Claims exceed what the skill can safely promise.

Soft fail:

1. README is accurate but intimidating.
2. Public copy is too theoretical.
3. User benefit appears too late.
4. File tree is too long.
5. The project sounds like an internal research note instead of a usable skill.

## Rewrite Rule

If public release discipline fails, rewrite by asking:

```text
What should a new user understand in the first 10 seconds?
What problem does this solve?
What can they try immediately?
What public claims are safe?
What internal details should move below the fold?
```

## Final Rule

Public release content should make the right user want to try the project before making them understand the whole architecture.
