# openclaw-rescue-instances

OpenClaw 多实例救援 Gateway 快速创建技能。按照官方文档规范，一键创建隔离的救援实例。

---

## 📖 描述

基于 OpenClaw 官方多实例指南 (`docs/gateway/multiple-gateways.md`)，自动化创建隔离的救援 Gateway 实例。

**适用场景：**
- 创建救援 Bot（主实例故障时备用）
- 隔离不同环境（开发/生产）
- 多配置测试
- 端口隔离需求

---

## 🎯 能力

| 能力 | 说明 |
|------|------|
| 创建救援实例 | 一键创建隔离的 Gateway 实例 |
| 端口自动分配 | 自动计算不冲突的端口 |
| 配置隔离 | 独立的配置文件、状态目录、工作目录 |
| LaunchAgent 集成 | 自动注册 macOS 开机自启服务 |
| 批量创建 | 支持一次性创建多个实例 |

---

## 🚀 使用方法

### 创建单个救援实例

```bash
# 默认创建（端口自动分配）
openclaw agent --message "创建一个救援实例，端口 19001"

# 指定端口
openclaw agent --message "创建救援实例，端口 20000"
```

### 创建多个救援实例

```bash
# 批量创建
openclaw agent --message "创建 3 个救援实例，端口从 19001 开始"
```

### 删除救援实例

```bash
openclaw agent --message "删除救援实例 rescue2"
```

---

## 📋 配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `base_port` | 19001 | 起始端口 |
| `instance_count` | 1 | 创建实例数量 |
| `port_spacing` | 1000 | 端口间隔（避免派生端口冲突） |
| `disable_wecom` | true | 是否禁用企业微信（避免冲突） |
| `copy_plugins` | false | 是否复制插件配置 |

---

## 📁 创建的文件

每个救援实例会创建以下内容：

```
~/.openclaw-rescueN/
├── openclaw.json          # 独立配置文件
├── workspace/             # 独立工作目录
├── sessions/              # 独立会话数据
├── credentials/           # 独立凭证
├── logs/
│   ├── gateway.log
│   └── gateway.err.log
└── agents/                # 独立 Agent 数据

~/Library/LaunchAgents/
└── ai.openclaw.gateway-rescueN.plist  # LaunchAgent 服务
```

---

## ⚙️ 隔离配置

每个实例完全隔离以下内容：

| 配置项 | 主实例 | 救援实例 |
|--------|--------|----------|
| 配置文件 | `~/.openclaw/openclaw.json` | `~/.openclaw-rescueN/openclaw.json` |
| 状态目录 | `~/.openclaw/` | `~/.openclaw-rescueN/` |
| 工作目录 | `~/.openclaw/workspace` | `~/.openclaw-rescueN/workspace` |
| 端口 | 8080 | 19001, 20000, ... |
| Service | `ai.openclaw.gateway` | `ai.openclaw.gateway-rescueN` |

---

## 🔧 维护命令

### 查看状态

```bash
# 查看所有实例
launchctl list | grep openclaw.gateway

# 健康检查
for port in 8080 19001 20000 30000 40000; do
  curl -sk https://localhost:$port/health && echo " ($port)"
done
```

### 重启实例

```bash
# 重启单个
launchctl kickstart -k gui/$UID/ai.openclaw.gateway-rescue1

# 重启所有
for name in gateway gateway-rescue1 gateway-rescue2; do
  launchctl kickstart -k gui/$UID/ai.openclaw.$name
done
```

### 查看日志

```bash
tail -f ~/.openclaw-rescue1/logs/gateway.log
```

---

## ⚠️ 注意事项

1. **端口间隔**：基础端口之间至少留 20 个端口，推荐 1000+（避免 browser/canvas/CDP 派生端口冲突）

2. **企业微信冲突**：多个实例不能用同一个 Bot ID 同时连接企业微信，会互相踢。建议：
   - 只在主实例启用企业微信
   - 或为每个实例配置不同的企业微信应用

3. **API 配额**：共享 API Key 时，配额是所有实例共用的

4. **磁盘空间**：每个实例约占用 100-500MB（取决于会话和缓存）

---

## 📖 官方文档参考

- [Multiple Gateways](/gateway/multiple-gateways)
- [Gateway Configuration](/gateway/configuration)
- [CLI Gateway](/cli/gateway)

---

## 📝 变更记录

| 日期 | 版本 | 说明 |
|------|------|------|
| 2026-03-27 | 1.0.0 | 初始版本，支持单实例和批量创建 |

---

## 💡 示例对话

```
用户：创建一个救援实例
助手：好的，正在创建救援实例 rescue1...
      - 配置文件：~/.openclaw-rescue/openclaw.json
      - 端口：19001
      - 服务：ai.openclaw.gateway-rescue
      创建完成！实例已启动。

用户：再创建两个，端口从 20000 开始
助手：正在创建 rescue2 (20000) 和 rescue3 (30000)...
      完成！两个实例都已启动。

用户：删除 rescue2
助手：正在删除救援实例 rescue2...
      - 卸载服务：ai.openclaw.gateway-rescue2
      - 删除配置：~/.openclaw-rescue2/
      完成！
```
