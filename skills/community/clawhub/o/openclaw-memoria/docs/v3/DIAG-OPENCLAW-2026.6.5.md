# DIAG-OPENCLAW-2026.6.5 — Compatibilité Memoria V3 ⇄ OpenClaw 2026.6.5

> **Mission** : maintenant que `openclaw@latest` (2026.6.5) est installé localement, déterminer
> EXACTEMENT ce qu'il faut pour écrire l'adaptateur OpenClaw de Memoria (couche 6 de la roadmap).
> Vérifie si les conclusions du `DIAG-OPENCLAW.md` (basé sur **2026.4.15**) tiennent toujours.
> **Lecture seule** — aucune config de production modifiée (`~/.openclaw/openclaw.json` n'existe
> même pas encore ; `mcp list/show` confirmés vides). Aucun `mcp set` de test n'a été nécessaire :
> tout a été vérifié dans les types/JS du `dist`.
>
> **Date** : 2026-06-11 · **Auteur** : Claude (Opus 4.8) · suite de `docs/v3/DIAG-OPENCLAW.md`.
>
> `$OC` = `/Users/primostudio/.nvm/versions/node/v22.22.2/lib/node_modules/openclaw`.
> Toutes les affirmations sont sourcées par un chemin (+ ligne) dans `$OC/dist` ou par une sortie CLI.

---

## TL;DR (ce qui a changé vs 2026.4.15, et ce que ça implique)

1. **Version réellement installée = `2026.6.5 (5181e4f)`** (`openclaw --version`), `engines.node`
   est passé de `>=22.14.0` à **`>=22.19.0`** (`$OC/package.json`). Le binaire est bien la nouvelle
   version (symlink `bin/openclaw → ../lib/node_modules/openclaw/openclaw.mjs`, daté 11 juin).
2. **Correction de cadrage important** : le schéma de version a changé. `2026.6.5` n'est **pas** une
   date calendaire (`AAAA.M.J`) comme le supposait le diag précédent, mais **`YYYY.M.PATCH`
   (numérotation de patch mensuelle)** : « switch release trains to `YYYY.M.PATCH` monthly patch
   numbering … pin the June 2026 floor at `2026.6.5` » (`$OC/CHANGELOG.md:30`). Donc 2026.6.5 = «train
   de juin, patch 5 », et non « 5 juin ».
3. **Les 6 hooks de Memoria existent toujours, intacts, et typés.** L'union de hooks est passée de
   29 (2026.4.15) à **39** (`PLUGIN_HOOK_NAMES`, `$OC/dist/hook-types-vtRHl7ZH.d.ts:332`). Aucun des
   6 hooks Memoria n'a disparu ni changé de payload de façon cassante (§2).
4. **LE changement bloquant pour Memoria** : un **nouveau gate de sécurité `allowConversationAccess`**
   (absent en 2026.4.15) **bloque par défaut** les *conversation hooks* pour tout plugin **non
   bundlé**. Memoria utilise `llm_output` et `agent_end`, qui sont des conversation hooks → **ils
   seront silencieusement bloqués** (warn + `return`) tant que la config ne pose pas
   `plugins.entries.memoria.hooks.allowConversationAccess=true`
   (`$OC/dist/registry-CQTOYCVL.js:4573-4592`). **C'est la cause #1 probable de la « casse » d'auto-capture
   en 2026.5/2026.6** — un nouveau « mort silencieux » qui n'existait pas au diag précédent.
5. **`allowPromptInjection` : inchangé** — ne bloque `before_prompt_build` que si **explicitement
   `=== false`** ; non défini = autorisé (`registry-CQTOYCVL.js:4555`). L'auto-recall reste OK par défaut.
6. **MCP natif : toujours là, enrichi.** Config `mcp.servers.<nom>` identique (stdio
   `{command,args,env,cwd}` ou HTTP `{url,transport,headers}`) ; CLI passée de 5 à **17 sous-commandes**
   (`add/configure/doctor/login/logout/probe/reload/status/tools` en plus). `openclaw mcp set` écrit
   bien `~/.openclaw/openclaw.json` (confirmé par le message du CLI). Recette exacte en §4.
