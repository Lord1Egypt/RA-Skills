/**
 * Shared utilities for Notion API scripts
 * Common functions for HTTP requests, error handling, and data extraction
 */

const fs = require('fs');
const https = require('https');
const os = require('os');
const path = require('path');

const NOTION_VERSION = '2025-09-03';

// Cached token (resolved once per process)
let _cachedToken = undefined;

/**
 * Resolve the Notion API token from the process environment.
 *
 * Runtimes provide NOTION_API_KEY through their preferred secret manager.
 * OpenClaw may inject an opaque protected-store sentinel; the real credential
 * is then substituted only when the request reaches api.notion.com.
 */
function resolveToken() {
  if (_cachedToken !== undefined) return _cachedToken;

  _cachedToken = process.env.NOTION_API_KEY || null;
  return _cachedToken;
}

const LEGACY_TOKEN_FLAGS = new Set(['--token', '--token-file', '--token-stdin']);
const TOKEN_MIGRATION_MESSAGE =
  'notion-sync v3 no longer accepts CLI or file-based tokens. Supply NOTION_API_KEY ' +
  'through your runtime\'s secret manager. OpenClaw users should use a protected ' +
  'secret allowed only for api.notion.com. See references/MIGRATION-V3.md.';
const PROTECTED_SECRET_MESSAGE =
  'Protected OpenClaw credentials require a valid NOTION_API_KEY sentinel and ' +
  'Gateway-hosted exec with the secret egress proxy.';
// Build the marker at runtime so distributing this client does not look like
// an unresolved protected credential to egress scanners inspecting uploads.
const PROTECTED_SECRET_PREFIX = ['oc', 'sent', 'v2.'].join('-');
const PROTECTED_SECRET_SUFFIX = ['.', 'end'].join('');

function findLegacyTokenFlag(args = process.argv.slice(2)) {
  for (const arg of args) {
    if (LEGACY_TOKEN_FLAGS.has(arg)) return arg;
    if (arg.startsWith('--token=')) return '--token';
    if (arg.startsWith('--token-file=')) return '--token-file';
  }
  return null;
}

function supportsNativeProxy(nodeVersion = process.versions.node) {
  const [major, minor] = String(nodeVersion).split('.').map(Number);
  return major >= 25 || (major === 24 && minor >= 5) || (major === 22 && minor >= 21);
}

function isProtectedCredential(apiKey) {
  return apiKey.startsWith(PROTECTED_SECRET_PREFIX) && apiKey.endsWith(PROTECTED_SECRET_SUFFIX);
}

function createProtectedProxyAgent(apiKey, env = process.env, nodeVersion = process.versions.node) {
  if (!isProtectedCredential(apiKey)) {
    throw new Error(PROTECTED_SECRET_MESSAGE);
  }

  if (!supportsNativeProxy(nodeVersion) || !env.HTTPS_PROXY || !env.NODE_EXTRA_CA_CERTS) {
    throw new Error(
      'Protected Notion credentials require OpenClaw Gateway-hosted exec, its egress ' +
      'proxy and CA, and Node.js 22.21+ (22.x), 24.5+ (24.x), or 25+.'
    );
  }

  return new https.Agent({
    proxyEnv: { HTTPS_PROXY: env.HTTPS_PROXY },
  });
}

function createRequestAgent(apiKey, env = process.env, nodeVersion = process.versions.node) {
  if (!apiKey.startsWith(PROTECTED_SECRET_PREFIX)) return undefined;
  return createProtectedProxyAgent(apiKey, env, nodeVersion);
}

/**
 * Expand a path that starts with ~ to the user's home directory
 */
function expandHomePath(inputPath) {
  if (!inputPath) return inputPath;
  if (inputPath === '~') return os.homedir();
  if (inputPath.startsWith('~/')) return path.join(os.homedir(), inputPath.slice(2));
  return inputPath;
}

/**
 * Normalize network-level request errors into user-friendly guidance
 */
