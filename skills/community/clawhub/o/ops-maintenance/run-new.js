#!/usr/bin/env node
/**
 * ops-maintenance 2.0 整合版
 * 单文件架构，包含所有核心功能
 * 保持与旧版 API 完全兼容
 */

const { Client } = require('ssh2')
const { readFile, writeFile, existsSync, mkdir, stat } = require('fs')
const { promisify } = require('util')
const path = require('path')

const mkdirAsync = promisify(mkdir)
const readFileAsync = promisify(readFile)
const writeFileAsync = promisify(writeFile)
const execAsync = promisify(require('child_process').exec)

// ============ 类型与实体 ============

class Server {
  constructor(host, port = 22, user = 'root', name, tags = []) {
    this.id = `${host}:${port}:${user}`
    this.host = host
    this.port = port
    this.user = user
    this.name = name || `server-${host.replace(/\./g, '-')}`
    this.tags = tags || []
  }
  static fromConfig(cfg) {
    return new Server(cfg.host, cfg.port || 22, cfg.user || 'root', cfg.name, cfg.tags || [])
  }
  getKey() { return `${this.host}:${this.port}:${this.user}` }
  hasTag(tag) { return this.tags.includes(tag) }
  getDisplayName() { return this.name || this.host }
}

const ServerStatus = { HEALTHY: 'healthy', WARNING: 'warning', OFFLINE: 'offline' }

class ServerHealth {
  constructor(server, status, metrics, services, error) {
    this.server = server
    this.status = status
    this.metrics = metrics
    this.services = services
    this.error = error
    this.checkedAt = new Date()
  }
  static healthy(server, metrics, services) { return new ServerHealth(server, ServerStatus.HEALTHY, metrics, services) }
  static offline(server, error) { return new ServerHealth(server, ServerStatus.OFFLINE, null, null, error) }
}

// ============ 配置管理 ============

function getConfigPath() {
  const home = process.env.HOME || process.env.USERPROFILE || '~'
  return path.join(home, '.config', 'ops-maintenance', 'servers.json')
}

class ConfigManager {
  constructor(configPath) {
    this.configPath = configPath || getConfigPath()
    this.servers = []
    this.watchers = []
  }

  async load() {
    try {
      if (!existsSync(this.configPath)) {
        await this.save([])
        this.servers = []
        return
      }
      const content = await readFileAsync(this.configPath, 'utf-8')
      this.servers = JSON.parse(content).map(cfg => Server.fromConfig(cfg))
      this.emit('change', this.servers)
    } catch (e) {
      console.error('配置加载失败:', e.message)
      this.servers = []
    }
  }

  async save(servers) {
    if (servers) this.servers = servers
    const configDir = this.configPath.replace(/[^/\\]+$/, '')
    if (!existsSync(configDir)) await mkdirAsync(configDir, { recursive: true })
    await writeFileAsync(this.configPath, JSON.stringify(this.servers.map(s => ({
      host: s.host, port: s.port, user: s.user, name: s.name, tags: s.tags
    })), null, 2) + '\n', 'utf-8')
  }

  getAll() { return [...this.servers] }
  getByTags(tags) { return this.servers.filter(s => tags.every(t => s.hasTag(t))) }
  getByHost(host) { return this.servers.find(s => s.host === host) || null }

  async add(config) {
    const server = Server.fromConfig(config)
    const idx = this.servers.findIndex(s => s.host === server.host)
    if (idx >= 0) this.servers[idx] = server
    else this.servers.push(server)
    await this.save()
    this.emit('serverAdded', server)
    return server
  }

  async remove(host) {
    const idx = this.servers.findIndex(s => s.host === host)
    if (idx >= 0) {
      this.servers.splice(idx, 1)
      await this.save()
      return true
    }
    return false
  }

  on(event, cb) { this.watchers.push(cb) }
  emit(event, data) { this.watchers.forEach(cb => cb(event, data)) }

  startWatch() {
    if (process.platform === 'win32') {
      this.interval = setInterval(() => this.load(), 2000)
    } else {
      try { this.watcher = require('fs').watch(this.configPath, () => this.load()) } catch {}
    }
  }

  stop() {
    if (this.watcher) { this.watcher.close(); this.watcher = null }
    if (this.interval) { clearInterval(this.interval); this.interval = null }
  }
}

// ============ 凭据 ============

