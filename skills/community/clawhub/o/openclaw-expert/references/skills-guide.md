# Skills — Entwicklung, Installation & Sicherheit

## Skill-Typen

| Typ | Pfad | Beschreibung |
|---|---|---|
| Bundled | Im npm-Paket | Mitgelieferte Skills |
| Managed | `~/.openclaw/skills/` | Via ClawHub installiert |
| Workspace | `<workspace>/skills/` | Manuell erstellt, pro Agent |

**Präzedenz bei Namenskonflikten:**
`<workspace>/skills` (höchste) → `~/.openclaw/skills` → bundled skills (niedrigste)

Zusätzliche Skill-Ordner (niedrigste Präzedenz) via `skills.load.extraDirs` in `openclaw.json`.

---

## Multi-Agent & Shared Skills

- **Per-Agent-Skills** liegen in `<workspace>/skills` — nur für diesen Agent sichtbar
- **Shared-Skills** liegen in `~/.openclaw/skills` — für alle Agents auf dieser Maschine
- **Shared-Folders** via `skills.load.extraDirs` — gemeinsamer Skill-Pack für mehrere Agents

---

## ClawHub — Registry & Sync

ClawHub ist die öffentliche Skills-Registry: **https://clawhub.com**

### Installieren

```bash
# Skill suchen
clawhub search "memory"
clawhub search "calendar"

# Installieren (default: ./skills oder fallback workspace)
clawhub install <skill-slug>

# Update
clawhub update <skill-slug>
clawhub update --all

# Nach Installation: Skills neu laden
openclaw skills reload
# ODER Gateway neu starten (Skills sind erst in neuer Session aktiv!)
openclaw gateway restart

# Installierte Skills anzeigen
openclaw skills list
```

### Sync (Publish)

```bash
# Alle Skills scannen + Updates publishen
clawhub sync --all
```

---

## SKILL.md-Format (AgentSkills-kompatibel)

### Minimales Frontmatter

```markdown
---
name: mein-skill
description: Beschreibung was der Skill tut und wann er getriggert werden soll.
---
```

**Pflichtfelder:**
- `name` — Nur Buchstaben, Zahlen, Bindestriche
- `description` — Wann der Skill aktiviert werden soll (Trigger-Phrasen)

**Wichtig:** Der Parser unterstützt **nur Single-Line** Frontmatter-Keys.

### Volles Frontmatter mit Metadata

```markdown
---
name: image-lab
description: Generate or edit images via a provider-backed image workflow
metadata:
  {
    "openclaw":
      {
        "emoji": "🖼️",
        "requires": { "bins": ["uv"], "env": ["GEMINI_API_KEY"], "config": ["browser.enabled"] },
        "primaryEnv": "GEMINI_API_KEY",
        "os": ["darwin", "linux"],
        "homepage": "https://example.com/skill",
        "always": false,
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "ripgrep",
              "bins": ["rg"],
              "label": "Install ripgrep (brew)",
            },
          ],
      },
  }
---
```

### Metadata-Felder (`metadata.openclaw`)

| Feld | Typ | Beschreibung |
|---|---|---|
| `always` | boolean | Skill immer laden (skip andere Gates) |
| `emoji` | string | Emoji für macOS Skills UI |
| `homepage` | string | URL für "Website" in macOS Skills UI |
| `os` | string[] | Plattform-Filter: `darwin`, `linux`, `win32` |
| `requires.bins` | string[] | Binaries, die auf PATH existieren müssen |
| `requires.anyBins` | string[] | Mindestens eines muss existieren |
| `requires.env` | string[] | Env-Vars, die existieren ODER in Config gesetzt sein müssen |
| `requires.config` | string[] | `openclaw.json`-Pfade, die truthy sein müssen |
| `primaryEnv` | string | Env-Var für `skills.entries.<name>.apiKey` |
| `install` | array | Installer-Specs für macOS Skills UI |

### Optional User-Invocable Flags

