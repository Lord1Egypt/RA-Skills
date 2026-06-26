# huo15-agent-extension

**别名：火一五智能体扩展技能**

## 简介

**动态Agent配置同步技能** - 将主Agent的工作区配置同步到动态创建的Agent工作区。

适用于企微、WhatsApp等支持动态Agent的通道插件。

## 功能

### 1. 配置文件同步

将主Agent工作区的配置文件同步到动态Agent工作区：

| 文件 | 说明 |
|------|------|
| AGENTS.md | Agent配置文件 |
| SOUL.md | 角色定义 |
| TOOLS.md | 工具配置 |
| IDENTITY.md | 身份定义 |
| USER.md | 用户配置 |
| HEARTBEAT.md | 心跳配置 |
| MEMORY.md | 记忆文件 |

**同步规则**：始终以主Agent内容为准，每次同步都会覆盖动态Agent的配置文件。

### 2. 目录同步

将主Agent工作区的目录同步到动态Agent工作区：

| 目录 | 说明 |
|------|------|
| skills/ | 技能目录 |
| memory/ | 记忆目录 |

**同步规则**：始终以主Agent内容为准，有冲突就覆盖。

### 3. 工作区路径规则

- **主Agent工作区**：`~/.openclaw/workspace`
- **动态Agent工作区**：`~/.openclaw/workspace-{agentId}`

## 使用方式

### 作为独立工具调用

```
同步主Agent配置到动态Agent
```

参数：
- `agentId`: 动态Agent的ID（如 `wecom-default-dm-xun`）
- `forceOverwrite`: 是否强制覆盖配置文件（默认true）

### 在代码中调用

```javascript
import { ensureDynamicAgentSynced } from './src/dynamic-agent.js';

// 同步配置
ensureDynamicAgentSynced('wecom-default-dm-xun');
```

## 实现位置

- **源码**：`~/.openclaw/extensions/wecom/src/dynamic-agent.ts`
- **编译后**：`~/.openclaw/extensions/wecom/dist/src/dynamic-agent.js`

## 依赖

- Node.js fs, path, os 模块
- 主Agent工作区必须存在于 `~/.openclaw/workspace`

## 注意事项

1. 此技能是企微插件的内置功能，不需要单独安装
2. 同步是自动触发的，当动态Agent首次创建时自动同步
3. 配置文件始终以主Agent为准，目录只复制新文件
