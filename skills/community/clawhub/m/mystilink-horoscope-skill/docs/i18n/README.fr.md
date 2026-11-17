# Mystilink Horoscope Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## Vue d’ensemble

Agent Skill pour l’astrologie natale occidentale : calcule planètes, maisons et aspects à partir de l’heure et du lieu de naissance via un script intégré, puis interprète avec des pages théoriques.

## Type de livraison

Paquet **Agent Skill**. N’implémente **pas** la matrice de langages des calculatrices. Frère optionnel : `mystilink-horoscope-calculator`.

## Prérequis

- Python 3.9+
- `pip install pyswisseph`
- Hôte compatible Agent Skills
- Réseau optionnel pour l’API Wiki

## Installation

Le nom de dossier doit être `mystilink-horoscope` :

```bash
cp -R mystilink-horoscope-skill /path/to/.cursor/skills/mystilink-horoscope
```

| Hôte | Chemin |
|------|------|
| Cursor | `.cursor/skills/mystilink-horoscope/` |
| Claude Code | `.claude/skills/mystilink-horoscope/` |

## Démarrage rapide

```bash
python3 scripts/astro_chart_calculate.py \
  --datetime "1990-05-15 14:30" \
  --timezone Asia/Shanghai \
  --lat 31.23 --lon 121.47 \
  --output json

python3 scripts/astro_chart_calculate.py \
  --birth-json examples/profile.v0.json \
  --output json
```

Options : `--zodiac tropical|sidereal`, `--true-solar-time`.

Succès : JSON sur stdout. Échec : sortie non nulle + JSON error.

## Flux de travail

1. Collecter les données de naissance — `examples/profile.v0.json` (BirthProfile) ou hérité `examples/profile.json`
2. Exécuter le script natal
3. Wiki optionnel :

```text
GET https://wiki.mystilink.com/api/v1/search?q=ascendant&system=horoscope&locale=en
GET https://wiki.mystilink.com/api/v1/pages/horoscope.concept.natal-chart?locale=en
```

4. Garder les données du thème distinctes de l’interprétation

Détails : `SKILL.md`. Orientation : `references/overview.md`.

## Exemples

- `examples/profile.v0.json` — BirthProfile (`mystilink.birth/0.1`, fictif)
- `examples/profile.json` — entrées natales héritées fictives

## Limites

- Requiert Swiss Ephemeris via `pyswisseph`
- Script intégré pour installation skill, pas un SDK multi-langues
- Locale Wiki omise → `en` ; repli éventuel `zh-Hans`

## Licence

MIT. Voir [LICENSE](../../LICENSE).

## Retours

Inclure la commande exacte (coordonnées/datetime fictifs) et la sortie/erreur JSON.
