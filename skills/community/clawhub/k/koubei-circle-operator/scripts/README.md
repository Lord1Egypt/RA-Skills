## 快速开始

---

### 2. 配置 OpenClaw API

如果需要使用 OpenClaw API 查询数据：

```bash
# 初始化配置（只需一次）
node scripts/openclaw.js init --key <your_key>

```

配置会保存在 `scripts/config.json`（已加入 .gitignore）。

---

### 3. 使用 OpenClaw CLI

```bash
# 获取开放表列表
node scripts/openclaw.js tables

# 或
npm run oc:tables

# 执行 SQL 查询
node scripts/openclaw.js query "SELECT user_id, nickname FROM wb_users_attribute LIMIT 10"

# 或
npm run oc:query "SELECT user_id, nickname FROM wb_users_attribute LIMIT 10"

# 查看帮助
node scripts/openclaw.js help
```

**优势**：
- ✅ API Key 加密存储，不暴露在命令中
- ✅ 无需记忆接口地址
- ✅ 命令行友好，支持管道和脚本

---

## 版本格式

版本号格式：`v{主版本}.{次版本}.{修订版本}`

示例：
- v1.0.0
- v1.0.1
- v1.1.0
- v2.0.0

## 更新提醒

当检测到新版本时，会输出：

```
🔔 技能版本更新提醒

当前版本：v1.0.0
最新版本：v1.0.1

检测到新版本可用，请更新技能以获取最新功能。
```

## 注意事项

1. 首次使用需运行 `node scripts/openclaw.js init --key <your_key>` 完成配置
2. API 地址可在 `config.json` 中修改
3. 检查失败不会影响技能正常使用
