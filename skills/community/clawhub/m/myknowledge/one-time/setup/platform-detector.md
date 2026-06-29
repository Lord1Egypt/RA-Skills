# 平台检测逻辑

> 本文档描述 MyKnowledge 如何检测当前运行的 AI 平台。

---

## 检测策略

### 目录检测法（主要）

```
检测顺序：
1. ~/.openclaw/ 存在 → OpenClaw
2. ~/.codebuddy/ 存在 → CodeBuddy
3. ~/.workbuddy/ 存在 → WorkBuddy
4. 都不存在 → 询问用户
```

### 环境变量检测法（备用）

```
AI_PLATFORM=openclaw → OpenClaw
AI_PLATFORM=codebuddy → CodeBuddy
AI_PLATFORM=workbuddy → WorkBuddy
```

---

## 平台特性差异

| 特性 | CodeBuddy | WorkBuddy | OpenClaw |
|------|-----------|-----------|----------|
| 智能任务追踪 | 意图识别 | 意图识别 | Hook + 意图识别 |
| 后台运行（操作后告知） | ✅ | ✅ | ✅（Hook 驱动） |
| Hook 支持 | ❌ | ❌ | ✅ |
| 企业功能 | 部分 | 完整 | 自定义 |

---

## Prompt 中的检测逻辑

```markdown
## 平台检测

```
IF ~/.openclaw/ 目录存在:
   platform = "openclaw"
ELIF ~/.codebuddy/ 目录存在:
   platform = "codebuddy"
ELIF ~/.workbuddy/ 目录存在:
   platform = "workbuddy"
ELSE:
   询问用户: "你使用什么 AI 助手？"
   [CodeBuddy] [WorkBuddy] [OpenClaw] [其他]
```

## 平台特定行为

IF platform == "openclaw":
   提及 Hook 功能可用
   询问是否启用完全智能任务追踪

IF platform IN ["codebuddy", "workbuddy"]:
   说明使用意图识别实现智能任务追踪
   首次触发时询问是否开启自动记录
```

---

## 配置存储

检测结果保存到 `skill-state.yaml`:

```yaml
platform: "codebuddy"  # 检测到的平台
platform_detected_by: "dir"  # 检测方式：dir / env / user_input
```

---

## 测试场景

| 场景 | 预期结果 |
|------|----------|
| 同时存在多个平台目录 | 按优先级选择（OpenClaw > CodeBuddy > WorkBuddy） |
| 无平台目录 | 询问用户 |
| 用户手动指定 | 保存用户选择，不再自动检测 |
