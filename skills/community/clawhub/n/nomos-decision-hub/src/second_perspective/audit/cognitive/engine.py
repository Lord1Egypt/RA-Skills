"""
第二视角认知审计引擎 (Cognitive Audit Engine)

设计定位：在「第二视角因果与剧情推演」框架下，对决策进行静态诊断与因果重构推演。
核心能力：
  1. 责任闭环锚定 —— 将审计绑定到具体的组织/角色/决策阶段，并附防重放 nonce。
  2. 静态诊断 —— 通过可插拔的分析插件，提取偏见、脆弱性等风险信号。
  3. 因果重构推演 —— 注入修正变量 (delta_vars) 重构逻辑链，并评估系统收敛至目标稳态。

本模块不含任何主观/概率化推测，仅做决定论因果处理。
"""

import os
import time
import uuid
import json
import copy
import hashlib
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, List, Callable, Optional, Protocol, Tuple

from ...version import VERSION
from .plugins.spiral import SpiralStack
from .plugins.meta import MetaCausalLedgerPlugin
from .plugins.topology import TOPOLOGY_VERSION


# ==================== LLM 协议与默认实现 ====================

class LLMProvider(Protocol):
    """大模型接口协议：实现此协议的任何类都可注入引擎。"""
    def generate(self, prompt: str, **kwargs) -> str: ...


