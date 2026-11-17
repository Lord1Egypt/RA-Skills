# 幼儿园英语课程体系 · Skill

> 面向 3-7 岁幼儿的英语启蒙体系课程。
> 一句话让大模型为你出练习页、批改、定级、给出家长指导。

[![version](https://img.shields.io/badge/version-1.0.0-blue.svg)]()
[![license](https://img.shields.io/badge/license-MIT-green.svg)]()
[![python](https://img.shields.io/badge/python-3.8%2B-yellow.svg)]()

---

## 5 秒上手

```
"给中班孩子出一份自然拼读练习"
"做一份英语诊断卷，看看孩子从哪级开始"
"按这份答案 JSON 出错题重练"
```

只要告诉 WorkBuddy 幼儿 + 英语意图，剩下的由本 Skill 自动完成：
**诊断 → 选级 → 组卷 → 打印 → 批改 → 进阶建议**。

## 四级体系

| 等级 | 主题 | 核心内容 |
|---|---|---|
| L1 | 字母启蒙 Letters | 字母描红、大小写配对、字母发音、主题词汇 |
| L2 | 自然拼读 Phonics | 听音辨字母、CVC 拼读、看图识词、补全单词 |
| L3 | 词汇句型 Words & Sentences | 高频词、主题词汇、5 类简单句型 |
| L4 | 阅读对话 Reading & Speaking | 句型运用、情景对话、自然拼读巩固 |

晋级标准：每个等级 10 题对 8 题即可进入下一级。

## 命令行（脚本方式）

```bash
# 一份练习（默认姓名空白可填）
python scripts/generate_worksheet.py --level L2 --seed 7 \
    --out 练习.html --json 答案.json

# 诊断卷（10 题覆盖全部题型，用于定级）
python scripts/generate_worksheet.py --preset diagnostic --out 诊断.html --json 答案.json

# 错题重练（按 JSON 中的题号生成同型新题）
python scripts/generate_worksheet.py --review 答案.json --wrong 2,5 --out 重练.html
```

常用参数：`--level L1-L4` · `--topics` 指定题型 · `--count` 题量 · `--lang zh/en` 双语 · `--columns` 分栏 · `--name` 预填姓名 · `--seed` 可复现。

## 特性

- 🖨️ **A4 可打印**：练习页 + 参考答案页一体输出，直接打印即用
- 🔁 **闭环学习**：诊断定级 → 练习 → 批改 → 错题重练 → 晋级
- 🧩 **题型插件化**：`scripts/generators/` 下 10 个题型，新增题型丢文件即用
- 🌏 **中英双语**：`--lang en` 切换纯英文页面
- 🎲 **seed 可复现**：同一 seed 生成完全相同的卷子

## License

MIT
