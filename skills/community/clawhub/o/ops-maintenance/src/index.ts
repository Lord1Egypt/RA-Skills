/**
 * 运维助手 Skill 实现
 *
 * ⚠️  平台限制：本技能仅支持 Linux/macOS 系统
 * - 所有本地检查功能（checkHealth、checkPerformance 等）依赖 Unix 命令
 * - Windows 系统上运行时将提示使用远程服务器检查
 *
 * 本模块提供运维检查功能，供 AI 助手调用
 */

import { exec } from 'child_process'
import { promisify } from 'util'
import { readFile, writeFile } from 'fs/promises'
import { join } from 'path'
import { existsSync, readFileSync } from 'fs'
import { Client } from 'ssh2'

const execAsync = promisify(exec)

/**
 * SSH 配置
 */
export interface SSHConfig {
  host: string
  port?: number
  user?: string
  password?: string  // 密码认证（可选）
  keyFile?: string
  name?: string  // 友好名称
  tags?: string[]  // 分组标签
}

/**
 * 服务器集群配置
 */
export interface ClusterConfig {
  name: string
  servers: SSHConfig[]
}

/**
 * 密码用户详细信息
 */
interface PasswordUserInfo {
  user: string
  lastChanged: string
  expires: string
  maxDays: string
  status: string
  daysLeft?: number
}

/**
 * 服务器列表配置文件路径
 */
function getServersConfigPath(): string {
  // 兼容 Windows 和 Unix 路径
  const home = process.env.HOME || process.env.USERPROFILE || '~'
  return join(home, '.config', 'ops-maintenance', 'servers.json')
}

/**
 * 服务器状态追踪文件路径（记录上次检查的服务器列表和修改时间）
 */
function getServerStatePath(): string {
  const home = process.env.HOME || process.env.USERPROFILE || '~'
  return join(home, '.config', 'ops-maintenance', 'server-state.json')
}

/**
 * 默认服务器配置目录
 */
function getConfigDir(): string {
  const home = process.env.HOME || process.env.USERPROFILE || '~'
  return join(home, '.config', 'ops-maintenance')
}

/**
 * 保存服务器列表
 */
export async function saveServers(servers: SSHConfig[]): Promise<void> {
  const configDir = getConfigDir()
  const configPath = getServersConfigPath()
  
  // 确保目录存在
  if (!existsSync(configDir)) {
    await execAsync(`mkdir -p "${configDir}"`)
  }
  
  await writeFile(configPath, JSON.stringify(servers, null, 2))
}

/**
 * 服务器状态追踪（记录上次检查时的服务器列表）
 */
interface ServerState {
  lastModified: number  // 配置文件最后修改时间
  serverChecksums: string[]  // 服务器的唯一标识（host:port:user）
  timestamp: number  // 上次检查的时间戳
}

/**
 * 加载服务器状态追踪
 */
async function loadServerState(): Promise<ServerState | null> {
  const statePath = getServerStatePath()
  try {
    const content = await readFile(statePath, 'utf-8')
    return JSON.parse(content)
  } catch {
    return null
  }
}

/**
 * 保存服务器状态追踪
 */
async function saveServerState(state: ServerState): Promise<void> {
  const stateDir = getConfigDir()
  const statePath = getServerStatePath()

  if (!existsSync(stateDir)) {
    await execAsync(`mkdir -p "${stateDir}"`)
  }

  await writeFile(statePath, JSON.stringify(state, null, 2))
}

/**
 * 计算服务器列表的校验和数组
 */
function calculateServerChecksums(servers: SSHConfig[]): string[] {
  return servers
    .map(s => `${s.host}:${s.port || 22}:${s.user || 'root'}`)
    .sort()
}

/**
 * 获取文件最后修改时间戳
 */
async function getFileMtime(path: string): Promise<number> {
  const { statSync } = await import('fs')
  try {
    const stats = statSync(path)
    return Math.floor(stats.mtimeMs) // 毫秒时间戳
  } catch {
    return 0
  }
}

/**
 * 检测新增服务器
 */
export async function detectNewServers(): Promise<{
  newServers: SSHConfig[];
  allServers: SSHConfig[];
  message: string;
}> {
  const currentState = await loadServerState()

  // 使用简单加载函数避免循环依赖
  const servers = await loadServersSimple()

  // 获取配置文件的最后修改时间
  const configPath = getServersConfigPath()
  const lastModified = await getFileMtime(configPath) || Date.now()

  // 计算当前服务器校验和
  const currentChecksums = calculateServerChecksums(servers)

  let newServers: SSHConfig[] = []
  let message = ''

  if (!currentState) {
    // 首次检查
    message = `📋 首次扫描，发现 ${servers.length} 台配置的服务器`
  } else if (lastModified !== currentState.lastModified) {
    // 配置文件已修改，检查新增的服务器
    const previousChecksums = new Set(currentState.serverChecksums)
    newServers = servers.filter(s => !previousChecksums.has(`${s.host}:${s.port || 22}:${s.user || 'root'}`))

    if (newServers.length > 0) {
      message = `🆕 检测到 ${newServers.length} 台新增服务器:\n${newServers.map(s => `  - ${s.name || s.host} (${s.user}@${s.host}:${s.port || 22})`).join('\n')}`
    } else {
      message = `✅ 配置文件已更新，但未发现新增服务器（可能是修改了现有配置）`
    }
  } else {
    // 配置文件未修改
    message = `📊 当前配置了 ${servers.length} 台服务器，无新增`
  }

  // 保存当前状态
  await saveServerState({
    lastModified,
    serverChecksums: currentChecksums,
    timestamp: Date.now()
  })

  return { newServers, allServers: servers, message }
}

/**
 * 内部使用：简单加载服务器列表（不触发检测）
 */
async function loadServersSimple(): Promise<SSHConfig[]> {
  const configPath = getServersConfigPath()

  try {
    const content = await readFile(configPath, 'utf-8')
    return JSON.parse(content)
  } catch {
    // 尝试从 SSH config 加载
    return loadSSHConfig()
  }
}

/**
 * 加载服务器列表（带变更检测）
 */
export async function loadServers(): Promise<SSHConfig[]> {
  const { allServers } = await detectNewServers()
  return allServers
}

/**
 * 从 SSH config 文件加载服务器（简化版本）
 */
function loadSSHConfig(): SSHConfig[] {
  // 如果没有 SSH config 文件，返回空数组
  return []
}

/**
 * 添加服务器
 */
export async function addServer(config: SSHConfig): Promise<void> {
  const servers = await loadServers()
  
  // 检查是否已存在
  const existing = servers.findIndex(s => s.host === config.host)
  if (existing >= 0) {
    servers[existing] = { ...servers[existing], ...config }
  } else {
    servers.push(config)
  }
  
  await saveServers(servers)
}

