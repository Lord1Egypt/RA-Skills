# Mystilink Tarot Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## Vue d’ensemble

Agent Skill pour le tarot : tire des cartes droites/renversées pour un tirage avec un script Node intégré, puis interprète via des pages de théorie des cartes. Préférez un tirage réel (script ou cartes fournies par l’utilisateur) ; n’inventez pas de tirages en silence.

## Type de livraison

Paquet **Agent Skill**. N’implémente **pas** la matrice de langages des calculatrices. La logique de tirage/validation est intégrée uniquement dans `scripts/` (pas de dépôt calculateur tarot séparé).

## Prérequis

- Node.js 18+
- Hôte compatible Agent Skills
- Réseau optionnel pour l’API Wiki

## Installation

Le nom de dossier doit être `mystilink-tarot` :

```bash
cp -R mystilink-tarot-skill /path/to/.cursor/skills/mystilink-tarot
```

| Hôte | Chemin |
|------|------|
| Cursor | `.cursor/skills/mystilink-tarot/` |
| Claude Code | `.claude/skills/mystilink-tarot/` |

## Démarrage rapide

```bash
node scripts/draw.mjs --spread three-card --seed 42
# or: echo '{"spread":"three-card","seed":42}' | node scripts/draw.mjs
```

Stdout JSON : cartes avec `id`, `name`, `orientation` (`upright`|`reversed`), positions. Les `id` de cartes s’alignent sur les pages Wiki `tarot.card.*`.

## Flux de travail

1. Clarifier la question et le tirage (défaut : three-card) ; voir `examples/draw-request.json`
2. Tirer via le script ou accepter les cartes fournies par l’utilisateur
3. Pour chaque carte, Wiki optionnel :

```text
GET https://wiki.mystilink.com/api/v1/search?q=The+Fool&system=tarot&locale=en
GET https://wiki.mystilink.com/api/v1/pages/<card.id>?locale=en
```

4. Lier chaque position à la question ; citer Wiki le cas échéant

Détails : `SKILL.md`. Notes de méthode : `references/method-draw.md`.

## Exemples

- `examples/draw-request.json` — requête de tirage exemple

## Limites

- Ne pas revendiquer de certitude médicale ou juridique
- Préférer une question claire par tirage
- Locale Wiki omise → `en`

## Licence

MIT. Voir [LICENSE](../../LICENSE).

## Retours

Inclure les flags/seed du tirage (ou JSON stdin) et le JSON stdout (questions fictives uniquement).
