## v1.2.6（2026-10-02）

- 链接口径统一：包内所有引导链接指向官方详情页（jinengpu.chat/mindvault-detail.html），购买动作在详情页完成，包内不出现支付直链
- 落地页链接定值（原占位符 16 处全替换）

## v1.2.5（2026-10-02）

- 锁口提示语口径调整：archive_index 的 mark/search/summary 与 jsonl_to_md 的运行提示改为中性「需按版本核对」措辞（行为不变：提示 + 退出码 1）
- jsonl_to_md 新增未渲染内容中性提示（分片含工具调用记录时显示条数，N=0 不打印）
- README / SKILL / _meta.json 付费对照表链接统一（官方渠道占位）
- README 尾注 / SKILL 末尾版本注记同步（原 v1.2.2 残留修正）
- 平台表补 Claude Code（~/.claude/projects/，CherryStudio Claude Code 模式覆盖）；frontmatter platforms 补 claudecode

## [1.2.4] - 2026-09-30

### Changed
- skillhub/ClawHub 搜索描述关键词化：前 100 字意图词命中 3→8（记忆×2/备份/换电脑/AI 失忆/Claude/WorkBuddy/归档），skill 逻辑零改动

## [1.2.3] - 2026-09-29

### Changed
- Listing 文案（description/keywords）补「记忆」词根，提升 memory/记忆/forget 泛词检索命中（skill 逻辑零改动）

## [1.2.2] - 2026-09-18
- **版本命名规则调整（重制）**：完整版 patch 以 `.1` 结尾，公开免费版以 `.2` 结尾；本版由原 v1.1.4 统一更名为 **v1.2.2**，功能内容与 v1.1.4 一致，仅版本号与本文档同步刷新
- **双文档联动断裂修复（与完整版 v1.2.1 同步）**：`PROJECT_SNAPSHOT.md`（唯一真相源）与 `PROJECT.md`（详细版）此前只要求"改后同步对端 + diff 关键字段"，实测出现更新日志条数不等（27 vs 31）、同日期条目重复、同日期文本漂移、章节正文残留旧事实（快照仍写 v1.0.1）——关键字段 diff 通过 ≠ 真正同步
- **新增 `scripts/snapshot_sync_check.py`（基础版免费开放，不加锁）**：纯标准库六维核账校验（更新日志条数 / 日期序列 / 逐字一致 / 倒序 / 章节标题集合 / 头部元数据），支持 `--help` 与 `--snapshot` / `--detail` 入参，发现断裂退出码非 0；已用真实双文档实跑通过，并以篡改样本反向验证（正确报断裂、退出码 1）
- **SKILL.md**：第四部分新增「Layer 3 双文档联动与核账校验（强制）」规范；故障排查由 10 条扩充至 12 条；Agent 评估块 `failure_paths` 同步为 12；版本统一至 1.2.2（日期 2026-09-18）
- **README.md / _meta.json**：文件结构与说明同步新增校验脚本，版本统一至 1.2.2
- **锁 4 口策略不变**：`archive_index` 的 mark/search/summary、`jsonl_to_md` 的 `--style full` / `--css` 仍为赞赏版功能，函数体完整保留未重写；新增校验脚本不锁

## [1.1.3] - 2026-09-17
- **GEO / 可信度改造（免费版）**：按 AI 可读性思路重构 SKILL.md 结构——`description` 前 128 字符改写为「核心功能 + 分片规则 + 输出物」（129→125 字符）；`keywords` 前置搜索意图词（对话备份/对话归档/Agent 长期记忆/上下文恢复/项目快照/规则萃取）；新增 `display_description`、`tags`、`slug`、`displayName` 字段
- **SKILL.md 结构重排**：核心用法（核心功能表 + 快速开始 + 命令参数速查）前置到前 500 字内；注意事项、FAQ、故障排查依次靠前；设计背景/迭代记录/作者信息后置
- **SKILL.md 新增**：FAQ 6 条（自然语言问答，含边界与增量安全性说明）、实测数据表（15.1MB / 69 分片 / 68 文件 14,949 条目 / stats 0.07s / 转换 ≈0.1s）、首次集成时间预估（约 10 分钟）、故障排查由 8 条扩充至 10 条、参考链接新增 GitHub/ClawHub/SkillHub 互链
- **README.md 改写**：首段与标题带入核心关键词；快速开始前置为 3 条命令；新增实测数据表、常见问题、数据与隐私章节；保留开源面貌（赞赏版说明置于文末）
- **_meta.json**：版本升至 1.1.3；新增 `slug` / `display_name` / `tested_evidence` / `links` 字段；keywords 中英文均按搜索意图重排
- **doc 修正（不动函数体）**：`archive_index.py`、`jsonl_to_md.py` 模块 docstring 中残留的"（完整版）"及完整版命令清单改为"（基础版 · 免费）"+ 实际可用命令（archive_index 的 usage 由 `print(__doc__)` 输出，此修正同时修正了运行时的帮助文本）
- 完整版（赞赏版 v1.1.1）不受本次改造影响，未做任何修改
- `LICENSE` 重命名为 `LICENSE.md` 并补全 MIT 协议全文（SkillHub 不接受无扩展名文件；GitHub 同样识别 LICENSE.md）

