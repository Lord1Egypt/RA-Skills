import fs from 'fs';
import path from 'path';
import https from 'https';
import os from 'os';

const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m'
};

export function log(color, ...args) {
  console.log(color + args.join(' ') + colors.reset);
}

export { colors };
export function error(...args) {
  log(colors.red, '❌', ...args);
}

export function success(...args) {
  log(colors.green, '✅', ...args);
}

export function info(...args) {
  log(colors.cyan, 'ℹ️', ...args);
}

export function warn(...args) {
  log(colors.yellow, '⚠️', ...args);
}

export function parseArgs(args) {
  const result = {
    command: null,
    args: [],
    options: {}
  };

  let currentOption = null;

  function toCamelCase(str) {
    return str.replace(/-([a-z])/g, g => g[1].toUpperCase());
  }

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if (arg.startsWith('--')) {
      const optionPart = arg.slice(2);
      const equalIndex = optionPart.indexOf('=');
      if (equalIndex !== -1) {
        let key = optionPart.slice(0, equalIndex);
        const value = optionPart.slice(equalIndex + 1);
        key = toCamelCase(key);
        result.options[key] = value;
        currentOption = null;
      } else {
        let key = optionPart;
        key = toCamelCase(key);
        currentOption = key;
        result.options[currentOption] = true;
      }
    } else if (currentOption) {
      result.options[currentOption] = arg;
      currentOption = null;
    } else if (!result.command) {
      result.command = arg;
    } else {
      result.args.push(arg);
    }
  }

  for (const key in result.options) {
    if (result.options[key] === true && !args.includes(`--${key}`)) {
    }
  }

  return result;
}

export function loadConfig(configPath) {
  if (!configPath) return {};
  
  const fullPath = path.resolve(configPath);
  if (!fs.existsSync(fullPath)) {
    error(`配置文件不存在: ${fullPath}`);
    process.exit(1);
  }
  
  try {
    const content = fs.readFileSync(fullPath, 'utf-8');
    const config = JSON.parse(content);
    return config;
  } catch (err) {
    error(`配置文件解析失败: ${err.message}`);
    process.exit(1);
  }
}

export function mergeOptions(cliOptions, configOptions) {
  const merged = { ...configOptions, ...cliOptions };
  
  for (const key in merged) {
    const value = merged[key];
    if (typeof value === 'string') {
      if (value === 'true') merged[key] = true;
      else if (value === 'false') merged[key] = false;
      else if (/^\d+$/.test(value)) merged[key] = parseInt(value);
    }
  }
  
  return merged;
}

export function getApiKey(providedKey) {
  const envKey = providedKey || process.env.MIAOYING_API_KEY;
  if (envKey) return envKey;

  // Fall back to ~/.miaoying/config.json
  const configPath = path.join(os.homedir(), '.miaoying', 'config.json');
  if (fs.existsSync(configPath)) {
    try {
      const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
      if (config.apiKey) return config.apiKey;
    } catch {
      // Config file exists but is unreadable — proceed to error
    }
  }

  error('未找到 MIAOYING_API_KEY');
  info('请运行 "miaoying login" 进行微信扫码登录');
  process.exit(1);
}