/**
 * 移除服务器
 */
export async function removeServer(host: string): Promise<void> {
  const servers = await loadServers()
  const filtered = servers.filter(s => s.host !== host)
  await saveServers(filtered)
}

/**
 * 按标签筛选服务器
 */
export async function getServersByTag(tag: string): Promise<SSHConfig[]> {
  const servers = await loadServers()
  return servers.filter(s => s.tags?.includes(tag))
}

/**
 * 批量检查所有服务器健康状态
 */
export async function checkAllServersHealth(
  tags?: string[],
  serverList?: SSHConfig[]  // 可选的服务器列表，避免重复检测
): Promise<{ server: string; status: string; details: string }[]> {
  const servers = serverList
    ? serverList
    : (tags
      ? await Promise.all(tags.map(getServersByTag)).then(arr => arr.flat())
      : await loadServers())

  const results: { server: string; status: string; details: string }[] = []

  for (const config of servers) {
    const name = config.name || config.host

    try {
      // 并行执行多个检查
      const [load, mem, disk] = await Promise.all([
        runRemoteCommand(config, 'uptime'),
        runRemoteCommand(config, 'free -h 2>/dev/null || echo "N/A"'),
        runRemoteCommand(config, 'df -h / | tail -1 | awk \'{print $5}\'')
      ])

      // 解析磁盘使用率
      const diskUsage = disk.includes('%') ? disk.match(/(\d+)%/)?.[1] || 'N/A' : 'N/A'
      const isHealthy = parseInt(diskUsage) < 90

      results.push({
        server: name,
        status: isHealthy ? '✅ 健康' : '⚠️ 磁盘 ' + diskUsage,
        details: `负载: ${load.split('load averages:')[1]?.trim() || 'N/A'}`
      })
    } catch (error: any) {
      results.push({
        server: name,
        status: '❌ 离线',
        details: error.message.substring(0, 50)
      })
    }
  }

  return results
}

/**
 * 批量执行命令到所有服务器
 */
export async function executeOnAllServers(
  command: string,
  tags?: string[]
): Promise<{ server: string; output: string }[]> {
  const servers = tags 
    ? await Promise.all(tags.map(getServersByTag)).then(arr => arr.flat())
    : await loadServers()
  
  const results: { server: string; output: string }[] = []
  
  // 并行执行
  await Promise.all(servers.map(async (config) => {
    const name = config.name || config.host
    try {
      const output = await runRemoteCommand(config, command)
      results.push({ server: name, output })
    } catch (error: any) {
      results.push({ server: name, output: `错误: ${error.message}` })
    }
  }))
  
  return results
}

/**
 * 批量添加服务器 (支持 IP:Port 格式)
 * 
 * @param servers 服务器列表，格式:
 *   - "192.168.1.100" (默认端口22)
 *   - "192.168.1.100:2222" (自定义端口)
 *   - "user@192.168.1.100" (指定用户)
 *   - "user@192.168.1.100:2222" (完整格式)
 *   - JSON 字符串数组
 */
export async function batchAddServers(servers: string[]): Promise<{ success: number; failed: number; details: string[] }> {
  const results: string[] = []
  let success = 0
  let failed = 0

  // 解析每个服务器字符串
  for (const serverStr of servers) {
    try {
      const config = parseServerString(serverStr)
      await addServer(config)
      success++
      results.push(`✅ ${config.name || config.host}:${config.port || 22} - 已添加`)
    } catch (error: any) {
      failed++
      results.push(`❌ ${serverStr} - ${error.message}`)
    }
  }

  return { success, failed, details: results }
}

/**
 * 从 CSV/JSON 批量导入
 * 
 * CSV 格式: host,port,user,name,tags
 * JSON 格式: 数组或单对象
 */
export async function importServersFromText(text: string): Promise<{ success: number; failed: number; servers: SSHConfig[] }> {
  const servers: SSHConfig[] = []
  let failed = 0

  // 尝试解析为 JSON
  try {
    const parsed = JSON.parse(text)
    const arr = Array.isArray(parsed) ? parsed : [parsed]
    for (const item of arr) {
      if (item.host) {
        servers.push({
          host: item.host,
          port: item.port || 22,
          user: item.user,
          name: item.name,
          tags: item.tags
        })
      }
    }
    if (servers.length > 0) {
      await saveServers([...await loadServers(), ...servers])
      return { success: servers.length, failed: 0, servers }
    }
  } catch {
    // 不是 JSON，尝试 CSV
  }

  // CSV 解析
  const lines = text.split('\n').filter(l => l.trim() && !l.startsWith('#'))
  for (const line of lines) {
    const parts = line.split(',').map(p => p.trim())
    if (parts[0]) {
      const hostPort = parts[0].split(':')
      servers.push({
        host: hostPort[0],
        port: hostPort[1] ? parseInt(hostPort[1]) : 22,
        user: parts[2] || undefined,
        name: parts[3] || undefined,
        tags: parts[4] ? parts[4].split(';') : undefined
      })
    }
  }

  // 保存
  const existing = await loadServers()
  await saveServers([...existing, ...servers])

  return { success: servers.length, failed, servers }
}

/**
 * 解析服务器字符串为配置
 * 
 * 支持格式:
 *   192.168.1.100
 *   192.168.1.100:2222
 *   user@192.168.1.100
 *   user@192.168.1.100:2222
 */
function parseServerString(serverStr: string): SSHConfig {
  let host = serverStr
  let user: string | undefined
  let port: number | undefined

  // 提取用户
  if (host.includes('@')) {
    const parts = host.split('@')
    user = parts[0]
    host = parts[1]
  }

  // 提取端口
  if (host.includes(':')) {
    const parts = host.split(':')
    host = parts[0]
    port = parseInt(parts[1])
  }

  // 生成友好名称
  const name = `server-${host.replace(/\./g, '-')}`

  return { host, port: port || 22, user, name }
}

/**
 * 服务器状态摘要
 */
/**
 * 格式化字节为人类可读格式 (GiB, MiB)
 */
function formatBytes(bytes: number): string {
  if (bytes >= 1073741824) {
    return `${(bytes / 1073741824).toFixed(1).replace(/\.0$/, '')}GiB`
  } else if (bytes >= 1048576) {
    return `${Math.round(bytes / 1048576)}MiB`
  } else if (bytes >= 1024) {
    return `${Math.round(bytes / 1024)}KiB`
  }
  return `${bytes}B`
}

