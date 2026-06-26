# CLAUDE.md — lobster-crawler-skill

> 本文件是项目的唯一规范源。Claude Code 交互模式自动加载，`claude -p` 循环模式同样自动加载。
> 如果你是通过 Codex 执行，请同时参阅 `agent.md`（Codex 兼容垫片）。

---

## 项目目标

为"龙虾"平台开发网络内容爬取技能：定向抓取 Webnovel、ReelShorts 等网站的书籍/短剧内容，沉淀站点地图，支持定时抓取、内容分级和钉钉播报。

核心方向：
- 定向爬取目标站点（Webnovel 小说、ReelShorts 短剧）的结构化内容
- 站点地图沉淀与增量更新
- 内容分级（高/中/低）+ 钉钉机器人定时播报

## 项目概况

- **语言**: Python 3.11+
- **爬虫框架**: Scrapy 2.11+
- **存储**: SQLite (MVP)，后续可升级 PostgreSQL
- **定时调度**: APScheduler
- **配置**: YAML（站点规则）+ 环境变量（密钥）
- **播报**: 钉钉机器人 Webhook
- **CLI**: click 命令行工具
- **依赖文件**: `requirements.txt`
- **项目元数据**: `pyproject.toml`
- 持续执行闭环：`scripts/claude_loop.sh` + `prompts/claude_loop_prompt.txt`
- 状态追踪：`docs/TODO.md` + `docs/STATE.md` + `docs/FEEDBACK.md`

### 关键目录

```
src/models/       — 数据模型 (Novel/Chapter/Episode ORM, SQLite)
src/spiders/      — Scrapy 爬虫 (base + 站点实现)
src/sitemap/      — 站点地图生成/查询
src/scheduler/    — APScheduler 定时调度
src/classifier/   — 内容分级引擎
src/broadcast/    — 钉钉播报 + 消息模板
src/cli.py        — CLI 入口 (click)
config/           — YAML 配置 (settings.yaml + sites/*.yaml)
```

---

## 编码规范

### 1. 依赖管理

- 位置：`requirements.txt`
- 每次新增第三方库的 import 时，必须同步更新 `requirements.txt`
- 每次删除依赖使用时，也要从 `requirements.txt` 中移除

### 2. 文档同步

以下文档需要随代码变化同步更新：

- **README.md**：项目结构、CLI 用法、启动方式变化时更新
- **docs/TODO.md**：任务完成时勾选
- **docs/MEMORY.md**：每次会话结束前或完成重要变更后，**主动**更新项目记忆，无需用户提醒。记录内容包括：本次做了什么、关键设计决策、踩过的坑、版本发布记录。同时同步更新 Claude Code 自动记忆（`~/.claude/projects/` 下的 `memory/MEMORY.md`）

### 3. 代码风格

- Python 代码遵循 PEP 8
- 使用 Google 风格 docstring
- 类型注解：所有公开函数必须有类型注解
- 命名：模块/变量 snake_case，类 PascalCase，常量 UPPER_SNAKE_CASE
- 配置文件使用 YAML，键名 snake_case

### 4. 执行后总结与经验沉淀

每次执行完用户命令后，必须在回复末尾附上**执行后总结**，包含：

1. **本次操作摘要**：做了什么、改了哪些文件
2. **分类归档**：判断是否产生需要归档的内容：
   - **BUG**：发现或修复的 bug → 记录到 `docs/FEEDBACK.md` 或 `bug_fix/`
   - **FEEDBACK**：流程改进、编码规范补充 → 记录到 `docs/FEEDBACK.md`
   - **规则沉淀**：反复出现的模式 → 更新 `docs/MEMORY.md`
3. **无产出也要说明**：明确标注"无需归档"

---

## 反馈与 Bug 修复闭环

本项目有两个问题输入通道，Agent 每轮执行前必须同时检查：

### 通道 1：`docs/FEEDBACK.md`（结构化反馈）

- 用户记录编码规范、流程改进、文档缺失等**持续性约束**
- 每轮执行前，阅读所有 `status: open` 条目
- Open 条目中的 `action` 字段是**强制约束**，本轮及后续所有轮次都必须遵守
- 如果当前任务涉及 open feedback 相关的代码/文件，必须在本轮一并修正
- 当某条 feedback 被完全解决后，移到 "Resolved" 段落并填写 `resolved-by`

