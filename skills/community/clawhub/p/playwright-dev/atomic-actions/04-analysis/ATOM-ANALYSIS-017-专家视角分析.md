# ATOM-ANALYSIS-017 - 专家视角分析

> 版本：V1.0  
> 状态：🟡 待规范  
> 最后更新：2026-03-07

---

## 📋 动作定义

**名称：** 专家视角分析  
**分类：** 分析层（Analysis Layer）  
**编号：** ATOM-ANALYSIS-017

**一句话描述：** 用 Critical Thinking 分析内容，质疑假设、验证逻辑、指出缺失

---

## 🎯 输入输出

### 输入
- **类型：** 文本
- **内容：** 待分析的内容

### 输出
- **类型：** 文本
- **内容：** 专家点评（质疑/验证/指出/建议）

---

## ⚙️ 偏好设置

### 分析方法（Critical Thinking）
| 方法 | 说明 | 示例 |
|------|------|------|
| 质疑假设 | 挑战前提条件 | "这个假设成立吗？" |
| 验证逻辑 | 检查推理过程 | "逻辑链条完整吗？" |
| 指出缺失 | 发现遗漏部分 | "缺少 XX 维度" |
| 提出改进 | 给出优化建议 | "建议增加 XX" |

### 分析维度
- **完整性：** 内容覆盖是否全面
- **正确性：** 关键信息是否准确
- **一致性：** 前后逻辑是否一致
- **可行性：** 建议是否可落地

### 表述风格
- **直接：** 不拐弯抹角
- **建设性：** 指出问题同时给建议
- **专业：** 体现领域知识

---

## 📝 操作步骤

```powershell
# 1. 分析内容结构
$content = "待分析的内容"

# 2. 质疑假设
$assumptions = IdentifyAssumptions($content)
$challenges = $assumptions | ForEach-Object { "假设：$_ - 成立吗？" }

# 3. 验证逻辑
$logicGaps = VerifyLogic($content)

# 4. 指出缺失
$missingItems = IdentifyMissing($content)

# 5. 提出改进
$improvements = SuggestImprovements($content)

# 6. 生成点评
$review = @"
## 🔍 专家视角分析

### 质疑假设
$($challenges -join "`n")

### 逻辑验证
$($logicGaps -join "`n")

### 缺失项
$($missingItems -join "`n")

### 改进建议
$($improvements -join "`n")
"@

return $review
```

---

## 🔄 使用场景

### 场景 1：专家点评 HTML 生成
```
触发：生成专家点评
  ↓
调用：ATOM-ANALYSIS-017
  ↓
输出：Critical Thinking 点评
  ↓
嵌入：HTML 的"深度洞察"章节
```

### 场景 2：项目方案评审
```
触发：项目方案提交
  ↓
调用：ATOM-ANALYSIS-017
  ↓
输出：评审意见
```

---

## 🔗 关联动作

### 前置动作
- 无（可独立执行）

### 后置动作
- ATOM-VISUAL-007：生成专家评分
- ATOM-VISUAL-005：生成 HTML 文件

### 常组合使用
- ATOM-ANALYSIS-017 + ATOM-VISUAL-007 + ATOM-VISUAL-005
  （分析 → 评分 → HTML）

---

## ✅ 检查清单

执行前确认：
- [ ] 内容非空
- [ ] 4 种方法都用上
- [ ] 表述建设性

---

_模块化定义 | 可独立调用 | 2026-03-07_
