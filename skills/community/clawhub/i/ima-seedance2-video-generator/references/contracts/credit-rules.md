# Credit Rules

This document explains how credit consumption is determined for this skill.

## Rule

Credit is **not** a static configuration value.

It must be derived from the model product list and the matched credit rule for the final parameter combination.

## Source Of Truth

The source of truth is:

- `all_credit_rules` returned by the product list API
- the matched `attribute_id`
- the matched `points` / `credit`

## What Affects Credit

Credit may change based on:

- `task_type`
- `model_id`
- `duration`
- `resolution`
- `aspect_ratio`
- `audio`
- other model-specific parameters returned in `credit_rules.attributes`

## What OpenClaw Must Not Do

OpenClaw must **not**:

- hardcode `credit`
- hardcode `attribute_id`
- infer cost from examples
- reuse a previous task's `attribute_id` for a new parameter combination

## What The Script Must Do

The script must:

1. query product list
2. load `all_credit_rules`
3. merge effective parameters
4. match the correct credit rule
5. set:
   - `parameters[0].attribute_id`
   - `parameters[0].credit`
   - `parameters[0].parameters.cast.attribute_id`
   - `parameters[0].parameters.cast.points`

## Why This Matters

If `attribute_id` and `credit` do not match the final parameter combination, create-task may fail or charge incorrectly.

## Practical Guidance

If the user changes:

- video duration
- resolution
- aspect ratio
- audio setting
- model

then the script must recalculate the matching rule before task creation.
