---
name: meta-skill
description: "Trajectory compiler that converts real OpenClaw session traces (or raw_trajectory_log) into a parameterized, reusable Skill via 4 stages: trace interception → DAG abstraction → schema+code synthesis → registration."
---

# Meta‑Skill — Trajectory Compiler

## Overview
Compile a concrete, parameter-filled execution trace into a reusable Skill with dynamic inputs. This skill implements a **4‑stage closed‑loop pipeline**:
1) Trace Interception → 2) DAG Abstraction → 3) Schema+Code Synthesis → 4) Registration.

## Stage 1 — Trace Interception (implemented)
Use `scripts/trace-from-session.js` to generate a **real trace** from OpenClaw session JSONL, or `scripts/trace-interceptor.js` for JSONL tool event streams.

## Stage 2 — DAG Construction & Abstraction (implemented)
Use `scripts/trajectory-compiler.js` to build a DAG and lift variables to inputs.

## Stage 3 — Code & Schema Synthesis (implemented)
Compiler emits `references/schema.json`, `references/plan.json`, `references/run-flow.md`, and `scripts/run.js`.

## Stage 4 — Registration & Hot Reload (implemented)
Compiler writes into the Skills directory and requires a skills refresh.

## Usage
See `references/pipeline.md` and `references/compiler-spec.md`.
