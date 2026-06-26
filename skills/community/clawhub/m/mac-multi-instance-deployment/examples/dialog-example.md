# Example Dialogue

## User

I want a generic Mac multi-instance layout for an OpenClaw-style workspace.

## Assistant

Use `main` for routing and shared indexes, `workbench` for active work,
`publish` for release bundles, `archive` for snapshots, and `private` for
secrets and runtime state.

## User

What should I do first?

## Assistant

Copy `config/local-multi-instance.example.env` into a private location, replace
the placeholder paths, then review `references/instances.md` before running
`./validate_repo.sh`.

