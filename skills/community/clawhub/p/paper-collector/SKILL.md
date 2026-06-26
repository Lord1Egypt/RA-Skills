---
name: paper-collector
description: 按用户指定的研究方向检索并筛选学术论文：在期刊官网、预印本平台与学术来源中搜索，必须阅读摘要后才可纳入结果。适用于用户要求查找、收集、筛选或整理某一主题/研究问题/方向的文献；若未提供研究方向则不得执行。支持可选“仅限期刊清单”模式、可选论文数量覆盖、可选 Markdown 输出路径。
---

# 文献收集器（paper Collector）

用于在**研究方向明确**时收集论文。只有当用户提供了主题、研究问题或方向时才可执行；若未提供，必须先追问。

## 必要输入门槛

在用户未明确研究方向前，禁止执行工作流。

可接受示例：

- “找城市热岛与健康风险相关文献”
- “Find papers on urban greening and mental health”
- “搜 climate adaptation in informal settlements”

不可接受示例：

- “帮我找文献”
- “collect papers for me”

若主题缺失：仅追问研究方向，不做其它动作。

## 默认值与可覆盖参数

除非用户明确覆盖，否则使用以下默认：

- **论文数量**：默认 5 篇。
- **输出方式**：Markdown 文件输出。
- **Markdown 文件输出**：在写文件前，如果拿不到.md文件输出的目标路径或目标文件夹，则改为在agent对话框中直接输出。
- **期刊清单限制**：若用户明确要求只在该期刊清单内搜索，则不得搜索期刊列表以外的期刊；若用户没有要求白名单，则可自由搜索。

显式运行时指令始终优先于默认值。

## 来源选择规则

### 1）“若用户强制要求仅限期刊清单”

则仅允许在下列有序期刊列表中搜索，并将其视为**严格优先队列**（默认给出了生态与环境相关方向的高质量期刊，用户可自行修改）：

1. Nature  
2. Science  
3. Proceedings of the National Academy of Sciences  
4. Nature Sustainability  
5. Nature Climate Change  
6. Nature Cities  
7. Nature Communications  
8. Science Advances  
9. Communications Earth & Environment  
10. Global Environmental Change  
11. One Earth  
12. Environmental Research Letters  
13. Environment International  
14. Landscape and Urban Planning  
15. Sustainable Cities and Society  
16. Urban Climate  
17. Computers Environment and Urban Systems  
18. Cities  
19. Health & Place  

按顺序检索。若用户要求 `N` 篇论文，先从列表前面的期刊尽量凑齐；只有前面期刊不足时才进入后面的期刊。

例如：用户要 20 篇，若 Nature + Science 已满足，则停止，不再检索更低优先级期刊。

采用多源检索，覆盖出版社站点、综合学术来源与预印本平台；**优先直接访问期刊白名单中的官网进行搜索**，摘要尽量以官方来源为准。

推荐来源白名单（参考）：

1. PubMed（https://pubmed.ncbi.nlm.nih.gov）
2. Google Scholar（https://scholar.google.com）
3. Semantic Scholar（https://www.semanticscholar.org）
4. ScienceDirect（https://www.sciencedirect.com）
5. 出版社官网/期刊官网（仅官网域名，示例，用户可自行修改）
   - Nature / Springer Nature（nature.com, springernature.com）
   - Science / AAAS（science.org）
   - PNAS（pnas.org）
   - Wiley（wiley.com）
   - Taylor & Francis（tandfonline.com）
   - SAGE（sagepub.com）
   - Oxford Academic（academic.oup.com）
   - Cambridge Core（cambridge.org/core）
   - JSTOR（jstor.org）
   - MDPI（mdpi.com）
   - Frontiers（frontiersin.org）
   - IEEE Xplore（ieeexplore.ieee.org）
   - ACM Digital Library（dl.acm.org）

规则：

- 学术索引/发现层仅用于发现候选，入选前必须回到主来源核验摘要。
- 非白名单来源仅在白名单不足以满足任务时作为补充，并需在输出中说明。
- 限制文献的时间范围是最近一个月，限制文献的时间范围是最近一个月，限制文献的时间范围是最近一个月。重要的事情说三遍。

## 工具优先级

按以下顺序使用：

### 优先第三方工具

若可用，优先已安装第三方工具，这里是示例（skills）：

1. `agent-browser`
2. `pinchtab`
3. `lightpanda`
4. `tavily-search`

执行规则：

- `第三方浏览器` 执行搜索时，统一使用 Google 查询入口：`https://www.google.com/search?q={keyword}`（将待检索英文关键词写入 `{keyword}`）。
- 对白名单站点，优先使用 `agent-browser` 通过上述入口定位并进入官网页面检索与抓取。
- 当站点检索失败、反爬受限、或需要快速扩展候选时，使用 `tavily-search` 做发现，再回到官网核验摘要。
- 也可以先使用 `tavily-search` 找文章，然后再使用 `agent-browser`（Google 查询入口）进行复核。

## 筛选硬规则：必须看摘要

不得仅凭标题入选。

对每个候选论文：

1. 打开论文页或可靠条目页。
2. 阅读摘要。
3. 基于摘要判断相关性。
4. 只有摘要与用户主题实质匹配，才可纳入。

若无法获取摘要，不得纳入（除非能从其他可靠来源拿到摘要）。

## 工作流

1. **解析请求**
   
   - 提取研究方向
   - 提取可选论文数量
   - 判断是否启用严格“仅限期刊清单”
   - 判断是否要求 `.md` 输出，并提取目标路径

2. **校验执行前提**
   
   - 研究方向缺失：立即停下并追问
   - 要求 `.md` 但未给路径：先追问路径

3. **选择来源与工具**
   
   - 应用清单模式或多源模式
   - 严格遵循工具优先级

4. **检索候选**
   
   - 围绕用户主题构建检索词
   - 清单模式必须按期刊优先顺序检索
   - 先收集超量候选，供摘要筛选淘汰

5. **摘要筛选**
   
   - 阅读每个候选摘要
   - 剔除离题、弱相关、重复、摘要不可得条目
   - 持续检索直到满足数量或来源耗尽

6. **返回结果**
   
   - 未明确要求 `.md`：直接在会话返回
   - 明确要求 `.md` 且有路径：写入文件并回报保存位置

## 输出要求

会话返回时，每篇论文至少包含：

- 标题
- 作者（若易得）
- 年份
- 期刊/平台
- 链接
- 基于摘要的相关性说明
- 一句摘要提炼结论

若无法满足请求数量，必须明确说明，并给出实际可交付的“已读摘要”论文数。
