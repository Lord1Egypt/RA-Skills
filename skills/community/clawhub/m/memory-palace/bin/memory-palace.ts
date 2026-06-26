#!/usr/bin/env node
import { MemoryPalaceManager } from '../dist/src/manager.js';
import { createTimeReasoning } from '../dist/src/background/time-reasoning.js';
import { defaultSummarizer } from '../dist/src/llm/summarizer.js';
import { defaultExtractor } from '../dist/src/llm/experience-extractor.js';
import { defaultExpander } from '../dist/src/llm/concept-expander.js';
import { defaultCompressor } from '../dist/src/llm/smart-compressor.js';
import { createLocalVectorSearch } from '../dist/src/background/vector-search.js';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Parse CLI arguments
const cliArgs = process.argv.slice(2);
let dbPath = null;

// Look for --db-path in arguments
for (let i = 0; i < cliArgs.length; i++) {
  if (cliArgs[i] === '--db-path' && i + 1 < cliArgs.length) {
    dbPath = cliArgs[i + 1];
    break;
  }
}

// Workspace path from env or default
const workspacePath = process.env.OPENCLAW_WORKSPACE || process.env.HOME + '/.openclaw/workspace';
const memoryPath = join(workspacePath, 'memory', 'palace');

// Create vector search provider with dbPath if provided
let vectorSearch = null;
if (dbPath) {
  const vectorConfig = { dbPath };
  vectorSearch = createLocalVectorSearch(vectorConfig);
  console.error('[memory-palace] Using custom db-path:', dbPath);
}

const manager = new MemoryPalaceManager({ 
  workspaceDir: memoryPath,
  vectorSearch 
});
const timeReasoning = createTimeReasoning();
const summarizer = defaultSummarizer;

const action = process.argv[2];

/**
 * Parse CLI arguments - supports both JSON and key=value formats
 * Examples:
 *   JSON: '{"id":"xxx","content":"test"}'
 *   key=value: id=xxx content=test
 */
function parseArgs(raw: string): Record<string, unknown> {
  if (!raw) return {};
  if (raw.includes('=')) {
    // key=value 格式解析
    return Object.fromEntries(raw.split(' ').map(pair => pair.split('=')));
  }
  // 回退 JSON 解析
  try {
    return JSON.parse(raw);
  } catch {
    return {};
  }
}

const args = parseArgs(process.argv[3] || '{}');

