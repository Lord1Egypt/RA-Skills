---
name: ORF News
description: "ORF.at RSS: news/sport (RDF) + science (RSS2). Überblick: 3× news (orf.at) + 1× sport + 1× science — science.orf.at niemals unter Nachrichten; drei ###-Sektionen, Titel als **[text](url)**."
tags: [news, orf, sport, science, österreich, rss]
hint_allow_substrings: ["orf", "orf.at", "nachrichten", "orf news", "österreich news", "austria news"]
requires: []
source: "https://rss.orf.at/"
---

# ORF — RSS (Nachrichten, Sport, Science)

Offizielle Feeds (chronologisch, viele Items). Übersicht: [rss.orf.at](https://rss.orf.at/).

| Rubrik | URL | Format |
|--------|-----|--------|
| **Nachrichten** | `https://rss.orf.at/news.xml` | RDF / RSS1.0 |
| **Sport** | `https://rss.orf.at/sport.xml` | RDF / RSS 1.0 |
| **Science** (science.orf.at) | `https://rss.orf.at/science.xml` | RSS2.0 |

## Wichtig: zwei XML-Formate

**News + Sport** (`news.xml`, `sport.xml`): RDF mit `<channel>`, dann viele Blöcke `<item rdf:about="…">` mit u. a.:

- `<title>` — Überschrift
- `<link>` — **kanonische Artikel-URL** (immer exakt übernehmen)
- `<description>` — Teaser (optional)
- `<dc:subject>` — Ressort (z. B. Tennis, Wirtschaft) — **nur ausgeben, wenn vorhanden**
- `<dc:date>` — Zeitstempel (Item)

**Science** (`science.xml`): klassisches RSS 2.0 mit `<item>` und u. a.:

- `<title>`, `<link>`, `<description>`, `<pubDate>`, `<category>` (oft „Wissenschaft“)

Parser/logisch: Pro Feed nur die **`<item>`-Blöcke** zählen — nicht die URL-Liste in `<items><rdf:Seq>` allein (die sind nur die Reihenfolge).

## Fetch (Tool `fetch`)

```text
https://rss.orf.at/news.xml
https://rss.orf.at/sport.xml
https://rss.orf.at/science.xml
```

**Mehrteilige Abfragen:** Wenn mehr als ein Feed nötig ist, **für jeden Feed einen eigenen `fetch`** ausführen — z. B. drei Aufrufe für Nachrichten + Sport + Science. Erst wenn alle benötigten Feeds da sind (oder klar fehlschlagen), die Antwort schreiben.

- Keinen Sport- oder Science-Block ausgeben, **wenn** `sport.xml` bzw. `science.xml` nicht geladen wurde.
- **Niemals** Sport- oder Science-Schlagzeilen aus `news.xml` „ableiten“ oder erfinden — URLs müssen **im jeweiligen Feed-XML** vorkommen.

## Welche Feeds laden?

| Nutzeranfrage (Beispiele) | Aktion |
|---------------------------|--------|
| allgemein: ORF / ORF News / Schlagzeilen / „was gibt’s bei ORF“ / Überblick | **`news.xml` + `sport.xml` + `science.xml`** (3 Fetches) |
| nur Nachrichten / Politik / „ohne Sport“ | nur `news.xml` |
| nur Sport | nur `sport.xml` |
| nur Science / Forschung / science.orf | nur `science.xml` |
| explizit „News und Sport“ (ohne Science) | `news.xml` + `sport.xml` |

So sind Sport und Science sichtbar, ohne alles in einen News-Feed zu pressen.

## Anzahl Meldungen (Überblick wirkt ruhiger)

Wenn **Nachrichten + Sport + Science** geladen werden (typische ORF-Überblicksfrage):

| Sektion | Items aus dem Feed (neueste zuerst) |
|---------|-------------------------------------|
| **Nachrichten** | **genau 3** |
| **Sport** | **genau 1** |
| **Science** | **genau 1** |

Nur wenn der Nutzer explizit mehr will („alle“, „längere Liste“, Zahl nennen): von dieser Verteilung abweichen.

**Nur ein** Feed geladen: bis zu **7** Items (oder weniger, wenn der Feed kürzer ist).

## Inhaltliche Regeln (Anti-Halluzination)

- Jede Zeile: **Titel + Link** müssen **1:1 aus demselben `<item>`** stammen.
- **Keine** zusätzlichen Meldungen, **keine** erfundenen URLs, **keine** „Kategorie:“-Präfixe erfinden. Bei News/Sport: Ressort **nur** aus `<dc:subject>`, wenn gesetzt. Bei Science: optional `<category>`.
- Senderzeile im Channel (`<title>news.ORF.at</title>` etc.) ist **kein** Artikel — ignorieren.
- Titel nicht „verbessern“ oder kürzen, wenn unsicher; Original `<title>` bevorzugen.

## Sektion nach Hostname (harte Regel)

Sortierung **nur** nach Herkunfts-Feed **und** sichtbar im `<link>`:

| Host im `<link>` | Sektion | Feed |
|------------------|---------|------|
| `orf.at` (Artikelpfad z. B. `/stories/…`) | **Nachrichten** | `news.xml` |
| `sport.orf.at` | **Sport** | `sport.xml` |
| `science.orf.at` | **Science** | `science.xml` |

**Verboten:** Science-Artikel (`science.orf.at`) oder Sport-Artikel (`sport.orf.at`) unter „Nachrichten“ zu listen — auch nicht mit Rubrik „Wissenschaft“. Eine lange Liste nur unter `### Nachrichten` ist **falsch**, sobald Links von mehreren Hosts vorkommen.

## Antwort — Layout (Pflichtstruktur)

Sprache wie der Nutzer (meist Deutsch). **Keine** Emoji-Deko in Überschriften. **Leerzeile** nach jeder Überschrift (`##` / `###`).

**Zeilenumbrüche:** Jede nummerierte Meldung **beginnt auf einer neuen Zeile** (nach `1.` / `2.` / `3.`). Niemals alle Punkte in **einem** Absatz oder eine Zeile ohne Leerzeilen zwischen den `###`-Blöcken weglassen.

**Link-Darstellung:** Den Artikel **nur** als Markdown-Link im Titel: `**[Titel](https://…/)**`. **Nicht** `*Link:*` oder URL doppelt in Klammern neben dem Titel — das ist unübersichtlich.

**Ein** geladener Feed:

```markdown
## ORF — [Nachrichten | Sport | Science]

*Stand laut Feed: …*

### Top-Meldungen

1. **[Überschrift genau aus dem XML](https://…/)**
2. …
```

**Mehrere** Feeds (typisch: Nachrichten + Sport + Science): **immer drei Unterüberschriften** `### Nachrichten`, `### Sport`, `### Science` — auch wenn eine Sektion nur einen Punkt hat.

```markdown
## ORF — Schlagzeilen

*Nachrichten, Sport, Science · Stand laut Feeds: …*

### Nachrichten (news.ORF.at)

1. **[Titel](https://orf.at/stories/…/)** — *Ressort*
2. **[Titel](https://orf.at/stories/…/)** — *Ressort*
3. **[Titel](https://orf.at/stories/…/)** — *Ressort*

### Sport (sport.ORF.at)

1. **[Titel](https://sport.orf.at/stories/…/)** — *Ressort*

### Science (science.orf.at)

1. **[Titel](https://science.orf.at/stories/…/)**
```

- **Überblick (3 Feeds):** **3 / 1 / 1** — unter Nachrichten **nur** `orf.at`-Links aus `news.xml`; **kein** `science.orf.at` in dieser Liste. Keine zusätzlichen Zeilen in Sport oder Science, außer der Nutzer verlangt mehr.
- Ressort-Zeile weglassen, wenn kein `<dc:subject>` bzw. keine sinnvolle Kategorie im Item.
- Optional eine **kurze** Zeile Teaser aus `<description>` — nur wenn sie im XML steht und die Lesbarkeit hilft (max. ~140 Zeichen).

## Mandatory

Non-negotiable checklist (single-file skill — everything lives in this README):

1. **Feeds & Zuordnung:** Items unter **Nachrichten** nur aus `https://rss.orf.at/news.xml`. Items unter **Sport** nur aus `https://rss.orf.at/sport.xml`. Items unter **Science** nur aus `https://rss.orf.at/science.xml`. Keine Story und keine URL **quers** zuordnen oder duplizieren.

2. **Hostname = Sektion:** `<link>` mit Host **`science.orf.at`** nur unter `### Science`. **`sport.orf.at`** nur unter `### Sport`. **`orf.at`** (News-Artikel) nur unter `### Nachrichten`. **Niemals** Science-URLs unter „Nachrichten“ listen — auch nicht mit Rubrik „Wissenschaft“.

3. **Allgemeine ORF-Frage:** Wenn der Nutzer nicht explizit auf eine Rubrik beschränkt (z. B. „ORF News“, „Schlagzeilen ORF“, „was gibt’s bei ORF“), **alle drei URLs** mit **drei separaten `fetch`-Aufrufen** laden, bevor geantwortet wird.

4. **XML:** `news.xml` und `sport.xml` sind **RDF/RSS1.0** (`<item rdf:about>`, `<dc:subject>`, `<dc:date>`). `science.xml` ist **RSS 2.0** (`<item>`, `<pubDate>`, `<category>`). Nicht nur die `<rdf:Seq>`-Links parsen — Titel/Links aus den **`<item>`**-Blöcken nehmen.

5. **Links:** Jede Schlagzeile braucht den **exakten** `<link>` aus dem **selben** Item. Keine erfundenen oder zusammengesetzten URLs. Darstellung: **`**[Titel](url)**`** — **kein** separates `*Link:*`-Feld.

6. **Layout:** `##` Gesamtüberschrift, dann **`### Nachrichten`**, **`### Sport`**, **`### Science`** (alle drei beim 3-Fetch-Überblick). Nach jeder `###`-Zeile eine **Leerzeile**; jede nummerierte Meldung **eigenständige Zeile(n)** — nicht alles in einen Absatz quetschen.

7. **Überblick — feste Quoten:** Sind alle drei Feeds geladen und der Nutzer hat keine andere Menge verlangt: **3** Nachrichten (nur `orf.at`), **1** Sport-Story, **1** Science-Story. **Nicht** 4+ unter Nachrichten, indem Science dort eingemischt wird.

8. **Keine erfundenen Inhalte:** Keine Sport-/Science-Zeilen aus dem Kopf; kein „Kultur:“ / „Wirtschaft:“ vor dem Titel erfinden — höchstens Ressort aus `<dc:subject>` bzw. `<category>`.

## Fehlerfälle

- Feed leer / HTTP-Fehler: kurz nennen, betroffene Sektion auslassen oder als fehlgeschlagen markieren — nichts erfinden.
- `science.xml` liefert **Wissenschaftsnews**, nicht den allgemeinen Politik-Mix — nicht als „normale Nachrichten“ verkaufen.

## When to use

Fragen zu ORF, ORF News, österreichischen Schlagzeilen, ORF Sport, science.orf / ORF Science, oder „was läuft bei ORF“.
