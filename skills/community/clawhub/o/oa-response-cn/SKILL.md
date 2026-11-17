---
name: oa-response-cn
description: 中国专利审查意见答复（OA答复）。当用户收到审查意见通知书，要写意见陈述书、改权利要求、说「帮我答复这份审查意见」「这个 OA 怎么答」「审查员说没有创造性怎么办」「第二次审查意见」时使用。常见说法：「OA答复」「审查意见答复」「意见陈述书」「权利要求修改」。Use when the user needs to respond to a Chinese patent office action. Drafts the response statement, amended claims and an amendment comparison table (Word). Also covers office action response and CNIPA examination opinions.
version: "1.0.8"
author: PatentMax
user-invocable: true
argument-hint: "[审查意见通知书 / 申请文件的路径]"
allowed-tools: Bash, Read, Write, Glob
---

# OA答复 · PatentMax

给审查意见通知书和申请文件，生成**中国专利审查意见答复**：意见陈述书、修改后的权利要求书、修改对照表，都是 Word。对比文件不用给，系统按通知书里的公开号自己去取。

**中途停两次，由你拿主意**：分析完给出 2～3 个答复策略让你选；权利要求改完先给你看、可以直接改，确认了才写意见陈述书。不想被问就说「按推荐来」，一次跑完。

使用问题、企业采购：访问 **ip930.com**，右下角「联系客服」。

**不需要 API Key 就能用。**

## 运行环境（必读，所有命令都适用）

部分 WorkBuddy 等环境的命令行不完整，`cat`、`ls`、`sleep`、`rm` 等可能找不到。为保证任何电脑都能跑通：

- 脚本路径一律写**绝对路径**：`$DIR/scripts/patentmax_oa.py`（`$DIR` 是本技能所在目录），不要写 `cd ... && ...`
- `python` 找不到时依次试 `python3`、`py`；还找不到就用 WorkBuddy 自带的：先用 Glob 在 `~/.workbuddy/binaries/python/versions/` 下找到 `python.exe`，用它的完整路径。**下文所有 `python` 都按这条替换**
- 不要用 `cat` 读文件、不要用 `sleep` 等待：读文件用 Read 工具；等待由脚本自己完成
- 命令在**用户的工作目录**里运行，生成的 Word 存到这个目录；也可以用 `--out-dir` 指定
- 命令超时设为 120 秒。脚本每条命令最多跑 30 秒就返回，不会卡住

## 核心原则

**只支持中国专利申请。** 美欧日等外国审查意见不要提交。

**材料要全文。** 审查意见通知书、申请文件（权利要求书 + 说明书）都要原文，不要摘要；漏了说明书，系统找不到修改依据。

**这是付费任务（¥15 一份，中途确认不另收费），执行前必须取得用户同意。** 命令必须显式加 `--yes`。

**策略和权利要求由用户决定。** 你负责把选项讲清楚，不替用户选、不替用户改。用户的调整意见**原话**转交（`--note`、改后的权利要求文件），不加工、不润色。

**不重新提交。** 跑得久不代表失败，只要没报错就继续 `wait`；对话断了、重开了，用同一个 `operation_id` 接着看。重新提交会新建任务、重复扣费。

## 什么时候用

| 用户说 | 怎么做 |
| --- | --- |
| 「帮我答复这份审查意见」「这个 OA 怎么答」 | ✅ 用 |
| 「审查员说没有创造性，怎么改权利要求」 | ✅ 用 |
| 「收到第二次审查意见通知书了」 | ✅ 用，材料里带上这一次的通知书；**权利要求书要用上一次答复后的版本**（见第 1 步） |
| 「美国 / 欧洲的 Office Action」 | ❌ 目前只支持中国申请 |
| 「帮我写专利」「写交底书」 | ❌ 用技术交底书 / 专利初稿 |
| 「看看这篇对比文件讲了什么」 | ❌ 用全球专利检索的单篇速览 |

## 用示例材料演示

