# 龙虾安全卫士 (openclaw-safe-guard) v1.2.3

## 📦 来源信息
- **作者**: ansengu11
- **仓库**: https://github.com/ansengu11/openclaw-safe-guard
- **主页**: https://clawhub.ai/ansengu11/openclaw-safe-guard
- **许可证**: MIT-0

## ✅ 可信验证
您可以通过以下方式验证此技能的真实性：
1. 直接从 GitHub 仓库克隆：`git clone https://github.com/ansengu11/openclaw-safe-guard.git`
2. 检查本地文件与仓库文件的哈希值

> 🦞 对 OpenClaw 系统安全检查设置及已安装和你想要安装的 Skills 进行静态安全扫描，检测权限风险、恶意代码和依赖风险

## ✅ 快速安装检查清单

**运行此技能前，请确保：**

- [ ] 系统已安装：`curl`、`jq`、`git`、`grep`、`find`
- [ ] 理解技能会**读取** `~/.openclaw/skills` 目录（可能包含其他技能的敏感信息）
- [ ] 理解技能会**访问** GitHub API 并**临时克隆**仓库到 `/tmp`
- [ ] 已在隔离环境测试运行

---

## 功能

此技能（Security Scanner / Skill Auditor / 安全审计工具）用于对 OpenClaw 系统安全检查设置及已安装和你想要安装的 Skills 进行静态安全扫描（安全审计、漏洞检测）：
- 扫描指定 Skill 的权限风险（permission audit）
- 检查是否有恶意代码（malware detection, vulnerability scan）
- 分析依赖包安全性（dependency analysis）
- 生成中文风险评估报告（Chinese language support）
- 给出修复建议（security recommendations）

**支持中文和英文界面输出**

## 触发条件

用户说以下内容时激活：
- "扫描 Skill 安全"
- "检查 Skill 风险"
- "这个 Skill 安全吗"
- "帮我看看这个技能"
- "扫描已安装的 Skills"
- "安全审计"
- "漏洞检测"
- "龙虾安全检测"
- "技能安全检测"
- "技能漏洞检测"

## 使用方式

```
用户: 帮我扫描 ansen-ai 这个 Skill
AI: → 调用 openclaw-safe-guard，输入 "ansen-ai"

用户: 检查 openclaw/skills 目录下的 Skills
AI: → 调用 openclaw-safe-guard，扫描所有已安装的 Skills
```

## 输出格式

```markdown
# 🔒 Skill 安全评估报告

## 基础信息
- 名称：xxx
- 路径：~/.openclaw/skills/xxx
- Stars：xx（来自 GitHub）
- 官方：✅/❌

## 风险评分：🟢 低风险 / 🟡 中风险 / 🔴 高风险
- **分数说明**：0-10 分 = 🟢 低风险，11-20 分 = 🟡 中风险，21+ 分 = 🔴 高风险
- **分数越低 = 越安全**

## 权限检查
| 权限 | 状态 | 风险 |
|------|------|------|
| 网络请求 | ✅ 无 | 低 |
| Shell 执行 | ⚠️ 有 | 中 |
| 文件访问 | ⚠️ 有 | 中 |

## 详细分析
### 代码检查
- 敏感信息泄露：❌ 未发现
- 恶意代码：❌ 未发现
- 可疑 API 调用：❌ 未发现

### 依赖检查
- 第三方包：无风险

## 建议
1. 建议审查 Shell 脚本内容
2. 建议仅授予必要权限

## 总结
该 Skill 风险等级：🟡 中风险
建议：可使用，但需注意权限
```

## ⚠️ 安全警告

**在安装此技能前，请注意以下风险：**

1. **文件系统读取**：此技能需要读取 `~/.openclaw/skills` 和 `~/.openclaw/workspace/skills` 目录，可能访问到其他技能中可能存在的敏感信息（如 API 密钥、凭证等）

2. **网络访问**：会访问 GitHub API（api.github.com）获取技能元数据

3. **临时文件**：在线扫描时会将第三方 GitHub 仓库克隆到 `/tmp` 目录，扫描完成后会清理

4. **仅静态分析**：不执行被扫描的技能代码，仅读取和分析源码

## 所需系统工具（必须安装）

| 工具 | 用途 |
|------|------|
| `curl` | 访问 GitHub API 获取技能信息 |
| `jq` | 解析 JSON 数据 |
| `git` | 克隆 GitHub 仓库（在线扫描时） |
| `grep` | 搜索代码中的敏感模式 |
| `find` | 查找技能文件 |

## 权限声明（完整清单）

```json
{
  "requires": {
    "filesystem": [
      "~/.openclaw/skills",
      "~/.openclaw/workspace/skills",
      "/tmp"
    ],
    "commands": [
      "curl",
      "jq", 
      "git",
      "grep",
      "find"
    ],
    "network": [
      "api.github.com",
      "github.com"
    ]
  },
  "dependencies": {
    "system_tools": [
      "curl",
      "jq",
      "git",
      "grep",
      "find"
    ]
  },
  "environment": {
    "description": "需要网络访问 GitHub API 获取 Skill 信息，临时文件写入 /tmp 目录"
  }
}
```

## 安装前建议

1. ✅ 确认系统已安装所需工具：curl, jq, git, grep, find
2. ✅ 人工审查 scan.sh 源码（已含在包内）
3. ✅ 建议在非 root 账户下运行
4. ✅ 如有条件，可在容器或只读环境中运行

## 示例

### 扫描单个 Skill
```
用户: 帮我看看 ansen-ai 安全吗
AI: 正在扫描 ansen-ai Skill...
[调用 openclaw-safe-guard]
AI: 扫描完成！该 Skill 风险等级为 🟢 低风险...
```

### 扫描所有 Skills
```
用户: 扫描所有已安装的 Skills
AI: 正在扫描 ~/.openclaw/skills 目录...
[调用 openclaw-safe-guard]
AI: 共扫描 X 个 Skills，发现 Y 个高风险...
```

## 限制

- ⚠️ 风险评估基于启发式规则，可能有误判
- ⚠️ 建议配合人工代码审查
- ⚠️ 不保证 100% 检测所有安全问题
- ⚠️ 官方仓库 (openclaw/*) 会标记为"已通过官方审核"，但仍会执行基础扫描

## 🔒 安全说明

### 已修复的安全问题
1. ✅ **命令注入漏洞**：所有用户输入都经过严格过滤
2. ✅ **系统信息探测**：已完全移除

### 已知风险
1. 读取 ~/.openclaw/skills 目录（可能访问其他技能的 API 密钥）
2. 从 GitHub 克隆代码到本地 /tmp

### 安全使用建议
- ✅ 始终在隔离环境（容器/虚拟机）中运行
- ✅ 不要以 root 权限运行
- ✅ 运行前备份重要数据
- ✅ 审查所有扫描结果，不要盲目信任

### 环境变量
| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `OPENCLAW_NONINTERACTIVE` | false | 设为 true 跳过确认提示 |