### 通道 2：`bug_fix/`（热修收件箱）

- 用户遇到具体 bug 时，在 `bug_fix/` 下放一个 `.md` 文件
- **优先级高于常规 TODO**：`bug_fix/` 下存在未解决的文件时，Agent 必须先处理
- 处理流程：
  1. 读取 `bug_fix/` 下每个 `.md` 文件，理解问题和修复建议
  2. 执行修复，如文件中包含验证方法则按其验证
  3. 在 `docs/FEEDBACK.md` 的 Resolved 段落追加一条记录（留痕）
  4. 将该 `.md` 文件移动到 `bug_fix/resolved/`（归档）
- 如果无法修复，在 `docs/FEEDBACK.md` Open 段落登记，并在输出 `blockers` 中注明

---

## 循环执行规则（claude_loop.sh 上下文）

> 以下规则在 `claude -p` 循环模式中生效。交互模式下作为参考。

### 全局规则

1. 每一轮只允许处理一个 `ACTIVE_TODO`
2. 执行前必须先阅读：
   - `docs/TODO.md`
   - `docs/STATE.md`
   - `docs/FEEDBACK.md`
   - `docs/MEMORY.md`
3. 只做完成当前 TODO 必需的最小修改，不顺手处理下一个 TODO
4. 只有在任务真实闭环后，才允许勾选 `docs/TODO.md`
5. 每轮结束必须更新 `docs/STATE.md`
6. 修改时优先复用现有目录结构，不做无关重构

### 实现原则

1. **先骨架，后细节**：先落数据结构与接口，再丰富体验
2. **先持久化，后编排**：先让状态能落盘，再引入复杂调度
3. **保持兼容**：已有接口短期内尽量保留，通过新增接口渐进演进
4. **最小可运行增量**：每个 TODO 都应产出能被验证的文件、接口或页面

### 修改边界

允许修改：
- `src/` 下所有 Python 源码
- `config/` 下所有 YAML 配置
- `tests/` 下所有测试
- `requirements.txt`、`pyproject.toml`
- `docs/` 下状态文件
- `README.md`

谨慎修改：
- `scrapy.cfg`（Scrapy 全局配置）
- `scripts/claude_loop.sh`（循环脚本）
- `prompts/claude_loop_prompt.txt`（循环 prompt）

禁止行为：
- 不经说明删除可运行的现有主流程
- 把多个 TODO 合并一轮一起做
- 未确认闭环就勾选 TODO
- 引入重型基础设施依赖作为第一步前置

### 实现优先级

按下面顺序推进，不跳步：
1. **Phase A** — 基础骨架：项目结构、数据模型、配置系统、站点地图、爬虫框架
2. **Phase B** — 站点适配：Webnovel / ReelShorts 配置与 Spider 实现
3. **Phase C** — 调度与分级：APScheduler 定时、内容分级、增量去重
4. **Phase D** — 播报与接口：消息模板、钉钉集成、RSS、CLI
5. **Phase E** — 运维与健壮性：日志监控、反爬增强、Docker 部署

### 输出 JSON

每轮最终必须只输出一个 JSON 对象，不要输出 markdown、代码块或额外解释。

```json
{
  "run_status": "success | blocked | failed",
  "active_todo": "Txxx",
  "completed": true | false,
  "summary": "short summary",
  "bugs_fixed": ["filename.md", ...],
  "files_changed": ["file1", "file2"],
  "state_updated": true | false,
  "todo_updated": true | false,
  "next_todo": "Txxx or empty string",
  "blockers": ["..."]
}
```

**completed=true 条件**（必须同时满足）：
- 当前 TODO 所需的代码/文档/脚本已实际修改完成
- `docs/STATE.md` 已写回本轮进度
- 没有阻塞当前 TODO 闭环的关键缺失

**completed=false 条件**（满足任一）：
- 只改了一半 / 仍需额外依赖才能判断完成 / 尚未补齐状态文件 / 结果不可验证
