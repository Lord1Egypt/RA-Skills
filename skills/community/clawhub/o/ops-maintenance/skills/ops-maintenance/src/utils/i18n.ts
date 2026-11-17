/**
 * i18n 国际化支持 (skills版本)
 */

export type Language = 'zh' | 'en'

const translations: Record<Language, Record<string, string>> = {
  zh: {
    'unknown_action': '未知操作',
    'available_ops': '可用操作',
    'health_check': '系统健康检查',
    'log_analysis': '日志分析',
    'performance_monitor': '性能监控',
    'port_check': '端口检查',
    'process_check': '进程检查',
    'disk_check': '磁盘使用',
    'password_check': '密码过期检查',
    'cluster_summary': '服务器集群状态',
    'network_diag': '网络诊断',
    'report': '运维报告',
    'audit': '审计日志',
    'docker_health': 'Docker健康巡检',
    'ssl_check': 'SSL证书检查',
    'security_audit': '安全审计',
    'alert_rules': '告警规则',
    'patrol_jobs': '巡检任务',
    'network_ping': '网络Ping检测',
    'network_dns': 'DNS解析',
    'network_traceroute': '路由追踪',
    'service_status': '服务状态检查',
    'config_change': '配置变更追踪',
    'smart_log': '智能日志分析',
    'help': '帮助',
    'version': '版本',
  },
  en: {
    'unknown_action': 'Unknown action',
    'available_ops': 'Available operations',
    'health_check': 'System Health Check',
    'log_analysis': 'Log Analysis',
    'performance_monitor': 'Performance Monitor',
    'port_check': 'Port Check',
    'process_check': 'Process Check',
    'disk_check': 'Disk Usage',
    'password_check': 'Password Expiration',
    'cluster_summary': 'Server Cluster Status',
    'network_diag': 'Network Diagnostics',
    'report': 'Operations Report',
    'audit': 'Audit Logs',
    'docker_health': 'Docker Health Check',
    'ssl_check': 'SSL Certificate Check',
    'security_audit': 'Security Audit',
    'alert_rules': 'Alert Rules',
    'patrol_jobs': 'Patrol Jobs',
    'network_ping': 'Network Ping',
    'network_dns': 'DNS Resolution',
    'network_traceroute': 'Traceroute',
    'service_status': 'Service Status Check',
    'config_change': 'Config Change Tracker',
    'smart_log': 'Smart Log Analysis',
    'help': 'Help',
    'version': 'Version',
  }
}

export function t(key: string, lang: Language = 'zh'): string {
  return translations[lang]?.[key] || key
}

export function getSystemLanguage(): Language {
  const lang = process.env.LANG || process.env.LC_ALL || ''
  if (lang.startsWith('en')) return 'en'
  return 'zh'
}