/**
 * 从 free -h 输出中提取数字字节值（单位可能是 kB/MB/GB）
 */
function parseSizeToBytes(str: string): number {
  if (!str) return 0
  const match = str.trim().match(/^([\d.]+)([KMGT]?)(i?B?)$/)
  if (!match) return 0
  const value = parseFloat(match[1])
  const unit = (match[2] + match[3]).toUpperCase()
  const units: Record<string, number> = {
    'B': 1,
    'KB': 1000,
    'KIB': 1024,
    'MB': 1000000,
    'MIB': 1048576,
    'GB': 1000000000,
    'GIB': 1073741824,
    'TB': 1000000000000,
    'TIB': 1099511627776
  }
  const multiplier = units[unit] || 1
  return Math.round(value * multiplier)
}

/**
 * 服务器状态摘要（表格形式）
 */
export async function getClusterSummary(): Promise<string> {
  // 1️⃣ 首先检测服务器配置变更
  const { message: changeMessage, allServers, newServers } = await detectNewServers()

  // 2️⃣ 执行健康检查（使用已加载的服务器列表避免重复检测）
  const results = await checkAllServersHealth(undefined, allServers)

  const online = results.filter(r => r.status.includes('健康')).length
  const warning = results.filter(r => r.status.includes('⚠️')).length
  const offline = results.filter(r => r.status.includes('❌')).length

  const lines: string[] = []
  lines.push('### 🖥️ 服务器集群状态\n')

  // 添加服务器变更检测信息
  lines.push(`**配置变更检测**: ${changeMessage}\n`)

  // 如果是新增服务器，高亮显示
  if (newServers.length > 0) {
    lines.push('**🎉 新增服务器:**')
    for (const s of newServers) {
      lines.push(`- ${s.name || s.host} (${s.user}@${s.host}:${s.port || 22})`)
    }
    lines.push('')
  }

  // 集群概览表格
  lines.push('#### 集群概览\n')
  lines.push('| 服务器名称 | IP地址 | 端口 | 用户 | 状态 | 运行时间 | 负载(1/5/15) | 内存使用 | 磁盘根分区 | Swap使用 |')
  lines.push('|-----------|--------|------|------|------|----------|-------------|----------|------------|----------|')

  // 为每台服务器收集详细信息并填充表格
  const serverDetails: any[] = []
  for (let i = 0; i < allServers.length; i++) {
    const server = allServers[i]
    const result = results[i]
    const name = server.name || server.host
    const host = server.host
    const port = server.port || 22
    const user = server.user || 'root'

    // 解析详细信息
    let uptime = '-'
    let load = '-'
    let mem = '-'
    let disk = '-'
    let swap = '-'
    let memUsedPct = 0
    let diskUsedPct = 0
    let swapUsedPct = 0

    // 判断服务器状态（用于详情获取）
    const _isHealthy = result.status.includes('健康')
    const _isWarning = result.status.includes('⚠️') || result.status.includes('警告') || result.status.includes('磁盘')
    const _isOffline = result.status.includes('❌') || result.status.includes('离线')

    const canFetchDetails = _isHealthy || _isWarning
    if (canFetchDetails) {
      try {
        // 尝试从详情中提取信息
        const details = result.details
        if (details && details !== result.status) {
          // 提取负载信息
          const loadMatch = details.match(/负载:\s*(.+)/)
          if (loadMatch) {
            load = loadMatch[1].trim()
          }
        }

        // 通过额外命令获取更详细信息
        try {
          const uptimeOutput = await runRemoteCommand(server, 'uptime')
          const uptimeMatch = uptimeOutput.match(/up\s+([^,]+),/)
          if (uptimeMatch) {
            uptime = uptimeMatch[1].trim()
          }
        } catch {}

        try {
          // 1. 获取易读格式用于显示
          const memOutputHr = await runRemoteCommand(server, 'free -h 2>/dev/null || free -k 2>/dev/null || echo "N/A"')
          const memLineHr = memOutputHr.split('\n').find(l => l.includes('Mem:'))
          if (memLineHr) {
            const partsHr = memLineHr.trim().split(/\s+/)
            if (partsHr.length >= 7) {
              const totalHr = partsHr[1]
              const usedHr = partsHr[2]
              if (totalHr && usedHr) {
                mem = `${usedHr}/${totalHr}`
              }
            }
          }

          // 2. 获取字节格式用于计算百分比
          const memOutput = await runRemoteCommand(server, 'free -b 2>/dev/null || free 2>/dev/null')
          const memLine = memOutput.split('\n').find(l => l.includes('Mem:'))
          if (memLine) {
            const parts = memLine.trim().split(/\s+/)
            if (parts.length >= 7) {
              const total = parseInt(parts[1])
              const used = parseInt(parts[2])
              if (total > 0) {
                memUsedPct = Math.round((used / total) * 100)
              }
            }
          }
        } catch {}

        try {
          const diskOutput = await runRemoteCommand(server, 'df -h / 2>/dev/null | tail -1')
          const parts = diskOutput.trim().split(/\s+/)
          if (parts.length >= 6) {
            const used = parts[4]
            const total = parts[1]
            disk = `${used}/${total}`
            // 从输出中提取百分比，通常是第5列 (索引4)
            const usePercent = parseInt(parts[4].replace('%', '')) || parseInt(parts[5].replace('%', '')) || 0
            diskUsedPct = usePercent
          }
        } catch {}

        try {
          // 1. 易读格式用于显示
          const swapOutputHr = await runRemoteCommand(server, 'free -h 2>/dev/null | grep Swap')
          if (swapOutputHr) {
            const partsHr = swapOutputHr.trim().split(/\s+/)
            if (partsHr.length >= 3) {
              swap = `${partsHr[2]}/${partsHr[1]}`
            }
          }

          // 2. 字节格式用于计算百分比
          const swapOutput = await runRemoteCommand(server, 'free -b 2>/dev/null | grep Swap')
          if (swapOutput && swapOutput.includes('Swap')) {
            const parts = swapOutput.trim().split(/\s+/)
            if (parts.length >= 3) {
              const total = parseInt(parts[1])
              const used = parseInt(parts[2])
              if (total > 0) {
                swapUsedPct = Math.round((used / total) * 100)
              }
            }
          }
        } catch {}
      } catch {
        // 忽略详细信息的获取错误
      }
    }

    // 状态格式化
    let statusDisplay = result.status
    if (_isHealthy) {
      statusDisplay = '✅ 健康'
    } else if (_isWarning) {
      statusDisplay = '⚠️ 警告'
    } else if (_isOffline) {
      statusDisplay = '❌ 离线'
    }

    lines.push(`| ${name} | ${host} | ${port} | ${user} | ${statusDisplay} | ${uptime} | ${load} | ${mem} | ${disk} | ${swap} |`)

    // 保存详细信息用于后续建议生成
    serverDetails.push({
      name,
      host,
      status: result.status,
      memUsedPct,
      diskUsedPct,
      swapUsedPct,
      connectionOk: _isHealthy || _isWarning
    })
  }

  lines.push('')

  // 3️⃣ 为每台服务器添加详细报告
  for (const server of allServers) {
    const name = server.name || server.host
    lines.push(`## 📊 ${name} 详细健康检查\n`)

    try {
      // 获取详细信息（包括系统信息、服务状态等）
      const detailReport = await checkRemoteHealth(server)
      lines.push(detailReport)
      lines.push('') // 空行分隔
    } catch (error: any) {
      lines.push(`❌ **连接失败**: ${error.message}\n`)
    }
  }

  // 4️⃣ 生成优化建议和操作步骤（表格形式）
  lines.push('### 💡 优化建议与操作步骤\n')
  lines.push('| 服务器 | 问题分类 | 严重等级 | 优化建议 | 操作步骤 |')
  lines.push('|--------|----------|----------|----------|----------|')

  const recommendations = generateRecommendations(serverDetails)
  for (const rec of recommendations) {
    lines.push(`| ${rec.server} | ${rec.category} | ${rec.severity} | ${rec.suggestion} | ${rec.steps} |`)
  }

  return lines.join('\n')
}

