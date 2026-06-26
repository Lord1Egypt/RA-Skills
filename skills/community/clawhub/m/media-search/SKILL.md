---
name: media-search
description: 当用户需要写新闻、找素材、查背景、核实信息、了解事件来龙去脉，或者提到"查一下"、"搜一下"、"找找相关报道"、"有什么最新消息"时，或开展互联网线索数据挖掘、新闻选题策划、内容采编、监测竞品或特定信源动态等业务时，需要进行全网媒体稿件检索、查找事件背景、行业数据、政策动态、人物信息、历史脉络等，都应使用此技能
---

# Media Search Tool

媒体库搜索工具技能，用于通过 search.py 脚本搜索媒体内容。

## Usage

```bash
python3 search.py --json-input '{"keywords": "搜索关键词", "limit": 10}' [--output-file results.json] [--output-console]
```

## Parameters

### Required Arguments
- `--json-input`: JSON格式的搜索参数

### Search Parameters (JSON Input)
| 参数名                  | 类型                | 默认值     | 可选值/格式                                       | 必填  | 说明                                      |
| -------------------- | ----------------- | ------- | -------------------------------------------- | --- | --------------------------------------- |
| `keywords`           | string            | 无       | 多个关键词用空格分隔                                   |  是 | 用户输入的搜索主题（如“乡村振兴 最新政策”），系统会自动拆分关键词提升召回率 |
| `keyword_position`   | string            | `标题或正文` | `仅标题`、`仅正文`、`标题或正文`                          |  否 | 指定关键词匹配位置                               |
| `publish_time_start` | string (datetime) | 见规则     | `yyyy-MM-dd HH:mm:ss`                        |  否 | 发布时间开始时间，支持模糊时间词（见下）                    |
| `publish_time_end`   | string (datetime) | 当前时间    | `yyyy-MM-dd HH:mm:ss`                        |  否 | 发布时间结束时间                                |
| `data_type`          | string            | 全部      | `news,app,weibo,wechat,wemedia,epaper`（逗号分隔） |  否 | 数据来源类型                                  |
| `source_name`        | string            | 全部信源    | 任意信源名称                                       |  否 | 指定媒体来源（支持模糊匹配）    如“人民日报”、“新华社”、“澎湃新闻”                      |
| `limit`              | integer           | 10      | 1 ~ 50                                       |  否 | 返回结果数量                                  |

### keywords 拆分规则

用于对用户输入的 `keywords` 进行智能拆分与规范化处理，以提升检索召回率与相关性。

#### 一、基础拆分规则

1. **按空格拆分**
   - 输入：`乡村振兴 最新政策`
   - 输出：`["乡村振兴", "最新政策"]`

2. **去除多余空格**
   - 自动去除首尾空格及重复空格

3. **大小写统一（英文）**
   - 全部转为小写（如：`AI Policy` → `ai policy`）

#### 二、分词增强规则

1. **中文分词（语义切分）**
   - 输入：`人工智能发展`
   - 输出：`["人工智能", "发展"]`

2. **中英文混合拆分**
   - 输入：`AI发展趋势`
   - 输出：`["ai", "发展", "趋势"]`

3. **数字与单位拆分**
   - 输入：`5G产业`
   - 输出：`["5g", "产业"]`

#### 三、停用词过滤
系统可过滤无意义词：的、了、和、是、在、与、及、以及、相关、方面、情况

### 自然语言时间解析规则

用于从用户输入（关键词 / 对话文本）中识别时间表达，并转换为标准时间范围（`publish_time_start` / `publish_time_end`）。

#### 模糊时间关键词

| 关键词 | 转换规则 |
|--------|----------|
| `最新` / `实时` | 当前时间 - 24 小时 |
| `近期` / `最近` | 当前时间 - 3 天 |


#### 相对时间表达

| 表达 | 转换规则 |
|------|----------|
| 最近1天 / 过去1天 | 当前时间 - 1 天 |
| 最近3天 | 当前时间 - 3 天 |
| 最近7天 / 最近一周 | 当前时间 - 7 天 |
| 最近1个月 | 当前时间 - 30 天 |
| 最近3个月 | 当前时间 - 90 天 |

#### 自然时间表达

| 表达 | 转换规则 |
|------|----------|
| 今天 | 当天 00:00:00 ~ 当前时间 |
| 昨天 | 昨天 00:00:00 ~ 23:59:59 |
| 前天 | 前天 00:00:00 ~ 23:59:59 |
| 本周 | 本周一 00:00:00 ~ 当前时间 |
| 上周 | 上周一 00:00:00 ~ 上周日 23:59:59 |
| 本月 | 本月1号 00:00:00 ~ 当前时间 |
| 上月 | 上月1号 00:00:00 ~ 上月最后一天 23:59:59 |
| 今年 | 当年 01-01 00:00:00 ~ 当前时间 |
| 去年 | 去年 01-01 00:00:00 ~ 12-31 23:59:59 |

