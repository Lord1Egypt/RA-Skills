-- ============================================
-- MIGRATION: TurboQuant Compression Support
-- 
-- Adds metadata columns for compressed embeddings
-- Run: sqlite3 muninn.db < migrations/001_turboquant.sql
-- ============================================

-- Add compression metadata to episodes
ALTER TABLE episodes ADD COLUMN embedding_compressed INTEGER DEFAULT 0;
ALTER TABLE episodes ADD COLUMN embedding_bits INTEGER DEFAULT 16;
ALTER TABLE episodes ADD COLUMN embedding_dimension INTEGER DEFAULT 768;

-- Add compression metadata to entities
ALTER TABLE entities ADD COLUMN embedding_compressed INTEGER DEFAULT 0;
ALTER TABLE entities ADD COLUMN embedding_bits INTEGER DEFAULT 16;
ALTER TABLE entities ADD COLUMN embedding_dimension INTEGER DEFAULT 768;

-- Add compression metadata to prototypes (if exists)
-- ALTER TABLE prototypes ADD COLUMN embedding_compressed INTEGER DEFAULT 0;
-- ALTER TABLE prototypes ADD COLUMN embedding_bits INTEGER DEFAULT 16;
-- ALTER TABLE prototypes ADD COLUMN embedding_dimension INTEGER DEFAULT 768;

-- Create index for compressed embeddings
CREATE INDEX IF NOT EXISTS idx_episodes_embedding_compressed ON episodes(embedding_compressed);
CREATE INDEX IF NOT EXISTS idx_entities_embedding_compressed ON entities(embedding_compressed);

-- ============================================
-- STORAGE FORMAT (embedding BLOB)
-- 
-- Compressed format:
-- - 4 bytes: dimension (uint32 LE)
-- - 1 byte: bits (uint8)
-- - 8 bytes: residual_norm (float64 LE)
-- - 8 bytes: original_norm (float64 LE)
-- - N bytes: mse_indices (ceil(dimension * bits / 8))
-- - M bytes: qjl_signs (ceil(dimension / 8))
-- 
-- Uncompressed format (FP16):
-- - dimension * 2 bytes: float16 array
-- 
-- ============================================

-- ============================================
-- MIGRATION NOTES
-- 
-- 1. Existing embeddings are stored as FP16 (uncompressed)
-- 2. New embeddings will be compressed by default (3-bit)
-- 3. To recompress existing embeddings:
--    - Read embedding BLOB
--    - If embedding_compressed = 0, decompress from FP16
--    - Compress with TurboQuant
--    - Update BLOB and set embedding_compressed = 1
-- 
-- ============================================