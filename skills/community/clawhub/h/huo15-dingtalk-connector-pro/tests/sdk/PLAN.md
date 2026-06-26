# sdk/helpers 模块测试方案

## 1. 目的与覆盖范围

`tests/sdk/helpers` 覆盖 SDK 层的工具函数集合，负责账号ID归一化、密钥输入处理、群组策略解析、频道状态管理等核心辅助功能。

主要覆盖（以测试文件实际引用为准）：

- 账号ID处理：**normalizeAccountId / DEFAULT_ACCOUNT_ID**
- 密钥输入验证：**isSecretInputRef / normalizeSecretInputString / resolveSecretInputValue / hasConfiguredSecretInput / normalizeResolvedSecretInputString**
- 群组策略：**resolveDefaultGroupPolicy / resolveAllowlistProviderRuntimeGroupPolicy**
- 频道状态：**createDefaultChannelRuntimeState / buildBaseChannelStatusSummary**
- 杂项工具：**addWildcardAllowFrom / formatDocsLink / normalizeString / parseAllowFromInput**

## 2. 用例表（覆盖现有测试）

### 2.1 normalizeAccountId

| 序号 | 输入 | 期望 |
|------|------|------|
| 1 | `"default"` / `"  DEFAULT  "` / `""` | 归一化为 DEFAULT_ACCOUNT_ID |
| 2 | `"  MyAccount  "` | 归一化为小写并去空格 `"myaccount"` |

### 2.2 isSecretInputRef

| 序号 | 输入 | 期望 |
|------|------|------|
| 3 | `{ source: "env", provider: "system", id: "KEY" }` | true |
| 4 | `{ source: "file", provider: "p", id: "i" }` | true |
| 5 | `null` / `"str"` / `{ source: "env" }` / `{ source: "env", provider: "", id: "x" }` | false |

### 2.3 normalizeSecretInputString

| 序号 | 输入 | 期望 |
|------|------|------|
| 6 | `"  abc  "` | `"abc"` |
| 7 | `""` | undefined |
| 8 | `{ source: "env", provider: "p", id: "i" }` | `"<env:p:i>"` |
| 9 | `42` | undefined |

### 2.4 resolveSecretInputValue

| 序号 | 输入 | 期望 |
|------|------|------|
| 10 | `"val"` | `"val"` |
| 11 | `"  "` | undefined |
| 12 | env ref + allowEnvRead=true | 解析环境变量值 |
| 13 | env ref + allowEnvRead 未设置 | 返回 ref 字符串 `"<env:system:TEST_SECRET_VAR>"` |
| 14 | file/exec ref | 返回 ref 字符串 `"<file:p:f>"` |
| 15 | `123` | undefined |

### 2.5 hasConfiguredSecretInput

| 序号 | 输入 | 期望 |
|------|------|------|
| 16 | `"abc"` | true |
| 17 | `"  "` | false |
| 18 | env ref + 环境变量已设置 | true |
| 19 | env ref + 环境变量未设置 | false |
| 20 | file/exec ref | true |
| 21 | `null` | false |

### 2.6 normalizeResolvedSecretInputString

| 序号 | 输入 | 期望 |
|------|------|------|
| 22 | `{ value: "abc", path: "p" }` | `"abc"` |
| 23 | `{ value: "  ", path: "p" }` | 抛出异常（non-empty） |
| 24 | env ref + 环境变量已设置 | 解析环境变量值 |
| 25 | env ref + 环境变量未设置 | 抛出异常（not set） |
| 26 | file/exec ref | 返回 ref 字符串 `"<file:p:f>"` |
| 27 | `{ value: 42, path: "p" }` | 抛出异常（must be a string or SecretInput） |

### 2.7 群组策略 helpers

| 序号 | 输入 | 期望 |
|------|------|------|
| 28 | resolveDefaultGroupPolicy({}) | `"open"` |
| 29 | resolveDefaultGroupPolicy 有配置 | 返回配置的 groupPolicy |
| 30 | resolveAllowlistProviderRuntimeGroupPolicy + providerConfigPresent=true | 返回配置的 groupPolicy |
| 31 | resolveAllowlistProviderRuntimeGroupPolicy + providerConfigPresent=true + 无 groupPolicy | 返回 defaultGroupPolicy |
| 32 | resolveAllowlistProviderRuntimeGroupPolicy + providerConfigPresent=false | 返回 `"disabled"` |

### 2.8 频道状态 helpers

| 序号 | 输入 | 期望 |
|------|------|------|
| 33 | createDefaultChannelRuntimeState | 返回包含 accountId、running=false 的状态对象 |
| 34 | buildBaseChannelStatusSummary | 填充默认值（running=false、lastStartAt=null） |

### 2.9 杂项 helpers

| 序号 | 输入 | 期望 |
|------|------|------|
| 35 | addWildcardAllowFrom() | `["*"]` |
| 36 | addWildcardAllowFrom(["u1"]) | `["u1", "*"]` |
| 37 | addWildcardAllowFrom(["u1", "*"]) | `["u1", "*"]` |
| 38 | formatDocsLink("/test", "label") | 包含 "/test" 的链接 |
| 39 | normalizeString("  a  ") | `"a"` |
| 40 | normalizeString("") / normalizeString(123) | undefined |
| 41 | parseAllowFromInput("a, b; c\nd") | `["a", "b", "c", "d"]` |

## 3. 预期正确输出与潜在错误

- **正确**：账号ID归一化逻辑统一；密钥输入验证严格区分有效/无效引用；环境变量解析正确处理允许/不允许读取的场景；群组策略按优先级正确解析；频道状态正确填充默认值。
- **潜在错误原因**：密钥引用结构不完整时未正确识别；环境变量未设置时未抛出异常或返回错误值；群组策略优先级判断错误；默认值填充遗漏导致状态不一致。
