# ClawRouter 安装与使用指南

**版本**: v1.0.0  
**最后更新**: 2026-03-08  
**作者**: 墨墨 (Mò)  
**官方文档**: https://github.com/blockrunai/ClawRouter

---

## 🚀 快速开始 (3 分钟)

### 方式 1: 一键安装 (推荐)

```bash
# 1. 安装 ClawRouter
curl -fsSL https://blockrun.ai/ClawRouter-update | bash

# 2. 重启 OpenClaw Gateway
openclaw gateway restart

# 3. 验证安装
curl http://localhost:8080/health
# 应返回：{"status": "ok"}
```

### 方式 2: Docker 部署

```bash
# 1. 启动 Docker 容器
docker run -d \
  -p 8080:8080 \
  -v ~/.clawrouter:/app/data \
  --name clawrouter \
  blockrun/clawrouter:latest

# 2. 查看日志
docker logs -f clawrouter

# 3. 验证安装
curl http://localhost:8080/health
```

### 方式 3: 源码安装

```bash
# 1. 克隆仓库
git clone https://github.com/blockrunai/ClawRouter.git
cd ClawRouter

# 2. 安装依赖
npm install

# 3. 启动服务
npm start

# 4. 验证安装
curl http://localhost:8080/health
```

---

## 💰 充值钱包

### 步骤 1: 获取钱包地址

```bash
# 打印钱包地址
clawrouter wallet address

# 输出示例：
# Base: 0x1234...5678
# Solana: ABCD...EFGH
```

### 步骤 2: 充值 USDC

**Base 链**:
1. 打开 Coinbase Wallet / MetaMask
2. 切换到 Base 网络
3. 转账 USDC 到钱包地址
4. 确认交易

**Solana 链**:
1. 打开 Phantom Wallet
2. 切换到 Solana 网络
3. 转账 USDC 到钱包地址
4. 确认交易

### 充值金额建议

| 使用场景 | 建议充值 | 预估请求数 |
|---------|---------|-----------|
| 个人测试 | $5 | 数千次 |
| 日常使用 | $20 | 数万次 |
| 生产环境 | $100+ | 数十万次 |

---

## 🔧 配置 OpenClaw

### 步骤 1: 复制配置模板

```bash
cp ~/.openclaw/skills/config-center/templates/clawrouter.json.example \
   ~/.openclaw/config/clawrouter.json
```

### 步骤 2: 编辑配置

```bash
vim ~/.openclaw/config/clawrouter.json
```

**修改内容**:
```json
{
  "enabled": true,  // 改为 true
  "proxy": {
    "api_key": "你的 API Key"  // 填入实际 API Key
  }
}
```

### 步骤 3: 设置权限

```bash
chmod 600 ~/.openclaw/config/clawrouter.json
```

### 步骤 4: 重启 Gateway

```bash
openclaw gateway restart --force
```

### 步骤 5: 验证配置

```bash
# 查看 ClawRouter 状态
clawrouter status

# 查看路由日志
tail -f ~/.clawrouter/logs/routing.log

# 测试请求
curl http://localhost:8080/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "anthropic/claude-sonnet-4",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

---

## 📊 监控与统计

### 查看成本统计

```bash
# 今日统计
clawrouter stats --today

# 本周统计
clawrouter stats --week

# 本月统计
clawrouter stats --month

# 实时统计
clawrouter stats --live
```

### 查看缓存状态

```bash
# 缓存统计
clawrouter cache stats

# 缓存命中率
clawrouter cache hit-rate

# 清理缓存
clawrouter cache clear
```

### 查看路由决策

```bash
# 查看最近路由决策
tail -n 50 ~/.clawrouter/logs/routing.log

# 查看 Claude 使用率
grep "claude" ~/.clawrouter/logs/routing.log | wc -l

# 查看节省金额
clawrouter savings
```

---

## 📈 成本对比案例

### 案例 1: 个人开发者

**使用前**:
```
月请求数：1,000
平均成本：$0.045/请求
月成本：$45
Claude 使用率：100%
```

**使用后**:
```
月请求数：1,000
平均成本：$0.012/请求
月成本：$12
Claude 使用率：23%
节省：$33/月 (73%)
```

### 案例 2: SaaS 应用

**使用前**:
```
月请求数：10,000
平均成本：$0.045/请求
月成本：$450
Claude 使用率：100%
```

**使用后**:
```
月请求数：10,000
平均成本：$0.0117/请求
月成本：$117
Claude 使用率：23%
节省：$333/月 (74%)
```

### 案例 3: AI 初创公司

**使用前**:
```
月请求数：50,000
平均成本：$0.048/请求
月成本：$2,400
Claude 使用率：100%
```

**使用后**:
```
月请求数：50,000
平均成本：$0.0125/请求
月成本：$624
Claude 使用率：23%
节省：$1,776/月 (74%)
```

---

## 🔍 故障排查

### 问题 1: ClawRouter 无法启动

**症状**:
```bash
curl http://localhost:8080/health
# 返回：curl: (7) Failed to connect to localhost port 8080
```

**解决方案**:
```bash
# 1. 检查端口占用
lsof -i :8080

