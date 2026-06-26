import { SecretManager } from '../key-manager';
import { SearchEngine, SearchResult, SearchOptions, QuotaInfo } from '../types';
import { validateSearchQuery } from '../utils/sanitize';
import * as https from 'https';

/**
 * Exa 搜索引擎适配器
 * API 文档: https://docs.exa.ai/reference/search
 * 专注于学术和技术搜索
 */
export class ExaEngine implements SearchEngine {
  name = 'exa';
  private secretManager = new SecretManager();
  private readonly baseUrl = 'api.exa.ai';
  private readonly timeout = 15000;

  async search(query: string, options: SearchOptions): Promise<SearchResult[]> {
    // 验证和清理输入
    const safeQuery = validateSearchQuery(query);
    const count = Math.min(options.count || 5, 10);

    // 获取 API Key
    let apiKey: string;
    try {
      apiKey = await this.secretManager.getEngineKey('exa');
    } catch (error) {
      throw new Error(`Exa API Key 未配置。请运行: npm run key:set exa`);
    }

    // 根据 intent 选择搜索类型
    const useAutoprompt = options.intent === 'academic' || options.intent === 'technical';

    // 调用 Exa API
    const requestBody = JSON.stringify({
      query: safeQuery,
      numResults: count,
      useAutoprompt: useAutoprompt,
      contents: {
        text: { maxCharacters: 500 },
      },
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
            'x-api-key': apiKey,
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
                reject(new Error(`Exa API 错误 (${res.statusCode}): ${errorData.message || errorData.error || '未知错误'}`));
                return;
              }

              const response = JSON.parse(data);
              const results: SearchResult[] = (response.results || []).map((item: any) => ({
                title: item.title || '',
                url: item.url || '',
                snippet: item.text || item.summary || '',
                engine: 'exa',
                originalScore: item.score || 0.85,
                publishedDate: item.publishedDate || undefined,
              }));

              console.log(`[Exa] 成功: ${results.length} 结果`);
              resolve(results);
            } catch (parseError: any) {
              reject(new Error(`Exa 响应解析错误: ${parseError.message}`));
            }
          });
        }
      );

      req.on('error', (err) => {
        reject(new Error(`Exa 请求失败: ${err.message}`));
      });

      req.on('timeout', () => {
        req.destroy();
        reject(new Error(`Exa 请求超时 (${this.timeout}ms)`));
      });

      req.write(requestBody);
      req.end();
    });
  }

  async checkQuota(): Promise<QuotaInfo> {
    // Exa 免费版: 1000 次/月
    // API 不提供实时配额查询，返回理论值
    return {
      used: 0, // 无法查询实际使用量
      limit: 1000,
      remaining: 1000,
    };
  }
}
