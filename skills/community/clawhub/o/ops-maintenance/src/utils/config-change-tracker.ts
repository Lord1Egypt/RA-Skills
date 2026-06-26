/**
 * 配置变更追踪器 v3.0
 *
 * 监控关键配置文件的变更，检测非预期修改
 * 支持本地和远程服务器
 */

import { exec } from 'child_process'
import { promisify } from 'util'
import { existsSync, mkdirSync, readFileSync, writeFileSync, readdirSync, statSync } from 'fs'
import { join } from 'path'
import { createHash } from 'crypto'
import { getAuditLogger } from './audit-logger.js'

const execAsync = promisify(exec)

// ============================================================
// 类型定义
// ============================================================

export interface TrackedFile {
  path: string
  alias?: string
  /** 首次记录的hash */
  baselineHash?: string
  /** 当前hash */
  currentHash?: string
  /** 上次检查时间 */
  lastChecked?: string
  /** 是否有变更 */
  changed: boolean
  /** 变更详情 */
  diff?: string
}

export interface ConfigSnapshot {
  path: string
  hash: string
  content: string
  timestamp: string
  size: number
}

export interface ChangeRecord {
  path: string
  oldHash: string
  newHash: string
  timestamp: string
  diff: string
  diffStat: { added: number; removed: number; changed: number }
}

export interface ConfigTrackerConfig {
  /** 要追踪的文件列表 */
  files: TrackedFile[]
  /** 快照存储目录 */
  snapshotDir: string
  /** 最多保留多少个历史快照 */
  maxSnapshots: number
}

// ============================================================
// 默认配置
// ============================================================

export const DEFAULT_TRACKED_FILES: TrackedFile[] = [
  { path: '/etc/nginx/nginx.conf', alias: 'nginx主配置', changed: false },
  { path: '/etc/ssh/sshd_config', alias: 'SSH配置', changed: false },
  { path: '/etc/sysctl.conf', alias: '内核参数', changed: false },
  { path: '/etc/fstab', alias: '文件系统挂载', changed: false },
  { path: '/etc/hosts', alias: 'Hosts文件', changed: false },
  { path: '/etc/resolv.conf', alias: 'DNS配置', changed: false },
  { path: '/etc/crontab', alias: '系统定时任务', changed: false },
]

// ============================================================
// 配置变更追踪器
// ============================================================

export class ConfigChangeTracker {
  private configDir: string
  private snapshotDir: string
  private trackerFile: string
  private historyFile: string
  private trackedFiles: TrackedFile[]
  private changes: ChangeRecord[] = []
  private maxSnapshots: number

  constructor(config?: Partial<ConfigTrackerConfig>) {
    this.configDir = join(process.env.HOME || '~', '.config/ops-maintenance')
    this.snapshotDir = config?.snapshotDir || join(this.configDir, 'config-snapshots')
    this.trackerFile = join(this.configDir, 'config-tracker.json')
    this.historyFile = join(this.configDir, 'config-changes.json')
    this.maxSnapshots = config?.maxSnapshots || 10

    if (!existsSync(this.snapshotDir)) {
      mkdirSync(this.snapshotDir, { recursive: true })
    }

    this.trackedFiles = this.loadTrackedFiles()
    this.changes = this.loadChanges()
  }

  // ----------------------------------------------------------
  // 文件管理
  // ----------------------------------------------------------

  /** 获取追踪文件列表 */
  getTrackedFiles(): TrackedFile[] {
    return [...this.trackedFiles]
  }

  /** 添加追踪文件 */
  addFile(path: string, alias?: string): void {
    const normalized = this.normalizePath(path)
    if (!this.trackedFiles.some(f => f.path === normalized)) {
      this.trackedFiles.push({ path: normalized, alias, changed: false })
      this.saveTrackedFiles()
    }
  }

  /** 移除追踪文件 */
  removeFile(path: string): boolean {
    const normalized = this.normalizePath(path)
    const idx = this.trackedFiles.findIndex(f => f.path === normalized)
    if (idx >= 0) {
      this.trackedFiles.splice(idx, 1)
      this.saveTrackedFiles()
      return true
    }
    return false
  }

  // ----------------------------------------------------------
  // 快照管理
  // ----------------------------------------------------------

  /** 为所有追踪文件创建基线快照 */
  async createBaseline(): Promise<{ created: number; failed: number; details: string[] }> {
    let created = 0
    let failed = 0
    const details: string[] = []

    for (const file of this.trackedFiles) {
      try {
        const snapshot = await this.takeSnapshot(file.path)
        if (snapshot) {
          file.baselineHash = snapshot.hash
          file.currentHash = snapshot.hash
          file.changed = false
          file.lastChecked = new Date().toISOString()
          this.saveSnapshot(snapshot)
          created++
          details.push(`✅ ${file.alias || file.path}: 已建立基线`)
        } else {
          failed++
          details.push(`❌ ${file.path}: 文件不存在或无法读取`)
        }
      } catch (error: any) {
        failed++
        details.push(`❌ ${file.path}: ${error.message}`)
      }
    }

    this.saveTrackedFiles()
    return { created, failed, details }
  }

