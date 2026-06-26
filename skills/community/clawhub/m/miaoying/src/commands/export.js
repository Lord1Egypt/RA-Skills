import fs from 'fs';
import path from 'path';
import {
  getApiKey,
  httpsRequest,
  API_HOST,
  log,
  colors,
  success,
  error,
  info,
  warn,
  safeJsonParse
} from '../utils.js';

// ==================== SECURITY CONSTANTS ====================

/**
 * Valid export types
 */
const VALID_EXPORT_TYPES = ['tongji', 'booking', 'toupiao', 'chacha'];

/**
 * Valid export formats
 */
const VALID_FORMATS = ['xlsx', 'jsonl'];

/**
 * Maximum records per page
 */
const MAX_LIMIT = 1000;

/**
 * Minimum records per page
 */
const MIN_LIMIT = 1;

/**
 * Validates export options
 * @param {string} activityId - Activity ID to validate
 * @param {object} options - Export options
 * @returns {{ valid: boolean, error?: string }}
 */
function validateExportOptions(activityId, options) {
  // Validate activity ID
  if (!activityId || typeof activityId !== 'string') {
    return { valid: false, error: 'Activity ID is required' };
  }

  // Check for path traversal in activityId
  if (activityId.includes('..') || activityId.includes('/') || activityId.includes('\\')) {
    return { valid: false, error: 'Invalid activity ID: contains forbidden characters' };
  }

  // Validate type
  const type = options.type || 'tongji';
  if (!VALID_EXPORT_TYPES.includes(type)) {
    return { valid: false, error: `Invalid type: ${type}. Allowed: ${VALID_EXPORT_TYPES.join(', ')}` };
  }

  // Validate format
  const format = options.format || 'xlsx';
  if (!VALID_FORMATS.includes(format)) {
    return { valid: false, error: `Invalid format: ${format}. Allowed: ${VALID_FORMATS.join(', ')}` };
  }

  // Validate limit
  if (options.limit) {
    const limit = parseInt(options.limit, 10);
    if (isNaN(limit) || limit < MIN_LIMIT || limit > MAX_LIMIT) {
      return { valid: false, error: `Invalid limit: must be between ${MIN_LIMIT} and ${MAX_LIMIT}` };
    }
  }

  return { valid: true };
}

/**
 * Validates and sanitizes output path
 * @param {string} outputPath - Output path to validate
 * @param {string} type - Export type
 * @param {string} activityId - Activity ID
 * @param {string} format - Export format
 * @returns {string} - Validated output path
 */
function validateAndResolveOutputPath(outputPath, type, activityId, format) {
  if (!outputPath) {
    // Generate default path
    outputPath = `./${type}-${activityId}-export.${format}`;
  }

  // Check for path traversal
  if (outputPath.includes('..')) {
    throw new Error('Path traversal not allowed in output path');
  }

  // Check for null bytes
  if (outputPath.includes('\0')) {
    throw new Error('Null bytes not allowed in output path');
  }

  // Resolve to absolute path
  const resolvedPath = path.resolve(outputPath);

  // Validate extension matches format
  const ext = path.extname(resolvedPath).toLowerCase();
  const expectedExt = format === 'xlsx' ? '.xlsx' : '.jsonl';
  if (ext && ext !== expectedExt) {
    warn(`Warning: Output file extension "${ext}" does not match format "${format}"`);
  }

  // Check if path is within current working directory (optional warning)
  const cwd = process.cwd();
  if (!resolvedPath.startsWith(cwd)) {
    warn('Warning: Output path is outside current working directory');
  }

  return resolvedPath;
}

/**
 * Validates cache path for incremental exports
 * @param {string} activityId - Activity ID
 * @returns {string} - Validated cache path
 */
function validateCachePath(activityId) {
  // Sanitize activity ID for use in path
  const sanitizedId = activityId.replace(/\.\./g, '_').replace(/[\/\\]/g, '_');

  const cachePath = path.resolve(`./.miaoying/cache/${sanitizedId}/meta.json`);
  const cwd = process.cwd();

  // Ensure cache path is within current working directory
  if (!cachePath.startsWith(cwd)) {
    throw new Error('Cache path validation failed');
  }

  return cachePath;
}

