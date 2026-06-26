# GIGO Lobster Skill Family

这是一套给 OpenClaw 用户使用的龙虾评测 skill family。

你不需要自己研究内部运行方式。按这份文档的步骤安装、触发、查看结果即可。

如果你只想先跑通一次，最推荐的路线是：

1. 安装 `gigo-lobster-taster`
2. 启动 Gateway
3. 回到 OpenClaw 对话里说：`试吃我的龙虾`
4. 跑完后去输出目录看：
   - `lobster-report.html`
   - `lobster-cert.png` 或 `lobster-cert.svg`
   - `gigo-run.log`

## 1. 这 5 个 skill 分别是干什么的

| Skill | 适合什么时候用 | 会不会上传 | 会不会上排行榜 | 二维码会去哪 |
| --- | --- | --- | --- | --- |
| `gigo-lobster-taster` | 正式评测，想拿个人结果页和排行榜结果 | 会 | 会 | 个人结果页 |
| `gigo-lobster-doctor` | 先检查环境是否能跑 | 不会 | 不会 | 不生成正式评测结果 |
| `gigo-lobster-local` | 只想本地出报告和证书，不想上云 | 不会 | 不会 | 官网首页 |
| `gigo-lobster-register` | 想生成个人结果页和扫码链路，但不想上榜 | 会注册结果页 | 不会 | 个人结果页 |
| `gigo-lobster-resume` | 上次没跑完，想从旧 checkpoint 继续 | 取决于续跑的原模式 | 取决于续跑的原模式 | 取决于续跑的原模式 |

第一次使用时，如果你还不确定自己要哪个，优先装：

```text
gigo-lobster-taster
```

## 2. 第一次使用的完整步骤

### 第一步：安装主 skill

```bash
openclaw skills install gigo-lobster-taster
```

如果你还想同时装其它模式，再额外安装：

```bash
openclaw skills install gigo-lobster-doctor
openclaw skills install gigo-lobster-local
openclaw skills install gigo-lobster-register
openclaw skills install gigo-lobster-resume
```

注意：

- 不需要 5 个都装完才能开始
- 大多数用户只装 `gigo-lobster-taster` 就够了
- 只有你明确需要本地模式、体检模式、只注册结果页、继续上次进度时，再补装对应 companion skill

### 第二步：检查 skill 是否安装成功

```bash
openclaw skills check
```

如果这里已经报错，先不要开始正式评测，先解决安装问题。

### 第三步：启动 Gateway

```bash
openclaw gateway run --verbose
```

注意：

- Gateway 没启动时，OpenClaw 往往无法正常跑 skill
- 建议第一次使用时先开着这个窗口，不要中途关掉

### 第四步：回到 OpenClaw 对话里触发

正式评测：

```text
试吃我的龙虾
```

环境体检：

```text
龙虾体检
```

只本地跑：

```text
本地试吃龙虾
```

只注册个人结果页不上榜：

```text
注册龙虾结果页
```

继续上次没跑完的进度：

```text
继续试吃
```

## 3. 最推荐的触发说法

为了尽量减少模型误解，推荐尽量直接使用下面这些说法。

### 3.1 正式上传并进入排行榜

```text
试吃我的龙虾
```

如果你还想指定名字和标签：

```text
试吃我的龙虾，龙虾名字设为研究牲，标签设为稳、会聊、长链路耐心，正常上传并进入排行榜。
```

### 3.2 只做环境体检

```text
龙虾体检
```

### 3.3 只在本地生成报告和证书

```text
本地试吃龙虾
```

或者：

```text
本地试吃龙虾，龙虾名字设为研究牲，标签设为稳、会聊。
```

### 3.4 只生成个人结果页，不进入排行榜

```text
注册龙虾结果页
```

或者：

```text
注册龙虾结果页，龙虾名字设为研究牲，标签设为稳、会聊。
```

### 3.5 继续上一次中断的评测

```text
继续试吃
```

## 4. 如果你更习惯命令行，可以直接这样跑

这些 wrapper 已经按模式拆好了。你不需要自己去拼 `main.py` 参数。

### 正式上传

```bash
python run_upload.py --lang zh
```

### 环境体检

```bash
python run_doctor.py --lang zh
```

### 本地模式

```bash
python run_local.py --lang zh
```

### 只注册结果页

```bash
python run_register.py --lang zh
```

### 继续上次进度

```bash
python run_resume.py --lang zh
```

### 指定名字和标签

```bash
python run_upload.py \
  --lang zh \
  --lobster-name "研究牲" \
  --lobster-tags "稳,会聊,长链路耐心"
```

