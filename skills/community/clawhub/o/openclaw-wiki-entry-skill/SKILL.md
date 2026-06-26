---
name: wiki-entry
description: Use when the operator asks to merge configured transit notes into domain wiki pages with source metadata, index updates, status transitions, and audit checks. Do not use for compiling raw inbox notes, casual note edits, or generic summarization.
version: 1.0.0
user-invocable: true
disable-model-invocation: true
metadata: {"openclaw":{"requires":{"bins":["bash","python3","awk","sed","grep","date","mv","mkdir"]},"envVars":[{"name":"OPENCLAW_VAULT","required":false,"description":"Vault root."},{"name":"WIKI_ENTRY_TRANSIT_DIR","required":false,"description":"Directory containing compiled transit notes."},{"name":"WIKI_ENTRY_DOMAIN_DIR","required":false,"description":"Directory containing domain wiki pages."},{"name":"WIKI_ENTRY_GRADUATED_DIR","required":false,"description":"Directory for fully graduated source notes."},{"name":"WIKI_ENTRY_INDEX_FILE","required":false,"description":"Knowledge index file path."},{"name":"WIKI_ENTRY_STATE_DIR","required":false,"description":"Directory for checkpoint state files."},{"name":"WIKI_ENTRY_QMD_ENTRY","required":false,"description":"Optional QMD CLI entry for history and contradiction search."},{"name":"WIKI_ENTRY_FUSION_LOG","required":false,"description":"Executor-specific physical file used for Step 5 fusion-marker audit."},{"name":"WIKI_ENTRY_TASK_RUN_ROOT","required":false,"description":"Executor-specific structured run log root."}],"skillKey":"wiki-entry"}}
---

你是入库执行器。目标是把配置的中转站文档按 A/B 路径融合到配置的领域 Wiki，并保证元数据一致性。

## 运行配置

业务路径由 OpenClaw / agent 配置注入，换执行 agent 时不改 Skill 本体：

- `OPENCLAW_VAULT`：Vault 根目录
- `WIKI_ENTRY_TRANSIT_DIR`：中转站
- `WIKI_ENTRY_DOMAIN_DIR`：领域 Wiki 目录
- `WIKI_ENTRY_GRADUATED_DIR`：已入库目录
- `WIKI_ENTRY_INDEX_FILE`：全局索引
- `WIKI_ENTRY_STATE_DIR`：checkpoint 状态目录
- `WIKI_ENTRY_QMD_ENTRY`：QMD 入口
- `WIKI_ENTRY_FUSION_LOG`：执行者自己的融合标记物理日志
- `WIKI_ENTRY_TASK_RUN_ROOT`：执行者自己的结构化 runs 目录

## 基本心法（必须执行）

1. 行动前先查：路径决策前先看目标 Wiki 现状，不能只看 `related_wiki`。
2. 一次做一件事：每一步结束先做 micro-audit，再进入下一步。
3. 失败立即停：审计失败就停下并报告，不允许带病继续。
4. 质量优先：入库速度慢可以接受，错入/漏写不可接受。

## 不可违反（硬底线）

1. Step 3 路径决策记录到自己当天日志后自行继续，不等待确认。
2. Step 9 元数据写入必须调用 `wiki_entry_meta_writeback.sh`，`_INDEX.md` 不再手工编辑；A 路径必须显式提供 `--index-category`。
3. Step 11 审计失败必须停止，不可绕过。
4. 所有步骤都要走 `wiki_entry_step_checkpoint.sh` 记录状态。
5. 中转站/已入库/原材料仓库默认 shortest wikilink，frontmatter 例外字段可带路径。
6. `status: waiting` 是唯一待入库触发条件；waiting 数量大于 0 时必须选择 1 篇进入负向过滤，不能因为没有 `graduated_to + pending_topics` 而跳过。
7. `graduated_to + pending_topics` 只表示优先级，不是入库准入条件。
8. 通用版路径必须显式来自 OpenClaw 配置、`OPENCLAW_VAULT` 或 `--vault`；运行门禁不得把当前目录隐式当作 vault 并自动建库。

## 入口

1. 若 `WIKI_ENTRY_FUSION_LOG` 未由执行 agent 配置注入，先派生运行时默认文件：

