# 🧠 Social Knowledge — Rules & Patterns
## When to activate
Read this file when:
- Updating skills/proaktiv/social_knowledge.json
- Processing calendar events or emails (morning briefing)
- Generating a ping that mentions a person by name
## Extraction Rules (after EVERY user reply, silently)
Scan the last 50 messages for social signals in DE and EN:
**Meetings**
- DE: "Treffen mit [Name]", "Termin mit [Name]", "Gespräch mit [Name]"
- EN: "meeting with [Name]", "appointment with [Name]", "call with [Name]"
**Birthdays**
- DE: "Geburtstag von [Name]", "[Name] hat Geburtstag"
- EN: "[Name]'s birthday", "birthday of [Name]"
**Preferences**
- DE: "[Name] mag/liebt/hasst [X]"
- EN: "[Name] likes/loves/hates/enjoys [X]"
**Relationships**
- DE: "mein Freund/meine Kollegin/mein Chef [Name]"
- EN: "my friend/my colleague/my boss [Name]"
## Write Rules
Update skills/proaktiv/social_knowledge.json:
```json
{"people": {"[Name]": {"key_facts": [{"fact": "...", "value": "..."}], "last_updated": "..."}}}
```
- Only add NEW facts — never overwrite existing ones
- Do this SILENTLY — never mention it to the user
- Skip if no new signals found
## Calendar + Mail Context
When processing calendar events or emails:
1. Check social_knowledge.json for known people in the event/mail
2. Use key_facts to personalize the ping message
3. Birthday reminder: 2 days in advance if person is in social_knowledge
4. Unknown person → write normally, never invent facts
