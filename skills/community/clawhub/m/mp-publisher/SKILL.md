# SKILL.md - 公众号文章发布流程

## 描述

完整的公众号文章发布工作流：选题生成 → 撰稿 → 审稿 → 配图 → 发布草稿。

## 触发条件

- 用户说"今天写X篇"
- 用户说"选题X"或"选X"
- 用户要求生成选题、写文章、发布公众号

## 工作流程

```
资料员（选题）→ 用户选择 → 撰稿员（搜索+撰写）→ 审稿员 → 美工（4图）→ 主编（发布草稿）
```

## 角色分工

| 角色 | agentId | 职责 |
|------|---------|------|
| 资料员 | work | 生成选题（arXiv论文+AI新闻） |
| 撰稿员 | writer | 搜索资料、撰写文章 |
| 审稿员 | reviewer | 评分审核（>=90分通过） |
| 美工 | designer | 生成4张配图（封面+3内页） |
| 主编 | mp-editor | 发布到公众号草稿箱 |

## 配置要求

### 1. 微信公众号配置

在 `~/.openclaw/workspace-mp-editor/.env` 中配置：

```env
WECHAT_APP_ID=your_app_id
WECHAT_APP_SECRET=your_app_secret
```

**IP白名单**：需在公众号后台添加运行机器的IP地址。

### 2. 配图API配置

在 `~/.openclaw/workspace-designer/.env` 中配置：

```env
DMX_API_KEY=your_api_key
```

### 3. 工作目录

- 文章存储：`~/.openclaw/workspace-work/`
- 配图存储：`~/.openclaw/workspace-designer/images/`
- 流程状态：`~/.openclaw/workspace-work/.workflow-state.json`

## 文章规范

### 标题格式
新闻事件 + 工程师视角的判断问题

### 结构要求
- 开头：第一段说清核心论点
- 结构：论点 → 论证 → 结论
- 配图标记：【配图1】【配图2】【配图3】
- 结尾：有变化的判断表达，避免"吴曦的判断"固化模式

### 审稿评分
- >= 90分：通过，启动美工
- < 90分：返回修改（最多3次）

### 配图规格
- 数量：4张（封面 + 3张内页）
- 尺寸：1376×768（16:9）
- 风格：科技感、简洁

## 使用方法

### 生成选题

```
用户：今天写三篇
```

系统会：
1. 启动资料员生成选题
2. 展示选题让用户选择
3. 用户选择后启动撰稿流程

### 选择选题

```
用户：选题1、2、3
```

系统会启动对应数量的撰稿任务。

## 文件结构

```
mp-publisher/
├── SKILL.md              # 本文件
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

---

_版本: 1.0.0_
_更新: 2026-04-04_
