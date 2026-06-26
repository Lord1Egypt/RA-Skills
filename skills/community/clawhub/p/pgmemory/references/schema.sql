-- pgmemory reference schema (documentation copy — authoritative source is migrations/)
-- This file documents the full schema as of the latest migration.

-- memories: core table
-- agent           TEXT        — OpenClaw agent ID (namespace)
-- namespace       TEXT        — sub-namespace within agent (default: 'default')
-- category        TEXT        — decision|constraint|infrastructure|vision|preference|context|task
-- key             TEXT        — unique identifier within agent (agent+key is unique)
-- content         TEXT        — the memory text
-- embedding       vector(1024)— semantic embedding (dimension from config)
-- importance      INT 1-3     — 1=transient, 2=important, 3=critical
-- relevance_score FLOAT 0-1   — decays over time, boosted by access_count
-- access_count    INT         — increments each time memory is returned in search
-- source          TEXT        — session|harvest:{namespace}|import|manual
-- tags            TEXT[]      — optional free-form tags
-- expires_at      TIMESTAMPTZ — NULL = never expires
-- last_accessed   TIMESTAMPTZ — last time returned in a search result
-- decay_rate_override FLOAT   — per-memory decay rate (NULL = use category default)

-- archived_memories: same columns + archived_at + archive_reason
-- Memories are never hard deleted — they move here on expiry/eviction.

-- session_state: one row per agent
-- current_task, summary, active_jobs[], blocked_on[], metadata JSONB

-- pgmemory_migrations: tracks applied migrations
-- version INT PK, filename TEXT, checksum TEXT, applied_at TIMESTAMPTZ

-- archive_reason values: expired | evicted | decayed | manual
-- archived_ttl_days: null = keep forever (default)
-- restore_on_access: if semantic search matches archived memory, auto-restore with relevance_score=1.0

-- Archive triggers (all default true, configurable independently):
-- on_expire  — expires_at passed
-- on_evict   — max_memories cap exceeded, lowest relevance_score evicted
-- on_decay   — relevance_score dropped below archive_threshold (default 0.1)
-- on_manual  — explicit --archive call or admin action
