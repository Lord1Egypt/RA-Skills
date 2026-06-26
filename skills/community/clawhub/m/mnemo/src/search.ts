/**
 * Memory Search - 向量语义搜索实现
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import type { MemorySystemConfig } from './index.js';
import { embedText } from './embed.js';

interface SearchResult {
  path: string;
  content: string;
  score: number;
  lines: number;
}

/**
 * 展开路径中的 ~ 和环境变量
 */
function expandPath(p: string): string {
  if (p.startsWith('~')) {
    return path.join(process.env.HOME || '', p.slice(1));
  }
  return path.resolve(p);
}

/**
 * 扫描记忆目录获取所有文件
 * 安全：只扫描 memoryDir 内的文件
 */
async function scanMemoryFiles(memoryDir: string, group?: string): Promise<string[]> {
  const files: string[] = [];
  const baseDir = expandPath(memoryDir);
  
  // 解析为绝对路径并验证
  const resolvedBaseDir = path.resolve(baseDir);
  
  // 确定搜索目录
  let searchDir = resolvedBaseDir;
  if (group) {
    // 防止 group 参数进行路径遍历
    const safeGroup = group.replace(/[^a-zA-Z0-9_-]/g, '');
    searchDir = path.join(resolvedBaseDir, 'groups', safeGroup);
  }

  // 验证搜索目录在 baseDir 内
  if (!searchDir.startsWith(resolvedBaseDir + path.sep) && searchDir !== resolvedBaseDir) {
    console.warn('[MemorySearch] 拒绝访问目录外:', searchDir);
    return files;
  }

  try {
    await fs.access(searchDir);
  } catch {
    // 目录不存在，返回空
    return files;
  }

  // 递归扫描 .md 文件
  async function scan(dir: string) {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory() && !entry.name.startsWith('.')) {
        await scan(fullPath);
      } else if (entry.name.endsWith('.md')) {
        files.push(fullPath);
      }
    }
  }

  await scan(searchDir);
  return files;
}

/**
 * 简单的关键词匹配（当向量不可用时的降级方案）
 */
async function keywordSearch(
  query: string,
  files: string[],
  topK: number
): Promise<SearchResult[]> {
  const results: SearchResult[] = [];
  const queryLower = query.toLowerCase();
  const queryWords = queryLower.split(/\s+/);

  for (const file of files) {
    try {
      const content = await fs.readFile(file, 'utf-8');
      const lines = content.split('\n');
      
      // 计算匹配分数
      let score = 0;
      let matchedLine = '';
      
      for (const line of lines) {
        const lineLower = line.toLowerCase();
        let lineScore = 0;
        
        for (const word of queryWords) {
          if (lineLower.includes(word)) {
            lineScore += 1;
            // 标题匹配加更多分
            if (line.startsWith('#') || line.startsWith('##')) {
              lineScore += 2;
            }
          }
        }
        
        if (lineScore > score) {
          score = lineScore;
          matchedLine = line;
        }
      }

      if (score > 0) {
        results.push({
          path: file,
          content: matchedLine || content.slice(0, 200),
          score,
          lines: lines.length
        });
      }
    } catch (e) {
      console.error(`[MemorySearch] 读取文件失败: ${file}`, e);
    }
  }

  // 按分数排序，返回 topK
  return results
    .sort((a, b) => b.score - a.score)
    .slice(0, topK);
}

/**
 * 向量搜索实现
 */
async function vectorSearch(
  query: string,
  files: string[],
  topK: number,
  config: MemorySystemConfig
): Promise<SearchResult[]> {
  // 获取查询向量
  const queryEmbedding = await embedText(query, config.embeddingModel);
  
  const results: SearchResult[] = [];

  for (const file of files) {
    try {
      const content = await fs.readFile(file, 'utf-8');
      const lines = content.split('\n');
      
      // 将内容分块，每 100 行一块
      const chunkSize = 100;
      for (let i = 0; i < lines.length; i += chunkSize) {
        const chunk = lines.slice(i, i + chunkSize).join('\n');
        const chunkEmbedding = await embedText(chunk, config.embeddingModel);
        
        // 计算余弦相似度
        const similarity = cosineSimilarity(queryEmbedding, chunkEmbedding);
        
        results.push({
          path: file,
          content: chunk,
          score: similarity,
          lines: lines.length
        });
      }
    } catch (e) {
      console.error(`[MemorySearch] 向量搜索文件失败: ${file}`, e);
    }
  }

  // 按相似度排序
  return results
    .sort((a, b) => b.score - a.score)
    .slice(0, topK);
}

/**
 * 余弦相似度计算
 */
function cosineSimilarity(a: number[], b: number[]): number {
  if (a.length !== b.length) return 0;
  
  let dotProduct = 0;
  let normA = 0;
  let normB = 0;
  
  for (let i = 0; i < a.length; i++) {
    dotProduct += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }
  
  return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}

/**
 * 主搜索函数
 */
export async function memorySearch(
  query: string,
  topK: number = 5,
  group?: string,
  config?: MemorySystemConfig
): Promise<{ results: SearchResult[] }> {
  const cfg = config || {
    memoryDir: '~/.openclaw/workspace/memory',
    vectorEnabled: true,
    embeddingModel: 'nomic-embed-text'
  } as MemorySystemConfig;

  console.log(`[MemorySearch] 搜索: "${query}" (group: ${group || 'all'}, topK: ${topK})`);

  // 获取所有记忆文件
  const files = await scanMemoryFiles(cfg.memoryDir, group);
  
  if (files.length === 0) {
    return { results: [] };
  }

  console.log(`[MemorySearch] 扫描到 ${files.length} 个记忆文件`);

  // 根据配置选择搜索方式
  let results: SearchResult[];
  
  if (cfg.vectorEnabled) {
    try {
      results = await vectorSearch(query, files, topK, cfg);
    } catch (e) {
      console.warn('[MemorySearch] 向量搜索失败，降级到关键词搜索', e);
      results = await keywordSearch(query, files, topK);
    }
  } else {
    results = await keywordSearch(query, files, topK);
  }

  // 格式化返回结果
  return {
    results: results.map(r => ({
      path: r.path.replace(expandPath(cfg.memoryDir), '').replace(/^[/\\]/, ''),
      content: r.content.slice(0, 500),
      score: Math.round(r.score * 100) / 100,
      lines: r.lines
    }))
  };
}
