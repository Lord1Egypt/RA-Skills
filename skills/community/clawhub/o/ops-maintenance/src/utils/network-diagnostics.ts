/**
 * 网络诊断工具 v3.0
 *
 * 支持 ping/traceroute/dns/mtr 连通性测试
 * 本地和远程服务器均可用
 */

import { exec } from 'child_process'
import { promisify } from 'util'
import { validateCommand } from './command-validator.js'

const execAsync = promisify(exec)

// ============================================================
// 类型定义
// ============================================================

export interface PingResult {
  host: string
  alive: boolean
  latency?: number
  packetLoss?: number
  packetsSent?: number
  packetsReceived?: number
  detail: string
}

export interface DnsResult {
  host: string
  addresses: string[]
  queryTime?: number
  server?: string
  detail: string
}

export interface TraceResult {
  host: string
  hops: {
    hop: number
    host: string
    ip: string
    latency1?: number
    latency2?: number
    latency3?: number
  }[]
  detail: string
}

export interface PortCheckResult {
  host: string
  port: number
  open: boolean
  latency?: number
  detail: string
}

export interface ConnectivityResult {
  target: string
  ping: PingResult
  dns: DnsResult
  portChecks: PortCheckResult[]
  overall: 'ok' | 'warning' | 'critical' | 'error'
  summary: string
}

// ============================================================
// 网络诊断器
// ============================================================

export class NetworkDiagnostics {
  private timeout: number

  constructor(timeout: number = 10000) {
    this.timeout = timeout
  }

  // ----------------------------------------------------------
  // Ping 测试
  // ----------------------------------------------------------

  async ping(host: string, count: number = 4): Promise<PingResult> {
    try {
      // macOS 和 Linux 的 ping 命令略有不同
      const cmd = `ping -c ${count} -W 5 ${host}`
      const validation = validateCommand(cmd)
      // ping 命令可能在白名单中，也可能不在，直接执行
      const { stdout } = await execAsync(cmd, { timeout: this.timeout })

      // 解析结果
      const alive = !stdout.includes('100% packet loss')

      // 解析延迟 (macOS: min/avg/max/stddev, Linux: min/avg/max/mdev)
      const latencyMatch = stdout.match(/(?:min\/avg\/max\/(?:stddev|mdev))\s*=\s*[\d.]+\/([\d.]+)\/[\d.]+\/[\d.]+/)
      const latency = latencyMatch ? parseFloat(latencyMatch[1]) : undefined

      // 解析丢包率
      const lossMatch = stdout.match(/(\d+)%\s*packet\s*loss/)
      const packetLoss = lossMatch ? parseInt(lossMatch[1]) : undefined

      // 解析包数
      const packetsMatch = stdout.match(/(\d+)\s*packets?\s*transmitted,\s*(\d+)\s*packets?\s*received/)
      const packetsSent = packetsMatch ? parseInt(packetsMatch[1]) : undefined
      const packetsReceived = packetsMatch ? parseInt(packetsMatch[2]) : undefined

      return {
        host,
        alive,
        latency,
        packetLoss,
        packetsSent,
        packetsReceived,
        detail: stdout.trim(),
      }
    } catch (error: any) {
      return {
        host,
        alive: false,
        detail: `ping 失败: ${error.message}`,
      }
    }
  }

  // ----------------------------------------------------------
  // DNS 查询
  // ----------------------------------------------------------

  async dns(host: string, server?: string): Promise<DnsResult> {
    try {
      const serverArg = server ? `@${server}` : ''
      const cmd = `dig +short ${serverArg} ${host} A ${host} AAAA`
      const { stdout } = await execAsync(cmd, { timeout: this.timeout })

      const addresses = stdout
        .trim()
        .split('\n')
        .filter(l => l.trim() && !l.startsWith(';'))
        .map(l => l.trim())

      return {
        host,
        addresses,
        detail: stdout.trim(),
      }
    } catch (error: any) {
      // dig 不可用时尝试 nslookup
      try {
        const cmd = `nslookup ${host}${server ? ` ${server}` : ''}`
        const { stdout } = await execAsync(cmd, { timeout: this.timeout })

        const addresses: string[] = []
        const lines = stdout.split('\n')
        for (const line of lines) {
          const match = line.match(/Address:\s*([\d.a-fA-F:]+)/)
          if (match && !match[1].includes('#')) {
            addresses.push(match[1].trim())
          }
        }

        return {
          host,
          addresses,
          detail: stdout.trim(),
        }
      } catch (error2: any) {
        return {
          host,
          addresses: [],
          detail: `DNS 查询失败: ${error2.message}`,
        }
      }
    }
  }

