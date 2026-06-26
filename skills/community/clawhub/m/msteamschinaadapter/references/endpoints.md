# MSTeams China Patch - 端点对照表

本文档列出 Microsoft Teams 全球版与中国版 (世纪互联) 的所有相关端点。

---

## 核心端点对照

### Azure AD 认证端点

| 用途 | 全球版 | 中国版 |
|------|--------|--------|
| **Authority** | `login.microsoftonline.com` | `login.chinacloudapi.cn` |
| **Authority (Partner)** | - | `login.partner.microsoftonline.cn` |
| **Discovery** | `login.microsoftonline.com/common/discovery/instance` | `login.chinacloudapi.cn/common/discovery/instance` |

### Bot Framework 端点

| 用途 | 全球版 | 中国版 |
|------|--------|--------|
| **API** | `api.botframework.com` | `api.botframework.azure.cn` |
| **Login** | `login.botframework.com` | `login.botframework.azure.cn` |
| **Token** | `token.botframework.com` | `token.botframework.azure.cn` |
| **JWKS** | `login.botframework.com/v1/.well-known/keys` | `login.botframework.azure.cn/v1/.well-known/keys` |

### Graph API 端点

| 用途 | 全球版 | 中国版 |
|------|--------|--------|
| **API** | `graph.microsoft.com` | `microsoftgraph.chinacloudapi.cn` |
| **v1.0** | `graph.microsoft.com/v1.0` | `microsoftgraph.chinacloudapi.cn/v1.0` |

---

## 详细端点列表

### AAD Token 端点

```
全球版:
https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token
https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize

中国版:
https://login.chinacloudapi.cn/{tenant}/oauth2/v2.0/token
https://login.chinacloudapi.cn/{tenant}/oauth2/v2.0/authorize
```

### AAD JWKS 端点

```
全球版:
https://login.microsoftonline.com/{tenant}/discovery/v2.0/keys
https://login.microsoftonline.com/common/discovery/v2.0/keys

中国版:
https://login.chinacloudapi.cn/{tenant}/discovery/v2.0/keys
https://login.chinacloudapi.cn/common/discovery/v2.0/keys
```

### AAD Issuer

```
全球版:
https://login.microsoftonline.com/{tenant}/v2.0
https://sts.windows.net/{tenant}/

中国版:
https://login.chinacloudapi.cn/{tenant}/v2.0
https://sts.chinacloudapi.cn/{tenant}/
```

### Bot Framework API

```
全球版:
https://api.botframework.com/v3/conversations
https://api.botframework.com/v3/conversations/{conversationId}/activities

中国版:
https://api.botframework.azure.cn/v3/conversations
https://api.botframework.azure.cn/v3/conversations/{conversationId}/activities
```

### Bot Token Scope

```
全球版:
https://api.botframework.com/.default

中国版:
https://api.botframework.azure.cn/.default
```

---

## MSAL 配置对照

### DEFAULT_AUTHORITY

```javascript
// 全球版
DEFAULT_AUTHORITY: "https://login.microsoftonline.com/common/"

// 中国版
DEFAULT_AUTHORITY: "https://login.chinacloudapi.cn/common/"
```

### DEFAULT_AUTHORITY_HOST

```javascript
// 全球版
DEFAULT_AUTHORITY_HOST: "login.microsoftonline.com"

// 中国版
DEFAULT_AUTHORITY_HOST: "login.chinacloudapi.cn"
```

### AAD_INSTANCE_DISCOVERY_ENDPT

```javascript
// 全球版
AAD_INSTANCE_DISCOVERY_ENDPT: "https://login.microsoftonline.com/common/discovery/instance?api-version=1.1&authorization_endpoint="

// 中国版
AAD_INSTANCE_DISCOVERY_ENDPT: "https://login.chinacloudapi.cn/common/discovery/instance?api-version=1.1&authorization_endpoint="
```

### GET_DEFAULT_TOKEN_AUTHORITY

```javascript
// 全球版
const GET_DEFAULT_TOKEN_AUTHORITY = (tenantId) => `https://login.microsoftonline.com/${tenantId}`;

// 中国版
const GET_DEFAULT_TOKEN_AUTHORITY = (tenantId) => `https://login.chinacloudapi.cn/${tenantId}`;
```

---

## JWT 验证配置

### allowedIssuer

```javascript
// 全球版
validateIssuer: { allowedIssuer: "https://api.botframework.com" }

