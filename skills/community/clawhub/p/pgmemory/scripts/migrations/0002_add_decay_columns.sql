-- pgmemory migration 0002
-- Decay columns were included in 0001 (relevance_score, access_count, last_accessed)
-- This migration adds the decay_rate column for per-memory override

-- UP

ALTER TABLE memories
  ADD COLUMN decay_rate_override FLOAT DEFAULT NULL;

COMMENT ON COLUMN memories.decay_rate_override IS
  'Per-memory decay rate override. NULL means use category default from config.';

-- DOWN

ALTER TABLE memories DROP COLUMN IF EXISTS decay_rate_override;
