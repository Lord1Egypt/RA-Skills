# 幼儿园识字与诗歌课程体系 (kindergarten-chinese-course)

面向 3-7 岁幼儿的识字与诗歌启蒙练习生成器。按 L1-L4 四级进阶，生成 A4 可打印练习页（看图认字、描红、组词、古诗带拼音、古诗填空），含答案页与家长指导。

## 5 秒上手

```bash
# 默认 L1 综合卷（认字+描红+儿歌），带评分栏
python scripts/generate_worksheet.py --level L1 --score \
  --out 识字_L1.html --json 识字_L1.json

# 中班综合卷（认字+描红+五言古诗）
python scripts/generate_worksheet.py --level L2 --topics recognize,trace,poem --seed 7 --score \
  --out 识字_L2.html --json 识字_L2.json
```

对 WorkBuddy 直接说更简单："给孩子出一份识字练习" / "生成一份古诗描红" / "出汉字填空默写"。

## 等级与题型

| 等级 | 年龄 | 题型 |
|---|---|---|
| L1 | 3-4 岁 | recognize 认字, trace 描红, poem 儿歌 |
| L2 | 4-5 岁 | recognize, trace, poem 五言古诗 |
| L3 | 5-6 岁 | recognize, trace, poem 七言古诗, word 组词 |
| L4 | 6-7 岁 | recognize, trace, poem, word, fill 古诗填空 |

## 完整命令清单

见 `references/activity-spec.md`；课程大纲见 `references/curriculum.md`；家长话术见 `references/pedagogy.md`。

## 规范
- 仅本地 Python 标准库，零外网。
- `--seed` / `--regen` 可字节级复现同一套题。
- 姓名经 HTML 转义，安全可打印。
