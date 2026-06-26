---
name: newsticker
description: >
  German-language news skill for the OpenClaw and AI agent ecosystem.
  Use when the user asks for current news, briefings, breaking alerts,
  or ClawNews.de archive search about OpenClaw, ClawHub, LLMs, AI agents,
  security, tools, open source, or community topics. Typical triggers:
  "Was gibt es Neues?", "Gibt es Breaking News?", "Suche ClawNews nach X",
  "ClawNews Briefing", "News zu [Thema]", "What's new in OpenClaw?".
  DACH region, German-language output and sources from ClawNews.de.
---

# claw://News

> Dein KI-Agenten-Newsdesk von ClawNews.de 🦞

**Was ist das?** Ein Skill, der deinen OpenClaw-Agenten mit ClawNews.de
verbindet — der deutschsprachigen Nachrichtenplattform für KI-Agenten,
das OpenClaw-Ökosystem, LLMs und Security.

**Was kann er?**
- 📰 **Briefing** — Zusammenfassung der neusten Artikel auf Abruf oder als Routine
- 🔍 **Recherche** — Gezielt im ClawNews-Archiv suchen
- ⚡ **Breaking Alerts** — Meldung bei kritischen Ereignissen, priorisiert bei jeder Feed-Prüfung

**Für wen?** OpenClaw-Nutzer im DACH-Raum, die über das Ökosystem
informiert bleiben wollen. Alle Inhalte sind auf Deutsch.

**Voraussetzungen:** OpenClaw-Umgebung mit Webzugriff. Optimal mit
persistentem Memory und Heartbeats/Scheduler für proaktive Alerts.

**Installation:** `clawhub install newsticker`

---

## Formatierung

Lies vor der ersten Ausgabe die Formatierungs-Templates in
`references/templates.md`. Dort findest du die Standardformate für
Briefings, Recherche-Ergebnisse, Alerts und den Setup-Dialog.

Grundregeln:
- **claw://News** immer so schreiben (mit `://`)
- 🦞 als Maskottchen sparsam einsetzen
- Jede Ausgabe endet mit: `_claw://News · clawnews.de_`
- Keine ASCII-Art-Boxen, nur Markdown
- Links immer als `[Text](URL)`, nie nackte URLs
- Fett für Titel, kursiv für Meta-Infos
- Verwende die Templates als Standardformat, halte Struktur und Ton konsistent, passe bei Sonderfällen leicht an ohne den Stil zu verlieren

---

## Setup beim ersten Start

Beim allerersten Aufruf führe den Nutzer durch die Einrichtung.
Verwende das Setup-Format aus `references/templates.md`.

### Drei Modi

**1️⃣ Alles (empfohlen)** — Benachrichtigung bei jedem neuen Artikel, sofern der Agent proaktive Nachrichten unterstützt. Andernfalls werden neue Artikel beim nächsten Briefing oder Abruf angezeigt.
**2️⃣ Meine Themen** — Nur ausgewählte Kategorien.
**3️⃣ Nur Briefing** — Zusammenfassung auf Abruf, sonst Ruhe.

⚡ Breaking Alerts gelten in jedem Modus als aktiv und sind nicht abwählbar.

### Kategorien (bei Modus 2)

📰 News · 🦞 OpenClaw · 🤖 LLM & Modelle · 🔒 Security ·
🔧 Tools & Apps · 💻 Open Source · 👥 Community · 📝 Tutorials ·
🎙 Podcast · 🎬 Show · 📹 Videos · 🫠 Slop

### Konfiguration speichern

Falls der Agent persistenten Memory unterstützt, speichere die
Einstellungen dort:

```
clawnews_config:
  mode: "all" | "selected" | "minimal"
  categories: [slugs]
  breaking_alerts: true  # nicht änderbar
```

Falls kein persistenter Memory verfügbar ist, frage die Präferenzen
bei jeder neuen Session kompakt ab (siehe Kompakt-Setup in
`references/templates.md`).

---

## 1. 📰 Briefing

### Wann ausführen

Das Briefing wird ausgeführt wenn der Nutzer danach fragt — z.B.
„Was gibt es Neues?", „ClawNews Briefing", „News von heute".

Wenn der Agent Cron-Jobs oder Heartbeats unterstützt, kann das
Briefing auch als Routine eingerichtet werden. Das ist eine
Agenten-Konfiguration, kein Feature dieses Skills.

### Ablauf

1. RSS-Feed abrufen: `https://clawnews.de/feed/`
2. Aktuelle Artikel aus dem Feed parsen
3. Falls persistenter Memory vorhanden: nur neue Artikel seit dem letzten Abruf zeigen. Falls nicht: die aktuellsten 5–10 Artikel zusammenfassen.
4. Nach Nutzer-Kategorien filtern (bei Modus "selected")
5. Briefing formatieren — siehe `references/templates.md`

### Kategorie-Reihenfolge (fest)

