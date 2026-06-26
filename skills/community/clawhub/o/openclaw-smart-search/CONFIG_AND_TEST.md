# Smart Search v1.0.9 配置和测试指南

> **创建时间**: 2026-03-26 01:28  
> **版本**: v1.0.9  
> **状态**: ✅ 配置完成，等待 API Key 配置

---

## 📋 当前配置状态

### ✅ 已完成

| 配置项 | 状态 | 说明 |
|--------|------|------|
| 主密钥生成 | ✅ 已完成 | 44 字符随机密钥 |
| 主密钥保存 | ✅ 已完成 | 保存在 `.env` 文件 |
| 加密配置文件 | ✅ 已完成 | v2.0 格式，带随机盐 |
| 文件权限 | ✅ 已完成 | 0o600（仅所有者可读写） |
| 项目依赖 | ✅ 已安装 | 所有 npm 包已安装 |
| 路由逻辑 | ✅ 已验证 | 所有优化已实现 |

### ⏳ 待完成

| 配置项 | 状态 | 说明 |
|--------|------|------|
| API Keys 配置 | ⏳ 待配置 | 需要至少配置一个引擎 |

---

## 🔧 配置步骤

### 方法 1：使用快速配置脚本（推荐）

```bash
cd ~/.agents/skills/openclaw-smart-search
bash scripts/quick-setup.sh
```

**步骤**：
1. 自动生成主密钥
2. 选择要配置的引擎
3. 输入 API Key
4. 自动完成配置

---

### 方法 2：手动配置

#### 步骤 1：加载主密钥

```bash
cd ~/.agents/skills/openclaw-smart-search
export OPENCLAW_MASTER_KEY=$(grep OPENCLAW_MASTER_KEY .env | cut -d'=' -f2)
echo "✅ 主密钥已加载（${#OPENCLAW_MASTER_KEY}字符）"
```

#### 步骤 2：配置 API Key

**选择至少一个引擎配置**：

**百炼 MCP**（中文搜索，2000 次/月）：
```bash
# 获取 API Key: https://dashscope.console.aliyun.com/apiKey
export BAILIAN_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxx"
```

**Tavily**（高级搜索，1000 次/月）：
```bash
# 获取 API Key: https://app.tavily.com/home
export TAVILY_API_KEY="tvly-xxxxxxxxxxxxxxxxxxxxxxxx"
```

**Serper**（Google 结果，2500 次/月）：
```bash
# 获取 API Key: https://serper.dev/dashboard
export SERPER_API_KEY="xxxxxxxxxxxxxxxxxxxxxxxx"
```

**Exa**（学术/技术，1000 次/月）：
```bash
# 获取 API Key: https://dashboard.exa.ai/api-keys
export EXA_API_KEY="xxxxxxxxxxxxxxxxxxxxxxxx"
```

**Firecrawl**（网页抓取，500 页/月）：
```bash
# 获取 API Key: https://www.firecrawl.dev/app/api-keys
export FIRECRAWL_API_KEY="fc-xxxxxxxxxxxxxxxxxxxxxxxx"
```

#### 步骤 3：运行配置向导

```bash
npm run setup
```

**交互式输入**所有引擎的 API Key。

#### 步骤 4：验证配置

```bash
npm run doctor
```

**预期输出**：
```
✅ Node.js              版本 v22.22.0
✅ npm                  版本 10.9.4
✅ mcporter             0.7.3
✅ OPENCLAW_MASTER_KEY  已设置
✅ 加密配置文件         权限正确
✅ API Keys             已配置（加密存储）
✅ 项目依赖             已安装
```

---

## 🧪 测试用例

### 测试 1：简单查询（应使用 2 个引擎）

```bash
npm run search "test"
```

**预期**：
- 引擎数：2 个
- 耗时：~2 秒
- 结果数：5-10 条

---

### 测试 2：普通查询（应使用 3 个引擎）

```bash
npm run search "OpenClaw 智能搜索"
```

**预期**：
- 引擎数：3 个
- 耗时：~2-3 秒
- 结果数：10-15 条

