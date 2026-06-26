# Routing Example

Use the instance roles like this:

- `main`: system entry, routing rules, shared indexes
- `workbench`: active local work and short-lived experiments
- `publish`: public-safe release packaging
- `archive`: long-term snapshots and read-only reference material
- `private`: secrets, runtime state, and local-only notes

If a doc or file is meant for the public repo, keep it out of `private`.
If a file is meant for a specific run, keep it out of `publish`.