export function httpsRequest(options, data) {
  return new Promise((resolve, reject) => {
    const req = https.request(options, res => {
      let body = '';
      res.on('data', chunk => (body += chunk));
      res.on('end', () => {
        try {
          const response = JSON.parse(body);
          if (response.errors) {
            reject(new Error(JSON.stringify(response.errors)));
          } else {
            resolve(response);
          }
        } catch (e) {
          reject(new Error(`Failed to parse: ${body}`));
        }
      });
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

export const API_HOST = 'www.aiphoto8.cn';

// ==================== URL SECURITY ====================

/**
 * Allowed domains for OSS downloads (SSRF protection)
 * Only these domains are allowed for file downloads to prevent SSRF attacks.
 * All domains are lowercase and do not include trailing dots.
 */
const ALLOWED_OSS_DOMAINS = [
  'cdn.hui51.cn',
  'hui51.oss-cn-beijing.aliyuncs.com'
];

/**
 * Request timeout in milliseconds (30 seconds)
 */
const REQUEST_TIMEOUT = 30000;

/**
 * Maximum file size for downloads (200 MB)
 */
const MAX_DOWNLOAD_SIZE = 20 * 1024 * 1024;

/**
 * Validates a URL against the allowlist for SSRF protection
 * @param {string} url - URL to validate
 * @returns {{ valid: boolean, url: string, error?: string }}
 */
export function validateDownloadUrl(url) {
  if (!url || typeof url !== 'string') {
    return { valid: false, url: '', error: 'URL is required' };
  }

  // Basic URL validation
  let parsedUrl;
  try {
    parsedUrl = new URL(url);
  } catch (e) {
    return { valid: false, url: '', error: 'Invalid URL format' };
  }

  // Only allow HTTPS (and HTTP for backward compatibility, but warn)
  if (parsedUrl.protocol !== 'https:' && parsedUrl.protocol !== 'http:') {
    return { valid: false, url: '', error: 'Only HTTP and HTTPS protocols are allowed' };
  }

  // Warn about HTTP (not secure)
  if (parsedUrl.protocol === 'http:') {
    warn('Warning: Using insecure HTTP connection');
  }

  // Validate domain against allowlist
  // Must match exactly or be a subdomain of an allowed domain
  const hostname = parsedUrl.hostname.toLowerCase();
  const isAllowed = ALLOWED_OSS_DOMAINS.some(allowed => {
    // Exact match
    if (hostname === allowed) {
      return true;
    }
    // Subdomain match: hostname must end with .allowed (not just contain it)
    // This prevents evil-cdn.hui51.cn from matching cdn.hui51.cn
    const suffix = '.' + allowed;
    return hostname.endsWith(suffix);
  });

  if (!isAllowed) {
    return {
      valid: false,
      url: '',
      error: `Domain not allowed: ${hostname}. Allowed domains: ${ALLOWED_OSS_DOMAINS.join(', ')}`
    };
  }

  return { valid: true, url: url };
}

/**
 * Validates a URL and returns sanitized version
 * @param {string} url - URL to validate
 * @returns {string} - Validated URL
 * @throws {Error} - If URL is invalid
 */
export function validateAndSanitizeUrl(url) {
  const result = validateDownloadUrl(url);
  if (!result.valid) {
    throw new Error(result.error);
  }
  return result.url;
}

export function resolveOssPath(rawPath, useThumbnail = true) {
  const CDN_DOMAIN = 'https://cdn.hui51.cn';

  // Validate rawPath input
  if (!rawPath || typeof rawPath !== 'string') {
    throw new Error('Invalid path provided');
  }

  // Check for path traversal in rawPath
  if (rawPath.includes('..')) {
    throw new Error('Path traversal not allowed');
  }

  if (rawPath.startsWith(CDN_DOMAIN) || rawPath.startsWith('http://') || rawPath.startsWith('https://')) {
    // Validate the URL is from allowed domain
    try {
      const url = new URL(rawPath);
      const hostname = url.hostname.toLowerCase();
      const isAllowed = ALLOWED_OSS_DOMAINS.some(allowed => {
        if (hostname === allowed) return true;
        const suffix = '.' + allowed;
        return hostname.endsWith(suffix);
      });
      if (!isAllowed) {
        warn(`Warning: URL domain ${hostname} is not in allowlist`);
      }
    } catch (e) {
      // If URL parsing fails, proceed with caution
      warn('Warning: Could not validate URL domain');
    }

    if (useThumbnail && !rawPath.includes('x-oss-process=style/export-w')) {
      let url = rawPath;
      if (url.includes('?')) {
        url = url.replace(/\?.*/, '') + '?x-oss-process=style/export-w';
      } else {
        url = url + '?x-oss-process=style/export-w';
      }
      return url;
    }
    return rawPath;
  }

  // Sanitize the path
  let normalizedPath = rawPath.replace(/\.\./g, '_').replace(/[\x00-\x1f]/g, '');

  if (!normalizedPath.startsWith('uploads/')) {
    normalizedPath = 'uploads/' + normalizedPath;
  }

  if (useThumbnail) {
    return CDN_DOMAIN + '/' + normalizedPath + '?x-oss-process=style/export-w';
  }

  return CDN_DOMAIN + '/' + normalizedPath;
}

export function extractFileId(ossUrl) {
  const match = ossUrl.match(/uploads\/([^\/\?]+)/);
  if (match) {
    return match[1];
  }
  const noExt = ossUrl.replace(/\.(jpg|png|jpeg|gif|webp)/i, '');
  return noExt.split('/')[0];
}

export function getOriginalFilename(ossUrl) {
  const match = ossUrl.match(/uploads\/([^\/\?]+)/);
  if (match) {
    const filename = match[1];
    const ext = filename.split('.').pop();
    return filename;
  }
  return 'file';
}

export function downloadOssFile(url, filePath, onProgress) {
  return new Promise((resolve, reject) => {
    // Validate URL for SSRF protection
    const validation = validateDownloadUrl(url);
    if (!validation.valid) {
      reject(new Error(validation.error));
      return;
    }

    // Validate file path for security
    try {
      const resolvedPath = path.resolve(filePath);
      const baseDir = getCacheBasePath();
      if (!resolvedPath.startsWith(baseDir)) {
        reject(new Error('File path must be within cache directory'));
        return;
      }
    } catch (err) {
      reject(new Error(`Invalid file path: ${err.message}`));
      return;
    }

    const file = fs.createWriteStream(filePath);
    let downloadedBytes = 0;

    // Create request with timeout and security options
    const req = https.get(url, {
      timeout: REQUEST_TIMEOUT,
      // Enable SSL certificate verification
      rejectUnauthorized: true
    }, (response) => {
      // Check for redirects - don't follow automatically for security
      if ([301, 302, 303, 307, 308].includes(response.statusCode)) {
        fs.unlink(filePath, () => {});
        reject(new Error('Redirects not allowed for security. Please use the final URL directly.'));
        return;
      }

      if (response.statusCode !== 200) {
        fs.unlink(filePath, () => {});
        reject(new Error(`HTTP ${response.statusCode}: ${response.statusMessage || 'Download failed'}`));
        return;
      }

      // Check content length for size limit
      const contentLength = parseInt(response.headers['content-length'], 10);
      if (contentLength && contentLength > MAX_DOWNLOAD_SIZE) {
        fs.unlink(filePath, () => {});
        reject(new Error(`File too large: ${(contentLength / 1024 / 1024).toFixed(2)} MB. Maximum: ${MAX_DOWNLOAD_SIZE / 1024 / 1024} MB`));
        return;
      }

      response.on('data', (chunk) => {
        downloadedBytes += chunk.length;
        // Check size limit during download
        if (downloadedBytes > MAX_DOWNLOAD_SIZE) {
          fs.unlink(filePath, () => {});
          reject(new Error(`Download exceeded maximum size of ${MAX_DOWNLOAD_SIZE / 1024 / 1024} MB`));
          req.destroy();
          return;
        }
        if (onProgress && contentLength) {
          const percent = Math.round((downloadedBytes / contentLength) * 100);
          onProgress(downloadedBytes, contentLength, percent);
        }
      });

      response.pipe(file);
      file.on('finish', () => {
        file.close();
        resolve(filePath);
      });
    });

    req.on('timeout', () => {
      req.destroy();
      fs.unlink(filePath, () => {});
      reject(new Error(`Download timed out after ${REQUEST_TIMEOUT / 1000} seconds`));
    });

    req.on('error', (err) => {
      fs.unlink(filePath, () => {});
      // Sanitize error message
      const safeMessage = err.message.replace(/[^a-zA-Z0-9\s\-.:]/g, '_');
      reject(new Error(`Download failed: ${safeMessage}`));
    });
  });
}

export function downloadOssFileSync(url, filePath, onProgress) {
  return new Promise((resolve, reject) => {
    // Validate URL for SSRF protection
    const validation = validateDownloadUrl(url);
    if (!validation.valid) {
      reject(new Error(validation.error));
      return;
    }

    // Validate file path for security
    try {
      const resolvedPath = path.resolve(filePath);
      const baseDir = getCacheBasePath();
      if (!resolvedPath.startsWith(baseDir)) {
        reject(new Error('File path must be within cache directory'));
        return;
      }
    } catch (err) {
      reject(new Error(`Invalid file path: ${err.message}`));
      return;
    }

    // Create request with timeout and security options
    const req = https.get(url, {
      timeout: REQUEST_TIMEOUT,
      rejectUnauthorized: true
    }, (response) => {
      // Check for redirects
      if ([301, 302, 303, 307, 308].includes(response.statusCode)) {
        if (fs.existsSync(filePath)) fs.unlink(filePath, () => {});
        reject(new Error('Redirects not allowed for security. Please use the final URL directly.'));
        return;
      }

      if (response.statusCode !== 200) {
        if (fs.existsSync(filePath)) fs.unlink(filePath, () => {});
        reject(new Error(`HTTP ${response.statusCode}: ${response.statusMessage || 'Download failed'}`));
        return;
      }

      const totalSize = parseInt(response.headers['content-length'], 10);

      // Check size limit
      if (totalSize && totalSize > MAX_DOWNLOAD_SIZE) {
        if (fs.existsSync(filePath)) fs.unlink(filePath, () => {});
        reject(new Error(`File too large: ${(totalSize / 1024 / 1024).toFixed(2)} MB. Maximum: ${MAX_DOWNLOAD_SIZE / 1024 / 1024} MB`));
        return;
      }

      let downloadedSize = 0;

      response.on('data', (chunk) => {
        downloadedSize += chunk.length;
        // Check size limit during download
        if (downloadedSize > MAX_DOWNLOAD_SIZE) {
          if (fs.existsSync(filePath)) fs.unlink(filePath, () => {});
          reject(new Error(`Download exceeded maximum size of ${MAX_DOWNLOAD_SIZE / 1024 / 1024} MB`));
          req.destroy();
          return;
        }
        if (onProgress && totalSize) {
          const percent = Math.round((downloadedSize / totalSize) * 100);
          onProgress(downloadedSize, totalSize, percent);
        }
      });

      const file = fs.createWriteStream(filePath);
      response.pipe(file);

      file.on('finish', () => {
        file.close();
        resolve(filePath);
      });
    });

    req.on('timeout', () => {
      req.destroy();
      if (fs.existsSync(filePath)) fs.unlink(filePath, () => {});
      reject(new Error(`Download timed out after ${REQUEST_TIMEOUT / 1000} seconds`));
    });

    req.on('error', (err) => {
      if (fs.existsSync(filePath)) {
        fs.unlink(filePath, () => {});
      }
      // Sanitize error message
      const safeMessage = err.message.replace(/[^a-zA-Z0-9\s\-.:]/g, '_');
      reject(new Error(`Download failed: ${safeMessage}`));
    });
  });
}

export function formatProgress(downloaded, total, percent) {
  const barLength = 40;
  const filledLength = Math.round((percent / 100) * barLength);
  const bar = '█'.repeat(filledLength) + '░'.repeat(barLength - filledLength);
  return `${bar} ${percent}% (${formatSize(downloaded)}/${formatSize(total)})`;
}

export function formatSize(bytes) {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
}

export async function getOssSign(apiKey) {
  const data = JSON.stringify({
    isVip: false
  });

  const response = await httpsRequest(
    {
      hostname: API_HOST,
      port: 443,
      path: '/api/openapi/oss-sign',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
        'Content-Length': Buffer.byteLength(data)
      }
    },
    data
  );

  if (response.statusCode && response.statusCode !== 200) {
    throw new Error(`HTTP ${response.statusCode}: ${response.message || 'Failed to get OSS sign'}`);
  }

  return response;
}

// ==================== SECURITY UTILITIES ====================

/**
 * Valid entity types for file caching - prevents path traversal via entityType
 */
const VALID_ENTITY_TYPES = ['Tongji', 'Booking', 'Toupiao', 'Chacha'];

/**
 * Maximum allowed length for entity IDs to prevent DoS
 */
const MAX_ID_LENGTH = 256;

/**
 * Validates and sanitizes an entity ID to prevent path traversal attacks
 * @param {string} id - The entity ID to validate
 * @param {string} context - Context for error messages (e.g., 'tongji', 'vote')
 * @returns {string} - Sanitized ID
 * @throws {Error} - If ID is invalid
 */
export function validateEntityId(id, context = 'entity') {
  if (!id || typeof id !== 'string') {
    throw new Error(`Invalid ${context} ID: must be a non-empty string`);
  }

  // Trim whitespace
  const trimmedId = id.trim();

  // Check length
  if (trimmedId.length === 0) {
    throw new Error(`Invalid ${context} ID: cannot be empty`);
  }

  if (trimmedId.length > MAX_ID_LENGTH) {
    throw new Error(`Invalid ${context} ID: exceeds maximum length of ${MAX_ID_LENGTH}`);
  }

  // Check for path traversal patterns
  if (trimmedId.includes('..') || trimmedId.includes('/') || trimmedId.includes('\\')) {
    throw new Error(`Invalid ${context} ID: contains forbidden characters`);
  }

  // Only allow alphanumeric, dash, underscore, and dot
  if (!/^[a-zA-Z0-9_.-]+$/.test(trimmedId)) {
    throw new Error(`Invalid ${context} ID: contains invalid characters`);
  }

  return trimmedId;
}

/**
 * Validates entity type against whitelist
 * @param {string} entityType - The entity type to validate
 * @returns {string} - Validated entity type
 * @throws {Error} - If entity type is invalid
 */
export function validateEntityType(entityType) {
  if (!entityType || typeof entityType !== 'string') {
    throw new Error('Entity type is required');
  }

  // Capitalize first letter if needed
  const normalized = entityType.charAt(0).toUpperCase() + entityType.slice(1).toLowerCase();

  if (!VALID_ENTITY_TYPES.includes(normalized)) {
    throw new Error(`Invalid entity type: ${entityType}. Allowed: ${VALID_ENTITY_TYPES.join(', ')}`);
  }

  return normalized;
}

/**
 * Sanitizes a file ID for safe filesystem operations
 * Removes path traversal sequences and normalizes the ID
 * @param {string} fileId - The file ID to sanitize
 * @returns {string} - Sanitized file ID safe for filesystem use
 */
export function sanitizeFileId(fileId) {
  if (!fileId || typeof fileId !== 'string') {
    return 'unknown';
  }

  // Remove any path traversal attempts
  let sanitized = fileId
    .replace(/\.\./g, '_')           // Remove parent directory references
    .replace(/[\/\\]/g, '_')          // Remove path separators
    .replace(/[\x00-\x1f]/g, '_')     // Remove control characters
    .replace(/[<>:"|?*]/g, '_')       // Remove invalid filename characters (Windows)
    .trim();

  // Limit length
  if (sanitized.length > MAX_ID_LENGTH) {
    const ext = sanitized.includes('.') ? '.' + sanitized.split('.').pop() : '';
    sanitized = sanitized.substring(0, MAX_ID_LENGTH - ext.length) + ext;
  }

  return sanitized || 'unknown';
}

/**
 * Validates a file path for safe operations
 * Ensures path is within allowed directories
 * @param {string} filePath - Path to validate
 * @param {string} basePath - Base directory the path should be within (defaults to cwd)
 * @returns {string} - Resolved safe path
 * @throws {Error} - If path is invalid or outside allowed directory
 */
export function validateFilePath(filePath, basePath = process.cwd()) {
  if (!filePath || typeof filePath !== 'string') {
    throw new Error('File path is required');
  }

  // Resolve to absolute path
  const resolvedPath = path.resolve(filePath);
  const normalizedBase = path.resolve(basePath);

  // Check for path traversal
  if (filePath.includes('..')) {
    throw new Error('Path traversal not allowed in file path');
  }

  // Ensure path is within base directory
  if (!resolvedPath.startsWith(normalizedBase)) {
    throw new Error('File path must be within the current working directory');
  }

  return resolvedPath;
}

/**
 * Validates an output file path for exports
 * @param {string} outputPath - Output path to validate
 * @returns {string} - Validated output path
 * @throws {Error} - If path is invalid
 */
export function validateOutputPath(outputPath) {
  if (!outputPath || typeof outputPath !== 'string') {
    throw new Error('Output path is required');
  }

  // Check for path traversal
  if (outputPath.includes('..')) {
    throw new Error('Path traversal not allowed in output path');
  }

  // Resolve and validate
  const resolved = path.resolve(outputPath);
  const cwd = process.cwd();

  // Warn if outside cwd (but allow it with explicit path)
  if (!resolved.startsWith(cwd)) {
    warn('Output path is outside current working directory');
  }

  // Validate extension for known formats
  const ext = path.extname(resolved).toLowerCase();
  const validExtensions = ['.xlsx', '.jsonl', '.json'];
  if (ext && !validExtensions.includes(ext)) {
    warn(`Unexpected file extension: ${ext}. Expected: ${validExtensions.join(', ')}`);
  }

  return resolved;
}

// ==================== FILE CACHE UTILITIES ====================

export function getCacheBasePath() {
  const homePath = process.platform === 'win32' ? process.env.USERPROFILE : process.env.HOME;
  if (!homePath) throw new Error('无法获取用户主目录');
  return path.join(homePath, '.miaoying', 'caches');
}

export function getCacheDirByEntityType(entityType, fileId = '') {
  // Validate entity type
  const validType = validateEntityType(entityType);

  // Sanitize file ID
  const safeFileId = sanitizeFileId(fileId);

  const basePath = getCacheBasePath();
  const dir = path.join(basePath, validType, safeFileId);

  // Verify the resolved path is still within cache directory (extra safety)
  const normalizedDir = path.resolve(dir);
  const normalizedBase = path.resolve(basePath);
  if (!normalizedDir.startsWith(normalizedBase)) {
    throw new Error('Invalid cache path: path traversal detected');
  }

  return dir;
}

/**
 * Safely parses JSON with detailed error handling
 * @param {string} jsonStr - JSON string to parse
 * @param {string} context - Context for error messages
 * @returns {any} - Parsed JSON data
 * @throws {Error} - If parsing fails
 */
export function safeJsonParse(jsonStr, context = 'JSON') {
  if (!jsonStr || typeof jsonStr !== 'string') {
    throw new Error(`${context} must be a non-empty string`);
  }

  try {
    return JSON.parse(jsonStr);
  } catch (err) {
    // Provide more helpful error message
    const preview = jsonStr.length > 50 ? jsonStr.substring(0, 50) + '...' : jsonStr;
    throw new Error(`Failed to parse ${context}: ${err.message}. Input: "${preview}"`);
  }
}

export function getLocalFilePath(entityType, fileId, useThumbnail = true) {
  // Validate and sanitize inputs
  const validType = validateEntityType(entityType);
  const safeFileId = sanitizeFileId(fileId);

  const basePath = getCacheBasePath();
  const dir = path.join(basePath, validType, safeFileId);

  // Verify path safety
  const normalizedDir = path.resolve(dir);
  const normalizedBase = path.resolve(basePath);
  if (!normalizedDir.startsWith(normalizedBase)) {
    throw new Error('Invalid file path: path traversal detected');
  }

  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }

  const ext = safeFileId.includes('.') ? safeFileId.split('.').pop() : 'jpg';
  const suffix = useThumbnail ? '_thumb' : '_original';
  const baseName = safeFileId.replace(/\.(jpg|png|jpeg|gif|webp)$/i, '');
  const filename = `${baseName}${suffix}.${ext}`;
  const fullPath = path.join(dir, filename);

  // Final safety check
  const normalizedFullPath = path.resolve(fullPath);
  if (!normalizedFullPath.startsWith(normalizedBase)) {
    throw new Error('Invalid file path: path traversal detected');
  }

  return fullPath;
}

export function isFileDownloaded(entityType, fileId, useThumbnail = true) {
  const filePath = getLocalFilePath(entityType, fileId, useThumbnail);
  return fs.existsSync(filePath);
}

export function showHelp() {
  console.log(`
${colors.bright}${colors.cyan}秒应 CLI 工具${colors.reset}

${colors.bright}━━━ 如何选择：预约 vs 统计 ━━━${colors.reset}

  ${colors.green}📅 使用预约 (miaoying book) 的情况：${colors.reset}
  • 需要"分时段预约"功能（如：上午/下午/晚上时段）
  • 需要控制每个时间段的人数（如：每时段限10人）
  • 用户提到：预约、订号、限号、时间段、时段预约

  ${colors.green}📊 使用统计 (miaoying create) 的情况：${colors.reset}
  • 需要收集信息、报名、打卡、问卷
  • 用户提到：统计、报名、问卷、收集信息、填表

  ${colors.green}📝 使用考试 (miaoying exam) 的情况：${colors.reset}
  • 需要创建在线考试、测验、问卷考试
  • 需要设置考试时长、自动阅卷、成绩排名
  • 用户提到：考试、测验、在线考试、问卷考试

  ${colors.green}🎓 使用选课 (miaoying create + type=24) 的情况：${colors.reset}
  • 学校选课、培训机构课程报名、兴趣班抢课
  • 需要展示课程列表、配额限制、时间安排
  • 用户提到：选课、抢课、课程选择、课程报名
  • ⚠️ 选课需要在 forms 中包含 type="24" 的课程选择字段

${colors.bright}━━━ 配置文件支持 ━━━${colors.reset}
  ${colors.cyan}--config <文件路径>${colors.reset}  从 JSON 配置文件加载选项
  配置文件示例 (config.json):
  {
    "title": "活动标题",
    "desc": "活动描述",
    "forms": [{"title": "姓名", "type": "text", "required": true}],
    "count": 100,
    "endTime": "2026-04-01T23:59:59",
    "anonymous": true
  }
  CLI 参数会覆盖配置文件中的同名选项

${colors.bright}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${colors.reset}

${colors.bright}使用方法:${colors.reset}
  miaoying create [options]              创建新的统计
  miaoying update [options]              更新统计
  miaoying list [options]                获取统计列表
  miaoying get <tongji-id>               获取单个统计详情
  miaoying totals <tongji-id> [options]  获取报名总数
  miaoying results <tongji-id> [options] 获取报名结果
  miaoying qrcode <tongji-id> [options]  生成二维码

  miaoying vote [options]                创建新的投票
  miaoying update-vote [options]          更新投票
  miaoying vote-list [options]            获取投票列表
  miaoying vote-get <toupiao-id>         获取投票详情
  miaoying vote-results <toupiao-id>     获取投票结果
  miaoying vote-qrcode <toupiao-id>      生成投票二维码

  miaoying book [options]                创建新的预约
  miaoying exam [options]                创建新的考试
   miaoying chacha-list [options]         获取查查列表
   miaoying chacha-get <chacha-id>        获取查查详情
   miaoying update-chacha [options]        更新查查
   miaoying export <activity-id> --type <type>  导出数据
   miaoying download <file-url>            下载 OSS 缩略图文件
   miaoying download <file-url> --original 下载 OSS 原图文件
   miaoying download <file-url> --entity <type> --verbose 下载并显示详细信息
   miaoying login                            微信扫码获取 API Key
   miaoying logout                           禁用当前 Key 并登出
   miaoying help                           显示帮助

${colors.bright}创建统计选项:${colors.reset}
  --title <标题>          统计标题 (必需)
  --desc <描述>           统计描述
  --info-forms <JSON>     表单字段 (JSON 数组)
  --count <数量>          人数限制
  --end-time <日期>       结束时间 (ISO 格式)
  --anonymous            匿名填写
  --qrcode                创建后自动生成二维码
  --app <应用名>           应用名 (qingtongji/huiyuan，默认 qingtongji)

${colors.bright}更新统计选项:${colors.reset}
  --id <ID>              统计 ID (必需)
  --title <标题>          统计标题
  --desc <描述>           统计描述
  --info-forms <JSON>     表单字段 (JSON 数组)
  --count <数量>          人数限制
  --end-time <日期>       结束时间 (ISO 格式)
  --anonymous            匿名填写
  --close <true/false>   关闭/开启统计
  --repeat <true/false>  允许重复打卡

${colors.bright}更新投票选项:${colors.reset}
  --id <ID>              投票 ID (必需)
  --title <标题>          投票标题
  --desc <描述>           投票描述
  --single <true/false>   单选投票
  --count <数量>          投票人数限制
  --end-time <日期>       结束时间 (ISO 格式)
  --publish-result <true/false>  公开结果
  --anonymous <true/false>       匿名投票
  --allow-vote <次数>     允许投票次数
  --min-select <数量>     最少选择数
  --max-select <数量>     最多选择数
  --options <JSON>        投票项配置 (JSON 格式)

${colors.bright}更新查查选项:${colors.reset}
  --id <ID>              查查 ID (必需)
  --title <标题>          查查标题
  --desc <描述>           查查描述
  --author-name <名称>    作者名称
  --sheets <JSON>         表格配置 (JSON 格式)

${colors.bright}创建投票选项:${colors.reset}
  --title <标题>          投票标题 (必需)
  --desc <描述>           投票描述
  --options <JSON>        投票项配置 (JSON 格式)
  --single                单选投票
  --multi                 多选项投票
  --count <数量>          投票人数限制
  --end-time <日期>       结束时间 (ISO 格式)
  --allow-vote <次数>     允许投票次数
  --min-select <数量>      最少选择数
  --max-select <数量>      最多选择数
  --publish-result        公开结果 (true/false)
  --anonymous             匿名投票
  --qrcode                创建后自动生成二维码

${colors.bright}创建预约选项:${colors.reset}
  --title <标题>          预约标题 (必需)
  --desc <描述>           预约描述
  --info-forms <JSON>     表单字段 (JSON 数组)
  --slots <数量>           每天时段数 (1=全天 7:00-23:59, 2=上午下午, 3=上下午晚上, 默认1)
  --count <数量>          每时段人数限制 (默认 20)
  --user-limit <次数>     每人预约次数限制 (默认 1)
  --start-time <日期>     开始时间 (ISO 格式)
  --end-time <日期>       结束时间 (ISO 格式)
  --fixed-no              使用固定名单模式
  --no-name <标签>        固定名单标签名 (序号/学号/工号/座位号，默认"序号")
  --qrcode                创建后自动生成二维码

${colors.bright}创建考试选项:${colors.reset}
  --title <标题>          考试标题 (必需)
  --desc <描述>           考试描述
  --duration <分钟>       考试时长 (默认 60 分钟)
  --questions <JSON>      考试题目 (JSON 数组)
  --info-forms <JSON>     信息收集字段 (JSON 数组)
  --start-time <日期>     开始时间 (ISO 格式)
  --end-time <日期>       结束时间 (ISO 格式)
  --fixed-no              使用固定名单模式 (默认启用)
  --no-fixed-no           不使用固定名单模式
  --no-name <标签>        固定名单标签名 (默认"学号")
  --qrcode                创建后自动生成二维码

${colors.bright}导出数据选项:${colors.reset}
  --type <类型>           活动类型 (tongji/booking/toupiao/chacha)
  --format <格式>         输出格式 (xlsx/jsonl，默认 xlsx)
  --output <路径>         输出文件路径
  --limit <数量>          每页记录数 (默认 100)
  --incremental/-i        增量导出模式
  --force/-f              强制全量导出

${colors.bright}获取统计/投票/预约列表选项:${colors.reset}
  --limit <数量>          返回数量 (默认 50)
  --skip <数量>           跳过数量 (分页)
  --title <标题>          按标题筛选（精确匹配）
  --search <关键词>       按关键词搜索（模糊匹配标题和内容）

${colors.bright}生成二维码选项:${colors.reset}
  --output <路径>         输出文件路径
  --app <应用名>           应用名 (qingtongji/huiyuan，默认 qingtongji)
  --type <类型>           实体类型 (tongji/booking/toupiao/chacha)

${colors.bright}环境变量:${colors.reset}
  MIAOYING_API_KEY         秒应 API 密钥 (必需)

${colors.bright}示例:${colors.reset}
  ${colors.cyan}# 创建统计${colors.reset}
  miaoying create --title "每日打卡" --desc "请完成每日打卡" --qrcode

  ${colors.cyan}# 获取统计列表${colors.reset}
  miaoying list --limit 10

  ${colors.cyan}# 创建投票${colors.reset}
  miaoying vote --title "选择班干部" --single --qrcode

  ${colors.cyan}# 创建预约${colors.reset}
  miaoying book --title "医生咨询预约" --slots 1 --count 20 --qrcode

  ${colors.cyan}# 创建考试${colors.reset}
  miaoying exam --title "期中考试" --duration 90 --qrcode

  ${colors.cyan}# 导出 xlsx 数据${colors.reset}
  miaoying export <activity-id> --type tongji

  ${colors.cyan}# 增量导出（自上次导出以来新增的数据）${colors.reset}
  miaoying export <activity-id> --type tongji --incremental

${colors.bright}获取 API Key:${colors.reset}
  首次使用时 AI 自动弹出二维码引导扫码获取
  如 Key 泄露，AI 会自动调用禁用接口并引导重新扫码
`);
}
