# Placeholder Map

When filling templates from interview answers, use this mapping.

## Interview Answer → Placeholder

| Placeholder | Source | Question |
|-------------|--------|----------|
| `{{USER_NAME}}` | User's name | Q1: What should I call you? |
| `{{USER_PRONOUNS}}` | Pronouns if offered | Q1 (optional) |
| `{{USER_EMAIL}}` | Email if offered | Q1 / follow-up |
| `{{USER_TITLE}}` | Job title | Q2: What do you do? |
| `{{USER_COMPANY}}` | Company name | Q2 |
| `{{USER_INDUSTRY}}` | Industry | Q2 |
| `{{USER_COMM_STYLE}}` | Communication preference | Q5: How should your agent talk to you? |
| `{{USER_COMM_PREF_1}}` | First comm rule | Q5 |
| `{{USER_COMM_PREF_2}}` | Second comm rule | Q5 |
| `{{USER_TIMEZONE}}` | IANA timezone | Q8: What's your timezone? |
| `{{USER_NOTES}}` | Any extras from interview | Q1-Q8 |
| `{{AGENT_NAME}}` | Agent name | Q3: What should your agent's name be? |
| `{{AGENT_EMOJI}}` | Agent emoji | Q3 (optional) |
| `{{AGENT_ROLE}}` | One-line role description | Q4: What's the main job? |
| `{{AGENT_PRESENTATION}}` | How the agent presents itself | Q3 + Q5 |
| `{{AGENT_VIBE}}` | Personality in a few words | Q5 |
| `{{SUCCESS_CRITERIA}}` | What "done" means for this agent | Q4 |
| `{{TONE_DESCRIPTION}}` | Paragraph describing tone | Q5 |
| `{{TONE_RULE_1}}` | First tone rule | Q5 |
| `{{TONE_RULE_2}}` | Second tone rule | Q5 |
| `{{TONE_RULE_3}}` | Third tone rule | Q5 |
| `{{GREEN_LIGHT_EXTRAS}}` | Extra autonomous actions | Q6: What should agent never do? (inverse) |
| `{{YELLOW_LIGHT_EXTRAS}}` | Extra notify-then-act | Q6 |
| `{{RED_LIGHT_EXTRAS}}` | Extra ask-first items | Q6 hard limits |
| `{{HEARTBEAT_INTERVAL}}` | e.g. "every 15 minutes" | Q7 + timezone |
| `{{ACTIVE_HOURS_START}}` | e.g. "07:00" | Q7 + timezone |
| `{{ACTIVE_HOURS_END}}` | e.g. "22:00" | Q7 + timezone |

## Defaults When Not Provided

| Placeholder | Default |
|-------------|---------|
| `{{USER_PRONOUNS}}` | omit the line |
| `{{AGENT_EMOJI}}` | ⚡ |
| `{{USER_TIMEZONE}}` | America/New_York |
| `{{HEARTBEAT_INTERVAL}}` | every 15 minutes |
| `{{ACTIVE_HOURS_START}}` | 07:00 |
| `{{ACTIVE_HOURS_END}}` | 22:00 |
| `{{GREEN_LIGHT_EXTRAS}}` | (none) |
| `{{YELLOW_LIGHT_EXTRAS}}` | (none) |
| `{{RED_LIGHT_EXTRAS}}` | (none) |

## Model Recommendation

For new agents with no specific preference, suggest:
- **Main agent:** `anthropic/claude-opus-4-6` (best quality, use Claude MAX if available)
- **Heartbeat:** `anthropic/claude-haiku-4-5` (cheap, fast, sufficient for check-ins)
- **Sub-agents/crons:** `anthropic/claude-sonnet-4-6` (good balance)
- **Fallbacks:** add `hatz/gpt-5.4` and `hatz/anthropic.claude-opus-4-6` to ensure uptime when primary is overloaded

Mention the fallback chain explicitly — new users often hit outages and don't know why the agent went silent.
