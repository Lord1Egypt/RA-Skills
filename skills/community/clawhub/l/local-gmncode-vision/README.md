# local-gmncode-vision

本技能为工作区内的通用识图兜底方案。

## 文件

- `SKILL.md`：调用说明
- 依赖脚本：`/home/ubuntu/.openclaw/workspace/scripts_gmncode_image.py`

## 快速测试

```bash
/home/ubuntu/.openclaw/workspace/scripts_gmncode_image.py /home/ubuntu/.openclaw/media/inbound/file.jpg "简要描述图像内容"
```

## 设计目的

当 OpenClaw 自带 `image` 工具因 provider 未注册、配置不完整或当前模型路由问题不可用时，仍然保留稳定可用的图片理解能力。