/**
 * 生成优化建议
 */
function generateRecommendations(serverDetails: any[]): any[] {
  const recommendations: any[] = []

  for (const detail of serverDetails) {
    const serverName = detail.name

    if (!detail.connectionOk) {
      recommendations.push({
        server: serverName,
        category: '连接问题',
        severity: '🔴 高',
        suggestion: 'SSH 连接失败，服务器不可达',
        steps: '1. 检查网络连通性<br>2. 确认 SSH 服务运行状态<br>3. 检查防火墙规则<br>4. 验证用户名/密码/密钥配置'
      })
      continue
    }

    // 检查 Swap 使用率
    if (detail.swapUsedPct >= 90) {
      recommendations.push({
        server: serverName,
        category: '内存瓶颈',
        severity: '🔴 高',
        suggestion: 'Swap 使用率超过 90%，内存严重不足',
        steps: '1. 增加物理内存<br>2. 优化应用内存使用<br>3. 检查内存泄漏<br>4. 调整 swappiness 参数'
      })
    } else if (detail.swapUsedPct >= 70) {
      recommendations.push({
        server: serverName,
        category: '内存压力',
        severity: '🟡 中',
        suggestion: 'Swap 使用率超过 70%，内存使用较高',
        steps: '1. 监控内存使用趋势<br>2. 识别高内存占用进程<br>3. 考虑增加内存'
      })
    }

    // 检查磁盘使用率
    if (detail.diskUsedPct >= 90) {
      recommendations.push({
        server: serverName,
        category: '磁盘空间',
        severity: '🔴 高',
        suggestion: '根分区使用率超过 90%，空间紧张',
        steps: '1. 清理日志文件<br>2. 删除临时不用的文件<br>3. 清理包管理器缓存<br>4. 扩展磁盘容量'
      })
    } else if (detail.diskUsedPct >= 80) {
      recommendations.push({
        server: serverName,
        category: '磁盘空间',
        severity: '🟡 中',
        suggestion: '根分区使用率超过 80%，建议清理',
        steps: '1. 查找大文件并清理<br>2. 归档旧日志<br>3. 清理未使用的软件包'
      })
    }

    // 检查内存使用率
    if (detail.memUsedPct >= 90) {
      recommendations.push({
        server: serverName,
        category: '内存瓶颈',
        severity: '🔴 高',
        suggestion: '物理内存使用率超过 90%',
        steps: '1. 立即重启高内存进程<br>2. 增加 swap 空间<br>3. 增加物理内存<br>4. 优化应用配置'
      })
    } else if (detail.memUsedPct >= 80) {
      recommendations.push({
        server: serverName,
        category: '内存压力',
        severity: '🟡 中',
        suggestion: '物理内存使用率超过 80%',
        steps: '1. 监控内存使用趋势<br>2. 识别内存消耗大户<br>3. 优化 JVM/应用堆配置'
      })
    }

    // 检查服务状态
    if (detail.status.includes('警告')) {
      recommendations.push({
        server: serverName,
        category: '服务异常',
        severity: '🟠 警告',
        suggestion: '必需服务未正常运行',
        steps: '1. 检查服务日志<br>2. 重启异常服务<br>3. 检查配置文件<br>4. 查看资源使用情况'
      })
    }
  }

  // 如果没有发现问题，添加一个积极建议
  if (recommendations.length === 0) {
    recommendations.push({
      server: '所有服务器',
      category: '状态良好',
      severity: '🟢 低',
      suggestion: '所有服务器运行状态正常',
      steps: '继续保持定期巡检，关注趋势变化'
    })
  }

  return recommendations
}

/**
 * 通过 SSH 执行远程命令
 */
/**
 * 通过 SSH 执行远程命令（支持密码认证）
 */
export async function runRemoteCommand(
  config: SSHConfig,
  command: string
): Promise<string> {
  return new Promise((resolve, reject) => {
    const conn = new Client()

    conn.on('ready', () => {
      conn.exec(command, (err: Error | undefined, stream: any) => {
        if (err) {
          conn.end()
          reject(err)
          return
        }

        let output = ''
        stream.on('data', (data: Buffer) => {
          output += data.toString()
        }).on('close', () => {
          conn.end()
          resolve(output || '(无输出)')
        })
      })
    })

    conn.on('error', (err: any) => {
      reject(err)
    })

    conn.on('close', () => {})

    try {
      const connectOptions: any = {
        host: config.host,
        port: config.port || 22,
        readyTimeout: 10000,
        keepaliveInterval: 5000,
        keepaliveCountMax: 3
      }

      if (config.user) {
        connectOptions.username = config.user
      } else {
        connectOptions.username = 'root'
      }

      if (config.password) {
        connectOptions.password = config.password
      } else if (config.keyFile) {
        connectOptions.privateKey = readFileSync(config.keyFile)
      }

      conn.connect(connectOptions)
    } catch (err) {
      reject(err)
    }
  })
}

/**
 * 执行系统命令并返回结果
 */
