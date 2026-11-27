# 端到端结果示例（用户说什么 → 助手怎么做 → 返回什么 → 落盘什么 → 怎么转述）

> 用途：让 Agent 知道"成功长什么样"、按什么结构向用户汇报。**字段名取真实返回，数值/题名均为示意**；
> 所有价格位一律写 `<实时报价>`，不得填具体数字（见 SKILL.md §七价格准则）。
> 落盘目录细则见 `artifacts.md`；每段对话结束的三段式汇报见 SKILL.md §八。

---

## 示例 1 · 中英文并行检索（最常用）

**用户说**：「帮我找近三年医学影像深度学习的中文核心期刊文献，能下全文的优先」

**助手调用链**：
```
owl.py quote --action search --params '{"query":"医学影像 深度学习","years":3,"core_only":true}'  # 先报价
owl.py run --quote <quote_id> → owl.py wait <run_id> --timeout 120 → owl.py report <run_id>
```

**返回结构（示意）**：
```json
{
  "run_id": "run_9f3c...",
  "status": "ok",
  "items": [
    {"title": "基于深度学习的医学影像分割研究", "doi": "10.xxxx/yyyy",
     "source": "cncore", "year": 2024, "fulltext_available": true}
  ],
  "points_charged": <实时报价返回的扣点>,
  "balance_avail": <owl_wallet 返回值>
}
```

**落盘**：`OwlWrite/02-文献/search-<run_id>.json`（命中题录），有全文的 PDF 进 `02-文献/fulltexts/`（需另调 `owl_fulltext`，实时报价）。

**给用户的话术**：
> 找到 N 篇（中文核心 M 篇，其中 K 篇可取全文）。题录已存 `02-文献/search-<run_id>.json`。本次检索扣 <points_charged> 点，余额 <balance_avail> 点。要哪几篇的全文 PDF，我按实时报价取直链。

**要点**：默认双路并行；`core_only=true` 只走核心刊；无结果不收费、换词重试；不要报具体单价。

---

## 示例 2 · 论文写作（后计价）

**用户说**：「写一篇 8000 字综述，题目是人工智能在医学影像诊断中的应用」

**助手调用链**：
```
owl.py quote --action write --params '{"title":"...","mode":"standard","words":8000}'  # 给预估区间
owl.py run --quote <quote_id> → owl.py wait <run_id> --timeout 120（没结束自动再查，不重复下单）
owl.py content <run_id> --save draft.md → owl.py report <run_id>
```

**返回结构（示意）**：`run_id`、`status=ok`、`word_count=8xxx`、`points_charged`（按实际成文字数结算，与报价一致）、`balance_avail`。

**落盘**：`OwlWrite/03-稿件/正文-draft1.md`（只增不覆盖）、`references.md`，参考文献并入 `02-文献/references.csv`。

**给用户的话术**：
> 初稿 8xxx 字已写到 `03-稿件/正文-draft1.md`，参考文献并入 `references.csv`。本次按实际字数扣 <points_charged> 点，余额 <balance_avail> 点。这是辅助草稿，请你核对文献与数据后用自己的语言定稿。

**要点**：报价是预估区间、结算按实际字数；写作无缓存；不承诺可直接提交。

---

## 示例 3 · 查重检测

**用户说**：「帮我查这篇论文的重复率」

**助手调用链**：
```
owl.py quote --action detect --params '{"product":"<owl_products 返回的查重品名 id>"}'  # 先报价
owl.py upload 论文.docx → 拿 file_id
owl.py run --quote <quote_id>（params 带 file_id）→ owl.py wait <run_id> → owl.py report <run_id>
```

**返回结构（示意）**：`run_id`、`status=ok`、报告下载链接、`points_charged`、`balance_avail`。

**落盘**：`OwlWrite/05-检测/<品名>-<日期>/` 下的官方报告。

**给用户的话术**：
> 查重报告已出（<品名>），存在 `05-检测/<品名>-<日期>/`，可在维普验真平台核验。本次扣 <points_charged> 点，余额 <balance_avail> 点。报告我帮你解读：重复集中在哪几段、哪些需要你自己重写——但我不能帮你改写降重。

**要点**：品名编码只做参考、真值取 `owl_products`/`owl_quote` 实时返回；检测失败自动退点。

---

