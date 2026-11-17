---
name: poyo-generate-persona
description: Create a reusable music persona on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `generate-persona`, completed music task ids, audio ids, persona names and descriptions, persona_id workflows, callbacks, music detail polling, and consistent follow-up music generation.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/generate-persona","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Generate Persona

## PoYo Links

- Model page: <https://poyo.ai/models/generate-persona>
- API docs: <https://docs.poyo.ai/api-manual/music-series/generate-persona>
- API key page: <https://poyo.ai/dashboard/api-key>

Use this skill to create a reusable music persona from an eligible completed audio track on PoYo. It helps agents validate the prerequisite `task_id` and `audio_id`, write a useful persona name and description, submit the async task, and explain how to retrieve the resulting `persona_id`.

## Use When

- The user mentions Generate Persona, music persona, `generate-persona`, `persona_id`, reusable vocal style, or reusable music style on PoYo.
- The user already has a completed eligible music task and the specific audio track id returned by PoYo.
- The workflow needs async submission, callback guidance, music detail polling, or use of a resulting persona in later music requests.

## Model Selection

- `generate-persona`: create a reusable persona from one eligible audio track.

## Prerequisites

- `task_id` must identify an eligible completed PoYo music task documented for persona creation.
- `audio_id` must identify the specific track from that completed task.
- Each audio track can have only one persona; an existing persona can produce a conflict response.

## Key Inputs

- `input.task_id` is required.
- `input.audio_id` is required.
- `input.name` is required and should clearly identify the reusable musical character.
- `input.description` is required and should describe genre, mood, instrumentation, vocal qualities, and other relevant musical characteristics.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not submit private audio, private task metadata, or confidential style descriptions unless the user trusts PoYo and the callback receiver.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Confirm that the user has the right to process the source audio and create a reusable persona from it.

## Execution

- Read `references/api.md` for endpoint details, prerequisites, request fields, examples, conflict handling, and result retrieval notes.
- Use `scripts/submit_generate_persona.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt the example from `references/api.md`.
- After submission, report the returned `task_id` clearly; retrieve the result through the documented music detail endpoint or wait for the webhook.

## Output Expectations

When helping with Generate Persona, include:

- selected model id
- prerequisite source `task_id` and `audio_id` status
- final payload or concise parameter summary
- persona name and description summary
- returned task id if a request was submitted
- next step: poll music detail or wait for webhook
- resulting `persona_id` when available
