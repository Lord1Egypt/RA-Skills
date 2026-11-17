# 练习页生成规范与脚本用法

## 脚本

`scripts/generate_worksheet.py`：生成自包含 A4 可打印 HTML（内嵌 CSS，无外部依赖）。

```
python scripts/generate_worksheet.py --level L4 --count 20 --out 练习.html --json 答案.json
```

### 参数

| 参数 | 说明 | 默认 |
|---|---|---|
| `--level` | L1-L5，见 `references/curriculum.md` | L4 |
| `--preset diagnostic` | 10 题跨级诊断卷，答案页标注每题等级 | 无 |
| `--topics` | 逗号分隔题型，默认按等级自动配置 | 按等级 |
| `--count` | 题目数量 | 20 |
| `--per-page` | 每页题数，默认 L1/L2=10、L3=12、L4/L5=16、诊断卷=10 | 按等级 |
| `--columns` | 每页列数 1/2/3；L1/L2 建议 1 列更宽松，大班高密度可用 3 列 | 2 |
| `--seed` | 随机种子，相同种子复现同一套题 | 随机 |
| `--title` | 自定义标题 | 自动生成 |
| `--no-answers` | 不生成答案页（口头作答时用） | 附答案页 |
| `--out` | 输出 HTML 路径（必填） | — |
| `--name` | 页眉预填孩子姓名 | 空 |
| `--review` | 错题重练：上次练习的 JSON 路径 | 无 |
| `--wrong` | 错题题号，逗号分隔，配合 `--review`；每个错题出 2 道同型新题 | 无 |
| `--json` | 同时输出题目/答案 JSON，供后续批改 | 无 |

### 可用题型

`count_objects` 数一数、`write_number` 数字描红、`circle_number` 圈数字、`next_number` 数的顺序、
`compare` 比大小、`compose` 分解组成、`add` 加法、`sub` 减法、`missing_addend` 填未知数、
`word_problem` 应用题、`add_carry` 进位加、`sub_borrow` 退位减、`mixed_20` 20 以内混合、
`ordinal` 序数（第几）、`color_by_number` 按数涂色、`picture_equation` 看图列式、`vertical` 竖式计算（L5）。

## 自检

改动 `generate_worksheet.py` 后，发版前必跑 `scripts/selftest.py`（退出码 0 才可打包发布）：

```
python scripts/selftest.py
python scripts/selftest.py --fix   # 打印修复建议
```

四项检查：① 题目唯一率（按各题型题目空间大小分级判定，小空间题型豁免）；② 答案合法性（数字/比较符/算式/序数/涂色等模式正则校验）；③ 等级题型覆盖（每级 ≥4 题型）；④ `build_questions` 同卷无重复。

## 版式规范（已内置在脚本 CSS 中，手工排版时遵循）

- 纸张 A4 纵向，页边距 10mm，正文区 190mm 宽
- 正文 16pt、计算式 19pt、图形 emoji 23pt、描红数字 34pt（幼儿视觉与书写尺度）
- 答题空：2.2em 宽下划线；运算符空 2.4em
- 每页页眉含：标题、等级与知识点、姓名/日期/用时/做对题数 填写栏
- 页脚含页码；答案页独立成页，标"家长用"
- 打印设置：勾选「背景图形」（否则田字格虚线不显示），缩放 100%
- 描红题使用田字格（20mm 见方，含十字中线），只要求笔顺与占格

## 常用配方

| 场景 | 命令要点 |
|---|---|
| 起点未知 | `--preset diagnostic` |
| 小班首次识数 | `--level L1 --topics count_objects,circle_number --count 10 --columns 1` |
| 练数字书写 | `--level L1 --topics write_number --count 5 --columns 1` |
| 补分解组成 | `--level L3 --topics compose --count 12` |
| 10 以内加减综合 | `--level L4 --count 20` |
| 进位加专项 | `--level L5 --topics add_carry --count 20` |
| 幼小衔接提速 | `--level L5 --topics mixed_20,word_problem --count 20`（限时 5 分钟） |
| 练序数/第几 | `--level L1 --topics ordinal --count 6 --columns 1` |
| 按数涂色 | `--level L1 --topics color_by_number --count 6 --columns 1` |
| 看图列式 | `--level L3 --topics picture_equation --count 10` |
| 竖式过渡 | `--level L5 --topics vertical --count 10` |
| 错题重练 | `--review 上次答案.json --wrong 4,7,11` |
| 大班高密度排版 | `--level L4 --count 24 --columns 3` |
| 口头作答（不要答案页） | 追加 `--no-answers` |
| 复现上次那套题 | 追加相同的 `--seed` |
