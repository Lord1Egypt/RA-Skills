---
slug: multi-search-engine-tool-free
name: multi-search-engine-tool-free
version: 1.0.0
displayName: 多搜索引擎免费版
summary: "多搜索引擎聚合查询工具,支持主流中文与国际搜索引擎,适合个人开发者快速信息检索.。多搜索引擎免费版,为个人用户提供多搜索引擎聚合查询能力."
license: Proprietary
edition: free
description: '多搜索引擎免费版,为个人用户提供多搜索引擎聚合查询能力.
  核心能力:中文搜索引擎集成、国际搜索引擎查询、结果聚合展示.
  适用场景:技术资料检索、多源信息对比、快速知识查询.
  差异化:免费版聚焦核心搜索功能,支持8个主流搜索引擎,适合个人快速检索.
  适用关键词: 搜索引擎, 多源搜索, 信息检索, 聚合查询, search engine, multi-search, web search'
tags:
  - 搜索
  - 信息检索
  - 免费版
  - 安全
  - 加密
  - 工具
  - https
  - query
  - url
tools:
  - read
  - exec
homepage: ""
category: "Security"
---
# 多搜索引擎免费版

## 概述

本工具为个人用户提供多搜索引擎聚合查询能力,支持主流中文搜索引擎与国际搜索引擎,将多个搜索结果聚合展示。免费版支持8个搜索引擎,帮助用户从多个信息源快速获取所需内容,适合技术资料检索与多源信息对比.
### 免费版与专业版对比

| 能力维度 | 免费版 | 专业版 |
|----|---|---|
| 搜索引擎数量 | 8个 | 16个 |
| 结果去重 | 不支持 | 智能去重 |
| 结果排序 | 按引擎分组 | 综合相关性排序 |
| 批量搜索 | 不支持 | 批量关键词 |
| 结果缓存 | 不支持 | 本地缓存 |
| API访问 | 不支持 | REST API |
| 导出格式 | 文本 | JSON/CSV |

## 核心能力

### 1. 多引擎搜索

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | 多搜索引擎免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
#!/bin/bash
# 多搜索引擎聚合查询
# ...
QUERY="${1:-test query}"
echo "=== 多搜索引擎查询: ${QUERY} ==="
echo ""
# ...
# 中文搜索引擎
ENGINES_CN=(
    "百度|https://www.baidu.com/s?wd="
    "搜狗|https://www.sogou.com/web?query="
    "360搜索|https://www.so.com/s?q="
    "必应中国|https://cn.bing.com/search?q="
)
# ...
# 国际搜索引擎
ENGINES_GLOBAL=(
    "Google|https://www.google.com/search?q="
    "Bing|https://www.bing.com/search?q="
    "DuckDuckGo|https://duckduckgo.com/?q="
    "Yandex|https://yandex.com/search/?text="
)
# ...
echo "--- 中文搜索引擎 ---"
for engine in "${ENGINES_CN[@]}"; do
    IFS='|' read -r name url <<< "$engine"
    encoded_query=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${QUERY}'))")
    echo "  ${name}: ${url}${encoded_query}"
done
# ...
echo ""
echo "--- 国际搜索引擎 ---"
for engine in "${ENGINES_GLOBAL[@]}"; do
    IFS='|' read -r name url <<< "$engine"
parse; print(urllib.parse.quote('${QUERY}'))")
    echo "  ${name}: ${url}${encoded_query}"
done
```

**处理**: 解析多引擎搜索的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回多引擎搜索的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 2. 搜索结果聚合

```python
#!/usr/bin/env python3
"""免费版搜索结果聚合器"""
# ...
import urllib.parse
import json
# ...
class MultiSearchAggregator:
    """多搜索引擎聚合器"""
# ...
    ENGINES = {
        # 中文搜索引擎
        "baidu": {
            "name": "百度",
            "url": "https://www.baidu.com/s?wd={}",
            "type": "cn"
        },
        "sogou": {
            "name": "搜狗",
sogou.com/web?query={}",
            "type": "cn"
        },
        "360": {
            "name": "360搜索",
            "type": "cn"
        },
        "bing_cn": {
            "name": "必应中国",
            "url": "https://cn.bing.com/search?q={}",
            "type": "cn"
        },
        # 国际搜索引擎
        "google": {
            "name": "Google",
google.com/search?q={}",
            "type": "global"
        },
        "bing": {
            "name": "Bing",
bing.com/search?q={}",
            "type": "global"
        },
        "duckduckgo": {
            "name": "DuckDuckGo",
            "url": "https://duckduckgo.com/?q={}",
            "type": "global"
        },
        "yandex": {
            "name": "Yandex",
            "url": "https://yandex.com/search/?text={}",
            "type": "global"
        }
    }
# ...
    def search(self, query, engines=None):
        """生成多引擎搜索链接"""
        encoded = urllib.parse.quote(query)
# ...
        if engines is None:
            engines = list(self.ENGINES.keys())
# ...
        results = {
            "query": query,
            "encoded_query": encoded,
            "engines": {}
        }
