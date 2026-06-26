---
name: identity-trust
display_name: 身份信托
version: 1.0.0
author: ZhenStaff
category: security
description: 面向 AI Agent 的去中心化身份（DID）和可验证凭证管理系统
tags: [did, identity, credentials, trust, w3c, blockchain, security, ai-agent, openclaw]
repository: https://github.com/ZhenRobotics/openclaw-identity-trust
license: MIT
---

# 🔐 身份信托 Skill

面向 AI Agent 的去中心化身份（DID）和可验证凭证管理系统，基于 W3C DID Core 和 W3C Verifiable Credentials 标准构建。

## 📋 概述

身份信托提供完整的去中心化身份管理解决方案，使 AI Agent 能够：
- 创建和管理去中心化标识符（DID）
- 签发和验证符合 W3C 标准的可验证凭证
- 建立 Agent 之间的信任关系
- 安全管理加密密钥
- 本地存储身份数据，保护隐私

## 📦 安装

### 步骤 1：安装软件包

**方式 A：通过 npm 安装（推荐）**

```bash
# 全局安装以使用 CLI
npm install -g openclaw-identity-trust

# 验证安装
identity-trust --version
```

**方式 B：从 GitHub 安装**

```bash
# 克隆仓库
git clone https://github.com/ZhenRobotics/openclaw-identity-trust.git
cd openclaw-identity-trust

# 安装依赖
npm install

# 构建
npm run build
```

### 步骤 2：验证安装

```bash
# 检查 CLI 是否正常工作
identity-trust info

# 创建你的第一个 DID
identity-trust did create
```

## 🚀 使用方法

### 何时使用此 Skill

**自动触发**条件（当用户消息包含以下内容时）：

- 关键词：`DID`、`可验证凭证`、`身份`、`信任`、`去中心化身份`
- 询问创建或管理数字身份
- 需要验证凭证或建立信任
- 想要实现 W3C DID/VC 标准
- 构建 Agent 身份认证系统

**触发示例**：
- "为我的 AI Agent 创建一个 DID"
- "签发一个可验证凭证"
- "如何验证这个凭证？"
- "设置去中心化身份用于身份认证"
- "评估这个 Agent 的信任等级"

**不使用此 Skill** 的场景：
- 仅需通用身份/密码管理（使用密码管理器）
- OAuth/SAML 认证（使用标准认证库）
- 简单用户账户（使用传统数据库）

## 🎯 核心功能

### 1. DID 管理
- **did:key** - 自包含，无需注册中心
- **did:web** - Web 托管的 DID，可公开验证
- **did:ethr** - 基于以太坊的 DID（基础支持）

### 2. 可验证凭证
- 符合 W3C VC 数据模型 1.1
- Ed25519 和 secp256k1 签名
- 过期日期管理
- 自定义声明支持

### 3. 信任评估
- 基于策略的信任评分
- 凭证验证
- 签发者信任链
- 声誉系统

### 4. 安全性
- Ed25519 现代密码学（默认）
- secp256k1 以太坊兼容签名
- 本地密钥存储于 `~/.openclaw/identity/`
- 无外部密钥依赖

## 💻 工具

此 Skill 为 AI Agent 提供 6 个核心工具：

### 1. `did_create` - 创建去中心化标识符

为 Agent 或实体创建新的 DID。

**参数**：
- `method`（字符串，可选）：DID 方法 - `key`、`web` 或 `ethr`（默认：`key`）
- `keyType`（字符串，可选）：加密密钥类型 - `Ed25519` 或 `secp256k1`（默认：`Ed25519`）
- `save`（布尔值，可选）：保存到本地存储（默认：`true`）

**返回值**：
- `did`（字符串）：生成的 DID 标识符
- `document`（对象）：完整的 DID 文档

**示例**：
```bash
identity-trust did create --method key --key-type Ed25519
```

### 2. `did_resolve` - 解析 DID 到文档

将 DID 解析为其 DID 文档。

**参数**：
- `did`（字符串，必需）：要解析的 DID（例如：`did:key:z6Mkf...`）

**返回值**：
- `document`（对象）：包含验证方法的 DID 文档

**示例**：
```bash
identity-trust did resolve did:key:z6MkfzZZD5gxQ...
```

### 3. `vc_issue` - 签发可验证凭证

签发符合 W3C 标准的可验证凭证。