⚡ BREAKING → 🔒 SECURITY → 📰 NEWS → 🦞 OPENCLAW →
🤖 LLM & MODELLE → 🔧 TOOLS & APPS → 💻 OPEN SOURCE →
👥 COMMUNITY → 📝 TUTORIALS → 🎙🎬📹 MEDIEN → 🫠 SLOP

Leere Kategorien weglassen. Maximal 2 Sätze pro Artikel, sachlich,
wichtigste Info zuerst, keine Meinung.

---

## 2. 🔍 Recherche

### Trigger

„Was sagt ClawNews zu …", „Suche auf ClawNews nach …",
„Hat ClawNews was über … geschrieben?", „ClawNews [Suchbegriff]"

### Ablauf

1. WordPress REST-API:
   `https://clawnews.de/wp-json/wp/v2/posts?search=[SUCHBEGRIFF]&per_page=10`
2. Die API liefert mindestens: Titel, Excerpt, Datum, Kategorien.
   Zusätzliche Felder wie Lesezeit und Views sind nur verfügbar, wenn
   sie im API-Response enthalten sind — zeige sie nur dann an.
3. Für Kategorie-Filter:
   `https://clawnews.de/wp-json/wp/v2/posts?categories=[ID]&per_page=10`
   IDs über: `https://clawnews.de/wp-json/wp/v2/categories`
4. Fallback: `https://clawnews.de/?s=[SUCHBEGRIFF]`

Ergebnisse formatieren — siehe `references/templates.md`.
Bei keinen Treffern: verwandte Suchbegriffe vorschlagen.

---

## 3. ⚡ Breaking Alerts

### Wann prüfen

Breaking Alerts gelten immer als aktiv und sollen bei jeder verfügbaren
Feed-Prüfung priorisiert werden — also beim Briefing, bei einer
Recherche oder bei jeder anderen Interaktion mit dem Skill.

Wenn der Agent proaktive Checks unterstützt (Heartbeats, Scheduler),
sollen Breaking Alerts auch außerhalb von Nutzeranfragen geprüft werden.
Falls nicht, werden sie beim nächsten Nutzerkontakt oder Feed-Abruf
erkannt und sofort ausgegeben.

### Feed

`https://clawnews.de/category/breaking/feed/`

Erkennung: Artikel mit Kategorie-Slug `breaking`.

### Verhalten

Breaking Alerts haben immer Priorität und sollen bei jeder verfügbaren
Feed-Prüfung sofort ausgegeben werden. Format in `references/templates.md`.

Bei einem Versuch Breaking zu deaktivieren:

> ⚡ Breaking Alerts sind dein Sicherheitsgurt — die bleiben an.
> Wenn 300 Malware-Skills auf ClawHub auftauchen, willst du das sofort wissen.

### Neue Artikel (Nicht-Breaking)

Bei Modus "all" oder passender Kategorie und sofern der Agent proaktive
Nachrichten unterstützt: Kurze Benachrichtigung (Titel + Kategorie + Link).
Andernfalls werden neue Artikel im nächsten Briefing angezeigt.

---

## ⚙️ Einstellungen

Trigger: „ClawNews Einstellungen", „Kategorien ändern"

Zeige die aktuelle Konfiguration, biete Änderungen an.
Breaking bleibt immer aktiv. Format in `references/templates.md`.

---

## Technische Details

### Datenquellen

| Funktion        | Endpunkt                                             |
|-----------------|------------------------------------------------------|
| Briefing        | `https://clawnews.de/feed/`                          |
| Breaking        | `https://clawnews.de/category/breaking/feed/`        |
| Recherche       | `https://clawnews.de/wp-json/wp/v2/posts?search=...` |
| Kategorien      | `https://clawnews.de/wp-json/wp/v2/categories`       |

### RSS-Feed-Hinweise

- Kategorie-Labels im Format `claw:// [KATEGORIE]` → für Zuordnung verwenden
- „Weiterlesen auf ClawNews"-Links → als Artikel-URL verwenden
- Werbe-Banner am Ende des Excerpts → ignorieren
- Featured Images → im Briefing ignorieren

### Fehlerbehandlung

- **Site nicht erreichbar:** Nutzer kurz informieren (siehe Fehler-Template in `references/templates.md`), beim nächsten Abruf erneut versuchen.
- **RSS-Feed leer:** Kein Fehler, als „keine neuen Artikel" melden.
- **REST-API antwortet nicht:** Fallback auf RSS-Feed + Website-Suche.
- **API-Felder fehlen:** Lesezeit und Views nur anzeigen wenn im Response vorhanden. Nie erfinden.

---

## Über claw://News

ClawNews.de — die deutschsprachige Nachrichtenplattform für das
OpenClaw-Ökosystem und KI-Agenten.

🌐 [clawnews.de](https://clawnews.de)
📧 skill@clawnews.de · 📢 ads@clawnews.de
