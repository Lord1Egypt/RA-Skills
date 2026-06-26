# Language Tutor Pro — Dashboard Integration Spec

## Overview

The Language Tutor Pro dashboard displays learning progress across all tracked languages. It reads from the skill's local data files and renders charts, stats, and tables on the NormieClaw dashboard.

## Data Flow

```
Agent sessions → data/*.jsonl (raw data)
                      ↓
scripts/export-progress.sh → data/dashboard-export.json (aggregated)
                      ↓
dashboard-kit/manifest.json → Dashboard route /language-tutor
```

### Refresh

Run `bash scripts/export-progress.sh` before loading the dashboard to ensure data is current. The manifest includes a `refresh_command` field that dashboards can invoke automatically.

## Route

**Path:** `/language-tutor`  
**Icon:** 🎓  
**Label:** Language Tutor

## Tables

### lt_sessions
Session history. One row per completed session.
- Source: `data/sessions.jsonl`
- Key columns: date, language, type (conversation/lesson/review/situation), duration, errors corrected, new vocabulary count

### lt_vocabulary
Full vocabulary ledger with spaced repetition state.
- Source: `data/vocabulary.jsonl`
- Key columns: word, translation, language, level, next review date, interval, ease factor, correct streak
- Filter: by language, by review status (due/upcoming/mastered)

### lt_grammar
Grammar rule tracker.
- Source: `data/grammar.jsonl`
- Key columns: rule name, language, level, status (introduced/learning/practiced/mastered), error count, last practiced
- Filter: by language, by status

### lt_progress
Aggregate metrics per language. Derived from `dashboard-export.json`.
- Source: `data/dashboard-export.json` → `learner.languages[]`
- Key columns: language, CEFR level, total vocab, mastered vocab, grammar rules, sessions, minutes, streak, accuracy

## Widgets

### Top Row — Key Stats (3 stat cards)

| Widget | Source | Field | Format |
|--------|--------|-------|--------|
| Current Streak | lt_progress | current_streak | "X days" |
| Words Learned | lt_progress | vocabulary_total | number |
| Grammar Mastered | lt_progress | grammar_mastered | number |

If the learner is studying multiple languages, show stats for the primary (most recent session) language, with a dropdown to switch.

### Charts Row

#### Vocabulary Growth (Line Chart)
- X-axis: Session date
- Y-axis: Cumulative new words added
- One line per language if multiple languages are active
- Source: lt_sessions → cumulative sum of `new_vocab`

#### Session Activity (Bar Chart)
- X-axis: Date (grouped by week)
- Y-axis: Total minutes practiced
- Color-coded by session type (conversation = blue, lesson = green, review = orange, situation = purple)
- Source: lt_sessions

#### Grammar Status (Doughnut Chart)
- Segments: introduced, learning, practiced, mastered
- Colors: gray, yellow, blue, green
- Source: lt_grammar → group by `status`

### Detail Tables

#### Recent Sessions
Last 20 sessions in reverse chronological order.
Columns: Date, Language, Type, Duration, Errors, New Words, Grammar Points.
Clicking a session row shows the full session notes.

#### Vocabulary (Sortable/Filterable)
Full vocabulary list with filters:
- Language dropdown
- Status filter: Due Today, Upcoming (next 7 days), Mastered, All
- Sort by: next review date, ease factor, date added
- Search by word or translation

#### Grammar Rules
All tracked grammar rules with filters:
- Language dropdown
- Status filter: introduced, learning, practiced, mastered
- Sort by: error count (descending), last practiced

## Color Scheme

| Element | Color |
|---------|-------|
| Primary accent | `#6366f1` (indigo) |
| Conversation sessions | `#3b82f6` (blue) |
| Guided lessons | `#22c55e` (green) |
| Vocab reviews | `#f59e0b` (amber) |
| Situation practice | `#a855f7` (purple) |
| Grammar: introduced | `#9ca3af` (gray) |
| Grammar: learning | `#eab308` (yellow) |
| Grammar: practiced | `#3b82f6` (blue) |
| Grammar: mastered | `#22c55e` (green) |
| Error/warning | `#ef4444` (red) |

## Empty States

- **No sessions yet:** "Start your first session by telling your agent 'Let's practice [language]'"
- **No vocabulary:** "Complete a conversation session to start building your word list"
- **No grammar tracked:** "Grammar rules are tracked as you practice — start a conversation or lesson"

## Multi-Language Support

If the learner is studying multiple languages:
- Top-level language switcher (tabs or dropdown)
- All charts and tables filter by selected language
- "All Languages" view shows combined stats with language column visible
