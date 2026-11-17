# 🔒 Vibe Codebase Audit - Deutsche Gebrauchsanleitung

## 📋 Übersicht

**Vibe Codebase Audit** ist ein umfassendes Sicherheits-Audit-Tool für KI-generierte Codebasen mit nativer Agenten-Integration, Multi-Provider-Unterstützung und Abhängigkeits-Sicherheits-Scanning.

> 🎉 **NEU in v2.0**: Agent-native Audit (kein API-Schlüssel erforderlich), Multi-Provider-Unterstützung, Abhängigkeits-Scanning, Konfigurations-Audit

---

## ⚡ Schnellstart

### Methode 1: Agent-native Audit (Empfohlen, Keine Einrichtung!)

```python
# Kein API-Schlüssel nötig! Aktuelles Agenten-LLM direkt verwenden
from vibe_audit_enhanced import vibe_audit_enhanced

result = await vibe_audit_enhanced(
    project_path=".",
    primary_provider="agent_llm"  # Aktuelles Agenten-LLM verwenden
)
```

### Methode 2: Mit Ihrem API-Schlüssel

```python
# Eigenen OpenAI/Claude/Andere API verwenden
result = await vibe_audit_enhanced(
    project_path=".",
    primary_provider="openai",  # oder "claude", "ollama", "deepseek"
    fallback_provider="claude"
)
```

### Methode 3: CLI-Verwendung

```bash
# Agenten-LLM verwenden (kein API-Schlüssel)
python vibe_audit_enhanced.py /pfad/zu/projekt --provider agent_llm

# OpenAI verwenden
python vibe_audit_enhanced.py /pfad/zu/projekt --provider openai

# Lokales Ollama-Modell verwenden
python vibe_audit_enhanced.py /pfad/zu/projekt --provider ollama
```

---

## 🆕 Neu in v2.0

### 1. 🤖 Agent-native Integration
- **Keine Einrichtung** - Kein API-Schlüssel erforderlich
- Verwendet die LLM-Verbindung Ihres aktuellen Agenten
- Nahtlose Integration mit OpenCode, Hermes, OpenClaw
- Geringere Kosten - bestehendes Agenten-Abonnement nutzen

### 2. 🔌 Multi-Provider-Unterstützung
- **Agent LLM** - Aktuellen Agenten verwenden (empfohlen)
- **OpenAI** - GPT-4, GPT-4-turbo
- **Claude** - Claude-3 Sonnet/Opus
- **DeepSeek** - Kostengünstige Alternative
- **Qwen/Tongyi** - Alibaba-Modelle
- **Ollama** - Lokale Modelle ausführen (kostenlos!)

### 3. 📦 Abhängigkeits-Sicherheits-Scanning
- Bekannte Schwachstellen (CVE) prüfen
- Veraltete Abhängigkeiten erkennen
- Lizenz-Compliance-Prüfung
- Unterstützung: npm, pip, maven, cargo, go mod

### 4. ⚙️ Konfigurations-Sicherheits-Prüfungen
- Erkenntnung exponierter .env-Dateien
- CORS-Fehlkonfiguration-Erkennung
- Debug-Modus-Erkennung
- SSL-Überprüfungen

---

## 📊 Tool-Vergleich

| Tool | Geschwindigkeit | Genauigkeit | Funktionen | API-Schlüssel | Am besten für |
|------|-----------------|-------------|------------|---------------|---------------|
| `vibe_audit_enhanced` | Mittel-Schnell | Hoch | Alle | Optional | **Produktion** |
| `vibe_audit_scan` | Schnell | Mittel | Basis | Nein | Schnelle Checks |
| `vibe_audit_multi_model` | Langsam | Höchste | AI-Konsens | Ja | Kritische Projekte |
| `vibe_audit_incremental` | Sehr Schnell | Mittel | Git-aware | Optional | CI/CD |

---

## 🌐 Provider-Konfiguration

### Agent LLM (Empfohlen)
```python
# Keine Einrichtung! Direkt verwenden:
primary_provider="agent_llm"
```

### OpenAI
```bash
export OPENAI_API_KEY="sk-..."
```

### Claude
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Ollama (Lokal, Kostenlos)
```bash
# Ollama installieren
curl -fsSL https://ollama.com/install.sh | sh

# Modell herunterladen
ollama pull llama2

# Im Audit verwenden
primary_provider="ollama"
```

---

## 🚨 Risikostufen

| Stufe | Bewertung | Aktion |
|-------|-----------|--------|
| ✅ SICHER | 0 | Bereit zum Veröffentlichen |
| 🟢 NIEDRIG | 1-19 | Geringe Probleme, Überprüfung empfohlen |
| 🟡 MITTEL | 20-49 | Überprüfen und korrigieren vor Veröffentlichung |
| 🟠 HOCH | 50-79 | Signifikante Probleme, Korrekturen erforderlich |
| 🔴 KRITISCH | 80-100 | **NICHT VERÖFFENTLICHEN** |

---

## 🤝 Unterstützte Agenten

- **OpenCode** - Native Skill
- **Hermes** - Plugin
- **OpenClaw** - Modul-Import
- **MCP-Clients** - Protokoll-Unterstützung

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/csmoove530/vibe-codebase-audit/issues)
- **Dokumentation**: Siehe SKILL.md
- **Beispiele**: Siehe examples/ Verzeichnis

---

**Veröffentlichen Sie mit Zuversicht. Auditieren Sie mit Strenge. Codieren Sie in Frieden.** 🚀
