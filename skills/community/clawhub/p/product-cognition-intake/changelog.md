# 变更记录

> 任何标签名/别名/阈值改动,必须**同步**:本包 `规范.md` + `system-prompt.md` + Python `app/retrieval/intro_parser.py` + Java `IntroSoftSpecParser`。否则运营写的内容系统识别不了。

## v3(2026-08-20)· 意图/推荐增强字段(准确率导向)
- 新增 5 标签:`需求:`/`解决问题:`(needs)、`用户会问:`/`搜索说法:`(query_phrases)、`不适合:`(not_for)、`差异化:`/`为什么选它:`(differentiators)、`契合理由:`(fit_reasons,`for<-reason`)。
- 目标:提升"意图理解准 + 推荐准",非省 LLM。逐字段作用见 `规范.md §2.1`。
- 落库:5 字段随认知卡进 `cognition` 列;`needs`/`query_phrases` **进 embed_text**(意图召回对齐),其余不进向量。
- ✅ 代码已对齐:Java `IntroSoftSpecParser`(别名/拆列/embed_text/单测 9/9) + Python `intro_parser.py`(v2+v3 别名、行首锚点、认知卡进 attributes、单测 5/5)。两侧解析输出同构。
- ⚠️ 补记:本次同时把 Python `intro_parser` 从 v1 直接补齐到 v2+v3(此前缺 定位/能力/允许表达),并将认知卡富结构由"顶层散落"收敛进 `attributes`(否则回 Java `Cpv` 反序列化会丢弃)。

## v2(2026-08-19)· 严格版,对齐产品方案 §4.3 认知卡
- 新增标签:`定位:`(positioning)、`能力:`(capabilities,`名<-证据`)、`允许表达:`(guardrails.allowed)。
- 严格规则:标签**行首锚点**生效,值可跨多行;值内冒号/分号不误切。
- 落库:结构化认知卡落 `t_product_attr`(新字段进 attributes JSON),原文留 `t_product_detail.ai_product_intro`。
- 向量:`embed_text` 只取能力/事实侧,排除卖点(is_claim)/推断/guardrails。
- 关联:Java 侧规则解析直落 spec `p_java_gns_node/docs/superpowers/specs/2026-08-19-intro-softspec-rule-parse-design.md`。

## v1(初版)· 冒号软标签
- 标签:核心卖点/关键事实/适用人群/适用场景/功效/推荐关键词/品牌/类目/禁用表达/常见问题。
- 判定:N≥3 且命中核心卖点/关键事实。
- 解析:Python `intro_parser.py`(全文匹配),LLM 兜底路径 S1。
