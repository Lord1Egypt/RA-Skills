import { SecretManager } from '../key-manager';
import { SearchEngine, SearchResult, SearchOptions, QuotaInfo } from '../types';
import { validateSearchQuery } from '../utils/sanitize';
import * as https from 'https';

/**
 * Firecrawl 搜索引擎适配器
 * API 文档: https://docs.firecrawl.dev/api-reference/endpoint/search
 * 专注于网页抓取和内容提取
 */
export class FirecrawlEngine implements SearchEngine {
  name = 'firecrawl';
  private secretManager = new SecretManager();
  private readonly baseUrl = 'api.firecrawl.dev';
  private readonly timeout = 20000; // Firecrawl 可能较慢

  async search(query: string, options: SearchOptions): Promise<SearchResult[]> {
    // 验证和清理输入
    const safeQuery = validateSearchQuery(query);
    const count = Math.min(options.count || 5, 10);

    // 获取 API Key
    let apiKey: string;
    try {
      apiKey = await this.secretManager.getEngineKey('firecrawl');
    } catch (error) {
      throw new Error(`Firecrawl API Key 未配置。请运行: npm run key:set firecrawl`);
    }

    // 调用 Firecrawl Search API
    const requestBody = JSON.stringify({
      query: safeQuery,
      limit: count,
      scrapeOptions: {
        formats: ['markdown'],
      },
    });

    return new Promise((resolve, reject) => {
      const req = https.request(
        {
          hostname: this.baseUrl,
          port: 443,
          path: '/v1/search',
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${apiKey}`,
            'Content-Length': Buffer.byteLength(requestBody),
          },
          timeout: this.timeout,
        },
        (res) => {
          let data = '';
          res.on('data', (chunk) => (data += chunk));
          res.on('end', () => {
            try {
              if (res.statusCode !== 200) {
                const errorData = JSON.parse(data);
                reject(new Error(`Firecrawl API 错误 (${res.statusCode}): ${errorData.message || errorData.error || '未知错误'}`));
                return;
              }

              const response = JSON.parse(data);
              const results: SearchResult[] = [];

              // Firecrawl 返回格式: { data: [...] }
              const items = response.data || response.results || [];
              for (const item of items) {
                results.push({
                  title: item.metadata?.title || item.title || '',
                  url: item.metadata?.sourceURL || item.url || '',
                  snippet: item.markdown?.substring(0, 300) || item.description || '',
                  content: item.markdown || undefined,
                  engine: 'firecrawl',
                  originalScore: 0.8,
                });
              }

              console.log(`[Firecrawl] 成功: ${results.length} 结果`);
              resolve(results);
            } catch (parseError: any) {
              reject(new Error(`Firecrawl 响应解析错误: ${parseError.message}`));
            }
          });
        }
      );

      req.on('error', (err) => {
        reject(new Error(`Firecrawl 请求失败: ${err.message}`));
      });

      req.on('timeout', () => {
        req.destroy();
        reject(new Error(`Firecrawl 请求超时 (${this.timeout}ms)`));
      });

      req.write(requestBody);
      req.end();
    });
  }

  async checkQuota(): Promise<QuotaInfo> {
    // Firecrawl 免费版: 500 页/月
    // API 不提供实时配额查询，返回理论值
    return {
      used: 0, // 无法查询实际使用量
      limit: 500,
      remaining: 500,
    };
  }
}
