---
name: tech_ai_news
version: 1.0.0
trigger: KI_NEWS, AI_NEWS
---

# Tech & KI News — Template & Rules

## Purpose
Kompaktes KI/Tech-News Briefing via Telegram.

## Output-Struktur
1. 🤖 Top KI-News (max 3 Headlines)
 - Format: Fettgedruckter Titel + 1 Satz Kontext
 - Nur Releases, Studien, Produkt-Launches — kein Hype
2. 💻 Tech-News (optional, max 2 Headlines)
 - Nur wenn relevant (Apple, Google, OpenAI, Anthropic, Meta)

## Content Rules
- IMMER zuerst suchen: brave_search → tavily_search
- Quellen: nur seriöse Tech-Medien (The Verge, Ars Technica, heise.de, etc.)
- Kein Ergebnis → "Keine aktuellen KI-News gefunden"
- Niemals Versionen, Preise oder Specs aus internem Wissen nennen
- Max 12 Zeilen gesamt

## Style
- Deutsch, sachlich
- Fakten first, kein Hype-Sprache
