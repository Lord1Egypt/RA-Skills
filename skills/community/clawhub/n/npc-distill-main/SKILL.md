---
name: npc-distill
description: 构建特定人物(上级/合作伙伴/客户)的本地数字分身,辅助汇报演练、风格化起草、决策预判。当用户粘贴某人物的发言、邮件、聊天记录、会议纪要、批注,或提供包含其内容的网页URL,或说出"投喂语料""练习汇报""模拟 NPC 反应""按X总风格起草""预演一下""数字分身""人格画像""压力测试我的方案"等意图时,自动启用本Skill。所有数据存储在本地单一memory文件中,人物使用代号(L001/L002)而非真名,适合开源场景与高隐私要求。兼容Claude Skills/Hermes Agent/LobsterAI/OpenClaw等所有遵循 agentskills.io 标准的Agent。
version: 0.2.2
author: open-source-community
license: MIT
homepage: https://github.com/clawhub/npc-distill
platform: any
---

# NPC Distill

> 把零散的 NPC 语料,蒸馏成可演练的数字分身。

## When to Use

启用本Skill的明确信号(任一即触发):

- 用户粘贴一段文字,提到这是 X 说的/写的/批注的
- 用户给出 URL,说想分析里面 X 的发言/观点
- 用户说要"练习汇报""模拟反应""压力测试方案""预演一下"
- 用户说要"按 X 的风格"起草内容
- 用户问"X 的画像""X 在意什么""X 的雷区"
- 用户主动说"启用 npc-distill"或"打开蒸馏工具"

不要触发的场景:

- 用户只是讨论领导力理论、管理学概念
- 用户让你扮演一个虚构角色(那是角色扮演,不是蒸馏)
- 用户问关于已故公众人物的事实(那是百科查询)

## Quick Reference

```
存储:    ~/npc-distill/memory-{npc_id}.md  (单文件,纯Markdown)
代号:    L001, L002, L003... (永远不要写真名)
脚本:    scripts/*.py (纯Python,需要 pyyaml + Python 3.9+)
模板:    templates/*.md (5个工作流)
```

5 个核心工作流(按用户意图加载对应模板):

| 用户意图 | 加载 | 输出 |
|---------|------|------|
| 投喂文本 | `templates/ingest-text.md` | 解析→展示→入库 |
| 投喂URL | `templates/ingest-url.md` | 抓取→筛选→入库 |
| 压测方案 | `templates/rehearse-pressure.md` | 5个尖锐提问 |
| 演练对话 | `templates/rehearse-dialogue.md` | 多轮角色扮演 |
| 起草内容 | `templates/draft-with-critique.md` | 初稿+自我批判+定稿 |

## Prerequisites

- **Python 3.9+**
- **pyyaml**: `pip install pyyaml>=6.0`

## 错误处理

| 情况 | 处理 |
|------|------|
| 用户粘贴的文本里没识别出明显说话人 | 询问"这段是 L001 说的全部,还是其中部分?" |
| 文本超长(>5000 字) | 提示"内容较多,我拆成几段逐一确认" |
| 文本含他人隐私(电话/账号/身份证) | 警告并询问是否要脱敏 |
| 用户中途改主意 | 不写入任何文件,清空临时抽取结果 |
| `update_memory.py --signals` 生成骨架条目（scene/channel=未知, weight=1.0, 无内容/判断） | **绕过脚本,手动 patch**: 用 patch 工具将骨架行替换为完整内容。参见下方"已知局限" |

## 已知局限

### 1. `update_memory.py --signals` JSON 解析不完整

**症状**: 传入结构完整的 signals JSON 后,脚本只提取了 date/attribution/weight,`scene`,`channel`,`tags`,`场景背景`,`内容`,`抽取信号`,`我的判断`等字段全部丢失：
```
## C-20260521-005 · (未命名)

- date: 2026-05-21
- scene: 未知
- channel: 未知
- attribution: paraphrased
- weight: 1.0
```

**根因**: `update_memory.py` 的 `--signals` 解析器只读取 signals JSON 的顶层字段,未展开 `corpus` 子结构。

**解决方案**: 不用 `--signals`,直接通过 `patch` 或 `write_file` 手动追加 corpus 条目到 `# 语料库` 区域。步骤：
```
1. 用 read_file 确认当前最后一个 corpus 条目和格式
2. 用 patch 将新条目追加到合适的顺序位置
3. 更新 YAML frontmatter 中的 evidence_count、updated 日期
4. 更新 画像综述 中的 evidence_count 引用（脚本通常不同步这里）
```

### 2. 画像综述 evidence_count 不同步

`update_memory.py` 更新 frontmatter 中的 `evidence_count`,但不更新 `# 画像综述` 概要行中的数字（例如 `evidence_count = 2` 停留在初始值）。每次 add_corpus 后需手动修正概要行。用 `patch` 搜索 `>` 号 + evidence_count 关键词定位。

### 3. corpus 名称字段（`· 标题`）不被脚本填充

`--signals` JSON 中的 `corpus.scene` 被忽略,条目显示为 `C-20260521-005 · (未命名)`。手动修改为有意义的中文标题。