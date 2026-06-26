---
name: motorsport_wec
version: 1.0.0
trigger: WEC, LE MANS, ENDURANCE
description: Update zur FIA World Endurance Championship mit Fokus auf die Hypercar-Klasse.
---

# WEC (World Endurance Championship) — Template & Rules

## Purpose
Faktenbasiertes Update zur WEC. Fokus auf Hypercar-Klasse.
Maximal 15 Zeilen. Harte Fakten.

## Execution Flow

1. Context Check: `date` ermitteln.

2. Recherche: Such-Tools: "WEC FIA World Endurance Championship news race [Jahr]" ODER "WEC Ergebnisse [Datum]".

3. Generierung: Antwortstruktur strikt befolgen.

## Output-Struktur

### 1. Event-Überschrift
Renn-Name (Dauer) + Ort
Format: ⏱️ [Rennen, z.B. 6 Hours of Spa / 24h Le Mans] — [Datum]

### 2. Status / Hypercar Fokus
Ist das Rennen live, kommend oder beendet?

Live: 🔴 LIVE (Stunde [X]/[Y]): Führender Hypercar: #[Nummer] [Team/Hersteller]
Beendet: 🏁 Sieger: #[Nummer] [Team/Hersteller] (Hypercar)
Kommend: Nächstes Rennen startet am [Wochentag] um [HH:MM] Uhr MEZ.

### 3. Hypercar WM-Stand (Hersteller)
Top 3 Hersteller
Format: 🏆 Hypercar-WM: 1. [Hersteller] [Punkte] | 2. [Hersteller] [Punkte] | 3. [Hersteller] [Punkte]

### 4. LMGT3 Klasse (Quick Mention)
Kurzer Hinweis auf LMGT3.
Format: GT3-Fokus: [Führendes/Siegreiches Team in LMGT3] vorne.

### 5. Besonderheit
Exakt 1 Satz zu Ausfällen, BoP-Änderungen oder Crashes.
Beispiel: Porsche #6 nach 4 Stunden wegen technischem Defekt ausgeschieden.

## Content Rules
- CLASS FOCUS: Immer primär auf "Hypercar" konzentrieren.
- CAR NUMBERS: Autonummer angeben (z.B. Toyota #7, Porsche #6).
- NO FLUFF: Keine epischen Renngeschichten, nur harte Fakten.
- SPRACHE: Deutsch, du-Form.

## Datums-Regel
BEVOR Recherche: `date` ausführen.