---
name: 头条全自动发布
description: 自动发布图文文章和微头条到头条号，支持选题、写文、配图生成、Cookie登录、图文混排发布的全自动流程，也可定时自动化执行。
---

# 头条全自动发布 Skill

全自动发布图文文章和微头条到头条号的 AI Agent Skill。

## 功能特性

- **图文文章发布**：从选题 → 写文 → 配图 → 发布的完整流程
- **微头条发布**：快速发布短内容（~200字）到微头条
- **配图生成**：自动生成水墨中国风配图（支持自定义风格）
- **Cookie 登录**：通过 Cookie 注入实现免验证码登录
- **图文混排**：正文与配图混排，排版美观
- **飞书通知**：发布成功/失败后自动推送通知
- **定时自动化**：支持每小时自动发布（可配置时间段）
- **热门话题获取**：自动从话题邀请中筛选围观最多的话题

## 前置条件

1. 已有头条号（mp.toutiao.com）
2. 已安装 Python 3.8+ 和 Playwright
3. Chrome 浏览器已安装
4. 已获取头条号的 Cookie（JSON 格式）

## 快速开始

### 第一步：配置账号

复制 `config/account_config.json.example` 为 `config/account_config.json`，填入你的信息：

```json
{
  "account_id": "你的头条账号ID",
  "account_name": "你的头条号名称",
  "cookie_file": "/path/to/toutiao_cookies.json",
  "inject_script": "/path/to/inject_cookies.sh",
  "feishu_config": {
    "app_id": "可选，飞书机器人APP_ID",
    "app_secret": "可选，飞书机器人APP_SECRET",
    "open_id": "可选，飞书通知接收人OPEN_ID"
  }
}
```

### 第二步：获取 Cookie

1. 用 Chrome 打开 https://mp.toutiao.com 并登录
2. 按 F12 → Application → Cookies → 复制所有 Cookie 到 JSON 文件
3. Cookie 有效期约 30 天，过期需重新获取

### 第三步：安装依赖

```bash
pip install playwright
playwright install chromium
pip install -r requirements.txt
```

## 使用方法

### 方式一：AI Agent 自动执行（推荐）

安装此 Skill 后，直接用自然语言指示 Agent：

- "帮我发布一篇关于「中年焦虑」的头条文章"
- "写一篇微头条，主题是职场困境，200字"
- "生成一张水墨中国风的配图"
- "设置每天 6 点到 23 点每小时自动发微头条"

Agent 会自动完成：选题 → 内容生成 → 配图生成 → Cookie 注入 → 发布 → 通知

### 方式二：脚本调用

```bash
# 发布图文文章
python3 scripts/publish_article.py
python3 scripts/publish_article.py --topic "中年困境"
python3 scripts/publish_article.py --no-publish  # 只生成不发布

# 发布微头条
python3 scripts/publish_weitoutiao.py
python3 scripts/publish_weitoutiao.py --content "你的内容"
python3 scripts/publish_weitoutiao.py --auto-topic  # 自动选题

# 定时自动化
python3 scripts/run_scheduler.py --type article
python3 scripts/run_scheduler.py --type weitoutiao
python3 scripts/run_scheduler.py --type both
```

## 工作流程

### 图文文章发布

```
选题/指定话题 → 生成文章内容 → 生成1张水墨风配图
→ Cookie注入登录 → 导航到发布页 → 填写标题 → 填写正文
→ 插入配图到正文 → 设置封面 → 勾选声明 → 发布 → 通知
```

**发布 URL**：`https://mp.toutiao.com/profile_v4/graphic/publish`

**关键步骤**：
1. 通过 Playwright CDP 连接已有 Chrome（端口 9222）
2. Cookie 注入后导航到发布页
3. 标题用 JS 原生 setter + 事件触发（避免 ProseMirror 拦截）
4. 正文用 `insertHTML` 一次性插入段落
5. 配图通过工具栏图片按钮 → file input 上传
6. 封面选择"单图"模式上传
7. 勾选"个人观点，仅供参考"声明
8. 点击"预览并发布" → "确认发布"

### 微头条发布

```
获取热门话题 → 生成短内容（~200字） → 生成配图
→ Cookie注入登录 → 导航到微头条发布页 → 填写内容
→ 上传配图 → 发布 → 通知
```

**发布 URL**：`https://mp.toutiao.com/profile_v4/weitoutiao/publish`

## 配置说明

### account_config.json

| 字段 | 必填 | 说明 |
|------|------|------|
| account_id | 是 | 头条账号 ID |
| account_name | 是 | 头条号名称 |
| cookie_file | 是 | Cookie JSON 文件路径 |
| inject_script | 否 | Cookie 注入脚本路径 |
| feishu_config | 否 | 飞书通知配置 |

