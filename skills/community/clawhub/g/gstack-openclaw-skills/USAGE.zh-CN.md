# 使用指南

<div align="center">

**GStack-Skills 详细使用指南**

[English](USAGE.md) | 简体中文

</div>

---

## 目录

- [简介](#简介)
- [核心技能详解](#核心技能详解)
- [高级用法](#高级用法)
- [最佳实践](#最佳实践)
- [故障排除](#故障排除)
- [常见问题](#常见问题)

---

## 简介

本指南详细介绍了 GStack-Skills 的所有功能和使用方法。如果你是第一次使用，建议先查看 [快速开始指南](QUICKSTART.md)。

---

## 核心技能详解

### 1. `/review` - 代码审查

**功能**：自动审查代码，发现并修复问题

**使用方式**：

```
/review
```

或自然语言：

```
审查我的代码
```

**执行内容**：

1. 读取当前分支的所有变更
2. 分析代码质量和安全性
3. 检测潜在问题（SQL 注入、XSS、未处理异常等）
4. 提供修复建议
5. 应用自动修复（如适用）

**输出示例**：

```
📋 代码审查报告

分支：feature/user-authentication
文件变更：12 个
行数：+342, -89

🐛 发现的问题
严重问题：
❌ src/db/queries.py:45 - SQL 注入风险
   - 问题：用户输入直接拼接到 SQL 查询
   - 影响：攻击者可以执行任意 SQL 命令
   - 修复：使用参数化查询

警告问题：
⚠️ src/utils/logger.js:23 - 使用过时的 API
   - 问题：console.log 在生产环境中应避免使用
   - 影响：性能下降和安全隐患
   - 修复：替换为专业日志库

✅ 自动修复
1. src/db/queries.py:45 - 应用参数化查询
2. src/utils/logger.js:23 - 替换为 winston

📊 审查总结
- 严重问题：1 个 → 1 个已修复
- 警告问题：1 个 → 1 个已修复
- 代码质量评分：85/100

状态：✅ 审查完成
建议：运行 /qa 进行测试
```

**高级选项**：

```
/review --strict          # 严格模式，更多警告
/review --fix-all         # 自动修复所有问题
/review --format=verbose  # 详细输出格式
```

---

### 2. `/qa` - 测试

**功能**：运行系统化测试并修复 bug

**使用方式**：

```
/qa
```

或自然语言：

```
测试我的代码
```

**执行内容**：

1. 发现并运行所有测试
2. 分析失败的测试
3. 定位 bug 根因
4. 提供修复建议
5. 验证修复效果

**输出示例**：

```
🧪 测试报告

测试套件：
• 单元测试：45 个
• 集成测试：18 个
• 端到端测试：5 个

📊 测试结果
单元测试：
✅ 通过：44/45
❌ 失败：1

集成测试：
✅ 通过：18/18

端到端测试：
✅ 通过：5/5

🐛 失败测试分析
测试：auth.test.js - test_invalid_login()
错误：Expected 401, got 500

根因分析：
- 服务器未正确处理无效凭证
- 数据库查询未捕获异常

修复方案：
1. src/api/auth.js:67 - 添加异常处理
2. src/utils/validator.js:12 - 改进输入验证

✅ 修复已应用
重新运行测试...
✅ 所有测试通过（68/68）

📈 健康评分：95/100

状态：✅ 测试完成
建议：可以运行 /ship 部署
```

**高级选项**：

```
/qa --unit-only        # 仅运行单元测试
/qa --integration      # 仅运行集成测试
/qa --coverage         # 生成代码覆盖率报告
/qa --verbose          # 详细输出
```

---

### 3. `/ship` - 部署

**功能**：一键部署到生产环境

**使用方式**：

```
/ship
```

或自然语言：

```
部署到生产环境
```

**执行内容**：

1. 验证分支状态
2. 运行所有测试
3. 合并基础分支
4. 更新版本号
5. 创建 Pull Request
6. 执行部署

**输出示例**：

```
🚀 部署报告

目标环境：Production
当前版本：v1.2.3
目标版本：v1.2.4

📋 部署前检查
✅ 工作区干净
✅ 所有测试通过（68/68）
✅ 代码审查通过
✅ 版本更新准备就绪

🔄 部署步骤
1. 合并基础分支... ✅
2. 运行测试... ✅ (68/68 通过)
3. 更新版本号... ✅ (v1.2.4)
4. 创建 PR... ✅ (#89)
5. 等待 CI... ✅
6. 合并 PR... ✅
7. 部署到生产... ✅

📊 部署结果
• 部署时间：2 分 34 秒
• 新功能：用户认证系统
• 修复：3 个 bug
• 改进：性能优化 15%

✅ 部署成功
生产环境：https://app.example.com
监控：https://monitor.example.com

状态：✅ 已上线
```

**高级选项**：

```
/ship --staging        # 部署到测试环境
/ship --dry-run        # 模拟部署，不实际执行
/ship --skip-tests     # 跳过测试（不推荐）
```

---

### 4. `/office-hours` - 产品创意验证

**功能**：快速验证产品创意是否值得开发

**使用方式**：

```
/office-hours 我想做一个 AI 代码审查工具
```

或详细描述：

```
/office-hours
我想开发一个工具，帮助开发者自动审查代码。
它能检测 bug、安全问题，并提供修复建议。
目标用户是中小型开发团队。
```

**执行内容**：

1. 分析问题陈述
2. 验证问题真实性
3. 市场调研
4. 竞争分析
5. 技术可行性评估
6. 商业价值分析

**输出示例**：

```
💡 产品创意验证

创意：AI 代码审查工具
类型：自动化开发工具

🔍 问题验证
问题描述：开发者花费 30% 时间在代码审查上
数据支持：
• Stack Overflow 调查：代码审查平均耗时 2.5 小时/PR
• GitHub 数据：大型项目平均 15+ 小时代码审查时间
• 开发者反馈：65% 认为代码审查是效率瓶颈

✅ 问题真实且严重

📊 市场验证
目标市场：
• 初创公司：50K+ 个团队
• 中小企业：500K+ 个团队
• 个人开发者：1M+ 个用户

市场趋势：
• DevSecOps 增长率：42% YoY
• 自动化工具采用率：78%
• AI 辅助开发需求：+156%

✅ 市场机会巨大

🎯 竞争分析
主要竞品：
1. SonarQube
   - 优势：成熟、功能全面
   - 劣势：价格高、配置复杂
   - 市场份额：60%

2. Codacy
   - 优势：易用、集成好
   - 劣势：规则固定、灵活性差
   - 市场份额：25%

3. DeepCode
   - 优势：AI 驱动、智能
   - 劣势：新、生态小
   - 市场份额：5%

差异化机会：
✅ 自动化修复（竞品仅检测）
✅ 自然语言交互（竞品仅 CLI）
✅ 低价格/免费基础版

✅ 存在差异化机会

🔧 技术可行性
核心技术：
• 代码分析：✅ 成熟
• AI 模型：✅ 可用（GPT-4, Claude）
• 自动修复：✅ 可行
• 集成：✅ 标准化

技术风险：
• 低 - 已有成熟解决方案

✅ 技术可行性高

💰 商业价值
定价策略：
• 个人版：免费
• 团队版：$29/月
• 企业版：$99/月

市场规模估计：
• TAM（总市场）：$500M
• SAM（可服务市场）：$150M
• SOM（可获得市场）：$30M

预期收入（第一年）：
• 免费用户：10K
• 付费用户：1K
• MRR（月经常性收入）：$29K

✅ 商业价值明确

📋 建议
核心功能（MVP）：
1. 自动代码审查
2. 安全问题检测
3. AI 驱动的修复建议
4. GitHub 集成

开发优先级：
1. 专注于自动化修复（差异化）
2. 优先个人开发者（获客）
3. 简化配置（易用性）

🎉 结论
✅ 值得做！
这是一个有巨大市场机会的项目，建议：
1. 快速构建 MVP（3-4 周）
2. 发布免费版吸引用户
3. 基于反馈快速迭代
```

---

### 5. `/investigate` - 调试

**功能**：智能定位问题根因

**使用方式**：

```
/investigate 登录功能有问题
```

或详细描述：

```
/investigate
问题：用户登录时经常失败
错误信息：500 Internal Server Error
发生频率：约 30% 的登录请求
影响：严重
```

**执行内容**：

1. 分析问题症状
2. 检查日志文件
3. 追踪调用链
4. 定位根本原因
5. 提供修复方案
6. 验证修复效果

**输出示例**：

```
🔍 问题调查

问题描述：登录功能间歇性失败
错误：500 Internal Server Error
频率：约 30% 的登录请求
影响：严重

🔬 症状分析
观察到的行为：
• 错误仅在高峰期出现
• 错误发生在数据库查询阶段
• 重试有时能成功

时间模式：
• 错误高峰：工作日 10:00-11:00, 15:00-16:00
• 错误低谷：夜间和周末
• 持续时间：5-10 分钟/次

✅ 症状模式明显

📋 日志分析
错误日志：
```
[ERROR] Database connection failed: Connection pool exhausted
[ERROR] Timeout while waiting for database connection
[ERROR] Retry attempt 3 failed
```

日志统计：
• 错误频率：平均 45 次/小时
• 错误类型：数据库连接问题 100%
• 错误分布：均匀分布在不同用户

关联日志：
• 请求量增加：同时期请求量增加 3x
• 查询时间：平均查询时间从 20ms 增加到 500ms
• 连接数：同时连接数从 10 增加到 50

✅ 日志清晰指向数据库问题

🔗 调用追踪
调用链：
```
Login Request
  → AuthController.login()
    → UserService.authenticate()
      → Database.query()
        → ConnectionPool.getConnection() ❌
```

性能分析：
• AuthController.login()：正常
• UserService.authenticate()：正常
• Database.query()：正常
• ConnectionPool.getConnection()：超时 ❌

瓶颈定位：
• 数据库连接池：是瓶颈
• 连接等待时间：最长 5 秒
• 连接池大小：10 个连接

✅ 调用链清晰

🎯 根因确认
根本原因：
数据库连接池耗尽

触发因素：
1. 高峰期并发请求增加（3x）
2. 连接池大小不足（10 个连接）
3. 部分查询执行时间过长（25x）
4. 缺少连接超时和重试机制

根本原因优先级：
1. 连接池大小不足：主要原因
2. 查询性能问题：次要原因
3. 缺少超时机制：加剧问题

✅ 根因明确

🔧 修复方案
方案 1：增加连接池大小（推荐）
```
# 配置
pool:
  min: 10
  max: 50  # 从 10 增加到 50
  idle_timeout: 30000
```
优点：简单、快速、有效
缺点：增加内存消耗
效果：预期解决 90% 的问题

方案 2：优化查询性能
```
-- 添加索引
CREATE INDEX idx_users_email ON users(email);

-- 优化查询
SELECT * FROM users WHERE email = $1
```
优点：提高整体性能
缺点：需要时间分析
效果：减少查询时间 80%

方案 3：添加超时和重试机制
```
// 配置
connection:
  timeout: 5000  // 5 秒超时
  retry: {
    attempts: 3,
    delay: 1000
  }
```
优点：提高稳定性
缺点：增加复杂度
效果：减少错误感知

综合方案：同时应用方案 1、2、3

✅ 修复方案完整

🚀 实施修复
已应用的修复：
1. ✅ 连接池大小：10 → 50
2. ✅ 添加索引：idx_users_email
3. ✅ 配置超时：5 秒
4. ✅ 配置重试：3 次

修复验证：
✅ 100 次并发测试：全部成功
✅ 查询时间：从 500ms 降至 30ms
✅ 连接等待：从 5 秒降至 50ms

监控配置：
✅ 添加连接池监控
✅ 添加慢查询告警
✅ 添加错误率监控

状态：✅ 问题已解决
建议：
• 持续监控连接池使用率
• 定期审查慢查询
• 考虑实施连接池动态调整
```

---

## 高级用法

### 链式命令

你可以将多个命令链式执行：

```
/review && /qa && /ship
```

或自然语言：

```
审查、测试并部署我的代码
```

AI 会自动：
1. 先执行 `/review`
2. 然后执行 `/qa`
3. 最后执行 `/ship`

如果任何一步失败，流程会停止并提示你。

---

### 条件执行

根据前一步的结果决定下一步：

```
/review
```

如果审查通过：
```
好的，现在测试
```

如果审查发现问题：
```
先修复这些问题
```

AI 会理解上下文并智能响应。

---

### 批量操作

对多个文件或目录操作：

```
/review src/api/
```

或：

```
/review --files=src/auth.js,src/user.js
```

---

### 自定义配置

创建 `.gstack.config.json` 文件：

```json
{
  "review": {
    "strict": true,
    "autoFix": true,
    "format": "verbose"
  },
  "qa": {
    "coverageThreshold": 80,
    "timeout": 60000
  },
  "ship": {
    "skipTests": false,
    "dryRun": false
  }
}
```

---

## 最佳实践

### 1. 持续集成

在 CI/CD 流程中集成 gstack-skills：

```yaml
# GitHub Actions 示例
name: CI

on: [push, pull_request]

jobs:
  review-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '18'
      - name: Install dependencies
        run: npm ci
      - name: Run review
        run: echo "/review" | openclaw
      - name: Run qa
        run: echo "/qa" | openclaw
```

---

### 2. 团队工作流

推荐的团队开发流程：

1. **开发前**
   ```
   /office-hours 描述功能需求
   /plan-eng-review 功能架构设计
   ```

2. **开发中**
   ```
   /review 定期审查
   ```

3. **开发后**
   ```
   /qa 全面测试
   /ship 部署
   ```

---

### 3. 代码质量标准

在团队中建立统一标准：

```json
{
  "standards": {
    "review": {
      "blockingIssues": ["security", "critical"],
      "autoFix": true
    },
    "qa": {
      "minimumCoverage": 80,
      "allTestsRequired": true
    },
    "ship": {
      "noWarnings": false,
      "noCriticalIssues": true
    }
  }
}
```

---

### 4. 文档同步

确保代码和文档同步：

```
/document-release
```

这个技能会：
- 检查代码变更
- 更新相关文档
- 同步 CHANGELOG
- 生成发布说明

---

## 故障排除

### 问题 1：技能未加载

**症状**：输入 `/review` 没有响应

**解决方案**：

1. 检查技能是否正确安装
   ```bash
   ls ~/.openclaw/skills/gstack-skills
   ```

2. 重启 OpenClaw/WorkBuddy

3. 查看日志：
   ```bash
   tail -f ~/.openclaw/logs/openclaw.log
   ```

---

### 问题 2：测试失败

**症状**：`/qa` 报告测试失败

**解决方案**：

1. 查看详细错误信息
   ```
   /qa --verbose
   ```

2. 手动运行失败测试：
   ```bash
   npm test -- --grep="test_name"
   ```

3. 检查测试环境配置

---

### 问题 3：部署失败

**症状**：`/ship` 报告部署失败

**解决方案**：

1. 检查网络连接
2. 验证 CI/CD 配置
3. 查看部署日志
4. 尝试 `--dry-run` 诊断

---

### 问题 4：性能问题

**症状**：技能执行很慢

**解决方案**：

1. 使用缓存
2. 限制分析范围
3. 更新依赖
4. 检查系统资源

---

## 常见问题

### Q: 可以自定义技能吗？

**A**: 可以！你可以：
- 修改现有技能
- 创建新技能
- 配置自定义选项

详见 [CONTRIBUTING.md](CONTRIBUTING.md)

---

### Q: 支持哪些语言？

**A**: GStack-Skills 语言无关，支持：
- Python, JavaScript, TypeScript
- Java, C++, Go, Rust
- Ruby, PHP, Swift
- 以及任何其他语言

---

### Q: 会修改我的代码吗？

**A**: 默认情况下：
- `/review` 和 `/qa` 会**建议**修复
- 不会自动修改代码
- 你可以查看后再决定

可以配置自动修复选项。

---

### Q: 安全吗？

**A**: 是的，GStack-Skills：
- ✅ 不会上传代码到外部服务器
- ✅ 所有操作在本地进行
- ✅ 开源代码，可审查
- ✅ 符合安全最佳实践

---

### Q: 如何获得帮助？

**A**:
- 查看 [CONVERSATION_GUIDE.md](CONVERSATION_GUIDE.md)
- 查看 [EXAMPLES.md](EXAMPLES.md)
- 提交 Issue：https://github.com/AICreator-Wind/gstack-openclaw-skills/issues
- 加入社区讨论

---

## 进阶资源

- [快速开始](QUICKSTART.md) - 5 分钟快速上手
- [对话指南](CONVERSATION_GUIDE.md) - 完整对话示例
- [使用示例](EXAMPLES.md) - 真实案例
- [安装指南](INSTALL.md) - 安装方法详解
- [贡献指南](CONTRIBUTING.md) - 如何贡献代码

---

## 支持

- 📧 邮件：support@openclaw.dev
- 🐛 问题报告：https://github.com/AICreator-Wind/gstack-openclaw-skills/issues
- 💬 讨论：https://github.com/AICreator-Wind/gstack-openclaw-skills/discussions

---

<div align="center">

**让 AI 为你工作，而不是反过来。**

[返回主页](README.zh-CN.md)

</div>
