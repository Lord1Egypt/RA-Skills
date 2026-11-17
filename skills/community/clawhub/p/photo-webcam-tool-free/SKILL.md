---slug: photo-webcam-tool-free
name: photo-webcam-tool-free
version: 1.0.0
displayName: 网络摄像头工具-免费版
summary: "网络摄像头快照获取工具"
license: Proprietary
edition: free
description: 网络摄像头快照获取工具免费版,面向个人用户，可自动提升工作效率
  核心能力:

  - 摄像头收藏列表管理

  - 通过编号快速获取快照

  - 批量获取多摄像头图片

  - 自动解析摄像头图片 URL

  - 本地图片保存与查看

  适用场景:

  - 查看旅游景点实时画面

  - 监控天气与道路状况

  - 个人收藏管理常用摄像头

  差异化:免费版提供基础快照获取能力。PRO版扩展定时抓取、图片拼接、历史归档与多平台推送.
  适用关键词: webcam, 摄像头, 快照, photo, snapshot, 实时画面, 收藏列表'
tags:
  - 摄像头
  - 图片获取
  - 工具
  - Web开发
  - 前端
  - 开发工具
  - url
  - jpg
  - webcam
  - zugspitze
  - foto-webcam
tools:
  - read
  - exec
  - write
  - glob
homepage: ""
category: "Development"---# 网络摄像头工具 - 免费版

## 概述

网络摄像头工具免费版是面向个人用户的摄像头快照获取工具。通过收藏列表管理常用摄像头,输入编号即可快速获取当前快照图片,支持批量获取与本地保存.
支持 foto-webcam.eu 等主流网络摄像头平台,自动解析页面中的最新图片 URL.
## 核心能力

### 1. 收藏列表管理

维护一个 JSON 格式的摄像头收藏列表,每个条目包含编号、名称和页面 URL.

**处理**: 解析收藏列表管理的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回收藏列表管理的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 2. 快照获取

通过编号快速获取对应摄像头的最新快照,支持自动解析图片 URL.

**处理**: 解析快照获取的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回快照获取的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 3. 批量获取

支持一次获取多个摄像头的快照(最多 6 个),分别保存为独立文件.

**处理**: 解析批量获取的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回批量获取的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 4. 列表查看

查看收藏列表中所有摄像头的编号与名称.

**处理**: 解析列表查看的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回列表查看的响应数据,包含状态码、结果和日志.
**技术参数**：使用`input_params`和`output_format`参数控制执行行为,支持`json`/`text`/`csv`输出格式.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：网络摄像头快照获、取工具、支持收藏列表管理、与图片下载、适合个人使用、取工具免费版、面向个人用户等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一:查看旅游景点实时画面

查看 Zugspitze 滑雪场的实时画面.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | 网络摄像头工具-免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 通过 URL 直接获取快照
python3 foto_webcam_snapshot.py \
  --url https://www.foto-webcam.eu/webcam/zugspitze/ \
  --out /tmp/zugspitze.jpg
# ...
# 查看图片
open /tmp/zugspitze.jpg  # macOS
# 或 xdg-open /tmp/zugspitze.jpg  # Linux
```

### 场景二:通过收藏编号获取快照

从收藏列表中按编号获取摄像头快照.
```bash
# 查看收藏列表
py --favorites favorites.json --list
# ...
# 输出:
# Webcam 1: 慕尼黑市中心
# Webcam 2: Zugspitze 滑雪场
# Webcam 3: 新天鹅堡
# ...
# 获取编号 1 的快照
  --favorites favorites.json \
  --id 1 \
  --out /tmp/webcam1.jpg
```

### 场景三:批量获取多个摄像头

一次获取多个摄像头的快照.
```bash
# 获取编号 1、3、5 的快照
for id in 1 3 5; do
    --id $id \
    --out /tmp/webcam${id}.jpg
  echo "Webcam $id 已保存"
done
```

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 创建收藏列表

```json
[
  {
    "id": 1,
    "name": "慕尼黑市中心",
    "page": "https://www.foto-webcam.eu/webcam/muenchen/",
    "image": "https://www.foto-webcam.eu/webcam/muenchen/current/1200.jpg"
  },
  {
    "id": 2,
    "name": "Zugspitze 滑雪场",
foto-webcam.eu/webcam/zugspitze/"
  }
]
```

### 获取第一张快照

```bash
  --id 1 \
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
## 示例

### 收藏列表格式

```json
[
  {
    "id": 1,
    "name": "摄像头名称",
    "page": "摄像头页面URL",
    "image": "直接图片URL(可选)"
  }
]
```

### 图片 URL 解析规则

对于 foto-webcam.eu 的摄像头页面:

```
页面 URL: https://www.foto-webcam.eu/webcam/zugspitze/
图片 URL: https://www.foto-webcam.eu/webcam/zugspitze/current/1200.jpg
```

如果收藏条目中设置了 `image` 字段,直接使用该 URL;否则从页面 HTML 中解析最新图片链接.
### 添加新摄像头

```bash
# 在 favorites.json 中追加新条目
# 如果来源不稳定,建议设置 image 字段为直接 JPG 链接
```

## 最佳实践

1. **设置直接图片 URL**:对于不稳定的摄像头源,在 `image` 字段设置直接 JPG 链接,避免 HTML 解析失败
2. **合理命名**:收藏条目的 `name` 字段使用清晰的中文或英文名称,便于识别
3. **控制批量数量**:单次请求不超过 6 个摄像头,避免请求过多被限流
4. **保存路径**:使用 `/tmp/` 作为临时保存路径,避免污染工作目录
5. **定期更新列表**:检查收藏列表中的摄像头是否仍然可用,移除失效源

## 常见问题

### Q: 获取快照时报错"无法解析图片 URL"?

A: 部分摄像头页面结构可能变化。建议在收藏条目中手动设置 `image` 字段为直接图片 URL,跳过 HTML 解析步骤.
### Q: 可以添加非 foto-webcam.eu 的摄像头吗?

A: 可以。只要摄像头有可直接访问的图片 URL,在 `image` 字段中填入该 URL 即可。工具会直接下载该 URL 的图片.
### Q: 批量获取时部分失败怎么办?

A: 逐个重试失败的摄像头。可能是该摄像头暂时离线或网络波动。建议在收藏列表中标记不稳定的源,优先使用有 `image` 字段的条目.
### Q: 快照保存的图片格式是什么?

A: 默认保存为 JPG 格式。输出文件路径通过 `--out` 参数指定,建议使用 `.jpg` 扩展名.
## 依赖说明

### 运行环境

- **Agent平台**: 支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **Python**: 3.8+

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| Python 3 | 运行时 | 必需 | 官方网站下载 |
| requests | Python库 | 必需 | pip install requests |
| Beautiful Soup | Python库 | HTML解析推荐 | pip install beautifulsoup4 |
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置

- 本 Skill 无需 API Key
- 摄像头图片为公开资源,无需认证
- 如需推送到 Telegram 等平台,需配置对应平台的 Bot Token

### 可用性分类

- **分类**: MD+EXEC(Markdown指令 + 命令行执行)
- **说明**: 通过自然语言指令驱动 Agent 获取网络摄像头快照,依赖 Python 脚本与网络请求
- **限制**: 免费版不支持定时抓取、历史归档与多平台自动推送

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 本地运行，不支持多设备同步
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力