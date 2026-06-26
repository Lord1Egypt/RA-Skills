# LiblibAI Skill for OpenClaw

使用 LiblibAI 的强大图像生成能力，在 OpenClaw 中直接生成 AI 图像。

## 功能

- **文生图 (text2img)** - 从文本提示生成高质量图像
- **图生图 (img2img)** - 基于现有图像进行重绘或风格转换
- **Ultra 模型** - 使用更高品质的 Ultra 模型生成
- **ComfyUI 工作流** - 运行自定义 ComfyUI workflows
- **文件上传** - 上传本地文件供生成任务使用

## 快速开始

### 配置

设置环境变量：

```bash
export LIBLIBAI_ACCESS_KEY="your-access-key"
export LIBLIBAI_SECRET_KEY="your-secret-key"
```

### 生成图像

```bash
# 使用技能提供的 CLI
liblibai text2img -p "一只可爱的小狗" -W 1024 -H 1024 -s 20

# 上传文件
liblibai upload image.jpg

# 异步提交并等待
liblibai submit text2img -p "风景画"
liblibai wait <uuid>
```

## 参数说明

详见 SKILL.md 文档。

## 许可

MIT License
