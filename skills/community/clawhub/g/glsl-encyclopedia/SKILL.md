---
name: glsl-encyclopedia
description: >-
  GLSL language/specification workflow for GLSL-specific questions, shader
  authoring and review, exact syntax and semantic lookup, built-in and
  qualifier reference, interface/layout reasoning, stage-specific behavior
  checks, version/extension rules, and compiler-error triage when the actual
  language layer is GLSL. Use when the request is clearly about GLSL itself:
  GLSL/OpenGL Shading Language syntax, shader source using `#version`,
  `layout(...)`, `in`/`out`, `uniform`, `buffer`, samplers/images,
  built-in variables/functions, interface blocks, stage-specific shader code,
  or `glslangValidator`/GLSL compiler errors in a GLSL context. Do not use
  for HLSL, WGSL, MSL, Slang, SPIR-V assembly, generic rendering questions,
  or Vulkan API/spec questions unless the language layer being debugged or
  discussed is specifically GLSL.
metadata: {"openclaw":{"emoji":"🎨","homepage":"https://docs.vulkan.org/glsl/latest/index.html"}}
---

# GLSL Encyclopedia

## Overview

Use a docs-first workflow for GLSL work. Prefer the official GLSL language/specification docs at `https://docs.vulkan.org/glsl/latest/index.html`, consult cached local copies under `.GLSL-Encyclopedia/` before re-fetching, and record useful authoritative excerpts plus environment-specific operational learnings so future work gets faster, safer, and more grounded.

This skill is for the **GLSL language/spec layer**. It should trigger for real GLSL syntax/semantic/interface questions, not for generic rendering talk and not for Vulkan API questions unless the actual issue is specifically about GLSL shader source.

## Workflow

1. **Classify the task**
   - Decide whether the task is a GLSL language question, shader-authoring task, shader-review task, compiler-error/debugging task, stage-specific behavior question, or cross-language translation/comparison task where GLSL is one side.
   - Use this skill when the task materially depends on GLSL syntax, qualifiers, types, built-ins, interface/layout rules, stage rules, preprocessor/version behavior, or shader authoring semantics.
   - Do not use this skill for generic rendering concepts, generic Vulkan API debugging, or non-GLSL shader languages unless the GLSL language layer is actually in play.

2. **Check local cache first**
   - Use `.GLSL-Encyclopedia/` as the local knowledge/cache root.
   - Check these locations first when relevant:
     - `.GLSL-Encyclopedia/docs/docs.vulkan.org/glsl/latest/...`
     - `.GLSL-Encyclopedia/notes/components/...`
     - `.GLSL-Encyclopedia/notes/patterns/...`
     - `.GLSL-Encyclopedia/inventory/...`
   - If a cached page or note already answers the question well enough, use it.

3. **Consult authoritative GLSL docs before answering or acting**
   - Before answering direct or indirect GLSL questions that depend on exact syntax, qualifier behavior, type rules, stage restrictions, built-in variable/function semantics, layout/interface rules, or version-sensitive details, consult the official GLSL docs unless the answer is already well-supported by the local cache.
   - Before performing non-trivial GLSL shader review or authoring guidance, consult the relevant docs first when:
     - exact language syntax or legal combinations matter
     - stage-specific behavior or interface matching is easy to misremember
     - the task involves compile errors, layout rules, extension/version behavior, or built-in semantics
   - If the problem is really about Vulkan API object behavior, synchronization, descriptors, swapchains, or VUID-driven valid-usage rules rather than GLSL language semantics, prefer the Vulkan skill instead of stretching this one.
   - Do not improvise fragile GLSL answers from memory when the docs are easy to check.

4. **Cache consulted docs locally**
   - When you consult a GLSL docs page, save a normalized cache copy under `.GLSL-Encyclopedia/docs/docs.vulkan.org/glsl/latest/...`.
   - Mirror the official docs path structure as much as practical.
   - Cache only pages actually consulted; do not try to mirror the whole GLSL spec eagerly.
   - Use `scripts/cache_doc.py` when appropriate.

