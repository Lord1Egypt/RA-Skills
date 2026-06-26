# PicWish Skills

[English](README.md)

基于 [佐糖（PicWish）API](https://picwish.com) 的 OpenClaw Skills —— 11 个原子化图像处理技能。

## 功能列表

| 技能 | 说明 |
|---|---|
| `picwish-segmentation` | 智能抠图（人像、物体、印章） |
| `picwish-face-cutout` | 人脸 / 头像抠图 |
| `picwish-upscale` | 图像超分辨率增强 |
| `picwish-object-removal` | 基于蒙版的物体擦除 |
| `picwish-watermark-remove` | 自动水印检测与去除 |
| `picwish-id-photo` | 证件照生成 |
| `picwish-colorize` | 黑白照片上色 |
| `picwish-compress` | 图像压缩与尺寸调整 |
| `picwish-ocr` | OCR 文字识别 |
| `picwish-smart-crop` | 文档 / 物体透视矫正 |
| `picwish-clothing-seg` | 服装语义分割 |

## 快速开始

### 1. 前置要求

- Node.js ≥ 18
- 佐糖 API Key（[点此获取](https://picwish.com/my-account?subRoute=api-key)）

### 2. 配置 API Key

```bash
# 方式一：环境变量（推荐）
export PICWISH_API_KEY="your_api_key_here"

# 方式二：OpenClaw 配置
openclaw config set skills.entries.picwish.apiKey "your_api_key_here"
```

**中国大陆用户**还需设置区域：

```bash
export PICWISH_REGION=cn
```

### 3. 通过 ClawHub 安装

```bash
npm install -g clawhub
clawhub install picwish-skills
```

### 4. 使用示例

```bash
node scripts/run_task.mjs --skill picwish-segmentation --input-json '{"image_url":"https://example.com/photo.jpg"}'
node scripts/run_task.mjs --skill picwish-upscale --input-json '{"image_file":"/path/to/local.jpg","type":"clean"}'
```

## 项目结构

```
picwish-skills/
├── package.json
├── SKILL.md                  # 根路由技能
├── scripts/                  # 入口与辅助模块（已发布）
│   ├── run_task.mjs          # 统一入口
│   └── lib/
│       ├── client.mjs        # HTTP 客户端
│       ├── errors.mjs        # 错误分类
│       └── constants.mjs     # 基础 URL、轮询配置、状态码
└── skills/                   # 11 个子技能定义
    ├── picwish-segmentation/SKILL.md
    ├── picwish-face-cutout/SKILL.md
    └── ...
```

## 环境变量

| 变量名 | 说明 | 默认值 |
|---|---|---|
| `PICWISH_API_KEY` | API Key | — |
| `PICWISH_REGION` | `cn`（大陆）/ `global` | `global` |
| `PICWISH_BASE_URL` | 覆盖 API 端点 | — |
| `PICWISH_POLL_TIMEOUT_MS` | 视觉任务轮询超时 | `30000` |
| `PICWISH_OCR_TIMEOUT_MS` | OCR 任务轮询超时 | `120000` |
| `PICWISH_POLL_INTERVAL_MS` | 轮询间隔 | `1000` |

## 许可证

MIT
