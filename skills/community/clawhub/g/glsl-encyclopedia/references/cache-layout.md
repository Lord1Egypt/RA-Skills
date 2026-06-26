# `.GLSL-Encyclopedia/` Cache Layout

Use this directory as the workspace-local data root for the skill.

## Directory tree

```text
.GLSL-Encyclopedia/
  docs/
    docs.vulkan.org/
      glsl/
        latest/
          ... cached official GLSL docs pages ...
  notes/
    components/
      ... per-component notes ...
    patterns/
      ... reusable GLSL notes ...
  inventory/
    access.md
    topology.md
    doc-index.md
```

## Placement rules

### `docs/`
Store cached copies of authoritative GLSL docs here.

Mirror the official docs path as much as practical.
Example:

```text
https://docs.vulkan.org/glsl/latest/chapters/variables.html
->
.GLSL-Encyclopedia/docs/docs.vulkan.org/glsl/latest/chapters/variables.md
```

### `notes/components/`
Store environment- or project-specific component notes here.

Suggested filenames:
- `vertex-stage.md`
- `fragment-stage.md`
- `compute-stage.md`
- `interfaces.md`
- `buffers-and-images.md`

### `notes/patterns/`
Store reusable operational notes here.

Examples:
- `layout-qualifiers.md`
- `interface-matching.md`
- `compiler-error-triage.md`
- `version-extension-gotchas.md`

### `inventory/`
Store environment-wide inventories here.

Suggested files:
- `access.md`
- `topology.md`
- `doc-index.md`

## Cache philosophy

Do not mirror the whole docs site eagerly.
Cache only the pages you actually consulted and expect to be useful later.
