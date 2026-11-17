# 幼儿园五大领域活动方案 · Skill

> 面向 3-6 岁幼儿的健康/语言/社会/科学/艺术五域活动库。
> 一句话让大模型为你挑活动、出可打印活动卡、排一周亲子计划。

[![version](https://img.shields.io/badge/version-1.0.0-blue.svg)]()
[![license](https://img.shields.io/badge/license-MIT-green.svg)]()
[![python](https://img.shields.io/badge/python-3.8%2B-yellow.svg)]()

---

## 5 秒上手

```
"给中班孩子安排三个科学小实验"
"这周末的亲子活动帮我挑两个，要户外的"
"按五大领域给大班排一周活动计划"
```

只要告诉 WorkBuddy 幼儿 + 活动/游戏/亲子意图，剩下的由本 Skill 自动完成：
**选域 → 挑活动 → 生成活动卡 → 组合周计划 → 家长安全提示**。

## 活动卡内容

每张 A4 活动卡包含：**领域目标 · 材料清单 · 分步玩法 · 家长安全提示 · 建议时长**。

内置 20 个活动，五域 × 四年龄段（小班/中班/大班/幼小衔接）全覆盖：
沉浮实验、彩虹牛奶画、超市小管家、家庭音乐会、书包整理大赛等。

## 命令行（脚本方式）

```bash
# 大班五域均衡 5 个活动
python scripts/generate_activity.py --age 大班 --domain all --count 5 --seed 11 --out 活动卡.html

# 中班只出科学+艺术
python scripts/generate_activity.py --age 中班 --domain science,art --count 3 --out 活动卡.html
```

参数：`--age` 年龄段 · `--domain` 五域缩写（health/lang/social/science/art）· `--count` 活动数 · `--seed` 可复现。

## 与练习型 Skill 的分工

- 要**练习页**（数学/思维/英语题）→ 使用对应的练习型 Skill
- 要**玩中学**（游戏、实验、手工、亲子）→ 用本 Skill

## 姊妹 Skill

- [kindergarten-math-course](https://skillhub.cn/skills/user_89a2cacc/kindergarten-math-course) — 识数与加减法 L1-L5
- kindergarten-thinking-course — 思维逻辑训练 L1-L4
- kindergarten-english-course — 英语启蒙 L1-L4

## License

MIT
