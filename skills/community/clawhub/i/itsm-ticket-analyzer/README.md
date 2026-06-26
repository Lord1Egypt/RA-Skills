# ITSM 工单分析技能

嘉为蓝鲸 ITSM 工单数据分析技能，支持工单分析、响应时间统计、问题分类、日报/周报生成。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)

---

## 🎯 功能特性

### 核心功能

- **📊 处理人工作量统计**
  - 处理人分布（工单数/占比）
  - 每个处理人的工单详情
  - 工作量对比分析

- **⏱️ 响应时间分析**
  - 已解决工单：平均响应时间、最快/最慢
  - 未解决工单：平均等待时间、最长等待
  - Top 5 最慢/最久工单列表

- **📂 问题分类统计**
  - 自动关键词分类（8 类）
  - 分类占比统计
  - 典型案例展示
  - 重复问题识别

- **💡 关键发现与建议**
  - 自动识别紧急问题（🔴）
  - 生成改进建议（🟡）
  - 风险预警

- **📝 日报/周报模板**
  - 标准日报格式
  - 标准周报格式
  - 可自定义

---

## 🚀 快速开始

### 安装

**方式 1：克隆仓库**
```bash
git clone https://github.com/<your-username>/openclaw-itsm-skill.git
cp -r openclaw-itsm-skill ~/.openclaw/workspace/skills/itsm-ticket-analyzer
```

**方式 2：手动下载**
1. 下载本仓库
2. 复制 `itsm-ticket-analyzer` 文件夹到 `~/.openclaw/workspace/skills/`
3. 重启 OpenClaw 或刷新技能

### 使用

**直接对 OpenClaw 说：**

```
分析工单文件：bk_itsm_20260311102252.xlsx
```

**或使用脚本：**

```bash
# 深度分析报告
python scripts/deep_analysis.py \
  --input /path/to/tickets.xlsx \
  --output report.md

# 单工单分析
python scripts/analyze_ticket.py \
  --input /path/to/new_ticket.csv

# 趋势分析
python scripts/trend_analysis.py \
  --input /path/to/tickets.csv \
  --period weekly
```

---

## 📊 分析维度

### 1. 处理人工作量

| 处理人 | 工单数 | 占比 |
|--------|--------|------|
| 未分配 | 11 | 57.9% |
| ryqhcf | 7 | 36.8% |

### 2. 响应时间

- **已解决工单**：平均 721.4 小时 (30.1 天)
- **未解决工单**：平均等待 182.1 天
- **最长等待**：352 天

### 3. 问题分类

| 分类 | 数量 | 占比 |
|------|------|------|
| 监控告警 | 4 | 21.1% |
| 数据问题 | 4 | 21.1% |
| 登录问题 | 3 | 15.8% |
| 服务宕机 | 3 | 15.8% |

---

## 📁 项目结构

```
itsm-ticket-analyzer/
├── SKILL.md                    # 技能说明（核心）
├── README.md                   # 本文档
├── LICENSE                     # MIT 许可证
├── scripts/
│   ├── analyze_ticket.py       # 单工单分析
│   ├── trend_analysis.py       # 趋势分析
│   └── deep_analysis.py        # 深度分析
└── references/                 # 参考资料目录
```

---

## 🔧 依赖

- Python 3.x
- pandas
- openpyxl

安装依赖：
```bash
pip install pandas openpyxl
```

---

## 📝 输出示例

### 深度分析报告

```markdown
## 📈 处理人工作量统计

| 处理人 | 工单数 | 占比 |
|--------|--------|------|
| 未分配 | 11 | 57.9% |
| ryqhcf | 7 | 36.8% |

## ⏱️ 响应时间分析

**已解决工单（11 个）:**
- 平均响应时间：721.4 小时 (30.1 天)
- 最快：0.0 小时
- 最慢：6235.6 小时

## 💡 关键发现与建议

**🔴 紧急**: 57.9% 工单未分配 — 需建立自动分配机制
**🔴 紧急**: 平均响应时间 30.1 天 — 严重超时
**🟡 关注**: 监控告警 类问题 4 个 — 建议专项优化
```

---

## 🎯 适用场景

- ✅ 嘉为蓝鲸 ITSM 用户
- ✅ 需要分析工单数据
- ✅ 生成工单日报/周报
- ✅ 识别高频问题
- ✅ 监控 SLA 响应时间

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## 🔗 相关链接

- **OpenClaw**: https://openclaw.ai
- **ClawHub**: https://clawhub.com
- **GitHub**: https://github.com/openclaw/openclaw
- **Discord**: https://discord.com/invite/clawd

---

## 📞 支持

如有问题，请：
1. 查看本 README
2. 提交 Issue
3. 加入 OpenClaw Discord 社区

---

_由 城哥 开发 | 大龙虾 🦞 协助_
