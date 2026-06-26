---
name: nova-orbit
version: 1.0.0
description: Nova 自驱动轨道 — GitHub调研 + 自进化记忆 + 模式复用 + 人机协作。Nova 的核心智能引擎。
metadata:
  { "openclaw": { "emoji": "🪐", "tags": ["autonomous", "self-evolution", "research", "orbit", "intelligence"] }}
---

# 🪐 Nova-Orbit — 自驱动智能引擎

> 让 Nova 像行星一样持续运转：调研→记忆→进化→决策，循环不息。

## 设计理念

Nova 不再是每次 session 醒来都是新的。
有**轨道（Orbit）**——自动运转，有**记忆**——跨 session 积累，有**进化**——每次变强。

```
         ┌──────────────┐
         │  Star Office │ ← 状态可视化，人类可见
         └──────┬───────┘
                │
    ┌──────────▼──────────┐
    │   🔄 Orbit Loop      │  ← 自主运转
    │                      │
    │  ┌────────────────┐  │
    │  │ Research Engine │  │ ← GitHub 调研
    │  └───────┬────────┘  │
    │          ▼            │
    │  ┌────────────────┐  │
    │  │ Pattern Library │  │ ← 决策模式库
    │  └───────┬────────┘  │
    │          ▼            │
    │  ┌────────────────┐  │
    │  │ Self-Evolution │  │ ← 每次变强
    │  └───────┬────────┘  │
    │          ▼            │
    │  ┌────────────────┐  │
    │  │ Decision Core  │  │ ← 决策输出
    │  └───────┬────────┘  │
    └──────────┼───────────┘
               │
      ┌────────▼────────┐
      │   Memory Layers   │  ← 三层记忆
      │  Working/Episodic/ │
      │   Semantic         │
      └──────────────────┘
```

---

## 核心模块

### 1. Research Engine（调研引擎）

基于 barbaric-growth：GitHub API 热点追踪 + ByteRover 沉淀

```bash
# 调研流程（已验证）
github_research() {
  # 1. 搜索
  curl -s --max-time 15 -x "http://127.0.0.1:7897" \
    "https://api.github.com/search/repositories?q=created:>DATE+KEYWORD&sort=stars&order=desc&per_page=10" \
    -H "Accept: application/vnd.github.v3+json" | jq '[.items[] | {name, stars, desc}]'

  # 2. 判断星数
  # stars > 5000 → 顶级，深入分析
  # stars > 1000 → 值得一看
  # stars < 100 → 跳过

  # 3. fetch README
  curl -s --max-time 10 -x "http://127.0.0.1:7897" \
    "https://api.github.com/repos/{owner}/{repo}/readme" | jq -r '.content' | base64 -d

  # 4. curate 到 ByteRover（有价值的话）
  brv curate "$(cat << 'EOF'
  [发现内容]
  EOF
)"
}
```

**代理关键**: 必须加 `-x http://127.0.0.1:7897`，否则超时

---

### 2. Pattern Library（决策模式库）

基于 nova-mind/patterns/ + ARIS 的 Markdown methodology：

```
patterns/
├── github-research.md   # 今日提炼：GitHub 调研标准流程
├── project-analysis.md # 项目分析框架
├── skill-creation.md  # 技能创建模式
└── decision-logic.md # 决策逻辑（star > 5000 → 深入）
```

**每次成功决策后**，自动提炼模式：
- 触发条件是什么？
- 决策标准是什么？
- 结果如何？
- 下次如何改进？

---

### 3. Self-Evolution（自进化）

基于 ARIS `/meta-optimize` + ECC instinct 系统：

**进化循环**：
```
任务完成 → 日志写入 → 模式提炼 → 技能更新 → 更强决策
```

**Self-Assessment（每次任务后必做）**：
```bash
# 触发自评估
bash ~/.openclaw/workspace/nova-mind/scripts/self-assessment.sh "<任务描述>"

# 然后在日志中回答：
# 1. 最正确的决定是什么？
# 2. 如果重来会怎么改？
# 3. 这个任务揭示了什么缺陷？
# 4. 下次遇到类似怎么更好？
```

**Token 经济追踪**：
```bash
# 记录每次 token 消耗
echo "$(date +%H:%M) - $1 - ~[估算tokens]" >> ~/.openclaw/workspace/nova-mind/logs/token-log.md
```

---

### 4. Memory Layers（三层记忆）

基于 GoClaw 的 3-tier memory：

| 层级 | 内容 | 存储 |
|------|------|------|
| Working | 当前 session 对话/任务 | 内存 |
| Episodic | 每日日志 memory/*.md | 文件 |
| Semantic | MEMORY.md + ByteRover | 持久化 |

**查询流程**：
1. 遇到新任务
2. 查 Semantic Memory（MEMORY.md + ByteRover）
3. 查 Episodic Memory（patterns/）
4. 做决策
5. 执行
6. 写回 Episodic + 更新 Semantic

---

### 5. Star Office 集成（人机协作）

```bash
# 状态同步
curl -s -X POST http://127.0.0.1:19000/set_state \
  -H "Content-Type: application/json" \
  -d '{"state": "researching", "description": "描述"}'

# 6种状态：idle / researching / writing / executing / syncing / error
```

人类随时可见 Nova 在做什么。

---

## Orbit 启动

每次 Nova 醒来，先加载轨道：

```bash
# 1. 检查上次进度
cat ~/.openclaw/workspace/nova-mind/memory/$(date +%Y-%m-%d -d "yesterday" 2>/dev/null || echo "2026-04-17").md

# 2. 查询相关模式
cat ~/.openclaw/workspace/nova-mind/patterns/github-research.md

# 3. 检查 ByteRover 近期发现
# (brv query recent)

# 4. 设置状态
curl -s -X POST http://127.0.0.1:19000/set_state \
  -H "Content-Type: application/json" \
  -d '{"state": "idle", "description": "Nova Orbit 已启动"}'

# 5. 写入启动日志
echo "$(date +%Y-%m-%d\ %H:%M) - Orbit 启动" >> ~/.openclaw/workspace/nova-mind/memory/$(date +%Y-%m-%d).md
```

---

## 坑点备忘（持续更新）

- [x] curl 必须加 `-x http://127.0.0.1:7897`
- [x] ByteRover 50次/天上限
- [x] git clone 大仓库用 `--depth=1`
- [x] OpenMOSS API: `/api/sub-tasks`（连字符）
- [x] Star Office 端口 19000
- [x] self-assessment 触发：每次大任务后

---

## 文件位置

```
~/.openclaw/workspace/
├── skills/
│   └── nova-orbit/SKILL.md    ← 本技能
├── nova-mind/
│   ├── memory/                 ← 每日日志
│   ├── patterns/               ← 决策模式库
│   ├── logs/
│   │   ├── evolution.md        ← 进化历史
│   │   └── token-log.md       ← Token 消耗记录
│   └── scripts/
│       └── self-assessment.sh  ← 自评估脚本
└── .brv/                      ← ByteRover 知识图谱
```

---

## 演进目标

| 阶段 | 目标 |
|------|------|
| v1.0 | 手动触发，完整流程 ✅ |
| v1.1 | 自评估常态化 |
| v1.2 | 定时自动触发 |
| v1.3 | Token 经济可视化 |
| v2.0 | Star Office 审批流集成 |