export async function exportData(activityId, options) {
  const apiKey = getApiKey(options?.apiKey);

  // Validate all export options
  const validation = validateExportOptions(activityId, options);
  if (!validation.valid) {
    error(validation.error);
    process.exit(1);
  }

  const type = options.type || 'tongji';
  const format = options.format || 'xlsx';

  // Validate and resolve output path
  let outputPath;
  try {
    outputPath = validateAndResolveOutputPath(options.output, type, activityId, format);
  } catch (err) {
    error(`Invalid output path: ${err.message}`);
    process.exit(1);
  }

  const limit = Math.min(Math.max(parseInt(options.limit) || 100, MIN_LIMIT), MAX_LIMIT);
  const since = options.since;
  const incremental = options.incremental || options.i;
  const force = options.force || options.f;

  info('开始导出数据...');
  log(colors.bright, '   活动ID:', activityId);
  log(colors.bright, '   类型:', type);
  log(colors.bright, '   每页记录数:', limit);
  if (since) {
    log(colors.bright, '   增量起始时间:', since);
  }

  // Validate cache path
  let cachePath;
  try {
    cachePath = validateCachePath(activityId);
  } catch (err) {
    warn(`Cache path validation failed, incremental mode disabled: ${err.message}`);
  }

  let lastExportAt = null;

  if (incremental && !force && cachePath) {
    try {
      if (fs.existsSync(cachePath)) {
        const cacheData = safeJsonParse(fs.readFileSync(cachePath, 'utf-8'), 'cache data');
        lastExportAt = cacheData.lastExportAt;
        log(colors.bright, '   增量模式: 自', lastExportAt, '以来');
      }
    } catch (err) {
      warn(`无法读取缓存，将进行全量导出: ${err.message}`);
    }
  }

  const queryParams = new URLSearchParams({
    type: type,
    activityId: activityId,
    limit: limit.toString()
  });

  if (lastExportAt) {
    queryParams.append('since', lastExportAt);
  }

  let allRecords = [];
  let allCols = [];
  let activityTitle = '';
  let totalFetched = 0;
  let cursor = null;
  let hasMore = true;
  let allMerges = [];

  while (hasMore) {
    if (cursor) {
      queryParams.set('cursor', cursor);
    }

    const requestPath = `/api/openapi/creator/export/data?${queryParams.toString()}`;

    try {
      const response = await httpsRequest(
        {
          hostname: API_HOST,
          port: 443,
          path: requestPath,
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${apiKey}`
          }
        },
        ''
      );

      if (!response.success) {
        error('API 请求失败:', response);
        process.exit(1);
      }

      const { data, activityInfo } = response;
      const { cols, rows, meta, merge = [] } = data;

      if (totalFetched === 0 && activityInfo) {
        activityTitle = activityInfo.title;
        allCols = cols;
        log(colors.bright, '   活动标题:', activityTitle);
        log(colors.bright, '   总记录数:', meta.total);
        log(colors.bright, '   导出模式:', meta.mode === 'incremental' ? '增量' : '全量');
      }

      allRecords.push(...rows);

      if (merge && merge.length > 0) {
        const currentRowIndex = totalFetched;
        merge.forEach(m => {
          allMerges.push({
            s: { r: m.s.r + currentRowIndex, c: m.s.c },
            e: { r: m.e.r + currentRowIndex, c: m.e.c }
          });
        });
      }

      totalFetched += meta.returnedCount;

      process.stdout.write(
        `\r${colors.cyan}已获取: ${totalFetched}/${meta.total} 条记录 (${Math.round((totalFetched / meta.total) * 100)}%)${colors.reset}`
      );

      hasMore = meta.hasMore;
      cursor = meta.nextCursor;

      queryParams.delete('cursor');
    } catch (err) {
      error('请求失败:', err.message);
      process.exit(1);
    }
  }

  console.log('');

  const dir = path.dirname(outputPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }

  if (format === 'xlsx') {
    await buildXlsx(
      allCols,
      allRecords,
      allMerges,
      activityTitle,
      outputPath,
      options,
      totalFetched
    );
  } else {
    buildJsonl(allRecords, outputPath, totalFetched);
  }

  // Use validated cache path
  const cacheDir = path.dirname(cachePath);
  if (cacheDir && !fs.existsSync(cacheDir)) {
    fs.mkdirSync(cacheDir, { recursive: true });
  }

  const metaCache = {
    activityId,
    type,
    activityTitle: activityTitle,
    lastExportAt: new Date().toISOString(),
    totalRecords: allRecords.length,
    cols: allCols
  };

  fs.writeFileSync(cachePath, JSON.stringify(metaCache, null, 2));
}

async function buildXlsx(
  allCols,
  allRecords,
  allMerges,
  activityTitle,
  outputPath,
  options,
  totalFetched
) {
  const XLSX = await import('xlsx');

  info('正在生成 xlsx 文件...');

  const headers = allCols.map(col => col.caption);

  const sheetData = [headers, ...allRecords];

  const worksheet = XLSX.utils.aoa_to_sheet(sheetData);

  if (allMerges && allMerges.length > 0) {
    worksheet['!merges'] = allMerges;
  }

  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, '导出数据');

  let xlsxPath = outputPath;
  if (!options.output) {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
    xlsxPath = `./${activityTitle}_${timestamp}.xlsx`;
  }

  XLSX.writeFile(workbook, xlsxPath);

  success(`导出完成!`);
  log(colors.bright, '   导出记录数:', totalFetched);
  if (allMerges.length > 0) {
    log(colors.bright, '   合并单元格:', allMerges.length);
  }
  log(colors.bright, '   保存位置:', xlsxPath);
}

function buildJsonl(allRecords, outputPath, totalFetched) {
  const stream = fs.createWriteStream(outputPath);
  for (const row of allRecords) {
    stream.write(JSON.stringify(row) + '\n');
  }
  stream.end();

  success(`导出完成!`);
  log(colors.bright, '   导出记录数:', totalFetched);
  log(colors.bright, '   保存位置:', outputPath);
}
