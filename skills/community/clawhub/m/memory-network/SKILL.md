---
name: memory-network
description: Social memory network — discover communities and build trust through shared emotional memory, not follower counts or algorithms. Powered by Echo's memory graph infrastructure.
metadata:
  version: 0.1.0
---

# Memory Network

Social memory network. Discover communities and build trust through shared emotional memory — not follower counts, not algorithms, not curated personas.

## How it works

Memory Network maps the social layer on top of individual memory graphs. When multiple people's memories resonate on the same experiences, emotions, or ideas, a network edge forms — creating organic communities grounded in genuine understanding.

### Core capabilities

- **Memory-based community discovery** — clusters of people whose memory graphs share deep structural similarity, surfaced automatically
- **Trust through transparency** — every connection is backed by visible memory evidence; no black-box recommendations
- **Cross-platform memory aggregation** — pull memories from ChatGPT, Gemini, Claude, and other AI conversations into a unified social graph
- **Real-time network evolution** — as new memories form, network connections strengthen, weaken, or emerge organically
- **Privacy-first sharing** — users choose which memory clusters are public, which are private, and which are matchable

## Architecture

Built on Echo's three-layer memory system:
1. **Identity layer** — compressed profile (~500 tokens), always available
2. **Working memory** — dynamic context per conversation (~5-10K tokens)
3. **Long-term storage** — Supabase + HNSW vector search (unlimited)

Network edges are computed across Layer 3, with social context injected through Layer 2.

## The vision

Every social platform today connects people through what they *show*. Memory Network connects people through what they *remember* — the experiences that shaped them, the ideas that moved them, the emotions they carry.

## Part of the Echo ecosystem

Memory Network is a component of [Echo Chat](https://iditor.com) by Iditor — building memory as social identity infrastructure.

## Status

Early development. Memory graph validated with 1,100+ memories, 23 clusters, emotion-aware matching active in beta (K-Factor 2, D7 retention 42%).
