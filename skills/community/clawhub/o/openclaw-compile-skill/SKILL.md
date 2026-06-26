---
name: compile
description: Use when the operator asks to compile the configured inbox knowledge notes into curated transit documents and archive source material with auditable links. Do not use for ordinary note editing, final wiki merging, or tasks that should only summarize content.
version: 1.0.0
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw":{"requires":{"bins":["bash","python3","awk","sed","grep","date","mv","mkdir","find","wc","rm"]},"envVars":[{"name":"OPENCLAW_VAULT","required":false,"description":"Vault root."},{"name":"COMPILE_INBOX_DIR","required":false,"description":"Inbox directory containing raw markdown notes."},{"name":"COMPILE_TRANSIT_DIR","required":false,"description":"Destination directory for compiled markdown notes."},{"name":"COMPILE_RAW_DIR","required":false,"description":"Archive directory for raw source markdown notes."},{"name":"COMPILE_STATE_DIR","required":false,"description":"Directory for checkpoint state files and short-lived run cache."},{"name":"COMPILE_QMD_ENTRY","required":false,"description":"Optional QMD CLI entry for history search."},{"name":"COMPILE_ACTOR_NAME","required":false,"description":"Executor name written to compiled_by."},{"name":"COMPILE_FILENAME_LOG_FILE","required":false,"description":"Executor-specific filename decision log."},{"name":"COMPILE_TASK_RUN_ROOT","required":false,"description":"Optional override for short-lived run cache root; normally leave unset."},{"name":"COMPILE_RUN_RETENTION_DAYS","required":false,"description":"Optional run cache retention days, default 14."},{"name":"COMPILE_RUN_MAX_FILES","required":false,"description":"Optional max run cache files, default 500."}],"skillKey":"compile"}}
---

你是编译执行器。目标是把配置的收件箱原文编译到配置的中转站，并把原文与图片安全归档到配置的原材料仓库。

## 运行配置

业务路径由 OpenClaw / agent 配置注入，换执行 agent 时不改 Skill 本体：

- `OPENCLAW_VAULT`：Vault 根目录
- `COMPILE_INBOX_DIR`：收件箱，必须由配置注入；未配置时流程失败，禁止回退到 `Inbox/`
- `COMPILE_TRANSIT_DIR`：中转站
- `COMPILE_RAW_DIR`：原材料仓库
- `COMPILE_STATE_DIR`：checkpoint 状态目录
- `COMPILE_QMD_ENTRY`：QMD 入口
- `COMPILE_ACTOR_NAME`：写入 `compiled_by` 的执行者名称，荔枝生产环境固定为 `荔枝`
- `COMPILE_FILENAME_LOG_FILE`：执行者自己的文件名决策日志，必须由配置注入
- 结构化 runs 由 Skill 自动写入 `.openclaw/state/compile/runs/`，只作为短期运行缓存

## 基本心法（必须执行）

1. 行动前先查：文件名核对和生成正文前都要先查历史（`query_history.sh`）。
2. 关键词先复用 `Knowledge/_INDEX.md` 里的现有主题词；查不到时再自己设计。
3. 一次做一件事：每一步结束先做 micro-audit，再进入下一步。
4. 失败立即停：`compile_check.sh` 审计失败就停下，不允许带病继续。
5. 质量优先：标题、frontmatter、双向链接的正确性高于处理速度。

## 不可违反（硬底线）

1. 标题不得自拟、改写、截短。
2. frontmatter 必须通过 `compile_frontmatter_gen.sh` 生成。
3. `compile_check.sh` FAIL 必须停止，并写 blocked checkpoint。
4. 所有步骤都要走 `compile_step_checkpoint.sh` 记录状态。
5. `original` / `compiled_version` 必须写带路径 wikilink，且必须回读验证。
6. 只能使用 OpenClaw 原生工具调用；禁止输出 `<invoke ...>`、XML、伪 tool 标签或把 shell 命令写成普通文本。
7. 若某一步需要运行脚本但上一条回复里没有真实工具调用成功落地，必须立即重新发起原生工具调用；不得假设“文本里的命令已经执行”并继续后续步骤。
8. 生产环境不得创建或扫描 Vault 顶层 `Inbox/`；真实收件箱由 `COMPILE_INBOX_DIR` 指定。

## 入口

1. 先跑预检查：

```bash
bash {baseDir}/scripts/compile_precheck.sh --vault "$OPENCLAW_VAULT"
```

2. 阅读完整流程：`references/workflow.md`
3. 按步骤执行，单步完成后记录 checkpoint。

## 核心脚本

- `compile_precheck.sh`：路径校验 + 收件箱待编译扫描
- `compile_clipper_fix.sh`：eb-clipper 脏数据修复
- `compile_duplicate_check.sh`：标题归一化 + source 兜底的重复检查
- `compile_filename_check.sh`：文件名与主题一致性核对（默认只报建议，传 `--apply` 才改名）
- `compile_frontmatter_gen.sh`：生成标准 frontmatter
- `compile_archive.sh`：归档原文、图片和双向链接
- `compile_step_checkpoint.sh`：防跳步 + micro-audit 门禁
- `compile_task_logger.sh`：记录短期结构化运行日志并自动清理旧 runs
- `compile_check.sh`：27 项机械性自审

## 快速命令

```bash
# Step 1.5 文件名核对
bash {baseDir}/scripts/compile_filename_check.sh \
  --file "$COMPILE_INBOX_DIR/示例.md" \
  --llm-summary "文章实际主题摘要" \
  --llm-keywords "关键词1,关键词2,关键词3"

# Step 2 frontmatter 生成
bash {baseDir}/scripts/compile_frontmatter_gen.sh \
  --title "示例标题" \
  --author "@author" \
  --source "https://example.com" \
  --compiled-by "$COMPILE_ACTOR_NAME" \
  --tags "compile,knowledge-pipeline" \
  --keywords "主题关键词1,主题关键词2" \
  --related-wiki "[[Harness Engineering]] | rough"

# Step 4 归档
bash {baseDir}/scripts/compile_archive.sh \
  --source "$COMPILE_INBOX_DIR/示例.md" \
  --compiled "$COMPILE_TRANSIT_DIR/示例.md" \
  --title "示例"
```

## 决策与检查文档

- 完整流程：`references/workflow.md`
- 标题规则：`references/title-rules.md`
- Frontmatter 规范：`references/frontmatter-spec.md`
- 收尾检查：`references/self-check-checklist.md`
- 历史错误对照：`references/error-playbook.md`

## 变更记录

| 日期 | 变更 |
|------|------|
| 2026-04-29 | Step 0.1.5 查重增强：新增 `compile_duplicate_check.sh`，标题先做归一化（忽略 `：` / `-` 等标点差异），并用 `source` URL 做二次兜底；当前查重范围只保留 `原材料仓库`，不再扫描 `中转站` 与 `已入库` |
| 2026-05-02 | 本机安装版收紧配置门禁：`COMPILE_INBOX_DIR` 与 `COMPILE_FILENAME_LOG_FILE` 缺失时 fail fast，不再回退或创建通用 `Inbox/` / `Openclaw/Ops/compile` 目录 |
| 2026-04-27 | Step 0.1.5 查重修正：比对目标从 `中转站` 改为 `已入库`。源文件全程不改动，文件名是唯一标识，只做文件名比对（原材料仓库 + 已入库）。同内容换标题的特例不处理 |
| 2026-04-27 | 源文件不改动原则确认：源文件在流水线中只做移动（收件箱→原材料仓库→已入库），内容和文件名不变。唯一例外：Step 0.0 clipper_fix 属于编译前预处理，不算改动源文件 |
