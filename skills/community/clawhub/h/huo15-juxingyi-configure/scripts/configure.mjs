#!/usr/bin/env node
/**
 * configure.mjs — 聚星逸(Juxingyi) OpenClaw 配置脚本
 *
 * 只做一件事:用 fsk- 密钥调聚星逸 /v1/models 接口,
 * 把返回的模型列表写入 ~/.openclaw/openclaw.json 的 fireworks-hub provider 段。
 *
 * 模型列表完全来自接口实时返回,不依赖任何本地硬编码的模型分类数据。
 *
 * 用法:
 *   node configure.mjs <fsk-key>              # 拉取模型列表并写入配置
 *   node configure.mjs <fsk-key> --list       # 只列出接口返回的模型(不写文件)
 *   node configure.mjs <fsk-key> --env        # 密钥用环境变量引用(更安全)
 *   node configure.mjs --switch <model-id>    # 切换主模型(支持前缀匹配)
 *   node configure.mjs --show                 # 查看当前聚星逸配置
 *   node configure.mjs --help | -h            # 显示帮助
 *   node configure.mjs --version | -v         # 显示版本号
 *
 * 零依赖,Node 18+(自带 fetch)。
 * 接入文档: https://fireworks-simulator.huo15.com/docs.html
 * 青岛火一五信息科技有限公司
 */

import { readFileSync, writeFileSync, existsSync, copyFileSync } from 'fs'
import { homedir } from 'os'
import { join, dirname } from 'path'
import { fileURLToPath } from 'url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const OPENCLAW_JSON = join(homedir(), '.openclaw', 'openclaw.json')
const META_PATH = join(__dirname, '..', '_meta.json')

// ── 聚星逸接口常量(依据接入文档 https://fireworks-simulator.huo15.com/docs.html) ──
const BASE_URL = 'https://fireworks-simulator-api.huo15.com/v1'
const PROVIDER = 'fireworks-hub'
const ENV_VAR = 'FIREWORKS_API_KEY'
// 生图/视频模型关键词——此类模型不能用于文本对话,接口若返回则跳过
const NON_TEXT_RE = /image|seedream|t2v|i2v|video|dall-?e|happyhorse/i

// ============================================================
// Node 版本检查(需 18+ 的原生 fetch)
// ============================================================
const NODE_MAJOR = parseInt(process.versions.node.split('.')[0], 10)
if (NODE_MAJOR < 18) {
  console.error(`\u274c 需要 Node.js 18+(当前 ${process.versions.node})。\n   Node 18+ 自带 fetch API,请升级: https://nodejs.org/`)
  process.exit(1)
}

// ============================================================
// 参数解析
// ============================================================
const args = process.argv.slice(2)
const flags = {
  list: args.includes('--list'),
  update: args.includes('--update'),
  show: args.includes('--show'),
  env: args.includes('--env'),
  help: args.includes('--help') || args.includes('-h'),
  version: args.includes('--version') || args.includes('-v'),
}
const switchIdx = args.indexOf('--switch')
const switchModel = switchIdx >= 0 ? args[switchIdx + 1] : null
const keyArg = args.find(a => a.startsWith('fsk-'))

// ============================================================
// 工具函数
// ============================================================
function fmtName(id) {
  return id.replace(/[-_]/g, ' ').replace(/\b\w/g, c => c.toUpperCase())
}

function timestamp() {
  return new Date().toISOString().replace(/[:.]/g, '-')
}

function readMeta() {
  return JSON.parse(readFileSync(META_PATH, 'utf8'))
}

// 模型 ID 解析:精确 → 大小写不敏感 → 前缀唯一匹配(歧义则报错)
function resolveModelId(input, ids) {
  if (ids.includes(input)) return input
  const lower = input.toLowerCase()
  const ci = ids.find(m => m.toLowerCase() === lower)
  if (ci) return ci
  const prefixes = ids.filter(m => m.toLowerCase().startsWith(lower))
  if (prefixes.length === 1) return prefixes[0]
  if (prefixes.length > 1) {
    console.error(`\u26a0\ufe0f "${input}" 匹配到多个模型,请更精确地指定:`)
    prefixes.forEach(m => console.error(`     ${m}`))
    process.exit(1)
  }
  return null
}

