---
name: IG link to Bili
description: 把 Instagram Reel 链接（用户提供）下载、翻译、转载到 B 站。**不做** IG feed/hashtag 自动抓取、**不做**点赞阈值筛选、**不做**去重、**不做**作者黑名单——链接都是用户主动给的，过滤掉反而是 surprise。当用户提供 instagram.com/reel/<code>/ 或 /p/<code>/ 链接并希望转载/搬运/上传到 B 站时激活。
version: 1.5.0
author: Taozi (Arvin Yin)
tags: [instagram, bilibili, motion-design, video, repost, single-link]
---

# IG link → Bili 转载

把用户给的一条（或一批）Instagram Reel/Post 链接下载、翻译、转载到 B 站。

**核心约束**：链接都是用户主动给的——**不做抓取/筛选/去重/黑名单**。

> **编辑风格不写死**（v1.5.0）：标题、描述、分区（category）、标签（tags）都**不固定**——
> 默认由 agent 按视频内容 + 用户意图临时决定，通过命令行参数传给 `upload_one.py`。
> 想给固定频道设默认的，复制 [`config.example.json`](./config.example.json) 为 `config.json` 填一次即可
> （解析优先级：命令行 > config.json > 兜底）。**不自动加入任何合集**。

> ⚠️ **撞墙时**——先读 [`references/diagnosis-methodology.md`](./references/diagnosis-methodology.md)，**再**读 [`references/pitfalls.md`](./references/pitfalls.md)。元归因纪律（裸 curl 验证 ≠ 真实请求形态）比单条 pitfall 更重要。

---

## 触发条件

用户消息里：
1. 含 instagram.com 链接（`/reel/<code>/`、`/p/<code>/`、`/tv/<code>/`）
2. **且**明确说"转载/搬运/上传/转 B 站"等意图

**不触发**：
- 用户只是分享链接、问内容是什么
- 链接是 YouTube（走 youtube-to-bilibili skill）

---

## 前置依赖

| 工具 | 用途 | 安装 |
|---|---|---|
| Python 3.8+ | 跑上传脚本 | 系统已带 |
| `httpx aiohttp beautifulsoup4 lxml requests` | B 站 API client | `pip install -r bilibili_uploader/requirements.txt` |
| `yt-dlp` | 公开下载 IG Reel（无需 IG 账号） | `brew install yt-dlp` 或 `pip install yt-dlp` |
| `ffmpeg` | 截视频第 1 秒做封面 | `brew install ffmpeg` |
| `browser_cookie3` | 从浏览器拉 B 站 cookie（首次必跑） | `pip install browser_cookie3` |
| B 站 cookie | **分发包里 credentials.json 是占位模板**，首次使用前必须自己刷 | `python3 scripts/setup_cookies.py`（自动探测浏览器；支持 chrome/edge/brave/arc/vivaldi/firefox/safari 等，不限 Chrome） |

**无 WebBridge 也能跑**——caption 通过 `yt-dlp --write-info-json` 拿（fallback）。

---

## 工作流（agent 视角）

对每个 IG 链接串行执行：

1. **解析 shortcode**——从 URL 抽 `reel/DYyvKNpEdoo/` 的 `DYyvKNpEdoo`
2. **下载 + 元数据**：
   ```bash
   ./scripts/prepare_media.sh <shortcode> [/tmp/ig_link_bili]
   ```
   → 产出 `<shortcode>.mp4` + `<shortcode>.info.json`（含 uploader/like_count/description）+ `<shortcode>thumb.jpg`
