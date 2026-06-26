---
name: jax-skill-security-scanner
description: 🔐 OpenClaw技能安全扫描器 - 专业级安全审计工具，检测敏感操作、木马后门，保护您的AI助手生态安全
emoji: 🔐
license: MIT
requires:
  bins: [node, npm]
install:
  - id: npm
    kind: npm
    package: "@jax-npm/skill-security-scanner"
tags: [security, scanner, audit, safety, openclaw, plugin]
author: jax-npm
version: 1.0.5
---

# 🔐 OpenClaw技能安全扫描器

**专业级安全审计工具，保护您的AI助手生态安全**

> 🚨 **安全警告**: 本工具本身被标记为高风险，这是预期的！安全扫描工具需要访问敏感功能来检测安全问题。请在使用前审查代码，确认其安全性和必要性。

## ✨ 核心功能

### 🔍 **智能敏感操作检测**
- **关键词扫描**: 自动识别SKILL.md中的危险命令（exec, rm, kill, sudo等）
- **代码分析**: 深度分析JavaScript/TypeScript代码中的安全隐患
- **依赖审查**: 检查package.json中的危险脚本和依赖
- **风险评级**: 自动评估技能风险等级（高/中/低）

### 🦠 **高级木马/后门检测**
- **网络后门**: 检测net, http, ws, socket.io等网络通信风险
- **文件系统**: 识别fs模块的危险文件操作
- **进程控制**: 监控child_process, exec, spawn等进程操作
- **数据外传**: 发现crypto, Buffer, base64等数据加密外传
- **代码混淆**: 识别eval, Function构造器等代码隐藏技术
- **组合模式**: 检测高风险的操作组合模式

### 🤖 **AI投毒检测 (新增)**
- **提示注入**: 检测ignore previous, disregard, override等指令覆盖攻击
- **越狱攻击**: 检测jailbreak, DAN, roleplay等绕过安全限制尝试
- **系统提示提取**: 检测提取system prompt的恶意请求
- **上下文污染**: 检测JSON/XML格式的伪装指令
- **代码注入**: 检测eval/import等危险代码执行
- **社会工程**: 检测诱导确认、伪装无害等手法

### 🎭 **虚假信息/幻觉检测 (新增)**
- **虚假广告**: 检测夸张宣传、虚假折扣、假冒促销
- **诈骗识别**: 检测中奖诈骗、账户安全诈骗、诱导转账
- **假冒产品**: 检测高仿、A货、假冒品牌
- **违规内容**: 检测违法交易、违规服务推广
- **虚假宣传**: 检测软文推广、虚假体验分享

### 📊 **专业报告系统**
- **多格式输出**: 文本、Markdown、JSON、增强文本、增强Markdown格式报告
- **风险统计**: 清晰的风险等级分布统计
- **木马摘要**: 详细的木马检测结果汇总
- **安全建议**: 针对性的安全改进建议
- **可视化**: 易于理解的报告格式
- **中高危清单**: 专门列出所有中高危技能，标记风险等级
- **风险摘要**: 快速查看中高危技能摘要

## 🚀 快速开始

### **通过ClawHub安装（推荐）**

```bash
# 搜索技能
npx clawhub search security-scanner

# 安装技能
npx clawhub install jax-skill-security-scanner --force

# 注意：需要--force参数，因为安全工具被标记为可疑
```

### **作为npm包安装**

```bash
# 全局安装命令行工具
npm install -g @jax-npm/skill-security-scanner

# 或作为项目依赖安装
npm install @jax-npm/skill-security-scanner
```

### **作为OpenClaw插件安装**

```bash
# 从npm安装
openclaw plugins add @jax-npm/skill-security-scanner

# 或从本地路径安装
openclaw plugins add ./skill-security-scanner
```

## 📖 详细使用指南

### **基本扫描**

```bash
# 扫描默认技能目录
skill-security-scan

# 指定扫描路径
skill-security-scan --scan-path "/path/to/your/skills"

# Windows路径
skill-security-scan --scan-path "C:\path\to\skills"
```

### **输出格式控制**

```bash
# 文本格式（默认）
skill-security-scan --format text

# Markdown格式（适合文档）
skill-security-scan --format markdown

# JSON格式（适合自动化处理）
skill-security-scan --format json

# 增强文本格式（包含中高危技能清单）
skill-security-scan --format enhanced-text

# 增强Markdown格式（包含中高危技能清单）
skill-security-scan --format enhanced-markdown

# 只显示中高危技能摘要
skill-security-scan --risk-summary

# 保存到文件
skill-security-scan --format enhanced-markdown > security-report.md
```

