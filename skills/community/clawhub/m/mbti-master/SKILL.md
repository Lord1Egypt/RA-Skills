---
name: mbti-master
description: Comprehensive MBTI personality analysis tool with quick testing, cognitive function analysis, compatibility matching, and trending MBTI games. Use when users want to explore their personality type, understand 16 personalities, check compatibility with others, or play MBTI-related interactive games.
metadata:
  author: ShenJian
  version: 1.0.0
  created: 2026-03-03
  license: MIT
  open_source: true
---

# MBTI Master - 人格类型分析工具

**创建者：申建**  
**开源协议：MIT License（允许自由使用、修改和分发）**

基于荣格认知功能理论的MBTI人格分析工具，包含快速测试、深度解析、社交匹配等趣味功能。

## 核心功能

### 1. 快速人格测试

```bash
bash scripts/quick_test.sh
```

4维度8题快速测试，5分钟获得你的MBTI类型。

### 2. 完整人格分析

查看任意类型的详细解析：
```bash
bash scripts/type_analysis.sh INTJ
bash scripts/type_analysis.sh ENFP
```

输出包含：
- 四字母含义解析
- 主导/辅助/第三/劣势认知功能
- 适合职业方向
- 人际关系特征
- 成长建议

### 3. 人格兼容性匹配

查看两种类型的相处模式：
```bash
bash scripts/compatibility.sh INTJ ENFP
```

### 4. 认知功能深度解析

理解8种认知功能：
```bash
bash scripts/cognitive_functions.sh
```

### 5. 趣味MBTI游戏

#### 5.1 人格猜猜看
```bash
bash scripts/guess_game.sh
```
根据描述猜测是哪种人格类型。

#### 5.2 今日人格运势
```bash
bash scripts/daily_horoscope.sh INTJ
```
基于MBTI类型的趣味日运（非真实预测，仅供娱乐）。

#### 5.3 最佳职业匹配
```bash
bash scripts/career_match.sh
```
根据测试结果推荐职业方向。

### 6. 16型人格速查

```bash
bash scripts/type_cheatsheet.sh
```
一键查看所有16种人格的核心特征对比表。

## 2026年MBTI新趋势

### 认知功能深度分析（超越四字母）

现代MBTI理论更关注8种认知功能而非简单四字母：

**感知功能（Perceiving）**
- Ni (内倾直觉)：洞察本质，预见未来
- Ne (外倾直觉)：探索可能，联想创新
- Si (内倾感觉)：细节记忆，经验传承
- Se (外倾感觉)：当下体验，感官敏锐

**判断功能（Judging）**
- Ti (内倾思考)：逻辑分析，构建体系
- Te (外倾思考)：效率优先，目标导向
- Fi (内倾情感)：价值坚守， authenticity
- Fe (外倾情感)：和谐共情，社交敏锐

### 有趣的人格互动现象

1. **镜像类型**（如INTJ ↔ ESFP）
   - 四种功能完全相同但顺序相反
   - 最容易互相吸引也最容易产生冲突

2. **黄金配对**（如INTJ ↔ ENFP）
   - 主导功能互补，能够互相激发成长

3. **功能栈共鸣**（如INTJ ↔ INFJ）
   - 仅一个字母差异，内在体验却大不相同

4. **阴影人格**（压力状态下）
   - 每个类型在极端压力下会表现出完全相反的特征

## 数据文件

所有人格类型数据存储在：
- `references/types/` - 16种人格详细档案
- `references/functions.md` - 8种认知功能详解
- `references/compatibility_matrix.csv` - 兼容性匹配表

## 使用场景

- 快速了解自我或他人的性格特征
- 团队建设中理解成员差异
- 职业规划和人际关系参考
- 社交破冰和趣味互动
- 深度心理学学习和认知功能分析

## 免责声明

MBTI仅作为自我认知的参考工具，不应作为评判他人或做出重大人生决策的唯一依据。人格具有复杂性和流动性，类型只是倾向而非定论。