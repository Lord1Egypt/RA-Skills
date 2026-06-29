/**
 * Ora社媒主页搜索专家 Skill Handler
 * 适配 OpenClaw 框架
 *
 * 两种查询模式：
 *   A. 关键词搜索 — 根据关键词 + 社媒类型搜索社媒账号，最多返回 20 条
 *   B. 域名/企业反查 — 根据企业名称或域名反查社媒账号，最多返回 5 条
 *
 * 鉴权：每次查询直接在请求头携带 AuthToken（无需预鉴权获取 queryToken）
 *       ⚠️ AuthToken 由 ora_sns_pro_api.js 内部实时从 OraAgent.key 读取，此处不再缓存
 * 额度：免费用户共 20 次，每次调用扣 1 次；付费用户可能有单日限额
 *      关键词搜索和域名反查共用同一账号额度
 */

const SocialMediaAPI = require('../tools/ora_sns_pro_api');

class SocialMediaHandler {
  constructor(config) {
    this.keywordSearchUrl = config.keyword_search_url || 'https://api.topeasychina.com:9443/DomainData/api/skill/socialMediaQuery';
    this.domainSearchUrl = config.domain_search_url || 'https://api.topeasychina.com:9443/DomainData/api/skill/socialMediaDomainQuery';

    // 🛡️ 安全校验：URL 必须在白名单中，防止恶意配置注入（防御纵深）
    if (!SocialMediaAPI.isAllowedUrl(this.keywordSearchUrl)) {
      throw new Error(`安全拦截：keyword_search_url 不在允许的白名单中: ${this.keywordSearchUrl}`);
    }
    if (!SocialMediaAPI.isAllowedUrl(this.domainSearchUrl)) {
      throw new Error(`安全拦截：domain_search_url 不在允许的白名单中: ${this.domainSearchUrl}`);
    }

    // ⚠️ 不再缓存 AuthToken — 由 ora_sns_pro_api.js 内部实时从 OraAgent.key 读取
    this.timeout = config.timeout || 30000;
    this.paymentUrl = config.payment_url || 'https://www.oraskl.com/platform';

    // 初始化 API 客户端（authToken 参数传空字符串，API 内部会实时读取文件）
    this.api = new SocialMediaAPI(
      this.keywordSearchUrl,
      this.domainSearchUrl,
      '',
      this.timeout,
      this.paymentUrl
    );
  }

  /**
   * 检测文本是否包含中文字符
   * @param {string} text
   * @returns {boolean}
   */
  _containsChinese(text) {
    return /[\u4e00-\u9fff\u3400-\u4dbf]/u.test(text);
  }

  /**
   * 检测用户是否明确要求使用中文查询
   * 匹配例如：「用中文搜」「必须用中文」「不要翻译」「中文查询」等
   * @param {string} input
   * @returns {boolean}
   */
  _userRequestedChineseSearch(input) {
    return /(用中文|必须中文|不要翻译|别翻译|中文搜索|中文查询|中文检索|原词|保留中文)/i.test(input);
  }

  /**
   * 处理请求入口
   */
  async handle(request) {
    const { user_input, params } = request;

    // 从用户输入中提取参数
    const extracted = this.extractParams(user_input, params);

    // 参数校验
    const validationError = this.validateParams(extracted);
    if (validationError) {
      return this.buildResponse('error', validationError);
    }

    // ── 根据搜索意图分流 ──
    if (extracted.searchMode === 'keyword') {
      return await this.handleKeywordSearch(extracted);
    } else {
      return await this.handleDomainSearch(extracted);
    }
  }

  // ══════════════════════════════════════════════
  // A. 关键词搜索处理
  // ══════════════════════════════════════════════

