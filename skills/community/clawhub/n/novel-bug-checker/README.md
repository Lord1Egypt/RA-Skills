# 🔍 novel-bug-checker

> **Publication-Grade Novel Quality Inspector · AI-Powered Narrative Bug Detection Tool**
>
> Professional-grade narrative quality audit tool for Chinese novels. Detects logic flaws, character inconsistencies, pacing issues, and narrative bugs with graded reports and repair suggestions.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
    <img src="assets/banner-light.svg" alt="novel-bug-checker banner" width="800">
  </picture>
</p>

<p align="center">
  <a href="README_EN.md">English</a> · <a href="README.md">中文</a>
</p>

<p align="center">
  <a href="https://clawhub.ai/USER/skills/novel-bug-checker"><img src="https://img.shields.io/badge/ClawHub-v1.0.0-7b2ff7?style=flat-square" alt="ClawHub"></a>
  <a href="https://github.com/USER/novel-bug-checker"><img src="https://img.shields.io/badge/GitHub-open-2ea44f?style=flat-square" alt="GitHub"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="MIT"></a>
</p>

---

## 🌟 为什么选择 novel-bug-checker？

| 维度 | 手动检查 | **novel-bug-checker** |
|------|---------|----------------------|
| 🎯 检测范围 | 依赖个人经验，容易遗漏 | **系统化扫描**：逻辑/角色/节奏/伏笔 全维度 |
| 📊 报告体系 | 口头反馈，难以量化 | **分级报告**：🔴致命/🟠严重/🟡中等/🟢轻微 |
| 🔧 修复方案 | 需要自行思考 | **策略库驱动**：每个 Bug 至少 3 种修复方案 |
| 🧠 理论支撑 | 凭直觉判断 | **叙事学理论**：时间线/因果链/角色弧线/信息密度 |
| 📝 辅助脚本 | 无 | **3 个 Python 脚本**：逻辑分析/节奏分析/一致性检查 |
| 🔄 可验证 | 无法复检 | **修复验证**：提供修改后自动重检确认修复效果 |

---

## ✨ 核心特性

### 🕵️ 逻辑漏洞检测
- **时间线矛盾**：事件顺序、时间计算、因果时序
- **因果断裂**：关键转折缺少前置条件、结果无原因支撑
- **能力突变**：未设定的能力突然出现、力量体系不一致
- **信息知晓不合理**：角色知道不应该知道的信息

### 👤 角色一致性检查
- **性格突变**：无动机的行为变化
- **动机矛盾**：目标与行动不一致
- **对话风格偏移**：语言特征与角色背景不符
- **成长弧线断裂**：角色发展缺少必要经历支撑

### 📈 节奏结构分析
- **信息密度**：评估分布，识别过载/稀疏段落
- **高潮铺垫**：检查高潮前的紧张感积累是否充分
- **场景过渡**：评估切换是否自然
- **伏笔管理**：追踪埋设与回收情况

### 🔄 修复验证
提供修改版本后自动重检，对比前后报告，标注已修复和新增问题。

---

## 📖 如何使用

### 安装技能

```bash
# OpenClaw 用户
openclaw skills install novel-bug-checker

# 或通过 ClawHub CLI
clawhub install novel-bug-checker
```

### 安装依赖

```bash
pip install jieba
```

> 仅依赖 `jieba`（中文分词），轻量无需重型 NLP 库。

### 开始检查

告诉 AI：**「帮我检查这段小说的逻辑漏洞」** 或直接粘贴小说章节内容。

AI 将自动执行：
1. 读取文本 → 2. 逻辑分析 → 3. 角色一致性检查 → 4. 节奏分析 → 5. 生成分级报告

### 命令行模式（可选）

```bash
# 逻辑分析
python scripts/logic-analyzer.py novel.txt -o report.txt

# 节奏分析
python scripts/rhythm-analyzer.py novel.txt -g 玄幻

# 角色一致性检查
python scripts/consistency-checker.py novel.txt -o report.txt
```

---

## 🏗️ 项目结构

```
novel-bug-checker/
├── SKILL.md                          # 技能主文件
├── README.md                         # 本文件（中文）
├── assets/                           # 资源目录
│   ├── banner-light.svg              # 浅色 Banner
│   └── banner-dark.svg               # 深色 Banner
├── references/                       # 参考资料
│   ├── bug-patterns.md               # 常见 Bug 模式分类
│   ├── character-consistency.md      # 角色一致性检查指南
│   ├── narrative-theory.md           # 叙事学理论基础
│   └── repair-strategies.md          # 修复策略库
├── scripts/                          # 分析脚本
│   ├── logic-analyzer.py             # 逻辑漏洞分析
│   ├── rhythm-analyzer.py            # 节奏分析
│   └── consistency-checker.py        # 角色一致性检查
├── templates/                        # 输出模板
│   ├── bug-report.txt                # Bug 报告模板
│   ├── repair-suggestions.txt        # 修复建议模板
│   └── summary-report.txt            # 总结报告模板
└── example.md                        # 使用示例
```

---

## 🎯 适用场景

- ✅ **长篇网络小说**：玄幻/都市/悬疑 — 大型故事架构的全面审查
- ✅ **出版级文学小说**：确保叙事质量达到专业标准
- ✅ **连载作品**：章节发布前的质量控制
- ✅ **完本修订**：最终出版前的通盘 Bug 排查
- ✅ **写作教学**：案例驱动的叙事问题分析与修复教学

---

## 🤝 贡献

Issues 和 PR 欢迎提交！  
本项目遵循 [MIT 许可证](LICENSE)，可自由使用、修改和分发。

---

## 📦 技术栈

- **运行环境**：OpenClaw AI Agent + Python 3
- **核心依赖**：jieba（中文分词）
- **格式**：Markdown + Python + TXT
- **许可证**：MIT

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/USER">USER</a><br>
  <sub>为每一部认真写作的小说的质量护航</sub>
</p>
