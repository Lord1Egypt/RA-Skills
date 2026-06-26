/**
 * LLM Answer Generator for LOCOMO Benchmark
 * 
 * Generates concise answers from retrieved memories using OpenAI API
 * Optimized for speed with minimal context
 */

import MemoryStore, { Memory } from '../storage/index.js';

// OpenAI API configuration
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const OPENAI_MODEL = 'gpt-4o-mini'; // Fast, cheap, good quality

/**
 * Generate concise answer from retrieved memories using OpenAI
 * Optimized for speed: uses minimal context and small response
 */
export async function generateAnswer(
  query: string,
  memories: Memory[],
  options?: { maxTokens?: number; model?: string }
): Promise<string> {
  // Edge case: no memories
  if (!memories || memories.length === 0) {
    return "I don't have information about that.";
  }

  // Use top 3 memories, truncate to first 400 chars each
  const context = memories
    .slice(0, 3)
    .map(m => m.content.slice(0, 400))
    .join('\n\n---\n\n');

  const model = options?.model || OPENAI_MODEL;
  const maxTokens = options?.maxTokens || 100;

  try {
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${OPENAI_API_KEY}`
      },
      body: JSON.stringify({
        model,
        messages: [
          {
            role: 'system',
            content: 'Answer questions based on the provided context. Be concise and specific. Use exact names, dates, and numbers from the context. If the answer is not in the context, say "I don\'t have information about that."'
          },
          {
            role: 'user',
            content: `Context:\n${context}\n\nQuestion: ${query}\n\nAnswer (be concise and specific):`
          }
        ],
        max_tokens: maxTokens,
        temperature: 0.1
      })
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`OpenAI API error: ${response.status} ${error}`);
    }

    const data = await response.json() as { choices: Array<{ message: { content: string } }> };
    return data.choices[0]?.message?.content?.trim() || "I don't have information about that.";
  } catch (error) {
    console.error('OpenAI generation failed:', error);
    // Fallback: extract relevant sentence from first memory
    const content = memories[0]?.content || '';
    const sentences = content.split(/[.!?]/).filter(s => s.trim().length > 10);
    return sentences[0]?.trim() + '.' || "I don't have information about that.";
  }
}

/**
 * Check if generated answer matches expected answer using OpenAI
 */
export async function checkAnswerWithLLM(
  generated: string,
  expected: string,
  question: string,
  options?: { model?: string }
): Promise<boolean> {
  const model = options?.model || OPENAI_MODEL;

  try {
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${OPENAI_API_KEY}`
      },
      body: JSON.stringify({
        model,
        messages: [
          {
            role: 'system',
            content: 'You are an answer evaluator. Judge if the generated answer contains the key information from the expected answer. Be lenient - if the generated answer conveys the same meaning, count it as correct. Reply with only "CORRECT" or "WRONG".'
          },
          {
            role: 'user',
            content: `Question: ${question}\nExpected Answer: ${expected}\nGenerated Answer: ${generated}\n\nIs the generated answer correct?`
          }
        ],
        max_tokens: 10,
        temperature: 0
      })
    });

    if (!response.ok) {
      throw new Error(`OpenAI API error: ${response.status}`);
    }

    const data = await response.json() as { choices: Array<{ message: { content: string } }> };
    const result = data.choices[0]?.message?.content?.trim().toUpperCase() || 'WRONG';
    return result === 'CORRECT';
  } catch (error) {
    console.error('OpenAI check failed:', error);
    // Fallback to substring matching
    const generatedLower = generated.toLowerCase();
    const expectedLower = expected.toLowerCase();
    return generatedLower.includes(expectedLower) ||
           expectedLower.split(', ').some(e => generatedLower.includes(e.toLowerCase()));
  }
}

// Simple cache for LLM responses
const answerCache = new Map<string, { answer: string; timestamp: number }>();
const CACHE_TTL_MS = 5 * 60 * 1000; // 5 minutes

/**
 * Generate answer with caching
 */
export async function generateAnswerWithCache(
  query: string,
  memories: Memory[],
  options?: { maxTokens?: number; model?: string }
): Promise<string> {
  const cacheKey = `${query}:${memories.map(m => m.id).join(',')}`;
  
  const cached = answerCache.get(cacheKey);
  if (cached && Date.now() - cached.timestamp < CACHE_TTL_MS) {
    return cached.answer;
  }

  const answer = await generateAnswer(query, memories, options);
  answerCache.set(cacheKey, { answer, timestamp: Date.now() });
  
  return answer;
}

/**
 * Check answer with caching
 */
export async function checkAnswerWithCache(
  generated: string,
  expected: string,
  question: string,
  options?: { model?: string }
): Promise<boolean> {
  const cacheKey = `check:${question}:${generated.slice(0, 50)}`;
  
  const cached = answerCache.get(cacheKey);
  if (cached && Date.now() - cached.timestamp < CACHE_TTL_MS) {
    return cached.answer === 'true';
  }

  const result = await checkAnswerWithLLM(generated, expected, question, options);
  answerCache.set(cacheKey, { answer: String(result), timestamp: Date.now() });
  
  return result;
}
