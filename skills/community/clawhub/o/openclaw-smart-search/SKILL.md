---
name: smart-search
description: 统一智能搜索技能，整合多个搜索引擎（百炼 MCP、Tavily、Serper、Exa、Firecrawl），自动选择最佳引擎并融合结果
homepage: https://github.com/openclaw/skills/tree/main/smart-search
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "bins": ["node", "mcporter"] },
        "env": ["OPENCLAW_MASTER_KEY"],
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "typescript ts-node @types/node dotenv",
              "label": "Install TypeScript dependencies",
            },
          ],
      },
  }
---

# Smart Search - 统一智能搜索

> **重要说明**: 本技能仅支持 CLI 方式调用，不提供 HTTP API。

## 快速开始

### 1. 安装依赖

点击技能卡片上的 **Install** 按钮，或手动运行：

```bash
cd ~/.agents/skills/smart-search
npm install
```

### 2. 配置 API Key

**方式一：使用配置向导（推荐）**

```bash
npm run setup
```

交互式输入 API Key，会自动加密存储到 `~/.openclaw/secrets/smart-search.json.enc`。

**方式二：逐个配置**

```bash
npm run key:set bailian
npm run key:set tavily
npm run key:set serper
npm run key:set exa
npm run key:set firecrawl
```

**方式三：从文件导入**

创建 `api-keys.json`：
```json
{
  "bailian": "sk-xxx",
  "tavily": "tvly-xxx",
  "serper": "xxx",
  "exa": "xxx",
  "firecrawl": "fc-xxx"
}
```

然后运行：
```bash
npm run key:import ./api-keys.json
```

### 3. 测试搜索

```bash
npm run search "OpenClaw 新功能"
```

## CLI 使用方式

### 基本搜索

```bash
# 在技能目录下执行
cd ~/.agents/skills/smart-search
npm run search "搜索内容"
```

### 带参数搜索

```bash
# 指定结果数量
npm run search "OpenClaw 新功能" -- --count=10

# 学术搜索（优先使用 Exa）
npm run search "LLM Agent planning" -- --intent=academic

# 技术搜索
npm run search "TypeScript 最佳实践" -- --intent=technical

# 新闻搜索
npm run search "最新 AI 动态" -- --intent=news

# 指定语言
npm run search "OpenClaw" -- --language=zh
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--count=<n>` | 返回结果数量 | 10 |
| `--language=<zh\|en>` | 语言偏好 | auto |
| `--intent=<type>` | 搜索意图 | general |
| `--timeout=<ms>` | 超时时间 | 5000 |

**intent 可选值**:
- `general` - 通用搜索
- `academic` - 学术搜索（优先 Exa）
- `technical` - 技术搜索（优先 Exa）
- `news` - 新闻搜索（优先 Tavily）

## API Key 管理

### 配置向导

```bash
npm run setup
```

交互式配置所有引擎。

### 查看状态

```bash
npm run key:status
```

显示所有引擎的配置状态和配额使用情况。

### 添加引擎

```bash
npm run key:set exa
```

### 轮换 Key

```bash
npm run key:rotate bailian
```

## 支持的搜索引擎

所有 5 个搜索引擎均已完整实现：

| 引擎 | 状态 | 免费额度 | 用途 | 配置命令 |
|------|------|----------|------|----------|
| 百炼 MCP | ✅ 已实现 | 2000 次/月 | 中文搜索 | `npm run key:set bailian` |
| Tavily | ✅ 已实现 | 1000 次/月 | 高级搜索 | `npm run key:set tavily` |
| Serper | ✅ 已实现 | 2500 次/月 | Google 结果 | `npm run key:set serper` |
| Exa | ✅ 已实现 | 1000 次/月 | 学术/技术搜索 | `npm run key:set exa` |
| Firecrawl | ✅ 已实现 | 500 页/月 | 网页抓取 | `npm run key:set firecrawl` |

**总计**: 约 7500 次/月搜索额度 🔍

### 智能路由策略

- **中文查询** → 百炼（中文优化）
- **英文查询** → Serper（Google 结果）
- **学术意图** → 添加 Exa
- **技术意图** → 添加 Exa
- **新闻意图** → 添加 Tavily
- **自动降级** → 引擎失败时自动切换备用引擎

