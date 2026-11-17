# 办公上下文管理 Playbook（增量信息）

> 本篇是 [skills/office-context/](../skills/office-context/SKILL.md) 的深层方法论：**怎么判断要不要建上下文、怎么采集、怎么注入、踩哪些坑**。
> 不重复子技能的能力列表，只写子技能装不下的决策与命令。

## 1. 决策树：这次要不要建上下文？

```
是否同一品牌 / 同一模板会重复产出？
├─ 否（一次性文档）            → 不建，直接在 md-to-office / ppt-automation 里手写参数
└─ 是
   ├─ 已有 assets/office-context.json？
   │  ├─ 是且 ≤90 天未变         → 直接读它注入
   │  └─ 是但已过期              → 走「季度复核清单」更新
   └─ 否                        → 走「品牌五件套采集」新建
```

判定信号：月度 / 周报、客户提案模板、公司对外材料、团队共享母版 → 建。
孤立的一次性笔记转 PPT → 不建。

## 2. 品牌五件套采集清单

采集时逐项向用户确认，**颜色务必要 HEX，不要 CSS 颜色名**（见踩坑 1）：

| 项 | 字段 | 示例 |
|----|------|------|
| 主色 | `primary` | `#1F4E79` |
| 辅色 | `secondary` | `#2E75B6` |
| 强调色 | `accent` | `#ED7D31` |
| 标题字体 | `heading_font` | `Microsoft YaHei` |
| 正文字体 | `body_font` | `Source Han Sans` |
| logo 路径 | `logo` | `assets/brand/logo.png` |
| Word 模板 | `reference_doc` | `assets/templates/report.docx` |
| PPT 母版 | `ppt_template` | `assets/templates/deck.pptx` |

## 3. 上下文文件 schema（`assets/office-context.json`）

> 直接复制 [assets/office-context.example.json](../assets/office-context.example.json) 作为起点，再填入你的品牌值，命名为 `assets/office-context.json`。

```json
{
  "brand": {
    "primary": "#1F4E79",
    "secondary": "#2E75B6",
    "accent": "#ED7D31",
    "heading_font": "Microsoft YaHei",
    "body_font": "Source Han Sans",
    "logo": "assets/brand/logo.png"
  },
  "templates": {
    "reference_doc": "assets/templates/report.docx",
    "ppt_template": "assets/templates/deck.pptx"
  },
  "skeletons": {
    "monthly_report": ["封面", "摘要", "指标", "分析", "下一步"],
    "proposal": ["问题", "方案", "报价", "案例"]
  },
  "updated": "2026-08-12"
}
```

> 路径用**相对仓库根**的写法，避免绝对路径在别的机器失效（见踩坑 2）。

## 4. 注入命令

**Word（Pandoc）**——用 reference-doc 携带品牌版式：

```bash
pandoc input.md -o out.docx \
  --reference-doc=assets/templates/report.docx \
  -V title-color=#1F4E79 -V fontfamily="Source Han Sans"
```

**PPT（python-pptx）**——读上下文套色（片段）：

```python
import json
from pptx import Presentation
ctx = json.load(open("assets/office-context.json"))
prs = Presentation(ctx["templates"]["ppt_template"])   # 母版带品牌色板
# 之后只填文字，配色由母版保证
```

**校验上下文没过期**：

```bash
python3 - <<'PY'
import json, datetime
c = json.load(open("assets/office-context.json"))
age = (datetime.date.today() - datetime.date.fromisoformat(c["updated"])).days
print("context age(days)=", age, "→ 需复核" if age > 90 else "OK")
PY
```

## 5. 踩坑清单

1. **颜色用 CSS 名而非 HEX**：`blue` 在不同渲染器下 RGB 不同，产出色板漂移。一律 HEX。
2. **模板用绝对路径**：`/Users/me/.../report.docx` 换机即失效。用相对仓库根路径。
3. **忘更新上下文导致旧版式**：品牌季更但上下文半年没动，产出还是老配色。设 90 天复核闹钟。
4. **把 `doc-style-rules.json` 当品牌库**：那是标题层级 / 结构门禁，不是色板。品牌单独存 `office-context.json`。
5. **母版缺失时硬套色**：没 PPT 母版就逐项改 shape 颜色，极易漏。优先提供 `ppt_template` 母版。

## 6. 检查清单

**新建项目上下文**
- [ ] 品牌五件套（HEX 色 ×3 + 字体 ×2 + logo）已采集
- [ ] `reference_doc` / `ppt_template` 路径可用且相对仓库根
- [ ] 常用骨架（章节顺序）已记录
- [ ] 已写入 `assets/office-context.json` 并 `git add`

**季度品牌复核**
- [ ] `office-context.json` 的 `updated` 是否 >90 天
- [ ] 主辅色 / 字体是否与当前 VI 一致
- [ ] 模板文件是否仍在原路径
- [ ] 更新 `updated` 字段并提交
