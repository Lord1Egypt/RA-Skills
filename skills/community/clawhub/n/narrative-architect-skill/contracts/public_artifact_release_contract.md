# Public Artifact Release Contract

## Purpose

This contract governs the final shape of public-facing artifacts.

It applies after the artifact has already been drafted.

It ensures the final answer is release-ready.

## Applies When

The user asks to publish, launch, release, or put content on:

```text
GitHub
website
landing page
public repository
open-source marketplace
documentation site
product page
social platform
public announcement
```

## Default Behavior

If the user asks for a publishable artifact, output the artifact directly.

Do not output internal analysis unless requested.

Do not mix assistant advice into the artifact.

If advice is necessary, put it after the artifact under:

```text
Notes for you, not for publication:
```

## Public README Structure

Default structure:

```markdown
# Project Name

One-line value proposition.

## What It Is

## Who It Is For

## What It Helps You Do

## Example Usage

## How It Works

## Installation

## Project Status

## Contributing

## License
```

Optional later sections:

```markdown
## Runtime Modes
## Project Structure
## Architecture
## Roadmap
## FAQ
```

Architecture must not appear before user value.

## First Screen Rule

The first screen should not contain:

```text
full file tree
full runtime chain
all harness names
internal development history
long methodology exposition
third-party author dependency
```

The first screen should contain:

```text
project name
one-line value
what it helps users do
who it is for
```

## Public Naming Rule

For public release, avoid names that imply unofficial affiliation with:

```text
authors
books
companies
frameworks
public figures
third-party platforms
```

If user insists on such a name, add a non-affiliation disclaimer or recommend a neutral public name.

## Internal Name vs Public Name

A project may have:

```text
internal_name
public_name
```

Example:

```yaml
internal_name: Robert Skill
public_name: Narrative Architect Skill
```

Public artifacts should use the public name by default.

Internal names may appear only if the user requests internal documentation.

## External Reference Rule

Avoid public wording like:

```text
Built on [famous book / famous person / company].
```

Prefer:

```text
Inspired by classic principles of [domain].
```

If naming a third party is unavoidable, use:

```text
This project is not affiliated with [third party].
```

## File Tree Rule

If included, keep file tree short and approximate.

Do not list every file unless:

```text
the user asks for architecture docs
the repo is specifically for contributors
the section is clearly marked as technical reference
```

Use:

```text
Project Structure
```

not:

```text
Full Internal File Tree
```

## Count Stability Rule

Avoid exact internal counts unless verified at render time.

Bad:

```text
17 harnesses
10 mappers
6 policies
```

Better:

```text
a set of mappers
quality harnesses
output contracts
regression cases
```

## Notes Rule

Assistant-side guidance should be outside the artifact.

Acceptable:

```text
Notes for you, not for publication:
- Replace <your-org> before publishing.
- Confirm the license before release.
```

Not acceptable inside artifact body:

```text
Before publishing, replace...
I used this name because...
```

unless the README has an intentional "Maintainer Notes" section.

## Final Release Checklist

Before final output:

```text
language matches request
public name is safe or risk is flagged
first screen shows user value
Markdown is clean
no UI residue
no fake install commands
license confirmed or TBD
architecture below the fold
notes separated
claims bounded
```

## Failure Modes

Hard fail:

1. Public artifact contains UI residue.
2. Artifact language mismatches request.
3. Public README starts with internal architecture.
4. Artifact implies unofficial third-party affiliation.
5. Installation or license is invented.
6. Notes are mixed into publishable artifact.
7. Project name is risky and unflagged.

Soft fail:

1. Too much architecture.
2. Too few usage examples.
3. Public value is vague.
4. README is usable but not inviting.
5. First screen is too abstract.

## Final Rule

Public artifacts should be written for strangers, not for the internal team.
