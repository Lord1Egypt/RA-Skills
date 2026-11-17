---
name: juejin-publisher-pro
description: 掘金全自动发布 + 知乎 CDP 半自动。login 扫码抓 Cookie，publish 一条龙：建稿（分类/双标签/摘要）→ PIL 生成封面并上传 → 挂专栏 → 发布 → 审核状态自检；column-new/column-cover 管理专栏。全部接口口径经真实账号逆向实测（2026-09），含机审驳回避坑。
license: MIT
---

# juejin-publisher-pro 操作手册

零框架依赖（Python 标准库 + websockets + pillow），真机全链路验证：本 skill 的每个接口口径都用真实账号发布过文章并过审。

## 首次配置

1. 把 `scripts/publish.py` 复制到写作项目根目录，`uv add websockets pillow`
2. `uv run publish.py login` ——拉起独立 profile 的 Chrome/Edge：扫码登掘金（自动抓 Cookie 存 `.juejin.env`，实测有效期约 1 年）、顺手扫知乎
3. `uv run publish.py columns --use <id>` 设默认专栏（可选）

## 文章格式（frontmatter 硬性要求）

```yaml
title_zhihu: 知乎版标题
title_juejin: 掘金版标题
description: 50~100 字摘要（掘金接口硬限制，不足拒绝、超限截断）
category_id: "6809637773935378440"   # 人工智能；速查表见 references/category_ids.md
tags: "AI,职业发展"                    # 掘金上限 2 个，自动映射（职业发展→程序员 等）
```

正文 Markdown；**所有 HTML 注释自动剥离**（内部笔记不外发）；封面不给就 PIL 自动生成 192×128。

## 命令速查

| 命令 | 用途 |
|---|---|
| `login` | 扫码抓 Cookie（掘金+知乎），记录设备 uuid |
| `whoami` | 验 Cookie、记 user_id |
| `preview 文章.md` | 离线校验：摘要长度/checklist 剥离/标签映射/URL 门禁 |
| `tags 关键词` | 搜掘金标签 ID |
| `columns` / `--use <id>` | 专栏列表 / 设默认 |
| `column-new 标题` | 新建专栏（纯 API），`--intro 简介` `--use` 建完设为默认 |
| `column-cover` | 专栏上 PIL 封面（16:9），`--column <id>` 指定、`--subtitle` 副标题 |
| `draft 文章.md` | 建草稿（分类+双标签+摘要+自动封面） |
| `publish 文章.md` | 全自动：建稿→传封面→挂专栏→发布→报审核状态（audit_guard 预警招聘词×钱数） |
| `status <article_id>` | audit_status -1=已驳回（此时 status 仍是 0，别误读）；status 0=审核中（前台 404 属正常），1/2=已上线 |
| `zhihu 文章.md [--auto]` | CDP 开知乎写文章页，自动填标题+注入正文；`--auto` 连发布也自动点（一键直发，创作声明沿用上次设置） |
| `cover 文章.md` | 手动补封面 |
| `cleanup` | 关闭 CDP 浏览器堆积的标签（防长期运行卡死；`--all` 连知乎写作页一起清） |

## 踩坑速查（逆向实测，2026-09）

- **请求必须带 `?aid=2608&uuid=<真实设备uuid>`**：随机 uuid 被 WAF 掐 TLS（SSL UNEXPECTED_EOF，重试无效）；login 自动收割真实值
- **建草稿响应 `article_id` 恒为 `"0"`**（未发布语义），真实草稿 ID 在 `data.id`
- **每篇最多 2 个标签**（err 4031）；标签搜索 = `tag_api/v1/query_tag_list {key_word}`，名字嵌在 `tag.tag_name`
- **发布成功 ≠ 上线**：`status 0`=审核中，前台 404、专栏对外空属正常；1/2 才可见
- **机审驳回重灾区「推广类」**：正文含招聘平台 URL/域名字符串+薪资数字会被按招聘广告驳回。url_guard 会警告；修法=URL 降为纯文字（「在 XX 平台搜 YY 可复核」），删旧文重发（实测有效）
- **标题级关键词同样触发**（2026-09-17 实测）：掘金标题含「高薪＋养不住」组合被按推广类驳回（正文干净也拦）——标题用金句钩子
- **正文「招聘语汇×钱数」同段落也是雷**（辩七实测）：正文「开出高薪招」紧挨营收数字同样被驳——改写参考：高薪招→真金白银请、招聘预算→预算、求职者→看机会的读者。publish 的 audit_guard 会预警
- **被驳后别反复重发相似内容**（辩七四连驳回实测）：相似内容重发会被越来越快地拒（第 4 次秒拒）且伤账号信用——要改就实质重写（换标题+全文重措辞+结构重排），隔天错峰再发
- **点名上市公司＋负面财务数字慎写**（推断雷区）：唱空具体公司的亏损/市值/撤材料数字易触发财经类审核，匿名化（「CV 四小龙之一的某算法上市公司」）保留数字与出处更稳
- **审核状态先看 audit_status 再看 status**：驳回文章 status 仍是 0（审核中假象），audit_status=-1 才是驳回
- **专栏 API**：`column/publish` 无 column_id=新建（data 返回新 id）、带 column_id=更新；`column/delete` 删除。专栏头图 16:9，column-cover 按 1280×720 生成
- **知乎发布可一键直发**（2026-09-18 实测）：知乎记住此前的创作声明等设置，点「发布」不弹设置弹窗直接成功——`zhihu --auto` 即全自动；新环境首次发布可能弹创作声明弹窗，工具会检测并提示人工补选。封面预览探针在 /edit 态常误报，以浏览器实际显示为准
- 接口间隔 ≥2.5 秒防风控（内置）；401/403=Cookie 失效重跑 login

## 发布节奏（用户自担）

**数量与间隔不做任何限制**（2026-09-19 用户决策：出问题由用户自己解决）。两条事实供参考、不构成约束：批量发布时各篇曝光会互相稀释；平台（尤其知乎）有服务端频率风控，过快可能被静默挂起（「发布中...」卡住）或触发 24h 限制。

## 定时发布模式（Windows + Python）

无人值守逐日发布：`scripts/auto_publish.py` + `auto_publish.bat` 配 Windows 计划任务（`schtasks /create /tn Blog_am /tr "...bat" /sc daily /st 09:15`；Git Bash 加 `MSYS_NO_PATHCONV=1`）。驱动自然排序 posts/*.md、按掘金标题去重、每日上限/最小间隔护栏、队列发完自动注销任务、`--only` 支持一次性补发。坑：Claude 的 CronCreate 只在 REPL 空闲时触发（不可靠）；**驱动无干跑，跑一次真发一次**。

## 伦理边界

仅供个人内容发布自动化。接口为抓包逆向所得、无官方文档，平台可能变更；控制频率，勿批量营销号式发布。