class EnvCredentialsProvider {
  async getCredentials(server) {
    const hostKey = server.host.replace(/[.:]/g, '_')
    const passEnv = `OPS_CRED_${hostKey}`
    const keyEnv = `OPS_KEY_${hostKey}`

    if (process.env[passEnv]) {
      const val = process.env[passEnv]
      return { password: val.includes(':') ? val.split(':', 2)[1] : val }
    }
    if (process.env[keyEnv] && existsSync(process.env[keyEnv])) {
      return { keyFile: process.env[keyEnv] }
    }
    return null
  }
}

// ============ SSH 客户端 ============

class SSHClient {
  constructor() {
    this.connections = new Map()
    this.credsProvider = null
  }

  setCredentialsProvider(provider) { this.credsProvider = provider }

  async execute(server, command, timeout = 30000) {
    const conn = await this.getConnection(server)
    return new Promise((resolve, reject) => {
      conn.exec(command, (err, stream) => {
        if (err) { this.closeConnection(server); return reject(new Error(`SSH失败: ${err.message}`)) }
        let out = ''
        stream.on('data', d => out += d.toString())
        stream.on('close', code => code === 0 ? resolve(out.trim()) : reject(new Error(`退出码${code}: ${out.substring(0,200)}`)))
      })
      setTimeout(() => {
        if (conn.isAuthenticated && conn.isAuthenticated()) {
          conn.requestForcePseudoTerminal((err) => { if (!err) conn.end() })
        }
        reject(new Error(`超时: ${command}`))
      }, timeout)
    })
  }

  async testConnection(server) {
    try { const conn = await this.connect(server); this.connections.set(server.getKey(), conn); return true }
    catch { return false }
  }

  async getConnection(server) {
    const key = server.getKey()
    let conn = this.connections.get(key)
    if (conn && this.isAlive(conn)) return conn
    conn = await this.connect(server)
    this.connections.set(key, conn)
    return conn
  }

  async connect(server) {
    return new Promise((resolve, reject) => {
      const conn = new Client()
      const opts = { host: server.host, port: server.port, username: server.user, readyTimeout: 30000, keepaliveInterval: 10000 }

      ;(async () => {
        try {
          if (this.credsProvider) {
            const creds = await this.credsProvider.getCredentials(server)
            if (creds) {
              if (creds.keyContent) opts.privateKey = Buffer.from(creds.keyContent)
              else if (creds.keyFile) opts.privateKey = readFileSync(creds.keyFile)
              else if (creds.password) opts.password = creds.password
            }
          }
          conn.connect(opts)
        } catch (e) { reject(new Error(`连接失败: ${e.message}`)) }
      })()

      conn.on('ready', () => resolve(conn))
      conn.on('error', e => reject(new Error(`SSH错误: ${e.message}`)))
      conn.on('close', () => this.connections.delete(server.getKey()))
    })
  }

  isAlive(conn) {
    return conn.isAuthenticated && conn.isAuthenticated() && !conn.isDestroyed
  }

  closeConnection(server) {
    const key = server.getKey()
    const conn = this.connections.get(key)
    if (conn) { conn.end(); this.connections.delete(key) }
  }

  async disconnect(server) { this.closeConnection(server) }
  async disconnectAll() { for (const [_, c] of this.connections) c.end(); this.connections.clear() }
}

// ============ 健康检查 ============

async function checkServerHealth(server, ssh) {
  try {
    const [uptimeOut, memOut, diskOut] = await Promise.all([
      ssh.execute(server, 'uptime'),
      ssh.execute(server, 'free -k 2>/dev/null || free 2>/dev/null'),
      ssh.execute(server, 'df -k / 2>/dev/null | tail -1')
    ])

    const loadMatch = uptimeOut.match(/load average:\s+([\d.]+),\s+([\d.]+),\s+([\d.]+)/)
    const loadAvg = loadMatch ? [parseFloat(loadMatch[1]), parseFloat(loadMatch[2]), parseFloat(loadMatch[3])] : [0,0,0]
    const uptime = uptimeOut.match(/up\s+([^,]+),/)?.[1]?.trim() || 'N/A'

    const memLine = memOut.split('\n').find(l => l.startsWith('Mem:'))
    let mem = { total: 0, used: 0, free: 0, available: 0, swapTotal: 0, swapUsed: 0 }
    if (memLine) {
      const p = memLine.trim().split(/\s+/)
      mem.total = parseInt(p[1]); mem.used = parseInt(p[2]); mem.free = parseInt(p[3]); mem.available = parseInt(p[6] || p[4])
      const swapLine = memOut.split('\n').find(l => l.startsWith('Swap:'))
      if (swapLine) {
        const sw = swapLine.trim().split(/\s+/)
        mem.swapTotal = parseInt(sw[1]); mem.swapUsed = parseInt(sw[2])
      }
    }

    const dparts = diskOut.trim().split(/\s+/)
    const diskUsage = parseFloat(dparts[4].replace('%', '')) || 0
    const disk = {
      mountPoint: dparts[5] || '/',
      total: parseInt(dparts[1]) * 1024,
      used: parseInt(dparts[2]) * 1024,
      available: parseInt(dparts[3]) * 1024,
      usagePercent: diskUsage
    }

    const metrics = { uptime, loadAverage: loadAvg, memory: mem, disk }
    const status = diskUsage >= 90 ? ServerStatus.WARNING : ServerStatus.HEALTHY
    return ServerHealth.healthy(server, metrics, [])
  } catch (error) {
    return ServerHealth.offline(server, error.message)
  }
}

