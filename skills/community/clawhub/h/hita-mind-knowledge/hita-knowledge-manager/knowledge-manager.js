/**
 * Knowledge Manager - 知识库智能管理器
 * 
 * 实现知识库的三层管理：
 * L1 热数据: 最近使用/高频/核心规则，完整内容
 * L2 温数据: 中期知识，保留摘要+标签
 * L3 冷数据: 历史归档，只保留元数据索引
 */

const fs = require('fs')
const path = require('path')

// ============== 默认配置 ==============

const DEFAULT_CONFIG = {
  layerThresholds: {
    L1ToL2Days: 30,
    L2ToL3Days: 90,
    maxL1Items: 50,
    maxL2Items: 200,
  },
  autoCompress: {
    enabled: true,
    scheduleCron: '0 3 * * *',
  },
  summaryLength: 200,
}

// ============== 核心类 ==============

class KnowledgeManager {
  /**
   * @param {string} storePath - 存储文件路径
   * @param {object} config - 配置（可选）
   */
  constructor(storePath = './knowledge-store.json', config = {}) {
    this.storePath = storePath
    this.config = { ...DEFAULT_CONFIG, ...config }
    this.store = this.loadStore()
  }

  /**
   * 加载存储
   */
  loadStore() {
    if (fs.existsSync(this.storePath)) {
      try {
        const data = fs.readFileSync(this.storePath, 'utf-8')
        return JSON.parse(data)
      } catch (e) {
        console.warn('[KnowledgeManager] 存储文件损坏，重新创建')
      }
    }
    return this.createEmptyStore()
  }

  /**
   * 创建空存储
   */
  createEmptyStore() {
    return {
      version: 1,
      lastModified: new Date().toISOString(),
      items: {},
      stats: {
        totalItems: 0,
        byLayer: { L1: 0, L2: 0, L3: 0 },
        byPriority: { high: 0, medium: 0, low: 0 },
      },
    }
  }

  /**
   * 保存存储
   */
  saveStore() {
    this.store.lastModified = new Date().toISOString()
    fs.writeFileSync(this.storePath, JSON.stringify(this.store, null, 2), 'utf-8')
  }

  /**
   * 更新统计
   */
  updateStats() {
    const stats = {
      totalItems: Object.keys(this.store.items).length,
      byLayer: { L1: 0, L2: 0, L3: 0 },
      byPriority: { high: 0, medium: 0, low: 0 },
    }
    for (const item of Object.values(this.store.items)) {
      stats.byLayer[item.layer]++
      stats.byPriority[item.priority]++
    }
    this.store.stats = stats
  }

  // ============== CRUD 操作 ==============

  /**
   * 添加知识条目
   */
  add({ title, layer = 'L1', tags = [], priority = 'medium', summary, fullContent, content }) {
    const id = this._generateId(title)
    const now = new Date().toISOString()

    const inputContent = summary || content || ''
    const maxLen = this.config.summaryLength || 200

    const actualFullContent = layer === 'L1' ? inputContent : undefined
    const actualSummary = inputContent.length > maxLen 
      ? inputContent.substring(0, maxLen) + '...'
      : inputContent

    const newItem = {
      id,
      title,
      layer,
      tags,
      priority,
      summary: actualSummary,
      fullContent: actualFullContent,
      accessCount: 0,
      lastAccess: null,
      compressedAt: null,
      archivedAt: null,
      createdAt: now,
      updatedAt: now,
    }

    this.store.items[id] = newItem
    this._enforceLayerLimits(layer)
    this.updateStats()
    this.saveStore()

    console.log(`[KnowledgeManager] 添加: ${title} → ${layer}`)
    return newItem
  }

  /**
   * 生成唯一ID
   */
  _generateId(title) {
    const base = title
      .toLowerCase()
      .replace(/[^a-z0-9\u4e00-\u9fa5]/g, '-')
      .substring(0, 30)
    const timestamp = Date.now().toString(36)
    return `${base}-${timestamp}`
  }