## 技术细节

- **加密**: AES-256-GCM
- **文件位置**: `~/.openclaw/secrets/smart-search.json.enc`
- **文件权限**: 0o600（仅所有者可读写）
- **密钥派生**: PBKDF2（10 万轮迭代）

## 故障排查

### 查看所有引擎状态

```bash
npm run key:status
```

### 测试单个引擎

```bash
npm run key:get bailian
npm run search "test"
```

### 重新配置

```bash
# 删除旧配置
rm ~/.openclaw/secrets/smart-search.json.enc

# 重新配置
npm run setup
```
---

## 🔑 密钥管理

### 主密钥配置

Smart Search 使用 **AES-256-GCM** 加密存储 API Keys，需要配置主密钥。

#### 方式一：环境变量（推荐）

```bash
# 生成强随机密钥
openssl rand -base64 32

# 设置环境变量
export OPENCLAW_MASTER_KEY="your-generated-key-at-least-32-characters"
```

或在 `.env` 文件中配置：

```env
OPENCLAW_MASTER_KEY=your-generated-key-at-least-32-characters
```

#### 方式二：.env 文件

```bash
# 复制示例文件
cp .env.example .env

# 编辑配置
nano .env
```

⚠️ **安全要求**：
- 主密钥至少 32 个字符
- 使用随机生成的密钥，不要使用密码或短语
- 不要将 `.env` 文件提交到版本控制
- 生产环境应使用密钥管理服务

### 密钥轮换

定期轮换 API Key 以增强安全性：

```bash
# 查看当前状态
npm run key:status

# 轮换指定引擎
npm run key:rotate bailian

# 完全重新配置
rm ~/.openclaw/secrets/smart-search.json.enc
npm run setup
```

### 加密技术细节

| 项目 | 说明 |
|------|------|
| **加密算法** | AES-256-GCM |
| **密钥派生** | PBKDF2-SHA256 |
| **迭代次数** | 100,000 轮 |
| **盐值** | 随机生成 16 字节盐，与加密配置一起存储 |
| **存储位置** | `~/.openclaw/secrets/smart-search.json.enc` |
| **文件权限** | 0o600（仅所有者可读写） |

---

## 🔐 安全性

### 数据安全

- **API Key 存储**: 使用 AES-256-GCM 加密存储
- **文件权限**: 配置文件权限为 0o600（仅所有者可读写）
- **无日志记录**: API Key 不会记录到日志中
- **隐私保护**: API Key 本地加密存储，搜索请求直接发送到各搜索引擎官方 API

### 输入验证

- **命令注入防护**: 所有用户输入经过严格验证和转义
- **长度限制**: 搜索关键词最大长度 500 字符
- **特殊字符过滤**: 自动过滤危险字符（`;`, `&`, `|`, `` ` ``, `$`, 等）
- **类型验证**: 所有参数经过类型检查

### 最佳实践

1. ✅ 定期轮换 API Key
2. ✅ 使用环境变量存储 Master Key
3. ✅ 不要分享加密配置文件
4. ✅ 在受信任的环境中运行
5. ✅ 定期更新依赖包

### 审计

- **访问日志**: 记录所有 API Key 的访问（不记录 Key 本身）
- **错误日志**: 记录错误但不包含敏感信息
- **可配置**: 可以禁用日志记录

---

## 🔐 安全说明

### 主密钥（OPENCLAW_MASTER_KEY）

**要求**：
- ✅ 至少 32 字符
- ✅ 使用强随机字符串
- ✅ 通过环境变量设置
- ✅ 不要提交到版本控制

**设置方法**：

```bash
# Linux/macOS
export OPENCLAW_MASTER_KEY="your-32-char-secure-random-string-here"

# 或添加到 ~/.bashrc 或 ~/.zshrc（推荐）
echo 'export OPENCLAW_MASTER_KEY="your-key"' >> ~/.bashrc
source ~/.bashrc

# Windows PowerShell
$env:OPENCLAW_MASTER_KEY="your-32-char-secure-random-string-here"

# 或添加到 $PROFILE
echo '$env:OPENCLAW_MASTER_KEY="your-key"' >> $PROFILE
```

**生成安全的主密钥**：

```bash
# Linux/macOS
openssl rand -base64 32

