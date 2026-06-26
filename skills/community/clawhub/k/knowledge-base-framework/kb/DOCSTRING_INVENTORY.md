# Docstring & Kommentar Inventar

Generiert: 2026-04-13

## Zusammenfassung

| Metrik | Anzahl |
|--------|--------|
| Python-Dateien | 27 |
| Mit Modul-Docstring | 17 |
| Ohne Modul-Docstring | 10 |
| Mit DE-Docstrings | 8 |
| Mit EN-Docstrings | 9 |
| Parse-Fehler | 1 |
| German-Umlaut-Probleme | 15 |

## Detail-Tabelle

| Datei | Modul | Classes | Functions | Inline | Probleme |
|-------|-------|---------|-----------|--------|----------|
| `__init__.py` | NONE | 0/0 | 0/0 | 0 | — |
| `__main__.py` | EN | 0/0 | 7/8 | 10 | — |
| `config.py` | NONE | 0/0 | 0/0 | 6 | German-Umlauts |
| `indexer.py` | EN | 0/0 | 0/0 | 0 | **PARSE ERROR** (`logger for this module`) |
| `update.py` | EN | 0/0 | 8/8 | 18 | — |
| `version.py` | NONE | 0/0 | 0/0 | 0 | — |
| `obsidian/__init__.py` | EN | 0/0 | 0/0 | 4 | — |
| `obsidian/indexer.py` | EN | 1/1 | 15/15 | 48 | — |
| `obsidian/parser.py` | EN | 0/0 | 5/5 | 31 | — |
| `obsidian/resolver.py` | EN | 1/1 | 10/10 | 42 | — |
| `obsidian/vault.py` | EN | 1/1 | 22/22 | 60 | — |
| `obsidian/writer.py` | EN | 1/1 | 21/21 | 73 | — |
| `scripts/__init__.py` | NONE | 0/0 | 0/0 | 0 | — |
| `scripts/index_pdfs.py` | EN | 4/4 | 19/25 | 35 | German-Umlauts (DE in 2 class-docs, 5 func-docs) |
| `scripts/kb_full_audit.py` | **DE** | 0/0 | 14/15 | 24 | German-Umlauts (8x inline, 8x func-doc) |
| `scripts/kb_ghost_scanner.py` | **DE** | 0/0 | 10/11 | 17 | German-Umlauts (4x inline, 3x func-doc) |
| `scripts/kb_warmup.py` | **DE** | 0/0 | 0/1 | 3 | German-Umlauts |
| `scripts/migrate.py` | EN? | 0/0 | 5/6 | 1 | — |
| `scripts/reembed_all.py` | **DE** | 0/0 | 2/3 | 10 | German-Umlauts |
| `scripts/sanitize.py` | EN | 0/0 | 4/4 | 18 | — |
| `scripts/sync_chroma.py` | EN? | 0/0 | 5/6 | 5 | German-Umlauts (2x func-doc) |
| `library/__init__.py` | NONE | 0/0 | 0/0 | 0 | — |
| `kb/framework/__init__.py` | NONE | 0/0 | 0/0 | 0 | — |
| `kb/framework/chroma_integration.py` | **DE** | 1/1 | 18/18 | 25 | German-Umlauts (1 class-doc, 10 func-docs) |
| `kb/framework/chroma_plugin.py` | **DE** | 2/2 | 13/13 | 22 | German-Umlauts (1 class-doc, 8 func-docs, 5x inline) |
| `kb/framework/embedding_pipeline.py` | **DE** | 3/3 | 14/14 | 36 | German-Umlauts (2 class-docs, 9 func-docs, 1x inline) |
| `kb/framework/hybrid_search.py` | **DE** | 3/3 | 17/17 | 77 | German-Umlauts (2 func-docs, 2x inline) |

## Probleme im Detail

### 🔴 Parse-Fehler
- **`indexer.py`** — Syntaxfehler in Zeile ~15: `logger for this module` (fehlendes `=`)

### ⚠️ German-Umlaute (15 Dateien)
Folgende Dateien enthalten deutsche Umlaute (äöüÄÖÜß) in Docstrings oder Kommentaren:

- `config.py` — Inline-Kommentar
- `scripts/reembed_all.py` — Modul-Docstring
- `scripts/kb_ghost_scanner.py` — 4× Inline, 3× Function-Docstring
- `scripts/index_pdfs.py` — 2 Class-Docstrings, 5 Function-Docstrings
- `scripts/kb_warmup.py` — Modul-Docstring
- `scripts/sync_chroma.py` — 2× Function-Docstring
- `scripts/kb_full_audit.py` — 8× Inline, 8× Function-Docstring
- `kb/framework/hybrid_search.py` — 2× Inline, 2× Function-Docstring
- `kb/framework/chroma_integration.py` — 1 Class-Docstring, 10× Function-Docstring
- `kb/framework/embedding_pipeline.py` — 1× Inline, 2 Class-Docstrings, 9× Function-Docstring
- `kb/framework/chroma_plugin.py` — 5× Inline, 1 Class-Docstring, 8× Function-Docstring

### ⚠️ Fehlende Modul-Docstrings (10 Dateien)
- `__init__.py`, `config.py`, `version.py`, `indexer.py`
- `scripts/__init__.py`, `scripts/migrate.py`
- `kb/framework/__init__.py`

### ⚠️ Keine Docstrings Coverage
- `config.py` — 0 Classes, 0 Functions, aber 6 Inline-Kommentare (evtl. Docstrings als inline?)
- `indexer.py` — Parse Error verhindert Analyse
- `scripts/kb_warmup.py` — 0/1 Functions gedocst

## Sprachverteilung

| Sprache | Modul-Docstrings | Class-Docstrings | Function-Docstrings |
|---------|------------------|------------------|---------------------|
| EN | 9 | 6 | ~140 |
| DE | 8 | 6 | ~55 |
| NONE | 10 | — | — |
| EN? | 2 | — | — |

## Empfehlungen

1. **`indexer.py` Parse-Fehler beheben** — blocking für AST-Analyse
2. **Fehlende Modul-Docstrings ergänzen** — besonders `__init__.py` Dateien
3. **German-Umlaute uniformisieren** — entscheiden: DE komplett oder EN komplett
4. **`scripts/kb_warmup.py`** — 0/1 Functions gedocst; docstring fehlt
