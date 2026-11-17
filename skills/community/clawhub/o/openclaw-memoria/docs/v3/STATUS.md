# Memoria V3 — État d'avancement

> Mis à jour en continu pendant le build. Phases = roadmap de la spec
> (`PLAN-Memoria-v3-2026-06-03.md` §15), adaptée par la décision kickoff
> (monorepo direct, Phase 0 fusionnée dans le port).

**Dernière mise à jour :** 2026-06-11 (session 5 — readiness test iMac : onboarding moteur, détection/import agents par bouton, install durcie)

## 🏁 État global : produit complet, partage multi-machines opérationnel

Fondation V3 complète (daemon/MCP/UI/secrets/migration/partage/providers/desktop) + **24 couches**
(voir `COUCHES-ETAT.md`) + **adaptateur OpenClaw** (auto-recall/capture) + **synchro inter-machines**
(hub-and-spoke, coffre partagé) + **identification d'interlocuteur** + **install 1-commande & bouton
mise à jour** + **onboarding moteur d'intelligence** (anti-mort-silencieuse) + **détection/connexion/
import d'agents par bouton**. **514 tests verts, CI verte.** UI à 14 écrans. 6 agents réels connectés.
Reste : terrain (init hub Mac Studio + join iMac), relais NAS optionnel, distribution npm/signature.



| Phase | Contenu | État |
|---|---|---|
| Scaffolding | Monorepo npm workspaces, TS strict, vitest, CI stricte, docs | ✅ fait |
| P1 — Fondation | core (schéma registry+contenu, storeFact/recall/forget), resolveStorageRoot, daemon singleton HTTP+token | ✅ fait (migration v3.34 en vague 2) |
| P2 — Sécurité & WAL | WAL source de vérité (replay boot), redaction secrets, SecretProvider (Keychain+AES), audit neutre | 🟡 vague 2 en cours (audit neutre ✅) |
| P3 — MCP + UI | pairing ✅ (code TTL→token), serveur MCP, UI web, benchmark anti-fuite v1 ✅ | 🟡 vague 2 en cours |
| P4 — Import + vectoriel | importeur OpenClaw ✅ (quarantaine+provenance+rollback), **sqlite-vec + recall hybride RRF ✅** (recallSemantic, indexation auto post-capture + boot), reste : importeurs MD/transcripts | 🟢 quasi fait |
| P5 — Partage gouverné | review-first ✅, **partage par référence ✅** (shareFacts/setScopeAccess/suggestIdentityFacts + routes), hard-delete ✅. Reste : UI matrice de partage, topics permissionnables, backup/restore | 🟢 cœur fait |
| P6 — Couches avancées | **graph/entités/relations/observations ✅** (CognitionEngine async + expansion graphe au recall + decay), import cognitif legacy ✅. Reste : clusters, 3D UMAP, couches D sur validation, adaptateur OpenClaw. **Diag OpenClaw ✅** | 🟢 gros morceau fait |
| Tauri | **Memoria.app + DMG construits et lancés ✅** (lib.rs 9 tests, page de lancement, icns) — reste : signature/notarisation (process Igara), Node embarqué v1.5 | 🟢 fait (non signé) |

**Benchmark recall (juge du produit)** : ✅ vert — anti-fuite inter-clients = 0 sur batterie de 5 requêtes,
défaut sûr sans contexte, pas de sur-masquage, dormant explicite, cap tokens. `packages/core/test/benchmark.test.ts`.

## 🟢 INSTALLATION RÉELLE (machine de Néto, 2026-06-10)

- Daemon actif sur `~/.memoria/data` (port/admin_token dans `~/.memoria/data/daemon.json`).
- **Claude Code connecté** : serveur MCP `memoria` enregistré en scope user
  (`claude mcp list` → ✔ Connected). Outils : memoria_recall / memoria_store_fact /
  memoria_capture_turn / memoria_set_context / memoria_get_context.
- Instance : `72615d82-7ee6-4a2e-82d7-24887fef1d59` (credentials chmod 600 dans `~/.memoria/credentials/`).
- E2E réel validé : capture → extraction qwen2.5:3b (~3 s) → recall ; secret jamais en clair.
- UI web : `http://127.0.0.1:<port>/ui/#token=<admin_token>` (les deux valeurs dans daemon.json).
- ⚠️ Le daemon pointe sur le build du repo (`packages/daemon/dist`) — relancer après un rebuild
  (`memoria stop && memoria start`). Auto-démarrage launchd : TODO.

