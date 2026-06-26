"""Tests for VectorStore (LanceDB + embeddings)."""
import pytest
import asyncio
import numpy as np
from pathlib import Path
from ghostclaw.core.vector_store import VectorStore

# Check if dependencies are available
try:
    import lancedb  # noqa: F401
    import fastembed  # noqa: F401
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False


pytestmark = pytest.mark.skipif(not HAS_DEPS, reason="lancedb or sentence-transformers not installed")


@pytest.fixture(autouse=True)
def mock_embedding_provider(mocker):
    """Mock EmbeddingProvider to avoid downloading models in tests."""
    from ghostclaw.core.vector_store.embedding import EmbeddingProvider
    
    # Mock initialize to do nothing
    mocker.patch.object(EmbeddingProvider, "initialize", return_value=None)
    
    # Mock embed_batch to return dummy vectors
    async def dummy_embed_batch(self, texts):
        import hashlib
        results = []
        for text in texts:
            # Word-based hashing for basic similarity
            words = text.lower().replace(",", " ").replace(".", " ").split()
            vec = np.zeros(384, dtype=np.float32)
            for word in set(words):
                if len(word) < 3: continue
                h = hashlib.sha256(word.encode()).digest()
                seed = int.from_bytes(h, "big") % 384
                vec[seed] += 1.0
            
            # Add some unique flavor based on whole text to avoid exact same vector for different order
            h_full = hashlib.sha256(text.encode()).digest()
            seed_full = int.from_bytes(h_full, "big") % 384
            vec[seed_full] += 0.1
            
            norm = np.linalg.norm(vec)
            if norm > 1e-6:
                vec = vec / norm
            else:
                # Fallback for very short text
                vec = np.ones(384, dtype=np.float32) / np.sqrt(384)
            results.append(vec)
        return results
        
    mocker.patch.object(EmbeddingProvider, "embed_batch", dummy_embed_batch)


@pytest.mark.asyncio
async def test_vector_store_init_and_ensure_table(tmp_path):
    """Test VectorStore can initialize LanceDB and create table."""
    db_path = tmp_path / "lancedb"
    store = VectorStore(db_path=db_path)
    assert not db_path.exists()
    await store.ensure_table()
    assert db_path.exists()
    # Table should exist
    assert store._table is not None
    await store.close()


@pytest.mark.asyncio
async def test_vector_store_embed_text(tmp_path):
    """Test single text embedding generation."""
    store = VectorStore(db_path=tmp_path / "lancedb")
    await store.initialize()
    text = "Hello world, this is a test."
    embedding = await store.embed_text(text)
    assert isinstance(embedding, np.ndarray)
    assert embedding.shape == (384,)  # all-MiniLM-L6-v2 dimension
    # Same text should produce same embedding (deterministic)
    embedding2 = await store.embed_text(text)
    np.testing.assert_array_equal(embedding, embedding2)
    await store.close()


@pytest.mark.asyncio
async def test_vector_store_embed_batch(tmp_path):
    """Test batch embedding generation."""
    store = VectorStore(db_path=tmp_path / "lancedb")
    await store.initialize()
    texts = ["First text", "Second text", "Third text"]
    embeddings = await store.embed_batch(texts)
    assert len(embeddings) == 3
    for emb in embeddings:
        assert isinstance(emb, np.ndarray)
        assert emb.shape == (384,)
    await store.close()


@pytest.mark.asyncio
async def test_vector_store_add_and_search(tmp_path):
    """Test adding chunks and performing similarity search."""
    store = VectorStore(db_path=tmp_path / "lancedb")
    await store.ensure_table()

    # Add some chunks
    report_id = 1
    chunks = [
        {"chunk_id": "issue-0", "text": "Authentication bypass vulnerability in login"},
        {"chunk_id": "issue-1", "text": "Memory leak in event loop causing high usage"},
        {"chunk_id": "ghost-0", "text": "CallbackHell pattern detected in async code"},
    ]
    base_metadata = {
        "repo_path": "/path/to/repo",
        "timestamp": "2026-03-14T10:00:00Z",
        "vibe_score": 75,
        "stack": "python",
    }
    await store.add_chunks(report_id, chunks, base_metadata)

    # Search for "authentication"
    results = await store.search("authentication", limit=5)
    assert len(results) >= 1
    # The top result should be the authentication chunk
    assert "authentication" in results[0]["text"].lower()
    assert results[0]["report_id"] == report_id
    assert "score" in results[0]
    assert 0 <= results[0]["score"] <= 1  # cosine similarity

    # Search for "memory leak"
    results = await store.search("memory leak", limit=5)
    assert len(results) >= 1
    assert "memory" in results[0]["text"].lower()

    # Search with repo_path filter should still work
    results = await store.search("callback", repo_path="/path/to/repo")
    assert any(r["repo_path"] == "/path/to/repo" for r in results)

    await store.close()


@pytest.mark.asyncio
async def test_vector_store_delete_and_clear(tmp_path):
    """Test clearing the embeddings table."""
    store = VectorStore(db_path=tmp_path / "lancedb")
    await store.ensure_table()

    # Add a chunk
    await store.add_chunks(1, [{"chunk_id": "t1", "text": "test"}], {})

    # Clear
    await store.clear()
    # After clear, table should be None (or empty)
    # Re-initialization would create new empty table; for now just verify we can re-ensure and it works
    await store.ensure_table()
    assert store._table is not None
    # Search should return empty
    results = await store.search("test")
    assert len(results) == 0
    await store.close()
