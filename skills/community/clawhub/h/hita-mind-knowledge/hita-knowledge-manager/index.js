/**
 * Knowledge Manager - CLI Entry Point
 * 
 * 用法:
 *   node index.js <命令> [参数]
 * 
 * 命令:
 *   add <标题> <内容> [标签...]    添加知识条目
 *   get <id>                       获取指定条目
 *   list [layer]                    列出所有条目 (L1|L2|L3)
 *   search <关键词> [标签...]       搜索知识
 *   delete <id>                     删除条目
 *   stats                           显示统计
 *   context [max]                   构建 AI 上下文
 *   compress                        执行压缩
 *   help                            显示帮助
 */

const path = require('path')
const { KnowledgeManager } = require('./knowledge-manager.js')

const args = process.argv.slice(2)
const command = args[0] || 'help'

const storePath = path.join(__dirname, 'knowledge-store.json')
const km = new KnowledgeManager(storePath)

function showHelp() {
  console.log(`
📚 Knowledge Manager - 知识库智能管理器

用法: node index.js <命令> [选项]

命令:
  add <标题> <内容> [标签...]    添加知识条目
  get <id>                       获取指定条目
  list [layer]                   列出所有条目 (L1|L2|L3)
  search <关键词> [标签...]       搜索知识
  delete <id>                    删除条目
  stats                          显示统计
  context [max]                  构建 AI 上下文
  compress                       执行压缩
  help                           显示帮助

示例:
  node index.js add "SQL注入研判" "判断SQL注入是否成功..." "web安全" "研判规则"
  node index.js search SQL注入
  node index.js list L1
  node index.js stats
  node index.js context 10
`)
}

async function main() {
  switch (command) {
    case 'add': {
      const title = args[1]
      const content = args[2]
      const tags = args.slice(3)
      if (!title || !content) {
        console.error('❌ 需要提供标题和内容')
        process.exit(1)
      }
      const item = km.add({ title, layer: 'L1', tags, priority: 'medium', summary: content })
      console.log(`✅ 添加成功: ${item.id}`)
      break
    }

    case 'get': {
      const id = args[1]
      if (!id) {
        console.error('❌ 需要提供ID')
        process.exit(1)
      }
      const item = km.get(id)
      if (!item) {
        console.log('❌ 未找到')
      } else {
        console.log(JSON.stringify(item, null, 2))
      }
      break
    }

    case 'list': {
      const layer = args[1] || null
      const items = km.list(layer)
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
        console.error('❌ 需要提供搜索关键词')
        process.exit(1)
      }
      const results = km.search({ query, tags })
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
        console.error('❌ 需要提供ID')
        process.exit(1)
      }
      if (km.delete(id)) {
        console.log('✅ 删除成功')
      } else {
        console.log('❌ 未找到')
      }
      break
    }

    case 'stats': {
      const stats = km.getStats()
      const capacity = km.getCapacityReport()
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
      console.log(km.buildContext({ maxItems: max }))
      break
    }

    case 'compress': {
      console.log('🗜️  执行压缩...\n')
      const result = km.compress()
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

    case 'help':
    default:
      showHelp()
  }
}

main().catch(console.error)
