---
name: model-rate-limiter
description: 限制大模型请求频率，每分钟不超指定次数（默认5次）。当用户提到"限制请求频率"、"限速"、"模型限流"、"每分钟不超过X次"时触发。
---

# Model Rate Limiter

限制 AI 模型请求频率，防止触发 API 限速。

## 配置文件

状态文件：`{workspace}/rate-limit-state.json`

```json
{
  "enabled": false,
  "maxPerMinute": 5,
  "windowMs": 60000,
  "timestamps": []
}
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `enabled` | 开关：`true`开启，`false`关闭 | `false` |
| `maxPerMinute` | 每分钟最大请求次数 | 5 |
| `windowMs` | 时间窗口（毫秒） | 60000 |

## 使用方式

### 查看当前状态

读取 `rate-limit-state.json` 文件。

### 开启限速

将 `enabled` 改为 `true`。

### 关闭限速

将 `enabled` 改为 `false`。

### 修改限制次数

修改 `maxPerMinute` 值，例如设为 3：

```json
{ "maxPerMinute": 3 }
```

### 手动重置计数

将 `timestamps` 设为空数组 `[]` 即可。

## 工作原理

每次模型请求前：
1. 读取 `rate-limit-state.json`
2. 若 `enabled: false`，直接放行
3. 若 `enabled: true`，清理 `windowMs` 外的旧时间戳
4. 若剩余次数 < 1，拒绝请求并提示等待
5. 否则写入当前时间戳，允许请求

## 示例对话

> 用户：开启限速  
> 操作：将 `enabled` 改为 `true`，回复"已开启限速，每分钟不超5次"

> 用户：改成每分钟3次  
> 操作：修改 `maxPerMinute: 3`，回复"已调整为每分钟3次"
