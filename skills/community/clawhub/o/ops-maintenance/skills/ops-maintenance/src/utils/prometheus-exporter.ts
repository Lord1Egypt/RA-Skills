/**
 * Prometheus 指标导出器
 *
 * 将系统健康指标导出为 Prometheus 格式，供 Prometheus/Grafana 使用
 */

import os from 'os'

export interface Metrics {
  [key: string]: number
}

export class PrometheusExporter {
  private port: number
  private hostname: string

  constructor(port: number = 9100) {
    this.port = port
    this.hostname = os.hostname()
  }

  /**
   * 收集系统指标并导出为 Prometheus 文本格式
   */
  async collectMetrics(): Promise<string> {
    const lines: string[] = []

    // 系统指标
    const loadAvg = os.loadavg()
    const totalMem = os.totalmem()
    const freeMem = os.freemem()
    const cpuCount = os.cpus().length
    const uptime = os.uptime()

    lines.push(`# HELP os_uptime_seconds System uptime in seconds`)
    lines.push(`# TYPE os_uptime_seconds gauge`)
    lines.push(`os_uptime_seconds{hostname="${this.hostname}"} ${uptime}`)

    lines.push(`# HELP os_cpu_count Number of CPU cores`)
    lines.push(`# TYPE os_cpu_count gauge`)
    lines.push(`os_cpu_count{hostname="${this.hostname}"} ${cpuCount}`)

    lines.push(`# HELP os_load_1m System load average 1m`)
    lines.push(`# TYPE os_load_1m gauge`)
    lines.push(`os_load_1m{hostname="${this.hostname}"} ${loadAvg[0]}`)

    lines.push(`# HELP os_load_5m System load average 5m`)
    lines.push(`# TYPE os_load_5m gauge`)
    lines.push(`os_load_5m{hostname="${this.hostname}"} ${loadAvg[1]}`)

    lines.push(`# HELP os_load_15m System load average 15m`)
    lines.push(`# TYPE os_load_15m gauge`)
    lines.push(`os_load_15m{hostname="${this.hostname}"} ${loadAvg[2]}`)

    lines.push(`# HELP os_memory_total_bytes Total memory in bytes`)
    lines.push(`# TYPE os_memory_total_bytes gauge`)
    lines.push(`os_memory_total_bytes{hostname="${this.hostname}"} ${totalMem}`)

    lines.push(`# HELP os_memory_free_bytes Free memory in bytes`)
    lines.push(`# TYPE os_memory_free_bytes gauge`)
    lines.push(`os_memory_free_bytes{hostname="${this.hostname}"} ${freeMem}`)

    lines.push(`# HELP os_memory_used_bytes Used memory in bytes`)
    lines.push(`# TYPE os_memory_used_bytes gauge`)
    lines.push(`os_memory_used_bytes{hostname="${this.hostname}"} ${totalMem - freeMem}`)

    lines.push(`# HELP os_memory_usage_ratio Memory usage ratio`)
    lines.push(`# TYPE os_memory_usage_ratio gauge`)
    lines.push(`os_memory_usage_ratio{hostname="${this.hostname}"} ${(totalMem - freeMem) / totalMem}`)

    return lines.join('\n') + '\n'
  }

  /**
   * 导出为 JSON 格式
   */
  async collectMetricsJSON(): Promise<object> {
    const metrics = await this.collectMetrics()
    const result: Record<string, number> = {}

    for (const line of metrics.split('\n')) {
      if (line.startsWith('#') || !line.trim()) continue
      const match = line.match(/^(\w+)\{hostname="[^"]*"\} ([\d.]+)$/)
      if (match) {
        result[match[1]] = parseFloat(match[2])
      }
    }

    return result
  }
}

let exporter: PrometheusExporter | null = null

export function getPrometheusExporter(port?: number): PrometheusExporter {
  if (!exporter) {
    exporter = new PrometheusExporter(port)
  }
  return exporter
}

export function resetPrometheusExporter(): void {
  exporter = null
}
