# Catalog-Aware Dynamic Model Selection

## 1. Purpose

This document defines the formal model-selection contract for image generation requests in this repo.

The goal is to ensure that model choice is driven by:

1. user-specified constraints
2. live catalog capabilities
3. user intent semantics

Model selection must not depend on hardcoded parameter-to-model mappings in documentation or prompt templates.

## 2. Core Principle

The runtime must first determine what the user explicitly requires, then determine what the live catalog can actually support, and only then choose a model.

The live catalog is the capability source of truth.

Examples of invalid static reasoning:

- `512px` always means model X
- logo requests always mean model Y
- preview requests always mean model Z

Examples of valid reasoning:

- the user requires `size=512px`
- the live catalog currently shows which models can satisfy `size=512px`
- among compatible models, semantic intent can help rank speed, cost, and quality

## 3. Source Of Truth

The runtime must use live catalog data as the authoritative source for compatibility checks.

Relevant catalog fields include:

- `model_id`
- `model_version`
- `form_config`
- `credit_rules`
- `attributes`
- default parameter values
- `attribute_id`

Historical behavior, documentation examples, and prior defaults are not sufficient proof that a model currently supports a parameter combination.

## 4. Request Understanding

Before selecting a model, the runtime must extract two categories of signal from the request.

### 4.1 Explicit Constraints

These are hard requirements unless the user later relaxes them:

- task type: `text_to_image` or `image_to_image`
- size: `512px`, `1k`, `2k`, `4k`, etc.
- aspect ratio: `1:1`, `16:9`, `9:16`, etc.
- output count: `n`
- quality and similar structured controls
- explicitly named model or model alias
- reference-image requirement

### 4.2 Semantic Intent

These are soft ranking signals and must not override explicit constraints:

- preview / draft / quick result
- low cost / save credits
- final quality / high fidelity / print
- poster / thumbnail / logo / product photo / style transfer
- speed-first vs quality-first vs cost-first

## 5. Constraint Matching

If the request contains explicit model-related constraints such as `size`, `aspect_ratio`, `n`, or `quality`, the runtime must attempt live catalog compatibility matching before defaulting to a preferred or recommended model.

Compatibility rules:

- if the live catalog explicitly supports the requested constraint combination, the model is compatible
- if the live catalog explicitly conflicts with the requested constraint combination, the model is incompatible
- if the live catalog provides insufficient evidence, the runtime must not claim compatibility as fact

Constraint compatibility is stronger than default preference.

## 6. Selection Order

Recommended model-selection order:

1. explicit `--model-id`
2. prompt-inferred model alias
3. live catalog compatibility match for explicit structured constraints
4. saved user preference, but only if compatible
5. recommended default model

Important:

- user preference must not override explicit incompatibility
- recommended defaults must not override explicit incompatibility
- semantic intent only ranks compatible candidates; it does not bypass constraints

## 7. Ranking Among Compatible Models

If multiple models are compatible with the explicit constraints, the runtime may rank them using semantic intent.

Examples:

- preview / draft / low-cost intent: prefer lower-credit compatible models
- final-quality intent: prefer stronger quality-oriented compatible models
- image-to-image continuity intent: prefer compatible models suited to reference-based editing

This ranking must remain dynamic and catalog-aware. It must not become a hidden static map.

## 8. Conflict Handling

If the user explicitly specifies a model and that model conflicts with the requested constraints:

- do not silently switch models
- do not continue with best-effort guessing
- fail clearly and explain the conflict

Recommended response shape:

- identify the conflicting parameters
- state that the selected model does not support them according to the live catalog
- suggest changing the model, removing the conflicting parameter, or inspecting the live model list

If a prompt-inferred model alias conflicts with explicit constraints:

- do not force the inferred model
- fail clearly and ask the user to adjust the prompt or parameters

## 9. No-Compatible-Model Handling

If no live catalog model supports the requested constraint combination:

- do not silently fall back to a default model
- do not pretend the request is supported
- return a clear user-facing error

The error should include:

- the parameters that could not be matched
- the fact that no live model currently supports them
- a suggestion to inspect the live model list or adjust the prompt/parameters

## 10. Insufficient-Evidence Handling

If the live catalog does not expose enough information to confidently match a parameter:

- do not invent support from documentation memory
- do not falsely claim incompatibility unless the catalog provides evidence
- use the existing runtime fallback behavior if the system contract allows backend validation to decide later

In other words:

- explicit evidence of incompatibility should block
- lack of evidence alone should not automatically block

## 11. Persistence Rule

Auto-selected compatibility matches are operational decisions, not long-term preferences.

The runtime must not write them back as persistent user defaults unless:

- the user explicitly chose the model, or
- product rules explicitly require auto-selections to become preferences

## 12. Post-Result Validation And Recovery

The runtime must treat backend task completion and user-facing success as different states.

Backend completion means:

- task creation succeeded
- polling reached a successful media state
- a result URL was returned

User-facing success additionally requires:

- the output actually satisfies the user's explicit constraints such as `aspect_ratio` or `size`

If backend completion succeeds but output validation fails:

- do not silently return the invalid result as success
- do not pretend the request was fulfilled

Recovery policy:

- if the user explicitly forced `--model-id`, do not auto-switch; fail clearly
- if the model was auto-selected or prompt-inferred, the runtime may retry with the next compatible live-catalog model
- retry candidates must come from the same live compatibility set used for initial selection
- if every compatible candidate fails output validation, fail clearly and report the attempted compatible models

## 13. Example

Request:

`生成一张 512px 的快速预览图：简约的咖啡店 Logo`

Correct interpretation:

- task type: `text_to_image`
- explicit constraint: `size=512px`
- semantic intent: preview, quick iteration, low-cost tendency, logo draft

Correct selection behavior:

1. inspect the live catalog
2. filter models using `size=512px` compatibility evidence
3. rank compatible models using preview / low-cost intent
4. choose the best compatible live model
5. if no compatible model exists, fail clearly instead of falling back to an incompatible default

Incorrect behavior:

- always use the recommended default model
- always use the saved preference regardless of compatibility
- hardcode `512px -> Nano Banana 2`
- silently switch away from a user-specified incompatible model

## 14. One-Sentence Rule

Match explicit user constraints against the live catalog first, use semantic intent only to rank compatible candidates, and fail clearly when no compatible model can be reliably chosen.
