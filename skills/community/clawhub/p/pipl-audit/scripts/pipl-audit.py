#!/usr/bin/env python3
"""
PIPL Audit — 个人信息保护法合规深度审计（免费 skill + 云端合规引擎）

基于《中华人民共和国个人信息保护法》（PIPL，2021 年 11 月 1 日施行）及配套规则，
覆盖 9 大审计域、32 项深度审计检查：审计范围与制度基础、告知同意、处理原则、
敏感个人信息与未成年人、个人权利、自动化决策、跨境传输、数据安全与事件响应、
治理与持续合规。审计视角聚焦证据审查、流程留痕与可追溯性。

本 skill 免费安装。检查项由 CQDev 云端合规引擎（compliancehub.cn）提供；
评分与额度在云端计算。首次使用请先在 compliancehub.cn 获取免费 API Key
（100 次免费调用）：
  - 打开：https://compliancehub.cn/account.html?skill=pipl-audit
  - 然后通过环境变量提供 Key：export COMPLIANCEHUB_API_KEY=<your-key>
    或保存到：~/.config/compliancehub/pipl-audit.key（mode 0600）

流程：
  1. 加载 API Key（环境变量 COMPLIANCEHUB_API_KEY，或 ~/.config/compliancehub/pipl-audit.key）
  2. 从云端规则库 API 拉取检查项（公开只读，单一事实来源）
  3. 交互式逐项收集审计状态（y=通过 / n=未通过 / na=不适用）
  4. 提交到云端 evaluate 端点，云端评分并返回报告数据
  5. 本地渲染专业审计报告（含风险等级、证据样例与整改建议）

没有 API Key？skill 会自动进入匿名试用模式：本地生成随机 anon_id，
每 skill 可获得 5 次真实云端评分（7 天窗口）。额度用尽后引导一键注册，
并携带 anon_id 保证进度不丢失。

仅使用 Python 内置 urllib，零第三方依赖。Key 走 HTTPS + Bearer 传输；
无硬编码、无隐蔽外传。网络访问仅发生在评分运行时：（a）从固定端点拉取
公开检查项规则库（只读，不发送任何作答）；（b）将你的作答与 API Key
（作为 Bearer token）发送到固定 evaluate 端点。--non-interactive /
--non-interactive-json 免费预览完全离线，使用内置 CHECK_ITEMS，绝不联网。
不收集任何凭据；注册在网站（compliancehub.cn/account.html）完成，不在终端。
"""


import sys, os, json, argparse, datetime, ssl, uuid
import urllib.request
import urllib.error
import urllib.parse

sys.path.insert(0, os.path.dirname(__file__))

# ─── Cloud endpoints ──────────────────────────────────────────────
# API_BASE is PINNED to the operator's official compliance cloud and is
# intentionally NOT overridable via an environment variable. Allowing a
# COMPLIANCEHUB_API_BASE override would let a malicious environment redirect
# users' compliance answers AND their API Key (sent as a Bearer token) to an
# attacker-controlled server — flagged by security scanners as a "redirectable
# cloud endpoint" / credential-exfiltration chain. The destination is fixed.
API_BASE = "https://compliancehub.cn"
SKILL_SLUG = os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RULES_URL = f"{API_BASE}/api/v1/rules/{SKILL_SLUG}/rules"        # public read: check items
EVALUATE_URL = f"{API_BASE}/api/v1/rules/{SKILL_SLUG}/evaluate"  # auth: scoring
ACCOUNT_PAGE = f"{API_BASE}/account.html?skill={SKILL_SLUG}&utm_source=skill&utm_medium=agent"      # unified account center (utm for attribution)


def _skill_version():
    pkg = os.path.join(os.path.dirname(__file__), "..", "package.json")
    try:
        if os.path.isfile(pkg):
            with open(pkg, encoding="utf-8") as f:
                return json.load(f).get("version", "2.0.0")
    except Exception:
        pass
    return "2.0.0"


