# kay-video-upload

多平台短视频自动发布工具，支持抖音、视频号、快手、小红书、B站。

## 特性

- 🚀 一键发布到 5 大平台
- 🔐 扫码登录，cookie 自动保存（有效期 30 天）
- 📁 完全自包含，无外部路径依赖
- 🎯 支持标题、标签、封面、定时发布
- 🛠️ 基于 Playwright + 本机 Chrome，稳定可靠

## 支持平台

| 平台 | 登录方式 | 定时发布 | 封面 | 商品链接 |
|------|----------|----------|------|----------|
| 抖音 | 扫码 | ✅ | ✅ | ✅ |
| 视频号 | 微信扫码 | ✅ | ✅ | ❌ |
| 快手 | 扫码 | ✅ | ❌ | ❌ |
| 小红书 | 手动登录 | ❌ | ✅ | ❌ |
| B站 | biliup 扫码 | ✅ | ❌ | ❌ |

## 快速开始

### 1. 安装

```bash
cd scripts/
python setup.py
```

自动完成：
- 检测本机 Chrome 路径
- 安装依赖（playwright、biliup 等）
- 配置 conf.py

### 2. 准备视频

在 `scripts/videos/` 目录（或通过环境变量 `VIDEO_DIR` 指定）下放置：

```
视频名.mp4       # 视频文件（必须）
视频名.txt       # 第一行标题，第二行 #标签1 #标签2（必须）
视频名.png       # 封面图（可选）
```

示例 `demo.txt`：
```
这是视频标题
#AI #科技 #教程
```

### 3. 登录平台

```bash
python publish.py login douyin    # 抖音
python publish.py login tencent   # 视频号
python publish.py login ks        # 快手
python publish.py login xhs       # 小红书
python publish.py login bilibili  # B站
```

每个平台只需登录一次，cookie 有效期约 30 天。

### 4. 发布视频

```bash
python publish.py run douyin      # 发布到抖音
python publish.py run all         # 发布到所有已登录平台
```

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `VIDEO_DIR` | 视频目录 | `scripts/videos/` |
| `CHROME_PATH` | Chrome 路径 | 自动检测 |
| `XHS_SERVER` | 小红书签名服务 | `http://127.0.0.1:11901` |

示例：
```bash
export VIDEO_DIR=/path/to/videos  # Linux/macOS
$env:VIDEO_DIR = "E:\videos"      # Windows PowerShell
```

## 在 OpenClaw 中使用

安装 skill 后，直接对话：

```
发布视频到抖音
把 videos 里的视频发到所有平台
抖音 cookie 过期了，重新登录
```

OpenClaw 会自动调用此 skill 完成操作。

## 注意事项

- 小红书需要额外的 XHS_SERVER 签名服务（可用 Docker 启动）
- 发布期间不要关闭自动弹出的 Chrome 窗口
- 定时发布默认从明天 16:00 开始，每天一条
- B站每条视频之间自动等待 30 秒（平台限速）

## 目录结构

```
scripts/
├── publish.py              # 统一入口
├── setup.py                # 安装向导
├── conf.py                 # 配置文件
├── videos/                 # 视频目录
├── cookies/                # 登录状态（自动生成）
├── uploader/               # 各平台模块
│   ├── douyin_uploader/
│   ├── tencent_uploader/
│   ├── ks_uploader/
│   ├── xhs_uploader/
│   └── bilibili_uploader/
└── utils/                  # 工具模块
```

## 依赖

- Python 3.10+
- playwright
- biliup
- loguru
- requests

由 `setup.py` 自动安装。

## License

MIT

## 致谢

基于 [social-auto-upload](https://github.com/dreammis/social-auto-upload) 的 uploader 模块构建。
