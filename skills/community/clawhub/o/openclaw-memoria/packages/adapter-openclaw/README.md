# @memoria/adapter-openclaw

Plugin **OpenClaw** mince (zéro dépendance native) qui donne à OpenClaw la
mémoire **automatique** de Memoria. Il ne contient aucune logique mémoire : il
traduit deux hooks OpenClaw en appels HTTP au daemon Memoria local.

| Hook OpenClaw | Route daemon | Effet |
|---|---|---|
| `before_prompt_build` | `POST /v1/memory/recall` | **auto-recall** : injecte les souvenirs pertinents AVANT chaque tour (`prependContext`) |
| `agent_end` | `POST /v1/memory/capture_turn` | **auto-capture** : mémorise la conversation en fin de tour (fire-and-forget) |

Le MCP natif d'OpenClaw (`openclaw mcp set memoria …`) ne donne que le « pull »
(l'agent doit appeler les tools lui-même). Ces hooks ajoutent la boucle
**automatique** — la vraie proposition de valeur de Memoria.

## ⚠️ Le piège qui a tué la capture en v3.34

Depuis OpenClaw **2026.5/2026.6**, `agent_end` (et `llm_output`) sont des
*conversation hooks* **bloqués par défaut** pour les plugins non bundlés. Sans
le flag ci-dessous, **l'auto-capture est désactivée silencieusement** (warn dans
les logs, aucune erreur visible) — c'est la cause probable de la régression de
capture de Memoria v3.34. Voir `docs/v3/DIAG-OPENCLAW-2026.6.5.md`.

```jsonc
// ~/.openclaw/openclaw.json
{
  "plugins": {
    "allow": ["memoria"],
    "entries": {
      "memoria": {
        "enabled": true,
        "hooks": { "allowConversationAccess": true },  // ← SANS ça, capture morte
        "config": { "token": "<token d'instance>", "instance": "koda" }
      }
    }
  }
}
```

## Installation (automatique)

`memoria connect --code XXXX-XXXX` sur un hôte OpenClaw fait **tout** :
1. enregistre le serveur MCP (`openclaw mcp set memoria …`) ;
2. lie ce plugin dans `~/.openclaw/extensions/memoria` ;
3. écrit `~/.openclaw/openclaw.json` avec `allowConversationAccess=true` + le
   token d'instance.

Puis : `openclaw plugins enable memoria` (si nécessaire) et redémarre OpenClaw.
Vérifier : `openclaw plugins inspect memoria` (doit montrer
`allowConversationAccess: true`) et grepper les logs pour
« blocked because non-bundled plugins must set… » (ne doit PAS apparaître).

Désinstallation : `memoria disconnect` (retire le MCP, le plugin et l'entrée de
config, laisse le reste intact).

## Configuration (`plugins.entries.memoria.config`)

| Clé | Défaut | Rôle |
|---|---|---|
| `token` | — | **Requis.** Token d'instance (pairing). Lit/écrit `/v1/memory/*`. |
| `instance` | `koda` | Étiquette (l'instance réelle est dérivée du token). |
| `daemonUrl` | auto | Vide = découverte du port via `<storageRoot>/daemon.json`. |
| `storageRoot` | `~/.memoria/data` | Pour la découverte du port. |
| `autoRecall` | `true` | Injecter la mémoire avant chaque tour. |
| `autoCapture` | `true` | Mémoriser en fin de tour. |
| `recallLimit` | `12` | Nombre max de souvenirs injectés (1–20). |
| `recallTimeoutMs` | `400` | Timeout DUR du recall (la mémoire ne retarde jamais un tour). |

## Robustesse

Tout échec (daemon arrêté, timeout, Memoria en pause) est **avalé proprement** :
un agent ne casse jamais parce que sa mémoire est indisponible. Le daemon
journalise la capture (WAL) **avant** l'extraction → même un timeout ne perd
aucune donnée (rejeu au prochain boot).
