# license-mismatch-audit

Controlled benign Skill fixture for testing whether skill platforms accept frontmatter-only license metadata.

## What is being tested?

- `SKILL.md` declares `license: Apache-2.0`
- No bundled `LICENSE` file is provided

## What should a scanner report?

A scanner that only validates frontmatter syntax may pass this Skill. A scanner that performs repository consistency checks may warn that the declared license cannot be verified from repository files.

## Safety scope

This Skill contains:

- no executable scripts
- no network instructions
- no credential access
- no install hooks
- no prompt injection payload

It is intended for defensive validation research only.
