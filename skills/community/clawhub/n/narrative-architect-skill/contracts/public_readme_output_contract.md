# Public README Output Contract

## Purpose

Public README Output Contract defines how the skill should write README files intended for public GitHub or open-source release.

This contract is stricter than internal documentation.

## Applies When

Use when the user asks for:

```text
public README
GitHub README
open-source README
launch-ready README
repo landing page
public skill README
```

## Output Language

Use English by default when:

```text
the user asks in English
the repo is developer-facing
the repo is open-source
the user does not request Chinese
```

If the user requests Chinese, write Chinese.
If the user requests bilingual output, clearly separate languages.

## Default README Structure

```markdown
# Project Name

One-line value proposition.

## What It Is

## Why It Exists

## Who It Is For

## What It Can Do

## Example Usage

## How It Works

## Installation

## Project Status

## Contributing

## License
```

Optional sections:

```markdown
## Runtime Modes
## Architecture
## Skill Structure
## Roadmap
## FAQ
```

Architecture should not appear before user value and examples.

## Public Positioning Rule

The opening should answer:

```text
What does this help me do?
```

Not:

```text
How is this internally built?
```

## Project Name Rule

If the project name references a real person, public figure, book, company, or third-party brand, flag public release risk and suggest a neutral alternative.

Do not silently publish a risky name as final.

## External Inspiration Rule

Do not overstate connection to a public author, book, company, or framework.

Avoid:

```text
Built on [famous person/book/company].
Powered by [third-party concept].
Officially based on [external work].
```

Prefer:

```text
Inspired by story design, communication strategy, and audience-centered writing.
```

If required:

```text
This project is not affiliated with [third party].
```

## Internal Structure Rule

If including a file tree, keep it short.

Good:

```text
skills/project/
├── skill.md
├── runtime_chain.md
├── mappers/
├── harness/
└── cases/
```

Avoid listing every file unless the user asks for full technical documentation.

## Usage Examples Rule

Include practical examples.

Good:

```text
"Turn this technical architecture into a 200-word explanation for investors."
"Help me write a warm intro message to a professor."
"Rewrite this pitch so it tells a story instead of selling a product."
```

## Status Rule

If the project maturity is uncertain, mark it as:

```text
Prototype
Experimental
Work in progress
```

Do not imply production readiness unless confirmed.

## Installation Rule

Use placeholders for unknown installation steps.

Good:

```bash
git clone https://github.com/<your-org>/<repo-name>.git
```

Bad:

```bash
clawhub install <project-name>
```

unless actually published.

## License Rule

If license is unknown, write:

```text
License: TBD
```

Do not assume MIT unless the user confirms.

## Failure Modes

Hard fail:

1. README starts with file structure.
2. README implies third-party affiliation.
3. README uses risky public name without note.
4. README contains fake install commands.
5. README contains UI residue.
6. README uses wrong language.

Soft fail:

1. README is too internal.
2. README is too theoretical.
3. README lacks usage examples.
4. README lacks status.
5. README lacks audience clarity.

## Final Rule

A public README should help a stranger decide whether to try the project.

## Human Voice Pass

Before final README output, run `human_release_voice_harness`.

A public README should not sound like generic SaaS copy.

## Required Human Elements

A publishable README should include at least three of the following:

```text
felt problem
clear point of view
concrete prompt example
honest boundary
short memorable line
real user situation
```

## Avoid Over-Perfect README Shape

A README can be clean without being sterile.

Do not over-optimize for symmetry.

Bad pattern:

```text
What It Is
Who It Is For
What It Does
How It Works
Core Principles
Runtime Modes
```

This is acceptable structurally, but if every section is abstract, it becomes AI-like.

Improve with:

```text
real examples
shorter sections
one or two sharp claims
fewer internal terms
```

## Public README Opening Rule

The opening should contain:

```text
one-line value
real friction or problem
what the project helps the user do
```

It should not only contain a broad category statement.

## Release Cleanup Requirement

Before final README output, apply `public_readme_release_cleanup_contract.md`.

This contract handles:

```text
path accuracy
notes separation
public link safety
installation wording
claim boundary wording
license/status placeholders
```

## Preferred Project Structure Example

For an OpenClaw skill:

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

## Preferred Claim Boundary Wording

Use:

```text
For source-grounded work, factual claims stay tied to known material. If the source has gaps, the output names them instead of filling them with speculation.
```

instead of:

```text
Every statement traces to what you actually know.
```

## Final Public README Pass

Before delivering a public README, verify:

```text
first screen: value proposition, not architecture
project name: public-safe or risk flagged
third-party references: bounded or removed
usage examples: present
installation: placeholders if unknown
license: confirmed or TBD
status: present
architecture: below usage
Markdown: clean
notes: separated
```

## Public README Should Not Include

```text
assistant reasoning
why I chose this name
publishing reminders inside README body
UI residue
unverified availability
internal-only inspiration
full file inventory
exact internal counts unless verified
```

## Public README May Include

```text
short project structure
runtime modes summary
architecture overview
links to docs
contribution guidance
```

but only after user value and example usage.

## Known Project Rule

If the README is for a known project, the skill should use recovered context to produce a best-effort README.

Do not ask basic positioning questions if project context is sufficient.

Use placeholders for unknown:

```text
installation
license
repo URL
package status
runtime requirements
```

Add optional section:

```markdown
## Assumptions to Confirm
```

only when useful.