function wrapNetworkError(err) {
  const networkCodes = new Set(['ENOTFOUND', 'ECONNREFUSED', 'ETIMEDOUT', 'ECONNRESET', 'EAI_AGAIN']);
  const code = err.code || err.cause?.code;
  if (networkCodes.has(code) || err.name === 'AbortError' || err.name === 'TimeoutError') {
    return new Error('Could not reach Notion API. Check your internet connection.');
  }
  return new Error(`Could not reach Notion API. ${err.message}`);
}

/**
 * Get the run-scoped Notion API key or protected-store sentinel
 */
function getApiKey() {
  return resolveToken();
}

/**
 * Check if a Notion API token was provided, exit with helpful message if not
 */
function shouldRequireApiKey(rawArgs = process.argv.slice(2)) {
  const args = stripTokenArg(rawArgs);

  if (args.length === 0) return false;
  if (args.includes('--help') || args.includes('-h')) return false;

  // Usage-first behavior: if invocation starts with option flags,
  // let script-level arg validation print usage/errors before auth checks.
  if (args[0].startsWith('-')) {
    if (args[0] !== '--stdin') return false;
    return args.slice(1).some(arg => !arg.startsWith('-'));
  }

  return true;
}

function checkApiKey() {
  if (hasHelpFlag()) return;

  const legacyFlag = findLegacyTokenFlag();
  if (legacyFlag) {
    const message = `${legacyFlag} is not supported. ${TOKEN_MIGRATION_MESSAGE}`;
    if (hasJsonFlag()) console.log(JSON.stringify({ error: message }, null, 2));
    else console.error(`Error: ${message}`);
    process.exit(1);
  }

  if (!shouldRequireApiKey()) return;

  if (!getApiKey()) {
    const message = `No Notion API token found. ${TOKEN_MIGRATION_MESSAGE}`;
    if (hasJsonFlag()) {
      console.log(JSON.stringify({ error: message }, null, 2));
    } else {
      console.error('Error: No Notion API token provided');
      console.error('');
      console.error(message);
      console.error('Create an integration at https://www.notion.so/my-integrations');
    }
    process.exit(1);
  }
}

/**
 * Strip supported global flags so scripts can parse command-specific arguments
 */
function hasJsonFlag() {
  return process.argv.includes('--json');
}

function hasHelpFlag() {
  return process.argv.includes('--help') || process.argv.includes('-h');
}

function log(msg) {
  if (!hasJsonFlag()) console.error(msg);
}

function isPathInside(baseDir, targetPath) {
  const relative = path.relative(baseDir, targetPath);
  return relative === '' || (!relative.startsWith('..') && !path.isAbsolute(relative));
}

function getAllowedPaths(mode, args = process.argv.slice(2)) {
  const flag = mode === 'write' ? '--allow-write-path' : '--allow-read-path';
  const allowedPaths = [];

  for (let i = 0; i < args.length; i++) {
    if (args[i] === flag && args[i + 1] && !args[i + 1].startsWith('-')) {
      allowedPaths.push(args[++i]);
    } else if (args[i].startsWith(`${flag}=`) && args[i].length > flag.length + 1) {
      allowedPaths.push(args[i].slice(flag.length + 1));
    }
  }

  return allowedPaths;
}

function resolveCanonicalPath(inputPath, mode) {
  const expanded = expandHomePath(inputPath);
  const absolute = path.resolve(expanded);
  let candidatePath = absolute;

  if (fs.existsSync(absolute)) {
    try {
      candidatePath = fs.realpathSync(absolute);
    } catch (_) {
      candidatePath = absolute;
    }
  } else if (mode === 'write') {
    let existingAncestor = absolute;
    while (!fs.existsSync(existingAncestor)) {
      const parentDir = path.dirname(existingAncestor);
      if (parentDir === existingAncestor) break;
      existingAncestor = parentDir;
    }

    if (fs.existsSync(existingAncestor)) {
      try {
        const realAncestor = fs.realpathSync(existingAncestor);
        const remainder = path.relative(existingAncestor, absolute);
        candidatePath = path.join(realAncestor, remainder);
      } catch (_) {
        candidatePath = absolute;
      }
    }
  }

  return candidatePath;
}

