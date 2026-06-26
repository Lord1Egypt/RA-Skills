# 入库错误防御手册（E1–E14）

> 为什么入库流程有这么多脚本门禁？因为以下 14 个错误**真实发生过**。
> 每条记录：发生了什么 → 根因 → 现在靠什么防住。
> 执行入库时如果想"跳过这步应该没事"，先来这里查一下。

---

## E1 — graduated_to 字段漏写

**事故**：4/24，一次 4 篇中转站文档入库后 graduated_to 为空，无法追溯去了哪个 Wiki。
**根因**：写正文和写元数据是两步操作，LLM 写完正文后忘了回头写 frontmatter。
**防御**：`wiki_entry_meta_writeback.sh` 原子写入 graduated_to + 回读验证。

## E2 — Wiki 来源表行遗漏

**事故**：4/19–4/20 连续 3 次审计发现 Wiki 来源表缺行，正文也没融合该篇内容。
**根因**：加载了规则但执行时跳过（加载 ≠ 激活）。写正文、写来源表、写演进是分散步骤。
**防御**：`wiki_entry_meta_writeback.sh` 幂等插入来源行（grep 去重后 sed 插入）。

## E3 — sources_count 虚高

**事故**：4/25 审计发现 6 个 Wiki 的 sources_count 比实际来源表行数多。
**根因**：每次入库 +1，但删除/合并来源时没 -1，累积偏差。
**防御**：`wiki_entry_meta_writeback.sh` 以"数来源表实际行数"为权威，回写 frontmatter。

## E4 — 入错 Wiki

**事故**：虚拟货币交易篇被错误入库到"Agent 记忆系统"Wiki。
**根因**：只看 `related_wiki` 字段+标题脑补，没读 Wiki 实际章节确认匹配。
**防御**：Step 6 `wiki_entry_wiki_scan.sh` 强制扫描目标 Wiki 关键词；Step 3 路径决策必须 Gavin 确认。

## E5 — context 满中断 → 空 Wiki 文件

**事故**：4/24，"Claude 高效工作流"入库时 context 满，创建了空 Wiki 文件但没写入内容。
**根因**：写 Wiki 是单步大写入，中断即半成品。
**防御**：`graduating` 保护状态 + `wiki_entry_precheck.sh` 启动扫描 + `wiki_entry_step_checkpoint.sh` 断点续做。

## E6 — MEMORY.md 路径错误

**事故**：荔枝每次心跳都尝试读 `workspace/main/MEMORY.md`，路径不存在。
**根因**：配置中路径写错，没有启动时校验。
**防御**：`wiki_entry_precheck.sh` 校验 6 条关键路径，任一不存在即 exit 1 阻断。

## E7 — wikilink 缺空格

**事故**：偶发，LLM 生成 `[[多Agent协调模式]]` 而非 `[[多 Agent 协调模式]]`。
**根因**：LLM 生成文本时随机丢空格。
**防御**：`wiki_entry_audit.sh` 检查 wikilink 目标文件是否存在（间接发现不匹配）。后续可加 shortest 格式检查。

## E8 — 入库流程跳步

**事故**：4/25 荔枝自报 6 条跳步记录。
**根因**：12 步流程长，没有"上一步未审计通过不能进下一步"的硬约束。
**防御**：`wiki_entry_step_checkpoint.sh` 双层防跳：Layer 1 检查前置步骤全 done，Layer 2 跑 `--audit-cmd` 微审计。

## E9 — _INDEX.md 漏更新

**事故**：偶发，入库完成但 _INDEX 未同步更新篇数。
**根因**：_INDEX 是大文件，context 高时容易跳过。
**防御**：`wiki_entry_meta_writeback.sh` 把 _INDEX 更新纳入原子操作 + 回读验证。

## E10 — 未扫描 Wiki 就决策方向

**事故**：4/25，直接凭 `related_wiki` 判断 B 路径，没看 Wiki 实际内容就写入，导致入错 Wiki（E4 根因之一）。
**根因**：凭字段+标题脑补，跳过了"读一下目标 Wiki 看匹配不匹配"。
**防御**：`wiki_entry_wiki_scan.sh` 强制 grep 目标 Wiki 章节关键词，无匹配则 BLOCK 不让进入 Step 7。

## E11 — 跳过融合笔记

**事故**：4/25，荔枝认为"内容简单不用写"，主动跳过 Wiki 入库融合笔记。
**根因**：LLM 自主判断"不需要"，没有强制检查。
**防御**：Step 5 的 micro-audit 强制 grep 当日 memory 文件中是否包含融合标记，不存在则 BLOCK。

## E12 — 演进记录追加遗漏

**事故**：4/25 多篇入库后 Wiki 演进记录未追加。
**根因**：写完正文以为"已记演进"，实际未追加。
**防御**：`wiki_entry_meta_writeback.sh` 把演进记录写入合并进同一次原子操作。

## E13 — 回读验证不完整

**事故**：多次，自审只查 graduated_to 和 sources_count，漏 last_updated 等字段。
**根因**：LLM 自审凭印象勾选（橡皮图章）。
**防御**：`wiki_entry_audit.sh` 脚本化全字段验证（含 last_updated 是否为今日）。

## E14 — 矛盾追踪默认跳过

**事故**：4/25 多篇标注"无矛盾，跳过"，但实际未检查。
**根因**："无矛盾"是默认值，LLM 不主动验证。
**防御**：`wiki_entry_meta_writeback.sh` grep Wiki 中 `⚡矛盾` 标记，有则 exit 2 要求显式判定后才能继续。

## E15 — audit 脚本 wikilink 路径覆盖不全

**事故**：4/26，荔枝心跳 Session 85689 Step 10 审计 blocked，`[[Claude Code 架构与配置]]`、`[[LLM 个人知识库]]`、`[[中转站]]` 被报为"目标不存在"。
**根因**：`wiki_entry_audit.sh` shortest wikilink 解析只查中转站/已入库/原材料仓库三个目录，未覆盖 `Knowledge/领域/`（Wiki 页面所在目录）；且最终校验只做 `-f`（文件检查），目录引用（如 `[[中转站]]`）无法通过。
**防御**：v2 修复——路径解析新增 `Knowledge/领域/`（p4）+ `Knowledge/` 目录回退（p5 + `-d` 检查）；最终校验改为 `{ [ ! -f "$p" ] && [ ! -d "$p" ]; }`。

---

## 速查：脚本 ↔ 错误对照

| 脚本 | 防御的错误 |
|---|---|
| `wiki_entry_precheck.sh` | E5, E6 |
| `wiki_entry_step_checkpoint.sh` | E8（跳步）+ 所有步骤的 micro-audit 入口 |
| `wiki_entry_wiki_scan.sh` | E10 |
| `wiki_entry_meta_writeback.sh` | E1, E2, E3, E9, E12, E14 |
| `wiki_entry_audit.sh` | E7, E13, E15 |
| `wiki_entry_xref_sync.sh` | 双向链接对称性 |
| `wiki_entry_mv_graduated.sh` | graduated 文档安全移动 |
