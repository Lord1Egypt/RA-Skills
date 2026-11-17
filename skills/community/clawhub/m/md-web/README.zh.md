# MD Web

> 把任意内容转成网页并生成可分享的链接。上传 Markdown 到 S3 兼容存储桶，由 Docsify 自动渲染。

[English](README.md) · 本文档为中文版，术语与英文版一致。

## 安装

按你使用的 agent / CLI 任选其一：

```bash
# ClawHub / OpenClaw
clawhub install md-web

# skills.sh（Vercel skills CLI —— 适用于 Claude Code、Cursor 等）
npx skills@1.7.2 add rockbenben/aishort-skills
```

请像上面那样固定 CLI 版本：不带版本的 `npx skills add …` 会在安装时解析到仓库当时的版本，
也就是你审过的安装器和真正跑起来的那个可能不是同一个。

固定的是**安装器**，不是**内容**。安装时取到的仍然是仓库当时的 skill；真正把内容钉住的是
skill 自己的发布版本 —— 请安装你读过的那个版本，升级之后再重装一次（版本号见
`skills/md-web/SKILL.md`）。审过安装器不等于审过 skill：装之前先读一遍。

或手动安装 —— clone 本仓库，把 `skills/md-web/` 目录拷贝（或软链）进你的 agent 读取的
skills 目录即可，只要是一个名为 `md-web` 的目录，具体路径按你的 agent 文档来。

## 快速开始

1. 安装 skill（见上方）
2. 首次使用时，AI 会引导你填写存储桶配置
3. 之后 AI 会先做一次「初始化站点」——把页面外壳和它的静态资源部署到你的桶，skill 升级后需要再做一次。
   这一步会改写桶根目录下的共享状态，需要请求中已有的授权或另行确认。
4. 再之后，告诉 AI「发布为公开分享链接」即可分享内容。

## 这个 skill 会动什么

下面是它会做的全部事情，除此之外什么都不做。

- **发布一篇文档**：只写入**一个**对象 —— `md-web/<时间戳>-<短名>-<后缀>.md`，位于桶的 `md-web/` 前缀下。不写别的，也不删任何东西。
- **初始化站点**（`--setup --confirm-shared-writes`）：这是**独立的命令**，绝不会作为发布的副作用顺带执行。先上传 `assets/<bundle-hash>/` 并更新根目录 `README.md`，成功后带条件替换根目录 `index.html`。这些是共享查看器文件，旧资产保留给缓存页面，现有文档 URL 不变。
- **`expire_days`**：唯一涉及桶管理的动作，**不设置就不会发生**。设置后，初始化步骤会**读取**桶的生命周期配置，并写回**属于它自己的那一条规则**，限定在 `md-web/` 前缀下；填 `0` 则移除这条规则。其它规则和桶级设置都会原样保留，该前缀下的上传会在 N 天后**自动删除**。
- **本地文件**：读取 `~/.md-web/config.json`（凭证与桶配置），写入 `~/.md-web/.deployed`（部署指纹提示）。发布前还通过配置的 S3 端点读取远端 `index.html`，确认正在使用的查看器。
- **仅此而已**：不碰其它桶、不碰其它前缀、不碰别的 skill 的文件、不写启动项、不建定时任务、不起后台服务、不连第三方服务、不发遥测。

一句话概括作用范围：本地运行 `node`，读取 `~/.md-web/config.json`（或 `MD_WEB_ACCESS_KEY` / `MD_WEB_SECRET_KEY`），**只**向你配置的 S3 端点发 HTTPS 请求，写入上传的 `.md` 和查看器资源，最多写一条限定在 `md-web/` 前缀下的生命周期规则，创建并删除至多一个临时文件，不触碰其它 skill，也不安装任何东西。

明确要求公开分享链接，即授权上传这篇文档及失败后的重试，AI 会在上传前说明公开访问范围。初始化站点会覆盖桶根目录的共享文件，保留策略变更会修改桶配置，这两项各自需要请求中已有的授权或另行确认。本地预览在本地完成。

## 存储桶配置

本 skill 需要一个 **S3 兼容的对象存储桶**并开启公共访问。以下以 Cloudflare R2 为例。