| Flag | Default | Beschreibung |
|---|---|---|
| `user-invocable` | `true` | Skill als `/slash-command` verfügbar |
| `disable-model-invocation` | `false` | Skill nicht im Model-Prompt laden |
| `command-dispatch` | — | `tool` für direkten Tool-Dispatch |
| `command-tool` | — | Tool-Name für `command-dispatch: tool` |
| `command-arg-mode` | `raw` | Args-Handling für Tool-Dispatch |

### Verzeichnis-Struktur

```
mein-skill/
├── SKILL.md           # Pflicht: Anweisungen
├── scripts/           # Optional: Ausführbare Skripte
├── references/        # Optional: Referenz-Dokumente
└── assets/            # Optional: Templates, Icons
```

### Workspace-Skills erstellen

```bash
mkdir -p ~/.openclaw/workspace/skills/mein-skill
# SKILL.md dort anlegen
openclaw skills reload
```

---

## Skill-Gating (Load-Time Filter)

OpenClaw filtert Skills beim Laden basierend auf `metadata.openclaw.requires`:

### Requirements-Check

```json5
{
  "requires": {
    "bins": ["uv", "python3"],        // Alle müssen auf PATH sein
    "anyBins": ["node", "bun"],      // Mindestens eines muss existieren
    "env": ["GEMINI_API_KEY"],       // Env-Var muss existieren oder in Config
    "config": ["browser.enabled"],   // openclaw.json-Pfad muss truthy sein
  },
}
```

**Wichtig bei Sandbox:**
- `requires.bins` wird auf dem HOST geprüft (Load-Time)
- In Sandbox muss Binary zusätzlich IM CONTAINER existieren
- Installiere via `agents.defaults.sandbox.docker.setupCommand`
- `setupCommand` braucht: `network != "none"`, `readOnlyRoot: false`, `user: "0:0"`

### Installer-Specs

```json5
{
  "install":
    [
      {
        "id": "brew",
        "kind": "brew",
        "formula": "ripgrep",
        "bins": ["rg"],
        "label": "Install ripgrep (brew)",
      },
      {
        "id": "npm",
        "kind": "node",
        "package": "typescript",
        "bins": ["tsc"],
        "label": "Install TypeScript (npm)",
      },
      {
        "id": "download",
        "kind": "download",
        "url": "https://example.com/binary",
        "archive": "tar.gz",
        "targetDir": "~/.openclaw/tools/my-skill",
      },
    ],
}
```

**Installer-Logik:**
- Gateway wählt EINEN bevorzugten Installer (brew > node > go > download)
- Mehrere `download`-Specs werden alle gelistet
- `os: ["darwin"]` filtert Optionen nach Plattform
- `skills.install.nodeManager` in Config: `npm` (default), `pnpm`, `yarn`, `bun`

---

## Config-Overrides

```json5
{
  skills: {
    install: {
      nodeManager: "pnpm",  // npm | pnpm | yarn | bun
    },
    load: {
      extraDirs: ["/path/to/shared/skills"],
      watch: true,
      watchDebounceMs: 250,
    },
    entries: {
      "my-skill": {
        enabled: true,
        apiKey: { source: "env", provider: "default", id: "MY_API_KEY" },
        env: { MY_VAR: "value" },
        config: { endpoint: "https://example.com" },
      },
      "peekaboo": { enabled: true },
      "sag": { enabled: false },
    },
    allowBundled: ["skill-one", "skill-two"],  // Optional: bundled-Skills-Allowlist
  },
}
```

**Regeln:**
- `enabled: false` deaktiviert Skill (auch bundled)
- `env` wird nur injiziert wenn Var nicht bereits gesetzt
- `apiKey` kann Plaintext-String ODER SecretRef sein
- `config`: Custom-Fields für Per-Skill-Konfig
- `allowBundled`: Allowlist für bundled Skills (managed/workspace Skills nicht betroffen)

---

## Environment-Injection (Per-Agent-Run)

Beim Start eines Agent-Runs:
1. Skill-Metadaten lesen
2. `skills.entries.<key>.env` und `apiKey` auf `process.env` anwenden
3. System-Prompt mit **eligible** Skills bauen
4. Originale Environment nach Run-Ende wiederherstellen

**Scoped to Agent-Run**, nicht global!

