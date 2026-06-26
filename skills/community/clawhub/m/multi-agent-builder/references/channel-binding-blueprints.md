# Channel Binding Blueprints

After team creation report, enter post-creation binding stage.
Default path is Single-Bot Mode and should be executed first.

## Mode 1: Single-Bot Mode (recommended default)

### Binding
- Bind one primary bot to `team-leader`.
- Specialist agents remain unbound to IM by default (internal A2A only).
- After user provides channel token/credentials, perform binding automatically.
- User may choose to skip auto-binding and configure manually.

### Usage
- User sends all requests to primary bot.
- Team Leader delegates internally and returns consolidated outputs.

### Suggested group settings
- `groupPolicy`: allow relevant groups only
- `requireMention`: true (reduce accidental triggers)
- `dmPolicy`: allow (for private escalations)

## Mode 2: Multi-Bot Group Mode

This mode assumes all role bots are added into one shared group.

### Binding
- Each key role maps to one bot in the same group.
- `team-leader` remains the only control-plane intake.
- Specialist bots are UI-plane participants (status visibility), not dispatch authority.

### Usage
- User addresses team-leader bot for tasks.
- Team Leader can @ role bots for visibility.
- Real execution trigger must still use A2A dispatch/callback.

### Required group configuration guidance
- `groupPolicy`: allow target group explicitly (whitelist)
- `requireMention`: true (prevent cross-talk/noise)
- `allowFrom` / routing: ensure only intended surfaces can trigger each role
- bot permissions in group: send messages, read mentions, post media if needed
- optional: restrict specialist bots from direct user task intake

### Operational rule
- "@ mention" = visibility signal
- A2A dispatch = execution signal

## User handoff checklist (for both modes)
- [ ] Role-to-bot mapping table confirmed
- [ ] Group/channel IDs confirmed
- [ ] groupPolicy configured
- [ ] requireMention configured
- [ ] activation ping passed per bot
- [ ] end-to-end delegation callback test passed
