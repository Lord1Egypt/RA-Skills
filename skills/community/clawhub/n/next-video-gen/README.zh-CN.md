# Next Video Gen 下一代视频生成

<p align="center">
  <strong>AI 图片/视频生成 via 火山引擎方舟平台 — 文生图、文生视频、图生视频、素材生视频，由 Seedance 2.0 驱动。</strong>
</p>

<p align="center">
  <a href="#功能介绍">功能</a> •
  <a href="#安装">安装</a> •
  <a href="#获取-api-key">API Key</a>
</p>

<p align="center">
  <strong>语言：</strong>
  <a href="README.md">English</a> |
  <a href="README.zh-CN.md">简体中文</a> |
  <a href="README.zh-TW.md">繁體中文</a>
</p>

---

## 功能介绍

适用于 AI 编程助手（Claude Code、Cursor 等）的图片/视频生成技能，基于火山引擎方舟平台的 Seedance 2.0 模型。

| 技能 | 描述 | 模型 |
|------|------|------|
| **Next Video Gen** | 文生图、文生视频、图生视频、素材生视频 | Seedance 2.0 |

---

## 安装

### 快速安装

```bash
openclaw skills add https://github.com/vennduan/next-video-gen
```

### 手动安装

```bash
git clone https://github.com/vennduan/next-video-gen.git
cd next-video-gen
openclaw skills add .
```

---

## 获取 API Key

1. 在 [console.volcengine.com/ark](https://console.volcengine.com/ark) 注册
2. 进入 API Keys 建立新密钥
3. 设置环境变量：

```bash
export DOUBAO_API_KEY=your_key_here
```

---

## 能力详情

- **文生图** — 文字描述生成高质量图片（PNG/JPEG/WebP）
- **文生视频** — 文字描述生成无声视频
- **文生视频（音画）** — 描述场景+声音，生成同步音视频（默认）
- **图生视频** — 图片 + 文字描述，生成无声视频
- **图生视频（音画）** — 图片 + 描述，生成带声音的视频（提供图片时默认）
- **素材生视频** — 视频 + 文字描述，基于已有视频素材生成新视频
- **多分辨率** — 图片：2K / 1K / HD；视频：480p / 720p / 1080p
- **弹性时长** — 视频 4–12 秒
- **多宽高比** — 图片：1:1 / 16:9 / 9:16；视频：16:9 / 9:16 / 1:1

### 使用示例

直接和代理对话：

> "生成一张未来城市日落的图片"

> "生成一个 5 秒的猫弹钢琴视频"

> "创建电影级海上日落画面，720p，16:9"

> "用这张图生成 8 秒的动画视频"

> "把这个视频处理成更鲜艳的色彩，加快节奏"

> "生成一个有欢快背景音乐和鸟叫声的视频"

代理会引导你补充缺失信息并处理生成。

### 系统需求

- 系统已安装 `curl` 和 `jq`
- 已设定 `DOUBAO_API_KEY` 环境变量

### 脚本参考

技能包含 `scripts/seedance-gen.sh` 供命令行直接使用：

```bash
# 文生图
./scripts/seedance-gen.sh "未来城市日落，霓虹灯闪烁" --mode txt2img

# 文生大图
./scripts/seedance-gen.sh "抽象艺术，鲜艳色彩" --mode txt2img --quality 2K

# 文生音画（默认，带声音）
./scripts/seedance-gen.sh "一只猫在草地上奔跑，阳光明媚，有鸟叫" --mode txt2video --duration 5

# 文生视频（无音频）
./scripts/seedance-gen.sh "海上日落延时摄影" --mode txt2video --no-audio

# 图生音画（默认，带声音）
./scripts/seedance-gen.sh "镜头缓慢推进，猫咪转身看向镜头" --mode img2video --image "https://example.com/cat.jpg"

# 图生视频（无音频）
./scripts/seedance-gen.sh "图片动起来" --mode img2video --image "https://example.com/img.jpg" --no-audio

# 素材生视频
./scripts/seedance-gen.sh "色彩更鲜艳，加快节奏" --mode vid2video --video "https://example.com/input.mp4"

# 指定分辨率和时长
./scripts/seedance-gen.sh "无人机航拍山谷" --mode txt2video --duration 8 --quality 1080p

# 竖屏视频
./scripts/seedance-gen.sh "瀑布流淌" --mode txt2video --aspect-ratio 9:16

# 关闭水印
./scripts/seedance-gen.sh "抽象艺术动画" --mode txt2video --watermark false
```

内容保存至 `~/Videos/next-video-gen/`（可透过 `NEXT_VIDEO_GEN_OUTPUT_DIR` 设定）。

### API 参数

完整 API 文档见 [references/api-params.md](references/api-params.md)。

---

## 文件结构

```
.
├── README.md                    # English
├── README.zh-CN.md              # 本文件（简体中文）
├── README.zh-TW.md              # 繁体中文
├── SKILL.md                     # 技能定义
├── _meta.json                   # 技能元数据
├── references/
│   └── api-params.md            # 完整 API 参数文档
└── scripts/
    └── seedance-gen.sh          # 生成脚本
```

---

## 常见问题

| 问题 | 解决方案 |
|------|---------|
| `jq: command not found` | 安装 jq：`apt install jq` / `brew install jq` |
| `401 Unauthorized` | 检查 `DOUBAO_API_KEY`，前往 [console.volcengine.com/ark](https://console.volcengine.com/ark) 确认 |
| `403 Forbidden` | 在火山引擎控制台检查 API 密钥权限 |
| `429 Too Many Requests` | 请求频率过高，稍等后重试 |
| 内容被拦截 | 修改提示词后重试 |
| 生成超时 | 视频通常需 1–3 分钟，图片通常 5–15 秒 |

---

## 授权条款

MIT
