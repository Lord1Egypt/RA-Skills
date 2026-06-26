---
name: kay-video-upload
description: 多平台短视频自动发布工具，支持抖音、视频号、快手、小红书、B站。当用户说"发布视频"、"上传视频到抖音/小红书/视频号/快手/B站"、"把视频发到所有平台"、"登录抖音"、"视频发布"等时使用此 skill。底层使用 Playwright + 本机 Chrome 操作各平台创作者后台完成自动发布，所有代码自包含在 scripts/ 目录，可直接复制到任意 OpenClaw 实例使用。
---

# video-publisher

完全自包含的多平台短视频发布 skill。所有代码在 `scripts/` 目录内，无外部依赖路径。

## 目录结构

```
scripts/
├── publish.py          # 统一入口（登录 + 发布）
├── setup.py            # 首次安装向导（检测 Chrome、安装依赖）
├── conf.py             # 配置（Chrome 路径由 setup.py 自动写入）
├── videos/             # 待发布视频放这里
├── cookies/            # 各平台登录状态（自动生成）
├── uploader/           # 各平台发布模块（来自 SAU）
│   ├── douyin_uploader/
│   ├── tencent_uploader/
│   ├── ks_uploader/
│   ├── xhs_uploader/
│   └── bilibili_uploader/
└── utils/              # 工具模块
```

## 视频目录规范

默认在 `scripts/videos/` 下放置视频，也可通过环境变量 `VIDEO_DIR` 指定其他目录：

```bash
export VIDEO_DIR=/path/to/your/videos  # Linux/macOS
$env:VIDEO_DIR = "E:\openclaw\video"   # Windows PowerShell
```

视频文件格式：
```
视频名.mp4       # 视频（必须）
视频名.txt       # 第一行标题，第二行 #标签1 #标签2（必须）
视频名.png       # 封面图（可选）
```

## 首次安装

```bash
cd scripts/
python setup.py
```

自动完成：检测 Chrome 路径、安装 playwright/biliup 等依赖、写入 conf.py。

## 常用操作

### 登录（每个平台首次或 cookie 过期时执行一次）
```bash
python publish.py login douyin    # 抖音（扫码）
python publish.py login tencent   # 视频号（微信扫码）
python publish.py login ks        # 快手（扫码）
python publish.py login xhs       # 小红书（手动登录后按 Enter）
python publish.py login bilibili  # B站（biliup 扫码）
```

### 发布
```bash
python publish.py run douyin      # 发布到抖音
python publish.py run tencent     # 发布到视频号
python publish.py run ks          # 发布到快手
python publish.py run xhs         # 发布到小红书
python publish.py run bilibili    # 发布到B站
python publish.py run all         # 发布到所有已登录平台
```

## 通过 OpenClaw 使用

直接说：
- "发布视频到抖音"
- "把 videos 里的视频发到所有平台"
- "抖音 cookie 过期了，重新登录"

OpenClaw 会自动定位到 skill 的 `scripts/` 目录执行对应命令。

## Agent 操作规范

1. 用户说"发布视频到 X 平台"
2. 检查 `scripts/cookies/<platform>_uploader/account.json` 是否存在
3. 不存在 → 执行 `python publish.py login <platform>`，告知用户扫码
4. 存在 → 执行 `python publish.py run <platform>`
5. 观察输出，完成后告知用户结果

执行命令时需先设置 Python 路径（Windows）：
```powershell
$env:PATH = '<python_dir>;<python_scripts_dir>;' + $env:PATH
python publish.py run douyin
```

详细平台说明见 `references/platforms.md`
