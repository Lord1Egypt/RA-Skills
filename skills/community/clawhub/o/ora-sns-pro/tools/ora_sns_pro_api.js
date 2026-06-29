/**
 * Ora社媒主页搜索专家 API 调用工具
 * 支持两种查询模式：
 *   A. 关键词搜索（socialMediaQuery）—— 根据关键词 + 社媒平台搜索，最多返回 20 条
 *   B. 域名/企业反查（socialMediaDomainQuery）—— 根据域名/企业名 + 社媒平台反查，最多返回 5 条
 *
 * 鉴权：每次查询直接在请求头携带 AuthToken（无需预先获取 queryToken）
 * 额度：免费用户共 20 次，每次调用扣减 1 次；付费用户可能有单日限额
 *      两个接口共用同一账号额度
 */

/**
 * 从 skills 目录下的 OraAgent.key 文件读取 AuthToken
 * 
 * ⚠️ 每次调用都实时读取，不缓存！
 * 用户可能在两次查询之间去网站支付并更新了 Token 文件，
 * 如果缓存旧 Token，后端无法识别用户为付费用户。
 */
const fs = require('fs');
const path = require('path');

// ══════════════════════════════════════════════
// API 端点白名单
// ══════════════════════════════════════════════

/**
 * 允许发起请求的 API 端点白名单
 * 仅允许向预先注册的端点发送 POST 请求，防止 SSRF 和任意 URL 调用风险
 */
const ALLOWED_URLS = Object.freeze([
  'https://api.topeasychina.com:9443/DomainData/api/skill/socialMediaQuery',
  'https://api.topeasychina.com:9443/DomainData/api/skill/socialMediaDomainQuery'
]);

/**
 * 校验 URL 是否在允许的白名单中
 * @param {string} url - 待校验的 URL
 * @returns {boolean} 是否允许
 */
function isAllowedUrl(url) {
  return ALLOWED_URLS.includes(url);
}

// ══════════════════════════════════════════════
// 安全的 OraAgent.key 路径解析
// ══════════════════════════════════════════════

/**
 * 安全地获取 OraAgent.key 文件的绝对路径
 * 
 * 使用 path.resolve 规范化路径，然后校验解析后的绝对路径
 * 确实位于 skills 根目录内，防止路径遍历攻击。
 * 
 * @returns {string|null} 安全的文件路径；路径不可信时返回 null
 */
function getSafeKeyFilePath() {
  // resolve 会将相对路径解析为绝对路径，并消除 '..' 片段
  const skillsDir = path.resolve(__dirname, '..', '..');
  const keyFilePath = path.resolve(skillsDir, 'OraAgent.key');

  // 规范化后再次 resolve 以确保一致，然后校验文件必须在 skillsDir 内
  const normalizedSkillsDir = path.resolve(skillsDir) + path.sep;
  const normalizedKeyPath = path.resolve(keyFilePath);

  if (!normalizedKeyPath.startsWith(normalizedSkillsDir)) {
    console.log('[SocialMediaAPI] 安全拦截：OraAgent.key 解析路径不在 skills 目录内');
    return null;
  }

  return normalizedKeyPath;
}

/**
 * 实时读取 OraAgent.key 文件中的 AuthToken
 * 使用安全的路径解析，防止路径遍历风险
 * @returns {string} AuthToken 值，文件不存在或为空时返回空字符串
 */
function readAuthToken() {
  try {
    const keyFilePath = getSafeKeyFilePath();
    if (!keyFilePath) {
      console.log('[SocialMediaAPI] 无法安全获取 OraAgent.key 路径，跳过读取');
      return '';
    }
    if (fs.existsSync(keyFilePath)) {
      const token = fs.readFileSync(keyFilePath, 'utf-8').trim();
      if (token) {
        console.log('[SocialMediaAPI] AuthToken 实时读取成功');
        return token;
      }
      console.log('[SocialMediaAPI] OraAgent.key 存在但为空');
      return '';
    }
    console.log('[SocialMediaAPI] OraAgent.key not found at:', keyFilePath);
    return '';
  } catch (e) {
    console.log('[SocialMediaAPI] 读取 OraAgent.key 失败:', e.message);
    return '';
  }
}

