# -*- coding: utf-8 -*-
"""未成年人保护合规护栏规则库。

覆盖《中华人民共和国未成年人保护法》（2021年6月1日施行）"网络保护"专章、
《未成年人网络保护条例》（2024年1月1日施行）、国家新闻出版署《关于防止未成年人
沉迷网络游戏的通知》（2019年11月1日施行，2021年8月进一步收紧至每周最多3小时）
的六大类高频违规表述。规则为声明式词表，纯本地、零网络。
"""

CATEGORIES = {
    "no_realname": {
        "label": "未落实实名认证",
        "risk": "high",
        "desc": "网络产品和服务未要求用户实名注册认证，或允许游客/匿名模式无限制使用。",
    },
    "no_minor_mode": {
        "label": "未提供未成年人模式/青少年模式",
        "risk": "high",
        "desc": "未区分成年与未成年用户，未提供未成年人专属模式或适龄内容管理。",
    },
    "no_antaddiction": {
        "label": "游戏未落实防沉迷/无时长限制",
        "risk": "high",
        "desc": "网络游戏未接入防沉迷系统，或允许未成年人无时段、无时长限制游玩。",
    },
    "induce_spend": {
        "label": "诱导未成年人消费/打赏",
        "risk": "high",
        "desc": "允许未成年人无限制充值、打赏，或以抽奖、返利等方式诱导未成年人消费。",
    },
    "child_info_no_consent": {
        "label": "收集儿童个人信息未取得监护人同意",
        "risk": "high",
        "desc": "处理不满十四周岁未成年人个人信息，未取得监护人单独同意或未告知监护人。",
    },
    "harmful_content": {
        "label": "向未成年人推送不良信息",
        "risk": "medium",
        "desc": "未对未成年人过滤暴力、色情、赌博、不良价值观等信息，或未建立网络欺凌处置机制。",
    },
}

