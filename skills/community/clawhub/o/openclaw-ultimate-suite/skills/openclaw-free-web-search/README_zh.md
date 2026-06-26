# OpenClaw 免费联网技能 v4.1

> **零费用 · 零 API Key · 隐私优先 · 模型无关**
> 唯一一个在回答前告诉你**该信多少**的免费 OpenClaw 联网技能。
> 支持任何担任 OpenClaw 指挥官的模型。

[English](./README.md)

---

## 这个技能解决什么问题

OpenClaw 官方的联网功能需要配置 Brave Search、Perplexity 或 Gemini 的 API Key，全都需要付费。这个技能提供一套完全免费的替代方案：本机运行自建 SearXNG 做元搜索，Scrapling 做反爬抓取，不需要任何 API Key，不需要任何付费服务，搜索记录完全留在本机。

大多数免费搜索技能只给你一份 URL 列表。这个技能多做了一步：在 agent 断言任何事实之前，先用 `verify_claim.py` 对该事实进行多源交叉验证，给出结构化置信度结论。agent 不再需要猜测信息是否可靠。

---

## 模型兼容性

这个技能本质上是三个 Python 脚本，通过 shell 命令调用。任何能执行 shell 命令的模型都可以使用，无需任何适配。

| 指挥官模型 | 兼容 |
|---|---|
| Claude 3.5 / 3.7 (Anthropic) | ✅ |
| GPT-4 / GPT-4o (OpenAI) | ✅ |
| Gemini 1.5 / 2.0 (Google) | ✅ |
| Mistral / Mixtral | ✅ |
| Llama 3 / 3.1 (Meta) | ✅ |
| DeepSeek V3 / R1 | ✅ |
| Qwen 3 / Qwen3-Coder (Alibaba) | ✅ |
| 任何支持 shell 工具的模型 | ✅ |

无论你使用本地部署的模型（通过 Ollama、vLLM 或其他推理框架），还是通过 API 调用的云端模型，这个技能的行为完全一致。

---

## 三工具架构

```
OpenClaw Agent（任意模型）
    │
    ├── 1. search_local_web.py   ← 找到相关 URL
    │       ├── 意图感知查询扩展（Agent Reach，自动生成 2-3 个子查询）
    │       ├── 并行多引擎：Bing + DuckDuckGo + Google + Startpage + Qwant
    │       ├── 综合质量评分：域名权威性(35%) + 时效性(20%) + 跨引擎验证(20%)
    │       │               + 摘要密度(15%) + 标题质量(10%)
    │       ├── 过滤付费墙 / 404 / 登录墙
    │       ├── 代理自动检测（环境变量 + 探测 7890/7897/1080 端口）
    │       └── 本地 SearXNG → 公共备用（searx.be）
    │
    ├── 2. browse_page.py        ← 深度读取页面内容
    │       ├── 第一级：Scrapling Fetcher（TLS 指纹伪装，约 1-3 秒）
    │       ├── 第二级：StealthyFetcher（绕过 Cloudflare Turnstile，约 5-15 秒）
    │       ├── 第三级：DynamicFetcher（完整 Playwright JS 渲染，约 10-30 秒）
    │       ├── 第四级：stdlib urllib（无 Scrapling 时的降级兜底）
    │       ├── 代理自动检测 + macOS 本地 Chrome 检测
    │       ├── 自适应 CSS 内容提取（兼容各类页面结构）
    │       ├── 付费墙检测 + 发布日期提取
    │       └── 置信度输出：HIGH / MEDIUM / LOW
    │
    └── 3. verify_claim.py       ← 这个事实该信多少？
            ├── 将断言扩展为 3 个搜索变体
            ├── 并行抓取 3-10 个独立来源
            ├── 对每个来源分类：AGREE / CONTRADICT / NEUTRAL
            ├── 域名权威性加权（Wikipedia/Reuters = 3×；Reddit = 1×）
            ├── 跨源一致性加成（多个来源互相印证时得分提升）
            ├── --urls 直接模式：指定已知 URL，无需 SearXNG
            └── 结论：VERIFIED / LIKELY_TRUE / UNCERTAIN / LIKELY_FALSE / UNVERIFIABLE
```