export async function runCommand(cmd: string, timeout: number = 10000): Promise<string> {
    // 在非 Linux/macOS 平台（如 Windows）上给出友好提示
    if (process.platform === 'win32') {
        return '⚠️ 当前系统为 Windows，runCommand 只能在 Linux/macOS 上执行。请改用远程服务器检查或在 Linux 环境中运行。';
    }
    try {
        // 默认使用 zsh（Linux/macOS）
        const { stdout, stderr } = await execAsync(cmd, { timeout, shell: '/bin/zsh' });
        return stdout || stderr || '(无输出)';
    } catch (error: any) {
        return `命令执行失败: ${error.message}`;
    }
}

/**
 * 系统健康检查
 */
export async function checkHealth(): Promise<string> {
  const results: string[] = []
  
  results.push('### 🩺 系统健康检查\n')
  
  // 负载
  results.push('**负载:**')
  results.push('```\n' + await runCommand('uptime') + '```\n')
  
  // 内存
  results.push('**内存:**')
  results.push('```\n' + await runCommand('vm_stat | head -10') + '```\n')
  
  // 磁盘
  results.push('**磁盘:**')
  results.push('```\n' + await runCommand('df -h | grep -E "^/dev"') + '```\n')
  
  // 核心服务状态
  const services = ['nginx', 'docker', 'postgresql', 'redis-server']
  results.push('**服务状态:**')
  for (const svc of services) {
    const status = await runCommand(`pgrep -f "${svc}" > /dev/null && echo "运行中" || echo "已停止"`)
    const emoji = status.includes('运行中') ? '✅' : '❌'
    results.push(`- ${svc}: ${emoji} ${status.trim()}`)
  }
  
  return results.join('\n')
}

/**
 * 日志分析
 */
export async function analyzeLogs(pattern: string = 'error', lines: number = 30): Promise<string> {
  const results: string[] = []
  results.push(`### 📋 日志分析 (搜索: "${pattern}")\n`)
  
  const logPaths = [
    '/var/log/system.log',
    `${process.env.HOME}/.npm/_logs/*.log`,
  ]
  
  for (const logPath of logPaths) {
    try {
      const output = await runCommand(`grep -i "${pattern}" "${logPath}" 2>/dev/null | tail -${lines}`)
      if (output && !output.includes('命令执行失败')) {
        results.push(`**${logPath}:**`)
        results.push('```\n' + output + '```')
      }
    } catch {
      // 跳过不存在的日志
    }
  }
  
  return results.join('\n') || '未找到匹配的日志'
}

/**
 * 性能监控 (适用于 Linux)
 * 在 Windows 上提示检查远程服务器
 */
export async function checkPerformance(): Promise<string> {
  const results: string[] = []
  results.push('### 📊 性能监控\n')

  // 检查是否为 Linux 系统
  const isLinux = await runCommand('uname -s 2>/dev/null')
  if (isLinux.includes('Linux')) {
    // CPU
    results.push('**CPU:**')
    results.push('```\n' + await runCommand('lscpu 2>/dev/null | head -10') + '```\n')

    // 内存和 CPU 使用
    results.push('**实时状态:**')
    results.push('```\n' + await runCommand('free -h && uptime') + '```\n')

    // 磁盘 I/O
    results.push('**磁盘 I/O:**')
    results.push('```\n' + await runCommand('iostat -d 2 2>/dev/null | tail -5 || echo "安装 sysstat 包以使用 iostat"') + '```\n')
  } else {
    // Windows/other - 提示检查远程服务器
    const servers = await loadServers()
    results.push('当前系统不支持本地性能监控，使用以下命令检查远程服务器：')
    results.push('')
    results.push('| 操作 | 命令 |')
    results.push('|------|------|')
    results.push(`| 全部服务器 | \`/ops-maintenance exec "free -h && uptime"\` |`)
    results.push(`| 单台 | \`/ops-maintenance user@host perf\` |`)

    if (servers.length > 0) {
      results.push('\n**已配置服务器:**')
      for (const s of servers) {
        results.push(`- ${s.name || s.host} (${s.user}@${s.host}:${s.port || 22})`)
      }
    }
  }

  return results.join('\n')
}

/**
 * 端口检查
 */
export async function checkPort(port?: number): Promise<string> {
  if (port) {
    return `### 🔌 端口 ${port}\n\`\`\`\n${await runCommand(`lsof -i :${port} 2>/dev/null || echo "端口未占用"`)}\n\`\`\``
  }
  
  return `### 🔌 监听端口\n\`\`\`\n${await runCommand('lsof -i -P | grep LISTEN | head -20')}\n\`\`\``
}

/**
 * 进程检查
 */
export async function checkProcess(name?: string): Promise<string> {
  if (name) {
    const output = await runCommand(`ps aux | grep -i "${name}" | grep -v grep | head -10`)
    const count = await runCommand(`pgrep -fc "${name}" 2>/dev/null || echo 0`)
    
    return `### ⚙️ 进程 "${name}"\n**运行实例: ${count.trim()}**\n\`\`\`\n${output || '未找到'}\n\`\`\``
  }
  
  return `### ⚙️ Top 进程 (按 CPU)\n\`\`\`\n${await runCommand('ps aux --sort=-%cpu | head -15')}\n\`\`\``
}

/**
 * 磁盘使用
 */
export async function checkDisk(): Promise<string> {
  const home = process.env.HOME || '~'

  const results: string[] = []
  results.push('### 💾 磁盘使用\n')

  results.push('**分区使用:**')
  results.push('```\n' + await runCommand('df -h') + '```\n')

  results.push('**大目录 (Home):**')
  results.push('```\n' + await runCommand(`du -sh "${home}"/* 2>/dev/null | sort -hr | head -10`) + '```')

  return results.join('\n')
}

/**
 * 密码过期检查 (本地)
 *
 * 支持 Linux (chage) 和 macOS 系统
 */
