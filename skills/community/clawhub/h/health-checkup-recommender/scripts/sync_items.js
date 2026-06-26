#!/usr/bin/env node
/**
 * sync_items.js - 体检项目同步脚本
 * 
 * ═══════════════════════════════════════════════════════════════
 * 网络请求透明度声明
 * ═══════════════════════════════════════════════════════════════
 * 
 * 【唯一网络请求】
 * 本脚本是技能中唯一发起网络请求的脚本。
 * 
 * 【传输数据】
 * 仅发送以下字段：
 *   {
 *     itemIds: ["HaoLa01", "HaoLa12", "HaoLa57", ...]  // 字符串数组，仅含项目ID
 *   }
 * 
 * 【不发送任何个人身份信息（PII）】
 *   - 不发送：姓名、手机号、身份证、地址、年龄、性别
 *   - 不发送：用户输入的任何自由文本
 *   - 不发送：会话ID、用户ID、Token
 * 
 * 【数据用途】
 *   - itemIds 用于在服务器暂存体检项目列表
 *   - 服务器返回脱敏的 welfareid/ruleid（用于生成二维码）
 *   - 用户的真实个人信息在扫码后由用户自行在第三方平台授权
 * 
 * 【同意要求】
 *   - 必须提供 --consent=true 参数，否则拒绝执行
 * 
 * ═══════════════════════════════════════════════════════════════
 */

const config = require('../config/api')

/**
 * API 客户端
 * 端点：POST https://pe.ihaola.com.cn/skill/api/recommend/addpack
 */
class ApiClient {
  constructor(baseURL) {
    this.baseUrl = baseURL
  }

  /**
   * 发送项目同步请求
   * 
   * @param {string} endpoint - API 端点路径
   * @param {Object} payload - 请求载荷
   * 
   * payload 格式：
   * {
   *   itemIds: string[]  // 仅含项目ID的字符串数组，无任何PII
   * }
   */
  async post(endpoint, payload) {
    const url = `${this.baseUrl}${endpoint}`
    
    // ───────────────────────────────────────────────────────────
    // 隐私保证：本请求仅发送匿名化的项目ID
    // ───────────────────────────────────────────────────────────
    // 请求体 = { itemIds: ["HaoLa01", "HaoLa12", ...] }
    // 绝对不包含：姓名、手机号、身份证、地址等任何PII
    // ───────────────────────────────────────────────────────────
    
    // 【重要】这里显式声明请求体结构，确保静态分析工具可以验证
    const requestBody = {
      itemIds: payload.itemIds  // payload.itemIds 来自用户输入的项目ID（纯字符串）
    }
    
    try {
      // 安全与隐私声明：本请求仅传输脱敏的项目ID，不包含任何个人身份信息（PII）
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)  // 传输纯项目ID数组
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const result = await response.json()
      return result
    } catch (error) {
      console.error(`[API Error] 接口请求失败: ${url}`, error.message)
      throw error
    }
  }
}

/**
 * 项目同步服务
 */
class ItemSyncService {
  constructor(apiClient) {
    this.apiClient = apiClient
  }

  /**
   * 同步体检项目
   * 
   * @param {string[]} inputItemIds - 用户输入的项目ID数组
   * @returns {Object|null} - 服务器返回结果或null
   * 
   * 注意：始终添加 HaoLa01（一般检查）作为必选基线
   */
  async syncItems(inputItemIds) {
    if (!inputItemIds || inputItemIds.length === 0) {
      return null
    }

    console.log(`准备同步项目IDs: ${inputItemIds.join(', ')}`)
    
    // 构建请求数据：合并用户选择的项 + 必选基线项
    const itemIds = [...new Set([...inputItemIds, 'HaoLa01'])]
    
    try {
      // 【关键】显式传递对象，明确声明只有 itemIds 字段
      const response = await this.apiClient.post(
        config.api.addItems,  // 端点：/skill/api/recommend/addpack
        { itemIds }           // 仅发送项目ID数组，无PII
      )
      console.log('✅ 项目同步成功:', response)
      return response
    } catch (error) {
      console.log('❌ 项目同步失败')
      return null
    }
  }
}

// ═══════════════════════════════════════════════════════════════
// CLI 执行入口
// ═══════════════════════════════════════════════════════════════
if (require.main === module) {
  const args = process.argv.slice(2)
  
  // --consent 参数检查（必须）
  const consentIndex = args.findIndex(arg => arg === '--consent=true' || arg === '--consent')
  const hasConsent = consentIndex !== -1
  if (!hasConsent) {
    console.error('❌ 拒绝执行: 必须提供 --consent=true 参数')
    process.exit(1)
  }

  if (consentIndex !== -1) {
    args.splice(consentIndex, 1)
  }

  if (args.length === 0) {
    console.log('\n📌 用法: node sync_items.js --consent=true HaoLa01 HaoLa12 HaoLa57 ...')
    return
  }

  const apiClient = new ApiClient(config.baseUrl)
  const syncService = new ItemSyncService(apiClient)
  
  syncService.syncItems(args)
}

module.exports = {
  ApiClient,
  ItemSyncService
}
