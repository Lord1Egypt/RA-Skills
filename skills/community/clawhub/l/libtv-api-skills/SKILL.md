---
name: "libtv-api-skills"
description: "通过 liblib.tv 生成 AI 图片/视频"
---

# 🎬 LibTV API Skills

通过 LibLib.tv 的 AI 能力生成和编辑图片/视频。

## 📌 功能

覆盖场景：
- **文生图** - Text to Image
- **图生图** - Image to Image
- **文生视频** - Text to Video  
- **图生视频** - Image to Video
- **做动画** - Image Animation
- **画一个 xxx** - Custom drawing
- **来段 xxx** - Custom video

## 🛠️ 安装依赖

```bash
npm install -g @libtv/skills
```

或者直接安装 ClawHub 市场的版本。

## 💡 使用方法

### 1. 创建会话

```bash
# 登录 LibLib.tv
$ libtv login

# 创建一个新的创作会话
$ libtv session create --name "我的视频创作"
```

### 2. 生成图片

**文生图：**
```bash
$ libtv text2image --prompt "一个蓝色的小龙虾在吃虾" --size 1024x1024
```

**图生图：**
```bash
$ libtv image2image --prompt "换个风格，赛博朋克" --image ./avatar.jpg
```

### 3. 生成视频

**文生视频：**
```bash
$ libtv text2video --prompt "一只蓝色小龙虾在海底游泳" --duration 5s
```

**图生视频：**
```bash
$ libtv image2video --image ./avatar.jpg --prompt "让小龙虾动起来"
```

### 4. 查询进度

```bash
# 查看任务状态
$ libtv query --task-id xxxxx

# 或者实时查看
$ libtv status --follow
```

### 5. 下载结果

```bash
# 批量下载
$ libtv download --all
```

## 🔧 API 参考

### 核心 API 端点

| 方法 | 路径 | 功能 |
|------|------|------|
| POST | `/openapi/session` | 创建会话 / 发送消息 |
| POST | `/openapi/file/upload` | 上传文件到 OSS |
| GET | `/openapi/task/status` | 查询任务状态 |
| GET | `/openapi/file/download` | 下载结果文件 |

### 鉴权

使用 Bearer Token 鉴权：
```
Authorization: Bearer {token}
```

Token 通过登录流程获取。

## 🌐 相关链接

- LibLib.tv: https://www.liblib.tv
- GitHub: https://github.com/libtv-labs/libtv-skills
- API 文档：https://www.liblib.tv/docs/api
