# md-img-r2

把 Markdown 里的本地图片直接上传到 Cloudflare R2，并将引用路径替换为公开 URL。它不依赖 PicList Desktop，只需要 Python 3 和一组 R2 配置。配置既可以来自环境变量，也可以来自 `.env` 文件。

---

## 设计目标

- 少依赖：不要求 PicList、Node.js 或第三方 Python 包
- 可分发：别人拿到整个目录后，补齐环境变量或 `.env` 就能用
- 可沉淀：对象 key 默认基于文件内容哈希生成，方便长期复用和避免重复命名冲突

---

## 支持的图片写法

- Markdown：`![](./imgs/a.png)`
- Markdown（带 title）：`![](./imgs/a.png "title")`
- HTML：`<img src="./imgs/a.png" width="300">`
- 引用式定义：

  ```md
  ![][img1]
  [img1]: ./imgs/a.png
  [img2]: <./imgs/b c.png> "title"
  ```

---

## 前置条件

你需要提前准备好 Cloudflare R2 的这些信息：

1. `CF_R2_ACCOUNT_ID`
2. `CF_R2_ACCESS_KEY_ID`
3. `CF_R2_SECRET_ACCESS_KEY`
4. `CF_R2_BUCKET`
5. `CF_R2_PUBLIC_BASE_URL`

可选配置：

- `CF_R2_REGION`
  默认 `auto`
- `CF_R2_ENDPOINT`
  默认 `https://<account_id>.r2.cloudflarestorage.com`
- `CF_R2_KEY_PREFIX`
  默认 `md-assets`

其中 `CF_R2_PUBLIC_BASE_URL` 应该是对外可访问的地址，例如：

```text
https://img.example.com
```

或者：

```text
https://pub-xxxxxxxx.r2.dev
```

---

## 目录结构

```text
md-img-r2/
  SKILL.md
  skill.json
  run.sh
  r2-config.env
  scripts/
    md_img_r2.py
  README.md
```

---

## 安装与准备

### 1) 放到你的项目中

```text
<repo>/.codex/skills/md-img-r2/
```

### 2) 确认入口脚本可运行

```bash
bash .codex/skills/md-img-r2/run.sh --help
```

### 3) 配置环境变量或 `.env`

推荐在项目根目录放一个 `.env` 文件：

```dotenv
CF_R2_ACCOUNT_ID=your-account-id
CF_R2_ACCESS_KEY_ID=your-access-key-id
CF_R2_SECRET_ACCESS_KEY=your-secret-access-key
CF_R2_BUCKET=your-bucket
CF_R2_PUBLIC_BASE_URL=https://img.example.com
CF_R2_KEY_PREFIX=articles
```

也可以继续用 shell 环境变量：

```bash
export CF_R2_ACCOUNT_ID=your-account-id
export CF_R2_ACCESS_KEY_ID=your-access-key-id
export CF_R2_SECRET_ACCESS_KEY=your-secret-access-key
export CF_R2_BUCKET=your-bucket
export CF_R2_PUBLIC_BASE_URL=https://img.example.com
export CF_R2_KEY_PREFIX=articles
```

`.env` 的作用很简单：

- 它是一个“项目级配置文件”
- 用来存放 R2 桶名、公开域名、访问密钥这类不应该写进代码的配置
- 这样你和别人分发同一个 skill 时，只需要各自换掉自己的 `.env`
- 一般应把 `.env` 加进 `.gitignore`，不要提交真实密钥

### 4) 先做一次 dry-run

```bash
bash .codex/skills/md-img-r2/run.sh ./article.md --dry-run
```

脚本会按这个顺序取配置：

1. 命令行参数
2. 当前 shell 环境变量
3. `.env` 文件
4. 默认值

如果没有显式传 `--env-file`，脚本默认按这个顺序找 `.env`：

1. `md-img-r2/.env`
2. `target` 所在目录向上查找最近的 `.env`
3. 当前工作目录下的 `.env`

---

## 使用方式

### 单文件替换

```bash
bash run.sh ./article.md
```

### 目录批处理

```bash
bash run.sh ./posts --recursive
```

### Dry run

```bash
bash run.sh ./article.md --dry-run
```

### 指定对象 key 前缀

```bash
bash run.sh ./article.md --key-prefix posts/2026-04
```

### 临时覆盖公开域名

```bash
bash run.sh ./article.md --public-base-url https://img.example.com
```

---

## 运行机制

- 脚本扫描 Markdown、HTML `img` 和引用式定义里的本地图片
- 同一文件内相同路径只上传一次
- 默认使用 `内容哈希 + 文件名` 生成对象 key
- 上传成功后，把原始本地路径替换成公开 URL
- 非 `--dry-run` 模式下会生成 `.bak` 备份和替换报告

默认 key 形式类似：

```text
articles/6d8f1e2ab4c9d011-cover.png
```

---

## 参数说明

| 参数 | 说明 |
| --- | --- |
| `target` | 必填。Markdown 文件路径或目录路径 |
| `--recursive` | target 为目录时递归处理所有 `*.md` |
| `--dry-run` | 不修改文件，只生成报告 |
| `--key-prefix` | 覆盖默认对象 key 前缀 |
| `--public-base-url` | 覆盖 `CF_R2_PUBLIC_BASE_URL` |
| `--endpoint` | 覆盖 `CF_R2_ENDPOINT` |
| `--bucket` | 覆盖 `CF_R2_BUCKET` |
| `--account-id` | 覆盖 `CF_R2_ACCOUNT_ID` |
| `--access-key-id` | 覆盖 `CF_R2_ACCESS_KEY_ID` |
| `--secret-access-key` | 覆盖 `CF_R2_SECRET_ACCESS_KEY` |
| `--region` | 覆盖 `CF_R2_REGION` |
| `--env-file` | 指定 `.env` 文件路径；不传时自动向上查找 |

---

## 对外分发建议

- 优先分享整个 `md-img-r2/` 目录，而不是只拷脚本
- 把 R2 配置要求写进使用说明，不要把密钥写进 skill 源码
- 推荐同时给对方一份 `r2-config.env` 模板，不要直接给真实 `.env`
- 分发前至少用一篇带本地图片的 Markdown 跑一次 `--dry-run`
- 如果平台要求上传压缩包，直接压缩整个 `md-img-r2/` 目录；不要把本地 `.env`、`.bak` 或 `.replace-report.json` 一起打包

---

## 常见问题

### 为什么上传成功了，但图片访问不到？

通常不是脚本问题，而是公开访问域名没有配好。先检查：

- `CF_R2_PUBLIC_BASE_URL` 是否是对外可访问的域名
- R2 桶是否已经绑定公开域名或可用的 `r2.dev` 地址
- CDN / 自定义域是否已经生效

### 为什么建议用环境变量而不是把配置写进代码？

因为这个 skill 的目标是可分发。配置放环境变量，才能让别人拿到 skill 后替换自己的桶和域名，不会把你的凭证一起带走。

### `.env` 和环境变量有什么区别？

本质上都是给脚本提供配置。

- 环境变量更适合临时执行或 CI
- `.env` 更适合项目本地长期使用
- 对这个 skill 来说，`.env` 只是把那几项环境变量写进一个文件，方便复用和分发
