# TencentDB-Agent-Memory 本地部署指南

> **设计原则**：检测先行，避免重复安装。已安装则跳过安装步骤，直接进入配置阶段。

---

## 一、插件概述

`tencentdb-agent-memory` 是腾讯云数据库团队开源的记忆插件，为 OpenClaw 提供对话记忆能力。采用本地 SQLite + sqlite-vec 后端，**零外部依赖、零配置**即可运行。

---

## 二、安装检测（必做）

在执行任何安装操作之前，先检测插件是否已安装：

```bash
npm list -g tencentdb-agent-memory 2>&1
```

**或者更快速地检查扩展目录：**
```bash
openclaw plugins list 2>&1 | findstr memory-tencentdb
```

### 判断结果

| 检测结果 | 含义 | 下一步 |
|----------|------|--------|
| `tencentdb-agent-memory@x.x.x` 有版本号 | ✅ 已安装 | → 直接进入 **第四节：配置阶段** |
| `not found` 或空 | ❌ 未安装 | → 进入 **第三节：安装步骤** |

---

## 三、安装步骤（未安装时执行）

### Step 1：安装插件

```bash
openclaw plugins install @tencentdb-agent-memory/memory-tencentdb
```

预期输出：
```
下载并提取完成
安装到 ~/.openclaw/extensions/memory-tencentdb
依赖包已安装
插件已注册 (memory-tdai)
配置文件已更新（备份到 openclaw.json.bak）
```

### Step 2：重启 Gateway 生效

```bash
openclaw gateway restart
```

等待 10~30 秒，确认 Gateway 状态恢复「运行中/健康」。

> ⚠️ **已安装用户跳过以上两步，直接进入配置阶段。**

---

## 四、本地配置（零依赖模式）

安装完成后，配置文件 `~/.openclaw/openclaw.json` 会自动生成基础配置：

```json5
{
  "memory-tencentdb": {
    "enabled": true
  }
}
```

### 推荐完整配置（优化召回质量）

```json5
{
  "memory-tencentdb": {
    "enabled": true,
    
    // 记忆提取配置
    "extraction": {
      "enabled": true,
      "enableDedup": true,              // 防重复记忆
      "maxMemoriesPerSession": 30,      // 单次对话最多存 30 条
      "model": ""                        // 留空复用 OpenClaw 默认模型
    },
    
    // 管线节奏
    "pipeline": {
      "everyNConversations": 3,         // 每 3 轮对话触发提炼
      "enableWarmup": true,             // 新对话从第 1 轮开始
      "l1IdleTimeoutSeconds": 60,       // 停嘴 60 秒后触发提炼
      "l2DelayAfterL1Seconds": 120      // L1 完后 2 分钟归纳场景块
    },
    
    // 召回配置（影响"能不能想起"）
    "recall": {
      "enabled": true,
      "strategy": "hybrid",             // keyword + embedding 融合
      "maxResults": 8,                  // 每次注入最多 8 条记忆
      "scoreThreshold": 0.25,           // 阈值略调低，避免"啥都想不起来"
      "timeoutMs": 5000
    },
    
    // Embedding：本地用 BM25，资源充裕可配远端
    "embedding": {
      "enabled": true,
      "provider": "none"                // 默认用 SQLite 内置 BM25
      // 如需远端 Embedding，替换为：
      // "provider": "openai",
      // "baseUrl": "https://your-embedding-endpoint/v1",
      // "apiKey": "sk-xxx",
      // "model": "text-embedding-3-small",
      // "dimensions": 1536
    },
    
    // 自动清理旧日志
    "clean": {
      "enabled": true,
      "keepDays": 30,                   // L0 原始日志保留 30 天
      "cleanTime": "03:00"
    }
  }
}
```

修改后重启生效：
```bash
openclaw gateway restart
```

---

## 五、关键补丁（工具调用支持）

执行 patch 脚本确保工具调用结果能被正确记录：

```bash
cd ~/.openclaw/extensions/memory-tencentdb
bash scripts/openclaw-after-tool-call-messages.patch.sh
openclaw gateway restart
```

> 如果脚本不存在（版本差异）可跳过，基础对话内容仍会正常记录。

---

## 六、上下文保护配置

在 `openclaw.json` 中添加以下配置，防止长对话中近期决策被压缩覆盖：

```json5
{
  "agents": {
    "defaults": {
      "memoryFlush": {
        "enabled": true,
        "reserveTokensFloor": 40000,
        "softThresholdTokens": 4000
      },
      "contextPruning": {
        "mode": "cache-ttl"
      }
    }
  }
}
```

---

## 七、验证安装

### 检查插件状态

```bash
# 查看插件列表
openclaw plugins list
# 应显示 memory-tencentdb ✓ enabled

# 查看 Gateway 状态
openclaw gateway status
# 应显示 Gateway 健康
```

### 功能验证

1. **训练阶段**：
   ```
   你：我叫阿杰，最讨厌回复里带emoji，我写代码只用FastAPI
   （等待确认"已记下"）
   ```

2. **测试阶段**（新对话或重启后）：
   ```
   你：我叫什么？我用啥框架？我讨厌什么？
   ```
   
   若能准确回答 → 记忆管线正常工作。

---

## 八、问题排查

| 症状 | 解法 |
|------|------|
| npm 安装超时 | `npm config set registry https://registry.npmmirror.com` |
| 权限报错 EACCES | 加 sudo 或使用 nvm 管理的 Node |
| Gateway 重启后起不来 | `openclaw logs gateway` 或查看 `~/.openclaw/logs/` |
| 记忆召回失败 | 检查配置中 `recall.enabled` 是否为 true |

---

## 九、进阶优化（可选）

### Soul File 配置（让 Agent 更懂你）

在 `~/.openclaw/workspace/` 下创建以下文件：

**SOUL.md**（身份和原则）：
```markdown
## 身份
你叫小龙虾，是我的个人 AI 助手。
气质：干脆利落、不废话、有执行力。

## 原则
1. 不知道就说不知道，不编造
2. 删除/发送/花钱类操作必须先确认
3. 先给结果，再给过程
4. 用户告知偏好时，回复确认"已记下"
5. 用中文思考，回复口语化
```

**USER.md**（用户偏好）：
```markdown
## 基本信息
- 名字：[你的名字]
- 职业：[你的职业]
- 常用技术栈：[技术栈]

## 偏好
- 回复风格：分点 > 段落，要可执行
- 代码风格：[偏好的风格]
```

---

**总结**：
1. **先执行检测命令**判断是否已安装；
2. **未安装**才执行 `openclaw plugins install`；
3. 之后统一进入配置阶段。插件默认使用 SQLite 后端即可工作，通过调整 `recall` 和 `pipeline` 配置可优化记忆召回质量。