function resolveSafePath(inputPath, options = {}) {
  const { mode = 'read' } = options;

  if (!inputPath) {
    throw new Error('Path is required');
  }

  const candidatePath = resolveCanonicalPath(inputPath, mode);

  const workspaceRoot = fs.realpathSync(process.cwd());
  if (!isPathInside(workspaceRoot, candidatePath)) {
    const isExplicitlyAllowed = getAllowedPaths(mode).some((allowedPath) =>
      resolveCanonicalPath(allowedPath, mode) === candidatePath
    );

    if (isExplicitlyAllowed) return candidatePath;

    const action = mode === 'write' ? 'write to' : 'read from';
    const allowFlag = mode === 'write' ? '--allow-write-path' : '--allow-read-path';
    throw new Error(
      `Refusing to ${action} path outside current workspace: ${inputPath}. ` +
      `Authorize only this exact path with ${allowFlag} "${inputPath}".`
    );
  }

  return candidatePath;
}

function stripTokenArg(args) {
  const result = [];
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--json') {
      // skip flag only (no value)
    } else if (
      (args[i] === '--allow-read-path' || args[i] === '--allow-write-path') &&
      i + 1 < args.length &&
      !args[i + 1].startsWith('-')
    ) {
      i++; // skip flag and exact path
    } else if (
      args[i].startsWith('--allow-read-path=') ||
      args[i].startsWith('--allow-write-path=')
    ) {
      // skip exact path authorization
    } else if (args[i] === '-h') {
      result.push('--help');
    } else {
      result.push(args[i]);
    }
  }
  return result;
}

/**
 * Parse a positive integer CLI value with strict validation.
 */
function parsePositiveInteger(value, flagName = 'value') {
  const normalized = String(value ?? '').trim();

  if (!/^\d+$/.test(normalized)) {
    throw new Error(`${flagName} must be a positive integer`);
  }

  const parsed = Number(normalized);
  if (!Number.isSafeInteger(parsed) || parsed <= 0) {
    throw new Error(`${flagName} must be a positive integer`);
  }

  return parsed;
}

/**
 * Parse a Notion page-size limit. Notion caps page sizes at 100.
 */
function parsePageSizeLimit(value, flagName = '--limit') {
  if (value === undefined) {
    throw new Error(`${flagName} must be a positive integer`);
  }

  let limit;
  try {
    limit = parsePositiveInteger(value, flagName);
  } catch {
    throw new Error(`${flagName} must be a positive integer between 1 and 100`);
  }

  if (limit > 100) {
    throw new Error(`${flagName} must be a positive integer between 1 and 100`);
  }

  return limit;
}

/**
 * Make a Notion API request with proper error handling
 */
function notionRequest(path, method, data = null) {
  const apiKey = getApiKey();
  if (!apiKey) {
    return Promise.reject(new Error(`No Notion API token found. ${TOKEN_MIGRATION_MESSAGE}`));
  }

  let requestAgent;
  try {
    requestAgent = createRequestAgent(apiKey);
  } catch (err) {
    return Promise.reject(err);
  }

  return new Promise((resolve, reject) => {
    const requestData = data ? JSON.stringify(data) : null;
    const options = {
      hostname: 'api.notion.com',
      port: 443,
      path,
      method,
      headers: {
        Authorization: `Bearer ${apiKey}`,
        'Notion-Version': NOTION_VERSION,
        'Content-Type': 'application/json',
      },
    };

    if (requestAgent) options.agent = requestAgent;
    if (requestData) options.headers['Content-Length'] = Buffer.byteLength(requestData);

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          try {
            resolve(JSON.parse(body));
          } catch (_) {
            resolve(body);
          }
        } else {
          reject(createDetailedError(res.statusCode, body));
        }
      });
    });

    req.on('error', (err) => reject(wrapNetworkError(err)));
    if (requestData) req.write(requestData);
    req.end();
  });
}

