"""
core/ — Infoseek 核心层（v3.1.0）

与 scripts/ 适配层（MCP/HTTP/CLI）分离，本目录只放纯逻辑模块。
状态持久化（claim / alias / 实体画像等 JSON）已外置到运行时数据目录
（默认 ~/.infoseek，可由 INFOSEEK_DATA_DIR / INFOSEEK_DB 配置），
不再写入 core/ 源码目录，详见 core/state_dir.py。

模块（22 个功能模块，不含本 __init__）：
- anchor_score_v2: v2 评分算法（核心）
- entities: 跨语言实体词典（100+）
- ner: 命名实体识别算法
- trust_sources: 统一信任源白名单
- llm_router: 多模型路由
- conflict_v3: 跨源矛盾检测（当前主用，别名归并 + 严重度评级）
- contradiction_scorer: 两句话矛盾评分（severity 四档）
- claim_store / entity_aliases / entity_profile / entity_pending / entity_enricher:
  实体相关状态管理（数据落运行时目录，见 state_dir）
- entity_graph / entity_heat / entity_tracker / entity_trajectory / entity_meta:
  实体图谱 / 热度 / 频次 / 轨迹 / 元信息
- freshness_cron / wikidata_sync: 新鲜度 cron / Wikidata 同步
- traced_export: 引用图谱导出
- state_dir: 运行时数据目录集中解析

⚠️ conflict_v2 为遗留实现（v2.x），已弃用，仅保留向后兼容导入；
   新代码请使用 conflict_v3 + contradiction_scorer。

模块命名规范：
- v2 API 统一以 _v2 后缀（如 anchor_score_v2）
- 不向后兼容的方法须明确 deprecation warning
"""

__version__ = "2.6.1"  # 单源对齐 scripts/mcp_tools_common.py:SKILL_VERSION（v1.8.1 治理）
__all__ = [
    "anchor_score_v2",
    "claim_store",
    "conflict_v2",        # 遗留：已弃用，仅向后兼容
    "conflict_v3",        # 当前主用矛盾检测
    "contradiction_scorer",
    "entities",
    "entity_aliases",
    "entity_enricher",
    "entity_graph",
    "entity_heat",
    "entity_meta",
    "entity_pending",
    "entity_profile",
    "entity_tracker",
    "entity_trajectory",
    "freshness_cron",
    "llm_router",
    "ner",
    "state_dir",
    "traced_export",
    "trust_sources",
    "wikidata_sync",
]
