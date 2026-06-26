"""
多路召回技能 (Skill: Multi-path Recall)
原始来源: app/ai_chat_agents/multi_call.py  (MultiCallService + MultiCallAgent.handle_message)

完整还原 execute_multi_call 的核心逻辑，去除：
  - autogen @message_handler / TopicId / publish_message / send_response
  - Neo4j / Milvus 适配器硬依赖（通过接口注入）

入参: MultiCallInput
出参: MultiCallOutput
"""

import json
import logging
import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Protocol, runtime_checkable

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════
# 0.  可注入的外部服务接口（Protocol）
#
#     实现说明：
#       Neo4jTableSchemaService  — 调用 Neo4j MCP Service，按表名查询 DDL。
#           原始调用: self.neo4j_adapter.service.ask(query)（同步），
#           在 async 上下文中用 asyncio.to_thread 包装。
#
#       MilvusQARecallService    — 调用 Milvus 向量数据库，
#           原始调用: self.milvus_adapter.recall_similar_questions(question, top_k)（async）。
#
#     这两个服务依赖真实的 Neo4j/Milvus 实例，无法内嵌实现；
#     通过 Protocol 约定接口，调用方自行提供实现（或 mock）。
# ═══════════════════════════════════════════════════════════════════

@runtime_checkable
class Neo4jTableSchemaService(Protocol):
    """
    Neo4j 表结构查询服务
    原始实现: app/ai_chat_agents/multi_call.py MultiCallService._get_table_scheme_from_neo4j
    """
    async def get_table_scheme(self, table_names: List[str]) -> str:
        """
        根据表名列表查询 DDL，返回 DDL 字符串。
        若查询失败，抛出异常，由调用方降级到默认 DDL。
        """
        ...


@runtime_checkable
class MilvusQARecallService(Protocol):
    """
    Milvus 问答对向量召回服务
    原始实现: app/ai_chat_agents/multi_call.py MultiCallService._recall_qa_pairs_as_array
    """
    async def recall_similar_questions(self, question: str, top_k: int) -> str:
        """
        返回 JSON 字符串，格式: [{"question": str, "sql": str}, ...]
        """
        ...


# ─────────────────────────────────────────────
# 1. 数据类：入参 / 出参
# ─────────────────────────────────────────────

@dataclass
class MetricInfo:
    """维度信息（与 recognize_intent.MetricInfo 保持一致）"""
    metric_name: str
    metric_code: str
    table_name: str
    metric_desc: str
    value: str
    original_value: str
    logic_dsl: str
    join: str = ""


@dataclass
class IndicatorMetricInfo:
    """指标维度信息"""
    indicator_name: str
    indicator_code: str
    indicator_metadata: str
    aggregation: str
    metric_info: List[MetricInfo] = field(default_factory=list)


@dataclass
class MultiCallInput:
    """多路召回的最小化入参"""
    user_message: str                                                     # 用户问题
    indicator_metrict: List[IndicatorMetricInfo] = field(default_factory=list)  # 来自意图识别
    memory_id: str = ""
    connection_id: int = 0
    l1_concepts: Dict[str, Any] = field(default_factory=dict)            # 兜底候选来源
    vector_candidates: Dict[str, Any] = field(default_factory=dict)      # 兜底候选来源


@dataclass
class MultiCallOutput:
    """多路召回的出参，即 SQLGeneratorContext 所需的全部字段"""
    user_message: str
    memory_id: str
    current_date: str
    table_scheme: str                                   # Neo4j 返回的 DDL
    indicator_metric: List[Dict[str, Any]]              # 转换后的 dict 格式指标列表
    Q_A_pairs: List[Dict[str, str]]                    # Milvus 召回的问答对
    connection_id: int = 0
    l1_concepts: Dict[str, Any] = field(default_factory=dict)
    vector_candidates: Dict[str, Any] = field(default_factory=dict)


# ─────────────────────────────────────────────
# 2. 核心业务类
# ─────────────────────────────────────────────

