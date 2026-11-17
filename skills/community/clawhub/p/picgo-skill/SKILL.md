---
name: picgo-skill
description: 调用本地 PicGo 服务上传本地图片。当用户需要上传图片时使用。
allowed-tools: Bash, Write, Read
---

# PicGo 图片上传

通过本地 PicGo 服务 API 上传本地图片。

## 依赖安装

```bash
pip install requests
```

## 使用方法

```bash
python3 ~/.openclaw/skills/picgo-skill/picgo_skill.py "图片路径1" [图片路径2] [图片路径3...]
```

## 环境变量

可选：设置 `PICGO_SERVER_URL` 指定 PicGo 服务地址（默认：http://127.0.0.1:36677）。

## 使用示例

```bash
python3 ~/.openclaw/skills/picgo-skill/picgo_skill.py "C:/Users/XIAOREN/.openclaw/workspace/cat_couplets.jpg"
python3 ~/.openclaw/skills/picgo-skill/picgo_skill.py "C:/img1.jpg" "D:/img2.png"
```

## 注意事项

- 超时时间：30 秒
- 支持同时上传多张图片
- 使用前请确保 PicGo Server服务已正常启动