### automation_settings.json

```json
{
  "article": {
    "enabled": true,
    "schedule": "0 * 6-23 * * *",
    "max_retries": 3,
    "timeout": 300
  },
  "weitoutiao": {
    "enabled": true,
    "schedule": "0 * 6-23 * * *",
    "auto_select_topic": true,
    "timeout": 180
  }
}
```

## 核心模块 API

### PlaywrightPublisher（浏览器自动化发布引擎）

```python
from core.playwright_publisher import PlaywrightPublisher

pub = PlaywrightPublisher(headless=False, account_name="你的账号名")
await pub.start()                          # 启动 CDP 连接
await pub.load_cookies("/path/to/cookies.json")  # 注入 Cookie
await pub.navigate_to_publish()            # 导航到发布页
await pub.fill_title("文章标题")            # 填写标题
await pub.fill_content("文章正文")          # 填写正文
await pub.insert_image("/path/to/img.png")  # 插入正文配图
await pub.upload_cover_image("/path/to/img.png")  # 设置封面
await pub.check_declarations()             # 勾选声明
success = await pub.publish()              # 发布
```

### PublisherManager（API 方式发布）

```python
from core.publisher import PublisherManager

pub = PublisherManager(config_file="config/account_config.json")

# 图文发布
result = await pub.publish_article(
    title="标题", content="内容",
    images=["/path/to/img1.png"],
    options={"personal_view": True}
)

# 微头条发布
result = await pub.publish_weitoutiao(
    content="微头条内容", image="/path/to/img.png"
)

# 获取热门话题
topics = await pub.get_topic_invitations()
topic = pub.get_hot_topic(topics)  # 围观最多的话题
```

## 配图生成

支持通过 AI 工具自动生成水墨中国风配图：

```python
# 推荐提示词模板
prompt = "水墨中国风画，竹子，宣纸底色，红色印章，极简留白"
size = "1024x1024"
```

**风格关键词**：竹子、宣纸、红色印章、极简、留白、山水、松树

## 故障排查

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 发布失败，提示重新登录 | Cookie 过期 | 重新获取 Cookie（有效期约30天） |
| 封面上传失败 | DOM 选择器变化 | 查看 logs/ 目录截图调试 |
| 配图生成失败 | AI 服务不可用 | 检查网络或换时段重试 |
| 预览对话框未弹出 | 页面加载慢 | 增加等待时间或检查截图 |
| 定时任务不执行 | schedule 配置错误 | 检查 automation_settings.json |
| AI 助手抽屉遮挡操作 | 头条 SPA 的 AI 浮层 | 自动用 JS 隐藏所有 drawer |

## 项目结构

```
toutiao-publisher/
├── SKILL.md                          # 本文件（ClawHub 标准格式）
├── README.md                         # 详细文档
├── requirements.txt                  # Python 依赖
├── config/
│   ├── account_config.json.example   # 账号配置模板
│   └── automation_settings.json      # 自动化设置
├── core/
│   ├── playwright_publisher.py       # Playwright 自动化发布引擎
│   ├── publisher.py                  # API 方式发布器
│   ├── article_generator.py          # 文章内容生成
│   ├── image_generator.py            # 配图生成
│   ├── cookie_manager.py             # Cookie 管理
│   └── notifier.py                   # 通知系统
├── scripts/
│   ├── publish_article.py            # 图文发布脚本
│   ├── publish_weitoutiao.py         # 微头条发布脚本
│   └── run_scheduler.py              # 定时任务脚本
├── templates/
│   ├── article_prompts/              # 文章生成提示词
│   └── weitoutiao_prompts/           # 微头条提示词
└── logs/                             # 日志目录
```

## 安全建议

- **不要**将 Cookie 文件或包含密钥的配置文件上传到公开仓库
- 使用 `.gitignore` 忽略 `config/account_config.json`
- 定期更新 Cookie（有效期约 30 天）
- 遵守头条平台规则，避免违规操作

## 许可证

MIT License - 欢迎自由使用和修改

## 变更日志

### v2.0.0 - 包含实际可执行代码
- 新增完整 Python 核心代码（core/ 目录）
- 所有硬编码个人信息替换为配置变量（从 config/account_config.json 读取）
- 新增 publish_article.py / publish_weitoutiao.py / run_scheduler.py 脚本
- 支持命令行参数调用
- 支持自定义个人画像（ArticleGenerator 支持传入 personal_profile）
- 新增 .gitignore 保护敏感配置

### v1.0.0 - 初始发布
- 文档和配置模板

## 版本

v2.0.0 - 包含完整代码，通用化配置，可直接使用