TERMS = [
    # 1. 未落实实名认证
    {"term": "无需实名认证", "category": "no_realname", "risk": "high",
     "suggestion": "应落实用户实名注册认证；网络游戏、直播、社交等须接入实名系统，禁止游客模式无限制使用。",
     "basis": "《未成年人保护法》网络保护专章；《未成年人网络保护条例》第二十二条（真实身份信息注册）。"},
    {"term": "不用实名", "category": "no_realname", "risk": "high",
     "suggestion": "应要求用户提供真实身份信息注册，不得允许匿名或虚假身份无限制使用。",
     "basis": "《未成年人网络保护条例》第二十二条。"},
    {"term": "游客模式无限制", "category": "no_realname", "risk": "high",
     "suggestion": "游客/体验模式应设置使用时限与功能限制，不得无限制使用全部服务。",
     "basis": "《未成年人网络保护条例》第二十二条及防沉迷相关规定。"},
    {"term": "no age verification", "category": "no_realname", "risk": "high",
     "suggestion": "Should require age/identity verification before providing services to minors.",
     "basis": "Minor Protection Law / Minor Network Protection Regulation: real-name registration."},

    # 2. 未提供未成年人模式
    {"term": "无青少年模式", "category": "no_minor_mode", "risk": "high",
     "suggestion": "应提供未成年人模式（青少年模式），开启后限制使用时长、消费、社交与内容推荐。",
     "basis": "《未成年人网络保护条例》第四十九条（未成年人模式）。"},
    {"term": "无未成年人模式", "category": "no_minor_mode", "risk": "high",
     "suggestion": "应提供未成年人专属模式，落实适龄内容与使用时长管理。",
     "basis": "《未成年人网络保护条例》第四十九条。"},
    {"term": "不区分成年未成年", "category": "no_minor_mode", "risk": "medium",
     "suggestion": "应对未成年用户与普通用户作区分，提供差异化的内容、时长与功能策略。",
     "basis": "《未成年人网络保护条例》未成年人模式要求。"},
    {"term": "no minor mode", "category": "no_minor_mode", "risk": "high",
     "suggestion": "Provide a minor/teen mode with time limits and content filtering.",
     "basis": "Minor Network Protection Regulation Art.49."},

    # 3. 游戏防沉迷
    {"term": "无游戏时长限制", "category": "no_antaddiction", "risk": "high",
     "suggestion": "网络游戏应接入防沉迷系统，限制未成年人游戏时长（现行规定每周累计不超3小时，仅周五六日及法定节假日20-21时）。",
     "basis": "《关于防止未成年人沉迷网络游戏的通知》（2019）及2021年补充通知。"},
    {"term": "未成年人可全天游戏", "category": "no_antaddiction", "risk": "high",
     "suggestion": "不得允许未成年人无时段限制游戏；应严格执行防沉迷时段与时长规定。",
     "basis": "国家新闻出版署防沉迷通知（2021补充）。"},
    {"term": "不接入防沉迷", "category": "no_antaddiction", "risk": "high",
     "suggestion": "网络游戏运营企业必须接入国家防沉迷实名验证系统，不得规避。",
     "basis": "《未成年人保护法》第七十五条；《防沉迷通知》。"},
    {"term": "no playtime limit", "category": "no_antaddiction", "risk": "high",
     "suggestion": "Online games must enforce anti-addiction playtime limits for minors.",
     "basis": "NPPA anti-addiction notice (2021)."},

    # 4. 诱导消费/打赏
    {"term": "未成年人可无限充值", "category": "induce_spend", "risk": "high",
     "suggestion": "应对未成年人充值设置限额与频次限制，并需监护人同意；不得无限制充值。",
     "basis": "《未成年人网络保护条例》第四十五条（网络游戏付费服务）；《未成年人保护法》第七十四条。"},
    {"term": "诱导未成年人打赏", "category": "induce_spend", "risk": "high",
     "suggestion": "直播、社交平台不得诱导未成年人打赏、消费；应关闭或严格限制未成年人打赏功能。",
     "basis": "《未成年人网络保护条例》第四十五条；网信办直播打赏规范。"},
    {"term": "诱导未成年人消费", "category": "induce_spend", "risk": "high",
     "suggestion": "不得以抽奖、返利、排行榜等方式诱导未成年人非理性消费。",
     "basis": "《未成年人网络保护条例》第四十五条。"},
    {"term": "no spending limit for minors", "category": "induce_spend", "risk": "high",
     "suggestion": "Impose spending limits and parental consent for minor purchases.",
     "basis": "Minor Protection Law Art.74; Minor Network Protection Regulation Art.45."},

    # 5. 儿童信息监护人同意
    {"term": "收集儿童信息无需家长同意", "category": "child_info_no_consent", "risk": "high",
     "suggestion": "处理不满十四周岁未成年人个人信息，应取得监护人单独同意，并制定专门规则告知监护人。",
     "basis": "《个人信息保护法》第三十一条（不满十四周岁需监护人同意）；《未成年人网络保护条例》第二十一条。"},
    {"term": "儿童信息无需监护人同意", "category": "child_info_no_consent", "risk": "high",
     "suggestion": "收集未成年人个人信息前应取得监护人同意，不得默认勾选或以隐蔽方式收集。",
     "basis": "《个人信息保护法》第三十一条；《未成年人网络保护条例》第二十一条。"},
    {"term": "默认收集未成年人信息", "category": "child_info_no_consent", "risk": "high",
     "suggestion": "不得默认收集未成年人个人信息；应单独征得监护人同意并告知收集目的与范围。",
     "basis": "《个人信息保护法》第三十一条。"},
    {"term": "no parental consent for kids", "category": "child_info_no_consent", "risk": "high",
     "suggestion": "Obtain verifiable parental consent before processing children's personal info.",
     "basis": "PIPL Art.31 (under-14 requires guardian consent)."},

        {"term": "儿童信息无需家长同意", "category": "child_info_no_consent", "risk": "high",
     "suggestion": "收集未成年人个人信息前应取得监护人（家长）同意，不得默认勾选或以隐蔽方式收集。",
     "basis": "《个人信息保护法》第三十一条；《未成年人网络保护条例》第二十一条。"},

# 6. 不良信息/网络欺凌
    {"term": "向未成年人推送不良内容", "category": "harmful_content", "risk": "medium",
     "suggestion": "应对未成年人过滤暴力、色情、赌博、迷信及不良价值观信息，建立专属内容池。",
     "basis": "《未成年人网络保护条例》第二十四条（信息内容管理）；《未成年人保护法》网络保护。"},
    {"term": "无不良信息过滤", "category": "harmful_content", "risk": "medium",
     "suggestion": "应建立针对未成年人的信息内容审核与过滤机制，不得向其展示不适宜内容。",
     "basis": "《未成年人网络保护条例》第二十四条。"},
    {"term": "未处置网络欺凌", "category": "harmful_content", "risk": "medium",
     "suggestion": "应建立网络欺凌、骚扰的识别与处置机制，并为未成年人提供便捷举报渠道。",
     "basis": "《未成年人网络保护条例》网络欺凌处置条款。"},
    {"term": "no content filter for minors", "category": "harmful_content", "risk": "medium",
     "suggestion": "Filter harmful content and provide anti-bullying reporting for minors.",
     "basis": "Minor Network Protection Regulation Art.24."},
]

CATEGORY_LABEL = {k: v["label"] for k, v in CATEGORIES.items()}
