# DIAG-OPENCLAW — Diagnostic de la casse du plugin Memoria v3.34

> **Mission** : prérequis de la Phase 6 (note de passation §1 : « diagnostiquer ce qui a cassé
> avant d'écrire l'adaptateur OpenClaw V3 »). Lecture seule — aucun code modifié.
> **Date** : 2026-06-10 · **Auteur** : Claude (Fable 5)
>
> Chaque affirmation est sourcée : soit un chemin de fichier local (avec ligne quand utile),
> soit une URL. `$OC` = `/Users/primostudio/.nvm/versions/node/v22.22.2/lib/node_modules/openclaw`.

---

## TL;DR

1. **OpenClaw installé ici : `2026.4.15` (npm global, Node 22). Dernière version npm : `2026.6.5`
   (publiée 2026-06-09).** La machine qui exécute réellement le gateway (et où la casse s'observe)
   est le **Mac Studio**, pas ce Mac : `~/.openclaw` n'existe pas ici et aucun gateway ne tourne.
2. **Les 6 hooks utilisés par Memoria v3.34 existent toujours** (`before_prompt_build`,
   `message_received`, `llm_output`, `agent_end`, `after_tool_call`, `after_compaction`) — dans la
   version installée ET dans la doc de la version courante. La casse n'est **pas** « les hooks ont
   disparu ».
3. La surface plugin a en revanche été **massivement restructurée** entre 2026.3.x et aujourd'hui
   (SDK `openclaw/plugin-sdk/*`, validation stricte de config, scan d'installation fail-closed,
   slot mémoire exclusif, politique `allowPromptInjection`). Les causes les plus probables de la
   casse sont **environnementales** (ABI native `better-sqlite3` vs Node du gateway, config rejetée,
   bug de mise à jour npm) — détaillées en §5.
4. **OpenClaw parle MCP nativement** (client stdio/SSE/streamable-http via le SDK officiel
   `@modelcontextprotocol/sdk`, tools exposés à l'agent sous `<serveur>__<tool>`), et sait aussi
   s'exposer comme serveur MCP (`openclaw mcp serve`). Config exacte en §6.
5. **Recommandation** : hybride. Dès la Phase 3, `memoria-mcp` se branche par **config MCP pure**
   (recall/store en mode « pull », trivial). En Phase 6, un **adaptateur natif mince** (~150-250
   lignes, zéro dépendance native, zéro logique locale) ajoute l'auto-recall/auto-capture via les
   hooks, en parlant au daemon Memoria. Détails en §7.

---

## 1. Version installée et canal de distribution

| Question | Réponse | Preuve |
|---|---|---|
| Version locale | `OpenClaw 2026.4.15 (041266a)` | `openclaw --version` (binaire `~/.nvm/versions/node/v22.22.2/bin/openclaw`) |
| Canal | **npm global** (`npm i -g openclaw`), symlink daté du 21 avril 2026 | `ls -la` du symlink → `../lib/node_modules/openclaw/openclaw.mjs` |
| Node requis | `>=22.14.0` | `$OC/package.json` (`engines.node`) |
| Dernière version publiée | `2026.6.5` (2026-06-09), dist-tags `beta=2026.6.5-beta.6`, `alpha=2026.5.19-alpha.1` | `npm view openclaw version dist-tags time` |
| Cadence | ~1 release/jour ouvré (versionnage calendaire `AAAA.M.J`) | `npm view openclaw time` |
| App macOS | **disparue** : `/Applications/OpenClaw.app` n'existe plus (le cache d'icônes ClickUp prouve qu'elle a existé : `~/Library/Application Support/ClickUp/App Icons Cache/Applications_OpenClaw_app_…`) | `ls /Applications` ; cache ClickUp |
| État local | `~/.openclaw` **n'existe pas** sur ce Mac ; aucun process gateway (`ps aux`) | vérifié 2026-06-10 |

**Conséquence importante** : le gateway qui a cassé Memoria tourne **ailleurs** (Mac Studio — cf.
`docs/v3/DECISIONS-LOG.md`, décision 2 du kickoff : la `memoria.db` de Koda y vit). La version
d'OpenClaw qui a réellement cassé le plugin est donc **inconnue depuis cette machine** —
vraisemblablement une 2026.5.x/2026.6.x (la casse a été constatée le 2026-06-10). Ce diagnostic
s'appuie sur la 2026.4.15 locale + le changelog/docs publics jusqu'à 2026.6.5.

### 1.1 `~/Library/Application Support/OpenClaw/` (bridge.sock, identity)

```
bridge.sock     socket UNIX, 0600, dernier mtime 13 mars 2026
identity/device.json        (créé 9 févr. 2026 — deviceId + paire de clés)
identity/device-auth.json   (0600 — secret, non lu)
```

- `file bridge.sock` → `socket`. **Personne n'écoute dessus** : `lsof -U | grep bridge` ne montre
  que le bridge navigateur de Claude Code (`/tmp/claude-mcp-browser-bridge-…`), rien côté OpenClaw.
- La chaîne `bridge.sock` n'apparaît **nulle part** dans le dist npm 2026.4.15 (grep sur
  `$OC/dist`), et le répertoire d'état du CLI npm est `~/.openclaw` (`$OC/dist/paths-Dvv9VRAc.js`
  contient `.openclaw` / `.openclaw/openclaw`).
