# 🇨🇳 中文翻译层说明（供自动化/同事参考）

邮件看板的「中文摘要翻译」模块靠一份 `workboard2_cn.json` 词典驱动。
生产这份词典分三步，前两步由 `daily_mail_board.py` 自动完成，第三步需要一次 LLM 翻译。

## 数据流

```
daily_mail_board.py（拉邮件后自动跑）
   └─ prep_cn.py        → cn_inbox_full.json   全量线程 + 清洗正文（fresh ≤1100 字）
        └─ build_cn_inbox.py → cn_inbox.json   每店筛「含 DDL 或近 14 天活跃」、上限 6
              └─ LLM 翻译    → workboard2_cn.json   ← 看板与飞书摘要消费
```

## 三步操作

```bash
# 1) 导出待译清单（精简，默认 cn_inbox.json；--full 用全量）
python cn_translate.py              # 打印待译清单
python cn_translate.py --full       # 全量（含其他待办 / 西葡）

# 2) 交给 LLM 翻译，产出「译文.json」，结构如下：
#    { "stores": { "Cologne": { "<thread_id>": {"summary": "...", "todos": ["..."], "risk": "..."} } } }

# 3) 校验并合并译文
python cn_translate.py --apply 译文.json
python cn_translate.py --show       # 查看当前词典概况
```

## 翻译规则（务必遵守）

每条线程输出三个字段，全部中文：

| 字段 | 含义 | 要求 |
|------|------|------|
| `summary` | 邮件沟通事项归纳 | 一段话，说清「谁 → 谁，沟通了什么事」，只显示发件人+收件人（抄送不显示） |
| `todos` | 待办事项 | 数组，逐条可执行；含日期/截止时写清楚 |
| `risk` | 风险提示 | 一句话；无风险可省略该字段 |

硬性规则：
- **方向语义**：A→B 说「我要休假」= **A** 休假（不是 B）。
- **删问候/落款**：只保留实质信息。
- **OOO 自动回复**：summary 注明「自动回复」，todos 给空数组，risk 注明休假区间/紧急联系方式。
- **不虚构**：正文没写的内容不要编造；拿不准就用英文原文关键词兜底。
- 同一 `thread_id` 只保留一条（跨 DREAME/MOVA 子目录重复时去重）。
- 若某线程已在 `workboard2_cn.json` 中且内容未变，可跳过（`--apply` 会保留旧译文）。

## 译文示例

```json
{
  "stores": {
    "Dusseldorf": {
      "OGY0MGFjMWYt...": {
        "summary": "杜塞旗舰店招标——ISI Global（Bartek）确认收到招标邀请，询问可进场施工日期、对接人及楼层。",
        "todos": ["回复 ISI Global 可进场日期/对接人/楼层", "8/21 前完成报价评审准备"],
        "risk": "报价截止 8/21 临近"
      }
    }
  }
}
```
