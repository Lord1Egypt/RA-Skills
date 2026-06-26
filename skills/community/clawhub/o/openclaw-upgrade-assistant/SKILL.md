---
name: "openclaw-upgrade-assistant"
description: "深度分析 OpenClaw 版本更新对现有配置的影响，生成兼容性报告并精准备份受影响文件。Invoke when user asks to analyze OpenClaw updates, check upgrade compatibility, or backup configs before upgrading."
---

# OpenClaw 升级前影响评估工具

自动分析 OpenClaw 官方更新对你的配置和备份系统的影响，生成详细报告并自动备份。

## 🎯 功能

- 🔍 获取官方最新版本更新内容
- 📊 分析更新对现有配置的影响
- ✅ 检查备份系统完整性
- 📝 生成详细影响分析报告
- 🔄 自动备份受影响的配置文件
- ⚠️ 提供升级建议和注意事项

## 🤝 与其他 Update 技能的关系

### 我们不做:
- ❌ 不执行 OpenClaw 更新
- ❌ 不自动更新技能包
- ❌ 不修改系统配置

### 我们专注:
- ✅ 升级前深度影响分析
- ✅ 配置兼容性评估
- ✅ 精准备份受影响文件
- ✅ 生成详细升级建议

### 完美互补:
- 先用 **openclaw-update-checker** 分析影响
- 再用 **Openclaw Update** 执行更新
- 安全 + 可靠！

### 典型使用场景:
```javascript
// 步骤 1: 分析影响（我们的技能）
const analysis = await openclaw.updateChecker.analyze();
if (analysis.compatibilityCheck.high === 0) {
  console.log('✅ 可以安全升级');
  
  // 步骤 2: 执行更新（使用 Openclaw Update 等工具）
  // openclaw update
}
```

## 🚀 使用示例

### 基础用法

```javascript
// 检查官方更新影响
const result = await openclaw.updateChecker.analyze();
console.log(result.report);
```

### 完整用法

```javascript
// 分析更新影响并生成报告
const analysis = await openclaw.updateChecker.analyze({
  currentVersion: '2026.3.13',  // 当前版本（可选，自动检测）
  targetVersion: 'latest',       // 目标版本（可选，默认 latest）
  backupAffected: true,          // 是否备份受影响的文件（可选，默认 true）
  generateReport: true,          // 是否生成报告（可选，默认 true）
  outputPath: './update-impact-report.md'  // 报告输出路径（可选）
});

// 输出分析结果
console.log('影响评估:', analysis.impactSummary);
console.log('需要关注的文件:', analysis.affectedFiles);
console.log('升级建议:', analysis.recommendations);
```

### 检查特定配置文件

```javascript
// 检查特定配置文件的兼容性
const configCheck = await openclaw.updateChecker.checkConfig({
  files: ['AGENTS.md', 'HEARTBEAT.md', 'scripts/*.js'],
  version: '2026.3.23'
});
```

### 生成备份

```javascript
// 备份当前配置
const backup = await openclaw.updateChecker.backup({
  destination: './backup/update-20260324',
  includeAffectedOnly: true  // 只备份受影响的文件
});
```

## 📋 工作流程

1. **获取版本信息**
   - 检测当前安装的 OpenClaw 版本
   - 获取官方最新版本信息
   - 读取 GitHub Release 更新日志

2. **分析更新内容**
   - 解析 Breaking Changes
   - 识别配置变更
   - 标记废弃功能
   - 记录新增功能

3. **检查本地配置**
   - 扫描工作区配置文件
   - 对比更新影响范围
   - 识别潜在兼容性问题

4. **生成影响报告**
   - 高优先级问题（必须处理）
   - 中优先级问题（建议处理）
   - 低优先级问题（需要注意）
   - 无影响项目（完全兼容）

5. **自动备份**
   - 备份受影响的配置文件
   - 创建版本快照
   - 记录备份清单

6. **提供建议**
   - 升级步骤
   - 升级后检查清单
   - 回滚方案

## 📊 输出示例

```markdown
# OpenClaw 更新影响分析报告

**分析时间**: 2026-03-24 11:09
**当前版本**: v2026.3.13
**目标版本**: v2026.3.23

## 影响评估

### 🔴 高优先级（必须处理）
- 无

### 🟡 中优先级（建议处理）
- 飞书媒体附件配置 - 官方已修复发送失败问题
- Exec 安全审批规则变更 - 可能需要重新审批命令

### 🟢 低优先级（需要注意）
- 浏览器 CDP 配置 - 官方优化复用逻辑
- 插件 SDK 路径变更 - 不影响最终用户

## 兼容性统计

| 类别 | 文件数 | 兼容性 |
|------|--------|--------|
| 核心配置 | 7 | ✅ 100% |
| 技能包 | 100+ | ✅ 100% |
| 自动化脚本 | 15+ | ✅ 100% |
| 文档 | 10 | ✅ 100% |

## 升级建议

1. 可以安全升级到 v2026.3.23
2. 升级后测试飞书图片发送
3. 检查浏览器连接是否正常
4. 关注 Exec 审批日志

## 备份清单

✅ 已备份 13 个文件到 ./backup/update-20260324
```

