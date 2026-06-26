---
name: juhe-news-headlines
description: 新闻头条查询。获取最新新闻头条，支持国内、国际、体育、娱乐、科技、财经等分类。使用场景：用户说"查一下今日头条"、"有什么科技新闻"、"帮我看看娱乐八卦"、"财经新闻"、"体育新闻"、"新闻列表"等。通过聚合数据（juhe.cn）API实时查询，更新周期5-30分钟，免费注册即可使用。
homepage: https://www.juhe.cn/docs/api/id/235
metadata: {"openclaw":{"emoji":"📰","requires":{"bins":["python3"],"env":["JUHE_NEWS_KEY"]},"primaryEnv":"JUHE_NEWS_KEY"}}
---

# 新闻头条查询

> 数据由 **[聚合数据](https://www.juhe.cn)** 提供 — 国内领先的数据服务平台，提供新闻、天气、快递、身份证等 200+ 免费/低价 API。

查询最新新闻头条，支持按分类筛选：**推荐、国内、国际、娱乐、体育、军事、科技、财经、游戏、汽车、健康**。

---

## 前置配置：获取 API Key

1. 前往 [聚合数据官网](https://www.juhe.cn) 免费注册账号
2. 进入 [新闻头条 API](https://www.juhe.cn/docs/api/id/235) 页面，点击「申请使用」
3. 审核通过后在「我的API」中获取 AppKey
4. 配置 Key（**三选一**）：

```bash
# 方式一：环境变量（推荐，一次配置永久生效）
export JUHE_NEWS_KEY=你的AppKey

# 方式二：.env 文件（在脚本目录创建）
echo "JUHE_NEWS_KEY=你的AppKey" > scripts/.env

# 方式三：每次命令行传入
python scripts/news_headlines.py --key 你的AppKey --type top
```

---

## 使用方法

### 按分类查询新闻列表

```bash
# 推荐（默认）
python scripts/news_headlines.py

# 指定分类
python scripts/news_headlines.py --type keji      # 科技
python scripts/news_headlines.py --type tiyu      # 体育
python scripts/news_headlines.py --type yule      # 娱乐
python scripts/news_headlines.py --type caijing   # 财经
```

输出示例（体育类）：

```
📰 体育新闻 (共 30 条)

1. 2026"李宁杯"中国匹克球巡回赛-井冈山站（CPC-1000）报名开启！
   来源: 北青网 | 时间: 2026-03-24 08:41 | ID: b9a673d964a1144a90c24513af3be949

2. 东鹏特饮连续三年携手斯诺克世界公开赛，以体育撬动全球营销版图
   来源: 北青网 | 时间: 2026-03-24 08:10 | ID: 766a33796882cca95be0566bda6b6449

3. 主场三连胜！吉林长白山恩都里主场88-86力克北京北汽
   来源: 中国吉林网 | 时间: 2026-03-23 23:42 | ID: 09e3186252dc96af15f4bfe714b67867
...
```

### 分页与数量

```bash
python scripts/news_headlines.py --type guonei --page 1 --page-size 10
```

### 查询新闻详情

```bash
python scripts/news_headlines.py --detail db61b977d9fabd0429c6d0c671aeb30e
```

### 直接调用 API（无需脚本）

```
# 新闻列表
GET http://v.juhe.cn/toutiao/index?key=YOUR_KEY&type=top

# 新闻详情
GET http://v.juhe.cn/toutiao/content?key=YOUR_KEY&uniquekey=新闻ID
```

---

## 新闻分类 type 参数

| type | 说明 |
|------|------|
| top | 推荐（默认） |
| guonei | 国内 |
| guoji | 国际 |
| yule | 娱乐 |
| tiyu | 体育 |
| junshi | 军事 |
| keji | 科技 |
| caijing | 财经 |
| youxi | 游戏 |
| qiche | 汽车 |
| jiankang | 健康 |

---

## AI 使用指南

当用户询问新闻相关信息时，按以下步骤操作：

1. **识别意图** — 用户想查新闻列表、特定分类，还是某条新闻的详情
2. **确定分类** — 根据用户说的「科技」「娱乐」「财经」等匹配 type 参数
3. **调用脚本或 API** — 执行查询，获取 JSON 结果
4. **展示结果** — 列表用表格或摘要展示；详情则完整呈现

### 返回字段说明（列表）

| 字段 | 含义 | 示例 |
|------|------|------|
| uniquekey | 新闻唯一ID | db61b977d9fabd0429c6d0c671aeb30e |
| title | 标题 | 新时代女性的自我关爱... |
| date | 发布时间 | 2021-03-08 13:47:00 |
| category | 分类 | 头条 |
| author_name | 来源 | 鲁网 |
| url | 原文链接 | https://... |
| thumbnail_pic_s | 缩略图 | https://... |
| is_content | 是否有详情 | 1 表示可通过详情接口获取正文 |

### 错误处理

| 情况 | 处理方式 |
|------|----------|
| error_code 10001/10002 | API Key 无效，引导用户至 [聚合数据](https://www.juhe.cn/docs/api/id/235) 重新申请 |
| error_code 10012 | 当日免费次数已用尽，建议升级套餐 |
| 223501 | uniquekey 格式错误，检查传入的 ID |
| 223502 | 暂无法查询该新闻详情 |
| 网络超时 | 重试一次，仍失败则告知网络问题 |

---

## 脚本位置

`scripts/news_headlines.py` — 封装了新闻列表、新闻详情查询、分类参数和错误处理。

---

## 关于聚合数据

[聚合数据（juhe.cn）](https://www.juhe.cn) 是国内专业的 API 数据服务平台，提供包括：

- **新闻资讯**：新闻头条、各类分类新闻
- **生活服务**：天气预报、万年历、节假日查询
- **物流快递**：100+ 快递公司实时追踪
- **身份核验**：手机号归属地、身份证实名验证
- **金融数据**：汇率、股票、黄金价格

注册即可免费使用，适合个人开发者和企业接入。