// ============================================================
// 从聚星逸 /v1/models 接口动态获取模型列表
// ============================================================
async function fetchModels(apiKey) {
  const url = `${BASE_URL}/models`
  const ctrl = new AbortController()
  const timer = setTimeout(() => ctrl.abort(), 15000)
  let resp
  try {
    resp = await fetch(url, {
      headers: { Authorization: `Bearer ${apiKey}` },
      signal: ctrl.signal,
    })
  } catch (e) {
    if (e.name === 'AbortError') {
      throw new Error(`请求超时(15s): ${url}\n   请检查网络或稍后重试。`)
    }
    throw new Error(`网络请求失败: ${e.message}\n   请检查网络连接或 Base URL 是否可达。`)
  } finally {
    clearTimeout(timer)
  }

  if (!resp.ok) {
    const body = await resp.text().catch(() => '')
    let hint = ''
    if (resp.status === 401) hint = '\n   提示: 密钥无效或已过期,请到聚星逸控制台确认。'
    else if (resp.status === 403) hint = '\n   提示: 密钥权限不足。'
    else if (resp.status >= 500) hint = '\n   提示: 聚星逸服务端异常,请稍后重试。'
    throw new Error(`API 返回 ${resp.status}: ${body.slice(0, 200)}${hint}`)
  }
  const data = await resp.json()
  const models = data.data || data.models || []
  if (!Array.isArray(models) || models.length === 0) {
    throw new Error('API 返回的模型列表为空。\n   请检查密钥权限或联系聚星逸支持。')
  }
  return models
}

// ============================================================
// 构造单个模型配置项
//
// 接口 /v1/models 按 OpenAI 兼容标准只返回 id / owned_by,
// 不返回 contextWindow / reasoning / maxTokens 等参数。
// 这里除 id / name 外填保守默认值,保证 OpenClaw 可直接调用;
// 用户可按需在 openclaw.json 中手动调整。
// ============================================================
function toModelEntry(id) {
  return {
    id,
    name: `${fmtName(id)} (聚星逸)`,
    reasoning: false,
    contextWindow: 131072,
    maxTokens: 8192,
    input: ['text'],
    cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
  }
}

// ============================================================
// 构造 provider + agents.defaults 配置
// ============================================================
function buildConfig(apiKey, rawModels) {
  const textModels = []
  const skipped = []
  for (const m of rawModels) {
    if (!m || typeof m.id !== 'string') continue
    if (NON_TEXT_RE.test(m.id)) { skipped.push(m); continue }
    textModels.push(toModelEntry(m.id))
  }

  if (textModels.length === 0) {
    throw new Error('接口返回的模型全部为生图/视频模型,没有可配置的文本对话模型。')
  }

  const apiKeyField = flags.env
    ? { source: 'env', provider: 'default', id: ENV_VAR }
    : apiKey

  const provider = {
    baseUrl: BASE_URL,
    apiKey: apiKeyField,
    api: 'openai-completions',
    models: textModels,
  }

  // 主模型取接口返回列表的第一个,其余作为 fallbacks
  const primaryId = textModels[0].id
  const prefixed = textModels.map(m => `${PROVIDER}/${m.id}`)
  const primary = `${PROVIDER}/${primaryId}`
  const fallbacks = prefixed.filter(p => p !== primary)

  const aliases = {}
  for (const m of textModels) {
    aliases[`${PROVIDER}/${m.id}`] = { alias: m.name }
  }

  const agents = { primary, fallbacks, models: aliases }
  return { provider, agents, textModels, skipped }
}

// ============================================================
// 读取 / 写入 openclaw.json
// ============================================================
function readOpenclawJson() {
  if (!existsSync(OPENCLAW_JSON)) {
    throw new Error(`未找到 ${OPENCLAW_JSON}\n请先运行 openclaw 初始化。`)
  }
  return JSON.parse(readFileSync(OPENCLAW_JSON, 'utf8'))
}

function writeOpenclawJson(config) {
  const bak = `${OPENCLAW_JSON}.bak.${timestamp()}`
  copyFileSync(OPENCLAW_JSON, bak)
  writeFileSync(OPENCLAW_JSON, JSON.stringify(config, null, 2) + '\n', 'utf8')
  return bak
}

