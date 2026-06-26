# multi-engine-auto-search - 全引擎自动聚合搜索

## 功能

自动发现所有已安装的搜索类技能脚本，并行调用后聚合去重输出。

## 调用方式

```bash
python run.py <关键词>
```

## 实现逻辑

1. 扫描 `~/.openclaw/skills/` 和 `~/.openclaw/workspace/skills/` 两个目录
2. 发现所有名字含 search/web/find/cn/browser 的技能的 run.py 或 scripts/search.py
3. **并行**用 subprocess 调用每个脚本（传入关键词 + `--json`）
4. 通过共享临时文件 `mes_result.json` 读取子进程 JSON 结果
5. 所有结果按 URL 去重
6. 无任何结果时自动用 Bing 直接兜底

## 支持的引擎/技能

| 技能 | 脚本 | 状态 |
|------|------|------|
| `browser-search-ultimate-cn` | run.py | ✅ 可用（Bing）|
| `cn-enhanced-search` | run.py | ✅ 可用（Bing）|
| `auto-all-search` | run.py | ✅ 可用（Bing）|
| `web-search-plus` | scripts/search.py | ⚠️ 需API Key |
| `multi-search-engine` | 无run.py | ❌ 空壳 |

## 技术细节

- 并行：ThreadPoolExecutor，无数量限制
- 子进程通信：临时文件（解决 subprocess stdout 中文编码问题）
- 兜底：Bing 直接 curl（`cn.bing.com`）
- 依赖：Python 3 标准库 + `curl.exe`

## 输出格式

```
== [Multi-Engine Search] <关键词> ==
[Discovery] Found N search skill(s)
[<skill>] +N
...
== [Core Answer] ==
  摘要1
  摘要2
== [Total: N unique | Sources: x, y] ==
N. [source] 标题
   摘要
   URL
```
