# 人物说唱视频制作官 · mv-sing-opener-skill

**一张人物图 + 一条说唱音频 → 一条 9:16 的开口说唱视频。**

人物不换、场景不乱；**速度等于音频本身的速度，成片长度等于人声长度**；单镜不超过 30 秒，超过就按句间切点自动拆镜，**绝不提速**。

![十站流水线](docs/images/pipeline.png)

> 这是一个 **Agent Skill**，不是开箱即用的 SaaS。它把创作流程、提示词契约和脚本固定下来；你需要自备人物图、说唱音频，以及可用的图片 / 视频生成接口。

---

## 它做什么，不做什么

**做**：让图片里的同一个人，跟着你给的说唱音频开口，产出一条竖屏视频。支持 30 秒 / 40 秒档位，画幅默认 9:16，可选出字幕。没有音频时，先产出可直接复制的**海绵音乐提示词**，等用户出曲回传后再继续。

**不做**：整首歌 MV、多镜叙事、镜头切换、自己生成音频、歌曲下载 / 翻唱、视频素材处理。

边界收窄是有意的。对口型是「人物、声音、时间」三个变量必须同时成立的问题，功能每多一个，就多一个变量会松。

---

## 六条核心口径

1. **音频先行**：先有声音，再有时间轴，最后才是画面。反过来做，后期一定对不上。
2. **一个字都不改速**：不用 `atempo`，不靠提速把 40 秒压成 30 秒。超过单镜上限就按信息段拆镜。
3. **四个创作角色前置**：任务解读 → 创意总监 → 钩子官 → 词作者；一站一角色、一站一份文件，不许串岗。
4. **口型由参考音频驱动**：`generate_audio: false`，每镜 `ref_audio_urls` 恰好一条。
5. **零可读文字**：画面不出现文字、数字、字母、logo、水印、二维码；歌词只做可选后期字幕。
6. **没有音频就停在 ④**：先交付歌词＋出曲参数＋**海绵音乐提示词**；没有用户本次回传的音频，不进 ⑥⑦⑧，也**不许从旧项目复制音频**。

![按句间切点拆镜](docs/images/split.png)

---

## 十站流程

| 站 | 角色 | 产出 |
|---|---|---|
| ⓪ 建档 | 项目管家 | 项目状态 / 需求卡 / 过程记录 |
| ① 解读任务 | 任务解读官 | `01-解读/01-任务书.md` |
| ② 出方案 | 创意总监 | `02-方案/01-方案.md` |
| ③ 写钩子 | 钩子官 | `02-方案/02-钩子句.md` |
| ④ 写歌词 | 词作者 | `02-方案/03-歌词.md` |
| ⑤ 素材与出曲 | 素材官 | 参考图 / 逐镜音频 |
| ⑥ 上传外网 | 上传官 | `03-上传/素材外网路径.json` |
| ⑦ 时间轴 + 提示词 | 提示词官 | `04-提示词/分镜JSON.json` |
| ⑧ 出片合成 | 出片官 | `成片片段/SXX.mp4` → `06-MV成片.mp4` |
| ⑨ 质检交付 | 质检官 | `06-质检/检查报告.md`、`交付清单.md` |

四个硬门：**任务门 → 图门 → 音频门 → 上传门**。任一不过就停住，如实报错，不假装已完成。

---

## 适合谁

适合：有一张正面清晰的人物图、有一段 30–40 秒的说唱音频、想做竖屏人物开口视频的人；想靠换人物和主题批量做同构内容的人。

不适合：想做整首三分钟 MV、多镜叙事、镜头切换、3D 或精细手绘的人；想让它自己作曲、自己翻唱的人；想无人值守批量抽卡的人。

---

## 环境要求

- Python 3.9+
- `ffmpeg` / `ffprobe`
- 一个支持「参考图 + 参考音频」驱动口型的视频生成接口（默认适配 Seedance 2.5 的 reference 模式）
- 可选：一个 OpenAI 兼容的图片生成接口（没有人物图时用）
- 一个能把本地目录映射成公网 URL 的静态站点 / 对象存储 / Nginx 目录

