# Nano-banana 图像生成与编辑 Skill

OpenClaw Agent Skill，使用 Nano-banana API 进行 AI 图像生成与编辑。

## ✨ 功能特性

- **文生图 (Text-to-Image)**: 根据文字描述生成图像
- **图生图 (Image-to-Image)**: 基于参考图生成新图像
- **自动压缩**: 超过 1MB 的图片自动压缩
- **飞书集成**: 生成的图片可直接在飞书中展示

## 📦 安装

### 方法一：使用 ClawHub（推荐）

```bash
clawhub install image-gen
```

### 方法二：手动安装

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/zweien/image-gen-skill.git image-gen
```

## ⚙️ 配置

在 OpenClaw workspace 目录下创建 `.env` 文件：

```bash
# ~/.openclaw/workspace/.env
IMAGE_API_BASE_URL=https://api.imyaigc.top
IMAGE_API_KEY=your-api-key-here
IMAGE_MODEL=gemini-3.1-flash-image-preview
IMAGE_SIZE=2K
IMAGE_ASPECT_RATIO=1:1
```

## 🚀 使用方法

### 文生图示例

```
生成一张夕阳下的海滩图片
画一只可爱的猫咪
创建一个赛博朋克风格的大龙虾，16:9 比例
```

### 图生图示例

```
基于这张图，改成水彩风格
把这张图改成夜景
参考这张图，生成一个类似风格的建筑
```

## 📐 支持的参数

### 宽高比 (aspect_ratio)
- `1:1` - 正方形（默认）
- `4:3`, `3:4` - 标准比例
- `16:9`, `9:16` - 宽屏/竖屏
- `2:3`, `3:2` - 照片比例
- `4:5`, `5:4` - 接近正方形
- `21:9` - 超宽屏

### 图像尺寸 (image_size)
- `1K` - 快速预览
- `2K` - 推荐默认
- `4K` - 高清大图
- `512px` - 小图

## 📁 目录结构

```
~/.openclaw/workspace/
├── img/                          # 生成的图片
│   ├── image_YYYYMMDD_HHMMSS_original.png  # 原始图片
│   └── image_YYYYMMDD_HHMMSS.png           # 压缩后
└── skills/
    └── image-gen/
        ├── SKILL.md              # Skill 说明
        ├── image-gen.sh          # 生成脚本
        ├── compress_image.py     # 压缩工具
        └── .env.example          # 配置示例
```

## 🔧 工作流程

### 文生图
1. 解析提示词和宽高比参数
2. 调用 Nano-banana API
3. 下载图片到 `workspace/img/`
4. 自动压缩（如需要）
5. 返回图片路径

### 图生图
1. 下载用户提供的参考图
2. 转换为 base64
3. 连同修改描述调用 API
4. 下载并保存生成结果

## 📝 注意事项

- 图片保存在 `~/.openclaw/workspace/img/` 目录
- 超过 1MB 自动压缩（原始文件保留）
- API 调用可能需要 30-60 秒
- 提示词会自动翻译为英文以获得更好效果

## 📄 License

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 🔗 相关链接

- [OpenClaw](https://github.com/openclaw/openclaw)
- [ClawHub](https://clawhub.com)
- [Nano-banana API](https://api.imyaigc.top)
