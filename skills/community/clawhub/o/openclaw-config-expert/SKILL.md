---
name: openclaw-config-expert
description: OpenClaw 配置管理专家。精通所有正确配置、智能修复配置、提供最佳实践、版本感知。使用场景：配置验证与修复、Agent 智能配置、模型路由优化、插件管理、版本迁移助手、紧急恢复。触发词："配置"、"修改 agent"、"调优"、"路由"、"版本升级"、"验证配置"、"优化配置"、"回滚"、"恢复"、"重启 Gateway"。
metadata:
  requires:
    bins: ["python3"]
    npm: []
---

# OpenClaw 配置专家 Skill

**版本**: 2.0.0  
**创建时间**: 2026-04-18  
**更新**: 融合优化版本 - 整合配置专家技能包完整功能  
**参考**: https://docs.openclaw.ai/concepts/architecture

---

## 🎯 核心能力

| 能力 | 说明 | 触发词 | 执行者 |
|------|------|--------|--------|
| **配置验证与修复** | 验证 openclaw.json 正确性，自动修复无效字段 | "验证配置"、"修复配置" | 迪逗/Hermes |
| **Agent 智能配置** | 添加/删除/修改 agent，优化子 agent 权限 | "添加 agent"、"agent 配置" | 迪逗/Hermes |
| **模型路由优化** | 配置智能路由规则，优化任务分发 | "路由"、"任务分发" | 迪逗 |
| **插件管理** | 启用/禁用插件，配置插件参数 | "插件"、"memory-wiki" | 迪逗 |
| **版本迁移助手** | 版本更新时自动迁移配置 | "版本升级"、"迁移" | 迪逗 |
| **紧急恢复** | OpenClaw 崩溃时回滚配置、重启 Gateway | "回滚"、"恢复"、"崩溃" | **Hermes** |

---

## 🚨 Hermes 紧急恢复功能

### 使用场景

当 OpenClaw 出现以下情况时，Hermes 可以执行紧急恢复：

1. **配置错误导致 Gateway 无法启动**
2. **Dashboard 无法访问**
3. **Agent 崩溃无法恢复**
4. **系统更新后配置不兼容**
5. **网络连接问题导致模型全部超时**

### Hermes 调用方式

```python
# 在 Hermes 的 prompt 中调用
emergency_script = "~/.openclaw/skills/openclaw-config-expert/scripts/emergency_recovery.py"

# 完整恢复流程
subprocess.run(["python3", emergency_script, "recover"])

# 回滚到指定备份
subprocess.run(["python3", emergency_script, "rollback", "--backup", "openclaw.json.bak"])

# 重启 Gateway
subprocess.run(["python3", emergency_script, "restart"])

# 检查状态
subprocess.run(["python3", emergency_script, "status"])
```

### 恢复流程

```
OpenClaw 崩溃
    ↓
Hermes 检测 (Gateway 未响应)
    ↓
执行 emergency_recovery.py recover
    ↓
1. 检查 Gateway 状态
2. 查找最新备份
3. 回滚配置
4. 重启 Gateway
5. 验证 Dashboard 可访问
    ↓
恢复成功 → 返回 Dashboard URL
恢复失败 → 返回详细错误日志
```

### 示例对话

```
用户：OpenClaw 崩溃了，Gateway 启动不了

Hermes: 检测到 Gateway 未运行，正在执行紧急恢复...

[紧急恢复流程]
1. ✅ 检查 Gateway 状态 - 未运行
2. ✅ 找到备份 - openclaw.json.bak
3. ✅ 配置已回滚
4. ✅ Gateway 重启成功
5. ✅ Dashboard 可访问

✅ 恢复成功！
Dashboard: http://127.0.0.1:18789
日志：~/.openclaw/logs/emergency-recovery.log
```

---

## 🔧 细粒度配置管理

### 配置修改命令

