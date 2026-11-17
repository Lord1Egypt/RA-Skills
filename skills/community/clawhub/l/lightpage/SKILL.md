---
metadata:
  slug: "lightpage"
  displayName: "lightpage"
  version: "0.14.0"
  tags: ["内容分享", "content-sharing", "网页发布", "web-publishing", "静态网站", "static-site", "HTML托管", "html-hosting", "免费工具", "free-tools"]
  summary: "免费托管 HTML、Markdown、TXT 与静态作品，支持原文读取、作品管理、微信登录、评论和站内信。 Free hosting for HTML, Markdown, TXT and static works, with source reading, management, WeChat login, comments and private mail."
  homepage: "https://lightpage.hqdx.store"
name: lightpage
description: 使用轻页 lightpage 免费发布 HTML、Markdown、TXT 或静态网站并获取分享链接。用户要求发布或分享作品、读取轻页正文、管理已有作品、更新个人头像／昵称／签名、设置分享方式、处理访问授权、查看访问统计、微信认领、生成分享二维码、联系作者或维护者、接入平台能力时使用。
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

### Capabilities：给页面接入平台能力

`capabilities` 用于发现轻页提供的页面能力，并获取接入说明。当前有访客微信登录（`login`）、位置评论（`comments`）、访问授权（`access`）和发布者主页（`home`）：访客可用微信登录表明身份，或围绕选中文字和页面位置发表评论。这些是页面访客使用的能力，作品所有者的登录与绑定按上节操作。

```bash
python3 "<skill目录>/scripts/litepage.py" capabilities
python3 "<skill目录>/scripts/litepage.py" capabilities comments
```

先查当前实例支持什么，再读取需要的能力说明。标准 UI／SDK 不满足用户需求时，允许按需读取该能力 guide_url 对应的 Markdown API 文档，直接调用接口实现自定义 UI；只读本次需要的能力，不预先加载全部文档。login/comments 也可按 instructions 接入 SDK。access 使用平台 API 与网关，沿现有作品链接使用，浏览器同源与用户许可要求见详情。随后正常发布或更新，无需增加发布开关；查询能力本身不会登录或上传。详细接入见[平台能力](references/capabilities.md)。

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
