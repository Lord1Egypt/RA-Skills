# INDEX.md 分类系统参考

## 脚本位置

`/root/.openclaw/workspace/scripts/memory/gen_references_index.py`

## 核心问题

纯 keyword 匹配无法可靠分类——很多书镜文件标题只有"书镜"两个字，匹配不到任何keyword。64篇未分类就是这么来的。

## 解决方案：FILE_OVERRIDES（显式映射）

在 `TOPIC_RULES` 之前加一层 `FILE_OVERRIDES` 字典，key=文件名片段，value=类别名。优先级最高。

```python
FILE_OVERRIDES = {
    "daodejing": "书镜 / 认知哲学",
    "zhuangzi": "书镜 / 认知哲学",
    "xiaocheng-": "小澄 / 佛学心法",  # 前缀匹配
    "youtube-": "AI Agent 与企业估值",
    "avision-macro": "宏观投研 / 量化交易",
    # ... ~180条
}
```

匹配逻辑：`if pattern.lower() in filename_lower: return topic`

## 分类体系（9个主题）

| Emoji | 类别 | 层 | 篇数(2026-07-25) |
|---|---|---|---|
| 🤖 | AI Agent 与企业估值 | L3 | 99 |
| 📚 | 书镜 / 认知哲学 | L1 | 31 |
| 💰 | 投资框架 / 商业思维 | L3 | 21 |
| 📊 | 宏观投研 / 量化交易 | L3 | 15 |
| ☸️ | 小澄 / 佛学心法 | L2 | 15 |
| 🏗️ | Harness Engineering | L3 | 18 |
| 🧠 | 觉察助手 / 产品哲学 | L2 | 10 |
| 🧬 | 创业 / 个人发展 | L1 | 10 |
| 🏠 | 地产 / Rebase | L3 | 6 |

## 新增分类的判断流程

1. 先看 `FILE_OVERRIDES` 是否有匹配
2. 没有 → 用 `TOPIC_RULES` 的 keyword 列表做 fallback
3. 都不匹配 → 进入未分类

## 新增文章时的维护

- 大多数文章只需要加到 `FILE_OVERRIDES` 一行
- 只有整个新类别的文章（如全新方向）才需要加 `TOPIC_RULES` 条目
- 修改后跑 `python3 gen_references_index.py` 验证未分类=0
