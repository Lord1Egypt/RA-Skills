# Mystilink Zi Wei Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## Vue d’ensemble

Agent Skill pour Zi Wei Dou Shu : construit un thème à douze palais (Si Hua optionnelle) avec un script Python intégré, puis interprète avec des pages théoriques. Le calcul de thème est sous `scripts/`.

## Type de livraison

Paquet **Agent Skill**. N’implémente **pas** la matrice de langages des calculatrices (C / C++ / C# / Java / JS / Python SDK). Frère optionnel : `mystilink-ziwei-calculator`.

## Prérequis

- Python 3.9+
- `pip install zhdate`
- Hôte compatible Agent Skills
- Réseau optionnel pour l’API Wiki

## Installation

Le nom de dossier doit être `mystilink-ziwei` :

```bash
cp -R mystilink-ziwei-skill /path/to/.cursor/skills/mystilink-ziwei
```

| Hôte | Chemin |
|------|------|
| Cursor | `.cursor/skills/mystilink-ziwei/` |
| Claude Code | `.claude/skills/mystilink-ziwei/` |

## Démarrage rapide

```bash
python3 scripts/ziwei_chart_calculate.py \
  --datetime "1990-05-15 14:30" \
  --timezone Asia/Shanghai \
  --gender female \
  --output json

python3 scripts/ziwei_chart_calculate.py \
  --birth-json examples/profile.v0.json \
  --output json
```

Options : `--si-hua`, `--year YYYY`, `--longitude E`, `--midnight-zi`.

Succès : JSON sur stdout. Échec : sortie non nulle + JSON error.

## Flux de travail

1. Collecter les données de naissance — `examples/profile.v0.json` (BirthProfile) ou hérité `examples/profile.json`
2. Exécuter le script de thème
3. Wiki optionnel :

```text
GET https://wiki.mystilink.com/api/v1/search?q=life+palace&system=ziwei&locale=en
GET https://wiki.mystilink.com/api/v1/pages/ziwei.concept.ming-gong?locale=en
```

4. Séparer faits du thème et interprétation

Détails : `SKILL.md`. Orientation : `references/overview.md`.

## Exemples

- `examples/profile.v0.json` — BirthProfile (`mystilink.birth/0.1`, fictif)
- `examples/profile.json` — entrées de naissance héritées fictives

## Limites

- Dépend de `zhdate` pour la conversion lunaire
- Script intégré pour usage skill autonome, pas un SDK multi-langues
- Locale Wiki omise → `en` ; repli éventuel `zh-Hans`

## Licence

MIT. Voir [LICENSE](../../LICENSE).

## Retours

Inclure la commande exacte (datetime fictif) et la sortie/erreur JSON.
