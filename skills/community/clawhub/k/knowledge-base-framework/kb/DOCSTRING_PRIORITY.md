# Docstring Cleanup - Priorisierungs-Plan

**Erstellt:** 2026-04-13  
**Input:** `DOCSTRING_INVENTORY.md` (27 Dateien, 10 ohne Modul-Docstring, 15 mit German-Umlaut-Problemen, 1 Parse-Fehler)

---

## Prioritäts-Ebenen

| Ebene | Kriterium | Dateien |
|-------|-----------|---------|
| 🔥 Kritisch | Core API, parse-blocking, Einstiegspunkte | 3 |
| 🟡 Hoch | Config, Update, häufig importiert | 3 |
| 🟢 Mittel | Scripts (User-facing Utilities) | 6 |
| 🔵 Niedrig | Library/knowledge_base (interne Module) | 4 |
| ✅ Bestanden | Keine Umlaute, kein Parse-Error | 11 |

---

## Batch 1 — Kritisch (Core API)

### 1. `indexer.py` 🔥
**Priorität:** 1  
**Grund:** Parse-Fehler blockiert AST-Analyse für das gesamte Projekt. Muss zuerst behoben werden.  
**Aktion:** Syntaxfehler in Zeile ~15 beheben (`logger for this module` → `logger = ...`)  
**Status:** ❌ Parse Error

### 2. `__main__.py` 🔥
**Priorität:** 2  
**Grund:** Haupteinstiegspunkt. 7/8 Functions dokumentiert, 10 Inline-Kommentare.  
**Aktion:** Fehlenden Function-Docstring ergänzen, Inline-Kommentare zu Docstrings konvertieren  
**Status:** ✅ EN, kein Parse-Problem, nur unvollständig

### 3. `config.py` 🔥
**Priorität:** 3  
**Grund:** Zentrale Konfiguration, wahrscheinlich von vielen Modulen importiert. 6 Inline-Kommentare mit German-Umlauten.  
**Aktion:** Modul-Docstring ergänzen (EN), German-Umlaute bereinigen, Inline → Docstring  
**Status:** ⚠️ Kein Modul-Docstring, German-Umlaute

---

## Batch 2 — Hoch (Config & Update)

### 4. `update.py` 🟡
**Priorität:** 4  
**Grund:** 8/8 Functions dokumentiert, EN. Solides Core-Modul mit Update-Logik.  
**Aktion:** Modul-Docstring ergänzen (EN), keine Umlaute → sauber  
**Status:** ✅ EN, nur Modul-Docstring fehlt

### 5. `obsidian/indexer.py` 🟡
**Priorität:** 5  
**Grund:** Kern-Indexer mit 15 Functions, 48 Inline-Kommentaren. Hauptsächlich genutzt.  
**Aktion:** Modul-Docstring prüfen, Inline-Kommentare konsolidieren  
**Status:** ✅ EN, vollständig dokumentiert

### 6. `obsidian/vault.py` 🟡
**Priorität:** 6  
**Grund:** Vault-Management, 22 Functions, 60 Inline-Kommentare.  
**Aktion:** Modul-Docstring ergänzen wenn fehlt  
**Status:** ✅ EN, vollständig dokumentiert

---

## Batch 3 — Mittel (Scripts - User-facing)

### 7. `scripts/kb_full_audit.py` 🟢
**Priorität:** 7  
**Grund:** 14/15 Functions, 24 Inline, viele Umlaute (8× Inline + 8× Func-Doc). Wichtigster Audit-Script.  
**Aktion:** German-Umlaute → EN, Modul-Docstring ergänzen  
**Status:** ⚠️ DE, 16 Umlaute-Instanzen

### 8. `scripts/index_pdfs.py` 🟢
**Priorität:** 8  
**Grund:** 4 Classes, 19/25 Functions, 35 Inline. PDF-Indexing wichtig für Nutzer.  
**Aktion:** Modul-Docstring EN, Umlaute in Class/Function-Docs bereinigen  
**Status:** ⚠️ EN-Modul aber DE in Class/Func-Docs

### 9. `scripts/kb_ghost_scanner.py` 🟢
**Priorität:** 9  
**Grund:** Ghost-Discovery, 10/11 Functions, 17 Inline. Umlaute in 4 Inline + 3 Func-Docs.  
**Aktion:** German-Umlaute bereinigen  
**Status:** ⚠️ DE, 7 Umlaute-Instanzen

---

## Batch 4 — Mittel (Scripts, weniger kritisch)

