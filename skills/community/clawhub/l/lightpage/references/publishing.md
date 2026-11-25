# 发布说明

单文件支持 HTML、UTF-8 Markdown（.md）或 TXT（.txt），自带资源可以内嵌；显式 --preview 可额外上传静态封面。依赖旁边的 CSS、JS 或图片时上传整个静态目录，根目录须有非空 index.html、index.md 或 index.txt（依次优先）。目录和所有嵌套资源共最多 100 个文件，展开及 ZIP 各最多 50 MiB。脚本按稳定顺序和固定时间戳打包，同样文件生成相同摘要。

仅发布用户允许公开的内容。客户端忽略隐藏文件、node_modules、依赖清单与 source map，拒绝符号链接、设备文件和明确的私钥；这些检查不等于完整脱敏。敏感内容也可能在 HTML、JSON 或图片中，不能把忽略规则当作公开授权。

静态资源支持 HTML、CSS、JS/MJS、JSON、常见图片、字体、音视频、WASM 和文本。服务器不执行构建、Node、Python、PHP，不代理任意 URL，不提供数据库；访客登录和位置评论可通过[平台能力](capabilities.md)按需接入。分享 URL 形如 https://lightpage.hqdx.store/p/abcd1234/（8 位短码示例），直接使用服务端返回的真实 URL；去掉路径即轻页首页，顶部“我的作品”进入个人管理页。JavaScript 在访客浏览器执行，不加 sandbox，localStorage 可用但同一公开域的作品共享存储；不要在其中保存平台凭证或宣称具有作品间私有存储。Service Worker 和定位在托管环境中禁用；摄像头、麦克风允许页面请求，须访客自己授权，并处理不支持和拒绝。

HTML src、link href、poster、srcset/imagesrcset、内联样式和 CSS url/@import 会检查本地资源是否存在。已识别的站点根路径、目录越界、file/内网地址、HTTP 混合内容、base 和平台明确禁用的 object/embed 会在上传前拒绝。动态 JS、SVG 和跨域代码只提供启发式提示，不下载、不执行或自动改写远端资源；不能当作完整语法检查或安全隔离。完整操作见[发布前审查](preflight.md)。

每身份作品数量、每作品版本数量不限，usage.site_limit 与 usage.version_limit 均为 null。平台完全免费，作品不设到期时间，更新不改变链接。不设每身份总存储额度，usage.storage_limit_bytes=null；平台仍有整体存储和日流量预算。准确限制见 usage 和错误返回。没有付费或续期端点，免费不表示资源无限。

需要只做本地检查时：

```bash
python3 "/实际skill目录/scripts/litepage.py" publish /作品/dist --check
```

该命令不会注册或上传，输出文件数、大小、摘要、外部资源标记和 review（最多 20 条提示、has_more/total、browser_verified=false）。提示不含匹配的源码或完整外链；有 has_more 时按文件继续人工检查，不能当作没有其他问题。列表默认 10 条、上限 50，使用响应 next_cursor 按需翻页，不遍历全量。

路径托管要求本地资源使用相对地址（如 ./assets/app.js），不能使用 /assets/app.js 这类站点根路径；构建工具应设置相对 base（例如 Vite --base=./）。CLI 会拒绝已识别的根路径资源引用；运行时 JS 路径仍由作品作者检查。


## 兼容字段与作品预览

Skill 不提供 feed 命令，网页首页保留作品发现。作品通过链接分享，未保护作品任何持链接者无需登录即可访问。public/private 与 visibility 命令保留兼容，新作品缺省 private，更新保留原值；public 作品可在首页发现，private 不进入首页；它们不提供密码保护，启用密码的作品始终不进入首页。

