# 练习页规范与组卷配方

## 脚本参数

```
python generate_worksheet.py --level L2 --count 8 --seed 7 \
  --out 幼儿英语_L2.html --json 幼儿英语_L2_答案.json
```

| 参数 | 默认值 | 说明 |
|---|---|---|
| `--level` | L1 | 等级 L1-L4 |
| `--count` | 按等级 | 题目数量，0 表示用默认（每级 8 题） |
| `--topics` | 按等级 | 逗号分隔题型，如 `sentence,sight_words` |
| `--seed` | 随机 | 随机种子，相同种子生成相同题目 |
| `--name` | 空 | 页眉预填孩子姓名（留空则显示手填下划线） |
| `--lang` | zh | 指导语语言：zh 中文 / en 英文 |
| `--columns` | 2 | 排版列数 2 或 3（高密度） |
| `--no-answers` | 关 | 不生成答案页（口头作答） |
| `--score` | 关 | 页尾显示评价栏（打印后手填） |
| `--preset` | 空 | `diagnostic` 生成 10 题诊断卷 |
| `--review` | 空 | 旧答案 JSON 路径，用于错题重练 |
| `--wrong` | 空 | 错题 id 列表，逗号分隔，配合 `--review` |
| `--out` | 必填 | 输出 HTML 路径 |
| `--json` | 必填 | 输出题目与答案 JSON 路径 |

## 版式规范

- A4 纵向，页边距默认，打印时勾选「背景图形」（描红框/虚线依赖背景）。
- 题型以卡片呈现，每卡含：编号+题型名、指导语、题面。
- 默认 2 列；对话/长句题型可用 `--columns 1` 获得更大空间。
- 末尾附参考答案页（家长用），口头作答时加 `--no-answers`。

## 常用组卷配方

```bash
# 1) 字母启蒙（小班，默认 L1 8 题）
python generate_worksheet.py --level L1 --name 小明 --out 英语_L1.html --json 英语_L1.json

# 2) 自然拼读专项（仅 CVC + 看图识词，题量减半思路：count 6）
python generate_worksheet.py --level L2 --topics phonics_cvc,word_pic --count 6 --out 拼读.html --json 拼读.json

# 3) 句型+对话（大班/衔接）
python generate_worksheet.py --level L4 --topics sentence,dialogue --count 6 --columns 1 --out 句型对话.html --json 句型对话.json

# 4) 起点诊断
python generate_worksheet.py --preset diagnostic --out 诊断卷.html --json 诊断卷.json

# 5) 错题重练（针对上次第 3、7 题）
python generate_worksheet.py --review 英语_L3.json --wrong 3,7 --out 错题重练.html --json 错题重练.json

# 6) 全英指导语（双语家庭）
python generate_worksheet.py --level L3 --lang en --name Tom --out english_L3.html --json english_L3.json
```

## 题型清单

| key | 名称 | 适用等级 |
|---|---|---|
| `letter_trace` | 字母描红 | L1 |
| `letter_match` | 大小写配对 | L1, L2 |
| `letter_sound` | 字母发音 | L1, L2 |
| `phonics_cvc` | 自然拼读 | L2, L4 |
| `word_pic` | 看图识词 | L2, L3 |
| `vocab_theme` | 主题词汇 | L1, L2, L3 |
| `fill_letter` | 补全单词 | L2, L3 |
| `sight_words` | 高频词 | L3, L4 |
| `sentence` | 简单句型 | L3, L4 |
| `dialogue` | 情景对话 | L4 |