  /** 检查所有追踪文件的变更 */
  async checkChanges(): Promise<{ changed: number; unchanged: number; failed: number; changes: ChangeRecord[] }> {
    let changed = 0
    let unchanged = 0
    let failed = 0
    const newChanges: ChangeRecord[] = []
    const audit = getAuditLogger()

    for (const file of this.trackedFiles) {
      try {
        const snapshot = await this.takeSnapshot(file.path)
        if (!snapshot) {
          failed++
          continue
        }

        if (!file.baselineHash) {
          // 首次检查，建立基线
          file.baselineHash = snapshot.hash
          file.currentHash = snapshot.hash
          file.changed = false
          unchanged++
        } else if (file.currentHash !== snapshot.hash) {
          // 检测到变更
          const oldSnapshot = this.loadLatestSnapshot(file.path)
          const diff = oldSnapshot ? this.computeDiff(oldSnapshot.content, snapshot.content) : '(无旧快照)'

          const oldHash = file.currentHash || ''
          const changeRecord: ChangeRecord = {
            path: file.path,
            oldHash,
            newHash: snapshot.hash,
            timestamp: new Date().toISOString(),
            diff: diff.substring(0, 5000),
            diffStat: this.parseDiffStat(diff),
          }

          newChanges.push(changeRecord)
          this.changes.push(changeRecord)

          file.currentHash = snapshot.hash
          file.changed = true
          changed++

          // 保存新快照
          this.saveSnapshot(snapshot)

          // 审计日志
          audit.logSuccess('config_change', file.path, undefined, undefined, {
            oldHash: file.currentHash,
            newHash: snapshot.hash,
            diffStat: changeRecord.diffStat,
          })
        } else {
          file.changed = false
          unchanged++
        }

        file.lastChecked = new Date().toISOString()
      } catch (error: any) {
        failed++
        audit.logFailure('config_check', file.path, error.message)
      }
    }

    this.saveTrackedFiles()
    this.saveChanges()
    this.cleanupOldSnapshots()

    return { changed, unchanged, failed, changes: newChanges }
  }

  /** 获取变更历史 */
  getChangeHistory(path?: string, limit: number = 20): ChangeRecord[] {
    let records = path
      ? this.changes.filter(c => c.path === this.normalizePath(path))
      : this.changes

    return records
      .sort((a, b) => b.timestamp.localeCompare(a.timestamp))
      .slice(0, limit)
  }

  // ----------------------------------------------------------
  // 内部方法
  // ----------------------------------------------------------

  private async takeSnapshot(filePath: string): Promise<ConfigSnapshot | null> {
    try {
      if (!existsSync(filePath)) return null

      const content = readFileSync(filePath, 'utf-8')
      const hash = createHash('sha256').update(content).digest('hex')
      const stat = statSync(filePath)

      return {
        path: filePath,
        hash,
        content,
        timestamp: new Date().toISOString(),
        size: stat.size,
      }
    } catch {
      return null
    }
  }