export async function checkPasswordExpiration(): Promise<string> {
  const results: string[] = []
  results.push('### 🔐 密码过期检查 (本地)\n')

  // 检查 chage 命令是否可用 (Linux)
  const chageAvailable = await runCommand('which chage 2>/dev/null && echo "available" || echo "unavailable"')

  if (chageAvailable.includes('available')) {
    // Linux: 获取所有有密码的用户
    const usersOutput = await runCommand('cat /etc/shadow 2>/dev/null | cut -d: -f1 | grep -v "^[$!*]$" | head -20')
    const users = usersOutput.trim().split('\n').filter(u => u.trim())

    if (users.length === 0) {
      results.push('未找到可检查的用户\n')
    } else {
      results.push('| 用户 | 上次修改 | 过期日期 | 最大天数 | 状态 |')
      results.push('|------|----------|----------|----------|------|')

      for (const user of users) {
        const u = user.trim()
        if (!u) continue
        try {
          const chageOutput = await runCommand(`chage -l "${u}" 2>/dev/null`)
          const lastChanged = chageOutput.match(/Last password change\s*:\s*(.+)/)?.[1]?.trim() || '-'
          const expires = chageOutput.match(/Password expires\s*:\s*(.+)/)?.[1]?.trim() || '-'
          const maxDays = chageOutput.match(/Maximum number of days between password change\s*:\s*(.+)/)?.[1]?.trim() || '-'

          // 判断状态
          let status = '✅ 有效'
          if (expires === 'never') {
            status = '⚠️ 永不过期'
          } else if (expires !== '-') {
            try {
              const expDate = new Date(expires)
              const now = new Date()
              const daysLeft = Math.ceil((expDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24))
              if (daysLeft < 0) {
                status = '❌ 已过期'
              } else if (daysLeft <= 7) {
                status = '⚠️ 即将过期'
              }
            } catch {}
          }

          results.push(`| ${u} | ${lastChanged} | ${expires} | ${maxDays} | ${status} |`)
        } catch {
          results.push(`| ${u} | - | - | - | ❌ 检查失败 |`)
        }
      }
    }
  } else {
    // macOS: 使用 PWPOLICY
    const pwdPolicyOutput = await runCommand('pwpolicy -getaccountpolicies 2>/dev/null | head -30')
    if (pwdPolicyOutput && !pwdPolicyOutput.includes('命令执行失败')) {
      results.push('**macOS 密码策略:**')
      results.push('```\n' + pwdPolicyOutput + '```\n')
    } else {
      results.push('无法获取密码过期信息 (不支持的系统)\n')
    }
  }

  return results.join('\n')
}

/**
 * 批量检查所有服务器密码过期状态
 * 检查每台服务器上所有用户的密码过期情况
 */
export async function checkAllServersPasswordExpiration(
  tags?: string[]
): Promise<Array<{
  server: string
  status: string
  details: string
  users?: PasswordUserInfo[]
}>> {
  const servers = tags
    ? await Promise.all(tags.map(getServersByTag)).then(arr => arr.flat())
    : await loadServers()

  const results: { server: string; status: string; details: string; users?: PasswordUserInfo[] }[] = []

  // 如果没有配置服务器，返回提示信息
  if (servers.length === 0) {
    results.push({
      server: '本地',
      status: '⚠️ 未配置服务器',
      details: '请在 ~/.config/ops-maintenance/servers.json 中添加服务器配置'
    })
    return results
  }

  for (const config of servers) {
    const name = config.name || config.host

    try {
      // 获取所有有密码的用户（排除系统用户）
      const usersOutput = await runRemoteCommand(config, 'cat /etc/shadow 2>/dev/null | cut -d: -f1 | grep -v "^[$!*]$" | head -20')
      const users = usersOutput.trim().split('\n').filter(u => u.trim())

      if (users.length === 0) {
        results.push({
          server: name,
          status: '✅ 无密码用户',
          details: '未找到需要检查的本地用户',
          users: []
        })
        continue
      }

      // 收集所有用户的详细信息
      const userDetails: Array<{
        user: string
        lastChanged: string
        expires: string
        maxDays: string
        status: string
        daysLeft?: number
      }> = []

      let hasExpired = false
      let hasWarning = false

      for (const user of users) {
        const u = user.trim()
        try {
          const chageOutput = await runRemoteCommand(config, `chage -l "${u}" 2>/dev/null`)
          const lastChanged = chageOutput.match(/Last password change\s*:\s*(.+)/)?.[1]?.trim() || '-'
          const expires = chageOutput.match(/Password expires\s*:\s*(.+)/)?.[1]?.trim() || '-'
          const maxDays = chageOutput.match(/Maximum number of days between password change\s*:\s*(.+)/)?.[1]?.trim() || '-'

          let userStatus = '✅ 有效'
          let daysLeftNum: number | undefined

          if (expires === 'never') {
            userStatus = '⚠️ 永不过期'
          } else if (expires !== '-') {
            try {
              const expDate = new Date(expires)
              const now = new Date()
              const daysLeft = Math.ceil((expDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24))
              daysLeftNum = daysLeft
              if (daysLeft < 0) {
                userStatus = '❌ 已过期'
                hasExpired = true
              } else if (daysLeft <= 7) {
                userStatus = '⚠️ 即将过期'
                hasWarning = true
              }
            } catch {}
          }

          userDetails.push({
            user: u,
            lastChanged,
            expires,
            maxDays,
            status: userStatus,
            daysLeft: daysLeftNum
          })
        } catch {
          userDetails.push({
            user: u,
            lastChanged: '-',
            expires: '-',
            maxDays: '-',
            status: '❌ 检查失败'
          })
        }
      }

      // 确定总体状态
      let status = '✅ 正常'
      let detail = `共 ${userDetails.length} 个用户`

      if (hasExpired) {
        status = '❌ 有密码已过期'
        const expiredUsers = userDetails.filter(u => u.status.includes('已过期')).map(u => u.user)
        detail = `${expiredUsers.length} 个用户密码已过期: ${expiredUsers.join(', ')}`
      } else if (hasWarning) {
        status = '⚠️ 有即将过期'
        const warningUsers = userDetails.filter(u => u.status.includes('即将过期')).map(u => `${u.user}(${u.daysLeft}天)`)
        detail = `${warningUsers.length} 个用户即将过期: ${warningUsers.join(', ')}`
      }

      results.push({
        server: name,
        status,
        details: detail,
        users: userDetails
      })
    } catch (error: any) {
      results.push({
        server: name,
        status: '❌ 检查失败',
        details: error.message.substring(0, 80),
        users: []
      })
    }
  }

  return results
}

/**
 * 生成密码过期检查的格式化报告
 */
