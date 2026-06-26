/**
 * TurboQuant Client - Uses persistent Python server for fast compression
 * 
 * Usage:
 *   // Start server (run once)
 *   const client = new TurboQuantClient();
 *   await client.start();
 *   
 *   // Compress (fast after warmup)
 *   const compressed = await client.compress(embedding);
 *   
 *   // Search
 *   const score = await client.similarity(query, compressed);
 *   
 *   // Stop when done
 *   await client.stop();
 */

import { spawn, ChildProcess } from 'child_process';
import * as path from 'path';

export class TurboQuantClient {
  private process: ChildProcess | null = null;
  private pending: Map<string, { resolve: Function; reject: Function }> = new Map();
  private buffer: string = '';
  private ready: Promise<void> | null = null;
  
  constructor(private pythonPath: string = 'python3') {}
  
  /**
   * Start the Python server (run once at startup)
   */
  async start(): Promise<void> {
    if (this.process) return;
    
    const serverPath = path.join(__dirname, 'turboquant-server.py');
    
    this.process = spawn(this.pythonPath, [serverPath], {
      stdio: ['pipe', 'pipe', 'pipe'],
    });
    
    this.process.stdout?.on('data', (data: Buffer) => {
      this.buffer += data.toString();
      this.processBuffer();
    });
    
    this.process.stderr?.on('data', (data: Buffer) => {
      console.error('TurboQuant stderr:', data.toString());
    });
    
    this.process.on('close', (code) => {
      console.log('TurboQuant server closed:', code);
      this.process = null;
    });
    
    // Wait for ready signal
    this.ready = new Promise((resolve, reject) => {
      const timeout = setTimeout(() => reject(new Error('TurboQuant startup timeout')), 30000);
      this.pending.set('ready', {
        resolve: () => { clearTimeout(timeout); resolve(); },
        reject,
      });
    });
    
    return this.ready;
  }
  
  /**
   * Stop the Python server
   */
  async stop(): Promise<void> {
    if (this.process) {
      this.process.kill();
      this.process = null;
    }
  }
  
  /**
   * Compress an embedding
   */
  async compress(embedding: number[], bits: number = 3): Promise<Buffer> {
    await this.ready;
    
    const id = Math.random().toString(36).slice(2);
    const result = new Promise<Buffer>((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.process?.stdin?.write(JSON.stringify({
        cmd: 'compress',
        id,
        e: embedding,
        b: bits,
      }) + '\n');
    });
    
    const response = await Promise.race([
      result,
      new Promise<Buffer>((_, reject) => 
        setTimeout(() => reject(new Error('Compress timeout')), 10000)
      ),
    ]);
    
    return response;
  }
  
  /**
   * Compute similarity
   */
  async similarity(query: number[], compressed: Buffer): Promise<number> {
    await this.ready;
    
    const id = Math.random().toString(36).slice(2);
    
    // Parse compressed buffer
    const dim = compressed.readUInt32LE(0);
    const bits = compressed.readUInt8(4);
    const norm = compressed.readDoubleLE(5);
    const indicesLen = Math.ceil(dim * bits / 8);
    const signsLen = Math.ceil(dim / 8);
    
    const indices = compressed.subarray(13, 13 + indicesLen).toString('base64');
    const signs = compressed.subarray(13 + indicesLen, 13 + indicesLen + signsLen).toString('base64');
    
    const result = new Promise<number>((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.process?.stdin?.write(JSON.stringify({
        cmd: 'similarity',
        id,
        q: query,
        c: { i: indices, s: signs, r: norm, d: dim, b: bits },
      }) + '\n');
    });
    
    return Promise.race([
      result,
      new Promise<number>((_, reject) =>
        setTimeout(() => reject(new Error('Similarity timeout')), 10000)
      ),
    ]);
  }
  
  /**
   * Ping the server
   */
  async ping(): Promise<boolean> {
    await this.ready;
    
    const result = new Promise<boolean>((resolve, reject) => {
      this.pending.set('ping', { resolve: () => resolve(true), reject });
      this.process?.stdin?.write(JSON.stringify({ cmd: 'ping' }) + '\n');
    });
    
    return Promise.race([
      result,
      new Promise<boolean>((_, reject) =>
        setTimeout(() => reject(new Error('Ping timeout')), 5000)
      ),
    ]);
  }
  
  private processBuffer(): void {
    const lines = this.buffer.split('\n');
    this.buffer = lines.pop() || '';
    
    for (const line of lines) {
      if (!line.trim()) continue;
      
      try {
        const data = JSON.parse(line);
        
        if (data.status === 'ready') {
          const pending = this.pending.get('ready');
          if (pending) {
            this.pending.delete('ready');
            pending.resolve();
          }
        } else if (data.id) {
          const pending = this.pending.get(data.id);
          if (pending) {
            this.pending.delete(data.id);
            if (data.error) {
              pending.reject(new Error(data.error));
            } else {
              // Convert to Buffer for compress
              if (data.cmd === 'compressed') {
                const buf = this.encodeCompressed(data);
                pending.resolve(buf);
              } else if (data.cmd === 'score') {
                pending.resolve(data.s);
              }
            }
          }
        }
      } catch (e) {
        console.error('TurboQuant parse error:', e);
      }
    }
  }
  
  private encodeCompressed(data: any): Buffer {
    const indices = Buffer.from(data.i, 'base64');
    const signs = Buffer.from(data.s, 'base64');
    const buf = Buffer.alloc(13 + indices.length + signs.length);
    
    buf.writeUInt32LE(data.d, 0);
    buf.writeUInt8(data.b, 4);
    buf.writeDoubleLE(data.r, 5);
    indices.copy(buf, 13);
    signs.copy(buf, 13 + indices.length);
    
    return buf;
  }
}

// Singleton for application use
let _client: TurboQuantClient | null = null;

export function getClient(): TurboQuantClient {
  if (!_client) {
    _client = new TurboQuantClient();
  }
  return _client;
}

export async function compress(embedding: number[], bits: number = 3): Promise<Buffer> {
  const client = getClient();
  if (!client['process']) {
    await client.start();
  }
  return client.compress(embedding, bits);
}

export async function similarity(query: number[], compressed: Buffer): Promise<number> {
  const client = getClient();
  if (!client['process']) {
    await client.start();
  }
  return client.similarity(query, compressed);
}