// ============================================================
// 主逻辑
// ============================================================
async function main() {
  // --- help / version(不联网、不读写配置) ---
  if (flags.help) return cmdHelp()
  if (flags.version) return cmdVersion()

  // --- show 模式 ---
  if (flags.show) return cmdShow()

  // --- switch 模式 ---
  if (switchModel) return cmdSwitch(switchModel)

  // --- 以下模式需要 API key ---
  if (!keyArg) {
    console.error(
      '用法: node configure.mjs <fsk-key> [--list|--update|--env]\n' +
      '      node configure.mjs --switch <model-id>\n' +
      '      node configure.mjs --show | --help | --version\n\n' +
      '缺少聚星逸 API Key(fsk- 开头)。'
    )
    process.exit(1)
  }

  // 校验密钥格式
  if (keyArg.length <= 4) {
    console.error('❌ 聚星逸 API Key 格式错误: fsk- 后应有密钥内容。')
    process.exit(1)
  }

  // 动态获取模型列表
  const rawModels = await fetchModels(keyArg)
  const { provider, agents, textModels, skipped } = buildConfig(keyArg, rawModels)

  // --- list 模式 ---
  if (flags.list) return cmdList(rawModels, textModels, skipped)

  // --- update 模式: 只刷新模型列表,保留主模型 ---
  if (flags.update) return cmdUpdate(provider, textModels, skipped)

  // --- 默认: 写入 openclaw.json(首次配置,主模型取列表第一个) ---
  return cmdConfigure(provider, agents, textModels, skipped)
}

// ============================================================
// 子命令实现
// ============================================================
function cmdList(rawModels, textModels, skipped) {
  console.log(`\n🛰️  聚星逸 · 可用模型(来自 /v1/models 接口)`)
  console.log(`   共 ${rawModels.length} 个,其中 ${textModels.length} 个文本对话模型\n`)

  console.log('文本对话模型(将写入配置):')
  textModels.forEach((m, i) => {
    const mark = i === 0 ? ' ★ 默认主模型' : ''
    console.log(`  ${m.id.padEnd(30)} ${m.name}${mark}`)
  })

  if (skipped.length) {
    console.log(`\n生图/视频模型(跳过,不配文本对话): ${skipped.length} 个`)
    skipped.forEach(m => console.log(`  ${m.id}`))
  }
  console.log()
}

function cmdConfigure(provider, agents, textModels, skipped) {
  const config = readOpenclawJson()

  // 合并 provider(只覆盖 fireworks-hub 段)
  if (!config.models) config.models = {}
  if (!config.models.providers) config.models.providers = {}
  if (!config.models.mode) config.models.mode = 'replace'
  config.models.providers[PROVIDER] = provider

  // 合并 agents.defaults
  if (!config.agents) config.agents = {}
  if (!config.agents.defaults) config.agents.defaults = {}
  config.agents.defaults.model = {
    primary: agents.primary,
    fallbacks: agents.fallbacks,
  }
  // 合并 alias(保留非 fireworks-hub 的已有条目,清理旧 fireworks-hub 条目)
  const existing = config.agents.defaults.models || {}
  for (const key of Object.keys(existing)) {
    if (key.startsWith(`${PROVIDER}/`)) delete existing[key]
  }
  for (const [key, val] of Object.entries(agents.models)) {
    existing[key] = val
  }
  config.agents.defaults.models = existing

  const bak = writeOpenclawJson(config)

  console.log(`\n✅ 聚星逸配置完成!`)
  console.log(`   备份: ${bak}`)
  console.log(`   模型数: ${textModels.length} 个文本对话模型${skipped.length ? `(跳过 ${skipped.length} 个生图/视频)` : ''}`)
  console.log(`   主模型: ${agents.primary}`)
  console.log(`   备选链: ${agents.fallbacks.length} 个模型`)
  console.log(`   密钥存储: ${flags.env ? `环境变量 ${ENV_VAR}` : '直接写入(明文)'}\n`)

  console.log('   主模型 & 备选链:')
  console.log(`   ★ ${agents.primary}`)
  agents.fallbacks.forEach(f => console.log(`     ${f}`))
  console.log()

  if (flags.env) {
    console.log(`⚠️  请确保环境变量 ${ENV_VAR} 已设置:`)
    console.log(`   export ${ENV_VAR}=fsk-你的密钥\n`)
  }

  console.log('重启 OpenClaw 后生效。')
}

