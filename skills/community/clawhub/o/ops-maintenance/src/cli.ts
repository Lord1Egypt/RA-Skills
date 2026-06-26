#!/usr/bin/env node
/**
 * ops-maintenance CLI v3.0
 *
 * 运维巡检一体化工具
 * 命令行入口
 */

import { Command } from 'commander'
import { getHealthChecker, formatHealthReport } from './utils/health-checker.js'
import { getSecurityAuditor } from './utils/security-auditor.js'
import { getAuditLogger } from './utils/audit-logger.js'
import { getSmartLogAnalyzer } from './utils/smart-log-analyzer.js'
import { getConfigChangeTracker } from './utils/config-change-tracker.js'
import { getReportGenerator } from './utils/report-generator.js'
import type { ReportFormat } from './utils/report-generator.js'

const program = new Command()

program
  .name('ops')
  .description('运维巡检一体化工具 v3.0')
  .version('3.0.0')

// ============================================================
// health 命令
// ============================================================

program
  .command('health')
  .description('系统健康检查')
  .option('-s, --service <name>', '检查指定服务')
  .option('-q, --quick', '快速检查(跳过耗时项)')
  .option('--json', 'JSON格式输出')
  .action(async (opts) => {
    try {
      const checker = getHealthChecker()
      if (opts.service) {
        const result = await checker.checkService(opts.service)
        console.log(JSON.stringify(result, null, 2))
      } else {
        const report = await checker.runAllChecks()
        if (opts.json) {
          console.log(JSON.stringify(report, null, 2))
        } else {
          console.log(formatHealthReport(report))
        }
      }
    } catch (error: any) {
      console.error(`❌ 健康检查失败: ${error.message}`)
      process.exit(1)
    }
  })

// ============================================================
// security 命令
// ============================================================

program
  .command('security')
  .description('安全审计')
  .option('-c, --category <cat>', '检查指定分类(ssh|firewall|permissions|docker|all)', 'all')
  .option('--fix', '尝试自动修复')
  .option('--json', 'JSON格式输出')
  .action(async (opts) => {
    try {
      const auditor = getSecurityAuditor()
      const findings = await auditor.runAllChecks()
      
      let filtered = findings
      if (opts.category !== 'all') {
        filtered = findings.filter(f => f.category === opts.category)
      }
      
      if (opts.json) {
        console.log(JSON.stringify(filtered, null, 2))
      } else {
        console.log(auditor.formatFindings(filtered))
      }

      if (opts.fix) {
        console.log('\n⚠️ 自动修复功能需要确认，当前仅展示修复建议')
        for (const f of filtered.filter(f => f.severity === 'high')) {
          console.log(`  - [${f.category}] ${f.title}: ${f.remediation}`)
        }
      }
    } catch (error: any) {
      console.error(`❌ 安全审计失败: ${error.message}`)
      process.exit(1)
    }
  })

// ============================================================
// audit 命令
// ============================================================

program
  .command('audit')
  .description('查看审计日志')
  .option('-l, --limit <n>', '显示条数', '20')
  .option('-a, --action <type>', '过滤操作类型')
  .option('--success', '只看成功')
  .option('--failed', '只看失败')
  .action(async (opts) => {
    try {
      const logger = getAuditLogger()
      const filters: any = { limit: parseInt(opts.limit) }
      if (opts.action) filters.action = opts.action
      if (opts.success) filters.status = 'success'
      if (opts.failed) filters.status = 'failure'

      const logs = logger.query(filters)
      console.log(logger.formatLogs(logs))
    } catch (error: any) {
      console.error(`❌ 查询审计日志失败: ${error.message}`)
      process.exit(1)
    }
  })

// ============================================================
// logs 命令
// ============================================================