- Conclusion : ce dossier est un **vestige de l'ancienne app macOS** (installée ~9 février, app
  supprimée depuis). Le `device.json`/`device-auth.json` correspond au mécanisme d'identité
  d'appareil du gateway (cf. breaking 2026.2.22 « remove legacy Gateway device-auth signature v1 »,
  changelog). **Rien à brancher dessus pour la V3** — c'est mort.

---

## 2. L'ancien contrat (ce que Memoria v3.34 consommait)

Sources : `legacy/openclaw.d.ts`, `legacy/openclaw.plugin.json`, `legacy/index.ts`.

- **Manifeste** `legacy/openclaw.plugin.json` : `{ id: "memoria", version: "3.25.1" (sic),
  configSchema: <JSON Schema brut>, uiHints, description, keywords }`. **Aucune déclaration de
  version OpenClaw supportée** (pas de champ `engines`/`minVersion` — et le format actuel n'en
  prévoit pas non plus, cf. §3.4). Le « chaos de versionnage » (3.34 vs 3.25.1) est déjà connu
  (note de passation §2).
- **Entrée** : `legacy/index.ts:58` exporte `register(api)` + `export default { register }`.
- **Type stub** `legacy/openclaw.d.ts` : module `openclaw/plugin-sdk/core` avec `logger`,
  `pluginConfig`, `config`, `workspace: { path }`, `on(event, handler)`, `modifyPrompt(cb)`.
  C'est un stub **maison** : au runtime le plugin n'utilise que `api.logger` (93×), `api.on` (7×)
  et `api.pluginConfig` (grep sur `legacy/*.ts`). `modifyPrompt` et `workspace` ne sont jamais
  appelés — leur présence dans le stub ne prouve pas qu'ils aient existé côté hôte.
- **Hooks réellement câblés** (tous via `api.on(nom, handler)`) :

| Hook | Usage Memoria | Fichier |
|---|---|---|
| `before_prompt_build` | recall — retourne `{ prependContext }` | `legacy/recall.ts:362,386` |
| `message_received` | continuous learning (buffer + urgence) | `legacy/continuous.ts:122` |
| `llm_output` | continuous learning (extraction périodique) | `legacy/continuous.ts:208` (annoncé header :9) |
| `after_tool_call` | capture procédurale temps réel | `legacy/procedural-hooks.ts:39` (doc du hook :14) |
| `agent_end` | capture session + auto-skill | `legacy/capture.ts:43`, `legacy/index.ts:359` |
| `after_compaction` | capture pré-perte de contexte | `legacy/capture.ts:253` (header :2) |

- **Workspace** : `legacy/index.ts:56` lit `process.env.OPENCLAW_WORKSPACE ||
  ~/.openclaw/workspace`. ⚠️ `OPENCLAW_WORKSPACE` n'apparaît **plus nulle part** dans le dist
  2026.4.15 (grep `$OC/dist`) — ce n'était pas/plus un contrat hôte. La résolution actuelle est
  par agent : défaut `~/.openclaw/workspace` (agent par défaut), `~/.openclaw/workspace-<agentId>`
  sinon, configurable via `agents.defaults.workspace` (`$OC/dist/agent-scope-KFH9bkHi.js`,
  fonction `resolveAgentWorkspaceDir`).
- **Installation** : clone dans `~/.openclaw/extensions/memoria` + `plugins.allow` +
  `plugins.entries.memoria.enabled/config` (`legacy/INSTALL.md`). Dépendance native :
  `better-sqlite3` — avec un piège ABI **déjà documenté par Memoria lui-même** :
  `legacy/CHANGELOG.md` v3.22.3 : « better-sqlite3 cross-Node-version build guide —
  `npx node-gyp rebuild --target=24.13.1` needed when shell Node differs from gateway's
  embedded Node ».

---

## 3. La surface plugin actuelle (2026.4.15 locale, confirmée par les docs 2026.6.x)

### 3.1 Les hooks existent toujours — et se sont enrichis

