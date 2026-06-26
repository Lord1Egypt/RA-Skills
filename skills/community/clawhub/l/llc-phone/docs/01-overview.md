# 01 — Model Overview & Selection Notes

This document intentionally distinguishes between current vendor-doc facts and
field observations. Use OpenAI's current model pages as the source of truth for
availability, pricing, and hard limits.

## The Realtime API model family

| Model | Status | Best for |
|---|---|---|
| `gpt-realtime-1.5` | OpenAI flagship voice model | Best default when call quality and capability matter most |
| `gpt-realtime-mini` | Lower-cost realtime model | High-volume or cost-sensitive voice workloads |
| `gpt-realtime` | Legacy / older realtime family | Existing stacks that already depend on it |
| `gpt-4o-realtime` | Older realtime family | Validate carefully before using for new builds |

**Default choice in this skill: `gpt-realtime-1.5`.**

Choose `gpt-realtime-mini` when cost or scale matters more than top-end voice
quality and reasoning performance. Choose `gpt-realtime-1.5` when you want the
strongest default capability envelope.

## Practitioner notes (non-authoritative)

The items below come from current practitioner reports and research gathered on
2026-04-02. They are useful for planning and testing, but they are not vendor
guarantees:

- `gpt-realtime-1.5` is generally the safer default for production voice-agent
  work.
- `gpt-realtime-mini` is worth evaluating when cost is a primary constraint.
- Long-session behavior, tool-use smoothness, and perceived voice naturalness
  should all be tested in your own stack before rollout.

## When to use `gpt-realtime-mini`

- You expect high call volume and need lower per-call cost.
- The workflow is narrow enough that reduced capability is acceptable.
- You can benchmark your prompts, tools, and latency targets before launch.

## Watch later

- Re-check OpenAI's model pages before each publish or major production change.
- Re-benchmark if you switch between `gpt-realtime-1.5`, `gpt-realtime-mini`,
  or older realtime families.
