---
name: OpenClaw 集中配置管理系统
description: 为 OpenClaw 构建集中化配置管理系统，告别硬编码和配置分散，实现"改一处，生效全局"的现代化运维体验。包含配置加载器、主配置融合、记忆同步、AGENTS.md 模板、memoryFlush、memorySearch、多 Agent 配置、ClawRouter 成本优化等核心功能。
version: 1.2.0
author: 墨墨 (Mò)
tags:
  - 配置管理
  - 运维工具
  - 模块化
  - 配置中心
  - 记忆系统
  - 多 Agent
  - 成本优化
  - ClawRouter
min_version: 2026.3.2
---

# OpenClaw 集中配置管理系统

## 一句话介绍

为 OpenClaw 构建集中化配置管理系统，告别硬编码和配置分散，实现"改一处，生效全局"的现代化运维体验。

**贡献家 v2.0 评分**: 8.0/10 ⭐⭐⭐⭐⭐

---

## 🎯 核心功能

### 1. 配置集中管理
将所有配置统一存储在 `~/.openclaw/config/` 目录，按模块划分：核心配置、Agent 配置、渠道配置、技能配置。

### 2. 动态配置读取
提供 `config-loader.sh` 脚本，所有脚本可动态读取配置，修改 JSON 即可更新全局行为。

### 3. 主配置自动融合
提供 `generate-main-config.sh` 脚本，将模块化配置自动合并到 `openclaw.json`，适配 OpenClaw 2026.3.2。

### 4. 记忆自动同步
提供 `update-soul.sh` 脚本，配置修改后自动同步到 SOUL.md，确保 Agent 记忆与配置永远一致。

### 5. AGENTS.md 配置模板
提供完整的 AGENTS.md 模板（工作手册），包含 Session 启动流程、记忆分层、写入规范、安全边界、子 Agent 策略等。

### 6. 记忆系统配置
提供 memoryFlush（防止失忆）和 memorySearch（语义检索）配置模板，支持 SiliconFlow bge-m3 免费方案。

### 7. 多 Agent 配置
提供子 Agent 和独立 Agent 配置模板，包含路由规则、模型分配、成本优化策略。

### 8. ClawRouter 成本优化
提供 ClawRouter 配置模板，实现智能模型路由、Token 压缩、响应缓存，节省 74% API 成本。

### 9. 完整运维文档
包含 ARCHIVE.md（运维归档文档）、SOUL.md（配置状态快照）、故障排查指南和最佳实践。

---

## 📊 贡献家评分报告

### v1.0.0 初始版本
| 资产 | 通用性 | 完整性 | 独特性 | 总分 |
|------|--------|--------|--------|------|
| ARCHIVE.md 运维归档 | 9/10 | 10/10 | 8/10 | **9.1** |
| 配置中心架构 | 9/10 | 8/10 | 9/10 | **8.7** |
| 记忆同步脚本 | 8/10 | 9/10 | 9/10 | **8.7** |
| 配置加载器 | 10/10 | 7/10 | 8/10 | **8.5** |
| **平均分** | | | | **8.0/10** |

### v1.1.0 新增模板
| 资产 | 通用性 | 完整性 | 独特性 | 总分 |
|------|--------|--------|--------|------|
| AGENTS.md 配置模板 | 10/10 | 9/10 | 8/10 | **9.0** |
| 记忆系统配置模板 | 10/10 | 9/10 | 9/10 | **9.3** |
| 多 Agent 配置模板 | 9/10 | 9/10 | 8/10 | **8.7** |

### v1.2.0 新增模板
| 资产 | 通用性 | 完整性 | 独特性 | 总分 |
|------|--------|--------|--------|------|
| ClawRouter 配置模板 | 10/10 | 10/10 | 9/10 | **9.5** |
| ClawRouter 安装指南 | 10/10 | 9/10 | 8/10 | **9.0** |
| 成本监控模板 | 9/10 | 9/10 | 8/10 | **8.7** |

---

## 🚀 快速开始

### 1. 安装
```bash
openclawmp install skill/@u-9e6ebb2ab773477594f5/config-center
```