// ============================================================
// cmdUpdate: 日常更新模型列表(保留主模型,只刷新 providers 段)
//
// 与 cmdConfigure(首次配置)的区别:
//   - cmdConfigure: 主模型取列表第一个,重置 fallbacks
//   - cmdUpdate: 保留当前主模型(若仍在列表中),只刷新模型列表
// 适用场景: 平台新增了模型,想拉取最新列表但不改自己选的主模型
// ============================================================
function cmdUpdate(newProvider, textModels, skipped) {
  const config = readOpenclawJson()
  const oldProv = config.models?.providers?.[PROVIDER]

  if (!oldProv) {
    console.error(`未找到 ${PROVIDER} provider,请先运行配置: node configure.mjs <fsk-key>`)
    process.exit(1)
  }

  // 当前主模型
  const oldPrimary = config.agents?.defaults?.model?.primary || null
  const oldPrimaryId = oldPrimary ? oldPrimary.replace(`${PROVIDER}/`, '') : null

  // 旧 / 新模型 ID 列表
  const oldIds = (oldProv.models || []).map(m => m.id)
  const newIds = textModels.map(m => m.id)

  // 决定主模型:旧主仍在列表 → 保留;否则取列表第一个并提示
  let primary, primaryChanged = false
  if (oldPrimaryId && newIds.includes(oldPrimaryId)) {
    primary = `${PROVIDER}/${oldPrimaryId}`
  } else {
    primary = `${PROVIDER}/${newIds[0]}`
    primaryChanged = !!oldPrimaryId // 之前有主模型但现在不在列表 = 被下架
  }

  // fallbacks = 新列表除 primary 外的全部
  const fallbacks = newIds.filter(id => `${PROVIDER}/${id}` !== primary).map(id => `${PROVIDER}/${id}`)

  // aliases 重新生成
  const aliases = {}
  for (const m of textModels) {
    aliases[`${PROVIDER}/${m.id}`] = { alias: m.name }
  }

  // 保留原密钥存储方式(明文 / env 引用都不动,更新模型列表不该改密钥)
  newProvider.apiKey = oldProv.apiKey

  // 写入 provider
  config.models.providers[PROVIDER] = newProvider

  // 写入 agents.defaults
  if (!config.agents) config.agents = {}
  if (!config.agents.defaults) config.agents.defaults = {}
  config.agents.defaults.model = { primary, fallbacks }

  // aliases: 清理旧 fireworks-hub 条目,写入新的(保留非 fireworks-hub 条目)
  const existing = config.agents.defaults.models || {}
  for (const key of Object.keys(existing)) {
    if (key.startsWith(`${PROVIDER}/`)) delete existing[key]
  }
  for (const [key, val] of Object.entries(aliases)) {
    existing[key] = val
  }
  config.agents.defaults.models = existing

  const bak = writeOpenclawJson(config)

  // 报告变更
  const added = newIds.filter(id => !oldIds.includes(id))
  const removed = oldIds.filter(id => !newIds.includes(id))

  console.log(`\n✅ 聚星逸模型列表已更新!`)
  console.log(`   备份: ${bak}`)
  console.log(`   模型数: ${oldIds.length} → ${newIds.length} 个文本对话模型${skipped.length ? `(跳过 ${skipped.length} 个生图/视频)` : ''}`)
  if (added.length) {
    console.log(`   ✨ 新增 ${added.length} 个:`)
    added.forEach(id => console.log(`     + ${id}`))
  }
  if (removed.length) {
    console.log(`   🗑️  移除 ${removed.length} 个:`)
    removed.forEach(id => console.log(`     - ${id}`))
  }
  if (primaryChanged) {
    console.log(`   ⚠️  旧主模型 ${oldPrimary} 已不在平台列表(可能下架),主模型切换为 ${primary}`)
  } else {
    console.log(`   主模型保留: ${primary}`)
  }
  console.log(`   备选链: ${fallbacks.length} 个模型`)
  console.log(`\n重启 OpenClaw 后生效。`)
}

