---
name: github-repo-evaluator
description: "GitHub 项目调研与对比工具。当用户要求'搜索 GitHub 项目'、'对比开源项目'、'选一个 XX 工具'、'哪个项目最受欢迎/活跃'、'评估哪个好'、'怎么选'等场景时使用。通过 GitHub API 搜索、采集数据、系统化对比，输出结构化推荐报告。"
version: 1.0.0
---

# GitHub 项目调研与对比 Skill

## 何时激活

当用户提出以下类型需求时，激活本 skill：
- "搜一下 GitHub 上 XX 相关的项目"
- "对比一下这几个项目"（提供具体仓库名）
- "哪个项目最受欢迎？"
- "帮我选一个 XX 工具"
- "这个项目怎么样？"
- "评估一下 XX 项目"
- "查一下 XX 项目的活跃度"
- "哪些项目在维护？"

---

## 核心方法论：六维评估法

每个项目从以下六个维度评估，最终输出对比表和推荐：

| 维度 | 权重 | 说明 |
|------|------|------|
| ⭐ Stars | 20% | 社区认可度，越大越成熟 |
| 🕐 最近更新 | 25% | 最后一次 commit 时间，越近越活跃 |
| 🐛 Issues | 15% | open issues 数量（太多说明不稳定） |
| 📖 功能完整性 | 25% | README 中功能列表的覆盖度 |
| 🔮 未来规划 | 15% | 有无 roadmap、changelog、release 说明 |
| 🏗️ 技术栈 | 加分项 | 技术栈是否现代、文档是否完整 |

---

## 执行流程

### Step 1：初步搜索

```bash
# 基础搜索，按 stars 排序
curl -s "https://api.github.com/search/repositories?q=关键词&sort=stars&order=desc&per_page=15"

# 如果有多个相关关键词，用 + 连接
curl -s "https://api.github.com/search/repositories?q=openclaw+ui&sort=stars&order=desc"

# 也可用 GitHub CLI
gh search repos "openclaw dashboard" --sort=stars --limit 15
```

**输出字段**：`full_name`, `description`, `stargazers_count`, `language`, `open_issues_count`, `pushed_at`, `updated_at`

### Step 2：基本信息采集

对候选项目逐个执行：

```bash
# 单项目基础信息
curl -s "https://api.github.com/repos/owner/repo"

# 最后一次 commit（判断活跃度）
curl -s "https://api.github.com/repos/owner/repo/commits?per_page=1"

# 最近 3 个 release
curl -s "https://api.github.com/repos/owner/repo/releases?per_page=3"

# 最近 5 个 open issues（用于判断维护状态）
curl -s "https://api.github.com/repos/owner/repo/issues?state=open&sort=created&per_page=5"
```

### Step 3：README 深度解析

```bash
# 获取 README 内容
curl -s "https://api.github.com/repos/owner/repo/readme" | python3 -c "
import sys,json,base64
d=json.load(sys.stdin)
print(base64.b64decode(d['content']).decode('utf-8'))
"
```

**解析要点：**
- 核心特性列表（Features）
- 快速开始指南（Quick Start）
- 技术栈说明
- 部署方式（Docker / 源码 / npm）
- 有无 Roadmap 或 CHANGELOG

### Step 4：四维对比表

构建对比表：

```
| 维度     | 项目A              | 项目B              | 项目C              |
|----------|--------------------|--------------------|--------------------|
| Stars    | 100+               | 1000+              | 500+               |
| 最后更新  | 近30天内            | 近7天内             | 近30天内            |
| 语言     | TypeScript/Node    | TypeScript/Node    | TypeScript/Node    |
| Issues   | <50                | <200               | <100               |
| 部署方式 | Docker/npm         | App/Docker         | Docker             |
| 核心功能 | 监控/安全           | 全功能工作台        | 沙箱/协作          |
```

> 📌 上表为通用模板骨架，实际对比时替换为真实数据。

### Step 5：需求匹配

根据用户**明确表达的需求**和**隐含需求**，做功能匹配：

```
用户需求 → 必须有 → 最好有 → 加分项
```

**示例：** 用户说要"管理 agent"，"不用命令行"，"易扩展"
- 必须有：Agent CRUD、UI 管理界面
- 最好有：Cron 管理、Skills 管理
- 加分项：多渠道支持、远程桌面

### Step 6：结构化输出

最终输出包含：

1. **一句话定位** — 每个项目是做什么的
2. **四维对比表** — 基础数据并列
3. **详细分析** — 每个项目的优缺点
4. **推荐结论** — 针对用户需求的最优选择
5. **备选方案** — 其他值得考虑的选择

---

## 常见场景的快速判断

### 场景：选一个 XX 工具

**优先级顺序：**
1. Stars 数 > 1000 → 成熟度高
2. 最后 commit < 1个月 → 还在维护
3. Issues < 100 → 相对稳定

**快速筛选公式：**
```bash
# 查看 stars > 100 且 最后更新 < 30天 的项目
curl -s "https://api.github.com/search/repositories?q=关键词+stars:>100&sort=updated&order=desc" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); [print(f\"{r['full_name']} | {r['stargazers_count']}⭐ | {r['pushed_at'][:10]}\") for r in d['items'][:10]]"
```

### 场景：对比 A 和 B 两个项目

直接抓两个项目的关键数据并列对比，重点看：
- 功能差异
- 最后更新时间
- Issues 处理速度（看 open vs closed 比例）
- 文档完整性

### 场景：评估某个项目能不能用

**必查项：**
1. 最后 commit 时间（> 3个月 → 谨慎）
2. Open issues 数（> 500 → 可能有遗留 bug）
3. 有无 CI/CD（.github/workflows）
4. README 是否详细
5. 有无 CHANGELOG 或版本发布记录

---

## 输出模板

```markdown
# 📊 GitHub 项目调研报告

## 调研背景
用户需求：{用户说的话}

## 候选项目概览
| 项目 | ⭐ Stars | 🕐 最近更新 | 🐛 Issues | 语言 |
|------|----------|-------------|-----------|------|
| ... | ... | ... | ... | ... |

## 深度对比

### 1. [项目名]
**定位：** 一句话描述
**优点：** 
**缺点：**
**适合场景：**

### 2. [项目名]
...

## 推荐结论

🥇 **最佳选择：项目名**
原因：针对用户需求的第一选择

🥈 **备选：项目名**
原因：适合 XX 场景

❌ **不推荐：项目名**
原因：维护状态不佳 / 功能不符合需求

---

## 下一步建议
- 如需安装，提供安装步骤
- 如需进一步调研，指出需要确认的问题
```

---

## 注意事项

1. **所有数据实时从 GitHub API 获取**，不要只凭记忆
2. **Stars 数量只是参考**，很多优质项目 Stars 不高但很实用
3. **最后更新时间是最重要的指标**，Stars 高但停更的项目不值得选
4. **结合用户实际场景**，功能再强但不适合用户场景的不推荐
5. **主动提出备选方案**，不要只给一个选项
6. **明确说明缺点**，让用户做知情决策
7. **遇到 403 rate limit 时**，换用 `gh api` 或等待