  /**
   * 获取知识条目
   */
  get(id) {
    const item = this.store.items[id]
    if (item) {
      item.accessCount++
      item.lastAccess = new Date().toISOString()
      this.saveStore()
    }
    return item || null
  }

  /**
   * 更新知识条目
   */
  update(id, updates) {
    const item = this.store.items[id]
    if (!item) return null

    const updated = {
      ...item,
      ...updates,
      id: item.id,
      createdAt: item.createdAt,
      updatedAt: new Date().toISOString(),
    }

    this.store.items[id] = updated
    this.updateStats()
    this.saveStore()
    return updated
  }

  /**
   * 删除知识条目
   */
  delete(id) {
    if (!this.store.items[id]) return false
    delete this.store.items[id]
    this.updateStats()
    this.saveStore()
    return true
  }

  /**
   * 列出所有知识
   */
  list(layer = null, options = {}) {
    let items = Object.values(this.store.items)

    if (layer) {
      items = items.filter(item => item.layer === layer)
    }

    items.sort((a, b) => {
      const timeA = a.lastAccess || a.createdAt
      const timeB = b.lastAccess || b.createdAt
      return timeB.localeCompare(timeA)
    })

    const offset = options.offset || 0
    const limit = options.limit || items.length
    return items.slice(offset, offset + limit)
  }

  // ============== 搜索 ==============

  /**
   * 搜索知识
   */
  search({ query, tags = [], layer = null, limit = 20 }) {
    let items = Object.values(this.store.items)

    if (layer) {
      items = items.filter(item => item.layer === layer)
    }

    if (tags.length > 0) {
      items = items.filter(item => tags.some(tag => item.tags.includes(tag)))
    }

    if (query) {
      const lowerQuery = query.toLowerCase()
      items = items.filter(item => {
        if (item.layer === 'L1' && item.fullContent) {
          return item.fullContent.toLowerCase().includes(lowerQuery)
        }
        return (
          item.title.toLowerCase().includes(lowerQuery) ||
          item.summary.toLowerCase().includes(lowerQuery) ||
          item.tags.some(tag => tag.toLowerCase().includes(lowerQuery))
        )
      })
    }

    const priorityOrder = { high: 0, medium: 1, low: 2 }
    items.sort((a, b) => {
      if (priorityOrder[a.priority] !== priorityOrder[b.priority]) {
        return priorityOrder[a.priority] - priorityOrder[b.priority]
      }
      return b.accessCount - a.accessCount
    })

    return items.slice(0, limit)
  }

  // ============== 分层压缩 ==============

  /**
   * 强制执行层级容量限制
   */
  _enforceLayerLimits(targetLayer) {
    const limits = this.config.layerThresholds
    const maxItems = limits[`max${targetLayer}Items`]

    const itemsInLayer = Object.values(this.store.items)
      .filter(item => item.layer === targetLayer)

    if (itemsInLayer.length <= maxItems) return

    const priorityOrder = { high: 0, medium: 1, low: 2 }
    itemsInLayer.sort((a, b) => {
      if (priorityOrder[a.priority] !== priorityOrder[b.priority]) {
        return priorityOrder[a.priority] - priorityOrder[b.priority]
      }
      const timeA = a.lastAccess || a.createdAt
      const timeB = b.lastAccess || b.createdAt
      return timeA.localeCompare(timeB)
    })

    const toDemote = itemsInLayer.slice(maxItems)
    for (const item of toDemote) {
      this.demote(item.id)
    }
  }

  /**
   * 降级条目（L1→L2→L3）
   */
  demote(id) {
    const item = this.store.items[id]
    if (!item) return false

    const now = new Date().toISOString()

    if (item.layer === 'L1') {
      item.layer = 'L2'
      item.summary = this._generateSummary(item.fullContent || item.summary)
      item.fullContent = undefined
      item.compressedAt = now
      console.log(`[KnowledgeManager] 降级 L1→L2: ${id}`)
    } else if (item.layer === 'L2') {
      item.layer = 'L3'
      item.summary = this._generateSummary(item.summary).substring(0, 100) + '...'
      item.compressedAt = now
      item.archivedAt = now
      console.log(`[KnowledgeManager] 降级 L2→L3: ${id}`)
    } else {
      return false
    }

    item.updatedAt = now
    this.updateStats()
    return true
  }

