# 识字与诗歌练习页 · 脚本参数与组卷配方

脚本路径：`C:\Users\李玉明\.workbuddy\skills\kindergarten-chinese-course\scripts\generate_worksheet.py`
（Windows 下 Python 不可用时改用 `C:\Users\李玉明\.workbuddy\binaries\python\versions\3.13.12\python.exe`）

## 参数说明

| 参数 | 说明 | 默认值 |
|---|---|---|
| `--level` | 等级 L1-L4 | L1 |
| `--count` | 汉字题量；仅诗歌题型时表示诗歌数量（上限 3） | 0（按等级默认：L1=8,L2=10,L3=12,L4=12） |
| `--topics` | 指定题型，逗号分隔；拼错会列出合法值；会限定到本等级可用题型 | 空（按等级默认题型） |
| `--seed` | 随机种子；相同 seed 复现同一套题；不指定则每次随机 | 随机 |
| `--name` | 孩子姓名（可预填）；不填则页眉留空下划线框，打印后手填 | 空 |
| `--no-name` | 强制姓名栏空白；忽略 `--name` 与 `--regen` JSON 里的旧姓名 | 关 |
| `--columns` | 认字/描红网格列数 1-6 | 4 |
| `--no-answers` | 不输出答案页 | 关 |
| `--lang` | 界面语言 `zh` / `en` | zh |
| `--score` | 页尾显示评分栏（得分/正确数/日期/评语，打印后手填） | 关 |
| `--out` | 生成的 HTML 路径（必填） | — |
| `--json` | 元数据 JSON 路径（必填，复现用） | — |
| `--regen <json>` | 从旧 JSON 复现原套题（用其存储的 seed/level/lang/name/count/topics） | — |
| `--list` | 列出所有题型与等级映射、诗歌池后退出 | — |

## 支持的 topic
`recognize` 看图认字 · `trace` 描红 · `poem` 古诗/儿歌 · `word` 组词 · `fill` 古诗填空

## 常用组卷配方

```bash
# 1) 标准 L2 综合卷（认字+描红+古诗），带评分栏
python generate_worksheet.py --level L2 --topics recognize,trace,poem --seed 7 --score \
  --out 识字_L2.html --json 识字_L2.json

# 2) 专练描红 + 认字（L1，字少图大）
python generate_worksheet.py --level L1 --topics recognize,trace --count 8 \
  --out 识字_L1_描红.html --json 识字_L1_描红.json

# 3) 古诗填空默写（L4）
python generate_worksheet.py --level L4 --topics fill --seed 3 \
  --out 古诗填空_L4.html --json 古诗填空_L4.json

# 4) 组词练习（L3）
python generate_worksheet.py --level L3 --topics word --count 10 \
  --out 组词_L3.html --json 组词_L3.json

# 5) 一键复现原套题
python generate_worksheet.py --regen 识字_L2.json --out 识字_L2_复现.html --json 识字_L2_复现.json

# 6) 浏览题型×等级映射与诗歌池
python generate_worksheet.py --list
```

## 版式规范
- 纸张：A4，页边距 14mm；`print-color-adjust:exact` 已开启，无需手动勾选「背景图形」。
- 卡片：圆角卡片，`break-inside:avoid` 避免跨页断裂。
- 列数：默认 4 列；`--columns 1` 给大字号/低视力，`--columns 6` 提密度。
- 一次默认一份练习；诗歌单次 ≤ 3 首。
- 答案页另存为 `<json名>_答案.html`。

## 元数据 JSON 结构
```json
{
  "level": "L2",
  "level_age": "中班 4-5 岁",
  "name": "",
  "lang": "zh",
  "count": 0,
  "seed": 7,
  "topics": ["recognize","trace","poem"],
  "chars": ["日","月","水","火"],
  "poems": ["咏鹅"]
}
```
批改古诗填空时对照答案页（含全诗原文），不要凭记忆重填。

## 扩展题型
新增题型：在 `generate_worksheet.py` 的 `ALL_TOPICS` / `LEVEL_TOPICS` / 数据区登记，并实现 `build_xxx()` 与 `render()` 中的分支即可，无需改动调用入口。
