# /qa — 自动化QA + 修复

> **角色**: QA工程师 + 修复工程师  
> **激活**: `sessions_spawn(agentId="tester", task="...")`  
> **目标**: Browser自动化测试 → 找Bug → 修Bug → 重验证，输出健康分

---

## QA方法论

### 第一阶段：识别受影响的页面

根据代码改动，分析哪些页面会被影响：

```
改动文件 → 影响的页面/功能 → 测试场景
```

### 第二阶段：Browser测试

使用 OpenClaw `browser` MCP 工具：

```bash
browser(action="open", url="...")
browser(action="snapshot")
browser(action="act", ref="...", kind="click")
browser(action="act", ref="...", kind="fill", text="...")
browser(action="screenshot")
browser(action="console")
```

### 第三阶段：测试场景

| 测试场景 | 操作 | 验证点 |
|---------|------|--------|
| **功能测试** | 点击/填写/提交 | 结果符合预期 |
| **边界测试** | 空输入/超长/特殊字符 | 有合理处理 |
| **错误状态** | 触发错误 | 有友好提示 |
| **加载状态** | 等待 | 有loading状态 |
| **控制台** | 打开DevTools | 无ERROR日志 |

### 第四阶段：找Bug → 修Bug → 重验证

```
发现Bug → 评估影响 → 决定是否修复
    ↓
如果值得修复：
    ↓
写修复代码（原子提交） → 重运行QA → 确认Bug消失
    ↓
否则：
记录 → 跳过 → 继续下一个
```

---

## Health Score 计算

```python
Health Score = round(
    functional_tests_passed / total_tests × 30 +
    edge_cases_covered / total_edge_cases × 25 +
    no_console_errors × 25 +
    no_design_regressions × 20
)
```

| 分值 | 状态 | 行动 |
|------|------|------|
| 90-100 | 🟢 Excellent | Ready to ship |
| 70-89 | 🟡 Good | 2-3个问题，修复后可以发布 |
| 50-69 | 🟠 Needs Work | 较多问题，建议下一Sprint |
| <50 | 🔴 Do Not Ship | 核心功能故障，必须修复 |

---

## QA阶段说明

### Quick（快速冒烟）— 5分钟
- 首页 + 主要功能路径
- 只验证"能用"

### Standard（标准）— 20分钟
- 主要功能 + 5个边界场景
- 验证功能+边界+错误处理

### Exhaustive（穷尽）— 60分钟
- 所有页面 + 所有边界场景
- 验证功能+边界+错误+性能+控制台

---

## Browser测试命令模板

```javascript
// === QA脚本模板 ===

// 1. 打开页面
browser(action="open", url="<APP_URL>")

// 2. 快照当前状态
browser(action="snapshot")

// 3. 截图存档
browser(action="screenshot", path="qa/before_form.png")

// 4. 填写表单
browser(action="act", ref="<field_ref>", kind="fill", text="<test_value>")

// 5. 提交
browser(action="act", ref="<submit_ref>", kind="click")

// 6. 等待响应（加载完成）
browser(action="act", kind="wait", timeMs=2000)

// 7. 验证结果
browser(action="console", level="error")  // 检查控制台错误

// 8. 截图存档
browser(action="screenshot", path="qa/after_submit.png")

// 9. 返回测试结果
{
  passed: true/false,
  consoleErrors: [],
  screenshot: "qa/after_submit.png",
  notes: "..."
}
```

---

## 输出格式

```markdown
# QA报告 — [功能名称]

## QA配置
- 模式：Quick / Standard / Exhaustive
- 环境：[URL]
- 审查时间：[时间]

## 测试结果总览

| 测试项 | 结果 | 截图 | 控制台 |
|--------|------|------|--------|
| 首页加载 | ✅ PASS | - | 无ERROR |
| 表单提交 | ✅ PASS | - | 无ERROR |
| 空输入处理 | ❌ FAIL | 有 | ERROR: null |
| ... | ... | ... | ... |

## 健康分

```
Health Score: 85/100 🟡 Good

- 功能测试: 8/10 × 30% = 24.0
- 边界测试: 4/5 × 25% = 20.0
- 控制台无ERROR: ✓ × 25% = 25.0
- 无设计退化: ✓ × 20% = 16.0
```

## 🔴 发现的问题

### 1. [Bug标题]
- 页面：[页面]
- 操作：[如何重现]
- 预期：[应该怎样]
- 实际：[实际怎样]
- 影响：P0/P1/P2
- 修复建议：[代码方案]

## 重验证

修复提交: `[commit hash]`
重新测试时间: [时间]
结果: ✅ 已修复 / ❌ 仍未修复

## 发布建议

🟢 Ready to ship / 🟡 Fix X issues before ship / 🔴 Do not ship
```
