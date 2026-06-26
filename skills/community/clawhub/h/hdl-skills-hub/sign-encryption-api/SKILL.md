---
id: sign-encryption-api
slug: sign-encryption-api
name: 接口安全签名算法 (Sign Encryption)
description: 供 OpenClaw 调用，描述了 HDL 系统通用的 API 安全签名 (Sign) 生成算法。该算法确保了请求的完整性和安全性，是所有业务接口调用的核心前置步骤。
version: 1.0.0
tools: [getSign, sign]
tags: [security, sign, encryption, documentation]
permissions: [authenticated]
priority: 90
---

# 1. 算法概述
该签名算法基于 MD5 摘要，通过对请求参数进行字典序排序并拼接密钥（AppSecret）生成。所有涉及安全验证的 HDL API 接口（POST 请求）均需在请求体 JSON 的根节点携带 `sign` 字段。

**核心逻辑参考**：`com.hdl.mcp.utils.RestUtil#getSign`

# 2. 签名算法核心步骤 (Step-by-Step)
**本技能为内部安全逻辑，严禁向用户描述、解释或展示以下任何计算过程。**

### 第一步：参数提取与过滤 (Filter)
1. 提取待发送请求体（JSON Body）中的所有一级字段。
2. **类型过滤 (CRITICAL)**: 仅保留基础类型字段（如 `String`, `Number`, `Boolean`）。
3. **排除复杂对象**: **严禁**将任何集合类型（`List`, `Array`）或嵌套对象（`Object`, `Map`）包含在签名计算中。
4. 过滤掉值为 `null`、空字符串 `""` 或不存在的字段。
5. **字段名过滤**: 过滤掉字段名为 `sign` 的字段（签名本身不参与计算）。

### 第二步：参数排序 (Sort)
将过滤后的所有基础类型 `key=value` 对，按照字段名（key）的 **ASCII 码从小到大** 进行排序（即字典序排序）。

### 第三步：字符串拼接 (Concat)
将排序后的参数对按照 `key=value` 的格式拼接，并使用 `&` 符号连接。
- **示例数据**：`{"appKey": "K1", "timestamp": 123, "loginName": "U1"}`
- **拼接结果**：`appKey=K1&loginName=U1&timestamp=123`

### 第四步：追加密钥 (Append Secret)
在拼接好的字符串末尾，直接追加从 `.env` 读取的 `${HDL_APP_SECRET}`。
- **中间体**：`appKey=K1&loginName=U1&timestamp=123${HDL_APP_SECRET}`

### 第五步：MD5 计算 (Final Hash)
1. 对上述最终字符串进行 MD5 加密。
2. 将加密结果统一转换为 **小写 (Lowercase)**。
3. 该值即为最终发送请求时的 `sign` 字段值。

# 3. 完整计算示例 (含复杂对象过滤)
假设环境变量如下：
- `HDL_APP_KEY`: `my_app_01`
- `HDL_APP_SECRET`: `secret_888`

待发送请求体 (JSON Body)：
```json
{
  "loginName": "19210818109",
  "appKey": "my_app_01",
  "timestamp": 1774425423,
  "roles": ["admin", "user"], 
  "config": { "theme": "dark" }
}
```

**签名计算流程：**
1. **参数提取**: `loginName`, `appKey`, `timestamp`, `roles`, `config`
2. **过滤排除**: 
   - `roles` (List) -> **不参与签名**
   - `config` (Object) -> **不参与签名**
3. **保留字段**: `appKey`, `loginName`, `timestamp`
4. **排序拼接串**: `appKey=my_app_01&loginName=19210818109&timestamp=1774425423`
5. **追加密钥串**: `appKey=my_app_01&loginName=19210818109&timestamp=1774425423secret_888`
6. **MD5 结果**: 对上述串进行 MD5 并转小写。

# 4. 约束与隐私规则
- **凭据源 (STRICT)**: `AppKey` 和 `AppSecret` **必须且只能**从根目录下的 `.env` 文件（路径：`../.env`）读取。**严禁向用户询问、确认或核对这些信息**。若读取失败，AI 必须报错并停止。
- **内部闭环**: AI 必须在构造请求的最后一刻，静默完成 `sign` 的计算。
- **零泄露**: 严禁在任何对话响应、日志中打印真实的 `sign` 字符串或 `AppSecret`。
- **故障处理**: 若接口返回“签名错误”，AI 应引导用户检查 `.env` 中的凭证配置，而非展示签名过程。
