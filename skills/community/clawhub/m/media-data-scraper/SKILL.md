---
name: 全网作品数据抓取分析工具（抖音小红书视频号快手B站通用）
description: 抓取抖音、小红书、B站、快手、视频号五大平台作品数据（播放/点赞/评论/分享/收藏），完全免费，无需登录/API Key/付费。支持飞书多维表格同步。
triggers:
  - 数据抓取
  - 数据解析
  - 查看数据
  - 分析数据
  - 抓取链接
  - 解析链接
  - 查看作品数据
  - 作品数据
  - 视频数据
  - 笔记数据
---

# 全网作品数据抓取分析工具（抖音小红书视频号快手B站通用）

## 触发条件
当用户提供社交媒体链接（抖音、小红书、B站、快手、视频号），或说出以下关键词时自动激活：
- 数据抓取、数据解析、查看数据、分析数据
- 抓取链接、解析链接、查看作品数据
- 作品数据、视频数据、笔记数据

## 支持平台

| 平台 | 链接格式 | 抓取方式 | 数据完整度 |
|------|---------|---------|-----------|
| B站 | bilibili.com/video/BVxxx | 公开API直调 | 100%（播放/点赞/投币/收藏/弹幕/评论/分享） |
| 抖音 | v.douyin.com/xxx | SSR数据提取 | 100%（播放/点赞/评论/分享/收藏） |
| 快手 | v.kuaishou.com/xxx | INIT_STATE提取 | 100%（播放/点赞/评论/分享/收藏） |
| 小红书 | xiaohongshu.com/explore/xxx | curl_cffi + xsec_token SSR | 100%（点赞/收藏/评论/分享） |
| 视频号 | weixin.qq.com/sph/xxx | API探测+浏览器DOM | 脚本模式需降级，有浏览器时100% |

## 执行流程

### 第一步：脚本抓取（首选）

```python
import sys
sys.path.insert(0, '/workspace/social-media-scraper')
from scraper import scrape_post, format_result, save_results

# 单个链接
result = scrape_post('用户提供的链接')
print(format_result(result))

# 批量抓取
from scraper import scrape_posts
results = scrape_posts(['链接1', '链接2', '链接3'])
save_results(results, '/workspace/social_data.json')
```

### 第二步：检查结果

- `status=success` → 数据完整，直接输出
- `status=partial` → 部分数据，输出已有数据并标注缺失
- `status=error` → 查看错误信息，决定是否需要浏览器降级

### 第三步：处理视频号（特殊流程）

视频号是微信封闭生态的纯SPA页面，**脚本模式无法获取数据**。当检测到视频号链接时，按以下流程处理：

#### 3A. 检查当前环境是否有浏览器工具

```python
from scraper import scrape_post, BROWSER_JS_CHANNELS

result = scrape_post('https://weixin.qq.com/sph/xxx')

if result['platform'] == 'channels':
    # 视频号必须浏览器环境
    if has_browser_capability():  # 检查是否有 browser_navigate 等工具
        # 使用浏览器降级
        browser_navigate(result.get('resolved_url', result['url']))
        browser_wait_for(time=3)
        data = browser_evaluate(BROWSER_JS_CHANNELS)
        # data 包含: author, description, likes, shares, collects, comments, publish_time, cover_url
    else:
        # 无浏览器环境，返回明确提示
        print("当前环境无浏览器工具，视频号数据无法获取。")
        print("解决方案：")
        print("1. 在支持浏览器的环境中运行")
        print("2. 使用第三方API服务（如TikHub）")
        print("3. 手动查看数据")
```

#### 3B. 浏览器降级详细步骤

**视频号浏览器降级**（必须，纯脚本无法获取）：
1. 用 `browser_navigate` 打开视频号链接
2. 等待页面加载（`browser_wait_for` 3秒）
3. 用 `browser_evaluate` 执行 `BROWSER_JS_CHANNELS` 提取数据
4. `BROWSER_JS_CHANNELS` 代码在 scraper.py 文件末尾

**小红书浏览器降级**（xsec_token过期时）：
1. 用 `browser_navigate` 打开小红书链接
2. 等待页面加载（`browser_wait_for` 2秒）
3. 用 `browser_evaluate` 执行 `BROWSER_JS_XHS` 提取数据
4. `BROWSER_JS_XHS` 代码在 scraper.py 文件末尾

