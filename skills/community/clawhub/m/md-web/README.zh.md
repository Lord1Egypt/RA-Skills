# MD Web

[English](README.md)

将任意内容转为网页并生成可分享的链接。上传 Markdown 到 S3 兼容存储桶，由 Docsify 自动渲染。

## 安装

按你使用的 agent / CLI 任选其一：

```bash
# ClawHub / OpenClaw
clawhub install md-web

# skills.sh（Vercel skills CLI —— 适用于 Claude Code、Cursor 等）
npx skills add rockbenben/aishort-skills
```

或手动安装 —— 将本仓库克隆到 agent 的 skills 目录（如 `~/.claude/skills/md-web`）。

## 快速开始

1. 安装 skill（见上方）
2. 首次使用时，AI 会引导你填写存储桶配置
3. 之后告诉 AI「用网页展示」即可将内容分享为链接

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
3. 权限选择 **对象读和写**（Object Read & Write）。如需自动过期功能（见下方 `expire_days`），需选择 **管理员读和写**（Admin Read & Write）
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
| expire_days | 否   | 上传文件自动删除天数（默认 `30`，`0` = 永久保留）        | `30`                                  |

> **提示**：R2.dev 子域有速率限制，生产环境建议为桶绑定自定义域名作为 `public_url`。

AI 会自动将配置写入 `~/.md-web/config.json`，之后不再需要重复配置。

## 使用方式

上传的内容通过生成的 URL **公开可访问**。仅在你明确要求时触发：

```text
做成网页
预览 README.md
/md-web path/to/file.md
分享为链接
```

AI 会返回一个链接，点击即可在浏览器中阅读渲染后的文档。

> **注意**：Markdown 中的图片引用（如 `![](image.png)`）不会被上传，仅上传 `.md` 文件本身。如文档包含图片，请使用绝对 URL。

## 安全须知

- **上传的内容通过返回的 URL 公开可访问** —— 切勿上传密钥、API token、个人隐私等敏感内容。
- S3 凭证以**明文**保存在 `~/.md-web/config.json`，请妥善保护该文件 —— 不要提交到仓库或外泄。
- **使用专用存储桶。** 上传文件统一放在 `md-web/` 键前缀下，自动过期规则也只作用于该前缀，所以本 skill 只会过期自己的文件；专用桶能进一步确保不影响你的其他对象或生命周期规则。

## 文件结构

```yaml
md-web/                     # Skill 目录（由 ClawHub 管理，升级时可能被替换）
├── SKILL.md              # AI 指令文件
├── upload.js             # 上传脚本（纯 Node.js，零依赖）
├── README.md             # 英文文档
├── README.zh.md          # 本文档
└── docsify-server/       # Docsify 服务文件（首次上传时自动部署）
    ├── index.html
    ├── README.md
    ├── .nojekyll
    └── assets/           # JS/CSS 资源（本地打包，无 CDN 依赖）
        ├── docsify.min.js
        ├── vue.css
        └── ...

~/.md-web/                  # 用户数据目录（升级时保留）
├── config.json           # 存储桶凭证与配置（首次使用时创建）
└── .deployed             # 部署指纹（跟踪服务端部署状态）
```

## 其他 S3 兼容服务

除 Cloudflare R2 外，本 skill 也支持任何 S3 兼容的对象存储：

- **AWS S3**：endpoint 为 `s3.REGION.amazonaws.com`
- **Backblaze B2**：endpoint 为 `s3.REGION.backblazeb2.com`
- **DigitalOcean Spaces**：endpoint 为 `REGION.digitaloceanspaces.com`
- **Wasabi**：endpoint 为 `s3.REGION.wasabisys.com`
- **腾讯云 COS**：endpoint 为 `cos.REGION.myqcloud.com`

只要能提供 S3 兼容 API 和公共访问 URL，都可以使用。
