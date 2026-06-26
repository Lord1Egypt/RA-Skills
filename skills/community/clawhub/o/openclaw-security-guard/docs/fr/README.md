# 📖 OpenClaw Security Guard - Documentation

<div align="center">

**Documentation Complète en Français**

[🏠 Accueil](./README.md) •
[🚀 Démarrage](./guides/getting-started.md) •
[📋 Référence CLI](./api/cli.md) •
[🇬🇧 English](../en/README.md) •
[🇲🇦 العربية](../ar/README.md)

</div>

---

## Table des Matières

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Démarrage Rapide](#démarrage-rapide)
4. [Fonctionnalités](#fonctionnalités)
5. [Référence CLI](#référence-cli)
6. [Dashboard](#dashboard)
7. [Scanners](#scanners)
8. [Configuration](#configuration)
9. [Score de Sécurité](#score-de-sécurité)
10. [Utilisation Programmatique](#utilisation-programmatique)
11. [Bonnes Pratiques](#bonnes-pratiques)
12. [Dépannage](#dépannage)
13. [FAQ](#faq)

---

## Introduction

**OpenClaw Security Guard** est une couche de sécurité complète pour les installations OpenClaw. Il fournit :

- 🔍 **5 Scanners de Sécurité** - Détection de secrets, mauvaises configurations et vulnérabilités
- 📊 **Dashboard Temps Réel** - Monitoring avec protection par mot de passe
- 🔧 **Auto-Fix** - Correction automatique des problèmes courants
- 🌍 **Multi-langue** - Anglais, Français, Arabe

### Pourquoi Vous en Avez Besoin

OpenClaw est puissant, mais les configurations par défaut peuvent exposer votre système à :

| Risque | Sans Guard | Avec Guard |
|--------|------------|------------|
| Clés API exposées | 😰 Inconnu | ✅ Détecté & Masqué |
| Injection de Prompt | 😰 Vulnérable | ✅ Blocage Temps Réel |
| Politique DM ouverte | 😰 N'importe qui peut écrire | ✅ Audit & Alerte |
| Pas de limites de coût | 😰 Dépenses illimitées | ✅ Monitoring des Coûts |
| Sandbox désactivé | 😰 Accès système complet | ✅ Auto-fix Disponible |

### Confidentialité

Cet outil est **100% privé** :

- ❌ Pas de télémétrie
- ❌ Pas de tracking
- ❌ Pas de requêtes externes
- ❌ Pas de collecte de données
- ✅ Tout s'exécute localement
- ✅ Open source - vérifiez vous-même

---

## Installation

### Prérequis

- Node.js 22 ou supérieur
- npm 10 ou supérieur

### Installation Globale (Recommandé)

```bash
npm install -g openclaw-security-guard
```

### Vérifier l'Installation

```bash
openclaw-guard --version
# Sortie: 1.0.0
```

### Utilisation avec npx (Sans Installation)

```bash
npx openclaw-security-guard audit
```

---

## Démarrage Rapide

### 1. Lancez Votre Premier Audit

```bash
openclaw-guard audit
```

Cela va scanner votre installation OpenClaw et afficher un rapport de sécurité :

```
🛡️ OpenClaw Security Guard v1.0.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Scanner de Secrets........ ✅ Aucun problème
🔧 Auditeur de Config........ ❌ 2 critiques
💉 Détecteur d'Injection..... ✅ Aucun problème
📦 Scanner de Dépendances.... ⚠️ 1 avertissement
🔌 Auditeur MCP.............. ✅ Aucun problème
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Score de Sécurité: 65/100
```

### 2. Corriger les Problèmes

```bash
# Mode interactif
openclaw-guard fix

# Mode automatique
openclaw-guard fix --auto
```

### 3. Démarrer le Dashboard

```bash
openclaw-guard dashboard
```

Au premier lancement, vous créerez un mot de passe. Puis accédez à : `http://localhost:18790`

---

## Fonctionnalités

### Scanners de Sécurité

| Scanner | Ce qu'il Fait |
|---------|---------------|
| **Secrets** | Détecte les clés API, tokens, mots de passe dans 15+ formats |
| **Config** | Audite la config OpenClaw contre 15+ règles de sécurité |
| **Prompts** | Détecte 50+ patterns d'injection de prompt |
| **Dépendances** | Vérifie les packages npm vulnérables |
| **Serveurs MCP** | Valide les serveurs MCP installés |

### Dashboard Temps Réel

- Score de sécurité en temps réel
- Monitoring des requêtes
- Suivi des coûts
- Détection des menaces
- Flux d'alertes
- Protégé par mot de passe

### Auto-Fix

- Sauvegarde avant les changements
- Mode interactif ou automatique
- Journal détaillé des modifications

---

## Référence CLI

### Options Globales

```bash
openclaw-guard [commande] [options]

Options:
  -V, --version         Affiche le numéro de version
  -c, --config <path>   Chemin vers le fichier de config
  -l, --lang <lang>     Langue (en|fr|ar)
  -v, --verbose         Sortie détaillée
  -q, --quiet           Mode silencieux (sans bannière)
  -h, --help            Affiche l'aide
```

### Commandes

#### `audit` - Lancer un Audit de Sécurité

```bash
openclaw-guard audit [options]

Options:
  --deep               Scan approfondi (plus lent mais complet)
  --quick              Scan rapide
  -o, --output <path>  Fichier de sortie
  -f, --format <fmt>   Format: text|json|html|md (défaut: text)
  --ci                 Mode CI (exit 1 si problèmes critiques)
```

**Exemples:**

```bash
# Audit basique
openclaw-guard audit

# Audit approfondi avec rapport HTML
openclaw-guard audit --deep -o rapport.html -f html

# Intégration CI/CD
openclaw-guard audit --ci
```

#### `dashboard` - Démarrer le Dashboard

```bash
openclaw-guard dashboard [options]

Options:
  -p, --port <port>     Port du dashboard (défaut: 18790)
  -g, --gateway <url>   URL de la Gateway OpenClaw (défaut: ws://127.0.0.1:18789)
  --no-browser          Ne pas ouvrir le navigateur automatiquement
```

#### `fix` - Corriger les Problèmes de Sécurité

```bash
openclaw-guard fix [options]

Options:
  --auto         Auto-fix sans confirmation
  --interactive  Mode interactif (défaut)
  --backup       Créer une sauvegarde avant les changements (défaut: true)
  --dry-run      Prévisualiser sans appliquer
```

#### `scan` - Lancer des Scanners Individuels

```bash
openclaw-guard scan <scanner> [options]

Scanners:
  secrets     Scanner les secrets exposés
  config      Auditer la configuration
  prompts     Détecter les patterns d'injection
```

#### `report` - Générer un Rapport

```bash
openclaw-guard report [options]

Options:
  -f, --format <fmt>    Format: html|json|md (défaut: html)
  -o, --output <path>   Chemin de sortie (défaut: ./security-report)
```

#### `hooks` - Gérer les Git Hooks

```bash
openclaw-guard hooks <action>

Actions:
  install      Installer le hook pre-commit
  uninstall    Supprimer le hook pre-commit
  status       Vérifier si le hook est installé
```

---

## Dashboard

### Configuration Initiale

1. Lancez `openclaw-guard dashboard`
2. Le navigateur s'ouvre sur `http://localhost:18790`
3. Vous verrez la page **Setup**
4. Créez un mot de passe (minimum 8 caractères)
5. Vous êtes connecté !

### Lancements Suivants

1. Lancez `openclaw-guard dashboard`
2. Le navigateur s'ouvre sur la page **Login**
3. Entrez votre mot de passe
4. Accédez au dashboard

### Fonctionnalités du Dashboard

| Fonctionnalité | Description |
|----------------|-------------|
| **Score de Sécurité** | Score 0-100 avec code couleur |
| **Requêtes/min** | Compteur de requêtes en temps réel |
| **Coût du Jour** | Suivi des coûts API |
| **Menaces** | Tentatives d'injection, rate limits, bloqués |
| **Statut Config** | Sandbox, DM policy, gateway, etc. |
| **Alertes** | Alertes de sécurité récentes |

### Réinitialisation du Mot de Passe

Si vous oubliez votre mot de passe, supprimez le fichier de config :

```bash
rm ~/.openclaw-security-guard/auth.json
```

Puis redémarrez le dashboard pour créer un nouveau mot de passe.

---

## Scanners

### Scanner de Secrets

Détecte les secrets exposés dans votre répertoire OpenClaw.

**Patterns Détectés:**

| Type | Exemple de Pattern |
|------|-------------------|
| OpenAI | `sk-...` |
| Anthropic | `sk-ant-...` |
| AWS | `AKIA...` |
| GitHub | `ghp_...`, `gho_...` |
| Slack | `xoxb-...`, `xoxp-...` |
| Stripe | `sk_live_...` |
| Clés Privées | `-----BEGIN RSA PRIVATE KEY-----` |
| Générique | Chaînes à haute entropie |

### Auditeur de Config

Valide la configuration OpenClaw selon les bonnes pratiques de sécurité.

**Règles Vérifiées:**

| Règle | Sévérité | Recommandation |
|-------|----------|----------------|
| Mode sandbox | Critique | Définir sur `always` |
| Politique DM | Haute | Définir sur `pairing` |
| Bind gateway | Critique | Définir sur `loopback` |
| Mode élevé | Haute | Désactiver |
| Rate limiting | Moyenne | Activer |

### Détecteur d'Injection de Prompt

Détecte les patterns d'injection de prompt dans les logs et messages.

**Catégories:**

1. **Override d'Instructions** - "ignore previous instructions"
2. **Manipulation de Rôle** - "you are now DAN"
3. **Prompt Système** - "system: ..."
4. **Jailbreak** - Phrases de jailbreak connues
5. **Exécution de Code** - Tentatives d'exécution de code
6. **Extraction de Données** - Tentatives d'extraction de données

---

## Configuration

### Emplacement du Fichier de Config

Créez `.openclaw-guard.json` dans :
- Répertoire du projet (priorité la plus haute)
- Répertoire home (`~/.openclaw-guard.json`)

### Configuration Complète

```json
{
  "scanners": {
    "secrets": {
      "enabled": true,
      "exclude": ["*.test.js", "node_modules/**", "*.log"]
    },
    "config": {
      "enabled": true,
      "strict": false
    },
    "prompts": {
      "enabled": true,
      "sensitivity": "medium"
    }
  },
  "dashboard": {
    "port": 18790,
    "openBrowser": true
  },
  "reporting": {
    "format": "html",
    "outputDir": "./security-reports"
  }
}
```

---

## Score de Sécurité

### Comment Il Est Calculé

Votre score de sécurité commence à 100 et diminue selon les problèmes :

| Facteur | Points Déduits |
|---------|----------------|
| Sandbox pas `always` | -20 |
| Politique DM est `open` | -15 |
| Gateway sur IP publique | -15 |
| Mode élevé activé | -10 |
| Rate limiting désactivé | -5 |
| Chaque finding critique | -10 |
| Chaque finding haute | -5 |
| Chaque finding moyenne | -2 |

### Plages de Score

| Score | Statut | Icône |
|-------|--------|-------|
| 80-100 | Sain | 🟢 |
| 60-79 | Attention Requise | 🟡 |
| 0-59 | Problèmes Critiques | 🔴 |

---

## Utilisation Programmatique

### Installation

```bash
npm install openclaw-security-guard
```

### Audit Rapide

```javascript
import { quickAudit } from 'openclaw-security-guard';

const results = await quickAudit('~/.openclaw');
console.log(`Score de Sécurité: ${results.securityScore}/100`);
console.log(`Critique: ${results.summary.critical}`);
console.log(`Haute: ${results.summary.high}`);
```

### Vérifier l'Injection de Prompt

```javascript
import { checkPromptInjection } from 'openclaw-security-guard';

const result = await checkPromptInjection('ignore all previous instructions');

if (!result.safe) {
  console.log('Injection détectée!');
  console.log('Patterns:', result.matches);
}
```

---

## Bonnes Pratiques

### 1. Audits Réguliers

```bash
# Ajouter à crontab pour des audits quotidiens
0 9 * * * openclaw-guard audit --quiet -o /var/log/openclaw-audit.json -f json
```

### 2. Intégration CI/CD

```yaml
# .github/workflows/security.yml
name: Audit de Sécurité
on: [push, pull_request]
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
      - run: npm install -g openclaw-security-guard
      - run: openclaw-guard audit --ci
```

### 3. Pre-commit Hooks

```bash
openclaw-guard hooks install
```

Cela empêche de commiter des secrets accidentellement.

---

## Dépannage

### "Command not found"

```bash
# Vérifier si npm bin est dans le PATH
echo $PATH | grep npm

# Ou utiliser npx
npx openclaw-security-guard audit
```

### "Permission denied"

```bash
# Corriger les permissions npm
npm config set prefix ~/.npm-global
export PATH=~/.npm-global/bin:$PATH
```

### Le Dashboard ne s'ouvre pas

```bash
# Vérifier si le port est utilisé
lsof -i :18790

# Utiliser un port différent
openclaw-guard dashboard --port 3001
```

---

## FAQ

### Mes données sont-elles envoyées quelque part ?

**Non.** Cet outil ne fait aucune requête externe. Tout s'exécute localement. Pas de télémétrie, pas de tracking, pas d'analytics.

### Puis-je l'utiliser en production ?

**Oui.** Cet outil est conçu pour une utilisation en production. Le dashboard est protégé par mot de passe et se lie uniquement à localhost.

### Comment mettre à jour ?

```bash
npm update -g openclaw-security-guard
```

### Puis-je contribuer ?

**Oui !** Voir [CONTRIBUTING.md](../CONTRIBUTING.md)

### Où signaler les bugs ?

Ouvrez une issue sur [GitHub](https://github.com/2pidata/openclaw-security-guard/issues)

### Qui a créé ceci ?

**Miloud Belarebia** - [2pidata.com](https://2pidata.com)

---

## Support

- 📖 [Documentation](https://github.com/2pidata/openclaw-security-guard/docs)
- 🐛 [Signaler un Bug](https://github.com/2pidata/openclaw-security-guard/issues)
- 💡 [Demander une Fonctionnalité](https://github.com/2pidata/openclaw-security-guard/issues)
- 🌐 [Site Web](https://2pidata.com)

---

<div align="center">

**Fait avec ❤️ par [Miloud Belarebia](https://github.com/2pidata)**

[2pidata.com](https://2pidata.com) • #databelarebia 🇲🇦

</div>
