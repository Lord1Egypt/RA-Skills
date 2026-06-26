# multi-search-fallback

多源搜索聚合技能——整合系统内所有搜索技能，通过 fallback 机制和多源交叉验证提高搜索准确性。

## 核心功能

- **Fallback 机制**：自动从 Brave → DuckDuckGo → 火山引擎 → Tavily → 多引擎联合 依次尝试
- **多源交叉验证**：调用 2+ 个搜索源时自动比对结果
- **置信度评分**：✅ 90%+ 高可信 / ⚠️ 60-89% 中等 / ❌ <60% 需复核
- **智能调度**：根据查询类型自动决定调用深度（简单 1-2 源，深入 3+ 源）

## 支持的搜索源

1. `web_search` - Brave/Google 搜索
2. `ddg-web-search` - DuckDuckGo fallback
3. `openclaw-skill-search-web` - 火山引擎（国内）
4. `tavily-search` - AI 优化搜索
5. `multi-search-engine` - 17 引擎联合
6. `deep-research-pro` - 深度研究
7. `academic-deep-research` - 学术文献
8. `mx_search` - 金融资讯

## 使用场景

- 搜索信息、查资料、做研究时
- 需要核实某个说法时（fact-check）
- 多源验证关键结论时
- 搜索结果不一致需要交叉比对时

## 输出格式

```
## 🔍 搜索结果 [query]
**置信度**：XX%（X/X 源一致）
### 核心发现
- ...
### 多源对比
| 搜索源 | 结果 | 状态 |
|--------|------|------|
```