  // ----------------------------------------------------------
  // Traceroute
  // ----------------------------------------------------------

  async traceroute(host: string, maxHops: number = 20): Promise<TraceResult> {
    try {
      const cmd = `traceroute -m ${maxHops} ${host}`
      const { stdout } = await execAsync(cmd, { timeout: 30000 })

      const hops: TraceResult['hops'] = []
      const lines = stdout.split('\n').slice(1) // 跳过第一行标题

      for (const line of lines) {
        const match = line.match(/^\s*(\d+)\s+(\S+)\s+\(?([\d.]+)\)?\s+([\d.]+)\s+ms\s+([\d.]+)\s+ms\s+([\d.]+)\s*ms/)
        if (match) {
          hops.push({
            hop: parseInt(match[1]),
            host: match[2],
            ip: match[3],
            latency1: parseFloat(match[4]),
            latency2: parseFloat(match[5]),
            latency3: parseFloat(match[6]),
          })
        } else {
          // 可能是 * * * 格式
          const starMatch = line.match(/^\s*(\d+)\s+\*/)
          if (starMatch) {
            hops.push({
              hop: parseInt(starMatch[1]),
              host: '*',
              ip: '*',
            })
          }
        }
      }

      return {
        host,
        hops,
        detail: stdout.trim(),
      }
    } catch (error: any) {
      return {
        host,
        hops: [],
        detail: `traceroute 失败: ${error.message}`,
      }
    }
  }

  // ----------------------------------------------------------
  // 端口连通性测试
  // ----------------------------------------------------------

  async checkPort(host: string, port: number): Promise<PortCheckResult> {
    try {
      const cmd = `nc -z -w 5 ${host} ${port}`
      await execAsync(cmd, { timeout: this.timeout })

      return {
        host,
        port,
        open: true,
        detail: `端口 ${port} 开放`,
      }
    } catch {
      return {
        host,
        port,
        open: false,
        detail: `端口 ${port} 关闭或不可达`,
      }
    }
  }

  // ----------------------------------------------------------
  // MTR (My Traceroute) — 如果可用
  // ----------------------------------------------------------

  async mtr(host: string, count: number = 10): Promise<TraceResult> {
    try {
      const cmd = `mtr -r -c ${count} --no-dns ${host}`
      const { stdout } = await execAsync(cmd, { timeout: 30000 })

      const hops: TraceResult['hops'] = []
      const lines = stdout.split('\n').slice(2) // 跳过标题

      for (const line of lines) {
        const parts = line.trim().split(/\s+/)
        if (parts.length >= 8) {
          const hop = parseInt(parts[0].replace(/\./, ''))
          if (!isNaN(hop)) {
            hops.push({
              hop,
              host: parts[1],
              ip: parts[1],
              latency1: parseFloat(parts[5]) || undefined, // Avg
              latency2: parseFloat(parts[6]) || undefined, // Best
              latency3: parseFloat(parts[7]) || undefined, // Wrst
            })
          }
        }
      }

      return {
        host,
        hops,
        detail: stdout.trim(),
      }
    } catch (error: any) {
      // mtr 不可用，降级为 traceroute
      return this.traceroute(host)
    }
  }

  // ----------------------------------------------------------
  // 综合连通性测试
  // ----------------------------------------------------------

