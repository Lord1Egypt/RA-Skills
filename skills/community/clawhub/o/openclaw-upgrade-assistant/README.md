# 📦 OpenClaw 升级前影响评估工具 Skill

## 🎯 功能

自动分析 OpenClaw 官方更新对你的配置和备份系统的影响，生成详细报告并自动备份。

## ✨ 特性

- 🔍 **自动检测版本** - 获取当前和最新 OpenClaw 版本
- 📊 **影响分析** - 分析更新对配置文件的影响程度
- ✅ **兼容性检查** - 检查所有配置文件、脚本、技能包的兼容性
- 📝 **生成报告** - 生成详细的 Markdown 格式分析报告
- 🔄 **自动备份** - 备份受影响的配置文件
- 💡 **升级建议** - 提供升级步骤和注意事项

## 🚀 快速开始

### 安装

```bash
# 从本地安装
openclaw skills install ./skills/openclaw-upgrade-assistant

# 或从 GitHub 安装
openclaw skills install github:Adgai115/Skill-Library
```

### 使用

#### 方式 1: 命令行

```bash
cd skills/openclaw-update-checker
node index.js
```

#### 方式 2: 在 Skill 中调用

```javascript
const updateChecker = require('./skills/openclaw-update-checker');

const result = await updateChecker.analyzeUpdateImpact({
  currentVersion: '2026.3.13',
  targetVersion: 'latest',
  backupAffected: true,
  generateReport: true
});

console.log(result);
```

#### 方式 3: 定时任务

在心跳系统中定期运行：

```javascript
// 每周日 9:00 检查更新
const analysis = await openclaw.updateChecker.analyze();
if (analysis.compatibilityCheck.high > 0) {
  await sendMessage(`⚠️ 发现 ${analysis.compatibilityCheck.high} 个高优先级更新`);
}
```

## 📊 输出示例

运行后会生成：

1. **控制台输出**
   ```
   🔍 开始分析 OpenClaw 更新影响...
   当前版本：v2026.3.13
   目标版本：v2026.3.23
   ✅ 获取到 2026.3.23 更新内容
   ✅ 扫描到 130 个配置文件
   ✅ 完成影响分析
   ✅ 已备份到：./backup/update-2026-03-24
   ✅ 报告已生成：OPENCLAW-UPDATE-IMPACT-ANALYSIS.md
   ```

2. **报告文件** - `OPENCLAW-UPDATE-IMPACT-ANALYSIS.md`

3. **备份目录** - `./backup/update-2026-03-24/`

## 📋 报告内容

生成的报告包含：

- 📊 兼容性统计表格
- 📋 官方更新内容回顾
- ⚠️ 受影响文件清单
- 💡 升级建议
- 📝 升级步骤
- ✅ 升级后检查清单
- 📦 备份信息

## ⚙️ 配置选项

```javascript
{
  currentVersion: '2026.3.13',    // 当前版本（可选，自动检测）
  targetVersion: 'latest',        // 目标版本（可选，默认 latest）
  backupAffected: true,           // 是否备份（可选，默认 true）
  generateReport: true,           // 是否生成报告（可选，默认 true）
  outputPath: './report.md'       // 报告路径（可选）
}
```

## 🔧 API 参考

### `analyzeUpdateImpact(options)`

分析更新影响

**参数**:
- `options.currentVersion` (string): 当前版本
- `options.targetVersion` (string): 目标版本
- `options.backupAffected` (boolean): 是否备份
- `options.generateReport` (boolean): 是否生成报告

**返回**:
```javascript
{
  releaseNotes: {...},
  affectedFiles: [...],
  compatibilityCheck: {
    high: 0,
    medium: 2,
    low: 3,
    none: 120
  },
  recommendations: [...],
  timestamp: '2026-03-24T11:09:00.000Z'
}
```

## 📁 文件结构

```
openclaw-update-checker/
├── SKILL.md              # Skill 文档
├── _meta.json            # 元数据
├── index.js              # 主程序
├── package.json          # 依赖配置
└── README.md             # 使用说明
```

## 🛠️ 依赖

- `fs-extra` - 文件操作
- `node-fetch` - HTTP 请求
- `semver` - 版本比较

## 📝 使用场景

### 1. 定期升级检查

每周运行一次，检查是否有新版本：

```javascript
// 每周日 9:00
const result = await analyzeUpdateImpact();
```

### 2. 升级前检查

准备升级前运行，确保兼容性：

```javascript
const analysis = await analyzeUpdateImpact();
if (analysis.compatibilityCheck.high === 0) {
  console.log('✅ 可以安全升级');
  // 执行升级
}
```

### 3. 备份检查

定期备份配置并验证完整性：

```javascript
await analyzeUpdateImpact({
  backupAffected: true,
  generateReport: false
});
```

## ⚠️ 注意事项

1. **权限**: 需要工作区文件读写权限
2. **网络**: 需要访问 GitHub API
3. **备份**: 建议升级前都运行一次检查
4. **报告**: 自动保存到工作区根目录

## 🐛 故障排查

### 问题：无法获取最新版本

**解决**: 手动指定版本
```javascript
await analyzeUpdateImpact({
  targetVersion: '2026.3.23'
});
```

### 问题：备份失败

**解决**: 检查磁盘空间和目录权限

## 📚 相关资源

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [OpenClaw GitHub Releases](https://github.com/openclaw/openclaw/releases)

## 📄 许可证

MIT License

## 👥 贡献者

- 潜助 🤖 (原创作者)

---

**版本**: 1.0.0  
**创建日期**: 2026-03-24  
**最后更新**: 2026-03-24
