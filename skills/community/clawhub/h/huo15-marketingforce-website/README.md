# T云建站技能 (MarketingForce Website Editor)

> 通过 CMS API 全功能管理迈富时(T云/MarketingForce)建站平台网站内容。

## 功能概览

覆盖 **20+ 模块**、**354 个 API 端点**：

| 模块 | 说明 | 命令 |
|------|------|------|
| 文章管理 | 文章增删改查、批量发布、SEO设置 | `mf_client.py articles` |
| 文章分类 | 分类管理、SEO配置 | `mf_client.py categories` |
| 产品管理 | 产品增删改查、批量导入 | `mf_client.py products` |
| 产品分类/标签 | 分类和标签管理 | `mf_client.py product-cats` |
| 短视频管理 | 抖音短视频、用户管理 | `mf_client.py videos` |
| 推荐管理 | 关键词推荐、锚点管理 | `mf_client.py keywords` |
| 营销互动/询盘 | 表单管理、询盘消息 | `mf_client.py inquiries` |
| 资源库 | 图片管理、相册、文件上传 | `mf_client.py images` |
| 网站设置 | 站点配置、客服、导航、主题 | `mf_client.py site-config` |
| SEO功能 | 关键词、敏感词、站点评分 | `mf_client.py seo-keywords` |
| 蜘蛛分析 | 蜘蛛抓取热页、趋势 | `mf_client.py spider` |
| 首页概况 | 站点状态、统计、诊断 | `mf_client.py dashboard` |
| 插件管理 | 浮动视频、分享、客服等 | `mf_client.py plugins` |
| 多语言 | 语言列表、翻译同步 | `mf_client.py languages` |
| 用户中心 | 会员管理、等级 | `mf_client.py members` |
| AI功能 | AI任务、内容提取 | `mf_client.py ai-tasks` |
| 系统管理 | 操作日志、备份 | `mf_client.py system-logs` |
| 模板管理 | 968+ 网站模板 | `mf_client.py templates` |

## 快速开始

### 1. 配置 Token

在 `scripts/.env` 中写入从浏览器获取的 Token：

```
MF_X_TOKEN=your_x_token
MF_ADMIN_TOKEN=token_your_admin_token
```

**获取方式**：浏览器 DevTools → Application → Cookies
- `.71360.com` → `X-Token`
- `.marketingforce.com` → `admin_token`

### 2. 验证 Token

```bash
python3 scripts/mf_client.py test
```

### 3. 使用

```bash
# 列出所有网站
python3 scripts/mf_client.py sites

# 列出文章
python3 scripts/mf_client.py articles

# 查看文章详情
python3 scripts/mf_client.py article 103

# 列出产品
python3 scripts/mf_client.py products

# 查看询盘消息
python3 scripts/mf_client.py inquiries

# 查看蜘蛛分析
python3 scripts/mf_client.py spider

# 查看站点概况
python3 scripts/mf_client.py dashboard
```

## 认证架构

```
浏览器登录 console.marketingforce.com
  → SSO (RSA加密 + 短信验证)
  → 获取 X-Token (控制台 session)
  → 访问 siteadmin.marketingforce.com
  → 获取 admin-token (站点管理 token)
```

两个 Token 都需要作为 HTTP Header 发送：
- `X-Token`: 控制台会话
- `admin-token`: 站点管理（格式 `token_<hex>`）

## API 架构

| 服务 | Base URL |
|------|----------|
| CMS | `https://api.71360.com/api/app/site-admin-api/admin_cms` |
| Site Admin | `https://api.71360.com/api/app/site-admin-api/admin` |
| Site/BPF | `https://api.71360.com/api/app/obor-nginx-php/tweb` |
| Console | `https://api.71360.com/api/app/aggregateservice-web/api` |

## 文件结构

```
huo15-marketingforce-website/
├── SKILL.md              ← ClawHub 嵌入源
├── _meta.json            ← 元数据
├── README.md             ← 本文件
├── scripts/
│   ├── mf_client.py      ← Python CLI 工具（50+ 命令）
│   └── .env              ← Token 存储（gitignored）
└── references/
    └── reference.md      ← 完整 354 端点 API 参考文档
```

## 当前配置的网站

- **账号**: shanghailongjie
- **网站**: www.uwtsd.com (威尔士三一圣大卫大学)
- **后台**: siteadmin.marketingforce.com

## 安全规则

- 编辑前始终备份原内容
- 先设为草稿(`status: 0`)预览，确认后再发布(`status: 1`)
- 删除前需用户确认，优先使用隐藏(`disabled: "true"`)
- 对用户提供的 HTML 内容进行 XSS 消毒
