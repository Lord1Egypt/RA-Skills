---
name: gnview-script-extraction
description: 本工具实现本地视频文件的上传与脚本分析，使用大模型支持对视频进行分析，同时支持自定义分析提示词，适配多种抖音/视频数据分析场景。
---

## 触发词
当用户需要以下场景时，可调用此工具：
- 视频内容结构化分析

## 依赖要求
1.  Python 3.7+
2.  安装requests库：`pip install requests`
3.  已获取API密钥（ARK_API_KEY）

## 使用方法
### 1. 上传本地视频
```bash
python3 scripts/script-extraction.py upload <本地视频路径> <ARK_API_KEY>
```
**参数说明**：
- `本地视频路径`：待分析的本地MP4视频文件路径
- `ARK_API_KEY`：VolcEngine ARK平台的API访问密钥

**返回结果**：成功上传后会输出视频文件ID（file_id），用于后续分析。

### 2. 分析视频脚本
```bash
python3 scripts/script-extraction.py analyze <file_id> <ARK_API_KEY> [--model <模型名称>] [--prompt <自定义提示词>]
```
**参数说明**：
- `file_id`：上传视频后获取的文件ID
- `ARK_API_KEY`：同上
- `--model`：可选，指定分析使用的大模型，默认值为`doubao-seed-2-0-lite-260215`
- `--prompt`：可选，自定义分析提示词，默认提示词为：
  ```
  请你描述下视频中的人物的一系列动作，以JSON格式输出开始时间（start_time）、结束时间（end_time）、事件（event）、是否危险（danger），请使用HH:mm:ss表示时间戳。
  ```

**示例**：
```bash
# 使用默认模型和提示词分析
python3 scripts/script-extraction.py analyze v1-abc123 your-ark-key

# 自定义提示词，提取视频台词和场景
python3 scripts/script-extraction.py analyze v1-abc123 your-ark-key --prompt "请提取视频中的所有台词和对应的场景描述"

# 指定自定义模型
python3 scripts/script-extraction.py analyze v1-abc123 your-ark-key --model doubao-seed-2-0-pro-260215
```

## 输出说明
- 上传成功：返回视频文件ID，可直接用于分析命令
- 分析成功：返回格式化的JSON结果，包含视频分析的结构化数据，如动作时间、事件描述、危险等级等。

## 注意事项
1.  仅支持MP4格式的视频文件
2.  上传的视频文件大小需符合VolcEngine ARK的限制
3.  API密钥需妥善保管，避免泄露
4.  自定义提示词需符合大模型的输入格式要求