```bash
# 修改单个配置项
python3 config_validator.py modify \
  --key "agents.defaults.model.primary" \
  --value "qwen/qwen-turbo"

# 修改嵌套配置
python3 config_validator.py modify \
  --key "channels.feishu.groupPolicy" \
  --value "allowlist"

# 修改多个配置项
python3 config_validator.py modify \
  --updates '{
    "session.reset.idleMinutes": 60,
    "tools.fs.workspaceOnly": true
  }'
```

### 配置优化命令

```bash
# 应用省钱配置
python3 agent_optimizer.py optimize --target cost-saving

# 应用性能配置
python3 agent_optimizer.py optimize --target performance

# 应用本地优先配置
python3 agent_optimizer.py optimize --target local-first

# 自定义优化
python3 agent_optimizer.py optimize \
  --model-primary "qwen/qwen-turbo" \
  --max-context 120000 \
  --compaction-threshold 0.6 \
  --idle-minutes 60
```

### 配置验证命令

```bash
# 验证配置
python3 config_validator.py validate

# 验证并修复
python3 config_validator.py validate --fix

# 输出 JSON 报告
python3 config_validator.py validate --json

# 详细验证
python3 config_validator.py validate --verbose
```

### 插件管理命令

```bash
# 列出所有插件
python3 plugin_manager.py --list

# 启用飞书插件
python3 plugin_manager.py --enable feishu

# 禁用插件
python3 plugin_manager.py --disable memory-wiki

# 生成插件报告
python3 plugin_manager.py --report
```

### 版本迁移命令

```bash
# 分析迁移需求
python3 version_migrator.py --analyze

# 执行迁移到最新版本
python3 version_migrator.py --migrate --target 2026.4.15

# 检查版本兼容性
python3 version_migrator.py --check
```

---

## 📁 文件结构

```
~/.openclaw/skills/openclaw-config-expert/
├── SKILL.md                        # 本文件
├── config_validator.py             # 配置验证器 (488 行)
├── agent_optimizer.py              # Agent 优化器 (407 行)
├── model_router.py                 # 模型路由器 (110 行)
├── plugin_manager.py               # 插件管理器 (480 行)
├── version_migrator.py             # 版本迁移器 (562 行)
├── openclaw_config_expert.py       # 统一入口
├── scripts/
│   ├── agents.py                   # Agent 管理
│   ├── emergency_recovery.py       # 紧急恢复 (Hermes 专用)
│   ├── validate.py                 # 快速验证脚本
│   └── model_router.py             # 模型路由脚本
├── config_templates/
│   ├── minimal.json                # 最小有效配置
│   ├── standard.json               # 标准生产配置
│   ├── enterprise.json             # 企业级配置
│   ├── development.json            # 开发环境配置
│   ├── cost-saving.json            # 省钱配置
│   ├── performance.json            # 性能配置
│   └── local-first.json            # 本地优先配置
└── references/
    ├── architecture.md             # 官方架构摘要
    └── changelog.md                # 版本更新日志
```

---

## 🎯 意图识别路由

```python
ROUTING_RULES = {
    # 紧急恢复 → Hermes
    r"崩溃 | 挂掉 | 启动不了 | 无法访问 | 回滚 | 恢复": "hermes",
    
    # 编程任务 → Hermes
    r"编程 | 代码|debug|脚本 | 开发": "hermes",
    
    # Compassion 任务 → Ollama 本地
    r"CRM|客户 | 订单 | 经销商": "crm-analyst",
    r"心理学 | 谈判 | 话术 | 沟通": "psychology-analyst",
    r"工控|PLC|HMI|伺服 | 技术": "industrial-analyst",
    r"标准 | 规范 | 认证 | 国标": "standards-analyst",
    r"商业 | 市场 | 竞争 | 策略": "weikong-business",
    
    # 配置管理 → 本 skill
    r"配置 | 设置 | 优化 | 调优 | 验证 | 修改": "openclaw-config-expert",
    
    # 版本相关 → 本 skill
    r"版本 | 升级 | 迁移 | 更新": "openclaw-config-expert",
    
    # 插件管理 → 本 skill
    r"插件 | plugin | 启用 | 禁用": "openclaw-config-expert",
    
    # 模型路由 → 本 skill
    r"模型 | model | 路由 | routing": "openclaw-config-expert",
}
```

