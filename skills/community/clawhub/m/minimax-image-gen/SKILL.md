---
name: minimax-image-gen
description: "使用 Minimax Image API 生成图片。支持文生图、13+ 种风格预设、跨平台。 neuroXY 专属画图技能！ Use when: 用户想生成图片、AI 画图、创建图像。 NOT for: 视频生成、动画制作。"
homepage: https://platform.minimaxi.com/docs/api-reference/image-generation-t2i
metadata:
  openclaw:
    emoji: "🎨"
    requires:
      bins: ["python3"]
      env: ["MINIMAX_API_KEY"]
    primaryEnv: MINIMAX_API_KEY
    install:
      - id: python-installed
        kind: note
        label: "Python 3 已预装 (OpenClaw 环境)"
---

# 🎨 minimax-image-gen

> **neuroXY 专属 AI 画图技能** | 基于 MiniMax Image API

[![GitHub](https://img.shields.io/badge/GitHub-neuroXY-blue)](https://github.com/Bluestar-34/neuroXY-space)
[![Version](https://img.shields.io/badge/Version-1.1.0-green)]()
[![Platform](https://img.shields.io/badge/Platform-Windows%2FMac%2FLinux-yellow)]()
[![License](https://img.shields.io/badge/License-MIT-orange)]()

## 📌 什么时候用

✅ **使用这个 skill：**
- "画一张图片"
- "生成一张可爱猫咪的照片"
- "用动漫风格画少女"
- "创建一个赛博朋克风格的城市图"

❌ **不要用这个 skill：**
- 视频生成 → 找其他工具
- 动画制作 → 找其他工具

## 🚀 快速开始

```bash
# 基本用法
python {baseDir}/scripts/gen.py -p "可爱的猫"

# 使用风格预设
python {baseDir}/scripts/gen.py -s "小猫" --preset 萌宠

# 生成并预览
python {baseDir}/scripts/gen.py -p "风景" --preview
```

## ⚙️ 配置

### API Key 配置

**方式一：环境变量（推荐）**
```powershell
# Windows
$env:MINIMAX_API_KEY = "your-api-key"

# Mac/Linux
export MINIMAX_API_KEY="your-api-key"
```

**方式二：OpenClaw 配置**
```json
{
  "skills": {
    "entries": {
      "minimax-image-gen": {
        "enabled": true,
        "env": {
          "MINIMAX_API_KEY": "your-key"
        }
      }
    }
  }
}
```

**方式三：自动加载**
本技能会自动从 `~/.openclaw/openclaw.json` 读取已配置的 Minimax API Key。

### 获取 API Key

访问：https://platform.minimaxi.com/user-center/interface-key

## 📖 使用指南

### 命令行参数

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--prompt` | `-p` | 图片描述（必填） | - |
| `--subject` | `-s` | 主体描述（用于预设） | - |
| `--count` | `-c` | 生成数量 (1-9) | 1 |
| `--aspect-ratio` | `-a` | 宽高比 | 1:1 |
| `--model` | `-m` | 模型 | image-01 |
| `--preset` | - | 风格预设 | - |
| `--style` | - | 风格类型 | - |
| `--out-dir` | `-o` | 输出目录 | ./output |
| `--preview` | - | 生成后预览 | false |
| `--list-presets` | - | 列出所有预设 | - |

### 宽高比选项

| 值 | 尺寸 | 适用场景 |
|----|------|----------|
| `1:1` | 1024×1024 | 头像、方形图 |
| `16:9` | 1280×720 | 壁纸、横幅 |
| `4:3` | 1152×864 | 照片 |
| `3:2` | 1248×832 | 摄影 |
| `2:3` | 832×1248 | 竖版人物 |
| `3:4` | 864×1152 | 竖版肖像 |
| `9:16` | 720×1280 | 手机壁纸 |
| `21:9` | 1344×576 | 超宽屏 |

### 模型说明

| 模型 | 说明 |
|------|------|
| `image-01` | 默认模型，高质量，支持所有宽高比 |
| `image-01-live` | 动漫/生活风格，支持风格参数 |

## 🎭 风格预设

本技能内置 **13 种** 精心调优的风格预设：

### 动漫/二次元
| 预设 | 说明 | 推荐宽高比 |
|------|------|------------|
| `动漫少女` | 动漫少女风格，大眼睛，精致五官 | 3:4 |
| `漫画风` | 漫画风格，简洁线条 | 1:1 |

### 艺术风格
| 预设 | 说明 | 推荐宽高比 |
|------|------|------------|
| `水彩画` | 水彩艺术风格，梦幻氛围 | 16:9 |
| `浮世绘` | 日本传统浮世绘风格 | 16:9 |
| `像素艺术` | 8-bit 复古游戏风格 | 1:1 |

### 人物/肖像
| 预设 | 说明 | 推荐宽高比 |
|------|------|------------|
| `证件照` | 专业证件照，白底 | 3:4 |
| `肖像` | 专业人像摄影，影棚灯光 | 3:2 |

### 创意/科幻
| 预设 | 说明 | 推荐宽高比 |
|------|------|------------|
| `赛博朋克` | 霓虹灯光，未来科技感 | 16:9 |

### 风景/建筑
| 预设 | 说明 | 推荐宽高比 |
|------|------|------------|
| `风景画` | 油画风格风景 | 16:9 |
| `建筑摄影` | 现代建筑摄影 | 3:2 |

### 动物/宠物
| 预设 | 说明 | 推荐宽高比 |
|------|------|------------|
| `萌宠` | 可爱宠物风格，大眼睛 | 1:1 |

### 产品/美食
| 预设 | 说明 | 推荐宽高比 |
|------|------|------------|
| `美食摄影` | 餐厅风格美食 | 1:1 |
| `产品图` | 商业产品摄影 | 1:1 |

### 使用预设

```bash
# 使用预设 + 主体
python gen.py -s "穿校服的少女" --preset 动漫少女

# 纯手动
python gen.py -p "赛博朋克城市" --preset 赛博朋克
```

### 仅 image-01-live 可用风格

| 风格值 | 说明 |
|--------|------|
| `漫画` | 漫画风格 |
| `元气` | 元气满满 |
| `中世纪` | 中世纪风格 |
| `水彩` | 水彩画风 |

## 💻 示例

### 示例 1：生成萌宠图片
```bash
python gen.py -s "英国短毛猫" --preset 萌宠 --preview
```

### 示例 2：创建风景壁纸
```bash
python gen.py -p "日落时的海滩" -a 16:9 -c 3 --preview
```

### 示例 3：动漫少女
```bash
python gen.py -s "粉色头发的女孩" --preset 动漫少女 --style 元气 --preview
```

### 示例 4：赛博朋克城市
```bash
python gen.py -p "未来的东京街头" --preset 赛博朋克 -c 4 --preview
```

### 示例 5：列出所有预设
```bash
python gen.py --list-presets
```

## 🔧 高级用法

### 自定义输出目录
```bash
python gen.py -p "图片" -o "E:/my-images"
```

### 禁用 Prompt 优化
```bash
python gen.py -p "具体描述" --no-optimizer
```

### 保存到指定位置并预览
```bash
python gen.py -p "猫" -o "C:/Users/asus/Pictures" --preview
```

## 📁 输出

- **目录**: `./output` (默认)
- **格式**: PNG
- **命名**: `minimax-{时间戳}-{描述}-{序号}.png`

## ⚠️ 错误处理

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 1002 | 限流 | 稍后重试 |
| 1004 | API Key 错误 | 检查 Key 是否正确 |
| 1008 | 余额不足 | 充值 |
| 1026 | 内容敏感 | 修改 prompt |
| 2013 | 参数错误 | 检查参数 |
| 2049 | 无效 API Key | 重新获取 Key |

## 🔐 安全特性

- ✅ 输入验证和清理
- ✅ API Key 不写入日志
- ✅ 敏感信息错误提示
- ✅ SSL/TLS 加密传输
- ✅ 超时保护

## 🌍 跨平台支持

| 平台 | 预览方式 |
|------|----------|
| Windows | 默认图片查看器 |
| macOS | Preview / Finder |
| Linux | xdg-open |

## 📝 更新日志

### v1.1.0 (2026-03-18)
- 🎉 添加 13 种风格预设
- ✨ 支持风格类型 (漫画/元气/中世纪/水彩)
- 🔧 优化跨平台兼容性
- 🛡️ 增强安全性
- 📖 完善文档

### v1.0.0 (2026-03-17)
- 🎨 初始版本
- ✨ 基本生成功能

## 📄 License

MIT License - Created by neuroXY

---

*有问题随时问 neuroXY！🦐*