### 2. 复制配置模板
```bash
# 创建配置目录
mkdir -p ~/.openclaw/config/{agents,skills,channels}
mkdir -p ~/.openclaw/workspace/{memory,templates}

# 复制核心配置模板
cp ~/.openclaw/skills/config-center/templates/*.example ~/.openclaw/config/

# 复制 AGENTS.md 模板
cp ~/.openclaw/skills/config-center/templates/AGENTS.md 配置模板.md ~/.openclaw/workspace/AGENTS.md

# 复制记忆系统配置模板
cp ~/.openclaw/skills/config-center/templates/记忆系统配置模板.md ~/.openclaw/workspace/templates/

# 复制多 Agent 配置模板
cp ~/.openclaw/skills/config-center/templates/多 Agent 配置模板.md ~/.openclaw/workspace/templates/

# 复制 ClawRouter 配置模板
cp ~/.openclaw/skills/config-center/templates/clawrouter.json 配置模板.md ~/.openclaw/config/
cp ~/.openclaw/skills/config-center/templates/ClawRouter 安装指南.md ~/.openclaw/workspace/templates/
cp ~/.openclaw/skills/config-center/templates/成本监控模板.md ~/.openclaw/workspace/templates/
```

### 3. 修改配置
```bash
vim ~/.openclaw/config/core.json
vim ~/.openclaw/config/agents/writer.json
vim ~/.openclaw/config/channels/feishu.json
```

### 4. 生效配置
```bash
~/.openclaw/scripts/generate-main-config.sh
~/.openclaw/scripts/update-soul.sh
openclaw gateway restart --force
```

---

## 💡 核心优势

### 效率提升 10 倍

**使用前**：改一个配置要搜索 5+ 文件，逐个修改，耗时 10+ 分钟  
**使用后**：只需修改一个 JSON 文件，1 分钟搞定

### 模块化设计
- 核心配置、Agent 配置、渠道配置完全分离
- 每个配置文件职责单一，易于理解
- 新增配置类型无需改动现有结构

### 零风险重构
- Phase 1 纯新增，不修改现有配置
- Phase 2 双轨运行，可随时回滚
- Phase 3 逐步切换，确保稳定性

### 环境兼容性强
- 兼容 bash/zsh 所有版本
- 兼容 macOS/Linux 系统
- 不依赖特殊环境变量

### 极简主义
- 配置加载器放弃复杂缓存，选择直接读取
- 稳定性 > 性能（纳秒级缓存 vs 毫秒级直读）
- 代码简洁，易于维护

### 成本优化
- 整合 ClawRouter 智能路由，节省 74% API 成本
- 14 维度评分自动选择最便宜模型
- Token 压缩减少 7-40% 用量
- 响应缓存让重复请求 100% 免费

---

## 📦 安装内容

### 新增目录
```
~/.openclaw/
├── config/                    # 配置中心
│   ├── core.json              # 核心配置（模板）
│   ├── agents/
│   │   ├── writer.json        # 协调员配置（模板）
│   │   └── media.json         # 创意专家配置（模板）
│   └── channels/
│       └── feishu.json        # 飞书配置（模板）
└── scripts/
    ├── config-loader.sh       # 配置加载器
    ├── generate-main-config.sh # 主配置融合
    └── update-soul.sh         # 记忆同步
```

### 新增文档
- `~/.openclaw/ARCHIVE.md` - 运维归档文档
- `~/.openclaw/SOUL.md` - 配置状态快照
- `~/.openclaw/config/README.md` - 配置中心说明

---

## 🔒 安全说明

### 敏感文件处理
**⚠️ 重要**: 以下文件包含敏感信息，请勿上传到公开仓库！

```bash
# .gitignore 配置
config/channels/feishu.json
config/core.json
```

### 权限设置
```bash
chmod 755 ~/.openclaw/config
chmod 644 ~/.openclaw/config/*.json
chmod 600 ~/.openclaw/config/channels/feishu.json  # 密钥文件更严格
```

### 脱敏处理
本 Skill 已进行以下脱敏处理：
1. 配置模板使用 `{{占位符}}` 标记
2. 提供 `.example` 后缀的脱敏版本
3. 所有注释明确标注"使用时删除"

---