7. **API plugin `register(api)` / `api.on(...)` / `api.pluginConfig` : inchangée et compatible
   legacy.** `api.on` accepte maintenant `{ priority?, timeoutMs? }` ; `modifyPrompt`/`workspace`
   restent absents (ils l'étaient déjà). Manifeste `openclaw.plugin.json` legacy toujours
   structurellement valide (§3).
8. **Recommandation inchangée mais précisée** : (a) **MCP pur** branche le recall/store/contexte
   « pull » tout de suite, zéro risque ; (b) **adaptateur hooks mince** (~180-260 lignes, zéro
   dépendance native) pour l'auto-recall/auto-capture, qui parle au **daemon Memoria HTTP** —
   **OBLIGATOIREMENT accompagné de l'instruction d'install `allowConversationAccess=true`**, sinon la
   capture est morte. Détails et mapping en §5.

---

## 1. Surface CLI — ce qui a bougé

| Domaine | 2026.4.15 (diag précédent) | 2026.6.5 (vérifié) | Preuve |
|---|---|---|---|
| Version | `2026.4.15 (041266a)` | `2026.6.5 (5181e4f)` | `openclaw --version` |
| Node requis | `>=22.14.0` | **`>=22.19.0`** | `$OC/package.json` (`engines.node`) |
| Schéma version | calendaire `AAAA.M.J` (supposé) | **`YYYY.M.PATCH` mensuel** | `$OC/CHANGELOG.md:30` |
| `openclaw mcp` | `list/serve/set/show/unset` (5) | **17** : `add, configure, doctor, list, login, logout, probe, reload, serve, set, show, status, tools, unset` | `openclaw mcp --help` |
| `openclaw plugins` | install/enable/list/doctor… | `build, disable, doctor, enable, init, inspect, install, list, marketplace, registry, search, uninstall, update, validate` | `openclaw plugins --help` |
| `--dangerously-force-unsafe-install` | bypass du scanner fail-closed | **« Deprecated no-op ; install policy and plugin hooks may still block »** | `openclaw plugins install --help` |

**Implication scanner** : le contournement historique du scan d'install a disparu (no-op). Pour
distribuer l'adaptateur sans heurter le scanner fail-closed, la bonne stratégie reste **zéro
dépendance native** + install locale (`plugins install --link <path>` ou dépôt direct dans
`~/.openclaw/extensions/`), pas un npm spec scanné. La policy d'install configurable vit dans
`security.installPolicy.*` (`$OC/dist/install-policy-C38HHrq7.js`).

---

## 2. Les 6 hooks Memoria en 2026.6.5 — état et gating

Source unique : `$OC/dist/hook-types-vtRHl7ZH.d.ts` (1036 l.). Les 6 hooks sont **présents dans
`PLUGIN_HOOK_NAMES` (l.332) et dans `PluginHookHandlerMap` (l.~970-993)**, avec ces signatures :

| Hook | Présent | Event type | Result | Ligne handler-map |
|---|---|---|---|---|
| `before_prompt_build` | ✅ | `PluginHookBeforePromptBuildEvent {prompt, messages}` | `{ systemPrompt?, prependContext?, appendContext?, prependSystemContext?, appendSystemContext? }` | 973 |
| `message_received` | ✅ | `PluginHookMessageReceivedEvent {from, content, …}` | `void` | 989 |
| `llm_output` | ✅ | `PluginHookLlmOutputEvent {runId, sessionId, provider, model, assistantTexts[], usage?, …}` | `void` | 979 |
| `after_tool_call` | ✅ | `PluginHookAfterToolCallEvent {toolName, params, result?, error?, durationMs?, runId?, toolCallId?}` | `void` | 993 |
| `agent_end` | ✅ | `PluginHookAgentEndEvent {runId?, messages, success, error?, durationMs?}` | `void` | 981 |
| `after_compaction` | ✅ | `PluginHookAfterCompactionEvent {messageCount, tokenCount?, compactedCount, sessionFile?}` | `void` | 983 |

### 2.1 Les DEUX gates qui décident si un hook Memoria s'exécute

Toute la logique d'autorisation est dans `registerTypedHook` :
`$OC/dist/registry-CQTOYCVL.js:4554-4599`.

- **`allowPromptInjection`** (l.4555) — concerne `PROMPT_INJECTION_HOOK_NAMES =
  ["agent_turn_prepare","before_prompt_build","before_agent_start","heartbeat_prompt_contribution"]`
  (`hook-types…:354`). Le hook n'est bloqué **que si `policy.allowPromptInjection === false`**. Non
  défini ⇒ **autorisé**. → **`before_prompt_build` (auto-recall) marche par défaut.** Inchangé vs 4.15.

- **`allowConversationAccess`** — **NOUVEAU en 2026.5/2026.6, absent en 2026.4.15.** Concerne
  `CONVERSATION_HOOK_NAMES = ["before_model_resolve","before_agent_reply","llm_input","llm_output",
  "before_agent_finalize","agent_end","before_agent_run"]` (`hook-types…:357`). Règle exacte
  (`registry-CQTOYCVL.js:4573-4592`) :
  ```js
  if (isConversationHookName(effectiveHookName)) {
    const explicitConversationAccess = policy?.allowConversationAccess;
    if (record.origin !== "bundled" && explicitConversationAccess !== true) {
      pushDiagnostic({ level:"warn", …,
        message:`typed hook "${hook}" blocked because non-bundled plugins must set
                 plugins.entries.${id}.hooks.allowConversationAccess=true` });
      return;                       // ← le handler n'est JAMAIS enregistré
    }
    if (record.origin === "bundled" && explicitConversationAccess === false) { …return; }
  }
  ```
  Schéma de config associé : `PluginEntryConfig.hooks.allowConversationAccess?: boolean`
  (`$OC/dist/types.openclaw-fYj4Ft14.d.ts:1452-1461`), aide opérateur
  `$OC/dist/runtime-schema-BV2sevMc.js:804`, zod `$OC/dist/zod-schema-Cx66_mMP.js:790`.

### 2.2 Tableau de gating des 6 hooks Memoria

| Hook | Gate prompt-injection | Gate conversation-access | Conséquence si rien configuré (plugin **non bundlé**) |
|---|---|---|---|
| `before_prompt_build` | oui (OK sauf `=false`) | non | **fonctionne** (auto-recall OK) |
| `message_received` | non | non | **fonctionne** |
| `after_tool_call` | non | non | **fonctionne** |
| `after_compaction` | non | non | **fonctionne** |
| `llm_output` | non | **OUI** | **BLOQUÉ** (continuous learning mort) |
| `agent_end` | non | **OUI** | **BLOQUÉ** (capture session + auto-skill mort) |

➡️ **Sans `allowConversationAccess=true`, l'auto-capture de Memoria (couches 1 + 21) est
silencieusement désactivée.** L'auto-recall (couche 6) survit. C'est exactement le profil « mort
silencieux partiel » redouté dans le diag précédent (§8.3), et la cause la plus plausible de la
régression observée sur le Mac Studio en 2026.5/2026.6.

### 2.3 Autres deltas de hooks (non bloquants)

- Union passée à 39 hooks ; **nouveaux** : `agent_turn_prepare`, `before_agent_run`,
  `before_agent_finalize`, `model_call_started`, `model_call_ended`, `heartbeat_prompt_contribution`,
  `cron_changed`, `resolve_exec_env`, plus `deactivate` formalisé.
- **Dépréciés** : `subagent_spawning` et `deactivate` (`DeprecatedPluginHookName`,
  `hook-types…:333`) — non utilisés par Memoria.
- `before_prompt_build` result gagne `appendContext` (en plus de `prepend*`/`*SystemContext`).
  Memoria retourne `{ prependContext }` → **toujours le bon mécanisme**.
- ⚠️ **`event.toolCallCount` lu par `legacy/index.ts:364` n'existe TOUJOURS pas** dans
  `PluginHookAgentEndEvent` (vérifié l.453 du d.ts). Le legacy lisait donc `undefined → 0` depuis
  toujours ; à corriger au portage (compter via `after_tool_call` ou via `event.messages`).
- `api.on(hook, handler, { priority?, timeoutMs? })` — `timeoutMs` est nouveau
  (`types-C_nat0ED.d.ts:8408-8411`) ; per-hook timeout aussi via
  `plugins.entries.<id>.hooks.timeoutMs`/`timeouts`.

---

## 3. API plugin & manifeste — compatibilité legacy

Fichier principal : `$OC/dist/types-C_nat0ED.d.ts`.

- **`OpenClawPluginApi` (l.8177-8412)** conserve tout ce dont Memoria a besoin :
  `config: OpenClawConfig` (8185), `pluginConfig?: Record<string,unknown>` (8186),
  `logger: PluginLogger` (8194), `resolvePath` (8407),
  `on:<K extends PluginHookName>(hookName, handler, opts?)` (8408), `registerTool` (8203),
  `registerMemoryCapability` (8382), `registerMemoryCorpusSupplement` (8389), `registerContextEngine`
  (8268). **Toujours pas de `modifyPrompt` ni `workspace`** (ils étaient déjà absents en 4.15 ;
  le stub `legacy/openclaw.d.ts` les déclarait à tort mais le runtime ne les appelle jamais).
- **Nouveauté** : l'API expose des **façades groupées** `api.session`, `api.agent`,
  `api.runContext`, `api.lifecycle` ; beaucoup de méthodes plates (`registerRuntimeLifecycle`,
  `setRunContext`, `registerSessionExtension`…) sont **`@deprecated` au profit de ces façades** —
  Memoria n'en utilise aucune, donc sans impact.
- **`OpenClawPluginDefinition` (l.8015-8034)** : `{ id?, name?, version?, kind?, configSchema?,
  register?(api), activate?(api), … }`. **`export default { register }` du legacy reste conforme.**
  `kind` runtime est `@deprecated` au profit du `kind` du manifeste (sans objet pour un plugin de
  hooks pur, qui n'a pas de `kind`).
- **Manifeste** : `legacy/openclaw.plugin.json` (`{id, version, configSchema, uiHints, description,
  keywords}`) reste structurellement valide. Référence d'un manifeste 2026.6.5 « riche » :
  `$OC/dist/extensions/memory-core/openclaw.plugin.json` (`{id, kind:"memory", contracts,
  activation, commandAliases, uiHints, configSchema}`). Toujours aucun champ de compat de version hôte.
- **Slot mémoire** : défaut **toujours `memory-core`** (`$OC/dist/slots-kpL659LX.js:7`
  `memory:"memory-core"` ; `$OC/dist/extensions/memory-core/` bundlé). Remplaçable via
  `plugins.slots.memory = "memoria"` (`PluginSlotsConfig`, `types.openclaw…:1482`). Réservé à l'option
  « intégration profonde » (§5.3), pas au V1.

---

## 4. RECETTE EXACTE — connecter Memoria par MCP (disponible immédiatement)

### 4.1 Commande

```bash
# variante stdio (recommandée pour V1 — même binaire que Claude Code / Cursor) :
openclaw mcp set memoria '{"command":"node","args":["/Users/primostudio/openclaw-memoria/packages/mcp/dist/bin.js","serve","--instance","koda"]}'

# OU forme « add » (probe avant de sauver, refuse si le serveur ne répond pas) :
openclaw mcp add memoria \
  --command node \
  --arg /Users/primostudio/openclaw-memoria/packages/mcp/dist/bin.js \
  --arg serve --arg --instance --arg koda
```

### 4.2 Fichier config résultant (`~/.openclaw/openclaw.json`)

Le CLI écrit **`~/.openclaw/openclaw.json`** (confirmé par le message :
« No MCP servers configured in `/Users/primostudio/.openclaw/openclaw.json` »). Bloc produit :

```json
{
  "mcp": {
    "servers": {
      "memoria": {
        "command": "node",
        "args": [
          "/Users/primostudio/openclaw-memoria/packages/mcp/dist/bin.js",
          "serve", "--instance", "koda"
        ]
      }
    }
  }
}
```

Schéma exact accepté : `McpServerConfig` (`$OC/dist/types.openclaw-fYj4Ft14.d.ts:1398-1428`) —
stdio (`command/args/env/cwd`) ou HTTP (`url`, `transport:"sse"|"streamable-http"`, `headers`,
`auth:"oauth"`, mTLS…). Variante HTTP (si on ajoute un endpoint MCP au daemon Memoria) :
`{"url":"http://127.0.0.1:<port>/mcp","transport":"streamable-http","headers":{"Authorization":"Bearer <token>"}}`.

### 4.3 Vérification

```bash
openclaw mcp list            # liste les serveurs
openclaw mcp probe memoria   # connecte et liste les tools réellement exposés
openclaw mcp status          # transport status sans se connecter
```

Côté agent, les tools apparaissent **préfixés `memoria__`** : `memoria__memoria_recall`,
`memoria__memoria_store_fact`, `memoria__memoria_capture_turn`, `memoria__memoria_set_context`,
`memoria__memoria_get_context` (nommage `<serverName>__<toolName>`, déjà vérifié dans le diag
précédent et inchangé). **Retrait propre** : `openclaw mcp unset memoria`.

### 4.4 Limite (inchangée)

Le MCP reste du **pull** : pas d'injection automatique avant chaque tour, pas de notification de fin
de tour. L'auto-recall/auto-capture exige donc soit les hooks (§5), soit une guidance d'agent
(AGENTS.md) qui ordonne d'appeler `memoria__memoria_recall`/`memoria__memoria_capture_turn`.

---

## 5. Adaptateur hooks — est-il nécessaire, et quoi écrire précisément ?

**Oui, nécessaire** si on veut l'auto-recall ET l'auto-capture (la proposition de valeur de
Memoria). Le MCP pur (§4) ne donne que le « pull ». L'adaptateur reste un **plugin OpenClaw mince,
zéro logique mémoire, zéro dépendance native**, qui traduit les hooks en appels HTTP au **daemon
Memoria** (127.0.0.1 + token).

### 5.1 Manifeste `packages/adapters/openclaw/openclaw.plugin.json`

```jsonc
{
  "id": "memoria",
  "version": "3.x",
  "configSchema": {
    "type": "object",
    "additionalProperties": true,
    "properties": {
      "daemonUrl":   { "type": "string", "default": "http://127.0.0.1:7077" },
      "token":       { "type": "string" },
      "instance":    { "type": "string", "default": "koda" },
      "autoRecall":  { "type": "boolean", "default": true },
      "autoCapture": { "type": "boolean", "default": true },
      "recallLimit": { "type": "number", "default": 12, "minimum": 1, "maximum": 20 }
    }
  },
  "uiHints": { "autoRecall": { "label": "Auto-Recall" }, "autoCapture": { "label": "Auto-Capture" } }
}
```
Pas de `kind` (plugin de hooks, pas de slot exclusif). Format validé vs `loadPluginManifest` 6.5.

### 5.2 Entrée `index.ts` — mapping hooks → daemon HTTP (~180-260 lignes)

```ts
import type { OpenClawPluginApi } from "openclaw/plugin-sdk/core"; // TYPE ONLY (effacé au runtime)

export function register(api: OpenClawPluginApi): void {
  const cfg = api.pluginConfig ?? {};
  const base = String(cfg.daemonUrl ?? "http://127.0.0.1:7077");
  const headers = cfg.token ? { Authorization: `Bearer ${cfg.token}` } : {};
  const post = (path, body, timeoutMs) =>
    fetch(base + path, { method:"POST", headers:{ "content-type":"application/json", ...headers },
      body: JSON.stringify(body), signal: AbortSignal.timeout(timeoutMs) });

  // (1) AUTO-RECALL — prompt-injection hook, OK par défaut (allowPromptInjection != false)
  if (cfg.autoRecall !== false) {
    api.on("before_prompt_build", async (event, ctx) => {
      try {
        const r = await post("/recall",
          { instance: cfg.instance, prompt: event.prompt, limit: cfg.recallLimit,
            sessionId: ctx?.sessionId, agentId: ctx?.agentId }, 300); // timeout dur 300 ms
        if (!r.ok) return;                       // échec = pas d'injection, jamais de throw
        const { prependContext } = await r.json();
        if (prependContext) return { prependContext };
      } catch (e) { api.logger.warn?.(`memoria recall skipped: ${String(e)}`); }
    }, { timeoutMs: 500 });
  }

  // (2) AUTO-CAPTURE — agent_end est un CONVERSATION hook → exige allowConversationAccess=true
  if (cfg.autoCapture !== false) {
    api.on("agent_end", async (event, ctx) => {
      try {
        await post("/capture_turn",
          { instance: cfg.instance, messages: event.messages, success: event.success,
            durationMs: event.durationMs, sessionId: ctx?.sessionId, agentId: ctx?.agentId }, 1500);
      } catch (e) { api.logger.warn?.(`memoria capture skipped: ${String(e)}`); }
    });
    // continuous learning (optionnel) — llm_output est AUSSI un conversation hook
    api.on("llm_output", async (event, ctx) => { /* POST /continuous fire-and-forget */ });
  }

  // (3) flush avant perte de contexte — NON gatés (gains nets vs legacy) :
  api.on("before_compaction", async (e) => { /* POST /flush */ });   // ni conv ni PI
  api.on("session_end",      async (e) => { /* POST /flush */ });    // ni conv ni PI
  // after_compaction / message_received / after_tool_call disponibles librement aussi.
}
export default { register };
```

### 5.3 ⚠️ INSTALL — l'étape sans laquelle la capture est morte

L'install DOIT poser le gate conversation, sinon `agent_end`/`llm_output` sont bloqués
silencieusement (§2.1). Dans `~/.openclaw/openclaw.json` :

```jsonc
{
  "plugins": {
    "allow": ["memoria"],
    "entries": {
      "memoria": {
        "enabled": true,
        "hooks": {
          "allowConversationAccess": true,   // ← OBLIGATOIRE pour agent_end + llm_output
          "allowPromptInjection": true       // (optionnel : défaut déjà permissif, mais explicite = robuste)
        },
        "config": { "daemonUrl": "http://127.0.0.1:7077", "token": "…", "instance": "koda" }
      }
    }
  }
}
```

- `plugins.entries.memoria.config.*` = la config lue par `api.pluginConfig`
  (modèle `plugins.entries.<id>.config`, `PluginEntryConfig.config`, `types.openclaw…:1480`).
- Découverte : déposer le plugin dans `~/.openclaw/extensions/memoria/` (toujours scanné) ou
  `openclaw plugins install --link <path>` ; puis `openclaw plugins enable memoria`.
- Vérif post-install : `openclaw plugins doctor` et `openclaw plugins inspect memoria` (affiche
  `policy.allowConversationAccess` / `allowPromptInjection`,
  `$OC/dist/plugins-inspect-command-DdC8RSLD.js:239`). Au boot du gateway, tout hook bloqué émet un
  warn « blocked because non-bundled plugins must set … » (`pushDiagnostic`) — à grepper dans les logs.

### 5.4 Intégration profonde (à NE PAS faire en V1)

`registerMemoryCapability({ promptBuilder, flushPlanResolver, runtime })` (l.8382) pour prendre le
**slot mémoire** (`plugins.slots.memory="memoria"`) et remplacer `memory-core`, et/ou
`registerMemoryCorpusSupplement` (l.8389) pour brancher le corpus Memoria dans le `memory_search`
natif. Puissant mais couplé à l'évolution du SDK ; à n'envisager qu'une fois l'étage hooks stabilisé.

---

## 6. Verdict — les conclusions du DIAG-OPENCLAW.md tiennent-elles ?

| Conclusion 2026.4.15 | Statut 2026.6.5 |
|---|---|
| OpenClaw parle MCP nativement (`mcp set`) | ✅ **Tient**, CLI enrichie (17 sous-commandes), config identique |
| Les 6 hooks legacy existent toujours | ✅ **Tient** (39 hooks typés, les 6 présents et stables) |
| Adaptateur (a) config MCP pure / (b) plugin hooks mince | ✅ **Tient**, mais (b) **DOIT** ajouter `allowConversationAccess=true` |
| `allowPromptInjection` permissif par défaut | ✅ **Tient** (`=== false` seulement) |
| `register(api)` + `api.on` + `pluginConfig` compatibles | ✅ **Tient** (`on` gagne `timeoutMs`) |
| `event.toolCallCount` (agent_end) douteux | ✅ **Confirmé absent** — à corriger au portage |
| `memory-core` = slot mémoire par défaut | ✅ **Tient** |

**Nouveauté majeure non anticipée** : le gate **`allowConversationAccess`** (par défaut **bloquant**
pour les plugins non bundlés sur `agent_end`/`llm_output`/etc.). C'est le seul vrai « breaking » pour
Memoria entre 2026.4.15 et 2026.6.5, et il explique proprement une régression silencieuse de la
capture.

---

## 7. Pièges & incertitudes restants

1. **`allowConversationAccess` par défaut = bloquant** : c'est LE piège. Toute install/doc Memoria
   doit le poser, et tout diagnostic terrain doit le vérifier en premier (`plugins inspect memoria`
   + logs « blocked because non-bundled… »). Risque : un opérateur qui met à jour OpenClaw sans
   re-poser ce flag perd la capture sans message d'erreur visible côté UX.
2. **Node ABI** : `engines.node >=22.19.0`. Si l'adaptateur garde **zéro dépendance native** (il
   parle au daemon par HTTP), le piège `better-sqlite3` du legacy disparaît entièrement. À ne PAS
   réintroduire de SQLite natif dans l'adaptateur.
3. **Scanner d'install fail-closed renforcé** : `--dangerously-force-unsafe-install` est un no-op.
   Tester l'install réelle de l'adaptateur (zéro dépendance native aide) ; sinon, install locale par
   `--link`/dépôt dans `extensions/`. Policy : `security.installPolicy.*`.
4. **Payloads de hooks** : valider sur la version cible par un **test de contrat** (gateway sandbox
   `OPENCLAW_STATE_DIR=$(mktemp -d)` + assertions sur les events reçus) plutôt que par confiance dans
   les `.d.ts`. En particulier `agent_end.messages` (forme exacte) et l'absence de `toolCallCount`.
5. **Cadence mensuelle + numérotation `YYYY.M.PATCH`** : re-vérifier `allowConversationAccess`
   (défaut) et `allowPromptInjection` à chaque train mensuel ; le durcissement de 2026.5/2026.6
   montre que ces défauts peuvent changer.
6. **Façades API dépréciées** : ne pas utiliser les méthodes plates `@deprecated`
   (`registerRuntimeLifecycle`, `registerSessionExtension`, `setRunContext`…). Memoria n'en a pas
   besoin, mais éviter de les introduire au portage.
7. **MCP « push » futur** : surveiller si OpenClaw expose un jour resources/prompts MCP injectés au
   prompt → rendrait l'étage hooks optionnel. Toujours pas le cas en 2026.6.5.

---

## Annexe — inventaire des preuves (2026.6.5)

| Élément | Chemin |
|---|---|
| Package npm OpenClaw 2026.6.5 | `$OC/` (`engines.node >=22.19.0`) |
| Hooks (union 39, handler map, gates) | `$OC/dist/hook-types-vtRHl7ZH.d.ts` (l.332, 354, 357, 453, 973-993) |
| **Enforcement des gates** (allowConversationAccess / allowPromptInjection) | `$OC/dist/registry-CQTOYCVL.js:4554-4599` |
| Types config (mcp, plugins.entries, slots, allowConversationAccess) | `$OC/dist/types.openclaw-fYj4Ft14.d.ts` (l.1398-1431, 1449-1482) |
| Aide opérateur `allowConversationAccess` | `$OC/dist/runtime-schema-BV2sevMc.js:804` |
| Zod schema hooks | `$OC/dist/zod-schema-Cx66_mMP.js:790` |
| API plugin (`OpenClawPluginApi`, `OpenClawPluginDefinition`) | `$OC/dist/types-C_nat0ED.d.ts` (l.8015-8034, 8177-8412) |
| Slot mémoire par défaut = memory-core | `$OC/dist/slots-kpL659LX.js:7` ; `$OC/dist/extensions/memory-core/openclaw.plugin.json` |
| Install policy / scanner fail-closed | `$OC/dist/install-policy-C38HHrq7.js`, `$OC/dist/install-security-scan-DyrEAKit.js` |
| Changelog 2026.6.5 (versioning `YYYY.M.PATCH`) | `$OC/CHANGELOG.md:30` |
| Config dir réelle | `~/.openclaw/openclaw.json` (confirmé par message CLI `mcp list`) |
| Contrat legacy Memoria | `legacy/openclaw.plugin.json`, `legacy/openclaw.d.ts`, `legacy/index.ts:58,359,364,388` |

URLs de référence (inchangées) : docs.openclaw.ai/plugins/hooks · /plugins/compatibility ·
/cli/mcp · /cli/plugins · github.com/openclaw/openclaw/blob/main/CHANGELOG.md
