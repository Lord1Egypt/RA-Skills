# Memoria V3 — État des 24 couches + plan des vagues

> Topo au 2026-06-10 (fin session 2). Les 24 couches viennent de la spec §12 (4 buckets).
> ✅ fait · 🟡 partiel · ⚪ à faire.

## L'essentiel d'abord

La **fondation V3** (ce qui n'existait PAS dans le plugin) est faite et c'est elle qui change tout :
daemon local, MCP multi-agent, pairing, connexion/déconnexion 1 commande, UI web, secrets (coffre),
migration + import (Koda + transcripts), partage gouverné, choix du moteur d'IA, recall hybride
sqlite-vec, app bureau Tauri. **C'est le gros du travail et c'est livré.**

Sur les 24 **couches cognitives** héritées : **les 24 sont portées** (vagues 5-7), avec leurs
corrections de bugs, testées, et la plupart visibles dans l'UI. Le cœur de Memoria V3 est complet ;
ce qui reste relève de la distribution (npm, signature, OpenClaw) et du raffinement (qualité des
libellés de thèmes, etc.) — voir TODO.md.

## Bucket A — Actif (fondation, tourne toujours) — 11 couches

| # | Couche | État | Note |
|---|---|---|---|
| 1 | db (schéma) | ✅ | schéma gouverné registry + contenu, FTS, triggers |
| 2 | scoring (+hot-tier) | ✅ | scoring complet + **hot-tier** (fait récemment accédé = chaud) [vague 6] |
| 3 | selective (dedup/contradiction) | ✅ | dedup + **détection de contradiction** (port/valeurs/négation) [vague 6] |
| 4 | lifecycle | ✅ | active/dormant/archived + review |
| 5 | budget (cap tokens) | ✅ | cap dur global (corrige le bug legacy) |
| 6 | procedural | ✅ | moteur match + recordExecution (failure_reasons), UI Procédures [vague 6] |
| 7 | feedback | ✅ | reinforce par usage réel (relevance_weight) [vague 6] |
| 8 | expertise | ✅ | domaines de maîtrise par agent + UI sur Agents [vague 6] |
| 9 | context-tree | ✅ | projet→client→org résolu, boost sur l'arbre [vague 6] |
| 10 | config/identity | ✅ | config.toml + identités/instances |
| 11 | WAL | ✅ | source de vérité, replay au boot, cleanup borné |

## Bucket B — Async (enrichissement hors réponse) — 7 couches

| # | Couche | État | Note |
|---|---|---|---|
| 12 | embeddings (index) | ✅ | sqlite-vec + indexer + recall hybride |
| 13 | graph (entités/relations) | ✅ | + expansion au recall + decay |
| 14 | **topics (thèmes)** | ✅ | classement auto entité-first + UI Thèmes + puces dans Revue/Mémoire [vague 5] |
| 15 | observations | ✅ | agrégation par sujet |
| 16 | fact-clusters | ✅ | regroupement structurel (Koda 52 clusters) [vague 6] |
| 17 | continuous | ✅ | capture en continu (captureTurn par tour) ; les « modes » de déclenchement sont côté adaptateur d'hôte |
| 18 | revision | ✅ | propose contradits/doublons, supersède sur validation [vague 7] |

## Bucket C — Opt-in — 3 couches

| # | Couche | État | Note |
|---|---|---|---|
| 19 | self-observation | ✅ | forces/faiblesses dérivées des procédures, UI sur Agents [vague 7] |
| 20 | markdown sync | ✅ | export .md par thème + commande `memoria export` [vague 7] |
| 21 | dialectic | ✅ | pour/contre/nuance depuis la mémoire (outil opt-in) [vague 7] |

## Bucket D — Sur validation — 3 couches

| # | Couche | État | Note |
|---|---|---|---|
| 22 | **patterns (récurrences)** | ✅ | détection des récurrences + UI Récurrences (consolider/écarter) [vague 5] |
| 23 | auto-skill | ✅ | propose des procédures depuis les récurrences [vague 7] |
| 24 | revision (mutations) | ✅ | applique la supersession sur validation [vague 7] |

## Le manque que tu as identifié (juste !)

Dans la **Revue**, on ne voit pas **dans quel sujet/thème** un souvenir va être rangé, et Memoria
ne **détecte pas encore les récurrences** (ce que faisait le plugin : repérer ce qui revient souvent
pour le consolider). Ce sont les couches **14 (topics)** et **22 (patterns)** — partielles/à faire.

## Plan des vagues à venir

### Vague 5 — Thèmes & récurrences (ta priorité)
- **topics auto** (couche 14) : à la capture, classer chaque fait dans un **sujet** (génération +
  affectation) → on sait où ça se range. Afficher le **thème dans la Revue et la Mémoire** + filtrer
  par thème.
- **patterns** (couche 22) : détecter les faits **récurrents** → proposer une consolidation (« tu as
  dit 5× que tu préfères X »). En bucket D (sur validation, pas automatique).
- UI : colonne/puce « sujet » dans Revue, filtre par thème, vue par sujet dans Mémoire.

### Vague 6 — Compléter la fondation cognitive
- scoring **hot-tier** (2), **contradiction** sémantique (3), moteur **procedural** (6),
  **feedback** (7) + **expertise** (8), **context-tree** complet (9), **fact-clusters** (16).

### Vague 7 — Couches profondes opt-in / validation
- self-observation (19), markdown sync (20), dialectic (21), auto-skill (23), revision (18/24).

### En parallèle / quand tu veux
- **UI** : améliorations que tu pointeras (thèmes, vue Mémoire par sujet, etc.).
- **Reconnecter OpenClaw** (adaptateur, diagnostic fait).
- **3D** (carte UMAP), **publication npm**, signature app, launchd.
- **Approuver/trier la quarantaine** (2266 faits) + **partager** les faits sur toi.

## Méthode
On garde la même : vagues d'agents en parallèle (worktrees), intégration + tests par moi, chaque
phase verte avant la suivante, doc + TODO à jour. 220 tests verts, CI verte.
