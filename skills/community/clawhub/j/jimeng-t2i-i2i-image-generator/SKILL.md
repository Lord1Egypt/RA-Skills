---
name: jimeng
description: Use Jimeng AI 4.0 (Volcengine) to generate images from text or image references, and optionally send results to Feishu.
---

# Jimeng AI 4.0 图片生成 Skill

使用火山引擎即梦AI 4.0 生成图片。

## 环境变量

```bash
export VOLCENGINE_AK="你的AccessKeyID"
export VOLCENGINE_SK="你的SecretAccessKey"
```

## 使用方式

```bash
./jimeng.sh <mode> <prompt> [reference_url] [target] [options]
```

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| mode | ✅ | `t2i` (文生图) 或 `i2i` (图生图) |
| prompt | ✅ | 图片描述 |
| reference_url | 图生图时可选 | 参考图片URL，不填则使用默认图片 |
| target | 可选 | 飞书用户ID，如 `user:ou_xxx`，不填则只输出URL |
| options | 可选 | 额外选项，如 `force_single=true` |

## 示例

### 文生图 (t2i)

```bash
# 文生图 - 生成一只可爱的猫咪
./jimeng.sh t2i "一只可爱的猫咪"

# 文生图 - 发送给飞书用户
./jimeng.sh t2i "蓝天白云" "user:ou_5ab7e4d11d7f28bebff34796cc967e24"

# 文生图 + 参考风格图
./jimeng.sh t2i "变成油画风格" "https://example.com/style.jpg"
```

### 图生图 (i2i)

```bash
# 图生图 - 使用默认参考图（Clawra头像）
./jimeng.sh i2i "戴上墨镜"

# 图生图 - 使用默认参考图
./jimeng.sh i2i "变成卡通风格"

# 图生图 - 自定义参考图
./jimeng.sh i2i "把这张照片变成素描风格" "https://example.com/photo.jpg"

# 图生图 - 发送给飞书用户
./jimeng.sh i2i "戴上牛仔帽" "" "user:ou_xxx"
```

## 默认参考图

图生图模式默认使用 Clawra 头像作为参考：
```
https://cdn.jsdelivr.net/gh/SumeLabs/clawra@main/assets/clawra.png
```

## 输出说明

- 直接运行：输出图片URL
- 指定 target：自动发送到飞书

## 图片格式

- 即梦AI 默认输出 **PNG 格式**
- URL 后缀是 `.image`，飞书可以正常发送
- 用户保存：复制链接后把 `.image` 改成 `.png`

## 文件结构

```
jimeng/
├── SKILL.md      # 本文件
└── scripts/
    ├── sign.py   # 火山引擎签名
    └── jimeng.sh # 主脚本
```
