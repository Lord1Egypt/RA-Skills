/**
 * Cross-Encoder Reranking
 * 
 * Uses a cross-encoder model to rerank retrieval results
 * for better precision. Cross-encoders jointly encode query+document,
 * providing more accurate relevance scores than separate encoding.
 */

import { pipeline, env } from '@xenova/transformers';

// Skip model download warnings
env.allowLocalModels = false;
env.useBrowserCache = true;

// Singleton reranker instance
let rerankerInstance: any = null;
let rerankerModel: string = 'cross-encoder/ms-marco-MiniLM-L-6-v2';

/**
 * Get or initialize the reranker
 */
async function getReranker() {
  if (!rerankerInstance) {
    console.log('🔄 Loading cross-encoder reranker...');
    rerankerInstance = await pipeline('feature-extraction', rerankerModel, {
      quantized: true,
    });
    console.log('✅ Cross-encoder reranker loaded');
  }
  return rerankerInstance;
}

/**
 * Rerank documents using cross-encoder
 * 
 * @param query - Search query
 * @param documents - Documents to rerank
 * @param topK - Number of top results to return
 * @returns Reranked documents with scores
 */
export async function rerankWithCrossEncoder<T extends { content: string; id: string }>(
  query: string,
  documents: T[],
  topK: number = 10
): Promise<Array<{ doc: T; score: number }>> {
  if (documents.length === 0) return [];
  if (documents.length === 1) {
    return [{ doc: documents[0], score: 1.0 }];
  }
  
  try {
    const reranker = await getReranker();
    
    // Create query-document pairs
    const pairs = documents.map(doc => `[CLS] ${query} [SEP] ${doc.content} [SEP]`);
    
    // Get scores for all pairs
    const outputs = await reranker(pairs, {
      pooling: 'mean',
      normalize: true,
    });
    
    // Extract scores and sort
    const scored = documents.map((doc, i) => ({
      doc,
      score: typeof outputs[i] === 'number' ? outputs[i] : outputs[i].data?.[0] || 0
    }));
    
    scored.sort((a, b) => b.score - a.score);
    
    return scored.slice(0, topK);
  } catch (error) {
    console.warn('Cross-encoder reranking failed:', error);
    // Fallback: return original order with uniform scores
    return documents.map(doc => ({ doc, score: 1.0 }));
  }
}

/**
 * Lightweight reranking using simpler method
 * Useful when cross-encoder is too slow
 */
export function lightweightRerank<T extends { content: string; id: string }>(
  query: string,
  documents: T[],
  topK: number = 10
): Array<{ doc: T; score: number }> {
  const queryTerms = new Set(
    query.toLowerCase().split(/\s+/).filter(t => t.length > 2)
  );
  
  const scored = documents.map(doc => {
    const contentTerms = doc.content.toLowerCase().split(/\s+/);
    let matches = 0;
    let positionBonus = 0;
    
    for (let i = 0; i < contentTerms.length; i++) {
      if (queryTerms.has(contentTerms[i])) {
        matches++;
        // Earlier matches get higher bonus
        positionBonus += 1 / (i + 1);
      }
    }
    
    const termScore = matches / Math.max(queryTerms.size, 1);
    const positionScore = positionBonus / Math.max(queryTerms.size, 1);
    
    return {
      doc,
      score: termScore * 0.7 + positionScore * 0.3
    };
  });
  
  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, topK);
}

/**
 * Set custom reranker model
 */
export function setRerankerModel(model: string) {
  rerankerModel = model;
  // Reset instance to load new model
  rerankerInstance = null;
}