---

### 测试 3：学术场景（应包含 Exa）

```bash
npm run search "transformer 论文"
```

**预期**：
- 引擎数：3 个
- 包含引擎：Exa + 百炼/Tavily
- 结果：学术论文相关

---

### 测试 4：抓取场景（应优先 Firecrawl）

```bash
npm run search "抓取网站内容"
```

**预期**：
- 引擎数：2 个
- 包含引擎：Firecrawl + 其他
- 结果：网页内容相关

---

### 测试 5：深度研究（应使用 5 个引擎）

```bash
npm run search "人工智能发展报告" -- --deep
```

**预期**：
- 引擎数：5 个（全部）
- 耗时：~3-4 秒
- 结果数：20-25 条
- 结果质量：最高

---

## 📊 性能预期

| 查询类型 | 引擎数 | 耗时 | 额度消耗 |
|----------|--------|------|----------|
| 简单查询 | 2 个 | ~2 秒 | 2 次 |
| 普通查询 | 3 个 | ~2-3 秒 | 3 次 |
| 学术场景 | 3 个 | ~2-3 秒 | 3 次 |
| 抓取场景 | 2 个 | ~2 秒 | 2 次 |
| 深度研究 | 5 个 | ~3-4 秒 | 5 次 |

**日均消耗**（20 次搜索）：
- 简单查询（60%）：24 次
- 普通查询（30%）：18 次
- 深度研究（10%）：10 次
- **总计**：~52 次/天

**Firecrawl 可用天数**：
- 500 页 ÷ (52 次/天 × 20% 抓取场景) ≈ **48 天**

---

## 🔍 诊断命令

### 查看配置状态

```bash
npm run doctor
```

### 查看 API Key 配置

```bash
npm run key:status
```

### 查看单个引擎配置

```bash
npm run key:get bailian
npm run key:get tavily
```

### 重新配置 API Keys

```bash
npm run setup
```

### 生成新主密钥

```bash
npm run key:generate-master
```

---

## ❓ 常见问题

### Q1: OPENCLAW_MASTER_KEY 未设置

**问题**：
```
❌ OPENCLAW_MASTER_KEY  未设置
```

**解决**：
```bash
export OPENCLAW_MASTER_KEY=$(grep OPENCLAW_MASTER_KEY .env | cut -d'=' -f2)
```

**永久生效**：
```bash
echo 'export OPENCLAW_MASTER_KEY="'$(grep OPENCLAW_MASTER_KEY .env | cut -d'=' -f2)'"' >> ~/.bashrc
source ~/.bashrc
```

---

### Q2: API Key 未配置

**问题**：
```
未配置 API Key。请运行：npm run setup
```

**解决**：
```bash
npm run setup
```

交互式输入至少一个引擎的 API Key。

---

### Q3: 解密失败

**问题**：
```
Salt not found in config file
```

**解决**：
```bash
# 重新生成配置文件
node test-config.js

# 重新配置 API Keys
npm run setup
```

---

### Q4: 引擎调用失败

**问题**：
```
[Bailian] API Error: 401 Unauthorized
```

**解决**：
1. 检查 API Key 是否正确
2. 检查 API Key 是否过期
3. 检查配额是否用完
4. 重新配置：`npm run key:set bailian`

---

## 📞 获取帮助

### 文档

- 技能位置：`~/.agents/skills/openclaw-smart-search/`
- 使用文档：`SKILL.md`
- CHANGELOG: `CHANGELOG.md`

### 链接

- ClawHub: https://clawhub.ai/fdenny11gg/openclaw-smart-search
- GitHub: https://github.com/fdenny11gg/openclaw-smart-search

### API Key 获取

- 百炼 MCP: https://dashscope.console.aliyun.com/apiKey
- Tavily: https://app.tavily.com/home
- Serper: https://serper.dev/dashboard
- Exa: https://dashboard.exa.ai/api-keys
- Firecrawl: https://www.firecrawl.dev/app/api-keys

---

**配置完成后，运行测试用例验证功能！** 🦐🚀