// ============ 密码检查 ============

async function checkServerPasswords(server, ssh) {
  try {
    const usersOut = await ssh.execute(server, 'cat /etc/shadow 2>/dev/null | cut -d: -f1 | grep -v "^[$!*]$" | head -20')
    const users = usersOut.trim().split('\n').filter(u => u.trim())
    if (users.length === 0) return []

    const userInfos = []
    for (const username of users) {
      try {
        const chageOut = await ssh.execute(server, `chage -l "${username}" 2>/dev/null`)
        const lastChanged = chageOut.match(/Last password change\s*:\s*(.+)/)?.[1]?.trim() || '-'
        const expires = chageOut.match(/Password expires\s*:\s*(.+)/)?.[1]?.trim() || '-'
        const maxDays = chageOut.match(/Maximum number of days between password change\s*:\s*(.+)/)?.[1]?.trim() || '-'

        let status = '✅ 有效'
        let daysLeft
        if (expires === 'never') status = '⚠️ 永不过期'
        else if (expires !== '-') {
          const exp = new Date(expires)
          const now = new Date()
          daysLeft = Math.ceil((exp - now) / (1000 * 60 * 60 * 24))
          if (daysLeft < 0) status = '❌ 已过期'
          else if (daysLeft <= 7) status = '⚠️ 即将过期'
        }
        userInfos.push({ user: username, lastChanged, expires, maxDays, status, daysLeft })
      } catch { userInfos.push({ user: username, status: '❌ 检查失败' }) }
    }
    return userInfos
  } catch { return [] }
}

// ============ 格式化 ============

function formatBytes(bytes) {
  if (bytes >= 1073741824) return `${(bytes / 1073741824).toFixed(1)}GB`
  if (bytes >= 1048576) return `${(bytes / 1048576).toFixed(1)}MB`
  if (bytes >= 1024) return `${(bytes / 1024).toFixed(1)}KB`
  return `${bytes}B`
}

function getStatusDisplay(status) {
  switch (status) {
    case ServerStatus.HEALTHY: return '✅ 健康'
    case ServerStatus.WARNING: return '⚠️ 警告'
    case ServerStatus.OFFLINE: return '❌ 离线'
    default: return '❓ 未知'
  }
}

function formatClusterReport(serverHealthList) {
  const lines = []
  lines.push('### 🖥️ 服务器集群状态\n')
  lines.push('| 服务器名称 | IP地址 | 端口 | 用户 | 状态 | 运行时间 | 负载(1/5/15) | 内存使用 | 磁盘根分区 | Swap使用 |')
  lines.push('|-----------|--------|------|------|------|----------|-------------|----------|------------|----------|')

  for (const h of serverHealthList) {
    const s = h.server
    const load = h.metrics ? `${h.metrics.loadAverage[0].toFixed(2)}, ${h.metrics.loadAverage[1].toFixed(2)}, ${h.metrics.loadAverage[2].toFixed(2)}` : '-'
    const uptime = h.metrics?.uptime || '-'
    const mem = h.metrics ? `${formatBytes(h.metrics.memory.used)}/${formatBytes(h.metrics.memory.total)}` : '-'
    const disk = h.metrics ? `${formatBytes(h.metrics.disk.used)}/${formatBytes(h.metrics.disk.total)} (${h.metrics.disk.usagePercent}%)` : '-'
    const swap = h.metrics && h.metrics.memory.swapTotal > 0
      ? `${formatBytes(h.metrics.memory.swapUsed)}/${formatBytes(h.metrics.memory.swapTotal)}`
      : '-'
    lines.push(`| ${s.getDisplayName()} | ${s.host} | ${s.port} | ${s.user} | ${getStatusDisplay(h.status)} | ${uptime} | ${load} | ${mem} | ${disk} | ${swap} |`)
  }

  lines.push('')
  return lines.join('\n')
}

