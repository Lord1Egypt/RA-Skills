# 案例库（v3.7 更新）

> 把 Allen 教学 + 蕉下案例 + 旺旺批改做成可逐个调阅学习的案例库。
> 配 `scripts/case_study.py`，对每个案例做"苏格拉底式拆解" — 先你自己回答，
> 再看范本分析。

## 案例目录（9 个真实案例 + 5 个模板）

### Allen 经典（7 个）
| ID | 案例 | 核心技法 |
|----|------|---------|
| 21 | [上班是不合理的超自然现象](allen_shangban.md) | 金句法 · 断句留白 · 情绪共识 |
| 22 | [薯你会买](allen_shuhui.md) | 造词三层结构 · 不必X就能Y |
| 11 | [惊蛰·领取春日礼](allen_lingqu.md) | 动词意境指向 |
| 18 | [人生尽兴指南六切面](allen_jinxing.md) | 同slogan多切面 · 互动阶梯 |
| 20 | [周三存档](allen_zhouwen.md) | 栏目化设计 · 内容延展性 |
| 19 | [春分·什么也不赶](allen_chunfen.md) | 节气减法 · 只取一个零件 |

### 品牌方法论（2 个）
| ID | 案例 | 核心技法 |
|----|------|---------|
| 2 | [蕉下品牌](jiaoxia_brand.md) | 三大句式 · 痛点→场景→方案→情绪 |
| 17 | [旺旺雪米饼](wangwang_xuemi.md) | 先做功课 · 60分五法 · 态度vs成分 |

### 冬日系列模板（5 个，待用户填充内容）
- [winter_01.md](winter_01.md) — 冬日宣言
- [winter_02.md](winter_02.md) — 拥抱温度
- [winter_03.md](winter_03.md) — Live展
- [winter_04.md](winter_04.md) — 尽兴星期三
- [winter_05.md](winter_05.md) — 冬日终章

## 文件 Schema

```markdown
---
case_id: <唯一标识>
title: <案例标题>
brand: <品牌>
product: <产品>
date: <日期>
teacher: Allen
key_technique: <核心技法>
jarvis_score: <评分>
---

## 原文要点
## 关键技法
## 苏格拉底式问题（5 个）
## 范本解读
## 你能学到的
```

## 怎么用

```bash
# 列所有案例
python3 scripts/case_study.py list

# 学习一个案例（苏格拉底模式：先问你，再给答）
python3 scripts/case_study.py study allen_shangban

# 跳过提问直接看范本
python3 scripts/case_study.py show allen_shangban

# 找相关案例
python3 scripts/case_study.py related "造词"
```