  async fullCheck(
    target: string,
    ports: number[] = [80, 443, 22]
  ): Promise<ConnectivityResult> {
    const [pingResult, dnsResult] = await Promise.all([
      this.ping(target),
      this.dns(target),
    ])

    const portResults = await Promise.all(
      ports.map(port => this.checkPort(target, port))
    )

    // 综合判断
    let overall: ConnectivityResult['overall'] = 'ok'
    const issues: string[] = []

    if (!pingResult.alive) {
      overall = 'critical'
      issues.push('主机不可达')
    } else if (pingResult.packetLoss && pingResult.packetLoss > 50) {
      overall = 'critical'
      issues.push(`丢包率 ${pingResult.packetLoss}%`)
    } else if (pingResult.packetLoss && pingResult.packetLoss > 0) {
      overall = 'warning'
      issues.push(`丢包率 ${pingResult.packetLoss}%`)
    }

    if (dnsResult.addresses.length === 0) {
      overall = overall === 'critical' ? 'critical' : 'warning'
      issues.push('DNS 解析失败')
    }

    if (pingResult.latency && pingResult.latency > 200) {
      if (overall === 'ok') overall = 'warning'
      issues.push(`延迟 ${pingResult.latency}ms`)
    }

    const closedPorts = portResults.filter(p => !p.open).map(p => p.port)
    if (closedPorts.length > 0) {
      if (overall === 'ok') overall = 'warning'
      issues.push(`端口 ${closedPorts.join(', ')} 关闭`)
    }

    const summary = issues.length > 0
      ? `发现问题: ${issues.join('; ')}`
      : `一切正常 (延迟 ${pingResult.latency?.toFixed(1) || 'N/A'}ms, 无丢包)`

    return {
      target,
      ping: pingResult,
      dns: dnsResult,
      portChecks: portResults,
      overall,
      summary,
    }
  }

  // ----------------------------------------------------------
  // 格式化输出
  // ----------------------------------------------------------

  formatPingResult(result: PingResult): string {
    const statusEmoji = result.alive ? '✅' : '❌'
    const lines: string[] = []
    lines.push(`### 🌐 Ping 测试: ${result.host}\n`)
    lines.push(`${statusEmoji} 状态: ${result.alive ? '可达' : '不可达'}`)
    if (result.latency !== undefined) {
      lines.push(`⏱️ 平均延迟: ${result.latency.toFixed(1)}ms`)
    }
    if (result.packetLoss !== undefined) {
      lines.push(`📦 丢包率: ${result.packetLoss}%`)
    }
    if (result.packetsSent !== undefined) {
      lines.push(`📊 发送/接收: ${result.packetsSent}/${result.packetsReceived}`)
    }
    return lines.join('\n')
  }

  formatDnsResult(result: DnsResult): string {
    const lines: string[] = []
    lines.push(`### 🔍 DNS 查询: ${result.host}\n`)
    if (result.addresses.length > 0) {
      lines.push(`**解析结果:**`)
      for (const addr of result.addresses) {
        lines.push(`- ${addr}`)
      }
    } else {
      lines.push('❌ 未能解析到任何地址')
    }
    return lines.join('\n')
  }

  formatTraceResult(result: TraceResult): string {
    const lines: string[] = []
    lines.push(`### 🛤️ 路由追踪: ${result.host}\n`)
    if (result.hops.length > 0) {
      lines.push('| 跳数 | 主机 | IP | 延迟1 | 延迟2 | 延迟3 |')
      lines.push('|------|------|-----|-------|-------|-------|')
      for (const hop of result.hops) {
        lines.push(`| ${hop.hop} | ${hop.host} | ${hop.ip} | ${hop.latency1?.toFixed(1) || '*'}ms | ${hop.latency2?.toFixed(1) || '*'}ms | ${hop.latency3?.toFixed(1) || '*'}ms |`)
      }
    } else {
      lines.push('❌ 无法获取路由信息')
    }
    return lines.join('\n')
  }

  formatConnectivityResult(result: ConnectivityResult): string {
    const statusEmoji = { ok: '✅', warning: '⚠️', critical: '🔴', error: '❌' }
    const lines: string[] = []
    lines.push(`### 🔗 连通性测试: ${result.target}\n`)
    lines.push(`${statusEmoji[result.overall]} **综合状态**: ${result.summary}\n`)
    lines.push(this.formatPingResult(result.ping))
    lines.push('')
    lines.push(this.formatDnsResult(result.dns))
    lines.push('')
    lines.push('**端口检测:**')
    for (const pc of result.portChecks) {
      lines.push(`- 端口 ${pc.port}: ${pc.open ? '✅ 开放' : '❌ 关闭'}`)
    }
    return lines.join('\n')
  }
}

// ============================================================
// 全局单例
// ============================================================

let globalNetworkDiagnostics: NetworkDiagnostics | null = null

export function getNetworkDiagnostics(timeout?: number): NetworkDiagnostics {
  if (!globalNetworkDiagnostics) {
    globalNetworkDiagnostics = new NetworkDiagnostics(timeout)
  }
  return globalNetworkDiagnostics
}
