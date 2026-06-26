/**
 * Smart Search - 统一智能搜索
 * 主入口文件
 * 
 * 功能：
 * - 智能路由：根据语言和意图选择最佳引擎
 * - 结果合并：多引擎结果去重、评分融合
 * - 超时控制：单个引擎超时 5 秒，不影响其他引擎
 * - 自动降级：主引擎失败时自动切换到备选引擎
 */

// 自动加载 .env 文件
import * as dotenv from 'dotenv';
import * as path from 'path';
dotenv.config({ path: path.join(__dirname, '..', '.env') });

import { SearchOptions, SearchResponse, SearchResult, EngineType } from './types';
import { SmartRouter } from './router';
import { ResultMerger } from './merger';
import { SecretManager } from './key-manager';

/**
 * 默认超时时间（毫秒）
 */
const DEFAULT_TIMEOUT = 5000;

/**
 * 默认最大结果数
 */
const DEFAULT_MAX_RESULTS = 10;

/**
 * 搜索引擎结果（带状态）
 */
interface EngineResult {
  engine: string;
  results: SearchResult[];
  status: 'success' | 'timeout' | 'error';
  error?: string;
  duration: number;
}

/**
 * 智能搜索主函数
 * 
 * @param query 搜索查询
 * @param options 搜索选项
 * @returns 搜索响应
 */
export async function smartSearch(
  query: string,
  options: SearchOptions = {}
): Promise<SearchResponse> {
  const startTime = Date.now();
  
  try {
    // 1. 检查配置
    const configCheck = await checkConfiguration();
    if (!configCheck.configured) {
      return {
        success: false,
        results: [],
        enginesUsed: [],
        fallback: false,
        error: `未配置 API Key。请运行: npm run setup\n详情: ${configCheck.message}`
      };
    }
    
    // 2. 初始化路由器和合并器
    const router = new SmartRouter();
    const merger = new ResultMerger();
    
    // 3. 选择搜索引擎
    const engines = router.select(query, options);
    const engineNames = engines.map(e => e.name);
    
    console.error(`[SmartSearch] 选中引擎: ${engineNames.join(', ')}`);
    
    // 4. 并发搜索（带超时和错误处理）
    const timeout = options.timeout || DEFAULT_TIMEOUT;
    const searchPromises = engines.map(engine =>
      searchWithTimeout(engine, query, options, timeout)
    );
    
    // 使用 Promise.allSettled 确保一个引擎失败不影响其他引擎
    const settledResults = await Promise.allSettled(searchPromises);
    
    // 5. 收集成功的结果
    const engineResults: EngineResult[] = settledResults.map((result, index) => {
      const engine = engines[index];
      
      if (result.status === 'fulfilled') {
        return {
          engine: engine.name,
          results: result.value,
          status: 'success',
          duration: 0
        };
      } else {
        const error = result.reason as Error;
        const isTimeout = error.message?.includes('timeout');
        return {
          engine: engine.name,
          results: [],
          status: isTimeout ? 'timeout' : 'error',
          error: error.message,
          duration: timeout
        };
      }
    });
    
    // 6. 统计结果
    const successfulResults = engineResults.filter(r => r.status === 'success');
    const failedResults = engineResults.filter(r => r.status !== 'success');
    
    // 输出失败信息
    for (const failed of failedResults) {
      console.error(`[${failed.engine}] ${failed.status}: ${failed.error}`);
    }
    
    // 7. 检查是否需要降级
    if (successfulResults.length === 0) {
      // 所有引擎都失败
      return {
        success: false,
        results: [],
        enginesUsed: engineNames,
        fallback: false,
        error: `所有搜索引擎都失败了: ${failedResults.map(r => `${r.engine}: ${r.error}`).join('; ')}`
      };
    }
    
    // 8. 合并结果
    const allResults = successfulResults.map(r => r.results);
    const mergedResults = merger.merge(allResults, {
      maxResults: options.count || DEFAULT_MAX_RESULTS,
      dedupByUrl: true,
      sortByScore: true,
      applyTimeDecay: true,
      applyEngineWeight: true
    });
    
    // 9. 获取合并统计
    const stats = merger.getMergeStats(allResults, mergedResults);
    
    // 10. 构建响应
    const duration = Date.now() - startTime;
    
    console.error(
      `[SmartSearch] 完成: ${stats.uniqueResults} 结果, ` +
      `去重 ${stats.duplicatesRemoved} 条, ` +
      `引擎 ${successfulResults.length}/${engines.length}, ` +
      `耗时 ${duration}ms`
    );
    
    return {
      success: mergedResults.length > 0,
      results: mergedResults,
      enginesUsed: successfulResults.map(r => r.engine),
      fallback: failedResults.length > 0
    };
    
  } catch (error: any) {
    console.error('[SmartSearch] 错误:', error);
    return {
      success: false,
      results: [],
      enginesUsed: [],
      fallback: false,
      error: error.message || '未知错误'
    };
  }
}

/**
 * 带超时的搜索
 */