---

## 推荐工作流

```
用户提问
    │
    ▼
search_local_web.py  →  获取 top 5 URL + 质量评分 + [cross-validated] 标签
    │
    ▼
browse_page.py       →  读取完整页面内容，输出置信度 HIGH / MEDIUM / LOW
    │                   Cloudflare 保护的页面改用 --mode stealth
    ▼
verify_claim.py      →  在断言关键事实前做多源交叉验证
    │                   VERIFIED / LIKELY_TRUE → 带引用自信回答
    │                   UNCERTAIN / LIKELY_FALSE → 明确告知用户
    ▼
回答，附来源 URL + 发布日期 + 置信度
```

---

## 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/wd041216-bit/openclaw-free-web-search.git
cd openclaw-free-web-search

# 2. 一键安装（SearXNG + Scrapling + Playwright）
./install_local_search.sh

# 3. 启动 SearXNG
./start_local_search.sh

# 4. 同步技能到 OpenClaw workspace
./sync_openclaw_workspace.sh

# 5. 重启 OpenClaw，三个工具立即生效
```

---

## 系统要求

- macOS（Apple Silicon 或 Intel）
- Python 3.8+
- OpenClaw 桌面应用

**可选但强烈推荐（启用反爬功能）：**

```bash
pip install scrapling[all]
python -m playwright install chromium
```

安装脚本 `./install_local_search.sh` 会自动处理以上所有依赖，无需手动执行。

---

## 使用方法

### 1. 网页搜索

```bash
# 基本搜索
python3 ~/.openclaw/workspace/skills/local-web-search/scripts/search_local_web.py \
  --query "DeepSeek V3 最新进展" --intent news --limit 5

# 搜索后自动浏览排名第一的结果
python3 ... --query "Qwen3 架构解析" --intent research --browse

# 对旧内容降权（适合需要最新信息的查询）
python3 ... --query "AI 模型排行" --max-age-days 30
```

### 2. 读取页面内容

```bash
# 自动模式（Scrapling 三级级联：快速 → 隐身 → 动态）
python3 ~/.openclaw/workspace/skills/local-web-search/scripts/browse_page.py \
  --url "https://example.com/article" --max-words 600

# 强制隐身模式（Cloudflare 保护的站点）
python3 ... --url "https://..." --mode stealth

# 完整 JS 渲染（React / Vue 等 SPA 应用）
python3 ... --url "https://..." --mode dynamic
```

### 3. 验证事实

```bash
# 自动模式：SearXNG 自动寻找来源
python3 ~/.openclaw/workspace/skills/local-web-search/scripts/verify_claim.py \
  --claim "DeepSeek V3 于 2025 年发布，参数量为 671B" \
  --sources 5

# 直接 URL 模式：指定已知来源，无需 SearXNG
python3 ... \
  --claim "DeepSeek V3 于 2025 年发布，参数量为 671B" \
  --urls https://deepseek.com/blog/... \
         https://en.wikipedia.org/wiki/DeepSeek

# 机器可读 JSON 输出
python3 ... --claim "..." --json
```

**输出示例：**

```
VERDICT    : 🟢 LIKELY_TRUE
CONFIDENCE : 72%
SOURCES    : 4 checked  (3 agree / 0 contradict / 1 neutral)
MODE       : FULL (Scrapling + StealthyFetcher)

[1] ✅ deepseek.com  [HIGH]  score=0.87
    Excerpt: "DeepSeek-V3, a strong Mixture-of-Experts (MoE) language model with 671B total parameters..."

[2] ✅ en.wikipedia.org  [HIGH]  score=0.85

[3] ✅ arxiv.org  [HIGH]  score=0.81