用户说「用示例材料演示」「先试一下看看效果」，或者手上没有审查意见只想看看能做出什么时，用技能自带的虚构演示案例：审查意见通知书 `$DIR/references/demo-office-action.md`、申请文件 `$DIR/references/demo-application.md`（水渠闸门自动除冰装置，对比文件 CN118166723B、CN109706897B 为真实公开专利，系统会自动获取）。提交前告诉用户：这是虚构的演示案例，照常收费，生成的文件仅供体验。用户说「按推荐来、不用问我」时加 `--auto`。

## 第 1 步：收齐材料

| 材料 | 必须吗 | 说明 |
| --- | --- | --- |
| 审查意见通知书 | 必须 | 全文，含审查员引用的对比文件公开号 |
| 申请文件 | 必须 | 权利要求书 + 说明书全文（可以是一个文件，也可以分开给） |
| 第二次及以后的通知书 | 注意版本 | **权利要求书必须是上一次答复后的版本**，说明书用原始申请的（修改依据以原始公开为准）。用户只给了原始申请文件时先问一句：「之前答复时改过权利要求吗？改过的话请给我改后的那版。」拿原始版去答，改的是已经失效的权利要求 |
| 对比文件 | 可选 | 不给就按通知书里的公开号自动取；用户手上有原文时给上更准（文件名带公开号，如 `CN109761224A.docx`） |

上一次的意见陈述书目前**不要**混进 `--application` 交上去，系统会当成申请文件的一部分。

`.docx` / `.txt` / `.md` 直接交给脚本。**PDF、扫描件、图片脚本读不了**：由你先读出全文，存成 `.txt` 再交。

## 第 2 步：确认后提交

先用一条消息列给用户确认（不花钱）：

```
📋 准备答复审查意见
- 案件：……（申请号 / 名称）
- 审查意见：第 N 次，主要理由……（一两句）
- 权利要求版本：原始申请 / 第 N 次答复后（第二次及以后的通知书必须是上次答复后的版本）
- 材料：通知书 ✓ 申请文件 ✓ 对比文件（自动获取 / 已提供 N 篇）
- 费用：¥15（中途确认不另收费；失败或取消全额退回）
- 流程：分析约 2～3 分钟 → 你选策略 → 改权利要求约 1 分钟 → 你确认 → 写意见陈述书约 1 分钟
```

用户回「确认」后运行：

```bash
python "$DIR/scripts/patentmax_oa.py" create --office-action "<绝对路径>/审查意见通知书.docx" --application "<绝对路径>/申请文件.docx" --title "案件简称" --yes

# 用户明确说「不用问我、按推荐来」时才加 --auto，一次跑完
python "$DIR/scripts/patentmax_oa.py" create --office-action "…" --application "…" --auto --yes
```

## 第 3 步：等待并报告进度

```bash
python "$DIR/scripts/patentmax_oa.py" wait --operation-id <operation_id>
```

| 退出码 | 含义 | 怎么做 |
| --- | --- | --- |
| 10 | 还在生成 | 发送输出里的进度，**然后立即再运行一次 `wait`** |
| 20 | 停下来等用户拿主意 | 按第 4 步 / 第 5 步处理 |
| 0 | 完成了 | 按第 6 步交付 |
| 1 | 出错 | 按「出错时」处理 |
| 2 | 输入有误，什么都没提交 | 按 `message` 补齐后再运行 |
| 3 | 同样的任务已经在跑 | 用输出里的 `operation_id` 运行 `wait`，**不要**换写法重新提交 |

进度照原文发，加图标：`[进度] 已开始……` → 🚀；`[进度] 排队中……` → 🕒；`[进度 X%] 某阶段，已用时……` → 📝 X% 某阶段，已用时……。等待期间只发进度，不加别的话、不自己估剩余时间；出结果前不要结束回复。

记下 `operation_id`，不主动展示给用户，用户问起再给。

## 第 4 步：选答复策略（退出码 20，`type` = `select_strategy`）

用大白话把每个策略讲给用户，**由用户来选，不要替他决定**：