**参数**：
- `issuerDid`（字符串，必需）：签发者的 DID
- `subjectDid`（字符串，必需）：主体的 DID
- `claims`（对象，必需）：要包含在凭证中的声明
- `type`（字符串，可选）：凭证类型（默认：`VerifiableCredential`）
- `expirationDays`（数字，可选）：有效期天数

**返回值**：
- `credential`（对象）：已签名的可验证凭证

**示例**：
```bash
identity-trust vc issue \
  --issuer did:key:z6Mkf... \
  --subject did:key:z6Mkp... \
  --claims '{"role":"developer","level":"senior"}' \
  --expiration 90
```

### 4. `vc_verify` - 验证凭证

验证可验证凭证的真实性和有效性。

**参数**：
- `credential`（对象，必需）：要验证的凭证
- `checkExpiration`（布尔值，可选）：检查过期日期（默认：`true`）

**返回值**：
- `verified`（布尔值）：凭证是否有效
- `checks`（对象）：详细验证结果

**示例**：
```bash
identity-trust vc verify <credential-id>
```

### 5. `identity_list` - 列出身份

列出所有存储的 DID 和凭证。

**参数**：无

**返回值**：
- `dids`（数组）：存储的 DID 列表
- `credentials`（数组）：存储的凭证列表

**示例**：
```bash
identity-trust did list
identity-trust vc list
```

### 6. `trust_evaluate` - 评估 Agent 信任度

基于凭证和策略评估 Agent 的信任等级。

**参数**：
- `agentDid`（字符串，必需）：要评估的 Agent DID
- `policy`（对象，可选）：信任策略配置

**返回值**：
- `trustLevel`（数字）：信任分数（0-100）
- `credentials`（数组）：用于评估的凭证
- `passed`（布尔值）：Agent 是否满足策略要求

**示例**：
```bash
# 编程式使用
import { evaluateTrust } from 'openclaw-identity-trust';

const result = await evaluateTrust('did:key:z6Mkf...', {
  minimumTrustLevel: 60,
  requiredCredentials: ['IdentityCredential'],
  trustedIssuers: ['did:key:authority...']
});
```

## 📚 CLI 命令

提供三个命令别名：
- `openclaw-identity-trust`
- `identity-trust`
- `idt`

### DID 命令

```bash
# 创建新的 DID
identity-trust did create [--method <key|web|ethr>] [--key-type <Ed25519|secp256k1>]

# 解析 DID
identity-trust did resolve <did>

# 列出所有 DID
identity-trust did list
```

### 可验证凭证命令

```bash
# 签发凭证
identity-trust vc issue \
  --issuer <did> \
  --subject <did> \
  --claims '<json>' \
  [--type <type>] \
  [--expiration <days>]

# 验证凭证
identity-trust vc verify <credential-id-or-json>

# 列出凭证
identity-trust vc list [--subject <did>]
```

### 实用命令

```bash
# 导出所有数据
identity-trust export

# 显示系统信息
identity-trust info
```

## 🔧 编程 API

在你的应用中作为 Node.js 库使用：

```typescript
import {
  generateDID,
  resolveDID,
  issueCredential,
  verifyCredential,
  LocalStorage
} from 'openclaw-identity-trust';

// 初始化存储
const storage = new LocalStorage();
await storage.initialize();

// 创建 DID
const { did, document, keyPair } = await generateDID('key', {
  keyType: 'Ed25519'
});

console.log('创建的 DID:', did);

// 签发凭证
const credential = await issueCredential({
  issuerDid: 'did:key:issuer...',
  issuerKeyPair: keyPair,
  subjectDid: did,
  claims: {
    role: 'ai-agent',
    capabilities: ['read', 'write', 'execute']
  },
  expirationDate: new Date(Date.now() + 90 * 24 * 60 * 60 * 1000)
});

// 验证凭证
const result = await verifyCredential(credential, {
  checkExpiration: true,
  localStore: storage.getDIDStore()
});

console.log('验证结果:', result.verified);
```

## 🎓 使用场景

### 1. AI Agent 身份

为 AI Agent 创建持久身份：

```bash
# 创建 Agent DID
identity-trust did create --method key

# 签发能力凭证
identity-trust vc issue \
  --issuer did:key:authority... \
  --subject did:key:agent... \
  --claims '{"agent":"GPT-Agent-001","capabilities":["api_access","data_read"]}'
```

### 2. 服务认证

验证访问服务的 Agent：

```typescript
const credential = await storage.getCredential(credentialId);
const result = await verifyCredential(credential);

if (result.verified) {
  // 授予服务访问权限
  console.log('访问已授权');
} else {
  console.log('访问被拒绝:', result.error);
}
```

