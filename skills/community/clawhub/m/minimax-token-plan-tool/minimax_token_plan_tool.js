#!/usr/bin/env node

/**
 * MiniMax Token Plan Tool - Search, Image Understanding & Usage Query
 *
 * Provides three tools:
 * - minimax_web_search: Web search using MiniMax Token Plan API
 * - minimax_understand_image: Image understanding using MiniMax VLM API
 * - minimax_token_plan_remains: Query remaining Token Plan usage
 *
 * IMPORTANT: This tool requires a special Token Plan API Key.
 * Regular MiniMax API keys will NOT work.
 */

const http = require('http');
const https = require('https');
const dns = require('dns').promises;
const fs = require('fs');
const net = require('net');
const path = require('path');
const { URL } = require('url');

// Get API key from environment
const API_KEY = process.env.MINIMAX_API_KEY;

// Get API host from environment. Only MiniMax official API hosts are allowed.
const ALLOWED_API_HOSTS = new Set([
  'https://api.minimaxi.com',
  'https://api.minimax.io'
]);
const DEFAULT_API_HOST = 'https://api.minimaxi.com';
const ALLOWED_REMOTE_IMAGE_PORTS = new Set(['', '80', '443']);
const MAX_REMOTE_IMAGE_BYTES = 10 * 1024 * 1024;
let API_HOST;


if (!API_KEY) {
  console.log(JSON.stringify({
    success: false,
    error: 'Missing required environment variable: MINIMAX_API_KEY. Note: You need a Token Plan API Key, not a regular MiniMax API key'
  }, null, 2));
  process.exit(1);
}

function resolveOrigin(origin) {
  return String(origin).trim().replace(/\/+$/, '');
}

function resolveApiHost(origin) {
  const resolved = resolveOrigin(origin || DEFAULT_API_HOST);
  if (!ALLOWED_API_HOSTS.has(resolved)) {
    throw new Error(`Unsupported MINIMAX_API_HOST: ${resolved}. Allowed values: ${Array.from(ALLOWED_API_HOSTS).join(', ')}`);
  }
  return resolved;
}

function getRemainsEndpoint() {
  return new URL('/v1/api/openplatform/coding_plan/remains', `${API_HOST}/`).toString();
}

const MIME_TYPES = {
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.png': 'image/png',
  '.gif': 'image/gif',
  '.webp': 'image/webp'
};

/**
 * Make request to MiniMax API
 */
function makeRequest(endpoint, options = {}) {
  return new Promise((resolve, reject) => {
    const {
      method = 'POST',
      data,
      headers = {}
    } = options;
    const url = new URL(endpoint, resolveOrigin(API_HOST));
    const payload = data === undefined ? null : JSON.stringify(data);

    const requestOptions = {
      hostname: url.hostname,
      port: url.port || undefined,
      path: `${url.pathname}${url.search}`,
      method,
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'MM-API-Source': 'Minimax-MCP',
        ...headers
      }
    };
    if (payload) {
      requestOptions.headers['Content-Type'] = requestOptions.headers['Content-Type'] || 'application/json';
      requestOptions.headers['Content-Length'] = Buffer.byteLength(payload);
    }

    const req = https.request(requestOptions, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          if (!body) {
            resolve({});
            return;
          }
          const json = JSON.parse(body);
          resolve(json);
        } catch (e) {
          if (res.statusCode && res.statusCode >= 200 && res.statusCode < 300) {
            resolve({ raw: body });
            return;
          }
          reject(new Error(`Failed to parse response: ${body}`));
        }
      });
    });

    req.on('error', reject);
    if (payload) {
      req.write(payload);
    }
    req.end();
  });
}

function getApiError(response) {
  if (!response || !response.base_resp) {
    return null;
  }
  if (response.base_resp.status_code === 0) {
    return null;
  }
  return response.base_resp.status_msg || `API error: ${response.base_resp.status_code}`;
}

function toErrorResult(message) {
  return {
    success: false,
    error: String(message || 'Unknown error')
  };
}

function toUtcIsoString(value) {
  if (typeof value !== 'number' || !Number.isFinite(value)) {
    return null;
  }
  return new Date(value).toISOString();
}

