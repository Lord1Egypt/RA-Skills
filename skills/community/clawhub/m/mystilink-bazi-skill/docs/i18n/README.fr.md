# Mystilink BaZi Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## Vue d’ensemble

Agent Skill pour le BaZi (Quatre Piliers) : calcule piliers, DaYun et LiuNian à partir des données de naissance via des scripts intégrés, puis interprète à l’aide de pages théoriques (maître du jour, dix dieux, concepts associés). Les scripts de calcul de thème sont sous `scripts/`.

## Type de livraison

Ce dépôt est un paquet **Agent Skill** (`SKILL.md` + `scripts/` + `references/` + `examples/`). Il n’implémente **pas** la matrice de langages C / C++ / C# / Java / JavaScript / Python des bibliothèques calculatrices. Pour un SDK/CLI multi-langues, voir le projet frère `mystilink-bazi-calculator` (optionnel ; non requis pour exécuter ce skill).

## Prérequis

- Python 3.9+ (`zoneinfo`)
- Hôte compatible Agent Skills
- Réseau optionnel pour l’API Mystilink Wiki pendant l’interprétation

## Installation

Installer sous le nom de dossier `mystilink-bazi` (correspond au `name` de `SKILL.md`) :

| Hôte | Chemin |
|------|------|
| Cursor | `.cursor/skills/mystilink-bazi/` |
| Claude Code | `.claude/skills/mystilink-bazi/` |

```bash
cp -R mystilink-bazi-skill /path/to/.cursor/skills/mystilink-bazi
```

## Démarrage rapide (scripts)

Depuis le répertoire du skill :

```bash
python3 scripts/bazi_calculate.py --date 1990-05-15 --hour 12
python3 scripts/bazi_calculate.py --birth-json examples/profile.v0.json
python3 scripts/bazi_calculate.py --profile-json examples/profile.json
python3 scripts/bazi_dayun_calculate.py --date 1990-05-15 --gender female --count 8
python3 scripts/bazi_liunian_calculate.py --year 2026 --day-stem 甲
```

Succès : JSON sur stdout. Échec : code de sortie non nul et JSON `{"error":…}`.

Les objets pilier incluent `stem_index`, `branch_index`, `text`, et l’ancien champ `ganzhi` (`=` `text`).

## Flux de travail

1. Collecter le profil de naissance — soit :
   - `examples/profile.v0.json` (`mystilink.birth/0.1` BirthProfile), ou
   - `examples/profile.json` (champs skill hérités)
2. Exécuter les scripts de thème selon besoin (`--birth-json` / `--profile-json` acceptent les deux formes)
3. Interpréter avec Wiki (optionnel) :

```text
GET https://wiki.mystilink.com/api/v1/search?q=day+master&system=bazi&locale=en
GET https://wiki.mystilink.com/api/v1/pages/bazi.concept.ri-zhu?locale=en
```

4. Séparer les **faits du thème** de l’**interprétation** ; citer la provenance Wiki le cas échéant

Instructions agent complètes : `SKILL.md`. Ids courts : `references/wiki-ids.md`.

## Exemples

- `examples/profile.v0.json` — BirthProfile (`mystilink.birth/0.1`, fictif)
- `examples/profile.json` — profil de naissance hérité (fictif) ; toujours accepté par les scripts

## Limites

- Les scripts sont des copies intégrées pour une installation skill autonome ; ce n’est pas un SDK multi-langues
- Les dates de termes solaires DaYun utilisent des jours civils approximatifs
- Le temps solaire vrai nécessite fuseau horaire et longitude
- Locale Wiki : omettre → `en` ; traductions manquantes peuvent basculer vers `zh-Hans`

## Licence

MIT. Voir [LICENSE](../../LICENSE).

## Retours

Signalez les défauts avec la commande exacte (dates fictives uniquement) et le JSON stdout/stderr.
