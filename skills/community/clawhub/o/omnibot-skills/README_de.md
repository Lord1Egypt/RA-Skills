<div align="center">

# 🤖 Omnibot

### Browser-Infrastruktur für KI-Agenten

[![Version](https://img.shields.io/badge/version-2.4.0-blue?style=flat-square)](./SKILL.md)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square)]()

[![SkillHub](https://img.shields.io/badge/SkillHub-omnibot-00A8E0?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNOCAwTDAgNFYxMkw4IDE2TDE2IDEyVjRMOCAwWiIgZmlsbD0id2hpdGUiLz48L3N2Zz4=)](https://skillhub.cn/skills/omnibot)
[![ClawHub](https://img.shields.io/badge/ClawHub-omnibot--skills-FF6B35?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNOCAxQzQuMTMgMSAxIDQuMTMgMSA4QzEgMTEuODcgNC4xMyAxNSA4IDE1QzExLjg3IDE1IDE1IDExLjg3IDE1IDhDMTUgNC4xMyAxMS44NyAxIDggMVpNOCAzQzkuNjYgMyAxMSA0LjM0IDExIDZDMTEgNy42NiA5LjY2IDkgOCA5QzYuMzQgOSA1IDcuNjYgNSA2QzUgNC4zNCA2LjM0IDMgOCAzWiIgZmlsbD0id2hpdGUiLz48L3N2Zz4=)](https://clawhub.ai/dennisjcy/skills/omnibot-skills)

[![Chrome Web Store](https://img.shields.io/badge/Chrome%20Web%20Store-Browser--Erweiterung-4285F4?style=flat-square&logo=google-chrome&logoColor=white)](https://chromewebstore.google.com/detail/fojlpefamkmjbboafmjkkaejohagbdgn)

**Verbinden Sie KI-Agenten mit einem echten Chromium-Browser.**<br>
Lesen Sie Seiten. Klicken Sie auf Schaltflächen. Füllen Sie Formulare aus. Navigieren Sie. Extrahieren Sie Inhalte. Sammeln Sie Beweise.<br>
Alles über einen lokalen Daemon und CLI — keine Headless-Hacks, keine fragilen Selektoren.

[Schnellstart](#-schnellstart) · [Wie Es Funktioniert](#-wie-es-funktioniert) · [Funktionen](#-funktionen) · [Dokumentation](#-dokumentation)

🌐 **[English](./README.md)** · **[中文](./README_zh.md)** · **[日本語](./README_ja.md)** · **[한국어](./README_ko.md)** · **[Español](./README_es.md)** · **[Français](./README_fr.md)**

</div>

---

## 🚀 Was ist Omnibot?

Omnibot überbrückt die Lücke zwischen KI-Agenten und dem echten Web. Es gibt Agenten wie **Hermes**, **Claude Code**, **Codex**, **OpenCode** und anderen die Fähigkeit, einen lebenden Chromium-Browser zu sehen und zu interagieren — genauso wie ein Mensch.

```
┌──────────────┐         ┌──────────────┐         ┌──────────────────┐
│   AI Agent   │ ──CLI──▶│  Omnibot     │ ──WS──▶ │  Chromium        │
│  (Hermes,    │         │  Daemon      │         │  Erweiterung     │
│   Claude...) │         │  :18765      │         │  (Echter Browser)│
└──────────────┘         └──────────────┘         └──────────────────┘
```

Kein Puppeteer. Kein Playwright. Kein Headless-Browser, der vorgibt, echt zu sein.<br>
**Ein echter Browser. Echte Cookies. Echte Erweiterungen. Echte Benutzer-Sitzungen.**

## 🎬 Video-Demonstrationen

<table>
<tr>
<td width="50%" align="center" valign="top">

### WeChat Official Account Analyse
**Hermes analysiert automatisch WeChat-Backend-Daten & Trends**

[![WeChat-Analyse](https://img.youtube.com/vi/xZ-_0TInCRE/maxresdefault.jpg)](https://youtu.be/xZ-_0TInCRE)

*Der Hermes-Agent meldet sich automatisch am WeChat Official Account-Backend an, extrahiert Benutzerwachstum, Artikel-Lesungen, Benutzerdemografie und erstellt einen vollständigen Datenanalysebericht.*

</td>
<td width="50%" align="center" valign="top">

### X (Twitter) KI-Nachrichten-Aggregator
**Hermes durchsucht X automatisch nach neuesten KI-Nachrichten**

[![X KI-Nachrichten](https://img.youtube.com/vi/PknnOhAE6bI/maxresdefault.jpg)](https://youtu.be/PknnOhAE6bI)

*Der Hermes-Agent durchsucht automatisch X (Twitter), sucht und filtert die neuesten KI-Nachrichten und organisiert sie in einem strukturierten Nachrichten-Briefing.*

</td>
</tr>
<tr>
<td width="50%" align="center" valign="top">

### Gerichtsprotokoll-Analyse
**Hermes sucht und analysiert Mordurteile**

[![Gerichtsanalyse](https://img.youtube.com/vi/PQQNDbzgXgQ/maxresdefault.jpg)](https://youtu.be/PQQNDbzgXgQ)

*Der Hermes-Agent durchsucht Gerichtsakten nach Mordfällen, liest 8 vollständige Falldateien und erstellt einen umfassenden Analysebericht mit Täterprofilen, Motiv-Analyse und Verbrechensmustern.*

</td>
<td width="50%" align="center" valign="top">

### Toutiao Auto-Publishing
**Hermes veröffentlicht automatisch Artikel auf Toutiao**

[![Toutiao-Veröffentlichung](https://img.youtube.com/vi/elUxHLp1C4Q/maxresdefault.jpg)](https://youtu.be/elUxHLp1C4Q)

*Der Hermes-Agent meldet sich automatisch bei Toutiao an, füllt Titel und Text aus, fügt Bilder ein, konfiguriert Cover und Werbeeinnahmen, zeigt eine Vorschau und veröffentlicht den Artikel mit einem Klick.*

</td>
</tr>
</table>

<div align="center">

**Weitere Anwendungsfälle warten auf Sie!**

</div>

## ✨ Funktionen

<table>
<tr>
<td width="50%" valign="top">

### 🔍 Beobachten
- Liest gerenderten Seiteninhalt als sauberen Text/Markdown
- Erstellt Schnappschüsse des vollständigen Barrierefreiheitsbaums mit interaktiven Referenzen
- Erfasst Screenshots von vollständigen Seiten oder bestimmten visuellen Bereichen
- Inspeziert Konsolenprotokolle, Netzwerkverkehr und DOM-Zustand

</td>
<td width="50%" valign="top">

### 🎯 Handeln
- Klickt auf Elemente nach semantischer Rolle, Platzhalter oder Barrierefreiheitsreferenz
- Füllt Formulare aus, wählt Optionen aus, markiert Kontrollkästchen — mit Ereignisversand
- Navigiert zwischen Seiten, verwaltet Tabs und Tab-Gruppen
- Zieht, scrollt, tippt, drückt Tasten — menschliche Interaktion

</td>
</tr>
<tr>
<td width="50%" valign="top">

### ✅ Überprüfen
- Wartet auf Bedingungen: URL-Änderungen, Elementsichtbarkeit, Texterscheinung
- Bestätigt Elementzustand: aktiviert, sichtbar, markiert, Wert
- Erfasst Netzwerkprotokolle und API-Beweise
- Mehrstufige Überprüfung mit Beobachten → Handeln → Überprüfen-Schleifen

</td>
<td width="50%" valign="top">

### 🛡️ Zuverlässig
- Sitzungs-Token-Workflow-Isolation
- Tab-gezielte Befehle — keine versehentlichen Cross-Tab-Mutationen
- 7-stufige Fallback-Kette von semantisch bis roh-CDP
- Integrierte Anti-Pattern-Wächter und Sicherheitsregeln

</td>
</tr>
</table>

## ⚡ Schnellstart

### 1. CLI installieren

Installieren Sie Omnibot CLI global über npm (empfohlen):

```bash
npm install -g @omniaibot/omnibot
```

Es erkennt automatisch Ihre Plattform und installiert die entsprechende Binärdatei. Führen Sie nach der Installation `omnibot doctor` aus, um die Installation zu überprüfen.

### 2. Browser-Erweiterung laden

- Öffnen Sie die [Omnibot-Erweiterungsseite im Chrome Web Store](https://chromewebstore.google.com/detail/fojlpefamkmjbboafmjkkaejohagbdgn)
- Klicken Sie auf **Zu Chrome hinzufügen** und schließen Sie die Installation ab
- Klicken Sie auf das Omnibot-Erweiterungssymbol in der oberen rechten Ecke Ihres Browsers
- Bestätigen Sie, dass die Erweiterung **Verbunden** anzeigt, oder kopieren Sie den Maschinencode aus dem Popup, um einen Aktivierungscode zu kaufen

Standardmäßig verbindet sich die Erweiterung mit dem lokalen WebSocket-Dienst unter `127.0.0.1:18765`.

Erweiterungs-Popup-Einstellungen:
- **WebSocket-Adresse**: `ws://127.0.0.1:18765`
- Der Verbindungsstatus wird automatisch aktualisiert
- Wenn die Verbindung fehlschlägt, führen Sie zuerst `omnibot doctor` aus, um den Daemon-Status zu überprüfen

### 3. Verbindung überprüfen

Sie müssen den Daemon nicht manuell starten. Beim Ausführen eines beliebigen Browser-Befehls startet die omnibot CLI automatisch den lokalen Daemon, und die Browser-Erweiterung verbindet sich über WebSocket mit `127.0.0.1:18765`.

```bash
omnibot doctor
omnibot tabs
```

`doctor` überprüft den Daemon- und Erweiterungsstatus. `tabs` listet die verfügbaren Browser-Tabs auf.

Wenn `doctor` anzeigt, dass die Erweiterung nicht verbunden ist, öffnen Sie Chrome/Edge, laden oder laden Sie die Browser-Erweiterung neu, und halten Sie mindestens einen HTTP/HTTPS-Tab offen.

### 4. Agent-Skills installieren

Omnibot v2 verwendet Skills anstelle von MCP-Prompt-Injektion:

```bash
omnibot skills install --agent hermes --profile nuwa
omnibot skills install --agent opencode
omnibot skills install --agent claude
omnibot skills install --agent codex
```

Integrierte Skill-Pfade anzeigen:

```bash
omnibot skills path
```

Omnibot kommt mit integrierten Skill-Konfigurationen für beliebte KI-Agenten. Wählen Sie Ihren Agenten von der Schnellstartseite aus, um den Installationsbefehl zu erhalten.

## 🔄 Wie Es Funktioniert

Jede Browser-Operation folgt einer disziplinierten Schleife:

```
  ┌──────────┐      ┌──────────┐      ┌──────────┐
  │ Beobachten│ ───▶ │ Handeln  │ ───▶ │Überprüfen│──┐
  │          │      │ (einmal) │      │          │  │
  └──────────┘      └──────────┘      └──────────┘  │
       ▲                                              │
       └──────────── bei Fehlschlag mit Fallback ─────┘
```

1. **Beobachten** — Schnappschuss der Seite, Inhalt lesen, aktuellen Zustand prüfen
2. **Handeln** — eine Operation mit dem besten verfügbaren Muster ausführen
3. **Überprüfen** — die erwartete Zustandsänderung mit Beweisen bestätigen

Wenn die Überprüfung fehlschlägt, beobachtet der Agent erneut und versucht die nächste Fallback-Stufe. Keine blinden Wiederholungen. Kein Raten.

## 🧩 Nativer Befehlsrouter

Omnibot wählt immer den engsten nativen Befehl für die Aufgabe:

| Absicht | Nativer Befehl | Nicht Das |
|---------|---------------|-----------|
| Seiteninhalt lesen | `read`, `get text` | ~~`execute-js`~~ |
| Auf Schaltfläche klicken | `find --action click`, `click @eN` | ~~`querySelector().click()`~~ |
| Formular ausfüllen | `fill`, `type` | ~~`element.value = "..."`~~ |
| Auf Zustand warten | `wait` | ~~`sleep 3`~~ |
| Scrollen | `scroll`, `scrollintoview` | ~~`window.scrollTo()`~~ |

**Nativ zuerst. JavaScript ist ein Fallback, keine Abkürzung.**

## 🏗️ Architektur

```
Agent Skill (SKILL.md)
    │
    ▼
omnibot CLI  ──────────────────────────────┐
    │                                       │
    ▼                                       ▼
Lokaler Daemon (:18765)             Chromium-Erweiterung
    │                                       │
    ├── Sitzungsverwaltung                  ├── DOM-Zugriff
    ├── Befehlsrouting                      ├── Barrierefreiheitsbaum
    ├── Tab-Verfolgung                      ├── Netzwerk-Abfangung
    └── Workflow-Isolation                  └── Visuelle Bereichserkennung
```

**Wichtige Designprinzipien:**
- **Zuverlässigkeit > Bequemlichkeit** — jede Aktion wird überprüft
- **Expliziter Zustand > Impliziter Zustand** — keine versteckten Annahmen
- **Muster > Befehl** — beginnen Sie mit der Aufgabe, nicht der API
- **Fallback ist erlaubt, aber nie zuerst**

## 📚 Dokumentation

| Ressource | Beschreibung |
|-----------|-------------|
| [SKILL.md](./SKILL.md) | Vollständige Agenten-Ausführungsspezifikation |
| [Befehlsreferenz](./references/command-reference.md) | Vollständige CLI-Befehlssuche |
| [Operationsmuster](./references/operation-patterns.md) | Lesen, Klicken, Ausfüllen, Scrollen, Navigieren, Warten, Extrahieren, Batch |
| [Anti-Pattern](./references/anti-patterns.md) | Häufige Fehler und wie man sie vermeidet |
| [Debugging & Beweise](./references/debugging-and-evidence.md) | Screenshots, Netzwerkprotokolle, Trace, Aufzeichnung/Wiedergabe |
| [Sitzungen & Tabs](./references/session-and-tabs.md) | Workflow-Isolation und Tab-Zielsetzung |
| [Fallback-Operationen](./references/fallback-operations.md) | 7-stufige Fallback-Kette erklärt |

## 🤝 Kompatible Agenten

Omnibot funktioniert mit jedem Agentensystem, das CLI-Befehle ausführen kann:

- 🧠 **Hermes** — native Integration
- 🟠 **Claude Code** — über Skill-Datei
- 📦 **Codex** — über Skill-Datei
- 🔓 **OpenCode** — über Skill-Datei
- 🔧 **Jedes CLI-fähige Agent** — über `omnibot`-Befehle

## 📋 Beispiel-Workflow

```bash
# Workflow-Kontext festlegen
export OMNIBOT_SESSION_TOKEN=research

# Neuen Tab öffnen
omnibot open "https://github.com"

# Seite mit interaktiven Referenzen schnappschüssen
omnibot snapshot -i --tab-id $TAB_ID

# Auf Suchfeld klicken und tippen
omnibot find placeholder "Search GitHub" --action type \
  --action-value "omnibot" --tab-id $TAB_ID

# Enter drücken
omnibot press Enter --tab-id $TAB_ID

# Auf Ergebnisse warten
omnibot wait --text "repositories" --tab-id $TAB_ID

# Ergebnisse lesen
omnibot read --tab-id $TAB_ID
```

## 📄 Lizenz

Proprietär. Siehe LICENSE für Details.

---

<div align="center">

**Gebaut für Agenten, die das Web sehen müssen — nicht nur abrufen.**

[⭐ Auf GitHub markieren](https://github.com/DennisJcy/Omnibot-skills) · [📖 Skill-Spezifikation lesen](./SKILL.md)

</div>
