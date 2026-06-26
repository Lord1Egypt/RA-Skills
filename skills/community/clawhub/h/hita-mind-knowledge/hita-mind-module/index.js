/**
 * Memory Module - AI 个人记忆系统
 * 8大分类：decisions/preferences/patterns/causality/contacts/feedback/projects/daily
 * 
 * 用法:
 *   node index.js <命令> [参数]
 * 
 * 命令:
 *   list [分类]           列出某分类的记忆
 *   search <关键词>        搜索所有分类
 *   stats                 显示统计
 *   context [分类] [条数] 构建上下文（默认5条）
 *   add <分类> <标题> <内容> 添加记忆
 *   delete <分类> <ID>   删除记忆
 *   update <ID> <新内容>  更新记忆
 *   help                  显示帮助
 */

const path = require('path')
const fs = require('fs')

const storePath = path.join(__dirname, 'memory-store.json')

// 初始化默认数据（可根据需要修改）
const DEFAULT_DATA = {
  decisions: [
    { id: 'dec_template_001', title: '【示例】模型选型', content: '使用 Qwen 作为主力对话模型，搜索用 Tavily。' },
  ],
  preferences: [
    { id: 'pref_template_001', title: '【示例】沟通风格', content: '简洁、直接、不啰嗦。直接给结论。' },
  ],
  patterns: [],
  causality: [],
  contacts: [],
  feedback: [],
  projects: [],
  daily: []
}

// 加载或初始化存储
function loadStore() {
  if (fs.existsSync(storePath)) {
    try {
      return JSON.parse(fs.readFileSync(storePath, 'utf-8'))
    } catch (e) {
      console.warn('[memory] 存储文件损坏，使用默认数据')
    }
  }
  const initial = { version: 1, lastModified: new Date().toISOString(), data: DEFAULT_DATA }
  fs.writeFileSync(storePath, JSON.stringify(initial, null, 2), 'utf-8')
  return initial
}

function saveStore(store) {
  store.lastModified = new Date().toISOString()
  fs.writeFileSync(storePath, JSON.stringify(store, null, 2), 'utf-8')
}

const store = loadStore()
const args = process.argv.slice(2)
const command = args[0] || 'help'

const CATEGORIES = ['decisions', 'preferences', 'patterns', 'causality', 'contacts', 'feedback', 'projects', 'daily']

function showHelp() {
  console.log(`
📔 Memory Module - AI 个人记忆系统

用法: node index.js <命令> [参数]

命令:
  list [分类]            列出某分类的记忆 (${CATEGORIES.join('/')})
  search <关键词>         搜索所有分类
  stats                  显示统计
  context [分类] [条数]  构建上下文 (默认5条)
  add <分类> <标题> <内容> 添加记忆
  delete <分类> <ID>     删除记忆
  update <ID> <新内容>   更新记忆
  help                   显示帮助

示例:
  node index.js list patterns
  node index.js search PPT
  node index.js stats
  node index.js context patterns 3
  node index.js add decisions "技术选型" "使用Qwen作为主力模型"
`)
}

function list(category) {
  if (category && !CATEGORIES.includes(category)) {
    console.log(`未知分类: ${category}，可用: ${CATEGORIES.join('/')}`)
    return
  }
  
  if (category) {
    const items = store.data[category] || []
    console.log(`\n📂 ${category} (${items.length}条)\n`)
    items.forEach(item => {
      console.log(`[${item.id}] ${item.title}`)
      console.log(`  ${item.content.substring(0, 80)}${item.content.length > 80 ? '...' : ''}`)
      console.log('')
    })
  } else {
    console.log('\n📔 全部记忆分类:\n')
    CATEGORIES.forEach(cat => {
      const count = (store.data[cat] || []).length
      console.log(`  ${cat}: ${count}条`)
    })
  }
}

function search(keyword) {
  if (!keyword) {
    console.log('需要提供关键词')
    return
  }
  const lower = keyword.toLowerCase()
  const results = []
  
  for (const [category, items] of Object.entries(store.data)) {
    for (const item of items) {
      if (item.title.toLowerCase().includes(lower) || item.content.toLowerCase().includes(lower)) {
        results.push({ category, ...item })
      }
    }
  }
  
  console.log(`\n🔍 搜索"${keyword}"，找到 ${results.length} 条:\n`)
  results.forEach(r => {
    console.log(`[${r.category}] ${r.title}`)
    console.log(`  ${r.content.substring(0, 100)}${r.content.length > 100 ? '...' : ''}`)
    console.log('')
  })
}

function stats() {
  console.log('\n📊 记忆统计:\n')
  let total = 0
  for (const [cat, items] of Object.entries(store.data)) {
    console.log(`  ${cat}: ${items.length}条`)
    total += items.length
  }
  console.log(`\n总计: ${total}条`)
  console.log(`最后更新: ${store.lastModified}`)
}

function buildContext(category, limit = 5) {
  let items = []
  
  if (category && CATEGORIES.includes(category)) {
    items = store.data[category] || []
  } else {
    for (const [cat, catItems] of Object.entries(store.data)) {
      items.push(...catItems.map(i => ({ ...i, category: cat })))
    }
    items.sort((a, b) => (b.updatedAt || '').localeCompare(a.updatedAt || ''))
  }
  
  items = items.slice(0, limit)
  
  console.log('\n📝 记忆上下文:\n')
  items.forEach(item => {
    console.log(`## [${item.category}] ${item.title}`)
    console.log(item.content)
    console.log('')
  })
}

function add(category, title, content) {
  if (!CATEGORIES.includes(category)) {
    console.log(`未知分类，可用: ${CATEGORIES.join('/')}`)
    return
  }
  
  if (!title || !content) {
    console.log('需要提供标题和内容')
    return
  }
  
  const id = `${category}_${Date.now().toString(36)}`
  const item = { 
    id, 
    title, 
    content, 
    createdAt: new Date().toISOString(), 
    updatedAt: new Date().toISOString() 
  }
  
  if (!store.data[category]) store.data[category] = []
  store.data[category].push(item)
  saveStore(store)
  
  console.log(`✅ 添加成功: [${category}] ${title}`)
}

function deleteItem(category, id) {
  if (!CATEGORIES.includes(category)) {
    console.log(`未知分类，可用: ${CATEGORIES.join('/')}`)
    return
  }
  
  const items = store.data[category] || []
  const idx = items.findIndex(i => i.id === id)
  if (idx === -1) {
    console.log(`❌ 未找到: ${id}`)
    return
  }
  
  items.splice(idx, 1)
  saveStore(store)
  console.log(`✅ 删除成功: ${id}`)
}

function update(id, newContent) {
  if (!newContent) {
    console.log('需要提供新内容')
    return
  }
  
  for (const [cat, items] of Object.entries(store.data)) {
    const item = items.find(i => i.id === id)
    if (item) {
      item.content = newContent
      item.updatedAt = new Date().toISOString()
      saveStore(store)
      console.log(`✅ 更新成功: ${id}`)
      return
    }
  }
  
  console.log(`❌ 未找到: ${id}`)
}

switch (command) {
  case 'list':
    list(args[1])
    break
  case 'search':
    search(args[1])
    break
  case 'stats':
    stats()
    break
  case 'context':
    buildContext(args[1], parseInt(args[2] || '5'))
    break
  case 'add':
    add(args[1], args[2], args.slice(3).join(' '))
    break
  case 'delete':
    deleteItem(args[1], args[2])
    break
  case 'update':
    update(args[1], args.slice(2).join(' '))
    break
  default:
    showHelp()
}
