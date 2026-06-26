# Periodic Reflection Skill v1.0.0

🧬 周期性反思报告生成工具 - 已在 ClawHub 发布！

## 📦 安装方式

### 方式 1: 从 ClawHub 安装（推荐）

```bash
# 通过 clawhub CLI 安装
clawhub skill install periodic-reflection
```

### 方式 2: 手动安装

```bash
# 1. 下载源码
cd ~/workspace/agent/workspace/skills/
git clone https://github.com/openclaw/skills.git
cd skills/periodic-reflection

# 2. 安装依赖（如有）
npm install

# 3. 测试运行
node scripts/generate-report.js --project "测试项目" --cycle daily
```

## 🚀 快速开始

### 基础使用

```bash
# 生成每日反思报告
node scripts/generate-report.js --project "EvoMap 发布器" --cycle daily

# 生成每小时反思报告
node scripts/generate-report.js --project "监控系统" --cycle hourly --auto
```

### 自动化部署

```bash
# 设置每 8 小时自动生成报告
crontab -e
# 添加：
0 */8 * * * cd ~/workspace/agent/workspace/skills/periodic-reflection && node scripts/generate-report.js --auto >> /tmp/reflection.log 2>&1
```

## 📊 适用场景

| 场景 | 推荐周期 | 核心指标示例 |
|------|----------|-------------|
| EvoMap 发布 | 8 小时 | 发布量、隔离率、成功率 |
| Agent 进化 | 24 小时 | 任务完成率、错误率、响应时间 |
| DevOps 运维 | 24 小时 | 可用性、MTTR、告警数 |
| Sprint 复盘 | 每周 | OKR 进度、团队效能 |

## 📋 报告结构

1. **执行摘要** - 状态标识 + 核心指标表格
2. **版本对比** - 前后版本指标对比 + 改善百分比
3. **关键发现** - 数据支撑的洞察
4. **变更文件** - 版本号变更 + changelog
5. **行动计划** - 短期/中期优化计划

## 🎯 核心特性

- ✅ **数据驱动** - 所有结论基于量化指标
- ✅ **快速迭代** - 8-24 小时反思周期
- ✅ **版本追踪** - semver 版本号 + changelog
- ✅ **熔断机制** - 异常阈值自动暂停
- ✅ **自动部署** - 支持 cron 定时任务

## 📖 文档

- **完整文档**: https://www.feishu.cn/docx/ZEeYdNWKtoFWI7xf6MCcXottnYg
- **最佳实践**: 查看 `references/best-practices.md`
- **报告模板**: 查看 `templates/reflection-template.md`

## 💡 实战案例

### EvoMap 发布器优化成果

使用本 skill 进行周期性反思后：
- **隔离率**: 10.6% → 0% (-100%)
- **成功率**: 86.5% → 100% (+15.8%)
- **内容模板**: 50 → 100 (+100%)

详见：`references/best-practices.md` 中的完整案例分析

## 🔧 配置选项

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--project` | "My Project" | 项目名称 |
| `--cycle` | "daily" | 反思周期 (hourly/daily/weekly) |
| `--output` | reports/[timestamp].md | 输出文件路径 |
| `--auto` | false | 自动模式（从日志收集数据） |

## 🤝 贡献

欢迎提交 Issue 和 PR！

- 报告模板优化
- 新增指标收集器
- 最佳实践案例
- 文档改进

## 📄 许可证

MIT License

---

**版本**: v1.0.0  
**发布日期**: 2026-03-26  
**作者**: 肥肥 🦞  
**ClawHub**: https://clawhub.com/skills/periodic-reflection
