# GC_NARR_023_PUBLIC_README_RELEASE_CLEANUP

## Purpose

Test whether the skill performs a final cleanup pass on a public README before release.

## Scenario

User asks:

```text
Please provide a README for this skill. I want to publish it on GitHub.
```

The draft is already good but still contains small release blockers.

## Required Behavior

the skill must:

1. Keep Markdown clean.
2. Remove UI residue.
3. Use correct project path.
4. Keep private notes outside the README.
5. Avoid unverified public links.
6. Use bounded installation wording.
7. Mark license as TBD unless confirmed.
8. Avoid overly absolute claim boundary wording.
9. Keep architecture below user value.
10. Deliver a copy-ready artifact.

## Bad Pattern

```text
## Project Structure

skills/
├── skill.md
├── runtime_chain.md
```

Why bad:

```text
May imply wrong repo structure.
```

## Good Pattern

```text
## Project Structure

skills/<skill-name>/
├── skill.md
├── runtime_chain.md
├── mappers/
├── principles/
├── harness/
├── contracts/
├── policies/
└── cases/
```

## Bad Pattern 2

```text
*Built on [OpenClaw](https://openclaw.ai)*
```

Why risky:

```text
May imply public link or official ecosystem relationship if not confirmed.
```

## Good Pattern 2

```text
Designed for OpenClaw-compatible skill runtimes.
```

## Bad Pattern 3

```text
Every statement traces to what you actually know.
```

Why too rigid:

```text
Over-constrains creative or strategic tasks.
```

## Good Pattern 3

```text
For source-grounded work, factual claims stay tied to known material. If the source has gaps, the output names them instead of filling them with speculation.
```

## Acceptance Criteria

Pass if:

1. Artifact is ready to paste.
2. Notes are separate.
3. README uses accurate project path.
4. Claim boundary wording is precise.
5. Public links are safe.
6. Install/license details are bounded.
7. No UI residue remains.
8. Output language matches request.
9. Project structure is below user value.
10. The README feels public, not internal.

Fail if:

1. The user must manually clean formatting.
2. Notes are mixed into artifact.
3. Path structure is misleading.
4. License is assumed.
5. Unverified public link remains.
6. The README still has release blockers.

## Golden Principle

The final 5% of README cleanup matters because it decides whether the artifact can actually be published.