3. **生成标题/描述/分区/标签**（agent 脑内，按内容 + 用户意图，不写死）：
   - **标题**：把 caption 译成中文标题。**前缀不强制**——若用户/`config.json` 指定了固定前缀就用，否则不加。
   - **描述**：建议格式 `转载来源：Instagram - 原作者：@<uploader>\n\n<1-2 句中文概述>\n\n—— 原简介 ——\n<原文>`；**不要在简介里写原视频链接**；保留 studio 名 / 软件名 / 行业英文术语不译。
   - **分区 category（必填）**：按视频内容选合适的 B 站分区 TID（如动画/创意/科技等，**别用游戏默认区**）。不确定就问用户，或读 `config.json`。
   - **标签 tags**：按内容取 3-8 个相关标签；或读 `config.json`。
   - 非中文 caption 才翻译；本身是中文直接用。
4. **上传 B 站**：
   ```bash
   python3 ./scripts/upload_one.py <shortcode> "<标题>" "<描述>" --category <TID> --tags 标签1,标签2
   ```
   - `--category` 必填（命令行或 `config.json` 二选一）；`--tags` 可选；来源默认自动用该 Reel 的 IG 链接
   - → 返回 JSON 含 `bvid` + `aid`
5. **验真**（**必做，**B 站接口异步——`upload_one.py` 返 success 不代表真成功）：
   ```bash
   sleep 60
   python3 ./scripts/verify_upload.py <bvid>
   ```
   → "OK <title>" 才是真成功；FAIL/PENDING 要重试或排查

   ⚠️ **不要跳过这一步**——2026-06-05 实测跳过的代价是把 8 个作者错误拉黑。详见 [`references/upload-verification.md`](./references/upload-verification.md)。
6. **撞墙时的诊断顺序**（2026-06-07 教训）：如果 `upload_one.py` 抛 `Expecting value: line 1 column 1` JSON 解析失败，**不要**先归因"B 站挂了"——按 `references/pitfalls.md` §7 决策树跑 Step 1-3。`api.bilibili.com/x/web-interface/nav` 的 `isLogin` 字段是判定 cookie 是否真有效的关键。
7. **汇报**：返回 B 站视频 URL `https://www.bilibili.com/video/<bvid>`

---

## 文件结构

```
ig-link-bili/
├── SKILL.md                      ← 你正在看的
├── config.example.json           ← 可选配置模板（复制为 config.json 设固定的分区/标签/标题前缀）
├── scripts/
│   ├── setup_cookies.py          ← 首次必跑：从本机浏览器抓 B 站 cookie 写入 credentials.json（支持多浏览器，自动验真）
│   ├── prepare_media.sh          ← 一步：下载 mp4 + 截封面 + 拉元数据 JSON
│   ├── upload_one.py             ← 单条上传 wrapper（分区/标签走参数或 config.json，不写死）
│   └── verify_upload.py          ← B 站 API 验真（带重试）
├── bilibili_uploader/            ← 自包含 B 站上传库（拷自 wscats/bilibili-all-in-one）
│   ├── main.py
│   ├── src/
│   ├── credentials.json.template ← cookie 模板（真 credentials.json 由 setup_cookies.py 生成，已 .gitignore）
│   └── requirements.txt
├── examples/                     ← 几个测试链接
└── references/                   ← 已知坑、失败案例
    ├── pitfalls.md               ← cookie 三件套、preupload 403 决策树等
    └── upload-verification.md
```

---

## 多条链接处理

用户一次贴 N 条链接（比如一个 IG profile 的几个 Reel）：
- **串行处理**——避免 B 站频率限制触发
- 每条之间 sleep 30-60s
- 一条失败不阻塞其他——记入失败列表，最后汇总

---

## Pitfalls

### B 站上传接口是异步的
接口立刻返 `success: true` + `bvid`，但 `api.bilibili.com/x/web-interface/view?bvid=X` 真可查可能要等 30s-2min。**不要看到 success 就立刻验真**——`verify_upload.py` 默认重试 3 次每次等 30s 兜底。

### IG 视频的 caption 来源
**不用 WebBridge**——`yt-dlp --write-info-json` 拿到的 `description` 字段就是 caption。
如果 description 是非英文（如俄语/西语）→ agent 翻译。
如果 description 是中文 → 直接用，不翻译。

