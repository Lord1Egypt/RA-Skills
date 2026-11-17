# 思维训练页 · 脚本参数与组卷配方

脚本路径：`C:\Users\李玉明\.workbuddy\skills\kindergarten-thinking-course\scripts\generate_worksheet.py`
（Windows 下 Python 不可用时改用 `C:\Users\李玉明\.workbuddy\binaries\python\versions\3.13.12\python.exe`）

## 参数说明

| 参数 | 说明 | 默认值 |
|---|---|---|
| `--level` | 等级 L1-L4 | L1 |
| `--count` | 题目数量，0 表示按等级默认（L1=6, L2=8, L3=8, L4=10）；上限 30 | 0 |
| `--topics` | 指定题型，逗号分隔；拼错会列出合法值；会限定到本等级可用题型 | 空（按等级默认题型） |
| `--seed` | 随机种子；相同 seed 复现同一套题；不指定则每次随机 | 随机 |
| `--name` | 孩子姓名（可预填）；不填则页眉留空下划线框，打印后手填 | 空 |
| `--no-name` | 强制姓名栏空白；忽略 `--name` 与 `--regen` JSON 里的旧姓名 | 关 |
| `--columns` | 排版列数 1 / 2 / 3 | 2 |
| `--no-answers` | 不输出答案页（口头作答时使用） | 关 |
| `--lang` | 界面语言 `zh` / `en`（题型指令与答案同步翻译） | zh |
| `--score` | 页尾显示得分/评分栏（打印后手填：得分、正确数、评语） | 关 |
| `--out` | 生成的 HTML 路径（必填） | — |
| `--json` | 答案 JSON 路径（必填，批改比对用） | — |
| `--preset diagnostic` | 生成诊断卷（覆盖全部题型；题量自动 ≥ 题型数） | — |
| `--review <json>` | 旧答案 JSON，用于错题重练 | — |
| `--wrong 4,7` | 错题 id 列表，配合 --review | — |
| `--regen <json>` | 从旧 JSON 复现原套题（用其存储的 seed/level/lang/name/count） | — |
| `--list` | 列出所有题型与等级映射后退出，不生成练习页 | — |

## 支持的 topic
`classify` 分类 · `match` 配对 · `same` 找相同 · `diff` 找不同 · `order` 排序 · `pattern` 规律 · `shape` 图形 · `position` 方位 · `compare` 比较 · `maze` 迷宫 · `swap` 等量代换

## 常用组卷配方

```bash
# 1) 标准 L2 练习 8 题（随机题型）
python generate_worksheet.py --level L2 --count 8 --seed 7 \
  --out 幼儿思维_L2.html --json 幼儿思维_L2_答案.json

# 2) 专练规律 + 图形 + 方位（L3）
python generate_worksheet.py --level L3 --topics pattern,shape,position \
  --out 幼儿思维_L3_专练.html --json 幼儿思维_L3_专练_答案.json

# 3) 起点未知 → 诊断卷
python generate_worksheet.py --level L1 --preset diagnostic --count 10 \
  --out 幼儿思维_诊断.html --json 幼儿思维_诊断_答案.json

# 4) 错题重练（第 4、7 题错）
python generate_worksheet.py --review 幼儿思维_L2_答案.json --wrong 4,7 \
  --out 幼儿思维_L2_错题重练.html --json 幼儿思维_L2_错题重练_答案.json

# 4b) 一键复现原套题（不重做，直接打印同一份）
python generate_worksheet.py --regen 幼儿思维_L2_答案.json \
  --out 幼儿思维_L2_复现.html --json 幼儿思维_L2_复现_答案.json

# 4c) 浏览所有题型与等级映射
python generate_worksheet.py --list

# 5) 口头作答（不打印答案）
python generate_worksheet.py --level L1 --no-answers --name 小明 \
  --out 幼儿思维_L1.html --json 幼儿思维_L1_答案.json
```

## 版式规范
- 纸张：A4，页边距 12mm；`print-color-adjust:exact` 已开启，无需手动勾选「背景图形」。
- 卡片：每题一张圆角卡片，`break-inside:avoid` 避免跨页断裂。
- 列数：L1/L2 用 2 列；L3/L4 题量较大可用 `--columns 3` 提密度；`--columns 1` 给大字号/低视力使用。
- 一次只出一页（一份练习），避免堆题；观察/专注类（maze/diff/same）单张自动 ≤ 4 题。
- 打印时答案页另起一页（`@media print` 已设 page-break-before）。

## 答案 JSON 结构
```json
{
  "level": 2,
  "name": "小明",
  "count": 8,
  "topics": ["classify","pattern","shape"],
  "activities": [
    {"id":1,"topic":"classify","title":"分类","instruction":"...","html":"...","answer":"第 3、5 个"}
  ]
}
```
批改时直接比对 `activities[].answer`，不要凭记忆重算。

## 扩展题型（插件机制）

题型以插件形式组织，主脚本 `generate_worksheet.py` 启动时通过 `generators/__init__.py` 自动扫描 `generators/g_*.py` 并注册，无需改动主文件。

新增一个题型：

1. 在 `scripts/generators/` 下新建 `g_mytopic.py`。
2. 顶部 `from common import *`（共享素材与 I18N 均在 `common.py`）。
3. 实现生成函数，签名固定为 `(level, rng, lang)`，返回四元组 `(title, instruction, html, answer)`：
   - `title` / `instruction` / `answer` 中的文案通过 `I18N[lang]["key"]` 取词，保证中英文都有；
   - 答案列表的分隔符用 `SEP[lang]`（中文 `、`、英文 `, `）。
4. 模块末尾声明 `TOPICS = {"mytopic": gen_mytopic}`，可选 `LEVELS = [3, 4]` 限定适用等级（省略表示全部等级）。

下次运行即自动生效，`--topics mytopic` 可直接点名出题，诊断卷也会覆盖到它。

**约定**：一个插件文件可包含多个相关题型（如 `g_classify.py` 含 分类/配对/找相同/找不同），按主题归类即可，不必一题一文件。
