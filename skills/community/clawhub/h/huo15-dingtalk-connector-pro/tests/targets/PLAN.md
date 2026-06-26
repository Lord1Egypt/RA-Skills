# targets 模块测试方案

## 1. 目的与覆盖范围

`tests/targets` 覆盖目标（用户/群组）ID 的解析、格式化和验证功能，处理不同格式的钉钉目标标识。

主要覆盖（以测试文件实际引用为准）：

- 目标归一化：**normalizeDingtalkTarget**
- 目标格式化：**formatDingtalkTarget**
- 目标验证：**looksLikeDingtalkId**

## 2. 用例表（覆盖现有测试）

### 2.1 normalizeDingtalkTarget

| 序号 | 输入 | 期望 |
|------|------|------|
| 1 | `"   "`（空字符串） | null |
| 2 | `"dingtalk:user:abc"` | `"abc"` |
| 3 | `"dd:user: abc "` | `"abc"` |
| 4 | `"ding:user:abc"` | `"abc"` |
| 5 | `"dingtalk:group:conv-1"` | `"conv-1"` |
| 6 | `"user:"` | null（空后缀） |
| 7 | `"group:   "` | null（空后缀） |
| 8 | `"  user-id-001  "` | `"user-id-001"`（无标记直接返回） |

### 2.2 formatDingtalkTarget

| 序号 | 输入 | 期望 |
|------|------|------|
| 9 | `" conv ", "group"` | `"group:conv"` |
| 10 | `" user ", "user"` | `"user:user"` |
| 11 | `"  raw  "` | `"raw"`（无类型直接返回） |

### 2.3 looksLikeDingtalkId

| 序号 | 输入 | 期望 |
|------|------|------|
| 12 | `""` / `"  "` | false |
| 13 | `"abc"` | true |
| 14 | `"user:abc"` | true |
| 15 | `"group:conv"` | true |
| 16 | `"dingtalk:user:abc"` | true |

## 3. 预期正确输出与潜在错误

- **正确**：不同前缀（dingtalk/dd/ding）的提供商标识正确识别；用户和群组目标正确解析；空值和无效格式正确返回 null；格式化函数正确添加类型前缀。
- **潜在错误原因**：前缀识别不完整导致某些格式无法解析；空值判断逻辑遗漏；类型前缀添加错误。
