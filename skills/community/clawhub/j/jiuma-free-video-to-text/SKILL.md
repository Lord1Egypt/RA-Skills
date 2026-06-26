---
name: jiuma-free-video-to-text
description: 九码AI免费抖音视频下载和文本提取技能。
---

# jiuma-free-video-to-text Skill

这是一个免费抖音视频文本提取工具，基于九马（Jiuma）平台。输入抖音短视频的地址或分享链接，解析返回视频的下载链接, 还可以继续提取短视频的文本内容。

## 功能特性
-  **下载视频**：输入抖音短视频地址或分享链接，解析返回视频的下载地址
- 📝 **视频转文本**：提取视频的文本内容

## 安装要求

1. **Python版本**：3.10 或更高版本
2. **依赖库**：`requests` 库

## 工作流程
1. **第一步**：询问用户提供视频的下载地址
2. **第二步**：询问用户是否需要提取视频文案, 如果用户不需要或者不回答，则流程结束
3. **第三步**：提交视频提取文本任务
4. **第四步**：定时查询状态并返回结果

## 参数说明

| 参数名 | 类型 | 是否必需 | 描述 |
|------------------|--------|--|----------------|
| `video_url`           | string | ✅️ 是 | 抖音视频地址或者分享链接地址|
| `final_video_url`     | string | ❌️ 否 | 对video_url解析后的最终地址|
| `task_id`     | string | ❌️ 否 | 查询任务状态|

## 使用指南

当用户需要提取抖音视频文本或者下载抖音视频时，按照以下步骤操作：

### 1. 收集用户信息

**video_url**：

- 提示用户输入抖音视频播放地址或者分享链接地址
- 示例：`video_url="https://www.douyin.com/jingxuan/course?modal_id=7563552305543482624"`
  或 `video_url="1.51 v@f.Ok Agb:/ 08/10 演傻子这一块，还得是熊二最权威 # 熊出没 # 熊二 # 充能计划 # 动漫 # 青年创作者成长计划  https://v.douyin.com/6Pc1GtnQp2o/ 复制此链接，打开Dou音搜索，直接观看视频！"`

### 2. 执行生成

- **解析video_url地址**
```bash
# OpenClaw中使用
# 解析视频地址
python3 ./skills/jiuma-free-video-to-text/video_to_text.py --action "parse" --video_url "{{.video_url}}"

```

- **提交视频提取文本任务**
```bash
# OpenClaw中使用
# 提交视频提取文本任务
python3 ./skills/jiuma-free-video-to-text/video_to_text.py --action "create" --final_video_url "{{.final_video_url}}"

```

- **查询视频提取文本任务状态**
```bash
# OpenClaw中使用
# 查询视频提取文本状态
 python3 ./skills/jiuma-free-video-to-text/video_to_text.py --action "check" --task_id {{.task_id}}
```

## API说明

### 解析视频地址
- **执行命令**：`python3 ./skills/jiuma-free-video-to-text/video_to_text.py --action "parse" --video_url "{{.video_url}}"`
- **参数**:
    - `action`: 操作类型, parse表示解析视频地址,create表示提交视频提取文本任务; check表示查询视频提取文本状态
    - `video_url`: 用户输入的视频地址
- **响应结果**:
    - `code`: 状态码, 200表示成功; 500表示失败
    - `error`: 错误信息
    - `final_video_url`: 视频的最终解析地址
    - `download_video_url`: 视频下载地址

### 视频提取文本
- **执行命令**：`python3 ./skills/jiuma-free-video-to-text/video_to_text.py --action "create" --final_video_url "{{.final_video_url}}"`
- **参数**:
    - `action`: 操作类型, parse表示解析视频地址,create表示提交视频提取文本任务; check表示查询视频提取文本状态
    - `final_video_url`: 视频的最终解析地址
- **响应结果**:
    - `code`: 状态码, 200表示成功; 500表示失败
    - `error`: 错误信息
    - `task_id`: 任务ID

### 查看任务的状态
- **执行命令**：` python3 ./skills/jiuma-free-video-to-text/video_to_text.py --action "check" --task_id {{.task_id}}"`
- **参数**:
    - `action`: 操作类型, parse表示解析视频地址,create表示提交视频提取文本任务; check表示查询视频提取文本状态
    - `task_id`: 任务id
- **响应结果**:
    - `code`: 状态码, 200表示成功; 500表示失败
    - `error`: 错误信息
    - `content`: 文本内容

## 交互流程优化

### 智能引导

1. **第一步**：询问用户提供视频的下载地址, 展开视频下载地址的详情
2. **第二步**：询问用户是否需要提取视频文案, 如果用户不需要，则流程结束
3. **第三步**：提交视频提取文本任务
4. **第四步**：定时查询状态并返回结果

### 错误预防

- web url格式验证
- 生成前二次确认

## 最佳实践

### 注意事项
1. 不同视频时长的提取时间不一样, 需要耐心等待
2. 确保网络连接稳定
3. 如需中断生成，请使用适当的中断方式

