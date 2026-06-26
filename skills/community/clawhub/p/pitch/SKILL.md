---
name: pitch-pro
description: Pitch development and presentation coaching for founders and salespeople. Use when user mentions investor pitches, sales presentations, elevator pitches, pitch decks, or persuasion scenarios. Builds value propositions, crafts pitches for different audiences, prepares for objections, and coaches delivery. All work is advisory - human judgment required for all decisions.
---

# Pitch

Pitch development system. From first principles to closed deals.

## Critical Privacy & Safety

### Data Storage (CRITICAL)
- **All pitch materials stored locally only**: `memory/pitch/`
- **No external sharing** of business plans or strategies
- **No integration** with presentation or email systems
- User controls all data retention and deletion

### Safety Boundaries (NON-NEGOTIABLE)
- ✅ Build value propositions and pitch narratives
- ✅ Generate questions and objection handlers
- ✅ Draft follow-up communications
- ✅ Coach on delivery and presentation
- ❌ **NEVER guarantee** funding or sales success
- ❌ **NEVER make business decisions** for the user
- ❌ **NEVER replace** human judgment in deals
- ❌ **NEVER share** confidential business information

## Quick Start

### Data Storage Setup
Pitch materials stored in your local workspace:
- `memory/pitch/pitches.json` - Pitch versions and content
- `memory/pitch/audiences.json` - Audience profiles
- `memory/pitch/objections.json` - Common objections and responses
- `memory/pitch/meetings.json` - Meeting notes and outcomes

Use provided scripts in `scripts/` for all data operations.

## Core Workflows

### Build Foundation
```
User: "Help me build my pitch foundation"
→ Use scripts/build_foundation.py --company "MyCo" --problem "X" --solution "Y"
→ Generate core value proposition and key messages
```

### Create Elevator Pitch
```
User: "Create a 60-second pitch for investors"
→ Use scripts/create_elevator_pitch.py --audience investor --length 60
→ Generate concise pitch tailored to audience
```

### Prepare for Objections
```
User: "What questions will investors ask?"
→ Use scripts/prep_objections.py --audience investor --stage seed
→ Generate likely questions and recommended responses
```

### Draft Follow-Up
```
User: "Draft follow-up email after the pitch"
→ Use scripts/draft_followup.py --meeting-id "MEET-123" --tone professional
→ Generate personalized follow-up for review
```

### Practice Delivery
```
User: "Coach me on my pitch delivery"
→ Use scripts/coach_delivery.py --pitch-id "PITCH-456"
→ Provide feedback on structure, clarity, and persuasion
```

## Module Reference

For detailed implementation:
- **Foundation Building**: See [references/foundation.md](references/foundation.md)
- **Elevator Pitches**: See [references/elevator-pitches.md](references/elevator-pitches.md)
- **Objection Handling**: See [references/objections.md](references/objections.md)
- **Audience Tailoring**: See [references/audiences.md](references/audiences.md)
- **Follow-Up Strategy**: See [references/follow-up.md](references/follow-up.md)
- **Delivery Coaching**: See [references/delivery.md](references/delivery.md)

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `build_foundation.py` | Develop core pitch elements |
| `create_elevator_pitch.py` | Generate 30/60/120-second pitches |
| `prep_objections.py` | Prepare for likely questions |
| `draft_followup.py` | Create meeting follow-ups |
| `coach_delivery.py` | Provide delivery feedback |
| `save_meeting_notes.py` | Log pitch outcomes |
| `generate_deck_outline.py` | Create pitch deck structure |
| `analyze_pitch.py` | Review pitch for gaps |

## Disclaimer

This skill provides pitch coaching and preparation support only. Success in fundraising or sales depends on many factors beyond pitch quality. No guarantee of outcomes is implied or provided.