### 封面策略：yt-dlp 拉 IG 官方封面 → ffmpeg 截帧兜底（2026-06-07 修订）

`prepare_media.sh` 的封面逻辑是**双保险**：
1. **优先**：`yt-dlp --write-thumbnail --convert-thumbnails jpg` 拉 IG 官方封面（CDN 单独资源，**经常是设计过的宣传图**）
2. **失败兜底**：`ffmpeg -ss 00:00:01 -vframes 1` 从 mp4 截第 1 秒帧

**Arvin 偏好 2026-06-07**：永远先尝试官方封面——截帧兜底通常拿到的是视频启动瞬间（黑屏/logo），信息量弱。**实测**：3 条 Reel 复测，2/3 拿到官方宣传封面（设计过的），1/3 自动 fallback 到截帧。

**只有一种情况失败**：极短视频（<1s）——`ffmpeg -ss 00:00:01` 抽不到帧——`upload_one.py` 检测到 cover 缺失会跳过，**B 站自动生成默认封面**。

### 撞墙时不要立刻归因到"上游抽风"（2026-06-07 Arvin 明确偏好 · 元归因纪律）

**症状**：upload 失败、`verify_upload.py` 报 PENDING、preupload 返 403、nav API 报 -101 ——**任一**出错时，agent 第一反应往往是"B 站挂了"或"接口被风控"。

**Arvin 明确反对**（2026-06-07 教训）：**撞墙时**先**排除自己的问题**（cookie / 编码 / shell 引号 / agent 读到的状态过期），**再**归因上游。

**错误示范**（2026-06-07 撞过的真实翻车）：
1. preupload 403 + HTML 错误页 → 立刻归因"**B 站 member 域临时抽风**"，连发 3 次重试
2. 跑了一遍裸 curl 验证 → 看到同样 403 → 强化"上游挂了"判断
3. **没做的事**：没看上传库请求 cookie 三件套齐不齐 / 没问 user 验证 cookie / 没自己诊断是不是这边 cookie 失效
4. Arvin 一句"**你验证了 B 站 cookie 账号吗？**"才回头查——**SESSDATA 是空字符串**（skill 自带占位）
5. 拿到真 cookie 刷上去后，**同一份上传库**、**同一段代码** → preupload 200、nav isLogin=True、upload 成功

**正确做法**（撞墙时强制顺序）：
1. **第 1 件事**——按 `references/pitfalls.md` §7 决策树跑 Step 1-3，**至少**跑到 Step 3 `isLogin` 判定
2. **第 2 件事**——如果有别的 agent（Codex / Claude Code / 别的 session）做过类似任务，**先看他们的反例**——他们的成功案例直接证伪"上游挂了"判断
3. **第 3 件事**——**不要**循环重试 3-5 次"等它自己好"——上游问题不会自愈
4. **第 4 件事**——把"已跑过 Step 1-3 + 看到的事实（status code / 错误页文案 / nav isLogin 值）"交给 Arvin，**让他决定**继续还是换路

**Arvin 的明确偏好原话**（2026-06-07）："**Codex 反例成立之前不要判'B 站挂了'。我们本机实测反例已否定了'风控全量拦截'理论。**"

**记忆锚点**：任何"上游抽风 / 风控 / 服务器挂"的判断，**必须有本机近 30 分钟的诊断证据**支撑，**且**没被别的 agent 反例证伪。**否则就是脑补**。

### credentials.json 必须自己刷（首次必做）
分发包里的 `bilibili_uploader/credentials.json` 是**占位模板**（`YOUR_SESSDATA_HERE`），直接用必然 403。
**首次使用前**在某个浏览器登录 bilibili.com，然后跑：
```bash
pip install browser_cookie3
python3 scripts/setup_cookies.py     # 自动探测；或 --browser firefox 指定
```
脚本从**同一浏览器同一会话**取三件套（`sessdata`+`bili_jct`+`buvid3`，缺一或混源必 -101，见 `references/pitfalls.md` §8）、写入 credentials.json、并验真。过期了重跑同一条命令。