```bash
# macOS
brew install ffmpeg
```

---

## 安装

```bash
git clone https://github.com/kongzichixiangjiao/mv-sing-opener-skill.git
cd mv-sing-opener-skill
pip install -r requirements.txt
```

把整个目录放进你的 agent skills 目录，或在项目里直接以它为工作目录。入口说明见 [`SKILL.md`](SKILL.md)。

---

## 配置

仓库只提交模板，不提交任何密钥。所有 key / 本地地址都放 `.env`：

```bash
cp env.example .env
# 编辑 .env
```

`.env` 已在 `.gitignore` 中，不会进 Git。脚本启动时会自动读取。

| 变量 | 说明 |
|---|---|
| `NEWAPI_IMAGE_BASE_URL` | OpenAI 兼容的图片接口地址（只在无图时需要） |
| `NEWAPI_IMAGE_KEY` | 图片接口 key；**只放 .env，不要提交** |
| `NEWAPI_IMAGE_MODEL` | 图片模型名 |
| `NEWAPI_IMAGE_QUALITY` | 图片质量 |
| `ASSET_URL_BASE` | 素材的公网根 URL，例如 `https://your-static-host.example.com/public/mv` |
| `ASSET_DEST_DIR` | 站点的磁盘目录，例如 `/var/www/public/mv` |
| `VIDEO_GATEWAY_BASE` | 视频生成网关地址 |
| `VIDEO_API_PREFIX` | 网关路径前缀，默认 `/v1`；直连其他路径时按网关文档改 |
| `VIDEO_MODEL` | 视频模型 ID |

`scripts/config.json` / `scripts/material-uploader/config.json` 是可选的本地配置，也已被 gitignore。不想用 `.env` 时可以复制对应的 `config.example.json`，但**不要把真实 key 写进任何会被提交的文件**。

`ASSET_DEST_DIR` 与 `ASSET_URL_BASE` 必须指向同一处：

```
本地 /var/www/public/mv/MV01-demo/04-图片/ref_人物.png
  ⇅
公网 https://your-static-host.example.com/public/mv/MV01-demo/04-图片/ref_人物.png
```

Nginx 示例：

```nginx
location /public/mv/ {
    alias /var/www/public/mv/;
    autoindex off;
}
```

> 上传后的素材是**公开可访问**的。不要传身份证、私密照、聊天截图或任何敏感文件。

---

## 快速开始

### 1. 建项目

```bash
python3 scripts/new_project.py --slug demo --duration 30 --image ~/Pictures/me.jpg
```

无图就省略 `--image`，后面按风格卡生成一张。

### 2. 对 agent 说

```text
继续这个项目：人物是<一个人物或主题>，说唱音频在 <路径>，
做成 9:16、30 秒、开口说唱的视频。
```

Agent 会从 ① 开始，一站一站停下来让你确认。想改哪一站就说「改方案」「换钩子」；想继续就说「下一步」。

### 3. 手动跑通后半程

```bash
P=assets/output/MV01-demo

# 上传（图 + 音频，硬门）
# 分镜 JSON 还没定稿时，先写一个只含 refs_urls / ref_audio_urls 的占位 JSON
python3 scripts/upload_project.py "$P" --verify --with-line-audio

# 写完分镜 JSON 后回填直链，不重传
python3 scripts/upload_project.py "$P" --fill-only
python3 scripts/upload_project.py "$P" --verify-json

# 干跑：只看请求体，不花钱
python3 scripts/generate_video.py "$P/04-提示词/分镜JSON.json" --dry-run

# 逐镜出片 → 合并 → 贴回原音轨
python3 scripts/generate_video.py "$P/04-提示词/分镜JSON.json"
python3 scripts/generate_video.py "$P/04-提示词/分镜JSON.json" --merge
python3 scripts/assemble.py "$P" --subtitle

# 质检
python3 scripts/qa.py "$P" --require-clip --verify-links
```

---

