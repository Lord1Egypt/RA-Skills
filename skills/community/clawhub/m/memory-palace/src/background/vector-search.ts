/**
 * Local Vector Search Provider
 * 
 * Provides vector similarity search using a local Python service with BGE-small-zh-v1.5 model.
 * Falls back to text-based search when the vector service is unavailable.
 */

import { spawn, ChildProcess } from 'child_process';
import * as http from 'http';
import * as path from 'path';
import { fileURLToPath } from 'url';
import type { VectorSearchProvider, VectorSearchResult } from '../types.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * Configuration for LocalVectorSearchProvider
 */
export interface LocalVectorSearchConfig {
  /** Host for the vector service (default: 127.0.0.1) */
  host?: string;
  /** Port for the vector service (default: 8765) */
  port?: number;
  /** Path to the Python vector service script */
  scriptPath?: string;
  /** Path to store vector database */
  dbPath?: string;
  /** BGE model to use (default: BAAI/bge-small-zh-v1.5) */
  model?: string;
  /** Auto-start the service if not running (default: true) */
  autoStart?: boolean;
  /** Timeout for HTTP requests in ms (default: 30000) */
  timeout?: number;
}

/**
 * Response from the vector service
 */
interface ServiceResponse<T> {
  status?: string;
  error?: string;
  results?: T[];
  embeddings?: number[][];
}

/**
 * Local Vector Search Provider
 * 
 * Implements VectorSearchProvider using a local Python service with BGE embeddings.
 * Provides semantic search capabilities for the Memory Palace system.
 */
export class LocalVectorSearchProvider implements VectorSearchProvider {
  private host: string;
  private port: number;
  private scriptPath: string;
  private dbPath: string;
  private model: string;
  private autoStart: boolean;
  private timeout: number;
  private serviceProcess: ChildProcess | null = null;
  private isRunning: boolean = false;
  private startupPromise: Promise<void> | null = null;

  constructor(config: LocalVectorSearchConfig = {}) {
    this.host = config.host || '127.0.0.1';
    this.port = config.port || 8765;
    this.scriptPath = config.scriptPath || path.join(__dirname, '../../scripts/vector-service.py');
    this.dbPath = config.dbPath || '/data/agent-memory-palace/data/vectors.db';
    this.model = config.model || 'BAAI/bge-small-zh-v1.5';
    this.autoStart = config.autoStart !== false;
    this.timeout = config.timeout || 30000;
  }

  /**
   * Check if the vector service is healthy
   */
  async isHealthy(): Promise<boolean> {
    return new Promise((resolve) => {
      const req = http.request(
        {
          hostname: this.host,
          port: this.port,
          path: '/health',
          method: 'GET',
          timeout: 5000,
        },
        (res) => {
          let data = '';
          res.on('data', (chunk) => (data += chunk));
          res.on('end', () => {
            try {
              const json = JSON.parse(data);
              resolve(json.status === 'ok');
            } catch {
              resolve(false);
            }
          });
        }
      );
      req.on('error', () => resolve(false));
      req.on('timeout', () => {
        req.destroy();
        resolve(false);
      });
      req.end();
    });
  }

  /**
   * Start the vector service
   */
  async start(): Promise<void> {
    if (this.isRunning) {
      return;
    }

    // Check if already running
    if (await this.isHealthy()) {
      this.isRunning = true;
      return;
    }

    // Start the Python service
    return new Promise((resolve, reject) => {
      const env: Record<string, string> = {
        ...process.env,
        VECTOR_DB_PATH: this.dbPath,
        BGE_MODEL: this.model,
      };

      this.serviceProcess = spawn('python3', [this.scriptPath, '--host', this.host, '--port', String(this.port)], {
        env,
        stdio: ['ignore', 'pipe', 'pipe'],
      });

      this.serviceProcess.on('error', (err) => {
        console.error('Failed to start vector service:', err);
        reject(err);
      });

      // Wait for service to be ready
      let output = '';
      const checkReady = (data: Buffer) => {
        output += data.toString();
        if (output.includes('Vector service running') || output.includes('Model loaded')) {
          // Give it a moment to fully initialize
          setTimeout(async () => {
            if (await this.isHealthy()) {
              this.isRunning = true;
              resolve();
            } else {
              reject(new Error('Service started but health check failed'));
            }
          }, 1000);
        }
      };

      this.serviceProcess.stdout?.on('data', checkReady);
      this.serviceProcess.stderr?.on('data', checkReady);

      // Timeout for startup
      setTimeout(() => {
        if (!this.isRunning) {
          reject(new Error('Vector service startup timeout'));
        }
      }, 60000);
    });
  }

