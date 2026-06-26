# Memory-System — Deep Dive

## Architektur-Überblick

OpenClaw nutzt ein dateibasiertes Markdown-Memory-System mit optionaler semantischer Suche.
**Kernprinzip: Dateien sind die Quelle der Wahrheit** — der Agent behält nur, was auf Disk geschrieben wird.

```
Workspace/
├── MEMORY.md              # Langzeit (kuratiert, nur private Sessions)
└── memory/
    ├── 2026-03-17.md      # Tages-Log (append-only)
    ├── 2026-03-18.md
    └── ...
```

### Memory-Ebenen

| Datei | Zweck | Wann geladen |
|-------|-------|--------------|
| `MEMORY.md` | Kuratierte Fakten, Entscheidungen, Präferenzen | Jede private Session |
| `memory/YYYY-MM-DD.md` | Tagesnotizen, Running-Log | Heute + Gestern am Session-Start |

> **Hinweis**: Wenn sowohl `MEMORY.md` als auch `memory.md` existieren, wird nur `MEMORY.md` geladen (Großbuchstaben priorisiert).

---

## Memory-Tools

OpenClaw stellt zwei Agent-Tools bereit:

### `memory_search`
Semantische Suche über indizierte Snippets:
- Gibt Snippet-Text (~700 Zeichen), Dateipfad, Zeilenbereich, Score zurück
- Unterstützt Hybrid-Suche (BM25 + Vektor)
- MMR für Diversität, Temporal Decay für Aktualität

### `memory_get`
Gezieltes Lesen einer Memory-Datei:
- Liest workspace-relative Pfade
- Optional mit Startzeile und Zeilenanzahl
- Graceful Degradation: Bei nicht existierender Datei wird `{text: "", path}` zurückgegeben

```json5
// Tool-Beispiel
memory_get({ path: "memory/2026-03-17.md", startLine: 50, lines: 20 })
```

---

## Memory Flush (automatisch vor Compaction)

Wenn eine Session sich der Context-Window-Grenze nähert, triggert OpenClaw einen stillen Turn:
- Agent wird aufgefordert, wichtige Infos in `memory/YYYY-MM-DD.md` zu schreiben
- Standard-Antwort: `NO_REPLY` (User sieht nichts)

### Konfiguration

```json5
agents: {
  defaults: {
    compaction: {
      reserveTokensFloor: 20000,
      memoryFlush: {
        enabled: true,
        softThresholdTokens: 4000,
        systemPrompt: "Session nearing compaction. Store durable memories now.",
        prompt: "Write any lasting notes to memory/YYYY-MM-DD.md; reply with NO_REPLY if nothing to store.",
      },
    },
  },
}
```

### Flush-Details

- **Trigger**: `tokenEstimate > contextWindow - reserveTokensFloor - softThresholdTokens`
- **Ein Flush pro Compaction-Zyklus** (in sessions.json getrackt)
- **Workspace muss schreibbar sein** (`workspaceAccess: "ro"` oder `"none"` → Flush übersprungen)

---

## Semantic Memory Search

### Provider-Auswahl (Auto-Detect)

Wenn `memorySearch.provider` nicht gesetzt ist, wählt OpenClaw automatisch:

1. `local` — wenn `memorySearch.local.modelPath` existiert
2. `openai` — wenn OpenAI-Key gefunden
3. `gemini` — wenn Gemini-Key gefunden
4. `voyage` — wenn Voyage-Key gefunden
5. `mistral` — wenn Mistral-Key gefunden
6. **disabled** — wenn kein Key

### Konfiguration