### 第一步：创建存储桶

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. 左侧菜单选择 **R2 对象存储**
3. 点击 **创建存储桶**，填写名称（如 `md-web`），区域选默认即可
4. 创建完成后进入桶的 **设置** 页面
5. 找到 **公开访问**，点击 **允许访问**，勾选 **R2.dev 子域**
6. 开启后会显示公共 URL，格式为 `https://pub-XXXX.r2.dev`
   → 这就是配置中的 **public_url**

### 第二步：创建 API 令牌

1. 在 R2 页面点击 **管理 R2 API 令牌**
2. 点击 **创建 API 令牌**
3. 权限选择 **对象读和写**（Object Read & Write）。只有设置 `expire_days`（要管理桶的生命周期规则）时才需要 **管理员读和写**（Admin Read & Write）
4. 范围可选 **仅限指定桶** → 选择刚才创建的桶
5. 创建后会显示：
   - **Access Key ID** → 配置中的 **access_key**
   - **Secret Access Key** → 配置中的 **secret_key**
   - **S3 端点** 格式为 `https://ACCOUNT_ID.r2.cloudflarestorage.com`
     → 去掉 `https://`，剩余部分就是 **endpoint**

### 第三步：告诉 AI

首次使用 skill 时，AI 会询问以下信息：

| 字段        | 必填 | 说明                                                     | 示例                                  |
| ----------- | ---- | -------------------------------------------------------- | ------------------------------------- |
| access_key  | 是   | API 访问密钥 ID                                          | `a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4`    |
| secret_key  | 是   | API 秘密访问密钥                                         | `a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6...` |
| endpoint    | 是   | S3 端点（不含 https://）                                 | `ACCOUNT_ID.r2.cloudflarestorage.com` |
| bucket      | 是   | 存储桶名称                                               | `md-web`                              |
| public_url  | 是   | 公共访问 URL（推荐自定义域名）                           | `https://pub-XXXX.r2.dev`             |
| region      | 否   | S3 区域（R2 用 `auto`，AWS S3 填实际区域如 `us-east-1`） | `auto`                                |
| expire_days | 否   | 上传文件 N 天后自动删除。**留空 = 本 skill 完全不碰桶的生命周期配置**（默认） | `30` |

> **提示**：R2.dev 子域有速率限制，生产环境建议为桶绑定自定义域名作为 `public_url`。

AI 会自动将配置写入 `~/.md-web/config.json`，之后不再需要重复配置。

不想把长期密钥写在文件里？可以不填 `access_key` / `secret_key`，改用环境变量
`MD_WEB_ACCESS_KEY` / `MD_WEB_SECRET_KEY`。两者都存在时以配置文件为准，老配置不受影响。

## 使用方式

上传的内容通过生成的 URL **公开可访问**。仅在你明确要求时触发，AI 也会在上传前告诉你链接是公开的：

```text
把这篇 Markdown 发布到我的公开存储桶
为这篇文档生成公开网页链接
/md-web path/to/file.md
```

转发已有链接、生成私密链接或本地预览，不代表授权公开上传。分享目的地或公开范围不明确时，先澄清再上传。

AI 会返回一个链接，点击即可在浏览器中阅读渲染后的文档。

> **注意**：Markdown 中的图片引用（如 `![](image.png)`）不会被上传，仅上传 `.md` 文件本身。如文档包含图片，请使用绝对 URL。

## 自动过期（`expire_days`）

留空时本 skill 不会发出任何桶级请求 —— 只需要 **对象读和写** 权限，桶里的生命周期配置原样不动。

填一个天数，则只维护一条限定在 `md-web/` 前缀下的规则；填 `0` 则移除这条规则。两种情况下
桶根目录的站点文件和其它对象都不会被波及，而且**你自己设的规则会保留**：脚本先读取桶的生命周期
配置，只丢弃自己那一条，再把其余规则原样写回。

管理它需要 **管理员读和写** 权限的令牌。令牌权限更窄时「初始化站点」照常完成，只是输出里会一闪而过一条
警告 —— 这时去控制台手动设置规则即可。改过之后重跑一次「初始化站点」。

## 安全须知