## 示例 4 · 引文核验 + 撤稿把关

**用户说**：「交稿前帮我看看这些引用靠不靠谱」

**助手调用链**（本技能内置，不转介其他技能）：
```
owl.py quote --action verify --params '{"refs":[...]}' → owl.py run --quote <quote_id>
owl.py report <run_id> --part simple
```

**返回结构（示意）**：逐条状态——
```
[1] VERIFIED        标题/年卷期与官方记录一致，附原始记录链接
[2] METADATA_MISMATCH  刊名或年份对不上：<用户填的> ≠ <官方记录>
[3] SUSPECT         检索不到匹配记录
[4] NOT_FOUND       无记录（不等于造假，可能本库未收录）
撤稿标记：retraction=<状态>
```

**落盘**：`OwlWrite/06-核验/` 报告；回写 `references.csv` 的 `verified` 列。

**给用户的话术**：
> N 条引文核完：M 条一致、K 条元数据对不上、J 条查无记录，其中 X 条有撤稿标记，都在 `06-核验/` 报告里，`references.csv` 的 verified 列也更新了。本次扣 <points_charged> 点。查无记录只代表本库未收录，建议再核对原始文献。

**要点**：撤稿库"无记录"≠安全；逐条核验按条计费（缓存价更低），定稿整体把关用参考文献质量检测（按篇）。

---

## 示例 5 · 专利查新（CLI/HTTP 专属）

**用户说**：「查这个技术方案的新颖性，出一份专利查新报告」

**助手调用链**：
```
owl.py patent --action patent_search --query "..."         # 秒级检索，先探现有专利
owl.py patent-report --op submit --type novelty --title "..." --input '{...}'  # 提交报告（按篇实时报价）
owl.py patent-report --op status --report_id <id>          # 轮询（每账号同时只跑一个）
owl.py patent-report --op download --report_id <id>
```

**返回结构（示意）**：`report_id`、`status`、`report_type=novelty`、Word 下载链接、`points_charged`（按篇精确冻结）、`balance_avail`。

**落盘**：`OwlWrite/07-专利/<类型>-<日期>/` 报告原件。

**给用户的话术**：
> 查新报告（<标题>）已生成并下载到 `07-专利/novelty-<日期>/`，可在报告里看现有专利对比与新颖性判断。本次按篇冻结扣 <points_charged> 点，余额 <balance_avail> 点。查新结论不等于授权前景保证，正式申请请咨询代理师。

**要点**：**没有 `owl_patent` 这个 MCP 工具**，专利只走 CLI/HTTP；失败不收费、24 小时超时自动全退；创新升级交付结构化清单而非 Word。

---

## 示例 6 · 排版导出 PDF

**用户说**：「把我这份 Word 按学校模板排成能提交的 PDF」

**助手调用链**：
```
owl.py quote --action typeset --params '{"mode":"docx","template":"学校模板.docx"}'  # 先报价
owl.py upload 论文.docx → owl.py run --quote <quote_id> → owl.py wait <run_id>
owl.py report <run_id>   # 看 content_gaps
```

**返回结构（示意）**：`run_id`、`status=ok`、PDF 下载链接、`content_gaps=[]`（若有搬不过去的内容会列出）、`points_charged`、`balance_avail`。

**落盘**：`OwlWrite/08-排版/论文-<日期>.pdf`。

**给用户的话术**：
> 已按模板排好，PDF 在 `08-排版/论文-<日期>.pdf`。本次扣 <points_charged> 点，余额 <balance_avail> 点。<如有 content_gaps：有 N 处内容没搬过去，列在报告里，需要你决定怎么补。>

**要点**：只排格式不改内容、不编参考文献；72 小时内同一篇改格式重排按缓存价；内容搬不过去如实说。

---

## 汇报自检（每条都过一遍）

1. **积分账**：三段式（扣点 / 余额 / 进度）齐全，数字只从 `points_charged`、`balance_avail` 取，不估算、不推算。
2. **成果物**：列真实路径，写完回读确认存在；没落盘成功的不写进汇报。
3. **价格**：本文件所有 `<实时报价>` 位在真实回复里用工具返回值填，不得写死单价；`1 积分 = 0.01 元` 是唯一固定换算。
4. **网址**：一律裸写域名，不用 Markdown 链接语法。