class SocialMediaAPI {
  /**
   * @param {string} keywordSearchUrl - 关键词搜索接口（POST），如 /api/skill/socialMediaQuery
   * @param {string} domainSearchUrl  - 域名/企业反查接口（POST），如 /api/skill/socialMediaDomainQuery
   * @param {string} authToken       - 授权令牌（用于 AuthToken 请求头）
   * @param {number} timeout         - 请求超时(ms)，默认 30000
   * @param {string} paymentUrl      - 付费升级链接
   */
  constructor(keywordSearchUrl, domainSearchUrl, authToken, timeout = 30000, paymentUrl = 'https://www.oraskl.com/platform') {
    this.keywordSearchUrl = keywordSearchUrl;
    this.domainSearchUrl = domainSearchUrl;
    // ⚠️ authToken 每次请求前实时从文件读取，此处仅在文件不存在时作为 fallback
    this._fallbackToken = authToken || '';
    this.timeout = timeout;
    this.paymentUrl = paymentUrl;

    // ── 用户状态（从每次 API 响应的 userData 中同步更新）──
    /** @type {boolean} 是否为付费用户 */
    this.payingUser = false;
    /** @type {number} 已使用次数 */
    this.usedCount = 0;
    /** @type {number} 可使用总次数 */
    this.availableUses = 20;

    // ── 最后错误信息 ──
    this.lastErrorMsg = '';
    this.lastErrorCode = 0;
  }

  // ══════════════════════════════════════════════
  // 用户状态更新
  // ══════════════════════════════════════════════

  /**
   * 从 API 响应的 userData 同步用户状态
   * @param {Object} userData - 响应中的 userData 字段
   */
  updateUserData(userData) {
    if (!userData) return;
    this.payingUser = !!userData.payingUser;
    if (userData.usedCount !== undefined && userData.usedCount !== null) {
      this.usedCount = userData.usedCount;
    }
    if (userData.availableUses !== undefined && userData.availableUses !== null) {
      this.availableUses = userData.availableUses;
    }
    console.log('[SocialMediaAPI] UserData updated — payingUser:', this.payingUser, ', usedCount:', this.usedCount, ', availableUses:', this.availableUses);
  }

  /**
   * 记录错误信息（来自 code=500 的响应）
   */
  recordError(msg, code = 500) {
    this.lastErrorMsg = msg || '';
    this.lastErrorCode = code;
  }

  // ══════════════════════════════════════════════
  // 通用请求方法
  // ══════════════════════════════════════════════

