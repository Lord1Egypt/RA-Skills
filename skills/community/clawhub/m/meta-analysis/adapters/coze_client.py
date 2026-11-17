"""
adapters/coze_client.py — meta-analysis 技能 → Coze 工作流 主路径客户端

设计（coze 唯一主路径）：
- 这是技能的**唯一计算路径**客户端。R 引擎（metafor/meta/netmeta + dispatcher run_task.R）
  运行在 coze 元分析工作流（src/r_engine/ + src/graphs/nodes/meta_analysis.py）。
- 本客户端把分析请求打包成信封，POST 到 coze 工作流的 /run 端点，解析返回的 JSON 结果
  （status / stats / figures[].svg / warnings / notes）。
- 数值判断由 coze 端 R 计算产出，本客户端只解析结构、绝不读取/改写数值结论。
- 接口契约见 coze 项目的 coze_contract.md（不随技能发布）。
- ⚠️ 回退已取消（2026-08-26）：coze 不可达 / 未授权时本客户端直接抛错，不再兜底本地引擎；
  原本地引擎 `adapters/_dev/local_engine.py` 已于 2026-09-01 按架构终态原则删除
  （原则：coze 为唯一计算真相源，本地不保留计算引擎）。

配置（环境变量）：
  COZE_META_ENDPOINT  工作流 /run 地址，默认 https://ct-meta.coze.site/run（2026-08-26 改造：
                     主工作流由 ct-meta2 互换为 ct-meta，新 token 见 adapters/coze_token.py）
  （回退）若该端点因 token 不一致返回 401/403，自动改用 FALLBACK_ENDPOINT
         （https://ct-meta2.coze.site/run，token 自动切换为 ct-meta2 专属 token）并重试；
         成功后结果附 _coze_endpoint_notice 提示。详见常量 FALLBACK_ENDPOINT。
  COZE_META_TOKEN    可选鉴权令牌（Bearer，全局覆盖所有端点）；留空则按 endpoint 取
                     adapters/coze_token.py 内嵌的公开 blob（随技能发布）
  COZE_META_TIMEOUT   请求超时秒数，默认 600

⚠️ 出站披露（ct-base §5 安全模型，全库强制）：
  本模块会把**分析数据**（研究事件数 / 样本量 / 效应量等，不含个人身份信息）POST 到
  coze 工作流端点（默认 https://ct-meta.coze.site/run）执行云端 R 计算。首次出站前
  须经用户确认（AUTH-BLOCK + 统一文案，见 _auth_gate）；确认后端点写入 config.json
  auto_approve_endpoints 白名单，后续免确认。未授权时直接抛 AuthRequiredError，
  由上层 run_analysis 转为结构化错误返回（不再兜底本地引擎）。payload 发送前经
  sanitize_payload() 脱敏。

依赖：标准库（urllib / json / os / re / sys）+ 同目录 coze_token（凭据解析，仅标准库）。
"""

import copy
import hashlib
import json
import mimetypes
import os
import re
import shutil
import socket
import subprocess
import sys
import threading
import time
import urllib.request
import urllib.error
import uuid

try:  # 作为包导入（adapters.coze_client）
    from .coze_token import get_token_for
except ImportError:  # 平铺模块直接运行（run_analysis 把 adapters 加入 sys.path）
    try:
        from coze_token import get_token_for
    except ImportError:
        get_token_for = None  # 极端情况：仅回退到 COZE_META_TOKEN 环境变量

# 出站信封前置校验 + 自动修复（2026-09-13 新增）：POST 前按 coze_contract.md 校验，
# 拦截装错的信封（无论来自 LLM 手搓 / 用户裸 POST / build_request 回归），并自动修复
# 最常见的结构错误（并行顶层数组 → data.rows[]、model random→REML、measure→sm）。
# 致命不合规 → 抛 EnvelopeValidationError（绝不发出去）。
try:
    from .coze_contract_validate import (
        validate_request as _validate_request_impl,
        EnvelopeValidationError as _EnvelopeValidationError,
    )
except ImportError:  # 平铺模块直接运行
    try:
        from coze_contract_validate import (
            validate_request as _validate_request_impl,
            EnvelopeValidationError as _EnvelopeValidationError,
        )
    except ImportError:
        _validate_request_impl = None
        _EnvelopeValidationError = None

# 公开别名（供 run_analysis / 上层 import）：EnvelopeValidationError
EnvelopeValidationError = _EnvelopeValidationError

# 2026-08-26 改造：主分析工作流切到 ct-meta2（新 token，aud=5v9HMQWtTSzxrEeZjI7kJJEzeMPrHXny），
# 同日后续互换：主工作流回切 ct-meta（旧 token，aud=oxwSsfwdtRRfByYIM8Xg3U4RQH5OgEjO），
# ct-meta2 降级为回退（新 token）。2026-08-31 起端点选择改由下方「开发期策略覆盖」段
# 按 DEV_POLICY.json 动态决定（默认生产态仍是 ct-meta 主 / ct-meta2 回退），故此处不再
# 硬编码 DEFAULT/FALLBACK，统一在文末覆盖段定义。


# 触发回退时向用户呈现的说明（主工作流地址已切换，已自动回退到备用 coze 端点）。
ENDPOINT_FALLBACK_NOTICE = (
    "主分析工作流地址已切换，本次分析已自动回退到备用 coze 端点完成"
)

# === 开发期策略覆盖（2026-08-31 起，meta-analysis 架构重构开发期）===
# 单源真相：本目录 DEV_POLICY.json 的 ct_meta_disabled 标志。
# 该期间用户要求：禁用 ct-meta 调用，coze 唯一站点 = ct-meta2，且不回退 ct-meta。
# 结束开发期时：删除 DEV_POLICY.json 并还原本段（DEFAULT/FALLBACK 回切 ct-meta/ct-meta2）。
_DEV_POLICY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "DEV_POLICY.json")


def _dev_ct_meta_disabled() -> bool:
    """读取开发期策略：是否禁用 ct-meta（仅走 ct-meta2）。无策略文件 → 正常生产态。"""
    try:
        with open(_DEV_POLICY_PATH, "r", encoding="utf-8") as _f:
            return bool(json.load(_f).get("ct_meta_disabled", False))
    except Exception:
        return False


if _dev_ct_meta_disabled():
    # 开发期：ct-meta2 为唯一站点，禁用 ct-meta（FALLBACK 置空 → 任何回退都不发生）
    DEFAULT_ENDPOINT = "https://ct-meta2.coze.site/run"
    FALLBACK_ENDPOINT = ""
else:
    # 正常生产态（无 DEV_POLICY.json 或 ct_meta_disabled=false）
    DEFAULT_ENDPOINT = "https://ct-meta.coze.site/run"
    FALLBACK_ENDPOINT = "https://ct-meta2.coze.site/run"

# 2026-08-29（ct-base §20.9 修订）：**删除版本号比对**——原 `EXPECTED_COZE_ENVELOPE_VERSION`
# 常量与 `_coze_version` / `_contract_version` 的比对逻辑一并移除。版本由 coze 端随发布
# 同步，本地不比对；**任何仅版本号差异（无数据内容/结构变化）一律不提示**，避免无谓打扰。
# 契约检测自此只做一件事：coze 返回的**数据内容/结构**与本地消费接口是否一致
# （见 _assess_contract）。coze 端 `_coze_version` 注入可保留，本地不再消费。

# 并发调用保护（用户 2026-08-28 要求）：多次 coze 出站调用之间**必须间隔 ≥1 秒**，
# 防止触发 coze 端限流（实测曾因密集请求被 429 限流至次日）。
# 实现：模块级锁 + 单调时钟，串行化"间隔决策"并强制最小间隔。间隔秒数可由
# 环境变量 COZE_META_MIN_INTERVAL（浮点秒）覆写，<=0 时关闭保护。
_RATE_LIMIT_LOCK = threading.Lock()
_LAST_CALL_TS = 0.0  # time.monotonic() of the most recently dispatched coze POST


