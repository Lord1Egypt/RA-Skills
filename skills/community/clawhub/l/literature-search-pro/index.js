/**
 * Literature Search Pro - Entry Point
 * 
 * Multi-source academic literature search with deduplication.
 * Integrates OpenAlex, Semantic Scholar, and arXiv.
 */

const { exec } = require('child_process');
const { promisify } = require('util');
const fs = require('fs').promises;
const path = require('path');

const execAsync = promisify(exec);

const SKILL_DIR = path.join(__dirname);
const SEARCH_SCRIPT = path.join(SKILL_DIR, 'search.py');
const CACHE_DIR = path.join(SKILL_DIR, 'cache');

/**
 * Search academic literature
 * @param {Object} options - Search options
 * @param {string} options.query - Search query
 * @param {number} options.limit - Max results (default: 10)
 * @param {number} options.yearMin - Minimum year (default: 2020)
 * @param {Array} options.sources - Data sources ['openalex', 'semantic_scholar', 'arxiv']
 * @param {boolean} options.deduplicate - Enable deduplication (default: true)
 * @param {boolean} options.refresh - Force refresh cache (default: false)
 * @returns {Promise<Object>} - Search results
 */
async function search(options) {
  const {
    query,
    limit = 10,
    yearMin = 2020,
    sources = ['openalex', 'semantic_scholar', 'arxiv'],
    deduplicate = true,
    refresh = false,
  } = options;

  if (!query) {
    throw new Error('Search query is required');
  }

  console.log(`📚 Searching literature: "${query}"`);
  console.log(`   Limit: ${limit}, Year >= ${yearMin}, Sources: ${sources.join(', ')}`);

  try {
    // Ensure cache directory exists
    await fs.mkdir(CACHE_DIR, { recursive: true });

    // Build command
    const args = [
      `"${query}"`,
      `--limit ${limit}`,
      `--year-min ${yearMin}`,
      `--sources ${sources.join(',')}`,
      deduplicate ? '--deduplicate' : '',
      refresh ? '--refresh' : '',
    ].filter(Boolean).join(' ');

    const command = `python "${SEARCH_SCRIPT}" ${args}`;

    const { stdout, stderr } = await execAsync(command, {
      cwd: SKILL_DIR,
      timeout: 300000, // 5 minutes
      maxBuffer: 10 * 1024 * 1024,
    });

    if (stderr && !stderr.includes('WARNING')) {
      console.warn('Search warnings:', stderr);
    }

    // Parse JSON output
    const results = JSON.parse(stdout);

    return {
      success: true,
      query,
      total: results.total,
      papers: results.papers,
      message: formatResults(results),
    };
  } catch (error) {
    console.error('❌ Literature search failed:', error.message);
    return {
      success: false,
      query,
      error: error.message,
      suggestions: getSearchSuggestions(error),
    };
  }
}

/**
 * Format search results for human reading
 */
function formatResults(results) {
  const lines = [
    `✅ 找到 ${results.total} 篇相关论文（已去重）`,
    '',
    '--- 搜索结果 ---',
    '',
  ];

  results.papers.slice(0, 10).forEach((paper, idx) => {
    lines.push(`**${idx + 1}. ${paper.title}**`);
    lines.push(`   - 作者：${paper.authors?.slice(0, 3).join(', ')}${paper.authors?.length > 3 ? ' 等' : ''}`);
    lines.push(`   - 年份：${paper.year}`);
    lines.push(`   -  venue: ${paper.venue || 'N/A'}`);
    lines.push(`   - 引用：${paper.citation_count || 0}`);
    if (paper.doi) lines.push(`   - DOI: ${paper.doi}`);
    if (paper.arxiv_id) lines.push(`   - arXiv: ${paper.arxiv_id}`);
    lines.push(`   - 摘要：${paper.abstract?.slice(0, 200)}${paper.abstract?.length > 200 ? '...' : ''}`);
    lines.push('');
  });

  if (results.papers.length > 10) {
    lines.push(`... 还有 ${results.papers.length - 10} 篇，查看完整结果获取全部列表`);
  }

  return lines.join('\n');
}

/**
 * Get troubleshooting suggestions
 */
function getSearchSuggestions(error) {
  const message = error.message.toLowerCase();
  
  if (message.includes('network') || message.includes('connection')) {
    return '检查网络连接，确保可以访问 OpenAlex/Semantic Scholar/arXiv';
  }
  if (message.includes('timeout')) {
    return '搜索超时，尝试减少返回数量或使用 --refresh 刷新缓存';
  }
  if (message.includes('parse') || message.includes('json')) {
    return '解析结果失败，尝试 --refresh 强制刷新缓存';
  }
  if (message.includes('api') || message.includes('rate limit')) {
    return 'API 限额，等待几分钟后重试或配置 Semantic Scholar API Key';
  }
  
  return '检查搜索词是否正确，或尝试更宽泛的关键词';
}

// Export for OpenClaw skill system
module.exports = {
  search,
};