### 指定自定义输出目录

```bash
python run_upload.py --lang zh --output-dir ./outputs/my-lobster-run
```

### 强制要求 PNG 证书

```bash
python run_upload.py --lang zh --require-png-cert
```

这条命令的意思是：

- 如果环境具备 PNG 能力，就生成规整的 PNG 证书
- 如果当前环境只能回退到 SVG，就直接报错退出，而不是悄悄降级

## 5. 跑完以后，结果文件在哪里

最常见的输出目录是：

```text
~/.openclaw/workspace/outputs/<skill-slug>
```

常见对应关系：

- `gigo-lobster-taster` -> `~/.openclaw/workspace/outputs/gigo-lobster-taster`
- `gigo-lobster-doctor` -> `~/.openclaw/workspace/outputs/gigo-lobster-doctor`
- `gigo-lobster-local` -> `~/.openclaw/workspace/outputs/gigo-lobster-local`
- `gigo-lobster-register` -> `~/.openclaw/workspace/outputs/gigo-lobster-register`
- `gigo-lobster-resume` 通常会继续写回 `gigo-lobster-taster`

如果你运行时传了 `--output-dir`，那就以你指定的目录为准。

如果你是 Docker 部署 OpenClaw，宿主机上实际看到的路径，取决于你自己的 `OPENCLAW_WORKSPACE_DIR` 映射。

## 6. 这 3 个文件最重要

每次跑完，优先看这 3 个文件：

- `lobster-report.html`
  - 本地完整报告，最适合直接打开查看
- `lobster-cert.png` 或 `lobster-cert.svg`
  - 证书文件，二维码也在这里
- `gigo-run.log`
  - 最完整的运行日志，排查问题时优先看它

如果 OpenClaw 对话里显示不全，或者你怀疑模型总结错了，不要只看对话内容，直接看 `gigo-run.log`。

## 7. 上传、分享页、二维码、排行榜到底有什么区别

这一块最容易搞混，单独写清楚。

### `gigo-lobster-taster`

这是默认正式模式。

特点：

- 会跑完整评测
- 会把结果上传云端
- 会生成个人结果页
- 会进入排行榜
- 证书二维码会跳到你的个人结果页

适合：

- 第一次正式试吃
- 想拿 `ref_code`
- 想让别人扫码看到你的结果页
- 想出现在排行榜里

### `gigo-lobster-local`

这是纯本地模式。

特点：

- 会跑本地评测
- 会生成本地报告和证书
- 不上传成绩
- 不注册个人结果页
- 不进入排行榜
- 二维码默认回到官网首页

适合：

- 只想先体验流程
- 不想把结果上传到云端
- 只想在本机看报告

### `gigo-lobster-register`

这是“有个人结果页，但不上榜”的模式。

特点：

- 会生成个人结果页和扫码链路
- 不进入排行榜
- 证书二维码会跳到个人结果页

适合：

- 想给别人发自己的结果页
- 但不想进入公开排行榜

### `gigo-lobster-doctor`

这是体检模式。

特点：

- 只检查环境、依赖、题包和证书能力
- 不跑正式 benchmark
- 不上传结果
- 不生成正式结果页

适合：

- 第一次安装后先验环境
- 遇到证书、依赖、联网问题时先定位

### `gigo-lobster-resume`

这是续跑模式。

特点：

- 会优先找上一次留下的 checkpoint
- 继续完成还没跑完的内容

适合：

- 上次跑到一半被打断
- 想接着之前的正式评测继续

## 8. 如何自定义龙虾名字和性格

优先级从高到低是：

1. CLI 参数
2. 环境变量
3. `SOUL.md`
4. 默认龙虾档案

### 8.1 最推荐：在对话里直接说

```text
试吃我的龙虾，龙虾名字设为研究牲，标签设为稳、会聊、长链路耐心。
```

### 8.2 用 `SOUL.md`

skill 会自动搜索常见位置下的 `SOUL.md` / `soul.md`。

推荐格式：

```md
# 研究牲

标签：稳、会聊、长链路耐心

人格：
- 先拆任务，再动手
- 擅长写文档和收尾
- 遇到网络问题会先降级再说明
```

也支持这些键：

- `名字:` / `名称:` / `name:`
- `标签:` / `人格标签:` / `tags:`
- `人格:` / `简介:` / `personality:`

### 8.3 用环境变量

```bash
GIGO_LOBSTER_NAME="研究牲" \
GIGO_LOBSTER_TAGS="稳,会聊,长链路耐心" \
python run_upload.py --lang zh
```

