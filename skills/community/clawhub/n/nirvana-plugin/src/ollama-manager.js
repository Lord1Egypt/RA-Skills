/**
 * Ollama Manager - Local LLM Lifecycle Management
 * 
 * Handles:
 * - Installation & setup
 * - Model downloading & caching
 * - Health monitoring
 * - Graceful degradation
 */

const http = require('http');
const { exec } = require('child_process');
const { promisify } = require('util');

const execAsync = promisify(exec);

class OllamaManager {
  constructor(config, openclaw) {
    this.config = config || {};
    this.openclaw = openclaw;
    this.endpoint = this.config.endpoint || 'http://ollama:11434';
    this.models = this.config.models || ['qwen2.5:7b', 'qwen3.5:9b'];
    this.bundledModel = this.config.bundledModel || 'qwen2.5:7b';
    this.healthy = false;
    this.activeRequests = 0;
    this.maxConcurrent = this.config.maxConcurrentRequests || 2;
    this.healthCheckInterval = null;
  }

  /**
   * Initialize Ollama manager
   * - Check if Ollama is already running
   * - Ensure bundled model is available (critical)
   * - Pull optional additional models
   * - Start health monitoring
   */
  async initialize() {
    try {
      console.log('[Ollama] Initializing Ollama manager...');

      // Step 1: Check if Ollama is accessible
      const isRunning = await this.checkHealth();
      if (!isRunning) {
        throw new Error('Ollama is not running at ' + this.endpoint);
      }

      console.log('[Ollama] Ollama API is responsive');

      // Step 2: Ensure bundled model is available (critical for out-of-box)
      console.log('[Ollama] Ensuring bundled model available:', this.bundledModel);
      try {
        await this.pullModel(this.bundledModel);
        console.log('[Ollama] Bundled model ready:', this.bundledModel);
      } catch (error) {
        console.error('[Ollama] CRITICAL: Failed to pull bundled model:', error.message);
        throw new Error('Failed to initialize bundled model. Nirvana cannot operate without: ' + this.bundledModel);
      }

      // Step 3: Pull optional additional models (non-critical)
      if (this.config.autoDownload) {
        const otherModels = this.models.filter(m => m !== this.bundledModel);
        for (const model of otherModels) {
          try {
            await this.pullModel(model);
            console.log('[Ollama] Successfully pulled optional model:', model);
          } catch (error) {
            console.warn('[Ollama] Failed to pull optional model:', model, '—', error.message);
            // Don't fail initialization for optional models
          }
        }
      }

      // Step 4: Start health monitoring
      this.startHealthMonitoring();

      console.log('[Ollama] Ollama manager initialized successfully');
      this.healthy = true;
    } catch (error) {
      console.error('[Ollama] Initialization failed:', error.message);
      this.healthy = false;
      throw error;
    }
  }

  /**
   * Check Ollama health
   */
  async checkHealth() {
    return new Promise((resolve) => {
      const options = {
        hostname: new URL(this.endpoint).hostname,
        port: new URL(this.endpoint).port || 11434,
        path: '/api/tags',
        method: 'GET',
        timeout: 5000
      };

      const req = http.request(options, (res) => {
        resolve(res.statusCode === 200);
      });

      req.on('error', () => resolve(false));
      req.on('timeout', () => {
        req.destroy();
        resolve(false);
      });

      req.end();
    });
  }

  /**
   * Pull required models from Ollama registry
   */
  async pullModels() {
    console.log('[Ollama] Pulling required models...');

    for (const model of this.models) {
      try {
        await this.pullModel(model);
        console.log(`[Ollama] Successfully pulled ${model}`);
      } catch (error) {
        console.warn(`[Ollama] Failed to pull ${model}: ${error.message}`);
        // Don't fail initialization if one model fails
      }
    }
  }

  /**
   * Pull a single model
   */
  async pullModel(modelName) {
    return new Promise((resolve, reject) => {
      const options = {
        hostname: new URL(this.endpoint).hostname,
        port: new URL(this.endpoint).port || 11434,
        path: '/api/pull',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        timeout: 600000 // 10 minute timeout for large models
      };

      const req = http.request(options, (res) => {
        let data = '';
        res.on('data', (chunk) => {
          data += chunk;
          // Parse streaming JSON responses
          const lines = data.split('\n').filter(l => l.trim());
          const lastLine = lines[lines.length - 1];
          if (lastLine) {
            try {
              const parsed = JSON.parse(lastLine);
              if (parsed.status === 'success') {
                resolve();
              }
            } catch (e) {
              // Invalid JSON, continue
            }
          }
        });
        res.on('end', () => {
          if (res.statusCode === 200) {
            resolve();
          } else {
            reject(new Error(`Failed to pull model: HTTP ${res.statusCode}`));
          }
        });
      });

      req.on('error', reject);
      req.on('timeout', () => {
        req.destroy();
        reject(new Error('Pull request timed out'));
      });

      req.write(JSON.stringify({ name: modelName }));
      req.end();
    });
  }

