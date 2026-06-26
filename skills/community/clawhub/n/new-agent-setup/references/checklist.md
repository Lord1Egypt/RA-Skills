# New Agent Setup — Vollständige Anleitung

**Erstellt:** 2026-03-05  
**Autor:** Gus  

---

## Phase 1: Informationen sammeln

Bevor ich irgendetwas konfiguriere, frage ich folgende Informationen ab:

### Von Tom benötigt:

**Agent-Identität:**
- [ ] **Name** (mit Grossbuchstaben, z.B. "Saul") → Agent-ID wird automatisch kleingeschrieben ("saul")
- [ ] **Rolle / Aufgabenbereich** (kurze Beschreibung)
- [ ] **Emoji** für die Identity (z.B. ⚖️)

**Discord:**
- [ ] **Bot Token** — aus dem Discord Developer Portal (`https://discord.com/developers/applications` → App → Bot → Token)
- [ ] **Bot/Application ID** — aus dem Developer Portal (App → General Information → Application ID)
- [ ] **Discord Channel ID** — nach Channel-Erstellung (siehe Phase 2)

**Optional:**
- [ ] Modell-Override (falls nicht Standard `anthropic/claude-sonnet-4-6`)

---

## Phase 2: Manuelle Vorbereitungen (durch Tom)

Diese Schritte müssen VOR meiner Konfiguration abgeschlossen sein:

### 2.1 Discord Bot einrichten

1. Auf `https://discord.com/developers/applications` gehen
2. "New Application" → Name = Agent-Name (z.B. "Saul")
3. Bot-Tab → "Add Bot" → Token kopieren und sicher aufbewahren
4. Application ID notieren (General Information)
5. Bot zum Server einladen:
   - OAuth2 → URL Generator → Scopes: `bot`
   - Bot Permissions: mindestens `Send Messages`, `Read Messages/View Channels`, `Read Message History`
   - Generierten Link öffnen und Bot zum Server hinzufügen

### 2.2 Discord Channel erstellen

1. Im Discord-Server einen neuen Text-Channel erstellen, Name = **kleingeschriebene Agent-ID** (z.B. `saul`)
2. Channel in die Kategorie **"Agent Direct Lines"** verschieben
3. Berechtigungen mit der Kategorie synchronisieren (Rechtsklick → "Sync Permissions")
4. Den neu eingeladenen Bot-User zu den Channel-Berechtigungen hinzufügen
5. Dem Bot-User **alle Berechtigungen auf Allow** setzen
6. Die Discord Channel ID notieren (Rechtsklick auf Channel → "Copy Channel ID")

### 2.3 Avatar-Bild vorbereiten

- Datei: `avatar-<agent-id>.png` (z.B. `avatar-saul.png`)
- Transparenter Hintergrund
- Muss nach der Einrichtung in den Workspace-Ordner kopiert werden: `~/.openclaw/workspace-<agent-id>/`

---

## Phase 3: Konfiguration (durch Gus, nach Bestätigung von Tom)

Erst wenn Tom alle Schritte aus Phase 2 abgeschlossen und bestätigt hat.

### 3.1 Backup
```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup-$(date +%Y%m%d-%H%M%S)
```

### 3.2 openclaw.json konfigurieren

Folgende Bereiche müssen ergänzt werden:

**a) Agent in `agents.list[]`:**
```json5
{
  "id": "<agent-id>",          // kleingeschrieben, z.B. "saul"
  "name": "<Agent-Name>",      // mit Grossbuchstaben, z.B. "Saul"
  "workspace": "/home/tom/.openclaw/workspace-<agent-id>",
  "identity": {
    "name": "<Agent-Name>",
    "emoji": "<emoji>"
  },
  "heartbeat": {
    "every": "60m",
    "target": "discord",
    "to": "channel:<discord-channel-id>"
  }
}
```

**b) Discord Account hinzufügen (`channels.discord.accounts`):**
```json5
"<agent-id>": {
  "token": "<bot-token>"
}
```

**c) Discord Channel-Routing (`channels.discord.guilds.<guild-id>.channels`):**
```json5
"<discord-channel-id>": {
  "allow": true,
  "requireMention": false
}
```

**d) Agent-Routing-Regel (`agentRouting` oder `routing`):**
```json5
{
  "agentId": "<agent-id>",
  "match": {
    "channel": "discord",
    "accountId": "<agent-id>"
  }
}
```

### 3.3 Gateway neu starten
```bash
openclaw gateway restart
```

### 3.4 Mission Control registrieren
```bash
MC_AGENT=<agent-id> ~/.openclaw/skills/mission-control/mc register <agent-id> --role "<Rolle>"
```

### 3.5 HEARTBEAT.md erstellen
Datei: `~/.openclaw/workspace-<agent-id>/HEARTBEAT.md`

```markdown
# HEARTBEAT.md

## 1. Mission Control (always first)
* Run: `MC_AGENT=<agent-id> ~/.openclaw/skills/mission-control/mc inbox --unread`
* Run: `MC_AGENT=<agent-id> ~/.openclaw/skills/mission-control/mc list --status pending`
* Run: `MC_AGENT=<agent-id> ~/.openclaw/skills/mission-control/mc checkin`
* Claim and work on any pending tasks assigned to <agent-id>

## 2. <Rollen-spezifische Checks>
* ...

## 3. Task Completion
* After completing a task: `MC_AGENT=<agent-id> ~/.openclaw/skills/mission-control/mc done <id> -m "what I did"`
* For urgent tasks: notify Gus via sessions_send at `agent:gus:discord:channel:1478790371902492916`

## Rules
* Late night (11pm to 7am): Only work on tasks, do not send unsolicited messages
* If nothing needs attention: respond HEARTBEAT_OK
* Do not message Tom directly — go through Gus
```