program
  .command('logs')
  .description('智能日志分析')
  .option('-p, --pattern <regex>', '搜索模式', 'error|warn|critical|fail')
  .option('-h, --hours <n>', '分析最近N小时', '1')
  .option('-f, --files <paths>', '日志文件路径(逗号分隔)')
  .option('--discover', '自动发现日志文件')
  .option('--trends', '只看趋势')
  .option('--anomalies', '只看异常')
  .action(async (opts) => {
    try {
      const analyzer = getSmartLogAnalyzer()
      
      let logPaths: string[]
      if (opts.files) {
        logPaths = opts.files.split(',')
      } else if (opts.discover) {
        logPaths = analyzer.discoverLogPaths()
        console.log(`🔍 发现日志文件: ${logPaths.join(', ')}\n`)
      } else {
        logPaths = analyzer.discoverLogPaths()
      }

      const result = await analyzer.analyze(
        logPaths,
        opts.pattern,
        parseInt(opts.hours)
      )

      if (opts.trends) {
        console.log('📈 日志趋势:')
        for (const t of result.trends) {
          const bar = '█'.repeat(Math.min(t.errors, 30))
          console.log(`  ${t.timeBucket.substring(11, 16)} ${bar} ${t.errors}`)
        }
      } else if (opts.anomalies) {
        console.log('🚨 检测到的异常:')
        for (const a of result.anomalies) {
          const emoji = { critical: '🔴', warning: '⚠️', info: 'ℹ️' }[a.severity]
          console.log(`  ${emoji} [${a.type}] ${a.description}`)
        }
      } else {
        console.log(analyzer.formatAnalysisResult(result))
      }
    } catch (error: any) {
      console.error(`❌ 日志分析失败: ${error.message}`)
      process.exit(1)
    }
  })

// ============================================================
// config 命令组
// ============================================================

const configCmd = program.command('config').description('配置变更追踪')

configCmd
  .command('list')
  .description('查看追踪文件列表')
  .action(() => {
    const tracker = getConfigChangeTracker()
    console.log(tracker.formatTrackedFiles())
  })

configCmd
  .command('add <path>')
  .description('添加追踪文件')
  .option('-a, --alias <name>', '文件别名')
  .action((path, opts) => {
    const tracker = getConfigChangeTracker()
    tracker.addFile(path, opts.alias)
    console.log(`✅ 已添加: ${path}`)
  })

configCmd
  .command('remove <path>')
  .description('移除追踪文件')
  .action((path) => {
    const tracker = getConfigChangeTracker()
    if (tracker.removeFile(path)) {
      console.log(`✅ 已移除: ${path}`)
    } else {
      console.log(`❌ 未找到: ${path}`)
    }
  })

configCmd
  .command('baseline')
  .description('建立配置基线')
  .action(async () => {
    const tracker = getConfigChangeTracker()
    const result = await tracker.createBaseline()
    console.log(`基线建立: ${result.created} 成功, ${result.failed} 失败`)
    for (const d of result.details) {
      console.log(`  ${d}`)
    }
  })

configCmd
  .command('check')
  .description('检查配置变更')
  .action(async () => {
    const tracker = getConfigChangeTracker()
    const result = await tracker.checkChanges()
    console.log(tracker.formatCheckResult(result))
  })

configCmd
  .command('history')
  .description('查看变更历史')
  .option('-p, --path <file>', '指定文件')
  .option('-n, --limit <n>', '显示条数', '20')
  .action((opts) => {
    const tracker = getConfigChangeTracker()
    const records = tracker.getChangeHistory(opts.path, parseInt(opts.limit))
    console.log(tracker.formatChangeHistory(records))
  })

// ============================================================
// report 命令
// ============================================================

program
 .command('report')
 .description('生成运维报告')
 .option('-f, --format <type>', '输出格式(markdown|json|text)', 'markdown')
 .option('--no-health', '跳过健康检查')
 .option('--no-security', '跳过安全审计')
 .option('--no-logs', '跳过日志分析')
 .option('--no-config', '跳过配置变更')
 .option('-t, --title <title>', '报告标题', '运维巡检报告')
 .action(async (opts) => {
 try {
 const generator = getReportGenerator()
 const report = await generator.generate({
 format: opts.format as ReportFormat,
 includeHealth: opts.health !== false,
 includeSecurity: opts.security !== false,
 includeLogs: opts.logs !== false,
 includeConfig: opts.config !== false,
 title: opts.title,
 })

 console.log(generator.format(report, opts.format as ReportFormat))
 } catch (error: any) {
 console.error(`❌ 生成报告失败: ${error.message}`)
 process.exit(1)
 }
 })

// ============================================================
// docker-health 命令
// ============================================================

