# wiki-entry 完整流程

> 本流程为 wiki-entry Skill 的正式版执行流程，使用脚本门禁、防跳步 checkpoint 与元数据一致性审计。

## Step 0 预检查

若 `WIKI_ENTRY_FUSION_LOG` 未由执行 agent 配置注入，先派生运行时默认文件。Step 5 的融合笔记必须写入这个文件：

```bash
export WIKI_ENTRY_FUSION_LOG="${WIKI_ENTRY_FUSION_LOG:-${WIKI_ENTRY_STATE_DIR:-$OPENCLAW_VAULT/.openclaw/state}/wiki_entry_fusion_$(date +%Y-%m-%d).md}"
```

```bash
bash {baseDir}/scripts/wiki_entry_precheck.sh --vault "$OPENCLAW_VAULT"
```

- 校验关键路径存在
- 列出 `status: graduating` 文档
- 扫描 `status: waiting` 文档数量
- 发现异常先处理恢复，再继续新任务
- **`status: waiting` 是唯一待入库触发条件；waiting 数量大于 0 时，必须选择 1 篇进入 Step 2 负向过滤**
- **`graduated_to + pending_topics` 只表示优先处理，不是入库准入条件；没有这类文档时，继续处理其他 waiting 文档**
- **预检查 exit 0 且 waiting 数量大于 0 时，不得只记录扫描后跳过入库**
- **退出码 3 = 中转站无待入库文档 → 跳过入库，直接写日志收工**
- 通用版支持任意用户路径，但必须显式传入 `--vault` 或配置 `OPENCLAW_VAULT`；运行门禁不会把当前目录隐式当作 vault，也不会自动创建业务目录
- 首次初始化目录/索引时，使用 `wiki_entry_precheck.sh --vault "$OPENCLAW_VAULT" --init`，初始化与正式运行分离

## Step 1 定位目标文档

- 读取目标中转站文档 frontmatter
- 提取 `related_wiki` 候选
- 校验目标文件存在
- 无参数或自动心跳模式下，按以下顺序自行选择 1 篇 waiting 文档：已部分入库待补充（`graduated_to` 有值且 `pending_topics` 有值）优先；其次同主题多篇积累；再次按 `related_wiki` 可落点明确度、文件新鲜度或列表顺序选择单篇

checkpoint:

```bash
bash {baseDir}/scripts/wiki_entry_step_checkpoint.sh \
  --step 1 --status done --audit-cmd "test -f 'Knowledge/中转站/目标文档.md'"
```

## Step 2 负向过滤

- 对重叠率和价值做负向过滤
- 输出：通过 / 不通过 + 理由

checkpoint（示例）：

```bash
bash {baseDir}/scripts/wiki_entry_step_checkpoint.sh \
  --step 2 --status done --audit-cmd "test -n '过滤理由已输出'"
```

## Step 3 路径决策（决策日志模式）

- 输出 A/B/拒绝 + 理由
- 路径决策前必须先查历史（`query_history.sh`）
- 决策后写入决策日志：记录到自己当天日志（memory/YYYY-MM-DD.md）的 `## 决策` 板块下，自行继续（不等待确认）
- 日志记录格式（写在 `## 决策` 下）：

```
- 文档：<中转站文档名>
- 路径：A / B
- 目标Wiki：<Wiki页名>
- 理由：<一句话>
```

```bash
bash {baseDir}/scripts/_shared/query_history.sh \
  --skill wiki-entry \
  --topic "目标主题" \
  --window 30 \
  --vault "$OPENCLAW_VAULT"

# Step 3 决策记录（写入当天日志 ## 决策 板块，格式见上方）

bash {baseDir}/scripts/wiki_entry_step_checkpoint.sh \
  --step 3 --status done --note "路径已决策，已写入日志"
```

## Step 4 标记 graduating

```bash
bash {baseDir}/scripts/wiki_entry_status_update.sh \
  --doc "Knowledge/中转站/目标文档.md" \
  --from waiting \
  --to graduating

bash {baseDir}/scripts/wiki_entry_step_checkpoint.sh \
  --step 4 --status done --audit-cmd "grep -q '^status: graduating' 'Knowledge/中转站/目标文档.md'"
```

## Step 5 精读与融合笔记

- 写当日融合笔记（用于追溯）
- 🔴 融合笔记必须写入当日 memory 文件，包含「融合标记」关键词（E11 防御）

checkpoint（audit-cmd 必须 grep 到融合标记，否则 BLOCK）：

```bash
bash {baseDir}/scripts/wiki_entry_step_checkpoint.sh \
  --step 5 --status done --audit-cmd "grep -q '融合标记' \"$WIKI_ENTRY_FUSION_LOG\""
```

> `WIKI_ENTRY_FUSION_LOG` 由执行 agent 配置指定。关键是**必须有物理文件证据**，不能靠 LLM 自报。

## Step 6 扫描目标 Wiki（防误入）

```bash
bash {baseDir}/scripts/wiki_entry_wiki_scan.sh \
  --wiki "Knowledge/领域/目标Wiki.md" \
  --keywords "关键词1,关键词2"
```

