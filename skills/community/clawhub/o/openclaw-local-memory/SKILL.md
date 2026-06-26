---
name: Local Memory
description: Brain-like local memory plugin for OpenClaw — stores, searches, and injects memories with importance scoring, entity extraction, and automatic consolidation.
---

# 🧠 Local Memory Plugin v0.4

**A brain-like memory system for OpenClaw. Remembers what matters, forgets what doesn't, and builds a persistent understanding of you over time.**

> Zero-config, no external service, no API key, works out of the box.

## Features

### 🧠 Brain-Like Memory Architecture
- **Hierarchical Memory**: Exchanges → Summaries → Profile
- **Importance Scoring**: Each memory scored 0-1 based on significance
- **Time Decay**: Importance decreases over time (adjustable rate)
- **Entity Tracking**: Extracts and tracks people, places, things
- **Semantic Chunking**: Long content auto-split into manageable pieces

### 🔍 Smart Recall
- **Multi-Factor Scoring**: Combines relevance, importance, AND recency
- **Profile Injection**: Builds and injects user profile periodically
- **Context Window**: Tracks conversation turns and manages memory refresh

### 💾 Intelligent Capture
- **Significance Detection**: Only captures meaningful content
- **Auto-Deduplication**: Won't store the same thing twice
- **Periodic Consolidation**: Summarizes accumulated content when context grows long
- **Category Detection**: Auto-categorizes as preference, fact, decision, entity, skill

### 🗑️ Self-Maintaining
- **Auto-Pruning**: Removes old/unimportant memories when limit reached
- **Importance Protection**: High-value memories kept longer
- **Memory Stats**: Track memory health and composition

## Tools

| Tool | Description |
|------|-------------|
| `local_memory_search` | Search memories by natural language (semantic) |
| `local_memory_store` | Manually save a specific memory |
| `local_memory_list` | List all memories, optionally filtered by category |
| `local_memory_profile` | View user profile (entities, preferences, facts) |
| `local_memory_stats` | View memory statistics |
| `local_memory_recent` | Get recently accessed memories |
| `local_memory_forget` | Delete memory matching a query |
| `local_memory_wipe` | Delete ALL memories (irreversible) |

## How It Works

### Memory Lifecycle

1. **Capture** → User + Assistant exchange
2. **Significance Assessment** → Score based on patterns (decisions score high, greetings low)
3. **Storage** → If significant enough, store with extracted entities and tags
4. **Importance Calculation** → Based on category, length, entities, source
5. **Decay Over Time** → Importance decreases exponentially
6. **Recall** → On query, combine TF-IDF relevance + importance + recency
7. **Pruning** → When max reached, lowest combined-score memories removed

### Recall Scoring Formula

```
score = (relevanceWeight × tfidf_similarity) 
      + (importanceWeight × decayed_importance)
      + (recencyWeight × recency_factor)
```

### Significance Detection Patterns

| Pattern | Category | Weight |
|---------|----------|--------|
| entschieden, geplant, wird, werden | decision | 0.30 |
| ich bin, mein, unser Unternehmen | identity | 0.25 |
| bevorzug, immer, nie, prefer | preference | 0.25 |
| api_key, password, token | credential | 0.20 |
| skill, können, fähig | skill | 0.20 |
| projekt, build, deploy | project | 0.15 |

## Configuration

```json
{
  "autoRecall": true,
  "autoCapture": true,
  "captureInterval": 8,
  "captureSignificantOnly": true,
  "minSignificanceScore": 0.5,
  "profileFrequency": 15,
  "includeProfileOnFirstTurn": true,
  "maxRecallResults": 5,
  "similarityThreshold": 0.35,
  "maxMemoryInjections": 3,
  "contextBudget": 2000,
  "maxMemories": 500,
  "pruneOlderThanDays": 30,
  "decayRate": 0.05,
  "chunkSize": 800,
  "importanceWeight": 0.25,
  "recencyWeight": 0.25,
  "relevanceWeight": 0.5
}
```

| Option | Default | Description |
|--------|---------|-------------|
| `autoRecall` | `true` | Inject relevant memories before each turn |
| `autoCapture` | `true` | Auto-capture conversation exchanges |
| `captureInterval` | `8` | Capture every N turns (higher = less storage) |
| `captureSignificantOnly` | `true` | Only capture significant content |
| `minSignificanceScore` | `0.5` | Min score to capture (higher = stricter) |
| `profileFrequency` | `15` | Inject profile every N turns (higher = less context) |
| `maxRecallResults` | `5` | Max memories injected per turn |
| `similarityThreshold` | `0.35` | Min relevance to inject |
| `maxMemoryInjections` | `3` | **Max memories to show per recall** |
| `contextBudget` | `2000` | **Max chars of memory context injected** |
| `maxMemories` | `500` | Maximum memories to keep |
| `pruneOlderThanDays` | `30` | Auto-delete memories older than N days |
| `decayRate` | `0.05` | Importance decay speed |
| `importanceWeight` | `0.25` | Weight of importance in scoring |
| `recencyWeight` | `0.25` | Weight of recency in scoring |
| `relevanceWeight` | `0.5` | Weight of TF-IDF relevance in scoring |

## Data Storage

All memories stored locally in:
```
~/.openclaw/memory/<containerTag>.json
```

Default: `~/.openclaw/memory/openclaw_local_memory.json`

## Privacy

- **100% Local**: No data leaves your machine
- **You Control**: Auto-capture can be disabled
- **Significance Filter**: Won't store every random message
- **No External APIs**: No internet required

## Requirements

- OpenClaw 2026.1.29 or later
- Node.js (built-in TF-IDF, no external dependencies)

## Tips

### For Best Results
1. Let it run for a few days — memory improves over time
2. Manually store important facts with `local_memory_store` 
3. Check profile with `local_memory_profile` periodically
4. Adjust `importanceWeight`, `recencyWeight`, `relevanceWeight` to your preference

### If Context Gets Long
- Reduce `summariseThreshold` to trigger earlier consolidation
- Increase `decayRate` to forget older stuff faster
- Lower `maxMemories` to prune more aggressively

### Forgot Something?
- Use `local_memory_forget query="what to forget"` to delete
- Use `local_memory_search` to find what you're looking for
