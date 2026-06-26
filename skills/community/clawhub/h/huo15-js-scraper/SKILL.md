---
name: huo15-js-scraper
description: JavaScript渲染网站抓取工具。当需要抓取JS渲染的页面（如企微文档、Vue/React SPA）、企查查企业数据获取）、绕过反爬、或者普通curl/wget/web_fetch无法获取内容的网站时使用此技能。支持Playwright和scrapling双引擎自动切换。
identifier: huo15-js-scraper
version: 1.2.1
author: 贾维斯
category: web-scraping
---

# huo15-js-scraper

JavaScript渲染网站抓取技能，支持Playwright和scrapling双引擎。

## 快速使用

```bash
# 基本用法（自动选择引擎）
python3 ~/.openclaw/workspace/skills/huo15-js-scraper/scripts/scrape.py <URL>

# 指定选择器
python3 ~/.openclaw/workspace/skills/huo15-js-scraper/scripts/scrape.py <URL> --selector ".content"

# 输出JSON
python3 ~/.openclaw/workspace/skills/huo15-js-scraper/scripts/scrape.py <URL> --output json

# 强制使用scrapling引擎
python3 ~/.openclaw/workspace/skills/huo15-js-scraper/scripts/scrape.py <URL> --engine scrapling
```

## 引擎选择策略

| 场景 | 推荐引擎 |
|------|---------|
| 企微文档 / 微信相关 | Playwright |
| Cloudflare保护站 | scrapling (stealth) |
| Vue/React SPA | Playwright |
| 简单静态页 | scrapling (basic) |
| 未知站 | Playwright（更稳定） |

## Python API

```python
from huo15_js_scraper import scrape

# 方式1：自动选择（推荐）
result = scrape('https://example.com')
print(result['content'])

# 方式2：强制Playwright
result = scrape('https://developer.work.weixin.qq.com/document/path/91756', engine='playwright')
```

## 企业微信文档知识库

已构建完整的企微官方文档知识库，位于：
`~/workspace/knowledge-base/企业微信文档/`

### 知识库结构

```
企业微信文档/
├── README.md (索引)
├── 01-快速入门/      - 开发前必读
├── 02-服务端API/     - 通讯录、消息、客户联系、企业支付...
├── 03-客户端API/     - 小程序API、JS-SDK
├── 04-工具资源/       - WeUI、错误码、频率限制
└── 99-附录/          - FAQ、更新日志
```

### 更新企微文档知识库

```bash
# 列出所有可抓取文档
python3 ~/.openclaw/workspace/skills/huo15-js-scraper/scripts/wecom_docs_scraper.py --list

# 抓取单个文档
python3 ~/.openclaw/workspace/skills/huo15-js-scraper/scripts/wecom_docs_scraper.py --path-id 90556 --category "01-快速入门" --title "快速入门"

# 批量抓取（更新全部52个文档）
python3 ~/.openclaw/workspace/skills/huo15-js-scraper/scripts/wecom_docs_scraper.py --all
```

### 核心文档

| 文档 | 路径ID | 说明 |
|------|--------|------|
| 快速入门 | 90556 | 开发前必读 |
| 获取access_token | 91039 | API认证基础 |
| 发送应用消息 | 90235 | 消息推送核心 |
| 创建成员 | 90195 | 通讯录管理 |
| 客户联系概述 | 92109 | 客户管理基础 |
| JS-SDK签名算法 | 90506 | 前端开发必备 |

## 企查查企业数据

企查查（qcc.com）企业信息查询，支持两种方式：
1. **✅ 推荐：MCP方式**（官方API，稳定可靠）
2. **备用：直接抓取**（需要账号登录，有反爬限制）

---

### 推荐方案：企查查MCP（官方API）

企查查提供官方MCP服务，支持 OpenClaw，已封装20+企业查询 SKILL。

**数据规模：**
- 3.65亿+ 市场主体
- 2.5亿+ 司法诉讼
- 2.1亿+ 知识产权
- 1.7亿+ 招投标

**MCP Servers（4个）：**