```
审查员的主要理由：……（examiner_flaws 里有审查员说得不对的地方，一并说）
区别特征：……（distinguishing_features，一两句）

A. 〈title〉（改动程度：amendment_level）—— 怎么改：amendment_summary；主要理由：core_arguments；风险：weaknesses
B. ……
推荐 〈recommended〉：recommendation_reason
```

有 `divisional_suggestion`（分案建议）时也讲一句，问用户要不要。有 `evidence_needed` 时提醒用户要准备什么证据。完整内容在 `details_file`，用户想细看再读。

用户选定后：

```bash
python "$DIR/scripts/patentmax_oa.py" strategy --operation-id <operation_id> --choose A
# 用户有调整意见（原话）、或不要分案时
python "$DIR/scripts/patentmax_oa.py" strategy --operation-id <operation_id> --choose B --note "用户原话" --no-divisional
```

## 第 5 步：确认修改后的权利要求（退出码 20，`type` = `confirm_claims`）

**把 `claims_text` 全文原样贴给用户**（用户要逐条核对），再用几句话讲 `amendment_summary`、每条改了什么（`amendment_rows`：合并了哪几项、修改依据），以及 `checks` 里的校验提示。问用户：原样确认，还是要改？

```bash
# 原样确认，开始写意见陈述书
python "$DIR/scripts/patentmax_oa.py" claims --operation-id <operation_id>

# 用户改了文字：把改后的全文（按「1. ……」逐项一行）写进文件，先校验
python "$DIR/scripts/patentmax_oa.py" claims --operation-id <operation_id> --file "<绝对路径>/改后的权利要求.txt" --check
# 校验结果给用户看，同意后确认
python "$DIR/scripts/patentmax_oa.py" claims --operation-id <operation_id> --file "<绝对路径>/改后的权利要求.txt"
```

两个确认点都要讲：超过 `expires_at` 不回复，任务会自动取消并全额退款。

## 第 6 步：交付（退出码 0）

按顺序发送：

```
✅ 100% 审查意见答复已生成
```

然后**把 `statement_text`（意见陈述书全文）原样贴出来**，不改字、不删减、不总结。

全文下面列出 Word 文件：

```
📄 Word 文件（已保存）：
- 意见陈述书：<files 里的路径>
- 修改后的权利要求书：<路径>（没改权利要求时没有这一份）
- 修改对照表：<路径>
```

`internal_files` 里的「复核提示」是给你和用户内部核对的，**不要提交给审查员**，提一句即可。有 `evidence_needed` 时提醒用户准备。

最后一句固定是：

> 递交前请专利代理师复核。在 https://api.ip930.com 控制台可以查看所有任务和余额。

**以上是本轮最后的输出，发完就停**：之后不再调用工具、不补表格、不写总结，等用户回复。

## 出错时

脚本出错时输出 `{"error": true, "message": "……"}`，`message` 是写给用户看的中文说明，里面已经写明了下一步怎么办。

- **原样转述 `message`，不猜原因、不补充建议、不自己换写法重试**
- 退出码 2：什么都没提交、没扣费，按 `message` 补齐后再运行
- 第一次运行时输出里有「[PatentMax] 已自动领取免费试用……」：把这句话原样转告用户一次
- 出现 `"free_trial": true`：免费试用用完、过期或想用其他功能，`message` 里写着怎么办（注册 PatentMax 再送 ¥50 体验额度），原样转告
- 任务失败或取消时，预扣的费用会**全额退回**，告诉用户这一点

## 它不做什么

**不保证授权。** 答复是否被接受由审查员决定；递交前请专利代理师复核。

**只支持中国专利申请**，不做美欧日等外国 OA、复审、无效。

**材料会发送到服务端处理。** 涉及保密内容时提醒用户一句。

## 相关能力

同一把正式密钥、同一个余额（免费试用只开通 OA答复，其他功能要注册后用正式密钥）：

- **全球专利检索**：看对比文件讲了什么、找更多现有技术
- **专利查新**：改完的方案还有没有人做过
- **技术交底书 / 专利初稿**：新申请从这里开始
