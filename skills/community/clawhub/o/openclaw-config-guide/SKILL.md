---
name: openclaw-config-guide
description: "OpenClaw configuration management best practices and common pitfalls. Use when: (1) User needs to modify OpenClaw configuration, (2) User asks about config paths or structure, (3) User encountered config errors, (4) Adding new providers or channels, (5) Before making any config changes - to avoid common mistakes like wrong paths or direct JSON editing."
---

# OpenClaw 配置管理指南

本技能提供 OpenClaw 配置管理的最佳实践，帮助避免常见错误。

## ⚠️ 黄金法则

**永远不要用 `write` 或 `edit` 直接修改配置文件！**

❌ 错误方式：
- 直接编辑 `~/.openclaw/openclaw.json`
- 猜测配置路径（如 `plugins.entries.discord.botToken`）
- 裸写 JSON 没有验证

✅ 正确方式：
- 使用 `gateway config.get` 查看当前配置
- 使用 `gateway config.patch` 做增量修改
- 修改后用 `gateway config.get` 验证

## 📋 配置前检查清单

每次修改配置前，按此顺序执行：

1. **读取现有配置**
   ```
   gateway config.get
   ```
   目的：确认当前结构，避免猜测路径

2. **确认正确路径**
   参考 `references/common-paths.md` 查找正确的配置项路径
   原则：**不确定时，宁可多看一眼，不要盲猜**

3. **使用 patch 修改**
   ```
   gateway config.patch
   {
     "channels": {
       "discord": {
         "enabled": true,
         "token": "YOUR_TOKEN"
       }
     }
   }
   ```

4. **验证修改结果**
   ```
   gateway config.get
   ```
   确认修改生效，无语法错误

## 🔥 常见错误案例

### 错误 1：Discord Token 路径错误
```json
// ❌ 错误路径
{
  "plugins": {
    "entries": {
      "discord": {
        "botToken": "xxx"  // 错误！
      }
    }
  }
}

// ✅ 正确路径
{
  "channels": {
    "discord": {
      "token": "xxx"  // 正确！
    }
  }
}
```

### 错误 2：直接覆盖整个配置
```json
// ❌ 危险！会丢失其他所有配置
gateway config.apply
{ ...新配置... }

// ✅ 安全！只修改指定部分
gateway config.patch
{ ...部分配置... }
```

## 📚 参考资源

- **配置路径速查表**: 见 `references/common-paths.md`
  - 包含常用配置项的正确路径
  - Provider 配置路径
  - Channel 配置路径
  - Agent 默认配置路径

## 🛠️ 配置管理命令

| 命令 | 用途 |
|------|------|
| `gateway config.get` | 查看当前完整配置 |
| `gateway config.patch` | 增量修改配置（推荐）|
| `gateway config.apply` | 完全替换配置（危险）|
| `gateway config.schema` | 查看配置 JSON Schema |

## 💡 最佳实践总结

1. **先读后写** - 永远不要假设配置结构
2. **用 patch 不用 apply** - 避免意外覆盖
3. **验证闭环** - 修改后必须验证
4. **参考速查表** - 不确定路径时查 `common-paths.md`
5. **不要猜测** - 看到实际配置再动手

---

记住：**配置错误会导致 OpenClaw 无法启动，务必谨慎！**
