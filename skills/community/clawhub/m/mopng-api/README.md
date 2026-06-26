# mopng-api

MoPNG API Skill for OpenClaw - 使用 mopng.cn API 进行图片处理。

## 功能

- **智能抠图** (`remove-bg`) - 自动去除图片背景
- **高清放大** (`upscale`) - 图片无损放大 2x/4x
- **智能扩图** (`outpainting`) - AI 智能扩展图片边界
- **图片翻译** (`translation`) - 翻译图片中的文字
- **文生图** (`text-to-image`) - 从文本描述生成图片
- **图生图** (`image-to-image`) - 基于参考图生成新图片

## 安装与配置

### 1. 安装 Skill（OpenClaw / Claude Code / Cursor）

在对应客户端中执行（对话命令或技能安装入口因产品而异，以各产品文档为准）：

```
/skill add https://raw.githubusercontent.com/jkin8010/mopng-api/refs/heads/main/SKILL.md

# 或

/skill add https://gitee.com/jkin8010/mopng-api/raw/main/SKILL.md
```

**前置依赖：** 本 Skill 需要 `uv` 与 `python3` 已安装；详见仓库根目录 [SKILL.md](https://github.com/jkin8010/mopng-api/blob/main/SKILL.md) 中的 metadata。

### 2. 获取 API Key

1. 打开 [https://mopng.cn/agent](https://mopng.cn/agent) 并登录  
2. 创建 **API Key**，复制备用  

### 3. 配置 `MOPNG_API_KEY`（私密配置，勿入对话）

**请勿在 AI 对话、工单、截图或公开仓库中粘贴 API Key。** 聊天与日志可能被保留；把密钥交给模型「代为写入环境」会增加泄露面，也不是使用本 API 的技术前提。

推荐做法：

1. **OpenClaw / 支持 JSON 配置的客户端：** 在本机配置文件的 `env` 段写入密钥（该文件勿提交 Git）。示例（占位符请换成你的密钥）：

```json
{
  "env": {
    "MOPNG_API_KEY": "<在此填入密钥，仅保存在本机>"
  }
}
```

2. **本机 Shell：** `export MOPNG_API_KEY='...'`（仅当前会话）或写入只对当前用户可读的配置文件。

3. **本地开发 / 克隆仓库：** 在项目根目录 `.env` 中设置 `MOPNG_API_KEY`（本仓库 `.gitignore` 已忽略 `.env`），或结合 `uv`/IDE 的 env 注入能力；确保 Python 3.10+ 与 `uv` 可用。

运行由 OpenClaw 托管时，宿主通常会设置 `OPENCLAW_WORKSPACE` 以限制可读写的路径；技能元数据与 `scripts/mopng_api.py` 会读取该变量。你可从仓库根目录 [SKILL.md](https://github.com/jkin8010/mopng-api/blob/main/SKILL.md) 查看完整说明。

## Claude 命令使用示例

### 智能抠图

```
remove-bg ./photo.jpg
```

```
remove-bg ./photo.jpg --output ./result.png --async-mode
```

### 高清放大

```
upscale ./photo.jpg --scale 2
```

```
upscale ./photo.jpg --scale 4 --tile-size 192 --tile-pad 24 --async-mode
```

### 智能扩图

```
outpainting ./photo.jpg --direction all --expand-ratio 0.5
```

```
outpainting ./photo.jpg --direction right --expand-ratio 0.3 --best-quality
```

### 图片翻译

```
translation ./photo.jpg --target-language en
```

```
translation ./photo.jpg --target-language ja --source-language zh
```

### 文生图

```
text-to-image --prompt "一只红嘴蓝鹊站在树枝上"
```

```
text-to-image --prompt "赛博朋克风格的未来城市" --output ./cyberpunk.png --model wanx-v2.5
```

### 图生图

```
image-to-image --input ./photo.jpg --prompt "把天空变成日落金色"
```

```
image-to-image --input ./portrait.jpg --prompt "转换为油画风格" --strength 0.7 --output ./portrait_oil.png
```

### 查看可用模型

```
list-models --type text_to_image
```

```
list-models --type image_to_image
```

## 命令参数速查

| 命令 | 必填参数 | 常用可选参数 |
|------|----------|--------------|
| `remove-bg` | `--input` | `--output`, `--output-format`, `--async-mode` |
| `upscale` | `--input` | `--output`, `--scale`, `--tile-size`, `--tile-pad`, `--async-mode` |
| `outpainting` | `--input` | `--output`, `--direction`, `--expand-ratio`, `--best-quality` |
| `translation` | `--input`, `--target-language` | `--output`, `--source-language` |
| `text-to-image` | `--prompt` | `--output`, `--model`, `--width`, `--height`, `--negative-prompt` |
| `image-to-image` | `--input`, `--prompt` | `--output`, `--strength`, `--model`, `--negative-prompt` |

## 使用技巧

### 1. 简化路径输入

Claude 会自动处理路径，可以直接输入：
```
remove-bg photo.jpg
```

### 2. 异步模式

对于耗时操作（抠图、放大），建议使用 `--async-mode`：
```
upscale photo.jpg --scale 2 --async-mode
```

### 3. 指定输出路径

默认会保存到工作区目录，也可以指定完整路径：
```
text-to-image --prompt "小猫" --output ./images/kitten.png
```

### 4. 图生图强度控制

`--strength` 参数控制变化程度：
- 0.3-0.5: 轻微变化，保留原图特征
- 0.6-0.8: 中等变化，风格转换
- 0.9-1.0: 大幅变化，仅保留构图

## 测试与安全扫描

```bash
uv sync
uv run pytest tests/ -v
uv run bandit -r scripts -ll
```

合并到 `main` 时 GitHub Actions 会运行上述 `pytest` 与 `bandit`（见 `.github/workflows/ci.yml`）。运行时仅依赖 Python 标准库，**无 PyPI 运行时依赖**；`pyproject.toml` 中的依赖列表为空属于刻意设计。

## API 文档

详见 [mopng.cn/agent/docs](https://mopng.cn/agent/docs)

## 许可证

MIT