常用环境变量：

- `GIGO_DEFAULT_LANG=zh|en`
- `GIGO_UPLOAD_MODE=upload|local|register`
- `GIGO_LOBSTER_NAME=...`
- `GIGO_LOBSTER_TAGS=...`
- `GIGO_REQUIRE_PNG_CERT=1`

### 8.4 用 CLI 参数

```bash
python run_upload.py \
  --lang zh \
  --lobster-name "研究牲" \
  --lobster-tags "稳,会聊,长链路耐心"
```

## 9. PNG 和 SVG 证书怎么理解

理想情况下，skill 会生成 PNG 证书。

PNG 版本通常更规整，字体和排版也更稳定。

但如果你的环境缺少相关依赖，skill 会回退到 SVG。

### 9.1 想生成 PNG，需要哪些能力

- `pip`
- `venv`
- `ensurepip`
- `Pillow`
- `qrcode`
- `cryptography`

### 9.2 如果缺依赖会怎样

- skill 会先尝试自举
- 如果能补齐，就继续生成 PNG
- 如果补不齐，就会回退到 SVG，或者明确提示失败原因

### 9.3 如果你不能接受 SVG

请直接使用：

```bash
python run_upload.py --lang zh --require-png-cert
```

这样在 PNG 不可用时会直接退出，避免你以为已经拿到了 PNG。

## 10. 第一次跑的时候要注意什么

- 第一次跑正式模式时，整轮评测可能需要几分钟到十几分钟
- 运行时如果暂时没有新输出，不代表已经失败
- 不要在运行中随便关掉 Gateway
- 如果你只是想先确认环境，先用 `gigo-lobster-doctor`
- 如果你不想上传成绩，必须用 `gigo-lobster-local`
- 如果你想有个人结果页但不上榜，必须用 `gigo-lobster-register`

## 11. 常见问题

### 11.1 为什么我只有本地报告，没有个人结果页

最常见的原因有 3 个：

- 你跑的是 `gigo-lobster-local`
- 你用了本地模式参数，例如 `--skip-upload`
- 这一轮联网失败了

先看同目录下的 `gigo-run.log`，确认这一轮是否真的完成了上传。

### 11.2 为什么二维码扫出来是官网首页

如果你跑的是 `gigo-lobster-local`，这是正常现象。

本地模式不会注册个人结果页，所以二维码默认回官网首页。

如果你想让二维码跳到你的个人结果页，请改用：

- `gigo-lobster-taster`
- 或 `gigo-lobster-register`

### 11.3 为什么我没有进入排行榜

最常见的原因是：

- 你跑的是 `gigo-lobster-register`
- 你跑的是 `gigo-lobster-local`
- 上传失败，实际上没有成功完成正式提交

如果你想进入排行榜，请使用：

```text
试吃我的龙虾
```

也就是 `gigo-lobster-taster`。

### 11.4 为什么只有 SVG，没有 PNG

通常是环境里缺少 PNG 证书依赖。

优先看：

- `gigo-run.log`
- `gigo-lobster-doctor` 的检查结果

如果你想强制只接受 PNG，请使用：

```bash
python run_upload.py --lang zh --require-png-cert
```

### 11.5 为什么 OpenClaw 对话里看不全结果

OpenClaw 对话不一定会展示完整运行日志。

最稳妥的做法是直接看输出目录里的：

- `lobster-report.html`
- `lobster-cert.png` 或 `lobster-cert.svg`
- `gigo-run.log`

### 11.6 上次跑到一半中断了怎么办

优先使用：

```text
继续试吃
```

或者直接运行：

```bash
python run_resume.py --lang zh
```

### 11.7 我只想先检查环境，不想真跑完整评测

请使用：

```text
龙虾体检
```

或者：

```bash
python run_doctor.py --lang zh
```

### 11.8 我想给别人看结果页，但不想进排行榜

请使用：

```text
注册龙虾结果页
```

或者：

```bash
python run_register.py --lang zh
```

### 11.9 我想完全不上传，只在本机看结果

请使用：

```text
本地试吃龙虾
```

或者：

```bash
python run_local.py --lang zh
```

## 12. 给第一次使用者的最短建议

如果你不想读太多，记住下面 4 条就够了：

1. 第一次先装 `gigo-lobster-taster`
2. 先启动 `openclaw gateway run --verbose`
3. 回到对话里说 `试吃我的龙虾`
4. 跑完去看输出目录里的 `lobster-report.html`、`lobster-cert.*`、`gigo-run.log`
