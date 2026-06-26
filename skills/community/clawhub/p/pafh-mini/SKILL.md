---
name: pahf
description: |
  PAHF (Personalized Agents from Human Feedback) - Continual Personalization Framework.
  
  Triggered when applying the PAHF three-step loop:
  (1) Pre-action Clarification - Resolve ambiguity before action, proactively ask for confirmation
  (2) Preference-grounded Action - Retrieve user preferences from memory to guide decisions
  (3) Post-action Feedback Integration - Collect feedback after action, update preference memory
  
  Use when:
  - User expresses preferences or habits
  - Need to make decisions with multiple valid options
  - User corrects or adjusts your behavior
  - Need to remember personalized settings
  - Detecting potential preference changes

dependencies:
  tools:
    - memory_search
    - memory_get
  files:
    read:
      - MEMORY.md
      - memory/YYYY-MM-DD.md
      - USER.md
      - IDENTITY.md
    write:
      - MEMORY.md
      - memory/YYYY-MM-DD.md
      - memory/users/{user}.md

privacy:
  - Reads and writes to local preference memory files
  - May access personal/identity data (USER.md, IDENTITY.md)
  - Requires user consent for persistent preference storage
  - All preference updates are logged with source and date

consent:
  required: true
  scope: |
    This skill will:
    - Read your preference memory files (MEMORY.md, USER.md, etc.)
    - Write preference updates to these files
    - Track preference changes over time
    
    Your preferences will be stored locally in ~/.openclaw/workspace/memory/
---

# PAHF - Continual Personalization Framework

> Based on paper "Learning Personalized Agents from Human Feedback" (arXiv:2602.16173)

## ⚠️ Privacy & Consent Notice

**Before using this skill**, understand that PAHF will:

