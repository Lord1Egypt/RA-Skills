---
name: Nano-Banana-Cut
description: AI图片生成与智能切割工具，基于AceData Nano Banana模型，支持多分辨率多尺寸生成，自动切割为2/4/6/9宫格，自带瀑布流作品管理、批量下载功能。使用场景：(1) 输入prompt生成AI图片并自动切割成九宫格等多宫格 (2) 上传图片进行智能多宫格切割 (3) 管理生成的图片作品，支持打包下载
---

# Nano-Banana-Cut AI图片生成切割工具

## 📖 功能说明

banana-cut 是一个功能强大的 AI 图片生成与智能切割工具，基于 AceData Nano Banana 系列模型，提供完整的 Web 界面进行图片生成、切割和管理。

### 核心功能

#### 🎨 图片生成
- **多种模型支持**：Nano Banana Pro、Nano Banana 2
- **多种分辨率**：1:1（方形）、16:9（横屏）、9:16（竖屏）、4:3（标准）、3:4（竖版）
- **多种质量**：1K (1024px)、2K (2048px)、4K (4096px)
- **图生图**：支持最多上传 6 张参考图进行图片编辑

#### ✂️ 智能切割
- **多种宫格**：支持 2/4/6/9 宫格切割
- **智能适配**：自动识别横竖比例，智能选择最佳切割方式
- **独立工具**：提供独立的切割 API，可单独使用

#### 🖼️ 作品管理
- **瀑布流展示**：自动适配不同图片比例，美观展示所有作品
- **缩略图生成**：自动生成 480P 缩略图
- **批量下载**：支持 ZIP 打包下载（原图 + 切割图 + 缩略图 + 生成信息）
- **文件管理**：一键打开文件目录

#### 🎯 任务管理
- **多任务并发**：支持多个任务同时轮询，互不阻塞
- **智能轮询**：第一次延迟 1 分钟，之后每 30 秒查询一次
- **任务恢复**：服务重启后自动恢复未完成任务
- **错误重试**：失败任务支持一键重新获取

#### 🎨 用户体验
- **双主题**：支持亮色/暗色主题切换
- **实时预览**：图片预览、切割图预览
- **本地存储**：自动保存用户配置（模型、分辨率、质量、宫格数）

---

## 🚀 快速开始

### 1. 启动服务

```bash
cd C:\Users\86137\.openclaw\workspace\skills\banana-cut
python server.py
```

访问地址：http://localhost:697

### 2. 配置 API 密钥

首次访问会自动弹出配置窗口，需要填写：

- **API_KEY（必填）**：用于图片生成功能
- **PLATFORM_TOKEN（可选）**：仅图生图/图片编辑功能需要

**获取密钥**：https://share.acedata.cloud/r/1uN88BrUTQ

配置会保存到 `.env` 文件中。

### 3. 生成图片

1. 输入提示词（支持中英文）
2. 选择模型、分辨率、质量
3. 选择宫格数（1/2/4/6/9）
4. 点击生成按钮
5. 等待任务完成（前端自动轮询）

### 4. 图生图（可选）

1. 点击左下角图片图标上传参考图（最多 6 张）
2. 输入提示词描述编辑需求
3. 点击生成按钮

---

## 📁 文件结构

```
banana-cut/
├── server.py              # Flask 主服务器
├── task.py                # 独立任务处理脚本
├── cut.py                 # 图片切割工具
├── upload.py              # 图片上传工具
├── set.json               # 配置文件（模型、分辨率、质量）
├── prompt.md              # 提示词模板
├── .env                   # 环境变量（API密钥）
├── .env.example           # 环境变量示例
├── SKILL.md               # 本文档
├── data/
│   └── works.db           # SQLite 数据库
└── templates/
    ├── index.html         # 主页面（瀑布流）
    └── admin.html         # 管理后台
```

---

## ⚙️ 配置说明

### set.json 配置文件

