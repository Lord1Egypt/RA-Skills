# 公众号文章发布工作流 (mp-publisher)

完整的公众号文章发布流程：选题生成 → 撰稿 → 审稿 → 配图 → 发布草稿。

## 功能特点

- 🤖 **AI驱动**：使用subagent系统，每个角色专注自己的任务
- 📝 **完整流程**：从选题到草稿，一站式完成
- 🎨 **自动配图**：支持DMXAPI生成科技感配图
- 📊 **流程监控**：实时追踪每个阶段的状态
- 🔄 **可恢复**：支持断点续传，超时自动恢复

## 快速开始

### 1. 安装技能

```bash
clawhub install mp-publisher
```

### 2. 运行初始化

```bash
~/.openclaw/workspace/skills/mp-publisher/scripts/setup.sh
```

### 3. 配置环境

编辑 `~/.openclaw/workspace-mp-editor/.env`：

```env
WECHAT_APP_ID=your_app_id
WECHAT_APP_SECRET=your_app_secret
```

编辑 `~/.openclaw/workspace-designer/.env`：

```env
DMX_API_KEY=your_api_key
```

### 4. 添加IP白名单

在微信公众号后台 → 设置与开发 → 基本配置 → IP白名单，添加运行机器的IP地址。

## 使用方法

### 生成选题

```
用户：今天写三篇
```

系统会自动：
1. 启动资料员生成选题
2. 展示选题让用户选择
3. 用户选择后启动撰稿流程

### 选择选题

```
用户：选题1、2、3
```

系统会启动对应数量的撰稿任务。

## 工作流程

```
资料员（选题）→ 用户选择 → 撰稿员（搜索+撰写）→ 审稿员 → 美工（4图）→ 主编（发布草稿）
```

| 角色 | agentId | 职责 |
|------|---------|------|
| 资料员 | work | 生成选题（arXiv论文+AI新闻） |
| 撰稿员 | writer | 搜索资料、撰写文章 |
| 审稿员 | reviewer | 评分审核（>=90分通过） |
| 美工 | designer | 生成4张配图（封面+3内页） |
| 主编 | mp-editor | 发布到公众号草稿箱 |

## 文章规范

### 标题格式
新闻事件 + 工程师视角的判断问题

### 配图规格
- 数量：4张（封面 + 3张内页）
- 尺寸：1376×768（16:9）
- 风格：科技感、简洁

### 审稿评分
- >= 90分：通过，启动美工
- < 90分：返回修改（最多3次）

## 文件结构

```
mp-publisher/
├── SKILL.md              # 技能说明
├── package.json          # 包配置
├── README.md             # 本文件
├── scripts/
│   ├── workflow-monitor.py    # 流程监控
│   └── setup.sh               # 环境初始化
├── templates/
│   └── article.md        # 文章模板
└── lib/
    ├── image_generator.py     # 配图生成
    └── draft_publisher.py     # 草稿发布
```

## 依赖

- OpenClaw subagent 系统
- 微信公众号 API
- DMX API（配图生成）
- arxiv-watcher 技能（论文搜索）
- tavily 技能（新闻搜索）

## 注意事项

1. **IP白名单**：发布前确保机器IP在公众号白名单中
2. **并发控制**：多篇文章可并行处理
3. **状态追踪**：每篇文章末尾有 `<!-- STATUS: xxx -->` 标记
4. **自动发布**：不尝试自动发布，只创建草稿

## 许可证

MIT License

---

_版本: 1.0.0_
_作者: 吴曦_
