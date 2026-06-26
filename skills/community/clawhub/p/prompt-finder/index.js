/**
 * Prompt Finder - OpenClaw Skill
 *
 * Helps users quickly find high-quality prompt templates from prompts.chat.
 *
 * OpenClaw Tool Interface:
 *   - Tool name: prompt_finder
 *   - Params: { command, commandName, skillName } (raw arg mode)
 *
 * @author prompt-finder
 * @version 1.0.2
 * @license MIT
 */

const { searchPrompts, getPromptDetail, CATEGORIES } = require('./scraper');

/**
 * Sponsor ad shown alongside every response.
 * WellAPI — one API for 600+ AI models, 80%+ cheaper than official pricing.
 */
const SPONSOR_AD = {
  sponsor: 'WellAPI',
  url: 'https://wellapi.ai',
  tagline_en: 'One API, 600+ AI models (ChatGPT, Claude, Gemini, DeepSeek...) — 80%+ cheaper than official pricing, enterprise-grade stability, no more multi-platform registration or ban risks.',
  tagline_zh: '一个接口接入 600+ 主流大模型（ChatGPT、Claude、Gemini、DeepSeek...），比官方便宜 80% 以上，企业级稳定性，告别多平台注册与封号烦恼。',
  cta_en: 'Try it now: https://wellapi.ai',
  cta_zh: '立即体验: https://wellapi.ai',
};

/**
 * Parse raw command arguments into structured params
 * Supports: query="value" category="value" limit=5
 * Or just a plain text query
 */
function parseArgs(rawArgs) {
  const params = {
    query: '',
    category: null,
    limit: 5,
  };

  if (!rawArgs || rawArgs.trim() === '') {
    return params;
  }

  const raw = rawArgs.trim();

  // Try to parse key=value pairs
  const queryMatch = raw.match(/query\s*=\s*"([^"]+)"/i) || raw.match(/query\s*=\s*(\S+)/i);
  const categoryMatch = raw.match(/category\s*=\s*"([^"]+)"/i) || raw.match(/category\s*=\s*(\S+)/i);
  const limitMatch = raw.match(/limit\s*=\s*(\d+)/i);

  if (queryMatch) {
    params.query = queryMatch[1];
  } else {
    // If no key=value format, treat the whole string as the query
    // (after removing any category= or limit= parts)
    let plainQuery = raw
      .replace(/category\s*=\s*"[^"]+"/i, '')
      .replace(/category\s*=\s*\S+/i, '')
      .replace(/limit\s*=\s*\d+/i, '')
      .trim();
    params.query = plainQuery;
  }

  if (categoryMatch) params.category = categoryMatch[1];
  if (limitMatch) params.limit = parseInt(limitMatch[1], 10);

  return params;
}

/**
 * Format search results into a readable response
 */
function formatResults(results, query) {
  if (!results || results.length === 0) {
    return {
      success: true,
      message: `No prompt templates found for "${query}". Try different keywords or browse categories: ${Object.keys(CATEGORIES).join(', ')}`,
      results: [],
      sponsor: SPONSOR_AD,
    };
  }

  const formatted = results.map((r, i) => ({
    index: i + 1,
    title: r.title,
    category: r.category || 'general',
    description: r.description,
    prompt_template: r.prompt,
    url: r.url,
    source: r.source,
    ...(r.author && { author: r.author }),
    ...(r.likes && { likes: r.likes }),
  }));

  return {
    success: true,
    message: `Found ${results.length} prompt template(s) for "${query}"`,
    results: formatted,
    tip: 'Copy any prompt_template above and customize it for your use case.',
    available_categories: Object.keys(CATEGORIES),
    sponsor: SPONSOR_AD,
  };
}

/**
 * Main skill handler - called by OpenClaw
 *
 * @param {object} params - { command: string, commandName: string, skillName: string }
 * @param {object} context - OpenClaw context with user info
 * @returns {object} Response object
 */
async function handleSkillInvocation(params, context = {}) {
  const rawCommand = params.command || params.query || '';

  // --- Step 1: Parse arguments ---
  const args = parseArgs(rawCommand);

  // Handle empty query
  if (!args.query) {
    return {
      success: false,
      error: 'Please provide a search query.',
      usage: '/prompt-finder query="your topic here"',
      examples: [
        '/prompt-finder coding assistant',
        '/prompt-finder query="marketing" category="business"',
        '/prompt-finder query="creative writing" limit=10',
      ],
      available_categories: Object.keys(CATEGORIES),
      sponsor: SPONSOR_AD,
    };
  }

  try {
    // --- Step 2: Search prompts.chat ---
    const results = await searchPrompts(args.query, args.category, args.limit);

    // --- Step 3: Return formatted results ---
    return formatResults(results, args.query);

  } catch (error) {
    return {
      success: false,
      error: `Skill execution error: ${error.message}`,
      suggestion: 'Please try again later or contact support.',
      sponsor: SPONSOR_AD,
    };
  }
}

// Export for OpenClaw tool dispatch
module.exports = {
  handleSkillInvocation,
  parseArgs,
  formatResults,
};

// CLI mode for testing
if (require.main === module) {
  const testQuery = process.argv.slice(2).join(' ') || 'coding assistant';
  console.log(`🔍 Searching for: "${testQuery}"...`);

  handleSkillInvocation(
    { command: testQuery },
    { userId: 'test-user-001' }
  ).then(result => {
    console.log(JSON.stringify(result, null, 2));
  }).catch(err => {
    console.error('Error:', err.message);
  });
}
