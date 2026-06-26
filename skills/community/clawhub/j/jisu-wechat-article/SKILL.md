---
name: "Wechat Article Search"
description: 按关键词搜索公众号文章，返回标题、摘要、时间、账号与链接等。当用户说：搜一下微信公众号里关于 AI 的文章、找几篇讲理财的推文，或类似公众号文章检索时，使用本技能。
metadata: { "openclaw": { "emoji": "🔎", "requires": { "bins": ["python3"] } } }
---

# 微信公众号文章搜索（Wechat Article Search）

用于按关键词搜索公众号文章，快速拿到：

- 标题
- 摘要
- 发布时间
- 来源公众号
- 链接（可选解析真实微信文章链接）

## 输出格式要求（严格）

当用户要“结果展示”时，必须严格按以下 5 行输出每条结果，不要输出 JSON，不要增加其他字段名：

```text
标题：{title}
摘要：{summary}
发布时间：{publish_time}
来源公众号：{source_account}
链接：{detail_url_or_url_real_or_url}
```

规则：

- 每条结果固定 5 行，字段顺序固定，不可变更。
- 多条结果时，按上述格式重复输出，结果与结果之间空一行。
- 字段无值时统一填 `无`。
- `链接` 字段优先使用 `detail_url`；若无 `detail_url` 则使用 `url_real`；仍无则使用 `url`。

## 依赖

```bash
pip install requests beautifulsoup4
```

## 脚本路径

- `skills/jisu-wechat-article/search.py`

## 使用方式

### 1) 常规搜索

```bash
python3 skills/jisu-wechat-article/search.py "关键词"
```

### 2) 指定数量

```bash
python3 skills/jisu-wechat-article/search.py "关键词" -n 15
```

### 3) 保存到文件

```bash
python3 skills/jisu-wechat-article/search.py "关键词" -n 20 -o out/result.json
```

### 4) 解析真实链接（会额外请求）

```bash
python3 skills/jisu-wechat-article/search.py "关键词" -n 5 -r
```

### 5) 保留 antispider 风控链接（调试用）

```bash
python3 skills/jisu-wechat-article/search.py "关键词" -n 5 -r --keep-antispider
```

### 6) 抓取正文（详情）

```bash
python3 skills/jisu-wechat-article/search.py "极速数据入驻 ClawHub" -n 5 --fetch-content
```

可与 `-r` 组合：

```bash
python3 skills/jisu-wechat-article/search.py "极速数据入驻 ClawHub" -n 5 -r --fetch-content
```

### 7) 正文抓取限制说明（重要）

当前环境下，`--fetch-content` 常会被搜狗/微信风控拦截（`content_status=blocked`），导致拿不到正文。这是站点风控行为，不是技能报错。

推荐做法：

1. 先用本技能获取搜索结果，拿到 `detail_url`（或 `url`）。
2. 将该搜狗链接在浏览器中打开，完成跳转后获取真实微信文章链接（`https://mp.weixin.qq.com/...`）。
3. 再用真实微信链接查看正文内容。

结论：技能可稳定返回“标题/摘要/发布时间/来源公众号/链接”，正文抓取成功率受风控影响，不保证每次可用。

### 8) `content_status=blocked` 标准回复模板

当正文抓取被拦截时，按下面模板返回（可替换占位符）：

```text
当前无法直接抓取正文（命中风控），但已为你找到文章信息：
标题：{title}
摘要：{summary_or_无}
发布时间：{publish_time_or_无}
来源公众号：{source_account_or_无}
链接：{detail_url_or_url}

请将上述链接在浏览器中打开，跳转后复制真实微信文章链接（mp.weixin.qq.com），即可查看正文。
```

## 与 微信公众号管理套件 结合使用

`wechat-mp` 是公众号运营工具集，支持发文到草稿箱、草稿管理、评论管理、用户管理（含黑名单）和数据统计。

推荐组合流程：

1. 用本技能搜索公众号文章，拿到标题、摘要、发布时间、来源公众号和链接；
2. 基于搜索结果整理选题与文案；
3. 用 `wechat-mp` 将内容发布到公众号草稿，并继续做评论/用户/数据运营。

相关链接：

- wechat-mp（ClawHub）：<https://clawhub.ai/jisuapi/wechat-mp>

## 参数说明

- `query`：搜索关键词（必填）
- `-n, --num`：返回数量（默认 10，最大 50）
- `-o, --output`：输出 JSON 文件路径（可选）
- `-r, --resolve-url`：尝试解析微信文章真实链接（会额外请求每条结果）
- `--fetch-content`：尝试抓取文章正文文本（会额外请求每条结果）
- `--content-max-chars`：正文文本最大长度（默认 6000）
- `--ua`：自定义 User-Agent
- `--ua-rotate`：启用内置 User-Agent 轮换
- `--retries`：每个请求最大重试次数（默认 1）
- `--retry-delay`：重试间隔秒数（默认 0.3）
- `--keep-antispider`：保留 `antispider` 风控链接（默认不保留）
- `--timeout`：请求超时秒数（默认 15）

## 输出字段（items 每条）

- `title`：文章标题
- `url`：搜索结果中的文章链接（可能是中间跳转）
- `detail_url`：详情页链接（始终返回；优先真实链接，失败时回退到搜索链接）
- `summary`：摘要
- `publish_time`：发布时间（页面可提取则返回）
- `source_account`：来源公众号名称
- `url_real`：真实微信文章链接（仅 `-r` 时尝试返回）
- `resolve_status`：真实链接解析状态（仅 `-r` 时返回，`ok/blocked/empty`）
- `content_url`：用于抓取正文的文章链接（仅 `--fetch-content`）
- `content_title`：正文页标题（仅成功抓取时返回）
- `content_text`：正文文本（仅 `--fetch-content`）
- `content_status`：正文抓取状态（`ok/blocked/no_mp_url/fetch_error/parse_empty`）
- `content_error`：正文抓取失败原因（仅失败时）

## 注意事项

- 本技能是网页抓取工具，请遵守目标站点使用条款与 robots 规则。
- 过高频率调用可能触发风控或封禁。
- 若你需要更强安全边界，建议在受限网络环境中运行。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下 API：

- **生活常用**：IP 查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA 赛事数据，邮编查询，WHOIS 查询，识图工具，二维码生成识别，手机空号检测
- **交通出行**：VIN 车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN 识别
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令
- **位置服务**：基站查询，经纬度地址转换，坐标系转换

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在 API 详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

