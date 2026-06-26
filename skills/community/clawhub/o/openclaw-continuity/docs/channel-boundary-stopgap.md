# Channel Boundary Stopgap

This document covers the **channel boundary stopgap** for two classes of outbound
leakage that the public skill alone cannot fully stop:

1. `<final> ... </final>` tags appearing in user-visible output
2. heartbeat/internal narration reaching outbound delivery

These are **host integration** concerns. They are not part of the public
skill's portable logic, but a host using this skill should wire a final
outbound defense.

## What belongs in the public skill

The skill may:

- reduce meta / narration in model-facing output
- keep runtime-context structured
- strip obvious internal wording during generation

The skill should **not** own:

- channel-specific outbound interception
- gateway runtime persistence behavior
- platform-specific delivery routing
- language-specific personal preferences such as Simplified→Traditional rewrite

## Recommended channel boundary stopgap

At the host layer, add a final outbound guard with these behaviors:

1. Strip `<final>` wrappers before outbound send
2. Strip heartbeat narration prefixes such as:
   - `This is another heartbeat poll...`
   - `Looking at the autoseed output...`
   - `Still no response...`
3. Keep the final message short and frontstage-safe
4. Apply the same logic to:
   - `message_sending`
   - heartbeat delivery persistence (for example `lastHeartbeatText`)

## Why this is outside the skill core

The skill runs during generation, but heartbeat delivery and final outbound
payloads may be resolved later by gateway/runtime code. If the host does not
intercept the final payload, raw narration can still leak even when the skill
already cleaned the generated text.

## Minimum validation

For a new host, verify all of the following:

1. `message_sending` fires on outbound delivery
2. `<final>` does not appear in the user-visible message
3. heartbeat/internal narration does not appear in the user-visible message
4. persisted heartbeat text (for example `lastHeartbeatText`) matches the final
   delivered text, not the raw pre-sanitize narration

## Release note

This stopgap is included as **boundary guidance**, not as a public skill promise.
The public package is allowed to ship the guidance and validation steps without
claiming it can guarantee all host frontstage safety by itself.