  /**
   * Stop the vector service
   */
  async stop(): Promise<void> {
    if (this.serviceProcess) {
      this.serviceProcess.kill();
      this.serviceProcess = null;
      this.isRunning = false;
    }
  }

  /**
   * Make an HTTP request to the vector service
   */
  private async request<T>(
    endpoint: string,
    data: Record<string, unknown>,
    timeout?: number
  ): Promise<ServiceResponse<T>> {
    return new Promise((resolve, reject) => {
      const body = JSON.stringify(data);
      const req = http.request(
        {
          hostname: this.host,
          port: this.port,
          path: endpoint,
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(body),
          },
          timeout: timeout || this.timeout,
        },
        (res) => {
          let responseData = '';
          res.on('data', (chunk) => (responseData += chunk));
          res.on('end', () => {
            try {
              resolve(JSON.parse(responseData));
            } catch (e) {
              reject(new Error(`Invalid JSON response: ${responseData}`));
            }
          });
        }
      );

      req.on('error', reject);
      req.on('timeout', () => {
        req.destroy();
        reject(new Error('Request timeout'));
      });

      req.write(body);
      req.end();
    });
  }

  /**
   * Ensure the service is running
   */
  private async ensureRunning(): Promise<void> {
    if (this.isRunning) {
      return;
    }

    if (await this.isHealthy()) {
      this.isRunning = true;
      return;
    }

    if (this.autoStart) {
      if (this.startupPromise) {
        return this.startupPromise;
      }
      this.startupPromise = this.start();
      try {
        await this.startupPromise;
      } finally {
        this.startupPromise = null;
      }
    } else {
      throw new Error('Vector service is not running and autoStart is disabled');
    }
  }

  /**
   * Search for similar content
   */
  async search(
    query: string,
    topK: number = 10,
    filter?: Record<string, unknown>
  ): Promise<VectorSearchResult[]> {
    await this.ensureRunning();

    const response = await this.request<{ id: string; score: number; metadata?: Record<string, unknown> }>(
      '/search',
      { query, topK, filter }
    );

    if (response.error) {
      throw new Error(`Search failed: ${response.error}`);
    }

    return (response.results || []).map((r) => ({
      id: r.id,
      score: r.score,
      metadata: r.metadata,
    }));
  }

  /**
   * Index a document
   */
  async index(
    id: string,
    content: string,
    metadata?: Record<string, unknown>
  ): Promise<void> {
    await this.ensureRunning();

    const response = await this.request('/index', { id, content, metadata });

    if (response.error) {
      throw new Error(`Index failed: ${response.error}`);
    }
  }

  /**
   * Remove a document from the index
   */
  async remove(id: string): Promise<void> {
    await this.ensureRunning();

    const response = await this.request('/remove', { id });

    if (response.error) {
      throw new Error(`Remove failed: ${response.error}`);
    }
  }

  /**
   * Encode texts to vectors (useful for custom similarity calculations)
   */
  async encode(texts: string[]): Promise<number[][]> {
    await this.ensureRunning();

    const response = await this.request<number[]>('/encode', { texts });

    if (response.error) {
      throw new Error(`Encode failed: ${response.error}`);
    }

    return response.embeddings || [];
  }
}

/**
 * Create a LocalVectorSearchProvider with default configuration
 */
export function createLocalVectorSearch(config?: LocalVectorSearchConfig): LocalVectorSearchProvider {
  return new LocalVectorSearchProvider(config);
}