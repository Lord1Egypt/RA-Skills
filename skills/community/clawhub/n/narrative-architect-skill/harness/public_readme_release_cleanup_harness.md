# Public README Release Cleanup Harness

## Purpose

Public README Release Cleanup Harness is the final check for README files intended for GitHub or public release.

It runs after:

```text
public_artifact_final_pass_harness
human_release_voice_harness
markdown_cleanliness_harness
language_match_harness
user_term_fidelity_harness
```

This harness does not rewrite the whole README by default. It performs final release cleanup.

## Applies To

Use this harness when the user asks for:

```text
GitHub README
public README
README.md for launch
open-source README
repo landing page
public skill README
developer-facing README
```

## Checkpoint 1: Correct Project Path

The project structure must show the actual repo or skill directory accurately.

Bad:

```text
skills/
├── skill.md
├── runtime_chain.md
```

Why bad:

```text
It suggests skill.md lives directly under skills/.
```

Better:

```text
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

Rule:

```text
If the artifact describes an OpenClaw skill, show the skill directory as a named subdirectory under skills/.
```

Use placeholders when needed:

```text
skills/<your-skill-name>/
```

or:

```text
skills/narrative_architect_skill/
```

depending on context.

## Checkpoint 2: Notes Must Stay Outside the Artifact

Private instructions to the user must not be part of the README.

Examples of private notes:

```text
Replace <your-org> before publishing.
Decide the license before release.
I used this name because...
If you insist on this internal name...
```

These may be shown after the README under:

```text
Notes for you, not for publication:
```

But they must be clearly outside the artifact.

Hard fail if:

```text
private notes are inside the README body
Chinese notes appear inside an English README
publishing reminders are mixed into artifact sections
```

## Checkpoint 3: Public Link Safety

Do not include public links unless they are confirmed.

Bad:

```markdown
Built on [OpenClaw](https://openclaw.ai)
```

if the public site or official relationship is not confirmed.

Safer alternatives:

```text
Designed for OpenClaw-compatible skill runtimes.
```

or:

```text
Built for OpenClaw-style skill runtimes.
```

Rule:

```text
If the link, ecosystem status, or official affiliation is uncertain, avoid the link and use bounded language.
```

## Checkpoint 4: Installation Language Must Be Typical, Not Absolute

Bad:

```text
Place the skill directory in your OpenClaw workspace under skills/.
```

Better:

```text
A typical local setup is to place the skill directory under skills/ in your OpenClaw workspace.
```

Rule:

```text
Unless the installation method is official and verified, describe it as typical or placeholder-based.
```

## Checkpoint 5: Claim Boundary Must Match Task Type

Avoid over-rigid claim boundary language that would block creative or strategic tasks.

Too rigid:

```text
Every statement traces to what you actually know.
```

Better:

```text
For source-grounded work, factual claims stay tied to known material. If the source has gaps, the output names them instead of filling them with speculation.
```

Rule:

```text
Claim boundary should apply strongly to factual/source-grounded work, without preventing naming, strategy, storytelling, or creative drafting.
```

## Checkpoint 6: Public README Should Avoid Internal Exact Counts

Avoid exact counts unless verified at render time.

Bad:

```text
10 mappers
18 harnesses
6 policies
9 regression tests
```

Better:

```text
mappers for context and story structure
harnesses for quality checks
contracts for output formats
policies for behavior
regression cases for testing
```

Rule:

```text
Public README should describe categories, not fragile internal counts.
```

## Checkpoint 7: Clean Markdown

Remove all UI residue:

```text
Copy
bash Copy
text Copy
Open in canvas
Tool output
```

Code blocks must be valid fenced Markdown.

Good:

```bash
git clone https://github.com/<your-org>/<repo-name>.git
```

Bad:

```text
bash
Copy
git clone ...
```

## Checkpoint 8: License and Status Must Be Confirmed or Marked

Do not assume license.

Use:

```text
License: TBD
```

unless the user confirms.

Status should be bounded:

```text
Prototype.
Experimental.
Work in progress.
```

Do not imply stable production readiness unless confirmed.

## Checkpoint 9: Artifact Should Be Copyable Without Cleanup

Before final output, ask:

```text
Can the README section be copied directly into GitHub?
Would private notes be accidentally included?
Are placeholders clear?
Are public claims safe?
```

If not, clean it.

## Failure Modes

Hard fail:

1. Wrong project path structure.
2. Private notes inside artifact body.
3. UI residue remains.
4. Unconfirmed public link or affiliation.
5. Fake install commands.
6. License assumed without confirmation.
7. Wrong language.
8. Markdown not paste-ready.

Soft fail:

1. Installation wording too absolute.
2. Claim boundary too rigid.
3. File structure too detailed.
4. Internal counts too precise.
5. README is clean but still slightly internal.

## Rewrite Rule

If failed, do a final cleanup pass only:

```text
fix paths
separate notes
remove UI residue
bound installation language
soften over-rigid claim boundary
remove unverified links
mark license/status as TBD if unknown
```

Do not rewrite the entire README unless the structure itself is wrong.

## Final Rule

A public README should be safe to paste, safe to publish, and safe to maintain.
