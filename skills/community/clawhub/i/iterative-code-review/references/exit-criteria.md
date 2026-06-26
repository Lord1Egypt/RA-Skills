# 退出标准详解

## 核心规则

**用户决定何时结束 Review。**

建议的退出条件：
1. 连续两轮 Review 都未发现任何 P0/P1/P2 问题
2. 用户对代码质量满意

## 流程控制

```javascript
let currentRound = 0;
const MAX_ROUNDS = 10;

function checkCompletion(currentRoundIssues) {
  currentRound++;
  
  // 最大轮次检查
  if (currentRound >= MAX_ROUNDS) {
    console.log(`已达到最大轮次 ${MAX_ROUNDS}，请用户决定是否继续。`);
    return { status: "USER_DECISION" };
  }
  
  // 汇总问题
  const mustFixIssues = currentRoundIssues.filter(i => 
    ['P0', 'P1', 'P2'].includes(i.level)
  );
  
  if (mustFixIssues.length === 0) {
    console.log("本轮未发现 P0/P1/P2 问题。是否继续下一轮确认？(y/n)");
    return { status: "USER_DECISION" };
  }
  
  console.log(`发现 ${mustFixIssues.length} 个问题。是否修复？(y/n)`);
  return { status: "USER_DECISION" };
}
```

## 流程图示

### 用户控制的流程

```
Round 1: 发现问题 → 向用户报告 → 用户决定是否修复
    ↓
用户同意 → Fixer → 用户审核修改
    ↓
Round 2: 发现问题 → 向用户报告 → 用户决定是否修复
    ↓
用户同意 → Fixer → 用户审核修改
    ↓
Round 3: 无问题 → 向用户报告 → 用户决定是否结束
    ↓
用户同意结束 → ✅ END
```

### 用户可以随时干预

```
任何阶段:
- 用户可以停止 Review
- 用户可以跳过某个问题的修复
- 用户可以要求更多轮次
- 用户可以手动修改代码
```

## 关键规则

- **用户控制** - 每一步都需要用户确认
- **MAX_ROUNDS = 10** - 建议的最大轮次，但用户可以决定继续
- **P3 不强制** - 可选修复，用户决定
- **透明报告** - 向用户清晰报告每轮发现的问题