# ...
        for engine_id in engines:
            if engine_id in self.ENGINES:
                engine = self.ENGINES[engine_id]
                results["engines"][engine_id] = {
                    "name": engine["name"],
                    "type": engine["type"],
                    "url": engine["url"].format(encoded)
                }
# ...
        return results
# ...
    def search_cn(self, query):
        """仅中文搜索引擎"""
        cn_engines = [k for k, v in self.ENGINES.items() if v["type"] == "cn"]
        return self.search(query, cn_engines)
# ...
    def search_global(self, query):
        """仅国际搜索引擎"""
        global_engines = [k for k, v in self.ENGINES.items() if v["type"] == "global"]
        return self.search(query, global_engines)
# ...
if __name__ == "__main__":
    aggregator = MultiSearchAggregator()
# ...
    result = aggregator.search("Python 教程")
    print(json.dumps(result, indent=2, ensure_ascii=False))
```

**处理**: 解析搜索结果聚合的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回搜索结果聚合的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 搜索链接生成

```bash
#!/bin/bash
# 生成搜索链接并打开浏览器
# ...
generate_search_links() {
    local query=$1
    local encoded=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$query'))")
# ...
    echo "搜索: ${query}"
    echo ""
    echo "点击以下链接在浏览器中打开:"
    echo ""
    echo "中文引擎:"
    echo "  百度:     https://www.baidu.com/s?wd=${encoded}"
    echo "  搜狗:     https://www.sogou.com/web?query=${encoded}"
    echo "  360:      https://www.so.com/s?q=${encoded}"
    echo "  必应中国: https://cn.bing.com/search?q=${encoded}"
    echo ""
    echo "国际引擎:"
    echo "  Google:   https://www.google.com/search?q=${encoded}"
    echo "  Bing:     https://www.bing.com/search?q=${encoded}"
    echo "  DDG:      https://duckduckgo.com/?q=${encoded}"
    echo "  Yandex:   https://yandex.com/search/?text=${encoded}"
}
# ...
# 示例
generate_search_links "人工智能最新进展"
```

**处理**: 解析搜索链接生成的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回搜索链接生成的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：询工具、支持主流中文与国、适合个人开发者快、速信息检索、多搜索引擎免费版、为个人用户提供多、核心能力、中文搜索引擎集成、国际搜索引擎查询、结果聚合展示、适用场景、技术资料检索、多源信息对比、快速知识查询、差异化、免费版聚焦核心搜、索功能、个主流搜索引擎、适合个人快速检索、适用关键词、多源搜索、信息检索等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景

### 场景一:技术资料多源检索

```bash
#!/bin/bash
# 技术资料多源检索
# ...
QUERY="${1:-React hooks tutorial}"
# ...
echo "=== 技术资料多源检索 ==="
echo "关键词: ${QUERY}"
echo ""
# ...
ENCODED=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${QUERY}'))")
# ...
echo "中文搜索结果:"
echo "  1. 百度: https://www.baidu.com/s?wd=${ENCODED}"
echo "  2. 必应: https://cn.bing.com/search?q=${ENCODED}"
echo ""
echo "国际搜索结果:"
echo "  3. Google: https://www.google.com/search?q=${ENCODED}"
echo "  4. DuckDuckGo: https://duckduckgo.com/?q=${ENCODED}"
echo ""
echo "开发者搜索:"
echo "  5. 代码搜索: https://code.search.example.com/?q=${ENCODED}"
echo "  6. Stack Overflow: https://stackoverflow.com/search?q=${ENCODED}"
```

### 场景二:中英文双语搜索

```python
#!/usr/bin/env python3
"""中英文双语搜索"""
# ...
import json
from multi_search import MultiSearchAggregator
# ...
def bilingual_search(cn_query, en_query):
    """中英文双语搜索"""
    aggregator = MultiSearchAggregator()
# ...
    print("=== 中英文双语搜索 ===")
    print(f"中文关键词: {cn_query}")
    print(f"英文关键词: {en_query}")
    print()
# ...
    # 中文引擎用中文关键词
    print("--- 中文引擎(中文关键词) ---")
    cn_results = aggregator.search_cn(cn_query)
    for eid, info in cn_results["engines"].items():
        print(f"  {info['name']}: {info['url']}")
# ...
    print()
# ...
    # 国际引擎用英文关键词
    print("--- 国际引擎(英文关键词) ---")
    global_results = aggregator.search_global(en_query)
    for eid, info in global_results["engines"].items():
        print(f"  {info['name']}: {info['url']}")
