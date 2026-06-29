# Markdown Cleanliness Harness

## Purpose

Ensure reusable Markdown artifacts are clean, paste-ready, and free from UI or tool artifacts.

Use this harness for:

```text
README
GitHub docs
API docs
Markdown proposals
Markdown emails
open-source documentation
technical docs
```

## Checkpoints

1. Does the output contain UI residue?
2. Are fenced code blocks valid?
3. Are headings properly formatted?
4. Are tables clean and readable?
5. Are notes separated from the artifact?
6. Is the artifact paste-ready?
7. Does the Markdown mix unsupported syntax or UI labels?

## Forbidden UI Artifacts

Remove:

```text
Copy
Open in canvas
bash Copy
text Copy
Tool output
Open in Gmail
Open in canvas
```

## Code Block Rule

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

## Notes Rule

If extra notes are needed, place them after the artifact under:

```markdown
## Notes
```

or outside the artifact, clearly separated.

Do not mix notes into README body unless they belong there.

## Failure Modes

Hard fail:

1. Contains UI residue.
2. Broken code fences.
3. Markdown is not paste-ready.
4. Commentary is mixed into artifact.
5. Language changes inside artifact unintentionally.

Soft fail:

1. Headings are inconsistent.
2. Tables are too wide.
3. Code examples lack placeholders.
4. Extra notes are not separated.

## Rewrite Rule

If failed:

```text
Remove UI residue.
Fix code fences.
Separate notes from artifact.
Regenerate clean Markdown only.
```

## UI Residue Hard Fail

For public artifacts, the following are hard failures:

```text
Copy
bash Copy
text Copy
Open in canvas
Tool output
```

If any appear, regenerate the artifact.

Do not ask the user to clean them manually.

## Artifact / Note Separation

Markdown artifact must not include assistant-side notes unless requested.

If notes are needed, output them after the artifact under:

```text
Notes for you, not for publication:
```

## Clean Code Block Rule

Use valid fenced code blocks only:

```bash
git clone https://github.com/<your-org>/<repo-name>.git
```

Never output:

```text
bash
Copy
git clone ...
```

## Final Rule

A Markdown artifact should be ready to paste into a repo without cleanup.

## Public README Cleanliness

For public README output, additionally check:

```text
no internal debug notes
no Chinese notes in English README unless requested
no UI residue
no excessive file tree
no unverified installation commands
no unconfirmed license
no third-party affiliation implication
```

If the README includes a long file tree, ask:

```text
Can this move to an Architecture section or separate docs file?
```

## Public Release Final Pass

Before final output, ensure:

```text
first screen explains user value
examples are practical
installation is bounded
status is clear
license is confirmed or marked TBD
```

## Release-Ready Markdown Rule

For README output, markdown cleanliness includes more than removing UI residue.

Also check:

```text
private notes are separated
code blocks are valid
placeholders are clear
file paths are accurate
license/status is not invented
section headings are clean
```

## Notes Are Not Markdown Pollution If Separated

Assistant notes may be included after the artifact if clearly separated.

Acceptable:

```text
Notes for you, not for publication:
- Replace <your-org>.
- Confirm license.
```

Not acceptable:

```text
Notes embedded inside README sections.
```
