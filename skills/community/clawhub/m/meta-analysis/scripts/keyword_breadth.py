"""keyword_breadth — 检索关键词「广度」约束（防 Coze 端点 1000+ 页爆炸）。

本模块是 ct- 技能库的统一底座资产，供 ct-registry 等对外检索技能导入使用
（``sys.path`` 注入 ``ct-base/scripts`` 后 ``from keyword_breadth import ...``）。

问题背景
--------
中国 CDE / WHO ICTRP / ChiCTR / ISRCTN / DRKS 等经统一 Coze ``/run`` 端点检索时，
工作流会**尝试完整翻页抓取**。若主关键词过于宽泛（如「肿瘤」「cancer」「治疗」），
结果可能超过 **1000 页**，无法全部抓取，既浪费共享端点资源又拿不到完整数据。

规则（源自 ct-registry 加固需求，沉淀为全库统一约定，见 BASE.md §11.x）
-------------------------------------------------------------------------
1. **多关键词组合检索**：主关键词（用于「首次完整检索」的那个词，例如 CDE
   ``multi_keyword`` 模式里排在第一位的词）**不能选最宽泛的那个**。应把最具体的
   词排到最前作为主词，其余词做交集（intersect）。
2. **只有一个关键词且可能过于宽泛**：直接提醒用户「数量可能太多」，并**要求缩小
   关键词范围**（技能停止检索，等用户给出更具体的词后重跑）。

对外公开检索、且**受 --max 上限约束**的源（如 CT.gov）只给 WARN，不强制中止——
因为这类源不会无脑翻千页。

对外经**共享 Coze 端点、会完整翻页**的源（CDE / WHO / ChiCTR / ISRCTN / DRKS）
命中「单关键词过宽」时**中止检索**，要求用户缩小范围。
"""

from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# 宽泛词词典（umbrella / 大类词，单独作为主词会导致结果爆炸）
# 仅收录「真正泛化」的类别词；具体疾病/药物（肺癌、糖尿病、osimertinib 等）不在此列。
# ---------------------------------------------------------------------------
BROAD_TERMS_EN = {
    "cancer", "cancers", "tumor", "tumour", "tumors", "tumours",
    "neoplasm", "neoplasms", "carcinoma", "therapy", "therapies",
    "treatment", "treatments", "drug", "drugs", "medicine", "medicines",
    "disease", "diseases", "disorder", "disorders", "syndrome", "syndromes",
    "infection", "infections", "inflammation", "pain", "vaccine", "vaccines",
    "chemotherapy", "radiotherapy", "immunotherapy", "screening", "diagnosis",
    "prognosis", "survival", "efficacy", "safety", "metastasis", "metastatic",
    "benign", "malignant", "prevention", "randomized", "randomised", "control",
    "controlled", "observational", "cohort", "registry", "registries",
    "patient", "patients", "adult", "adults", "female", "male", "elderly",
    "infant", "infants", "pediatric", "paediatric", "chronic", "acute",
    "autoimmune", "biomarker", "gene", "genetic", "molecular", "protein",
    "antibody", "clinical", "trial", "trials", "study", "studies",
}

BROAD_TERMS_ZH = {
    "肿瘤", "癌症", "癌", "治疗", "疗法", "药物", "药", "疾病", "病", "症",
    "综合征", "感染", "炎症", "疼痛", "临床", "疫苗", "化疗", "放疗", "免疫",
    "筛查", "诊断", "预后", "生存", "疗效", "安全", "转移", "良性", "恶性",
    "预防", "随机", "对照", "观察", "队列", "注册", "患者", "病人", "成人",
    "女性", "男性", "老年", "婴幼儿", "心脏", "肝", "肺", "脑", "血液",
    "通用", "试验", "研究",
}

# 具体药物特征（命中即视为「具体词」，覆盖宽泛判定）
_DRUG_EN = re.compile(
    r"\d|"                                  # 含数字（如 AZD9291）
    r"(?:mab|nab|inib|nib|ciclib|cept|vir|vir|ane|olol|parib|tinib|"
    r"zumab|umab|limab|mumab|parin|caine|statin|sartan|pril|azine|"
    r"mycin|cycline|oxacin|dipine|idone|axcept|trectinib)$",
    re.I,
)
_DRUG_ZH = re.compile(
    r"单抗|珠单抗|双抗|替尼|他汀|沙坦|普利|地平|洛尔|格列|胰岛素|加宾|"
    r"环素|沙星|唑仑|西泮|巴比妥|胞苷|替尼|布韦|韦|帕尼|非尼|曲塞|他赛|"
    r"紫杉|长春|柔比星|铂|单抗类",
)


def _norm(kw):
    """归一化用于词典匹配：去空白、转小写（CJK 不受影响）。"""
    if not kw:
        return ""
    return re.sub(r"\s+", "", str(kw)).lower().strip()


def looks_like_drug(kw):
    """命中具体药物形态（英文后缀/数字，或中文药物词根）→ 视为具体词。"""
    if not kw:
        return False
    if _DRUG_EN.search(kw):
        return True
    if _DRUG_ZH.search(kw):
        return True
    return False


