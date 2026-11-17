#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
init.py — 本体论智能体 · 引导式实例化引擎
本体论智能体 (Ontology Agent) · 天津市微数人工智能科技有限责任公司

职责（对应 GUIDE 六步 + 六层人设模型）：
  1. match_pack(text)           第1步：根据企业描述匹配行业包
  2. collect_profile(answers)   第2~4步：采集企业画像（含 D 老板画像 / E 文化 / F 上下文）
  3. generate_instance(...)     生成 instance.yaml（与 semantic.yaml 模板分离）
  4. build_experts(...)         第3步：生成专家团清单（带入 action_specs 能力 + 六层人设拼装）

设计为「被运行时（WorkBuddy / EdgeClaw / 本地）调用」的辅助模块，
同时支持 CLI 演示： python init.py --demo
"""
import os
import re
import yaml

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKS_DIR = os.path.join(BASE, "references", "packs")
INSTANCE_PATH = os.path.join(BASE, "instance.yaml")
TEMPLATE_PATH = os.path.join(BASE, "experts-template", "department_experts.yaml")
DEPT_ACTIONS_PATH = os.path.join(BASE, "references", "department_actions.yaml")
ACTION_SPECS_PATH = os.path.join(BASE, "references", "action_specs.yaml")

# 团队包名后缀（用户拍板：替代"专家团"，更贴"数字公司"隐喻，可对接真实员工与场景）
TEAM_SUFFIX = "本体论智能体数字公司"
TEAM_SUFFIX_EN = "Ontology Agent Digital Company"


# ── 命名辅助 ────────────────────────────────────────────────────────
def team_display_name(short_name, lang="en"):
    """Team display name: {short name} / Ontology Agent Digital Company."""
    suffix = TEAM_SUFFIX_EN if lang == "en" else TEAM_SUFFIX
    return f"{short_name} / {suffix}" if short_name else suffix


def slugify(text):
    """生成机器安全的包 id（部署时 expert-manager 可进一步规范化）。"""
    s = re.sub(r"[^0-9a-zA-Z]+", "-", text).strip("-").lower()
    return s or "ontology-digital-company"


# ── 第1步：匹配行业包 ────────────────────────────────────────────────
def _load_pack_files(lang="en"):
    """Load pack files for one language. Returns {canonical_pid: data}.

    canonical_pid has no `.zh` suffix, so `opc.yaml` and `opc.zh.yaml` both map to `opc`.
    This keeps pack ids stable across languages (scripts and instance.yaml rely on them).
    """
    out = {}
    if not os.path.isdir(PACKS_DIR):
        return out
    for fn in os.listdir(PACKS_DIR):
        if not fn.endswith((".yaml", ".yml")):
            continue
        is_zh = fn.endswith(".zh.yaml")
        if lang == "en" and is_zh:
            continue          # English mode: ignore Chinese originals
        if lang == "zh" and not is_zh:
            continue          # Chinese mode: use the .zh originals
        pid = fn[:-8] if is_zh else fn[:-5]
        with open(os.path.join(PACKS_DIR, fn), encoding="utf-8") as fh:
            out[pid] = yaml.safe_load(fh)
    return out


def load_packs(lang="en"):
    """Load industry packs for `lang` ('en' or 'zh'); fall back to the other language if empty."""
    packs = _load_pack_files(lang)
    if not packs:
        packs = _load_pack_files("zh" if lang == "en" else "en")
    return packs


def match_pack(user_text, packs=None, lang="en"):
    """返回 (pack_id, score, reason)。关键词命中越多得分越高。

    Matches in the requested language first; if nothing hits, falls back to the other
    language's keyword set so a Chinese description still resolves to the canonical pack id.
    """
    packs = packs or load_packs(lang)
    user_text = (user_text or "").lower()

    def _scan(mapping):
        best, best_score, hits_best = None, 0, []
        for pid, p in mapping.items():
            kws = p.get("meta", {}).get("match_keywords", [])
            hits = [k for k in kws if k.lower() in user_text]
            if len(hits) > best_score:
                best, best_score, hits_best = pid, len(hits), hits
        return best, best_score, hits_best

    best, best_score, hits = _scan(packs)
    if best is None:
        # cross-language fallback: Chinese description vs English keywords (and vice versa)
        best, best_score, hits = _scan(_load_pack_files("zh" if lang == "en" else "en"))
    if best is None:
        return None, 0, "未匹配到已知行业包，建议补充描述或新增 pack"
    return best, best_score, "命中关键词: " + "、".join(hits)


# ── 第2~4步：采集企业画像（六层）─────────────────────────────────────
def collect_profile(answers):
    """answers: dict。返回规范化 profile，含 C 实例基础 + D 老板画像 + E 文化 + F 上下文。"""
    return {
        # C 层：实例基础数据
        "short_name": answers.get("short_name", ""),
        "company": answers.get("company", ""),
        "enterprise_type": answers.get("enterprise_type", ""),
        "legal_form": answers.get("legal_form", ""),
        "region": answers.get("region", ""),
        "industry": answers.get("industry", ""),
        "scale": answers.get("scale", ""),
        "credit_code": answers.get("credit_code", ""),
        "departments": list(answers.get("departments", [])),
        "workflow": list(answers.get("workflow", [])),
        # D 层：老板个人画像（10 维度）
        "owner_profile": answers.get("owner_profile", {}) or {},
        # E 层：企业文化 / 品牌声量
        "culture": answers.get("culture", {}) or {},
        # F 层：动态业务上下文
        "context": answers.get("context", {}) or {},
    }


# ── 部门动作 + 动作 spec 加载（用于给专家注入真实能力）──────────────
def ref_path(filename, lang="en", subdir="references"):
    """Resolve a kernel data file for the requested language.

    en -> references/<filename>
    zh -> references/<stem>.zh.yaml when present, else the English default.
    """
    p = os.path.join(BASE, subdir, filename)
    if lang == "zh":
        stem = filename[:-len(".yaml")] if filename.endswith(".yaml") else filename
        zhp = os.path.join(BASE, subdir, stem + ".zh.yaml")
        if os.path.isfile(zhp):
            return zhp
    return p


def tpl_path(lang="en"):
    """Expert template path for the requested language."""
    zhp = os.path.join(BASE, "experts-template", "department_experts.zh.yaml")
    if lang == "zh" and os.path.isfile(zhp):
        return zhp
    return os.path.join(BASE, "experts-template", "department_experts.yaml")


def load_department_actions(lang="en"):
    p = ref_path("department_actions.yaml", lang)
    if not os.path.isfile(p):
        return {}
    da = yaml.safe_load(open(p, encoding="utf-8"))
    out = {}
    for code, body in da.get("departments", {}).items():
        out[code] = [a["slug"] for a in body.get("actions", [])]
    return out


def load_action_specs(lang="en"):
    p = ref_path("action_specs.yaml", lang)
    if not os.path.isfile(p):
        return {}
    a = yaml.safe_load(open(p, encoding="utf-8"))
    return a.get("actions", {})


# ── 部门库（24 部门模板）与私有覆盖合并 ──────────────────────────────
def load_template(template_path=None, lang="en"):
    template_path = template_path or tpl_path(lang)
    with open(template_path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def resolve_departments(instance, template_path=None, lang="en"):
    """合并技能包部门库(模板) + 用户私有覆盖(instance)，返回最终部门清单。

    覆盖项（只存于 instance.yaml 的 company-data，绝不修改技能包本体）：
      - disabled_departments : 停用部门 code 列表
      - department_aliases   : {code: 显示名} 改名
      - department_genders   : {code: male/female} 指定性别（仅影响头像/语感，不影响能力）
      - custom_departments   : [{code,name,gender,expertise,tools_ref,persona}] 私有新增部门
    """
    template_path = template_path or tpl_path(lang)
    tpl = load_template(template_path, lang)
    all_depts = {d["code"]: d for d in tpl["departments"]}
    base = list(instance.get("departments")
                or [d["code"] for d in tpl["departments"] if d.get("core")])
    disabled = set(instance.get("disabled_departments") or [])
    aliases = instance.get("department_aliases") or {}
    genders = instance.get("department_genders") or {}
    resolved = []
    for code in base:
        if code in disabled:
            continue
        d = all_depts.get(code)
        if not d:
            continue
        rd = dict(d)
        if code in aliases:
            rd["name"] = aliases[code]
        rd["gender"] = genders.get(code, d.get("gender_default", "male"))
        resolved.append(rd)
    # 私有新增部门（用户自定义，不在技能包内，是个人部署层覆盖）
    for cd in instance.get("custom_departments") or []:
        resolved.append({
            "code": cd.get("code"),
            "name": cd.get("name", cd.get("code")),
            "gender": cd.get("gender", "male"),
            "expertise": cd.get("expertise", ""),
            "tools_ref": cd.get("tools_ref", ""),
            "persona": cd.get("persona", {}),
            "core": False,
            "custom": True,
        })
    return resolved


def list_catalog(template_path=None, lang="en"):
    """返回 24 部门库目录（core/可选 + 性别默认 + 适用场景），供引导时给用户挑选。"""
    tpl = load_template(template_path, lang)
    return [
        {k: d.get(k) for k in ("code", "name", "core", "category",
                               "gender_default", "when_to_include", "expertise")}
        for d in tpl["departments"]
    ]


def load_instance(path):
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def save_instance(path, inst):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        yaml.safe_dump(inst, fh, allow_unicode=True, sort_keys=False)


def customize_instance(slug, action, **kw):
    """对用户私有 instance.yaml 做定制；返回更新后的 instance（失败返回 None）。"""
    path = default_instance_path(slug)
    if not os.path.isfile(path):
        print(f"[customize] 未找到实例: {path}（请先用 init.py 生成实例）")
        return None
    inst = load_instance(path)
    if action == "rename":
        inst.setdefault("department_aliases", {})[kw["code"]] = kw["name"]
        print(f"[customize] {kw['code']} 改名为「{kw['name']}」")
    elif action == "gender":
        inst.setdefault("department_genders", {})[kw["code"]] = kw["gender"]
        print(f"[customize] {kw['code']} 性别设为 {kw['gender']}（仅影响头像/语感）")
    elif action == "disable":
        dd = inst.setdefault("disabled_departments", [])
        if kw["code"] not in dd:
            dd.append(kw["code"])
        print(f"[customize] 停用部门 {kw['code']}")
    elif action == "enable":
        inst["disabled_departments"] = [c for c in inst.get("disabled_departments", [])
                                        if c != kw["code"]]
        print(f"[customize] 启用部门 {kw['code']}")
    elif action == "add":
        cd = kw["custom"]
        inst.setdefault("custom_departments", []).append(cd)
        if cd["code"] not in inst.get("departments", []):
            inst.setdefault("departments", []).append(cd["code"])
        print(f"[customize] 新增私有部门 {cd['code']}（{cd.get('name')}）")
    elif action == "remove":
        inst["custom_departments"] = [c for c in inst.get("custom_departments", [])
                                      if c.get("code") != kw["code"]]
        inst["departments"] = [c for c in inst.get("departments", []) if c != kw["code"]]
        print(f"[customize] 移除私有部门 {kw['code']}")
    else:
        print(f"[customize] 未知 action: {action}")
        return inst
    save_instance(path, inst)
    return inst


# ── 生成 instance.yaml（模板与实例分离）─────────────────────────────
def company_data_dir(short_name=None):
    """稳定数据目录：~/.workbuddy/company-data/<slug>/，与技能代码分离、跨工作区有效。
    无简称时回退到技能目录（兼容 --demo）。"""
    slug = slugify(short_name) if short_name else ""
    if not slug:
        return BASE
    return os.path.join(os.path.expanduser("~"), ".workbuddy", "company-data", slug)


def default_instance_path(short_name):
    return os.path.join(company_data_dir(short_name), "instance.yaml")


def default_memory_path(short_name):
    return os.path.join(company_data_dir(short_name), "company-memory.md")


def _init_memory_log(mem_path, profile):
    """首次为某公司初始化记忆日志种子（含 PII 红线说明），不覆盖已有文件。"""
    os.makedirs(os.path.dirname(mem_path), exist_ok=True)
    company = profile.get("company") or profile.get("short_name") or "本公司"
    etype = profile.get("enterprise_type", "")
    region = profile.get("region", "")
    content = (
        f"# {company} · 公司记忆日志\n\n"
        "> 本文件由本体论智能体自动维护，持续累积 owner 确认的事实 / 决策 / 风险。\n"
        "> 跨会话持久，数字公司（专家团）每次会话开始会读取。\n"
        "> PII 红线：身份证 / 银行卡 / 票据影像等敏感信息一律不写入明文。\n\n"
        "## 基础信息\n"
        f"- 公司：{company}\n"
        f"- 类型：{etype}\n"
        f"- 地区：{region}\n\n"
        "## 决策记录\n"
        "（待补充：owner 在对话中确认的关键决策、风险、变更）\n"
    )
    with open(mem_path, "w", encoding="utf-8") as fh:
        fh.write(content)


def generate_instance(pack_id, profile, packs=None, out_path=None, lang="en"):
    packs = packs or load_packs(lang)
    pack = packs.get(pack_id, {})
    specs = load_action_specs(lang)
    short = profile.get("short_name", "")
    if out_path is None:
        # 默认落到稳定数据目录；无简称时回退技能目录（兼容 --demo）
        out_path = default_instance_path(short) if short else INSTANCE_PATH
    instance = {
        "meta": {
            "generated_by": "ontology-agent/init.py",
            "pack_id": pack_id,
            "pack_display": pack.get("meta", {}).get("display_name", pack_id),
            "team_name": team_display_name(short, lang),
            "team_slug": slugify(team_display_name(short, lang)),
            "template_ref": "references/semantic.yaml",  # 实例引用模板，不复制
            "action_specs_total": len(specs),            # 引用逻辑层动作库规模
        },
        "profile": profile,
        "departments": list(profile["departments"]),
        "workflow": list(profile["workflow"]),
        "policy_hooks": pack.get("policy_hooks", {}),
    }
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        yaml.safe_dump(instance, fh, allow_unicode=True, sort_keys=False)
    # 自动初始化记忆日志种子（仅当该公司尚无记忆日志时，绝不覆盖）
    if short:
        mem_path = default_memory_path(short)
        if not os.path.isfile(mem_path):
            _init_memory_log(mem_path, profile)
    return out_path


# ── 六层人设拼装：A 基础部门 + B 行业包风味 + C 实例 + D 老板 + E 文化 + F 上下文 ──
def _fill(text, op, cul):
    """把 persona 文本中的 {owner_*} / {culture_*} 占位符替换为 D/E/F 实际值。"""
    mapping = {
        "{owner_addr}": op.get("address_as", op.get("name", "老板")),
        "{owner_decision}": op.get("decision_style", "商议型"),
        "{owner_risk}": op.get("risk_appetite", "平衡"),
        "{owner_comm}": op.get("comm_style", "口语化、简洁"),
        "{owner_auth}": op.get("auth_boundary", "关键操作须经老板确认"),
        "{owner_taboo}": op.get("taboo", ""),
        "{culture_voice}": cul.get("voice", "专业、务实"),
        "{culture_taboo}": cul.get("taboo_topics", ""),
    }
    for k, v in mapping.items():
        if v:
            text = text.replace(k, v)
    return text


# ── 双语术语标准层（注入专家 system_prompt，使标准层真正被使用而非空置）──
_GLOSSARY_CACHE = None
def load_glossary():
    """加载 references/glossary.yaml（双语术语标准层），带模块级缓存。"""
    global _GLOSSARY_CACHE
    if _GLOSSARY_CACHE is None:
        p = os.path.join(BASE, "references", "glossary.yaml")
        with open(p, encoding="utf-8") as fh:
            _GLOSSARY_CACHE = yaml.safe_load(fh)
    return _GLOSSARY_CACHE

def glossary_block(lang="en"):
    """Render a compact terminology appendix in the requested language.

    en -> English terms with the internal machine key in parentheses
    zh -> Chinese terms with the internal machine key in parentheses
    """
    g = load_glossary() or {}
    en = (lang == "en")
    joiner = ", " if en else "、"
    def term(v, key):
        if not isinstance(v, dict):
            return "%s(%s)" % (v if en else v, key)
        name = (v.get("en") or v.get("zh") or "?") if en else (v.get("zh") or v.get("en") or "?")
        return "%s(%s)" % (name, key)
    lines = []
    depts = g.get("departments", {})
    if depts:
        lines.append(("- Departments (%d): " if en else "- 部门（%d）：") % len(depts)
                     + joiner.join(term(v, k) for k, v in depts.items()))
    srcs = g.get("sources", {})
    if srcs:
        parts = []
        for k, v in srcs.items():
            parts.append("%s=%s" % (k, v if isinstance(v, str) else (v.get("en") or v.get("zh", ""))))
        lines.append(("- Action source codes: " if en else "- 动作来源代号：") + joiner.join(parts))
    ents = g.get("entities", {})
    if ents:
        if en:
            ent_txt = ", ".join(str(k) for k in ents.keys())
        else:
            ent_txt = joiner.join(term(v, k) for k, v in ents.items())
        lines.append(("- Semantic entities (%d): " if en else "- 语义实体（%d）：") % len(ents) + ent_txt)
    packs = g.get("industry_packs", {})
    if packs:
        lines.append(("- Industry packs (%d): " if en else "- 行业包（%d）：") % len(packs)
                     + joiner.join(term(v, k) for k, v in packs.items()))
    cc = g.get("core_concepts", {})
    if cc:
        c = joiner.join(term(v, v.get("en", k)) for k, v in cc.items() if isinstance(v, dict))
        if c:
            lines.append(("- Core concepts: " if en else "- 核心概念：") + c)
    if not lines:
        return ""
    head = ("[Terminology standard layer] Use these English terms consistently; the identifier in "
            "parentheses is the internal machine key - do not show it to the user."
            if en else
            "【术语标准层·中英对照】（输出请统一使用中文术语；括号内为系统内部英文标识，"
            "便于你识别规范字段，不要向用户展示英文标识）")
    return head + "\n" + "\n".join(lines)


# ── 厂商联系信息（注入专家 system_prompt，使部门专家也能回答「如何联系微数 AI」）──
_VENDOR_CONTACT_CACHE = None
def contact_block(lang="en"):
    """加载 references/contact.yaml，渲染厂商联系信息。单一信息源，与 SKILL.md 正文一致。
    返回空串表示无联系信息（不应发生）。"""
    global _VENDOR_CONTACT_CACHE
    if _VENDOR_CONTACT_CACHE is None:
        p = os.path.join(BASE, "references", "contact.yaml")
        try:
            with open(p, encoding="utf-8") as fh:
                _VENDOR_CONTACT_CACHE = yaml.safe_load(fh) or {}
        except FileNotFoundError:
            _VENDOR_CONTACT_CACHE = {}
    c = _VENDOR_CONTACT_CACHE
    if not c:
        return ""
    website = c.get("official_website", "")
    email = c.get("contact_email", "")
    phone = c.get("contact_phone", "")
    if not (website or email or phone):
        return ""
    en = (lang == "en")
    vendor = c.get("short_name_en") if en else c.get("short_name")
    vendor = vendor or c.get("short_name") or "Weishu AI"
    if en:
        lines = ["[Vendor contact] Produced by %s. For technical support or enterprise deployment, reach out through the channels below:" % vendor]
    else:
        lines = ["【厂商联系】（本产品由%s出品，如需技术支持/企业级部署请通过以下渠道联系）" % vendor]
    if website:
        lines.append(("- Official website: " if en else "- 官方网址：") + website)
    if email:
        lines.append(("- Contact email: " if en else "- 联系邮箱：") + email)
    if phone:
        lines.append(("- Contact phone: " if en else "- 联系电话：") + phone)
    return "\n".join(lines)

def compose_system_prompt(d, persona, flavor, team, prof, op, cul, ctx, lang="en"):
    """把六层拼成最终 system_prompt。占位符来自 D/E/F，基础部门人设(A)只写一次。"""
    name = d["name"]
    role = _fill(persona.get("role", d["expertise"]), op, cul)
    resp_lines = persona.get("responsibilities", [])
    resp = "\n".join(f"- {x}" for x in resp_lines) or "- （见职责说明）"
    style = _fill(persona.get("working_style", ""), op, cul)
    boundaries = _fill(persona.get("boundaries", ""), op, cul)
    report_style = _fill(persona.get("report_style", "结论先行，附依据"), op, cul)

    owner_name = op.get("name", "老板")
    owner_title = op.get("title", "负责人")
    owner_addr = op.get("address_as", owner_name)
    owner_decision = op.get("decision_style", "商议型")
    owner_risk = op.get("risk_appetite", "平衡")
    owner_comm = op.get("comm_style", "口语化、简洁")
    owner_auth = op.get("auth_boundary", "关键操作须经老板确认")
    owner_taboo = op.get("taboo", "")
    culture_voice = cul.get("voice", "专业、务实")
    culture_taboo = cul.get("taboo_topics", "")

    ctx_stage = ctx.get("stage", "成长早期")
    ctx_products = ctx.get("products", "核心业务")
    ctx_customers = ctx.get("customers", "待定")
    company = prof.get("company") or ctx.get("company", "")
    region = prof.get("region", "")
    industry = prof.get("industry", "")

    flavor_text = flavor.get(name) or flavor.get("default", "（本行业包未定义额外红线）")

    # 边界 + 禁忌拼接（清理多余标点）
    taboo_line = ""
    if owner_taboo:
        taboo_line += f"禁忌：{owner_taboo}。"
    if culture_taboo:
        taboo_line += f"品牌禁忌话题：{culture_taboo}。"
    boundaries_final = boundaries.rstrip("。") + ("；" + taboo_line if taboo_line else "")

    en = (lang == "en")
    if en:
        T = {
            "intro": "You are the {name} expert of \u201c{team}\u201d.",
            "role": "[Role] ", "resp": "[Responsibilities]",
            "style": "[Working style] ",
            "decision": "- Follow the owner ({owner_addr}) decision style: {owner_decision}; risk appetite: {owner_risk}.",
            "comm": "- Communication and output tone: {owner_comm}; brand voice: {culture_voice}.",
            "redline": "[Industry red lines] ", "boundary": "[Boundaries] ",
            "report": "Report to {owner_name} ({owner_title}); {owner_auth}; reporting format: {report_style}",
            "bg": "[Company background] {company} ({region} / {industry}), stage: {ctx_stage}; core business: {ctx_products}; customers: {ctx_customers}.",
        }
    else:
        T = {
            "intro": "\u4f60\u662f\u300c{team}\u300d\u65d7\u4e0b\u7684{name}\u4e13\u5bb6\u3002",
            "role": "\u3010\u89d2\u8272\u3011", "resp": "\u3010\u804c\u8d23\u3011",
            "style": "\u3010\u5de5\u4f5c\u98ce\u683c\u3011",
            "decision": "- \u51b3\u7b56\u98ce\u683c\u9075\u5faa\u8001\u677f\uff08{owner_addr}\uff09\u7684\u504f\u597d\uff1a{owner_decision}\uff1b\u98ce\u9669\u504f\u597d\uff1a{owner_risk}\u3002",
            "comm": "- \u6c9f\u901a\u4e0e\u8f93\u51fa\u8154\u8c03\uff1a{owner_comm}\uff1b\u54c1\u724c\u8bed\u6c14\uff1a{culture_voice}\u3002",
            "redline": "\u3010\u884c\u4e1a\u7ea2\u7ebf\u3011", "boundary": "\u3010\u8fb9\u754c\u3011",
            "report": "\u3010\u6c47\u62a5\u3011\u5411 {owner_name}\uff08{owner_title}\uff09\u6c47\u62a5\uff1b{owner_auth}\uff1b\u6c47\u62a5\u53e3\u5f84\uff1a{report_style}",
            "bg": "\u3010\u516c\u53f8\u80cc\u666f\u3011{company}\uff08{region}\u00b7{industry}\uff09\uff0c\u5f53\u524d\u9636\u6bb5\uff1a{ctx_stage}\uff1b\u6838\u5fc3\u4e1a\u52a1\uff1a{ctx_products}\uff1b\u5ba2\u6237\uff1a{ctx_customers}\u3002",
        }
    sep = "; " if en else "；"
    taboo_line = ""
    if owner_taboo:
        taboo_line += ("Taboo: " if en else "禁忌：") + owner_taboo + ("." if en else "。")
    if culture_taboo:
        taboo_line += ("Brand taboo topics: " if en else "品牌禁忌话题：") + culture_taboo + ("." if en else "。")
    boundaries_final = boundaries.rstrip("。.") + (sep + taboo_line if taboo_line else "")

    head = T["intro"].format(team=team, name=name)
    return "\n".join([
        head,
        T["role"] + role,
        T["resp"],
        resp,
        T["style"] + style,
        T["decision"].format(owner_addr=owner_addr, owner_decision=owner_decision, owner_risk=owner_risk),
        T["comm"].format(owner_comm=owner_comm, culture_voice=culture_voice),
        T["redline"] + flavor_text,
        T["boundary"] + boundaries_final,
        T["report"].format(owner_name=owner_name, owner_title=owner_title,
                           owner_auth=owner_auth, report_style=report_style),
        T["bg"].format(company=company, region=region, industry=industry,
                       ctx_stage=ctx_stage, ctx_products=ctx_products, ctx_customers=ctx_customers),
        glossary_block(lang),
        contact_block(lang),
    ])


# ── 第3步：构建专家团清单（带入 action_specs 真实能力 + 六层人设）──────────────
def build_experts(pack_id, departments=None, template_path=None, instance=None, lang="en"):
    tpl = load_template(template_path, lang)
    all_depts = {d["code"]: d for d in tpl["departments"]}
    dept_actions = load_department_actions(lang)
    specs = load_action_specs(lang)
    packs = load_packs(lang)
    pack = packs.get(pack_id, {})
    flavor = pack.get("flavor", {}) or {}

    prof = (instance or {}).get("profile", {}) if instance else {}
    short = prof.get("short_name", "")
    team = team_display_name(short, lang) if short else (TEAM_SUFFIX_EN if lang == "en" else TEAM_SUFFIX)
    op = prof.get("owner_profile", {}) or {}
    cul = prof.get("culture", {}) or {}
    ctx = prof.get("context", {}) or {}

    # 合并模板 + 用户私有覆盖（改名/性别/增删）；显式传 departments 时优先用其筛选
    if departments:
        resolved = [dict(all_depts[c]) for c in departments if c in all_depts]
    else:
        resolved = resolve_departments(instance or {}, template_path, lang)
    experts = []
    for d in resolved:
        code = d["code"]
        # 该部门动作 → 从 action_specs 取真实描述，作为专家能力清单
        caps = []
        for slug in dept_actions.get(code, []):
            sp = specs.get(slug)
            if sp:
                caps.append({"action": slug, "name": sp.get("name", slug),
                             "desc": (sp.get("desc") or "")[:80]})
        persona = d.get("persona", {})
        sys_prompt = compose_system_prompt(d, persona, flavor, team, prof, op, cul, ctx, lang)
        experts.append({
            "name": tpl["generation"]["naming"].format(dept_name=d["name"]),
            "code": code,
            "role": tpl["generation"]["per_department_role"],
            "expertise": d["expertise"],
            "tools_ref": d["tools_ref"],
            "gender": d.get("gender", "male"),   # 供头像选择（不影响能力）
            "report_to": tpl["generation"]["report_to"],
            "team": team,
            "persona": persona,
            "system_prompt": sys_prompt,
            "capabilities": caps,   # 该部门真实动作能力（对照资料库融合）
        })
    return experts


# ── CLI 演示 ───────────────────────────────────────────────────────
def _demo(lang="en"):
    print("=== Ontology Agent guided instantiation demo (six-layer persona model) ===\n")
    text = ("I run a one person company providing AI technology services in Tianjin"
            if lang == "en" else "\u6211\u5f00\u4e86\u4e00\u5bb6\u4e00\u4eba\u516c\u53f8\uff0c\u5728\u5929\u6d25\u505a AI \u6280\u672f\u670d\u52a1")
    pid, score, reason = match_pack(text, lang=lang)
    print(f"[Step 1] Company description: {text}")
    print(f"          Matched pack: {pid} (score={score}) - {reason}\n")

    depts = [d["code"] for d in yaml.safe_load(open(tpl_path(lang), encoding="utf-8"))["departments"]]

    if lang == "en":
        # seed profile - English edition
        seeds = {
            "short_name": "Weishu",
            "company": "Tianjin Weishu Artificial Intelligence Technology Co., Ltd.",
            "enterprise_type": "one person company",
            "legal_form": "single-member limited liability company",
            "region": "Heping District, Tianjin",
            "industry": "AI technology services",
            "scale": "1 (legal representative)",
            "credit_code": "91120101MA82QPB89J",
            "departments": depts,
            "workflow": ["order intake", "delivery", "invoicing", "bookkeeping", "tax filing", "review"],
            "owner_profile": {
                "name": "Li Shunran", "title": "Founder and sole shareholder", "address_as": "Shunran",
                "decision_style": "deliberative (data-driven)", "risk_appetite": "conservative (compliance first)",
                "comm_style": "concise, plain English, no charts",
                "auth_boundary": "tax filing / invoicing / contract signing require owner reconfirmation",
                "background": "technology / AI", "value_priority": "compliance and growth in balance",
                "availability": "available during business hours",
                "taboo": "never disclose unpublished roadmap or credentials",
                "language": "English",
            },
            "culture": {
                "mission": "Use AI to help one-person companies run ontology-native and stay compliant at low cost",
                "voice": "professional, pragmatic, no hype", "taboo_topics": "no political or sensitive topics",
            },
            "context": {
                "stage": "just founded (2026-07-08)", "products": "Memory Pen Sprite, FindIt, Ontology Agent",
                "customers": "ToB (enterprises/developers) + potential OPC clients",
                "quarterly_goal": "ship the reference implementation + policy monitoring",
                "tool_stack": "DingTalk / WeCom / Feishu to be connected",
            },
        }
    else:
        # seed profile - Chinese original
        seeds = {
            "short_name": "\u5fae\u6570",
            "company": "\u5929\u6d25\u5e02\u5fae\u6570\u4eba\u5de5\u667a\u80fd\u79d1\u6280\u6709\u9650\u8d23\u4efb\u516c\u53f8",
            "enterprise_type": "\u4e00\u4eba\u516c\u53f8",
            "legal_form": "\u4e00\u4eba\u6709\u9650\u8d23\u4efb\u516c\u53f8",
            "region": "\u5929\u6d25\u5e02\u548c\u5e73\u533a",
            "industry": "\u4eba\u5de5\u667a\u80fd\u6280\u672f\u670d\u52a1",
            "scale": "1\u4eba\uff08\u6cd5\u4eba\uff09",
            "credit_code": "91120101MA82QPB89J",
            "departments": depts,
            "workflow": ["\u63a5\u5355", "\u4ea4\u4ed8", "\u5f00\u7968", "\u8bb0\u8d26", "\u62a5\u7a0e", "\u590d\u76d8"],
            "owner_profile": {
                "name": "\u674e\u987a\u7136", "title": "\u521b\u59cb\u4eba\u517c\u552f\u4e00\u80a1\u4e1c",
                "address_as": "\u987a\u7136",
                "decision_style": "\u5546\u8bae\u578b\uff08\u504f\u6570\u636e\u652f\u6491\uff09",
                "risk_appetite": "\u4fdd\u5b88\uff08\u5408\u89c4\u4f18\u5148\uff09",
                "comm_style": "\u53e3\u8bed\u5316\u3001\u7b80\u6d01\u3001\u7eaf\u4e2d\u6587\u3001\u4e0d\u8981\u6e32\u67d3\u56fe",
                "auth_boundary": "\u62a5\u7a0e/\u5f00\u7968/\u7b7e\u7ea6\u7b49\u5173\u952e\u64cd\u4f5c\u987b\u672c\u4eba\u4e8c\u6b21\u786e\u8ba4",
                "background": "\u6280\u672f/AI", "value_priority": "\u5408\u89c4\u4e0e\u589e\u957f\u5e76\u91cd",
                "availability": "\u5de5\u4f5c\u65f6\u6bb5\u53ef\u6279",
                "taboo": "\u4e0d\u900f\u9732\u672a\u516c\u5f00\u7684\u4ea7\u54c1\u8def\u7ebf\u4e0e\u51ed\u8bc1",
                "language": "\u4e2d\u6587",
            },
            "culture": {
                "mission": "\u7528 AI \u5e2e\u4e00\u4eba\u516c\u53f8\u628a\u516c\u53f8\u672c\u4f53\u8bba\u5316\u3001\u4f4e\u6210\u672c\u5408\u89c4\u8fd0\u8425",
                "voice": "\u4e13\u4e1a\u3001\u52a1\u5b9e\u3001\u4e0d\u6d6e\u5938",
                "taboo_topics": "\u4e0d\u6d89\u53ca\u653f\u6cbb\u4e0e\u654f\u611f\u8bdd\u9898",
            },
            "context": {
                "stage": "\u521a\u6210\u7acb\uff082026-07-08\uff09",
                "products": "\u8bb0\u5fc6\u7b14\u7cbe\u7075\u3001\u627e\u4e1c\u897f\u3001\u672c\u4f53\u8bba\u667a\u80fd\u4f53",
                "customers": "ToB\uff08\u4f01\u4e1a/\u5f00\u53d1\u8005\uff09+ \u6f5c\u5728 OPC \u5ba2\u6237",
                "quarterly_goal": "\u8dd1\u901a\u53c2\u8003\u5b9e\u73b0+\u653f\u7b56\u5de1\u68c0",
                "tool_stack": "\u5f85\u63a5\u5165\u9489\u9489/\u4f01\u5fae/\u98de\u4e66",
            },
        }
    profile = collect_profile(seeds)
    path = generate_instance(pid, profile, out_path=INSTANCE_PATH, lang=lang)
    instance = yaml.safe_load(open(path, encoding="utf-8"))
    print(f"[第2~4步] 已生成实例: {path}")
    print(f"          团队包名: {instance['meta']['team_name']}  (slug: {instance['meta']['team_slug']})\n")

    experts = build_experts(pid, instance=instance, lang=lang)
    total_caps = sum(len(e["capabilities"]) for e in experts)
    print(f"[第3步] 已生成 {len(experts)} 位专家，合计 {total_caps} 项动作能力:")
    for e in experts:
        print(f"  - {e['name']} （{e['code']}，团队: {e['team']}，汇报给 {e['report_to']}，能力 {len(e['capabilities'])} 项）")
    print("\n=== 示例：财税专家 拼装后 system_prompt（含 D/E/F 注入）===")
    fin = next((e for e in experts if e["code"] == "finance"), None)
    if fin:
        print(fin["system_prompt"])


# ── CLI ──────────────────────────────────────────────────────────
def _cmd_customize():
    import argparse
    ap = argparse.ArgumentParser(description="本体论智能体 · 实例化与部门定制")
    ap.add_argument("--demo", action="store_true", help="跑引导式实例化演示（六层人设）")
    ap.add_argument("--catalog", action="store_true", help="列出 24 部门库（core/可选 + 性别默认 + 适用场景）")
    ap.add_argument("--slug", help="公司简称 slug（指向 company-data/<slug>/instance.yaml）")
    ap.add_argument("--list-depts", action="store_true", help="列出某公司当前生效的部门清单")
    ap.add_argument("--rename", nargs=2, metavar=("CODE", "NAME"), help="部门改名（私有覆盖）")
    ap.add_argument("--gender", nargs=2, metavar=("CODE", "GENDER"), help="指定部门性别 male/female（仅头像/语感）")
    ap.add_argument("--disable", metavar="CODE", help="停用某部门")
    ap.add_argument("--enable", metavar="CODE", help="启用某部门")
    ap.add_argument("--add-dept", metavar="CODE", help="新增私有部门（配合 --name/--gender/--expertise）")
    ap.add_argument("--name", help="--add-dept 的显示名")
    ap.add_argument("--expertise", help="--add-dept 的职能描述")
    ap.add_argument("--persona-text", help="--add-dept 的自定义人设（一句角色描述即可）")
    ap.add_argument("--remove-dept", metavar="CODE", help="移除某私有部门")
    ap.add_argument("--lang", choices=["en", "zh"], default="en", help="en=English packs (default) / zh=Chinese original packs")
    args = ap.parse_args()

    if args.catalog:
        print("=== 24 部门库 ===")
        for d in list_catalog():
            tag = "核心" if d["core"] else "可选"
            print(f"  [{tag}] {d['code']:<16} {d['name']:<8} 默认性别:{d['gender_default']:<6} | {d['when_to_include']}")
        return
    if args.demo:
        _demo(lang=args.lang)
        return
    if not args.slug:
        ap.error("定制类操作需要 --slug <公司简称>")

    if args.list_depts:
        path = default_instance_path(args.slug)
        inst = load_instance(path) if os.path.isfile(path) else None
        if not inst:
            print(f"未找到实例: {path}")
            return
        for d in resolve_departments(inst):
            print(f"  - {d['code']:<16} {d['name']:<8} 性别:{d.get('gender','male')} "
                  f"{'[私有]' if d.get('custom') else ''}")
        return
    if args.rename:
        customize_instance(args.slug, "rename", code=args.rename[0], name=args.rename[1])
    elif args.gender:
        g = args.gender[1].lower()
        if g not in ("male", "female"):
            ap.error("--gender 只能是 male 或 female")
        customize_instance(args.slug, "gender", code=args.gender[0], gender=g)
    elif args.disable:
        customize_instance(args.slug, "disable", code=args.disable)
    elif args.enable:
        customize_instance(args.slug, "enable", code=args.enable)
    elif args.add_dept:
        if not args.name:
            ap.error("--add-dept 需要 --name")
        custom = {
            "code": args.add_dept,
            "name": args.name,
            "gender": (args.gender[1].lower() if args.gender else "male"),
            "expertise": args.expertise or "",
            "tools_ref": "",
            "persona": {"role": args.persona_text or args.expertise or args.name,
                        "responsibilities": [], "working_style": "",
                        "boundaries": "按 owner 授权与合规红线执行",
                        "report_style": "结论先行"},
        }
        customize_instance(args.slug, "add", custom=custom)
    elif args.remove_dept:
        customize_instance(args.slug, "remove", code=args.remove_dept)
    else:
        ap.print_help()


if __name__ == "__main__":
    _cmd_customize()