- 无命中则 BLOCK，回到 Step 3 重新决策

## Step 7 分段写 Wiki

- 写 Wiki 章节前先做矛盾检查（`query_history.sh --include-contradictions`）
- LLM 生成内容，脚本写入文件（不再用 Edit 工具直接编辑 Wiki）
- 先骨架，后分段调用 `wiki_entry_content_write.sh` 逐章节写入
- **默认走 `--content-file` 路径**：LLM 先 Write 内容到临时文件，再传路径给脚本。`--content` 仅用于短文本测试
- 脚本内置回读验证，不需要额外手动回读

```bash
# 矛盾检查（不变）
bash {baseDir}/scripts/_shared/query_history.sh \
  --skill wiki-entry \
  --topic "目标主题" \
  --window 30 \
  --include-contradictions \
  --vault "$OPENCLAW_VAULT"

# 分段写入（新）— 每个章节调用一次
bash {baseDir}/scripts/wiki_entry_content_write.sh \
  --wiki "Knowledge/领域/目标Wiki.md" \
  --section "## 核心知识" \
  --content-file "/tmp/wiki_section_content.md" \
  --mode append

bash {baseDir}/scripts/wiki_entry_step_checkpoint.sh \
  --step 7 --status done --audit-cmd "grep -q '^## 核心知识' 'Knowledge/领域/目标Wiki.md'"
```

## Step 8 交叉链接

- 补充相关主题双向链接

```bash
bash {baseDir}/scripts/wiki_entry_xref_sync.sh \
  --wiki "Knowledge/领域/目标Wiki.md"
```

- exit 0 = 全部对称；exit 1 = 有补链动作（检查补链内容是否合理）

## Step 9 元数据原子写回（必须脚本）

- `_INDEX.md` 的来源数 / 日期 / 新主题插入都由脚本完成，不再手工编辑。
- A 路径在 Step 3 决策时必须同时确认 `_INDEX` 分类名，供 `--index-category` 使用。

```bash
bash {baseDir}/scripts/wiki_entry_meta_writeback.sh \
  --wiki "Knowledge/领域/目标Wiki.md" \
  --source-doc "Knowledge/中转站/目标文档.md" \
  --source-row "| [[目标文档]] | @作者 | 核心贡献 | 已入库 |" \
  --evolution-row "| 2026-04-25 | 入库更新 |" \
  --path B \
  --index-file "Knowledge/_INDEX.md"

bash {baseDir}/scripts/wiki_entry_meta_writeback.sh \
  --wiki "Knowledge/领域/新主题Wiki.md" \
  --source-doc "Knowledge/中转站/目标文档.md" \
  --source-row "| [[目标文档]] | @作者 | 首次贡献 | 已入库 |" \
  --evolution-row "| 2026-04-25 | 首次入库 |" \
  --path A \
  --index-file "Knowledge/_INDEX.md" \
  --index-category "知识管理"
```

## Step 10 状态收口（graduating → graduated / waiting）

> `wiki_entry_status_update.sh` 在本 workflow 中用于 **Step 4 / Step 10**。

- **全部内容已入库**：`graduating -> graduated`
- **部分内容已入库**：`graduating -> waiting`，并保留 `graduated_to + pending_topics`

```bash
# 全部内容已入库
bash {baseDir}/scripts/wiki_entry_status_update.sh \
  --doc "Knowledge/中转站/目标文档.md" \
  --from graduating \
  --to graduated

bash {baseDir}/scripts/wiki_entry_step_checkpoint.sh \
  --step 10 --status done --audit-cmd "grep -q '^status: graduated' 'Knowledge/中转站/目标文档.md'"

# 部分内容已入库
bash {baseDir}/scripts/wiki_entry_status_update.sh \
  --doc "Knowledge/中转站/目标文档.md" \
  --from graduating \
  --to waiting

bash {baseDir}/scripts/wiki_entry_step_checkpoint.sh \
  --step 10 --status done --audit-cmd "grep -q '^status: waiting' 'Knowledge/中转站/目标文档.md'"
```

## Step 11 审计（失败即停）

```bash
bash {baseDir}/scripts/wiki_entry_audit.sh \
  --wiki "Knowledge/领域/目标Wiki.md"
```

## Step 12 移动 graduated 文档与收尾

```bash
bash {baseDir}/scripts/wiki_entry_mv_graduated.sh \
  --source-doc "Knowledge/中转站/目标文档.md"
```

- status: waiting（有 graduated_to + pending_topics）的文档留在中转站，不移动

**记录（按执行者区分）**：

| 执行者 | 写入位置 | 内容 |
|--------|---------|------|
| **执行者** | 自己的当日日志 / context 文件 | 记录入库主题、产出路径和剩余风险 |
| **长期记忆** | 执行者自己的长期记忆文件（如有） | 仅记录可复用经验，避免流水账 |

**向 Gavin 汇报**（所有执行者统一）：
- 入库主题
- 产出 Wiki 页面路径
- graduated / 回到 waiting 文档各几篇
- 发现的知识缺口（[待充实] 标记了什么）
