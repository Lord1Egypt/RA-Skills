# OpenClaw 配置专家 Skill - 自动路由设置

**版本**: 1.2.0  
**功能**: 自动识别配置相关自然语言，路由到配置专家 skill 执行

---

## 🎯 功能说明

当用户发送配置相关的自然语言消息时，**自动路由到 openclaw-config-expert skill 执行**，而不是由默认 agent 处理。

---

## 📋 支持的自然语言模式

| 场景 | 自然语言示例 | 自动执行命令 |
|------|-------------|--------------|
| **配置验证** | "验证配置"、"检查配置"、"配置有问题吗" | `config.py validate` |
| **配置修复** | "修复配置"、"自动修复"、"配置错了" | `config.py fix` |
| **配置修改** | "把主模型改成 qwen-turbo"、"设置空闲超时为 60" | `config.py modify --key X --value Y` |
| **配置优化** | "优化配置"、"调优"、"节约成本" | `config.py optimize` |
| **紧急恢复** | "崩溃了"、"启动不了"、"Gateway 挂了" | `config.py recover` |
| **Agent 管理** | "添加 agent"、"删除 agent" | `config.py agents` |
| **版本升级** | "版本更新"、"升级版本" | `config.py migrate` |

---

## 🔧 工作原理

```
用户消息
    ↓
路由拦截器 (router.py)
    ↓
匹配关键词/正则表达式
    ↓
匹配成功 → 执行 config.py 对应命令 → 返回结果
    ↓
匹配失败 → 交给默认 agent 处理
```

---

## 📁 文件位置

```
~/.openclaw/skills/openclaw-config-expert/
├── config.py                   # 统一入口
├── router.py                   # 路由拦截器 ⭐
├── routing_rules.json          # 路由规则 ⭐
├── config_validator.py         # 配置验证器
└── scripts/
    ├── emergency_recovery.py   # 紧急恢复
    └── ...
```

---

## 🚀 使用方式

### 方式 1：直接调用 (推荐)

```bash
# 验证配置
python3 config.py validate

# 修改配置
python3 config.py modify --key "session.reset.idleMinutes" --value "30"

# 优化配置
python3 config.py optimize --target cost-saving

# 紧急恢复
python3 config.py recover
```

### 方式 2：自然语言 (自动路由)

```
用户：帮我验证一下配置
→ 自动路由 → python3 config.py validate

用户：把主模型改成 qwen-turbo
→ 自动路由 → python3 config.py modify --key "agents.defaults.model.primary" --value "qwen/qwen-turbo"

用户：Gateway 崩溃了，启动不了
→ 自动路由 → python3 config.py recover
```

---

## 🧪 测试路由

```bash
# 测试路由拦截器
python3 router.py --test

# 测试单条消息
python3 router.py "把主模型改成 qwen-turbo"
```

---

## ⚙️ 路由规则配置

编辑 `routing_rules.json` 添加/修改路由规则：

```json
{
  "routing_rules": [
    {
      "name": "配置修改",
      "patterns": ["修改配置", "把.*改成", "设置.*为"],
      "action": "skill",
      "skill": "openclaw-config-expert",
      "command": "python3 config.py modify",
      "priority": 1
    }
  ]
}
```

---

## 📊 Token 消耗

| 操作 | 路由前 (qwen3.5-plus) | 路由后 (qwen-turbo) | 节约 |
|------|----------------------|---------------------|------|
| 配置验证 | ¥0.002 | ¥0.0003 | 85% |
| 配置修改 | ¥0.003 | ¥0.0004 | 87% |
| 配置优化 | ¥0.005 | ¥0.0007 | 86% |
| 紧急恢复 | ¥0.008 | ¥0.0010 | 88% |

**平均节约 85-90% Token 成本！**

---

## ✅ 最佳实践

1. **优先使用自然语言** - 系统会自动路由
2. **复杂配置用命令** - 直接调用 `config.py modify --updates '{}'`
3. **紧急情况用 recover** - Hermes 可调用 `config.py recover`
4. **定期验证配置** - `config.py validate`

---

## 🎯 示例对话

### 示例 1：配置验证

```
用户：帮我检查一下配置有没有问题

[自动路由到 config.py validate]

✅ 配置验证报告
状态：✅ 通过
警告：0
建议：0
```

### 示例 2：配置修改

```
用户：把空闲超时改成 30 分钟

[自动路由到 config.py modify]

✅ 配置已更新:
   session.reset.idleMinutes: 60 → 30
```

### 示例 3：紧急恢复

```
用户：Gateway 崩溃了，Dashboard 打不开

[自动路由到 config.py recover]

✅ 恢复成功！
Dashboard: http://127.0.0.1:18789
```

---

## 🔗 相关文件

- `config.py` - 统一入口脚本
- `router.py` - 路由拦截器
- `routing_rules.json` - 路由规则
- `SKILL.md` - Skill 完整文档

---

**维护者**: 迪逗 🫘  
**最后更新**: 2026-04-18  
**版本**: 1.2.0 (自动路由)
