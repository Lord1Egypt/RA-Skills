/**
 * LeanContext Integration for OpenClaw
 * 
 * Automatically compresses tool outputs to reduce token usage.
 * Hooks into OpenClaw's tool execution pipeline.
 */

import { createHash } from 'crypto';
import { statSync, readFileSync } from 'fs';

// Configuration
interface LeanCtxConfig {
  enabled: boolean;
  threshold: number;
  cacheEnabled: boolean;
  excludedPaths: string[];
  excludedCommands: string[];
}

const config: LeanCtxConfig = {
  enabled: true,
  threshold: 100,
  cacheEnabled: true,
  excludedPaths: ['node_modules', '.git', 'dist', 'build', '.svelte-kit'],
  excludedCommands: ['cat', 'echo', 'head', 'tail']
};

// Cache
interface CacheEntry {
  hash: string;
  compressed: string;
  mtime: number;
  size: number;
}

const cache = new Map<string, CacheEntry>();
let metrics = {
  readCalls: 0,
  execCalls: 0,
  tokensSaved: 0,
  cacheHits: 0,
  totalCompression: 0
};

// Load config from OpenClaw
function loadConfig(): void {
  try {
    // In production, this would read from OpenClaw's config
    // For now, use defaults
  } catch (e) {
    // Use defaults
  }
}

// Main hook - wrap read tool
export function wrapRead(originalRead: Function): Function {
  return async function(filePath: string, options?: any) {
    if (!config.enabled) {
      return originalRead(filePath, options);
    }

    // Check exclusions
    if (config.excludedPaths.some(p => filePath.includes(p))) {
      return originalRead(filePath, options);
    }

    // Get original content
    const content = await originalRead(filePath, options);
    
    // Only compress text files
    if (typeof content !== 'string') {
      return content;
    }

    // Check if should compress
    if (!shouldCompress(filePath)) {
      return content;
    }

    metrics.readCalls++;

    // Check cache
    const hash = computeHash(content);
    const cached = cache.get(filePath);
    
    if (cached && cached.hash === hash) {
      metrics.cacheHits++;
      return cached.compressed;
    }

    // Compress
    const compressed = compressContent(content, filePath);
    
    // Update cache
    if (config.cacheEnabled) {
      cache.set(filePath, {
        hash,
        compressed,
        mtime: Date.now(),
        size: content.length
      });
    }

    // Update metrics
    const origTokens = estimateTokens(content);
    const compTokens = estimateTokens(compressed);
    metrics.tokensSaved += (origTokens - compTokens);
    metrics.totalCompression += ((origTokens - compTokens) / origTokens) * 100;

    return compressed;
  };
}

// Main hook - wrap exec tool
export function wrapExec(originalExec: Function): Function {
  return async function(command: string, ...args: any[]) {
    if (!config.enabled) {
      return originalExec(command, ...args);
    }

    // Check exclusions
    const baseCmd = command.split(' ')[0];
    if (config.excludedCommands.includes(baseCmd)) {
      return originalExec(command, ...args);
    }

    // Get original output
    const output = await originalExec(command, ...args);
    
    if (typeof output !== 'string') {
      return output;
    }

    metrics.execCalls++;

    // Compress based on command type
    const compressed = compressExecOutput(command, output);
    
    // Update metrics
    const origTokens = estimateTokens(output);
    const compTokens = estimateTokens(compressed);
    metrics.tokensSaved += (origTokens - compTokens);

    return compressed;
  };
}

// Compression functions
function shouldCompress(filePath: string): boolean {
  const exts = ['.ts', '.tsx', '.js', '.jsx', '.py', '.svelte', '.go', '.rs', '.java', '.kt'];
  return exts.some(ext => filePath.endsWith(ext));
}

function compressContent(content: string, filePath: string): string {
  const ext = filePath.slice(filePath.lastIndexOf('.'));
  
  switch (ext) {
    case '.ts':
    case '.tsx':
    case '.js':
    case '.jsx':
      return compressTypeScript(content);
    case '.py':
      return compressPython(content);
    case '.svelte':
      return compressSvelte(content);
    default:
      return compressGeneric(content);
  }
}