class MultiCallSkill:
    """
    多路召回技能

    完整还原 MultiCallService.execute_multi_call 逻辑：
      Step 1: 从 IndicatorMetricInfo 提取去重后的表名
      Step 2: 并行执行 Neo4j 表结构召回 + Milvus QA 对召回
      Step 3: 将 IndicatorMetricInfo 列表转换为 dict 格式
      Step 4: 组装并返回 MultiCallOutput

    外部依赖通过构造器注入（均为可选，不注入时降级到默认值）：
      neo4j_query_fn  : async (table_names: List[str]) -> str
                        返回 DDL 字符串；不注入时返回内置默认 DDL。
      milvus_recall_fn: async (question: str, top_k: int) -> str
                        返回 JSON 字符串（list[{question, sql}]）；不注入时返回 []。
    """

    DEFAULT_DDL = """
CREATE TABLE `ads_bi_pos_ord_sale_pt_d_1df_2mi` (
    `dt`        VARCHAR(8)    COMMENT '日期',
    `shop_code` VARCHAR(32)   COMMENT '店铺编码',
    `shop_name` VARCHAR(128)  COMMENT '店铺名称',
    `sku_code`  VARCHAR(64)   COMMENT 'SKU编码',
    `sku_name`  VARCHAR(256)  COMMENT 'SKU名称',
    `net_amt`   DECIMAL(18,2) COMMENT '净销售额',
    `net_cnt`   INT           COMMENT '销售数量',
    `ord_cnt`   INT           COMMENT '订单数'
) ENGINE=OLAP;
-- 默认表结构，实际应从 Neo4j 查询获取
"""

    def __init__(
            self,
            neo4j_service: Optional[Neo4jTableSchemaService] = None,
            milvus_service: Optional[MilvusQARecallService] = None,
            qa_top_k: int = 5,
    ):
        """
        Args:
            neo4j_service:  Neo4jTableSchemaService 实现，负责查询表结构 DDL；
                            不传则降级到内置默认 DDL（DEFAULT_DDL）。
            milvus_service: MilvusQARecallService 实现，负责向量召回 QA 对；
                            不传则跳过 QA 召回，返回空列表。
            qa_top_k:       Milvus 召回 Top-K 数量，默认 5。
        """
        self.neo4j_service  = neo4j_service
        self.milvus_service = milvus_service
        self.qa_top_k       = qa_top_k

    # ──────────────────────────────────────────────────────────────────
    # 对外唯一入口
    # ──────────────────────────────────────────────────────────────────

    async def run(self, inp: MultiCallInput) -> MultiCallOutput:
        """
        执行多路召回（完整还原 MultiCallService.execute_multi_call）

        Step 1: 提取表名
        Step 2: 并行调用 Neo4j + Milvus
        Step 3: 转换指标格式
        Step 4: 组装输出
        """
        logger.info(f"开始多路召回: query='{inp.user_message}'")

        # Step 1: 提取唯一表名（原 _extract_table_names）
        table_names = self._extract_table_names(inp.indicator_metrict)
        logger.info(f"提取到 {len(table_names)} 个表名: {table_names}")

        # Step 2: 并行召回（原 asyncio.gather(neo4j_task, milvus_task)）
        neo4j_task = self._get_table_scheme(table_names)
        milvus_task = self._recall_qa_pairs(inp.user_message, self.qa_top_k)
        table_scheme, q_a_pairs = await asyncio.gather(neo4j_task, milvus_task)

        logger.info(f"Neo4j 表结构召回完成，Milvus 问答对: {len(q_a_pairs)} 条")

        # Step 3: 转换指标格式（原 _convert_indicator_metrics）
        indicator_metrics = self._convert_indicator_metrics(inp.indicator_metrict)

        # Step 4: 组装输出
        return MultiCallOutput(
            user_message=inp.user_message,
            memory_id=inp.memory_id,
            current_date=datetime.now().strftime("%Y-%m-%d"),
            table_scheme=table_scheme,
            indicator_metric=indicator_metrics,
            Q_A_pairs=q_a_pairs,
            connection_id=inp.connection_id,
            l1_concepts=inp.l1_concepts,
            vector_candidates=inp.vector_candidates,
        )

    # ──────────────────────────────────────────────────────────────────
    # 私有方法（与原 MultiCallService 方法 1:1 对应）
    # ──────────────────────────────────────────────────────────────────

    def _extract_table_names(self, indicator_metrict: List[IndicatorMetricInfo]) -> List[str]:
        """
        从 IndicatorMetricInfo 列表中提取所有表名并去重（原 _extract_table_names）

        来源：
          - indicator.indicator_metadata  (主表)
          - metric.table_name             (关联表)
        """
        table_names_set: set = set()
        for indicator in indicator_metrict:
            if indicator.indicator_metadata:
                table_names_set.add(indicator.indicator_metadata)
            for metric in indicator.metric_info:
                if metric.table_name:
                    table_names_set.add(metric.table_name)
        return sorted(list(table_names_set))

    async def _get_table_scheme(self, table_names: List[str]) -> str:
        """
        从 Neo4j 获取表结构 DDL（原 _get_table_scheme_from_neo4j）

        原始实现: MultiCallService._get_table_scheme_from_neo4j
          - 调用 self.neo4j_adapter.service.ask(query)（同步）
          - 在 async 上下文中用 asyncio.to_thread 包装
          - 失败时降级到默认 DDL

        此处通过 Neo4jTableSchemaService 接口调用；未注入则降级。
        """
        if not table_names:
            logger.warning("未提供表名，使用默认 DDL")
            return self.DEFAULT_DDL

        if not self.neo4j_service:
            logger.warning("neo4j_service 未注入，使用默认 DDL")
            return self.DEFAULT_DDL

        try:
            result = await self.neo4j_service.get_table_scheme(table_names)
            if result and result.strip():
                return result
            logger.warning("Neo4j 返回空结果，使用默认 DDL")
            return self.DEFAULT_DDL
        except Exception as e:
            logger.error(f"Neo4j 查询失败: {e}")
            return self.DEFAULT_DDL

    async def _recall_qa_pairs(self, question: str, top_k: int) -> List[Dict[str, str]]:
        """
        从 Milvus 召回相似 QA 对（原 _recall_qa_pairs_as_array）

        原始实现: MultiCallService._recall_qa_pairs_as_array
          - 调用 self.milvus_adapter.recall_similar_questions(question, top_k)（async）
          - 解析返回的 JSON 字符串为 [{question, sql}] 数组

        此处通过 MilvusQARecallService 接口调用；未注入则返回空列表。
        """
        if not self.milvus_service:
            logger.warning("milvus_service 未注入，跳过 QA 对召回")
            return []

        try:
            response = await self.milvus_service.recall_similar_questions(question, top_k)
            return self._parse_qa_response_to_array(response, top_k)
        except Exception as e:
            logger.error(f"Milvus QA 对召回失败: {e}")
            return []

    def _parse_qa_response_to_array(self, response: str, top_k: int) -> List[Dict[str, str]]:
        """
        解析 Milvus 返回的 JSON 字符串为 [{question, sql}] 数组（原 _parse_qa_response_to_array）
        """
        try:
            cleaned = response.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()

            qa_pairs_data = json.loads(cleaned)
            if isinstance(qa_pairs_data, list):
                return [
                    {"question": item.get("question", ""), "sql": item.get("sql", "")}
                    for item in qa_pairs_data[:top_k]
                    if isinstance(item, dict)
                ]
            logger.warning(f"Milvus 返回格式不是 list，类型: {type(qa_pairs_data)}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"解析 Milvus JSON 失败: {e}")
            return []
        except Exception as e:
            logger.error(f"处理 Milvus 结果异常: {e}")
            return []

    def _convert_indicator_metrics(
            self, indicator_metrics: List[IndicatorMetricInfo]
    ) -> List[Dict[str, Any]]:
        """
        将 IndicatorMetricInfo dataclass 列表转换为 dict 格式（原 _convert_indicator_metrics）
        """
        result = []
        for metric in indicator_metrics:
            result.append({
                "indicator_name":     metric.indicator_name,
                "indicator_code":     metric.indicator_code,
                "indicator_metadata": metric.indicator_metadata,
                "aggregation":        metric.aggregation,
                "metric_info": [
                    {
                        "metric_name":    m.metric_name,
                        "metric_code":    m.metric_code,
                        "table_name":     m.table_name,
                        "metric_desc":    m.metric_desc,
                        "logic_dsl":      m.logic_dsl,
                        "original_value": m.original_value,
                        "value":          m.value,
                        "join":           m.join,
                    }
                    for m in metric.metric_info
                ],
            })
        return result


# ═══════════════════════════════════════════════════════════════════
# 3.  真实服务实现（独立运行时使用）
# ═══════════════════════════════════════════════════════════════════

def _load_dotenv() -> None:
    from pathlib import Path
    try:
        from dotenv import load_dotenv
        search_path = Path(__file__).resolve().parent
        for _ in range(8):
            for name in (".env", ".env.dev", ".env.local"):
                env_file = search_path / name
                if env_file.exists():
                    load_dotenv(env_file, override=False)
                    print(f"[配置] 已加载: {env_file}")
                    return
            search_path = search_path.parent
        print("[配置] 未找到 .env，使用系统环境变量")
    except ImportError:
        print("[警告] pip install python-dotenv")


class _RealNeo4jService:
    """
    真实 Neo4j 表结构查询服务
    - 根据表名列表查询各表的列信息，拼装为 CREATE TABLE DDL 字符串
    使用 .env 中的 NEO4J_URI / NEO4J_USER / NEO4J_PASSWORD 配置
    """

    def __init__(self) -> None:
        import os
        from neo4j import GraphDatabase

        uri      = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user     = os.getenv("NEO4J_USER", "neo4j")
        password = os.getenv("NEO4J_PASSWORD", "")
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
        self._driver.verify_connectivity()
        logger.info(f"Neo4j 连接成功: {uri}")

    def close(self) -> None:
        self._driver.close()

    def _query_table_columns(self, table_name: str) -> List[Dict[str, Any]]:
        """查询单张表的字段列表（从 columns_json 字段解析）"""
        import json as _json
        label = "FactTable" if ("ads_" in table_name or "ods_" in table_name) else "DimensionTable"
        cypher = f"""
            MATCH (t:{label} {{table_name: $table_name}})
            RETURN t.columns_json AS columns_json
        """
        with self._driver.session() as session:
            result = session.run(cypher, {"table_name": table_name})
            record = result.single()
            if not record:
                return []
            try:
                cols = _json.loads(record["columns_json"] or "[]")
                return [c for c in cols if c.get("name") != "dt"]
            except Exception:
                return []

    def _columns_to_ddl(self, table_name: str, columns: List[Dict[str, Any]]) -> str:
        """将列信息列表转换为 CREATE TABLE DDL"""
        lines = []
        for col in columns:
            name    = col.get("name", "unknown")
            dtype   = col.get("type", "VARCHAR(255)")
            comment = col.get("comment") or col.get("description", "")
            line    = f"    `{name}` {dtype}"
            if comment:
                line += f" COMMENT '{comment}'"
            lines.append(line)
        cols_str = ",\n".join(lines) if lines else "    -- 无列信息"
        return f"CREATE TABLE `{table_name}` (\n{cols_str}\n) ENGINE=OLAP;\n"

    async def get_table_scheme(self, table_names: List[str]) -> str:
        """查询多张表的 DDL，拼接为字符串返回"""
        ddl_parts: List[str] = []
        for table_name in table_names:
            try:
                cols = await asyncio.to_thread(self._query_table_columns, table_name)
                ddl_parts.append(self._columns_to_ddl(table_name, cols))
            except Exception as e:
                logger.warning(f"查询表结构失败 {table_name}: {e}")
                ddl_parts.append(f"-- 无法获取表 {table_name} 的结构\n")
        return "\n".join(ddl_parts)


class _RealMilvusQAService:
    """
    真实 Milvus QA 对向量召回服务
    - recall_similar_questions → 向量搜索，返回 JSON 字符串 [{question, sql}]
    使用 .env 中的 MILVUS_* / EMBEDDING_* 配置
    """

    def __init__(self) -> None:
        import os, json as _json
        from pymilvus import MilvusClient as PyMilvusClient
        from openai import OpenAI

        host       = os.getenv("MILVUS_HOST", "localhost")
        port       = int(os.getenv("MILVUS_PORT", "19530"))
        user       = os.getenv("MILVUS_USER", "")
        password   = os.getenv("MILVUS_PASSWORD", "")
        db_name    = os.getenv("MILVUS_DB_NAME", "default")
        self._collection = os.getenv("MILVUS_COLLECTION", "dev_vanna_sql")

        uri    = f"http://{host}:{port}"
        kwargs = {"uri": uri}
        if user and password:
            kwargs.update({"user": user, "password": password, "db_name": db_name})
        self._milvus = PyMilvusClient(**kwargs)

        self._embed_client = OpenAI(
            api_key=os.getenv("EMBEDDING_API_KEY", ""),
            base_url=os.getenv("EMBEDDING_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
        )
        self._embed_model = os.getenv("EMBEDDING_MODEL", "text-embedding-v4")

    def _vectorize(self, text: str) -> List[float]:
        resp = self._embed_client.embeddings.create(
            model=self._embed_model, input=[text], dimensions=1024, encoding_format="float"
        )
        return resp.data[0].embedding

    async def recall_similar_questions(self, question: str, top_k: int) -> str:
        import json as _json
        try:
            vec = await asyncio.to_thread(self._vectorize, question)
            results = self._milvus.search(
                collection_name=self._collection,
                data=[vec],
                anns_field="vector",
                search_params={"metric_type": "L2", "params": {"nprobe": 10}},
                limit=top_k,
                output_fields=["id", "text", "sql"],
            )
            qa_list = []
            for hits in results:
                for hit in hits:
                    entity = hit.get("entity", {})
                    if entity.get("text") and entity.get("sql"):
                        qa_list.append({"question": entity["text"], "sql": entity["sql"]})
            return _json.dumps(qa_list, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Milvus QA 召回失败: {e}")
            return "[]"


# ═══════════════════════════════════════════════════════════════════
# 4.  流水线工作目录 & main 入口（可独立运行）
# ═══════════════════════════════════════════════════════════════════

def _get_workflow_dir() -> "Path":  # type: ignore[name-defined]
    """
    返回技能流水线共享工作目录：<skills根>/.workflow/
    目录不存在时自动创建。

    所有 *_output.json 统一存放于此目录，各技能通过约定的文件名衔接：
        rewrite_output.json → intent_output.json → multicall_output.json
        → sql_output.json → audit_output.json
    """
    from pathlib import Path
    skills_root = Path(__file__).resolve().parent.parent   # skills/
    wf_dir = skills_root / ".workflow"
    wf_dir.mkdir(parents=True, exist_ok=True)
    return wf_dir


def _backup_if_exists(path: "Path") -> None:  # type: ignore[name-defined]
    """将 path 文件备份为 .bak.json，覆盖旧备份"""
    from pathlib import Path
    p = Path(path)
    if p.exists():
        bak = p.parent / (p.stem + ".bak.json")
        p.replace(bak)


async def main() -> None:
    """
    独立运行入口

    读取上一步 intent_output.json，执行多路召回（Neo4j 表结构 + Milvus QA 对）。

    用法（从任意目录均可运行，输入/输出统一在 skills/.workflow/）:
        python multi_call.py
        python multi_call.py --input /path/to/intent_output.json
        python multi_call.py --clean       # 清理本步及后续输出再运行

    输出文件 multicall_output.json 供下一步 sql_generator.py 读取。
    """
    import argparse, os, json as _json
    from pathlib import Path

    wf = _get_workflow_dir()
    default_input  = str(wf / "intent_output.json")
    default_output = str(wf / "multicall_output.json")

    parser = argparse.ArgumentParser(description="多路召回技能 — 独立运行")
    parser.add_argument("--input",  default=default_input,  help=f"上一步输出文件 (默认: {default_input})")
    parser.add_argument("--output", default=default_output, help=f"本步输出文件 (默认: {default_output})")
    parser.add_argument("--clean",  action="store_true",    help="运行前删除本步及后续输出文件")
    args = parser.parse_args()

    if args.clean:
        for name in ("multicall_output.json", "sql_output.json", "audit_output.json"):
            stale = wf / name
            if stale.exists():
                stale.unlink()
                print(f"[清理] 已删除: {stale}")

    # 1. 加载环境变量
    _load_dotenv()

    # 2. 读取上一步输出
    if not os.path.exists(args.input):
        print(f"[错误] 找不到输入文件 {args.input}，请先运行 recognize_intent.py")
        return

    with open(args.input, encoding="utf-8") as f:
        prev = _json.load(f)

    # 若上一步已命中 QA 对，直接透传
    if prev.get("is_qa_shortcut") and prev.get("matched_sql"):
        print("[跳过] 上一步已命中 QA 对，直接透传 SQL")
        result = {
            "is_qa_shortcut":   True,
            "matched_sql":      prev["matched_sql"],
            "user_message":     prev.get("final_query", ""),
            "indicator_metric": [],
            "Q_A_pairs":        [],
            "table_scheme":     "",
            "current_date":     datetime.now().strftime("%Y-%m-%d"),
            "memory_id":        "",
            "connection_id":    0,
            "l1_concepts":      {},
            "vector_candidates":{},
        }
        with open(args.output, "w", encoding="utf-8") as f:
            _json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"[输出] 已保存到: {args.output}")
        return

    query            = prev.get("final_query", "")
    indicator_metric = prev.get("indicator_metric", [])
    l1_concepts      = prev.get("l1_concepts", {})
    vector_candidates= prev.get("vector_candidates", {})

    if not query:
        print("[错误] 输入文件中缺少 final_query 字段")
        return

    # 3. 初始化真实服务
    neo4j_service   = None
    milvus_service  = None
    try:
        neo4j_service  = _RealNeo4jService()
    except Exception as e:
        print(f"[警告] Neo4j 连接失败: {e}，将使用默认 DDL")
    try:
        milvus_service = _RealMilvusQAService()
    except Exception as e:
        print(f"[警告] Milvus 连接失败: {e}，QA 对召回将跳过")

    # 4. 构建 MultiCallInput
    metric_objs = []
    for im in indicator_metric:
        metric_info_list = [
            MetricInfo(
                metric_name=m.get("metric_name", ""),
                metric_code=m.get("metric_code", ""),
                table_name=m.get("table_name", ""),
                metric_desc=m.get("metric_desc", ""),
                value=m.get("value", ""),
                original_value=m.get("original_value", ""),
                logic_dsl=m.get("logic_dsl", ""),
                join=m.get("join", ""),
            )
            for m in im.get("metric_info", [])
        ]
        metric_objs.append(IndicatorMetricInfo(
            indicator_name=im.get("indicator_name", ""),
            indicator_code=im.get("indicator_code", ""),
            indicator_metadata=im.get("indicator_metadata", ""),
            aggregation=im.get("aggregation", ""),
            metric_info=metric_info_list,
        ))

    inp = MultiCallInput(
        user_message=query,
        indicator_metrict=metric_objs,
        l1_concepts=l1_concepts,
        vector_candidates=vector_candidates,
    )

    # 5. 执行多路召回
    skill = MultiCallSkill(
        neo4j_service=neo4j_service,
        milvus_service=milvus_service,
    )

    print(f"\n[运行] 多路召回: '{query}'")
    output = await skill.run(inp)

    # 6. 清理 Neo4j 连接
    if neo4j_service:
        try:
            neo4j_service.close()
        except Exception:
            pass

    # 7. 整理并保存输出
    result = {
        "is_qa_shortcut":    False,
        "matched_sql":       None,
        "user_message":      output.user_message,
        "memory_id":         output.memory_id,
        "current_date":      output.current_date,
        "table_scheme":      output.table_scheme,
        "indicator_metric":  output.indicator_metric,
        "Q_A_pairs":         output.Q_A_pairs,
        "connection_id":     output.connection_id,
        "l1_concepts":       output.l1_concepts,
        "vector_candidates": output.vector_candidates,
    }

    _backup_if_exists(args.output)
    with open(args.output, "w", encoding="utf-8") as f:
        _json.dump(result, f, ensure_ascii=False, indent=2)

    # 8. 打印摘要
    print(f"\n{'='*60}")
    print(f"问题        : {output.user_message}")
    print(f"日期        : {output.current_date}")
    print(f"QA 对数量   : {len(output.Q_A_pairs)}")
    print(f"DDL 长度    : {len(output.table_scheme)} 字符")
    print(f"{'='*60}")
    print(f"[输出] 已保存到: {args.output}")
    print(f"[下一步] python ../sql-generator/sql_generator.py   (读取 {args.output})")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    )
    asyncio.run(main())
