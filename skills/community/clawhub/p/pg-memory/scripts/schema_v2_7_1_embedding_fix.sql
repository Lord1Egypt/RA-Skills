-- pg-memory v2.7.1: Update embedding dimension from 1536 to 1024 (BGE-M3 via Ollama)
-- Run this on existing databases to update the embedding column

-- Step 1: Drop the old embedding column (data will be lost, but that's acceptable for embeddings)
ALTER TABLE observations DROP COLUMN IF EXISTS embedding;

-- Step 2: Add new embedding column with correct dimension (1024 for BGE-M3 via Ollama)
ALTER TABLE observations ADD COLUMN embedding vector(1024);

-- Step 3: Recreate the index for semantic search
DROP INDEX IF EXISTS idx_observations_embedding;
CREATE INDEX idx_observations_embedding 
    ON observations USING ivfflat(embedding vector_cosine_ops) 
    WHERE embedding IS NOT NULL;

-- Step 4: Update version tracking (if table exists)
DO $$
BEGIN
    IF EXISTS (SELECT FROM pg_tables WHERE tablename = 'schema_migrations') THEN
        INSERT INTO schema_migrations (version, applied_at) 
        VALUES ('2.7.1', NOW())
        ON CONFLICT (version) DO UPDATE SET applied_at = NOW();
    END IF;
END
$$;

-- Note: Existing embeddings (1536-dim or 384-dim) are incompatible with new column.
-- They will be regenerated on next observation capture or can be batch-regenerated
-- using the regenerate_embeddings.py script.