5. **Separate authoritative documentation from local observations**
   - Store official-doc-derived material under `.GLSL-Encyclopedia/docs/...`.
   - Store environment-specific operational knowledge under:
     - `.GLSL-Encyclopedia/notes/components/`
     - `.GLSL-Encyclopedia/notes/patterns/`
     - `.GLSL-Encyclopedia/inventory/`
   - Distinguish clearly between:
     - authoritative documented behavior
     - observed project/environment shader conventions
     - inferred best-practice guidance

6. **Record useful local learnings**
   - After useful live work, save durable notes such as:
     - project-specific shader conventions
     - recurring compile/validation-error patterns
     - stage-interface or layout gotchas
     - version/extension adoption decisions
     - safe/unsafe operational boundaries for the codebase or environment
   - Prefer concise durable notes over re-learning the same GLSL details later.

## Live Work Rules

- Treat authoritative GLSL docs lookup as the default preflight for non-trivial GLSL work.
- Prefer read/inspect first when entering unfamiliar shader code.
- Treat stage interfaces, layout qualifiers, buffer/image/sampler usage, preprocessor/version behavior, built-in semantics, and compiler-error interpretation as higher-sensitivity areas.
- When uncertainty remains after checking cache + docs, say so and avoid bluffing.
- When answering a question, mention when useful whether the answer comes from cached official docs, a fresh official docs lookup, or live observed shader/project state.

## Data Root

Use this workspace-local root for cache and notes:

- `.GLSL-Encyclopedia/`

Expected structure:

- `.GLSL-Encyclopedia/docs/docs.vulkan.org/glsl/latest/...`
- `.GLSL-Encyclopedia/notes/components/...`
- `.GLSL-Encyclopedia/notes/patterns/...`
- `.GLSL-Encyclopedia/inventory/...`

Use `scripts/init_workspace.py` to create or repair the expected directory structure.

## Note Destinations

- Component-specific observations → `.GLSL-Encyclopedia/notes/components/<component-name>.md`
- Reusable GLSL patterns/gotchas → `.GLSL-Encyclopedia/notes/patterns/<topic>.md`
- Environment-wide shader/access info → `.GLSL-Encyclopedia/inventory/*.md`
- Cached official docs → `.GLSL-Encyclopedia/docs/docs.vulkan.org/glsl/latest/...`

## Secrets / Sensitive Data

- Do not store plaintext credentials, API keys, session tokens, private URLs, recovery codes, or other secrets in the encyclopedia notes/inventory tree.
- If a note needs to mention access details, keep it high-level and redact or omit secret material.
- Treat these workspace notes as operational memory, not as a secrets vault.

## Resources

- `scripts/init_workspace.py` — create or repair the `.GLSL-Encyclopedia/` directory tree.
- `scripts/cache_doc.py` — fetch and cache a consulted official GLSL docs page under `.GLSL-Encyclopedia/docs/...`.
- `references/workflow.md` — detailed operating workflow and evidence-handling rules.
- `references/cache-layout.md` — canonical `.GLSL-Encyclopedia/` directory structure.
- `references/topic-map.md` — useful GLSL topic groupings for faster authoritative lookup.

## Good Outcomes

- Answer a GLSL question using cached or freshly checked official docs instead of guesswork.
- Inspect GLSL shader code after checking the relevant docs and record any new project-specific language or convention knowledge.
- Build a growing local GLSL knowledge cache that makes later work faster, safer, and more grounded.
- Turn one-off GLSL discoveries into durable notes so future work does not rediscover them from scratch.

## Avoid

- Answering GLSL-specific questions purely from memory when the docs are easy to consult.
- Treating local project shader conventions as if they were guaranteed authoritative GLSL behavior.
- Dumping large amounts of low-value docs into the workspace without a reason.
- Writing project-specific observations into the official-doc cache tree.
- Confusing generic Vulkan API questions with GLSL language questions when the actual issue is not about GLSL itself.
