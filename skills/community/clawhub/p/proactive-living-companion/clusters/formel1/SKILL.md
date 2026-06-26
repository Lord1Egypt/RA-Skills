---
name: motorsport_f1
version: 1.0.0
trigger: FORMEL 1, F1
description: Liefert ein schnelles Update zum aktuellen Formel 1 Rennwochenende und WM-Stand.
---

# Formel 1 — Template & Rules

## Purpose
Kompaktes Update zur Formel 1. Fokus auf das aktuelle/nächste Rennen, Sessions und den WM-Kampf.
Maximal 15 Zeilen. Kurz und prägnant.

## Execution Flow

1. Context Check: `date` ausführen.

2. Recherche: Such-Tools mit Query: "Formel 1 nächstes Rennen [Jahr]" ODER "Formel 1 Ergebnisse heute".

3. Generierung: Antwort nach Output-Struktur aufbauen.

## Output-Struktur

### 1. Event-Überschrift
Grand Prix Name + Strecke + Datum
Format: 🏎️ [Land] GP — [Streckenname] | [DD.MM.YYYY]
Fallback wenn Sommerpause: 🏎️ Formel 1 — Aktuell in der Sommerpause.

### 2. Aktueller Status / Nächste Session
Was steht heute/als nächstes an?
Format: Nächste Session: [Session-Name] | [Wochentag], [HH:MM] Uhr MEZ
Alternative: Rennsieger: [Fahrer] ([Team])

### 3. Top 3 Fahrer-WM
Platz, Fahrer, Punkte
Format: 🏆 WM: 1. [Fahrer] [Punkte] | 2. [Fahrer] [Punkte] | 3. [Fahrer] [Punkte]

### 4. Top 3 Konstrukteurs-WM
Platz, Team, Punkte
Format: ⚙️ Teams: 1. [Team] [Punkte] | 2. [Team] [Punkte] | 3. [Team] [Punkte]

### 5. Flash-News / Drama (Optional)
Nur wenn relevant (Strafen, Upgrades, Crashes).
Exakt 1 Satz.
Beispiel: News: Hamilton erhält 5-Plätze Grid-Penalty wegen Motorwechsel.

## Content Rules
- NO HALLUCINATION: Nur verifizierte Daten. Kalender-Änderungen beachten!
- TIMEZONE: Uhrzeiten in MEZ/MESZ umrechnen.
- NO FLUFF: Keine unnötigen Beschreibungen.
- SPRACHE: Deutsch, du-Form.

## Datums-Regel
BEVOR Recherche: `date` ausführen.