# hekouwang-claude-md-doctor-skill

**简体中文** · [English](README.en.md)

[![CI](https://github.com/huiyonghkw/hekouwang-claude-md-doctor-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/huiyonghkw/hekouwang-claude-md-doctor-skill/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)
![open source](https://img.shields.io/badge/open%20source-free-success.svg)

> **会勇禾口王的AI笔记** 出品 · `@huiyonghkw`
> _不聊 AI 会不会取代你，只聊先用 AI 的人怎么取代你。_

CLAUDE.md 体检器 —— 检查任意项目的 `CLAUDE.md` 是否符合"把它当**运行时配置**、
不是项目说明书"的最佳实践，给出评分卡 + 修复建议。

<p align="center">
  <img src="examples/demo.gif" width="720" alt="hekouwang-claude-md-doctor-skill 体检演示">
  <br><sub>↑ 一句「检查我的 CLAUDE.md」/ <code>python3 check.py</code>，秒出评分 + 修复建议（免费 CLI）</sub>
</p>

一句话判据：**CLAUDE.md 每次会话都被重新加载、要付上下文费。值不值得每次会话都为这段内容付一次费？**

<p align="center">
  <img src="examples/report-card.gif" width="420" alt="CLAUDE.md 体检报告卡（动效示例）">
  <br><sub>↑ 品牌可视化报告卡（<b>付费增值</b>示例）——评分弧随分数填充、等级 D→A 变色。免费版输出文本/JSON 报告。</sub>
</p>

## 为什么需要它

很多人把 CLAUDE.md 写成"项目说明书"：塞进历史、技术决策、营销叙事，动辄上千行。
结果模型在冗长上下文里迷失，还挤掉了真正理解代码的空间。这个工具把 10 条可检查的
最佳实践固化下来，让任何人一键体检自己的项目。

核心立场是 Claude Code 之父 Boris Cherny / Cat Wu 的 **context minimalism —— 别跟模型较劲做加法**：
模型每代都在变强，你今天费劲搭的脚手架很快白搭。所以评分按"减法优先"加权，
"越短越准"类核心项权重更高，"加内容"类项缺了不重罚。

## 10 项检查

1. 篇幅 ≤ 200 行（路由器不是图书馆）
2. 禁止清单（Do NOT introduce）
3. 规则可操作（非"写干净代码"式空话）
4. 路由器不是图书馆（大块下沉 docs/ 留指针）
5. 高危模块有本地 CLAUDE.md（碰钱/认证/迁移）
6. 关键规则有 Hook 强制（不靠模型记忆）
7. 跨会话记忆回路（MEMORY.md）
8. 工作风格块（你是谁 / 你讨厌什么 · 限 3–5 行）
9. 30 秒三问（产品 / 技术栈 / 新代码放哪）
10. 别替模型补它已经会的（无"如何使用 X / 教程"式随模型升级即过时的冗余）

## 用法

### 在 Claude Code 里（推荐）
直接说：「**检查我的 CLAUDE.md**」「**CLAUDE.md 体检**」——会自动跑机检 +
模型定性复核，给出评分和按优先级的修复建议，并可代为修复。

### 命令行直接跑（零依赖，仅需 Python 3）
```bash
python3 check.py [项目目录]          # 默认当前目录，输出彩色报告
python3 check.py [项目目录] --json   # 机器可读 JSON（CI 可用）
```
退出码：有 FAIL → 1，否则 0（可用于 CI 卡关）。

### Docker（不想装 Python 也能跑）
```bash
# 拉官方镜像直接用（打 tag 时 GitHub Actions 自动发布到 GHCR）
docker run --rm -v "$PWD:/work" ghcr.io/huiyonghkw/hekouwang-claude-md-doctor-skill

# 或本地自建
docker build -t claude-md-doctor .
docker run --rm -v "$PWD:/work" claude-md-doctor            # 体检当前项目
docker run --rm -v "$PWD:/work" claude-md-doctor /work --json
```

### 接进 CI 卡关（GitHub Actions 示例）
```yaml
- uses: actions/setup-python@v5
  with: { python-version: "3.x" }
- name: CLAUDE.md 体检（不合格则拦 PR）
  run: |
    curl -sO https://raw.githubusercontent.com/huiyonghkw/hekouwang-claude-md-doctor-skill/main/check.py
    python3 check.py .
```
本仓库自身的 CI 见 [`.github/workflows/ci.yml`](.github/workflows/ci.yml)（语法 + good/bad 夹具 + JSON 合法性）。

## 免费 / 付费（Freemium）

- **免费（开源内核）**：命令行体检器 `check.py` —— 文本 / JSON 报告、评分、退出码。
  本地或 Docker 随便跑、随便接进 CI。这是开放内核，永久免费。
- **付费（增值服务）**：**品牌可视化体检报告卡** —— 评分弧 + 等级带 + 九项明细的
  精美分享图（适合汇报 / 发圈 / 放进 PR）。它依赖私有视觉系统（品牌字体与版式，
  即私有 Skill `hekouwang-content-factory`，**GitHub 上为 PRIVATE 仓库，非授权无法 clone / 获取**），
  **不随本仓库分发**。需要出图版报告，请联系 **@huiyonghkw** 获取。

> 一句话：**跑检查免费，出「好看的报告图」找我。**

## 设计

- **机检层（`check.py`）**：确定性、零依赖、可移植，跑启发式检查并打分。
- **定性层（`SKILL.md`）**：模型读正文复核机检盲区（图书馆 vs 路由器、规则是否可执行），
  再出最终报告与修复方案。
- **安全**：绝不读取 `.env` / `*.key` / `*.pem` 等密钥文件；体检只读，改动需确认。

## 评分档位

A 优秀 ≥85 · B 良好 ≥70 · C 及格 ≥50 · D 建议重写 <50

## 许可协议 / License

本仓库代码以 **MIT License** 开源 —— 免费使用、修改、分发、商用，仅需保留版权与许可声明。详见 [LICENSE](LICENSE)。

> 范围说明：MIT 覆盖本仓库代码（`check.py` / `SKILL.md` 等）。品牌名「会勇禾口王的AI笔记」与**付费可视化报告卡**（依赖未公开的品牌字体与版式）属增值服务，不在开源范围内——但这不影响你免费、自由地使用命令行体检器。

## 贡献 / Contributing

欢迎提 Issue / PR：新增检查项、降低误报、补充其它语言/框架的启发式规则。
保持零运行时依赖（仅 Python 3 标准库）是硬约束。

---

<sub>—— 会勇禾口王的AI笔记 · @huiyonghkw · AI 实战拆解：编程 × 内容创作 × 自动化（硬核 · 具体 · 可复制）</sub>
