# Mystilink Liu Yao Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## Vue d’ensemble

Agent Skill pour Liu Yao (jet à six lignes) : forme des hexagrammes à partir de six jets avec un script Node intégré, puis interprète avec des pages de méthode et des chapitres du Zhouyi depuis Wiki. Une affaire, un jet. N’inventez pas de citations classiques.

## Type de livraison

Paquet **Agent Skill**. N’implémente **pas** la matrice de langages des calculatrices. La logique de jet est intégrée uniquement dans `scripts/` (pas de dépôt calculateur Liu Yao séparé).

## Prérequis

- Node.js 18+
- Hôte compatible Agent Skills
- Réseau recommandé pour les pages de méthode Wiki et les classiques

## Installation

Le nom de dossier doit être `mystilink-liuyao` :

```bash
cp -R mystilink-liuyao-skill /path/to/.cursor/skills/mystilink-liuyao
```

| Hôte | Chemin |
|------|------|
| Cursor | `.cursor/skills/mystilink-liuyao/` |
| Claude Code | `.claude/skills/mystilink-liuyao/` |

## Démarrage rapide

```bash
node scripts/cast.mjs --seed 42
# or fixed throws: node scripts/cast.mjs --throws "3,2,3,3,2,3"
```

Stdout JSON : six lignes (bas→haut), drapeaux de mouvement, clés d’hexagramme si disponibles. Le modèle de pièces suit l’aide du script (face=3, pile=2 en somme).

## Flux de travail

1. Une affaire claire (`examples/cast-request.json`) ; refuser les jets multi-sujets
2. Jeter via le script ou accepter les jets fournis par l’utilisateur
3. Lire via Wiki, par exemple :

```text
GET https://wiki.mystilink.com/api/v1/pages/liuyao.method.six-casts?locale=en
GET https://wiki.mystilink.com/api/v1/pages/liuyao.rule.ben-zhi-bian?locale=en
GET https://wiki.mystilink.com/api/v1/pages/shared.work.yijing.gua.01-qian?locale=zh-Hans
```

4. Préférer les references / cites Wiki pour les passages du Zhouyi

Détails : `SKILL.md`. Orientation : `references/overview.md`.

## Exemples

- `examples/cast-request.json` — requête de jet exemple

## Limites

- Les classiques basculent souvent vers `zh-Hans` lorsque d’autres locales manquent de texte
- L’aide de jet intégrée reflète la sémantique pièce→ligne du produit sous forme simplifiée
- Locale Wiki omise → `en`

## Licence

MIT. Voir [LICENSE](../../LICENSE).

## Retours

Inclure seed/throws et le JSON stdout (affaires fictives uniquement).
