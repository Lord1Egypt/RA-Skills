---
name: ingest_document
description: Ingest a single document, uploaded file, meeting note, experiment record, or chat-provided material into a personal or team knowledge base, including summaries, source archiving, duplicate checks, and project/person aggregation updates.
---

# Skill: ingest_document — 日常单条资料入库

## 用途

把用户日常发来的单个资料入库到个人知识库、团队知识库，或用户明确要求时双写两个库。

支持类型：

- 论文 paper
- 行业调研 survey
- 开源项目 project
- 技术文档 doc
- 实验记录 experiment
- 会议纪要 meeting
- 代码仓库总览 codebase
- 个人笔记 note

## 触发条件

Activate when:

- 用户上传单个 PDF/Word/Excel/txt/md 文件并要求保存
- 用户发一段会议纪要、实验记录、想法并要求保存
- 用户发链接并要求保存，不是批量资料源接入
- 用户明确说“存到个人库 / 团队库 / 两边都存”

Do NOT activate when:

- Gitea 仓库批量编译 → `batch_compile`
- 查询知识库 → `query_kb`
- GitHub repo 评估“值不值得/能不能复现” → `eval_repo`
- 用户未注册 → `init_workspace`

## 目标库判断

先调用：

```bash
python3 scripts/ingest_one.py \
  --sender_id <SenderId> \
  --chat_type <ChatType> \
  --chat_id <GroupSubject> \
  --message_sid <MessageSid> \
  --message "<用户消息>" \
  [--type_hint meeting]
```

规则：

- 私聊默认个人知识库，身份使用 `SenderId`。
- 团队群里明确 @bot 入库时，必须先用 `GroupSubject` 查 `chat_bindings.json`。
- 群聊未绑定团队：拒绝入库，提示管理员先绑定本群。
- 群聊默认入当前群绑定的团队知识库。
- 群聊中不允许存入个人知识库；个人资料必须私聊处理。
- 群聊发送者 `SenderId` 必须是绑定团队成员。
- 私聊内容像团队会议/项目资料时，先追问存个人库还是团队库。
- 私聊内容需要确认入库目标时，优先使用脚本返回的 `interactive_card` 发送飞书互动卡片；按钮值 `ingest_target:personal/team/both` 先交给 `resolve_target_action.py`，再按返回的 `explicit_target` 再次调用 `ingest_one.py`。
- 普通成员可以提交单条资料到团队库。
- 普通成员不能创建新项目。
- 用户明确要求“两边都存”时才双写。

## OpenClaw 语义步骤

1. 提取正文：文件用 `text_extractors.py`，纯文本直接写临时 txt。
2. 判断资料类型。
3. 调 `render_summary_template.py` 获取该资料类型的结构模板；把返回 JSON 里的 `rules`、`quality_checklist`、`must_capture_fields` 和 `markdown_template` 一起交给 MiniMax，让它严格按模板生成 Markdown 草稿，写到 `/tmp/paperkb/draft_summary.md`。
4. 单条查重：确定重复/疑似重复都要问用户，优先发送 `check_duplicate.py` 返回的 `interactive_card`。按钮值 `duplicate:overwrite/save_new/cancel` 交给 `resolve_duplicate_action.py` 转成保存策略。
5. 调 `save_document.py` 保存 summary。
6. 如生成概念/资源/人物/综述页，调 `save_page.py`。
7. 如果是团队会议纪要或实验记录，调 `update_project_people.py` 更新项目与人物聚合页。

生成草稿前调用：

```bash
python3 scripts/render_summary_template.py \
  --type_key <paper|survey|project|doc|experiment|meeting|codebase|note> \
  --title "<标题>" \
  --project_id <project_id> \
  --source_id "<source_id>" \
  --source_path "<source_path>" \
  --source_url "<source_url>" \
  --source_commit "<source_commit>" \
  --save_to /tmp/paperkb/summary_template.json
```

MiniMax 生成时必须遵守：