function compressTypeScript(content: string): string {
  // Remove comments
  let compressed = content
    .replace(/\/\*[\s\S]*?\*\//g, '')
    .replace(/\/\/.*$/gm, '')
    .replace(/^\s*\n/gm, '');

  // Simple function body collapsing
  const lines = compressed.split('\n');
  const result: string[] = [];
  let inFunction = false;
  let braceCount = 0;
  let signature = '';

  for (const line of lines) {
    const trimmed = line.trim();
    
    // Keep imports/exports
    if (trimmed.startsWith('import ') || trimmed.startsWith('export ')) {
      result.push(line);
      continue;
    }

    // Keep type definitions
    if (trimmed.startsWith('type ') || trimmed.startsWith('interface ')) {
      result.push(line);
      continue;
    }

    // Detect function
    if (/^(async\s+)?(function|const|let|var)\s+\w+.*=.*(\(|=\u003e)/.test(trimmed) ||
        /^(async\s+)?\w+\s*\([^)]*\)\s*[:{]/.test(trimmed)) {
      signature = line;
      inFunction = true;
      braceCount = (line.match(/{/g) || []).length - (line.match(/}/g) || []).length;
      
      if (braceCount <= 0) {
        result.push(line);
        inFunction = false;
      }
      continue;
    }

    if (inFunction) {
      braceCount += (line.match(/{/g) || []).length;
      braceCount -= (line.match(/}/g) || []).length;

      if (braceCount <= 0) {
        result.push(signature);
        result.push('  // ...');
        inFunction = false;
      }
    } else {
      result.push(line);
    }
  }

  return result.join('\n');
}

function compressPython(content: string): string {
  return content
    .replace(/#.*$/gm, '')
    .replace(/'''[\s\S]*?'''/g, '')
    .replace(/"""[\s\S]*?"""/g, '')
    .replace(/^\s*\n/gm, '')
    .replace(/\n{3,}/g, '\n\n');
}

function compressSvelte(content: string): string {
  // Keep structure, minimize script/style
  const scriptMatch = content.match(/&lt;script&gt;([\s\S]*?)&lt;\/script&gt;/);
  if (scriptMatch) {
    const compressed = compressTypeScript(scriptMatch[1]);
    return content.replace(scriptMatch[1], compressed);
  }
  return content;
}

function compressGeneric(content: string): string {
  return content
    .replace(/^\s*\n/gm, '')
    .replace(/\n{3,}/g, '\n\n');
}

function compressExecOutput(command: string, output: string): string {
  // Git log
  if (command.startsWith('git log')) {
    return output
      .split('\n')
      .filter(l => l.startsWith('commit ') || l.trim().startsWith('Author:') || l.trim().startsWith('Date:'))
      .slice(0, 30)
      .join('\n');
  }

  // Git status
  if (command.startsWith('git status')) {
    return output
      .split('\n')
      .filter(l => l.includes('branch') || l.includes('modified:') || l.includes('new file:') || l.includes('deleted:'))
      .join('\n');
  }

  // NPM install
  if (command.match(/npm.*install/)) {
    const match = output.match(/added (\d+) packages?/);
    return match ? `Added: ${match[1]} packages` : 'Install complete';
  }

  // Generic - limit lines
  return output.split('\n').slice(0, 100).join('\n');
}

// Utilities
function computeHash(content: string): string {
  return createHash('md5').update(content).digest('hex').slice(0, 16);
}

function estimateTokens(text: string): number {
  return Math.ceil(text.length / 4);
}

// Get metrics
export function getMetrics(): object {
  const totalCalls = metrics.readCalls + metrics.execCalls;
  return {
    ...metrics,
    avgCompression: totalCalls > 0 ? (metrics.totalCompression / totalCalls).toFixed(1) : 0,
    cacheSize: cache.size
  };
}

// Clear cache
export function clearCache(): void {
  cache.clear();
}

// Initialize
loadConfig();

// Export for OpenClaw
export default {
  wrapRead,
  wrapExec,
  getMetrics,
  clearCache
};