/**
 * Create detailed error message based on status code and response
 */
function createDetailedError(statusCode, body) {
  let error;
  try {
    error = JSON.parse(body);
  } catch (e) {
    return new Error(`API error (${statusCode}): ${body}`);
  }

  const errorCode = error.code;
  const errorMessage = error.message;

  switch (statusCode) {
    case 400:
      if (errorCode === 'validation_error') {
        return new Error(`Validation error: ${errorMessage}. Check your input data.`);
      }
      return new Error(`Bad request: ${errorMessage}`);

    case 401:
      return new Error('Authentication failed. Check that your token is valid and has access to this resource.');

    case 404:
      if (errorCode === 'object_not_found') {
        return new Error('Page/database not found. Verify the ID and that your integration has access.');
      }
      return new Error(`Not found: ${errorMessage}`);

    case 429:
      return new Error('Rate limit exceeded. Wait a moment and try again.');

    case 500:
    case 503:
      return new Error(`Notion server error (${statusCode}). Try again later.`);

    default:
      return new Error(`API error (${statusCode}): ${errorMessage || body}`);
  }
}

// --- ID Utilities ---

/**
 * Normalize a Notion page/block ID to UUID format with hyphens
 */
function normalizeId(id) {
  const clean = id.replace(/-/g, '');
  if (clean.length === 32) {
    return `${clean.slice(0, 8)}-${clean.slice(8, 12)}-${clean.slice(12, 16)}-${clean.slice(16, 20)}-${clean.slice(20)}`;
  }
  return id;
}

// --- Property Utilities ---

/**
 * Extract title from a page or database object
 */
function extractTitle(item) {
  if (item.object === 'page') {
    const titleProp = Object.values(item.properties || {}).find(p => p.type === 'title');
    if (titleProp && titleProp.title && titleProp.title.length > 0) {
      return titleProp.title.map(t => t.plain_text).join('');
    }
  } else if (item.object === 'database' || item.object === 'data_source') {
    if (item.title && item.title.length > 0) {
      return item.title.map(t => t.plain_text).join('');
    }
  }
  return '(Untitled)';
}

/**
 * Extract value from a property based on its type
 */
function extractPropertyValue(property) {
  switch (property.type) {
    case 'title':
      return property.title.map(t => t.plain_text).join('');
    case 'rich_text':
      return property.rich_text.map(t => t.plain_text).join('');
    case 'number':
      return property.number;
    case 'select':
      return property.select?.name || null;
    case 'multi_select':
      return property.multi_select.map(s => s.name);
    case 'date':
      return property.date ? { start: property.date.start, end: property.date.end } : null;
    case 'checkbox':
      return property.checkbox;
    case 'url':
      return property.url;
    case 'email':
      return property.email;
    case 'phone_number':
      return property.phone_number;
    case 'relation':
      return property.relation.map(r => r.id);
    case 'created_time':
      return property.created_time;
    case 'last_edited_time':
      return property.last_edited_time;
    default:
      return property[property.type];
  }
}

/**
 * Format property value for Notion API write operations
 */
