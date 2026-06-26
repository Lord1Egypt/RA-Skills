# 学习日志参考：写作模式与示例

## LRN（Learning）写作模式

### 模式1：工具发现
```markdown
## LRN-20260405-001: web_fetch vs browser 的选择原则

**来源**: 牢大自主进化第4轮
**日期**: 2026-04-05

### 核心
静态页面用 `web_fetch`，动态页面（JS渲染）用 `browser`。

### 细节
- `web_fetch`：轻量快速，适合静态内容提取
- `browser`：完整浏览器环境，慢但能处理复杂JS

### 适用
任何网页抓取任务，优先尝试 web_fetch，失败再换 browser。
```

### 模式2：配置技巧
```markdown
## LRN-20260405-002: clawhub 限流机制

**来源**: 水产市场安装失败
**日期**: 2026-04-05

### 核心
clawhub 限制 30次/分钟，超限需等待60秒重试。

### 细节
- 搜索和安装共享限额
- 建议安装多个技能时批次操作，中间留间隔

### 踩坑
连续安装3个技能后触发限流，等待重试成功。
```

## ERR（Error）写作模式

### 模式：真实踩坑记录
```markdown
## ERR-20260405-001: skillhub_install 在 Windows 全失败

**错误类型**: 环境兼容性
**发生频率**: 100%（Windows必现）

### 问题
使用 `skillhub_install` 工具在 Windows 上安装任何技能都失败。

### 原因
skillhub CLI 在 Windows 环境检测失败，回退到 skillhub API，但 API 也无法正常工作。

### 解决
切换使用 `clawhub` CLI 替代。

### 预防
Windows 环境优先使用 clawhub，不尝试 skillhub_install。
```

## FEAT（Feature）写作模式

### 模式：技能评估
```markdown
## FEAT-20260405-001: agent-council 多Agent管理系统

**评分**: ⭐⭐⭐⭐⭐ (5/5)
**类型**: skill
**来源**: 水产市场 clawhub install

### 亮点
完整的多Agent创建与管理工具包，支持 Discord 频道绑定和 Agent 间通信。

### 使用方法
1. 创建Agent配置目录
2. 定义 SOUL.md / HEARTBEAT.md
3. 使用 sessions_send/spawn 进行 Agent 间通信

### 注意事项
需要 Discord Bot Token 才能使用频道功能。
```

## DEC（Decision）写作模式

### 模式：架构决策
```markdown
## DEC-20260405-001: 技能存储位置选择

**问题**: 用户创建的技能应该存储在哪里？
**选项**:
1. `~/.qclaw/skills/` - 用户目录
2. `~/.openclaw/skills/` - 应用目录
3. `resources/openclaw/config/skills/` - 打包目录

**决策**: 选择1 `~/.qclaw/skills/`

**理由**: 
- 应用更新不会丢失
- 便于版本管理
- 与 OpenClaw 内置技能分离

### 后果
✅ 技能持久化，重装应用保留
⚠️ 需要手动备份
```

## IDEA（Idea）写作模式

```markdown
## IDEA-20260405-001: 自动化技能评分系统

**灵感来源**: 进化循环中手动评估技能

### 想法
基于使用频率、功能完整性、社区活跃度自动给技能打分。

### 实现思路
1. 抓取水产市场评分
2. 结合 VirusTotal 安全评分
3. 计算综合评分辅助选择

### 优先级
中 - 可行但非紧急
```
