# Principles

## Purpose
Keep `openclaw-consensus` narrow, truthful, and useful.

This repo exists to build a focused OpenClaw-native skill for 2-round cross-model deliberation. Its value comes from bounded workflow, cross-provider comparison, durable artifacts, and clear synthesis — not from pretending to be a magical expert replacement.

## What this project is
- a focused OpenClaw-native deliberation skill
- a bounded 2-round cross-model workflow
- a decision-support tool for costly-to-be-wrong questions
- an artifact-first system that preserves model outputs and final synthesis clearly
- a repo meant to demonstrate OpenClaw's real orchestration edge across providers

## What this project is not
- not a replacement for lawyers, accountants, engineers, doctors, or other experts
- not a legal-advice engine
- not an execution agent
- not an open-ended multi-cycle debate system
- not a web app in MVP
- not a local-model routing platform in MVP
- not a generic “AI swarm” repo

## Core product rules
- the workflow is exactly 2 rounds
- MVP is generic only — no domain modes
- disagreement must be preserved, not flattened away
- uncertainty must be surfaced explicitly
- the final output must separate consensus, disagreement, uncertainty, and escalation points
- boundedness is a feature, not a temporary weakness

## Repo truthfulness rules
- docs must not claim features that do not exist
- examples must not imply expert replacement
- public framing must stay mechanism-first for OpenClaw users
- command docs must reflect the real command surface only
- implementation expansion should follow product proof, not curiosity

## Anti-scope-creep rules
- no domain-specific modes in MVP
- no web UI in MVP
- no browser product shell in MVP
- no local CLI or Ollama routing in MVP
- no execution workflows in MVP
- no third round, dynamic rounds, or convergence loops in MVP
- no feature should be added just because a model occasionally feels uncertain

## Quality bar
- the repo should be explainable in one paragraph
- artifacts should be readable and inspectable by humans
- the final synthesis should help the user decide what is stable and what needs escalation
- prompt complexity should serve clarity, not cleverness
- meaningful disagreement is a valuable output, not a failure mode

## Safety and positioning rules
- consensus increases confidence; it does not create certainty
- disagreement is an escalation signal, not a bug to hide
- the tool may reduce unnecessary expert review in some cases, but must never promise to replace expert judgment
- risky claims such as “if all models agree, you do not need a lawyer” are out of scope for this project

## Expansion rule
Future expansion is allowed only after the MVP is real, understandable, and validated.
Possible later directions may include domain presets, different provider routes, or a broader product shell — but none of those belong in MVP by default.