def _ua():
    return f"{SKILL_SLUG}/{_skill_version()}"


# ─── API Key resolution ──────────────────────────────────────────

def _key_path():
    """Private, per-user key store OUTSIDE the skill directory.

    The API Key is written here (mode 0600) rather than inside the skill
    folder, so it is never committed to source control or shared with the
    workspace. This addresses the 'plaintext API key in shared/source-
    controlled workspace' concern raised in security review.
    """
    d = os.path.join(os.path.expanduser("~"), ".config", "compliancehub")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, f"{SKILL_SLUG}.key")


def load_api_key():
    """Resolve API Key precedence:
      1) env COMPLIANCEHUB_API_KEY (ephemeral, safest)
      2) private store ~/.config/compliancehub/<slug>.key (mode 0600)
    """
    env_key = os.environ.get("COMPLIANCEHUB_API_KEY")
    if env_key and env_key.strip():
        return env_key.strip()
    p = _key_path()
    if os.path.isfile(p):
        try:
            with open(p, encoding="utf-8") as f:
                s = f.read().strip()
                if s:
                    return s
        except Exception:
            pass
    return None


def _anon_id_path():
    """Per-user anonymous trial id store (mode 0600), outside the skill dir."""
    d = os.path.join(os.path.expanduser("~"), ".config", "compliancehub")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, f"{SKILL_SLUG}.anon_id")


def load_or_create_anon_id():
    """Return the persistent anonymous trial id, creating a fresh uuid on first run.

    The anon_id lets the cloud engine keep a 7-day, up-to-5-use anonymous quota
    per skill WITHOUT requiring registration first. It is a plain random uuid and
    carries no personal data; it is only used to continue the anonymous trial
    and to pre-fill the registration page when the trial runs out.
    """
    p = _anon_id_path()
    if os.path.isfile(p):
        try:
            with open(p, encoding="utf-8") as f:
                s = f.read().strip()
                if s and len(s) <= 64:
                    return s
        except Exception:
            pass
    aid = str(uuid.uuid4())
    try:
        with open(p, "w", encoding="utf-8") as f:
            f.write(aid)
        os.chmod(p, 0o600)
    except Exception:
        pass
    return aid


def _register_page(anon_id=None):
    """Registration funnel URL. The anon_id is passed through so the account page
    can keep the visitor's trial context and make registering a one-click jump."""
    url = ACCOUNT_PAGE
    if anon_id:
        url += "&anon_id=" + urllib.parse.quote(anon_id)
    return url


# ─── Rule data source (cloud rule-library API, public read) ──────

def fetch_rules():
    """Fetch pipl-audit items from the cloud rule library (public, no Key needed).

    Returns a mapped item list (id=item_key / name / desc / ref / category /
    recommendation); returns None on any error so the caller falls back to the
    built-in CHECK_ITEMS.
    """
    try:
        ctx = ssl.create_default_context()
        req = urllib.request.Request(RULES_URL, headers={"User-Agent": _ua()})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            if resp.status != 200:
                return None
            payload = json.loads(resp.read().decode("utf-8"))
        if not payload.get("success"):
            return None
        raw_items = payload.get("items") or []
        if not raw_items:
            return None
        items = []
        for it in raw_items:
            items.append({
                "id": it.get("item_key"),
                "name": it.get("name"),
                "desc": it.get("question") or it.get("description") or "",
                "ref": it.get("legal_ref") or "",
                "category": it.get("category_name") or "",
                "recommendation": it.get("recommendation") or "",
            })
        return items
    except Exception:
        return None


# ─── Check items (fallback data source) ─────────────────────────

