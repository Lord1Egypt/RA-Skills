#!/usr/bin/env python3
"""
Regenerate embeddings for existing observations using BGE-M3 (384-dim)

This script fetches all observations without embeddings (or with old 1536-dim embeddings)
and regenerates them using Ollama's BGE-M3 model.

Usage:
    python3 scripts/regenerate_embeddings.py [--batch-size 50] [--limit 100]

Options:
    --batch-size  Number of embeddings to generate per batch (default: 50)
    --limit       Maximum observations to process (default: all)
    --dry-run     Show what would be done without making changes
"""

import sys
import json
import argparse
import urllib.request
import urllib.error
from datetime import datetime
from typing import List, Dict, Any, Optional

# Add scripts directory to path
sys.path.insert(0, __file__.rsplit('/', 1)[0])

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor, execute_values
except ImportError:
    print("❌ psycopg2 not installed. Run: pip3 install psycopg2-binary")
    sys.exit(1)


class BGEEmbedding:
    """Generate embeddings using Ollama's BGE-M3 model"""
    
    def __init__(self, model: str = "bge-m3:latest", host: str = "http://localhost:11434"):
        self.model = model
        self.host = host
        self.session = None
    
    def generate(self, text: str) -> Optional[List[float]]:
        """Generate embedding for a single text"""
        if not text or len(text.strip()) == 0:
            return None
        
        url = f"{self.host}/api/embeddings"
        payload = {
            "model": self.model,
            "prompt": text
        }
        
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                embedding = result.get('embedding')
                if embedding and len(embedding) == 1024:
                    return embedding
                else:
                    print(f"  ⚠️  Invalid embedding dimension: {len(embedding) if embedding else 'None'}")
                    return None
        except Exception as e:
            print(f"  ❌ Error generating embedding: {e}")
            return None
    
    def generate_batch(self, texts: List[str]) -> List[Optional[List[float]]]:
        """Generate embeddings for multiple texts"""
        embeddings = []
        for i, text in enumerate(texts):
            print(f"  Processing {i+1}/{len(texts)}...", end='\r')
            embeddings.append(self.generate(text))
        print(f"  ✓ Completed {len(texts)} embeddings")
        return embeddings


def get_db_connection():
    """Connect to PostgreSQL database"""
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='openclaw_memory',
            user='skipppotter'
        )
        print("✅ Connected to PostgreSQL")
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        sys.exit(1)


def get_observations_needing_embeddings(conn, limit: Optional[int] = None) -> List[Dict]:
    """Fetch observations that need embeddings regenerated"""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # Get observations with NULL embedding or wrong dimension
    query = """
        SELECT id, content, title, tags
        FROM observations
        WHERE embedding IS NULL OR vector_dims(embedding) != 1024
        ORDER BY updated_at DESC
    """
    
    if limit:
        query += f" LIMIT {limit}"
    
    cur.execute(query)
    observations = cur.fetchall()
    cur.close()
    
    print(f"📊 Found {len(observations)} observations needing embeddings")
    return observations


def update_embeddings(conn, observations: List[Dict], embeddings: List[Optional[List[float]]]) -> int:
    """Update observations with new embeddings"""
    if not observations or not embeddings:
        return 0
    
    cur = conn.cursor()
    updated = 0
    
    for obs, embedding in zip(observations, embeddings):
        if embedding:
            try:
                # Use psycopg2's adapt for vector type
                from psycopg2.extras import Json
                cur.execute("""
                    UPDATE observations 
                    SET embedding = %s::vector,
                        updated_at = NOW()
                    WHERE id = %s
                """, (Json(embedding), obs['id']))
                updated += 1
            except Exception as e:
                print(f"  ❌ Failed to update {obs['id'][:8]}...: {e}")
    
    conn.commit()
    cur.close()
    
    return updated


def main():
    parser = argparse.ArgumentParser(description='Regenerate embeddings for pg-memory observations')
    parser.add_argument('--batch-size', type=int, default=50, help='Batch size for processing')
    parser.add_argument('--limit', type=int, default=None, help='Max observations to process')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done')
    args = parser.parse_args()
    
    print("=" * 60)
    print("🔄 pg-memory Embedding Regenerator (BGE-M3 384-dim)")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Batch size: {args.batch_size}")
    print(f"Limit: {args.limit or 'all'}")
    print(f"Dry run: {args.dry_run}")
    print()
    
    # Test Ollama connection
    print("🔌 Testing Ollama connection...")
    embedder = BGEEmbedding()
    test_result = embedder.generate("test")
    if not test_result or len(test_result) != 1024:
        print(f"❌ Ollama BGE-M3 not working. Expected 1024-dim, got {len(test_result) if test_result else 'None'}")
        print("   Make sure Ollama is running: ollama serve")
        print("   And BGE-M3 is pulled: ollama pull bge-m3")
        sys.exit(1)
    print("✅ Ollama BGE-M3 ready (1024-dim)")
    print()
    
    # Connect to database
    conn = get_db_connection()
    
    # Get observations needing embeddings
    observations = get_observations_needing_embeddings(conn, args.limit)
    
    if not observations:
        print("✅ All observations already have valid 384-dim embeddings!")
        conn.close()
        return
    
    print()
    
    if args.dry_run:
        print(f"📋 DRY RUN: Would regenerate {len(observations)} embeddings")
        for obs in observations[:5]:
            content = obs['content'][:60] if obs['content'] else 'N/A'
            print(f"   - {content}...")
        if len(observations) > 5:
            print(f"   ... and {len(observations) - 5} more")
        conn.close()
        return
    
    # Process in batches
    total = len(observations)
    processed = 0
    updated = 0
    
    print(f"🔄 Processing {total} observations in batches of {args.batch_size}...")
    print()
    
    for i in range(0, total, args.batch_size):
        batch = observations[i:i + args.batch_size]
        batch_num = (i // args.batch_size) + 1
        total_batches = (total + args.batch_size - 1) // args.batch_size
        
        print(f"Batch {batch_num}/{total_batches}")
        
        # Prepare texts for embedding
        texts = []
        for obs in batch:
            # Combine title and content for better embedding
            text_parts = []
            if obs.get('title'):
                text_parts.append(obs['title'])
            if obs.get('content'):
                text_parts.append(obs['content'])
            if obs.get('tags'):
                text_parts.append('Tags: ' + ', '.join(obs['tags']))
            texts.append(' | '.join(text_parts))
        
        # Generate embeddings
        embeddings = embedder.generate_batch(texts)
        
        # Update database
        batch_updated = update_embeddings(conn, batch, embeddings)
        processed += len(batch)
        updated += batch_updated
        
        print(f"✓ Batch complete: {batch_updated}/{len(batch)} updated")
        print(f"Progress: {processed}/{total} ({100*processed/total:.1f}%)")
        print()
    
    # Summary
    print("=" * 60)
    print("✅ Regeneration Complete!")
    print("=" * 60)
    print(f"Total observations: {total}")
    print(f"Processed: {processed}")
    print(f"Successfully updated: {updated}")
    print(f"Failed: {processed - updated}")
    print(f"Success rate: {100*updated/processed:.1f}%" if processed > 0 else "N/A")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    conn.close()


if __name__ == '__main__':
    main()
