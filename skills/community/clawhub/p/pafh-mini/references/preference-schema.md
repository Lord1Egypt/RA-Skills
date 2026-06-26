# Preference Memory Schema Definition

> Defines how preferences are stored, tracked, and retrieved in the PAHF framework

---

## Privacy & Consent

**Before storing any preference**:
- ✅ Confirm significant new preferences with user
- ✅ Log all updates with source and date for transparency
- ❌ Never store sensitive data (passwords, credentials, financial details, health info)

**Write Confirmation Policy**:

| Change Type | Confirmation | Example |
|-------------|--------------|---------|
| New core preference | Yes | "Should I remember you prefer PDF?" |
| Preference update | No (logged) | "Actually I prefer Word now" |
| Daily observation | No | "Noticed you prefer morning meetings" |
| Sensitive data | Never store | Passwords, credentials, etc. |

---

## Preference Entry Format

### Basic Format

```markdown
> **Preference Name**: Preference value [LEARNED: YYYY-MM-DD, source] [UPDATED: YYYY-MM-DD]
> - Detailed description (optional)
> - Example scenarios (optional)
```

### Source Markers

| Source Marker | Description |
|--------------|-------------|
| `[LEARNED: date, explicit instruction]` | User directly stated |
| `[LEARNED: date, user feedback]` | Learned from correction |
| `[LEARNED: date, observation]` | Inferred from behavior patterns |
| `[UPDATED: date]` | Preference has changed |

---

## Preference Category Definitions

### 1. Communication Preferences (communication)

```yaml
category: communication
fields:
  style:
    - concise | detailed | balanced
    - [LEARNED: date, source]
  tone:
    - formal | casual | friendly
  language:
    - primary: zh | en
    - mixed_allowed: boolean
  response_format:
    - markdown | plain_text
    - bullet_points: preferred | neutral | avoid
```

Example:
```markdown
> **Communication Style**: Concise, direct [LEARNED: 2026-02-20, user feedback]
> - Avoid lengthy explanations
> - Prioritize conclusions and action items
```

### 2. Workstyle Preferences (workstyle)

```yaml
category: workstyle
fields:
  time_preference:
    - morning_person | night_owl | flexible
  decision_style:
    - quick | thoughtful | consensus
  priority_framework:
    - urgent_important | custom_rules
  break_pattern:
    - pomodoro | natural | scheduled
```

Example:
```markdown
> **Decision Style**: Thoughtful [LEARNED: 2026-01-15, observation]
> - Important decisions need time to consider
> - Likes to see option comparisons
> [UPDATED: 2026-02-28] Recently prefers faster decision rhythm
```

### 3. Technical Preferences (technical)

```yaml
category: technical
fields:
  formats:
    document: pdf | docx | md
    data: csv | json | xlsx
    image: png | jpg | svg
  tools:
    - preferred_tools: []
    - avoided_tools: []
  code_style:
    - language_preferences: {}
    - commenting: verbose | minimal
```

Example:
```markdown
> **Document Format**: PDF [LEARNED: 2026-03-05, explicit instruction]
> **Code Style**: Python preferred, detailed comments [LEARNED: 2026-02-10, user feedback]
```

### 4. Content Preferences (content)

```yaml
category: content
fields:
  interests:
    - topics: []
    - avoid: []
  depth:
    - overview | detailed | comprehensive
  sources:
    - preferred: []
    - trusted: []
    - avoid: []
  news_focus:
    - frontier_research: boolean
    - papers_breakthroughs: boolean
    - industry_reviews: boolean
```

Example:
```markdown
> **Interest Areas**: AI, tech news, productivity tools [LEARNED: 2026-01-20, observation]
> **Content Depth**: Prefers in-depth analysis over surface news
> **News Focus**: Frontier research, papers, breakthroughs over reviews [LEARNED: 2026-03-06, user feedback]
```

### 5. Personal Settings (personal)

```yaml
category: personal
fields:
  contacts:
    - frequent: [{name, context}]
    - important: [{name, priority}]
  locations:
    - home: string
    - work: string
    - frequent: [{name, address}]
  schedules:
    - daily_routine: {}
    - exceptions: []
```

Example:
```markdown
> **Frequent Contacts**:
> - John (project collaboration) [LEARNED: 2026-02-15, observation]
> - Jane (technical support)
```

---

## Preference Conflict Handling

### Conflict Detection

When multiple relevant preferences are retrieved and may conflict:

```markdown
Detection Process:
1. List all relevant preferences
2. Check timestamps (newest takes priority)
3. Check source weight:
   - Explicit instruction > User feedback > Observation
4. If still uncertain → Pre-action clarification
```

### Conflict Resolution

```markdown
> **Preference A**: Concise replies [LEARNED: 2026-02-20, user feedback]
> **Preference B**: Detailed explanations [LEARNED: 2026-03-03, user feedback]
> 
> ⚠️ Potential conflict detected
> - Recent preference B may reflect temporary need
> - Need to observe subsequent patterns
> - Consider pre-action confirmation
```

---

## Preference Update Rules

### When to Update Long-term Memory (MEMORY.md)

- User explicitly says "always do this from now on"
- Same feedback appears 3+ times
- Preference persists over 2 weeks

**With confirmation**: Ask "Should I remember this for future interactions?"

### When to Only Update Short-term Memory (memory/YYYY-MM-DD.md)

- User says "this time/today"
- Temporary needs
- Patterns under observation

**No confirmation needed**: Daily observations are logged automatically.

### Preference Expiration Handling

```markdown
> **Old Preference**: ... [LEARNED: 2026-01-10] [EXPIRED: 2026-02-15]
> - Reason: User behavior consistently deviates from this preference
> - Replaced by: New preference [LEARNED: 2026-02-20]
```

---

## Preference Retrieval Strategy

### Keyword Mapping

| Task Type | Retrieval Keywords |
|-----------|-------------------|
| Reply message | communication style, language preference |
| Generate report | document format, content depth |
| Schedule | time preference, priority |
| Code task | technical preferences, code style |
| Search information | content preferences, source preferences |
| News briefing | news focus, interests, depth |

### Context-aware Retrieval

```markdown
Consider when retrieving:
1. Current task type
2. Recent interaction history
3. Time context (weekday/weekend, morning/evening)
4. How similar scenarios were handled historically
```

---

## Audit Trail

All preference updates are logged for transparency:

### Change Log Table

```markdown
| Date | Change | Trigger |
|------|--------|---------|
| 2026-03-06 | News focus: frontier research over reviews | user feedback |
| 2026-03-05 | Document format: PDF | explicit instruction |
```

### User Review

Users can inspect their stored preferences at any time:
- `MEMORY.md` - Long-term preferences
- `memory/YYYY-MM-DD.md` - Recent changes
- `memory/users/{user}.md` - User-specific preferences

---

**Remember**: The purpose of preference memory is to reduce ambiguity, not create complexity. When retrieval and processing costs are too high, prioritize pre-action clarification.
