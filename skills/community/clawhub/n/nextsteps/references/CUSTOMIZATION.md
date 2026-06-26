# User Customization Protocol

## Configurable Properties

| Property | Type | Default | Valid Range | Description |
|----------|------|---------|-------------|-------------|
| enabled | bool | true | true/false | Master switch for NextSteps |
| display-count | int | 5 | 1–7 | Number of suggestions shown |
| min-count | int | 1 | 1–3 | Minimum suggestions (error recovery) |
| max-count | int | 7 | 5–10 | Maximum allowed suggestions |
| preferred-categories | list | [all] | category names | Categories to prioritize |
| excluded-categories | list | [] | category names | Categories to never show |
| format | string | standard | standard/compact | Display format |
| show-footer | bool | true | true/false | Show the NextSteps footer |
| include-backlog | bool | true | true/false | Include backlog items in suggestions |
| include-lateral | bool | true | true/false | Include lateral-jump suggestions |

## Explicit Customization — Intent Detection

Detect these 9 patterns as customization requests:

1. **Count change**: "show me 3 next steps" / "give me more suggestions" / "fewer suggestions please"
2. **Category preference**: "more deep-dive suggestions" / "I like the actionable tasks"
3. **Category exclusion**: "don't show me lateral suggestions" / "skip the creative ones"
4. **Format change**: "use compact format" / "number the suggestions" / "shorter suggestions"
5. **Enable/disable**: "turn off next steps" / "disable suggestions" / "stop showing suggestions"
6. **Re-enable**: "turn next steps back on" / "enable suggestions again"
7. **Backlog toggle**: "don't include backlog items" / "stop showing backlog"
8. **Footer toggle**: "hide the footer" / "don't show the tip at the bottom"
9. **Reset**: "reset my next steps preferences" / "go back to defaults"

## Write-Confirm-Apply Flow

When a customization intent is detected:

### Step 1 — Parse
Extract the property and desired value from the user's message.

### Step 2 — Validate
Check that the value is within valid range (see table above). If invalid:
- Respond: "I can set display-count between 1 and 7. Want me to set it to [closest valid value]?"
- Do NOT silently clamp or ignore.

### Step 3 — Confirm
Before writing, confirm with the user:
- Single property: "I'll update your NextSteps preference: `display-count` → 3. Sound good?"
- Multiple properties: List all changes and confirm once.

### Step 4 — Apply
After confirmation:
1. Update the value in `.nextsteps/PREFERENCES.md`
2. Log `[CONFIG-CHANGE] property: display-count, old: 5, new: 3` in HISTORY.md
3. Acknowledge: "Done — I'll show 3 suggestions from now on."

### Step 5 — Immediate Effect
Apply the change to the very next set of suggestions (same response if possible, otherwise next response).

## Implicit Learning (No Confirmation Needed)

### Count Learning
Three signals indicate implicit count preference:
1. User consistently selects from only the first N suggestions → hypothesis: user wants N
2. User asks for more detail on suggestion N+1 (beyond visible set) → user wants more
3. User scrolls/interacts with all suggestions → current count is appropriate

See SELF-IMPROVE.md for confidence levels and when to auto-adjust vs suggest.

### Category Learning
Four rules for implicit category preference:
1. 3+ selections of category X in 10 entries → promote to STRONG
2. 0 selections of category X in 15 entries → demote one tier
3. New topic appears 3+ times in user conversations → add to Topic Affinities as MODERATE
4. Topic not mentioned for 30+ entries → demote from STRONG to MODERATE (never below MODERATE for learned topics)

These adjustments happen silently. They are logged in HISTORY.md but do not require user confirmation.

## Disable/Enable Protocol

### Disabling
When user says "turn off next steps" or similar:
1. Set `enabled: false` in PREFERENCES.md
2. Log `[DISABLED]` in HISTORY.md
3. Respond: "NextSteps disabled. Say 'enable next steps' anytime to turn them back on."
4. Stop appending suggestions to responses immediately.
5. STILL maintain BACKLOG.md if topics are mentioned (passive collection).

### Re-enabling
When user says "enable next steps" or similar:
1. Set `enabled: true` in PREFERENCES.md
2. Log `[ENABLED]` in HISTORY.md
3. Respond: "NextSteps re-enabled!" and immediately append suggestions.
4. On re-enable, generate fresh suggestions from current context (not stale pre-disable state).

## Negative Feedback Handling

When user expresses dissatisfaction with suggestions:
- "these suggestions aren't helpful" → trigger immediate self-diagnostic (see SELF-IMPROVE.md)
- "stop suggesting X" → add X to `ignored-topics` in PREFERENCES.md, confirm
- "I already know how to do X" → add X to `ignored-topics`, promote more novel categories
- "too basic" / "too advanced" → note in Topic Affinities as complexity hint, adjust suggestion depth accordingly

## Reset Protocol

When user requests a reset:
1. Confirm: "This will reset all NextSteps preferences to defaults. Your history will be preserved. Continue?"
2. After confirmation, replace `## User Configuration` section with defaults
3. Reset all category preferences to MODERATE
4. Clear `ignored-topics` and `ignored-types`
5. Log `[CONFIG-CHANGE] property: all, old: custom, new: defaults`
6. Keep HISTORY.md and BACKLOG.md intact — only preferences are reset