| Server | 别名 | 主要能力 |
|--------|------|---------|
| qcc-company | 企业基座 | 工商登记、股权结构 |
| qcc-risk | 风控大脑 | 34项风险扫描工具 |
| qcc-ipr | 知产引擎 | 专利、商标、软著 |
| qcc-operation | 经营罗盘 | 招投标、资质、舆情 |

**安装步骤：**

```bash
# 1. 注册获取API Key
# 访问 https://agent.qcc.com 注册

# 2. 添加到OpenClaw配置
# 在OpenClaw插件配置中添加企查查MCP服务器

# MCP接入地址: https://agent.qcc.com/mcp
# 需要配置 API Key 认证
```

**预置 SKILL（发送消息给AI即可加载）：**

```
请加载并使用这个 SKILL：https://github.com/duhu2000/financial-services-qcc
```

**SKILL命令示例：**

```bash
# KYB企业核验（~30秒）
/kyb-verification-qcc 华为技术有限公司

# IC Memo投资备忘录（~30秒）
/ic-memo-qcc 宁德时代 --round Series-B

# 企业画像速览（~3分钟）
/strip-profile-qcc 美团平台有限公司

# 知识产权尽调
/ip-due-diligence-qcc 企业名称 --peer 竞品

# 供应链风险评估
/supply-chain-risk-qcc 企业名称 --tier 1

# 关联方穿透
/related-party-qcc 企业名称 --depth 5
```

**输出格式：** 支持 `.md` / `.docx` / `.pptx`

---

### 备用方案：直接抓取

如无法使用MCP，可使用直接抓取方式（需要企查查账号）。

#### 安装依赖

```bash
pip3 install playwright --break-system-packages
playwright install chromium
```

#### 登录（首次使用）

```bash
# 生成二维码截图，扫码登录
python3 ~/.openclaw/workspace/skills/huo15-js-scraper/scripts/qichacha_scraper.py --login
```

> 登录后Cookie自动保存到 `~/.cache/huo15-js-scraper/qichacha_cookies.json`

#### 搜索企业

```bash
# 搜索企业
python3 ~/.openclaw/workspace/skills/huo15-js-scraper/scripts/qichacha_scraper.py --search "腾讯" --limit 10

# 输出JSON
python3 ~/.openclaw/workspace/skills/huo15-js-scraper/scripts/qichacha_scraper.py --search "腾讯" --output json
```

#### 企业详情

```bash
# 获取企业详细信息（部分需要VIP）
python3 ~/.openclaw/workspace/skills/huo15-js-scraper/scripts/qichacha_scraper.py --company "https://www.qcc.com/firm/xxxxx.html"
```

#### 返回信息示例

**搜索结果（无需登录可查看基础信息）：**
- 公司名称
- 企业状态（开业/存续/吊销）
- 行业分类
- 注册资本
- 法定代表人

**详细信息（可能需要VIP）：**
- 工商信息
- 股东信息
- 年报数据
- 风险信息

#### 注意事项

- 企查查搜索功能需要登录才能访问
- 详细信息（如年报、股东）需要VIP账号
- Cookie有效期约7天，过期需重新登录
- 建议设置 `--wait 5` 等待页面渲染

## 常见问题

### Q: 企微文档怎么抓？
```bash
python3 ~/.openclaw/workspace/skills/huo15-js-scraper/scripts/scrape.py \
  "https://developer.work.weixin.qq.com/document/path/91756" \
  --wait 5
```

### Q: 提示playwright未安装？
```bash
pip3 install playwright --break-system-packages
playwright install chromium
```

### Q: scrapling安装？
```bash
pip3 install "scrapling[all]" --break-system-packages
scrapling install
```

### Q: 内容为空或获取到跳转页面？
增加 `--wait` 时间，让JS有更多时间渲染：
```bash
python3 ...scrape.py <URL> --wait 5
```

## 依赖安装

```bash
# Playwright（主引擎）
pip3 install playwright --break-system-packages
playwright install chromium

# scrapling（降级引擎）
pip3 install "scrapling[all]" --break-system-packages
scrapling install
```

## 工作原理

1. 优先使用 Playwright（chromium headless）加载页面，等待networkidle
2. 等待指定时间让JS渲染完成
3. 通过CSS选择器提取内容
4. 如果Playwright失败，自动降级到scrapling