  /**
   * 升级条目（L3→L2→L1）
   */
  promote(id) {
    const item = this.store.items[id]
    if (!item || item.layer === 'L1') return false

    if (item.layer === 'L2') {
      console.warn(`[KnowledgeManager] L2→L1 需要外部提供完整内容: ${id}`)
      return false
    } else if (item.layer === 'L3') {
      console.warn(`[KnowledgeManager] L3→L2 需要外部提供完整内容: ${id}`)
      return false
    }

    this.updateStats()
    return true
  }

  /**
   * 生成摘要
   */
  _generateSummary(content) {
    if (content.length <= this.config.summaryLength) {
      return content
    }
    return content.substring(0, this.config.summaryLength).trim() + '...'
  }

  /**
   * 执行定时压缩
   */
  compress() {
    const result = {
      demoted: [],
      promoted: [],
      archived: [],
      errors: [],
    }

    const now = new Date()
    const thresholds = this.config.layerThresholds

    for (const item of Object.values(this.store.items)) {
      try {
        if (item.priority === 'high') continue

        const lastAccess = item.lastAccess ? new Date(item.lastAccess) : new Date(item.createdAt)
        const daysSinceAccess = Math.floor((now.getTime() - lastAccess.getTime()) / (1000 * 60 * 60 * 24))

        if (item.layer === 'L1' && daysSinceAccess > thresholds.L1ToL2Days) {
          if (this.demote(item.id)) {
            result.demoted.push(item.id)
          }
        } else if (item.layer === 'L2' && daysSinceAccess > thresholds.L2ToL3Days) {
          if (this.demote(item.id)) {
            result.demoted.push(item.id)
          }
        }
      } catch (error) {
        result.errors.push(`${item.id}: ${error}`)
      }
    }

    this.saveStore()
    return result
  }

  // ============== 上下文构建 ==============

  /**
   * 为 AI 构建上下文
   */
  buildContext({ maxItems = 10, includeLayers = ['L1', 'L2'], tags = [] } = {}) {
    let items = Object.values(this.store.items)
      .filter(item => includeLayers.includes(item.layer))

    if (tags.length > 0) {
      items = items.filter(item => tags.some(tag => item.tags.includes(tag)))
    }

    items.sort((a, b) => {
      if (a.layer !== b.layer) {
        return a.layer === 'L1' ? -1 : 1
      }
      return b.accessCount - a.accessCount
    })

    items = items.slice(0, maxItems)

    const lines = ['## 知识库上下文\n']

    for (const item of items) {
      lines.push(`### ${item.title} [${item.layer}]`)
      if (item.tags.length > 0) {
        lines.push(`标签: ${item.tags.join(', ')}`)
      }
      lines.push(`优先级: ${item.priority}`)
      
      if (item.layer === 'L1' && item.fullContent) {
        lines.push(item.fullContent)
      } else {
        lines.push(item.summary)
      }
      lines.push('')
    }

    return lines.join('\n')
  }

  // ============== 统计 ==============

  /**
   * 获取统计信息
   */
  getStats() {
    return {
      ...this.store.stats,
      storePath: this.storePath,
      lastModified: this.store.lastModified,
    }
  }

  /**
   * 获取容量报告
   */
  getCapacityReport() {
    const limits = this.config.layerThresholds
    return {
      L1: {
        current: this.store.stats.byLayer.L1,
        max: limits.maxL1Items,
        usage: `${Math.round(this.store.stats.byLayer.L1 / limits.maxL1Items * 100)}%`,
      },
      L2: {
        current: this.store.stats.byLayer.L2,
        max: limits.maxL2Items,
        usage: `${Math.round(this.store.stats.byLayer.L2 / limits.maxL2Items * 100)}%`,
      },
      L3: {
        current: this.store.stats.byLayer.L3,
        max: Infinity,
        usage: 'unlimited',
      },
    }
  }
}

