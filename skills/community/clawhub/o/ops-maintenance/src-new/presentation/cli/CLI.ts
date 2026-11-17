/**
 * CLI 入口模块
 * 协调所有组件完成命令执行
 */

import type {
  Server,
  ISSHClient,
  IServerRepository,
  ClusterHealthReport,
  PasswordCheckResult,
  DiskInfo,
  OpsAction
} from '../../config/schemas'
import { type EmailConfig, INotifier } from '../../config/schemas'
import { CommandParser, ParsedCommand } from './CommandDispatcher'
import { MarkdownFormatter } from '../formatters/MarkdownFormatter'
import { JsonFormatter } from '../formatters/JsonFormatter'
import { HealthCheckUseCase } from '../../core/usecases/HealthCheckUseCase'
import { PasswordCheckUseCase } from '../../core/usecases/PasswordCheckUseCase'
import { DiskCheckUseCase } from '../../core/usecases/DiskCheckUseCase'
import { ThresholdChecker, DEFAULT_THRESHOLDS } from '../../infrastructure/monitoring/ThresholdChecker'
import { HealthChecker } from '../../infrastructure/monitoring/HealthChecker'
import { MemoryCache } from '../../infrastructure/cache/CacheRepository'
import type { ICacheRepository } from '../../config/schemas'
import { Logger } from '../../utils/logger'

/**
 * CLI 应用主类
 */
export class CLI {
  private parser: CommandParser
  private markdownFormatter: MarkdownFormatter
  private jsonFormatter: JsonFormatter
  private logger: Logger

  // 依赖项（需要外部注入）
  private serverRepo?: IServerRepository
  private sshClient?: ISSHClient
  private cache?: ICacheRepository
  private emailConfig?: Partial<EmailConfig>

  constructor() {
    this.parser = new CommandParser()
    this.markdownFormatter = new MarkdownFormatter()
    this.jsonFormatter = new JsonFormatter()
    this.logger = Logger.getLogger('CLI')
  }

  /**
   * 注入依赖
   */
  setDependencies(
    serverRepo: IServerRepository,
    ssh: ISSHClient,
    cache: ICacheRepository,
    emailConfig?: Partial<EmailConfig>
  ): void {
    this.serverRepo = serverRepo
    this.sshClient = ssh
    this.cache = cache
    this.emailConfig = emailConfig
  }

  /**
   * 执行命令
   */
  async execute(args: string[]): Promise<string> {
    try {
      // 解析命令
      const command = this.parser.parse(args)
      this.logger.debug('执行命令:', command)

      // 检查依赖
      if (!this.serverRepo || !this.sshClient || !this.cache) {
        throw new Error('依赖未注入，请先调用 setDependencies()')
      }

      // 根据动作执行
      const result = await this.dispatch(command)

      // 格式化输出
      const formatter = command.format === 'json' ? this.jsonFormatter : this.markdownFormatter
      const output = this.formatOutput(result, formatter, command.action)

      return output
    } catch (error: any) {
      this.logger.error('命令执行失败:', error)
      return this.formatError(error)
    }
  }

  /**
   * 分派命令到对应的用例
   */
  private async dispatch(command: ParsedCommand): Promise<any> {
    switch (command.action) {
      case 'health':
      case 'check':
      case 'cluster':
        return this.executeHealthCheck(command)

      case 'email-config':
        return this.executeEmailConfig(command)

      case 'password':
      case 'passwd':
      case 'expire':
        return this.executePasswordCheck(command)

      case 'disk':
      case 'space':
        return this.executeDiskCheck(command)

      case 'logs':
      case 'log':
        return this.executeLogAnalysis(command)

      case 'perf':
      case 'performance':
        return this.executePerformanceCheck(command)

      case 'ports':
      case 'port':
        return this.executePortCheck(command)

      case 'process':
      case 'proc':
        return this.executeProcessCheck(command)

      default:
        throw new Error(`未实现的操作: ${command.action}`)
    }
  }

  /**
   * 执行健康检查
   */
  private async executeHealthCheck(command: ParsedCommand): Promise<ClusterHealthReport> {
    // 初始化 UseCase
    const thresholdChecker = new ThresholdChecker(DEFAULT_THRESHOLDS)
    const healthChecker = new HealthChecker()

    const useCase = new HealthCheckUseCase(
      this.serverRepo!,
      this.sshClient!,
      this.cache!,
      healthChecker,
      thresholdChecker
    )

    const input = {
      tags: command.tags,
      force: false
    }

    return await useCase.execute(input)
  }

  /**
   * 执行密码检查
   */
  private async executePasswordCheck(command: ParsedCommand): Promise<PasswordCheckResult[]> {
    const useCase = new PasswordCheckUseCase(
      this.serverRepo!,
      this.sshClient!
    )

    return await useCase.execute(command.tags)
  }

