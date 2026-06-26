# Installation Memoria

## Option A : Installation automatique (recommandé)

```bash
curl -fsSL https://raw.githubusercontent.com/Primo-Studio/openclaw-memoria/main/install.sh | bash
```

Le script :
1. Vérifie les prérequis (Node.js, npm, Ollama)
2. Pull les modèles Ollama (gemma3:4b + nomic-embed-text-v2-moe)
3. Clone le repo et installe les dépendances
4. **Auto-configure `openclaw.json`** (ajoute memoria aux plugins avec backup)
5. Détecte les données existantes (cortex.db, memoria.db, facts.json)

Le client garde le contrôle total : toute config peut être modifiée après dans `openclaw.json`.

## Option B : Installation manuelle

### Prérequis

- **OpenClaw** installé et fonctionnel
- **Node.js** ≥ 20 avec `npm` dans le PATH
- **Ollama** installé ([ollama.ai](https://ollama.ai))

### 1. Installer les modèles Ollama

```bash
ollama pull gemma3:4b              # LLM extraction (3.3 GB)
ollama pull nomic-embed-text-v2-moe  # Embeddings (957 MB)
```

Vérifier : `ollama list` doit afficher les deux modèles.

### 2. Installer le plugin

```bash
git clone https://github.com/Primo-Studio/openclaw-memoria.git \
  ~/.openclaw/extensions/memoria

cd ~/.openclaw/extensions/memoria
npm install
```

### 3. Configurer openclaw.json

**Config minimale** — tout le reste a des defaults intelligents :

```json
{
  "plugins": {
    "allow": ["memoria"],
    "entries": {
      "memoria": { "enabled": true }
    }
  }
}
```

**Config complète** (si vous voulez personnaliser) :

```json
{
  "memoria": {
    "enabled": true,
    "config": {
      "autoRecall": true,
      "autoCapture": true,
      "recallLimit": 12,
      "captureMaxFacts": 8,
      "defaultAgent": "koda",
      "contextWindow": 200000,
      "syncMd": true,
      "llm": {
        "provider": "ollama",
        "model": "gemma3:4b"
      },
      "embed": {
        "provider": "ollama",
        "model": "nomic-embed-text-v2-moe",
        "dimensions": 768
      }
    }
  }
}
```

### 4. Vérifier et démarrer

```bash
openclaw doctor          # Vérifier la config
openclaw gateway restart # Redémarrer
openclaw status          # Vérifier le chargement
```

Vous devez voir :
```
[plugins] memoria: v3.22.3 registered (X facts, Y observations, ... continuous: every 4 turns)
```

### 5. Migration automatique

**Depuis cortex.db** : Memoria détecte automatiquement un ancien `cortex.db` et migre les données en `memoria.db` au premier démarrage. Zéro action nécessaire. Utilise `VACUUM INTO` pour gérer les DB en mode WAL.

**Depuis facts.json** (memory-convex) :

```bash
cd ~/.openclaw/extensions/memoria
npx tsx migrate.ts
```

---

## Bugs connus à l'installation

### ❌ `syncMd` doit être un boolean

**Erreur** : `plugins.entries.memoria.config.syncMd: must be boolean`
**Cause** : écrire `"syncMd": { "enabled": true }` au lieu de `"syncMd": true`
**Fix** : `"syncMd": true`

### ❌ `embed.dims` n'existe pas

**Erreur** : `must NOT have additional properties`
**Cause** : le champ s'appelle `dimensions`, pas `dims`
**Fix** : `"dimensions": 768`

### ❌ `llm.default` n'existe pas

**Erreur** : `must NOT have additional properties`
**Cause** : les champs `provider` et `model` sont directement dans `llm`, pas dans `llm.default`
**Fix** :
```json
"llm": {
  "provider": "ollama",
  "model": "gemma3:4b"
}
```

### ❌ `fallback[].type` n'existe pas

**Erreur** : propriété inconnue
**Cause** : le champ s'appelle `provider`, pas `type`
**Fix** : `{ "provider": "ollama", "model": "gemma3:4b" }`

### ❌ DB path = workspace root, pas le fichier

Le constructeur `MemoriaDB()` attend le **workspace root** (ex: `~/.openclaw/workspace`).
Il crée automatiquement `memory/memoria.db` dedans.
Ne pas passer le chemin de la DB directement.

### ⚠️ Ollama modèles = 0 malgré process running

**Symptôme** : `ollama list` retourne vide, mais le process tourne
**Cause** : Ollama app lancée mais aucun modèle pull
**Fix** : `ollama pull gemma3:4b && ollama pull nomic-embed-text-v2-moe`

### ⚠️ `npm` / `node` not found via SSH

**Cause** : SSH ne charge pas le PATH complet (brew, nvm, etc.)
**Fix** : `export PATH=/opt/homebrew/bin:$PATH` avant les commandes

### ⚠️ "loaded without install/load-path provenance"

**Cause** : plugin local, pas installé via `openclaw plugin install`
**Impact** : warning non-bloquant, le plugin fonctionne
**Fix** : ajouter dans `plugins.allow` (déjà fait si vous suivez le guide)

---

## Config minimale (copier-coller)

Pour une installation rapide avec Ollama local :

```json
{
  "plugins": {
    "allow": ["memoria"],
    "entries": {
      "memoria": {
        "enabled": true,
        "config": {
          "autoRecall": true,
          "autoCapture": true,
          "syncMd": true,
          "llm": { "provider": "ollama", "model": "gemma3:4b" },
          "embed": { "provider": "ollama", "model": "nomic-embed-text-v2-moe", "dimensions": 768 }
        }
      }
    }
  }
}
```

---

## Providers supportés

| Provider | LLM | Embeddings | Prérequis |
|----------|-----|------------|-----------|
| `ollama` | ✅ | ✅ | Ollama installé, modèles pull |
| `lmstudio` | ✅ | ✅ | LM Studio avec serveur local |
| `openai` | ✅ | ✅ | Clé API OpenAI |
| `openrouter` | ✅ | ❌ | Clé API OpenRouter |
| `anthropic` | ✅ | ❌ | Clé API Anthropic (Claude) |

### Anthropic (Claude API)

Config avec Claude comme LLM d'extraction :
```json
"llm": {
  "provider": "anthropic",
  "model": "claude-haiku-3-5",
  "apiKey": "sk-ant-..."
}
```

Ou en fallback :
```json
"fallback": [
  { "provider": "ollama", "model": "gemma3:4b" },
  { "provider": "anthropic", "model": "claude-haiku-3-5", "apiKey": "sk-ant-..." }
]
```

Note : Anthropic ne supporte pas les embeddings. Utilisez Ollama ou OpenAI pour les embeddings.