### **高级选项**

```bash
# 详细模式（显示更多信息）
skill-security-scan --verbose

# 只显示高风险
skill-security-scan --filter high

# 排除特定技能
skill-security-scan --exclude "skill1,skill2"

# 自定义敏感关键词
skill-security-scan --keywords "exec,rm,kill,sudo,eval"

# 生成增强报告（包含中高危技能清单）
skill-security-scan --enhanced

# 只显示中高危技能摘要
skill-security-scan --risk-summary
```

### **通过OpenClaw使用**

```bash
# 直接调用
openclaw skill-security-scan

# 带参数调用
openclaw skill-security-scan --format json --scan-path ./skills
```

## 🎯 使用场景

### **1. 新技能安全审查**
```bash
# 审查新下载的技能
skill-security-scan --scan-path ./new-skills --format markdown
```

### **2. 定期安全审计**
```bash
# 每月安全审计
skill-security-scan --format json --output monthly-audit-$(date +%Y-%m).json
```

### **3. CI/CD集成**
```bash
# 在CI流水线中集成
skill-security-scan --format json | jq '.highRiskCount'
# 如果高风险技能>0，则失败
```

### **4. 技能开发安全自查**
```bash
# 开发过程中自查
skill-security-scan --scan-path ./my-skill --verbose
```

### **5. 中高危技能清单生成**
```bash
# 生成包含中高危技能清单的增强报告
skill-security-scan --format enhanced-text

# 生成Markdown格式的增强报告
skill-security-scan --format enhanced-markdown > risk-report.md

# 快速查看中高危技能摘要
skill-security-scan --risk-summary

# 输出示例：
# 📋 中高危技能摘要:
# 
# 🔴 高危技能:
#   • coding-agent ⚠️
#   • tmux
# 
# 🟡 中危技能:
#   • feishu-doc
#   • feishu-drive
# 
# 📊 总计: 4个中高危技能
```

## 📊 报告示例

### **文本报告示例**
```
📊 OpenClaw 技能安全扫描报告
📅 扫描时间: 2026/3/13 11:55:02
📁 扫描路径: /path/to/skills
🔍 扫描技能: 52个

📊 风险统计:
  🔴 高风险: 4个
  🟡 中风险: 48个
  🟢 低风险: 0个

🦠 木马检测摘要:
  检测技能: 52/52
  高风险: 0个
  中风险: 0个
  可疑文件: 0个

🔴 高风险技能:
  • coding-agent (⚠️ 系统技能)
    ⚠️ 检测到敏感操作: exec, spawn, kill
  • tmux (⚠️ 系统技能)
    ⚠️ 检测到敏感操作: send-keys, kill-session
```

### **JSON报告结构**
```json
{
  "scanTime": "2026-03-13T11:55:02.000Z",
  "scanPath": "/path/to/skills",
  "totalSkills": 52,
  "riskStats": {
    "high": 4,
    "medium": 48,
    "low": 0
  },
  "trojanDetection": {
    "scannedSkills": 52,
    "highRisk": 0,
    "mediumRisk": 0,
    "suspiciousFiles": 0
  },
  "highRiskSkills": [
    {
      "name": "coding-agent",
      "riskLevel": "high",
      "sensitiveOperations": ["exec", "spawn", "kill"],
      "trojanPatterns": []
    }
  ]
}
```

## ⚙️ 配置说明

### **OpenClaw配置文件**
```yaml
# openclaw.json
{
  "plugins": {
    "entries": {
      "skill-security-scanner": {
        "config": {
          "scanPath": "/path/to/skills",
          "defaultFormat": "markdown",
          "sensitiveKeywords": [
            "exec", "shell", "rm", "delete", "format",
            "kill", "sudo", "eval", "import", "require"
          ],
          "trojanPatterns": {
            "network": ["net", "http", "ws", "socket.io"],
            "filesystem": ["fs.write", "fs.unlink", "fs.rmdir"],
            "process": ["child_process", "exec", "spawn"],
            "crypto": ["crypto", "Buffer", "base64"]
          }
        }
      }
    }
  }
}
```

### **环境变量**
```bash
# 设置默认扫描路径
export SKILL_SCAN_PATH="/path/to/skills"

# 设置默认输出格式
export SKILL_SCAN_FORMAT="json"

# 启用详细日志
export SKILL_SCAN_VERBOSE="true"
```