## 小红书特别说明

### xsec_token 机制
- 小红书分享链接中的 `xsec_token` 是临时凭证，有效期约5分钟
- **必须使用完整的分享链接**（包含 xsec_token 参数）才能获取完整数据
- 纯笔记ID链接（如 `xiaohongshu.com/explore/xxx`）会被 300031 拦截
- token 过期后脚本会明确提示"xsec_token 已过期，请使用最新的分享链接"

### 用户操作指引
- 从小红书App点击"分享"→"复制链接"，粘贴完整链接
- 不要手动删除链接中的 xsec_token 参数
- 如果提示token过期，重新从App复制分享链接即可

### 技术实现
- 使用 `curl_cffi` 模拟 Chrome TLS 指纹（绕过 JA3 检测）
- 从 SSR 渲染的 HTML 中提取 `window.__INITIAL_STATE__` 大型 JSON
- 深度 JSON 清理：处理 undefined、空值、尾部逗号等非法格式
- 标题为空时自动使用描述前50字作为标题

## 依赖安装

```bash
pip install curl_cffi requests beautifulsoup4 lxml brotli
```

核心依赖：`curl_cffi`（小红书必需）、`requests`（通用）、`beautifulsoup4`（Meta兜底）

## 飞书多维表格同步（可选）

支持将每次抓取的数据自动同步到飞书多维表格，方便统一管理和分析。

### 首次使用提示

首次调用 `scrape_post()` 时，会自动输出一次性提示（不占用使用次数）：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 飞书多维表格同步（可选）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

您可以将抓取的数据自动同步到飞书多维表格...

👉 如需配置，请对我说"配置飞书"
👉 如不需要，直接开始抓取即可，此提示不会再次显示
```

### 用户主动配置

当用户说"配置飞书"、"设置飞书推送"等关键词时，按以下流程处理：

```python
from feishu_sync import handle_config_command, setup_config

# 1. 判断用户意图并获取配置指引
result = handle_config_command("配置飞书")
if result["is_config_command"]:
    print(result["guide"])  # 展示配置指引给用户
    # 引导用户提供参数...

# 2. 收集到用户参数后，调用 setup_config() 完成配置
config_result = setup_config(
    base_url="https://xxx.feishu.cn/base/XXXXXX",  # 多维表格链接
    table_id="tblxxxxx",                            # 数据表ID（可选）
    app_id="cli_xxxxxx",                            # 无lark-cli时必填
    app_secret="xxxxxx"                             # 无lark-cli时必填
)
print(config_result["message"])
```

### 配置方式

**方式一：lark-cli（推荐，环境有 lark-cli 时自动使用）**
- 安装：`pip install lark-cli`
- 授权：`lark-cli auth login`
- 只需提供多维表格链接即可

**方式二：飞书开放平台 API（无 lark-cli 时使用）**
- 前往 open.feishu.cn 创建应用
- 获取 App ID 和 App Secret
- 为应用添加"多维表格"权限（bitable:record）
- 提供 App ID、App Secret 和 Base Token

### 同步字段

推送到飞书多维表格的字段包括：

| 字段 | 说明 |
|------|------|
| 平台 | 抖音/小红书/B站/快手/视频号 |
| 作品标题 | 作品标题 |
| 作者 | 作者昵称 |
| 链接 | 原始链接 |
| 播放量 | 播放量（格式化，如 1.2万） |
| 点赞数 | 点赞数 |
| 评论数 | 评论数 |
| 分享数 | 分享数 |
| 收藏数 | 收藏数 |
| 发布时间 | 作品发布时间 |
| 抓取时间 | 数据抓取时间 |

### 注意事项
- 配置环节的对话**不占用** `scrape_post` 的使用次数计数
- 配置完成后，每次抓取成功会自动推送，无需额外操作
- 推送失败不影响核心抓取功能，仅打印警告

## 备选方案：DrissionPage 浏览器降级

当内置 browser 工具不可用、或 browser_navigate/browser_evaluate 执行失败时，可使用 DrissionPage 作为备选浏览器方案。DrissionPage 是纯 Python 浏览器自动化库，API 简洁，抗检测能力较强。

### 安装

```bash
pip install DrissionPage
```

注意：需要系统安装 Chromium 内核浏览器（Chrome 或 Edge）。Linux 无界面环境需额外安装 `chromium-browser`。

### 视频号 DrissionPage 降级（实测通过）

```python
from DrissionPage import ChromiumPage, ChromiumOptions

