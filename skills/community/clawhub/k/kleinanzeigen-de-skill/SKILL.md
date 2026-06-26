---
name: kleinanzeigen-de-skill
description: >
  Erstelle und verwalte Verkaufsanzeigen speziell auf kleinanzeigen.de.
  Verwende diesen Skill wenn der Human sagt, er will etwas auf kleinanzeigen.de verkaufen,
  eine Anzeige erstellen, oder wenn "kleinanzeigen" im Gespräch fällt.
  Nicht für Käufe oder Interessenten-Kommunikation, nicht für andere Plattformen.
---

# Kleinanzeigen Helper

## Workflow

### 1. Produkt erfragen
Wenn der Human sagt, er will etwas verkaufen, frage nach:
- **Produktname** (genaue Bezeichnung / Modell)
- **Zustand** (wie neu, sehr gut, gut, gebraucht, mit Gebrauchsspuren)
- **Zubehör** (originales Zubehör, Ladegerät, Karton, etc.)
- **Mängel** (Kratzer, Dellen, funktionale Einschränkungen)
- **Standort** (für Abholung, ggf. PLZ)
- **Versand** (ja/nein, ggf. Kosten)
- **Fotos**: Frage ob der Human Fotos hat. Falls nein: suche lizenzfreie Produktbilder von Wikimedia Commons (upload.wikimedia.org) oder offiziellen Hersteller-Presseseiten. Verwende keine Bilder von Amazon oder kommerziellen Händlerseiten – diese sind urheberrechtlich geschützt.

### 2. Preisrecherche
Siehe `references/pricing.md`.

### 3. Preisvorschlag + Freigabe
- Präsentiere dem Human den vorgeschlagenen Preis mit Begründung
- Warte auf Freigabe oder Korrektur

### 4. Beschreibung generieren
- Vermeide generische Floskeln
- Erwähne Zustand, Zubehör, Mängel ehrlich
- Gib relevante technische Details an
- Halte sie sachlich und vollständig
- Format: Fließtext mit Absätzen, ca. 5-10 Sätze
- Keine Preise oder Versandkosten in der Beschreibung nennen (nur im Preisfeld)
- Bezahlmethoden wie PayPal/Überweisung erwähnen

### 5. Browser-Automation zum Einstellen
Nach Freigabe von Text + Preis:

1. Starte Browser und navigiere zu "kleinanzeigen.de"
2. Frage den Human nach E-Mail + Passwort für den Login
3. Gib die Anmeldedaten ein
4. **SMS-Code**: Der Human gibt den Code, sobald er per SMS ankommt. Warte auf ihn.
5. Navigiere zu "Anzeige aufgeben" / "einstellen"
6. Gib den Titel ein, damit die Kategorie automatisch erkannt wird, und wähle sie aus
7. Wähle bei Bedarf die passende Kategorie aus (siehe `references/categories.md`)
8. Fülle:
   - **Titel**: Produktname + Zustandskurzform + ggf. "Garantie"
   - **Art**: passende Artikelart auswählen (z.B. Kamera & Zubehör)
   - **Zustand**: korrekten Zustand auswählen
   - **Beschreibung**: Der generierte Text
   - **Preis**: Der abgestimmte Preis
   - **Preistyp**: VB (Verhandlungsbasis) auswählen
   - **Standort**: Vom Human angeben lassen
   - **Versandoption**: DHL Paket auswählen, Hermes abwählen
9. **Fotos**: 
   - Hat der Human Fotos gegeben → hochladen
   - Hat der Human keine → lizenzfreie Produktbilder von Wikimedia Commons oder offiziellen Hersteller-Presseseiten suchen und hochladen
   - **Hinweis**: Verwende keine Bilder von Amazon, Händlerseiten oder anderen Anzeigen – diese sind urheberrechtlich geschützt. Bei Unsicherheit den Human bitten, eigene Fotos zu machen.
10. Speichere als **Entwurf** (nicht veröffentlichen)
11. Gib dem Human den Link zum Entwurf

### 6. Abschluss
Teile dem Human mit: "Entwurf ist fertig. Hier der Link: [Link]. Du kannst jetzt:
- Fotos hinzufügen/ersetzen
- Preistyp und Versand prüfen
- Alles durchsehen
- Veröffentlichen wenn du zufrieden bist"

## Rechtliche Hinweise

- Der Nutzer ist selbst verantwortlich für die Einhaltung der Nutzungsbedingungen von kleinanzeigen.de sowie der Urheberrechte Dritter.
- Der Skill erstellt Anzeigen als Entwürfe – die Veröffentlichung und alle Inhalte liegen in der Verantwortung des Nutzers.
- Für Bilder sollten nach Möglichkeit eigene Fotos verwendet werden. Fremde Produktbilder nur aus lizenzfreien Quellen (Wikimedia Commons, offizielle Presse-Portale) verwenden.
