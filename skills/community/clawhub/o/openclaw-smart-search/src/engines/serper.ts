import { SecretManager } from '../key-manager';
import { SearchEngine, SearchResult, SearchOptions, QuotaInfo } from '../types';
import { validateSearchQuery } from '../utils/sanitize';
import * as https from 'https';

/**
 * Serper 搜索引擎适配器
 * API 文档: https://serper.dev/api
 * 提供谷歌搜索结果
 */
export class SerperEngine implements SearchEngine {
  name = 'serper';
  private secretManager = new SecretManager();
  private readonly baseUrl = 'google.serper.dev';
  private readonly timeout = 15000;

  async search(query: string, options: SearchOptions): Promise<SearchResult[]> {
    // 验证和清理输入
    const safeQuery = validateSearchQuery(query);
    const count = Math.min(options.count || 5, 10);

    // 获取 API Key
    let apiKey: string;
    try {
      apiKey = await this.secretManager.getEngineKey('serper');
    } catch (error) {
      throw new Error(`Serper API Key 未配置。请运行: npm run key:set serper`);
    }

    // 调用 Serper API
    const requestBody = JSON.stringify({
      q: safeQuery,
      num: count,
    });

    return new Promise((resolve, reject) => {
      const req = https.request(
        {
          hostname: this.baseUrl,
          port: 443,
          path: '/search',
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-API-KEY': apiKey,
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
                reject(new Error(`Serper API 错误 (${res.statusCode}): ${errorData.message || '未知错误'}`));
                return;
              }

              const response = JSON.parse(data);
              const results: SearchResult[] = [];

              // 处理 organic 结果（网页搜索）
              if (response.organic) {
                for (const item of response.organic) {
                  results.push({
                    title: item.title || '',
                    url: item.link || '',
                    snippet: item.snippet || '',
                    engine: 'serper',
                    originalScore: 0.85,
                  });
                }
              }

              console.log(`[Serper] 成功: ${results.length} 结果`);
              resolve(results);
            } catch (parseError: any) {
              reject(new Error(`Serper 响应解析错误: ${parseError.message}`));
            }
          });
        }
      );

      req.on('error', (err) => {
        reject(new Error(`Serper 请求失败: ${err.message}`));
      });

      req.on('timeout', () => {
        req.destroy();
        reject(new Error(`Serper 请求超时 (${this.timeout}ms)`));
      });

      req.write(requestBody);
      req.end();
    });
  }

  async checkQuota(): Promise<QuotaInfo> {
    // Serper 免费版: 2500 次/月
    // API 不提供实时配额查询，返回理论值
    return {
      used: 0, // 无法查询实际使用量
      limit: 2500,
      remaining: 2500,
    };
  }
}