```json
{
  "server": {
    "url": "https://api.acedata.cloud/nano-banana/images",
    "task_url": "https://api.acedata.cloud/nano-banana/tasks",
    "upload_url": "https://platform.acedata.cloud/api/v1/files/",
    "apikey": ""
  },
  "models": [
    {"name": "Nano Banana Pro", "model": "nano-banana-pro", "logo": "🍌"},
    {"name": "Nano Banana 2", "model": "nano-banana-2", "logo": "🍌"}
  ],
  "resolutions": [
    {"name": "1:1 方形", "ratio": "1:1", "icon": "■"},
    {"name": "16:9 横屏", "ratio": "16:9", "icon": "▬"},
    {"name": "9:16 竖屏", "ratio": "9:16", "icon": "▮"},
    {"name": "4:3 标准", "ratio": "4:3", "icon": "▭"},
    {"name": "3:4 竖版", "ratio": "3:4", "icon": "▯"}
  ],
  "qualities": [
    {"name": "1K (1024px)", "size": "1K", "icon": "🖥️"},
    {"name": "2K (2048px)", "size": "2K", "icon": "🖥️"},
    {"name": "4K (4096px)", "size": "4K", "icon": "🖥️"}
  ],
  "save_path": "C:/Users/86137/Desktop/banana"
}
```

**注意事项**：
- `apikey` 字段已废弃，请使用 `.env` 文件配置
- `save_path` 可自定义图片保存路径

### .env 环境变量

```bash
# 请访问 https://share.acedata.cloud/r/1uN88BrUTQ 获取以下配置
API_KEY=your-api-key-here
PLATFORM_TOKEN=your-platform-token-here
```

### prompt.md 提示词模板

生成图片时会自动读取该文件，将 `{num}` 替换为选择的宫格数，可自定义模板内容。

```markdown
##生成要求：##
严格生成一张{num}宫格的高质量图片，每个格子的内容根据输入的提示词完全独立...

##用户要求：##
{prompt}
```

---

## 🗄️ 数据库结构

数据库文件：`data/works.db`

### works 表结构

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| model | TEXT | 使用的模型 |
| date | TEXT | 生成日期，格式 YYYY-MM-DD HH:MM:SS |
| state | INTEGER | 状态：1=生成中，10=成功，99=失败，0=文件丢失 |
| prompt | TEXT | 生成提示词 |
| ratio | TEXT | 分辨率比例 |
| quality | TEXT | 图片质量 |
| task_id | TEXT | 模型返回的任务ID |
| num | INTEGER | 切割宫格数：1/2/4/6/9 |
| path | TEXT | 保存目录路径 |
| filename | TEXT | 主图文件名 |
| ext | TEXT | 图片扩展名 |
| request_data | TEXT | 请求参数JSON |
| error | TEXT | 错误信息 |
| respond | TEXT | 接口返回内容JSON |

---

## 💾 保存目录结构

每个生成任务会创建独立目录：`保存路径/YYYYMMDDHHMMSS/`

目录下包含：
- `main.ext`：生成的原始主图
- `480p.ext`：480P 缩略图
- `1.ext` ~ `n.ext`：切割后的子图（n=宫格数）
- `data.txt`：生成信息和参数说明

---

## 🔌 API 接口

### 配置相关

#### GET /api/config/check
检查配置状态

**返回**：
```json
{
  "success": true,
  "msg": "配置正常"
}
```

#### POST /api/config/save
保存配置

**参数**：
```json
{
  "api_key": "your-api-key",
  "platform_token": "your-platform-token"
}
```

#### GET /api/config
获取配置（模型、分辨率、质量）

### 图片生成

#### POST /api/generate
生成图片

**参数**：
```json
{
  "prompt": "图片描述",
  "model": 0,
  "ratio": 0,
  "quality": 1,
  "num": 9,
  "images": []
}
```

**返回**：
```json
{
  "success": true,
  "msg": "任务提交成功",
  "work_id": 1
}
```

#### GET /api/poll/:id
轮询任务状态

**返回**：
```json
{
  "success": true,
  "data": {
    "state": 10,
    "error": "",
    "task_id": "xxx",
    "respond": {}
  }
}
```

### 作品管理

#### GET /api/works
获取所有作品列表

#### GET /api/work/:id
获取单个作品详情

#### GET /api/download/:id
打包下载作品

#### POST /api/open-folder/:id
打开文件目录

### 图片上传

#### POST /api/upload
上传图片（需要 PLATFORM_TOKEN）

### 图片切割

#### POST /api/cut
切割图片

**参数**：
```json
{
  "path": "图片路径",
  "num": 9,
  "out": "输出目录（可选）"
}
```

### 管理接口

#### GET /api/admin/works
获取所有任务（管理后台）

#### POST /api/admin/retry/:id
重试任务

#### POST /api/admin/close/:id
关闭任务