**Wichtig:** Niemals leer lassen — leere HEARTBEAT.md = Heartbeat wird übersprungen!

### 3.6 System-Cron ergänzen
Nächsten freien Minuten-Slot wählen (bestehende Belegung prüfen mit `crontab -l`):
```bash
(crontab -l; echo "<minute>,<minute+10>,...  * * * * MC_AGENT=<agent-id> ~/.openclaw/skills/mission-control/mc checkin >> ~/.openclaw/logs/mc-checkin.log 2>&1") | crontab -
```

Aktuelle Belegung:
- Minute 0: gus
- Minute 1: walt
- Minute 2: jesse
- Minute 3: skyler
- Minute 4: mike
- **Minute 5: nächster Agent**

### 3.7 MEMORY.md erstellen ⚠️ PFLICHT

Datei: `~/.openclaw/workspace-<agent-id>/MEMORY.md`

```markdown
# MEMORY.md — Long Term Memory

**Purpose:** Durable facts, active projects, and pointers. Details live in daily files — semantic search holt sie wenn gebraucht.
**Regel:** Niemals vollständigen Projektinhalt hier ablegen. Nur: Was existiert + Suchbegriff für `memory_search`.

---

## Memory-Regel: Projektkontext

Details von Projekten **nicht** vollständig hier ablegen — das bläht den Context auf.
Stattdessen: kurzer Pointer-Eintrag + `memory_search("Projektname")` wenn Details gebraucht werden.

Beispiel:
- **p-xyz** — Kurzbeschreibung → Details: `memory_search("p-xyz")`

---

Review and update this file regularly. Daily files (memory/YYYY-MM-DD.md) are raw notes. This file is curated pointers.
```

### 3.8 Session-Key in MEMORY.md speichern
Format: `<agent-id>=\`agent:<agent-id>:discord:channel:<channel-id>\``

### 3.8 Onboarding-Message senden
Via `sessions_send` mit `timeoutSeconds: 30` — mc-Workflow, Pfad, Gus Session-Key erklären.

---

## Phase 3b: OneDrive-Zugriff (optional, nach Rückfrage)

Vor der Einrichtung fragen:
> "Soll der neue Agent OneDrive-Zugriff erhalten? Wenn ja, auf welche Libraries?"

Aktuell verfügbare Libraries:
- `assistants` → `~/.openclaw/onedrive/assistants/` (gemeinsamer Arbeitsordner aller Agents)

Falls ja:

1. **Ordner im Workspace anlegen:**
```bash
mkdir -p ~/.openclaw/workspace-<agent-id>/onedrive
```

2. **Symlink pro Library erstellen:**
```bash
ln -sf ~/.openclaw/onedrive/<library> ~/.openclaw/workspace-<agent-id>/onedrive/<library>
```

3. **Agent anweisen**, seinen eigenen Unterordner anzulegen:
```bash
# z.B. für assistants:
mkdir ~/.openclaw/onedrive/assistants/<Agent-Name>/
```

4. **Verifizieren**, dass die Datei unter `~/.openclaw/onedrive/assistants/<Agent-Name>/` erscheint und von Tom auf seinem Laptop sichtbar ist.

**Hinweis:** Symlinks zeigen immer auf den absoluten Pfad `~/.openclaw/onedrive/<library>` — nicht auf `~/OneDrive/` oder andere Pfade.

## Phase 4: Abschlusskontrolle

- [ ] `mc fleet` zeigt neuen Agent
- [ ] Gateway läuft fehlerfrei (`openclaw gateway status`)
- [ ] MEMORY.md erstellt (mit Pointer-Regel)
- [ ] HEARTBEAT.md nicht leer
- [ ] Crontab korrekt gestaffelt (`crontab -l`)
- [ ] Session-Key in MEMORY.md eingetragen
- [ ] Agent hat Onboarding bestätigt
- [ ] Avatar-Bild liegt in `~/.openclaw/workspace-<agent-id>/avatar-<agent-id>.png`
- [ ] Tom weiss: Avatar-Bild muss noch kopiert werden falls nicht geschehen
- [ ] OneDrive-Zugriff: Symlinks korrekt gesetzt (falls gewünscht)
- [ ] Agent hat eigenen Unterordner in `assistants/` angelegt und Test-Datei abgelegt
- [ ] Tom kann die Datei auf seinem Laptop sehen

---

## Namenskonvention

| Feld | Format | Beispiel |
|------|--------|---------|
| Discord Bot Name | Grossbuchstabe | "Saul" |
| Agent-ID | Kleinbuchstaben | "saul" |
| Workspace-Ordner | `workspace-<agent-id>` | `workspace-saul` |
| Avatar-Datei | `avatar-<agent-id>.png` | `avatar-saul.png` |
| Session-Key | `agent:<agent-id>:discord:channel:<id>` | `agent:saul:discord:channel:123...` |
