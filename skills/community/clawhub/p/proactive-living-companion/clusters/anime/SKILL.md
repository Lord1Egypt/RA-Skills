---
name: anime
version: 1.0.0
trigger: ANIME
---

# Anime — Deutsche Synchro auf Crunchyroll, Netflix, Prime, Disney+

## User Preferences
- **Streaming:** Crunchyroll, Netflix, Prime Video, Disney+
- **Genres:** Action, Adventure, Fantasy, Isekai, Shonen, Comedy, Romance, Slice-of-Life, Drama, Mystery, Psychological, Supernatural, School
- **Dub:** Immer Deutsche Synchro bevorzugen
- **Studio:** Egal
- **Ping:** "Neue Anime-Serien"

## Search Queries
```
"Neue Anime-Serien" "Deutsch synchronisiert" "2026"
"Anime Starttermin" "Crunchyroll" "Deutsch"
"Neuer Anime" "Netflix" "Deutsch" "April 2026"
"Anime auf Deutsch" "Prime Video" "Dub"
"Crunchyroll Neuerscheinungen" "Deutsche Synchro"
```

## Output Template

```
🎬 Neue Anime-Serien auf Deutsch

**TITEL** — (Deutsch)
**OT:** japanischer Titel

Genre: Genre1, Genre2
DE-Start: YYYY-MM | Streaming: Crunchyroll/Netflix/Prime/Disney+
Dub: ✅ Deutsch | Sub: ✅ Japanisch

Kurzinhalt (2-3 Sätze, spoiler-frei):

Für Daniel interessant wegen: [Genre/Ähnlich wie X]:
```

## Filter Rules
1. NUR Deutsche Synchro oder Ankündigung dafür
2. Nur Genres die der User mag
3. Starttermin in den nächsten 1-2 Monaten
4. Max 2-3 Anime pro Ping (nicht überfordern)

## Quality Gates
- Kein Ergebnis gefunden → kein Ping
- Unsichere Info → lieber skip
- Crunchyroll hat fast alles → als Primary Source nutzen
- Bei "Für [USER] interessant" → generisch halten, keinen Namen hardcoden

## Quality Gates
- Kein Ergebnis gefunden → kein Ping
- Unsichere Info → lieber skip
- Crunchyroll hat fast alles → als Primary Source nutzen
