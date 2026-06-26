# Security model

## Sensitivity

OpenAI OAuth switching is a credential-adjacent workflow.

Even when the skill does not expose raw secrets in normal output, the surrounding runtime may contain:

- OAuth access / refresh material
- JWT-like tokens
- callback payloads
- account identifiers
- usage and attribution logs
- rollback backups

## Public-skill security rules

A publishable ClawHub skill must not bundle:

- `auth-profile.json`
- live `skill-data/state/*`
- backup copies of `auth-profiles.json`
- OAuth callback files
- OAuth session files
- cached runtime probes from a real machine
- token ledgers from a real machine
- `__pycache__`
- machine-specific secrets or credentials

## Design rule

The public skill provides:

- workflow guidance
- compatibility checks
- path discovery
- packaging policy
- safe release scaffolding

The public skill does not serve as a dump of one operator machine's runtime state.

## Publication gate

If any credential-bearing files are present in the publication source tree, publication must stop until the tree is sanitized.
