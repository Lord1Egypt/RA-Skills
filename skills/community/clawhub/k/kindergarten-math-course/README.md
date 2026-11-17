# 幼儿园识数与加减法体系课程 · Skill

> 面向 3-7 岁幼儿的数学启蒙体系课程。
> 一句话让大模型为你出练习页、批改、定级、给出家长指导。

[![version](https://img.shields.io/badge/version-1.2.0-blue.svg)]()
[![license](https://img.shields.io/badge/license-MIT-green.svg)]()
[![python](https://img.shields.io/badge/python-3.8%2B-yellow.svg)]()

---

## 5 秒上手

```
"给中班孩子出一份 6-10 识数练习"
"做一份数学诊断卷，看看孩子到哪级了"
"上次错了几道题，按这份 JSON 出同型题重练"
```

只要告诉 WorkBuddy 幼儿 + 数学意图，剩下的由本 Skill 自动完成：
**诊断 → 选级 → 组卷 → 打印 → 批改 → 进阶建议**。

## 五级体系

| 等级 | 主题 | 核心内容 |
|---|---|---|
| L1 | 识数 1-5 | 点数、认数字、数物对应 |
| L2 | 识数 6-10 | 点数 10、数的顺序、相邻数 |
| L3 | 比大小与分解组成 | 比较、分与合 |
| L4 | 10 以内加减 |加减运算、看图列式 |
| L5 | 20 以内进退位 | 凑十法、破十法 |

晋级标准：每个等级 10 题对 8 题即可进入下一级。

## 命令行（脚本方式）

```bash
# 一份练习（预填姓名 + 三列排版）
python scripts/generate_worksheet.py --level L2 --seed 7 --name 小明 \
    --columns 3 --out 练习.html --json 答案.json

# 诊断卷（用于定级）
python scripts/generate_worksheet.py --preset diagnostic --out 诊断.html --json 答案.json

# 错题重练
python scripts/generate_worksheet.py --review 答案.json --wrong 2,5 --out 重练.html
```

## 自检

```bash
python scripts/selftest.py
```

## 特性

- 🖨️ **A4 可打印**：练习页 + 参考答案页一体输出，直接打印即用
- 🔁 **闭环学习**：诊断定级 → 练习 → 批改 → 错题重练 → 晋级
- 📝 **错题重练**：按错题题型生成同型新题，不是简单重复原题
- 🎲 **seed 可复现**：同一 seed 生成完全相同的卷子

## 姊妹 Skill

- kindergarten-english-course — 英语启蒙 L1-L4
- kindergarten-thinking-course — 思维逻辑训练 L1-L4
- kindergarten-activity-course — 五大领域亲子活动方案

## License

MIT