# 无头模式（服务器环境）
co = ChromiumOptions().headless(True)
page = ChromiumPage(co)

# 有界面模式（本地环境）
# page = ChromiumPage()

page.get('https://weixin.qq.com/sph/ASywao2nB1')
page.wait.doc_loaded()

# 注意: run_js() 执行匿名函数时必须用 return (...) 包裹
data = page.run_js('''
    return (() => {
        const r = {};
        const descEl = document.querySelector('.feed-desc-wrap');
        if (descEl) r.description = descEl.textContent?.trim();
        const locEl = document.querySelector('.feed-location-wrap');
        if (locEl) r.location = locEl.textContent?.trim();
        const timeEl = document.querySelector('.feed-create-time-wrap');
        if (timeEl) r.publish_time = timeEl.textContent?.trim();
        const authorEl = document.querySelector('.author-operate-container .clickable-area');
        if (authorEl) r.author = authorEl.textContent?.trim();
        const items = document.querySelectorAll('.operate-item');
        const icons = Array.from(items).map(el => {
            const text = el.querySelector('.operate-item-text')?.textContent?.trim();
            return text;
        });
        if (icons[0]) r.likes = parseInt(icons[0]) || 0;
        if (icons[1]) r.shares = parseInt(icons[1]) || 0;
        if (icons[2]) r.collects = parseInt(icons[2]) || 0;
        if (icons[3]) r.comments = parseInt(icons[3]) || 0;
        const vp = document.querySelector('.video-player');
        if (vp) r.cover_url = vp.src;
        return r;
    })()
''')

print(data)  # {'author': 'xxx', 'description': 'xxx', 'likes': 2, ...}
page.quit()
```

### 小红书 DrissionPage 降级（xsec_token 过期时备选）

```python
from DrissionPage import ChromiumPage

page = ChromiumPage()
page.get('https://www.xiaohongshu.com/explore/xxxxx?xsec_token=TOKEN')
page.wait.doc_loaded()

data = page.run_js('''
    return (() => {
        const r = {};
        try {
            const state = window.__INITIAL_STATE__;
            const noteMap = state?.note?.noteDetailMap;
            if (noteMap) {
                for (const nid of Object.keys(noteMap)) {
                    const note = noteMap[nid]?.note;
                    if (note && (note.title || note.desc)) {
                        const inter = note.interactInfo || {};
                        const user = note.user || {};
                        r.title = note.title || note.desc?.substring(0, 50);
                        r.author = user.nickname;
                        r.likes = inter.likedCount;
                        r.collects = inter.collectedCount;
                        r.comments = inter.commentCount;
                        r.shares = inter.shareCount;
                        break;
                    }
                }
            }
        } catch(e) {}
        return r;
    })()
''')

print(data)
page.quit()
```

### DrissionPage 关键注意事项
- `page.run_js()` 执行匿名函数**必须用 `return (...)` 包裹**，否则无法获取返回值
- 无头模式下视频号可能需要设置 `--headless=new` 和中文字体
- DrissionPage 无 WebDriver 特征，抗检测优于 Selenium
- 适合 Python 环境，其他语言环境请使用内置 browser 工具

## 输出字段

| 字段 | 说明 |
|------|------|
| platform | 平台名称 |
| title | 作品标题 |
| author | 作者昵称 |
| description | 文案/描述 |
| tags | 标签列表 |
| views | 播放量（B站/快手） |
| likes | 点赞数 |
| comments | 评论数 |
| shares | 分享数 |
| collects | 收藏数 |
| coins | 投币数（B站） |
| favorites | 作者收藏（快手） |
| danmaku | 弹幕数（B站） |
| duration | 时长（秒） |
| publish_time | 发布时间 |
| cover_url | 封面图URL |
| status | success/partial/error |
| strategy_used | 使用的抓取策略 |