## 目录结构

```text
assets/output/MV01-demo/
├── 00-项目状态.md
├── 00-过程记录.md
├── 00-输入/
│   ├── 需求卡.md
│   ├── 素材/
│   └── 音频/
│       ├── S01.wav
│       ├── S02.wav
│       └── 原声-原始.wav
├── 01-解读/01-任务书.md
├── 02-方案/
│   ├── 01-方案.md
│   ├── 02-钩子句.md
│   ├── 03-歌词.md
│   ├── 05-海绵音乐提示词.md
│   └── 04-时间轴.md
├── 03-上传/素材外网路径.json
├── 04-图片/ref_人物.png
├── 04-提示词/
│   ├── 分镜JSON.json
│   └── 提示词-S01.md
├── 成片片段/S01.mp4
├── 06-MV成片.mp4
└── 06-质检/
    ├── 检查报告.md
    └── 交付清单.md
```

---

## 脚本

| 脚本 | 作用 |
|---|---|
| `new_project.py` | 建档：目录、状态、需求卡、过程记录、项目登记 |
| `log_step.py` | 每站追加一条过程记录；不写记录视为未完成 |
| `cut_audio.py` | 只做裁区间 + 补齐 + 末段淡出，**没有变速参数** |
| `generate_images.py` | 无人物图时按风格卡出参考图，默认一次一张 |
| `upload_project.py` | 上传参考图 / 音频，回填公网直链，HEAD 200 核验 |
| `generate_video.py` | 读分镜 JSON 逐镜出片；支持 `--dry-run`、`--only`、`--merge` |
| `assemble.py` | 贴回原音轨、精确裁秒、可选字幕 |
| `qa.py` | 查 JSON 契约、时长、直链、六段式标题、成片与音轨 |

成本纪律：**先 `--dry-run`，再出 1 条；不连出、不批量抽卡。** 不满意只重出有问题的那一镜。

---

## 为什么口型难

三个输入必须同时成立：

| 输入 | 决定什么 | 缺了会怎样 |
|---|---|---|
| 参考音频 | 什么时候开口、开合多大 | 全程闭嘴，或随机开合 |
| 参考图 | 这是谁、穿什么、在哪 | 换脸、换装、人物漂移 |
| 时间轴 | 每个字落在第几秒 | 嘴在动，但跟字对不上 |

这套流程的做法是：先锁音频和参考图，再把时间轴写成整数秒，最后用六段式提示词把可验收条件逐条写死。

30 秒的密字说唱是这套模型最难的一档。如果糊嘴、对不上，按顺序最多调两次：

1. 时间轴切得更碎（1–3 秒一块）
2. 提示词加强「逐字开合、不吞字、不连读」

仍不行就停下来，给三条降级路径：换更清晰的正面图；换慢一点的成曲（BPM 85–90）；改走多镜整首流程。**不要假装已经对上口型。**

---

## 常见故障

| 现象 | 处理 |
|---|---|
| 完全不动嘴 | 查 `ref_audio_urls` 是否恰好 1 条、`generate_audio` 是否 `false`、请求体是否有 `audio_url` |
| 嘴动但整体早 / 晚 | 时间轴起点没对齐首句；把第一块起点挪到真实首声 |
| 节奏对、字不对 | 歌词没加引号，或一块塞了太多字；补引号、拆 1–3 秒小段 |
| 后半段越来越飘 | 末块没收到该镜 `seconds`；原速重切，末块对齐 |
| 糊嘴 / 双嘴 | 重出同一条；负面清单加「糊嘴、双嘴、连读」 |
| 人物不像 / 换脸感 | 确认用的是用户图；逐项锁住脸、发型、服装、配饰；降低推近幅度 |
| 唱成旋律腔 | 明确写「说唱，不是旋律、不是念白」；负面加「旋律唱腔」 |
| 画面出现文字 / logo | 画风段加「零可读文字、无 logo」；重出 |
| 上传 404 | 命名空间＝项目文件夹名；图与音频都重跑 `--verify`；注意中文路径编码 |
| 只传音频后图片全 404 | 上传器 `overwrite_dir:true` 会先删整目录；整项目一起传，或加 `--no-overwrite-dir` |

