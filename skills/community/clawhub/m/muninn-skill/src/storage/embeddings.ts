/**
 * Muninn Embedding Service
 * 
 * Generates embeddings using:
 * - Local mode: Ollama (nomic-embed-text)
 * - Cloud mode: BYOK or hosted via Muninn API
 * 
 * With TurboQuant compression for 5x storage reduction.
 */

import { getMode, isCloud } from './mode.js';

// Simple imports - compression is optional
type CompressedResult = { embedding: number[]; compressed?: Buffer };

// Local embedding via Ollama
async function generateLocalEmbedding(text: string): Promise<number[]> {
  const ollamaHost = process.env.OLLAMA_HOST || 'http://localhost:11434';
  const model = process.env.EMBEDDING_MODEL || 'nomic-embed-text';
  
  const response = await fetch(`${ollamaHost}/api/embeddings`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ model, prompt: text }),
  });
  
  if (!response.ok) {
    throw new Error(`Ollama embedding failed: ${response.statusText}`);
  }
  
  const data = await response.json();
  return data.embedding;
}

// Cloud embedding via Muninn API
async function generateCloudEmbedding(text: string): Promise<number[]> {
  const apiUrl = process.env.MUNINN_API_URL || 'https://api.muninn.au';
  const apiKey = process.env.MUNINN_API_KEY;
  
  const response = await fetch(`${apiUrl}/v1/embeddings`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`,
    },
    body: JSON.stringify({ input: text }),
  });
  
  if (!response.ok) {
    throw new Error(`Muninn API embedding failed: ${response.statusText}`);
  }
  
  const data = await response.json();
  return data.data[0].embedding;
}

/**
 * Generate embedding for text using the configured mode
 */
export async function generateEmbedding(text: string): Promise<number[]> {
  if (isCloud()) {
    return generateCloudEmbedding(text);
  }
  return generateLocalEmbedding(text);
}

/**
 * Generate embeddings for multiple texts
 */
export async function generateEmbeddings(texts: string[]): Promise<number[][]> {
  return Promise.all(texts.map(t => generateEmbedding(t)));
}

/**
 * Get embedding dimensions based on mode
 */
export function getEmbeddingDimensions(): number {
  if (isCloud()) {
    return parseInt(process.env.EMBEDDING_DIMENSIONS || '1536');
  }
  return 768; // nomic-embed-text
}

/**
 * Generate embedding with optional compression
 * 
 * Usage:
 *   const { embedding, compressed } = await generateWithCompression(text);
 *   // Store 'compressed' in Supabase as BLOB
 */
export async function generateWithCompression(
  text: string,
  bits: number = 3
): Promise<CompressedResult> {
  const embedding = await generateEmbedding(text);
  
  // Lazy-load compression module (only if needed)
  const { compress } = await import('./turboquant-simple.js');
  const compressed = await compress(embedding, bits);
  
  return { embedding, compressed };
}

/**
 * Compute similarity for search
 * 
 * Usage:
 *   const score = await computeSimilarity(query, storedBuffer);
 */
export async function computeSimilarity(
  query: number[],
  compressedBuffer: Buffer
): Promise<number> {
  const { similarity } = await import('./turboquant-simple.js');
  return similarity(query, compressedBuffer);
}

/**
 * Compression statistics
 */
export function getCompressionStats(bits: number = 3): {
  ratio: number;
  savings: number;
} {
  const dim = getEmbeddingDimensions();
  const originalBytes = dim * 2;
  const compressedBytes = 13 + Math.ceil(dim * bits / 8) + Math.ceil(dim / 8);
  
  return {
    ratio: originalBytes / compressedBytes,
    savings: 1 - (compressedBytes / originalBytes),
  };
}