  /**
   * 执行磁盘检查
   */
  private async executeDiskCheck(command: ParsedCommand): Promise<DiskInfo[]> {
    const useCase = new DiskCheckUseCase(
      this.serverRepo!,
      this.sshClient!
    )

    return await useCase.execute(command.tags)
  }

  /**
   * 执行日志分析（占位）
   */
  private async executeLogAnalysis(command: ParsedCommand): Promise<string> {
    // TODO: 实现日志分析 UseCase
    return '日志分析功能尚未实现'
  }

  /**
   * 执行性能检查（占位）
   */
  private async executePerformanceCheck(command: ParsedCommand): Promise<string> {
    // TODO: 实现性能检查 UseCase
    return '性能检查功能尚未实现'
  }

  /**
   * 执行端口检查（占位）
   */
  private async executePortCheck(command: ParsedCommand): Promise<string> {
    // TODO: 实现端口检查 UseCase
    const port = command.arg
    return `端口检查 ${port ? '端口 ' + port : '所有端口'} 功能尚未完全实现`
  }

  /**
   * 执行进程检查（占位）
   */
  private async executeProcessCheck(command: ParsedCommand): Promise<string> {
    // TODO: 实现进程检查 UseCase
    const name = command.arg || '所有进程'
    return `进程检查 ${name} 功能尚未完全实现`
  }

  /**
   * 格式化输出
   */
  private formatOutput(result: any, formatter: any, action: string): string {
    if (action === 'password' || action === 'passwd') {
      return formatter.formatPasswordReport(result)
    } else if (action === 'disk') {
      // 磁盘检查使用 JSON 格式化或简单文本
      if (formatter instanceof JsonFormatter) {
        return formatter.formatDiskReport(result)
      } else {
        return this.formatDiskMarkdown(result)
      }
    } else {
      // 集群健康报告
      return formatter.formatClusterReport(result)
    }
  }

  /**
   * 格式化磁盘检查的 Markdown
   */
  private formatDiskMarkdown(disks: DiskInfo[]): string {
    const lines: string[] = []
    lines.push('### 💾 磁盘使用检查\n')

    lines.push('| 服务器 | 挂载点 | 总容量 | 已用 | 可用 | 使用率 |')
    lines.push('|--------|--------|--------|------|------|--------|')

    for (const disk of disks) {
      const total = this.formatBytes(disk.total)
      const used = this.formatBytes(disk.used)
      const avail = this.formatBytes(disk.available)
      lines.push(`| ${disk.server} | ${disk.mountPoint} | ${total} | ${used} | ${avail} | ${disk.usagePercent}% |`)
    }

    lines.push('')
    return lines.join('\n')
  }

  /**
   * 格式化错误
   */
  private formatError(error: Error): string {
    return `❌ **错误**: ${error.message}\n\n使用 \`/ops-maintenance help\` 查看帮助。`
  }

  /**
   * 格式化字节
   */
  private formatBytes(bytes: number): string {
    if (bytes >= 1073741824) {
      return `${(bytes / 1073741824).toFixed(1)}GB`
    } else if (bytes >= 1048576) {
      return `${(bytes / 1048576).toFixed(1)}MB`
    } else if (bytes >= 1024) {
      return `${(bytes / 1024).toFixed(1)}KB`
    }
    return `${bytes}B`
  }

  /**
   * 获取帮助信息
   */
  getHelp(): string {
    return this.parser.getHelp()
  }

  /**
   * 执行邮件配置测试
   */
  private async executeEmailConfig(command: ParsedCommand): Promise<string> {
    if (!this.emailConfig?.user || !this.emailConfig?.password) {
      return '❌ 邮件未配置，请使用以下格式设置:\n' +
        '  ops-maintenance email-config set --host SMTP_HOST --port PORT --user USER --password PASS --from FROM_ADDR --to EMAIL1 --to EMAIL2\n' +
        '  或使用环境变量: OPS_EMAIL_HOST, OPS_EMAIL_PORT, OPS_EMAIL_USER, OPS_EMAIL_PASSWORD, OPS_EMAIL_FROM, OPS_EMAIL_TO'
    }

    const { EmailNotifier } = await import('../../infrastructure/notifiers/EmailNotifier')
    const notifier = new EmailNotifier(this.emailConfig || {})

    try {
      await notifier.init()
      await notifier.notify('邮件配置测试', '这是一条测试邮件，来自 Ops Maintenance 邮件通知功能。', 'info')
      return '✅ 邮件配置正常，测试邮件已发送'
    } catch (error: any) {
      return `❌ 邮件发送失败: ${error.message}`
    }
  }
}