---

## 隐私、版权与合规

- 本仓库**不包含**任何 API key、内部地址、真人照片、个人音频或样例成片；只保留 `docs/images/` 下两张风格卡生成的虚构人物示例图。
- `scripts/config.json`、`scripts/material-uploader/config.json`、`assets/output/` 默认被 `.gitignore` 忽略。
- 上传到公网的素材是公开的：不要传身份证、私密照、聊天截图、未公开的商业素材。
- 真人图片必须取得本人授权；不影射在世公众人物、明星、IP、品牌。
- 未成年人默认只做健康表达。
- 不克隆可识别真人的声音；不下载、不翻唱受版权保护的歌曲。
- 对外发布请标注 **AI 生成**。

---

## 项目状态

`v3.1.4`：流程、脚本、提示词契约和质检清单可用；新增无音频时的海绵音乐提示词输出与音频来源硬门。示例项目不随仓库发布（含个人音频与真人参考图），只保留两张风格卡生成的示例图。

出片需要你自己的视频网关和公网存储；没有网关时，最多跑到分镜 JSON。仓库不附带任何可用网关。

---

## 已知限制

- 只支持图片素材，不支持视频素材续写。
- 单镜 ≤ 30 秒；超过必须拆镜，拆镜后各镜用同一张参考图。
- 不做整首 MV、多镜叙事、镜头切换。
- 不生成音频；音频要你提供，或按 ④ 的**海绵音乐提示词**去外部出曲；回传后才继续。
- 出片依赖你自己的视频网关；仓库不附带任何可用网关。
- 不是无人值守的批量工具：每站都要确认，出片前要干跑。

---

## 文档

- [`SKILL.md`](SKILL.md) —— 完整流程、铁律、提示词模板、JSON 契约
- [`references/01-任务解读与方案.md`](references/01-任务解读与方案.md) —— 任务书、概念可行性、母题、选点
- [`references/02-钩子句.md`](references/02-钩子句.md) —— 原数字、生活落点、4 分制
- [`references/03-歌词写作.md`](references/03-歌词写作.md) —— 结构、押韵、字秒比、七问六刀
- [`references/09-海绵音乐提示词.md`](references/09-海绵音乐提示词.md) —— 无音频时的一段式出曲提示词、30s/40s 模板
- [`references/04-时间轴与字幕.md`](references/04-时间轴与字幕.md) —— 整数秒、ASR 对齐、字幕
- [`references/05-素材与上传.md`](references/05-素材与上传.md) —— 图片校验、音频只切不改速、上传
- [`references/06-提示词与出片.md`](references/06-提示词与出片.md) —— 六段式模板、JSON 契约、出片
- [`references/07-排障与质检.md`](references/07-排障与质检.md) —— 故障表、QA 清单、诚实降级
- [`references/08-公共经验.md`](references/08-公共经验.md) —— 10 条硬口径
- [`references/画面动态与感染力.md`](references/画面动态与感染力.md) —— 三层动态、画面事件
- [`references/对口型经验总结.md`](references/对口型经验总结.md) —— 口型三要素与实测复盘
- [`references/合规红线.md`](references/合规红线.md) —— 真人、IP、未成年人、AI 标识

示例参考图（由风格卡生成，不是真人）：

| 二郎神 | 哪吒 |
|---|---|
| ![二郎神](docs/images/example-laojun.jpg) | ![哪吒](docs/images/example-nezha.jpg) |

---

## English

An agent skill that turns **one character image + one rap vocal track** into a **9:16 lip-synced rap video**. The output length always equals the vocal length; anything over 30 seconds is split at sentence boundaries instead of being sped up. It includes a four-role writing pipeline, a six-section prompt contract, upload verification, rendering, and QA scripts. You provide the image, the audio, and your own model gateway.

---

## License

MIT. See [`LICENSE`](LICENSE).
