# Public README Release Cleanup Contract

## Purpose

This contract defines the final release shape for GitHub README output.

It applies after the README draft has already passed public positioning, markdown cleanliness, and human voice checks.

## Applies When

Use when the user asks for:

```text
final README
publishable README
GitHub README
launch-ready README
README for public release
```

## Required Final Shape

A publishable README may include:

```markdown
# Project Name

> One-line value proposition.

Intro paragraph.

## What It Is

## Who It's For

## Try It / Example Usage

## How It Works

## Installation

## Project Structure

## Status

## Contributing

## License
```

But exact section order may vary depending on project type.

## Required Release Conditions

Before delivery, verify:

```text
language matches user request
public name is safe or risk is flagged
first screen communicates user value
no UI artifacts
no private notes inside artifact
no unconfirmed license
no fake install command
project path is accurate
architecture is below user value
claims are bounded
```

## Project Structure Rule

Use named skill directory:

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

Do not show:

```text
skills/
├── skill.md
```

unless that is truly the repo root structure.

## Notes Separation Rule

If notes are needed, output them after the README under:

```text
Notes for you, not for publication:
```

The notes must not be inside the README.

## Public Link Rule

Only include official public links if they are confirmed.

If not confirmed, use neutral language:

```text
Designed for OpenClaw-compatible skill runtimes.
```

instead of linked claims.

## Installation Placeholder Rule

Use placeholders for unknown repo, org, package, or install command.

Good:

```bash
git clone https://github.com/<your-org>/<repo-name>.git
```

Bad:

```bash
clawhub install <project>
```

unless verified.

## License Rule

If license is unknown:

```text
TBD
```

Do not assume MIT, Apache-2.0, or any other license.

## Claim Boundary Wording Rule

For general-purpose creative/communication tools, do not write overly absolute claim rules.

Preferred wording:

```text
For source-grounded work, factual claims stay tied to known material. If the source has gaps, the output names them instead of filling them with speculation.
```

## Failure Modes

Hard fail:

1. README requires cleanup before publishing.
2. Private notes mixed into artifact.
3. Incorrect path structure.
4. Unverified public link or affiliation.
5. License assumed.
6. Install command invented.
7. UI residue remains.

Soft fail:

1. Claim boundary too broad.
2. Structure too internal.
3. Project status vague.
4. Notes separated but language mismatched.

## Final Rule

A release-ready README should be clean enough to paste and bounded enough to trust.