def _assess_contract(parsed: dict) -> tuple:
    """coze 响应「数据内容/结构一致性」契约检测（单一入口，ct-base §20.9 范本）。

    2026-08-28 综合定稿：把 meta-analysis 的结构漂移自适应与 ct-base 的旧机制统一到
    本函数。2026-08-29 修订（ct-base §20.9 同步）：**移除版本漂移检测**——版本号差异
    不再触发任何提醒，只有数据内容/结构与本地接口对不上时才提示。

    唯一的检测信号（自愈优先）：
      结构/数据内容漂移：识别已知字段别名并自适应归一化（quality_gate / checks /
      pooled / figures 形态），保证报告仍能渲染；映射发生时记 drift 说明。
      对无法自适应的结构缺失，仅记录告警、不臆造数据。

    ⚠️ 以下情况**一律不提示**（零噪音原则）：
      - coze 返回 `_coze_version` / `_contract_version` 与本地不同（版本由发布同步，
        本地不比对）；
      - coze 未注入版本标记；
      - 结构一致、无别名映射发生。

    Returns: (parsed, drift_notes, needs_upgrade)
      drift_notes 非空 => 已自适应或检测到不一致，交给 rendering.py 在 HTML 横幅提示升级；
      needs_upgrade 仅为机器可读标记（写回 parsed），本函数**不产生任何用户可见提示**
      （用户可见提示统一只在渲染层的 HTML 横幅，避免 stderr / notes 重复提示）。
    """
    if not isinstance(parsed, dict):
        return parsed, [], False
    notes = []
    p = parsed

    # ---- 结构漂移：已知字段别名 → 本地期望字段（仅当期望字段缺失、且别名存在时映射）----
    # 1) 质量评估块
    if not isinstance(p.get("quality_gate"), dict):
        for a in ("quality_gate_v2", "qgate", "quality", "qagate"):
            if isinstance(p.get(a), dict):
                p["quality_gate"] = p[a]
                if a in p:
                    del p[a]
                notes.append(f"coze 响应字段已变更：质量评估由 `{a}` 改为 `quality_gate`，已自动适配")
                break
    if isinstance(p.get("quality_gate"), dict):
        qg = p["quality_gate"]
        if "checks" not in qg:
            for ca in ("items", "list", "entries", "checks_list"):
                if isinstance(qg.get(ca), list):
                    qg["checks"] = qg[ca]
                    if ca in qg:
                        del qg[ca]
                    notes.append(f"coze 响应字段已变更：质量评估条目由 `{ca}` 改为 `checks`，已自动适配")
                    break

    # 2) 合并效应量
    if isinstance(p.get("stats"), dict):
        st = p["stats"]
        if not isinstance(st.get("pooled"), dict):
            for pa in ("estimate", "effect", "pooled_estimate"):
                if isinstance(st.get(pa), dict):
                    st["pooled"] = st[pa]
                    notes.append(f"coze 响应字段已变更：合并效应量由 `{pa}` 改为 `pooled`，已自动适配")
                    break

    # 3) figures 结构兜底（dict → list；图体别名 image/svg_data/base64 → svg）
    figs = p.get("figures")
    if isinstance(figs, dict):
        p["figures"] = [
            {"type": k, "svg": v} for k, v in figs.items() if isinstance(v, str)
        ]
        notes.append("coze 响应结构已变更：figures 由 dict 改为 list，已自动适配")
    elif isinstance(figs, list):
        for i, f in enumerate(figs):
            if isinstance(f, dict) and "svg" not in f and "url" not in f:
                for fa in ("image", "svg_data", "base64"):
                    if isinstance(f.get(fa), str):
                        f["svg"] = f[fa]
                        notes.append(f"coze 响应字段已变更：figures[{i}] 图体由 `{fa}` 改为 `svg`，已自动适配")
                        break

    # 原「4) 版本漂移」已于 2026-08-29 移除（ct-base §20.9 修订）：
    # coze 返回 `_coze_version` / `_contract_version` 与本地不同**不再触发提醒**——
    # 版本由 coze 端随发布同步，本地只检测数据内容/结构一致性。
    # 相关常量 EXPECTED_COZE_ENVELOPE_VERSION 已一并删除，避免死代码。

    # 去重（保持顺序）
    seen, uniq = set(), []
    for n in notes:
        if n not in seen:
            seen.add(n)
            uniq.append(n)
    return p, uniq, bool(uniq)


def _endpoint() -> str:
    return os.environ.get("COZE_META_ENDPOINT", DEFAULT_ENDPOINT).rstrip("/")


def _acquire_rate_limit() -> None:
    """并发调用保护：确保相邻两次 coze POST 之间**至少间隔 1 秒**（可由
    COZE_META_MIN_INTERVAL 覆写），避免触发 coze 端限流（429）。

    用模块级锁串行化"间隔决策"，仅在决策期间持锁（含必要的 sleep 占位），
    网络请求本身在锁释放后发出——既保证 ≥1s 间距，又不把网络延迟锁在临界区内。

    作用域：同一 Python 进程内的多线程并发（本技能典型调用场景）。跨进程并发
    需另加文件锁，当前未实现（如需多进程同时调用 coze，再扩展）。
    """
    try:
        interval = float(os.environ.get("COZE_META_MIN_INTERVAL", "1.0"))
    except (TypeError, ValueError):
        interval = 1.0
    if interval <= 0:
        return
    global _LAST_CALL_TS
    with _RATE_LIMIT_LOCK:
        now = time.monotonic()
        wait = interval - (now - _LAST_CALL_TS)
        if wait > 0:
            time.sleep(wait)
            now = time.monotonic()
        _LAST_CALL_TS = now


# --------------------------------------------------------------------------
# 归因标识（query_origin）— 2026-08-29 修复
# --------------------------------------------------------------------------
# 原设计把 query_origin 的计算放在 run_analysis.py，再作为参数传进 run_meta；
# 直接调用本模块的路径（__main__ 自测 / coze_integration_test / deploy_retest
# --live / 外部脚本）都不传 → coze 端 `state.query_origin or ""` 兜底成空串 →
# 飞书归因列空白，且**绕过了按 query_origin 计的限流**。现下沉到本模块：
# 任何调用路径都自动带上归因，无法为空。
def _default_query_origin(debug: bool = False) -> str:
    """主机名 SHA-256 作为调用发起来源标识（"sha256:" + 64hex）。

    debug=True 时前缀 "debug:"——调试/冒烟流量在飞书归因列可直接筛出，
    不与真实用户流量混计（2026-08-29：排查发现自测调用污染了生产日志表）。
    """
    try:
        host = socket.gethostname() or "unknown"
    except Exception:  # noqa: BLE001
        host = "unknown"
    digest = hashlib.sha256(host.encode("utf-8")).hexdigest()
    return ("debug:sha256:" if debug else "sha256:") + digest


# 入口标识（entry_point）— 2026-10-07 新增
# 区分调用来源：技能本身（"skill"） vs 工作台 web 应用（"workbench"）。
# 透传写入飞书 entry_point 列，供后台按来源筛选/统计。
# 默认 "skill"；工作台进程在 fullflow 入口调用 set_entry_point("workbench") 覆盖。
_ENTRY_POINT = "skill"


def set_entry_point(value: str) -> None:
    """覆盖进程级入口标识（工作台调用以标记 workbench）。"""
    global _ENTRY_POINT
    _ENTRY_POINT = value or "skill"


# --------------------------------------------------------------------------
# ct-base coze_io_contract：skill_version（顶层） + user_language（params 内）
# — 2026-09-11 补齐（此前 meta-analysis 出站信封缺这两个字段）
# --------------------------------------------------------------------------
# 契约来源：ct-base/references/coze_io_contract.md §1.1 / §1.2（全库单一事实来源）。
#   · skill_version：顶层信封字段（与 query_origin 同级），**不得**嵌套进 params/report；
#     取值 = SKILL.md frontmatter `version:`（单一事实来源，升版本免改代码），读取失败回退常量。
#   · user_language：**仅**存在于请求 params 内（顶层不得双写），zh/en；服务端读取顺序
#     params.user_language → 顶层（向后兼容）→ 空。仅供 coze 端决定文案语言，非强制覆盖。
_SKILL_VERSION_FALLBACK = "2.12.0"


def _skill_version() -> str:
    """技能版本号：读技能根 SKILL.md frontmatter 的 `version:`，失败回退常量。

    ct-base §1.2：作为**顶层**信封字段随每次出站携带，供服务端按发布版本归因调用量。
    """
    try:
        skill_md = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "SKILL.md")
        with open(skill_md, encoding="utf-8") as f:
            head = f.read(4000)
        m = re.search(r"^version:\s*([0-9][\w.\-]*)", head, re.M)
        if m:
            return m.group(1)
    except Exception:  # noqa: BLE001 — 读版本失败绝不阻断出站，回退常量
        pass
    return _SKILL_VERSION_FALLBACK


def _resolve_user_language(override: str | None = None) -> str:
    """语言提示（zh/en）—— ct-base §1.1 三级优先级。

    1) 显式 override 最高（中文语境→zh / 英文→en）；
    2) 否则按 scripts/i18n.py::_current_lang() 判定；
    3) 失败回退 "zh"。
    与 `locale`（引擎输出开关）并存，本字段仅作 caller→coze 的提示。
    """
    if override:
        v = str(override).strip().lower()
        if v.startswith("zh"):
            return "zh"
        if v.startswith("en"):
            return "en"
    try:
        _scripts = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
        if _scripts not in sys.path:
            sys.path.insert(0, _scripts)
        import i18n as _i18n  # type: ignore
        lang = (_i18n._current_lang() or "").lower()
        if lang.startswith("zh"):
            return "zh"
        if lang.startswith("en"):
            return "en"
    except Exception:  # noqa: BLE001
        pass
    return "zh"


def _with_user_language(params: dict | None, override: str | None = None) -> dict:
    """把 user_language 注入 params（已有有效值不覆盖）—— §1.1 单一承载位。"""
    out = dict(params or {})
    cur = str(out.get("user_language") or "").strip().lower()
    if cur.startswith("zh"):
        out["user_language"] = "zh"
    elif cur.startswith("en"):
        out["user_language"] = "en"
    else:
        out["user_language"] = _resolve_user_language(override)
    return out


# --------------------------------------------------------------------------
# 调用方约束：query_origin 发送层硬守卫 — 2026-08-30 新增
# --------------------------------------------------------------------------
# 背景：2.2.28 客户端已在 run_meta 自动注入 query_origin，但仍有"裸 POST /run、
# 复制契约示例、body 缺 query_origin"的调用产生飞书空归因记录（2026-08-30 实测
# CTDB_searchlog 三条）。本守卫放在**序列化发送前**——任何绕过 run_meta 注入、
# 或将来改动导致 query_origin 丢失的路径，只要走到出站这步就发不出空归因请求。
_ORIGIN_RE = re.compile(r"^(?:debug:)?sha256:[0-9a-f]{64}$")


def _assert_query_origin(payload: dict) -> str:
    """硬校验出站 payload 必须携带**有效** query_origin（调用方约束，不可绕过）。

    有效值 = `[debug:]sha256:` + 64 位十六进制（主机名哈希）。缺失 / 空串 /
    格式非法均抛 ValueError，绝不带空归因出站。
    """
    qo = (payload or {}).get("query_origin")
    if not isinstance(qo, str) or not _ORIGIN_RE.match(qo):
        raise ValueError(
            "调用方约束：出站请求必须携带有效 query_origin（[debug:]sha256:<64hex>），"
            "当前为 %r。请经 coze_client.run_meta / run_analysis 调用，或自行填充 "
            "_default_query_origin()。空归因会让调用绕过按 query_origin 计的限流，"
            "且飞书日志无法溯源。" % (qo,)
        )
    return qo