# 或使用 Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

**安全警告**：
- ⚠️ 不要在终端打印密钥
- ⚠️ 不要提交到 Git
- ⚠️ 不要分享给他人
- ⚠️ 定期轮换密钥

### 密钥管理实现

**加密算法**：
- AES-256-GCM（认证加密）
- PBKDF2 密钥派生（10 万轮迭代）
- 随机盐（16 字节，每次加密都不同）

**密钥生命周期**：
1. 主密钥通过环境变量提供
2. 使用 PBKDF2 派生加密密钥
3. 随机盐与加密数据一起存储
4. API Key 加密存储在 `~/.openclaw/secrets/smart-search.json.enc`
5. 文件权限：0o600（仅所有者可读写）

**代码位置**：
- 密钥管理：`src/key-manager.ts`
- 输入验证：`src/utils/sanitize.ts`
- 安全执行：`src/engines/bailian.ts`（使用 spawn，shell: false）

### 安全最佳实践

1. ✅ 定期轮换 API Key
2. ✅ 使用环境变量存储 Master Key
3. ✅ 不要分享加密配置文件
4. ✅ 在受信任的环境中运行
5. ✅ 定期更新依赖包
6. ✅ 在权限有限的用户账户中运行
7. ✅ 检查依赖：`npm audit`
8. ✅ 运行测试：`npm test`

### 安全审计

**已完成的修复**：
- ✅ Shell 注入修复（v1.0.3）- 使用 spawn 替代 exec
- ✅ 输入验证增强（v1.0.3）- 白名单 + 注入检测
- ✅ 密钥管理完善（v1.0.3）- 环境变量 + 加密
- ✅ 随机盐生成（v1.0.3）- 每次加密都使用新盐
- ✅ 自动加载 .env（v1.0.11）- 不需要手动 source

**ClawHub 安全扫描**：
- ✅ 无硬编码密钥
- ✅ 无恶意网络调用
- ✅ 依赖包安全
- ✅ 代码符合声明的目的

### Shell 命令执行安全说明

**静态分析警告说明**：

ClawHub 静态分析工具检测到代码中使用 `child_process`，但这**不是安全问题**：

**安全实践**：
```typescript
// ✅ 安全：使用 spawn，参数作为数组传递
spawn('mcporter', ['call', 'WebSearch.bailian_web_search', `query=${query}`], {
  shell: false,  // 不通过 shell 执行
  stdio: ['pipe', 'pipe', 'pipe']
});

// ❌ 不安全：使用 exec，参数经过 shell 解析
exec(`mcporter call ... query="${query}"`);  // 有注入风险
```

**代码位置**：
- `src/engines/bailian.ts` - 使用 `spawn()` + `shell: false`
- `scripts/doctor.ts` - 使用 `spawnSync()` 检查依赖
- `scripts/setup-bailian.ts` - 使用 `spawnSync()` 检查配置

**为什么安全**：
1. ✅ 使用 `spawn()` 而非`exec()`
2. ✅ 参数作为数组传递，不经过 shell 解析
3. ✅ 设置 `shell: false` 明确禁用 shell
4. ✅ 所有输入经过 `validateSearchQuery()` 验证
5. ✅ 无用户输入直接传递给 shell

**参考**：
- Node.js 安全最佳实践：https://nodejs.org/en/docs/guides/security/#child-processes
- OWASP 命令注入防护：https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html

### 故障排查

**问题**: "Salt not found in config file"

**原因**: v1.0.3 的安全修复使用随机盐，旧配置文件不兼容

**解决方案**:
```bash
# 删除旧配置文件
rm ~/.openclaw/secrets/smart-search.json.enc

# 重新配置
npm run setup
```

**问题**: "OPENCLAW_MASTER_KEY environment variable is required"

**原因**: 未设置主密钥环境变量

**解决方案**:
```bash
# 设置环境变量
export OPENCLAW_MASTER_KEY="your-32-char-secure-random-string"

# 或添加到 ~/.bashrc
echo 'export OPENCLAW_MASTER_KEY="your-key"' >> ~/.bashrc
source ~/.bashrc
```