---

## 📊 配置 Schema 核心字段

### agents.defaults

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `model.primary` | string | qwen/qwen3.5-plus | 主模型 |
| `model.fallback` | string | deepseek/deepseek-chat | 备用模型 |
| `workspace` | string | ~/OpenClaw 输出 | 工作目录 |
| `subagents.allowAgents` | array | ["hermes"] | 允许的子 agent |
| `timeoutSeconds` | number | 172800 | 超时时间 (48h) |

### session

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `store` | string | .openclaw-memory | 会话存储目录 |
| `dmScope` | string | per-channel-peer | DM 作用域 |
| `reset.mode` | string | idle | 重置模式 |
| `reset.idleMinutes` | number | 60 | 空闲超时 |
| `scope` | string | per-sender | 会话作用域 |

### models.providers.qwen

| 字段 | 类型 | 说明 |
|------|------|------|
| `baseUrl` | string | https://dashscope.aliyuncs.com/compatible-mode/v1 |
| `apiKey` | string | sk-xxx (阿里 API Key) |
| `api` | string | openai-completions |
| `models[]` | array | 模型列表 |

### tools

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `profile` | string | coding | 工具配置集 |
| `elevated` | object | {} | 提权工具配置 |
| `fs.workspaceOnly` | boolean | true | 文件系统限制 |
| `agentToAgent.enabled` | boolean | true | Agent 间通信 |

### channels.feishu

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `enabled` | boolean | true | 启用飞书 |
| `appId` | string | cli_xxx | 飞书应用 ID |
| `appSecret` | string | xxx | 飞书应用密钥 |
| `dmPolicy` | string | allowlist | DM 策略 |
| `groupPolicy` | string | allowlist | 群聊策略 |

### plugins.entries.memory-wiki

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `enabled` | boolean | true | 启用插件 |
| `config.vaultPath` | string | ~/.openclaw-memory/wiki | Wiki 存储路径 |
| `config.autoCreate` | boolean | true | 自动创建页面 |

---

## 📝 使用示例

### 示例 1：Hermes 紧急恢复

```
用户：OpenClaw 崩溃了，Dashboard 打不开

Hermes: 检测到 Gateway 未运行，执行紧急恢复...

[执行 emergency_recovery.py recover]

✅ 恢复成功！
- 配置已回滚到：openclaw.json.bak
- Gateway 已重启
- Dashboard: http://127.0.0.1:18789

日志：~/.openclaw/logs/emergency-recovery.log
```

### 示例 2：细粒度修改配置

```
用户：把主模型改成 qwen-turbo，空闲超时改成 30 分钟

openclaw-config-expert:
正在修改配置...

✅ 配置已更新:
- agents.defaults.model.primary: qwen/qwen-turbo
- session.reset.idleMinutes: 30

正在重启 Gateway...
✅ Gateway 已重启

新配置已生效！
```

### 示例 3：优化配置

```
用户：帮我优化配置，节约成本

openclaw-config-expert:
正在应用省钱配置模板...

✅ 优化完成:
- 主模型：qwen3.5-plus → qwen-turbo (节约 90%)
- 自动压缩：启用 (threshold=0.6)
- 空闲超时：60 分钟
- Compassion 任务：全部 Ollama 本地

预计月度成本：¥500 → ¥50 (节约 90%)
```

### 示例 4：版本迁移

```
用户：升级到最新版本，配置需要迁移吗？

openclaw-config-expert:
正在分析版本差异...

📊 版本分析报告:
- 当前版本：2026.2.28
- 目标版本：2026.4.15
- 废弃字段：3 个
- 新增功能：5 个

正在执行迁移...
✅ 迁移完成！
- 已删除废弃的 memory 配置
- 已启用新的 session.store 格式
- 已更新插件配置结构

备份：openclaw.json.bak
```

### 示例 5：插件管理

```
用户：启用飞书插件，禁用 memory-wiki

openclaw-config-expert:
正在管理插件...

✅ 插件状态已更新:
- feishu: enabled → enabled ✅
- memory-wiki: enabled → disabled ⏸️

正在重启 Gateway...
✅ Gateway 已重启
```