CHECK_ITEMS = [
    {"id": "audit.art6-9", "name": "审计范围与制度基础", "desc": "是否建立了覆盖 PIPL 全流程（收集/存储/使用/加工/传输/删除）的合规制度与数据地图？", "ref": "第 6-9 条 / 第 51 条", "category": "A. 审计范围与制度基础", "recommendation": "梳理处理活动全景，建立数据地图与制度文件，并留存版本与发布记录。", "severity": "high"},
    {"id": "audit.data_map", "name": "数据资产清单", "desc": "是否维护完整的个人数据资产清单（数据源、处理目的、流转路径、保存期限）？", "ref": "第 6 条 / 第 51 条", "category": "A. 审计范围与制度基础", "recommendation": "建立并定期更新数据资产台账，标注敏感信息与出境场景。", "severity": "high"},
    {"id": "audit.staff_training", "name": "人员培训与考核", "desc": "是否对处理个人信息的员工开展定期合规培训并留存培训/考核记录？", "ref": "第 9 条 / 第 52 条", "category": "A. 审计范围与制度基础", "recommendation": "制定培训计划，覆盖数据处理与安全责任，保留参训与考核证据。", "severity": "medium"},
    {"id": "audit.art13-14", "name": "告知内容完整性", "desc": "告知是否覆盖处理者身份、处理目的与方式、信息种类、保存期限、权利行使与投诉渠道等全部要素？", "ref": "第 13-14 条", "category": "B. 告知同意审计", "recommendation": "对照第 13/14 条逐项核验告知文本要素，缺失项补齐并留痕。", "severity": "high"},
    {"id": "audit.consent_validity", "name": "同意有效性", "desc": "同意是否真实自愿、明确清晰、在收集前取得，且敏感处理单独同意不被捆绑？", "ref": "第 13-15 条 / 第 29 条", "category": "B. 告知同意审计", "recommendation": "审查同意获取链路：独立性、可理解性、可拒绝性，并验证敏感场景的单独同意。", "severity": "critical"},
    {"id": "audit.consent_withdrawal", "name": "撤回机制", "desc": "是否提供与给予同意同等便捷的撤回渠道，且撤回后即时停止处理？", "ref": "第 15-16 条", "category": "B. 告知同意审计", "recommendation": "部署与授权同等入口的撤回机制，验证撤回后处理停止与数据处置。", "severity": "high"},
    {"id": "audit.consent_records", "name": "同意留痕", "desc": "是否留存同意的时间、内容、版本与证明，并支持按需回溯？", "ref": "第 16 条", "category": "B. 告知同意审计", "recommendation": "建立同意台账（时间戳/版本/上下文），支持审计回溯。", "severity": "medium"},
    {"id": "audit.minimization", "name": "最小必要审查", "desc": "是否定期审查收集字段与处理目的的匹配度，并删除超范围数据？", "ref": "第 6 条", "category": "C. 处理原则审计", "recommendation": "建立字段-目的映射审查机制，定期清理非必要收集。", "severity": "high"},
    {"id": "audit.transparency", "name": "公开透明", "desc": "隐私政策是否清晰易懂、与实际处理一致，并随业务变更及时更新？", "ref": "第 7 条", "category": "C. 处理原则审计", "recommendation": "核对隐私政策与实际处理一致性，建立变更触发更新机制。", "severity": "medium"},
    {"id": "audit.data_quality", "name": "数据质量", "desc": "是否有数据准确性验证、更正与过期清理机制？", "ref": "第 8 条", "category": "C. 处理原则审计", "recommendation": "建立数据准确性校验与过期数据清理流程。", "severity": "medium"},
    {"id": "audit.sensitive_id", "name": "敏感信息识别", "desc": "是否建立敏感个人信息识别标准（生物识别/健康/金融/行踪等）并完成分类标注？", "ref": "第 28 条", "category": "D. 敏感信息与未成年人审计", "recommendation": "制定识别标准，全量盘点并标注敏感信息资产。", "severity": "critical"},
    {"id": "audit.sensitive_consent", "name": "敏感处理独立同意", "desc": "敏感信息处理是否取得单独同意，且处理目的严格限定于必要场景？", "ref": "第 29 条", "category": "D. 敏感信息与未成年人审计", "recommendation": "验证敏感处理的单独同意与目的限定，审计超范围使用。", "severity": "high"},
    {"id": "audit.minors", "name": "未成年人保护", "desc": "是否对不满 14 周岁未成年人建立监护人同意的验证与保护机制？", "ref": "第 31 条", "category": "D. 敏感信息与未成年人审计", "recommendation": "部署年龄核验与监护人同意机制，留存验证证据。", "severity": "high"},
    {"id": "audit.rights_channel", "name": "权利受理渠道", "desc": "是否提供便捷的查阅/复制/更正/删除/可携带请求入口？", "ref": "第 44-45 条", "category": "E. 个人权利审计", "recommendation": "梳理并公开权利请求入口，验证渠道可用性。", "severity": "high"},
    {"id": "audit.rights_processing", "name": "权利响应流程", "desc": "是否在法定期限内响应权利请求，并有身份核验与拒绝理由记录？", "ref": "第 44-48 条", "category": "E. 个人权利审计", "recommendation": "建立响应时限监控、身份核验与拒绝记录机制。", "severity": "high"},
    {"id": "audit.rights_deletion", "name": "删除权执行", "desc": "删除请求是否覆盖备份副本与第三方共享链路？", "ref": "第 47 条", "category": "E. 个人权利审计", "recommendation": "验证删除指令的传播与备份清理，留存执行证据。", "severity": "high"},
    {"id": "audit.rights_portability", "name": "可携带权", "desc": "是否支持以结构化、通用、可机读格式导出个人信息？", "ref": "第 45 条第 3 款", "category": "E. 个人权利审计", "recommendation": "实现标准格式导出接口并验证互操作性。", "severity": "medium"},
    {"id": "audit.rights_explanation", "name": "解释与人工干预", "desc": "是否对自动化决策提供解释说明与人工复核渠道？", "ref": "第 24 条 / 第 48 条", "category": "E. 个人权利审计", "recommendation": "提供决策解释接口与人工申诉复核通道。", "severity": "medium"},
    {"id": "audit.automated_disclosure", "name": "自动化决策告知", "desc": "是否向个人告知自动化决策的存在、逻辑与影响？", "ref": "第 24 条", "category": "F. 自动化决策审计", "recommendation": "审查自动化决策场景的告知完整性与可理解性。", "severity": "high"},
    {"id": "audit.automated_fairness", "name": "公平性审计", "desc": "是否定期审计自动化决策的公平性、避免不合理差别待遇并支持人工复核？", "ref": "第 24 条", "category": "F. 自动化决策审计", "recommendation": "建立公平性评估机制，抽查定价/营销场景的差别待遇。", "severity": "high"},
    {"id": "audit.cross_border_path", "name": "出境路径合规", "desc": "出境是否基于安全评估/标准合同/认证之一，并留存相应凭证？", "ref": "第 38 条", "category": "G. 跨境传输审计", "recommendation": "核验出境路径凭证的有效性与申报记录。", "severity": "critical"},
    {"id": "audit.cross_border_notice", "name": "出境告知与单独同意", "desc": "是否告知境外接收方名称、联系方式、处理目的与信息种类，并取得单独同意？", "ref": "第 39 条", "category": "G. 跨境传输审计", "recommendation": "验证出境告知内容与单独同意获取证据。", "severity": "high"},
    {"id": "audit.cross_border_reassessment", "name": "出境再评估", "desc": "出境情形变化（规模/目的/接收方）时是否重新评估、补办申报或重新取得同意？", "ref": "第 38-40 条", "category": "G. 跨境传输审计", "recommendation": "建立出境变更触发复审机制并留存再评估记录。", "severity": "high"},
    {"id": "audit.security_controls", "name": "安全技术措施", "desc": "是否部署加密、访问控制、脱敏等与风险相称的技术措施？", "ref": "第 9 条 / 第 51 条", "category": "H. 数据安全与事件响应审计", "recommendation": "审查加密、权限与脱敏控制的实际覆盖与有效性。", "severity": "critical"},
    {"id": "audit.security_org", "name": "安全管理组织", "desc": "是否明确安全责任人、制度与操作规程？", "ref": "第 51 条", "category": "H. 数据安全与事件响应审计", "recommendation": "核验安全责任分工、制度文件与操作规范落地。", "severity": "high"},
    {"id": "audit.breach_detection", "name": "事件监测与分级", "desc": "是否建立安全事件监测、分类分级与定级机制？", "ref": "第 57 条", "category": "H. 数据安全与事件响应审计", "recommendation": "审查监测告警链路与事件分级标准。", "severity": "high"},
    {"id": "audit.breach_response", "name": "事件响应与通知", "desc": "是否具备应急响应预案、补救措施与按规定通知机制？", "ref": "第 57 条", "category": "H. 数据安全与事件响应审计", "recommendation": "验证预案完整性、演练记录与通知义务履行。", "severity": "critical"},
    {"id": "audit.dpo", "name": "个人信息保护负责人", "desc": "是否依法指定个人信息保护负责人并公示联系方式？", "ref": "第 52 条", "category": "I. 治理与持续合规审计", "recommendation": "核验负责人任命、职责履行与公示。", "severity": "high"},
    {"id": "audit.pia", "name": "保护影响评估", "desc": "是否对法定情形开展个人信息保护影响评估并保存报告（至少 3 年）？", "ref": "第 55-56 条", "category": "I. 治理与持续合规审计", "recommendation": "审查 PIA 覆盖范围、报告质量与保存期限。", "severity": "high"},
    {"id": "audit.internal_audit", "name": "定期合规审计", "desc": "是否至少每年开展一次合规审计并跟踪整改闭环？", "ref": "第 54 条", "category": "I. 治理与持续合规审计", "recommendation": "核验年度审计计划、执行记录与整改闭环。", "severity": "high"},
    {"id": "audit.delegation", "name": "委托处理管理", "desc": "委托处理是否签订含目的/范围/期限/保护义务的合同，并对受托方实施监督？", "ref": "第 21-23 条", "category": "I. 治理与持续合规审计", "recommendation": "盘点受托方、核验合同条款与监督措施。", "severity": "high"},
    {"id": "audit.platform_duty", "name": "大型平台特别义务", "desc": "平台型处理者是否建立独立监督机构、社会监督与年度报告机制？", "ref": "第 58 条", "category": "I. 治理与持续合规审计", "recommendation": "核验特别义务履行证据（监督机构/报告/投诉机制）。", "severity": "medium"},
]


