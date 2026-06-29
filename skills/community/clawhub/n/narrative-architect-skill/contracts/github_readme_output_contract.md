# GitHub README Output Contract

## Purpose

Ensure GitHub README outputs are usable, accurate, clean, and publication-ready.

A GitHub README is not just marketing copy. It is a developer-facing artifact. It must be clear, structured, truthful, and easy to paste into a repository.

## Applies When

Use this contract when the user asks for:

```text
GitHub README
README.md
open-source project description
repo documentation
skill README
package landing page
developer documentation
```

## Default Language

Use English by default when:

```text
the user asks in English
the artifact is intended for GitHub or open-source publishing
the user does not request Chinese
```

If the user asks in English, all user-facing notes and the README should be in English.

## Output Location

Default: output the README in the dialogue.

Write to a file only if:

```text
the user explicitly asks to save/write/export
the environment task requires file output
file-based exchange has already been established
```

## Markdown Cleanliness

The README must be clean Markdown.

Do not include:

```text
Copy
Open in canvas
bash Copy
text Copy
UI labels
tool output notes
Chinese commentary inside English README
```

Use proper fenced code blocks:

```bash
git clone https://github.com/<your-org>/<repo-name>.git
```

## Required Structure

Use this default structure unless the user specifies another:

```markdown
# Project Name

One-line description.

## What It Is

## Why It Exists

## Core Features

## How It Works

## Example Usage

## Installation

## Roadmap

## Contributing

## License
```

For skill repos, optionally include:

```markdown
## Skill Structure
## Agent Roles
## Runtime Modes
```

## Claim Boundary

Do not invent:

```text
installation commands
package availability
ClawHub availability
npm package name
PyPI package name
license status
supported integrations
API keys
runtime requirements
benchmarks
compatibility
official affiliations
production maturity
```

Use placeholders when unknown:

```text
<your-org>
<repo-name>
<install-command>
<TBD>
```

## Installation Rule

Bad:

```bash
clawhub install <project-name>
```

unless the package is actually published on ClawHub.

Better:

```bash
# Replace with your actual install command
<install-command>
```

or:

```bash
git clone https://github.com/<your-org>/<repo-name>.git
```

## Requirements Rule

Do not state specific requirements unless known.

Bad:

```text
No API keys needed.
OpenClaw gateway required.
Works with all model providers.
```

Better:

```text
Requirements depend on your OpenClaw runtime and model provider configuration.
```

## Name Availability Rule

Do not claim name availability unless verified.

Bad:

```text
GitHub likely does not collide.
Google almost does not collide.
The name is available.
```

Better:

```text
Before publishing, check GitHub, package registries, and domain availability.
```

## README Voice

Good README voice:

```text
clear
specific
developer-friendly
confident but bounded
not overhyped
```

Avoid:

```text
too much manifesto
empty slogans
AI buzzwords
unverified promises
guaranteed outcomes
```

## Overclaim Control

Avoid:

```text
Run your entire company automatically.
Guaranteed startup success.
No human team needed.
Fully automated engineering.
Never write boilerplate again.
```

Prefer:

```text
Reduce repetitive setup work.
Coordinate agent-assisted engineering workflows.
Generate first drafts of scaffolding, docs, tests, and release artifacts.
Keep engineers focused on architecture, logic, and product decisions.
```

## Example Usage

Examples should be concrete but bounded.

Good:

```text
"Scaffold a FastAPI project with PostgreSQL and GitHub Actions."
"Draft test skeletons for these API endpoints."
"Generate a README outline for this repo."
```

Bad:

```text
"Run my whole engineering team."
"Build the entire product automatically."
```

## Status Rule

If maturity is unknown, mark as:

```text
Experimental
Prototype
Work in progress
```

Do not imply stable production maturity unless confirmed.

## Failure Modes

Hard fail:

1. README is in the wrong language.
2. README contains fake install commands.
3. README claims package or name availability without evidence.
4. README uses inconsistent project name.
5. README contains UI artifacts.
6. README mixes languages unintentionally.
7. README is mostly marketing and lacks usage details.

Soft fail:

1. README is too vague.
2. README lacks examples.
3. README lacks project status.
4. README lacks contribution guidance.
5. README sounds like translated English.

## Final Rule

A GitHub README should be paste-ready, truthful, and useful to a developer or early user.

## Public Release Priority

When a README is intended for public release, use `public_readme_output_contract.md` in addition to this contract.

Priority order:

```text
1. Public positioning
2. Naming and affiliation safety
3. Language match
4. README structure
5. Claim boundary
6. Markdown cleanliness
7. Narrative quality
```

## Architecture Placement Rule

Do not lead with full file structure.

If file structure is useful, place it after:

```text
what it is
who it is for
use cases
example usage
installation
```

or move to:

```text
docs/architecture.md
```

## Public Third-Party Reference Rule

If the README references a real author, book, company, platform, or framework:

```text
avoid implying official affiliation
avoid using the third party as the main public brand unless authorized
prefer neutral description
add disclaimer if needed
```

## User Value First Rule

The README opening should not describe internal mappers, harnesses, or chains.

It should describe what the user can do with the project.