program
 .command('docker-health')
 .description('Docker 容器健康巡检')
 .option('-c, --container <name>', '检查指定容器')
 .option('--images', '只检查镜像更新')
 .option('--max-restarts <n>', '最大重启次数阈值', '5')
 .option('--max-image-age <days>', '镜像过期天数阈值', '90')
 .option('--json', 'JSON格式输出')
 .action(async (opts) => {
 try {
 const { DockerHealthChecker } = await import('./utils/docker-health-checker.js')
 const checker = new DockerHealthChecker({
 maxRestartCount: parseInt(opts.maxRestarts),
 maxImageAgeDays: parseInt(opts.maxImageAge),
 })

 if (opts.images) {
 const images = await checker.checkImageUpdates()
 const old = images.filter(i => i.needsUpdate)
 const fresh = images.filter(i => !i.needsUpdate)
 if (opts.json) {
 console.log(JSON.stringify({ old, fresh }, null, 2))
 } else {
 if (old.length > 0) {
 console.log(`⚠️ ${old.length} 个镜像需要更新:`)
 for (const img of old) {
 console.log(`  [!] ${img.image} - ${img.daysOld}天前创建`)
 }
 }
 console.log(`✅ ${fresh.length} 个镜像状态正常`)
 }
 return
 }

 if (opts.container) {
 const result = await checker.inspectByName(opts.container)
 if (!result) {
 console.error(`❌ 未找到容器: ${opts.container}`)
 process.exit(1)
 }
 if (opts.json) {
 console.log(JSON.stringify(result, null, 2))
 } else {
 const mark = result.status === 'critical' ? '❌' : result.status === 'warning' ? '⚠️' : '✅'
 console.log(`${mark} ${result.container} (${result.image}): ${result.status}`)
 for (const issue of result.issues) {
 const im = issue.severity === 'critical' ? '!!!' : ' ! '
 console.log(`  [${im}] ${issue.type}: ${issue.message}`)
 console.log(`       -> ${issue.suggestion}`)
 }
 }
 return
 }

 const report = await checker.runFullInspection()
 if (opts.json) {
 console.log(JSON.stringify(report, null, 2))
 } else {
 console.log(checker.formatReport(report))
 }
 } catch (error: any) {
 console.error(`❌ Docker健康巡检失败: ${error.message}`)
 process.exit(1)
 }
 })

// ============================================================
// ssl 命令
// ============================================================

program
 .command('ssl <domains...>')
 .description('SSL证书监控 (域名列表)')
 .option('-p, --port <n>', '指定端口', '443')
 .option('--warn-days <n>', '提前N天告警', '30')
 .option('--critical-days <n>', '提前N天严重告警', '7')
 .option('--detail', '显示证书详情(单域名)')
 .option('--json', 'JSON格式输出')
 .action(async (domains, opts) => {
 try {
 const { SSLMonitor } = await import('./utils/ssl-monitor.js')
 const monitor = new SSLMonitor({
 domains,
 warnDays: parseInt(opts.warnDays),
 criticalDays: parseInt(opts.criticalDays),
 port: parseInt(opts.port),
 })

 if (opts.detail && domains.length === 1) {
 const domain = domains[0]
 const result = await monitor.checkDomain(domain, parseInt(opts.port))

 if (result.status === 'error') {
 console.error(`❌ ${domain} - ${result.error || '连接失败'}`)
 process.exit(1)
 }

 const cert = result.cert
 if (!cert) {
 console.error(`❌ ${domain} - 无法获取证书信息`)
 process.exit(1)
 }

 if (opts.json) {
 console.log(JSON.stringify(result, null, 2))
 } else {
 const mark = cert.status === 'valid' ? '✅' : cert.status === 'expiring-soon' ? '⚠️' : '❌'
 console.log(`${mark} SSL 证书详情: ${domain}:${opts.port}`)
 console.log(`  域名: ${cert.subject}`)
 console.log(`  颁发者: ${cert.issuer}`)
 console.log(`  有效期: ${cert.validFrom} ~ ${cert.validTo}`)
 console.log(`  剩余: ${cert.daysRemaining} 天`)
 console.log(`  协议: ${cert.protocol}`)
 if (cert.sanDomains.length > 0) {
 console.log(`  SAN: ${cert.sanDomains.join(', ')}`)
 }
 if (result.chainIssues.length > 0) {
 console.log(`  ⚠️ 链路问题:`)
 for (const ci of result.chainIssues) {
 console.log(`    - ${ci}`)
 }
 }
 }
 return
 }

 const report = await monitor.checkDomains(domains)
 if (opts.json) {
 console.log(JSON.stringify(report, null, 2))
 } else {
 console.log(monitor.formatReport(report))
 }
 } catch (error: any) {
 console.error(`❌ SSL检查失败: ${error.message}`)
 process.exit(1)
 }
 })

// ============================================================
// 启动
// ============================================================

program.parse()