def _validate_outbound(env: dict) -> dict:
    """POST 前按 coze 契约校验出站信封；返回（可能已自动修复的）信封。

    2026-09-13 新增（用户诉求：避免装错的信封到达 coze）：
      - 校验库可用时：修复成功（ok） → 返回修复后的信封（附 _envelope_repaired 提示）；
        致命不合规 → 抛 _EnvelopeValidationError（绝不发出去，由上层转结构化错误）。
      - 校验库不可用时退化为透传（不阻断主路径，仅丢失防御性校验）。
    """
    if _validate_request_impl is None or _EnvelopeValidationError is None:
        return env
    res = _validate_request_impl(env)
    if not res.ok:
        raise _EnvelopeValidationError(env, res)
    repaired = res.repaired
    if res.repaired_notes:
        repaired = copy.deepcopy(repaired)
        repaired["_envelope_repaired"] = res.repaired_notes
    return repaired


# --------------------------------------------------------------------------
# 请求指纹 + 短窗幂等去重 — 2026-08-29 新增
# --------------------------------------------------------------------------
# 背景：一次调试中同一份数据被连续调用两次（仅 figure.plots 不同），coze 端无
# 去重、客户端只有 ≥1s 节流 → 算力翻倍、飞书记录翻倍、限流计数失真。现对
# (task, data, params, figure) 做指纹，窗口内同指纹直接复用上次结果（不发请求）。
# 作用域：进程内（与 _acquire_rate_limit 同级）；跨进程需文件锁，暂未实现。
_DEDUP_LOCK = threading.Lock()
_DEDUP_CACHE: dict = {}  # fingerprint -> (monotonic_ts, result_dict)
_DEDUP_MAX_ENTRIES = 32


def _dedup_window() -> float:
    """去重窗口秒数（COZE_META_DEDUP_WINDOW 覆写，默认 60；<=0 关闭去重）。"""
    try:
        return float(os.environ.get("COZE_META_DEDUP_WINDOW", "60.0"))
    except (TypeError, ValueError):
        return 60.0


