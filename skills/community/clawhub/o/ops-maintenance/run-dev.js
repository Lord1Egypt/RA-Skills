#!/usr/bin/env node
/**
 * ops-maintenance 开发模式入口
 * 显示开发状态和快速命令
 */

const fs = require('fs')

console.log(`
🚀 ops-maintenance 2.0 开发模式
============================

📊 架构重构进度：
""")

// 显示任务进度
const tasks = [
  { name: '类型系统 (types.ts)', status: '✅ 完成' },
  { name: 'ConfigManager 配置管理器', status: '✅ 完成' },
  { name: 'SSHClient 客户端', status: '✅ 完成' },
  { name: 'ConnectionPool 连接池', status: '✅ 完成' },
  { name: 'Cache 缓存系统', status: '✅ 完成' },
  { name: 'HealthChecker 健康检查策略', status: '✅ 完成' },
  { name: 'ThresholdChecker 阈值检查', status: '✅ 完成' },
  { name: 'UseCases 用例层', status: '✅ 完成' },
  { name: 'Formatter 格式化器', status: '✅ 完成' },
  { name: 'LegacyAdapter 向后兼容适配器', status: '✅ 完成' },
  { name: 'Container 依赖注入容器', status: '✅ 完成' },
  { name: '编译和集成测试', status: '⏳ 待完成' }
]

for (const task of tasks) {
  console.log(`  ${task.status} ${task.name}`)
}

console.log(`
📝 快速命令：
   node run.js cluster              - 集群健康检查（使用旧版逻辑）
   node run-new.js cluster          - 使用新架构（开发中）
   npm run build                    - 编译 TypeScript
   npm test                         - 运行测试

🔧 环境配置：
   编辑 ~/.config/ops-maintenance/servers.json 添加服务器
   或设置环境变量（推荐）：
     export OPS_CRED_10_119_120_143="salt:password"

💡 下一步：
   1. 修复编译错误，完成核心模块集成
   2. 编写单元测试
   3. 更新文档
   4. 发布 v2.0.0

查看详细文档：docs/ARCHITECTURE.md
    `)

// 如果有参数，直接执行
if (process.argv[2]) {
  const { execSync } = require('child_process')
  try {
    execSync('node run.js ' + process.argv.slice(2).join(' '), { stdio: 'inherit' })
  } catch {
    // 忽略错误
  }
}