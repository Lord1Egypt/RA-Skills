# GLSL Encyclopedia Workflow

## Core stance

Use the authoritative GLSL specification/docs plus local observed shader/project state together.

Default order:
1. check `.GLSL-Encyclopedia/` cache/notes
2. check official GLSL docs when needed
3. inspect live shader/project state
4. answer or act
5. record durable learnings

## When docs lookup is mandatory

Do a docs lookup before answering or acting when any of these are true:
- the user asks about GLSL syntax, qualifiers, built-ins, type rules, layout/interface behavior, or stage restrictions
- the task involves shader source review, compile errors, interface matching, uniforms/buffers/samplers/images, or version/extension behavior
- the task involves a version-sensitive feature or behavior you are not highly confident about
- the task involves live authoring/review guidance and the exact language rule boundaries matter

## Cache-first rule

Before fetching docs, check whether the needed material already exists under:
- `.GLSL-Encyclopedia/docs/docs.vulkan.org/glsl/latest/...`
- `.GLSL-Encyclopedia/notes/components/...`
- `.GLSL-Encyclopedia/notes/patterns/...`
- `.GLSL-Encyclopedia/inventory/...`

If the local cache is good enough, use it.
If not, fetch/check the official docs and then cache what you used.

## How to cache docs

Use `scripts/cache_doc.py`.

Typical usage:

```bash
python3 scripts/cache_doc.py   --url 'https://docs.vulkan.org/glsl/latest/chapters/variables.html'   --root '<workspace>/.GLSL-Encyclopedia'
```

The script will:
- fetch the page
- convert it into a normalized markdown-ish cache file
- place it under `.GLSL-Encyclopedia/docs/docs.vulkan.org/glsl/latest/...`
- add metadata such as source URL and fetch timestamp

## How to store local knowledge

### Component notes

Use `.GLSL-Encyclopedia/notes/components/<component-name>.md` for:
- shader-stage or subsystem purpose
- sensitive language/interface boundaries
- discovered quirks

### Pattern notes

Use `.GLSL-Encyclopedia/notes/patterns/<topic>.md` for:
- recurring layout/interface patterns
- repeated compile/debugging gotchas
- version/extension conventions
- project-specific shader design conventions

### Inventory files

Use `.GLSL-Encyclopedia/inventory/` for:
- project/access inventory
- shader architecture/runtime layout
- documentation index

## Distinguish evidence types

When writing notes, label information mentally as one of:
- **Authoritative docs** — from the GLSL specification/docs
- **Observed local state** — from live shader/project inspection
- **Inference/recommendation** — your judgment based on docs + local state

Do not blur these together.

## Recommended answer style

When it helps, mention whether your answer is based on:
- cached official docs
- freshly checked official docs
- live shader/project inspection
- best-practice inference

## High-sensitivity areas

Treat these as high-sensitivity even when you have live access:
- stage interface matching
- layout qualifiers and memory-layout assumptions
- built-in variable/function semantics
- version and extension gating
- compiler-error interpretation that could mislead shader design

For these, prefer docs lookup even if you think you remember the rule.