def _dedup_fingerprint(payload: dict) -> str:
    """对请求体（task/data/params/figure）做稳定指纹。

    只取四个业务字段，忽略 request_id / _debug / query_origin 等观测字段——
    否则同一分析换个 request_id 就绕过去重。
    """
    core = {k: payload.get(k) for k in
            ("task", "data", "params", "figure", "stage", "pipeline_id",
             "contract_version", "schema")}
    blob = json.dumps(core, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def _dedup_lookup(fp: str) -> dict | None:
    """命中窗口内同指纹的历史结果则返回其深拷贝（不发出网络请求），否则 None。"""
    if _dedup_window() <= 0:
        return None
    with _DEDUP_LOCK:
        hit = _DEDUP_CACHE.get(fp)
        if not hit:
            return None
        ts, cached = hit
        if (time.monotonic() - ts) > _dedup_window():
            _DEDUP_CACHE.pop(fp, None)
            return None
        return copy.deepcopy(cached)


def _dedup_store(fp: str, result: dict) -> None:
    """仅缓存成功结果（status=ok/warn）。

    失败不缓存——否则一次偶发失败会毒化整个窗口，后续真实重试全被短路。
    """
    if _dedup_window() <= 0:
        return
    if not isinstance(result, dict) or result.get("status") not in ("ok", "warn"):
        return
    with _DEDUP_LOCK:
        if len(_DEDUP_CACHE) >= _DEDUP_MAX_ENTRIES and fp not in _DEDUP_CACHE:
            oldest = min(_DEDUP_CACHE.items(), key=lambda kv: kv[1][0])[0]
            _DEDUP_CACHE.pop(oldest, None)
        _DEDUP_CACHE[fp] = (time.monotonic(), copy.deepcopy(result))


def _resolve_token(endpoint: str = "") -> str:
    """按端点解析 coze 鉴权 token，优先级：env COZE_META_TOKEN(全局) >
    endpoint 专属内嵌 blob > 历史默认 blob。

    2026-08-26 改造：主工作流 ct-meta 与回退端点 ct-meta2 使用不同的工作流 JWT，
    故 token 按 endpoint 分别解析（coze_token.get_token_for）。
    """
    if get_token_for is not None:
        return get_token_for(endpoint) or ""
    return os.environ.get("COZE_META_TOKEN", "")


def _headers(endpoint: str = "") -> dict:
    h = {"Content-Type": "application/json"}
    tok = _resolve_token(endpoint)
    if tok:
        h["Authorization"] = "Bearer " + tok
    return h


def _timeout() -> int:
    try:
        return int(os.environ.get("COZE_META_TIMEOUT", "600"))
    except ValueError:
        return 600


def _is_token_error(code: int, body: str) -> bool:
    """判定 coze 返回是否为 token 不一致 / 鉴权失败（401/403 + token/auth/invalid 关键字）。

    仅在此类错误时触发端点回退（FALLBACK_ENDPOINT），避免掩盖其他 4xx/5xx。
    """
    if code not in (400, 401, 403):
        return False
    t = (body or "").lower()
    return any(k in t for k in ("token", "unauthor", "forbidden", "invalid", "auth"))


def _post_run(run_url: str, body: bytes, headers: dict, timeout: int):
    """POST 到 coze /run 端点，返回 (raw_text, elapsed_seconds)。

    HTTPError → 抛 _CozeHttpError（带 code/body，供 token 错误判定）；
    网络层 URLError → 抛 RuntimeError（不可达，不触发回退）。
    """
    req = urllib.request.Request(run_url, data=body, headers=headers, method="POST")
    _t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        raise _CozeHttpError(
            e.code,
            e.read().decode("utf-8", "ignore")[:1000],
            f"coze 工作流返回 HTTP {e.code}",
        )
    except urllib.error.URLError as e:
        raise RuntimeError(
            f"无法连接 coze 工作流（{run_url}）：{e.reason}。"
            f"默认端点应为 https://ct-meta.coze.site/run（如被旧配置覆盖，"
            f"请检查 COZE_META_ENDPOINT 是否误指向 localhost）。"
        )
    return raw, time.time() - _t0


# ---- ct-base §5 出站授权门控（2026-08-19 全库统一范式） ----

class AuthRequiredError(RuntimeError):
    """coze 出站未授权（首次出站须用户确认，ct-base §5 授权门控）。

    由 run_analysis.py 捕获 → 转为结构化错误返回（不再兜底本地引擎）。
    """


class _CozeHttpError(RuntimeError):
    """coze 工作流返回 HTTP 错误，携带 code/body 供调用方判断是否为 token 鉴权失败。"""

    def __init__(self, code: int, body: str, message: str):
        super().__init__(message)
        self.code = code
        self.body = body


def _config_path() -> str:
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")


def _load_config() -> dict:
    try:
        with open(_config_path(), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def _save_config(cfg: dict) -> None:
    with open(_config_path(), "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def approve_endpoint(endpoint: str) -> None:
    """用户确认后，将端点写入 auto_approve_endpoints 白名单（ct-base §5）。

    ⚠️ 仅可在**用户明确同意**后调用（agent 引导但绝不代决）；已预置端点
    （如技能作者默认放行的 coze 端点）不受影响。返回 True 表示本次调用免确认。
    """
    cfg = _load_config()
    approved = cfg.setdefault("auto_approve_endpoints", [])
    if endpoint not in approved:
        approved.append(endpoint)
        _save_config(cfg)


def _auth_gate(endpoint: str) -> bool:
    """出站授权门控：端点已在白名单 → True；否则 stderr 输出 AUTH-BLOCK +
    统一确认文案（由 agent 呈现给用户），返回 False（调用方转结构化错误，不阻断流程）。

    §5 统一文案（中文，按技能名/端点/发送内容适配；禁止出现内部术语）。
    """
    approved = _load_config().get("auto_approve_endpoints", [])
    if endpoint in approved:
        return True
    sys.stderr.write(
        "\nAUTH-BLOCK: outbound not approved yet\n"
        "⚠️ [meta-analysis] 需要把您的分析数据发送到外部服务器进行计算：\n"
        f"目标服务器：{endpoint}\n"
        "发送内容：您的分析数据（研究事件数 / 样本量 / 效应量等，不含任何个人身份信息）\n"
        "⚠️ 重要提示：本技能所有统计计算（meta / metafor / netmeta 等 R 引擎）"
        "均依赖云端 coze 执行。如不同意发送，将无法完成分析。\n"
        "是否允许本次发送？确认后本会话内不再重复询问。\n"
    )
    return False


def sanitize_payload(payload: dict) -> dict:
    """出站 payload 发送前脱敏（ct-base §5）：剥离 PII（身份证 / 手机号 / 邮箱）。

    meta-analysis 数据通常是研究级汇总（事件数/样本量），但兜底清理任何可能混入的
    个人标识字段值（递归遍历字符串值）。绝不回显 token / payload 明文。
    """
    id_card = re.compile(r"\b\d{17}[\dXx]\b")
    phone = re.compile(r"\b1[3-9]\d{9}\b")
    email = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b")

    def _clean(v):
        if isinstance(v, str):
            v = id_card.sub("[ID-CARD]", v)
            v = phone.sub("[PHONE]", v)
            v = email.sub("[EMAIL]", v)
            return v
        if isinstance(v, dict):
            return {k: _clean(x) for k, x in v.items()}
        if isinstance(v, list):
            return [_clean(x) for x in v]
        return v

    return _clean(payload)


def _fill_external_svgs(parsed: dict, timeout: int = 30) -> dict:
    """coze 返回体重组**兜底**入口（2026-08-28 manifest 方案重构，2026-08-29 起降级为 fallback）。

    主路径已迁移到 §20.8 模式 B：本地 `run_meta` 优先经 `_coze_full` 下载完整 JSON；
    仅当响应**无** `_coze_full`（老 coze 响应）时才调用本函数。

    若响应含 `_coze_manifest`（老 manifest 方案 coze 响应）：GET manifest → 逐 path 写回原值 →
    重组为原始 JSON（含 svg/r 代码/统计值）。

    **旧契约**：无 `_coze_manifest` 时走 figures[].url→svg、repro.url→r、`_coze_externalized` 逐块回填。

    - 超时 / 网络失败 → 保留引用并标记 _*_fetch_failed，绝不抛错中断分析。
    """
    if not isinstance(parsed, dict):
        return parsed
    # 新契约：manifest 单文件重组（优先级最高）
    manifest = parsed.get("_coze_manifest")
    if isinstance(manifest, dict) and manifest.get("storage") == "s3" and manifest.get("url"):
        return _reassemble_from_manifest(parsed, manifest, timeout=timeout)
    # 旧契约（向后兼容）：figures[].url / repro.url / _coze_externalized 逐项回填
    return _fill_external_svgs_legacy(parsed, timeout=timeout)


def _fetch_full_json(parsed, timeout=30):
    """优先经 `_coze_full` 下载完整 JSON（2026-08-29 §20.8 模式 B 落点）。

    coze 端把完整信封（含 figures/repro）整体写为单个 S3 文件并内联 `_coze_full` 链接；
    本地收到内联删减版后，**优先**下载完整 JSON 作分析源（零删减、含 figures/repro）。
    下载失败 / 无 `_coze_full` 链接 → 返回 None（调用方降级到 `_fill_external_svgs` 旧契约：
    manifest 重组 + 旧 figures[].url / repro.url 回填），保持对老 coze 响应向后兼容。
    """
    if not isinstance(parsed, dict):
        return None
    full = parsed.get("_coze_full")
    if not (isinstance(full, dict) and full.get("storage") == "s3" and full.get("url")):
        return None
    try:
        with urllib.request.urlopen(full["url"], timeout=timeout) as r:
            data = json.loads(r.read().decode("utf-8"))
    except Exception:  # noqa: BLE001
        parsed["_full_fetch_failed"] = True
        return None
    if not isinstance(data, dict):
        parsed["_full_fetch_failed"] = True
        return None
    # 完整数据本身不带 _coze_full（那是内联信封的链接），移除以防下游误用。
    data.pop("_coze_full", None)
    return data


def _reassemble_from_manifest(parsed: dict, manifest: dict, timeout: int = 30) -> dict:
    """按 manifest 重组原始 JSON（2026-08-28，用户提案）：
    coze 端把超 4000 的最大块（figures/repro/stats 子块）统一移进单个 S3 manifest 文件，
    manifest 为 [{path, value}, ...]，主返回体挂 `_coze_manifest = {storage:"s3", url}`。
    此处 GET manifest → 按 path 写回 value → 重组为原始 JSON。

    - path 支持 `figures[i]`（列表下标）与 `stats.xxx` 点路径。
    - 写回时若该位置当前仍是 {storage:"s3",type:"block"} 引用（未被本地改动）才覆盖。
    - 超时 / 网络失败 → 保留 manifest 引用并在主返回体标 _manifest_failed，绝不抛错中断。
    - 重组完成后移除 `_coze_manifest`（下游见到的即原始结构）。
    """
    url = manifest.get("url")
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            manifest_list = json.loads(r.read().decode("utf-8"))
    except Exception:  # noqa: BLE001
        parsed["_manifest_failed"] = True
        return parsed
    if not isinstance(manifest_list, list):
        parsed["_manifest_failed"] = True
        return parsed

    def _resolve_target(root, path):
        """返回 (容器, key) 或 (list, idx) 以便写回；找不到返回 None。"""
        if path.startswith("figures["):
            # figures[i]
            m = path[8:-1]
            if not m.isdigit():
                return None
            idx = int(m)
            figs = root.get("figures")
            if not isinstance(figs, list) or idx >= len(figs):
                return None
            return figs, idx
        # stats.a.b 点路径
        parts = path.split(".")
        node = root
        for p in parts[:-1]:
            if not isinstance(node, dict) or p not in node:
                return None
            node = node[p]
        if not isinstance(node, dict) or parts[-1] not in node:
            return None
        return node, parts[-1]

    for entry in manifest_list:
        if not isinstance(entry, dict):
            continue
        p = entry.get("path")
        if not p:
            continue
        target = _resolve_target(parsed, p)
        if target is None:
            continue
        container, key = target
        cur = container[key]
        # 仅当仍是外置引用时才写回；已被本地改动为实际内容则跳过
        if isinstance(container, dict):
            is_ref = (isinstance(cur, dict) and cur.get("storage") == "s3"
                      and cur.get("type") == "block")
            if is_ref:
                container[key] = entry.get("value")
        else:  # list
            if isinstance(cur, dict) and cur.get("storage") == "s3" and cur.get("type") == "block":
                container[key] = entry.get("value")
    # 重组完成，移除 manifest 引用（下游见原始结构）
    parsed.pop("_coze_manifest", None)
    return parsed


def _fill_external_svgs_legacy(parsed: dict, timeout: int = 30) -> dict:
    """旧契约（2026-08-28 起仅向后兼容）：figures[].url→svg、repro.url→r、_coze_externalized 逐块回填。"""
    if not isinstance(parsed, dict):
        return parsed
    figs = parsed.get("figures")
    if isinstance(figs, list):
        for fig in figs:
            if not isinstance(fig, dict):
                continue
            if fig.get("url") and not fig.get("svg"):
                try:
                    with urllib.request.urlopen(fig["url"], timeout=timeout) as r:
                        fig["svg"] = r.read().decode("utf-8")
                except Exception:  # noqa: BLE001
                    fig["_svg_fetch_failed"] = True
    repro = parsed.get("repro")
    if isinstance(repro, dict) and repro.get("url") and not repro.get("r"):
        try:
            with urllib.request.urlopen(repro["url"], timeout=timeout) as r:
                repro["r"] = r.read().decode("utf-8")
        except Exception:  # noqa: BLE001
            repro["_repro_fetch_failed"] = True
    # 旧契约的 stats 逐块回填
    refs = parsed.get("_coze_externalized")
    if isinstance(refs, list):
        _inflate_externalized(parsed, refs, timeout=timeout)
    return parsed


def _inflate_externalized(parsed: dict, refs: list | None = None, timeout: int = 30) -> dict:
    """（旧契约，2026-08-28 起仅向后兼容）回填 _coze_externalized 逐块外置的引用。"""
    if not isinstance(parsed, dict):
        return parsed
    if refs is None:
        refs = parsed.get("_coze_externalized")
    if not isinstance(refs, list):
        return parsed

    def _get_ref_node(node, parts):
        cur = node
        for p in parts[:-1]:
            if not isinstance(cur, dict) or p not in cur:
                return None
            cur = cur[p]
        if not isinstance(cur, dict) or parts[-1] not in cur:
            return None
        return cur, parts[-1]

    for ref in refs:
        path = ref.get("path")
        url = ref.get("url")
        if not path or not url:
            continue
        loc = _get_ref_node(parsed, path.split("."))
        if loc is None:
            continue
        node, key = loc
        cur_val = node.get(key)
        if not (isinstance(cur_val, dict) and cur_val.get("storage") == "s3"
                and cur_val.get("type") == "block"):
            continue
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                raw = r.read().decode("utf-8")
            val = json.loads(raw)
            node[key] = val
        except Exception:  # noqa: BLE001
            if not isinstance(cur_val, dict):
                cur_val = {"storage": "s3", "type": "block", "url": url}
            cur_val["_inflate_failed"] = True
            node[key] = cur_val
    return parsed


def _post_run_with_fallback(run_url: str, body: bytes, headers: dict, timeout: int):
    """POST /run（主端点），token 鉴权失败（401/403 + token 关键字）回退 FALLBACK_ENDPOINT
    （回退端点使用自身 token）。返回 (raw_text, elapsed_seconds, used_fallback, final_run_url)。

    供 run_meta 与 run_stage 共用，避免两端各写一份回退逻辑（消除重复）。
    """
    try:
        _acquire_rate_limit()
        raw, elapsed = _post_run(run_url, body, headers, timeout)
        return raw, elapsed, False, run_url
    except _CozeHttpError as e:
        ep = _endpoint()
        # 开发期 FALLBACK_ENDPOINT 可能置空（禁用 ct-meta）→ 不回退；
        # 仅当配置了回退端点且当前端点非回退端点时才重试。
        if FALLBACK_ENDPOINT and _is_token_error(e.code, e.body) and ep != FALLBACK_ENDPOINT:
            fb_url = FALLBACK_ENDPOINT if FALLBACK_ENDPOINT.endswith("/run") else FALLBACK_ENDPOINT + "/run"
            fb_headers = _headers(fb_url)
            if not _auth_gate(fb_url):
                raise AuthRequiredError(
                    f"coze 回退端点未授权（{fb_url} 不在 auto_approve_endpoints 白名单）。"
                )
            try:
                _acquire_rate_limit()
                raw, elapsed = _post_run(fb_url, body, fb_headers, timeout)
                return raw, elapsed, True, fb_url
            except _CozeHttpError as e2:
                raise RuntimeError(
                    f"coze 主端点与回退端点均因 token 不一致失败（{e2.code}）。"
                    f"{ENDPOINT_FALLBACK_NOTICE}"
                )
        raise
    except RuntimeError:
        raise


def run_meta(task: str, data: dict, params: dict | None = None,
             figure: dict | None = None, query_origin: str | None = None,
             entry_point: str | None = None,
             debug: bool = False, user_language: str | None = None,
             timeout: int | None = None) -> dict:
    """调用 coze 元分析工作流，返回解析后的结果 dict。

    Args:
        task:   任务类型（pairwise_meta / nma / metareg / ... 见 coze_contract.md）
        data:   分析数据（{"rows": [...], "colmap": {...}}）
        params: 分析参数（sm / model / subgroup / reference_group ...）
        figure: 出图控制（{"plots": [...], "width": 7, "height": 5}）
        query_origin: 调用发起来源标识（sha256:<64hex>，透传写入飞书 query_origin 列，
                      取值方式与 ct-registry 参考项目一致，2026-08-19）。
                      **留空时由本函数自动生成**（主机名 SHA-256，2026-08-29 修复：
                      空归因会让调用绕过按 query_origin 计的限流，且飞书日志无法溯源）。
        debug:   调试/冒烟标记（默认 False）。True 时 payload 附 `_debug: true`，
                  归因标识加 "debug:" 前缀，便于在飞书日志里把非生产流量筛出来。

    Returns:
        dict: {status, stats, figures:[{type,format,svg}], warnings, notes, task}
        另附观测字段：
          `_request_id`                本次请求 UUID（每次调用都不同）
          `_dedup_hit` / `_dedup_original_request_id`
                                       命中短窗去重时出现（结果复用自哪次请求）

    Raises:
        RuntimeError: coze 端点不可用或返回非 2xx。
    """
    # 2026-08-20 设计收紧（用户确认）：coze 端**永远只返回 SVG**——
    # 无论调用方是否请求 png，都强制 format="svg"；PNG 需求一律由本地呈现层
    # rendering.svg_to_png() / run_analysis.render_figures(mode="png_file") 转换
    # （coze 端零 png 路径，避免 png_base64 占用带宽/上下文）。
    fig = dict(figure or {})
    fig["format"] = "svg"
    # 兼容性兜底（2026-08-26 契约实测）：历史 spec 可能用 `byvar` 字段名，
    # coze 端点只认 `subgroup`（`byvar`/`group`/`by` 静默失效）；此处归一化，避免静默失效。
    if params and "byvar" in params:
        params = {**params, "subgroup": params.pop("byvar")}
    # 归因标识（2026-08-29）：未显式传入时自动生成 —— 任何调用路径都不再产生空归因。
    origin = query_origin or _default_query_origin(debug=debug)
    entry_point = entry_point or _ENTRY_POINT  # 入口标识：skill/workbench（2026-10-07）
    # 请求追踪 ID（2026-08-29）：飞书两条相邻记录无法区分"两次独立调用"还是
    # "一次调用的重放"，现每次调用带 UUID，随结果一并返回，便于事后对账。
    request_id = str(uuid.uuid4())
    payload = {
        "task": task,
        "data": data or {},
        # ct-base §1.1：user_language 仅承载于 params（顶层不双写）
        "params": _with_user_language(params, user_language),
        "figure": fig,
        "query_origin": origin,
        "entry_point": entry_point,  # 调用入口标识（2026-10-07）：skill/workbench
        "request_id": request_id,
        # ct-base §1.2：skill_version 为**顶层**信封字段，不得嵌套进 params
        "skill_version": _skill_version(),
    }
    if debug:
        payload["_debug"] = True
    # 2026-09-13：POST 前按 coze 契约校验出站信封；修复成功则替换为修复后的信封，
    # 致命不合规则抛 EnvelopeValidationError（绝不把装错的信封发到云端）。
    payload = _validate_outbound(payload)
    # 短窗幂等去重（2026-08-29）：窗口内完全相同的请求直接复用上次结果，
    # 不再打 coze —— 避免误双击 / 调试连跑把算力与飞书日志翻倍。
    fp = _dedup_fingerprint(payload)
    cached = _dedup_lookup(fp)
    if cached is not None:
        original_rid = cached.get("_request_id", "")
        cached["_dedup_hit"] = True
        cached["_dedup_original_request_id"] = original_rid
        cached["_request_id"] = request_id
        return cached
    # 2026-08-19 修复：DEFAULT_ENDPOINT/COZE_META_ENDPOINT 可能已带 /run 后缀
    # （旧逻辑无条件再拼 /run → 请求打到 /run/run → 404 Not Found）
    ep = _endpoint()
    run_url = ep if ep.endswith("/run") else ep + "/run"
    # ct-base §5 授权门控：首次出站须用户确认（未授权 → AuthRequiredError → 结构化错误）
    if not _auth_gate(run_url):
        raise AuthRequiredError(
            f"coze 出站未授权（端点 {run_url} 不在 auto_approve_endpoints 白名单）。"
            f"如同意发送请让用户确认后调用 approve_endpoint('{run_url}') 再重试。"
        )
    # ct-base §5：出站 payload 发送前脱敏（剥离 PII）
    payload = sanitize_payload(payload)
    # 调用方约束（2026-08-30）：序列化出站前硬校验 query_origin 非空且格式合法，
    # 覆盖主端点与回退端点（body 只构造一次、两次 POST 复用）——杜绝空归因出站。
    _assert_query_origin(payload)
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = _headers(ep)
    used_fallback = False

    # 主端点请求；token 不一致（401/403 + token 关键字）则回退 FALLBACK_ENDPOINT
    # （**回退端点使用自身专属 token**，见 _headers(fb_url)）
    raw, _elapsed, used_fallback, run_url = _post_run_with_fallback(
        run_url, body, headers, timeout if timeout is not None else _timeout())

    outer = json.loads(raw)
    # /run 返回 GlobalState（GraphOutput.result = R 引擎 JSON 字符串）
    result_str = outer.get("result") if isinstance(outer, dict) else None
    if not result_str:
        # 兼容直接返回结构化结果的情况
        fallback = outer if isinstance(outer, dict) else {"status": "error", "notes": "空响应"}
        fallback.setdefault("_request_id", request_id)
        return fallback
    try:
        parsed = json.loads(result_str)
    except json.JSONDecodeError:
        return {"status": "error",
                "notes": f"coze 返回非 JSON 结果：{result_str[:500]}",
                "_request_id": request_id}
    # 2026-08-29 §20.8 模式 B：优先经 `_coze_full` 下载完整 JSON（含 figures/repro，零删减）
    # 作分析源；下载失败 / 无链接降级旧契约（_fill_external_svgs：manifest 重组 +
    # 旧 figures[].url / repro.url 回填），保持对老 coze 响应向后兼容。
    full = _fetch_full_json(parsed, timeout=30)
    if full is not None:
        parsed = full
    else:
        _fill_external_svgs(parsed)
    # 契约漂移检测 + 自适应（coze 响应结构与本地技能"对不上"时，自动归一化；
    # 用户可见提示统一只在 rendering.py 的 HTML 横幅，此处不写 stderr / 不污染 notes）
    if isinstance(parsed, dict):
        parsed, _drift_notes, _needs_upgrade = _assess_contract(parsed)
        if _drift_notes:
            parsed["_contract_drift"] = _drift_notes
            parsed["_needs_upgrade"] = _needs_upgrade
    # 透出飞书写入状态（coze 端 GraphOutput 顶层字段，2026-08-19）
    if isinstance(parsed, dict):
        for _k in ("feishu_write_success", "feishu_write_time"):
            if _k in outer:
                parsed[_k] = outer[_k]
        # 仅诊断参考：coze 请求→响应往返秒数（R 计算 + 网络；非界面渲染时间）
        parsed["coze_elapsed_seconds"] = round(_elapsed, 1)
        # 端点回退提示：原地址因 token 不一致触发回退，提示用户技能已升级、地址有变。
        # 用户可见提示统一只在 rendering.py 的 HTML 横幅（由 _coze_endpoint_notice 驱动），
        # 此处不写 stderr / 不污染 notes。
        if used_fallback:
            parsed["_coze_endpoint_notice"] = ENDPOINT_FALLBACK_NOTICE
        parsed["_request_id"] = request_id
    # 仅成功结果入去重缓存（失败不缓存，避免偶发失败毒化窗口内后续真实重试）
    _dedup_store(fp, parsed)
    return parsed


def health() -> bool:
    """探测 coze 端点**可达性**（非功能健康）。

    2026-08-19 修正：coze 自定义域名通常仅暴露 /run，/health 路由未必存在——旧实现
    探测 /health 在服务正常时也可能误报 False。现改为探测 /run：
    - 2xx / 4xx / 5xx（含 401 缺 token、405 方法不允许）均证明服务已响应 → 可达 True；
    - 仅网络层错误 / 超时 / DNS 失败 → False（真正不可达）。
    """
    ep = _endpoint().rsplit("/run", 1)[0] or DEFAULT_ENDPOINT.rsplit("/run", 1)[0]
    # 2026-08-29：探测包带 `probe` 标记 + 调试归因，不再发空信封 `{}`。
    #   - 新 coze 端（已部署）：识别 probe → 跳过 R 计算与飞书写入，日志表零污染；
    #   - 旧 coze 端（未部署）：不认识该字段（pydantic extra='ignore'）→ 仍会写一条，
    #     但至少带 `debug:` 归因前缀可筛出，不再是空白归因。
    # 2026-08-29（补）：带上 Bearer token，使 probe 能越过网关鉴权真正进 langgraph。
    #   不带 token 时请求被网关在鉴权层挡回（401），根本进不了图，probe 短路是"睡着"的；
    #   带 token 后 coze 端会在 meta_analysis 节点直接短路、不调 R 引擎、不写飞书，
    #   既验证可达性，又零算力零日志污染。token 解析失败时退化为无 token 探测（401 仍算可达）。
    try:
        probe_body = json.dumps(
            {"probe": True, "query_origin": _default_query_origin(debug=True)},
            ensure_ascii=False,
        ).encode("utf-8")
    except Exception:  # noqa: BLE001 — 极端情况下退化为最简探测包，探测本身不应失败
        probe_body = b'{"probe": true}'
    headers = {"Content-Type": "application/json"}
    try:
        tok = _resolve_token(ep)
        if tok:
            headers["Authorization"] = "Bearer " + tok
    except Exception:  # noqa: BLE001 — token 解析失败不应阻断探测
        pass
    try:
        req = urllib.request.Request(
            ep + "/run", method="POST", data=probe_body, headers=headers,
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            return True  # 2xx
    except urllib.error.HTTPError:
        return True  # 4xx/5xx：服务已响应（401/404/405 均说明可达）
    except Exception:
        return False  # 网络层/超时：不可达


# ============================================================================
# Phase 0 — per-stage Pipeline 客户端（本地薄客户端骨架）
# 设计（对齐 contracts/pipeline_stage/v1.0.0/SPEC.md + coze_contract.md §9）：
#   - run_stage()        发送 per-stage 信封；旧 per-task 信封 → 委派 run_meta（R1 双模）。
#   - parse_stage_response()  解析 stage_result/next_human_action/tool_cards（coze 端以
#                         JSON 字符串承载，与 result 同模式）+ 兼容旧 result 内层。
#   - execute_tool_cards()  复用 need_tool 范式：request_upload → 本地上传；ct-* → 查表执行。
#   - run_pipeline()     薄客户端编排（发→解析→执行 tool_card→回填 stage_context→续跑），
#                         红线 gate 强执（gate≠none & required → 阻断自动续跑，交人工）。
#   - _upload_file()/download_attachments()  文件双向传输（S3 预签名）。
#   - billing 仅透传（account_id/billing_token 可选，预留接口）。
# 所有网络动作可经 transport 注入（测试用），不依赖真实 coze 部署。
# ============================================================================

CONTRACT_VERSION = "1.0.0"
STAGE_SCHEMA_ID = "meta.pipeline.stage/v1"
_STAGE_FIELDS = ("contract_version", "schema", "pipeline_id", "pipeline", "stage")
# 🔴 红线闸集合：命中且 required=True 时，run_pipeline 阻断自动续跑（SPEC §8 / coze_contract §9.2）。
_REDLINE_GATES = {"extraction_review", "final_inclusion", "manuscript_approval", "reference_verification"}

_UPLOAD_PUT_TIMEOUT = 120
_DOWNLOAD_TIMEOUT = 120


def _http_put(url: str, data: bytes, headers: dict | None = None, timeout: int = _UPLOAD_PUT_TIMEOUT) -> int:
    """PUT 上传（S3 预签名），返回 HTTP 状态码。测试可 monkeypatch 本函数。"""
    req = urllib.request.Request(url, data=data, method="PUT", headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status


def _http_get(url: str, timeout: int = _DOWNLOAD_TIMEOUT) -> bytes:
    """GET 下载，返回字节。测试可 monkeypatch 本函数。"""
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.read()


def _is_legacy_envelope(env: dict) -> bool:
    """双模判定：无管线字段即 legacy（对齐 BACKWARD_COMPAT.md / coze_contract §9.5 R1）。"""
    return not any(k in env for k in _STAGE_FIELDS)


def build_stage_payload(env: dict, debug: bool = False,
                        user_language: str | None = None) -> dict:
    """规范化 stage 信封：补齐 contract_version/schema/request_id/query_origin
    + skill_version（顶层）/ user_language（params 内，ct-base §1.1/§1.2）；
    coze 恒只返 SVG（2026-08-20 收紧）；byvar→subgroup 归一化。"""
    env = dict(env)
    fig = dict(env.get("figure") or {})
    fig["format"] = "svg"
    env["figure"] = fig
    if env.get("params") and "byvar" in env["params"]:
        env["params"] = {**env["params"], "subgroup": env["params"].pop("byvar")}
    if "contract_version" not in env:
        env["contract_version"] = CONTRACT_VERSION
    if "schema" not in env:
        env["schema"] = STAGE_SCHEMA_ID
    if "request_id" not in env:
        env["request_id"] = str(uuid.uuid4())
    env["query_origin"] = env.get("query_origin") or _default_query_origin(debug=debug)
    # 入口标识（2026-10-07）：skill/workbench，透传飞书 entry_point 列
    env["entry_point"] = env.get("entry_point") or _ENTRY_POINT
    # ct-base §1.1/§1.2：语言仅落 params、版本仅落顶层；调用方已给有效值则不覆盖。
    env["params"] = _with_user_language(env.get("params"), user_language)
    if not env.get("skill_version"):
        env["skill_version"] = _skill_version()
    if debug:
        env["_debug"] = True
    return env


def attach_billing(env: dict, account_id: str | None = None,
                   billing_token: str | None = None) -> dict:
    """billing 标识仅透传（预留接口，向后兼容）：account_id/billing_token 二选一，
    与 query_origin（匿名机器指纹）完全独立。缺失 → legacy/未计量路径。"""
    if account_id:
        env["account_id"] = account_id
    if billing_token:
        env["billing_token"] = billing_token
    return env


def run_stage(env: dict, debug: bool = False, transport=None,
              user_language: str | None = None) -> dict:
    """发送 per-stage 信封并解析响应。

    - 旧 per-task 信封（无管线字段）→ 委派 run_meta（R1 双模在客户端层也成立）。
    - 新 stage 信封 → 经 transport（默认 _post_run_with_fallback）POST /run，
      parse_stage_response 解析。transport 签名同 _post_run：(url, body, headers, timeout)。
    """
    if _is_legacy_envelope(env):
        return run_meta(
            env.get("task"), env.get("data"), env.get("params"),
            env.get("figure"), query_origin=env.get("query_origin"),
            entry_point=env.get("entry_point"), debug=debug,
            user_language=user_language,
        )
    payload = build_stage_payload(env, debug=debug, user_language=user_language)
    # 2026-09-13：POST 前按 coze 契约校验出站信封（同 run_meta 主路径）。
    payload = _validate_outbound(payload)
    fp = _dedup_fingerprint(payload)
    cached = _dedup_lookup(fp)
    if cached is not None:
        cached["_dedup_hit"] = True
        return cached
    ep = _endpoint()
    run_url = ep if ep.endswith("/run") else ep + "/run"
    if not _auth_gate(run_url):
        raise AuthRequiredError(
            f"coze 出站未授权（端点 {run_url} 不在 auto_approve_endpoints 白名单）。"
            f"如同意发送请让用户确认后调用 approve_endpoint('{run_url}') 再重试。"
        )
    payload = sanitize_payload(payload)
    _assert_query_origin(payload)  # 出站硬守卫，杜绝空归因（2026-08-30）
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = _headers(ep)
    transport = transport or _post_run_with_fallback
    _tr = transport(run_url, body, headers, _timeout())
    # transport 可能返回 2 元组 (raw, elapsed) 或 4 元组 (raw, elapsed, used_fallback, final_url)：
    # 真实 HTTP transport (_post_run_with_fallback) 返回 4 元组；本地 local_transport 返回 2 元组。
    # 向后兼容两种形态（2026-08-31 修复：此前真实调用因 4 元组解包崩溃，被 local_transport 的 2 元组掩盖）。
    raw, elapsed = _tr[0], _tr[1]
    outer = json.loads(raw)
    parsed = parse_stage_response(outer, payload.get("request_id"), elapsed=elapsed)
    _dedup_store(fp, parsed)
    return parsed


def parse_stage_response(outer, request_id, elapsed: float = 0.0) -> dict:
    """解析 coze 返回的 stage 信封。

    coze 端 stage_result/next_human_action/tool_cards 以 JSON 字符串承载（与 result 同模式，
    见 coze_contract §9.1）。本函数统一解析为对象，并兼容旧 result 内层（Block B 计算，
    R2 仍填充 result）。红线闸信号由 run_pipeline 消费。
    """
    if not isinstance(outer, dict):
        return {"status": "error", "notes": "coze 返回非 JSON 对象",
                "_request_id": request_id, "_gate_blocked": False}
    out = {"_request_id": request_id, "coze_elapsed_seconds": round(elapsed, 1)}
    for _k in ("feishu_write_success", "feishu_write_time", "_coze_endpoint_notice"):
        if _k in outer:
            out[_k] = outer[_k]

    def _json_or_obj(v):
        if v is None:
            return None
        if isinstance(v, str):
            try:
                return json.loads(v)
            except Exception:  # noqa: BLE001
                return {"_raw": v}
        return v

    stage_present = any(k in outer for k in ("stage_result", "next_human_action", "tool_cards"))
    if stage_present:
        out["mode"] = "stage"
        out["stage_result"] = _json_or_obj(outer.get("stage_result"))
        out["next_human_action"] = _json_or_obj(outer.get("next_human_action"))
        out["tool_cards"] = _json_or_obj(outer.get("tool_cards")) or []
        out["stage"] = _json_or_obj(outer.get("stage"))
        out["pipeline_id"] = outer.get("pipeline_id")
    else:
        out["mode"] = "legacy"

    # 兼容：result 内层（Block B 计算阶段，R2 仍填充 result）
    result_str = outer.get("result")
    if isinstance(result_str, str) and result_str:
        try:
            inner = json.loads(result_str)
        except json.JSONDecodeError:
            inner = {"status": "error", "notes": f"coze 返回非 JSON 结果：{result_str[:500]}"}
        full = _fetch_full_json(inner, timeout=30) if isinstance(inner, dict) else None
        if full is not None:
            inner = full
        else:
            _fill_external_svgs(inner)
        if isinstance(inner, dict):
            inner, _drift, _up = _assess_contract(inner)
            if _drift:
                inner["_contract_drift"] = _drift
                inner["_needs_upgrade"] = _up
        out["result"] = inner
        for _f in ("status", "stats", "figures", "warnings", "notes", "task", "repro"):
            if isinstance(inner, dict) and _f in inner:
                out[_f] = inner[_f]
    elif not stage_present:
        # 既无 stage 字段也无 result → 直接把 outer 当结果（兼容直接返回结构化结果）
        for _f in ("status", "stats", "figures", "warnings", "notes", "task"):
            if _f in outer:
                out[_f] = outer[_f]

    # 响应侧 attachments（下载引用）
    atts = outer.get("attachments")
    if isinstance(atts, str):
        try:
            atts = json.loads(atts)
        except Exception:  # noqa: BLE001
            atts = None
    out["attachments"] = atts if isinstance(atts, list) else []

    # 红线闸强执信号：gate≠none & required → 阻断自动续跑
    nha = out.get("next_human_action")
    gate_blocked = bool(
        isinstance(nha, dict) and nha.get("gate") in _REDLINE_GATES and nha.get("required")
    )
    out["_gate_blocked"] = gate_blocked
    return out


def resolve_skill_dir(base: str) -> str:
    """解析技能安装目录，兼容 SkillHub 的 `__skillhub` 后缀命名。

    SkillHub 安装时可能把技能命名为 `ct-literature__skillhub` 而非 `ct-literature`，
    调用方不应硬编码任一名字。依次尝试原路径 → 追加 `__skillhub` 后缀，返回首个存在的目录；
    都不存在则返还原值（让上层报错信息更直观）。
    """
    base = os.path.expanduser(base)
    if os.path.isdir(base):
        return base
    alt = base + "__skillhub"
    if os.path.isdir(alt):
        return alt
    return base


# ---------------------------------------------------------------------------
# 解释器解析（修复 tool_mapping_meta.json 硬编码 python 路径导致的静默失效）
# ---------------------------------------------------------------------------
# 历史问题：映射表把 `C:/Anaconda3/python.exe` 写死在 cmd[0]，换机/换装后该路径不存在，
# subprocess 抛 FileNotFoundError → 被 execute_tool_cards 的 except 吞成 status:error
# → 上层读到空结果，界面表现为"检索 0 篇 / 注册库无返回"而**不报错**（A2 检索、
# A1 注册库查重均受影响）。故改为占位符 `{python}` 运行时解析，硬编码路径降级为
# "候选之一"。优先级：显式环境变量 → Anaconda base → 当前解释器 → PATH。
_PYTHON_PLACEHOLDER = "{python}"

_PYTHON_CANDIDATES = (
    r"C:/Tools/Anaconda3/python.exe",   # 本机 Anaconda base（实测位置）
    r"C:/Anaconda3/python.exe",         # 旧约定路径，保留兼容
    "/opt/anaconda3/bin/python",
    "/opt/homebrew/bin/python3",
    "/usr/local/bin/python3",
    "/usr/bin/python3",
)

_PYTHON_EXE_CACHE = None


def resolve_python_exe() -> str:
    """解析驱动 ct-* 子进程的 Python 解释器绝对路径（结果进程内缓存）。

    只接受**实际存在**的文件：配置里写的不等于存在的。全部候选落空时回退
    sys.executable，让 subprocess 如实报错，而不是被静默吞掉。
    """
    global _PYTHON_EXE_CACHE
    if _PYTHON_EXE_CACHE:
        return _PYTHON_EXE_CACHE

    for env_key in ("META_PYTHON", "WORKBUDDY_PYTHON"):
        cand = (os.environ.get(env_key) or "").strip()
        if cand and os.path.isfile(cand):
            _PYTHON_EXE_CACHE = cand
            return cand

    for cand in _PYTHON_CANDIDATES:
        if os.path.isfile(cand):
            _PYTHON_EXE_CACHE = cand
            return cand

    if sys.executable and os.path.isfile(sys.executable):
        _PYTHON_EXE_CACHE = sys.executable
        return sys.executable

    _PYTHON_EXE_CACHE = shutil.which("python") or shutil.which("python3") or "python"
    return _PYTHON_EXE_CACHE


def _load_tool_mapping() -> dict:
    """加载 tool_mapping_meta.json（Block A/C 需要的 ct-* 本地调用映射）。缺失返回空。

    skill_dir 中的 ~ 在此展开为绝对路径（subprocess 不会自动展开 ~）；
    若目录不存在，自动回退到 `__skillhub` 后缀的同名目录（SkillHub 安装兼容）。
    cmd 中的 `{python}` 占位符在此解析为真实解释器路径（见 resolve_python_exe）。
    """
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tool_mapping_meta.json")
    try:
        with open(p, encoding="utf-8") as f:
            data = json.load(f)
    except Exception:  # noqa: BLE001
        return {}
    py = None
    for spec in data.values():
        if not isinstance(spec, dict):
            continue
        if spec.get("skill_dir"):
            spec["skill_dir"] = resolve_skill_dir(spec["skill_dir"])
        cmd = spec.get("cmd")
        if isinstance(cmd, list) and any(
            isinstance(c, str) and _PYTHON_PLACEHOLDER in c for c in cmd
        ):
            if py is None:
                py = resolve_python_exe()
            spec["cmd"] = [
                c.replace(_PYTHON_PLACEHOLDER, py) if isinstance(c, str) else c
                for c in cmd
            ]
    return data


def _parse_tool_output(text):
    """解析 ct-* 子进程 stdout 为结构化结果。

    - 整段是合法 JSON（对象/数组）→ 直接返回；
    - 否则按行解析 NDJSON（ct-literature 逐行 print(json.dumps(rec))），收集所有 dict / 展开 list；
    - 无可解析记录 → 返回原始字符串（便于上层诊断）。
    """
    if not text:
        return ""
    text = text.strip()
    try:
        return json.loads(text)
    except Exception:  # noqa: BLE001
        pass
    records = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except Exception:  # noqa: BLE001
            continue
        if isinstance(obj, dict):
            records.append(obj)
        elif isinstance(obj, list):
            records.extend(obj)
    return records if records else text


def _upload_file(local_path, purpose: str | None = None, storage: str = "s3") -> dict:
    """构建本地文件的 AttachmentRef（key/filename/mime/size_bytes/sha256/purpose）。
    实际 PUT 到 S3 预签名 URL 由 execute_tool_cards 在拿到 put_url 后完成。

    测试可 monkeypatch coze_client._http_put 避免真实网络。
    """
    p = os.path.abspath(local_path)
    if not os.path.isfile(p):
        raise FileNotFoundError(p)
    with open(p, "rb") as f:
        data = f.read()
    sha = hashlib.sha256(data).hexdigest()
    size = len(data)
    mime = mimetypes.guess_type(p)[0] or "application/octet-stream"
    ref = {"storage": storage, "key": f"pipeline/uploads/{sha}_{os.path.basename(p)}",
           "filename": os.path.basename(p), "mime": mime, "size_bytes": size, "sha256": sha}
    if purpose:
        ref["purpose"] = purpose
    return ref


def download_attachments(attachments, out_dir) -> list:
    """下载响应侧 attachments（含预签名 GET url），校验 sha256，落盘 out_dir。
    返回 list[dict]{filename,path,ok,sha256_ok}。失败不抛错，标 ok=False。

    测试可 monkeypatch coze_client._http_get 避免真实网络。
    """
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    results = []
    for att in (attachments or []):
        if not isinstance(att, dict) or not att.get("url"):
            results.append({"ok": False, "reason": "missing url", "ref": att})
            continue
        try:
            raw = _http_get(att["url"])
            sha_ok = True
            if att.get("sha256"):
                sha_ok = hashlib.sha256(raw).hexdigest() == att["sha256"]
            fname = att.get("filename") or os.path.basename(att.get("key") or "download")
            path = os.path.join(out_dir, fname)
            with open(path, "wb") as f:
                f.write(raw)
            results.append({"filename": fname, "path": path, "ok": True, "sha256_ok": sha_ok})
        except Exception as e:  # noqa: BLE001
            results.append({"ok": False, "reason": str(e)[:200], "ref": att})
    return results


def execute_tool_cards(cards, out_dir: str = ".", cwd: str | None = None,
                       on_line=None) -> list:
    """执行 coze 下发的 tool_cards（复用 need_tool 范式）。

    - need_tool == "request_upload" → 本地逐个上传 params["_local_files"] 所列文件
      （每项 {path, purpose} 或纯路径），put_url 由 params["_put_urls"]{path: url} 提供；
      返回 AttachmentRef[]。
    - 其他（ct-* 等）→ 查 tool_mapping_meta.json 构造 CLI 执行（草稿兜底）。
    返回 list[{card_ref, need_tool, status, result}]，绝不抛错中断管线。

    on_line: 可选的实时输出回调 f(line: str)，供上层（工作台底部信息栏）展示后台进度。
      - **不传（默认）**：走原 `subprocess.run(capture_output=True)` 一次性捕获，行为完全不变。
      - **传入**：改走 `Popen` 逐行流式读 stdout+stderr，每行即时回调，同时收集完整
        输出供 `_parse_tool_output` 正常解析（结果一致性不受影响）。
      回调自身抛错被吞掉，绝不影响主流程。
    """
    out_dir = os.path.abspath(out_dir)
    mapping = _load_tool_mapping()
    outputs = []
    for card in (cards or []):
        if not isinstance(card, dict):
            continue
        need = card.get("need_tool")
        cref = card.get("card_ref")
        params = card.get("params") or {}
        draft = card.get("draft_answer")
        try:
            if need == "request_upload":
                local_files = params.get("_local_files") or []
                put_urls = params.get("_put_urls") or {}
                refs = []
                for item in local_files:
                    lp = item if isinstance(item, str) else item.get("path")
                    purp = None if isinstance(item, str) else item.get("purpose")
                    if not lp:
                        continue
                    ref = _upload_file(lp, purpose=purp)
                    url = put_urls.get(lp) or put_urls.get(os.path.basename(lp))
                    if url:
                        with open(os.path.abspath(lp), "rb") as f:
                            _http_put(url, f.read(), headers={"Content-Type": ref["mime"]})
                        ref["put_url"] = url
                    refs.append(ref)
                outputs.append({"card_ref": cref, "need_tool": need,
                                "status": "ok", "result": {"attachments": refs}})
            else:
                spec = mapping.get(need)
                if not spec or not spec.get("cmd"):
                    outputs.append({"card_ref": cref, "need_tool": need, "status": "error",
                                    "result": {"error": f"未找到工具映射: {need}", "draft_answer": draft}})
                    continue
                cmd = [c.format(skill_dir=spec.get("skill_dir", "")) if isinstance(c, str) and "{skill_dir}" in c else c
                       for c in spec["cmd"]]
                for pname, flag in (spec.get("arg_map") or {}).items():
                    if pname in params:
                        val = params[pname]
                        # Boolean-style flags (BooleanOptionalAction: --flag / --no-flag).
                        # Convention: flag name "include-X" maps to --include-X / --no-include-X.
                        # Since fetcher default is True, only append --no-* when explicitly False.
                        if isinstance(val, bool) and ("include" in pname or "exclude" in pname):
                            if not val:
                                # Append the negative variant: --include-X → --no-include-X
                                cmd.append("--no-" + flag.lstrip("-"))
                            # True = default → no flag needed
                        else:
                            cmd += [flag, str(val)]
                for f in (spec.get("fixed_flags") or []):
                    cmd.append(f)
                timeout_s = card.get("timeout_sec", 120)
                if on_line is not None:
                    # 流式路径：逐行读 stdout（stderr 合并）→ 实时回调，同时收集完整输出。
                    # 显式 utf-8 + errors=replace：后台进度行含 emoji/中文，避免 Windows
                    # 默认编码（cp936）解码失败打断检索。
                    # CREATE_NO_WINDOW：阻止 Windows 为子进程弹出控制台窗口（提交时不要黑框）。
                    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                            stderr=subprocess.STDOUT, text=True,
                                            bufsize=1, encoding="utf-8",
                                            errors="replace", cwd=cwd,
                                            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
                    chunks = []
                    for line in proc.stdout:
                        chunks.append(line)
                        try:
                            on_line(line.rstrip())
                        except Exception:  # noqa: BLE001 — 展示层回调失败不阻断检索
                            pass
                    proc.stdout.close()
                    proc.wait(timeout=timeout_s)
                    stdout_text, stderr_text, rc = "".join(chunks), "", proc.returncode
                else:
                    # 原路径（默认）：一次性捕获，行为与改动前完全一致。
                    proc = subprocess.run(cmd, capture_output=True, text=True,
                                          timeout=timeout_s, cwd=cwd,
                                          creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
                    stdout_text, stderr_text, rc = proc.stdout, proc.stderr, proc.returncode
                if rc != 0:
                    outputs.append({"card_ref": cref, "need_tool": need, "status": "error",
                                    "result": {"stderr": (stderr_text or "")[:500],
                                               "draft_answer": draft}})
                    continue
                res = _parse_tool_output(stdout_text)
                outputs.append({"card_ref": cref, "need_tool": need, "status": "ok", "result": res})
        except Exception as e:  # noqa: BLE001
            outputs.append({"card_ref": cref, "need_tool": need, "status": "error",
                            "result": {"exception": f"{type(e).__name__}: {e}", "draft_answer": draft}})
    return outputs


def run_stage_local(env: dict, debug: bool = False, transport=None) -> dict:
    """本地 R 引擎镜像（coze 代码同源，不经 coze 云）。

    供冻结期离线真实计算 / 测试：把 stage 信封翻译为 run_task.R 的 input，
    经本机 Rscript 调用 adapters/coze/src/r_engine/run_task.R，解析结果包成
    coze 风格响应（{stage_result:{result:{stats,...}}}），供 block_b._extract_coze_stats
    原样消费，下游 B2/B3/B4 零改动。非 coze 部署路径，仅本地开发/演示/回归使用。
    """
    import json as _json
    import os as _os
    import tempfile as _tf
    import shutil as _sh
    import subprocess as _sp

    task = env.get("task")
    data = env.get("data") or []
    params = env.get("params") or {}
    em = params.get("effect_measure") or "OR"
    rows = data if isinstance(data, list) else (data.get("rows") or [])
    inp = {
        "task": task,
        "data": {"rows": rows},
        "params": {"sm": em, "model": "random"},
        "figure": {"format": "svg", "plots": ["forest", "funnel"]},
    }
    rdir = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
                         "coze", "src", "r_engine")
    rscript = _os.environ.get("RSCRIPT_BIN", r"C:/Tools/R-4.6.1/bin/Rscript.exe")
    run_task = _os.path.join(rdir, "run_task.R")
    d = _tf.mkdtemp(prefix="meta_local_")
    ip = _os.path.join(d, "in.json")
    op = _os.path.join(d, "out.json")
    try:
        with open(ip, "w", encoding="utf-8") as f:
            _json.dump(inp, f, ensure_ascii=False)
        try:
            proc = _sp.run([rscript, run_task, "--input", ip, "--output", op],
                           capture_output=True, text=True, timeout=180,
                           creationflags=getattr(_sp, "CREATE_NO_WINDOW", 0))
        except Exception as e:  # noqa: BLE001
            return {"status": "error",
                    "notes": f"本地 R 引擎调用失败: {type(e).__name__}: {e}",
                    "_request_id": env.get("pipeline_id"), "_gate_blocked": False}
        if not _os.path.exists(op):
            return {"status": "error",
                    "notes": f"本地 R 引擎无输出: {proc.stderr[-1500:]}",
                    "_request_id": env.get("pipeline_id"), "_gate_blocked": False}
        out = _json.load(open(op, encoding="utf-8"))
        stats = out.get("stats")
        figures = out.get("figures", [])
        return {
            "stage_result": {
                "result": {
                    "stats": stats,
                    "figures": figures,
                    "task": task,
                    "notes": out.get("notes"),
                    "warnings": out.get("warnings", []),
                    # 复现 R 代码（供 HTML 报告折叠展示；run_task.R 顶层 repro 字段）
                    "repro": out.get("repro"),
                }
            },
            "_local_engine": True,
            "_coze_endpoint_notice": "本地 R 引擎镜像（coze 代码同源），未经 coze 云。",
        }
    finally:
        _sh.rmtree(d, ignore_errors=True)


def run_pipeline(initial_env: dict, max_stages: int = 20, debug: bool = False,
                 transport=None, out_dir: str = ".") -> dict:
    """薄客户端编排（I/O 入口）：发→解析→执行 tool_card→回填 stage_context→续跑；
    红线闸 gate≠none & required 阻断自动续跑，交人工。

    Returns:
        {done, await_human, gate, final, stages[], attachments[], tool_card_outputs[]}
    """
    env = dict(initial_env)
    env.setdefault("stage_context",
                   {"human_decisions": [], "tool_card_outputs": [], "artifacts": []})
    stages = []
    all_tool_outputs = []
    downloaded = []
    for _i in range(max_stages):
        resp = run_stage(env, debug=debug, transport=transport)
        stages.append(resp)
        if resp.get("attachments"):
            downloaded += download_attachments(resp["attachments"], out_dir)
        # 🔴 红线闸：阻断自动续跑，交人工
        if resp.get("_gate_blocked"):
            return {"done": False, "await_human": True,
                    "gate": (resp.get("next_human_action") or {}).get("gate"),
                    "final": resp, "stages": stages,
                    "attachments": downloaded, "tool_card_outputs": all_tool_outputs}
        # 执行 tool_cards 并回填 stage_context（不回发 coze，下请求携带）
        cards = resp.get("tool_cards") or []
        if cards:
            outs = execute_tool_cards(cards, out_dir=out_dir)
            all_tool_outputs += outs
            env["stage_context"]["tool_card_outputs"] += outs
            if isinstance(env.get("stage"), dict):
                env["stage"]["intent"] = "resume"
            continue
        # 无 tool_card 且非闸 → 据 next_human_action 决定
        nha = resp.get("next_human_action") or {}
        ntype = nha.get("type")
        if ntype == "none" and (resp.get("stage") or {}).get("status") == "completed":
            return {"done": True, "await_human": False, "gate": None, "final": resp,
                    "stages": stages, "attachments": downloaded,
                    "tool_card_outputs": all_tool_outputs}
        if ntype not in (None, "none"):
            return {"done": False, "await_human": True, "gate": nha.get("gate"), "final": resp,
                    "stages": stages, "attachments": downloaded,
                    "tool_card_outputs": all_tool_outputs}
        st = (resp.get("stage") or {}).get("status")
        if st in ("need_data", "failed"):
            return {"done": False, "await_human": True, "gate": nha.get("gate"), "final": resp,
                    "stages": stages, "attachments": downloaded,
                    "tool_card_outputs": all_tool_outputs}
    return {"done": False, "await_human": True, "gate": "max_stages_reached",
            "final": stages[-1] if stages else None, "stages": stages,
            "attachments": downloaded, "tool_card_outputs": all_tool_outputs}


if __name__ == "__main__":
    # 2026-08-29：删除原「硬编码 sample 调 run_meta」的自测入口。
    # 它是飞书 08-29 两条空归因 pairwise_meta 记录的来源 —— 注释还停留在
    # 「需要本地已启动 coze 服务」的年代，端点早已换成公网，于是**调试动作直接
    # 往生产日志表写记录**。且它与 case1_pairwise_binary 完全重复、无独立价值。
    # 现自测方式（都不再裸调 run_meta）：
    #   python adapters/coze_client.py --health    仅探测端点可达性，不发起分析请求
    #   python scripts/run_meta.py <request.json>  走生产路径冒烟（自动带归因 + 去重）
    if "--health" in sys.argv:
        print("coze endpoint reachable:", health())
    else:
        print("用法:\n"
              "  python adapters/coze_client.py --health     探测 coze 端点可达性\n"
              "  python scripts/run_meta.py <request.json>   走生产路径冒烟（推荐）")