  async handleKeywordSearch(extracted) {
    const { keywords, socialMediaType } = extracted;
    const results = [];
    let errorCount = 0;
    let stopped = false;
    let stopReason = '';

    // 🌐 中文关键词检测：提醒调用方应当先翻译为英文
    for (const kw of keywords) {
      if (this._containsChinese(kw)) {
        console.warn(`[SocialMediaHandler] ⚠️ 关键词 "${kw}" 包含中文字符！数据源主要是英文数据，中文关键词可能匹配不到结果。请先将关键词翻译为英文后再查询。`);
      }
    }

    for (const kw of keywords) {
      if (stopped) break;

      try {
        const result = await this.api.searchByKeyword({
          keyword: kw,
          socialMediaType
        });

        if (result.code === 200) {
          results.push({
            keyword: kw,
            data: Array.isArray(result.data) ? result.data : [],
            count: Array.isArray(result.data) ? result.data.length : 0
          });
        } else if (result.code === 500) {
          // 处理三种错误
          const msg = result.msg || '';
          if (msg.includes('免费额度已用完') || msg.includes('当日请求次数已达上限')) {
            stopped = true;
            stopReason = msg;
            // 把当前结果也标记一下，不继续了
          } else if (msg.includes('鉴权失败')) {
            return this.buildResponse('error', `❌ **鉴权失败，请检查 AuthToken 配置。**\n\n请确保 skills 目录下的 \`OraAgent.key\` 文件内容正确。`);
          } else {
            errorCount++;
          }
        } else {
          // 前端参数错误等情况
          errorCount++;
        }
      } catch (err) {
        errorCount++;
      }
    }

    return this.formatKeywordResults(results, extracted, errorCount, stopped ? stopReason : null);
  }

  /**
   * 格式化关键词搜索结果
   */
  formatKeywordResults(results, extracted, errorCount, stopReason) {
    const platformNames = {
      'facebook': 'Facebook',
      'linkedin': 'LinkedIn',
      'twitter': 'Twitter/X',
      'instagram': 'Instagram'
    };
    const platformName = platformNames[extracted.socialMediaType] || extracted.socialMediaType;
    const totalHits = results.reduce((sum, r) => sum + r.count, 0);

    let content = `## 🔍 ${platformName} 关键词搜索结果\n\n`;
    content += `**搜索关键词:** ${extracted.keywords.join(', ')}\n`;
    content += `**共查询 ${results.length + (this._stopCount || 0)} 个关键词，获取 ${totalHits} 条结果**`;
    if (errorCount > 0) content += `，${errorCount} 条查询失败`;
    content += `\n---\n\n`;

    if (stopReason) {
      if (stopReason.includes('免费额度已用完')) {
        content += `> ⚠️ 查询过程中免费额度已用完，以下为额度耗尽前已获取的结果。\n\n`;
      } else if (stopReason.includes('当日请求次数已达上限')) {
        content += `> ⚠️ 当日请求次数已达上限，以下为限额用尽前已获取的结果。额度将在次日 0 点自动重置。\n\n`;
      }
    }

    if (results.length === 0 && !stopReason) {
      content += '未找到匹配的社媒账号，请尝试更换关键词。';
    } else if (results.length === 0 && stopReason) {
      content += '额度已用完，未能获取任何结果。';
    } else {
      for (const item of results) {
        content += `### 📌 关键词: "${item.keyword}"（${item.count} 条）\n`;
        if (item.count === 0) {
          content += '未找到相关社媒账号\n\n';
          continue;
        }
        for (let i = 0; i < item.data.length; i++) {
          const d = item.data[i];
          content += `- **${d.title || '未命名'}**\n`;
          content += `  - 🔗 社媒主页: ${d.social_media_url || '-'}\n`;
          if (d.url) content += `  - 🌐 官网: ${d.url}\n`;
          if (d.country_tag) content += `  - 🇺🇸 国家: ${d.country_tag.toUpperCase()}\n`;
          if (d.keywords) {
            const kw = d.keywords.length > 150 ? d.keywords.substring(0, 150) + '...' : d.keywords;
            content += `  - 🏷️ 标签: ${kw}\n`;
          }
          if (d.description) {
            const desc = d.description.length > 200 ? d.description.substring(0, 200) + '...' : d.description;
            content += `  - 📝 简介: ${desc}\n`;
          }
          content += `\n`;
        }
      }
    }

    // 追加额度信息
    content += this.api.getUsageFooter();

    return this.buildResponse('success', content, {
      results,
      total: totalHits,
      errors: errorCount,
      stopped: !!stopReason,
      stopReason: stopReason || ''
    });
  }

  // ══════════════════════════════════════════════
  // B. 域名/企业反查处理
  // ══════════════════════════════════════════════

