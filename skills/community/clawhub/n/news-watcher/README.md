# News Watcher - Playwright Skill

一个使用 Playwright 实时监听虚拟货币新闻的 OpenClaw Skill。

## 快速开始

### 安装依赖

```bash
cd ~/.openclaw/workspace/skills/news-watcher
npm install
# 或
pnpm install
```

### 基础使用

```bash
# 监听 CoinDesk（每 60 秒检查一次）
npm run watch

# 监听 PANews
npm run watch:panews

# 自定义间隔
node scripts/watch-news.js --site coindesk --interval 120
```

## 集成到 OpenClaw

这个 skill 会在 OpenClaw gateway 启动时自动加载。

## 工作流程

1. 定期访问新闻网站
2. 提取最新文章列表
3. 计算内容哈希
4. 与上次保存的哈希比对
5. 如有变化，通知 Agent

## 使用场景

### 场景 1：后台持续监听

```bash
# 在后台运行（使用 nohup 或 screen）
nohup node ~/.openclaw/workspace/skills/news-watcher/scripts/watch-news.js &
```

### 场景 2：定时检查（配合 Cron）

```bash
openclaw cron add \
  --name "News Check" \
  --cron "*/30 * * * *" \
  --session isolated \
  --message "检查最新加密新闻变化" \
  --announce \
  --channel telegram \
  --to 8015532995
```

### 场景 3：由 Agent 按需调用

```bash
openclaw agent --message "监听 CoinDesk 新闻，告诉我有什么重要新闻"
```

## 文件结构

```
news-watcher/
├── scripts/watch-news.js      # 主脚本
├── skill.json                  # OpenClaw 工具定义
├── package.json                # 依赖
├── SKILL.md                    # 完整文档
├── README.md                   # 本文件
└── _meta.json                  # 元数据
```

## 关键文件说明

### skill.json
定义了 OpenClaw 如何调用这个 skill：
- 工具名称：`news_watch`
- 命令：`node scripts/watch-news.js`
- 参数：`site`、`check_interval`

### watch-news.js
核心实现：
- 使用 Playwright 加载网页
- 提取新闻内容
- 通过 MD5 哈希检测变化
- 输出结果到控制台

## 原理

使用 **哈希变化检测** 而不是 RSS 订阅：

```
第一次运行：
网站内容 → 提取 → 计算 Hash → 保存（baseline）

后续运行：
网站内容 → 提取 → 计算 Hash → 对比上次 Hash
    ↓
  相同 → 无更新
  不同 → 有新闻！ → 通知
```

**优点：**
- ✅ 不依赖 RSS（即使网站没有 RSS）
- ✅ 能检测到任何内容变化
- ✅ 性能高效（只对比哈希)

**缺点：**
- ✅ 需要定期访问网站
- ⚠️ 可能还是比不上真实的 webhook 快（但比轮询快得多）

## 下一步改进

- [ ] 支持 WebSocket 实时检测
- [ ] 添加关键词过滤
- [ ] 支持多网站并行监听
- [ ] 集成到 OpenClaw 系统服务（自启动）
- [ ] 添加 Discord 通知

## 故障排除

**问题：** Playwright 无法加载页面  
**解决：** 检查网络，或增加超时时间

**问题：** 看不到输出  
**解决：** 运行时加 `PLAYWRIGHT_HEADLESS=false` 查看浏览器

**问题：** 内存占用过高  
**解决：** 增加检查间隔（`--interval 300`）

## 许可证

MIT
