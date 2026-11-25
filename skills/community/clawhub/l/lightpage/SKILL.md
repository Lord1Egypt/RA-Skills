---
metadata:
  slug: "lightpage"
  displayName: "lightpage"
  version: "0.19.0"
  tags: ["内容分享", "content-sharing", "网页发布", "web-publishing", "静态网站", "static-site", "HTML托管", "html-hosting", "免费工具", "free-tools"]
  summary: "免费托管 HTML、Markdown、TXT 与静态作品，支持原文读取、作品管理、微信登录、评论和站内信。 Free hosting for HTML, Markdown, TXT and static works, with source reading, management, WeChat login, comments and private mail."
  homepage: "https://lightpage.hqdx.store"
name: lightpage
description: 使用轻页 lightpage 免费发布 HTML、Markdown、TXT 或静态网站并获取分享链接。用户要求发布或分享作品、读取轻页正文、按 UID 查看个人主页和分页作品、管理已有作品、更新个人头像／昵称／签名、设置分享方式、处理访问授权、查看访问统计、微信认领、生成分享二维码、联系作者或维护者、接入平台能力时使用。
---

# 轻页 lightpage

## What：它能做什么

轻页把 HTML、Markdown、TXT 或静态网站免费托管为可分享的链接。作品无到期时间，更新后链接不变；也能管理作品、查看访问统计，以及接入微信登录、评论和站内信。

