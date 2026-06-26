# Autopilot Slash Command Reference v9

Complete command interface with generative, editorial, and narrative commands.

## Command Map

| Command | New? | Description |
|---------|------|-------------|
| `/autopilot` | — | Full mode: historical memory sweep + generative + editorial + creative + inline buttons |
| `/autopilot create [what]` | — | Maximum innovation |
| `/autopilot imagine [what]` | — | Brainstorm only |
| `/autopilot ideas` | v9 | Show generative ideas queue |
| `/autopilot status` | — | Dashboard + all stats + memory sweep status |
| `/autopilot review` | — | Quality + creativity + editorial review |
| `/autopilot propose` | — | Strategic + creative + generative |
| `/autopilot narrative` | v9 | Project narrative arc |
| `/autopilot schedule` | — | All scheduled tasks |
| `/autopilot remember [text]` | — | Persistent memory capture |
| `/autopilot off` | — | Pause |
| `/autopilot turbo` | — | Speed mode |
| `/autopilot learn` | — | Learning report |
| `/autopilot decisions` | — | Decision audit |
| `/autopilot reset` | — | Clear session |

---

## `/autopilot ideas` — Generative Ideas Queue (NEW)

Show all originated ideas with status.

```
─── Ideen-Queue — [N] Ideen ───

💭 1. [Idee]
   Auslöser: [Beobachtung]
   Wert: [Hoch/Mittel]
   Status: ✅ Ausführungsbereit

💭 2. [Idee]
   Auslöser: [Muster]
   Status: ⏳ Wartet auf [Voraussetzung]

💭 3. [Idee]
   Auslöser: [Lücke]
   Status: ⏳ Wartet auf passendes Projekt
```

Auto-action: If items are "Ready", offer to execute #1 immediately.

---

## `/autopilot narrative` — Project Narrative (NEW)

Show the story that connects all project deliverables.

```
─── Projekt-Narrativ: [Name] ───

📖 Act I — Foundation
   [Was etabliert wurde in Sessions 1-2]
   📄 [Deliverable] — [Rolle in der Geschichte]

📖 Act II — Development
   [Was gebaut wurde]
   📄 [Deliverable] — [Rolle]
   📄 [Deliverable] — [Rolle]

📖 Act III — Expansion
   [Was darüber hinaus wuchs]
   📄 [Deliverable] — [Rolle]

Themen:
• [Wiederkehrendes Thema 1]
• [Wiederkehrendes Thema 2]

Narrative-Lücken:
⚠️ [Deliverable] ist nicht mit dem Rest verbunden → Vorschlag: [Brücke]
```

---

## `/autopilot review` — Triple Gate Review

```
🔍 Qualitätsprüfung:
📄 [File]: ✅ Qualität | 🎨 Kreativität ✅ | ✂️ Redaktionell ✅
📄 [File]: ✅ Qualität | 🎨 ⚠️→✅ | ✂️ ⚠️→[Schnitt]→✅

───
Qualität: [N]/[N] | Kreativität: [N]/[N] | Redaktionell: [N] Schnitte
```

---

## `/autopilot propose` — Enhanced Proposals

```
📈 Strategie + Kreativität + Generativ:

1. 🥇 [Strategische Empfehlung]
   💡 Kreativer Ansatz: [Was]
   💭 Generativ: [Was niemand erwähnt hat]
   ✂️ Redaktionell: [Was weglassen]
   ⏱️ [Aufwand] | 🎯 [Wann]

2. 🥈 [Empfehlung]
   💡 [Kreativer Ansatz]
```

---

## `/autopilot learn` — Enhanced Learning Report

```
─── Lernbericht v9 ───

📈 Evolution: [N] | 🛠️ Capabilities: [N] | 📅 Geplant: [N]

🧠 Generative Intelligenz:
  💭 [N] Ideen generiert | [N] ausgeführt | [N] in Queue
  Auslöser: [Top-Muster]

✂️ Editorial:
  [N] Schnitte | Am häufigsten: [Art von Schnitt]

🔮 Alchemie:
  [N] Constraints in Möglichkeiten verwandelt
  Top-Constraint: [Welcher am häufigsten]

🎨 Geschmacksprofil:
  Visuell: [X] | Ton: [X] | Risiko: [X]
  Editorial: [More/Less is more] | Überraschungen: [X]

📖 Projekt-Narrativ: [Status]
```

---

## Natural Language Triggers (Extended)

| Category | Triggers |
|----------|----------|
| Autonomy | "mach mal", "just do it", "handle it", "autopilot" |
| Memory | "merke dir", "erinnere mich" |
| Schedule | "plane das", "remind me" |
| Creative | "sei kreativ", "etwas besonderes", "überrasche mich" |
| Brainstorm | "ideen?", "vorschläge?", "brainstorm" |
| Editorial | "kürzer", "einfacher", "weniger", "auf den Punkt" |
| Narrative | "wie passt das zusammen?", "übersicht", "zusammenhang" |
| Generative | "was fällt dir ein?", "hast du ideen?", "was soll ich machen" |
| Status | "was steht an?", "status" |
