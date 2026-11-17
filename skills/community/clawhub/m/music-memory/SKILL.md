---
name: music-memory
description: A practice journal that actually remembers the music — recordings, chord progressions, technique work, and lesson notes stored with full musical context in BlueColumn. Use when tracking guitar/music practice, coaching students, or recalling what was played, how it went, and what to drill next. Requires a BlueColumn API key (bc_live_*).
---

# Music Memory — BlueColumn Skill

Most agents treat a practice recording like any other audio file. This skill treats it like a musician does: the take matters, but so does the key it was in, the chords underneath it, the technique being worked, and what the coach said about it. Store all of it together and recall becomes musical — "show me every take where the barre chords buzzed" just works.

## Store a take with its musical context

Send the recording URL plus a structured context block. The audio gets transcribed; the context gets embedded alongside it, so recall sees both.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-remember \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "audio_url": "https://example.com/week3-take2.mp3",
    "text": "MUSIC CONTEXT — Instrument: acoustic-steel | Key: A minor | Tempo: 92 BPM | Techniques: barre-chords, hammer-on | Chord progression: Am → F → C → G | Notes: Student still buzzing the B string on the F barre during transitions. Ring finger anchoring helped.",
    "title": "Week 3 practice take 2 — Am F C G, Sep 7"
  }'
```

No recording? Notation and lesson summaries work the same way — put the chord map and technique focus in the text block.

## Recall like a coach

The filters are semantic, not rigid. Ask in music terms:

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-recall \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "What problems keep showing up in barre chord transitions? (instrument: acoustic-steel; techniques: barre-chords)"}'
```

Useful recall patterns:
- Progress check: "How has the bend accuracy changed over the last month of takes?"
- Set-list prep: "Which songs in E minor have we practiced and how did the last run-through go?"
- Technique coverage: "What techniques have we NOT touched in the last two weeks?"

## Log the small stuff fast

Quick observations between takes — use a note instead of a full session:

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-note \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Capo 2 fixed the F#m buzz — student prefers lighter gauge strings on the dreadnought."}'
```

## Coach workflow

1. Before a lesson: recall the student's recent takes and open issues.
2. During: log each take with technique tags and one-line notes.
3. After: recall the session, extract what improved and what to drill, and store it as the next session's plan.

## MCP shortcut

If your agent runs the `bluecolumn-mcp` server (npm: `bluecolumn-mcp`), the same flow is two tool calls: `music_remember` (typed fields for instrument, key, tempo, techniques, chords, notes) and `music_recall` (query + instrument/technique/style filters). The REST examples above are the equivalent wire format.
