# Migration for Existing Setups

Use this file when preflight shows the user already has OpenClaw agents, bindings, Feishu accounts, or older multi-agent experiments.

## Goal

Add the new wizard-managed setup with the least possible disruption.

## Default migration stance

Always prefer:

- add, do not replace
- patch minimally
- preserve existing working parts
- back up before editing

Do not assume old config is wrong just because it looks complex.

## What counts as an existing setup

Treat the setup as existing if you see any of these:

- multiple agents already present
- non-empty `bindings`
- non-empty `channels.feishu`
- custom workspaces
- evidence of prior channel routing

## Safe migration order

1. read current config
2. summarize what already exists in plain language
3. back it up
4. choose new IDs and names that do not collide
5. make one small addition first
6. verify before restart
7. restart only if needed
8. verify again after restart
9. only then add the next piece

## Safe wording for existing users

Good examples:

- "You already have 3 agents. I’ll leave them alone and only add the new ones."
- "You already have Feishu settings. I’ll reuse what still works and only add the missing accounts or bindings."
- "I found older bindings. I will not replace them unless you ask me to."
- "Let’s add one new assistant first, make sure it works, and then we can add the next one."

## Collision handling

If an agent ID already exists:

- create a new safe ID instead of reusing it blindly
- explain the new ID simply if needed

If a Feishu account key already exists:

- inspect whether it is already tied to a working bot
- if uncertain, do not overwrite it
- create a new account key for the wizard flow

## When to stop and ask

Pause and ask a short question only if:

- replacing an existing binding would change current user-facing behavior
- reusing an old Feishu account would be ambiguous
- the user appears to have an intentionally customized multi-agent setup

## What not to do

- do not wipe `bindings`
- do not delete old agents
- do not replace all of `channels.feishu`
- do not silently convert private-chat routing to group routing
- do not claim success without verifying the old setup still looks intact