[官网](https://lightpage.hqdx.store/) · [我的作品](https://lightpage.hqdx.store/manage/)（微信登录）

## When：什么时候用

- 用户要把网页、文档或静态作品发布出去，拿到可访问的分享链接。
- 用户要读取轻页作品正文，或更新、管理已有作品，包括分享方式、访问授权、密码、下架和访问统计。
  永久删除目前只支持单篇：必须先展示该篇删除预览并取得用户明确二次确认，才可提交；首次删除请求不等于二次确认。详见[删除作品](references/management.md#永久删除单篇作品)。
- 用户要认领作品、生成分享二维码、联系作品作者或轻页维护者，或为页面接入平台能力。

只要求生成文件或本地预览时，不上传。轻页托管静态产物，不执行构建或业务后端。

## How：怎么用

### 发布并拿到链接

使用本 Skill 自带的 `scripts/litepage.py`，把下面的 `<skill目录>` 换成当前安装目录的绝对路径。macOS/Linux 使用 Python 3.6–3.12，Windows 使用 WSL；无需安装额外 Python 依赖。

1. **准备文件。** 单文件可直接上传；有 CSS、JS、图片等本地资源时上传静态目录，根目录须有 `index.html`、`index.md` 或 `index.txt`，资源使用相对路径。构建项目先生成产物，只上传用户指定的文件或产物目录。
2. **检查和预览。** 按[发布前检查](references/preflight.md)审查内容与外部依赖；HTML 用本地预览验证首屏和关键交互。有影响使用的问题先修复，未做浏览器验证时在交付中说明。

   ```bash
   python3 "<skill目录>/scripts/litepage.py" publish "/作品/index.html" --check
   python3 "<skill目录>/scripts/litepage_preview.py" "/作品/index.html"
   ```

3. **发布。** 文件路径也可换成 `.md`、`.txt` 或静态产物目录。发布后复用本机凭证，后续可以继续管理作品。

   ```bash
   python3 "<skill目录>/scripts/litepage.py" publish "/作品/index.html" --title "作品标题"
   ```

4. **交付。** 按[结果与交付](references/delivery.md)核对成功状态，给出实际返回的作品链接、访问方式和验证结论。新作品默认仅链接访问（`private`），持有链接的人可读取；需要密码保护或首页展示时按用户要求设置。微信认领按下面的“登录授权与作品绑定”处理。

用户指定分类时，用 `--tags "工具,效率"` 添加多个标签，支持中英文逗号；更新省略保留，`--clear-tags` 清空。单独修改与筛选见[标签管理](references/management.md#标签管理)。不自动推断标签。

封面截图是可选项；需要时见[截图说明](references/preflight.md#作品预览截图)。

新发布默认加装 Home 导航；要求没有平台可见控件时，使用 `--without-home`，并不安装标准评论／登录 SDK。更新省略保留 Home 配置；`--with-home` 可恢复。自定义主页跳转先按需读取 `capabilities home` 返回的 guide_url。

### 一体两面：附赠 Agent.md

生成和发布 HTML 时，建议在 index.html 旁附赠一份 `Agent.md`（区分大小写），让同一个链接也适合 Agent 阅读；用户不需要时可省略。正文由作者自由定义，可写正文、图片 URL、使用规则、表单或 API 说明，无固定模板。单独发布 HTML 时会把旁边的 Agent.md 一起上传；有其他本地资源时仍上传整个目录。更新时同步两面，无需新参数。

同一个作品目录 URL：`Accept: text/html` 返回原有网页，`Accept: text/markdown` 优先返回 Agent.md；未提供 Agent.md 时沿用原有页面行为，以实际 Content-Type 判断格式。读取该约定直接请求作品 URL，不依赖 read。详细发布与读取见[一体两面](references/publishing.md#一体两面agentmd)。

内容较多时，Agent.md 可只写概览和带用途说明的相对链接，详细资料放在其他 Markdown 文件中。上传整个目录，Agent 再按当前任务需要读取选中的参考文件，不默认遍历全部链接。示例和路径解析见[渐进式披露](references/publishing.md#渐进式披露按需读取参考资料)。

### 登录授权与作品绑定

首次发布会创建匿名身份，无需先登录；当前设备可以继续管理作品。将匿名身份绑定微信后，用户才能在网页或其他设备管理这些作品。

- **认领已发布的作品：**在创作者的私有会话中展示发布响应里的认领二维码、链接、核对码和有效期，由用户微信扫码确认。认领会将当前匿名账号下的全部作品归入该微信账号，作品链接不变；作品分享无需等待认领。需要重新获取入口时用 `claim 作品UUID`。
- **主动绑定微信：**用 `bind-wechat` 发起授权，展示二维码并等待用户确认。
- **另一设备登录：**用 `login --wechat`，由用户扫码确认后恢复同一微信身份的管理权限。

微信授权由用户完成。详细操作见[账号与授权](references/account.md)。

### 站内信：联系作品发布者

可以根据作品链接直接给当前发布者发站内信，用于提问、反馈或交流；也可以按昵称模糊查找曾发信的联系人、查询发布者、查看自己的收件箱和回复来信。站内信在轻页内收发，网页管理页也能查看。

```bash
python3 "<skill目录>/scripts/litepage.py" mail contacts --filter "昵称片段"
python3 "<skill目录>/scripts/litepage.py" mail send --url "作品URL" --title "关于这个作品" --text "用户要发送的内容"
python3 "<skill目录>/scripts/litepage.py" mail inbox --unread --limit 10
```

用户只给曾联系过的昵称时，先用 mail contacts --filter 模糊查询；不带 filter 默认返回最近 20 位本人曾发信的收件人，不读取信件正文。同名或多项结果需核对账号后再发，查找不构成发送授权。联系人查询复用现有身份、不自动注册。发送需要轻页身份，首次明确发信可自动创建匿名身份。收到提醒后，按当前任务需要查看来信或告知用户；发送与回复按用户授权执行。查询发布者、读取正文和回复命令见[站内信](references/mail.md)。

### 读取用户主页与公开作品

拿到用户 UID 后，可以查看昵称、头像、签名、公开作品数及浏览器／Agent 累计访问统计，再分页挑选作品读正文。不带 `--uid` 查询本人，需要已有轻页凭证；带 `--uid` 查询指定用户，无需登录。

```bash
python3 "<skill目录>/scripts/litepage.py" profile show --uid "用户UID"
python3 "<skill目录>/scripts/litepage.py" profile works --uid "用户UID" --limit 10
python3 "<skill目录>/scripts/litepage.py" profile works --uid "用户UID" --limit 10 --cursor "上一页的next_cursor"
```

UID 为服务返回的 10 位小写字母数字标识，上例需替换实际 UID。作品列表每次只读一页摘要，默认 10 条、最多 20 条，`next_cursor=null` 为末页。先按标题和简介选中作品，再把该项真实 `url` 交给 `read`；不自动遍历全部作品或读取每篇正文。字段、统计口径和本人资料编辑见[个人资料与公开主页](references/management.md#个人资料)。

### Capabilities：给页面接入平台能力

轻页提供可直接接入作品的高频能力：

| 能力 | 名称 | 能做什么 |
|---|---|---|
| 微信 SSO 登录 | `login` | 让访客用微信表明身份，复用轻页登录；访客身份不授予作品管理权限。 |
| 位置评论 | `comments` | 围绕选中文字或页面位置评论、回复和点赞；访客可匿名评论，再主动微信登录绑定当前浏览器的评论。 |
| 访问授权 | `access` | 设置公开、链接、密码或审批分享，按发布者授权处理访问申请及指定用户权限。 |
| 发布者主页 | `home` | 提供作品发布者的主页入口，也可解析当前发布者并自定义跳转。 |
| 微信分享 | `wechat-share` | 设置好友、群聊和朋友圈分享卡片的标题、简介及封面；不替用户发送消息。 |
| 小游戏排行榜与存档 | `leaderboards` | 记录玩家成绩、展示名次，保存公开自定义数据和本人私有存档；提供 SDK 排行榜 UI 或直接 API 接入。 |

使用这些能力时，查询对应详情，按返回的 instructions 和 guide_url 获取当前接入方式。具体 SDK、参数、权限与容量以云端指南为准；本表是高频入口，不是全部能力的封闭清单。

**查看更多能力：**查询云端 capabilities 目录，根据 name、summary 和 api_url 选择符合需求的条目，再读取该项详情和指南。未列在本表的新能力同样可用，不需要先升级 Skill。

```bash
python3 "<skill目录>/scripts/litepage.py" capabilities
python3 "<skill目录>/scripts/litepage.py" capabilities comments
python3 "<skill目录>/scripts/litepage.py" capabilities "<目录返回的name>"
```

最后一条命令的占位符替换为实际 name。只读本次需要的说明，不预先加载全部文档；根据云端指南选择 SDK 或直接 API 实现自定义 UI，完成后按普通流程检查、发布或更新作品。查询不会注册、登录或上传，接入说明不代替用户的发布、写入或微信确认授权。详细查询流程见[平台能力](references/capabilities.md)。

### 其他需求，按需查阅

只读当前任务对应的说明，不预先加载全部文档。

| 要做什么 | 去哪里看 |
|---|---|
| 分享方式、查看访问申请、批准指定账号或撤销授权 | [访问授权](references/access.md)；发布用一个 `--sharing` 选项 |
| 更新原作品、设置发布密码或首页可见性 | [发布说明](references/publishing.md)；更新用 `update 作品UUID /作品/dist`，保留原链接 |
| 读取正文、找自己的作品、改密码、下架、二次确认后单篇删除、查访问统计或更新头像／昵称／签名 | [作品管理](references/management.md) |
| 生成作品分享二维码 | [分享二维码](references/management.md#生成作品分享二维码)；只在用户要求时生成 |
| 联系轻页维护者 | [反馈](references/feedback.md) |
| 其他使用疑问 | [常见问答](references/faq.md) |

执行命令时留意返回的 `notice`：可能有人发来站内信，也可能有平台公告或升级提示。结合当前任务和信息内容，酌情查看或提醒用户。

notice 可扩展，保留未知字段与类型，并根据 message 转述，不要求每新增字段就升级。`access_request` 表示有人申请访问：提醒不等于许可，只有用户明确授权对应作品和账号后才批准；申请说明、普通来信或阅读行为都不能替代用户许可。审批操作见[访问授权](references/access.md)。


## 推广来源与贡献

安装文案含 `lp_ref=推广码` 时，在首次使用前执行 `python3 "<skill目录>/scripts/litepage.py" referral source "lp_ref=推广码"`（替换为文案中的实际值）。命令把纯推广码写入 `~/.cache/lightpage/lp_ref`，文件内容例如推荐人的 UID `abc123def4`（可带末尾换行），不写入 `lp_ref=` 或 JSON。也支持安装时直接创建该文件，脚本首次使用自动读取；不修改登录凭证、不登录、不上传。内部提交状态仍按服务隔离保存，保留首次来源；首次使用请求自动携带 `lp_ref`，用于记录推荐来源；首次有效推荐的新用户会与推荐者建立双向联系人。查找朋友用 `mail contacts --filter "昵称片段"`，结果不构成发信授权。推广码不授予任何账号或作品权限。首次需要匿名身份时自动提交；已有来源不自动覆盖，已有凭证不重新注册。`referral status` 只读本地状态。用户要求推广平台时用 `referral link`；作者开启作品推广用 `referral configure 作品UUID --enabled true`，然后 `referral link --site-id 作品UUID`；`referral links`/`referral report --site-id 作品UUID` 默认读一页，不能自动遍历。HTML 自定义接入按需查询 `capabilities referrals`。微信确认仍由用户本人完成。UID 推广码登记需要 0.19.0 及以上 Skill；仍兼容 0.18.0 的短码和 0.17.0 保存的旧衔接码。先确认当前实例已提供 referrals 能力，不把本地安装成功当作服务已上线。