// ============== CLI 入口 ==============

function showHelp() {
  console.log(`
📚 Knowledge Manager - 知识库智能管理器

用法: node index.js <命令> [选项]

命令:
  add <标题> <内容> [标签...]    添加知识条目
  get <id>                       获取指定条目
  list [layer]                   列出所有条目 (可选: L1|L2|L3)
  search <关键词> [标签...]       搜索知识
  delete <id>                    删除条目
  compress                      执行压缩
  stats                          显示统计
  context [max]                  构建 AI 上下文
  help                           显示帮助

示例:
  node index.js add "SQL注入研判" "判断SQL注入是否成功..." "web安全" "研判规则"
  node index.js search SQL注入
  node index.js list L1
  node index.js compress
`)
}

function main() {
  const args = process.argv.slice(2)
  const command = args[0] || 'help'

  const manager = new KnowledgeManager('./knowledge-store.json')

  switch (command) {
    case 'add': {
      const title = args[1]
      const content = args[2]
      const tags = args.slice(3)
      if (!title || !content) {
        console.error('需要提供标题和内容')
        process.exit(1)
      }
      const item = manager.add({ title, content, tags })
      console.log('✅ 添加成功:', item.id)
      break
    }

    case 'get': {
      const id = args[1]
      if (!id) {
        console.error('需要提供ID')
        process.exit(1)
      }
      const item = manager.get(id)
      console.log(JSON.stringify(item, null, 2))
      break
    }

    case 'list': {
      const layer = args[1] || null
      const items = manager.list(layer)
      console.log(`\n📚 共 ${items.length} 条知识:\n`)
      for (const item of items) {
        const tags = item.tags.length > 0 ? ` [${item.tags.join(', ')}]` : ''
        console.log(`[${item.layer}] ${item.title}${tags}`)
        console.log(`   ID: ${item.id} | 访问: ${item.accessCount}次 | 优先级: ${item.priority}`)
        console.log('')
      }
      break
    }

    case 'search': {
      const query = args[1]
      const tags = args.slice(2)
      if (!query) {
        console.error('需要提供搜索关键词')
        process.exit(1)
      }
      const results = manager.search({ query, tags })
      console.log(`\n🔍 找到 ${results.length} 条结果:\n`)
      for (const item of results) {
        console.log(`[${item.layer}] ${item.title}`)
        console.log(`  摘要: ${item.summary.substring(0, 80)}...`)
        console.log('')
      }
      break
    }

    case 'delete': {
      const id = args[1]
      if (!id) {
        console.error('需要提供ID')
        process.exit(1)
      }
      if (manager.delete(id)) {
        console.log('✅ 删除成功')
      } else {
        console.log('❌ 未找到')
      }
      break
    }

    case 'compress': {
      console.log('🗜️  执行压缩...\n')
      const result = manager.compress()
      if (result.demoted.length === 0) {
        console.log('✅ 没有需要压缩的条目')
      } else {
        console.log(`降级: ${result.demoted.length}条`)
      }
      if (result.errors.length > 0) {
        console.log(`错误: ${result.errors.join(', ')}`)
      }
      break
    }

    case 'stats': {
      const stats = manager.getStats()
      const capacity = manager.getCapacityReport()
      console.log('\n📊 统计信息:\n')
      console.log(`总条目: ${stats.totalItems}`)
      console.log(`L1: ${capacity.L1.current}/${capacity.L1.max} (${capacity.L1.usage})`)
      console.log(`L2: ${capacity.L2.current}/${capacity.L2.max} (${capacity.L2.usage})`)
      console.log(`L3: ${capacity.L3.current}/unlimited`)
      break
    }

    case 'context': {
      const max = parseInt(args[1] || '10')
      console.log('\n📝 AI 上下文:\n')
      console.log(manager.buildContext({ maxItems: max }))
      break
    }

    case 'help':
    default:
      showHelp()
  }
}

// 如果直接运行此文件
if (require.main === module) {
  main()
}

module.exports = { KnowledgeManager }
