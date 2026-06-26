<!-- Referenced by SKILL.md — do not rename or move this file -->

# claw://News — Formatierungs-Templates

Dieses Dokument enthält die Standardformate für alle Funktionen des
claw://News Skills. Verwende sie als Ausgangspunkt, halte Struktur
und Ton konsistent, und passe bei Sonderfällen leicht an ohne den
Stil zu verlieren.

---

## Setup-Dialog

### Willkommen

> 🦞 **claw://News — Setup**
>
> Willkommen bei deinem KI-Agenten-Newsdesk!
> ClawNews.de versorgt dich mit allem rund um OpenClaw,
> KI-Agenten, LLMs und Security.
>
> Lass uns kurz einrichten, wie du informiert werden willst.

### Modus wählen

> **Wie möchtest du benachrichtigt werden?**
>
> **1️⃣ Alles** _(empfohlen)_
> Jeder neue Artikel wird angezeigt — beim nächsten Abruf oder, falls dein Agent proaktive Nachrichten unterstützt, auch direkt.
>
> **2️⃣ Meine Themen**
> Nur Kategorien, die dich interessieren.
>
> **3️⃣ Nur Briefing**
> Zusammenfassung auf Abruf, sonst Ruhe.
>
> _⚡ Breaking Alerts gelten in jedem Modus als aktiv und sind nicht abwählbar._

### Kategorien

> **Welche Themen interessieren dich?**
>
> ☐ 📰 **News** — Tagesaktuelle Meldungen
> ☐ 🦞 **OpenClaw** — Alles rund um OpenClaw
> ☐ 🤖 **LLM & Modelle** — Sprachmodelle, Benchmarks, Releases
> ☐ 🔒 **Security** — Sicherheitslücken, Malware, Advisories
> ☐ 🔧 **Tools & Apps** — Software und Integrationen
> ☐ 💻 **Open Source** — Community-Projekte und Repos
> ☐ 👥 **Community** — Events, Personen, Diskussionen
> ☐ 📝 **Tutorials** — Anleitungen und Guides
> ☐ 🎙 **Podcast** — ClawNews Podcast-Episoden
> ☐ 🎬 **Show** — ClawNews Show-Format
> ☐ 📹 **Videos** — Video-Content
> ☐ 🫠 **Slop** — Kurioses und Memes aus der KI-Welt
>
> _Nenne einfach die Kategorien die du willst._

### Bestätigung

> ✅ **claw://News ist eingerichtet!**
>
> 📰 Briefing: **auf Abruf** _(oder als Routine, falls dein Agent das unterstützt)_
> 🔔 Modus: **[MODUS]**
> ⚡ Breaking: **immer aktiv**
>
> Sag jederzeit _„ClawNews Einstellungen"_ um etwas zu ändern.
>
> _claw://News · clawnews.de_

---

## Briefing — mit Artikeln

> 📰 **claw://News — Briefing**
> _[Wochentag], [Datum]_
>
> **[Anzahl] neue Artikel:**
>
> ---
>
> ⚡ **BREAKING**
>
> **[Titel]**
> [Zusammenfassung in 1-2 Sätzen. Klar, sachlich, auf den Punkt.]
> 🔗 [Weiterlesen →](URL)
>
> ---
>
> 🔒 **SECURITY**
>
> **[Titel]**
> [Zusammenfassung in 1-2 Sätzen.]
> 🔗 [Weiterlesen →](URL)
>
> ---
>
> 📰 **NEWS**
>
> **[Titel]**
> [Zusammenfassung in 1-2 Sätzen.]
> 🔗 [Weiterlesen →](URL)
>
> ---
>
> _claw://News · clawnews.de_ 🦞

## Briefing — keine neuen Artikel

> 📰 **claw://News — Briefing**
> _[Wochentag], [Datum]_
>
> Keine neuen relevanten Artikel gefunden.
> Ruhiger Tag in der KI-Agenten-Welt. 🦞
>
> _claw://News · clawnews.de_

---

## Recherche — Treffer

> 🔍 **claw://News — Recherche**
> _Suche: „[SUCHBEGRIFF]"_
>
> **[Anzahl] Treffer:**
>
> ---
>
> **1. [Titel]**
> _📅 [Datum] · 📂 [Kategorie]_
> _⏱ [Lesezeit] · 👁 [Views] Aufrufe_ _(nur wenn verfügbar)_
> [Zusammenfassung in 2-3 Sätzen basierend auf dem Excerpt.]
> 🔗 [Vollständiger Artikel →](URL)
>
> **2. [Titel]**
> _📅 [Datum] · 📂 [Kategorie]_
> [Zusammenfassung in 2-3 Sätzen.]
> 🔗 [Vollständiger Artikel →](URL)
>
> ---
>
> _claw://News · clawnews.de_ 🦞

## Recherche — keine Treffer

> 🔍 **claw://News — Recherche**
> _Suche: „[SUCHBEGRIFF]"_
>
> Keine Treffer für _„[SUCHBEGRIFF]"_.
>
> **Verwandte Suchbegriffe:**
> [2-3 alternative Begriffe vorschlagen die thematisch passen]
>
> _claw://News · clawnews.de_ 🦞

---

## Breaking Alert

> 🚨 **claw://News — BREAKING** ⚡
>
> **[TITEL]**
>
> [Zusammenfassung in 3-4 Sätzen:
> Was ist passiert? Warum ist das relevant?
> Was sollte der Nutzer tun?]
>
> 🔗 [Vollständiger Artikel →](URL)
>
> _claw://News · clawnews.de_

---

## Neue-Artikel-Benachrichtigung (Nicht-Breaking)

> 🔔 **claw://News**
> **[Titel]** · _[Kategorie]_
> 🔗 [Lesen →](URL)

Kurz und unaufdringlich. Nur Titel, Kategorie, Link.

---

## Einstellungen

> ⚙️ **claw://News — Einstellungen**
>
> **Modus:** [Alles / Meine Themen / Nur Briefing]
> **Breaking:** ⚡ immer aktiv
>
> **Aktive Kategorien:**
> ✅ News · ✅ OpenClaw · ✅ Security
> ✅ LLM & Modelle · ❌ ~~Tutorials~~
> ❌ ~~Podcast~~ · ❌ ~~Videos~~ · ✅ Slop
>
> _Was möchtest du ändern?_
>
> _claw://News · clawnews.de_ 🦞

---

## Fehler-Meldung

> ⚠️ **claw://News** — clawnews.de ist gerade nicht erreichbar
> oder liefert keine verwertbaren Daten.
> Ich versuche es beim nächsten Abruf erneut.

---

## Kompakt-Setup (für Sessions ohne persistenten Memory)

Wenn der Agent keinen persistenten Memory hat, frage bei neuen Sessions
kompakt nach den Präferenzen:

> 🦞 **claw://News** — Kurz-Setup: Welche Kategorien interessieren dich?
> _(Oder sag „alles" für alle Themen.)_
