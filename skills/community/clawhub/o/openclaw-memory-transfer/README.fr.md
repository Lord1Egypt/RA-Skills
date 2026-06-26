# openclaw-memory-transfer

> **Migration de mémoire sans friction pour OpenClaw.** Récupérez vos souvenirs de ChatGPT, Claude, Gemini, Copilot et plus — en moins de 10 minutes.

[![Powered by MyClaw.ai](https://img.shields.io/badge/Powered%20by-MyClaw.ai-blue)](https://myclaw.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[English](README.md) | [中文](README.zh-CN.md) | [Deutsch](README.de.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [Italiano](README.it.md) | [Español](README.es.md)

---

Vous avez passé des mois (voire des années) avec ChatGPT. Il connaît votre style d'écriture, vos projets, vos préférences. Quand vous passez à OpenClaw, rien de tout cela ne devrait repartir de zéro.

**Memory Transfer** extrait tout ce que votre ancien AI sait de vous, nettoie les données et les importe dans le système de mémoire d'OpenClaw. Dites simplement à votre agent d'où vous venez.

## Utilisation

Dites à votre agent OpenClaw :

```
Je viens de ChatGPT
```

ou :

```
Migrer mes données depuis Gemini
```

Votre agent gère tout — étape par étape, en langage clair.

## Sources supportées

| Source | Méthode | Action requise |
|--------|---------|----------------|
| **ChatGPT** | Export ZIP | Cliquez sur Exporter dans les paramètres, envoyez le ZIP |
| **Claude.ai** | Guidé par prompt | Copiez un prompt, collez le résultat |
| **Gemini** | Guidé par prompt | Copiez un prompt, collez le résultat |
| **Copilot** | Guidé par prompt | Copiez un prompt, collez le résultat |
| **Perplexity** | Guidé par prompt | Copiez un prompt, collez le résultat |
| **Claude Code** | Scan automatique | Rien — automatique |
| **Cursor** | Scan automatique | Rien — automatique |
| **Windsurf** | Scan automatique | Rien — automatique |

## Ce qui est migré

| Catégorie | Destination | Exemples |
|-----------|------------|----------|
| Identité | `USER.md` | Nom, profession, langue, fuseau horaire |
| Style de communication | `USER.md` | Ton d'écriture, préférences de formatage |
| Connaissances | `MEMORY.md` | Projets, expertise, insights |
| Patterns comportementaux | `MEMORY.md` | Workflows, habitudes, corrections |
| Préférences d'outils | `TOOLS.md` | Stack technique, plateformes |

## Installation

```bash
clawhub install openclaw-memory-transfer
```

## Licence

MIT

---

**Powered by [MyClaw.ai](https://myclaw.ai)**
