# Claude 平台适配

MyKnowledge 支持 Claude 平台，提供与 CodeBuddy、WorkBuddy、OpenClaw 类似的功能。

---

## 安装方式

### 方式一：Claude 插件目录（推荐）

```bash
# 1. 创建插件目录
mkdir -p ~/.claude/plugins/myknowledge

# 2. 复制 Skill 文件
cp -r /path/to/MyKnowledge/* ~/.claude/plugins/myknowledge/

# 3. 在 Claude 设置中启用插件
```

### 方式二：Claude 项目级配置

```bash
# 在项目根目录创建
mkdir -p .claude

# 创建 settings.json
touch .claude/settings.json
```

**settings.json 示例：**

```json
{
  "plugins": [
    {
      "name": "myknowledge",
      "path": "~/.claude/plugins/myknowledge",
      "enabled": true
    }
  ],
  "hooks": {
    "myknowledge": {
      "enabled": true,
      "config": {
        "keywords": ["分析", "统计", "挖掘", "开发", "设计", "调研"],
        "minKeywordCount": 3
      }
    }
  }
}
```

---

## 功能支持

| 功能 | Claude 支持情况 |
|------|----------------|
| 知识库创建 | ✅ 完整支持 |
| 需求管理 | ✅ 完整支持 |
| 自动检测（操作后告知） | ✅ 依赖意图识别（操作前提示用户） |
| Hook 自动触发 | ⚠️ 需 Claude 支持 Hooks API |
| 会话恢复 | ✅ 完整支持 |

---

## 配置说明

### hooks.json 配置

```json
{
  "name": "myknowledge",
  "version": "1.4.89",
  "events": ["message:received"],
  "enabled": false,
  "config": {
    "keywords": ["分析", "统计", "挖掘", "开发", "设计", "调研"],
    "minKeywordCount": 2,
    "excludePatterns": ["简单", "粗略", "快速"]
  }
}
```

### 配置项说明

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `enabled` | boolean | false | 是否启用 Hook |
| `keywords` | string[] | [...] | 复杂任务关键词列表 |
| `minKeywordCount` | number | 3 | 触发所需最小关键词数（避免误触发） |
| `excludePatterns` | string[] | [...] | 排除模式（降低触发概率） |

---

## 使用示例

### 主动使用

```
用户：创建知识库
Claude：我将为您创建知识库。请选择类型：
       [全局知识库] - 位于 ~/.myknowledge/global/
       [项目知识库] - 位于当前项目目录
```

### 自动检测使用（后台运行，操作后告知）

```
用户：帮我分析这个销售数据
Claude：（自动检测到复杂任务）
       已自动创建知识库并记录需求 REQ-20260609-001
       （首次会自动询问是否开启自动记录）
```

---

## 与其他平台对比

| 平台 | 检测方式 | 用户告知 |
|------|----------|----------|
| CodeBuddy | 意图识别 | 操作前提示用户 |
| WorkBuddy | 意图识别 | 操作前提示用户 |
| OpenClaw | Hook 驱动 | 事件触发，操作后告知 |
| **Claude** | **意图识别 / Hooks** | **操作前提示用户** |

> **注意**：Claude 的 Hook 支持取决于具体实现和环境，目前主要通过意图识别实现自动检测（操作前提示用户）。

---

## 故障排除

### 问题：插件未生效

**解决方案：**
1. 检查插件路径是否正确
2. 确认 settings.json 格式正确
3. 重启 Claude 应用

### 问题：自动检测过于敏感

**解决方案：**
1. 调整 `minKeywordCount` 为更高的值（如 3）
2. 添加更多 `excludePatterns`
3. 完全禁用自动检测

### 问题：知识库创建失败

**解决方案：**
1. 检查目录权限
2. 确认磁盘空间充足
3. 查看 Claude 控制台日志

---

## 相关文件

- `hooks.json` - Hook 配置文件
- `hooks/claude/handler.js` - Hook 处理函数
- `../SKILL.md` - Skill 主入口
- `../settings.yaml` - 全局配置