## Journal de session

### 2026-06-11 — Session 5 (readiness test iMac — 3 chantiers parallèles, 514 tests verts)
- **Moteur d'intelligence (anti-mort-silencieuse)** : provider **LM Studio** (extraction, OpenAI-compatible
  local), `detectLlmOptions()` (Ollama/LM Studio/clés/OpenClaw — clés API en clair réutilisables via
  `copyOpenClawKey`, OAuth honnêtement refusé), **`GET /v1/admin/llm_health`** (extraction+embeddings avec
  raisons + `wal_pending`), job `ollama_pull` avec progression NDJSON. **Onboarding** étape « Moteur
  d'intelligence » obligatoire (cartes + badges, pulls avec barres de progression, commandes de clé à
  copier, bouton Tester, mode dégradé = opt-in explicite encart rouge). **Bannière Dashboard** quand
  extraction indisponible / souvenirs en attente. Embeddings = Ollama-only V1 (dit explicitement).
- **Agents par bouton** : `detectAgents()` (CLI + transcripts comptés + DB legacy OpenClaw + croisement
  registry), routes `agents_detect` / `agents_connect` (pairing+credentials+enregistrement MCP EN
  PROCESSUS daemon, échec visible avec repli manuel), **job d'import asynchrone dans le daemon**
  (`import_start`/`import_status` : transcripts avec onProgress → quarantaine Revue ; legacy snapshot →
  adoption ; gate 422 sans moteur ; 1 seul job ; garde-fou quarantaine non vide). UI Agents section
  « Sur cette machine » (Détecter / Connecter / Importer avec progression / Démarrer de zéro).
  CLI `memoria import`. `register.ts`+`credentials.ts` déplacés mcp→core (ré-export intact).
