---
name: golang-logging
description: >
  Golang 日志规范 SKILL。严格规定如何在 Golang 代码中添加日志，必须参考项目其他地方仿写，或使用指定的 xlogging.D().Error(fmt.Sprintf(...)) 形式。
  适用于所有 Golang 开发场景的日志记录，包括 MCP 客户端、后端服务、数据处理等。
metadata:
  label: Golang 日志规范
---

# Golang 日志规范 SKILL

## 一、执行模式（强约束）

本 SKILL 采用"强制规范执行模式"，必须遵守：

1. **禁止自行构造日志语句**，必须遵循本规范
2. 优先**参考项目中其他 Golang 代码进行仿写**
3. 如果找不到参考，则**必须**使用本 SKILL 规定的固定形式
4. 日志描述需清晰，包含上下文（服务名、操作、变量）

---

## 二、日志库引入

```go
import (
    "fmt"
    "your-company/xlogging"
)
```

---

## 三、日志使用规则

### 3.1 基本规则

| 规则项 | 说明 |
|--------|------|
| 优先仿写 | 参考项目中其他 Golang 代码进行仿写 |
| 固定形式 | 若无法找到参考，必须使用 `xlogging.D().Error(fmt.Sprintf("...：%+v", err))` 形式 |
| 字符串入参 | **Error 入参必须是字符串**，动态参数**必须**用 `fmt.Sprintf` 拼接 |
| 上下文清晰 | 日志描述需包含服务名、操作、变量等上下文信息 |

### 3.2 日志 Level 选择

| Level | 使用场景 | 示例 |
|-------|----------|------|
| **Error** | 错误/异常（必须 fmt.Sprintf） | 服务调用失败、数据库连接错误 |
| **Warn** | 潜在问题、非致命异常 | 非 200 状态码、降级处理 |
| **Info** | 关键业务成功、重要里程碑 | 服务启动完成、任务处理完成 |
| **Debug** | 调试信息（生产环境谨慎） | 参数打印、中间状态 |
| **Trace** | 详细追踪（开发环境使用） | 进入/离开函数 |

---

## 四、常见日志场景示例

### 4.1 错误处理（核心场景）

```go
// 基础错误日志
if err != nil {
    xlogging.D().Error(fmt.Sprintf("eagleeye service return err：%+v", err))
    return nil, err
}

// 完整上下文（推荐）
if err != nil {
    xlogging.D().Error(fmt.Sprintf("query organization failed, uuid: %s, err: %+v", uuid, err))
    return nil, fmt.Errorf("query organization failed: %w", err)
}

// 带数据的错误
if resp.StatusCode != http.StatusOK {
    xlogging.D().Error(fmt.Sprintf("mcp service returned non-200 status: %d, body: %s", resp.StatusCode, string(body)))
    return nil, fmt.Errorf("unexpected status code: %d", resp.StatusCode)
}
```

### 4.2 正常流程日志

```go
// 关键业务成功
xlogging.D().Info(fmt.Sprintf("successfully fetched %d organizations for keyword: %s", len(orgs), keyword))

// 调试信息
xlogging.D().Debug(fmt.Sprintf("mcp request params: %+v", params))
xlogging.D().Debug(fmt.Sprintf("processing batch %d/%d", current, total))

// 追踪信息
xlogging.D().Trace(fmt.Sprintf("entering %s function", funcName))
```

### 4.3 警告日志

```go
// 非致命异常
if resp.StatusCode != 200 {
    xlogging.D().Warn(fmt.Sprintf("mcp service returned non-200 status: %d, body: %s", resp.StatusCode, body))
}

// 降级处理
xlogging.D().Warn(fmt.Sprintf("cache miss for key: %s, falling back to database", key))
```

### 4.4 性能日志

```go
// 操作耗时统计
start := time.Now()
defer func() {
    xlogging.D().Info(fmt.Sprintf("operation completed, cost: %v", time.Since(start)))
}()

// 带上下文的性能日志
start := time.Now()
result, err := callMCP(ctx, toolName, params)
xlogging.D().Info(fmt.Sprintf("mcp call %s completed, cost: %v", toolName, time.Since(start)))
```

### 4.5 MCP 调用场景

```go
func callMCPTool(ctx context.Context, toolName string, params map[string]interface{}) (interface{}, error) {
    xlogging.D().Debug(fmt.Sprintf("calling mcp tool: %s, params: %+v", toolName, params))

    start := time.Now()
    resp, err := mcpClient.Call(ctx, toolName, params)
    if err != nil {
        xlogging.D().Error(fmt.Sprintf("mcp tool %s failed: %+v", toolName, err))
        return nil, err
    }

    xlogging.D().Info(fmt.Sprintf("mcp tool %s success, cost: %v", toolName, time.Since(start)))
    return resp, nil
}
```

---

## 五、生产环境注意事项

| 注意事项 | 说明 |
|----------|------|
| 日志级别 | 生产环境默认 Info 级别，Debug/Trace 谨慎开启 |
| Error 级别 | 必须始终记录，确保问题可追踪 |
| 敏感信息 | 禁止在日志中打印密码、Token、个人信息等敏感数据 |
| 日志大小 | 避免打印过大的响应体，可采样或截断 |
| 性能影响 | 高频操作避免过多日志，考虑异步或批量 |

---

## 六、严格禁止（NEVER DO）

| 禁止项 | 错误示例 | 正确做法 |
|--------|----------|----------|
| 自行发明格式 | `log.Printf("error: %v", err)` | `xlogging.D().Error(fmt.Sprintf("...：%+v", err))` |
| 直接传 err 对象 | `xlogging.D().Error(err)` | `xlogging.D().Error(fmt.Sprintf("...：%+v", err))` |
| 不记录关键错误 | 直接返回 err 而不记录 | 先记录再返回 |
| 日志级别滥用 | 用 Info 记录调试信息 | 使用 Debug/Trace |
| 敏感信息泄露 | 打印密码、Token | 脱敏或省略 |

---

## 七、参考

- 项目现有 Golang 代码（优先参考）
- `your-company/xlogging` 内部文档

---

**更新记录**：
- 2026/04/08 优化为标准 SKILL 格式（添加执行模式、规范结构、完善示例、添加禁止事项）
