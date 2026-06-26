---
name: nuberea
description: "Bible research platform for AI agents. NuBerea provides direct access to original-language Hebrew and Greek morphology, the LSJ and BDB lexicons, KJV Bible text, Dead Sea Scrolls, NT manuscript transcriptions, and Septuagint LXX — all queryable via typed tools or freeform SQL joins. Use NuBerea for Bible study, biblical languages, exegesis, word studies, Scripture lookup, lexicon definitions, Strong's numbers, morphological parsing, synoptic parallels, and ancient manuscripts."
---

# NuBerea

Bible research platform — Hebrew/Greek morphology, lexicons, Bible texts, manuscripts, scrolls — queryable via MCP tools or SQL analytics.

## Databases

| Schema | Table | Description | Rows |
|---|---|---|---|
| `hebrew` | `morphemes` | Hebrew Bible morphological analysis (Macula) | 467,770 |
| `greek` | `morphemes` | Greek NT morphological analysis (Macula) | 137,741 |
| `lxx` | `morphemes` | Septuagint (LXX) morphological analysis | 623,693 |
| `lsj` | `entries` | Liddell-Scott-Jones Greek Lexicon | 119,553 |
| `bdb` | `entries` | Brown-Driver-Briggs Hebrew Lexicon | 10,221 |
| `abbott_smith` | `entries` | Abbott-Smith NT Greek Lexicon | 555 |
| `kjv` | `verses` | King James Version Bible text | 36,821 |
| `cntr` | `transcriptions` | CNTR Greek NT manuscript transcriptions | 41,956 |
| `dss` | `scrolls` | Dead Sea Scrolls word annotations | 500,991 |
| `aland` | `pericopes` | Synoptic parallel pericopes (Aland) | 330 |

## Tool Collections

57 MCP tools organized by prefix:

- **`bible_kjv_*`** — get_verse, get_chapter, get_verse_range, search_text, run_sql
- **`macula_hebrew_*`** — query_verse, search_lemma, search_strong, search_word, run_sql
- **`macula_greek_*`** — same as hebrew but for Greek NT
- **`macula_lxx_*`** — same for Septuagint
- **`lexicon_lsj_*`** — lookup, search, search_latin, search_definition, search_strong
- **`lexicon_bdb_*`** — lookup, search_strong, search_transliteration, search_definition
- **`lexicon_abbott_smith_*`** — lookup, search_strong, search_definition
- **`scroll_dss_*`** — get_scroll, get_fragment, search_lemma, list_scrolls
- **`transcription_cntr_*`** — get_verse, list_manuscripts
- **`synoptic_*`** — find_parallels, find_parallels_range, search, list_pericopes
- **`analytics_*`** — query (SQL), list_databases, describe_table, schema_introspect

## Example Workflows

### Analyze a Hebrew word across the Bible

Tool call — `macula_hebrew_search_lemma`:
```json
{ "lemma": "חֶסֶד", "limit": 20 }
```

Or via `analytics_query` (SQL):
```sql
SELECT book_id, COUNT(*) as uses
FROM hebrew.morphemes
WHERE lemma = 'חֶסֶד'
GROUP BY book_id
ORDER BY uses DESC
```

### Compare Greek NT with Septuagint

Tool call — `analytics_query` (SQL):
```sql
SELECT g.lemma, g.gloss, COUNT(*) as nt_uses,
  (SELECT COUNT(*) FROM lxx.morphemes l WHERE l.lemma = g.lemma) as lxx_uses
FROM greek.morphemes g
WHERE g.book_id = 'John' AND g.chapter = 1
GROUP BY g.lemma, g.gloss
ORDER BY nt_uses DESC
LIMIT 15
```

### Cross-reference morphology with lexicon

Tool call — `analytics_query` (SQL):
```sql
SELECT g.text, g.lemma, g.gloss, l.definition_text
FROM greek.morphemes g
LEFT JOIN lsj.entries l ON g.lemma = l.headword
WHERE g.book_id = 'Rom' AND g.chapter = 8 AND g.verse = 28
ORDER BY g.word_position
```
