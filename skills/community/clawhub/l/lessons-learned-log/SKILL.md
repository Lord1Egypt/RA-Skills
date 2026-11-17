---
name: lessons-learned-log
description: "踩坑记录——把出错、返工、被纠正的经历记成可检索的条目，做类似任务前先按关键词查一遍，避免同一个坑踩两次。当用户说「记一下这个坑」「以后别再犯这个错」「开工前先查查踩过的坑」「整理踩坑记录」时使用。"
author: Captain
version: 0.1.0
display_name: "踩坑记录"
display_name_en: "Lessons Learned Log"
description_zh: "踩坑记录：出错、返工、被纠正后，按现象、根因、正确做法、触发场景、验证方式记一条，存成按主题分文件的 Markdown；开工前用附带的 Python 标准库脚本按关键词检索；定期合并重复、淘汰过时条目。适用于 AI 助手，也适用于个人工作笔记。"
description_en: "Turn every mistake, rework or correction into a searchable lesson entry in plain Markdown, search it by keyword before similar tasks with a bundled standard-library Python script, and periodically merge or retire stale entries."
tags:
  - "踩坑记录"
  - "踩坑"
  - "避坑"
  - "经验教训"
  - "错题本"
  - "复盘笔记"
  - "lessons learned"
  - "mistake log"
examples_zh:
  - "刚才你把文件路径写错了，记一下这个坑，以后别再犯"
  - "开始写这份周报前，先查查我们以前踩过哪些坑"
  - "踩坑记录攒了几十条，帮我合并重复的、清理过时的"
---

# 踩坑记录

定位一句话：**记录本身不值钱，开工前真的去查才值钱。** 把每次出错、返工、被纠正变成一条下次能搜到、能照做的记录。适用于 AI 助手的长期协作，也适用于人自己的工作笔记。

## 什么时候必须记、什么时候先查

出现下面任何一种，当场记一条，不等「有空再整理」：

1. 被用户纠正：「不对」「我之前说过」「不是这个意思」；
2. 返工：交出去的东西被退回重做；
3. 报错或卡住超过 10 分钟，最后找到的原因并不显而易见；
4. 说错了事实：把推测当结论，被指出没有依据；
5. 差点出事：发错对象、删错文件、覆盖了别人的版本，哪怕及时拦住了；
6. 同一个问题第二次出现——第一次没记，第二次必须记。

不用记：纯手滑的错别字、一次性且不会再遇到的环境问题、总结不出可照做动作的事。

先查的时机：开始一项以前做过同类的任务之前；执行发送、删除、覆盖、付款这类不可撤销的动作之前；用户提到「上次那个问题」时。

## 条目格式与存放位置

一坑一条，以 `### ` 开头，字段各占一行，脚本按字段检索：

```markdown
### 交付文件只写了相对路径，用户找不到
- 关键词：路径, 文件位置, 交付, 链接
- 触发场景：把报告、表格、网页结果交给用户时
- 现象：用户回复「report.html 在哪？打不开」
- 根因：默认用户和我在同一个目录，实际不在
- 正确做法：交付物一律写完整路径，如 /Users/xiaowang/周报/report.html
- 验证方式：交付前把路径粘到文件管理器地址栏，能直接打开
- 类别：被用户纠正（第 2 次）
- 最后验证：2026-09-19
- 状态：有效
```

写法要求：现象写可观察的事实（原话、报错原文）；根因写「为什么会这样」，不写「粗心」；正确做法写成下次能照做的动作，带具体值；验证方式写怎么确认做对了；类别写被纠正、返工、报错或差点出事，括号里记第几次；状态只用「有效」「存疑」「已过时：原因」三种。

存放：纯文本 Markdown，放固定目录——个人用 `~/lessons/`，项目用项目根目录下的 `lessons/`。按主题分文件，如 `文件与路径.md`、`写作与格式.md`、`日程与时间.md`；新主题先放 `杂项.md`，攒够 5 条再拆出去；单个文件超过约 30 条再拆。

## 流程：开工前查，出错后记

把下面的脚本存成 `lessons_search.py`，只用 Python 标准库：