**撞墙症状（必认）**：`upload_one.py` 抛 `Expecting value: line 1 column 1` + `curl api.bilibili.com/x/web-interface/nav`
返 `isLogin: false` —— **几乎一定是本机 cookie 失效**（不是 B 站上游），先 `python3 scripts/setup_cookies.py` 重刷再说。
30 秒判定：
```bash
SESSDATA=$(python3 -c "import json,pathlib; print(json.loads(pathlib.Path('bilibili_uploader/credentials.json').read_text())['sessdata'])")
curl -sS -m 10 "https://api.bilibili.com/x/web-interface/nav" -b "SESSDATA=$SESSDATA" | python3 -c "import json,sys; print('isLogin:', json.load(sys.stdin)['data']['isLogin'])"
# false → 重刷 cookie；true → 才考虑按 §7 决策树查上游
```

### yt-dlp 公开下载无 IG 账号
对公开 Reel，yt-dlp **不需要任何 Instagram 登录态**——零封号风险。如果某个 shortcode 公开下载失败（罕见），脚本会原样报错，不会 fallback 到 Cookie 认证。

### 不做 4 类排除 / 不做去重
旧 skill 的"教程/BTS/广告/访谈"4 类排除**不在本 skill 范围内**。链接都是用户给的，用户已经知道内容。
同样的，本 skill **不做去重**——用户重复给链接就重复传（让用户自己发现）。
如果你**确实需要过滤**，在 agent 调 upload_one.py 之前自己加判断。

---

## 失败处理

| 现象 | 排查 |
|---|---|
| `yt-dlp` 报 HTTP 4xx/5xx | VPN/网络问题，确认能访问 instagram.com |
| `yt-dlp` 报 "Sign in to view" | 该 Reel 是非公开的，换链接 |
| `upload_one.py` 返 "video not found" | 没跑 `prepare_media.sh`，或 shortcode 拼错 |
| `upload_one.py` 返 "cookie expired" | `bilibili_uploader/credentials.json` 需要更新——在 Chrome 登录 B 站后用 `browser_cookie3` **三件套一起**提取。详见 `references/pitfalls.md` §6 §8 |
| `verify_upload.py` 返 PENDING | 正常，等 1-2 分钟再 retry |
| `verify_upload.py` 返 FAIL 多次 | B 站可能真把这条拒收了（站内外重复 / 版权）——别再传，告知用户 |
| `upload_one.py` 抛 `Expecting value: line 1 column 1` JSON 解析失败 | preupload 返了 HTML 不是 JSON。**先不要判定"CDN 抽风"**——按 `references/pitfalls.md` §7 决策树跑 Step 1-3 诊断：curl preupload 看状态码 + curl `api.bilibili.com/x/web-interface/nav` 验 `isLogin` 字段。**可能是 SESSDATA 空 / 三件套不配套（§8）/ skill 自带 cookie 是空（§9）/ ig-link-bili 池与主池不同步（见上方"credentials.json 与主池独立"pitfall）**，不一定都是 B 站上游问题。**必须先验登录态再归因**。 |

---

## 与原 `instagram-to-bilibili` skill 的关系

**原 skill（v1.5.0）**：自动抓 IG feed/hashtag + 阈值筛选 + cron 调度。**今天反复撞墙的部分**（login wall / yt-dlp 不支持列表 / WebBridge 行为古怪）全在这。

**本 skill（v1.1.0）**：用户给链接，下+译+传+验。不抓取、不筛选。

**两者并列存在**——根据场景选：
- 用户主动说"转载这条 IG 链接" → 用本 skill
- cron 跑 / 自动抓 → 用原 skill

> 注：`instagram-to-bilibili` 是作者本机的另一个 skill，分发包里**不含**它；本节仅说明定位差异。