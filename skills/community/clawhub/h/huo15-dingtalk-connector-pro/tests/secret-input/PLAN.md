# secret-input 模块测试方案

## 1. 目的与覆盖范围

`tests/secret-input` 覆盖密钥输入的 Schema 构建和验证功能，确保密钥配置的格式正确性，并提供相关的辅助函数。

主要覆盖（以测试文件实际引用为准）：

- Schema 构建：**buildSecretInputSchema**
- 辅助函数：**hasConfiguredSecretInput / normalizeSecretInputString / normalizeResolvedSecretInputString**

## 2. 用例表（覆盖现有测试）

### 2.1 buildSecretInputSchema

| 序号 | 输入 | 期望 |
|------|------|------|
| 1 | `"plain-secret"` | 解析成功，返回原字符串 |
| 2 | `{ source: "env", provider: "system", id: "DINGTALK_SECRET" }` | 解析成功，返回结构化对象 |
| 3 | `{ source: "env", provider: "", id: "" }` | 抛出异常（无效结构） |

### 2.2 重新导出的辅助函数

| 序号 | 输入 | 期望 |
|------|------|------|
| 4 | hasConfiguredSecretInput("abc") | true |
| 5 | normalizeSecretInputString(" a ") | `"a"` |
| 6 | normalizeResolvedSecretInputString({ value: " b ", path: "channels.dingtalk-connector.clientSecret" }) | `"b"` |

## 3. 预期正确输出与潜在错误

- **正确**：Schema 正确验证纯字符串密钥和结构化密钥引用；无效的结构化对象被正确拒绝；辅助函数行为符合预期。
- **潜在错误原因**：Schema 验证规则不完整，导致无效结构通过；辅助函数重新导出的行为与原实现不一致。
