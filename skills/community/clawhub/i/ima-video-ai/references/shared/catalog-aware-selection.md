# Catalog-Aware Dynamic Model Selection

## Purpose

This document defines the model-selection contract for the natural-language wrapper and any future higher-level orchestration around `ima_runtime_cli.py`.

The goal is to ensure model choice is driven by:

1. user-specified constraints
2. live catalog capabilities
3. user intent semantics

Model choice must not depend on hardcoded parameter-to-model mappings in docs or prompt templates.

## Core Principle

The system must first determine what the user explicitly requires, then determine what the live catalog can actually support, and only then choose a model.

The live catalog is the capability source of truth.

Examples of invalid static reasoning:

- `reference video` always means `ima-pro-fast`
- `quality=1080p` always means one fixed model
- `preview` always means the same low-cost model regardless of current catalog

Examples of valid reasoning:

- the user requires `reference audio`
- the live catalog currently shows which models expose that media capability
- among compatible models, semantic intent can rank speed, cost, and quality

## Source Of Truth

Compatibility checks should use live catalog fields such as:

- `model_id`
- `model_version`
- `model_types`
- `files.acceptType`
- `form_config`
- `credit_rules`
- `attributes`
- default parameter values
- `attribute_id`

Historical behavior, documentation examples, and prior defaults are not sufficient proof that a model currently supports a request.

## Request Understanding

Before selecting a model, separate the request into two signal classes.

### Explicit Constraints

Hard requirements unless the user relaxes them:

- `task_type`
- reference media types: image / video / audio
- `duration`
- `resolution`
- `aspect_ratio`
- audio generation toggle
- explicitly named model or model alias

### Semantic Intent

Soft ranking signals only:

- preview / draft / quick result
- low cost / save credits
- final quality / cinematic / premium
- continuity / reference-driven identity

Semantic intent may rank compatible candidates. It must not override explicit incompatibility.

## Selection Order

Recommended selection order for the natural-language wrapper:

1. explicit model alias in user request
2. live catalog compatibility match for media + structured constraints
3. saved user preference, but only if compatible
4. semantic ranking among remaining compatible models
5. clarification if multiple compatible candidates remain and semantic ranking is unstable

Important:

- explicit preference must not override explicit incompatibility
- saved preference must not override explicit incompatibility
- recommendations must not override explicit incompatibility

## Conflict Handling

If the request explicitly names a model and that model conflicts with the media or parameter constraints:

- do not silently switch
- do not continue with best-effort guessing
- fail clearly

The error should identify:

- the conflicting media or parameters
- the fact that the selected model does not support them according to the live catalog
- the next step: change model, remove the conflicting input, or inspect the live model list

## No-Compatible-Model Handling

If no live model supports the request:

- do not silently fall back
- do not pretend the request is supported
- return a clear error with the unsupported media or parameters

## Insufficient-Evidence Handling

If the live catalog does not expose enough information to prove support:

- do not invent support from memory
- do not falsely claim incompatibility unless catalog evidence exists
- let the structured runtime perform the remaining backend validation where the current contract permits it

## Wrapper Rule

Match explicit user constraints against the live catalog first, use semantic intent only to rank compatible candidates, and fail or clarify when no stable compatible model can be chosen.
