---
name: ai_audio_suno
version: 1.0.0
trigger: SUNO, SUNOAI, AI MUSIC
description: Liefert News zu Suno AI Updates und bietet eine optimale Prompt-Struktur für Musikgenerierung.
---

# Suno AI — Template & Rules

## Purpose
Zwei Ziele:
1. Kurzes Update zu neuen Suno-Versionen/Features
2. Optimaler Copy-Paste-Prompt für Musikgenerierung
Maximal 15 Zeilen.

## Execution Flow

1. Recherche: Such-Tools mit Query: "Suno AI latest update release notes [Monat/Jahr]".

2. Strukturierung: Aktuellste Versionsnummer und neue Features extrahieren.

3. Generierung: Antwort aufbauen.

## Output-Struktur

### 1. Aktuelle Version & Status
Aktuellste Suno-Version und wichtigstes Feature.
Format: 🎵 Suno Status: Aktuelle Version [vX.X] | Top-Feature: [Neues Feature]

### 2. News / Update Flash
1-2 Bulletpoints mit neuesten Entwicklungen.
Format: - [News 1]
- [News 2]
Falls keine News: Keine größeren Updates in den letzten 4 Wochen.

### 3. Prompting Pro-Tipp (Randomisiert)
Kurzer, technischer Tipp für bessere Suno-Ergebnisse.
Format: 💡 Pro-Tipp: Nutze Meta-Tags wie [Pre-Chorus] oder [Guitar Solo] im Textfeld.

### 4. Blueprint (Copy & Paste Vorlage)
Gerüst zum Befüllen:

Style of Music: [Genre1, Genre2, Tempo, Mood, Vokalart]
Lyrics-Struktur:
[Intro]
[Verse 1]
[Chorus]
[Outro]

## Content Rules
- NO HALLUCINATION: Keine Versionen erfinden.
- STYLE TAGS: Suno arbeitet mit Tags besser als mit ganzen Sätzen.
- COMPACT: Keine langen Erklärungen. Nur News + Tools.
- SPRACHE: Deutsch, du-Form.

## Datums-Regel
BEVOR Recherche: `date` ausführen.