#### 默认时间规则

当用户**未提供任何时间信息**时：
publish_time_start = 当前时间 - 90 天
publish_time_end = 当前时间

#### 解析规则说明

1. 所有“当前时间”均指系统当前时间（`now`）
2. 时间范围统一输出格式：yyyy-MM-dd HH:mm:ss


### Output Arguments
- `--output-file` (string, optional): 将结果保存到指定JSON文件
- `--output-console` (flag, optional): 强制输出到控制台

## Output Storage

### 1. JSON Output File
当指定 `--output-file` 时保存为JSON格式：
```json
{
  "total": 100,
  "fallback_to_web": false,
  "items": [
    {
      "title": "文章标题",
      "summary": "文章摘要",
      "source_name": "信源名称",
      "data_type": "news",
      "url": "https://example.com"
    }
  ]
}
```

### 2. Console Output
格式化文本输出到控制台，包含：
- 查询元数据（查询词、后端、时间、数量）
- 每个结果的详细信息
- 链接、摘要、正文预览

## 生成文件管理

### 默认生成位置
默认情况下，所有生成的文件保存在当前SKILL目录下：
- JSON输出文件需要手动指定完整路径，例如：`sources/result.json`

### 清理策略
生成的JSON文件应根据情况删除：
- **需要删除时**：JSON文件为临时/中间结果且不再需要时
- **需要保留时**：JSON文件包含需要保留的重要数据时
- **判断标准**：根据文件内容的重要性和项目持续需求来评估

示例清理流程：
```bash
# 生成结果到指定目录
python3 search.py --json-input '{"keywords": "test"}' --output-file sources/result.json

# 使用结果后，如不再需要则清理
rm sources/result.json  # 删除临时JSON文件
```

## Examples

### Basic Search
```bash
python3 search.py --json-input '{"keywords": "人工智能 政策", "limit": 20}'
```

### Search with Source Filter
```bash
python3 search.py --json-input '{"keywords": "乡村振兴", "limit": 10}'
```

### Search with Time Range
```bash
python3 search.py --json-input '{
  "keywords": "人民日报 一带一路",
  "source_name": "人民日报",
  "publish_time_start": "2026-03-25 00:00:00",
  "publish_time_end": "2026-04-01 17:02:28"
}'
```

### Save to JSON File
```bash
python3 search.py --json-input '{"keywords": "经济 发展"}' --output-file results.json
```

### Console Output Only
```bash
python3 search.py --json-input '{"keywords": "科技创新"}' --output-console
```

## Environment Requirements

需要配置API密钥环境变量：
- `NEWS_BIGDATA_API_KEY`: API密钥
- `NEWS_BIGDATA_API_SECRET`: API密钥密钥

## 脚本异常处理

当运行 search.py 脚本发生异常时：
- 系统会在控制台显示具体的错误信息
- 脚本会立即停止执行并返回错误代码
- 用户可根据显示的错误信息进行相应的故障排除

常见异常情况：
- API密钥配置缺失或无效
- JSON输入格式错误
- 网络连接问题
- 参数验证失败

## Integration Notes

1. **Auto-save**: 所有搜索结果自动保存到sources文件夹
2. **Multi-format**: 支持JSON文件、控制台、Markdown三种输出
3. **Parameter validation**: 自动验证参数范围和必填项
4. **Logging**: 详细的操作日志输出到控制台

## Dependencies

- `scripts/media_search.py`: 核心搜索引擎
- `scripts/SearchParameters`: 搜索参数模型
- `scripts/MediaSearchEngine`: 媒体搜索引擎类

## Workflow Integration

### Basic Search Workflow
```bash
# 1. Search and view results in console
python3 search.py --json-input '{"keywords": "关键词"}' --output-console

# 2. Search and save to file
python3 search.py --json-input '{"keywords": "关键词"}' --output-file results.json

# 3. Search with filters
python3 search.py --json-input '{
  "keywords": "关键词",
  "limit": 20
}'
```

### Advanced Usage
```bash
# Search with multiple criteria
python3 search.py --json-input '{
  "keywords": "人工智能 机器学习",
  "keyword_position": "标题或正文",
  "source_name": "科技日报",
  "limit": 30
}' --output-file ai_research.json
```

## Troubleshooting

- **API Error**: 检查环境变量 `NEWS_BIGDATA_API_KEY` 和 `NEWS_BIGDATA_API_SECRET`
- **JSON Parse Error**: 验证JSON格式正确性
- **No Results**: 尝试调整关键词或时间范围
- **Permission Error**: 确保有写入sources文件夹的权限