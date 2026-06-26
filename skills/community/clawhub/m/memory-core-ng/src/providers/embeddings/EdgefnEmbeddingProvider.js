/**
 * 🎯 Edgefn Embeddings Provider
 * 实现标准接口，支持 Edgefn API
 */

const https = require('https');
const { EmbeddingProvider } = require('../../interfaces');
const { ResilientService } = require('../../utils/resilience');

class EdgefnEmbeddingProvider extends EmbeddingProvider {
  constructor(config = {}) {
    super();
    
    this.config = {
      apiKey: config.apiKey || process.env.EDGEFN_API_KEY,
      baseUrl: config.baseUrl || 'https://api.edgefn.net/v1',
      model: config.model || 'BAAI/bge-m3',
      dimensions: config.dimensions || 1024,
      timeout: config.timeout || 15000,
      verbose: config.verbose || false,
      ...config
    };
    
    if (!this.config.apiKey) {
      throw new Error('Edgefn API key is required');
    }
    
    this.name = 'edgefn-embeddings';
    this.resilience = new ResilientService({
      maxRetries: 2,
      baseDelay: 500,
      ...config.resilience
    });
    
    this.stats = {
      totalCalls: 0,
      successfulCalls: 0,
      failedCalls: 0,
      totalTexts: 0,
      totalTokens: 0
    };
    
    this.log(`🚀 ${this.name} provider initialized`);
  }
  
  getName() {
    return this.name;
  }
  
  getDimensions() {
    return this.config.dimensions;
  }
  
  supportsBatch() {
    return true;
  }
  
  getMaxBatchSize() {
    return 50; // Edgefn API 限制
  }
  
  async generateEmbeddings(texts) {
    if (!texts || !Array.isArray(texts) || texts.length === 0) {
      throw new Error('Texts must be a non-empty array');
    }
    
    this.stats.totalCalls++;
    this.stats.totalTexts += texts.length;
    
    // 估算 tokens（近似）
    this.stats.totalTokens += texts.reduce((sum, text) => sum + Math.ceil(text.length / 4), 0);
    
    return this.resilience.execute(
      () => this._callEmbeddingsAPI(texts),
      {
        fallback: (error) => this._fallbackEmbeddings(texts, error),
        operationName: 'generateEmbeddings',
        textsCount: texts.length
      }
    );
  }
  
  async _callEmbeddingsAPI(texts) {
    return new Promise((resolve, reject) => {
      const requestData = {
        model: this.config.model,
        input: texts,
        dimensions: this.config.dimensions
      };
      
      const req = https.request(
        `${this.config.baseUrl}/embeddings`,
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
                
                if (parsed.data && Array.isArray(parsed.data)) {
                  const embeddings = parsed.data.map(item => item.embedding);
                  
                  this.stats.successfulCalls++;
                  this.log(`✅ Generated ${embeddings.length} embeddings`);
                  
                  resolve(embeddings);
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
  
  async _fallbackEmbeddings(texts, originalError) {
    this.log(`⚠️  Using fallback embeddings due to: ${originalError.message}`);
    
    // 简单降级：返回零向量
    const dimensions = this.getDimensions();
    const zeroVector = new Array(dimensions).fill(0);
    
    return texts.map(() => [...zeroVector]); // 复制数组
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

module.exports = EdgefnEmbeddingProvider;