```json5
agents: {
  defaults: {
    memorySearch: {
      enabled: true,
      provider: "openai",           // "openai" | "gemini" | "voyage" | "mistral" | "local" | "ollama"
      model: "text-embedding-3-small",

      // Remote-Provider-Optionen
      remote: {
        apiKey: { source: "env", provider: "default", id: "OPENAI_API_KEY" },
        baseUrl: "https://api.openai.com/v1",  // Optional: Custom Endpoint
        headers: { "X-Custom": "value" },      // Optional: Custom Headers
        batch: { enabled: true, concurrency: 2 }, // Batch-API für große Korpora
      },

      // Lokale Embeddings
      local: {
        modelPath: null,  // Oder "hf:ggml-org/embeddinggemma-300m-qat-q8_0-GGUF/..."
      },

      // Zusätzliche Pfade
      extraPaths: ["../team-docs", "/srv/shared-notes"],

      // Embedding-Cache
      cache: {
        enabled: true,
        maxEntries: 50000,
      },
    },
  },
}
```

---

## Hybrid Search (BM25 + Vektor)

Kombiniert semantische Ähnlichkeit mit exakten Keyword-Matches:

```json5
agents: {
  defaults: {
    memorySearch: {
      query: {
        hybrid: {
          enabled: true,
          vectorWeight: 0.7,       // 0-1, Gewicht für Vektor-Score
          textWeight: 0.3,         // 0-1, Gewicht für BM25-Score
          candidateMultiplier: 4,  // Kandidaten-Pool = maxResults * multiplier
        },
      },
    },
  },
}
```

### Warum Hybrid?

- **Vektor-Suche** gut für: "Mac Studio gateway host" ≈ "the machine running the gateway"
- **BM25** gut für: exakte IDs (`a828e60`), Code-Symbole, Fehlerstrings

---

## MMR Re-Ranking (Diversität)

Vermeidet redundante Ergebnisse mit Maximal Marginal Relevance:

```json5
memorySearch: {
  query: {
    hybrid: {
      mmr: {
        enabled: true,
        lambda: 0.7,  // 0 = max Diversität, 1 = max Relevanz
      },
    },
  },
}
```

**Beispiel**: Suche nach "home network setup"
- Ohne MMR: 5 fast identische Ergebnisse
- Mit MMR: Diverse Ergebnisse (Router-Config, AdGuard, VLAN-Setup)

---

## Temporal Decay (Aktualität)

Bevorzugt aktuelle Memory-Einträge:

```json5
memorySearch: {
  query: {
    hybrid: {
      temporalDecay: {
        enabled: true,
        halfLifeDays: 30,  // Score halbiert sich alle 30 Tage
      },
    },
  },
}
```

**Decay-Berechnung**: `decayedScore = score × e^(-λ × ageInDays)`

**Evergreen-Dateien** werden nicht decayed:
- `MEMORY.md`
- Nicht-datierte Dateien in `memory/` (z.B. `memory/projects.md`)

---

## QMD Backend (Experimental)

Alternatives Such-Backend mit BM25 + Vektor + Reranking:

```json5
memory: {
  backend: "qmd",
  citations: "auto",  // "auto" | "on" | "off"
  qmd: {
    command: "qmd",  // Oder Pfad zum Binary
    searchMode: "search",  // "search" | "vsearch" | "query"
    includeDefaultMemory: true,

    paths: [
      { name: "docs", path: "~/notes", pattern: "**/*.md" },
    ],

    sessions: {
      enabled: true,
      retentionDays: 30,
      exportDir: "~/.openclaw/agents/<id>/qmd/sessions",
    },

    update: {
      interval: "5m",
      debounceMs: 15000,
      onBoot: true,
    },

    limits: {
      maxResults: 6,
      maxSnippetChars: 700,
      timeoutMs: 4000,
    },

    scope: {
      default: "deny",
      rules: [
        { action: "allow", match: { chatType: "direct" } },
        { action: "deny", match: { keyPrefix: "discord:channel:" } },
      ],
    },
  },
}
```

### QMD-Details

- **Installation**: `bun install -g https://github.com/tobi/qmd`
- **SQLite**: Muss Extension-Unterstützung haben (`brew install sqlite` auf macOS)
- **Modelle**: Auto-Download von HuggingFace bei erstem `qmd query`
- **Fallback**: Bei QMD-Fehler wird automatisch auf SQLite-Backend zurückgefallen

---

## Multimodal Memory (Gemini Embedding 2)

Indexiert Bilder und Audio (nur mit Gemini Embedding 2):