export async function checkAllServersPasswordExpirationReport(
  tags?: string[]
): Promise<string> {
  const results = await checkAllServersPasswordExpiration(tags)
  const servers = await loadServers()
  const getServer = (name: string) => servers.find(s => (s.name || s.host) === name)

  const lines: string[] = []
  lines.push('### 🔐 服务器密码过期检查\n')

  // 检查是否有配置服务器
  const noServers = results.length === 1 && results[0].status.includes('未配置')
  if (noServers) {
    lines.push('| 服务器名称 | 状态 | 详细信息 |')
    lines.push('|-----------|------|----------|')
    lines.push(`| ${results[0].server} | ${results[0].status} | ${results[0].details} |`)
    lines.push('')
    lines.push('**请添加服务器后使用：**')
    lines.push('```')
    lines.push('/ops-maintenance add-server <IP> --name <名称> --user <用户>')
    lines.push('/ops-maintenance password    # 重新检查密码过期')
    lines.push('```\n')
    return lines.join('\n')
  }

  // 第一部分：服务器概览表
  lines.push('#### 服务器概览')
  lines.push('| 服务器名称 | IP地址 | 状态 | 概要 |')
  lines.push('|-----------|--------|------|------|')

  for (const r of results) {
    const server = getServer(r.server)
    const ip = server ? server.host : '-'
    lines.push(`| ${r.server} | ${ip} | ${r.status} | ${r.details} |`)
  }

  lines.push('')

  // 第二部分：每台服务器的详细用户密码信息
  for (const r of results) {
    const server = getServer(r.server)
    const hostInfo = server ? `${server.host}:${server.port || 22}` : '-'

    lines.push(`#### 📊 ${r.server} (${hostInfo}) - ${r.status}`)

    if ((r as any).users && (r as any).users!.length > 0) {
      const users = (r as any).users!
      lines.push('| 用户 | 上次修改 | 过期日期 | 最大天数 | 剩余天数 | 状态 |')
      lines.push('|------|----------|----------|----------|----------|------|')

      for (const u of users) {
        const daysLeftStr = u.daysLeft !== undefined ?
          (u.daysLeft < 0 ? `已过期${Math.abs(u.daysLeft)}天` : `${u.daysLeft}天`) : '-'
        lines.push(`| ${u.user} | ${u.lastChanged} | ${u.expires} | ${u.maxDays} | ${daysLeftStr} | ${u.status} |`)
      }
      lines.push('')
    } else if (r.status.includes('❌ 检查失败')) {
      lines.push(`**连接失败**: ${r.details}\n`)
    } else {
      lines.push(`未找到需要检查的本地用户\n`)
    }
  }

  // 第三部分：优化建议表
  const hasIssue = results.some(r =>
    r.status.includes('❌ 有密码已过期') ||
    r.status.includes('⚠️ 有即将过期') ||
    r.status.includes('⚠️ 永不过期')
  )

  const allFailed = results.every(r => r.status.includes('❌ 检查失败'))

  if (allFailed) {
    lines.push('### 💡 优化建议\n')
    lines.push('| 服务器 | 严重等级 | 建议 | 操作步骤 |')
    lines.push('|--------|----------|------|----------|')
    lines.push('| 所有服务器 | 🔴 高 | 所有服务器连接失败，无法检查密码过期 | 1. 检查网络连通性<br>2. 验证 SSH 配置<br>3. 确认用户名/密码/密钥 |')
    lines.push('')
  } else if (!hasIssue) {
    lines.push('### 💡 优化建议\n')
    lines.push('| 服务器 | 严重等级 | 状态 | 说明 |')
    lines.push('|--------|----------|------|------|')
    lines.push('| 所有服务器 | 🟢 低 | 正常 | 所有可达服务器密码状态正常，建议定期巡检 |')
    lines.push('')
  } else {
    lines.push('### 💡 优化建议\n')
    lines.push('| 服务器 | 用户 | 严重等级 | 建议 | 操作步骤 |')
    lines.push('|--------|------|----------|------|----------|')

    for (const r of results) {
      if ((r as any).users) {
        for (const u of (r as any).users!) {
          if (u.status === '❌ 已过期') {
            lines.push(`| ${r.server} | ${u.user} | 🔴 高 | 密码已过期 | 1. 立即修改密码<br>2. 检查密码策略<br>3. 更新相关应用配置<br>`)
          } else if (u.status === '⚠️ 即将过期') {
            lines.push(`| ${r.server} | ${u.user} | 🟡 中 | 密码即将过期(${u.daysLeft}天) | 1. 计划修改密码<br>2. 通知相关人员<br>`)
          }
        }
      }
    }
    lines.push('')
  }

  return lines.join('\n') || '未找到密码过期信息'
}


/**
 * 远程服务器健康检查
 */
export async function checkRemoteHealth(
  config: SSHConfig,
  services: string[] = ['nginx', 'docker', 'postgresql', 'redis-server']
): Promise<string> {
  const results: string[] = []
  results.push(`### 🩺 远程服务器健康检查 (${config.host})\n`)
  
  // 系统信息
  results.push('**系统:**')  
  results.push('```\n' + await runRemoteCommand(config, 'uptime && free -h && df -h') + '```\n')
  
  // 服务状态
  results.push('**服务状态:**')
  for (const svc of services) {
    const status = await runRemoteCommand(config, `systemctl is-active ${svc} 2>/dev/null || pgrep -f "${svc}" >/dev/null && echo "running" || echo "stopped"`)
    const emoji = status.trim() === 'active' || status.trim() === 'running' ? '✅' : '❌'
    results.push(`- ${svc}: ${emoji} ${status.trim()}`)
  }
  
  return results.join('\n')
}

/**
 * 远程服务器端口检查
 */
export async function checkRemotePort(config: SSHConfig, port?: number): Promise<string> {
  if (port) {
    return `### 🔌 端口 ${port} (${config.host})\n\`\n\`\n${await runRemoteCommand(config, `lsof -i :${port} 2>/dev/null || netstat -tlnp | grep :${port}`)}\n\`\`\``
  }
  
  return `### 🔌 监听端口 (${config.host})\n\`\n\`\n${await runRemoteCommand(config, 'lsof -i -P | grep LISTEN | head -20')}\n\`\`\``
}

/**
 * 远程服务器进程检查
 */
export async function checkRemoteProcess(config: SSHConfig, name?: string): Promise<string> {
  if (name) {
    const output = await runRemoteCommand(config, `ps aux | grep -i "${name}" | grep -v grep | head -10`)
    return `### ⚙️ 进程 "${name}" (${config.host})\n\`\n\`\n${output}\n\`\`\``
  }
  
  return `### ⚙️ Top 进程 (${config.host})\n\`\n\`\n${await runRemoteCommand(config, 'ps aux --sort=-%cpu | head -15')}\n\`\`\``
}

/**
 * 远程服务器磁盘检查
 */
export async function checkRemoteDisk(config: SSHConfig): Promise<string> {
  const results: string[] = []
  results.push(`### 💾 磁盘使用 (${config.host})\n`)

  results.push('**分区:**')
  results.push('\`\n\`' + await runRemoteCommand(config, 'df -h') + '\`\n\`')

  results.push('**大目录:**')
  results.push('\`\n\`' + await runRemoteCommand(config, 'du -sh /* 2>/dev/null | sort -hr | head -10') + '\`\n\`')

  return results.join('\n')
}

/**
 * 远程服务器性能检查 (Linux)
 */