async function searchWithTimeout(
  engine: { name: string; search: (q: string, o: SearchOptions) => Promise<SearchResult[]> },
  query: string,
  options: SearchOptions,
  timeout: number
): Promise<SearchResult[]> {
  const startTime = Date.now();
  
  try {
    // 使用 Promise.race 实现超时
    const results = await Promise.race([
      engine.search(query, options),
      createTimeoutPromise(timeout, engine.name)
    ]);
    
    const duration = Date.now() - startTime;
    console.error(`[${engine.name}] 成功: ${results.length} 结果, 耗时 ${duration}ms`);
    
    return results;
  } catch (error: any) {
    const duration = Date.now() - startTime;
    console.error(`[${engine.name}] 失败 (${duration}ms): ${error.message}`);
    throw error;
  }
}

/**
 * 创建超时 Promise
 */
function createTimeoutPromise(timeout: number, engineName: string): Promise<never> {
  return new Promise((_, reject) => {
    setTimeout(() => {
      reject(new Error(`[${engineName}] 超时 (${timeout}ms)`));
    }, timeout);
  });
}

/**
 * 检查配置
 */
async function checkConfiguration(): Promise<{ configured: boolean; message: string }> {
  try {
    const secretManager = new SecretManager();
    const config = await secretManager.readConfig();
    
    const configuredEngines = Object.entries(config.engines)
      .filter(([_, cfg]) => cfg.apiKey && cfg.enabled)
      .map(([name, _]) => name);
    
    if (configuredEngines.length === 0) {
      return {
        configured: false,
        message: '未配置任何搜索引擎的 API Key'
      };
    }
    
    return {
      configured: true,
      message: `已配置引擎: ${configuredEngines.join(', ')}`
    };
  } catch (error: any) {
    return {
      configured: false,
      message: error.message || '配置文件不存在'
    };
  }
}

/**
 * 快速搜索（仅使用主引擎）
 */
export async function quickSearch(
  query: string,
  options: SearchOptions = {}
): Promise<SearchResponse> {
  const router = new SmartRouter();
  const analysis = router.analyzeQuery(query, options);
  // 中文或混合语言使用百炼，英文使用 Serper
  const primaryEngine = router.getEngine(
    (analysis.language === 'zh' || analysis.language === 'mixed') ? 'bailian' : 'serper'
  );
  
  try {
    const results = await searchWithTimeout(primaryEngine, query, options, 3000);
    
    return {
      success: results.length > 0,
      results: results.slice(0, options.count || 5),
      enginesUsed: [primaryEngine.name],
      fallback: false
    };
  } catch (error: any) {
    return {
      success: false,
      results: [],
      enginesUsed: [primaryEngine.name],
      fallback: false,
      error: error.message
    };
  }
}

/**
 * 学术搜索（使用 Exa 引擎）
 */
export async function academicSearch(
  query: string,
  options: SearchOptions = {}
): Promise<SearchResponse> {
  return smartSearch(query, { ...options, intent: 'academic' });
}

/**
 * 技术搜索（使用 Exa 引擎）
 */
export async function technicalSearch(
  query: string,
  options: SearchOptions = {}
): Promise<SearchResponse> {
  return smartSearch(query, { ...options, intent: 'technical' });
}

/**
 * 新闻搜索（使用 Tavily 引擎）
 */
export async function newsSearch(
  query: string,
  options: SearchOptions = {}
): Promise<SearchResponse> {
  return smartSearch(query, { ...options, intent: 'news' });
}

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.error('Usage: npm run search "<query>" [options]');
    console.error('\nOptions:');
    console.error('  --count=<n>           Number of results (default: 10)');
    console.error('  --language=<zh|en>   Language preference');
    console.error('  --intent=<type>       Search intent (general, academic, technical, news)');
    console.error('  --deep                Deep research mode (use all 5 engines)');
    console.error('  --timeout=<ms>        Timeout in milliseconds (default: 5000)');
    console.error('\nExamples:');
    console.error('  npm run search "OpenClaw 新功能"');
    console.error('  npm run search "LLM Agent planning" --intent=academic');
    console.error('  npm run search "OpenClaw MCP 配置" --intent=technical --language=zh');
    console.error('  npm run search "人工智能发展报告" --deep');
    process.exit(1);
  }
  
  // 解析参数
  const query = args[0];
  const options: SearchOptions = {};
  
  for (let i = 1; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--count=')) {
      options.count = parseInt(arg.split('=')[1], 10);
    } else if (arg.startsWith('--language=')) {
      options.language = arg.split('=')[1] as 'zh' | 'en';
    } else if (arg.startsWith('--intent=')) {
      options.intent = arg.split('=')[1] as 'general' | 'academic' | 'technical' | 'news';
    } else if (arg === '--deep') {
      options.deep = true;
      options.intent = 'research'; // 深度研究模式
    } else if (arg.startsWith('--timeout=')) {
      (options as any).timeout = parseInt(arg.split('=')[1], 10);
    }
  }
  
  // 执行搜索
  smartSearch(query, options).then(response => {
    console.log(JSON.stringify(response, null, 2));
  }).catch(error => {
    console.error('Error:', error.message);
    process.exit(1);
  });
}