  async handleDomainSearch(extracted) {
    const { queries, socialMediaType } = extracted;
    const results = [];
    let errorCount = 0;
    let stopped = false;
    let stopReason = '';

    for (const query of queries) {
      if (stopped) break;

      try {
        const result = await this.api.searchByDomain({
          companyName: query.companyName || '',
          domain: query.domain || '',
          socialMediaType
        });

        if (result.code === 200) {
          results.push({
            label: query.companyName || query.domain,
            companyName: query.companyName || '',
            domain: query.domain || '',
            data: Array.isArray(result.data) ? result.data : [],
            count: Array.isArray(result.data) ? result.data.length : 0
          });
        } else if (result.code === 500) {
          const msg = result.msg || '';
          if (msg.includes('免费额度已用完') || msg.includes('当日请求次数已达上限')) {
            stopped = true;
            stopReason = msg;
          } else if (msg.includes('鉴权失败')) {
            return this.buildResponse('error', `❌ **鉴权失败，请检查 AuthToken 配置。**\n\n请确保 skills 目录下的 \`OraAgent.key\` 文件内容正确。`);
          } else {
            errorCount++;
          }
        } else {
          errorCount++;
        }
      } catch (err) {
        errorCount++;
      }
    }

    return this.formatDomainResults(results, extracted, errorCount, stopped ? stopReason : null);
  }

  /**
   * 格式化域名/企业反查结果
   */
  formatDomainResults(results, extracted, errorCount, stopReason) {
    const platformNames = {
      'facebook': 'Facebook',
      'linkedin': 'LinkedIn',
      'twitter': 'Twitter/X',
      'instagram': 'Instagram'
    };
    const platformName = platformNames[extracted.socialMediaType] || extracted.socialMediaType;
    const totalHits = results.reduce((sum, r) => sum + r.count, 0);

    let content = `## 🔍 ${platformName} 企业社媒查询结果\n\n`;
    content += `**共查询 ${results.length + errorCount} 个目标，获取 ${totalHits} 条结果**`;
    if (errorCount > 0) content += `，${errorCount} 条查询失败`;
    content += `\n---\n\n`;

    if (stopReason) {
      if (stopReason.includes('免费额度已用完')) {
        content += `> ⚠️ 查询过程中免费额度已用完，以下为额度耗尽前已获取的结果。\n\n`;
      } else if (stopReason.includes('当日请求次数已达上限')) {
        content += `> ⚠️ 当日请求次数已达上限，以下为限额用尽前已获取的结果。额度将在次日 0 点自动重置。\n\n`;
      }
    }

    if (results.length === 0 && !stopReason) {
      content += '未找到匹配的社媒账号，请尝试更换企业名称或域名。';
    } else if (results.length === 0 && stopReason) {
      content += '额度已用完，未能获取任何结果。';
    } else {
      for (const item of results) {
        content += `### 📌 ${item.label}\n`;
        if (item.count === 0) {
          content += '未找到相关社媒账号\n\n';
          continue;
        }
        for (let i = 0; i < item.data.length; i++) {
          const d = item.data[i];
          content += `- **${d.title || '未命名'}**\n`;
          content += `  - 🔗 社媒主页: ${d.social_media_url || '-'}\n`;
          if (d.url) content += `  - 🌐 官网: ${d.url}\n`;
          if (d.country_tag) content += `  - 🇺🇸 国家: ${d.country_tag.toUpperCase()}\n`;
          if (d.keywords) {
            const kw = d.keywords.length > 150 ? d.keywords.substring(0, 150) + '...' : d.keywords;
            content += `  - 🏷️ 标签: ${kw}\n`;
          }
          if (d.description) {
            const desc = d.description.length > 200 ? d.description.substring(0, 200) + '...' : d.description;
            content += `  - 📝 简介: ${desc}\n`;
          }
          content += `\n`;
        }
      }
    }

    // 追加额度信息
    content += this.api.getUsageFooter();

    return this.buildResponse('success', content, {
      results,
      total: totalHits,
      errors: errorCount,
      stopped: !!stopReason,
      stopReason: stopReason || ''
    });
  }

  // ══════════════════════════════════════════════
  // 参数提取与校验
  // ══════════════════════════════════════════════

  /**
   * 参数校验
   */
  validateParams(params) {
    if (!params.socialMediaType) {
      return '请指定社媒平台，支持: LinkedIn、Facebook、Twitter/X、Instagram';
    }
    if (params.searchMode === 'keyword' && (!params.keywords || params.keywords.length === 0)) {
      return '请提供搜索关键词，例如：「搜索 LED」「LinkedIn 搜索 solar panel」';
    }
    if (params.searchMode === 'domain' && (!params.queries || params.queries.length === 0)) {
      return '请至少提供企业名称或域名其中之一。例如：「查一下 Loyola Medicine 的 LinkedIn」或「查 armaiolo.it 的 Facebook」';
    }
    return null;
  }

