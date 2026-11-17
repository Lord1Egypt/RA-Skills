# 隐私搜索 - 5 分钟快速上手指南

> 从零开始，5 分钟内完成安装并执行你的第一次隐私搜索。

---

## 🚀 一键安装（推荐）

```bash
python scripts/quick_setup.py
```

一键完成：创建 venv → 安装依赖 → 复制配置 → 验证安装。

---

## 📋 手动安装（如需控制每一步）

### Step 1: 创建虚拟环境

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

### Step 2: 安装依赖

```bash
pip install -r requirements.txt
```

### Step 3: 复制配置

```bash
cp references/config.yaml.example config.yaml
```

### Step 4: 验证安装

```bash
python scripts/search.py "test"
```

---

## 🔍 你的第一次搜索

### 基础搜索（默认引擎）

```bash
python scripts/search.py "Python asyncio 教程"
```

输出示例：
```
🔍 搜索: Python asyncio 教程 | 模式: normal | 结果: 18 条

[1] Python asyncio 异步编程入门教程
    https://docs.python.org/zh-cn/3/library/asyncio.html
    本教程将带你了解 Python asyncio 模块的基础知识...
    — bing

[2] 超详细的 Python asyncio 教程，从入门到精通
    https://www.cnblogs.com/...
    本文详细介绍 Python asyncio 的使用方法...
    — baidu
```

### 隐私搜索（strict 模式）

```bash
python scripts/search.py "Python asyncio 教程" --privacy strict
```

输出示例：
```
搜索: Python asyncio 教程 | 模式: strict | 来源: 实时 | 结果: 12 条

[1] Python Asynchronous Programming
    https://docs.python.org/3/library/asyncio.html
    Learn how to use asyncio for concurrent programming...
    — yandex

[2] Async IO in Python: A Complete Walkthrough
    https://realpython.com/async-io-python/
    Async IO is a concurrent programming design...
    — startpage, qwant
```

> strict 模式仅使用 SearXNG/Yandex/Startpage/Qwant/Brave/DDG。
> 即使显式指定 `--engines baidu` 也会被拒绝，避免隐私承诺被绕过。

### 缓存加速

相同查询在 1 小时内直接复用结果，输出标注「来源: 缓存」。

```bash
python scripts/search.py "Python asyncio 教程"     # 来源: 实时
python scripts/search.py "Python asyncio 教程"     # 来源: 缓存，秒回
python scripts/search.py "Python asyncio 教程" --no-cache   # 强制刷新
```

### 引擎体检

搜不到结果时，先判断是引擎坏了还是关键词没匹配：

```bash
python scripts/search.py --selftest
```

输出会标明每个引擎是「正常」「被拦截」还是「选择器失效」。

### 显示错误诊断网络问题时

```bash
python scripts/search.py "test" --privacy strict --verbose
```

网络故障时的输出：
```
============================================================
🔍 错误诊断报告：

🌐 网络问题：
  ✗ duckduckgo: 网络连接失败: Connection timed out after 10s
    1. 检查网络连接是否正常（ping www.baidu.com）
    2. 确认网络环境不受限制

🔧 引擎问题：
  ✗ yandex: 引擎解析或请求失败: HTML parser error
    1. yandex 可能已更新页面结构
    2. 暂不支持该引擎（可排除）
```

---

## strict 模式可用引擎

| 引擎 | 来源 | 国内速度 | 隐私保护 | 状态 |
|------|------|---------|---------|------|
| **SearXNG** | 本机 | ⭐⭐⭐⭐⭐ 极快 | 极高 | ✅ 最优先 |
| **Yandex** | 俄罗斯 | ⭐⭐⭐⭐ 快 | 中等 | ✅ 默认启用 |
| **Startpage** | 荷兰（Google 代理） | ⭐⭐⭐ 中等 | 高 | ✅ 默认启用 |
| **Qwant** | 法国 | ⭐⭐⭐ 中等 | 高 | ✅ 默认启用 |
| **Brave** | 美国 | ⭐⭐ 较慢 | 高 | ✅ 默认启用 |
| **DuckDuckGo** | 美国 | ⭐ 不稳定 | 极高 | ⚠️ 最后备选 |

优先顺序：SearXNG → Yandex → Startpage → Qwant → Brave → DuckDuckGo

若以上全部不可用，默认**停止搜索**而非降级到国内引擎——因为 strict 用户的预期是宁可无结果也不泄露查询词。确需降级请加 `--allow-fallback`。

---

## 📝 推荐配置（首次只需改 3 项）

```yaml
# config.yaml - 新手推荐修改项
search:
  default_engines: ["baidu", "bing", "duckduckgo", "searxng"]  # ✅ 第1项
  timeout: 15                                                     # ✅ 第2项（网速慢可增大）

privacy:
  default_mode: strict                                            # ✅ 第3项（默认 privacy）
```

其他配置项暂不需要修改。

### 想隐藏 IP

strict 模式不隐藏 IP，需自行配置代理：

```yaml
privacy:
  strict:
    proxy: "http://127.0.0.1:7890"    # 支持 http:// 与 socks5://
```

---

## 🔧 启动 SearXNG（推荐）

SearXNG 本地实例是 strict 模式的隐私基石，建议启动。

### Docker 方式（推荐）

```bash
python scripts/searxng_manager start --method docker
```

### pip 方式（无 Docker）

```bash
python scripts/searxng_manager start --method pip
```

### 验证

```bash
python scripts/searxng_manager status
# 应显示 running: true
```

---

## ❓ 常见问题

### Q1: 安装依赖失败？

```bash
# 换用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q2: SearXNG 启动失败？

Docker 方式失败时，改用 pip：
```bash
python scripts/searxng_manager start --method pip
```

### Q3: 国内使用 strict 模式搜不到结果？

按顺序自动尝试 Yandex → Startpage → Qwant → Brave → DDG。全部失败时默认停止并提示，不会静默降级。

只用国内直连较好的几个：
```bash
python scripts/search.py "关键词" --privacy strict --engines yandex,startpage,qwant,searxng
```

确需降级到国内引擎：
```bash
python scripts/search.py "关键词" --privacy strict --allow-fallback
```

### Q4: 如何排除某个引擎？

```bash
# 排除 yandex，用其他 strict 引擎
python scripts/search.py "关键词" --privacy strict --engines startpage,qwant,searxng
```

### Q5: 如何查看隐私保护详情？

```bash
# 独立的隐私报告
python scripts/privacy report

# 搜索时附带本次实际生效的隐私设置
python scripts/search.py "关键词" --privacy strict --privacy-report
```

### Q6: 搜索记录会留在本地吗？

会。缓存与历史存于 `~/.workbuddy/output/privacy-search-cache.db`。

```bash
python scripts/search.py --cache-stats        # 查看占用
python scripts/search.py --history            # 查看历史
python scripts/search.py --clear-cache        # 清空缓存
python scripts/search.py --clear-history      # 清空历史
```

共享设备上建议在 config.yaml 设 `cache.enabled: false`。

---

## 📚 下一步

- 完整文档 → [SKILL.md](../SKILL.md)
- 搜索引擎适配器详情 → [engines_zh.md](engines_zh.md)
- 配置说明 → [config.yaml.example](config.yaml.example)

有建议？联系邮箱：njskills@agent.qq.com