class OpenAIProvider:
    """使用 urllib 调用 OpenAI 兼容接口的 LLM 实现（零外部依赖）。

    Args:
        api_key:   API 密钥。
        model:     模型名称，如 "gpt-4o"、"deepseek-chat"。
        base_url:  API 基础地址，默认 "https://api.openai.com/v1"。
        timeout:   请求超时（秒）。

    数据出境合规提示：
        - 默认 base_url 指向境外 "https://api.openai.com/v1"，调用即涉及数据出境。
        - 境内部署应传入境内端点（如 DeepSeek、通义千问），并对输入做脱敏处理。
        - 五算子因果审计本身不调用任何 LLM；仅「LLM 增强分析」可选启用时使用本类。
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o",
        base_url: str = "https://api.openai.com/v1",
        timeout: int = 120,
    ):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def generate(self, prompt: str, **kwargs) -> str:
        import urllib.request
        import urllib.error

        temperature = kwargs.get("temperature", 0.7)
        max_tokens = kwargs.get("max_tokens", 4096)

        body = json.dumps({
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                return result["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            return f"[LLM Error] HTTP {e.code}: {e.read().decode('utf-8', errors='replace')[:200]}"
        except Exception as e:
            return f"[LLM Error] {e}"


@dataclass
class ResponsibilityAccount:
    """责任节点数据类：用于把一次审计绑定到最小决策单元（具体责任节点）。

    Attributes:
        organization: 责任所属组织。
        role:        责任角色（如决策者 / 复核者）。
        stage:       决策阶段（须在 config 的 allowed_stages 内才合法）。
        nonce:       防重放随机串；未显式提供时自动生成，用于审计去重与追溯。
    """
    organization: str
    role: str
    stage: str
    nonce: Optional[str] = None

    def __post_init__(self) -> None:
        # 未提供 nonce 时自动生成 8 位十六进制随机串，保证审计记录唯一可追溯
        if not self.nonce:
            self.nonce = uuid.uuid4().hex[:8]


class AuditConfigLoader:
    """审计配置加载器：从字典或 JSON 文件载入审计运行参数（免责声明、允许阶段、自定义字段等）。"""
    @staticmethod
    def load_from_dict(config: Dict[str, Any]) -> Dict[str, Any]:
        # 配置已是字典时直接透传（保留扩展点：可在此做校验/默认值补全）
        return config

    @staticmethod
    def load_from_json(path: str) -> Dict[str, Any]:
        # 从 JSON 文件读取配置；以 utf-8 解析以支持中文等字符
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)


class AuditPlugin:
    """审计插件：将一个具名分析函数封装为可注册的审计单元。

    Args:
        name:         插件名称，作为报告中的分析键。
        analyze_func: 分析函数，接收 decision_context 并返回任意分析结果（通常为含 status 的字典）。
    """

    def __init__(self, name: str, analyze_func: Callable[[Dict[str, Any]], Any]):
        self.name = name
        self.analyze = analyze_func


# ==================== 收敛判定器（移植自 SPL 内核） ====================


class ConvergenceState(str, Enum):
    """形式化收敛五状态分类。

    BLOCKED          本轮出现阻断项（必需输入缺失等），立即终止，不算收敛
    BUDGET_EXHAUSTED 跑满 max_loops 或能量预算耗尽仍未收敛 —— 不是收敛
    FIXED_POINT      相邻两层的风险集合完全相同 —— 不动点，收敛
    NO_GAIN          风险集合清空且无未决假设 —— 无残留风险，收敛
    DIVERGED         仍有风险或未决假设，且与上层不同 —— 发散，需人工介入

    FIXED_POINT 与 NO_GAIN 都算真收敛，区别在于「停在哪」：
      NO_GAIN      = 停在一片干净的风险区（风险清零）
      FIXED_POINT  = 停在某个风险上不再变化（风险有界但不为零）
    只有 BUDGET_EXHAUSTED 是「跑完了但没跑到」——所以 is_true_convergence
    特意把它排除在外，防止把「时间到了」误当成「想通了」。
    """

    FIXED_POINT = "FIXED_POINT"
    NO_GAIN = "NO_GAIN"
    BUDGET_EXHAUSTED = "BUDGET_EXHAUSTED"
    DIVERGED = "DIVERGED"
    BLOCKED = "BLOCKED"

    @property
    def is_true_convergence(self) -> bool:
        return self in (ConvergenceState.FIXED_POINT, ConvergenceState.NO_GAIN)


class SpiralVerdict(str, Enum):
    """螺旋层终局。与收敛五状态并列存在，不互相替换。

    ConvergenceState 回答「结构收敛了吗」；SpiralVerdict 回答「这圈螺旋
    为什么停下」。两者会同时出现，各自独立可读——把它们合并成一个枚举，
    正是「把时间到了当成想通了」的温床。
    """

    CONVERGED = "CONVERGED"
    BUDGET_EXHAUSTED = "BUDGET_EXHAUSTED"
    AWAITING_HUMAN = "AWAITING_HUMAN"
    ORIGIN_DRIFT = "ORIGIN_DRIFT"
    SUPERPOSITION_VIOLATION = "SUPERPOSITION_VIOLATION"
    BLOCKED = "BLOCKED"

    # —— 极限收敛器（limit_reconstruct / spiral_step）专用 ——
    # 规范元因果基底第二条（并行收敛）：极限处唯一收敛（S∞ = S*）。
    LIMIT_REACHED = "LIMIT_REACHED"      # 距离归零并连续数层保持 → 抵达 S∞ = S*
    NOT_MONOTONE = "NOT_MONOTONE"        # 距离不再严格下降 → 不再逼近，必须停
    FLAT_SPIRAL = "FLAT_SPIRAL"          # 半径连续数层不降 → 只在原地扩圈
    ADVANCED = "ADVANCED"                # 单层推进成功且仍可继续（非终局）


@dataclass
class AuditEvent:
    """链上事件。

    sealed_hash 在 _append_event 时一次性写入。其后任何对 payload / event_type /
    timestamp / nonce 的改动都会使 hash 与 sealed_hash 不一致，从而被检出。
    为 None 表示该事件未经封存，内容不可验证。
    """

    event_type: str
    payload: Dict[str, Any]
    prev_hash: str
    timestamp: float = field(default_factory=time.time)
    nonce: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    sealed_hash: Optional[str] = None

    @property
    def hash(self) -> str:
        """本事件的链上哈希。三个 json 参数都有讲究，不能随手改：

        sort_keys=True     键序不影响结果，字典构造顺序无关紧要
        ensure_ascii=False 中文按原字符参与哈希，避免编码路径差异
        default=str        datetime 之类不可序列化的对象退化为字符串，
                           宁可损失精度也不让整条链崩掉

        注意：这个属性是**实时重算**的，任何事后修改都会改变它的返回值。
        因此校验不拿它当基准，而拿 _append_event 时写下的 sealed_hash 当基准——
        否则比对恒成立，篡改检测形同虚设。
        """
        blob = json.dumps({
            "event_type": self.event_type,
            "payload": self.payload,
            "prev_hash": self.prev_hash,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
        }, sort_keys=True, ensure_ascii=False, default=str)
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()


class ConvergenceChecker:
    """形式化收敛判定（P-1 终止 / P-2 不动点 / P-3 风险有界）。"""

    BLOCKING_STATUSES = {"BLOCKED", "CRITICAL"}
    HIGH_RISK_STATUSES = {"HIGH_RISK"}

    @staticmethod
    def classify(
        round_idx: int,
        max_rounds: int,
        previous_risks: frozenset,
        current_risks: frozenset,
        has_blocking: bool,
        has_unresolved_assumptions: bool,
    ) -> ConvergenceState:
        # 判定是一张**优先级链**，从上到下第一个命中即返回，顺序不可调换：
        #   1. has_blocking                → BLOCKED
        #   2. round_idx >= max_rounds     → BUDGET_EXHAUSTED
        #   3. 与上层风险集合同样且无未决  → FIXED_POINT
        #   4. 风险清空且无未决            → NO_GAIN
        #   5. 其余                        → DIVERGED
        #
        # 为什么阻断排在最前：必需输入缺失时，后面任何「看起来收敛了」
        # 的信号都不可信——风险集清零可能只是因为算子根本没拿到输入。
        #
        # 第 3 条要求 round_idx > 0：首层没有「上层」可比，必须落到后面几条。
        if has_blocking:
            return ConvergenceState.BLOCKED
        if round_idx >= max_rounds:
            return ConvergenceState.BUDGET_EXHAUSTED
        if round_idx > 0 and previous_risks == current_risks and not has_unresolved_assumptions:
            return ConvergenceState.FIXED_POINT
        if not current_risks and not has_unresolved_assumptions:
            return ConvergenceState.NO_GAIN
        return ConvergenceState.DIVERGED

    @staticmethod
    def extract_risk_set(report: Dict[str, Any]) -> Tuple[frozenset, bool]:
        # 风险键的构成是 (算子名, status, 结果的规范化 JSON)。
        # 必须把整个结果序列化进去，只比较 status 会漏掉
        # 「同一个 WARNING 但内容变了」这种情况——
        # 而那恰恰是 FIXED_POINT 需要识别的变化。
        risks = set()
        has_blocking = False
        for pname, result in report.get("analysis", {}).items():
            if not isinstance(result, dict):
                continue
            status = result.get("status")
            if status is None:
                # 部分插件输出 pass/halt_count 而非 status，不归一化则该插件级
                # 阻断对收敛判定不可见。halt_count>0 视为结构性阻断，
                # 其余 pass=False 只作 HIGH_RISK 信号。
                halt = result.get("halt_count")
                if isinstance(halt, int) and halt > 0:
                    status = "BLOCKED"
                elif result.get("pass") is False:
                    status = "HIGH_RISK"
            if status in ConvergenceChecker.BLOCKING_STATUSES:
                has_blocking = True
                risks.add((
                    pname, status,
                    json.dumps(result, sort_keys=True, default=str, ensure_ascii=False),
                ))
            elif status in ConvergenceChecker.HIGH_RISK_STATUSES or status == "WARNING":
                risks.add((
                    pname, status,
                    json.dumps(result, sort_keys=True, default=str, ensure_ascii=False),
                ))
        return frozenset(risks), has_blocking


class CognitiveAuditEngine:
    """认知审计引擎核心：负责责任锚定、静态诊断与因果重构推演。

    Args:
        account: 责任账户（组织/角色/阶段），用于责任闭环锚定。
        config:  审计配置（免责声明、allowed_stages、custom_fields 等）。
    """

    def __init__(self, account: ResponsibilityAccount, config: Dict[str, Any]):
        self.account = account
        self.config = config
        self.plugins: List[AuditPlugin] = []
        self.llm_provider: Optional[LLMProvider] = None
        # 哈希链：事件一经封存即不可改，链根是整次审计的唯一指纹。
        self.event_chain: List[AuditEvent] = []
        self._prev_event_hash: str = 'ROOT'
        # 可注入的确定性时钟；不注入即用真实时间（仅影响 timestamp，不影响 nonce）
        self._clock: Optional[float] = None
        # 人工批准过的进化候选（记账，不改代码）。代际 = len(_evolution_approvals)，
        # 因此「这份链根属于第几代引擎」可自证。
        self._evolution_approvals: List[Dict[str, Any]] = []

        # 校验责任阶段合法性：若配置限定了 allowed_stages，阶段不在其中则拒绝初始化
        allowed_stages = self.config.get("allowed_stages", [])
        if allowed_stages and account.stage not in allowed_stages:
            raise ValueError(f"Unsupported stage: {account.stage}")

    def set_llm_provider(self, provider: LLMProvider) -> None:
        """注入大模型接口，启用 LLM 增强语义分析。"""
        self.llm_provider = provider

    def register_plugin(self, plugin: AuditPlugin) -> None:
        # 注册一个审计插件，供后续 audit / reconstruct 调用
        self.plugins.append(plugin)

    def audit(
        self,
        decision_context: Dict[str, Any],
        save_log: bool = False,
        log_dir: str = "logs",
    ) -> Dict[str, Any]:
        """
        静态诊断阶段：提取上下文、遍历注册插件并生成偏见/脆弱性评估报告。

        Args:
            decision_context: 决策上下文（待审计的输入数据）。
            save_log:        是否将本次报告落盘为本地审计日志，默认 False（不落盘）。
            log_dir:          日志目录，默认 "logs"（相对当前工作目录）。
        Returns:
            报告字典：含免责声明、责任账户、各插件分析结果、自定义字段。
            若 save_log=True，报告将额外包含 log_path 字段（日志文件绝对路径）。
        """
        report = {
            "disclaimer": self.config.get("disclaimer", ""),          # 免责声明（来自配置）
            "responsibility_account": self.account.__dict__,          # 责任账户快照，用于追溯
            "analysis": {},                                            # 各插件分析结果容器
            "custom_fields": self.config.get("custom_fields", {})      # 配置中的自定义字段透传
        }
        # 隔离调用方上下文：内部键（责任账户、前序结果）注入浅拷贝，防止污染原始输入
        ctx = dict(decision_context)
        ctx["_responsibility_account"] = self.account.__dict__
        prior: Dict[str, Any] = {}
        ctx["_prior_audit_results"] = prior
        # 阈值走配置而不是散落在算子里的常数：同一份输入在不同地方必须算出
        # 同一个 A6 / A10，否则账本失去可比性。
        ctx["_config"] = getattr(self, "config", {}) or {}
        # 极限收敛器的状态回传位：由螺旋层注入，供 META 读「是否已抵达 S∞ = S*」。
        # 不注入即为空——缺就是缺，不猜。
        ctx.setdefault("_limit_state", {})
        ctx.setdefault("_spiral_state", {})

        # STATE 负责汇总前四级结果，无论注册顺序都强制最后执行
        ordered = [p for p in self.plugins if p.name != "STATE"] + \
                  [p for p in self.plugins if p.name == "STATE"]
        # 按序运行插件，结果同时写入报告与前序聚合（供 STATE 最终裁定）
        for plugin in ordered:
            result = plugin.analyze(ctx)
            report["analysis"][plugin.name] = result
            prior[plugin.name] = result

        # LLM 增强语义分析（若已注入 provider；不参与 STATE 聚合）
        if self.llm_provider is not None:
            llm_analysis = self._llm_enhanced_audit(decision_context)
            if llm_analysis:
                report["analysis"]["llm_enhanced"] = llm_analysis

        # ── 报告视图装配 ──
        # 少了这一层，TPG 算出了拓扑、META 结出了账本，报告顶层却什么都看不见，
        # 上层（adapter / hub / 报告渲染）只能去 analysis 里翻——翻不到就等于没算。
        # 三块视图都只在对应算子存在时才写入：只跑原五算子子集的调用方，报告
        # 结构与扩展前逐字节一致。兼容不是靠解释，是靠不写入空字段。
        tpg = report["analysis"].get("TPG")
        if isinstance(tpg, dict):
            report["topology"] = {
                "graph_hash": tpg.get("graph_hash", ""),
                "node_count": tpg.get("node_count", 0),
                "edge_count": tpg.get("edge_count", 0),
                "source": tpg.get("source"),
                "validation": tpg.get("validation", {}),
                "relative_labels": tpg.get("relative_labels", {}),
                # 公理 5：链内时序 + 观测位置（本次审计站在哪条链上）
                "time_order": tpg.get("time_order", {}),
                "graph": tpg.get("topology", {}),
            }

        bfc = report["analysis"].get("BFC")
        if isinstance(bfc, dict):
            report["bfc"] = {
                "status": bfc.get("status"),
                "reason": bfc.get("reason"),
                "verdicts": bfc.get("verdicts", []),
                "remediation": bfc.get("remediation", []),
            }

        meta = report["analysis"].get("META")
        if isinstance(meta, dict):
            # 注意：元因果账本**不参与**任何阻断判定（META 是 T2，结构上不允许）。
            report["meta_ledger"] = {
                "status": meta.get("status"),
                "reason": meta.get("reason"),
                "bases": meta.get("meta_bases", {}),
                "high_risk_bases": meta.get("high_risk_bases", []),
                "warning_bases": meta.get("warning_bases", []),
            }

        # 本地审计日志落盘（默认关闭，显式 save_log=True 才写入）
        if save_log:
            report["log_path"] = self._write_log(report, log_dir)

        return report

    # -------- 算子清单 / 哈希链 --------

    def _ordered_plugins(self) -> List[Any]:
        """执行顺序：STATE 恒最后（它汇总前面所有算子），其余保持注册顺序。"""
        return ([p for p in self.plugins if getattr(p, "name", "") != "STATE"]
                + [p for p in self.plugins if getattr(p, "name", "") == "STATE"])

    def operator_manifest(self) -> List[Dict[str, Any]]:
        """算子清单：执行顺序 + 名称 + 版本。

        与 SPL 内核的偏差：内核清单含「权限层 tier」（T1 结构性 / T2 信号 /
        T3 叙事），由内核在引擎层强制；Nomos 的插件契约更薄（只有 PLUGIN_NAME /
        PLUGIN_VERSION），没有 tier 概念，故此处不产出 tier 字段，算子集指纹
        也只由 (名, 版本, 顺序) 推导。**这是有意的偏差，不是遗漏**：在没有
        层级强制机制的一侧声称自己有层级，比如实说没有更危险。
        """
        return [{
            'order': i,
            'name': getattr(p, 'name', ''),
            'version': getattr(p, 'PLUGIN_VERSION', ''),
        } for i, p in enumerate(self._ordered_plugins())]

    def operator_set_hash(self) -> str:
        """算子集指纹：仅由 (名, 版本, 顺序) 推导，可跨进程复算。"""
        blob = json.dumps(
            [[m['name'], m['version'], m['order']] for m in self.operator_manifest()],
            sort_keys=True, ensure_ascii=False,
        )
        return hashlib.sha256(blob.encode('utf-8')).hexdigest()[:16]

    def _append_event(self, event_type: str, payload: Dict[str, Any]) -> AuditEvent:
        idx = len(self.event_chain)
        ts = self._clock if self._clock is not None else time.time()
        # 确定性 nonce：由前序哈希 / 事件类型 / 序号推导，取代 uuid4 随机值，
        # 否则同一输入两次运行的链根不同，可复现性就被破坏了。
        nonce = hashlib.sha256(
            f'{self._prev_event_hash}|{event_type}|{idx}'.encode('utf-8')
        ).hexdigest()[:8]
        ev = AuditEvent(
            event_type=event_type, payload=payload,
            prev_hash=self._prev_event_hash, timestamp=ts, nonce=nonce,
        )
        # 封存：自此刻起，内容若被改动即与封存值不符。
        ev.sealed_hash = ev.hash
        self.event_chain.append(ev)
        self._prev_event_hash = ev.sealed_hash
        return ev

    @property
    def chain_root_hash(self) -> str:
        """链根哈希，即最后一个事件的 sealed_hash；空链时为哨兵值「ROOT」。

        这是整个审计的唯一指纹。要对外披露校验凭据，披露的应该是它，
        并且这个值必须存在报告之外的地方（落盘后与报告分离保存）——
        与报告放在一起就等于没有锚点。
        """
        return self._prev_event_hash

    @staticmethod
    def _neighbourhood(topo: Dict[str, Any]) -> Dict[str, set]:
        """把拓扑压成 1-邻域表：{节点: {(方向, 邻居, 关系)}}。"""
        table: Dict[str, set] = {}
        for edge in (topo or {}).get('edges', []) or []:
            if not isinstance(edge, dict):
                continue
            src, dst = str(edge.get('src', '')), str(edge.get('dst', ''))
            rel = str(edge.get('relation', 'causal'))
            if not src or not dst:
                continue
            table.setdefault(src, set()).add(('out', dst, rel))
            table.setdefault(dst, set()).add(('in', src, rel))
        return table

    @classmethod
    def _stable_nodes(cls, previous: Optional[Dict[str, Any]],
                      current: Dict[str, Any]) -> List[str]:
        """已收敛节点 = 相邻两层 1-邻域完全一致的节点。

        这是「收敛」在拓扑层唯一的可判定定义：节点本身没名字、没属性，
        能收敛的只有它的连接关系。邻域一致即结构不动点，可冻结。
        """
        if not previous:
            return []
        prev_table = cls._neighbourhood(previous)
        curr_table = cls._neighbourhood(current)
        return sorted(n for n, nb in curr_table.items()
                      if nb and prev_table.get(n) == nb)

    # -------- 算子 ⊛∞：自主进化层（版本谱系 · 只提案不适用） --------

    # 缺口 → 结构改进方向的映射。方向是**引擎自身的输入契约**，
    # 不是对用户决策的建议 —— 引擎永远 decision-agnostic。
    EVOLUTION_HINTS: Dict[str, str] = {
        'ORI': '把原点 / 目标稳态 / 资源三项从「运行时检查」前移为输入契约必填',
        'NS': '把该叙事遮蔽模式纳入 A6 阈值的显式声明，而不是事后统计',
        'IAP': '把该隐含假设纳入 assumptions 必填清单',
        'LCH': '把该薄弱点纳入 branches 覆盖度校验（每条假设都必须有 ΔD）',
        'TPG': '把该拓扑违规升级为 .tpg 语法层的编译期拦截',
        'BFC': '把该证据缺口前移为事实声明阶段的必填校验',
        'CCS': '把该因果缺口前移为假设声明阶段的必填校验',
        'GRF': '把该现实反馈缺口前移为灰度放量的前置条件',
        'META': '把该元基账本的阈值纳入 config，使口径可显式声明',
        'STATE': '把该裁定出口的缺失条件前移为输入契约必填',
    }
    EVOLUTION_HINT_DEFAULT = '把该结构缺口前移为输入契约的显式校验项'

    def evolution_lineage(self) -> Dict[str, Any]:
        """版本谱系：这份链根属于第几代引擎。

        自主进化与可复现性之所以能共存，全靠这一个对象：
        进化改了算子集 → operator_set_hash 变 → lineage_hash 变 → 证书随之变；
        而**旧代际的链根仍然可以被旧代际的算子集复算出来**，因为代际是显式
        声明的，不是靠「记得当时是什么样」推断的。
        """
        lineage: Dict[str, Any] = {
            'generation': len(self._evolution_approvals),
            'nomos_version': VERSION,
            'topology_version': TOPOLOGY_VERSION,
            'operator_set_hash': self.operator_set_hash(),
            'operator_count': len(self.operator_manifest()),
            'approved_proposals': [p.get('id') for p in self._evolution_approvals],
        }
        lineage['lineage_hash'] = hashlib.sha256(
            json.dumps(lineage, sort_keys=True, ensure_ascii=False).encode('utf-8')
        ).hexdigest()[:16]
        return lineage

    def evolve(
        self,
        decision_context: Dict[str, Any],
        approved_deltas: Optional[List[Dict[str, Any]]] = None,
        max_loops: int = 8,
        energy_budget: Optional[float] = None,
        loop_cost: float = 1.0,
        gap_threshold: int = 1,
        proposal_limit: int = 8,
    ) -> Dict[str, Any]:
        """⊛∞ 自主进化层：引擎自己发现结构缺口，但**永不自己改写判定规则**。

        规范里的同名接口（IR 层）已把这层写死：
            evolve(g, delta) -> Graph            运行期演化入口
            g = rewrite(g, best_rule(g))         图重写（DPO 语义）
            「每次重写必须保持 Constraint 可满足」  ← 门控
            停机：CSP 最小不动点 g_{n+1} == g_n   ← 图同构判定
            A10 审计熵增 ≈ version 的单调递增速率，**有界**才收敛于 S*
        本方法是它们的落地 —— 但**刻意少了「自动 apply」那一步**。

        为什么引擎不许自己 apply
        ------------------------
        自主 apply 会同时摧毁三样东西：
            1. 可复现性   同输入 + 同 nonce + 同 clock 必须同链根；
            2. 证书证据力 第三方要能拿同一份代码复算出同一个根；
            3. 不自驱纪律 引擎永不自己生成修正。
        所以产出是**候选清单**，不是新规则。三条恒等式写死在返回值里：
            candidate.applies_automatically 恒 False
            candidate.requires_human        恒 True
            auto_applied                    恒 0
        人工裁决走 approve_evolution_proposal()：它只**记账**（升代际），
        不改代码 —— 改代码必须由人做，返回里明写 applied_to_code=False。

        候选口径（纯计数，零学习、零权重、零 LLM）
        -------------------------------------------
        每一层审计里，凡是 status 不属于 {PASS, SKIPPED} 的算子，或元因果账本里
        不是 PASS 的元基，都记一次出现；**出现次数 ≥ gap_threshold** 的缺口
        才成为候选。「反复出现」是唯一的入选标准 —— 一次性的异常不是结构缺口。
        """
        if gap_threshold < 1:
            raise ValueError('gap_threshold must be >= 1')
        if max_loops < 1:
            raise ValueError('max_loops must be >= 1')

        stack = SpiralStack(energy_budget=energy_budget, loop_cost=loop_cost)
        current_ctx = copy.deepcopy(decision_context)
        approved = list(approved_deltas or [])

        tally: Dict[str, Dict[str, Any]] = {}
        provenance_per_layer: List[int] = []
        layer_hashes: List[str] = []
        loops: List[Dict[str, Any]] = []
        previous_risks: frozenset = frozenset()
        previous_topo: Optional[Dict[str, Any]] = None
        state = ConvergenceState.DIVERGED
        verdict = SpiralVerdict.AWAITING_HUMAN
        final_report: Dict[str, Any] = {}
        origin_drift = False
        fixed_round: Optional[int] = None
        fixed_hash = ''

        for idx in range(max_loops + 1):
            if idx > 0 and not stack.can_run():
                verdict = SpiralVerdict.BUDGET_EXHAUSTED
                loops.append({'loop': idx, 'state': state.value,
                              'verdict': verdict.value,
                              'reason': 'ENERGY_BUDGET_EXHAUSTED',
                              'energy_left': stack.energy_left})
                break

            if idx < len(approved):
                delta = approved[idx]
                if not isinstance(delta, dict) or not delta:
                    verdict = SpiralVerdict.BLOCKED
                    loops.append({'loop': idx, 'state': ConvergenceState.BLOCKED.value,
                                  'verdict': verdict.value,
                                  'reason': 'EMPTY_OR_INVALID_DELTA'})
                    break
                current_ctx.update(delta)
                self._append_event('DELTA_APPLIED',
                                   {'loop': idx, 'delta_keys': sorted(delta.keys())})
            elif idx > 0:
                verdict = SpiralVerdict.AWAITING_HUMAN
                loops.append({'loop': idx, 'state': state.value,
                              'verdict': verdict.value, 'awaiting_human': True,
                              'reason': 'NO_MORE_APPROVED_DELTAS'})
                break

            loop_ctx = dict(current_ctx)
            loop_ctx['_spiral_state'] = stack.to_dict()
            report = self.audit(loop_ctx)
            final_report = report
            analysis = report.get('analysis', {}) or {}

            # ── 缺口登记：本层所有非 PASS 的结构信号 ──
            def _note(code: str, operator: str, status: str, layer: int) -> None:
                entry = tally.setdefault(code, {
                    'code': code, 'operator': operator,
                    'observed_status': status, 'occurrences': 0, 'evidence_layers': [],
                })
                entry['occurrences'] += 1
                entry['evidence_layers'].append(layer)

            for op in sorted(analysis):
                # META 的缺口由下面按元基逐条登记（粒度更细、口径更准）。
                # 这里再登记一次它的汇总状态，同一个缺口就会在候选清单里出现两遍，
                # 「反复出现」这个唯一入选标准就被人为地刷高了。
                if op == 'META':
                    continue
                res = analysis.get(op)
                if not isinstance(res, dict):
                    continue
                st = res.get('status')
                if st is None or st in ('PASS', 'SKIPPED'):
                    continue
                _note(f"{op}:{res.get('reason', st)}", op, str(st), idx)

            meta = analysis.get('META')
            if isinstance(meta, dict):
                for base, body in sorted((meta.get('meta_bases') or {}).items()):
                    if isinstance(body, dict) and body.get('status') != 'PASS':
                        _note(f"META.{base}:{body.get('reason')}", 'META',
                              str(body.get('status')), idx)

            topo = report.get('topology', {}).get('graph', {}) or {}
            graph_hash = report.get('topology', {}).get('graph_hash', '')
            origin_hash = report.get('origin_anchor', {}).get('origin_hash', '')
            previous_topo_for_this = previous_topo

            # ── 最小不动点：g_{n+1} == g_n（图同构判定）──
            if layer_hashes and graph_hash and graph_hash == layer_hashes[-1]:
                if fixed_round is None:
                    fixed_round, fixed_hash = idx, graph_hash
            layer_hashes.append(graph_hash)
            provenance_per_layer.append(len(topo.get('provenance', []) or []))

            current_risks, has_blocking = ConvergenceChecker.extract_risk_set(report)
            has_unresolved = bool(
                report.get('implicit_assumptions', {}).get('missing_required'))
            state = ConvergenceChecker.classify(
                round_idx=idx, max_rounds=max_loops,
                previous_risks=previous_risks, current_risks=current_risks,
                has_blocking=has_blocking,
                has_unresolved_assumptions=has_unresolved,
            )

            origin_drift = stack.origin_drift(origin_hash)
            converged_nodes = self._stable_nodes(previous_topo_for_this, topo)
            layer = stack.push(
                state=state.value, origin_hash=origin_hash,
                risk_set=current_risks, graph_hash=graph_hash, topology=topo,
                converged_nodes=converged_nodes, index=idx, unresolved=has_unresolved,
            )

            loops.append({
                'loop': idx, 'state': state.value, 'risk_count': layer.radius,
                'graph_hash': graph_hash, 'layer_hash': layer.layer_hash,
                'newly_frozen': sorted(converged_nodes),
                'provenance_entries': provenance_per_layer[-1],
                'energy_left': layer.energy_left,
            })

            if origin_drift:
                verdict = SpiralVerdict.ORIGIN_DRIFT
                break
            if any(v['severity'] == 'HALT' for v in stack.violations):
                verdict = SpiralVerdict.SUPERPOSITION_VIOLATION
                break
            if state != ConvergenceState.DIVERGED:
                if state.is_true_convergence:
                    verdict = SpiralVerdict.CONVERGED
                elif state == ConvergenceState.BLOCKED:
                    verdict = SpiralVerdict.BLOCKED
                else:
                    verdict = SpiralVerdict.BUDGET_EXHAUSTED
                break
            if stack.is_static():
                verdict = SpiralVerdict.FLAT_SPIRAL
                break

            previous_risks = current_risks
            previous_topo = topo

        # ── A10 审计熵增：每层留痕条数（version 递增速率的离散版）──
        layers_n = max(1, len(provenance_per_layer))
        a10 = round(sum(provenance_per_layer) / layers_n, 6) if provenance_per_layer else 0.0
        ceiling = MetaCausalLedgerPlugin._ceiling(
            {'_config': self.config}, 'audit_entropy_ceiling',
            MetaCausalLedgerPlugin.DEFAULT_AUDIT_ENTROPY_CEILING)
        bounded = a10 <= ceiling
        monotone = all(b >= a for a, b in zip(provenance_per_layer,
                                              provenance_per_layer[1:]))

        # ── 候选清单：反复出现的缺口才入选 ──
        proposals: List[Dict[str, Any]] = []
        for code in sorted(tally):
            entry = tally[code]
            if entry['occurrences'] < gap_threshold:
                continue
            proposals.append({
                'id': 'EVO-' + hashlib.sha256(code.encode('utf-8')).hexdigest()[:8],
                'code': code,
                'operator': entry['operator'],
                'observed_status': entry['observed_status'],
                'occurrences': entry['occurrences'],
                'evidence_layers': entry['evidence_layers'],
                'proposed_change': self.EVOLUTION_HINTS.get(
                    entry['operator'], self.EVOLUTION_HINT_DEFAULT),
                'status': 'PROPOSED',
                # 三条恒等式：候选永远不会自己生效。
                'applies_automatically': False,
                'requires_human': True,
            })
        proposals = proposals[:proposal_limit]

        lineage = self.evolution_lineage()
        self._append_event('EVOLUTION_SCAN', {
            'proposals': len(proposals),
            'auto_applied': 0,
            'lineage_hash': lineage['lineage_hash'],
            'a10': a10,
            'bounded': bounded,
            'fixed_point_round': fixed_round,
        })

        return {
            'nomos_version': VERSION,
            'verdict': verdict.value,
            'final_state': state.value,
            'is_true_convergence': state.is_true_convergence,
            'origin_drift': origin_drift,
            'lineage': lineage,
            'audit_entropy': {
                'a10': a10,
                'per_layer': provenance_per_layer,
                'version_monotone': monotone,
                'ceiling': ceiling,
                'bounded': bounded,
                'doctrine': '审计有界：A10 有界，使演化收敛于 S*',
            },
            'fixed_point': {
                'found': fixed_round is not None,
                'round': fixed_round,
                'graph_hash': fixed_hash,
                'criterion': 'g_{n+1} == g_n（图同构判定）',
            },
            'proposals': proposals,
            'proposal_count': len(proposals),
            'gap_threshold': gap_threshold,
            # 三条恒等式的对外断言：任何一次 evolve 都必须满足。
            'auto_applied': 0,
            'requires_human': True,
            'loops': loops,
            'total_loops': len(loops),
            'spiral': stack.to_dict(),
            'final_report': final_report,
            'session_root_hash': self.chain_root_hash,
        }

    def approve_evolution_proposal(
        self,
        proposal: Dict[str, Any],
        approved_by: str,
    ) -> Dict[str, Any]:
        """人工裁决进化候选：**只记账，不改代码**。

        这是「只提案，人工 apply」的落点。它做两件事、且只做两件事：
            1. 把批准记录进事件链（署名的、可复核的）；
            2. 让版本谱系升一代 —— 此后新产生的链根都带这个代际号。

        它**不做**的事，恰恰是最重要的一件：不去改引擎的判定规则。
        原因不是技术上做不到，而是做法本身会毁掉证书：引擎一旦能改自己的
        判定标准，第三方就再也无法「拿同一份代码复算出同一个根」，
        这样产出的证书只是一张自签名的纸。
        """
        pid = str((proposal or {}).get('id', '')).strip()
        if not pid:
            raise ValueError('缺少候选 id：无法记账')
        signer = str(approved_by or '').strip()
        if not signer:
            raise ValueError('人工裁决必须署名：approved_by 不能为空')

        record = {
            'id': pid,
            'code': str(proposal.get('code', '')),
            'approved_by': signer,
            'generation': len(self._evolution_approvals),
        }
        self._evolution_approvals.append(record)
        self._append_event('EVOLUTION_APPROVED', record)
        return {
            'approved': record,
            'lineage': self.evolution_lineage(),
            # 引擎升了代际，但没有改自己的判定规则。
            'applied_to_code': False,
            'requires_code_change': True,
            'note': '引擎永不自动改写判定规则；本记录只声明「人已批准该结构变更」。'
                    '实际改代码必须由人完成，完成后须升版本号。',
        }

    def _write_log(self, report: Dict[str, Any], log_dir: str) -> str:
        """
        将审计报告写入本地日志目录（决定论 IO 操作，无随机性）。

        Args:
            report:  audit() 产出的完整报告字典。
            log_dir: 日志目录路径。
        Returns:
            日志文件的绝对路径。
        """
        # 提取唯一审计 ID：优先取 STATE 插件证书中的 audit_id，兜底用 nonce+时间戳
        audit_id = None
        state_result = report.get("analysis", {}).get("STATE", {})
        if isinstance(state_result, dict):
            audit_id = state_result.get("certificate", {}).get("audit_id")
        if not audit_id:
            nonce = self.account.nonce or uuid.uuid4().hex[:8]
            audit_id = f"SPL-{nonce}-{int(time.time())}"

        os.makedirs(log_dir, exist_ok=True)
        path = os.path.join(log_dir, f"{audit_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        return os.path.abspath(path)

    def _llm_enhanced_audit(self, decision_context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """使用 LLM 对决策上下文进行语义级偏见/风险分析，返回结构化审计结果。"""
        prompt = (
            "你是一个认知审计专家。请对以下决策上下文进行语义级分析，"
            "识别潜在的认知偏见、逻辑漏洞和脆弱性信号。\n\n"
            f"决策上下文：\n{json.dumps(decision_context, ensure_ascii=False, indent=2)}\n\n"
            "请以 JSON 格式返回分析结果，包含以下字段：\n"
            "- bias_flags: 检测到的偏见列表（每条含 type, evidence, severity）\n"
            "- logic_gaps: 逻辑漏洞列表（每条含 description, impact）\n"
            "- risk_signals: 风险信号列表（每条含 signal, level）\n"
            "- overall_assessment: 总体评估文本"
        )
        try:
            raw = self.llm_provider.generate(prompt, temperature=0.3, max_tokens=4096)
            # 尝试从返回中提取 JSON 块
            result = json.loads(raw)
            if isinstance(result, dict):
                return result
            # 兜底：如果返回的不是 JSON 字典，包装为文本分析
            return {"llm_raw_analysis": raw}
        except Exception:
            return None

    def reconstruct(
        self, 
        decision_context: Dict[str, Any], 
        delta_vars: Dict[str, Any],
        convergence_evaluator: Optional[Callable[[Dict[str, Any], Dict[str, Any]], bool]] = None
    ) -> Dict[str, Any]:
        """
        因果重构推演算子：
        1. 注入修正变量 (delta_vars) 重构逻辑链条
        2. 进行二次反事实校验与审计
        3. 评估系统是否收敛至目标稳态

        Args:
            decision_context:       原始决策上下文。
            delta_vars:             修正变量（注入以重构逻辑链）。
            convergence_evaluator:  可选自定义收敛评估器，签名为 (original_report, reconstructed_report) -> bool。
        Returns:
            推演结果字典：含收敛状态、修正变量、重构上下文及重构报告。
        """
        # 1. 隔离并重构决策上下文：深拷贝避免污染原始输入，再叠加修正变量
        reconstructed_context = copy.deepcopy(decision_context)
        reconstructed_context.update(delta_vars)

        # 2. 获取原始报告与重构后的二次审计报告（对同一组插件做反事实对比）
        original_report = self.audit(decision_context)
        reconstructed_report = self.audit(reconstructed_context)

        # 3. LLM 收敛性语义评估（若已注入 provider）
        llm_convergence = None
        if self.llm_provider is not None:
            llm_convergence = self._llm_convergence_assess(
                original_report, reconstructed_report, delta_vars
            )

        # 3. 收敛性判定：优先使用自定义评估器，否则退回默认阻断状态检测
        if convergence_evaluator:
            is_converged = convergence_evaluator(original_report, reconstructed_report)
        else:
            is_converged = self._default_convergence_check(reconstructed_report)

        return {
            "status": "CONVERGED" if is_converged else "DIVERGED",  # 收敛/发散状态
            "delta_variables": delta_vars,                          # 实际注入的修正变量
            "reconstructed_context": reconstructed_context,          # 重构后的上下文
            "reconstructed_report": reconstructed_report,            # 重构后的审计报告
            "is_converged": is_converged,                           # 布尔收敛标志
            "llm_convergence": llm_convergence,                     # LLM 语义收敛评估（若有）
        }

    def _llm_convergence_assess(
        self,
        original_report: Dict[str, Any],
        reconstructed_report: Dict[str, Any],
        delta_vars: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        """使用 LLM 对重构前后的审计报告进行语义级收敛性评估。"""
        prompt = (
            "你是一个因果收敛评估专家。请比较以下两份审计报告（原始 vs 重构后），"
            "判断注入修正变量后系统是否已收敛至目标稳态。\n\n"
            f"修正变量：{json.dumps(delta_vars, ensure_ascii=False)}\n\n"
            f"原始报告：\n{json.dumps(original_report, ensure_ascii=False, indent=2)}\n\n"
            f"重构后报告：\n{json.dumps(reconstructed_report, ensure_ascii=False, indent=2)}\n\n"
            "请以 JSON 格式返回评估结果，包含以下字段：\n"
            "- converged: true/false\n"
            "- reasoning: 评估依据\n"
            "- residual_risks: 残余风险列表（若有）"
        )
        try:
            raw = self.llm_provider.generate(prompt, temperature=0.3, max_tokens=4096)
            return json.loads(raw)
        except Exception:
            return None

    @staticmethod
    def _default_convergence_check(reconstructed_report: Dict[str, Any]) -> bool:
        """
        默认判定逻辑：检查重构后的分析插件输出中是否已无高风险或中断状态。
        只要任一插件结果状态为 BLOCKED / HIGH_RISK / CRITICAL，即判定未收敛。
        """
        analysis = reconstructed_report.get("analysis", {})
        for plugin_name, result in analysis.items():
            # 仅对含 status 字段的字典型结果做判定，避免非预期结构引发异常
            if isinstance(result, dict) and result.get("status") in ["BLOCKED", "HIGH_RISK", "CRITICAL"]:
                return False
        return True