## 🔧 故障排除

### **常见问题**

**Q: 扫描时显示"目录不存在"错误**
```bash
# 错误：扫描目录不存在
# 解决方案：指定正确的路径
skill-security-scan --scan-path "C:\Users\Administrator\.openclaw\workspace\skills"
```

**Q: 工具被标记为高风险，是否安全？**
```
A: 这是预期的！安全扫描工具需要访问敏感功能来检测安全问题。
   建议：1. 审查源代码 2. 在受控环境中使用 3. 定期更新
```

**Q: 如何信任这个工具？**
```
A: 1. 查看源代码: https://github.com/jax-npm/skill-security-scanner
   2. 自行构建: npm run build
   3. 在沙盒环境中测试
```

**Q: 扫描结果太多误报？**
```bash
# 调整敏感度
skill-security-scan --keywords "exec,rm"  # 只检测最危险的命令

# 排除系统技能
skill-security-scan --exclude "coding-agent,tmux,canvas"
```

### **性能优化**
```bash
# 只扫描最近修改的技能
find ./skills -type f -name "SKILL.md" -mtime -7 | xargs skill-security-scan

# 并行扫描（如果有多个目录）
skill-security-scan --scan-path ./skills1 &
skill-security-scan --scan-path ./skills2 &
wait
```

## 📈 最佳实践

### **1. 定期扫描计划**
```bash
# 每周扫描（添加到cron）
0 2 * * 1 skill-security-scan --format json --output weekly-scan-$(date +\%Y-\%m-\%d).json
```

### **2. 技能入库审查**
```bash
# 新技能入库前必须通过安全审查
skill-security-scan --scan-path ./new-skill --format markdown > review.md
# 审查review.md，确认安全后才能入库
```

### **3. 安全基线设置**
```bash
# 设置安全基线：高风险技能不能超过2个
high_risk=$(skill-security-scan --format json | jq '.riskStats.high')
if [ $high_risk -gt 2 ]; then
  echo "❌ 安全基线被突破！高风险技能过多"
  exit 1
fi
```

### **4. 监控和告警**
```bash
# 监控高风险技能变化
current=$(skill-security-scan --format json | jq '.highRiskSkills | length')
previous=$(cat last-scan.json | jq '.highRiskSkills | length')

if [ $current -gt $previous ]; then
  echo "🚨 警告：高风险技能增加！"
  # 发送告警通知
fi
```

## 🛡️ 安全建议

### **立即行动**
1. **审查高风险技能** - 确认其安全性和必要性
2. **限制权限** - 为高风险技能设置最小必要权限
3. **监控行为** - 记录所有敏感操作日志

### **中期改进**
1. **建立白名单** - 只允许运行受信任的技能
2. **实施沙盒** - 在隔离环境中运行高风险技能
3. **代码审查** - 新技能必须经过安全审查

### **长期策略**
1. **安全培训** - 提高技能开发者的安全意识
2. **自动化审计** - 集成到CI/CD流水线
3. **威胁建模** - 定期进行安全威胁分析

## 🔄 更新和维护

### **检查更新**
```bash
# 检查npm包更新
npm outdated -g @jax-npm/skill-security-scanner

# 更新到最新版本
npm update -g @jax-npm/skill-security-scanner
```

### **版本历史**
- **v1.0.3** (2026-03-13): 新增中高危技能清单功能，支持增强报告格式
- **v1.0.2** (2026-03-09): 修复bug，优化性能，改进报告格式
- **v1.0.1** (2026-03-09): 添加木马检测功能，增强敏感操作识别
- **v1.0.0** (2026-03-09): 初始版本发布，基础扫描功能

### **问题反馈**
- **GitHub Issues**: https://github.com/jax-npm/skill-security-scanner/issues
- **邮件支持**: security@jax-npm.com
- **文档**: https://docs.jax-npm.com/skill-security-scanner

## 📄 许可证

MIT License - 详见 [LICENSE](https://github.com/jax-npm/skill-security-scanner/blob/main/LICENSE)

## 🙏 致谢

感谢所有贡献者和用户，是你们的反馈让这个工具变得更好！

---

**🔐 安全提示**: 安全是一个持续的过程，不是一次性的任务。定期扫描、持续监控、及时响应是保持系统安全的关键。

**🚀 开始保护您的OpenClaw生态吧！**