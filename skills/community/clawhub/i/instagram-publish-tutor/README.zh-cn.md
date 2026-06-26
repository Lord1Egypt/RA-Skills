# instagram-publish

> [EN](README.md) | 中文

通过 Meta Graph API,一行命令把图片发到 Instagram。

- **一次性设置**:在 Meta / Instagram 网页端完成 5 步手动操作
- **重复发图**:一条 Python 命令搞定,三个 API 调用全包
- 所有凭证放在 `.env` 里,**绝不提交到 git**

## 环境要求

- Python 3.7+
- 一个 Instagram **Creator(创作者)** 或 **Business(商家)** 账号
- 一个配置好 Instagram API 访问权限的 Meta Developer App(参见[设置步骤](#设置步骤))
- 一张**公网可访问**的图片 URL(S3 / OSS / GitHub Raw / 任意 CDN)

## 安装

```bash
git clone <本仓库> ~/.claude/skills/instagram-publish
cd ~/.claude/skills/instagram-publish
cp .env.example .env
```

## 设置步骤

> 首次设置必须人工完成 —— 涉及登录、邮箱验证、Meta 后台点击操作,无法自动化。完整流程见 [`SKILL.md`](./SKILL.md) 的 **Part 1** 部分。简要版:

1. 把 Instagram 账号切换为 **Creator(创作者)**
2. 在 <https://developers.facebook.com/> 创建 Meta Developer 账号
3. 创建 App → use case 选 **"Manage messaging & content on Instagram"** → **不要**连接 Business portfolio
4. 完善 App 基本设置(图标、隐私政策 URL、数据删除 URL、类别)后点 **Publish**
5. 在 **Use cases → Customize → API setup with Instagram login** 里授予权限,添加你的 Instagram 账号,点 **Generate token**

把得到的 token(以 `IGAA...` 开头)存到 `.env`。

## 配置

`.env`(从 `.env.example` 复制):

```ini
IG_USERNAME=你的账号handle         # 仅作记录,显示在成功输出里
ACCESS_TOKEN=IGAAxxxxxxxxxxxx     # 必填
IG_USER_ID=2700xxxxxxxxx     # 选填 —— 留空则脚本自动从 /me 拉取
```

> ⚠️ **绝对不要把 `.env` 提交到 git。** 这个 token 等同于你账号的发帖权限,一旦泄露立即在 Meta 后台吊销重发。

## 使用

```bash
# 发一张图
python3 scripts/publish.py \
  --image-url "https://example.com/photo.jpg" \
  --caption "Hello from the Graph API"

# 验证 token + 创建容器,但跳过最后一步发布(用来调试)
python3 scripts/publish.py \
  --image-url "https://example.com/photo.jpg" \
  --caption "先看看" \
  --dry-run

# .env 在别的位置
python3 scripts/publish.py --image-url "..." --env /path/to/.env

# 指定 Graph API 版本
python3 scripts/publish.py --image-url "..." --api-version v23.0
```

成功时的输出:

```
✓ Token valid — user: @xxxxxxx (id: 2700xxxxxxxxxx)
✓ Container created: xxxxxxxxxxxx
✓ Published: xxxxxxxxxxxx
  https://www.instagram.com/p/xxxxxxxxxxxxx
```

## 故障排查

| 报错 | 原因 | 解决 |
|---|---|---|
| `Media download has failed` | Meta 服务器访问不到你的 `image_url` | 把图片放到公网(S3 / OSS / GitHub Raw / CDN)。在**未登录**的浏览器里能打开,Meta 才能访问。 |
| `Unsupported post request` | Token 缺发帖权限 | 回到 App 后台 → **Use cases → Customize → API setup with Instagram login**,重新 Generate token,把权限全勾上。 |
| `/me` 返回 HTTP 400 / OAuthException 190 | Token 过期或格式错 | 在 App 后台重新生成 token,更新 `.env` 里的 `ACCESS_TOKEN`。 |
| `ACCESS_TOKEN not found` | `.env` 缺失或为空 | `cp .env.example .env` 并填入 `ACCESS_TOKEN`。 |

更详细的设置说明和 Graph API 参数,见 [`SKILL.md`](./SKILL.md)。

## 目录结构

```
instagram-publish/
├── SKILL.md            # 完整技术参考(给 AI agent 看)
├── README.md           # 英文说明
├── README.zh-cn.md     # 本文件
├── .env.example        # 凭证模板
├── .gitignore          # 防止 .env 被提交
└── scripts/
    └── publish.py      # 三步发布脚本(只依赖标准库)
```

## 安全提醒

- `.gitignore` 已经把 `.env` 排除 —— 不要改这条规则
- 长期 token 也会过期(默认 ~60 天),过期就在后台重新生成
- token 一旦泄露,**立即**在 App 后台吊销并重发,不要心存侥幸