# ─── Interactive collection ──────────────────────────────────────

def collect_responses(items):
    """Collect per-item compliance status interactively (y=pass / n=fail / na=n/a)."""
    responses = []
    total = len(items)
    print(f"\n📋 PIPL Compliance Audit — {total} items")
    print("   请逐项输入审计结论（y=通过 / n=未通过 / na=不适用）\n")
    for i, item in enumerate(items):
        idx = i + 1
        while True:
            ans = input(f"  [{idx}/{total}] {item['name']} [{item['ref']}]\n"
                        f"        {item['desc']}\n"
                        f"        (y/n/na) > ").strip().lower()
            if ans in ('y', 'n', 'na'):
                if ans == 'na':
                    responses.append({**item, "status": "na"})
                else:
                    responses.append({**item, "status": "pass" if ans == 'y' else "fail"})
                break
            print("        please enter y, n or na")
    return responses


def build_submission(responses):
    """Convert interactive results to cloud evaluate request items (na excluded)."""
    items = []
    for r in responses:
        if r["status"] == "na":
            continue
        items.append({
            "item_key": r["id"],
            "passed": r["status"] == "pass",
            "evidence": None,
        })
    return items


# ─── Cloud scoring ───────────────────────────────────────────────

def call_evaluate(key, submission, anon_id=None):
    """Call the cloud evaluate endpoint; returns (data, error)."""
    payload = {"items": submission, "context": None}
    if anon_id:
        payload["anon_id"] = anon_id
    body = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json", "User-Agent": _ua()}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    req = urllib.request.Request(
        EVALUATE_URL,
        data=body,
        headers=headers,
        method="POST",
    )
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            if resp.status != 200:
                return None, f"cloud returned HTTP {resp.status}"
            return json.loads(resp.read().decode("utf-8")), None
    except urllib.error.HTTPError as e:
        detail = ""
        try:
            detail = json.loads(e.read().decode("utf-8", "ignore")).get("detail", "")
        except Exception:
            pass
        if e.code == 401:
            return None, "API Key invalid or unauthorized; get a new one at %s (then set COMPLIANCEHUB_API_KEY or save to the key file)" % ACCOUNT_PAGE
        if e.code == 403:
            if anon_id:
                # Anonymous trial exhausted -> the caller routes to registration.
                return None, "ANON_QUOTA_EXHAUSTED"
            return None, f"free quota exhausted: {detail} (get a new key at %s)" % ACCOUNT_PAGE
        if e.code == 404:
            return None, f"rule library not open: {detail}"
        return None, f"cloud error HTTP {e.code}: {detail}"
    except Exception as e:
        return None, f"cloud call failed: {e}"


