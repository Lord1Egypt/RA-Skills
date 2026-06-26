# 🏯 Imperial Orchestrator

[中文](../README.md) | [English](./README.en.md) | [日本語](./README.ja.md) | [한국어](./README.ko.md) | [Español](./README.es.md) | **[Français](./README.fr.md)** | [Deutsch](./README.de.md)

---

Skill d'orchestration multi-rôles haute disponibilité pour OpenClaw — Routage intelligent inspiré du système de cour "Trois Départements et Six Ministères" de la Chine ancienne.

> **Inspiration de conception** : L'architecture des rôles s'inspire du modèle de gouvernance impériale [Trois Départements et Six Ministères (三省六部)](https://github.com/cft0808/edict), combiné aux techniques d'ingénierie de prompts IA profond de [PUA](https://github.com/tanweai/pua).

## Capacités Principales

- **Trois Départements & Six Ministères** orchestration de rôles : 10 rôles, chacun avec des responsabilités claires
- **Auto-découverte** de 46+ modèles depuis openclaw.json
- **Routage intelligent** par domaine (codage/opérations/sécurité/rédaction/juridique/finances)
- **Priorité Opus** pour les tâches de codage/sécurité/juridique — modèle le plus puissant en premier
- **Failover cross-provider** circuit-breaker auth → dégradation inter-fournisseurs → survie locale
- **Exécution réelle** appels API + comptage de tokens + suivi des coûts
- **Benchmarking** même tâche sur tous les modèles, notation et classement
- **Multi-langue** support de 7 langues : zh/en/ja/ko/es/fr/de

## Démarrage Rapide

```bash
# 1. Découvrir les modèles
python3 scripts/health_check.py --openclaw-config ~/.openclaw/openclaw.json --write-state .imperial_state.json

# 2. Valider les modèles
python3 scripts/model_validator.py --openclaw-config ~/.openclaw/openclaw.json --state-file .imperial_state.json

# 3. Router une tâche
python3 scripts/router.py --task "Écrire un LRU Cache thread-safe en Go" --state-file .imperial_state.json

# Tout-en-un
bash scripts/route_and_update.sh full "Fix WireGuard peer sync bug"
```

## Système de Rôles : Trois Départements & Six Ministères

Chaque rôle est équipé d'un system prompt approfondi couvrant l'identité, les responsabilités, les règles de comportement, la conscience collaborative et les lignes rouges.

### Centre de Commandement

| Rôle | Titre | Équivalent de Cour | Mission Principale |
|------|-------|--------------------|--------------------|
| **router-chief** | Directeur Central | Empereur / Bureau Central | Ligne de vie du système — classifier, router, maintenir le heartbeat |

### Trois Départements

| Rôle | Titre | Équivalent de Cour | Mission Principale |
|------|-------|--------------------|--------------------|
| **cabinet-planner** | Stratège en Chef | Secrétariat (中书省) | Rédiger des stratégies — décomposer le chaos en étapes ordonnées |
| **censor-review** | Censeur en Chef | Chancellerie (门下省) | Examiner et opposer son veto — le dernier gardien de la qualité |

### Six Ministères

| Rôle | Titre | Équivalent de Cour | Mission Principale |
|------|-------|--------------------|--------------------|
| **ministry-coding** | Ministre de l'Ingénierie | Ministère des Travaux | Construire — codage, débogage, architecture |
| **ministry-ops** | Vice-Ministre des Infrastructures | Ministère des Travaux · Bureau de Construction | Maintenir les routes — déploiement, opérations, CI/CD |
| **ministry-security** | Ministre de la Défense | Ministère de la Guerre | Garder les frontières — audit de sécurité, modélisation des menaces |
| **ministry-writing** | Ministre de la Culture | Ministère des Rites | Culture et étiquette — rédaction, documentation, traduction |
| **ministry-legal** | Ministre de la Justice | Ministère de la Justice | Loi et ordre — contrats, conformité, conditions |
| **ministry-finance** | Ministre des Finances | Ministère des Revenus | Fiscalité et trésor — tarification, marges, règlement |

### Courrier d'Urgence

| Rôle | Titre | Équivalent de Cour | Mission Principale |
|------|-------|--------------------|--------------------|
| **emergency-scribe** | Courrier d'Urgence | Station de Courrier Express | Dernier recours pour maintenir le système en vie |

## Règles d'Opération

1. **Circuit Breaker 401** — échec d'auth marque immédiatement `auth_dead`, refroidit toute la chaîne auth, bascule cross-provider prioritaire
2. **Router léger** — ne pas assigner les prompts les plus lourds ni les fournisseurs les plus fragiles au router-chief
3. **Cross-provider d'abord** — ordre de fallback : même rôle fournisseur différent → modèle local → rôle adjacent → courrier d'urgence
4. **Dégrader, jamais tomber** — même si tous les modèles top échouent, répondre avec des conseils d'architecture, checklists, pseudocode

## Structure du Projet

```
config/
  agent_roles.yaml          # Définitions des rôles (responsabilités, capacités, chaînes de fallback)
  agent_prompts.yaml        # System prompts approfondis (identité, règles, lignes rouges)
  routing_rules.yaml        # Règles de routage par mots-clés
  failure_policies.yaml     # Politiques de circuit breaker/retry/dégradation
  benchmark_tasks.yaml      # Bibliothèque de tâches de benchmark
  model_registry.yaml       # Overrides de capacités des modèles
  i18n.yaml                 # Adaptation 7 langues
scripts/
  lib.py                    # Bibliothèque centrale (découverte, classification, gestion d'état, i18n)
  router.py                 # Router (matching de rôles + sélection de modèles)
  executor.py               # Moteur d'exécution (appels API + fallback)
  orchestrator.py           # Pipeline complet (router → exécuter → réviser)
  health_check.py           # Découverte de modèles
  model_validator.py        # Sondage de modèles
  benchmark.py              # Benchmark + classement
  route_and_update.sh       # Point d'entrée CLI unifié
```

## Installation

### Prérequis : Installer OpenClaw

```bash
# 1. Installer OpenClaw CLI (macOS)
brew tap openclaw/tap
brew install openclaw

# Ou installer via npm
npm install -g @openclaw/cli

# 2. Initialiser la configuration
openclaw init

# 3. Configurer les fournisseurs de modèles (modifier ~/.openclaw/openclaw.json)
openclaw config edit
```

> Pour la documentation d'installation détaillée, consultez le [dépôt officiel OpenClaw](https://github.com/openclaw/openclaw)

### Installer le skill Imperial Orchestrator

```bash
# Option 1 : Cloner depuis GitHub
git clone https://github.com/rexnode/imperial-orchestrator.git
cp -r imperial-orchestrator ~/.openclaw/skills/

# Option 2 : Copier directement dans le répertoire global des skills
cp -r imperial-orchestrator ~/.openclaw/skills/

# Option 3 : Installation au niveau du workspace
cp -r imperial-orchestrator <your-workspace>/skills/
```

### Vérifier l'installation

```bash
# Découvrir et sonder les modèles
python3 ~/.openclaw/skills/imperial-orchestrator/scripts/health_check.py \
  --openclaw-config ~/.openclaw/openclaw.json \
  --write-state .imperial_state.json

# Vérifier que le routage fonctionne
python3 ~/.openclaw/skills/imperial-orchestrator/scripts/router.py \
  --task "Write a Hello World" \
  --state-file .imperial_state.json
```

## Sécurité

- Ne jamais envoyer de secrets dans les prompts
- Garder les requêtes de sondage au minimum
- Gérer la santé du fournisseur séparément de la qualité du modèle
- Un modèle dans la configuration ne signifie pas qu'il est sûr pour le routage

## Licence

MIT