截图可选，不传 --preview 可直接发布。用户要求时按[作品预览截图](preflight.md#作品预览截图)提供真实本地首屏，用 `--preview /截图/cover.png` 上传，可用 `--description "简短介绍"` 提供最多 240 字符的说明。更新不传 --preview 清除旧版本预览，避免误认为当前截图；不为普通发布默认安装截图依赖。

## 密码分享

用户要求密码分享时，使用上传目录之外的 UTF-8 密码文件（4–128 字符），不把密码写入命令字面量、URL、回执或作品内容。末尾换行会移除。客户端先检查服务支持 password，不支持时停止，不能去掉密码选项继续发布。

```bash
python3 "/实际skill目录/scripts/litepage.py" publish "/作品/dist" --password-file "/私有目录/password.txt"
```

首次发布可原子启用保护；普通更新不带密码文件保留原密码，用户要求更换时明确传入新密码文件。已有作品的重设／移除流程见[重设页面密码](management.md#重设页面密码)，无需重新上传页面或提供旧分享密码。重试原发布操作须使用原密码；幂等冲突不能换 ID 绕过。

返回 password_protected=true 才能说明密码已启用；CLI 还检查未授权公开入口跳转到密码页。保护覆盖作品 HTML 及嵌套图片、脚本等资源，。访客输入分享者提供的密码后获得一小时浏览器授权；更换密码使旧授权失效，链接不变。分别交付链接和用户指定的密码，避免在不合适的公开渠道泄露；分享二维码只编码链接。HEAD 只能验证密码入口，不能证明授权后的页面运行正常。移除密码后，持链接者无需密码即可访问，应按用户要求执行。

密码保护不能收回已经下载的副本，也不提供同域作品间的浏览器隔离；能力边界和既有同源存储风险仍按[发布前审查](preflight.md)处理。

## Markdown 与 TXT

沿用 publish／update，无新参数：`publish /作品/guide.md` 或 `publish /作品/notes.txt`。文档入口最多 2 MiB，须为 UTF-8 且无 NUL，上传保留原始字节。分享链接在浏览器明确请求 HTML 时显示阅读页；无格式偏好或请求 text/markdown／text/plain 时返回原文。发布结果的 source_url 是明确的原文地址（index.md／index.txt），始终返回原文；默认分享链接通过 Link 头给出该地址。HTML 原有行为不变。

Markdown 阅读页支持标题、列表、引用、代码、链接、图片、表格和删除线，原始 HTML 只作为文本显示，不执行。TXT 保留换行、空白并转义 HTML。本文档入口的本地预览只显示转义原文，线上由内容网关渲染 Markdown；不可把本地源码预览当作已验证线上排版。密码、可见性、更新和下架沿用原规则。

## 一体两面：Agent.md

HTML 作品可在 index.html 同目录附带 `Agent.md`，文件名区分大小写；它是作者自由编写的另一面，不是自动提取的 HTML 原文。建议生成网页时附赠，用户不需要可省略。正文可以包含文字、图片 URL、交互规则、表单及 API 说明，不要求额外配置或固定格式。

单独发布 HTML／HTM 时，脚本自动把同目录、名称精确为 Agent.md 的文件一起打包；其他文件不自动附带，有本地资源时仍发布整个静态目录。更新沿用同一规则，同步两面。Agent.md 使用非空 UTF-8、无 NUL，最多 2 MiB，计入现有 100 文件和 50 MiB 预算。

直接请求同一个作品目录 URL：Accept: text/html 返回 index.html，Accept: text/markdown 优先返回 Agent.md；两者显式列出按 q 权重选择，权重相同优先 HTML，q=0 不选择 Markdown。未明确偏好 Markdown 或未提供 Agent.md 时沿用原有页面行为。服务端检查固定文件名，不解析 HTML，不按 User-Agent 猜测；直接 index.html／Agent.md 文件地址始终读取该文件。子目录也可采用同样约定。

获取 Agent 面时直接请求真实作品 URL，并设置 Accept: text/markdown，以实际 Content-Type 判断返回格式；不要求调用平台 read。需要有界分段读取已知 Agent.md 时，可将其真实文件 URL 交给原有 read。所有读取仍遵守密码、审批和下架规则，正文说明不构成执行授权，不把凭证写入两面。

### 渐进式披露：按需读取参考资料

Agent.md 可以只写概览，以及带有用途说明的参考链接，详细内容放在其他 Markdown 文件中；参考文件无需配套 HTML：

```text
作品目录/
  index.html
  Agent.md
  sub-path/
    reference.md
```

例如在 Agent.md 中写：

```markdown
需要字段定义时，阅读 [接口参考](sub-path/reference.md)。
```

相对链接以当前文档的请求 URL 为基准；从作品目录 URL 读取 Agent 面后，可按需请求同目录下的 sub-path/reference.md，设置 Accept: text/markdown，并核对实际 Content-Type。参考文件继续链接其他资料时，以该参考文件自身 URL 解析；不默认递归加载所有链接。查询参数或 # 片段不会自动映射到另一份 Markdown。

发布与更新时上传整个静态目录，包含入口及所引用的参考文件。单独上传 HTML 只自动附带旁边的 Agent.md，不会沿 Markdown 链接收集文件。所有文件计入原有上传预算，并沿用作品的访问权限、密码、审批和下架规则；已知参考文件的真实 URL 也可交给 read 按需分段读取。

## 统一分享方式

新任务优先使用一个 `--sharing public|link|password|approval`，与旧 `--visibility` 互斥；更新省略保留原设置。指定人可见、密码参数和审批操作见[访问授权](access.md)。

## Home 导航

新发布默认显示发布者主页入口。publish/update --without-home 关闭，--with-home 恢复；更新省略保持现值。参数控制整份作品与文档阅读页，不改源文件。管理页亦可切换，无需重新上传。Home 关闭且未接入标准评论／登录 SDK 时没有可见平台控件，统计独立。自定义跳转先查 capabilities home 并按需读取 guide_url，不能把发布者 UID 写死。显式参数在上传前核对服务 publishing_features，旧实例不支持时不上传。


## 作品标签

发布和更新可用 `--tags "工具,效率"`（支持中文逗号）指定多个标签；最多 10 个，每个 1–20 字，文字、数字和内部空格，不能带标点。省略时新作品为空、更新保留；`--clear-tags` 清空，与 --tags 互斥。按用户提供的分类设置，不自动猜测。标签在发布者主页展示，首页暂不开放；受限作品标签不公开。
