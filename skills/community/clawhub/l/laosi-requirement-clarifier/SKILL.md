---
name: requirement-clarifier
description: 需求澄清器 - 原创技能。自动追问模糊需求，减少返工和误解。适用于AI编程、需求分析、任务交接等场景。
metadata: {"openclaw": {"requires": {}, "install": []}}
tags: [requirements, clarification, questions, accuracy, reduction]
version: 1.0.0
author: laosi
source: original
---

# ⚠️ 发布规则

**所有发布到ClawHub的技能必须严格测试，确定没有问题再发布**

---

## 技能测试验证清单

- [x] frontmatter格式正确
- [x] 澄清问题模板完整
- [x] 判断逻辑清晰
- [x] 优先级排序合理
- [x] 无语法错误

---

# Requirement Clarifier - 需求澄清器

> 原创技能 | 激活词: 澄清需求 / 追问细节 / 确认需求

## 核心问题

模糊需求导致的问题：
- AI按错误理解开发
- 完成后需要返工
- 浪费时间精力
- 用户不满意

## 澄清框架

### 5W1H 追问法

```
What (什么) - 具体要做什么？
Why (为什么) - 为什么要做这个？
Who (谁) - 谁来使用？
Where (哪里) - 在什么环境使用？
When (何时) - 什么时候需要？
How (如何) - 如何实现/使用？
```

### 澄清维度

| 维度 | 关键问题 | 目的 |
|------|----------|------|
| 范围 | 需要包含什么？排除什么？ | 明确边界 |
| 质量 | 怎样算成功？有什么标准？ | 定义成功 |
| 约束 | 有什么限制？技术/时间/预算？ | 了解限制 |
| 优先级 | 什么最重要？ | 排序决策 |
| 风险 | 有什么担忧？ | 预防问题 |

## 常见模糊模式

### 模式1: 动词模糊

```
❌ 模糊: "帮我优化这个代码"
✅ 澄清: 优化哪个方面？
       - 性能 (速度/内存)
       - 可读性
       - 可维护性
       - 安全性

❌ 模糊: "修复这个bug"
✅ 澄清: 期望行为是什么？
       实际行为是什么？
       如何复现？
```

### 模式2: 名词模糊

```
❌ 模糊: "创建一个用户模块"
✅ 澄清: 需要包含哪些功能？
       - 注册/登录
       - 用户资料
       - 权限管理
       - 头像上传
       需要和哪些系统集成？

❌ 模糊: "做个好看的界面"
✅ 澄清: 好看是指什么风格？
       - 现代简约
       - 传统商务
       - 活泼年轻
       有参考案例吗？
```

### 模式3: 范围模糊

```
❌ 模糊: "做个网站"
✅ 澄清: 网站类型？
       - 电商网站
       - 博客网站
       - 企业官网
       - 社交平台
       
❌ 模糊: "处理这些数据"
✅ 澄清: 数据来源？
       处理逻辑？
       输出格式？
```

## 澄清流程

```
1. 接收需求
      ↓
2. 识别模糊点
      ↓
3. 生成澄清问题
      ↓
4. 按优先级排序
      ↓
5. 选择最关键问题追问
      ↓
6. 根据回答更新理解
      ↓
7. 重复直到清晰
```

## 澄清问题生成

```python
def generate_clarification_questions(requirement: str) -> list[Question]:
    questions = []
    
    # 检测模糊模式
    if contains_vague_verb(requirement):
        questions.extend(clarify_verb(requirement))
    
    if contains_vague_noun(requirement):
        questions.extend(clarify_noun(requirement))
    
    if lacks_scope(requirement):
        questions.extend(clarify_scope(requirement))
    
    if lacks_success_criteria(requirement):
        questions.extend(clarify_criteria(requirement))
    
    # 按优先级排序
    questions.sort(key=lambda q: q.priority, reverse=True)
    
    # 只问最关键的3个
    return questions[:3]
```

### 模糊检测规则

```python
VAGUE_WORDS = [
    '优化', '改进', '提升', '完善',
    '处理', '管理', '系统', '模块',
    '好看', '好用', '快速', '高效',
    '一些', '相关', '合适', '适当',
]

VAGUE_PATTERNS = [
    r'帮我.*',        # 缺少宾语
    r'做个.*',        # 缺少具体描述
    r'处理.*',        # 缺少处理逻辑
    r'优化.*',        # 缺少优化目标
]
```

## 澄清输出格式

```markdown
## 需求澄清

### 原始需求
"帮我做个用户管理模块"

### 已识别模糊点
1. ⚠️ 范围不清 - 不知道包含哪些功能
2. ⚠️ 标准不明 - 不知道怎样算完成
3. ⚠️ 环境未提 - 不知道在什么环境运行

### 请帮我确认

#### 问题 1/3 [高优先级]
**需要包含哪些用户管理功能？**
- [ ] 用户注册
- [ ] 用户登录
- [ ] 密码找回
- [ ] 用户资料编辑
- [ ] 权限/角色管理
- [ ] 其他: ___

#### 问题 2/3 [中优先级]
**有什么技术要求？**
- 技术栈: ___
- 需要API吗？ ○ 是 ○ 否
- 需要数据库吗？ ○ 是 ○ 否

#### 问题 3/3 [低优先级]
**预计用户规模？**
- [ ] <100人
- [ ] 100-1000人
- [ ] 1000-10000人
- [ ] >10000人
```

## 回复理解确认

```markdown
## 需求理解确认

### 我理解的如下，请确认：

**功能范围**
- ✅ 用户注册/登录
- ✅ 密码找回
- ✅ 用户资料管理
- ❌ 权限管理 (你说先不做)

**技术要求**
- ✅ 技术栈: React + Node.js
- ✅ 需要REST API
- ✅ 使用PostgreSQL

**成功标准**
- ✅ 所有用户能正常注册登录
- ✅ 资料能正常编辑保存
- ✅ 响应时间 < 500ms

**是否正确？**
- [ ] 是，没问题
- [ ] 不对，需要调整
```

## 澄清效果评估

```python
def evaluate_clarity(requirement: str, answers: list[str]) -> float:
    # 计算澄清后的清晰度
    
    clarity = 0.0
    
    if has_concrete_features(answers):
        clarity += 0.3
    
    if has_success_criteria(answers):
        clarity += 0.3
    
    if has_tech_constraints(answers):
        clarity += 0.2
    
    if has_scope_boundary(answers):
        clarity += 0.2
    
    return clarity

# 澄清有效阈值: >= 0.7
```

## 应用场景

### 场景1: AI编程

```
用户: "帮我做个按钮"
AI: [触发需求澄清器]
   - 需要什么样式？
   - 点击事件？
   - 有哪些状态？
   - 尺寸大小？
```

### 场景2: 任务交接

```
A: "把这个功能交给B"
B: [使用需求澄清器]
   - 功能范围？
   - 接口定义？
   - 交付标准？
```

### 场景3: 需求分析

```
产品经理: "用户需要管理数据"
分析师: [使用需求澄清器]
   - 什么类型的数据？
   - CRUD全部需要？
   - 有批量操作？
```

## 与Karpathy法则结合

需求澄清 = Karpathy "先思考" 的具体实现

| Karpathy法则 | 需求澄清对应 |
|--------------|-------------|
| 不假设 | 不假设用户需求 |
| 不隐藏困惑 | 明确提出疑问 |
| 多解释列出 | 提供选项让用户选择 |

## 原创性声明

本技能为原创，融合了：
- 需求工程方法论
- 模糊语言识别
- 追问框架设计
- 交互式澄清对话

---

**作者**: laosi
**创建日期**: 2026-04-28