`$OC/dist/plugin-sdk/src/plugins/hook-types.d.ts:12` (version installée) liste 29 hooks typés :

```
before_model_resolve, before_prompt_build, before_agent_start, before_agent_reply,
llm_input, llm_output, agent_end, before_compaction, after_compaction, before_reset,
inbound_claim, message_received, message_sending, message_sent, before_tool_call,
after_tool_call, tool_result_persist, before_message_write, session_start, session_end,
subagent_spawning, subagent_delivery_target, subagent_spawned, subagent_ended,
gateway_start, gateway_stop, before_dispatch, reply_dispatch, before_install
```

**Les 6 hooks de Memoria y sont tous.** La doc de la version courante
([docs.openclaw.ai/plugins/hooks](https://docs.openclaw.ai/plugins/hooks)) les confirme et en
ajoute d'autres (`agent_turn_prepare`, `model_call_started/ended`, `heartbeat_prompt_contribution`,
`cron_changed`, `resolve_exec_env`, `reply_payload_sending`…). Dépréciations annoncées :
`before_agent_start` → migrer vers `before_model_resolve` + `before_prompt_build` ;
`deactivate` → `gateway_stop` (suppression après 2026-08-16).

Contrats utiles à l'adaptateur V3 (mêmes fichiers, version installée) :

- `before_prompt_build` : event `{ prompt, messages }` → résultat
  `{ systemPrompt?, prependContext?, prependSystemContext?, appendSystemContext? }`
  (`hook-before-agent-start.types.d.ts`). **Le retour `{ prependContext }` du recall legacy est
  donc toujours le bon mécanisme** — `modifyPrompt` n'existe pas dans l'API actuelle
  (absent de `OpenClawPluginApi`, `types.d.ts:1538-1657`). Les deux nouveaux champs
  `*SystemContext` servent le prompt-caching (guidance statique).
- `agent_end` : event `{ messages, success, error?, durationMs? }` + ctx
  `{ runId?, agentId?, sessionKey?, sessionId?, workspaceDir?, … }` (`hook-types.d.ts:18-29,63-68`).
  ⚠️ le champ `event.toolCallCount` lu par `legacy/index.ts:364` n'est **pas** dans le type — à
  revérifier au portage. La doc précise : fire-and-forget côté gateway, awaité (timeout 30 s) côté CLI.
- `llm_output` : event `{ runId, sessionId, provider, model, assistantTexts[], usage? }`
  (`hook-types.d.ts:48-62`).
- `after_tool_call` : `{ toolName, params, result?, error?, durationMs? }` (`hook-types.d.ts:177-185`).
- `session_start` / `session_end` / `before_compaction` / `before_reset` : nouveaux, très pertinents
  pour Memoria (capture avant perte de contexte ; `session_end` porte `reason`, `sessionFile`…).

### 3.2 L'API de plugin (`OpenClawPluginApi`) a beaucoup grossi

`$OC/dist/plugin-sdk/src/plugins/types.d.ts:1538-1657`. Points clés pour nous :

- `on<K extends PluginHookName>(hookName, handler, opts?: { priority? })` — typé, mais accepte la
  même forme d'appel que le legacy (noms inchangés). Un nom de hook inconnu est **ignoré avec un
  diagnostic warn** (loader : « unknown typed hook "…" ignored », `$OC/dist/loader-DYW2PvbF.js`,
  fonction `registerTypedHook`).
- `registerTool`, `registerCommand`, `registerService`, `registerHttpRoute`, `registerGatewayMethod`,
  `registerCli`, `registerHook` (événements internes coarse, distincts des hooks typés).
- **Slot mémoire exclusif** : `registerMemoryCapability({ promptBuilder?, flushPlanResolver?,
  runtime?, publicArtifacts? })` (`types.d.ts:1630`, contrat complet dans
  `$OC/dist/plugin-sdk/src/plugins/memory-state.d.ts`). Le propriétaire du slot se choisit dans la
  config : `plugins.slots.memory` (« "none" disables memory plugins »,
  `$OC/dist/plugin-sdk/src/config/types.plugins.d.ts`). Par défaut le slot appartient au plugin
  bundlé **`memory-core`** (cf. changelog 2026.4.x : « load the explicitly selected memory-slot
  plugin during gateway startup » #64423 ; `plugins.entries.memory-core.config.*`). Suppléments non
  exclusifs : `registerMemoryPromptSupplement`, `registerMemoryCorpusSupplement` (search/get d'un
  corpus additionnel), `registerMemoryEmbeddingProvider`.
- **Slot context-engine exclusif** : `registerContextEngine` (`types.d.ts:1624`), introduit en
  2026.3.7 (changelog : « ContextEngine plugin slot with full lifecycle hooks (bootstrap, ingest,
  assemble, compact, afterTurn…) », #22201) — l'alternative la plus profonde pour une mémoire.
- `api.pluginConfig` existe toujours (config de `plugins.entries.<id>.config`), `api.logger` aussi
  (signature quasi identique). `api.workspace` n'existe pas ; à la place : `ctx.workspaceDir` dans
  les hooks, `api.resolvePath`, et `OpenClawPluginServiceContext.workspaceDir`.

### 3.3 Politique de sécurité des hooks : `allowPromptInjection`

Nouveau depuis **2026.3.7** (changelog : « add `plugins.entries.<id>.hooks.allowPromptInjection`,
validate unknown typed hook names at runtime, … stripping prompt-mutating fields when prompt
injection is disabled », #36567).

- Schéma : `plugins.entries.<id>.hooks.allowPromptInjection?: boolean`
  (`types.plugins.d.ts:1-17`, zod strict dans `$OC/dist/zod-schema-BO9ySEsE.js`).
- Comportement (loader, `registerTypedHook`) : si **explicitement `false`**,
  `before_prompt_build` est **bloqué entièrement** (« typed hook … blocked by
  plugins.entries.<id>.hooks.allowPromptInjection=false ») et `before_agent_start` est contraint
  (champs prompt strippés via `stripPromptMutationFieldsFromLegacyHookResult`). **Non défini =
  autorisé** (le test est `=== false`).
- Pour Memoria : l'auto-recall dépend de ce flag. À documenter dans l'install V3 (et à vérifier
  sur la machine cassée — cf. §8).

### 3.4 Manifeste, chargement, découverte

- Manifeste **toujours** `openclaw.plugin.json` (JSON5 accepté). Champs **requis : `id` et
  `configSchema`** ; optionnels : `kind`, `name`, `version`, `enabledByDefault`,
  `legacyPluginIds`, `skills`, `contracts`, `commandAliases`, `uiHints`…
  (`$OC/dist/manifest-DKZWfJEu.js`, fonction `loadPluginManifest`). Le manifeste legacy de Memoria
  **reste structurellement valide**. Toujours pas de champ de compat de version hôte.
- Entrées candidates : `index.ts`, `index.js`, `index.mjs`, `index.cjs`
  (`DEFAULT_PLUGIN_ENTRY_CANDIDATES`, même fichier). Le TS est chargé via `jiti` (dépendance
  `jiti@^2.6.1`, `$OC/package.json`) — l'entrée TS de Memoria reste chargeable.
- Forme du module : `OpenClawPluginDefinition = { id?, configSchema?, register?(api), activate?(api), … }`
  ou directement `(api) => void` (`types.d.ts:1513-1526`). `export default { register }` legacy =
  toujours conforme. (`activate` est l'alias de compat, cf.
  [docs.openclaw.ai/plugins/compatibility](https://docs.openclaw.ai/plugins/compatibility).)
- Découverte : extensions bundlées + `<configDir>/extensions` (= `~/.openclaw/extensions`) +
  `<workspace>/.openclaw/extensions` + `plugins.load.paths`
  (`$OC/dist/discovery-DGQFjH8F.js`). **L'emplacement legacy `~/.openclaw/extensions/memoria`
  est donc toujours scanné.** Installation gérée : `openclaw plugins install
  <path|archive|npm:|git:|clawhub:|marketplace>` puis `openclaw plugins enable <id>` (sortie CLI
  locale + [docs.openclaw.ai/tools/plugin](https://docs.openclaw.ai/tools/plugin)).

### 3.5 Les vrais « breaking changes » plugin de la période (changelog embarqué + GitHub)

Source : `$OC/CHANGELOG.md` et
[github.com/openclaw/openclaw/blob/main/CHANGELOG.md](https://github.com/openclaw/openclaw/blob/main/CHANGELOG.md).

| Version | Breaking pertinent |
|---|---|
| 2026.1.20 | **Config inconnue/invalide ⇒ le gateway refuse de démarrer** (« Reject invalid/unknown config entries and refuse to start the gateway for safety. Run `openclaw doctor --fix` ») |
| 2026.3.7 | `allowPromptInjection` (cf. §3.3) ; slot ContextEngine |
| 2026.3.13 | Un seul fichier mémoire racine chargé (`MEMORY.md` prioritaire sur `memory.md`) — touche la stratégie syncMd legacy |
| 2026.3.22/24 | **Refonte SDK : seule surface publique = `openclaw/plugin-sdk/*` (sous-chemins étroits)** ; `openclaw/extension-api` retiré (en 2026.4.15 il subsiste en pont déprécié qui émet un warning, `$OC/dist/extensionAPI.js`). A cassé des plugins tiers : [issue #52902](https://github.com/openclaw/openclaw/issues/52902) (plugin Lark). Aussi : migrations de config > 2 mois supprimées (« very old legacy keys now fail validation »), install ClawHub-first |
| 2026.3.31 | **Scan d'installation fail-closed** : findings « dangerous-code critical » ⇒ install refusée sans `--dangerously-force-unsafe-install` ; dépréciation des sous-chemins provider legacy |
| 2026.4.2 / 2026.4.5 | Config plugin déplacée vers `plugins.entries.<id>.config.*` (modèle généralisé) ; suppression d'alias config legacy |
| 2026.4.24 | Suppression `api.registerEmbeddedExtensionFactory` (non utilisé par Memoria) |
| 2026.5.12 | Rien côté plugins (BlueBubbles/proxy) |

**Entre 2026.4.15 et 2026.6.5, aucune entrée « Breaking » du changelog ne supprime un des 6 hooks
ni le format de manifeste.** La politique officielle de compat
([docs.openclaw.ai/plugins/compatibility](https://docs.openclaw.ai/plugins/compatibility)) :
adaptateurs nommés, fenêtre max 3 mois entre warning et suppression.

---

## 4. MCP : oui, natif, dans les deux sens

### 4.1 Client MCP (consommer memoria-mcp) — vérifié dans le code installé

- Config typée au niveau racine : `OpenClawConfig.mcp?: McpConfig`
  (`$OC/dist/plugin-sdk/src/config/types.openclaw.d.ts:112`), avec
  `McpConfig.servers: Record<string, McpServerConfig>` ; `McpServerConfig` = **stdio**
  (`command`, `args`, `env`, `cwd`) ou **HTTP** (`url`, `transport: "sse" | "streamable-http"`,
  `headers`, `connectionTimeoutMs`) (`$OC/dist/plugin-sdk/src/config/types.mcp.d.ts`).
- Le runtime embarque le **SDK MCP officiel** : `$OC/dist/pi-bundle-mcp-tools-vusm-AE2.js`
  importe `@modelcontextprotocol/sdk/client` + `StdioClientTransport` + `SSEClientTransport` +
  `StreamableHTTPClientTransport` (lignes 9-12) et consomme
  `normalizeConfiguredMcpServers(params.cfg?.mcp?.servers)`.
- **Nommage des tools côté agent : `<serverName>__<toolName>`** (ligne 287 :
  `` `${params.serverName}__${candidateToolName}` `` ; renommage provider-safe loggé ligne 622).
  Introduit en 2026.3.31 (changelog : « materialize bundle MCP tools with provider-safe names
  (`serverName__toolName`), support optional `streamable-http` transport… », #49505).
- Doc : [docs.openclaw.ai/cli/mcp](https://docs.openclaw.ai/cli/mcp) — tools exposés dans les
  profils `coding` et `messaging`, `toolFilter.include/exclude` par serveur, backoff sur échecs
  répétés. (La doc actuelle ajoute `auth: "oauth"`, `probe`, `tools`, `login` — plus riche que la
  CLI 2026.4.15 locale qui n'a que `list/serve/set/show/unset`.)

### 4.2 Serveur MCP (exposer OpenClaw)

`openclaw mcp serve` « Expose OpenClaw channels over MCP stdio » (sortie CLI locale ; doc :
`openclaw mcp serve --url wss://… --token-file …`). Sans intérêt direct pour Memoria, mais
confirme que MCP est un citoyen de première classe.

### 4.3 Enregistrement exact d'un serveur MCP Memoria

Dans `~/.openclaw/openclaw.json` (ou via `openclaw mcp set memoria '<json>'`) :

```json
{
  "mcp": {
    "servers": {
      "memoria": {
        "command": "memoria-mcp",
        "args": [],
        "env": { "MEMORIA_STORAGE_ROOT": "~/.memoria/data" }
      }
    }
  }
}
```

→ l'agent voit `memoria__memoria_recall`, `memoria__memoria_store_fact`,
`memoria__memoria_capture_turn`, `memoria__memoria_set_context`, `memoria__memoria_get_context`
(les 5 tools déjà validés avec Claude Code, cf. `docs/v3/STATUS.md` « INSTALLATION RÉELLE »).
Variante HTTP (notre daemon écoute déjà en local) : `{ "url": "http://127.0.0.1:<port>/mcp",
"transport": "streamable-http", "headers": { "Authorization": "Bearer <token>" } }` — à n'activer
que si on ajoute un endpoint MCP HTTP au daemon ; le mode stdio suffit pour V1.

**Limite structurelle du MCP pur** : c'est du **pull**. OpenClaw n'offre aujourd'hui aucun
mécanisme MCP d'injection automatique avant chaque tour ni de notification de fin de tour
(vérifié : `pi-bundle-mcp-tools` ne fait que matérialiser des *tools* ; rien dans
`types.mcp.d.ts` ni la doc CLI MCP ne câble resources/prompts MCP dans le system prompt).
L'auto-recall et l'auto-capture de Memoria exigent donc soit les hooks (§3.1), soit la
coopération du modèle (system prompt qui ordonne d'appeler `memoria__memoria_recall`).

---

## 5. Alors, qu'est-ce qui a (probablement) cassé ?

Constat : **le contrat consommé par Memoria (manifeste, `register(api)`, `api.on` × 6, retour
`prependContext`) est toujours supporté dans 2026.4.15 et documenté dans 2026.6.x.** La casse
vient donc presque sûrement d'une (ou plusieurs) des couches autour, classées par probabilité :

1. **ABI native `better-sqlite3` vs Node du gateway** (probabilité haute). Le plugin embarque un
   module natif compilé pour UN Node ; OpenClaw exige désormais Node ≥ 22.14 (`$OC/package.json`)
   et les upgrades npm changent le runtime. C'est un mode de panne **déjà vécu et documenté par
   Memoria** (`legacy/CHANGELOG.md` v3.22.3 : crash silencieux sur gateway Node 24.x, fix =
   `node-gyp rebuild --target=…`). Symptôme type : `ERR_DLOPEN_FAILED / NODE_MODULE_VERSION
   mismatch` au `register()`, plugin marqué en erreur dans `openclaw plugins doctor`.
2. **Gateway qui refuse de démarrer ou purge la config** (probabilité moyenne-haute). Depuis
   2026.1.20 toute clé inconnue/invalide **bloque le démarrage** ; depuis 2026.3.24 les
   migrations de clés legacy > 2 mois sont supprimées (« very old legacy keys now fail validation »).
   Une config `openclaw.json` écrite à l'époque 2026.2/2026.3 peut être rejetée après upgrade —
   l'opérateur lance `openclaw doctor --fix`, qui peut désactiver/élaguer l'entrée plugin.
3. **Bug de mise à jour npm laissant les plugins silencieusement non chargés** (probabilité
   moyenne). [Issue #71812](https://github.com/openclaw/openclaw/issues/71812) : « openclaw update
   leaves plugin-runtime-deps/<version>/…/plugin-sdk in ENOTEMPTY state — every channel plugin
   silently fails to load » — exactement la fenêtre temporelle de notre casse (juin 2026), et un
   fix « CLI/update: prune stale packaged dist chunks after npm upgrades » est dans 2026.4.15
   (#66959). Symptôme : plugin présent mais aucun hook actif, zéro log.
4. **Réinstallation bloquée par le scan fail-closed** (probabilité moyenne si le plugin a été
   réinstallé via `openclaw plugins install`) : depuis 2026.3.31, des findings « critical » du
   scanner de code dangereux font échouer l'installation (Memoria fait du `fs` + SQLite natif +
   réseau Ollama — plausible). Contournement officiel : `--dangerously-force-unsafe-install`.
   N'affecte PAS le chargement depuis `~/.openclaw/extensions` déjà en place.
5. **Slot mémoire / memory-core** (probabilité faible pour la casse, certaine pour la friction) :
   le bundled `memory-core` possède le slot mémoire par défaut (prompt mémoire, `memory_get`,
   dreaming…). Memoria-legacy, qui n'enregistre aucune capability, cohabite en doublonnant la
   sémantique mémoire — pas un crash, mais des comportements croisés (double injection, budgets
   réduits par « trim default startup/skills prompt budgets », changelog 2026.4.15).
6. **`allowPromptInjection=false`** (probabilité faible : il faut l'avoir explicitement posé, ou
   qu'un durcissement par défaut soit intervenu dans 2026.5/2026.6 — non trouvé dans le changelog,
   mais à vérifier sur la machine cible) : recall mort, capture vivante — mort partielle silencieuse.

À noter : la refonte SDK 2026.3.22/24 (`openclaw/plugin-sdk/*`, suppression `extension-api`) a
cassé d'autres plugins tiers ([#52902](https://github.com/openclaw/openclaw/issues/52902)) mais
**pas mécaniquement Memoria**, qui n'importe l'hôte qu'en type (`import type … from
"openclaw/plugin-sdk/core"`, `legacy/index.ts:17`) — effacé à l'exécution.

---

## 6. Réponse à la question (c) : MCP natif — oui

Voir §4. Résumé : client MCP natif (stdio + SSE + streamable-http, SDK officiel), tools agent
préfixés `<serveur>__`, config `mcp.servers.<nom>` + CLI `openclaw mcp set/list/show/unset`
(2026.4.15) enrichie (`add/configure/probe/tools/login/…`) dans la version courante. OpenClaw est
aussi serveur MCP (`openclaw mcp serve`).

---

## 7. RECOMMANDATION pour l'adaptateur V3 (Phase 6)

**Hybride : MCP pur d'abord (Phase 3, trivial), adaptateur natif mince ensuite (Phase 6).**

### Étage 1 — Config MCP pure (disponible dès maintenant, P6 « trivial »)

- Une commande d'install qui fait `openclaw mcp set memoria
  '{"command":"memoria-mcp"}'` (ou édite `mcp.servers` du `openclaw.json`) + un README.
- Donne : recall/store/contexte **à la demande** dans tous les agents OpenClaw, zéro code dans le
  process du gateway, zéro exposition aux refontes du plugin-SDK, même binaire que pour Claude
  Code/Cursor (validé : STATUS.md « Claude Code connecté »).
- Ne donne PAS : auto-recall systématique ni auto-capture (§4.3). Atténuation possible sans
  plugin : instruire l'appel des tools mémoire via la guidance d'agent (AGENTS.md/SOUL.md du
  workspace), fiabilité dépendante du modèle.

### Étage 2 — Adaptateur natif mince `packages/adapters/openclaw` (Phase 6)

Un plugin OpenClaw **sans aucune logique mémoire et sans dépendance native** (c'est ce qui a tué
le legacy) : ~150-250 lignes qui traduisent les hooks en appels HTTP au daemon Memoria
(127.0.0.1 + token, transport déjà tranché — DECISIONS-LOG §4).

- Manifeste : `openclaw.plugin.json` `{ id: "memoria", version, configSchema (JSON Schema minimal :
  daemonUrl?, token?, autoRecall, autoCapture, recallLimit), uiHints }` — format inchangé (§3.4).
- Entrée `index.ts` : `register(api)` →
  - `api.on("before_prompt_build", …)` → `POST /recall` au daemon → retour
    `{ prependContext }` (+ budget court, timeout dur ~300 ms, **échec = log warn + pas
    d'injection**, jamais de throw) ;
  - `api.on("agent_end")` (+ `llm_output` si continuous) → `POST /capture_turn` fire-and-forget ;
  - `api.on("session_end" | "before_compaction" | "before_reset")` → flush de capture (nouveaux
    hooks, gains nets vs legacy) ;
  - aucun import runtime de `openclaw/plugin-sdk/*` (types only) → immunité maximale aux refontes.
- Install doc : `plugins.entries.memoria.hooks.allowPromptInjection` laissé par défaut (= autorisé)
  mais documenté ; `plugins.allow`/`enabled` comme avant.
- Option d'intégration plus profonde, **à évaluer seulement après** : `registerMemoryCapability`
  pour prendre le slot mémoire (`plugins.slots.memory = "memoria"`) et remplacer proprement
  `memory-core` (prompt builder + `MemorySearchManager`), et/ou `registerMemoryCorpusSupplement`
  pour brancher le corpus Memoria dans `memory_search` natif. Puissant mais couplé : à ne tenter
  qu'une fois l'étage hooks stabilisé, contre la version OpenClaw du moment.
- **Câblage côté monorepo (notes pour l'intégrateur)** : l'adaptateur vit dans
  `packages/adapters/openclaw` (spec §4 : le core ne connaît aucun hook d'hôte) ; il ne parle
  qu'au daemon HTTP — jamais à `packages/core` directement ni aux fichiers SQLite.

### Pourquoi pas « MCP pur » seul ?

Parce que la proposition de valeur de Memoria (mémoire **automatique** : auto-recall layer 6,
continuous learning layer 21, capture layer 1) exige des points d'accroche par tour, que MCP ne
fournit pas chez OpenClaw aujourd'hui (§4.3). Et pourquoi pas « hooks seuls » ? Parce que le MCP
donne l'accès explicite multi-hôtes (Claude Code, Cursor…) déjà opérationnel et sert de chemin de
secours quand une release OpenClaw casse l'étage hooks — exactement le scénario qu'on vient de vivre.

---

## 8. Incertitudes restantes et comment les lever

1. **Version exacte d'OpenClaw sur le Mac Studio + état réel du plugin.** À relever sur place :
   `openclaw --version`, `openclaw plugins list`, `openclaw plugins doctor`,
   `openclaw doctor`, et les logs gateway au boot (diagnostics du loader : chaque échec de
   chargement/hook y est mentionné, cf. `pushDiagnostic` dans `$OC/dist/loader-DYW2PvbF.js`).
   C'est LA donnée qui transformera le §5 (candidats) en cause confirmée.
2. **Reproduction locale sans risque** : `OPENCLAW_STATE_DIR=$(mktemp -d) openclaw …` avec un
   `openclaw.json` minimal pointant `plugins.load.paths` vers une copie de `legacy/` — permet de
   voir le diagnostic exact du loader sur la 2026.4.15 (et sur `npm:openclaw@latest` dans un
   prefix jetable) sans toucher l'état machine. Non fait ici (mission lecture seule ; le gateway
   exécute du code, et `legacy/` dépend d'un `npm install` + Ollama).
3. **Comportement par défaut `allowPromptInjection` dans 2026.5/2026.6** : vérifié `=== false`
   (donc permissif) dans 2026.4.15 ; aucun durcissement trouvé au changelog jusqu'à 2026.6.5, mais
   à re-vérifier sur la version cible au moment de la Phase 6 (cadence de release quotidienne).
4. **Payloads exacts des hooks sur la version cible** (ex. `event.toolCallCount` absent du type
   `PluginHookAgentEndEvent`, §3.1) : figer en Phase 6 par un test de contrat dans l'adaptateur
   (boot d'un gateway sandbox + assertions sur les events reçus), pas par confiance dans les d.ts.
5. **MCP « push » futur** : surveiller si OpenClaw expose un jour resources/prompts MCP ou un
   équivalent d'injection automatique pilotée par serveur MCP — ça rendrait l'étage 2 optionnel.
   ([docs.openclaw.ai/cli/mcp](https://docs.openclaw.ai/cli/mcp), changelog).
6. **Distribution** : `openclaw plugins install` préfère ClawHub depuis 2026.3.22 et scanne le code
   (fail-closed). Pour la release V3 : tester l'install de l'adaptateur via le scanner (zéro
   dépendance native aide beaucoup) et évaluer une publication ClawHub.

---

## Annexe — inventaire des preuves locales

| Élément | Chemin |
|---|---|
| Package npm OpenClaw 2026.4.15 | `/Users/primostudio/.nvm/versions/node/v22.22.2/lib/node_modules/openclaw/` |
| Types plugin API (1658 l.) | `$OC/dist/plugin-sdk/src/plugins/types.d.ts` |
| Types hooks (415 l.) | `$OC/dist/plugin-sdk/src/plugins/hook-types.d.ts` |
| Types prompt-injection | `$OC/dist/plugin-sdk/src/plugins/hook-before-agent-start.types.d.ts` |
| Types slot mémoire | `$OC/dist/plugin-sdk/src/plugins/memory-state.d.ts` |
| Types config plugins/slots | `$OC/dist/plugin-sdk/src/config/types.plugins.d.ts` |
| Types MCP | `$OC/dist/plugin-sdk/src/config/types.mcp.d.ts` |
| Runtime MCP client | `$OC/dist/pi-bundle-mcp-tools-vusm-AE2.js` |
| Loader plugins (politique hooks) | `$OC/dist/loader-DYW2PvbF.js` |
| Parser manifeste | `$OC/dist/manifest-DKZWfJEu.js` |
| Découverte plugins | `$OC/dist/discovery-DGQFjH8F.js` |
| Changelog embarqué (jusqu'à 2026.4.15) | `$OC/CHANGELOG.md` |
| Vestiges app macOS | `~/Library/Application Support/OpenClaw/{bridge.sock,identity/}` |
| Contrat legacy Memoria | `legacy/openclaw.d.ts`, `legacy/openclaw.plugin.json`, `legacy/index.ts`, `legacy/{recall,continuous,capture,procedural-hooks}.ts`, `legacy/INSTALL.md`, `legacy/CHANGELOG.md` |

URLs : [docs.openclaw.ai/plugins/hooks](https://docs.openclaw.ai/plugins/hooks) ·
[docs.openclaw.ai/plugins/compatibility](https://docs.openclaw.ai/plugins/compatibility) ·
[docs.openclaw.ai/plugins/sdk-migration](https://docs.openclaw.ai/plugins/sdk-migration) ·
[docs.openclaw.ai/tools/plugin](https://docs.openclaw.ai/tools/plugin) ·
[docs.openclaw.ai/cli/mcp](https://docs.openclaw.ai/cli/mcp) ·
[github.com/openclaw/openclaw/blob/main/CHANGELOG.md](https://github.com/openclaw/openclaw/blob/main/CHANGELOG.md) ·
[issue #52902](https://github.com/openclaw/openclaw/issues/52902) ·
[issue #71812](https://github.com/openclaw/openclaw/issues/71812)