// ============ 主应用 ============

class OpsMaintenance {
  constructor() {
    this.configManager = new ConfigManager()
    this.sshClient = new SSHClient()
    this.credsProvider = new EnvCredentialsProvider()
    this.sshClient.setCredentialsProvider(this.credsProvider)
    this.configManager.startWatch()
  }

  async init() { await this.configManager.load() }

  async cluster() {
    await this.init()
    const servers = this.configManager.getAll()
    const healthList = []
    for (const server of servers) {
      const health = await checkServerHealth(server, this.sshClient)
      healthList.push(health)
    }
    return formatClusterReport(healthList)
  }

  async password(tags) {
    await this.init()
    const servers = tags ? this.configManager.getByTags(tags) : this.configManager.getAll()
    const results = []
    for (const server of servers) {
      const users = await checkServerPasswords(server, this.sshClient)
      let status = '✅ 正常'
      let details = `共 ${users.length} 个用户`
      const expired = users.filter(u => u.status.includes('已过期'))
      if (expired.length > 0) {
        status = '❌ 有密码已过期'
        details = `${expired.length} 个: ${expired.map(u => u.user).join(', ')}`
      }
      results.push({ server: server.getDisplayName(), host: server.host, status, details, users })
    }
    return this.formatPasswordReport(results)
  }

  formatPasswordReport(results) {
    const lines = []
    lines.push('### 🔐 服务器密码过期检查\n')
    lines.push('| 服务器名称 | IP地址 | 状态 | 概要 |')
    lines.push('|-----------|--------|------|------|')
    for (const r of results) {
      const emoji = r.status.includes('已过期') ? '❌' : r.status.includes('即将过期') ? '⚠️' : '✅'
      lines.push(`| ${r.server} | ${r.host} | ${emoji} ${r.status} | ${r.details} |`)
    }
    lines.push('')
    for (const r of results) {
      if (r.users && r.users.length > 0) {
        lines.push(`#### 📊 ${r.server}`)
        lines.push('| 用户 | 上次修改 | 过期日期 | 最大天数 | 剩余天数 | 状态 |')
        lines.push('|------|----------|----------|----------|----------|------|')
        for (const u of r.users) {
          const daysStr = u.daysLeft !== undefined ? (u.daysLeft < 0 ? `已过期${Math.abs(u.daysLeft)}天` : `${u.daysLeft}天`) : '-'
          const emoji = u.status.includes('已过期') ? '❌' : u.status.includes('即将过期') ? '⚠️' : '✅'
          lines.push(`| ${u.user} | ${u.lastChanged} | ${u.expires} | ${u.maxDays} | ${daysStr} | ${emoji} ${u.status} |`)
        }
        lines.push('')
      }
    }
    return lines.join('\n')
  }

  async shutdown() {
    this.configManager.stop()
    await this.sshClient.disconnectAll()
  }
}

// ============ 入口 ============

async function main() {
  const args = process.argv.slice(2)
  const app = new OpsMaintenance()

  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    console.log(`
🛠️  ops-maintenance 2.0 - 运维助手

用法:
  node run.js <action> [options]

操作:
  cluster / health       - 集群健康检查
  password / passwd      - 密码过期检查
  disk / space           - 磁盘检查（开发中）
  logs <pattern>         - 日志分析（开发中）
  perf                   - 性能监控（开发中）

选项:
  @<tag>                - 按标签筛选 (如 @production)
  --json, -j            - JSON 输出
  --help, -h            - 显示帮助

示例:
  node run.js cluster                  # 集群检查
  node run.js password @production     # 生产环境密码检查
  node run.js password --json          # JSON 格式

    `)
    process.exit(0)
  }

  try {
    await app.init()
    const action = args[0]
    const tags = args.filter(a => a.startsWith('@')).map(a => a.substring(1))
    const isJson = args.includes('--json') || args.includes('-j')

    let result
    if (action === 'cluster' || action === 'health' || action === 'check') {
      result = await app.cluster()
    } else if (action === 'password' || action === 'passwd' || action === 'expire') {
      result = await app.password(tags)
    } else {
      console.log(`未知操作: ${action}`)
      console.log('使用 --help 查看可用命令')
      process.exit(1)
    }

    console.log(result)
  } catch (error) {
    console.error('❌ 错误:', error.message)
    process.exit(1)
  } finally {
    await app.shutdown()
  }
}

main().catch(err => { console.error('运行失败:', err); process.exit(1) })