## [1.1.2] - 2026-09-15
- 恢复双版本拆分：以 v1.1.1 完整版为基线派生**基础版（免费）**，函数体不重写，仅施加 4 类锁定
- archive_index.py：锁定 mark/search/summary 三命令（print 赞赏提示 + sys.exit(1)），基础版保留 stats/pending
- jsonl_to_md.py：--style 仅允许 minimal；--css 注释移除；保留 minimal 渲染全链路
- SKILL.md / _meta.json：版本统一至 1.1.2，注明基础版能力边界与赞赏版获取方式（https://wzyp.cn/item/p0r2lb）
- archive_export.py：无差异，三模归档 + 增量合并全量开放

## [1.1.1] - 2026-09-14
- **archive_export.py（P0-1 修复）**：OpenClaw 模式新增独立 `role == 'toolResult'` 分支——现代 OpenClaw 格式 toolResult 为独立消息（含 toolCallId/toolName/content/isError），旧版仅在 assistant 内嵌套处理导致独立消息整条丢失；现按 toolCallId 精确匹配/无 id 按 toolName 匹配待配对 toolCall，调用 process_tool 写出
- **archive_export.py（P0-2 修复）**：OpenClaw/Marvis 模式 toolCall 参数读取改为优先 `arguments`（OpenClaw 真实字段，可含 partialArgs 流式增量层），兼容旧 `args`/`input`；修复此前恒读空导致 49.1% 工具参数数据损失
- **archive_export.py（P1-1 修复）**：增量归档命名与实际轮次区间脱钩修复——文件名与索引 rounds 字段改用实际包含条目的轮次范围（actual_min-actual_max）而非固定窗口起点，消除增量阶段 rounds 前缀错标
- **archive_export.py（P1-3 修复）**：round-0 消息（首条 user 之前的消息）不再被静默丢弃，纳入首个批次归档，文件轮次区间与索引计数一致
- **archive_index.py（P1-2 修复）**：`search --rounds` 区间重叠判定由 `lo <= s <= hi or lo <= e <= hi` 改为 `s <= hi and e >= lo`，覆盖"目标区间完全包含文件区间"场景
- **archive_export.py（新增 WorkBuddy 模式）**：整合 raw-conversation-backup v1.0.1 的 WorkBuddy 原生会话文件机制为第三种模式 `workbuddy`，从 `~/.workbuddy/projects/<cwd 编码>/<sessionId>.jsonl` 逐字提取，机制差异（逐字保序禁排序 / 毫秒戳转 ISO+08:00 / callId 配对 / user_query 剥离 system-reminder）写入 _index.json；README 同步
- **SKILL.md / _meta.json**：版本统一至 1.1.1，平台/机制适配表补充 WorkBuddy；三脚本依赖无新增

## [修复记录] - 2026-09-11（基于 1.1.0 发布前评审，版本号维持 1.1.0 不变）

- **jsonl_to_md.py**（F1 修复）：`--style full` 下 Tool 消息改为读取 archive_export 实际导出的字段（args_summary / files / urls / errors），修复此前误读 error/summary/result_preview 导致 Tool 内容全丢的问题；同时保留旧字段兼容回退
- **jsonl_to_md.py**（F2 修复）：Agent 工具调用参数优先读取 tool_calls 元素内的 args，回退读取 Agent 条目顶层 key_params，修复参数读取层级错误
- **archive_index.py**（F3 修复）：`search --rounds` 改为解析 exporter 实际写入的 rounds 字符串（如 "16-30"），并新增 parse_rounds 兼容函数，修复按轮次检索失效
- **archive_index.py**（F4 修复）：stats / pending / summary 的消息数统计由不存在的 total_messages 字段改为 entries（JSONL 条数即消息数），修复统计恒 0 或 '?'
- **SKILL.md**：AIGC 块补齐为完整 7 字段（Label/ContentProducer/ProduceID/ReservedCode1/ContentPropagator/PropagateID/ReservedCode2，与 readme1.md 一致）；参考链接前补充原创性说明
- **文案统一软化**：README.md / readme1.md / SKILL.md 中"强制五步思考/每次任务自动执行"统一为"可选五步思考（用户说「走流程」/「DRASV」时激活）"，消除与 SKILL.md"可选协议"的矛盾；"永久归档/永久备份/30 秒恢复"等绝对化表述改为"长期归档/长期备份/快速恢复"；"数据主权完全属于用户"改为"掌握在用户手中"
- **readme1.md**：文末新增"购买与支持"小节，补充链动小铺链接 https://wzyp.cn/item/p0r2lb
- **SKILL.md**：隐私说明明确备份数据写入本地 archive/ 目录（每对话独立子目录，含 _index.json 索引）

## [1.1.0] - 2026-09-11
- 完整版改造：不再区分免费版/赞赏版，三脚本全部功能统一开放
- archive_index.py：解锁 mark/search/summary 完整实现；cmd_mark 加入 B9 if_version 乐观版本令牌 + B15 索引缺失即异常，写时 index_version 自增
- archive_export.py：修复 merge_index 7 参数调用/6 参数定义不匹配的历史 bug（此前 _index.json 只能手动生成）；merge_index 首次写入以实际新文件落盘；写索引携带 index_version，统一索引同步版本号（B9/B15 语义落地）
- jsonl_to_md.py：恢复 --style full 与 --css HTML 输出，支持全部角色渲染
- SKILL.md / readme1.md / _meta.json：版本统一至 1.1.0，去除付费墙文案

## [1.0.0] - 2026-07-14
- 初始发布：MindVault 思维永生系统
- 5000+ 轮实战验证
