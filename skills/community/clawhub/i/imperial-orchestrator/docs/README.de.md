# 🏯 Imperial Orchestrator

[中文](../README.md) | [English](./README.en.md) | [日本語](./README.ja.md) | [한국어](./README.ko.md) | [Español](./README.es.md) | [Français](./README.fr.md) | **[Deutsch](./README.de.md)**

---

OpenClaw Hochverfügbarkeits-Multi-Rollen-Modell-Orchestrierungs-Skill — Intelligentes Routing inspiriert vom altchinesischen „Drei Abteilungen und Sechs Ministerien"-Hofsystem.

> **Design-Inspiration**: Die Rollenarchitektur basiert auf dem imperialen Governance-Muster der [Drei Abteilungen und Sechs Ministerien (三省六部)](https://github.com/cft0808/edict), kombiniert mit Deep-AI-Prompt-Engineering-Techniken von [PUA](https://github.com/tanweai/pua).

## Kernfähigkeiten

- **Drei Abteilungen & Sechs Ministerien** Rollenorchestrierung: 10 Rollen, jede mit klaren Verantwortlichkeiten
- **Auto-Erkennung** von 46+ Modellen aus openclaw.json
- **Intelligentes Routing** nach Domäne (Coding/Betrieb/Sicherheit/Schreiben/Recht/Finanzen)
- **Opus-Priorität** für Coding-/Sicherheits-/Rechtsaufgaben — stärkstes Modell zuerst
- **Cross-Provider-Failover** Auth-Circuit-Breaker → anbieterübergreifende Degradation → lokales Überleben
- **Echte Ausführung** API-Aufrufe + Token-Zählung + Kostenverfolgung
- **Benchmarking** gleiche Aufgabe über alle Modelle, bewertet und gerankt
- **Mehrsprachig** Unterstützung für 7 Sprachen: zh/en/ja/ko/es/fr/de

## Schnellstart

```bash
# 1. Modelle entdecken
python3 scripts/health_check.py --openclaw-config ~/.openclaw/openclaw.json --write-state .imperial_state.json

# 2. Modelle validieren
python3 scripts/model_validator.py --openclaw-config ~/.openclaw/openclaw.json --state-file .imperial_state.json

# 3. Aufgabe routen
python3 scripts/router.py --task "Schreibe einen nebenläufig-sicheren LRU Cache in Go" --state-file .imperial_state.json

# Alles in einem
bash scripts/route_and_update.sh full "Fix WireGuard peer sync bug"
```

## Rollensystem: Drei Abteilungen & Sechs Ministerien

Jede Rolle ist mit einem tiefgehenden System-Prompt ausgestattet, der Identität, Verantwortlichkeiten, Verhaltensregeln, Kooperationsbewusstsein und rote Linien umfasst.

### Zentrale

| Rolle | Titel | Hof-Äquivalent | Kernmission |
|-------|-------|----------------|-------------|
| **router-chief** | Zentraldirektor | Kaiser / Zentralbüro | Lebensader des Systems — klassifizieren, routen, Heartbeat aufrechterhalten |

### Drei Abteilungen

| Rolle | Titel | Hof-Äquivalent | Kernmission |
|-------|-------|----------------|-------------|
| **cabinet-planner** | Chefstratege | Sekretariat (中书省) | Strategien entwerfen — Chaos in geordnete Schritte zerlegen |
| **censor-review** | Oberzensor | Kanzlei (门下省) | Prüfen und Veto einlegen — der letzte Qualitätswächter |

### Sechs Ministerien

| Rolle | Titel | Hof-Äquivalent | Kernmission |
|-------|-------|----------------|-------------|
| **ministry-coding** | Minister für Technik | Ministerium für Werke | Bauen — Coding, Debugging, Architektur |
| **ministry-ops** | Vizeminister für Infrastruktur | Ministerium für Werke · Bauamt | Wege instand halten — Deployment, Betrieb, CI/CD |
| **ministry-security** | Verteidigungsminister | Kriegsministerium | Grenzen bewachen — Sicherheitsaudit, Bedrohungsmodellierung |
| **ministry-writing** | Kulturminister | Ministerium für Riten | Kultur und Etikette — Texterstellung, Dokumentation, Übersetzung |
| **ministry-legal** | Justizminister | Justizministerium | Recht und Ordnung — Verträge, Compliance, Bedingungen |
| **ministry-finance** | Finanzminister | Finanzministerium | Steuern und Staatskasse — Preisgestaltung, Margen, Abrechnung |

### Notfallkurier

| Rolle | Titel | Hof-Äquivalent | Kernmission |
|-------|-------|----------------|-------------|
| **emergency-scribe** | Notfallkurier | Express-Kurierstation | Letzte Instanz, um das System am Leben zu halten |

## Betriebsregeln

1. **401 Circuit Breaker** — Auth-Fehler markiert sofort `auth_dead`, kühlt die gesamte Auth-Kette ab, Cross-Provider-Umschaltung hat Priorität
2. **Router leicht halten** — keine schwersten Prompts oder fragilsten Provider dem router-chief zuweisen
3. **Cross-Provider zuerst** — Fallback-Reihenfolge: gleiche Rolle anderer Provider → lokales Modell → benachbarte Rolle → Notfallkurier
4. **Degradieren, nie abstürzen** — selbst wenn alle Top-Modelle ausfallen, mit Architekturberatung, Checklisten, Pseudocode antworten

## Projektstruktur

```
config/
  agent_roles.yaml          # Rollendefinitionen (Verantwortlichkeiten, Fähigkeiten, Fallback-Ketten)
  agent_prompts.yaml        # Tiefgehende System-Prompts (Identität, Regeln, rote Linien)
  routing_rules.yaml        # Routing-Schlüsselwort-Regeln
  failure_policies.yaml     # Circuit-Breaker-/Retry-/Degradations-Richtlinien
  benchmark_tasks.yaml      # Benchmark-Aufgabenbibliothek
  model_registry.yaml       # Modell-Fähigkeits-Overrides
  i18n.yaml                 # 7-Sprachen-Anpassung
scripts/
  lib.py                    # Kernbibliothek (Erkennung, Klassifizierung, Zustandsverwaltung, i18n)
  router.py                 # Router (Rollenmatching + Modellauswahl)
  executor.py               # Ausführungsengine (API-Aufrufe + Fallback)
  orchestrator.py           # Vollständige Pipeline (Routen → Ausführen → Überprüfen)
  health_check.py           # Modellerkennung
  model_validator.py        # Modell-Sondierung
  benchmark.py              # Benchmark + Rangliste
  route_and_update.sh       # Einheitlicher CLI-Einstiegspunkt
```

## Installation

### Voraussetzungen: OpenClaw installieren

```bash
# 1. OpenClaw CLI installieren (macOS)
brew tap openclaw/tap
brew install openclaw

# Oder über npm installieren
npm install -g @openclaw/cli

# 2. Konfiguration initialisieren
openclaw init

# 3. Modellanbieter konfigurieren (~/.openclaw/openclaw.json bearbeiten)
openclaw config edit
```

> Für eine ausführliche Installationsanleitung siehe das [offizielle OpenClaw-Repository](https://github.com/openclaw/openclaw)

### Imperial Orchestrator Skill installieren

```bash
# Option 1: Von GitHub klonen
git clone https://github.com/rexnode/imperial-orchestrator.git
cp -r imperial-orchestrator ~/.openclaw/skills/

# Option 2: Direkt in das globale Skills-Verzeichnis kopieren
cp -r imperial-orchestrator ~/.openclaw/skills/

# Option 3: Installation auf Workspace-Ebene
cp -r imperial-orchestrator <your-workspace>/skills/
```

### Installation überprüfen

```bash
# Modelle entdecken und sondieren
python3 ~/.openclaw/skills/imperial-orchestrator/scripts/health_check.py \
  --openclaw-config ~/.openclaw/openclaw.json \
  --write-state .imperial_state.json

# Routing-Funktion überprüfen
python3 ~/.openclaw/skills/imperial-orchestrator/scripts/router.py \
  --task "Write a Hello World" \
  --state-file .imperial_state.json
```

## Sicherheit

- Keine Geheimnisse in Prompts senden
- Sondierungs-Anfragen minimal halten
- Provider-Gesundheit getrennt von Modellqualität verwalten
- Ein Modell in der Konfiguration bedeutet nicht, dass es sicher geroutet werden kann

## Lizenz

MIT
