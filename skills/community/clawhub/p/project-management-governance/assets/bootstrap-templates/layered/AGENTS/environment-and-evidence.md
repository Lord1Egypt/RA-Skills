# Environment And Evidence

> Last Updated: {{DATE}}
> Status: Draft

## Environment Boundaries

Always distinguish:
- local development
- test or staging
- production or target environments
- external services and remote platforms

Do not silently mix paths, credentials, settings, or runtime assumptions across environments.

## Evidence Rules

Before debugging or risky changes, collect evidence such as:
- file layout
- configs
- logs and stack traces
- sample inputs and outputs
- interface contracts
- dependency state

Do not present a guess as a confirmed cause.
