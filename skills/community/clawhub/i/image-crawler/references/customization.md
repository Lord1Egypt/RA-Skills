# 自定义与接口说明

## 脚本架构

```
scripts/
├── image_crawler.py    # 主脚本：整合百度+Bing，支持去重/拓展/监控
├── baidu_crawler.py    # 百度引擎模板（独立可用）
└── bing_crawler.py     # Bing引擎模板（独立可用）
```

**image_crawler.py** 是完整的采集工具，直接使用即可。
**baidu/bing_crawler.py** 是独立的引擎模板，适合理解原理或二次开发。

## image_crawler.py CLI 参数

| 参数 | 短写 | 默认值 | 说明 |
|------|------|--------|------|
| `--keywords` | `-k` | 必填 | 搜索关键词，可多次指定 |
| `--count` | `-n` | 100 | 目标图片数量 |
| `--output` | `-o` | ./crawled_images | 输出目录 |
| `--engine` | `-e` | baidu | 搜索引擎：baidu / bing / both |
| `--expand` | | false | 启用关键词拓展 |
| `--expand-terms` | | 内置词 | 自定义拓展词，逗号分隔 |
| `--min-size` | | 5 | 最小文件大小（KB） |
| `--timeout` | | 15 | 单张下载超时（秒） |
| `--stall-timeout` | | 60 | 停滞中断超时（秒） |
| `--progress-interval` | | 10 | 每 N 张输出进度 |
| `--json` | | false | JSON 格式输出 |

## JSON 输出格式（--json 模式）

每行一个 JSON 对象，type 字段标识消息类型：

```jsonl
{"type": "start",    "keywords": [...], "target": 100, "engine": "baidu", "output": "/path"}
{"type": "info",     "message": "关键词拓展: 2 → 10 个"}
{"type": "search",   "engine": "baidu", "keyword": "挖掘机", "found": 30, "new": 28}
{"type": "progress", "downloaded": 50, "target": 100, "failed": 3, "dedup": 2, "speed": 2.1, "eta": "24s"}
{"type": "stall",    "message": "已 30s 无新图片，继续尝试..."}
{"type": "error",    "message": "连续 15 次下载失败，可能触发反爬机制"}
{"type": "done",     "total": 95, "failed": 5, "dedup_removed": 8, "elapsed": 47.3, "output": "/path"}
```

## 去重机制

### 三层去重

1. **URL 去重** — 相同 URL 不重复下载
2. **内容 hash 去重** — 不同 URL 但内容相同的图片只保留一张（MD5）
3. **跨次运行去重** — hash 持久化到输出目录的 `.dedup_hashes.json`

### .dedup_hashes.json

自动维护在输出目录下，格式：

```json
{
  "hashes": ["d41d8cd9...", "..."],
  "urls": ["https://...", "..."],
  "count": 95,
  "updated": "2026-03-28 14:00:00"
}
```

重新运行时自动加载，已下载过的图片不会重复。删除此文件即可重置去重状态。

## 关键词拓展

### 内置拓展（--expand）

默认添加修饰词：`高清`、`实拍`、`工作现场`、`施工`。

例如 `挖掘机` → `挖掘机, 高清挖掘机, 实拍挖掘机, 工作现场挖掘机, 施工挖掘机`

### 自定义拓展（--expand-terms）

```bash
python image_crawler.py -k 挖掘机 --expand --expand-terms "三一,卡特,小松,沃尔沃,临工"
```

生成：`挖掘机, 三一挖掘机, 卡特挖掘机, 小松挖掘机, ...`

### Agent 智能拓展

SKILL.md 中指导 agent 利用 LLM 能力生成领域相关的拓展词，比内置词库更精准。

## 添加新搜索引擎

在 image_crawler.py 中添加新引擎类，实现两个方法即可：

```python
class NewEngine:
    NAME = "new_engine"

    def search(self, keyword: str, count: int = 60) -> list:
        """返回 URL 字符串列表"""
        ...

    def download(self, url: str, filepath: str, timeout: int = 15) -> bool:
        """下载图片到 filepath，成功返回 True"""
        ...
```

然后在 `ImageCrawler.__init__` 中注册：

```python
if self.engine_name in ("new_engine", "both"):
    self.engines.append(NewEngine())
```

## 常见问题

### 百度返回空结果
- 检查网络是否正常
- 可能被临时限流，等待几分钟重试
- 尝试更换关键词

### Bing 搜索到 0 张
- Bing 返回的 HTML 中双引号编码为 `&quot;`，脚本已处理（html.unescape）
- 如果仍为 0，可能是 Bing 页面结构更新，需检查 murl 正则

### 下载成功但图片损坏
- 调大 `--min-size` 过滤小文件
- 部分源站返回非图片内容（如 HTML 错误页），百度引擎已做 content-type 检查

### 反爬触发
- 降低采集速度：增大脚本中的 `time.sleep`
- 更换 User-Agent
- 分批采集，每批之间间隔较长时间