---

## Session-Snapshot (Performance)

OpenClaw snapshottet **eligible Skills beim Session-Start** und re-used die Liste für folgende Turns in der gleichen Session.

Änderungen an Skills oder Config greifen in der nächsten neuen Session.

Skills können auch mid-Session refreshen (Skills Watcher oder neuer Remote-Node).

---

## Remote macOS Nodes (Linux Gateway)

Wenn Gateway auf Linux läuft, aber ein macOS Node verbunden ist mit `system.run` erlaubt:
- macOS-only Skills werden als eligible behandelt, wenn Binary auf Node existiert
- Agent führt Skills via `nodes` tool aus (`nodes.run`)
- Skills bleiben sichtbar wenn Node offline geht; Invocations schlagen fehl bis Reconnect

---

## Security-Hinweise

### Risiko-Bewertung

- **26% der Community-Skills** enthalten mind. eine Schwachstelle (Cisco)
- Risiken: Prompt-Injections, Tool-Poisoning, versteckte Malware in `scripts/`
- Unsichere Datenverarbeitung

### Schutzmaßnahmen

1. **Quellcode reviewen** vor Installation
2. **ClawHub "Hide Suspicious"** aktivieren
3. **VirusTotal-Report** auf ClawHub-Seite prüfen
4. **Code in Claude einfügen** und nach Risiken fragen
5. **Sandbox nutzen**: `agents.defaults.sandbox.mode: "non-main"`
6. **Nur verifizierte Skills** von bekannten Autoren installieren

### Secret-Handling

```json5
// Env-Injection läuft im HOST-Prozess (nicht Sandbox!)
skills: {
  entries: {
    "my-skill": {
      apiKey: { source: "env", provider: "default", id: "MY_API_KEY" },
      // NICHT in prompts/logs verwenden!
    },
  },
}
```

---

## Token-Impact (Skills List)

Eligible Skills werden als kompakte XML-Liste in den System-Prompt injiziert.

**Kosten-Formel (Zeichen):**
```
total = 195 + Σ (97 + len(name_escaped) + len(description_escaped) + len(location_escaped))
```

**Beispiel:**
- Base overhead: 195 Zeichen
- Per Skill: 97 Zeichen + XML-escaped Feldlängen
- ~97 Zeichen ≈ 24 Tokens (OpenAI-style Tokenizer)

---

## Skills Watcher (Auto-Refresh)

```json5
skills: {
  load: {
    watch: true,
    watchDebounceMs: 250,
  },
}
```

Watcht Skill-Folder und updated Snapshot bei `SKILL.md`-Änderungen.

---

## CLI-Referenz

```bash
# Skills auflisten
openclaw skills list

# Skills neu laden (nach Installation)
openclaw skills reload

# ClawHub
clawhub search <query>
clawhub install <slug>
clawhub update <slug>
clawhub update --all
clawhub sync --all
```

---

## Troubleshooting

| Problem | Lösung |
|---|---|
| Skill nicht sichtbar | `openclaw skills list` → SKILL.md-Format prüfen (name + description im YAML) |
| Skill nicht aktiv nach Installation | `openclaw gateway restart` (Skills erst in neuer Session!) |
| Nur 1 von 6 Skills registriert | YAML-Syntax-Fehler (Doppelpunkt in description escapen) |
| Binary nicht gefunden in Sandbox | `setupCommand` mit `network: "bridge"`, `readOnlyRoot: false`, `user: "0:0"` |
| `requires.bins` Check schlägt fehl | Binary auf HOST vorhanden? In Sandbox separat installieren |
| Skill disabled trotz Config | `enabled: true` explizit setzen |
| Env nicht injiziert | Var bereits in `process.env`? Check: `skills.entries.<name>.env` |

---

## Verwandte Docs

- **Quick-Ref**: `references/quick-reference.md` — Skills-CLI Einzeiler
- **Config**: `references/config-reference.md` — skills.* Schema
- **Security**: `references/security-hardening.md` — Skill Security & Gating
- **CLI**: `references/cli-reference.md` — `openclaw skills` und `clawhub` Befehle