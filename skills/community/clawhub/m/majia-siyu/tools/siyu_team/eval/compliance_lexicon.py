"""合规与静态反模式规则的单一真源。

本模块只定义“匹配什么”；命中在客户文案、内部报告、知识原子或引证中
是否硬卡，由 :mod:`siyu_team.eval.static` 按 ``ScanMode`` 判定。插件 lint
可以继续导入 ``PATTERNS``、``INDUCE_PATTERN`` 和 ``PRIVACY_PATTERN``。
"""
from __future__ import annotations

from dataclasses import dataclass
import re


# “第一”只在可能构成名次主张时进入候选。操作序号、时间序号、章节与
# 第一方/第一性等普通表达在词法层直接排除，避免让上下文层承担必然误报。
_FIRST_CLAIM = (
    r"第一(?!"
    r"步|周|天|阶段|轮|批|次|版|章|节|条|项|部分|季度|个月|年|"
    r"个|种|位|方|性|时间|原则|原因|问题|目标|指标|任务|动作|"
    r"责任|优先级|现场|屏"
    r")"
)

ABSOLUTE_SUPERLATIVE_PATTERN = re.compile(
    rf"({_FIRST_CLAIM}|最便宜|最好|最佳|最优|最强|最高级|最低价|国家级|"
    r"世界级|史上最|绝无仅有|独一无二|顶级)"
)

GUARANTEE_PATTERN = re.compile(
    r"(100\s*%|百分之百|永久免费|稳赚(?:不赔)?|包赚|零风险|"
    r"保证.{0,5}(?:成功|有效|赚钱|增收|盈利))"
)

RESTRICTED_TOOL_PATTERN = re.compile(r"(外挂|群发软件|虚拟定位|改定位)")
RISK_TERM_PATTERN = re.compile(r"(诱导分享)")

# 兼容旧 COMPLIANCE_RED flag；上下文扫描会把否定、归因、引证等命中
# 降级成可解释的 soft mention，而不会沿用这里的默认 hard。
COMPLIANCE_RED_PATTERN = re.compile(
    rf"({RESTRICTED_TOOL_PATTERN.pattern[1:-1]}|"
    rf"{RISK_TERM_PATTERN.pattern[1:-1]}|"
    rf"{ABSOLUTE_SUPERLATIVE_PATTERN.pattern[1:-1]}|"
    rf"{GUARANTEE_PATTERN.pattern[1:-1]})"
)

ABSOLUTE_CLAIM_PATTERN = re.compile(
    r"(绝对|唯一|独家|首个|领先|极致|王牌|领导品牌)"
)

NO_CALIBRATION_PATTERN = re.compile(
    r"(转化率|复购率|加微率)(?!.{0,30}(分母|UV|加微数|周期|时间窗|=|除以))"
)

NO_METRIC_PATTERN = re.compile(r"(率|人数|GMV|客单|复购|留存|触达)")

# 群发和欢迎语共用的社交裂变门槛。数字同时支持阿拉伯数字和常见中文数字。
_COUNT = r"(?:\d+|[一二两三四五六七八九十百两]+)"
INDUCE_PATTERN = re.compile(
    rf"(转发.{{0,12}}(?:领|送|得|抽|享|免|换|兑换|解锁)|"
    rf"集(?:满|齐|够)?\s*{_COUNT}?\s*个?赞|"
    rf"拉\s*{_COUNT}\s*(?:个|位)?人(?:.{{0,8}}(?:领|送|得|抽|享|免|换|解锁))?|"
    rf"拉够\s*{_COUNT}|"
    r"分享.{0,4}(?:到|给).{0,4}(?:群|好友)|"
    rf"邀请\s*{_COUNT}\s*位?好友|"
    rf"{_COUNT}\s*人成团才)"
)

# 欢迎语中未带授权口径的敏感信息索取信号。
PRIVACY_PATTERN = re.compile(
    r"(留.{0,3}(手机号|电话|微信号)|发.{0,3}(身份证|定位|位置)|"
    r"报.{0,3}(手机号|电话)|"
    r"加我.{0,4}(发|留).{0,4}(定位|手机号|身份证)|银行卡|身份证号|"
    r"(手机号|电话|身份证|定位|微信号).{0,6}"
    r"(发给|给我|留一?下|报一?下|填一?下|提供|登记))"
)


@dataclass(frozen=True)
class LexiconRule:
    """A context-neutral regex rule consumed by the mode-aware scanner."""

    rule: str
    flag: str
    description: str
    severity: float
    default_hard: bool
    pattern: re.Pattern[str] | None
    absence_rule: bool = False


RULES: tuple[LexiconRule, ...] = (
    LexiconRule(
        "restricted_or_absolute_claim",
        "COMPLIANCE_RED",
        "限制工具、虚假保证或绝对化宣传候选",
        0.20,
        True,
        COMPLIANCE_RED_PATTERN,
    ),
    LexiconRule(
        "rate_without_calibration",
        "NO_CALIBRATION",
        "出现转化/复购率但无口径",
        0.15,
        False,
        NO_CALIBRATION_PATTERN,
    ),
    LexiconRule(
        "absolute_advertising_claim",
        "ABSOLUTE_CLAIM",
        "广告绝对化主张候选",
        0.10,
        False,
        ABSOLUTE_CLAIM_PATTERN,
    ),
    LexiconRule(
        "missing_metric",
        "NO_METRIC",
        "全文无可埋点指标",
        0.10,
        False,
        NO_METRIC_PATTERN,
        absence_rule=True,
    ),
    LexiconRule(
        "induced_share_mechanism",
        "INDUCE_SHARE",
        "诱导分享、集赞或拉人解锁机制（企微高风险）",
        0.20,
        True,
        INDUCE_PATTERN,
    ),
    LexiconRule(
        "privacy_collection",
        "PRIVACY_COLLECT",
        "疑似未授权索取手机号、身份证等敏感信息",
        0.15,
        False,
        PRIVACY_PATTERN,
    ),
)


# v1 tuple 接口保留一个小版本，供尚未迁移到 RULES 的脚本使用。
# (flag, 说明, severity, 默认是否硬卡, 正则)
PATTERNS = [
    (
        "COMPLIANCE_RED",
        "限制工具、虚假保证或绝对化宣传候选",
        0.20,
        True,
        COMPLIANCE_RED_PATTERN,
    ),
    (
        "NO_CALIBRATION",
        "出现转化/复购率但无口径",
        0.15,
        False,
        NO_CALIBRATION_PATTERN,
    ),
    (
        "ABSOLUTE_CLAIM",
        "广告绝对化主张候选",
        0.10,
        False,
        ABSOLUTE_CLAIM_PATTERN,
    ),
    ("NO_RESPONSIBLE_PARTY", "SOP 段无责任人", 0.10, False, None),
    (
        "NO_METRIC",
        "全文无可埋点指标",
        0.10,
        False,
        NO_METRIC_PATTERN,
    ),
]