  private saveSnapshot(snapshot: ConfigSnapshot): void {
    const safeName = snapshot.path.replace(/\//g, '_')
    const dir = join(this.snapshotDir, safeName)
    if (!existsSync(dir)) mkdirSync(dir, { recursive: true })

    const filename = `snap-${Date.now()}.json`
    writeFileSync(join(dir, filename), JSON.stringify(snapshot, null, 2))
  }

  private loadLatestSnapshot(filePath: string): ConfigSnapshot | null {
    const safeName = filePath.replace(/\//g, '_')
    const dir = join(this.snapshotDir, safeName)
    if (!existsSync(dir)) return null

    const files = readdirSync(dir)
      .filter(f => f.startsWith('snap-') && f.endsWith('.json'))
      .sort()
      .reverse()

    if (files.length === 0) return null

    try {
      return JSON.parse(readFileSync(join(dir, files[0]), 'utf-8'))
    } catch {
      return null
    }
  }

  private cleanupOldSnapshots(): void {
    for (const file of this.trackedFiles) {
      const safeName = file.path.replace(/\//g, '_')
      const dir = join(this.snapshotDir, safeName)
      if (!existsSync(dir)) continue

      const files = readdirSync(dir)
        .filter(f => f.startsWith('snap-') && f.endsWith('.json'))
        .sort()
        .reverse()

      // 只保留最近 maxSnapshots 个
      const toDelete = files.slice(this.maxSnapshots)
      for (const f of toDelete) {
        try { require('fs').unlinkSync(join(dir, f)) } catch { /* skip */ }
      }
    }
  }

  private computeDiff(oldContent: string, newContent: string): string {
    const oldLines = oldContent.split('\n')
    const newLines = newContent.split('\n')
    const result: string[] = []

    // 简单的行级 diff
    const maxLen = Math.max(oldLines.length, newLines.length)
    for (let i = 0; i < maxLen; i++) {
      const oldLine = oldLines[i] || ''
      const newLine = newLines[i] || ''

      if (oldLine !== newLine) {
        if (i >= oldLines.length) {
          result.push(`+ ${newLine}`)
        } else if (i >= newLines.length) {
          result.push(`- ${oldLine}`)
        } else {
          result.push(`- ${oldLine}`)
          result.push(`+ ${newLine}`)
        }
      }
    }

    return result.join('\n')
  }

  private parseDiffStat(diff: string): { added: number; removed: number; changed: number } {
    const lines = diff.split('\n').filter(l => l.trim())
    return {
      added: lines.filter(l => l.startsWith('+ ')).length,
      removed: lines.filter(l => l.startsWith('- ')).length,
      changed: Math.min(
        lines.filter(l => l.startsWith('+ ')).length,
        lines.filter(l => l.startsWith('- ')).length
      ),
    }
  }

  private normalizePath(p: string): string {
    return p.replace(/\/+$/, '')
  }

  // 持久化
  private loadTrackedFiles(): TrackedFile[] {
    if (existsSync(this.trackerFile)) {
      try { return JSON.parse(readFileSync(this.trackerFile, 'utf-8')) } catch { /* skip */ }
    }
    return [...DEFAULT_TRACKED_FILES]
  }

  private saveTrackedFiles(): void {
    writeFileSync(this.trackerFile, JSON.stringify(this.trackedFiles, null, 2))
  }

  private loadChanges(): ChangeRecord[] {
    if (existsSync(this.historyFile)) {
      try { return JSON.parse(readFileSync(this.historyFile, 'utf-8')) } catch { /* skip */ }
    }
    return []
  }

  private saveChanges(): void {
    // 只保留最近1000条
    const recent = this.changes.slice(-1000)
    writeFileSync(this.historyFile, JSON.stringify(recent, null, 2))
  }

  // ----------------------------------------------------------
  // 格式化输出
  // ----------------------------------------------------------

  formatCheckResult(result: { changed: number; unchanged: number; failed: number; changes: ChangeRecord[] }): string {
    const lines: string[] = []
    lines.push('### 📝 配置变更检查结果\n')
    lines.push(`**变更**: ${result.changed} | **未变**: ${result.unchanged} | **失败**: ${result.failed}\n`)

    if (result.changes.length > 0) {
      lines.push('**🔴 检测到变更的文件**:')
      for (const change of result.changes) {
        lines.push(`\n#### ${change.path}`)
        lines.push(`- 时间: ${change.timestamp}`)
        lines.push(`- Hash: ${change.oldHash.substring(0, 8)}... -> ${change.newHash.substring(0, 8)}...`)
        lines.push(`- 统计: +${change.diffStat.added} -${change.diffStat.removed} ~${change.diffStat.changed}`)
        if (change.diff) {
          lines.push(`\`\`\`diff\n${change.diff.substring(0, 2000)}\n\`\`\``)
        }
      }
    } else if (result.changed === 0) {
      lines.push('✅ 所有追踪文件无变更')
    }

    return lines.join('\n')
  }

  formatTrackedFiles(): string {
    const lines: string[] = []
    lines.push('### 📋 追踪文件列表\n')

    for (const file of this.trackedFiles) {
      const statusEmoji = file.changed ? '🔴' : (file.baselineHash ? '✅' : '⬜')
      lines.push(`${statusEmoji} **${file.alias || file.path}**`)
      lines.push(`   路径: ${file.path}`)
      if (file.baselineHash) {
        lines.push(`   基线: ${file.baselineHash.substring(0, 12)}...`)
      }
      if (file.lastChecked) {
        lines.push(`   上次检查: ${file.lastChecked}`)
      }
      lines.push('')
    }

    return lines.join('\n')
  }

  formatChangeHistory(records: ChangeRecord[]): string {
    if (records.length === 0) return '暂无变更历史'

    const lines: string[] = []
    lines.push('### 📜 变更历史\n')

    for (const record of records) {
      lines.push(`**${record.path}** — ${record.timestamp}`)
      lines.push(`   +${record.diffStat.added} -${record.diffStat.removed} ~${record.diffStat.changed}`)
      lines.push('')
    }

    return lines.join('\n')
  }
}

// ============================================================
// 全局单例
// ============================================================

let globalConfigChangeTracker: ConfigChangeTracker | null = null

export function getConfigChangeTracker(): ConfigChangeTracker {
  if (!globalConfigChangeTracker) {
    globalConfigChangeTracker = new ConfigChangeTracker()
  }
  return globalConfigChangeTracker
}