[4] ➖ techcrunch.com  [HIGH]  score=0.44
```

---

## 结论参考

| 结论 | 置信度 | 含义 |
|---|---|---|
| ✅ VERIFIED | ≥ 75% | 多个高权威来源一致认可 |
| 🟢 LIKELY_TRUE | 55–74% | 多数来源支持该断言 |
| 🟡 UNCERTAIN | 35–54% | 证据混杂或不足 |
| 🔴 LIKELY_FALSE | 15–34% | 多个来源与该断言矛盾 |
| ⬜ UNVERIFIABLE | < 15% | 无法找到相关来源 |

---

## 搜索意图选项

| 意图 | 适用场景 | 使用的引擎 |
|---|---|---|
| `general` | 默认 | bing, ddg, google |
| `factual` | 事实、文档、定义 | bing, google, ddg |
| `news` | 突发新闻、最新动态 | bing, ddg, google |
| `research` | 论文、GitHub、技术深度 | google, startpage, bing |
| `tutorial` | 教程、代码示例 | google, bing, ddg |
| `comparison` | A vs B、评测对比 | google, bing, startpage |
| `privacy` | 敏感查询 | ddg, startpage, qwant |

---

## 抓取模式（browse_page.py）

| 模式 | 引擎 | 适用场景 | 速度 |
|---|---|---|---|
| `auto` | 第一级 → 第二级 → 第三级 | 默认，优先最快 | 自适应 |
| `fast` | Scrapling `Fetcher` | 普通站点，TLS 伪装 | 约 1-3 秒 |
| `stealth` | `StealthyFetcher` | Cloudflare、反爬保护 | 约 5-15 秒 |
| `dynamic` | `DynamicFetcher` | 重 JS / SPA 应用 | 约 10-30 秒 |

---

## 服务管理

```bash
./start_local_search.sh    # 启动 SearXNG
./stop_local_search.sh     # 停止 SearXNG
./doctor.sh                # 健康检查（SearXNG + Scrapling + Playwright）
```

---

## 环境变量

| 变量名 | 默认值 | 说明 |
|---|---|---|
| `LOCAL_SEARCH_URL` | `http://127.0.0.1:18080` | 本地 SearXNG 地址 |
| `LOCAL_SEARCH_FALLBACK_URL` | `https://searx.be` | 本地服务不可用时的公共备用 |
| `LOCAL_SEARCH_PROXY` | _(自动检测)_ | 手动指定代理（如 `http://127.0.0.1:7890`） |

代理检测优先级：`LOCAL_SEARCH_PROXY` > `HTTPS_PROXY` > `ALL_PROXY` > 自动探测本地 7890/7897/1080 端口。

---

## 如何验证联网已生效

```bash
# 测试本地 SearXNG API
curl "http://127.0.0.1:18080/search?q=test&format=json"

# 测试搜索脚本
python3 ~/.openclaw/workspace/skills/local-web-search/scripts/search_local_web.py \
  --query "OpenClaw latest release"
```

---

## 与其他免费技能对比

| 技能 | 搜索 | 反爬浏览 | 交叉验证 | 代理支持 | 模型无关 |
|---|---|---|---|---|---|
| **本技能 (v4.1)** | ✅ 多引擎 | ✅ 三级 Scrapling | ✅ 多源结论 | ✅ 自动检测 | ✅ 任意模型 |
| `hugoreno/scrapling-browse` | ❌ | ✅ Scrapling | ❌ | ❌ | ✅ |
| `keef-agent/openclaw-scrapling` | ❌ | ✅ Scrapling | ❌ | ❌ | ✅ |
| 通用 SearXNG 技能 | ✅ 单引擎 | ❌ 仅 `web_fetch` | ❌ | ❌ | ✅ |

---

## 常见问题排查

先运行健康检查脚本：

```bash
./doctor.sh
```

常见问题及处理方式：

- **本地搜索服务不可达**：执行 `./start_local_search.sh` 启动 SearXNG。
- **Scrapling 未安装**：执行 `pip install scrapling[all]`，或重新运行 `./install_local_search.sh`。
- **Playwright 未安装**：执行 `python -m playwright install chromium`。
- **公共备用实例返回空结果**：部分公共 SearXNG 实例对机器人请求有限制，建议安装 Scrapling 以提升接受率，或通过 `LOCAL_SEARCH_FALLBACK_URL` 指定其他实例。
- **代理环境下 TLS 错误**：脚本会自动对本地 MITM 代理（如 Clash）放宽 TLS 验证，无需手动处理。

---

## 许可证

MIT © 2025