## ⚙️ 配置

在 `openclaw.json` 中添加配置：

```json
{
  "skills": {
    "entries": {
      "openclaw-update-checker": {
        "config": {
          "autoBackup": true,
          "backupDestination": "./backup",
          "reportFormat": "markdown",
          "includeVersionHistory": true,
          "githubRepo": "openclaw/openclaw"
        }
      }
    }
  }
}
```

## 🔧 API 参考

### `analyze(options)`

分析更新影响

**参数**:
- `options.currentVersion` (string, 可选): 当前版本，默认自动检测
- `options.targetVersion` (string, 可选): 目标版本，默认 'latest'
- `options.backupAffected` (boolean, 可选): 是否备份受影响文件，默认 true
- `options.generateReport` (boolean, 可选): 是否生成报告，默认 true
- `options.outputPath` (string, 可选): 报告输出路径

**返回**:
```javascript
{
  impactSummary: {
    high: 0,
    medium: 2,
    low: 3,
    none: 120
  },
  affectedFiles: [...],
  recommendations: [...],
  report: "完整报告内容"
}
```

### `checkConfig(options)`

检查配置文件兼容性

**参数**:
- `options.files` (string[]): 文件路径列表
- `options.version` (string): 目标版本

**返回**:
```javascript
{
  compatible: [...],
  incompatible: [...],
  warnings: [...]
}
```

### `backup(options)`

备份配置文件

**参数**:
- `options.destination` (string): 备份目标路径
- `options.includeAffectedOnly` (boolean): 是否只备份受影响文件
- `options.files` (string[], 可选): 指定要备份的文件

**返回**:
```javascript
{
  backupPath: "./backup/update-20260324",
  files: [...],
  timestamp: "2026-03-24T11:09:00+08:00"
}
```

### `getReleaseNotes(version)`

获取指定版本的更新说明

**参数**:
- `version` (string): 版本号或 'latest'

**返回**:
```javascript
{
  version: "2026.3.23",
  releaseDate: "2026-03-24",
  changes: [...],
  breakingChanges: [...],
  fixes: [...],
  features: [...]
}
```

## 📦 依赖

- `node-fetch` - HTTP 请求
- `semver` - 版本比较
- `fs-extra` - 文件操作
- `js-yaml` - YAML 解析（可选）

## 🛠️ 安装

```bash
# 从 ClawHub 安装（推荐）
openclaw skills install openclaw-update-checker

# 或从 GitHub 安装
openclaw skills install github:Adgai115/openclaw-260324/skills/openclaw-update-checker
```

## 📝 使用场景

### 场景 1: 定期升级检查

每周运行一次，检查是否有新版本并分析影响：

```javascript
// 定时任务：每周日 9:00
const result = await openclaw.updateChecker.analyze();
if (result.impactSummary.high > 0) {
  await openclaw.message.send({
    to: 'user',
    message: `⚠️ 发现 ${result.impactSummary.high} 个高优先级更新，请查看报告`
  });
}
```

### 场景 2: 升级前检查

准备升级前运行，确保兼容性：

```javascript
// 升级前
const analysis = await openclaw.updateChecker.analyze();
if (analysis.impactSummary.high === 0) {
  console.log('✅ 可以安全升级');
  await openclaw.exec({ command: 'pnpm add -g openclaw@latest' });
} else {
  console.log('⚠️ 存在兼容性问题，请先处理');
}
```

### 场景 3: 备份检查

定期备份配置并验证完整性：

```javascript
// 每天 2:00
await openclaw.updateChecker.backup({
  destination: `./backup/daily-${new Date().toISOString().split('T')[0]}`,
  includeAffectedOnly: false
});
```

## ⚠️ 注意事项

1. **权限**: 需要工作区文件读写权限
2. **网络**: 需要访问 GitHub API
3. **备份**: 建议升级前都运行一次检查
4. **报告**: 生成的报告会自动保存到工作区

## 🐛 故障排查

### 问题：无法获取最新版本

**解决**:
```javascript
// 手动指定版本
await openclaw.updateChecker.analyze({
  targetVersion: '2026.3.23'
});
```

### 问题：备份失败

**解决**:
```javascript
// 检查磁盘空间
// 确保备份目录存在
await openclaw.exec({ command: 'mkdir -p ./backup' });
```

### 问题：报告生成失败

**解决**:
```javascript
// 检查输出路径权限
// 尝试使用绝对路径
await openclaw.updateChecker.analyze({
  outputPath: 'E:/Dev/.openclaw/workspace/update-report.md'
});
```

## 📚 相关资源

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [OpenClaw GitHub Releases](https://github.com/openclaw/openclaw/releases)
- [备份最佳实践](https://docs.openclaw.ai/gateway/backup)

## 📄 许可证

MIT License

## 👥 贡献者

- 潜助 🤖 (原创作者)

---

**版本**: 1.0.0  
**创建日期**: 2026-03-24  
**最后更新**: 2026-03-24
