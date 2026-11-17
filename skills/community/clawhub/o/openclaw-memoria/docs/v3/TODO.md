# Memoria V3 — TODO de passation

> **But** : reprendre le travail SANS contexte oral. Lire d'abord `STATUS.md`, puis ce fichier,
> puis `DECISIONS-LOG.md`. Spec gelée = `~/Downloads/Memoria-V3-Dossier-Dev-2026-06-10/PLAN-Memoria-v3-2026-06-03.md`.
> Carte des agents/mémoires à récupérer = `AGENTS-RESEAU.md`.

## Reprendre le travail

```bash
cd ~/openclaw-memoria        # branche memoria-v1
npm install && npm run build && npm test   # doit être 100% vert AVANT toute modif
```

- Le « juge du produit » = `packages/core/test/benchmark.test.ts` (anti-fuite = 0). Toute
  évolution du recall doit le laisser vert.
- Règle anti « mort silencieuse » : aucun catch muet ; tout chemin actif a un test qui le prouve.
  ~106 bugs legacy documentés `docs/v3/port-map.json` — ne pas les réintroduire.
- Auteur git = **Hello-Primo**. `.claude/`, `dist/`, `*.tsbuildinfo` gitignorés.

## ✅ Déjà fait (sessions 1-2, 2026-06-10)

- **Fondation** : monorepo (core/daemon/mcp/cli/web + apps/desktop), schéma gouverné, CI stricte verte.
- **Recall** : fan-out FTS + **vectoriel sqlite-vec hybride** (recallSemantic) + **expansion graphe**,
  anti-fuite inter-clients = 0, cap tokens.
- **Capture** : WAL-first, redaction secrets (gate dur, coffre Keychain/AES), extraction LLM
  (Ollama/Anthropic), review-first.
- **Cognition** (bucket B) : entités/relations/observations async + decay.
- **Gouvernance** : pairing, partage par référence (`shareFacts`/`setScopeAccess`/`suggestIdentityFacts`),
  hard-delete, audit neutre, capture_mode (pause/incognito).
- **Migration** : Koda (Mac Studio) récupérée — 3515 faits + 364 procédures + 3038 entités +
  3329 relations + 1920 observations, embeddings réindexés. Importeur legacy + adoption.
- **Connexion/déconnexion** : 1 commande (`connect`/`disconnect`), auto-enregistrement MCP par hôte.
- **UI** : Dashboard, Agents, Mémoire, Revue, Audit, Réglages, Onboarding, sélecteur pause.
- **Desktop** : Memoria.app + DMG construits.
- **Agents connectés en réel** : Claude Code (`72615d82`), Codex (`0b5322e1`), Koda (`405290ba`, mémoire complète).

## ✅ Session 3 (2026-06-11) — Contrôle & config + audit OpenClaw

- **Kill-switch global** (`config.enabled`) : `memoria enable`/`disable` + engine `isEnabled/setEnabled`
  + daemon no-op ANNONCÉ (`{disabled:true}`) sur capture/recall en pause + toggle UI Réglages.
- **Suppression définitive d'agent** : `deleteInstance` (engine+registry), `memoria delete-agent --yes`,
  route `POST /v1/admin/delete_agent`, bouton « Supprimer » (confirm) écran Agents. ≠ revoke (efface la DB privée).
- **Déplacement du stockage (clé USB)** : `moveStorage` (rename même volume / cpSync+rm cross-volume) +
  `memoria move --to <dir>` (arrête le daemon, déplace, réécrit `config.toml`). UI : commande affichée.
- **Lancement auto au login** : `control/autostart.ts` (LaunchAgent launchd, KeepAlive), `memoria autostart on|off`,
  route `POST /v1/admin/autostart`, toggle UI. macOS only (échoue proprement ailleurs).