async function main() {
  let result;
  
  switch (action) {
    // ========== 基础操作 ==========
    case 'write':
      result = await manager.store({
        content: args.content,
        location: args.location,
        tags: args.tags,
        importance: args.importance,
        type: args.type
      });
      break;
      
    case 'get':
      // 支持对象风格: { id } 或旧版: id 字符串
      result = await manager.get(args.id);
      break;
      
    case 'update':
      result = await manager.update({
        id: args.id,
        content: args.content,
        tags: args.tags,
        importance: args.importance,
        summary: args.summary
      });
      break;
      
    case 'delete':
      result = await manager.delete(args.id, args.permanent);
      break;
      
    case 'search':
      // 支持对象风格 { query, ...options }
      result = await manager.recall({
        query: args.query,
        tags: args.tags,
        topK: args.topK || args.top_k,
        location: args.location
      });
      break;
      
    case 'list':
      result = await manager.list({
        location: args.location,
        tags: args.tags,
        status: args.status,
        limit: args.limit
      });
      break;
      
    case 'stats':
      result = await manager.stats();
      break;
      
    case 'restore':
      result = await manager.restore(args.id);
      break;
      
    // ========== 记忆关联 ==========
    case 'link':
      // 将两条记忆关联起来
      // 参数: { sourceId, targetId, type, note? }
      result = await manager.linkMemories(args.sourceId, {
        type: args.type,
        targetId: args.targetId,
        note: args.note,
      });
      break;
      
    case 'get_related':
      // 获取关联记忆
      // 参数: { id, type? }
      result = await manager.getRelatedMemories(args.id, args.type);
      break;

    // ========== 经验管理 ==========
    case 'record_experience':
      // 命令格式: record_experience <content> <applicability> <source> [category]
      // 或者通过 args: { content, applicability, source, category }
      result = await manager.recordExperience({
        content: args.content,
        applicability: args.applicability,
        source: args.source,
        category: args.category,
        tags: args.tags
      });
      break;
      
    case 'get_experiences':
      // 命令格式: get_experiences [--category] [--verified]
      result = await manager.getExperiences({
        category: args.category,
        verified: args.verified,
        limit: args.limit || 10,
        sortByVerified: args.sortByVerified
      });
      break;
      
    case 'verify_experience':
      // 命令格式: verify_experience <id> <effective>
      result = await manager.verifyExperience({
        id: args.id,
        effective: args.effective
      });
      break;
      
    case 'get_relevant_experiences':
      // 支持对象风格 { context, limit }
      result = await manager.getRelevantExperiences({
        context: args.context,
        limit: args.limit || 5
      });
      break;
      
    case 'experience_stats':
      result = await manager.getExperienceStats();
      break;

    // ========== LLM 增强功能 ==========
    case 'summarize':
      // 命令格式: summarize <id>
      const mem = await manager.get(args.id);
      if (!mem) {
        throw new Error(`Memory not found: ${args.id}`);
      }
      const summaryResult = await summarizer.summarize(mem.content);
      result = summaryResult.success ? summaryResult.data : { error: summaryResult.error };
      break;
      
    case 'parse_time':
      // 命令格式: parse_time <expression>
      // 使用规则引擎解析时间
      const timeContext = timeReasoning.parseTimeQuery(args.expression);
      result = {
        hasTimeReasoning: timeContext.hasTimeReasoning,
        keywords: timeContext.keywords,
        resolvedDate: timeContext.resolvedDate,
        expression: args.expression
      };
      break;
      
    // ========== LLM 经验提取 ==========
    case 'extract_experience':
      // 命令格式: extract_experience [--memory_ids] [--category]
      // 从记忆中提取可复用的经验
      const extractMemoryIds = args.memory_ids || [];
      const extractCategory = args.category || null;
      
      // 如果没有指定 memory_ids，获取所有记忆
      let memoriesToExtract;
      if (extractMemoryIds.length > 0) {
        memoriesToExtract = [];
        for (const id of extractMemoryIds) {
          const mem = await manager.get(id);
          if (mem) {
            // 按 category 过滤
            if (!extractCategory || mem.tags?.includes(extractCategory)) {
              memoriesToExtract.push(mem);
            }
          }
        }
      } else {
        // 获取所有记忆
        const allMemories = await manager.list({ limit: 100 });
        memoriesToExtract = allMemories;
        if (extractCategory) {
          memoriesToExtract = memoriesToExtract.filter(m => 
            m.tags?.includes(extractCategory)
          );
        }
      }
      
      const extractResult = await defaultExtractor.extract(memoriesToExtract, {
        focusArea: extractCategory,
        maxExperiences: 20
      });
      
      result = {
        experiences: extractResult.success ? extractResult.data.map(exp => ({
          content: exp.experience,
          category: extractCategory || 'general',
          applicability: exp.context,
          lessons: exp.lessons,
          bestPractices: exp.bestPractices,
          sourceMemoryId: extractMemoryIds.length === 1 ? extractMemoryIds[0] : null
        })) : [],
        count: extractResult.success ? extractResult.data.length : 0,
        error: extractResult.error || null
      };
      break;
      
    case 'expand_concepts':
      // 命令格式: expand_concepts <query> [--mode]
      // 使用 LLM 动态扩展搜索概念
      const expandQuery = args.query;
      const expandMode = args.mode || 'search';
      
      const expandResult = await defaultExpander.expand(expandQuery, {
        maxKeywords: 10,
        maxDomains: 3
      });
      
      result = {
        originalQuery: expandQuery,
        expandedKeywords: expandResult.success ? expandResult.data?.keywords || [] : [expandQuery],
        relatedConcepts: expandResult.success ? expandResult.data?.keywords?.slice(0, 5) || [] : [],
        domains: expandResult.success ? expandResult.data?.domains || [] : []
      };
      break;
      
    case 'compress':
      // 命令格式: compress <memory_ids>
      // 智能压缩多条记忆
      const compressMemoryIds = args.memory_ids || [];
      
      if (compressMemoryIds.length < 2) {
        result = { error: '需要至少 2 条记忆才能压缩' };
        break;
      }
      
      // 获取要压缩的记忆
      const memoriesToCompress = [];
      for (const id of compressMemoryIds) {
        const mem = await manager.get(id);
        if (mem) {
          memoriesToCompress.push(mem);
        }
      }
      
      if (memoriesToCompress.length < 2) {
        result = { error: '有效的记忆少于 2 条，无法压缩' };
        break;
      }
      
      const compressResult = await defaultCompressor.compress(memoriesToCompress, {
        minMemories: 2,
        maxContentLength: 500
      });
      
      const totalOriginalChars = memoriesToCompress.reduce((sum, m) => sum + m.content.length, 0);
      
      if (compressResult.success) {
        result = {
          compressedMemories: compressMemoryIds.map((id, idx) => ({
            id: id,
            compressedContent: idx === 0 ? compressResult.data?.compressedContent : null,
            preservedKeyInfo: idx === 0 ? compressResult.data?.preservedKeyInfo || [] : [],
            compressionRatio: compressResult.data?.compressionRatio || 0
          })),
          totalOriginalChars,
          totalCompressedChars: compressResult.data?.compressedContent?.length || 0
        };
      } else {
        result = { error: compressResult.error || '压缩失败' };
      }
      break;
      
    default:
      console.error('Unknown action:', action);
      console.error('Available actions:');
      console.error('  - write, get, update, delete, search, list, stats, restore');
      console.error('  - record_experience, get_experiences, verify_experience, get_relevant_experiences, experience_stats');
      console.error('  - summarize, parse_time');
      console.error('  - extract_experience, expand_concepts, compress');
      console.error('  - link, get_related');
      process.exit(1);
  }
  
  console.log(JSON.stringify(result, null, 2));
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});