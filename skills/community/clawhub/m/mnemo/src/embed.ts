/**
 * Embed - Ollama 向量嵌入封装
 *
 * 安全修复 [1/3]：
 * - 移除 child_process exec / curl shell 调用，改用原生 fetch
 *   → 彻底消除通过用户内容注入 shell 命令的风险
 * - checkOllama() 改为直接 HTTP 探测，不再执行任何 shell 命令
 * - 修正拼写错误：nomatic-embed-text → nomic-embed-text
 * - 修复 generateFallbackEmbedding 中 LCG 未累进 seed 的 bug（原实现
 *   每次迭代 seed 不变，导致 768 维全为同一个值）
 */

const OLLAMA_BASE_URL = 'http://localhost:11434';

/**
 * 检查 Ollama 是否运行（通过 HTTP 探测，不执行任何 shell 命令）
 */
export async function checkOllama(): Promise<boolean> {
  try {
    const res = await fetch(`${OLLAMA_BASE_URL}/api/tags`, {
      signal: AbortSignal.timeout(5000),
    });
    if (!res.ok) return false;
    const data = await res.json() as { models?: { name: string }[] };
    return (data.models ?? []).some(
      (m) => m.name.includes('nomic-embed-text') || m.name.includes('embed')
    );
  } catch {
    return false;
  }
}

/**
 * 调用 Ollama 生成向量嵌入
 * 所有参数通过 JSON body 传递，不拼接到任何 shell 命令中
 */
export async function embedText(
  text: string,
  model: string = 'nomic-embed-text'   // 修正：nomatic → nomic
): Promise<number[]> {
  const cleanText = text.replace(/\n+/g, ' ').trim();

  if (!cleanText) {
    return new Array(768).fill(0);
  }

  try {
    const res = await fetch(`${OLLAMA_BASE_URL}/api/embeddings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      // 安全：内容作为 JSON 数据传输，不经过 shell 解析
      body: JSON.stringify({ model, prompt: cleanText }),
      signal: AbortSignal.timeout(30000),
    });

    if (!res.ok) {
      throw new Error(`Ollama HTTP ${res.status}: ${res.statusText}`);
    }

    const response = await res.json() as { embedding?: number[] };

    if (response.embedding && Array.isArray(response.embedding)) {
      return response.embedding;
    }

    throw new Error('Invalid embedding response');
  } catch (e) {
    console.error('[Embed] 向量生成失败，降级到关键词搜索:', e);
    return generateFallbackEmbedding(cleanText);
  }
}

/**
 * 生成降级向量（当 Ollama 不可用时）
 * 修复：LCG 每步更新 state，避免生成全相同维度的向量
 */
function generateFallbackEmbedding(text: string): number[] {
  let state = hashString(text);
  const vector: number[] = [];

  for (let i = 0; i < 768; i++) {
    // 每步更新 state（原代码此处未更新，导致所有维度值相同）
    state = (state * 1103515245 + 12345) & 0x7fffffff;
    vector.push((state % 1000) / 1000 - 0.5);
  }

  const norm = Math.sqrt(vector.reduce((sum, v) => sum + v * v, 0));
  return norm === 0 ? vector : vector.map((v) => v / norm);
}

/**
 * djb2 字符串哈希
 */
function hashString(str: string): number {
  let hash = 5381;
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) + hash) ^ str.charCodeAt(i);
    hash = hash & hash;
  }
  return Math.abs(hash);
}

/**
 * 批量嵌入
 */
export async function embedTexts(
  texts: string[],
  model: string = 'nomic-embed-text'
): Promise<number[][]> {
  return Promise.all(texts.map((text) => embedText(text, model)));
}

/**
 * 计算余弦相似度
 */
export function cosineSimilarity(a: number[], b: number[]): number {
  if (a.length !== b.length) return 0;

  let dot = 0, normA = 0, normB = 0;
  for (let i = 0; i < a.length; i++) {
    dot   += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }

  const denom = Math.sqrt(normA) * Math.sqrt(normB);
  return denom === 0 ? 0 : dot / denom;
}
