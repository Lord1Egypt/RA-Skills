# Mystilink Router Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## Vue d’ensemble

Agent Skill qui choisit un skill de métaphysique Mystilink (BaZi, Zi Wei, tarot, Liu Yao ou horoscope occidental) lorsque l’utilisateur n’a pas nommé de système, demande quelle méthode convient, ou mélange plusieurs traditions. Il ne calcule pas de thèmes ni de tirages.

## Type de livraison

Ce dépôt est un paquet **Agent Skill** (`SKILL.md` + references + examples). Il n’implémente **pas** la matrice de langages C / C++ / C# / Java / JavaScript / Python utilisée par les bibliothèques calculatrices.

## Prérequis

- Un hôte compatible Agent Skills (Cursor, Claude Code, OpenClaw, Hermes, ou équivalent)
- Les skills de théorie cibles installés si vous comptez poursuivre après le routage

## Installation

Clonez ou copiez ce dépôt dans le répertoire skills de l’hôte sous le nom `mystilink-router` (le nom de dossier doit correspondre au `name` dans `SKILL.md`) :

| Hôte | Chemin |
|------|------|
| Cursor | `.cursor/skills/mystilink-router/` ou `~/.cursor/skills/mystilink-router/` |
| Claude Code | `.claude/skills/mystilink-router/` ou `~/.claude/skills/mystilink-router/` |

```bash
cp -R mystilink-router-skill /path/to/.cursor/skills/mystilink-router
```

## Utilisation

Suivez `SKILL.md`. Heuristiques de routage :

| Besoin | Skill |
|------|--------|
| Date/heure de naissance → structure long terme, dix dieux | `mystilink-bazi` |
| Naissance → douze palais / étoiles Zi Wei | `mystilink-ziwei` |
| Lieu + heure de naissance → planètes/maisons/aspects | `mystilink-horoscope` |
| Une question concrète, cartes symboliques | `mystilink-tarot` |
| Une question concrète, hexagramme / lignes mouvantes | `mystilink-liuyao` |

Aide Wiki optionnelle (réseau) :

```text
GET https://wiki.mystilink.com/api/v1/pages/shared.concept.choosing-a-system?locale=en
```

Après le choix, chargez le `SKILL.md` de ce skill et continuez. Préférez un système principal par requête.

## Exemples

Voir `examples/routing-cases.md` pour des intentions utilisateur et cibles attendues.

## Limites

- Aucun script de calcul dans ce skill
- Ne lance pas plusieurs systèmes « au cas où »
- Les appels Wiki sont optionnels ; omettre `locale`/`lang` → `en` ; les traductions manquantes peuvent basculer vers `zh-Hans`

## Licence

MIT. Voir [LICENSE](../../LICENSE).

## Retours

Signalez les défauts avec le texte d’intention (fictif uniquement) et le skill sélectionné ou manqué.