// 中国版
validateIssuer: { allowedIssuer: "https://api.botframework.azure.cn" }
```

### audience

```javascript
// 全球版
audience: ["https://api.botframework.com"]

// 中国版
audience: ["https://api.botframework.azure.cn"]
```

### jwksUri

```javascript
// 全球版
jwksUri: "https://login.botframework.com/v1/.well-known/keys"

// 中国版
jwksUri: "https://login.botframework.azure.cn/v1/.well-known/keys"
```

---

## 补丁替换规则

### 必须替换的端点

| 全球端点 | 中国端点 | 优先级 |
|----------|----------|--------|
| `login.microsoftonline.com` (Authority) | `login.chinacloudapi.cn` | 高 |
| `api.botframework.com` | `api.botframework.azure.cn` | 高 |
| `login.botframework.com` | `login.botframework.azure.cn` | 高 |
| `token.botframework.com` | `token.botframework.azure.cn` | 高 |
| `graph.microsoft.com` | `microsoftgraph.chinacloudapi.cn` | 中 |

### 可选替换

| 全球端点 | 中国端点 | 说明 |
|----------|----------|------|
| `sts.windows.net` | `sts.chinacloudapi.cn` | AAD issuer |

---

## 环境变量配置

### 设置中国区端点

```bash
# AAD Authority
MSTEAMS_AUTHORITY=https://login.partner.microsoftonline.cn

# 或使用 chinacloudapi.cn
MSTEAMS_AUTHORITY=https://login.chinacloudapi.cn
```

---

## SSRF Allowlist 配置

### DEFAULT_MEDIA_HOST_ALLOWLIST

媒体下载 SSRF 安全策略的主机名后缀允许列表。

```javascript
// 全球版
const DEFAULT_MEDIA_HOST_ALLOWLIST = [
  "graph.microsoft.com",
  "graph.microsoft.us",
  "graph.microsoft.de",
  "graph.microsoft.cn",
  "sharepoint.com",
  "azureedge.net",
  "microsoft.com"
];

// 中国版 - 需要添加
const DEFAULT_MEDIA_HOST_ALLOWLIST = [
  "graph.microsoft.com",
  "graph.microsoft.us",
  "graph.microsoft.de",
  "graph.microsoft.cn",
  "microsoftgraph.chinacloudapi.cn",  // ⬅️ 新增
  "sharepoint.com",
  "azureedge.net",
  "microsoft.com"
];
```

### DEFAULT_MEDIA_AUTH_HOST_ALLOWLIST

认证请求 SSRF 安全策略的主机名后缀允许列表。

```javascript
// 全球版
const DEFAULT_MEDIA_AUTH_HOST_ALLOWLIST = [
  "api.botframework.azure.cn",
  "botframework.com",
  "smba.trafficmanager.net",
  "graph.microsoft.com",
  "graph.microsoft.us",
  "graph.microsoft.de",
  "graph.microsoft.cn"
];

// 中国版 - 需要添加
const DEFAULT_MEDIA_AUTH_HOST_ALLOWLIST = [
  "api.botframework.azure.cn",
  "botframework.com",
  "smba.trafficmanager.net",
  "graph.microsoft.com",
  "graph.microsoft.us",
  "graph.microsoft.de",
  "graph.microsoft.cn",
  "microsoftgraph.chinacloudapi.cn"  // ⬅️ 新增
];
```

### 错误症状

当 SSRF Allowlist 未包含中国端点时，会出现以下错误：

```
Blocked hostname (not in allowlist): microsoftgraph.chinacloudapi.cn
msteams.graph.message - SSRF blocked
msteams.graph.collection - SSRF blocked
```

### 修复方法

1. 定位 `graph-users-*.js` 文件
2. 添加 `microsoftgraph.chinacloudapi.cn` 到两个 Allowlist
3. 重启 Gateway

---

## 参考链接

- [Azure China 21Vianet 文档](https://docs.microsoft.com/azure/china/)
- [Microsoft Graph 中国端点](https://docs.microsoft.com/graph/deployments)
- [Bot Framework 区域](https://docs.microsoft.com/azure/bot-service/bot-builder-basics-regions)