# 2. 如果有占用，杀掉进程
kill -9 <PID>

# 3. 或者更换端口
vim ~/.openclaw/config/clawrouter.json
# 修改： "endpoint": "http://localhost:8081/v1"

# 4. 重启
openclaw gateway restart
```

### 问题 2: 路由策略不生效

**症状**:
```bash
# 所有请求仍然使用 Claude
clawrouter stats
# Claude 使用率：100%
```

**解决方案**:
```bash
# 1. 检查配置
cat ~/.openclaw/config/clawrouter.json | jq '.enabled'
# 应返回：true

# 2. 检查路由策略
cat ~/.openclaw/config/clawrouter.json | jq '.routing.strategy'
# 应返回："cost_optimized"

# 3. 查看路由日志
tail -f ~/.clawrouter/logs/routing.log

# 4. 重启 Gateway
openclaw gateway restart --force
```

### 问题 3: 缓存未命中

**症状**:
```bash
clawrouter cache stats
# 命中率：0%
```

**解决方案**:
```bash
# 1. 检查缓存是否启用
cat ~/.openclaw/config/clawrouter.json | jq '.cache.enabled'
# 应返回：true

# 2. 检查 TTL 设置
cat ~/.openclaw/config/clawrouter.json | jq '.cache.ttl_minutes'
# 应返回：10

# 3. 清理缓存重试
clawrouter cache clear

# 4. 发送重复请求测试
curl http://localhost:8080/v1/chat/completions ... (相同请求 2 次)
```

### 问题 4: API Key 无效

**症状**:
```bash
# 返回：401 Unauthorized
```

**解决方案**:
```bash
# 1. 检查 API Key 是否正确
cat ~/.openclaw/config/clawrouter.json | jq '.proxy.api_key'

# 2. 重新获取 API Key
clawrouter wallet api-key

# 3. 更新配置
vim ~/.openclaw/config/clawrouter.json

# 4. 重启
openclaw gateway restart
```

---

## 📚 常见问题

### Q1: ClawRouter 安全吗？

**A**: 非常安全！
- ✅ 开源项目 (MIT License)
- ✅ 本地运行，数据不出境
- ✅ 5K+ GitHub Stars
- ✅ 20,000+ 生产请求验证

### Q2: 支持哪些模型？

**A**: 支持 41+ 模型：
- Anthropic: Claude Opus/Sonnet/Haiku
- OpenAI: GPT-4o/GPT-4o-mini/GPT-4
- Zhipu: GLM-4/GLM-3-Turbo
- DeepSeek: DeepSeek-Chat/DeepSeek-Coder
- 更多：见官方文档

### Q3: 缓存会不会导致数据过期？

**A**: 不会！
- 缓存 TTL 默认 10 分钟
- 可自定义 (1-60 分钟)
- 可随时清理缓存
- 重复请求才缓存，新请求正常处理

### Q4: 智能路由会不会选错模型？

**A**: 概率极低！
- 14 维度评分算法
- <1ms 评分速度
- 77% 请求准确路由到便宜模型
- 23% 复杂请求仍用 Claude

### Q5: 充值后能退款吗？

**A**: 
- 支持随时提现
- USDC 稳定币，无汇率损失
- 提现到原充值地址
- 手续费：$0.5 (Base 链) / $0.1 (Solana 链)

---

## 🖤 作者备注

**整合说明**:
- 本指南基于 ClawRouter 官方文档整理
- 结合 OpenClaw 集中配置管理系统设计
- 所有命令已验证可用
- 成本数据来自官方 (2026-03-08)

**参考资料**:
- ClawRouter GitHub: https://github.com/blockrunai/ClawRouter
- BlockRun 官网：https://blockrun.ai/
- X 文章 (108 万观看): https://x.com/bc1beat/status/2030322072329548219

**维护者**: 墨墨 (Mò)  
**许可**: MIT  
**最后更新**: 2026-03-08

---

**⚠️ 使用提示**: 
1. 首次使用建议小额充值 ($5)
2. 监控成本变化，确认节省效果
3. 遇到问题先查看故障排查章节
4. 加入官方 Discord 获取支持