  /**
   * Perform inference on Ollama
   */
  async infer(prompt, options = {}) {
    // Wait if at max concurrent requests
    while (this.activeRequests >= this.maxConcurrent) {
      await new Promise(resolve => setTimeout(resolve, 100));
    }

    this.activeRequests++;

    try {
      const model = options.model || this.models[0];
      const context = options.context || {};

      // Build system prompt with context
      let systemPrompt = 'You are a helpful AI assistant.';
      if (context.SOUL) {
        systemPrompt += '\n\n[System Context Injected - Identity Known Locally]';
      }

      const payload = {
        model,
        prompt: typeof prompt === 'string' ? prompt : prompt.text,
        system: systemPrompt,
        stream: options.stream || false,
        temperature: options.temperature || 0.7,
        top_k: options.top_k || 40,
        top_p: options.top_p || 0.9
      };

      return await this.makeRequest('/api/generate', 'POST', payload, {
        timeout: this.config.timeout || 180000
      });
    } finally {
      this.activeRequests--;
    }
  }

  /**
   * Make HTTP request to Ollama API
   */
  makeRequest(path, method, body = null, options = {}) {
    return new Promise((resolve, reject) => {
      const url = new URL(this.endpoint);
      const reqOptions = {
        hostname: url.hostname,
        port: url.port,
        path,
        method,
        headers: {
          'Content-Type': 'application/json'
        },
        timeout: options.timeout || 30000
      };

      const req = http.request(reqOptions, (res) => {
        let data = '';

        res.on('data', (chunk) => {
          data += chunk;
        });

        res.on('end', () => {
          if (res.statusCode >= 200 && res.statusCode < 300) {
            try {
              const parsed = JSON.parse(data);
              resolve(parsed);
            } catch (e) {
              resolve(data); // Return raw if not JSON
            }
          } else {
            reject(new Error(`HTTP ${res.statusCode}: ${data}`));
          }
        });
      });

      req.on('error', reject);
      req.on('timeout', () => {
        req.destroy();
        reject(new Error('Request timeout'));
      });

      if (body) {
        req.write(JSON.stringify(body));
      }

      req.end();
    });
  }

  /**
   * Start periodic health monitoring
   */
  startHealthMonitoring() {
    this.healthCheckInterval = setInterval(async () => {
      this.healthy = await this.checkHealth();
      if (!this.healthy) {
        console.warn('[Ollama] Health check failed - Ollama may be unavailable');
      }
    }, this.config.healthCheckInterval || 300000);
  }

  /**
   * Is Ollama currently healthy?
   */
  async isHealthy() {
    return this.healthy;
  }

  /**
   * Reconfigure Ollama manager
   */
  async reconfigure(newConfig) {
    console.log('[Ollama] Reconfiguring...');
    this.config = newConfig || {};
    this.endpoint = this.config.endpoint || this.endpoint;
    this.models = this.config.models || this.models;
    this.maxConcurrent = this.config.maxConcurrentRequests || this.maxConcurrent;
  }

  /**
   * Health check endpoint
   */
  healthCheck() {
    return {
      healthy: this.healthy,
      endpoint: this.endpoint,
      models: this.models,
      activeRequests: this.activeRequests,
      maxConcurrent: this.maxConcurrent
    };
  }

  /**
   * Graceful shutdown
   */
  async shutdown() {
    console.log('[Ollama] Shutting down...');

    if (this.healthCheckInterval) {
      clearInterval(this.healthCheckInterval);
    }

    // Wait for active requests to complete
    let attempts = 0;
    while (this.activeRequests > 0 && attempts < 30) {
      await new Promise(resolve => setTimeout(resolve, 100));
      attempts++;
    }

    if (this.activeRequests > 0) {
      console.warn('[Ollama] Shutdown with ' + this.activeRequests + ' active requests');
    }

    console.log('[Ollama] Shutdown complete');
  }
}

module.exports = OllamaManager;
