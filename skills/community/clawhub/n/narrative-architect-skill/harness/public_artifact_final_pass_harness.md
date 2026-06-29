# Public Artifact Final Pass Harness

## Purpose

Public Artifact Final Pass Harness is the last check before any public-facing artifact is delivered.

It applies to:

```text
GitHub README
open-source documentation
developer docs
public repo landing page
website copy
product page
marketplace listing
launch post
public skill description
public proposal
```

This harness checks whether the artifact is ready for external readers, not just internally correct.

## Priority

Run this harness after:

```text
language_match_harness
user_term_fidelity_harness
source_fidelity_harness
markdown_cleanliness_harness
public_release_harness
```

It is the final release gate.

## Core Rule

```text
Public artifacts must be user-value-first, source-safe, markdown-clean, and publication-ready.
```

---

## Checkpoint 1: First-Screen Value

A stranger should understand the project within the first screen.

The first screen should answer:

```text
What is this?
Who is it for?
What problem does it solve?
Why should I keep reading?
```

Good:

```text
Turn complex ideas into story-driven communication.
```

Bad:

```text
This skill contains multiple mappers, harnesses, runtime modes, and policies.
```

Internal architecture must not appear before user value.

---

## Checkpoint 2: Public Name Safety

If the public project name references a real person, famous author, book, company, framework, public figure, or third-party brand, flag risk.

Risk examples:

```text
possible affiliation confusion
trademark confusion
copyright association
unwanted dependency on another brand
searchability problems
```

Safer action:

```text
Use a neutral public name.
Keep internal nickname private.
Mention inspiration only in careful, non-affiliation language if needed.
```

Bad:

```text
Built on [famous author]'s book.
```

Better:

```text
Inspired by classic story design, communication strategy, and audience-centered writing.
```

If mentioning a third party is necessary:

```text
This project is not affiliated with [third party].
```

---

## Checkpoint 3: Public Inspiration Boundary

Do not make private inspiration the public positioning.

Internal:

```text
the skill
McKee-inspired story chain
```

Public:

```text
Narrative Architect Skill
Story-driven communication skill
Communication architecture framework
```

Private references can live in:

```text
docs/background.md
docs/methodology.md
```

Public README should not depend on them.

---

## Checkpoint 4: Architecture Placement

Architecture should come after:

```text
what it is
who it is for
what it helps users do
example usage
installation / status
```

If architecture is long, move it to:

```text
docs/architecture.md
```

README may include a short structure summary, but not a full system dump unless user explicitly requests an architecture-first README.

Bad early section:

```text
## Skill Structure
[long file tree]
```

Better later section:

```text
## Project Structure

A simplified layout:

skills/project/
├── skill.md
├── runtime_chain.md
├── mappers/
├── harness/
└── cases/
```

---

## Checkpoint 5: No Exact Internal Counts Unless Verified

Avoid exact internal counts in public README unless automatically verified.

Risky:

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
regression cases for testing
```

Exact counts become stale quickly.

---

## Checkpoint 6: Claim Boundary

Public claims must be bounded.

Avoid:

```text
guarantees persuasion
works for every audience
automates communication
replaces human judgment
always creates compelling stories
```

Prefer:

```text
helps structure communication
supports audience-specific drafting
reduces common narrative failures
provides reusable checks
helps users turn complex material into clearer stories
```

---

## Checkpoint 7: Artifact Hygiene

The artifact must contain no UI residue.

Remove:

```text
Copy
Open in canvas
bash Copy
text Copy
Tool output
Open in Gmail
```

Code blocks must be clean:

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

---

## Checkpoint 8: Notes Separation

Assistant notes must not be mixed into the artifact.

If notes are needed, separate them clearly after the artifact:

```text
Notes for you, not for the README:
- Replace <your-org> before publishing.
- Confirm license before release.
```

Do not include such notes inside the README unless the user explicitly requests a README section for notes.

---

## Checkpoint 9: Installation / License Safety

Do not invent:

```text
install commands
package availability
registry status
license
runtime requirements
official integrations
production readiness
```

Use placeholders:

```text
<your-org>
<repo-name>
<install-command>
License: TBD
```

If license is not confirmed, do not assume MIT.

---

## Checkpoint 10: Public Reader Usability

The artifact should help a public reader act.

A README should include:

```text
what it is
who it is for
what it can do
example usage
installation or setup placeholder
project status
contributing guidance
license or TBD
```

If the README only explains philosophy, it fails.

---

## Failure Modes

Hard fail:

1. UI residue remains.
2. Wrong language.
3. README starts with internal architecture.
4. Public name implies unofficial affiliation.
5. License or install command is invented.
6. Artifact contains unverified availability claims.
7. Notes are mixed into publishable content.
8. Full file tree appears before user value.
9. Internal methodology is used as public positioning.

Soft fail:

1. User value appears too late.
2. Architecture is too detailed.
3. Public positioning is too theoretical.
4. README lacks examples.
5. README is accurate but intimidating.
6. First screen does not tell reader why to care.

## Rewrite Rule

If this harness fails, regenerate using:

```text
Project Name
→ one-line value
→ what it is
→ who it is for
→ what it helps users do
→ example usage
→ how it works
→ installation / status
→ architecture summary
→ contributing / license
```

Then remove all UI residue and separate assistant notes.

## Human Voice Final Check

After checking public release safety and cleanliness, check whether the artifact still sounds generated.

Ask:

```text
Would a stranger feel this was written by someone who has experienced the problem?
Does the opening contain a real friction?
Is there a point of view?
Could this copy be pasted onto any generic AI tool?
```

If the answer suggests AI-like genericness, run `human_release_voice_harness`.

## Do Not Sacrifice Delivery Discipline

Human voice must not introduce:

```text
unverified claims
messy Markdown
wrong language
over-casual tone
offensive personality
unsupported drama
```

Human voice is a final tuning layer, not permission to break artifact rules.

## README Release Cleanup Trigger

If the public artifact is a README, run:

```text
public_readme_release_cleanup_harness
```

after markdown cleanliness and human release voice checks.

## Final README Path Check

If the README contains a project structure section, verify the path reflects the intended repository or skill directory.

For OpenClaw skills, prefer:

```text
skills/<skill-name>/
```

not:

```text
skills/
```

unless the root truly contains the files directly.

## Notes Separation Check

If the response contains notes for the user, ensure they are outside the publishable artifact.

Notes should be introduced with:

```text
Notes for you, not for publication:
```

## Public Link Check

If the README contains a public ecosystem link, verify that the link and implied affiliation are known.

If uncertain, replace with neutral wording.

## Final Rule

A public artifact should be ready to paste into GitHub or a public page without cleanup.