- 模板中的章节不要删除；原文没有的信息填“未提及”。
- 不得补充外部常识或自己猜测；不确定但有原文线索时写“资料显示不完整：<线索>”。
- 保留关键数字、实验结果、版本、路径、链接、页码等可追溯证据。
- 每篇都必须填写“知识库定位”“证据索引”“关键词与实体”，方便后续查询、项目聚合和引用。
- 会议和实验必须抽取行动项；缺负责人或截止时间则写“未提及”。
- 最后一节必须保留“来源与可追溯信息”。

各类型重点记录：

- `paper`：研究问题、任务边界、核心贡献、方法流程、数据/指标/基线、主结果、消融、失败案例、局限、团队可复用点。
- `survey`：调研范围、资料来源可信度、分类框架、关键结论与证据、主要玩家/方案、趋势、机会、风险、信息缺口。
- `project`：目标场景、功能边界、架构、依赖、许可证、安装运行、测试复现、成熟度、安全隐私风险、团队改造成本。
- `doc`：适用版本、前置条件、核心概念、步骤/API/命令/配置、示例、约束、排错、项目关系。
- `experiment`：目标、假设、成功标准、变量和对照、环境、代码 commit、数据/模型、结果、异常、结论、产物、下一步行动。
- `meeting`：时间、参会人、议题、讨论分歧、决定、行动项、风险阻塞、开放问题、项目页更新建议。
- `codebase`：仓库目标、入口、目录结构、核心模块、数据流/调用链、环境配置、外部服务、运行测试、复现风险、改造建议。
- `note`：产生背景、触发材料、核心想法、依据、假设、不确定点、关联知识、可执行下一步、待验证问题。

## 保存文档

保存前先查重：

```bash
python3 scripts/check_duplicate.py --owner <owner> --repo <repo> \
  --title "<标题>" --source_id "<source_id>" --source_path "<source_path>"
```

确定重复时询问是否覆盖；疑似重复时询问是否继续保存。

```bash
python3 scripts/save_document.py \
  --owner <kb_owner> --repo <kb_repo> \
  --title "<标题>" \
  --summary_file /tmp/paperkb/draft_summary.md \
  --type_key meeting \
  --brief "<一句话简介>" \
  --keywords "关键词1,关键词2" \
  --scope team \
  --team_id <team_id> \
  --project_id general \
  --people "张三,李四" \
  --source_file_path "<本地原始文件路径>"
```

`--source_file_path` 会把原始文档归档到 `source_files/`。
群聊入库时，把 `SenderId` 记录为操作者，把 `GroupSubject` 记录为来源群，把 `MessageSid` 记录为消息来源。

## 更新项目/人物页

```bash
python3 scripts/update_project_people.py \
  --owner <team_kb_owner> --repo <team_kb_repo> \
  --project_id <project_id> \
  --title "<资料标题>" \
  --doc_path "<save_document 返回 path>" \
  --people "张三,李四" \
  --timeline "<时间线事件>" \
  --decisions "<达成决定>" \
  --open_questions "<未解决问题>"
```

## 回复要求

回复必须说明：

- 存入个人库/团队库/双写
- 资料类型
- 所属项目
- 生成页面链接
- 更新了哪些项目/人物/概念页

所有链接都来自脚本返回的 Gitea URL。

## 脚本清单

- `ingest_one.py`：解析私聊/群聊目标知识库
- `chat_context.py`：解析 OpenClaw 群聊上下文和群绑定
- `resolve_target_action.py`：解析入库目标选择卡片按钮
- `render_summary_template.py`：输出不同资料类型的结构化 summary 模板
- `summary_templates.py`：维护资料类型模板和生成规则
- `check_duplicate.py`：单条入库查重
- `resolve_duplicate_action.py`：解析重复资料处理卡片按钮
- `save_document.py`：保存 summary 和原始文件
- `save_page.py`：保存概念/资源/人物等聚合页
- `update_project_people.py`：更新团队项目和人物聚合页
- `cards.py`：生成飞书互动卡片 payload