  /**
   * 发起 POST 请求到指定 URL
   * @param {string} url     - 接口地址
   * @param {Object} body    - 请求体 JSON
   * @returns {Promise<Object>} { code, msg, userData, data }
   */
  async _post(url, body) {
    // 🛡️ 安全校验：URL 必须在白名单中，防止向任意地址发起请求
    if (!isAllowedUrl(url)) {
      const err = new Error(`安全拦截：不允许向未注册的 URL 发起请求: ${url}`);
      console.error('[SocialMediaAPI]', err.message);
      throw err;
    }

    // ⚠️ 每次请求前实时读取 AuthToken，不缓存
    // 用户在两次查询之间可能已付费并更新了 Token 文件
    const currentAuthToken = readAuthToken() || this._fallbackToken;
    console.log('[SocialMediaAPI] 当前 AuthToken:', currentAuthToken ? `present (first 8 chars: ${currentAuthToken.substring(0, 8)}...)` : 'MISSING');

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'AuthToken': currentAuthToken
        },
        body: JSON.stringify(body),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`API请求失败 (${response.status}): ${errorText}`);
      }

      const result = await response.json();
      console.log('[SocialMediaAPI] _post response:', JSON.stringify(result).substring(0, 300));

      // 同步用户数据
      if (result.userData) {
        this.updateUserData(result.userData);
      } else {
        console.warn('[SocialMediaAPI] ⚠️ API 响应中缺少 userData 字段！无法更新 payingUser 状态。当前 payingUser 保持为:', this.payingUser);
      }

      // 记录错误（仅当非200时）
      if (result.code !== 200) {
        this.recordError(result.msg || '未知错误', result.code);
      } else {
        // 成功响应时清除之前的错误状态，防止残留的额度错误信息污染后续展示
        this.recordError('', 0);
      }

      return result;
    } catch (error) {
      clearTimeout(timeoutId);
      if (error.name === 'AbortError') {
        throw new Error(`请求超时 (${this.timeout}ms)`);
      }
      throw error;
    }
  }

  // ══════════════════════════════════════════════
  // A. 关键词搜索（socialMediaQuery）
  // ══════════════════════════════════════════════

  /**
   * 根据关键词搜索社媒账号
   * POST {keywordSearchUrl}
   * 每次返回最多 20 条数据
   *
   * 🌐 重要：数据源主要是英文，keyword 应为英文关键词。
   * 如用户输入中文，请先翻译为英文后再调用此方法。
   *
   * @param {Object} params
   * @param {string} params.keyword         - 搜索关键词（如 "led", "solar panel"）
   * @param {string} params.socialMediaType - 平台类型: facebook / linkedin / twitter / instagram
   * @returns {Promise<Object>} { code, msg, userData, data: Array }
   */
  async searchByKeyword(params) {
    const { keyword, socialMediaType } = params;

    // 参数校验
    if (!socialMediaType) {
      return {
        code: -1,
        msg: '请指定社媒平台，支持: Facebook、LinkedIn、Twitter/X、Instagram'
      };
    }
    if (!keyword || !keyword.trim()) {
      return {
        code: -1,
        msg: '请提供搜索关键词，例如：led、solar panel、家具'
      };
    }

    // 🌐 检测中文关键词并输出警告
    if (/[\u4e00-\u9fff\u3400-\u4dbf]/u.test(keyword)) {
      console.warn(`[SocialMediaAPI] ⚠️ 关键词 "${keyword}" 包含中文字符！数据源主要是英文数据，中文查询可能匹配不到结果。建议先翻译为英文。`);
    }

    try {
      const result = await this._post(this.keywordSearchUrl, {
        keyword: keyword.trim(),
        socialMediaType: socialMediaType
      });

      return result;
    } catch (error) {
      return {
        code: -1,
        msg: `关键词搜索请求失败: ${error.message}`
      };
    }
  }

  // ══════════════════════════════════════════════
  // B. 域名/企业反查（socialMediaDomainQuery）
  // ══════════════════════════════════════════════

  /**
   * 根据域名或企业名称反查社媒账号
   * POST {domainSearchUrl}
   * 每次返回最多 5 条数据
   *
   * @param {Object} params
   * @param {string} params.companyName     - 企业名称（与 domain 至少填一个）
   * @param {string} params.domain          - 企业域名（与 companyName 至少填一个）
   * @param {string} params.socialMediaType - 平台类型
   * @returns {Promise<Object>} { code, msg, userData, data: Array }
   */
  async searchByDomain(params) {
    const { companyName, domain, socialMediaType } = params;

    // 参数校验
    if (!socialMediaType) {
      return {
        code: -1,
        msg: '请指定社媒平台，支持: Facebook、LinkedIn、Twitter/X、Instagram'
      };
    }
    if ((!companyName || !companyName.trim()) && (!domain || !domain.trim())) {
      return {
        code: -1,
        msg: '请至少提供企业名称或域名其中之一。例如：「查一下 Loyola Medicine 的 LinkedIn」或「查 armaiolo.it 的 Facebook」'
      };
    }

    try {
      const result = await this._post(this.domainSearchUrl, {
        companyName: (companyName || '').trim(),
        domain: (domain || '').trim(),
        socialMediaType: socialMediaType
      });

      return result;
    } catch (error) {
      return {
        code: -1,
        msg: `域名反查请求失败: ${error.message}`
      };
    }
  }

  // ══════════════════════════════════════════════
  // 便捷方法
  // ══════════════════════════════════════════════

  /** 在指定平台按关键词搜索（keyword 应为英文，如含中文请先翻译） */
  async searchKeywordOn(keyword, socialMediaType) {
    if (/[\u4e00-\u9fff\u3400-\u4dbf]/u.test(keyword)) {
      console.warn(`[SocialMediaAPI] ⚠️ searchKeywordOn: 关键词 "${keyword}" 含中文，可能匹配不到结果`);
    }
    return this.searchByKeyword({ keyword, socialMediaType });
  }

  /** 在多个平台按关键词搜索（keyword 应为英文，如含中文请先翻译） */
  async searchKeywordOnAll(keyword, platforms = ['facebook', 'linkedin', 'twitter', 'instagram']) {
    if (/[\u4e00-\u9fff\u3400-\u4dbf]/u.test(keyword)) {
      console.warn(`[SocialMediaAPI] ⚠️ searchKeywordOnAll: 关键词 "${keyword}" 含中文，可能匹配不到结果`);
    }
    const results = {};
    for (const platform of platforms) {
      try {
        const r = await this.searchByKeyword({ keyword, socialMediaType: platform });
        results[platform] = r.code === 200 ? (r.data || []) : [];
      } catch (e) {
        results[platform] = [];
      }
    }
    return results;
  }

  /** 通过企业名称反查指定平台 */
  async searchCompanyOn(companyName, socialMediaType) {
    return this.searchByDomain({ companyName, domain: '', socialMediaType });
  }

  /** 通过域名反查指定平台 */
  async searchDomainOn(domain, socialMediaType) {
    return this.searchByDomain({ companyName: '', domain, socialMediaType });
  }

  // ══════════════════════════════════════════════
  // 获取当前使用量信息
  // ══════════════════════════════════════════════

  /**
   * 获取当前使用量摘要
   * @returns {{payingUser: boolean, availableUses: number, usedCount: number, paymentUrl: string}}
   */
  getUsageInfo() {
    return {
      payingUser: this.payingUser,
      availableUses: this.availableUses,
      usedCount: this.usedCount,
      paymentUrl: this.paymentUrl
    };
  }

  /**
   * 生成尾部提示文本
   * 根据 payingUser 和额度状态自动选择模板
   * 
   * ⚠️ 重要原则：仅在 API 明确返回 code=500 错误时才显示"额度耗尽"相关提示。
   * 禁止基于本地 usedCount/availableUses 计数自行判断额度是否用完。
   * 后端接口是额度状态的唯一权威来源。
   * 
   * @returns {string}
   */
  getUsageFooter() {
    // ── 付费用户 ──
    if (this.payingUser) {
      // 仅当 API 明确返回"当日超额"错误时才展示限额提示
      if (this.lastErrorCode === 500 && this.lastErrorMsg.includes('当日请求次数已达上限')) {
        return `\n---\n⚠️ **当日请求次数已达上限，额度将在次日 0 点自动重置。**\n\n💎 如需提升日限额或其他支持，请联系客服。`;
      }
      // 付费用户正常情况：仅展示续费链接，不展示任何额度用尽的提示
      return `\n---\n💎 **您已是付费用户，如需续费 →** [点击续费](${this.paymentUrl})`;
    }

    // ── 免费用户：仅当 API 明确返回"免费额度已用完"错误时才展示额度耗尽提示 ──
    // ⚠️ 不再基于 usedCount >= availableUses 的本地计数自行判断
    if (this.lastErrorCode === 500 && this.lastErrorMsg.includes('免费额度已用完')) {
      return `\n---\n❌ **免费额度已用完（${this.usedCount}/${this.availableUses}次）**\n\n🔓 [立即升级包年 →](${this.paymentUrl})`;
    }

    // ── 免费用户：正常展示（仅展示使用量信息，不声明额度已用完）──
    return `\n---\n🆓 **免费额度:** 可免费使用 ${this.availableUses} 次，当前已使用 ${this.usedCount} 次\n🔓 [升级包年 →](${this.paymentUrl})`;
  }
}

// 对外暴露安全校验工具方法，供 handler 等调用方使用
SocialMediaAPI.isAllowedUrl = isAllowedUrl;
SocialMediaAPI.ALLOWED_URLS = ALLOWED_URLS;

module.exports = SocialMediaAPI;