```bash
export WIKI_ENTRY_FUSION_LOG="${WIKI_ENTRY_FUSION_LOG:-${WIKI_ENTRY_STATE_DIR:-$OPENCLAW_VAULT/.openclaw/state}/wiki_entry_fusion_$(date +%Y-%m-%d).md}"
```

2. 先跑预检查：

```bash
bash {baseDir}/scripts/wiki_entry_precheck.sh --vault "$OPENCLAW_VAULT"
```

3. 若是首次空目录初始化，必须由安装/初始化阶段显式执行：

```bash
bash {baseDir}/scripts/wiki_entry_precheck.sh --vault "$OPENCLAW_VAULT" --init
```

4. 阅读完整流程：`references/workflow.md`
5. 按步骤执行，单步完成后记录 checkpoint。

## 核心脚本

- `wiki_entry_precheck.sh`：路径校验 + graduating 扫描
- `wiki_entry_step_checkpoint.sh`：防跳步 + micro-audit 门禁
- `wiki_entry_wiki_scan.sh`：目标 Wiki 章节命中检查
- `wiki_entry_meta_writeback.sh`：来源/演进/sources_count/graduated_to/_INDEX 原子写回
- `wiki_entry_content_write.sh`：章节定位 + 正文插入/替换（Step 7）
- `wiki_entry_status_update.sh`：frontmatter status 字段修改（本 workflow 的 Step 4/10）
- `wiki_entry_audit.sh`：三件套一致性审计

## 快速命令

```bash
# Step 3 决策记录（格式见 workflow.md Step 3，写入当天日志 ## 决策 板块）
bash {baseDir}/scripts/wiki_entry_step_checkpoint.sh \
  --step 3 --status done --note "路径已决策，已写入日志"

# Step 9 元数据写回（B 路径）
bash {baseDir}/scripts/wiki_entry_meta_writeback.sh \
  --wiki "Knowledge/领域/Skills 系统.md" \
  --source-doc "Knowledge/中转站/示例.md" \
  --source-row "| [[示例]] | @author | 贡献描述 | 已入库 |" \
  --evolution-row "| 2026-04-25 | 入库更新 |" \
  --path B \
  --index-file "Knowledge/_INDEX.md"

# Step 9 元数据写回（A 路径）
bash {baseDir}/scripts/wiki_entry_meta_writeback.sh \
  --wiki "Knowledge/领域/新主题Wiki.md" \
  --source-doc "Knowledge/中转站/示例.md" \
  --source-row "| [[示例]] | @author | 首次贡献 | 已入库 |" \
  --evolution-row "| 2026-04-25 | 首次入库 |" \
  --path A \
  --index-file "Knowledge/_INDEX.md" \
  --index-category "知识管理"

# Step 11 审计
bash {baseDir}/scripts/wiki_entry_audit.sh \
  --wiki "Knowledge/领域/Skills 系统.md"
```

## 决策与检查文档

- 路径决策：`references/path-decision.md`
- 完整流程：`references/workflow.md`
- 收尾检查：`references/self-check-checklist.md`
- 错误防御手册：`references/error-playbook.md`（E1–E15）

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| c-v7 | 2026-05-03 | 同步调用版心跳硬门禁：waiting>0 必入负向过滤；graduated_to/pending_topics 只做优先级；预检运行与初始化分离，禁止隐式 cwd 建库 |
| c-v6 | 2026-04-28 | Step 3 决策日志从独立文件改为写入执行者自己当天日志（memory/YYYY-MM-DD.md），删除 Openclaw/Ops/团队/荔枝入库决策日志.md |
| c-v5 | 2026-04-27 | 修正文档编号漂移：path-decision 移除 awaiting_gavin 残留；workflow 补全 Step 10 状态收口；SKILL 明确 status_update.sh 用于 Step 4/10 |
| c-v4 | 2026-04-26 | Step 4/7 脚本化：新增 content_write.sh + status_update.sh，消除 LLM Edit 依赖 |
| c-v3 | 2026-04-26 | Step 3 硬底线从"等待确认"改为"决策日志模式"，workflow.md 同步 |
| c-v2 | 2026-04-26 | `wiki_entry_audit.sh` wikilink 路径修复：新增 Knowledge/领域/ + 目录引用回退（E15） |
| c-v1 | 2026-04-25 | 首版正式上线：12 步流程 + 7 个脚本护栏 + error-playbook E1–E14 |