### 3. 信任网络

在 Agent 之间建立信任关系：

```typescript
const trust = await evaluateTrust(agentDid, {
  minimumTrustLevel: 60,
  requiredCredentials: ['IdentityCredential', 'CapabilityCredential'],
  trustedIssuers: [authorityDid],
  allowExpired: false
});

if (trust.passed) {
  console.log(`Agent 受信任，信任等级: ${trust.trustLevel}%`);
}
```

## 📐 技术标准

本实现遵循以下标准：

- **W3C DID Core 1.0** - 去中心化标识符规范
- **W3C Verifiable Credentials Data Model 1.1** - 可验证凭证标准
- **Ed25519 Signature 2020** - 现代加密签名
- **Multibase Encoding** - Base58btc 编码用于 did:key

## 🔒 安全性

### 密码学
- **Ed25519** - 现代椭圆曲线签名（默认）
- **secp256k1** - 以太坊兼容签名
- **@noble/curves** - 经审计的密码学库
- **@noble/hashes** - 安全哈希

### 密钥存储
- 私钥本地存储于 `~/.openclaw/identity/`
- 无云存储或外部依赖
- 用户完全控制所有加密材料

### 最佳实践
1. 永远不要分享私钥
2. 始终为凭证设置过期日期
3. 信任前先验证凭证
4. 对关键操作使用强信任策略
5. 定期轮换密钥

## 🛠️ 配置

### 存储位置

默认：`~/.openclaw/identity/`

结构：
```
~/.openclaw/identity/
├── dids.json          # 存储的 DID 文档
├── credentials.json   # 签发/接收的凭证
└── keys.json          # 加密的私钥
```

### 环境变量

```bash
# 可选：自定义存储路径
OPENCLAW_IDENTITY_PATH=/custom/path

# 用于 did:web 解析（如果使用网络）
OPENCLAW_IDENTITY_NETWORK_ENABLED=true
```

## 🐛 故障排除

### 常见问题

**问题**：`Error: Private key not found`
```bash
# 解决方案：确保创建 DID 时保存了
identity-trust did create --save
```

**问题**：`Error: Failed to resolve DID`
```bash
# 解决方案：检查 DID 格式和网络设置
identity-trust did resolve did:key:z6Mkf...
```

**问题**：`Error: Signature verification failed`
```bash
# 解决方案：检查签发者 DID 和凭证完整性
identity-trust vc verify --no-expiration <credential>
```

## 📖 文档

- **完整文档**：[README.md](https://github.com/ZhenRobotics/openclaw-identity-trust#readme)
- **快速入门**：[QUICKSTART.md](https://github.com/ZhenRobotics/openclaw-identity-trust/blob/main/QUICKSTART.md)
- **API 参考**：[src/types.ts](https://github.com/ZhenRobotics/openclaw-identity-trust/blob/main/src/types.ts)
- **GitHub**：https://github.com/ZhenRobotics/openclaw-identity-trust
- **npm 包**：https://www.npmjs.com/package/openclaw-identity-trust

## 🔄 更新和变更日志

### v1.0.0 (2026-03-08)

首次发布，包含：
- DID 生成和解析（did:key、did:web、did:ethr）
- 可验证凭证签发和验证
- 信任评估系统
- 带 3 个命令别名的 CLI 工具
- 编程 API
- 带加密的本地存储
- 符合 W3C 标准

## 🤝 贡献

欢迎贡献！请：
1. Fork 仓库
2. 创建功能分支
3. 进行更改
4. 提交 Pull Request

## 📄 许可证

MIT 许可证 - 查看 [LICENSE](https://github.com/ZhenRobotics/openclaw-identity-trust/blob/main/LICENSE)

## 🔗 链接

- **GitHub**：https://github.com/ZhenRobotics/openclaw-identity-trust
- **npm**：https://www.npmjs.com/package/openclaw-identity-trust
- **ClawHub**：https://clawhub.ai/ZhenStaff/identity-trust
- **问题反馈**：https://github.com/ZhenRobotics/openclaw-identity-trust/issues

## 💬 支持

- **问题反馈**：https://github.com/ZhenRobotics/openclaw-identity-trust/issues
- **讨论**：https://github.com/ZhenRobotics/openclaw-identity-trust/discussions
- **邮箱**：support@zhenrobot.com

---

**用 ❤️ 为 OpenClaw 生态系统构建**