def is_broad_keyword(kw):
    """判断单个关键词是否「过于宽泛」（不宜单独作为 Coze 端点主词）。

    判定优先级：
      1. 药物形态命中 -> 不宽泛（具体）。
      2. 归一化后命中宽泛词典 -> 宽泛。
      3. 其余（具体疾病名、复合词、药物）→ 不宽泛。
    """
    if not kw:
        return False
    if looks_like_drug(kw):
        return False
    n = _norm(kw)
    if not n:
        return False
    # 中英分别查词典
    if n in BROAD_TERMS_EN:
        return True
    # 中文：整词匹配（避免「肺癌」被「癌」误判）
    if n in BROAD_TERMS_ZH:
        return True
    return False


def specificity_score(kw):
    """具体度评分：越高越「具体」，应优先作为主词。"""
    if not kw:
        return -100
    s = len(kw)  # 字符越长通常越具体
    toks = [t for t in str(kw).split() if t]
    if len(toks) > 1:
        s += 4 * (len(toks) - 1)  # 复合词加分
    if looks_like_drug(kw):
        s += 8  # 药物具体词加权
    if is_broad_keyword(kw):
        s -= 12  # 宽泛词重罚
    return s


def choose_primary_keyword(words):
    """多关键词重排：把最具体的词放到最前（作为主词），其余保持原序做交集。

    稳定排序（具体度相同者保留原相对顺序）。返回新的列表，不改原列表。
    """
    if not words:
        return list(words)
    ranked = sorted(words, key=specificity_score, reverse=True)
    # 稳定化：按 (score, 原索引) 排序，保证同分时原序
    order = sorted(range(len(words)), key=lambda i: (-specificity_score(words[i]), i))
    return [words[i] for i in order]


def plan_coze_keywords(words):
    """为 Coze（完整翻页）端点规划关键词策略。

    参数
    ----
    words : list[str]
        用户给出的关键词（1 个或多个；多关键词即组合检索）。

    返回
    ----
    dict，键：
      - ``ordered`` (list[str]) : 重排后的关键词（具体词在前）。
      - ``primary`` (str)       : 最终主词。
      - ``broad``  (bool)        : 主词是否仍过宽。
      - ``action`` (str)         : ``"proceed"`` / ``"reorder"`` / ``"abort"``。
          - ``proceed`` : 单/多关键词，主词具体，可直接检索。
          - ``reorder`` : 多关键词，已重排（主词由宽泛改为具体），可直接检索。
          - ``abort``   : 主词过宽且无更具体备选（单关键词过宽，或多关键词全宽）
                           -> 调用方应**停止检索、要求用户缩小关键词范围**。
      - ``message`` (str)        : 人类可读说明（用于日志/提示）。
    """
    if not words:
        return {"ordered": [], "primary": "", "broad": False,
                "action": "proceed", "message": "无关键词"}

    if len(words) == 1:
        kw = words[0]
        broad = is_broad_keyword(kw)
        return {
            "ordered": [kw], "primary": kw, "broad": broad,
            "action": "abort" if broad else "proceed",
            "message": (f"单关键词 {kw!r} 过于宽泛, 结果可能超过千页; "
                        f"请缩小关键词范围后再检索。") if broad
                       else f"单关键词 {kw!r} 具体度足够。",
        }

    ordered = choose_primary_keyword(words)
    primary = ordered[0]
    broad = is_broad_keyword(primary)
    if broad:
        return {
            "ordered": ordered, "primary": primary, "broad": True,
            "action": "abort",
            "message": (f"组合关键词 {words} 重排后主词仍为宽泛词 {primary!r}; "
                        f"请提供更具体的组合词（如具体疾病/药物/分期）。"),
        }
    changed = ordered != list(words)
    return {
        "ordered": ordered, "primary": primary, "broad": False,
        "action": "reorder" if changed else "proceed",
        "message": (f"多关键词已重排为主词优先: {ordered}") if changed
                   else f"多关键词主词已具体: {ordered}",
    }


if __name__ == "__main__":
    # 自测：改动后跑 `python keyword_breadth.py` 验证。
    tests = [
        ("cancer", True), ("肿瘤", True), ("治疗", True), ("糖尿病", False),
        ("肺癌", False), ("osimertinib", False), ("Osimertinib", False),
        ("非小细胞肺癌", False), ("lung cancer", False),
    ]
    for kw, exp in tests:
        got = is_broad_keyword(kw)
        print(f"{'OK ' if got == exp else 'XX '} is_broad({kw!r}) = {got} (exp {exp})")
    print("reorder:", choose_primary_keyword(["cancer", "osimertinib", "lung"]))
    print("plan single broad:", plan_coze_keywords(["cancer"])["action"])
    print("plan multi:", plan_coze_keywords(["cancer", "osimertinib"])["action"],
          plan_coze_keywords(["cancer", "osimertinib"])["ordered"])
