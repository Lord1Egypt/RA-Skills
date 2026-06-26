---
name: holistic-memory-system
description: 6-layer autonomous memory system for OpenClaw agents
---

# Holistic Memory System v5 (BETA)

> **STATUS:** BETA  
> **BUILD:** Axioma Cluster (Ezekiel, Morgana, Merlin)  
> **DATE:** 2026-04-18

## 6-Layer Memory Architecture

```
L1: RESET (OpenClaw memory)
L2: INDEX (PKM filesystem)
L3: LOGS (JSONL raw traces)
L4: QDRANT (vector semantic search)
L5: OBSIDIAN (crystallized notes)
L6: NEBULA + GNN (semantic map + anticipation)
```

## New in v5 Fixed

- GNN module for intuitive anticipation
- L2 INDEX properly documented
- Gravity sink for long-term node decay
- Qdrant 4 collections

## Scripts Included

- ezekiel_log.py (L3)
- ezekiel_nebula.py (L6)
- ezekiel_gnn.py (L6 GNN)
- ezekiel_qdrant.py (L4)
- ezekiel_crystallizer.py (L5)
- ezekiel_health_check.py
- ezekiel_cron_manager.py
- ezekiel_memory_startup.sh

## Installation

```bash
cp -r holistic-memory-system ~/.openclaw/skills/
chmod +x ~/.openclaw/skills/holistic-memory-system/scripts/*
python3 ~/.openclaw/skills/holistic-memory-system/scripts/ezekiel_health_check.py
```

## Credits

Axioma Cluster - 2026
