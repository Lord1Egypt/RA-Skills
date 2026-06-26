# 📋 排除内容与归位对策

**更新时间**: 2026-03-26 23:43

---

## 🎯 排除原则

### ✅ 排除的（敏感/不必要）

| 排除项 | 原因 | 归位对策 |
|--------|------|---------|
| **credentials/** | API Keys（敏感信息） | 归位后重新配置 |
| ***.key** | 证书文件（敏感） | 归位后重新配置 |
| ***.pem** | 证书文件（敏感） | 归位后重新配置 |
| ***.env** | 环境变量（敏感） | 归位后重新配置 |
| **.git/** | Git 仓库（不需要） | 无影响 |
| **completions/** | 缓存（可重新生成） | 无影响 |
| ***.log** | 日志（不需要） | 无影响 |
| **.DS_Store** | 系统文件（不需要） | 无影响 |
| **__pycache__/** | Python 缓存（可重新生成） | 无影响 |

### ❌ 不排除的（必需）

| 文件/目录 | 原因 |
|----------|------|
| **node_modules/** | Skills 的依赖，排除后无法运行 |
| **skills/** | 核心功能 |
| **memory/** | 用户数据 |
| **config/** | 配置信息 |
| **cron/** | 定时任务 |

---

## 🔐 敏感信息处理

### credentials/（API Keys）

**为什么不打包**:
```bash
# 包含敏感信息
~/.openclaw/credentials/
├── openai.key      # OpenAI API Key
├── claude.key      # Claude API Key
├── github.token    # GitHub Token
└── ...
```

**归位对策**:
```bash
# 归位后，手动配置
openclaw config set openai.api_key sk-xxx
openclaw config set claude.api_key sk-xxx

# 或使用配置文件
cat > ~/.openclaw/credentials/openai.key << EOF
sk-xxx
EOF
```

**提示**:
```
✅ 归位完成！

请重新配置:
  - API Keys (openclaw config set)
  - Channel 配置
```

---

## 📦 node_modules/ 处理

### 为什么不排除？

**原因**:
```bash
# Skills 依赖 node_modules
~/.openclaw/skills/just-note/
├── bin/migrate
└── node_modules/    # 必需！
    └── clawhub/     # ClawHub SDK
```

**如果排除**:
```bash
# 归位后
~/.openclaw/skills/just-note/
├── bin/migrate
└── node_modules/    # ❌ 丢失！

# 结果：Skill 无法运行
./bin/migrate
# Error: Cannot find module 'clawhub'
```

**大小估算**:
```
node_modules/: ~10-50MB（取决于 Skills 数量）
可以接受，不排除
```

---

## 📋 完整的打包/归位流程

### 打包时

```bash
openclaw-migrate pack --output ~/openclaw-pack/

# 输出:
📦 打包 Skills...
   ✅ 工作区 Skills: 9 个（包含 node_modules）
   ✅ ClawHub Skills: 50 个（包含 node_modules）

📦 打包 Memory...
   ✅ Memory: 31 个文件

📦 打包配置（排除敏感信息）...
   ✅ 配置：已打包
   ⚠️  已排除：credentials/, *.env, *.key（需要重新配置）
```

---

### 归位时

```bash
openclaw-migrate unpack --input ~/openclaw-pack/

# 输出:
🏠 开始归位 OpenClaw...

📦 恢复 Skills...
   ✅ 工作区 Skills: 9 个（包含 node_modules，可直接运行）
   ✅ ClawHub Skills: 50 个（包含 node_modules，可直接运行）

📦 恢复 Memory...
   ✅ Memory: 31 个文件

📦 恢复配置...
   ✅ 配置：已恢复

✅ 归位完成！

请重新配置:
  - API Keys (openclaw config set)
  - Channel 配置
```

---

## 🔧 归位后配置清单

### 必须配置

| 配置项 | 命令 | 说明 |
|--------|------|------|
| **OpenAI API Key** | `openclaw config set openai.api_key sk-xxx` | 如果使用 OpenAI |
| **Claude API Key** | `openclaw config set claude.api_key sk-xxx` | 如果使用 Claude |
| **Channel 配置** | 参考文档 | 微信/飞书等 |

### 可选配置

| 配置项 | 命令 | 说明 |
|--------|------|------|
| **GitHub Token** | `openclaw config set github.token ghp_xxx` | 如果使用 Git |
| **其他 API Keys** | `openclaw config set` | 根据需要 |

---

## 💡 最佳实践

### 1. 使用环境变量管理 API Keys

**在源机器**:
```bash
# 导出 API Keys（不要打包）
cat > ~/api-keys-backup.txt << EOF
openai.api_key=sk-xxx
claude.api_key=sk-xxx
github.token=ghp_xxx
EOF

# 加密保存
gpg -c ~/api-keys-backup.txt
```

**在目标机器**:
```bash
# 解密并导入
gpg -d ~/api-keys-backup.txt.gpg | while read line; do
  openclaw config set $line
done
```

---

### 2. 使用配置管理工具

**创建配置脚本**:
```bash
#!/bin/bash
# setup-config.sh

echo "配置 API Keys..."
openclaw config set openai.api_key $OPENAI_API_KEY
openclaw config set claude.api_key $CLAUDE_API_KEY
openclaw config set github.token $GITHUB_TOKEN

echo "配置完成！"
```

**使用**:
```bash
# 归位后运行
export OPENAI_API_KEY=sk-xxx
export CLAUDE_API_KEY=sk-xxx
export GITHUB_TOKEN=ghp_xxx
./setup-config.sh
```

---

### 3. 使用密码管理器

**1Password / LastPass / Bitwarden**:
```
1. 在源机器保存 API Keys 到密码管理器
2. 在目标机器从密码管理器获取
3. 配置到 OpenClaw
```

**优点**:
- 安全
- 跨设备同步
- 不需要手动备份

---

## 🎯 总结

### 排除策略

| 类型 | 策略 | 原因 |
|------|------|------|
| **敏感信息** | ✅ 排除 | 安全 |
| **node_modules** | ❌ 不排除 | Skills 运行必需 |
| **缓存/日志** | ✅ 排除 | 可重新生成 |

### 归位对策

| 排除项 | 对策 |
|--------|------|
| **API Keys** | 手动配置 / 密码管理器 |
| **node_modules** | 已打包，无需处理 |
| **缓存** | 自动重新生成 |

### 核心原则

> **排除敏感的，保留必需的**
> 
> - credentials/ → 排除（安全）
> - node_modules/ → 不排除（必需）
> - 其他 → 根据情况

---

**状态**: ✅ **排除策略已优化**  
**下一步**: 测试归位后 Skills 是否正常运行
