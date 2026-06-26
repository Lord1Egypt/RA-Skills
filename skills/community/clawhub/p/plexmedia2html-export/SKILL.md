---
name: plexmedia2html-export
description: "Exports Plex Media Library (Movies & TV Shows) as static HTML pages. Features: Multilingual (EN/DE), token obfuscation (machine-bound), genre filter, detail popups. | Exportiert Plex Mediathek (Filme & Serien) als statische HTML-Seiten. Features: Multilingual (EN/DE), Token-Obfuskierung (maschinengebunden), Genre-Filter, Detail-Popups."
language: ["en", "de"]
---

# PlexMedia2HTML Export v1.2.3

**[English](#english) | [Deutsch](#deutsch)**

---

<a name="english"></a>
## 🇬🇧 English

Exports your Plex Media Library as static HTML pages.

### Features v1.2.3

- 🎬 **Movies & TV Shows** beautifully displayed
- 🏷️ **Genre Filter** for quick finding
- 🔍 **Detail Popups** with all metadata
- 🌍 **Multilingual** – English & German
- 🔐 **Token Obfuscation** – Machine-bound (not true encryption)
- 📱 **Responsive Design** for all devices
- ⚡ **Fast** – no Plex login required after export

### Installation

Requires Python 3.8+. **No external dependencies** needed.

```bash
# Install via ClawHub
clawhub install plexmedia2html-export

# Or manually copy and make executable
chmod +x ~/.openclaw/workspace/skills/plexmedia2html-export/plex-export
```

The `plex-export` wrapper is ready to use.

### Onboarding

The following values will be requested on first run:

#### 1. Plex Server URL
```
Example: http://192.168.1.100:32400
```

#### 2. Plex Token
```
1. Open Plex Web → Settings → General → Advanced
2. Click "Show Token"
3. Copy the token here
```

**Note:** The token is obfuscated with a machine-specific key (not truly encrypted).

#### 3. Language
```
en (English) or de (German)
```

#### 4. Export Path (optional)
```
Default: ~/Exports/
```

### Configuration

Configuration is stored in `~/.openclaw/workspace/data/plexmedia2html-export/config.json`:

```json
{
  "plex_url": "http://192.168.1.100:32400",
  "plex_token_encrypted": "BASE64_ENCRYPTED_TOKEN",
  "export_path": "~/Exports",
  "movies_per_page": 18,
  "series_per_page": 18,
  "language": "en"
}
```

**Important:** The Plex token is never stored in plain text!

### Usage

```bash
# First export
plex-export

# With self-signed certificate (disable SSL verification)
plex-export --insecure

# As cron job (daily at 2 AM)
0 2 * * * /usr/bin/python3 ~/.openclaw/workspace/skills/plexmedia2html-export/export.py
```

---

<a name="deutsch"></a>
## 🇩🇪 Deutsch

Exportiert deine Plex Mediathek als statische HTML-Seiten.

### Features v1.2.3

- 🎬 **Filme & Serien** übersichtlich dargestellt
- 🏷️ **Genre-Filter** für schnelles Finden
- 🔍 **Detail-Popups** mit allen Metadaten
- 🌍 **Multilingual** – Englisch & Deutsch
- 🔐 **Token-Obfuskierung** – Maschinengebunden (nicht echte Verschlüsselung)
- 📱 **Responsive Design** für alle Geräte
- ⚡ **Offline-fähig** – Cover-Bilder werden lokal gespeichert

### Installation

Der Skill benötigt Python 3.8+ und hat **keine externen Dependencies**.

```bash
# Skill installieren (via ClawHub)
clawhub install plexmedia2html-export

# Oder manuell kopieren und ausführbar machen
chmod +x ~/.openclaw/workspace/skills/plexmedia2html-export/plex-export
```

Der Wrapper `plex-export` ist direkt ausführbar.

### Onboarding

Beim ersten Aufruf werden folgende Werte abgefragt:

#### 1. Plex-Server URL
```
Beispiel: http://192.168.1.100:32400
```

#### 2. Plex Token
```
1. Öffne Plex Web → Einstellungen → Allgemein → Erweitert
2. Klicke auf "Token anzeigen"
3. Kopiere den Token hierhin
```

**Hinweis:** Der Token wird obfuskiert mit einem maschinenspezifischen Schlüssel gespeichert (nicht verschlüsselt).

#### 3. Sprache
```
en (Englisch) oder de (Deutsch)
```

#### 4. Export-Pfad (optional)
```
Standard: ~/Exports/
```

### Konfiguration

Die Konfiguration wird in `~/.openclaw/workspace/data/plexmedia2html-export/config.json` gespeichert:

```json
{
  "plex_url": "http://192.168.1.100:32400",
  "plex_token_encrypted": "BASE64_ENCRYPTED_TOKEN",
  "export_path": "~/Exports",
  "movies_per_page": 18,
  "series_per_page": 18,
  "language": "de"
}
```

**Wichtig:** Der Plex-Token wird nie im Klartext gespeichert!

### Nutzung

```bash
# Erstmaliger Export
plex-export

# Mit selbst-signiertem Zertifikat (SSL-Verification deaktivieren)
plex-export --insecure

# Als Cron-Job (täglich um 2 Uhr)
0 2 * * * /usr/bin/python3 ~/.openclaw/workspace/skills/plexmedia2html-export/export.py
```

---

## Security / Sicherheit

**Privacy Note:**
- The skill reads `/etc/machine-id` (Linux) or derives a fallback from hostname+username
- This is used to bind the obfuscated token to the current machine
- No data is transmitted; the ID is only used locally for the obfuscation key

**Token Storage (Obfuscation):**
- Tokens are obfuscated using XOR + Base64
- Obfuscation key is derived from `/etc/machine-id` or hostname+username
- Token cannot be deobfuscated on a different machine
- This is **not encryption** — it prevents casual snooping but not determined attackers
- For true security, use OS keyring or manually enter password each time

**SSL/TLS:**
- By default, SSL certificate verification is enabled (secure)
- Use `--insecure` flag only for self-signed certificates (not recommended)

**File Permissions:**
- Config file is automatically set to `chmod 600` (owner read/write only)
- After first run, verify: `ls -la ~/.openclaw/workspace/data/plexmedia2html-export/config.json`

---

## Lizenz / License

**MIT** – Frei verwendbar und modifizierbar / Free to use and modify.

**Versions:**
- v1.2.3 – English default language, fixed navigation links
- v1.2.2 – SSL verification enabled by default, file permissions enforced, --insecure flag
- v1.2.1 – Fixed imports, honest documentation
- v1.2.0 – Token obfuscation + Multilingual + Bug fixes
- v1.1.0 – Multilingual support
- v1.0.0 – Initial release