function millisecondsToDayTimeString(value) {
  if (typeof value !== 'number' || !Number.isFinite(value)) {
    return null;
  }
  const totalSeconds = Math.max(0, Math.floor(value / 1000));
  const days = Math.floor(totalSeconds / 86400);
  const hours = Math.floor((totalSeconds % 86400) / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;

  return [
    String(days).padStart(2, '0'),
    String(hours).padStart(2, '0'),
    String(minutes).padStart(2, '0'),
    String(seconds).padStart(2, '0')
  ].join(':');
}

function formatWebSearchResults(response) {
  if (!response || !Array.isArray(response.organic)) {
    return [];
  }
  return response.organic.map(item => ({
    title: item.title || '',
    link: item.link || item.url || '',
    snippet: item.snippet || item.content || '',
    date: item.date || ''
  }));
}

function formatRemainsResponse(response) {
  if (!response || !Array.isArray(response.model_remains)) {
    return [];
  }
  return response.model_remains.map(item => ({
    model_name: item.model_name || '',
    period_start_time: toUtcIsoString(item.start_time),
    period_end_time: toUtcIsoString(item.end_time),
    remains_time: millisecondsToDayTimeString(item.remains_time),
    period_quota: item.current_interval_total_count ?? 0,
    period_remaining: item.current_interval_usage_count ?? 0,
    weekly_quota: item.current_weekly_total_count ?? 0,
    weekly_remaining: item.current_weekly_usage_count ?? 0,
    weekly_start_time: toUtcIsoString(item.weekly_start_time),
    weekly_end_time: toUtcIsoString(item.weekly_end_time),
    weekly_remains_time: millisecondsToDayTimeString(item.weekly_remains_time)
  }));
}

/**
 * Normalize a MIME type value from headers.
 */
function normalizeMimeType(value) {
  return String(value || '').split(';')[0].trim().toLowerCase();
}

function getMimeTypeFromPath(filePath) {
  return MIME_TYPES[path.extname(filePath).toLowerCase()] || null;
}

function isBlockedHostname(hostname) {
  const normalized = String(hostname || '').trim().toLowerCase();
  return normalized === 'localhost' || normalized.endsWith('.localhost');
}

function isPrivateIPv4(ip) {
  const parts = ip.split('.').map(Number);
  if (parts.length !== 4 || parts.some(Number.isNaN)) {
    return true;
  }
  const [a, b] = parts;
  if (a === 0 || a === 10 || a === 127) {
    return true;
  }
  if (a === 100 && b >= 64 && b <= 127) {
    return true;
  }
  if (a === 169 && b === 254) {
    return true;
  }
  if (a === 172 && b >= 16 && b <= 31) {
    return true;
  }
  if (a === 192 && b === 168) {
    return true;
  }
  if (a === 198 && (b === 18 || b === 19)) {
    return true;
  }
  if (a >= 224) {
    return true;
  }
  return false;
}

function isPrivateIPv6(ip) {
  const normalized = ip.toLowerCase();
  return (
    normalized === '::' ||
    normalized === '::1' ||
    normalized.startsWith('fc') ||
    normalized.startsWith('fd') ||
    normalized.startsWith('fe8') ||
    normalized.startsWith('fe9') ||
    normalized.startsWith('fea') ||
    normalized.startsWith('feb') ||
    normalized.startsWith('fec') ||
    normalized.startsWith('fed') ||
    normalized.startsWith('fee') ||
    normalized.startsWith('fef') ||
    normalized.startsWith('ff')
  );
}

function isBlockedIpAddress(ip) {
  const family = net.isIP(ip);
  if (family === 4) {
    return isPrivateIPv4(ip);
  }
  if (family === 6) {
    return isPrivateIPv6(ip);
  }
  return true;
}

async function validateRemoteImageUrl(imageUrl) {
  const url = new URL(imageUrl);
  if (url.protocol !== 'http:' && url.protocol !== 'https:') {
    throw new Error(`Unsupported remote image protocol: ${url.protocol}`);
  }
  if (!ALLOWED_REMOTE_IMAGE_PORTS.has(url.port)) {
    throw new Error(`Unsupported remote image port: ${url.port}`);
  }
  if (url.username || url.password) {
    throw new Error('Remote image URL must not include credentials');
  }
  if (isBlockedHostname(url.hostname)) {
    throw new Error(`Blocked remote image hostname: ${url.hostname}`);
  }

  const records = await dns.lookup(url.hostname, { all: true, verbatim: true });
  if (!records.length) {
    throw new Error(`Unable to resolve remote image hostname: ${url.hostname}`);
  }
  for (const record of records) {
    if (isBlockedIpAddress(record.address)) {
      throw new Error(`Blocked remote image address: ${record.address}`);
    }
  }

  return url;
}

async function fetchRemoteImageAsDataUrl(imageUrl, redirectCount = 0) {
  if (redirectCount > 5) {
    throw new Error('Too many redirects while fetching remote image');
  }

  const url = await validateRemoteImageUrl(imageUrl);
  return new Promise((resolve, reject) => {
    const client = url.protocol === 'http:' ? http : https;
    const req = client.request(url, {
      method: 'GET',
      timeout: 15000,
      headers: {
        'User-Agent': 'MiniMax-Token-Plan-Tool/1.0'
      }
    }, (res) => {
      const statusCode = res.statusCode || 0;
      if (statusCode >= 300 && statusCode < 400 && res.headers.location) {
        const redirectedUrl = new URL(res.headers.location, imageUrl).toString();
        res.resume();
        resolve(fetchRemoteImageAsDataUrl(redirectedUrl, redirectCount + 1));
        return;
      }

      if (statusCode < 200 || statusCode >= 300) {
        res.resume();
        reject(new Error(`Failed to fetch remote image: HTTP ${statusCode}`));
        return;
      }

      const mimeType = normalizeMimeType(res.headers['content-type']) || getMimeTypeFromPath(url.pathname);
      if (!mimeType || !mimeType.startsWith('image/')) {
        res.resume();
        reject(new Error(`Remote URL did not return a supported image content type: ${mimeType || 'unknown'}`));
        return;
      }

      const chunks = [];
      let totalBytes = 0;
      res.on('data', chunk => {
        totalBytes += chunk.length;
        if (totalBytes > MAX_REMOTE_IMAGE_BYTES) {
          req.destroy(new Error(`Remote image exceeds ${MAX_REMOTE_IMAGE_BYTES} bytes`));
          return;
        }
        chunks.push(chunk);
      });
      res.on('end', () => {
        const buffer = Buffer.concat(chunks);
        resolve(`data:${mimeType};base64,${buffer.toString('base64')}`);
      });
    });

    req.on('timeout', () => {
      req.destroy(new Error('Timed out while fetching remote image'));
    });
    req.on('error', reject);
    req.end();
  });
}

/**
 * Process image source and convert it to a data URL.
 */
async function processImageSource(imageSource) {
  // Download remote images so the upstream API receives a stable data URL.
  if (imageSource.startsWith('http://') || imageSource.startsWith('https://')) {
    return fetchRemoteImageAsDataUrl(imageSource);
  }

  // It's a local file - convert to base64
  // Strip @ prefix if present
  let filePath = imageSource.startsWith('@') ? imageSource.slice(1) : imageSource;

  if (!fs.existsSync(filePath)) {
    throw new Error(`File not found: ${filePath}`);
  }

  const mimeType = getMimeTypeFromPath(filePath);
  if (!mimeType) {
    const ext = path.extname(filePath).toLowerCase();
    throw new Error(`Unsupported image type: ${ext || '(no extension)'}. Supported types: .jpg, .jpeg, .png, .gif, .webp`);
  }
  const fileContent = fs.readFileSync(filePath);
  const base64 = fileContent.toString('base64');

  return `data:${mimeType};base64,${base64}`;
}

/**
 * Web Search Tool using Token Plan API
 *
 * Uses MiniMax's token plan search endpoint for real-time web search.
 * The backend endpoint path remains /coding_plan/.
 */
async function webSearch(query) {
  if (!query || typeof query !== 'string') {
    return toErrorResult('Missing required parameter: query');
  }

  try {
    // Use MiniMax Token Plan search API
    const response = await makeRequest('/v1/coding_plan/search', {
      data: {
        q: query
      }
    });
    const apiError = getApiError(response);
    if (apiError) {
      return toErrorResult(apiError);
    }

    return {
      success: true,
      results: formatWebSearchResults(response)
    };
  } catch (error) {
    return toErrorResult(error.message);
  }
}

/**
 * Understand Image Tool using Token Plan VLM API
 *
 * Uses MiniMax's vision model to analyze images.
 * The backend endpoint path remains /coding_plan/.
 */
async function understandImage(imageSource, prompt) {
  if (!prompt || typeof prompt !== 'string') {
    return toErrorResult('Missing required parameter: prompt');
  }

  if (!imageSource || typeof imageSource !== 'string') {
    return toErrorResult('Missing required parameter: image_source');
  }

  try {
    // Convert local files or remote URLs into data URLs before upload.
    const processedImageUrl = await processImageSource(imageSource);

    // Use MiniMax Token Plan VLM API
    const response = await makeRequest('/v1/coding_plan/vlm', {
      data: {
        prompt: prompt,
        image_url: processedImageUrl
      }
    });
    const apiError = getApiError(response);
    if (apiError) {
      return toErrorResult(apiError);
    }

    // Extract content from response
    const content = response.content;

    if (!content) {
      return toErrorResult('No content returned from VLM API');
    }

    return {
      success: true,
      caption: content
    };
  } catch (error) {
    return toErrorResult(error.message);
  }
}

/**
 * Query remaining Token Plan usage
 *
 * Uses MiniMax's open platform remains endpoint.
 */
async function getTokenPlanRemains() {
  try {
    const response = await makeRequest(getRemainsEndpoint(), {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    const apiError = getApiError(response);
    if (apiError) {
      return toErrorResult(apiError);
    }

    return {
      success: true,
      remains: formatRemainsResponse(response)
    };
  } catch (error) {
    return toErrorResult(error.message);
  }
}

// CLI interface
const args = process.argv.slice(2);
const command = args[0];

async function main() {
  try {
    API_HOST = resolveApiHost(process.env.MINIMAX_API_HOST);

    if (command === 'web_search') {
      const query = args[1];
      const result = await webSearch(query);
      console.log(JSON.stringify(result, null, 2));
    } else if (command === 'understand_image') {
      const imageSource = args[1];
      const prompt = args.slice(2).join(' ') || 'Describe this image';
      const result = await understandImage(imageSource, prompt);
      console.log(JSON.stringify(result, null, 2));
    } else if (command === 'remains') {
      const result = await getTokenPlanRemains();
      console.log(JSON.stringify(result, null, 2));
    } else if (command === 'tools') {
      // Return available tools in OpenClaw skill format
      console.log(JSON.stringify({
        tools: [
          {
            name: 'minimax_web_search',
            description: 'Web search using MiniMax Token Plan API - search real-time or external information',
            inputSchema: {
              type: 'object',
              properties: {
                query: {
                  type: 'string',
                  description: 'Search query. 3-5 keywords work best'
                }
              },
              required: ['query']
            }
          },
          {
            name: 'minimax_understand_image',
            description: 'Image understanding using MiniMax Token Plan VLM API',
            inputSchema: {
              type: 'object',
              properties: {
                image_source: {
                  type: 'string',
                  description: 'Image source - supports HTTP/HTTPS URL or local file path (strip @ prefix)'
                },
                prompt: {
                  type: 'string',
                  description: 'Question or analysis request for the image'
                }
              },
              required: ['image_source', 'prompt']
            }
          },
          {
            name: 'minimax_token_plan_remains',
            description: 'Query remaining MiniMax Token Plan usage and quota information',
            inputSchema: {
              type: 'object',
              properties: {},
              additionalProperties: false
            }
          }
        ]
      }, null, 2));
    } else {
      console.error('Usage:');
      console.error('  minimax-token-plan-mcp web_search <query>');
      console.error('  minimax-token-plan-mcp understand_image <image_source> <prompt>');
      console.error('  minimax-token-plan-mcp remains');
      console.error('  minimax-token-plan-mcp tools');
      process.exit(1);
    }
  } catch (error) {
    console.log(JSON.stringify(toErrorResult(error.message), null, 2));
    process.exit(1);
  }
}

main().catch(err => {
  console.log(JSON.stringify(toErrorResult(err && err.message ? err.message : err), null, 2));
  process.exit(1);
});