export async function checkRemotePerformance(config: SSHConfig): Promise<string> {
  const results: string[] = []
  results.push(`### 📊 远程服务器性能 (${config.host})\n`)

  // CPU 信息
  results.push('**CPU 信息:**')
  results.push('```\n' + await runRemoteCommand(config, 'lscpu 2>/dev/null | head -20 || cat /proc/cpuinfo | head -20') + '```\n')

  // 内存状态
  results.push('**内存状态:**')
  results.push('```\n' + await runRemoteCommand(config, 'free -h') + '```\n')

  // 系统负载
  results.push('**系统负载:**')
  results.push('```\n' + await runRemoteCommand(config, 'uptime') + '```\n')

  // 磁盘 I/O (尝试 iostat 或 vmstat)
  results.push('**磁盘 I/O:**')
  const iostat = await runRemoteCommand(config, 'iostat -dx 1 1 2>/dev/null | head -20 || echo "iostat 未安装"')
  results.push('```\n' + iostat + '```\n')

  // 网络连接数
  results.push('**网络连接:**')
  const connections = await runRemoteCommand(config, 'ss -tan | wc -l 2>/dev/null || netstat -tan | wc -l')
  results.push(`当前 TCP 连接数: \`${connections.trim() || 'N/A'}\``)

  return results.join('\n')
}

/**
 * 远程服务器日志检查
 */
export async function checkRemoteLogs(
  config: SSHConfig, 
  pattern: string = 'error',
  lines: number = 30
): Promise<string> {
  const results: string[] = []
  results.push(`### 📋 远程日志 (${config.host}, 搜索: "${pattern}")\n`)
  
  // 常见日志路径
  const logPaths = [
    '/var/log/syslog',
    '/var/log/nginx/error.log',
    '/var/log/apache2/error.log',
    '~/.npm/_logs/*.log'
  ]
  
  for (const logPath of logPaths) {
    const output = await runRemoteCommand(config, `grep -i "${pattern}" ${logPath} 2>/dev/null | tail -${lines}`)
    if (output && !output.includes('失败')) {
      results.push(`**${logPath}:**`)
      results.push('\`\n\`' + output + '\`\n\`')
    }
  }
  
  return results.join('\n') || '未找到匹配的日志'
}

/**
 * 运维操作类型定义
 */
export type OpsAction = 'health' | 'logs' | 'perf' | 'ports' | 'process' | 'disk' | 'password' | 'passwd' | 'expire' | 'network' | 'report' | 'audit' | 'docker' | 'ssl' | 'security' | 'cluster'

/**
 * 运维操作执行入口
 */
export async function executeOp(action: string, arg?: string): Promise<string> {
  switch (action.toLowerCase()) {
    case 'health':
    case 'check':
      return checkHealth()
    case 'logs':
    case 'log':
      return analyzeLogs(arg || 'error')
    case 'perf':
    case 'performance':
      return checkPerformance()
    case 'ports':
    case 'port':
      return checkPort(arg ? parseInt(arg) : undefined)
    case 'process':
    case 'proc':
      return checkProcess(arg)
    case 'disk':
    case 'space':
      return checkDisk()
    case 'password':
    case 'passwd':
    case 'expire':
      return checkAllServersPasswordExpirationReport()
    case 'network':
      return networkPing(arg || 'localhost')
    case 'report':
      return getClusterSummary()
    case 'audit':
      return getAuditStats()
    case 'docker':
      return dockerHealthCheck()
    case 'ssl':
      return sslCheck(['localhost'])
    case 'security':
      return '安全审计功能可通过 CLI 命令 ops security 使用'
    case 'cluster':
      return getClusterSummary()
    default:
      return `未知操作: ${action}\n\n可用操作: health, logs, perf, ports, process, disk, password, network, report, audit, docker, ssl, security, cluster`
  }
}

/**
 * 远程运维操作
 */
export async function executeRemoteOp(
  action: string,
  config: SSHConfig,
  arg?: string
): Promise<string> {
  switch (action.toLowerCase()) {
    case 'health':
    case 'check':
      return checkRemoteHealth(config)
    case 'logs':
    case 'log':
      return checkRemoteLogs(config, arg || 'error')
    case 'perf':
    case 'performance':
      return checkRemotePerformance(config)
    case 'ports':
    case 'port':
      return checkRemotePort(config, arg ? parseInt(arg) : undefined)
    case 'process':
    case 'proc':
      return checkRemoteProcess(config, arg)
    case 'disk':
      return checkRemoteDisk(config)
    case 'password':
    case 'passwd':
    case 'expire':
      return checkRemotePasswordExpiration(config)
    default:
      return `未知操作: ${action}`
  }
}

/**
 * 远程服务器密码过期检查
 */
export async function checkRemotePasswordExpiration(config: SSHConfig): Promise<string> {
  const results: string[] = []
  results.push(`### 🔐 远程密码过期检查 (${config.host})\n`)

  try {
    const usersOutput = await runRemoteCommand(config, 'cat /etc/shadow 2>/dev/null | cut -d: -f1 | grep -v "^[$!*]$" | head -20')
    const users = usersOutput.trim().split('\n').filter(u => u.trim())

    if (users.length === 0) {
      results.push('未找到可检查的用户\n')
    } else {
      results.push('| 用户 | 上次修改 | 过期日期 | 最大天数 | 状态 |')
      results.push('|------|----------|----------|----------|------|')

      for (const user of users) {
        const u = user.trim()
        if (!u) continue
        try {
          const chageOutput = await runRemoteCommand(config, `chage -l "${u}" 2>/dev/null`)
          const lastChanged = chageOutput.match(/Last password change\s*:\s*(.+)/)?.[1]?.trim() || '-'
          const expires = chageOutput.match(/Password expires\s*:\s*(.+)/)?.[1]?.trim() || '-'
          const maxDays = chageOutput.match(/Maximum number of days between password change\s*:\s*(.+)/)?.[1]?.trim() || '-'

          let status = '✅ 有效'
          if (expires === 'never') {
            status = '⚠️ 永不过期'
          } else if (expires !== '-') {
            try {
              const expDate = new Date(expires)
              const now = new Date()
              const daysLeft = Math.ceil((expDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24))
              if (daysLeft < 0) status = '❌ 已过期'
              else if (daysLeft <= 7) status = '⚠️ 即将过期'
            } catch {}
          }

          results.push(`| ${u} | ${lastChanged} | ${expires} | ${maxDays} | ${status} |`)
        } catch {
          results.push(`| ${u} | - | - | - | ❌ 检查失败 |`)
        }
      }
    }
  } catch (error: any) {
    results.push(`❌ 连接失败: ${error.message}`)
  }

  return results.join('\n')
}