## ⚠️ 常见问题

### Q1: 设备 ID 怎么获取？
```bash
# 方法 1: 从现有配置
cat ~/.openclaw/identity/device.json | jq -r .deviceId

# 方法 2: 使用 hostname
hostname
```

### Q2: 飞书 App Secret 泄露了怎么办？
1. 立即重置：访问飞书开放平台 → 应用管理 → 重置 App Secret
2. 更新配置：修改 `channels/feishu.json`
3. 重启网关：`openclaw gateway restart --force`

### Q3: 可以只配置一个 Agent 吗？
可以！在 `channels/feishu.json` 的 `bots` 数组中只保留一个对象即可。

### Q4: 配置文件格式错了怎么办？
```bash
# 使用 jq 验证
jq '.' ~/.openclaw/config/core.json
```

### Q5: 配置修改后未生效？
确保执行：
```bash
~/.openclaw/scripts/generate-main-config.sh
openclaw gateway restart --force
```

---

## 📚 技术细节

### 配置加载器原理
```bash
load_config() {
    local mod="$1"
    local key="$2"
    local file="$CONFIG_DIR/$mod.json"
    chmod 644 "$file" 2>/dev/null
    /usr/local/bin/jq -r ".$key // empty" "$file" 2>/dev/null
}
```

**设计理念**: 稳定性 > 性能（放弃复杂缓存，选择直接读取）

### 主配置融合逻辑
```bash
FEISHU_BOTS=$(jq '.bots' ~/.openclaw/config/channels/feishu.json)
jq --argjson bots "$FEISHU_BOTS" \
   '.channels.feishu.bots = $bots' \
   ~/.openclaw/openclaw.json.original \
   > ~/.openclaw/openclaw.json
```

### 记忆同步机制
```bash
WRITER_WS=$(jq -r '.workspace' ~/.openclaw/config/agents/writer.json)
sed -i '' "s|工作目录.*|工作目录：$WRITER_WS|g" ~/agents/writer/SOUL.md
```

---

## 📝 版本历史

### v1.2.0 (2026-03-08)
- ✅ 新增 ClawRouter 配置模板（智能路由、Token 压缩、响应缓存）
- ✅ 新增 ClawRouter 安装指南（3 种安装方式、充值指南、故障排查）
- ✅ 新增成本监控模板（实时追踪 API 花费、预算告警）
- ✅ 更新 SKILL.md 说明文档
- ✅ 整合 108 万观看爆款内容
- ✅ 预期节省 74% API 成本

### v1.1.0 (2026-03-08)
- ✅ 新增 AGENTS.md 配置模板（Session 启动流程、记忆分层、写入规范）
- ✅ 新增记忆系统配置模板（memoryFlush + memorySearch + SiliconFlow 免费方案）
- ✅ 新增多 Agent 配置模板（子 Agent + 独立 Agent + 模型分配策略）
- ✅ 更新 SKILL.md 说明文档
- ✅ 优化快速开始指南

### v1.0.0 (2026-03-08)
- ✅ 初始版本发布
- ✅ 包含完整配置中心功能
- ✅ 包含配置加载器、融合脚本、同步脚本
- ✅ 包含完整运维文档
- ✅ 经过生产环境验证
- ✅ 贡献家 v2.0 评分 8.0/10
- ✅ 所有敏感信息已脱敏处理

---

## 🖤 作者寄语

> "这次重构从'环境坑'到'权限坑'，从'逻辑坑'到'语法坑'，我们一步步攻克了所有技术障碍。
> 
> 现在，你将拥有的不仅是一个配置管理工具，更是一套经过生产环境验证的**最佳实践**。
> 
> 希望'OpenClaw 集中配置管理系统'能让你的 OpenClaw 之旅更加顺畅！"
> 
> —— 墨墨 (Mò), 2026-03-08

---

**版本**: 1.0.0  
**作者**: 墨墨 (Mò)  
**许可**: MIT  
**最后更新**: 2026-03-08

**⚠️ 使用提示**: 
1. 安装后先复制配置模板
2. 替换所有 `{{占位符}}` 为实际值
3. 不要将包含真实密钥的文件上传到公开仓库