#### POST /api/admin/delete/:id
删除任务

#### POST /api/shutdown
关闭服务

---

## 🛠️ 独立工具使用

### cut.py - 图片切割工具

```bash
python cut.py -path 图片路径 -num 9 [-out 输出目录]
```

**参数**：
- `-path`：图片路径（必填）
- `-num`：宫格数 2/4/6/9（必填）
- `-out`：输出目录（可选，默认原图片目录）

### task.py - 任务处理工具

```bash
python task.py -id 任务ID
python task.py -task_id 模型任务ID
```

**参数**：
- `-id`：数据库任务ID
- `-task_id`：模型返回的任务ID
- `-num`：宫格数（可选，默认读取数据库）

### upload.py - 图片上传工具

```bash
python upload.py -file 图片路径
```

---

## 🎯 使用场景

### 场景1：生成九宫格图片
1. 打开 http://localhost:697
2. 输入提示词："生成一张3x3九宫格电影海报图片"
3. 选择 9 宫格
4. 点击生成
5. 等待完成，查看瀑布流展示

### 场景2：图生图编辑
1. 上传参考图（最多6张）
2. 输入描述："参考原图风格，生成..."
3. 点击生成
4. 查看结果

### 场景3：管理已生成作品
1. 点击作品查看详情
2. 下载 ZIP 打包
3. 打开文件目录
4. 以图生图

### 场景4：失败任务重试
1. 切换到错误记录视图（导航栏感叹号按钮）
2. 点击失败任务查看详情
3. 点击"重新获取"
4. 查看实时日志

---

## 🔧 故障排除

### 问题1：未配置 API_KEY
**症状**：自动弹出配置窗口

**解决**：填写 API_KEY，保存后刷新页面

### 问题2：图片生成失败
**症状**：任务状态为失败

**解决**：
1. 查看错误详情
2. 检查 API_KEY 是否正确
3. 点击"重新获取"重试

### 问题3：服务启动失败
**症状**：端口被占用

**解决**：
```bash
# 查看端口占用
netstat -ano | findstr :697

# 结束进程
taskkill /F /PID 进程ID

# 重新启动
python server.py
```

### 问题4：瀑布流布局错乱
**症状**：图片显示异常

**解决**：刷新页面，前端会重新初始化 Masonry

---

## 📊 性能优化

### 多任务并发
- 支持多个任务同时轮询
- 每个任务独立定时器，互不阻塞
- 第一次延迟 1 分钟，之后每 30 秒查询

### 前端轮询
- 轮询逻辑完全由前端控制
- 减少服务器压力
- 支持页面刷新自动恢复

### 数据库优化
- 使用 SQLite 轻量级数据库
- 自动检测并添加新字段
- 支持旧数据库平滑升级

---

## 🔄 更新日志

### v2.0.0 (2026-03-25)
- ✅ 修复数据库表结构缺少 respond 字段
- ✅ 移除 API Key 硬编码，改用环境变量
- ✅ 修复全局锁导致任务阻塞问题
- ✅ 优化任务恢复机制
- ✅ 修复瀑布流缩小问题
- ✅ 修复弹窗重叠问题
- ✅ 优化轮询策略（第一次1分钟，之后30秒）
- ✅ 支持多任务并发轮询
- ✅ 清理无用文件

### v1.0.0 (2026-03-23)
- 🎉 初始版本发布
- ✅ 基础图片生成功能
- ✅ 智能切割功能
- ✅ 瀑布流展示
- ✅ 批量下载功能

---

## 📝 开发者备注

### 技术栈
- **后端**：Flask + SQLite + PIL
- **前端**：jQuery + Masonry + imagesLoaded
- **API**：AceData Nano Banana API

### 扩展建议
1. 添加更多 AI 模型支持
2. 添加图片滤镜功能
3. 添加批量生成功能
4. 添加用户认证系统
5. 添加 WebSocket 实时推送

### 贡献代码
欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License

---

## 🆘 获取帮助

- **文档**：本 SKILL.md 文件
- **API 官网**：https://share.acedata.cloud/r/1uN88BrUTQ
- **问题反馈**：在 OpenClaw 社区提问

## 联系我们
**email:** zhuxi0906@gmail.com
**微信** jakeycis
如果有功能开发需求，可以联系我，由于开放语言和方案的改变，这个skill还有一些小BUG没完成。