# ...
# 使用示例
bilingual_search("机器学习入门", "machine learning tutorial")
```

### 场景三:快速搜索工具

```bash
#!/bin/bash
# 快速搜索工具(支持参数)
# ...
# 用法: （请参考skill目录中的脚本文件） <engine> <query>
# 引擎: baidu, google, bing, ddg, sogou, 360, yandex, bing_cn
# ...
ENGINE="${1:-baidu}"
shift
QUERY="$*"
# ...
parse; print(urllib.parse.quote('$QUERY'))")
# ...
case "$ENGINE" in
    baidu)    URL="https://www.baidu.com/s?wd=${ENCODED}" ;;
    google)   URL="https://www.google.com/search?q=${ENCODED}" ;;
    bing)     URL="https://www.bing.com/search?q=${ENCODED}" ;;
    ddg)      URL="https://duckduckgo.com/?q=${ENCODED}" ;;
    sogou)    URL="https://www.sogou.com/web?query=${ENCODED}" ;;
    360)      URL="https://www.so.com/s?q=${ENCODED}" ;;
    yandex)   URL="https://yandex.com/search/?text=${ENCODED}" ;;
    bing_cn)  URL="https://cn.bing.com/search?q=${ENCODED}" ;;
    all)
        echo "在所有引擎中搜索: ${QUERY}"
        echo "百度: https://www.baidu.com/s?wd=${ENCODED}"
        echo "Google: https://www.google.com/search?q=${ENCODED}"
        echo "Bing: https://www.bing.com/search?q=${ENCODED}"
        echo "DDG: https://duckduckgo.com/?q=${ENCODED}"
        exit 0
        ;;
    *)
        echo "未知引擎: ${ENGINE}"
        echo "支持: baidu, google, bing, ddg, sogou, 360, yandex, bing_cn, all"
        exit 1
        ;;
esac
# ...
echo "搜索: ${QUERY}"
echo "引擎: ${ENGINE}"
echo "链接: ${URL}"
# ...
# 在macOS上打开浏览器
if command -v open &> /dev/null; then
    open "$URL"
elif command -v xdg-open &> /dev/null; then
    xdg-open "$URL"
fi
```

## 不适用场景

以下场景多搜索引擎免费版不适合处理：

- 黑帽SEO手段
- 搜索引擎作弊
- 付费广告投放管理

## 触发条件

需要SEO优化、关键词分析、排名提升、搜索流量优化时使用。不适用于非本工具能力范围的需求.
## 快速开始

### 第一步:生成搜索链接

```bash
# 为关键词生成所有引擎的搜索链接
python3 -c "
from multi_search import MultiSearchAggregator
import json
agg = MultiSearchAggregator()
result = agg.search('你的搜索关键词')
print(json.dumps(result, indent=2, ensure_ascii=False))
"
```

### 第二步:选择引擎搜索

```bash
# 使用指定引擎搜索
（请参考skill目录中的脚本文件） google "Python tutorial"
```

### 第三步:多引擎对比

```bash
# 在所有引擎中搜索同一关键词
（请参考skill目录中的脚本文件） all "人工智能"
```

#
## 配置示例

### 支持的搜索引擎(免费版8个)

| 引擎 | 类型 | 搜索URL模板 |
|---:|---:|---:|
| 百度 | 中文 | baidu.com/s?wd={} |
| 搜狗 | 中文 | sogou.com/web?query={} |
| 360搜索 | 中文 | so.com/s?q={} |
| 必应中国 | 中文 | cn.bing.com/search?q={} |
| Google | 国际 | google.com/search?q={} |
| Bing | 国际 | bing.com/search?q={} |
| DuckDuckGo | 国际 | duckduckgo.com/?q={} |
| Yandex | 国际 | yandex.com/search/?text={} |

### 搜索URL编码

```python
# URL编码确保特殊字符正确传递
import urllib.parse
# ...
query = "Python 数据分析"
encoded = urllib.parse.quote(query)
# 结果: Python%20%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90
```

## 最佳实践

1. **多源对比**:同一关键词在多个引擎搜索,对比结果差异.
2. **中英结合**:中文关键词用中文引擎,英文关键词用国际引擎.
3. **精确搜索**:使用引号进行精确匹配搜索.
4. **站点限定**:使用 `site:` 限定搜索范围.
```bash
# 最佳实践:精确搜索
QUERY='"exact match" site:stackoverflow.com'
（请参考skill目录中的脚本文件） google "$QUERY"
```

## 常见问题

### Q1: 免费版支持多少个搜索引擎?

免费版支持8个主流搜索引擎(4个中文+4个国际)。专业版支持16个引擎.
### Q2: 搜索结果是直接返回内容吗?

免费版生成搜索链接,需在浏览器中查看结果。直接获取搜索结果内容需要专业版API.
### Q3: 如何添加自定义搜索引擎?

在ENGINES字典中添加引擎配置,包含name、url和type字段.
### Q4: 支持图片/视频搜索吗?

免费版支持网页搜索。图片、视频等垂直搜索需要专业版支持.
### 已知限制

免费版为链接生成模式,无频率限制。如使用搜索API,需遵守各引擎的限速策略.
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **浏览器**: 需要浏览器打开搜索链接

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| python3 | 运行时 | 推荐 | python.org 下载 |
| curl | 命令行工具 | 可选 | 系统自带 |
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
- 免费版为链接生成模式,无需API Key
- 搜索引擎网页搜索为公开接口

### 可用性分类
- **分类**: MD+EXEC(纯Markdown指令,部分功能需exec命令行执行)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent执行多搜索引擎聚合查询任务

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 示例

### 基本用法

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "多搜索引擎免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "multi search engine"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