| Action | Files | Data Type |
|--------|-------|-----------|
| **Read** | MEMORY.md, USER.md, IDENTITY.md, memory/*.md | Preferences, identity, personal info |
| **Write** | MEMORY.md, memory/YYYY-MM-DD.md, memory/users/*.md | Preference updates, change logs |

**All preference updates are**:
- Logged with `[LEARNED: date, source]` marker
- Tracked in Preference Change Log table
- Stored locally in `~/.openclaw/workspace/memory/`

**User consent is required** for persistent preference storage. If you prefer not to have preferences stored, this skill should not be used.

---

## Core Philosophy

**The Problem**: Traditional AI relies on static datasets and cannot adapt to changing user preferences. You correct it once, it makes the same mistake again.

**The Solution**: PAHF enables continual personalization through dual feedback channels + explicit memory:
- 🎯 **Pre-action Clarification**: Ask when uncertain, don't guess
- 💾 **Preference Memory**: Explicitly store user preferences, not implicit encoding
- 🔄 **Post-action Feedback**: Every feedback is a learning opportunity

---

## Dependencies

This skill requires the following tools to be available:

| Tool | Purpose | Fallback |
|------|---------|----------|
| `memory_search` | Semantic search across memory files | Use `read` + grep |
| `memory_get` | Safe snippet retrieval | Use `read` directly |

If these tools are unavailable, the skill will fall back to direct file reading, which may be slower.

---

## The PAHF Loop (Three Steps)

### Step 1: Pre-action Clarification

**When to Ask**:
- Task has multiple reasonable options (e.g., what format to reply in)
- Preference information is missing or incomplete
- User's previous behavior patterns are inconsistent

**How to Ask**:
```
❌ Wrong: Silently guess and get it wrong
✅ Right: Briefly list options, let user confirm

Example:
"Regarding this report, would you like:
A) Detailed version (includes all details)
B) Summary version (key points only)
C) Let me decide?"
```

**When NOT to Ask**:
- Task is urgent and obvious
- Clear preference is already recorded
- Asking would disrupt the flow

### Step 2: Preference-grounded Action

**Retrieve Preferences**: Find relevant preferences from memory files

**Memory File Locations**:
- `MEMORY.md` - Long-term preferences, core values
- `memory/YYYY-MM-DD.md` - Recent preference changes
- `USER.md` - Basic user information
- `IDENTITY.md` - Your identity settings
- `memory/users/{user}.md` - User-specific preferences

**Retrieval Method**:
1. **Preferred**: Use `memory_search` tool to search keywords
2. **Fallback**: Use `memory_get` for safe snippet retrieval
3. **Manual**: Read relevant files directly

**When No Preference Found**:
- Use reasonable defaults
- Record this decision for future adjustment

### Step 3: Post-action Feedback Integration

**Identify Feedback**:
- Direct correction: "No, I wanted..."
- Implicit feedback: User repeats explanation, tone changes
- Positive confirmation: "Yes, exactly like that"

**Update Memory** (with confirmation for significant changes):
```
# Feedback Type Judgment
if user explicitly corrects:
    This is an important preference → Update MEMORY.md
    Ask: "Should I remember this for future interactions?"
    
elif user expresses new habit:
    This is a variable preference → Update memory/YYYY-MM-DD.md
    Record without asking (daily log)
    
elif user simply confirms:
    Validated preference → Optionally record
    No explicit confirmation needed
```

**Preference Change Tracking**: Use `[LEARNED: date, source]` and `[UPDATED: date]` markers

---

## Write Confirmation Policy

To balance personalization with user control:

| Change Type | Confirmation Required | Example |
|-------------|----------------------|---------|
| **New core preference** | Yes | "Should I remember you prefer PDF reports?" |
| **Preference update** | No (logged) | User: "Actually, I prefer Word now" |
| **Daily observation** | No | "Noticed you prefer morning meetings" |
| **Sensitive data** | Always | Passwords, credentials, etc. (never store) |

**Sensitive data is NEVER stored**:
- ❌ Passwords, API keys, tokens
- ❌ Financial details (account numbers, etc.)
- ❌ Health information
- ❌ Any data explicitly marked as sensitive

---

## Preference Memory Structure

See [references/preference-schema.md](references/preference-schema.md)

### Core Fields

```markdown
## Preference Categories

### Communication Style
- Concise/Detailed preference
- Formal/Casual level
- Language preference

### Work Habits
- Time scheduling
- Priority judgment
- Decision style

### Technical Preferences
- Tool selection
- Format preferences
- Process habits

### Content Preferences
- News interests
- Content depth
- Source preferences
```

---

## Practical Examples

### Example 1: Learning New Preference

```
User: "From now on, always send reports in PDF format"

PAHF Response:
1. Pre-action: ✓ Clear instruction, no clarification needed
2. Retrieve: Check MEMORY.md → No such preference recorded
3. Execute: Confirm receipt, update with consent

Agent: "Got it! I'll remember to send reports in PDF format. This preference has been saved to your profile."

Update MEMORY.md:
> **Report Format**: PDF [LEARNED: 2026-03-05, explicit instruction]
```

### Example 2: Handling Ambiguity

```
User: "Help me organize these files"

PAHF Response:
1. Pre-action: Detected ambiguity
   - Organize by what? Date/Type/Project?
   - Output format? List/Table/Report?
   
2. Ask:
   "To organize these files, I need to know:
   - How to organize? (Date/Type/Project)
   - Output format? (List/Table)"
   
User: "By date, in table format"

3. Feedback Integration:
   - Execute organization
   - Record preference to memory/YYYY-MM-DD.md
   - No confirmation needed (daily observation)
```

### Example 3: Preference Drift Detection

```
Historical Preference (MEMORY.md):
> **Communication Style**: Concise, direct [LEARNED: 2026-02-20]

Recent Change (memory/2026-03-03.md):
> User emphasized wanting detailed explanations today

PAHF Behavior:
1. Detected preference conflict
2. Use recent preference (detailed)
3. Observe subsequent feedback
4. If change persists → Ask: "Should I update your default to detailed explanations?"
5. If confirmed → Update long-term preference with [UPDATED: date]
```

---

## Importance of Dual Feedback Channels

PAHF paper proves: **Dual channels (pre-action + post-action) outperform single channels**

| Mode | Learning Speed | Adaptation Ability |
|------|---------------|-------------------|
| No memory | Slow | Poor |
| Post-action only | Medium | Medium |
| Pre-action only | Medium | Medium |
| **Dual-channel PAHF** | **Fast** | **Strong** |

**Why Dual Channels Work**:
- Pre-action: Proactively avoid errors, clarify intent
- Post-action: Capture implicit preferences, adapt to changes

---

## Best Practices

### ✅ Good Practices

1. **Layered Preference Storage**
   - Core preferences → MEMORY.md (stable)
   - Recent changes → memory/YYYY-MM-DD.md (dynamic)
   - User-specific → memory/users/{user}.md

2. **Regular Review**
   - Check for preference conflicts during heartbeat
   - Identify preference drift trends

3. **Explicitly Record Sources**
   ```markdown
   > **Preference**: Concise replies [LEARNED: 2026-02-20, user feedback]
   > **Preference**: PDF format [LEARNED: 2026-03-05, explicit instruction]
   ```

4. **Ask Before Storing Sensitive Preferences**
   - When in doubt, ask for confirmation
   - Never store credentials or secrets

### ❌ Practices to Avoid

1. **Don't Implicitly Assume**: Ask if uncertain
2. **Don't Over-record**: Recording every detail creates noise
3. **Don't Ignore Changes**: "This time is different" is an important signal
4. **Don't Store Without Consent**: Ask for significant new preferences

---

## Integration with Existing Memory System

PAHF enhances rather than replaces existing memory system:

| File | Original Purpose | PAHF Enhancement |
|------|-----------------|------------------|
| MEMORY.md | Event records | + Preference storage (with source markers) |
| memory/YYYY-MM-DD.md | Daily logs | + Preference change tracking |
| USER.md | User information | + Basic preferences |
| memory/users/{user}.md | User records | + PAHF preference format |
| HEARTBEAT.md | Periodic checks | + Preference consistency checks |

---

## Audit & Transparency

All preference updates are logged and traceable:

1. **Source Marker**: Every preference has `[LEARNED: date, source]`
2. **Change Log**: Preference Change Log table tracks all changes
3. **Date Stamps**: `[UPDATED: date]` for modifications
4. **User Review**: Users can inspect memory files at any time

To review your stored preferences:
```
Read MEMORY.md for long-term preferences
Read memory/YYYY-MM-DD.md for recent changes
Read memory/users/{your-name}.md for user-specific preferences
```

---

Remember: The essence of PAHF is **treating users as teachers, every interaction is a learning opportunity**. Ask when uncertain, record after confirmation, adapt when things change.