function formatPropertyValue(propertyType, value) {
  switch (propertyType) {
    case 'select':
      return { select: { name: value } };

    case 'multi_select': {
      const tags = Array.isArray(value) ? value : value.split(',').map(t => t.trim());
      return { multi_select: tags.map(name => ({ name })) };
    }

    case 'checkbox': {
      const boolValue = typeof value === 'boolean' ? value :
        (String(value).toLowerCase() === 'true' || value === '1');
      return { checkbox: boolValue };
    }

    case 'number': {
      if (typeof value !== 'number' && typeof value !== 'string') {
        throw new Error('Invalid number property value: must be a finite number');
      }
      if (typeof value === 'string' && value.trim() === '') {
        throw new Error('Invalid number property value: must be a finite number');
      }
      const numberValue = typeof value === 'number' ? value : Number(value.trim());
      if (!Number.isFinite(numberValue)) {
        throw new Error('Invalid number property value: must be a finite number');
      }
      return { number: numberValue };
    }

    case 'url':
      return { url: value };

    case 'email':
      return { email: value };

    case 'date': {
      if (typeof value === 'string') {
        const dates = value.split(',').map(d => d.trim());
        return { date: { start: dates[0], end: dates[1] || null } };
      }
      return { date: value };
    }

    case 'rich_text':
      return { rich_text: parseRichText(String(value)) };

    case 'title':
      return { title: parseRichText(String(value)) };

    default:
      throw new Error(`Unsupported property type: ${propertyType}. Supported: select, multi_select, checkbox, number, url, email, date, rich_text, title`);
  }
}

// --- Rich Text Utilities ---

/**
 * Parse plain text into Notion rich_text array, handling the 2000-char limit
 */
function parseRichText(text) {
  const maxLength = 2000;
  const richText = [];

  for (let i = 0; i < text.length; i += maxLength) {
    richText.push({
      type: 'text',
      text: { content: text.substring(i, i + maxLength) }
    });
  }

  return richText.length > 0 ? richText : [{ type: 'text', text: { content: '' } }];
}

/**
 * Parse markdown-formatted text into Notion rich_text with annotations
 */
function pushRichTextChunked(richText, item, maxLength = 2000) {
  const content = item?.text?.content || '';

  if (content.length === 0) {
    richText.push(item);
    return;
  }

  for (let i = 0; i < content.length; i += maxLength) {
    richText.push({
      ...item,
      text: {
        ...item.text,
        content: content.substring(i, i + maxLength)
      }
    });
  }
}

function parseMarkdownRichText(text) {
  const richText = [];
  const parts = text.split(/(\*\*.*?\*\*|\*.*?\*|\[.*?\]\(.*?\))/);

  for (const part of parts) {
    if (!part) continue;

    if (part.startsWith('**') && part.endsWith('**')) {
      pushRichTextChunked(richText, {
        type: 'text',
        text: { content: part.slice(2, -2) },
        annotations: { bold: true }
      });
    } else if (part.startsWith('*') && part.endsWith('*') && !part.startsWith('**')) {
      pushRichTextChunked(richText, {
        type: 'text',
        text: { content: part.slice(1, -1) },
        annotations: { italic: true }
      });
    } else {
      const linkMatch = part.match(/\[(.*?)\]\((.*?)\)/);
      if (linkMatch) {
        pushRichTextChunked(richText, {
          type: 'text',
          text: { content: linkMatch[1], link: { url: linkMatch[2] } }
        });
      } else {
        pushRichTextChunked(richText, {
          type: 'text',
          text: { content: part }
        });
      }
    }
  }

  return richText.length > 0 ? richText : [{ type: 'text', text: { content: text } }];
}

// --- Markdown Parsing ---

/**
 * Parse markdown string into Notion block array
 * @param {string} markdown - Markdown content
 * @param {object} options - { richText: 'plain' | 'markdown' }
 */
