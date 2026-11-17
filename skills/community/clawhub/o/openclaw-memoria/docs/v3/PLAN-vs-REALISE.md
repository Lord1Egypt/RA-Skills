# Memoria V3 — Bilan vs le plan initial (spec gelée, roadmap 6 phases)

> Comparaison de l'état au 2026-06-10 avec `PLAN-Memoria-v3-2026-06-03.md` (Partie II, §15).
> ✅ fait · 🟡 partiel · ⚪ pas fait.

| Phase | Objectif (Definition of Done) | État |
|---|---|---|
| **0 — Stabiliser** | CI qui casse vraiment, 15 bugs fermés, versions alignées | ✅ (monorepo direct : fixes intégrés au port, CI stricte verte) |
| **1 — Fondation** | core compile+tourne, migration sans perte, daemon singleton, contrat core testé | ✅ |
| **2 — Sécurité & WAL** | crash/restart 0 perte, WAL borné, secret jamais retourné en clair | ✅ |
| **3 — MCP + UI** | connecter un agent, capturer, retrouver, 2ᵉ agent isolé, pause, **benchmark anti-fuite = 0** | ✅ |
| **4 — Import + vectoriel** | import réel sans doublon, recall hybride > FTS, garde de dimension | ✅ (Koda + transcripts, sqlite-vec) |
| **5 — Partage gouverné** | user partagé visible 2 agents, client A invisible en client B, forget partout, audit neutre | ✅ — sauf **backup/restore** ⚪ |
| **6 — Couches avancées** | couches B/C/D **activables**, coût LLM sous budget, **carte 3D**, benchmark complet | 🟡 — couches ✅, **activation des options** ⚪→ (en cours), **3D** ⚪, **adaptateur OpenClaw** ⚪ (diag fait) |

## Ce qui reste vraiment du plan initial

1. **Activation des options** (Phase 6 DoD « couches B/C/D activables ») — *en cours, c'est l'objet du jour*.
2. **Carte 3D** (visualisation UMAP du graphe, §10/§13) — ⚪.
3. **Adaptateur OpenClaw** (Phase 6) — ⚪, diagnostic fait (`DIAG-OPENCLAW.md`).
4. **Backup / restore** (Phase 5, §11) — ⚪ (le backup de migration existe, pas une commande générale).
5. **Wizard de téléchargement des modèles** (Ollama, §14 install) avec barres de progression — ⚪.
6. **`getSecretRef` / `secret_access: value_on_request`** de bout en bout MCP (§9) — 🟡.

## Au-delà du plan (bonus livrés)

- Connexion/déconnexion en **1 commande** (auto-enregistrement MCP) — pas dans le plan.
- Choix du **provider LLM par l'utilisateur** (Ollama/OpenAI/Anthropic/OpenRouter) — au-delà des « 3 profils » prévus.
- Écrans **Thèmes / Récurrences / Procédures / Révisions / Coffre / Système** + aperçu agents.
- **Affinage des libellés de thèmes à l'IA** (bouton).
- Script de **vérification des 24 couches** une par une.

**Conclusion :** les 6 phases du plan sont atteintes à ~90 %. Le cœur (phases 0-5) est complet ;
la phase 6 a ses 24 couches mais il manquait l'**activation des options** (corrigé), la **3D** et
l'**adaptateur OpenClaw**. Le reste relève de la distribution.