### 10. `scripts/sync_chroma.py` 🟢
**Priorität:** 10  
**Grund:** 5/6 Functions, 5 Inline. Umlaute in 2 Func-Docs.  
**Aktion:** Modul-Docstring ergänzen, Umlaute bereinigen  
**Status:** ⚠️ EN?, Umlaute

### 11. `scripts/reembed_all.py` 🟢
**Priorität:** 11  
**Grund:** 2/3 Functions, 10 Inline. Umlaute in Modul-Docstring.  
**Aktion:** Modul-Docstring EN, Umlaute bereinigen  
**Status:** ⚠️ DE im Modul-Docstring

### 12. `scripts/migrate.py` 🟢
**Priorität:** 12  
**Grund:** 5/6 Functions, nur 1 Inline. Wenig Dokumentation.  
**Aktion:** Modul-Docstring ergänzen  
**Status:** ⚠️ EN?, nur Modul-Docstring fehlt

---

## Batch 5 — Niedrig (Library/knowledge_base - interne Module)

### 13. `kb/framework/hybrid_search.py` 🔵
**Priorität:** 13  
**Grund:** 3 Classes, 17 Functions, 77 Inline. Höchste Inline-Dichte. Umlaute in 2 Inline + 2 Func-Docs.  
**Aktion:** German-Umlaute bereinigen, Docstrings konsolidieren  
**Status:** ⚠️ DE, viele Umlaute

### 14. `kb/framework/embedding_pipeline.py` 🔵
**Priorität:** 14  
**Grund:** 3 Classes, 14 Functions, 36 Inline. Umlaute in 1 Inline + 2 Class + 9 Func-Docs.  
**Aktion:** Umlaute bereinigen, Class-Docstrings EN  
**Status:** ⚠️ DE, 12 Umlaute-Instanzen

### 15. `kb/framework/chroma_integration.py` 🔵
**Priorität:** 15  
**Grund:** 1 Class, 18 Functions, 25 Inline. Umlaute in 1 Class + 10 Func-Docs.  
**Aktion:** Umlaute bereinigen  
**Status:** ⚠️ DE, 11 Umlaute-Instanzen

### 16. `kb/framework/chroma_plugin.py` 🔵
**Priorität:** 16  
**Grund:** 2 Classes, 13 Functions, 22 Inline. Umlaute in 5 Inline + 1 Class + 8 Func-Docs.  
**Aktion:** Umlaute bereinigen  
**Status:** ⚠️ DE, 14 Umlaute-Instanzen

---

## ✅ Keine Aktion nötig (Bestanden)

| Datei | Status |
|-------|--------|
| `version.py` | Kein Parse-Problem, nur kein Modul-Docstring |
| `__init__.py` | Core, kein Bedarf |
| `scripts/__init__.py` | Minimale Datei |
| `library/__init__.py` | Minimale Datei |
| `kb/framework/__init__.py` | Minimale Datei |
| `scripts/kb_warmup.py` | Nur 0/1 Functions, nicht kritisch |
| `obsidian/__init__.py` | EN, vollständig |
| `obsidian/parser.py` | EN, vollständig |
| `obsidian/resolver.py` | EN, vollständig |
| `obsidian/writer.py` | EN, vollständig |

---

## Abhängigkeiten-Beachtung

```
config.py (Batch 1)
  └── wird importiert von: __main__.py, update.py, obsidian/*, scripts/*, library/*
      → Muss VOR allen anderen gefixt werden!

indexer.py (Batch 1)
  └── Core-Indexer, importiert von obsidian/*
      → Parse-Fehler VOR obsidian/* beheben

kb/framework/* (Batch 5)
  └── Internal, importiert von obsidian/* und scripts/*
      → NACHDEM Core + Scripts fertig
```

---

## Empfohlene Reihenfolge

```
Phase 1: Batch 1 (3 Dateien) — Blockierende Issues
Phase 2: Batch 2 (3 Dateien) — Core stabilisieren
Phase 3: Batch 3 (3 Dateien) — User-facing Scripts
Phase 4: Batch 4 (3 Dateien) — Restliche Scripts
Phase 5: Batch 5 (4 Dateien) — Library intern (niedrigste Priorität)
```

---

## Sprach-Entscheidung empfohlen

**Empfehlung:** EN als Standard für alle öffentlichen APIs, Scripts und Library-Module.

**Begründung:**
- `obsidian/*` ist bereits vollständig EN ✓
- `__main__.py`, `update.py` sind EN ✓
- `scripts/index_pdfs.py` hat EN-Modul-Docstring aber DE-Class/Func-Docs (inkonsistent)
- `kb/framework/*` ist durchgehend DE (viel Arbeit nötig)

**Konsequenz:** ~55 DE-Function-Docstrings → EN konvertieren.