- **Route `GET /v1/admin/control`** : enabled + autostart status + storageInfo (pour l'UI).
- **Relations entre thèmes** (demande Néto) : `TopicEngine.relations()` (graphe par faits/entités partagés,
  borné 28 nœuds/70 arêtes, `via` = entités fortes d'abord, bruit filtré). `Memoria.topicRelations`,
  route `GET /v1/admin/topic_relations`, vue SVG circulaire « Relations » dans l'écran Thèmes (0 dépendance).
  Validé sur Koda : 23 nœuds, 70 arêtes réelles (JamBoard↔CoreBluetooth, RSMA↔Devis, Directus↔SEO).
- **Recherche globale** : `Memoria.globalSearch` (tous agents d'un coup, résultat étiqueté de l'agent),
  route `GET /v1/admin/search?q=`, option « 🔍 Toutes les mémoires » dans l'écran Mémoire.
- Tests : `control.test.ts` (9) + `topics.test.ts` relations (3). Suite = **374 verts**. Daemon réel redémarré,
  routes control/topic_relations/search vérifiées live.
- **Audit OpenClaw 2026.6.5** (`DIAG-OPENCLAW-2026.6.5.md`) : ⚠️ **NOUVEAU gate `allowConversationAccess`
  bloque par défaut** les hooks de conversation (`llm_output`, `agent_end`) pour tout plugin non bundlé →
  **cause #1 plausible de la casse de capture v3.34**. L'install de l'adaptateur DOIT poser
  `plugins.entries.memoria.hooks.allowConversationAccess=true`. L'auto-recall (`before_prompt_build`) survit.

## ✅ Session 4 (2026-06-11) — Réseau multi-machines + interlocuteur + install/update

- **Interlocuteur (Personnes)** : registry v3 `person_identifiers` (tel/mail/Telegram/WhatsApp/handle,
  normalisés, 1 identifiant→1 personne) + colonnes persons (relation/org_id/user_id). Engine
  `identifyInterlocutor` (+ faits connus), `describeInterlocutor`, CRUD. Routes admin + route mémoire
  `identify_interlocutor` + **outil MCP `memoria_identify_interlocutor`**. Écran **Personnes** (UI). 7 tests.
- **Synchro inter-machines** (hub-and-spoke, design `SYNC-INTER-MACHINES.md`) :
  - content v2 (provenance origin_machine_id/rev/content_hash + tombstones) + `sync/merge.ts` LWW
    déterministe + `sync/clock.ts`. registry v4 (sync_peers/cursor/secret_envelopes/nonces).
  - `sync/peer-auth.ts` (HMAC ±60 s + nonce 5 min), `sync/secrets-sync.ts` (GVK AES-GCM, sealGvk scrypt),
    GVK/CPK en Keychain. `SyncEngine` (invite/completePairing/authenticate/collectDelta/snapshot/
    applyIncoming/serveSecrets ; join/pull/push/syncAll/tick/leave). **adoptScope** aligne les IDs de scope.
  - daemon : **second listener LAN** (hub) `/v1/sync/*` (HMAC) ; admin/memory restent loopback
    (anti-rebinding préservé) ; timer best-effort (spoke). Routes admin sync + CLI `memoria sync *` + UI Réglages.
  - Tests : sync-merge (11) + sync-crypto (10) + sync-engine intégration in-memory (8) + **sync-http 2 daemons
    réels (4)**. Coffre inter-machines validé (secret déchiffré chez le spoke, jamais en clair sur le réseau).
  - ⏳ Reste OPTIONNEL : incrément 6 (relais NAS QNAP pour bootstrap quand le hub dort) + `sync verify`.
- **Install iMac + mise à jour** : `scripts/install-memoria.sh` (1 commande, non-dev), route+CLI+bouton UI
  **Mise à jour** (git pull + build + redémarrage auto), `GET /v1/admin/version`. Guide `INSTALLATION-RESEAU.md`.
- Suite = **430 verts**. Tout vérifié live sur le daemon réel (version, sync status, personnes).
- **Terrain (Néto/Badette)** : sur le Mac Studio `memoria sync init-hub` + redémarrer + inviter ;
  sur l'iMac, `install-memoria.sh` puis « Relier au hub » → Luna partage la mémoire d'équipe + le coffre avec Koda.

## Reste à faire (ordre conseillé)

### Import des mémoires Claude Code / Codex
- [x] ~~Importeur de transcripts~~ **FAIT + INTÉGRÉ** : `Memoria.importTranscripts`.
- [x] ~~Bulk import RÉEL avec gpt-4o-mini~~ **FAIT 2026-06-10** : **2266 faits en quarantaine**
      (Claude Code 1021, Codex 1245) en ~28 min. Échantillon qwen nettoyé avant. Idempotent.
- [x] ~~Providers OpenAI/OpenRouter + choix utilisateur~~ FAIT (Réglages UI + clés par fichier).
- [ ] **Approuver/trier la quarantaine** : 2266 faits dormants à valider. Options pour Néto :
      - Écran Revue « Tout approuver » par agent (chaque agent récupère SA mémoire active). Le plus
        rapide ; un peu de bruit (gpt-4o-mini extrait parfois de l'éphémère) mais ranké au recall.
      - Tri sélectif si Néto préfère.
- [ ] **Partager les faits sur Néto** : écran Partage → par agent, `suggestIdentityFacts` (50 candidats
      réels/agent : préférences, identité, conventions) → cocher → `shareFacts` vers `user`. Reste
      la décision de Néto.
- [ ] (optionnel) prompt d'extraction encore plus sélectif / post-filtre de l'éphémère résiduel.

### UI manquante
- [x] ~~Écran Partage (matrice scopes × agents)~~ **FAIT** (`Sharing.tsx`) : matrice « qui lit quoi »
      (`setPolicy`), explorateur de contenu de scope, panneau « Faits sur toi à partager »
      (`suggestIdentityFacts` → `shareFacts` vers `user`). Vérifié live (top candidat Koda = « Neto Pompeu »).
      Reste optionnel : raffiner le tri des candidats identité (du bruit type « Token » dans la longue traîne).
- [ ] Écran Organisations & projets (créer org client, projet, scopes) — logique core prête.
- [x] ~~Onboarding : barres de progression de téléchargement des modèles Ollama (spec §14)~~ **FAIT session 5**
      (étape « Moteur d'intelligence » complète : choix Ollama/LM Studio/clés/OpenClaw, pulls avec
      progression, mode dégradé explicite).
- [x] ~~Vue relations entre thèmes~~ **FAIT** (onglet « Relations » écran Thèmes, graphe SVG).
- [x] ~~Recherche globale (tous agents)~~ **FAIT** (option « Toutes les mémoires » écran Mémoire).

### Reconnecter OpenClaw (P6) — FAIT (adaptateur livré + validé E2E)
- [x] ~~Diagnostic compatibilité 2026.6.5~~ **FAIT** (`DIAG-OPENCLAW-2026.6.5.md`).
- [x] ~~Adaptateur hooks mince~~ **FAIT** : `packages/adapter-openclaw` (zéro dépendance native).
      `before_prompt_build`→`/v1/memory/recall` (timeout dur 400 ms → `prependContext`),
      `agent_end`→`/v1/memory/capture_turn` (VRAI fire-and-forget, WAL persiste avant extraction).
      Découverte du port via `daemon.json`, auth token d'instance. 12 tests de contrat.
- [x] ~~Install auto + gate~~ **FAIT** : `memoria connect` (openclaw) pose le serveur MCP + lie le plugin
      dans `~/.openclaw/extensions/memoria` + écrit `openclaw.json` avec **`allowConversationAccess=true`**
      (sinon capture morte). `disconnect` nettoie. 4 tests (paths injectables). `event.toolCallCount` non lu (corrigé).
- [x] ~~Validation bout-en-bout~~ **FAIT 2026-06-11** sur le daemon réel : recall injecte un fait semé,
      `agent_end` capture une conversation, gpt-4o-mini extrait le fait, recallable juste après. Instance test supprimée.
- [ ] **Reste (terrain)** : sur le Mac Studio, `openclaw plugins enable memoria` + `plugins inspect memoria`
      (vérifier `allowConversationAccess: true`) + grep logs « blocked because non-bundled… » ; reconnecter Koda
      avec son vrai token (re-pairing) et confirmer la capture en conditions réelles. Optionnel : hook `llm_output`
      (continuous learning) + `after_compaction` (flush avant perte de contexte).

### Couches avancées restantes (P6)
- [ ] Clusters (fact-clusters), carte 3D UMAP (opt-in), couches D sur validation (patterns/auto-skill).
- [ ] Job cron daemon : `decayCognition` quotidien (méthode prête, manque le scheduler).

### Distribution & finitions
- [ ] **Publier npm** (`@memoria/*` ou `@primo-studio/memoria`) — tant que non publié, les commandes
      utilisent le chemin local `node ~/openclaw-memoria/packages/mcp/dist/bin.js` (déjà géré par le
      daemon et connect). Après publication : repasser aux formes `npx -y @memoria/mcp`.
- [ ] Signature/notarisation `Memoria.app` (process Igara), Node embarqué SEA (v1.5).
- [x] ~~Auto-démarrage daemon au login (launchd plist macOS)~~ **FAIT** (`memoria autostart on` + toggle UI).
- [ ] `getSecretRef`/`secret_access` de bout en bout (engine→daemon→MCP `memoria_get_secret_ref`).
- [ ] Renommer le repo `openclaw-memoria` → `memoria` (à la release, décision Néto).
- [ ] Récupérer **Sol** (Mac mini) quand Néto le voudra — procédure dans AGENTS-RESEAU.md.

## ✅ Session 5 (2026-06-11) — Readiness test iMac

- Onboarding « Moteur d'intelligence » + santé LLM (`llm_health`, bannière Dashboard, provider LM Studio
  extraction) ; détection d'agents + connexion 1 clic + import par bouton (job daemon, progression, Revue) ;
  `memoria import` ; install-memoria.sh durci (CLT, garde anti-écrasement, PATH, autostart, ouverture UI) ;
  `memoria ui` = défaut. 514 tests verts. Détail : STATUS.md session 5.
- Reste de ce chantier : embeddings LM Studio (V1 = Ollama-only, dit explicitement dans la santé) ;
  harmoniser le tutoiement de l'écran Agents historique ; annulation d'un job d'import ;
  vérité terrain du format SQLite `auth_profile_stores` OpenClaw (table vide ici, parsing défensif).

### Tests sync flaky (préexistant — à corriger dans le chantier sync)
- [ ] `sync-engine.test.ts` + `sync-http.test.ts` : contention Keychain macOS réel
      (`security add-generic-password -U` sur `__cluster_pairing_key`) + port LAN fixe 47733 →
      passer ces tests sur `secretsVault: 'aes-vault'` + port 0.

## Pièges connus
- bm25 NON comparable entre DB → scoring fan-out = couverture de requête (`content.ts searchFacts`). Ne pas « simplifier ».
- FTS5 : maintenance par TRIGGERS uniquement (pas de rebuild manuel sans rowid).
- Embeddings : `model`+`dimensions` obligatoires, comparaison inter-dim interdite (cosine throw).
- Mode JSON Ollama : demander un OBJET `{"facts":[...]}`, pas un tableau nu (petits modèles).
- Le daemon pointe sur le build du repo : `memoria stop && memoria start` après un rebuild.
- Migration : toujours `.backup` (snapshot cohérent) côté source, jamais toucher l'original.
