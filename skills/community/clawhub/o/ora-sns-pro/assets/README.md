# Ora社媒主页搜索专家 Skill

## 📖 简介

一款面向外贸和商务场景的社交媒体数据搜索工具。支持两种搜索模式：
- **关键词搜索**：按产品/行业关键词在 Facebook、LinkedIn、Twitter/X、Instagram 平台上搜索企业和联系人数据
- **域名/企业反查**：通过企业名称或域名反查其在四大社媒平台上的官方账号

帮助用户快速找到潜在客户、合作伙伴或竞品信息。

## ✨ 核心功能

| 功能 | 说明 | 典型场景 |
|------|------|----------|
| 🔍 关键词搜索 | 按关键词 + 社媒平台搜索，每平台最多 20 条 | "搜索 LED 的 LinkedIn" |
| 🏢 企业反查 | 按企业名称反查社媒账号，最多 5 条 | "查 Loyola Medicine 的 Facebook" |
| 🌐 域名反查 | 按域名反查社媒账号，最多 5 条 | "查 armaiolo.it 的社媒" |
| 📊 批量查询 | 支持多个关键词/企业/域名批量搜索 | "查这 10 家公司的 LinkedIn" |

### 支持平台

| 平台 | API 参数 | 关键词搜索 | 域名反查 |
|------|----------|:---------:|:-------:|
| Facebook | `facebook` | ✅ | ✅ |
| LinkedIn | `linkedin` | ✅ | ✅ |
| Twitter/X | `twitter` | ✅ | ✅ |
| Instagram | `instagram` | ✅ | ✅ |

## 🚀 使用示例

### 关键词搜索
> "在 LinkedIn 上搜索 LED"
> "Facebook 搜一下 solar panel"
> "搜 furniture, lighting, decoration 三个关键词的 Instagram"

### 域名/企业反查
> "查一下 Loyola Medicine 的 LinkedIn"
> "armaiolo.it 这个域名的 Facebook 账号"
> "Apple 和 Microsoft 的 Twitter 主页"

## 🔧 配置说明

```json
{
  "skills": {
    "entries": {
      "ora-sns-pro": {
        "config": {
          "keyword_search_url": "https://api.topeasychina.com:9443/DomainData/api/skill/socialMediaQuery",
          "domain_search_url": "https://api.topeasychina.com:9443/DomainData/api/skill/socialMediaDomainQuery",
          "auth_token": "",
          "timeout": 30000,
          "payment_url": "https://www.oraskl.com/platform"
        }
      }
    }
  }
}
```

| 配置项 | 必填 | 说明 |
|--------|------|------|
| `keyword_search_url` | 是 | 关键词搜索接口（POST） |
| `domain_search_url` | 是 | 域名/企业反查接口（POST） |
| `auth_token` | 是 | 授权令牌，优先从 skills 目录下的 `OraAgent.key` 文件中取值 |
| `timeout` | 否 | 请求超时（毫秒），默认 30000 |
| `payment_url` | 否 | 付费升级链接 |

## 📊 返回数据字段

| 字段 | 说明 |
|------|------|
| `title` | 企业/主页名称 |
| `url` | 企业官网 URL |
| `social_media_url` | 社媒平台主页 URL |
| `description` | 企业简介/描述 |
| `keywords` | 业务关键词/标签 |
| `country_tag` | 所在国家代码 |

## 💰 额度机制

- **免费用户**：共 20 次查询额度，关键词搜索和域名反查共用
- **付费用户**：无总次数限制，可能有单日请求上限（次日 0 点重置）
- 每次调用任意查询接口扣减 1 次额度

## 🛠️ 技术架构

```
用户输入 → 参数提取 → 模式判定 → API调用 → 格式化输出
                ↓            ↓           ↓
         ora_sns_pro_handler.js → ora_sns_pro_api.js
                                         ├── POST socialMediaQuery（关键词）
                                         └── POST socialMediaDomainQuery（域名反查）
```

## 📦 文件结构

```
ora-sns-pro/
├── SKILL.md                    # 技能定义文件
├── manifest.json               # 发布清单
├── _meta.json                  # 元数据
├── .clawhub/
│   └── origin.json             # ClawHub 来源信息
├── assets/
│   └── README.md               # ClawHub 展示页
├── handlers/
│   └── ora_sns_pro_handler.js # 请求处理逻辑
└── tools/
    └── ora_sns_pro_api.js     # API 调用封装
```

## 📝 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 3.0.0 | 2026-05-29 | 重大重构：移除独立鉴权，新增双接口（关键词+域名反查），统一额度机制 |
| 2.1.0 | 2026-05-29 | 批量超额处理机制 |
| 2.0.0 | 2026-05-28 | 改为企业名称/域名反查模式 |
| 1.0.0 | 2026-05-27 | 初始发布 |