# ─── Report rendering ────────────────────────────────────────────

def render_text(data, items):
    s = data
    lines = [
        "=" * 60,
        "  PIPL Compliance Audit Report (cloud-scored)",
        "  Law: 中华人民共和国个人信息保护法 (PIPL)",
        f"  Engine version: {s.get('version', '?')}",
        f"  Compliance score: {s.get('score')}/100",
        "=" * 60,
        f"  Overview: {s.get('total_items')} items counted | ✅ Pass {s.get('passed_count')} | ❌ Fail {s.get('failed_count')} | Free quota left {s.get('quota_remaining')}",
        "=" * 60,
    ]
    sev_label = {"critical": "🔴 严重", "high": "🟠 高", "medium": "🟡 中", "low": "🟢 低"}
    current_cat = ""
    for r in items:
        if r.get("category") != current_cat:
            current_cat = r.get("category", "")
            lines.append(f"\n  ── {current_cat} ──")
        icon = "✅" if r.get("passed") else "❌"
        sev = r.get("severity") or ""
        sev_txt = f"  [风险等级：{sev_label.get(sev, sev)}]" if sev else ""
        lines.append(f"\n  {icon} [{r.get('item_key')}] {r.get('name')}{sev_txt}")
        lines.append(f"    Status: {'Pass' if r.get('passed') else 'Fail'}")
        if r.get("legal_ref"):
            lines.append(f"    Authority: {r.get('legal_ref')}")
        if not r.get("passed"):
            meta = r.get("meta") or {}
            rt = meta.get("remediation_template")
            if rt:
                lines.append(f"    🔧 整改建议: {rt.get('summary', '')}")
                for step in (rt.get("steps") or [])[:3]:
                    lines.append(f"       · {step}")
            lt = meta.get("legal_text")
            if lt and lt.get("snippet"):
                lines.append(f"    📜 法条依据: {lt.get('snippet', '')}")
        if r.get("recommendation"):
            lines.append(f"    Recommendation: {r.get('recommendation')}")
    lines.append("=" * 60)
    lines.append("\n💡 Disclaimer: This report is generated by the CQDev cloud compliance engine for reference only and does not constitute legal advice.")
    return "\n".join(lines)