- **上传的内容通过返回的 URL 公开可访问，且没有「取消发布」这一步**（除非设置了 `expire_days`，届时上传的文件会在 N 天后自动删除）—— 切勿上传密钥、API token、个人隐私等敏感内容。
- 凭证以**明文**保存在 `~/.md-web/config.json`（也可放在 `MD_WEB_ACCESS_KEY` / `MD_WEB_SECRET_KEY` 环境变量里）。在 macOS / Linux 上脚本会把配置文件权限收紧到仅本人可读写；无论哪种方式都请保护好它 —— 不要提交到仓库或外泄。
- **不需要任何提权。** 上面那次权限收紧是本 skill 唯一做的权限变更：它只动你自己家目录下的文件，以你本人的身份执行。skill 不会请求 root、不会执行任何提权命令，也不会碰你家目录和所配置存储桶以外的任何文件。
- **使用专用存储桶。** 上传与过期规则都限定在 `md-web/` 前缀下，但专用桶能保证本 skill 的桶管理权限远离你真正在意的数据。
- **查看器会把你上传的 Markdown 当作 HTML 渲染在页面上。** GFM、表格、`<details>` 和行内 HTML 都能正常渲染。有两道防线把它约束住：路由守卫只加载 `md-web/` 下的同源路径（构造的链接无法让查看器从其他源拉取文档），以及不含 `'unsafe-inline'` 的 CSP（文档里的 HTML 无法执行脚本）。但 CSP **拦不住**文档往页面里**插入元素** —— 所以发布前要检查陌生来源的 Markdown 和行内 HTML；是否亲手编写并不能替代内容检查。请把页面当作公开且不可信的内容：任何能写这个桶的人都能往里放东西。
- 文档保留原语言。查看器界面为英文，字数统计跟随文档内容。

## 文件结构

```yaml
md-web/                     # Skill 目录（由 ClawHub 管理，升级时可能被替换）
├── SKILL.md              # AI 指令文件
├── upload.js             # 上传脚本（纯 Node.js，零依赖）
├── README.md             # 英文文档
├── README.zh.md          # 本文档
└── docsify-server/       # 查看器文件（由「初始化站点」步骤上传）
    ├── index.html
    ├── README.md
    └── assets/           # JS/CSS 资源（本地打包，无 CDN 依赖）
        ├── config.js     # 查看器配置 + 文档路由守卫
        ├── docsify.min.js
        ├── vue.css
        └── ...

~/.md-web/                  # 用户数据目录（升级时保留）
├── config.json           # 存储桶凭证与配置（首次使用时创建）
└── .deployed             # 本地部署提示，发布时还会核对远端入口
```

`upload.js` 对 `docsify-server/` 拍摄文件快照并计算指纹（忽略点号文件），将资产放到 `assets/<bundle-hash>/`，全部上传成功后才切换 `index.html`。本地提示加上远端入口检查，可以发现升级、删除或另一套安装替换了查看器；此时发布以 `SETUP_REQUIRED` 停下，需要明确执行初始化。旧文档链接和落地 README 路径继续有效。

初始化用 ETag 条件替换入口（`If-Match`，首次部署为 `If-None-Match: *`）。遇到 `SETUP_CONFLICT` 先核对正在使用的查看器再重试，不自动覆盖竞争者。服务商需要支持条件写入并返回 ETag，不提供无条件回退。依据为 [S3 条件写入](https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-writes.html)与 [R2 S3 兼容说明](https://developers.cloudflare.com/r2/api/s3/api/)。从旧的平铺资产版本升级时需初始化一次。旧平铺资产、版本目录和中断上传的残留均保留，不自动清理，也不扩大生命周期规则的作用范围。

生命周期变更需与其他管理员串行执行：S3 整体替换策略，没有原子的单规则更新。初始化在写前复读，发现并发编辑、不支持／不完整 XML 或规则 ID 归属冲突时告警，不重放失败的策略写入。最后一次读与写之间仍有竞争窗口。告警时应核实实际保留策略，查看器仍可使用。

## 其他 S3 兼容服务

除 Cloudflare R2 外，本 skill 也支持任何 S3 兼容的对象存储：

- **AWS S3**：endpoint 为 `s3.REGION.amazonaws.com`
- **Backblaze B2**：endpoint 为 `s3.REGION.backblazeb2.com`
- **DigitalOcean Spaces**：endpoint 为 `REGION.digitaloceanspaces.com`
- **Wasabi**：endpoint 为 `s3.REGION.wasabisys.com`
- **腾讯云 COS**：endpoint 为 `cos.REGION.myqcloud.com`

安全初始化还需要对象读取、ETag 和条件对象写入。使用其他 S3 兼容服务时，应先确认这些能力。
