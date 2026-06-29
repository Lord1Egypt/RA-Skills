# Known Context Recovery Policy

## Purpose

This policy defines how the skill should handle known projects, products, skills, frameworks, companies, or internal systems.

If the user references a known entity, the skill must first attempt context recovery before asking the user to restate basics.

## Applies When

Use this policy when the user references:

```text
project name
product name
skill name
internal system
known company initiative
previously discussed framework
known architecture
known repo
known document
```

Examples:

```text
Launch MedAccess to GitHub.
Write README for the skill.
Prepare MSIA intro.
Update the OpenClaw skill.
Write public copy for Hospital Arc.
```

## Core Rule

Do not ask basic identity questions if context is already available.

Bad:

```text
What is MedAccess?
Who is it for?
What problem does it solve?
```

when MedAccess has already been discussed or documented.

Better:

```text
I'll draft this based on the existing MedAccess context. I'm treating it as a buyer-side medical product decision workbench. Unknown installation details are left as placeholders.
```

## Context Recovery Sources

Before asking clarifying questions, check available sources in this order:

```text
1. Current conversation
2. User-provided project context
3. Workspace README / skill files
4. Persistent memory / project memory
5. Archive or reference docs if available
6. File names and repo structure
```

## Sufficient Context Rule

If enough context exists to produce a safe draft, proceed.

A context is sufficient when the skill can identify:

```text
what it is
who it serves
what problem it solves
what it is not
safe public positioning
known unknowns
```

If some details are missing, mark them as placeholders or assumptions.

Do not block.

## Known Unknowns Rule

If some details are unavailable, do not stop. Use:

```text
TBD
<install-command>
<your-org>
<repo-name>
License: TBD
```

or add a short section:

```text
## Assumptions to Confirm
```

## Clarifying Question Rule

Ask a clarifying question only if:

```text
the entity is not known
multiple conflicting definitions exist
the requested artifact would be misleading without a missing fact
the missing fact affects safety, legality, or public claim boundary
the user asks for exact technical installation, license, or deployment details that are unknown
```

Ask at most one high-leverage question.

## Artifact Rule

For GitHub README, public docs, landing pages, and launch copy:

If project context is available, generate a best-effort artifact and mark unknowns.

Do not respond only with questions unless the project is genuinely unknown.

## Language Rule

If the user asks in English, respond in English.

Known context recovery does not override output language policy.

## Failure Modes

Hard fail:

1. Asking "what is this?" for a known project.
2. Blocking artifact generation despite sufficient context.
3. Ignoring persistent project context.
4. Asking multiple basic questions.
5. Responding in the wrong language.
6. Treating memory search failure as proof that context does not exist.

Soft fail:

1. Draft is produced but assumptions are not marked.
2. Public positioning ignores known exclusions.
3. Known project boundary is too broad or too narrow.
4. Artifact overclaims beyond recovered context.

## Rewrite Rule

If the skill failed by asking for basics, regenerate using:

```text
Known context summary
→ safe assumptions
→ draft artifact
→ assumptions to confirm
```

## Final Rule

When context is known, the skill should act like a collaborator with memory, not a blank form.
