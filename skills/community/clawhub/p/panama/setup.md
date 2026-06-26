# Setup — Panama Travel Guide

## First-Time Setup

When user mentions Panama travel for the first time:

### 1. Create Memory Structure
```bash
mkdir -p ~/panama
```

### 2. Initialize Memory File
Create `~/panama/memory.md` using `memory-template.md`.

### 3. Gather Trip Context Naturally
Ask in conversational flow:
- Entry status: visa-free, visa pending, or nationality rules still unclear?
- Travel window: exact dates, month range, or open season?
- Trip shape: city break, islands, highlands, surf, diving, wildlife, or mixed?
- Transfer tolerance: happy with boats and domestic flights, or wants low-friction over variety?
- Constraints: budget, mobility, kids, remote work, driving comfort, seasickness, heat tolerance.
- Pace: one base, two bases, or a more active route.

### 4. Save to Memory
Update `~/panama/memory.md` with current goals, constraints, open decisions, and transport tolerance.

## Returning Users

If `~/panama/memory.md` exists:
1. Read it silently
2. Reuse known preferences and friction points
3. Ask only what changed
4. Update memory with deltas

## Quick Start Responses

**"I want a beach trip in Panama"**
-> Ask: surf or calm water, boat tolerance, nightlife vs quiet, and travel month.
-> Then use: `regions.md`, `bocas-del-toro.md`, `guna-yala-and-san-blas.md`, `azuero-and-pacific-coast.md`.

**"I have one week in Panama"**
-> Ask: one base or two, city plus nature vs islands, and whether flights are acceptable.
-> Then use: `itineraries.md`, `regions.md`, `transport-domestic.md`.

**"I want coffee, hiking, and cooler weather"**
-> Ask: hiking level, rain tolerance, and whether sunrise/early starts are fine.
-> Then use: `boquete-and-chiriqui-highlands.md`, `weather-and-seasonality.md`, `road-trips-and-driving.md`.

## Important Notes

- The key quality lever is transfer friction, not raw distance.
- Boat logistics and weather windows can break island-heavy itineraries.
- Panama is easy to overstuff because maps look small and flights are short.
- Keep at least one fallback for rain, rough seas, or delayed transfers.