```json5
agents: {
  defaults: {
    memorySearch: {
      provider: "gemini",
      model: "gemini-embedding-2-preview",
      multimodal: {
        enabled: true,
        modalities: ["image", "audio"],  // Oder ["all"]
        maxFileBytes: 10000000,          // 10 MB Limit
      },
      extraPaths: ["assets/reference", "voice-notes"],
      fallback: "none",  // Multimodal erfordert "none"
    },
  },
}
```

**Unterstützte Formate**:
- Bilder: `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.heic`, `.heif`
- Audio: `.mp3`, `.wav`, `.ogg`, `.opus`, `.m4a`, `.aac`, `.flac`

---

## Session Memory Search (Experimental)

Indexiert Session-Transkripte für Recall:

```json5
agents: {
  defaults: {
    memorySearch: {
      experimental: { sessionMemory: true },
      sources: ["memory", "sessions"],
      sync: {
        sessions: {
          deltaBytes: 100000,    // ~100 KB
          deltaMessages: 50,     // JSONL-Zeilen
        },
      },
    },
  },
}
```

**Hinweis**: Session-Indexierung ist opt-in und läuft asynchron.

---

## Embedding Cache

Vermeidet erneutes Embedding unveränderter Texte:

```json5
agents: {
  defaults: {
    memorySearch: {
      cache: {
        enabled: true,
        maxEntries: 50000,  // ~50K Chunks
      },
    },
  },
}
```

---

## SQLite Vector Acceleration (sqlite-vec)

Beschleunigt Vektor-Suche in SQLite:

```json5
agents: {
  defaults: {
    memorySearch: {
      store: {
        vector: {
          enabled: true,  // Default: true
          extensionPath: "/path/to/sqlite-vec",  // Optional
        },
      },
    },
  },
}
```

---

## Was indexiert wird

| Dateityp | Indexiert |
|----------|-----------|
| `MEMORY.md` | ✅ |
| `memory/**/*.md` | ✅ |
| `extraPaths` (Markdown) | ✅ |
| `extraPaths` (Bilder/Audio) | ✅ (nur Gemini Embedding 2) |
| Session-Transkripte | ✅ (experimental, opt-in) |

**Index-Speicherort**: `~/.openclaw/memory/<agentId>.sqlite`

---

## Troubleshooting

### Memory-Tools nicht verfügbar

```bash
# Prüfen ob memorySearch aktiviert ist
openclaw config get agents.defaults.memorySearch.enabled

# Provider prüfen
openclaw config get agents.defaults.memorySearch.provider
```

### Embedding-Fehler

```bash
# OpenAI-Key setzen
export OPENAI_API_KEY="sk-..."

# Oder in Config
openclaw config set agents.defaults.memorySearch.provider openai
```

### QMD-Binary nicht gefunden

```bash
# Installieren
bun install -g https://github.com/tobi/qmd

# Oder fallback auf SQLite
openclaw config set memory.backend sqlite
```

### Re-Index erzwingen

```bash
# Index zurücksetzen (bei Provider/Modell-Wechsel)
rm ~/.openclaw/memory/<agentId>.sqlite

# Gateway neu starten
systemctl --user restart openclaw-gateway
```

---

## CLI-Befehle

```bash
# Memory flush (manuell)
openclaw memory flush

# Sessions auflisten
openclaw sessions list

# Sessions bereinigen
openclaw sessions clean
```

---

## Best Practices

1. **Memory schreiben**: Bei Entscheidungen, Präferenzen, wichtigen Fakten → in `MEMORY.md`
2. **Tagesnotizen**: In `memory/YYYY-MM-DD.md` (append-only)
3. **Bei "Merke dir das"**: Agent bitten, in Memory zu schreiben
4. **MEMORY.md privat halten**: Niemals in Group-Sessions laden
5. **Hybrid + MMR + Decay aktivieren**: Beste Recall-Qualität

---

## Referenz

- Docs: https://docs.openclaw.ai/concepts/memory
- Companion Skill: `cognee-openclaw-memory` für Knowledge-Graph-Memory