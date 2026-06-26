# Hub Execution

This skill should execute through the Maliang Hub / Nano backend.

## Execution surfaces

Use backend capability endpoints for:
- writing
- image generation/editing
- voice generation
- BGM generation
- video generation
- composed transforms

Use backend project endpoints for:
- list projects
- create project
- project summary
- workspace link
- director run orchestration

Use task polling for long-running work:
- image
- video
- heavy project phases

## Persistence rule

- `one-shot`: `persist.mode = "none"`
- `project`: `persist.mode = "project"`

## Canonical state rule

For project work, cloud project state is canonical.
Local skill state is convenience only.