- **Install & CLI** : `install-memoria.sh` durci (check git/Xcode CLT avec popup+consigne, avertissement
  Node non-LTS, **garde anti-écrasement** si modifs locales, init non muet, PATH ~/.zshrc idempotent,
  `autostart on`, ouverture auto de l'UI, shim node runtime). **`memoria ui`** = commande par défaut
  (`memoria` tout court ouvre l'interface ; --help intact). INSTALLATION-RESEAU.md à jour (étape 1bis moteur).
- Vérifié live sur le daemon réel : llm_health (gpt-4o-mini + nomic prêts, LM Studio non détecté,
  OpenClaw sans clé réutilisable), agents_detect (Claude Code 159 transcripts / Codex 38 / OpenClaw,
  tous already_connected), import_status idle, UI 200, `memoria ui` ouvre le navigateur, update « Déjà à jour ».
- ⚠️ Flakiness PRÉEXISTANTE confirmée (base f2799a0) : tests sync se disputent le Keychain réel
  (`__cluster_pairing_key`) + port LAN fixe 47733 → à corriger dans le chantier sync (aes-vault + port 0).

### 2026-06-10 — Session 1 (kickoff)
- Clone `Primo-Studio/openclaw-memoria` → `~/openclaw-memoria`, HEAD = `4556c4d` (v3.34.0, base de l'audit).
- Branche `memoria-v1`, ancien code → `legacy/` (commit 1).
- Décisions kickoff Néto (voir DECISIONS-LOG.md).
- Cartographie legacy TERMINÉE : 10 agents, `docs/v3/port-map.json` (106 bugs documentés file:line,
  recettes de portage par module, schéma v3.34 complet pour la migration).
- Scaffolding monorepo : root + core/daemon/mcp/cli/web, CI stricte (remplace la CI menteuse), vitest 4.
- Ollama : `nomic-embed-text` + `qwen2.5:3b` téléchargés ✓. rustup/cargo installés ✓ (Tauri prêt).
- **Core P1 livré** : registry+contenu (schéma complet, FTS triggers, embeddings model/dim), pairing
  code→token, storeFact gouverné, recall fan-out anti-fuite, forget hard-delete, doctor/stats,
  browseFacts, capture_mode. 30 tests.
- **Daemon P1 livré** : HTTP 127.0.0.1, auth 3 niveaux, singleton lock-file, routes admin+memory,
  service statique UI /ui/, boot-test CI.
- **Benchmark recall v1 vert** (a déjà attrapé un vrai bug de conception : bm25 non comparable
  inter-DB → scoring couverture-dominant).
- Vague 2 intégrée (7 pistes) : secrets, LLM, capture/WAL, MCP, CLI, web, migration legacy. Capture
  câblée bout-en-bout, E2E réel qwen2.5:3b validé (3 faits/3 s, secret jamais en clair).
- Review-first actif (faits dormants + file de revue + écran UI + sélecteur pause).
- Vague 3 : **recall hybride sqlite-vec** (RRF, permissions jamais contournées, synonymes retrouvés
  — validé en réel avec nomic-embed-text via le daemon), **lanceur Tauri** (9 tests Rust),
  **diagnostic OpenClaw** (MCP natif confirmé → P6 simplifié).
- CI GitHub **VERTE** (matrice ubuntu+macos × Node 20/22/24) après fix garde réseau platform-aware.
- **Installé en réel** : daemon + MCP Claude Code ✔ Connected + premiers souvenirs capturés.
- **Memoria.app construite (DMG inclus) et lancée avec succès** : check Node → daemon → UI.
  DMG : `apps/desktop/src-tauri/target/release/bundle/dmg/Memoria_0.1.0_aarch64.dmg`.

### Session 2 (suite) — Koda + cognition + partage
- **Mémoire de Koda récupérée** (Mac Studio `192.168.1.98`) : 3515 faits + 364 procédures adoptés
  dans sa mémoire privée + **3038 entités + 3329 relations + 1920 observations** (graphe cognitif)
  importées depuis le backup. 1917 embeddings réindexés. Voir `docs/v3/AGENTS-RESEAU.md`.
- **Partage gouverné par référence** : `shareFacts` (privé→user/org), `setScopeAccess` (matrice),
  `suggestIdentityFacts` (propose les faits sur l'utilisateur, ne décide pas).
- **Couches cognitives bucket B** : graph/entités/relations/observations, async post-capture,
  **expansion graphe au recall** (anti-fuite garantie), decay quotidien.
- **UI Onboarding** (<60 s, détection providers) + **Réglages** (profil LLM, stockage).
- 179 tests verts. Reste à faire : voir `TODO.md` (UI partage, OpenClaw, clusters/3D, publication npm).

### 2026-06-11 — Session 3 (contrôle + visualisation + OpenClaw)
- **Contrôle & config** : kill-switch (pause Memoria), suppression définitive d'agent, déplacement
  stockage (clé USB, `memoria move`), lancement auto au login (launchd, `memoria autostart`). CLI + routes + UI.
- **Relations entre thèmes** (graphe SVG, écran Thèmes) + **recherche globale** (tous agents, écran Mémoire).
- **Audit OpenClaw 2026.6.5** : cause racine de la casse capture v3.34 = gate `allowConversationAccess`
  (bloque les hooks de conversation par défaut). `docs/v3/DIAG-OPENCLAW-2026.6.5.md`.
- **Adaptateur OpenClaw livré** (`packages/adapter-openclaw`, zéro dépendance native) : `before_prompt_build`
  →/recall, `agent_end`→/capture (fire-and-forget). `memoria connect` installe le plugin + pose le gate +
  le token. **Validé E2E sur le daemon réel** (recall + capture + extraction gpt-4o-mini). 16 tests.

### 2026-06-11 — Session 4 (réseau multi-machines + interlocuteur + install/update)
- **Identification de l'interlocuteur** (écran Personnes) : `person_identifiers` (tel/mail/Telegram/
  WhatsApp/handle), `identifyInterlocutor`, outil MCP `memoria_identify_interlocutor`. 7 tests.
- **Synchro inter-machines** (design `SYNC-INTER-MACHINES.md`, hub-and-spoke) : provenance + LWW
  déterministe (content v2), `SyncEngine` (pairing/HMAC/pull/push/coffre/bootstrap), second listener LAN
  `/v1/sync/*` (admin/memory restent loopback), CLI `memoria sync *`, UI Réglages. Coffre inter-machines
  (valeurs chiffrées GVK, jamais en clair sur le réseau). **Validé : 2 daemons réels sur HTTP.** 33 tests sync.
- **Install + mise à jour** : `scripts/install-memoria.sh` (1 commande non-dev), bouton « Mise à jour »
  UI + `memoria update` (git pull+build+redémarrage), `docs/v3/INSTALLATION-RESEAU.md`.
- **430 tests verts.** Daemon réel : 6 agents, 5785 souvenirs. Terrain restant : init hub + join iMac.