def render_html(data, items):
    s = data
    score = s.get("score", 0)
    color = "#4caf50" if score >= 80 else "#ff9800" if score >= 60 else "#f44336"
    rows = ""
    sev_cls = {"critical": "#dc2626", "high": "#ea580c", "medium": "#ca8a04", "low": "#16a34a"}
    sev_label = {"critical": "严重", "high": "高", "medium": "中", "low": "低"}
    current_cat = ""
    for r in items:
        if r.get("category") != current_cat:
            current_cat = r.get("category", "")
            rows += f'<tr class="category-row"><td colspan="6">{current_cat}</td></tr>\n'
        icon = "✅" if r.get("passed") else "❌"
        cls = "pass" if r.get("passed") else "fail"
        sev = r.get("severity") or ""
        sev_badge = ""
        if sev:
            color = sev_cls.get(sev, "#64748b")
            sev_badge = f'<span style="background:{color};color:#fff;padding:2px 8px;border-radius:10px;font-size:.75rem">{sev_label.get(sev, sev)}</span>'
        rec = r.get("recommendation") or "Keep it up"
        meta = r.get("meta") or {}
        rt = meta.get("remediation_template")
        if not r.get("passed") and rt:
            rec = f"🔧 {rt.get('summary', '')}（整改期限约 {rt.get('deadline_days', '')} 天）"
        rows += f"""<tr class="{cls}"><td>{icon}</td><td>{r.get('name')}</td><td>{r.get('legal_ref') or ''}</td><td>{sev_badge}</td><td>{cls.upper()}</td><td>{rec}</td></tr>\n"""
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>PIPL 个人信息保护法合规深度审计报告</title>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC',sans-serif;max-width:960px;margin:2rem auto;padding:0 1rem;color:#333}}
h1{{border-bottom:2px solid #2563eb;padding-bottom:.5rem}}
.score-card{{background:linear-gradient(135deg,#2563eb,#1d4ed8);color:#fff;padding:2rem;border-radius:12px;text-align:center;margin:1.5rem 0}}
.score{{font-size:4rem;font-weight:700}}
.summary{{display:flex;gap:2rem;justify-content:center;margin-top:1rem}}
.summary div{{text-align:center;font-size:1.2rem}}
table{{width:100%;border-collapse:collapse;margin-top:1.5rem}}
th{{background:#f1f5f9;text-align:left;padding:.75rem;border-bottom:2px solid #e2e8f0}}
td{{padding:.75rem;border-bottom:1px solid #e2e8f0}}
tr.pass td:first-child{{color:#4caf50}}
tr.fail td:first-child{{color:#f44336}}
tr.category-row td{{background:#dbeafe;font-weight:600;color:#1d4ed8}}
.note{{color:#94a3b8;margin-top:2rem;font-size:.85rem}}
</style></head>
<body>
<h1>PIPL 个人信息保护法合规深度审计报告</h1>
<p>Law: 中华人民共和国个人信息保护法 (PIPL) 及配套规则</p>
<p>Engine version: {s.get('version','?')} ｜ Free quota left: {s.get('quota_remaining')}</p>
<div class="score-card"><div class="score">{score}</div><div>合规评分 / 100</div>
<div class="summary"><div>✅ 通过<br><b>{s.get('passed_count')}</b></div><div>❌ 未通过<br><b>{s.get('failed_count')}</b></div><div>检查项<br><b>{s.get('total_items')}</b></div></div></div>
<table><thead><tr><th></th><th>检查项</th><th>法条</th><th>风险等级</th><th>状态</th><th>整改建议</th></tr></thead><tbody>{rows}</tbody></table>
<p class="note">本报告由 CQDev 云端合规引擎生成，仅供参考，不构成法律意见。</p>
</body></html>"""


def generate_report(payload, format="text"):
    """Render report from cloud response. payload is the full evaluate JSON."""
    data = payload.get("data", {}) if isinstance(payload, dict) else {}
    items = data.get("items", [])
    if format == "json":
        return json.dumps(payload, ensure_ascii=False, indent=2)
    elif format == "html":
        return render_html(data, items)
    return render_text(data, items)


# ─── Main entry ──────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="PIPL compliance audit (free skill + cloud engine)")
    parser.add_argument("--non-interactive", action="store_true", help="free preview mode (list items, no scoring)")
    parser.add_argument("--non-interactive-json", action="store_true", help="free preview JSON mode (for sandbox case generation)")
    parser.add_argument("--format", "-f", choices=["text", "json", "html"], default="text")
    parser.add_argument("--output", "-o", help="report output file path")
    args = parser.parse_args()

    # ── free previews run OFFLINE using the bundled CHECK_ITEMS (no network) ──
    if args.non_interactive or args.non_interactive_json:
        items = CHECK_ITEMS
        if args.non_interactive_json:
            preview_data = [{
                "id": item["id"], "name": item["name"],
                "desc": item["desc"], "ref": item["ref"], "category": item["category"],
            } for item in items]
            print(json.dumps({
                "preview": True,
                "total_items": len(items),
                "free": True,
                "needs_api_key": True,
                "offline": True,
                "register_page": ACCOUNT_PAGE,
                "message": "This check is free, but scoring runs on the CQDev cloud engine and needs a free API Key.",
                "preview_items": preview_data,
            }, ensure_ascii=False, indent=2))
            return

        # ── free preview (list items, no scoring, no Key) ──
        print(f"\n🔍 Free preview mode — {len(items)} items (offline, bundled); scoring needs a free API Key\n")
        current_cat = ""
        for it in items:
            if it.get("category") != current_cat:
                current_cat = it.get("category", "")
                print(f"\n  ── {current_cat} ──")
            print(f"  • [{it['id']}] {it['name']}  [{it['ref']}]")
            print(f"      {it['desc']}")
        print(f"\n💡 Scoring runs on the cloud engine. Get a free API Key: {ACCOUNT_PAGE}")
        return

    # ── full check: registered Key, or anonymous trial when no Key ──
    key = load_api_key()
    anon_id = None
    if not key:
        anon_id = load_or_create_anon_id()
        print("🔒 匿名试用模式：本检查将通过 compliancehub.cn 云端引擎真实评分，无需注册可免费试 5 次。")
        print("   你的作答将发送到 compliancehub.cn 云端引擎进行评分，用于生成本次合规报告；详细数据处理见隐私政策 https://compliancehub.cn/privacy.html")
    # Check items come from the cloud rule library; fall back to built-in CHECK_ITEMS on failure
    items = fetch_rules() or CHECK_ITEMS
    responses = collect_responses(items)
    submission = build_submission(responses)
    if not submission:
        print("❌ No countable items (all marked not applicable).")
        sys.exit(1)

    print("\n⏳ Submitting to cloud compliance engine for scoring…")
    payload, err = call_evaluate(key, submission, anon_id)
    if err == "ANON_QUOTA_EXHAUSTED":
        reg = _register_page(anon_id)
        if args.format == "json":
            print(json.dumps({"error": "anon_quota_exhausted",
                              "message": "匿名试用额度已用尽（每 skill 5 次），请注册后继续使用",
                              "get_key_page": reg}, ensure_ascii=False, indent=2))
        else:
            print("❌ 匿名试用的 5 次额度已用尽。")
            print("💡 注册即可继续使用（免费 API Key 含 100 次额度）。")
            print(f"👉 打开注册页（已带入你的试用进度）：{reg}")
        sys.exit(2)
    elif err:
        print(f"❌ {err}")
        sys.exit(1)

    report = generate_report(payload, format=args.format)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"✅ Report saved to: {args.output}")
    else:
        print(report)
    data_out = payload.get("data") or {}
    if anon_id:
        tl = data_out.get("trials_left")
        if tl is not None:
            print(f"\n💡 匿名试用剩余次数：{tl}/5（注册后每把 Key 含 100 次免费额度）。")
    else:
        rem = data_out.get("quota_remaining")
        if rem is not None:
            print(f"\n💡 This Key's remaining free quota: {rem} calls.")


if __name__ == "__main__":
    main()
