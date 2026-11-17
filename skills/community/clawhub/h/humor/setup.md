# Setup — Humor

Read this on first use to load the learned humor state. Do not interview the user — asking someone how they like their jokes is itself a failed joke.

## How To Load State

1. Read `~/Clawic/data/humor/config.yaml` if it exists. Apply its values.
2. For anything absent, use the defaults in the Configuration table of `SKILL.md` — do not ask.
   - `humor_ceiling: bold`, `probe_rate: 1`, `cooldown_messages: 3`, `emoji_policy: mirror`, `off_limits_topics: none`.
3. Read `~/Clawic/data/humor/profile.md` for the learned profile (Works, Fails, Intensity, Contexts, Signals). If Works is non-empty you may skip cold start, but still open at subtle (`feedback.md` Maintenance).
4. Absence of any file is fine; create from `memory-template.md` on the first humor event, and proceed silently.

## Recording Preferences (only when the user declares one)

Write to config **only** when the user states a preference in the course of conversation — never as a questionnaire.

- "Tone it down" / "less jokes" → lower `humor_ceiling` one step. "You can be funnier" → raise it one step (earned intensity still gates below it).
- "Stop joking" / "just be professional" → `humor_ceiling: off`. This is a success state, not a failure (`feedback.md` Anti-Gaming).
- "Never joke about X" → append X to `off_limits_topics`; permanent until they revoke.
- "No emojis" → `emoji_policy: never`.
- A standing context flag ("this project is serious", "the team channel is casual") → record under the Contexts preference area.

If the user has said nothing, store nothing.

## What the Data Folder Holds

See `memory-template.md` for formats: `profile.md` (learned taste), `history.md` (attempts log, 30-entry cap), `callbacks.md` (running jokes), `wins.md` (verbatim hits). Observed patterns go to the profile; declared preferences go to config — an observation never overwrites a declared preference without the user's confirmation.
