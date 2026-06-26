/**
 * 🎯 Edgefn Rerank Provider
 * 实现标准接口，支持 Edgefn Reranker API
 */

const https = require('https');
const { RerankProvider, RerankResult } = require('../../interfaces');
const { ResilientService } = require('../../utils/resilience');

class EdgefnRerankProvider extends RerankProvider {
  constructor(config = {}) {
    super();
    
    this.config = {
      apiKey: config.apiKey || process.env.EDGEFN_API_KEY,
      baseUrl: config.baseUrl || 'https://api.edgefn.net/v1',
      model: config.model || 'bge-reranker-v2-m3',
      timeout: config.timeout || 15000,
      verbose: config.verbose || false,
      ...config
    };
    
    if (!this.config.apiKey) {
      throw new Error('Edgefn API key is required');
    }
    
    this.name = 'edgefn-reranker';
    this.resilience = new ResilientService({
      maxRetries: 2,
      baseDelay: 500,
      ...config.resilience
    });
    
    this.stats = {
      totalCalls: 0,
      successfulCalls: 0,
      failedCalls: 0,
      totalDocuments: 0,
      totalQueries: 0
    };
    
    this.log(`🚀 ${this.name} provider initialized`);
  }
  
  getName() {
    return this.name;
  }
  
  getMaxDocuments() {
    return 100; // Edgefn API 限制
  }
  
  async rerank(query, documents) {
    if (!query || typeof query !== 'string') {
      throw new Error('Query must be a non-empty string');
    }
    
    if (!documents || !Array.isArray(documents) || documents.length === 0) {
      throw new Error('Documents must be a non-empty array');
    }
    
    this.stats.totalCalls++;
    this.stats.totalQueries++;
    this.stats.totalDocuments += documents.length;
    
    return this.resilience.execute(
      () => this._callRerankAPI(query, documents),
      {
        fallback: (error) => this._fallbackRerank(query, documents, error),
        operationName: 'rerank',
        queryLength: query.length,
        documentsCount: documents.length
      }
    );
  }
  
  async _callRerankAPI(query, documents) {
    return new Promise((resolve, reject) => {
      const requestData = {
        model: this.config.model,
        query: query,
        documents: documents
      };
      
      const req = https.request(
        `${this.config.baseUrl}/rerank`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.config.apiKey}`,
            'Content-Type': 'application/json',
            'User-Agent': 'MemoryCore/1.0'
          },
          timeout: this.config.timeout
        },
        (res) => {
          let responseData = '';
          res.on('data', chunk => responseData += chunk);
          res.on('end', () => {
            try {
              if (res.statusCode === 200) {
                const parsed = JSON.parse(responseData);
                
                if (parsed.results && Array.isArray(parsed.results)) {
                  const results = parsed.results.map((item, index) => 
                    new RerankResult(index, item.relevance_score || 0)
                  );
                  
                  this.stats.successfulCalls++;
                  this.log(`✅ Reranked ${documents.length} documents`);
                  
                  resolve(results);
                } else {
                  reject(new Error('Invalid response format from Edgefn API'));
                }
              } else {
                reject(new Error(`Edgefn API error ${res.statusCode}: ${responseData.substring(0, 200)}`));
              }
            } catch (e) {
              reject(new Error(`Failed to parse response: ${e.message}`));
            }
          });
        }
      );
      
      req.on('error', reject);
      req.on('timeout', () => {
        req.destroy();
        reject(new Error('Request timeout'));
      });
      
      req.write(JSON.stringify(requestData));
      req.end();
    });
  }
  
  async _fallbackRerank(query, documents, originalError) {
    this.log(`⚠️  Using fallback reranking due to: ${originalError.message}`);
    
    // 简单降级：返回均匀分数
    return documents.map((_, index) => 
      new RerankResult(index, 0.1 + (0.9 * index / Math.max(documents.length - 1, 1)))
    );
  }
  
  getStats() {
    const successRate = this.stats.totalCalls > 0 
      ? this.stats.successfulCalls / this.stats.totalCalls 
      : 0;
    
    return {
      ...this.stats,
      name: this.name,
      successRate: Math.round(successRate * 10000) / 100,
      resilienceStats: this.resilience.getStats()
    };
  }
  
  log(...args) {
    if (this.config.verbose) {
      console.log(`[${this.name}]`, ...args);
    }
  }
}

module.exports = EdgefnRerankProvider;