```python
"""按关键词检索踩坑记录；加 --stale 90 列出 90 天没复核的条目。"""
import argparse, datetime, pathlib, re

def entries(root):
    for f in sorted(pathlib.Path(root).expanduser().rglob("*.md")):
        text = f.read_text(encoding="utf-8", errors="replace")
        for block in re.split(r"(?m)^(?=### )", text):
            if block.startswith("### "):
                yield f.name, block.strip()

def field(block, name):
    m = re.search(r"(?m)^- %s[：:]\s*(.*)$" % name, block)
    return m.group(1).strip() if m else ""

ap = argparse.ArgumentParser()
ap.add_argument("root")
ap.add_argument("words", nargs="*")
ap.add_argument("--stale", type=int, help="只列最后验证早于 N 天的条目")
ap.add_argument("--all", action="store_true", help="连「已过时」的一起列")
a = ap.parse_args()
hits = []
for fname, block in entries(a.root):
    if "已过时" in field(block, "状态") and not a.all:
        continue
    if a.stale is not None:
        d = re.search(r"\d{4}-\d{2}-\d{2}", field(block, "最后验证"))
        age = (datetime.date.today() - datetime.date.fromisoformat(d.group())).days if d else 9999
        if age <= a.stale:
            continue
    key = (block.splitlines()[0] + field(block, "关键词") + field(block, "触发场景")).lower()
    score = sum(block.lower().count(w.lower()) + 2 * key.count(w.lower()) for w in a.words)
    if score or not a.words:
        hits.append((score, fname, block))
for score, fname, block in sorted(hits, key=lambda h: -h[0]):
    print(f"[{score}] {fname} | {block.splitlines()[0][4:]} | {field(block, '状态')} {field(block, '最后验证')}")
    print(f"    正确做法：{field(block, '正确做法')}")
    print(f"    验证方式：{field(block, '验证方式')}")
print(f"共 {len(hits)} 条" if hits else "没有相关记录")
```

开工前：

1. 从任务里抽 3–5 个关键词：对象（周报、表格）、动作（导出、发送、覆盖）、环境（macOS、Windows）。
2. 运行 `python3 lessons_search.py ~/lessons 路径 交付 周报`。方括号里是得分，命中标题、关键词、触发场景的会额外加分。
3. 把命中条目的「正确做法」写进本次计划，逐条当检查项执行；没命中也要说一句「已查踩坑记录，无相关条目」。

出错后：

1. 先解决问题，再按格式写一条，放进对应主题文件；
2. 写之前用同样的关键词查一次：已有同根因的条目就更新它（类别里的次数加一、补充现象、改最后验证日期），不另开新条；
3. AI 助手第一次在用户电脑上建记录目录前，先问一次存放位置；不能写文件时，把整条输出给用户自己保存。

## 定期合并与淘汰

每月一次，或每新增 20 条做一次：

1. 运行 `python3 lessons_search.py ~/lessons --stale 90`，列出 90 天没复核的条目；
2. 逐条判断：仍然成立的改「最后验证」日期；工具或流程已变的，状态改成「已过时：原因」——不删除，脚本默认不再列出，加 `--all` 才显示；
3. 合并同根因的条目：现象合并列出，次数相加，保留写得最具体的那条正确做法；
4. 同一个坑出现 3 次以上，说明光记录不够，把它升级成固定规则，写进工作规范或助手的常驻指令。

## 最常见的错误

- 只写现象不写根因：「导出失败了」——下次还是不知道怎么办。
- 正确做法写成态度：「以后注意」「要细心」不是做法。
- 不写触发场景和关键词：记了但永远搜不到。
- 一条里塞三个坑：命中后分不清哪句有用，拆开写。
- 只记不查：开工前从不打开，等于没记。

## 输出契约

- 记录时：交付完整条目（现象、根因、正确做法、触发场景、验证方式五项必填）和写入文件的完整路径；更新已有条目时说明改了哪几行。
- 查询时：交付所用关键词、命中条目（标题 + 正确做法）、据此加进计划的检查项；无命中明确说「已查踩坑记录，无相关条目」。
- 复核时：交付过期条目清单与每条的处理结果（续期 / 已过时 / 合并）。

## 边界与不做什么

- 记事不记人：不写对任何人的评价；不写密码、账号、身份证号等敏感信息——记录会长期保存，也可能被分享。
- 不代替事故复盘：造成实际损失的事件走单位的复盘流程，这里只沉淀可复用的做法。
- 记录是参考不是命令：旧条目可能已过时，与用户当前的明确要求冲突时，以用户当前要求为准，并指出冲突。
- 不擅自改用户文件：新建目录、写入或合并记录，按用户约定的位置进行；没约定就先问。
