# news-to-markdown Skill

> 输入文章 URL，输出干净的 Markdown 正文 — 17 个平台专项优化，专为 AI Agent 设计

## 快速开始

### 推荐：固定版本 + launcher（无子进程、无版本漂移）

```bash
# 一次性安装
npm install -g news-to-markdown@3.3.1

# 之后通过 launcher 调用
node scripts/run.js convert --url "https://www.toutiao.com/article/123"
node scripts/run.js convert --url "https://mp.weixin.qq.com/s/xxx" --output article.md
node scripts/run.js convert --url "https://36kr.com/p/xxx" --download-images --output-dir ./article
```

`scripts/run.js` 解析已安装的固定版本 npm 包并通过 `require()` 在进程内运行，对参数做 allow-list 与长度/控制字符校验后注入到 CLI 的 `argv`，不调用 `npx`、不 fork 子进程、不进入 shell。

### 备选：`npx --yes`（一次性试用 / 隔离沙箱）

> ⚠️ `npx --yes news-to-markdown@^3.3.1` **每次调用都会从 npm 拉取范围内的最新版本**——无 lockfile、无完整性校验，存在供应链漂移面。仅建议在临时容器 / 沙箱里快速试用，常驻使用请走上面的 launcher 路径。

```bash
npx --yes news-to-markdown@^3.3.1 --url "https://www.toutiao.com/article/123"
```

### 与 browser-web-search 配合：搜索 → 提取正文

```bash
bws site toutiao/search "ai agent" --count 3
node scripts/run.js convert --url "https://www.toutiao.com/article/111"
```

## 专项优化平台（17 个）

| 平台 | 域名 |
|-----|------|
| **今日头条** | toutiao.com |
| **微信公众号** | mp.weixin.qq.com |
| **小红书** | xiaohongshu.com |
| **知乎** | zhihu.com |
| **36kr** | 36kr.com |
| **虎嗅** | huxiu.com |
| **华尔街见闻** | wallstreetcn.com |
| **澎湃新闻** | thepaper.cn |
| **InfoQ** | infoq.cn / infoq.com |
| **Bilibili 专栏** | bilibili.com |
| **掘金** | juejin.cn |
| **CSDN** | csdn.net |
| **博客园** | cnblogs.com |
| **简书** | jianshu.com |
| **SegmentFault** | segmentfault.com |
| **开源中国** | oschina.net |
| **人人都是产品经理** | woshipm.com |

其余平台走通用算法（Mozilla Readability），大多数文章均可正常提取。

## 参数速查

| 参数 | 说明 |
|-----|------|
| `--url` | 文章 URL（必填） |
| `--output` | 输出文件路径 |
| `--download-images` | 下载图片到本地 |
| `--output-dir` | 图片输出目录 |
| `--no-metadata` | 只要正文，不含标题/作者/时间 |
| `--selector` | 自定义内容区域 CSS 选择器 |
| `--noise` | 移除指定元素（逗号分隔） |
| `--verbose` | 详细日志 |

## 环境要求

- Node.js >= 18.0.0
- `npm install -g news-to-markdown@3.3.1`（推荐路径必需；`npx` 备选路径无需）
- 可选：`npx playwright install chromium`（动态页面回退；首次会从 CDN 下载 Chromium 二进制，建议在沙箱/容器中执行）

## 文档

详细使用说明：[SKILL.md](./SKILL.md)

## 链接

- [news-to-markdown GitHub](https://github.com/sipingme/news-to-markdown)
- [npm 包](https://www.npmjs.com/package/news-to-markdown)

## License

MIT