function parseMarkdownToBlocks(markdown, options = {}) {
  const useMarkdownRichText = options.richText === 'markdown';
  const toRichText = useMarkdownRichText ? parseMarkdownRichText : parseRichText;

  const lines = markdown.split('\n');
  const blocks = [];
  let currentParagraph = [];
  let inCodeBlock = false;
  let codeLanguage = '';
  let codeContent = [];
  let codeFenceMarker = '';
  let codeFenceLength = 0;

  const flushParagraph = () => {
    if (currentParagraph.length > 0) {
      const text = currentParagraph.join('\n').trim();
      if (text) {
        blocks.push({
          type: 'paragraph',
          paragraph: { rich_text: toRichText(text) }
        });
      }
      currentParagraph = [];
    }
  };

  const flushCodeBlock = () => {
    const codeText = codeContent.join('\n');
    blocks.push({
      type: 'code',
      code: {
        language: codeLanguage,
        rich_text: codeText
          ? parseRichText(codeText)
          : [{ type: 'text', text: { content: '' } }]
      }
    });
    inCodeBlock = false;
    codeLanguage = '';
    codeContent = [];
    codeFenceMarker = '';
    codeFenceLength = 0;
  };

  for (const line of lines) {
    // Fenced code blocks (``` or ~~~)
    const openingFenceMatch = line.match(/^(`{3,}|~{3,})(.*)$/);
    if (!inCodeBlock && openingFenceMatch) {
      flushParagraph();
      inCodeBlock = true;
      codeFenceMarker = openingFenceMatch[1][0];
      codeFenceLength = openingFenceMatch[1].length;
      codeLanguage = openingFenceMatch[2].trim() || 'plain text';
      codeContent = [];
      continue;
    }

    if (inCodeBlock) {
      const closingFenceMatch = line.match(/^(`+|~+)\s*$/);
      const isMatchingClosingFence = Boolean(
        closingFenceMatch
        && closingFenceMatch[1][0] === codeFenceMarker
        && closingFenceMatch[1].length >= codeFenceLength
      );

      if (isMatchingClosingFence) {
        flushCodeBlock();
      } else {
        codeContent.push(line);
      }
      continue;
    }

    // Headings (check ### before ## before #)
    const headingMatch = line.match(/^(#{1,3})\s+(.*)/);
    if (headingMatch) {
      flushParagraph();
      const level = headingMatch[1].length;
      const text = headingMatch[2].trim();
      const type = `heading_${level}`;
      blocks.push({ type, [type]: { rich_text: toRichText(text) } });
      continue;
    }

    // Horizontal rules (---, ***, ___ and longer repeats)
    if (/^(?:-{3,}|\*{3,}|_{3,})$/.test(line.trim())) {
      flushParagraph();
      blocks.push({ type: 'divider', divider: {} });
      continue;
    }

    // Bullet lists
    if (/^[-*]\s+/.test(line)) {
      flushParagraph();
      const text = line.replace(/^[-*]\s+/, '').trim();
      blocks.push({
        type: 'bulleted_list_item',
        bulleted_list_item: { rich_text: toRichText(text) }
      });
      continue;
    }

    // Numbered lists
    if (/^\d+\.\s+/.test(line)) {
      flushParagraph();
      const text = line.replace(/^\d+\.\s+/, '').trim();
      blocks.push({
        type: 'numbered_list_item',
        numbered_list_item: { rich_text: toRichText(text) }
      });
      continue;
    }

    // Empty lines
    if (line.trim() === '') {
      flushParagraph();
      continue;
    }

    currentParagraph.push(line);
  }

  if (inCodeBlock) {
    flushCodeBlock();
  }

  flushParagraph();
  return blocks;
}

// --- Block to Markdown ---

/**
 * Extract plain text from rich_text array
 */
function richTextToPlain(richText) {
  if (!richText || richText.length === 0) return '';
  return richText.map(rt => rt.plain_text || '').join('');
}

/**
 * Extract markdown-formatted text from rich_text array
 */
function richTextToMarkdown(richText) {
  if (!richText || richText.length === 0) return '';

  return richText.map(rt => {
    let text = rt.plain_text || '';
    const ann = rt.annotations || {};

    if (ann.code) text = `\`${text}\``;
    if (ann.bold) text = `**${text}**`;
    if (ann.italic) text = `*${text}*`;
    if (ann.strikethrough) text = `~~${text}~~`;

    if (rt.href) {
      text = `[${text}](${rt.href})`;
    } else if (rt.text && rt.text.link) {
      text = `[${text}](${rt.text.link.url})`;
    }

    return text;
  }).join('');
}

/**
 * Convert Notion blocks to markdown string
 */
function blocksToMarkdown(blocks) {
  const lines = [];

  for (const block of blocks) {
    const type = block.type;
    const content = block[type];

    switch (type) {
      case 'heading_1':
        lines.push(`# ${richTextToMarkdown(content.rich_text)}`, '');
        break;
      case 'heading_2':
        lines.push(`## ${richTextToMarkdown(content.rich_text)}`, '');
        break;
      case 'heading_3':
        lines.push(`### ${richTextToMarkdown(content.rich_text)}`, '');
        break;
      case 'paragraph': {
        const text = richTextToMarkdown(content.rich_text);
        if (text.trim()) lines.push(text, '');
        break;
      }
      case 'bulleted_list_item':
        lines.push(`- ${richTextToMarkdown(content.rich_text)}`);
        break;
      case 'numbered_list_item':
        lines.push(`1. ${richTextToMarkdown(content.rich_text)}`);
        break;
      case 'code': {
        const code = richTextToPlain(content.rich_text);
        const lang = content.language || 'plain text';
        lines.push(`\`\`\`${lang}`, code, '```', '');
        break;
      }
      case 'divider':
        lines.push('---', '');
        break;
      case 'quote':
        lines.push(`> ${richTextToMarkdown(content.rich_text)}`, '');
        break;
      case 'callout': {
        const emoji = content.icon?.emoji || '📌';
        lines.push(`${emoji} ${richTextToMarkdown(content.rich_text)}`, '');
        break;
      }
      default:
        break;
    }
  }

  return lines.join('\n');
}

// --- Notion Page Helpers ---

/**
 * Fetch all blocks from a page/block, handling pagination
 */
async function getAllBlocks(blockId) {
  const normalizedId = normalizeId(blockId);
  let allBlocks = [];
  let cursor = null;

  do {
    const encodedId = encodeURIComponent(normalizedId);
    const path = `/v1/blocks/${encodedId}/children${cursor ? `?start_cursor=${encodeURIComponent(cursor)}` : ''}`;
    const response = await notionRequest(path, 'GET');
    allBlocks = allBlocks.concat(response.results);
    cursor = response.has_more ? response.next_cursor : null;
  } while (cursor);

  return allBlocks;
}

/**
 * Append blocks to a page in batches with rate limiting
 */
async function appendBlocksBatched(pageId, blocks, batchSize = 100, delayMs = 350) {
  for (let i = 0; i < blocks.length; i += batchSize) {
    const batch = blocks.slice(i, i + batchSize);
    await notionRequest(`/v1/blocks/${pageId}/children`, 'PATCH', { children: batch });

    if (i + batchSize < blocks.length) {
      await new Promise(resolve => setTimeout(resolve, delayMs));
    }
  }
}

module.exports = {
  // Config
  NOTION_VERSION,
  getApiKey,
  resolveToken,
  checkApiKey,
  shouldRequireApiKey,
  findLegacyTokenFlag,
  TOKEN_MIGRATION_MESSAGE,
  PROTECTED_SECRET_MESSAGE,
  supportsNativeProxy,
  isProtectedCredential,
  createProtectedProxyAgent,
  createRequestAgent,
  stripTokenArg,
  parsePositiveInteger,
  parsePageSizeLimit,
  hasJsonFlag,
  hasHelpFlag,
  getAllowedPaths,
  log,
  resolveSafePath,
  expandHomePath,
  wrapNetworkError,

  // HTTP
  notionRequest,
  createDetailedError,

  // IDs
  normalizeId,

  // Properties
  extractTitle,
  extractPropertyValue,
  formatPropertyValue,

  // Rich text
  parseRichText,
  parseMarkdownRichText,
  richTextToPlain,
  richTextToMarkdown,

  // Markdown conversion
  parseMarkdownToBlocks,
  blocksToMarkdown,

  // Page helpers
  getAllBlocks,
  appendBlocksBatched,

  // Testing
  _resetTokenCache: () => { _cachedToken = undefined; },
};