---

## 🔗 相关技能

- **skill-creator**: 创建和编辑技能
- **ontology**: 存储配置实体和关系
- **self-improving-agent**: 从配置错误中学习
- **wiki-maintainer**: 维护记忆 Wiki

---

## 📞 故障排查

### Gateway 无法启动

```bash
# Hermes 执行紧急恢复
python3 ~/.openclaw/skills/openclaw-config-expert/scripts/emergency_recovery.py recover

# 查看日志
cat ~/.openclaw/logs/gateway.log

# 检查网络连通性
ping open.feishu.cn
curl -I https://api.deepseek.com

# 手动启动
openclaw gateway start
```

### 配置验证失败

```bash
# 查看详细错误
python3 config_validator.py validate --verbose

# 自动修复
python3 config_validator.py validate --fix

# 回滚到上一个可用版本
python3 emergency_recovery.py rollback
```

### Dashboard 无法访问

```bash
# 检查 Gateway 状态
python3 emergency_recovery.py status

# 重启 Gateway
python3 emergency_recovery.py restart

# 检查端口
lsof -i :18789
```

### 模型全部超时（网络问题）

```bash
# 检查 DNS 解析
nslookup open.feishu.cn
nslookup api.deepseek.com

# 检查代理设置
echo $HTTP_PROXY
echo $HTTPS_PROXY

# 测试网络连通性
curl -v https://api.deepseek.com/v1/models

# 查看错误日志
tail -100 ~/.openclaw/logs/gateway.log
```

---

## 🎯 最佳实践

### 配置修改流程

1. **验证当前配置** - `validate`
2. **备份配置** - 自动备份到 .bak
3. **修改配置** - `modify` 或 `optimize`
4. **再次验证** - `validate`
5. **重启 Gateway** - `gateway restart`
6. **验证功能** - 访问 Dashboard 测试

### 紧急恢复流程

1. **检测故障** - Hermes 自动检测或用户报告
2. **执行恢复** - `emergency_recovery.py recover`
3. **验证结果** - 检查 Dashboard 可访问性
4. **记录日志** - 保存到 emergency-recovery.log
5. **通知用户** - 返回恢复结果和 Dashboard URL

### 定期维护

```bash
# 每周检查配置健康
python3 config_validator.py validate --report

# 每月检查版本更新
python3 version_migrator.py --check-updates

# 每季度优化 Agent 配置
python3 agent_optimizer.py --optimize

# 清理旧日志
find ~/.openclaw/logs -name "*.log" -mtime +30 -delete
```

---

## 📦 配置模板库

### minimal.json - 最小有效配置
```json
{
  "gateway": {"mode": "local", "bind": "loopback", "port": 18789},
  "agents": {
    "defaults": {"model": {"primary": "deepseek/deepseek-chat"}},
    "list": [{"id": "main", "default": true, "name": "Main Agent"}]
  }
}
```

### standard.json - 标准生产配置
- 多模型 Provider 支持
- 飞书集成配置
- 多 Agent 专业配置
- 完整的工作空间设置

### enterprise.json - 企业级配置
- 高级安全设置
- 多环境支持
- 监控和日志配置
- 高可用性设置

### development.json - 开发环境配置
- 调试模式启用
- 详细日志输出
- 本地模型支持
- 快速迭代配置

### cost-saving.json - 省钱配置
- 使用低成本模型
- 启用自动压缩
- 优化缓存策略
- 本地优先处理

---

## 🔄 维护与更新

### 更新配置知识库
```bash
# 更新配置模板
python3 config_validator.py --update-templates

# 同步版本信息
python3 version_migrator.py --sync-versions

# 检查技能更新
python3 version_migrator.py --check-updates
```

### 贡献
欢迎提交：
- 新的配置模板
- 验证规则改进
- 优化算法
- 故障排除案例

---

**维护者**: 迪逗 🫘  
**最后更新**: 2026-04-18  
**版本**: 2.0.0 (融合优化版 - 整合配置专家技能包)
