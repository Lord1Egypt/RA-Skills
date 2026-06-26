---
name: level-design-checklist-skill
title: Level Design Checklist Skill
description: Guides structured help for level design reviews using clear templates, checks, and safe defaults.
version: 0.1.0
author: Abdullah
license: MIT-0
tags:
  - game
  - level-design-checklist
  - openclaw
  - templates
---

# Level Design Checklist Skill

## Purpose
Help a game creator review and improve a level design before building, testing, or publishing it.

Use this skill for platformer levels, top-down levels, puzzle rooms, combat arenas, tutorial stages, and small indie game maps.

## Inputs
Ask for or collect:
- Game genre
- Level goal
- Player abilities available in this level
- Main mechanic or teaching point
- Level map, sketch, blockout, or short description
- Target difficulty
- Known problems or player feedback

## Checklist

### 1. Player Goal
- The objective is clear within the first few seconds.
- The player can understand where to go next.
- The level has a start, middle, and finish.

### 2. Readability
- Important paths are visually stronger than decoration.
- Hazards, enemies, pickups, exits, and interactable objects are easy to recognize.
- The camera or viewpoint supports the main action.

### 3. Flow
- The level introduces one idea at a time.
- Safe practice comes before dangerous use.
- Challenge increases gradually.
- There are no long empty sections unless they serve pacing.

### 4. Fair Challenge
- Failures feel understandable, not random.
- Checkpoints or recovery points match the difficulty.
- Enemy and hazard placement gives the player time to react.
- Optional hard routes are clearly optional.

### 5. Mechanics
- The level teaches or tests the intended mechanic.
- Required abilities are available before they are needed.
- There are no softlocks or required jumps/actions that exceed intended player skill.

### 6. Rewards and Secrets
- Rewards guide exploration without confusing the main route.
- Secrets have visual hints or logic.
- Risk and reward feel balanced.

### 7. Performance and Scope
- The level is not overloaded with unnecessary objects.
- Reused assets are consistent.
- The level can be playtested quickly.

### 8. Playtest Notes
Record:
- Where players got confused
- Where players died unfairly
- Where players ignored the intended route
- What felt fun
- What should be cut or simplified

## Output Template

```text
Level Review: [level name]

Goal:
- [clear objective]

Strong points:
- [what works]

Problems found:
- [issue 1]
- [issue 2]

Fix plan:
1. [small fix]
2. [small fix]
3. [test again]

Playtest focus:
- Watch if players understand [specific moment]
```

## Safety and Scope
- Do not recommend copyrighted level copying.
- Do not overbuild the level before testing.
- Prefer small playable improvements over large redesigns.