function cmdSwitch(modelId) {
  const config = readOpenclawJson()
  const prov = config.models?.providers?.[PROVIDER]

  if (!prov) {
    console.error(`未找到 ${PROVIDER} provider,请先运行配置: node configure.mjs <fsk-key>`)
    process.exit(1)
  }

  const ids = (prov.models || []).map(m => m.id)
  const fullId = resolveModelId(modelId, ids)

  if (!fullId) {
    console.error(`模型 "${modelId}" 不在聚星逸可用列表中。`)
    console.error(`可用模型: ${ids.join(', ')}`)
    process.exit(1)
  }

  const oldPrimary = config.agents?.defaults?.model?.primary || '(未设置)'
  const newPrimary = `${PROVIDER}/${fullId}`

  if (!config.agents) config.agents = {}
  if (!config.agents.defaults) config.agents.defaults = {}
  if (!config.agents.defaults.model) config.agents.defaults.model = {}

  config.agents.defaults.model.primary = newPrimary

  // 从 fallbacks 中移除新 primary
  const fallbacks = config.agents.defaults.model.fallbacks || []
  config.agents.defaults.model.fallbacks = fallbacks.filter(f => f !== newPrimary)

  // 旧 primary 加入 fallbacks 首位
  if (oldPrimary !== newPrimary && oldPrimary !== '(未设置)' && !fallbacks.includes(oldPrimary)) {
    config.agents.defaults.model.fallbacks.unshift(oldPrimary)
  }

  const bak = writeOpenclawJson(config)

  console.log(`\n✅ 主模型已切换`)
  console.log(`   备份: ${bak}`)
  console.log(`   旧主: ${oldPrimary}`)
  console.log(`   新主: ${newPrimary}`)
  console.log(`   备选: ${config.agents.defaults.model.fallbacks.length} 个模型\n`)
  console.log('重启 OpenClaw 后生效。')
}

function cmdShow() {
  const config = readOpenclawJson()
  const prov = config.models?.providers?.[PROVIDER]

  if (!prov) {
    console.log(`\n❌ 尚未配置聚星逸 (${PROVIDER})。`)
    console.log(`   运行: node configure.mjs <fsk-key>\n`)
    return
  }

  const primary = config.agents?.defaults?.model?.primary || '(未设置)'
  const fallbacks = config.agents?.defaults?.model?.fallbacks || []

  console.log(`\n🛰️  聚星逸当前配置`)
  console.log(`   Provider: ${PROVIDER}`)
  console.log(`   Base URL: ${prov.baseUrl}`)
  console.log(`   API 类型: ${prov.api}`)
  const keyDisplay = typeof prov.apiKey === 'string'
    ? `直接密钥 (${prov.apiKey.slice(0, 8)}…)`
    : `环境变量 ${prov.apiKey?.id || '?'}`
  console.log(`   密钥方式: ${keyDisplay}`)
  console.log(`   文本模型: ${(prov.models || []).length} 个`)
  console.log(`   主模型:   ${primary}`)

  if (fallbacks.length) {
    console.log(`   备选链:`)
    fallbacks.forEach(f => console.log(`     ${f}`))
  }
  console.log()

  if (prov.models?.length) {
    console.log('   已配模型:')
    prov.models.forEach(m => {
      const mark = `${PROVIDER}/${m.id}` === primary ? ' ★' : '  '
      console.log(`   ${mark} ${m.id.padEnd(30)} ${m.name}`)
    })
  }
  console.log()
}

// ============================================================
// 子命令: help / version
// ============================================================
function cmdHelp() {
  const meta = readMeta()
  console.log(`
聚星逸配置 · huo15-juxingyi-configure v${meta.version}

只做一件事:用 fsk- 密钥调聚星逸 /v1/models 接口,把模型列表写入 openclaw.json。
模型列表完全来自接口实时返回,不依赖本地硬编码数据。

用法:
  node configure.mjs <fsk-key>            拉取模型列表并写入配置(主模型取列表第一个)
  node configure.mjs <fsk-key> --list     只列出接口返回的模型(不写文件)
  node configure.mjs <fsk-key> --update   日常更新模型列表(保留当前主模型)
  node configure.mjs <fsk-key> --env      密钥用环境变量 ${ENV_VAR} 引用(首次配置时更安全)
  node configure.mjs --switch <model-id>  切换主模型(支持前缀匹配)
  node configure.mjs --show               查看当前聚星逸配置
  node configure.mjs --help | -h          显示本帮助
  node configure.mjs --version | -v       显示版本号

环境变量:
  ${ENV_VAR}                 --env 模式下从此环境变量读取密钥

接入文档: https://fireworks-simulator.huo15.com/docs.html
更多信息: https://cnb.cool/huo15/ai/huo15-skills
`)
}

function cmdVersion() {
  const meta = readMeta()
  console.log(`huo15-juxingyi-configure v${meta.version}`)
}

// ============================================================
main().catch(err => {
  console.error(`\n❌ ${err.message}\n`)
  process.exit(1)
})