  /**
   * 从用户输入中提取参数
   * 自动判断搜索模式：关键词搜索 vs 域名/企业反查
   *
   * @param {string} input - 用户原始输入
   * @param {Object} overrideParams - 显式传入的参数（可覆盖自动提取）
   * @returns {Object} { searchMode, socialMediaType, keywords: [], queries: [] }
   */
  extractParams(input, overrideParams) {
    const result = {
      searchMode: 'domain',    // 默认域名/企业反查模式
      socialMediaType: '',
      keywords: [],
      queries: []              // [{companyName, domain}]
    };

    const domainPattern = /([a-zA-Z0-9][-a-zA-Z0-9]*\.)+(com|org|net|cn|io|co|uk|de|jp|fr|kr|us|ca|au|it|es|nl|se|br|in|ru|pl|ch|be|at|no|dk|fi|pt|mx|ar|sg|hk|tw|nz|ie|za|info|biz|tv|me|cc|xyz|top|tech|online|store|shop|website|club|site|link|live|world|icu|fun|wiki|design|ink|pro|dev|app|gov|edu|mil|int)/ig;

    // ── 1. 识别社媒平台类型 ──
    const platformPatterns = [
      { pattern: /(facebook|fb)(\s|$|搜|查|找|上|的|账号|主页|社媒)/i, type: 'facebook' },
      { pattern: /(linkedin|领英)(\s|$|搜|查|找|上|的|账号|主页|社媒)/i, type: 'linkedin' },
      { pattern: /(twitter|推特|twitter)(\s|$|搜|查|找|上|的|账号|主页|社媒)/i, type: 'twitter' },
      { pattern: /(instagram|ins|ig)(\s|$|搜|查|找|上|的|账号|主页|社媒)/i, type: 'instagram' }
    ];

    for (const { pattern, type } of platformPatterns) {
      if (pattern.test(input)) {
        result.socialMediaType = type;
        break;
      }
    }

    // 宽松匹配兜底
    if (!result.socialMediaType) {
      const loosePatterns = [
        { pattern: /facebook|fb/i, type: 'facebook' },
        { pattern: /linkedin|领英/i, type: 'linkedin' },
        { pattern: /twitter|推特/i, type: 'twitter' },
        { pattern: /instagram|ins|ig/i, type: 'instagram' }
      ];
      for (const { pattern, type } of loosePatterns) {
        if (pattern.test(input)) {
          result.socialMediaType = type;
          break;
        }
      }
    }

    // ── 2. 识别域名 ──
    const domainMatches = input.match(domainPattern);
    let foundDomain = '';
    if (domainMatches && domainMatches.length > 0) {
      foundDomain = domainMatches[0].toLowerCase();
    }

    // ── 3. 提取企业名称（域名反查模式）──
    // 优先从引号中提取
    let companyName = '';
    const quoteMatch = input.match(/["""「『](.+?)[""」』]/);
    if (quoteMatch) {
      const candidate = quoteMatch[1].trim();
      if (!domainPattern.test(candidate) && candidate.length > 1) {
        companyName = candidate;
      }
    }

    // "查/找 + 实体 + 的/在 + 平台" 模式 → 域名反查
    if (!companyName) {
      const companyRx = /(?:查一下|查询|查找|查|找一下|找|帮我查|帮我找)\s*(.+?)\s*(?:的|在|上)\s*(?:社媒|社交|facebook|linkedin|twitter|instagram|fb|领英|推特|ins|ig)(?:\s*(?:账号|主页|页面))?$/i;
      const m = input.match(companyRx);
      if (m) {
        const c = m[1].trim().replace(/\b(facebook|linkedin|twitter|instagram|fb|领英|推特|ins|ig)\b/gi, '').trim();
        if (c.length > 0) companyName = c;
      }
    }

    // ── 4. 提取关键词（关键词搜索模式）──
    let keywordMatch = null;
    if (!companyName && !foundDomain) {
      // 模式A: "平台 + 搜/搜索 + 关键词" → "LinkedIn 搜 solar panel"
      const m1 = input.match(/(?:在)?\s*(facebook|linkedin|twitter|instagram|fb|领英|推特|ins|ig)\s*(?:上)?\s*(?:搜索|搜一下|搜|查找|找|查)\s*(.+)/i);
      if (m1) keywordMatch = (m1[2] || '').trim();
    }
    if (!companyName && !foundDomain && !keywordMatch) {
      // 模式B: "搜索/搜 + 关键词" → "搜索 LED", "搜 furniture"
      const m2 = input.match(/^(?:搜索|搜一下|搜)\s*(?:关键词|关键字)?\s*[:：]?\s*(.+)/i);
      if (m2) keywordMatch = (m2[1] || '').trim();
    }
    if (keywordMatch) {
      // 清理尾部残留的平台名
      keywordMatch = keywordMatch.replace(/\s*(?:的|在|上)?\s*(?:facebook|linkedin|twitter|instagram|fb|领英|推特|ins|ig)\s*(?:账号|主页|页面)?\s*$/gi, '').trim();
    }

    // 🌐 标记：关键词是否含中文、用户是否要求中文搜索
    const needsChineseTranslation = keywordMatch && this._containsChinese(keywordMatch) && !this._userRequestedChineseSearch(input);

    // ── 5. 确定搜索模式 ──
    if (foundDomain || companyName) {
      result.searchMode = 'domain';
      result.queries = [{
        companyName: companyName || '',
        domain: foundDomain || ''
      }];
    } else if (keywordMatch) {
      result.searchMode = 'keyword';
      result.keywords = [keywordMatch];
      // 🌐 标记是否需要翻译：关键词含中文 且 用户未明确要求中文搜索
      result._needsChineseTranslation = needsChineseTranslation;
      if (needsChineseTranslation) {
        console.log(`[SocialMediaHandler] ⚠️ 关键词 "${keywordMatch}" 含中文，需要翻译为英文后再查询`);
      }
    } else {
      // 都不明确 → 把整个输入去噪后当关键词
      let cleaned = input
        .replace(/\b(查询一下|查询|搜索一下|搜索|搜一下|搜|找一下|找|帮我查|帮我找|帮我搜|查一下|查|的|在|上)\b/g, ' ')
        .replace(/\b(facebook|linkedin|twitter|instagram|fb|领英|推特|ins|ig|社媒|社交|账号|主页|页面)\b/gi, ' ')
        .replace(/\s+/g, ' ')
        .trim();
      if (cleaned.length > 1 && !domainPattern.test(cleaned)) {
        result.searchMode = 'keyword';
        result.keywords = [cleaned];
        // 🌐 标记是否需要翻译
        if (this._containsChinese(cleaned) && !this._userRequestedChineseSearch(input)) {
          result._needsChineseTranslation = true;
          console.log(`[SocialMediaHandler] ⚠️ fallback 关键词 "${cleaned}" 含中文，需要翻译为英文后再查询`);
        }
      }
    }

    // ── 6. 批量查询支持 ──
    // 如果用户提供了用逗号、顿号、换行分隔的列表
    if (result.searchMode === 'keyword' && result.keywords.length === 1) {
      const kw = result.keywords[0];
      // 检测是否为逗号/换行分隔的多个关键词
      const parts = kw.split(/[,，、\n]+/).map(s => s.trim()).filter(s => s.length > 0);
      if (parts.length > 1) {
        result.keywords = parts;
        // 🌐 批量关键词：检查每个是否含中文且用户未要求中文搜索
        const hasChineseKws = parts.some(p => this._containsChinese(p));
        const userWantsChinese = this._userRequestedChineseSearch(input);
        if (hasChineseKws && !userWantsChinese) {
          result._needsChineseTranslation = true;
          console.log(`[SocialMediaHandler] ⚠️ 批量关键词含中文，需要翻译为英文后再查询`);
        }
      }
    }

    if (result.searchMode === 'domain' && result.queries.length === 1) {
      const q = result.queries[0];
      const label = q.companyName || q.domain;
      if (label) {
        const parts = label.split(/[,，、\n]+/).map(s => s.trim()).filter(s => s.length > 0);
        if (parts.length > 1) {
          result.queries = parts.map(p => {
            const isDomain = domainPattern.test(p);
            domainPattern.lastIndex = 0; // 重置 regex
            return {
              companyName: isDomain ? '' : p,
              domain: isDomain ? p : ''
            };
          });
        }
      }
    }

    // ── 7. 显式参数覆盖 ──
    if (overrideParams) {
      if (overrideParams.searchMode) result.searchMode = overrideParams.searchMode;
      if (overrideParams.socialMediaType) result.socialMediaType = overrideParams.socialMediaType;
      if (overrideParams.keywords) result.keywords = overrideParams.keywords;
      if (overrideParams.queries) result.queries = overrideParams.queries;
      if (overrideParams.companyName || overrideParams.domain) {
        result.searchMode = 'domain';
        result.queries = [{
          companyName: overrideParams.companyName || '',
          domain: overrideParams.domain || ''
        }];
      }
    }

    return result;
  }

  /**
   * 构建标准响应
   */
  buildResponse(status, message, data = null) {
    return {
      status,
      message,
      data,
      timestamp: new Date().toISOString()
    };
  }
}

module.exports = SocialMediaHandler;
