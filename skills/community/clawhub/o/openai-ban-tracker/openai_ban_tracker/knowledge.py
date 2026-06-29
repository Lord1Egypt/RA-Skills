"""OpenAI account ban knowledge base — known reasons, risk factors, appeal templates."""

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class RiskLevel(Enum):
    SAFE = ("安全", "green")
    LOW = ("低风险", "yellow")
    MEDIUM = ("中风险", "bright_yellow")
    HIGH = ("高风险", "red")
    CRITICAL = ("极高风险", "bold red")


@dataclass
class BanReason:
    id: str
    title_zh: str
    title_en: str
    description_zh: str
    risk_level: RiskLevel
    common_patterns: List[str] = field(default_factory=list)
    prevention_tips: List[str] = field(default_factory=list)
    appeal_success_rate: str = "未知"


BAN_REASONS: List[BanReason] = [
    BanReason(
        id="shared-account",
        title_zh="共享/合租账号",
        title_en="Shared Account",
        description_zh=(
            "多人共用一个 OpenAI 账号，IP 地址频繁跳变，"
            "触发风控系统。OpenAI 检测到同一账号在短时间内"
            "从不同地区/国家登录时，会判定为账号被盗或违规共享。"
        ),
        risk_level=RiskLevel.CRITICAL,
        common_patterns=[
            "tb/闲鱼购买合租账号",
            "和朋友共用 ChatGPT Plus",
            "频繁切换 VPN 节点导致 IP 变动",
            "美国登录 → 日本登录 → 英国登录（短时间内）",
        ],
        prevention_tips=[
            "使用独享账号，避免合租",
            "固定 VPN/代理节点，减少 IP 跳变",
            "如果必须共享，确保所有用户在同一地区",
        ],
        appeal_success_rate="低（共享违反 ToS，通常不恢复）",
    ),
    BanReason(
        id="third-party-topup",
        title_zh="第三方代充/黑卡",
        title_en="Third-party Top-up / Stolen Card",
        description_zh=(
            "通过淘宝、闲鱼等平台找代充，对方使用盗刷信用卡"
            "支付。OpenAI 发现支付风控异常后封号。"
            "这是近期最高频的封号原因，波及面极广。"
        ),
        risk_level=RiskLevel.CRITICAL,
        common_patterns=[
            "淘宝/闲鱼代充 ChatGPT Plus / API 额度",
            "尼区/土区廉价礼品卡（iTunes 等）",
            "第三方网站代付",
            "价格明显低于官方（如 ¥20 买 $20 额度）",
        ],
        prevention_tips=[
            "始终使用自己的信用卡/借记卡直接支付",
            "通过 OpenAI 官方支持的支付渠道充值",
            "如果无法直接支付，使用正规虚拟卡（如 Depay 等）",
        ],
        appeal_success_rate="极低（关联到盗刷卡的账号通常不会恢复）",
    ),
    BanReason(
        id="vpn-ip-abuse",
        title_zh="代理/IP 被污染",
        title_en="Abused VPN/Proxy IP",
        description_zh=(
            "使用的 VPN/代理 IP 曾被大量 OpenAI 用户使用，"
            "IP 段已被 OpenAI 标记为垃圾流量源。"
            "常见于机场/公用代理节点。"
        ),
        risk_level=RiskLevel.HIGH,
        common_patterns=[
            "使用廉价 VPN 服务商",
            "机场共享节点",
            "IP 段与大量被封账号重合",
            "使用 Tor 或公开代理",
        ],
        prevention_tips=[
            "使用独立的、干净的住宅 IP",
            "避免公共 VPN 节点",
            "考虑使用独享 VPS + 自建代理",
        ],
        appeal_success_rate="中等（证明自己是正常用户后可恢复）",
    ),
    BanReason(
        id="region-mismatch",
        title_zh="地区信息不匹配",
        title_en="Region Mismatch",
        description_zh=(
            "账号注册时填写的地区、支付卡的发卡地区、"
            "实际访问 IP 所在地区三者不一致，"
            "触发 OpenAI 的风控规则。"
        ),
        risk_level=RiskLevel.HIGH,
        common_patterns=[
            "使用美国地址注册，但用中国信用卡支付",
            "支付卡地区和 IP 地区不一致",
            "频繁修改 billing 地址",
        ],
        prevention_tips=[
            "保持注册地区、支付地区、访问 IP 地区一致",
            "使用与支付卡同地区的代理 IP",
            "不要频繁修改 billing 地址",
        ],
        appeal_success_rate="中等（提供身份验证后可解封）",
    ),
    BanReason(
        id="api-abuse",
        title_zh="API 滥用 / 违规使用",
        title_en="API Abuse",
        description_zh=(
            "API 调用频率过高、用于违规场景（生成成人内容、"
            "欺诈等）、或绕开安全限制。OpenAI 自动监控触发封禁。"
        ),
        risk_level=RiskLevel.HIGH,
        common_patterns=[
            "短时间内大量 API 调用",
            "使用 API 生成违禁内容",
            "绕过 OpenAI 内容安全策略",
            "未授权的自动化批量操作",
        ],
        prevention_tips=[
            "遵守 OpenAI 使用政策和使用条款",
            "实现合理的限流和重试逻辑",
            "启用内容安全过滤",
        ],
        appeal_success_rate="低（严重违规不恢复，轻度可解封）",
    ),
    BanReason(
        id="payment-chargeback",
        title_zh="支付拒付 / 退单",
        title_en="Payment Chargeback",
        description_zh=(
            "银行卡发起 chargeback（拒付/争议交易），"
            "OpenAI 方收到退单通知后立即封号。"
            "即使是误操作，恢复也比较困难。"
        ),
        risk_level=RiskLevel.CRITICAL,
        common_patterns=[
            "银行自动标记交易为可疑",
            "用户主动发起退款争议",
            "用他人信用卡后被持卡人拒付",
        ],
        prevention_tips=[
            "不要发起 chargeback，先联系 OpenAI 客服",
            "使用自己的信用卡支付",
            "确认银行不会误判 OpenAI 交易",
        ],
        appeal_success_rate="低（取消争议后可恢复，但流程漫长）",
    ),
    BanReason(
        id="suspicious-login",
        title_zh="可疑登录行为",
        title_en="Suspicious Login Activity",
        description_zh=(
            "登录模式异常：短时间内多次登录失败、"
            "从异常地区登录、使用已知泄露的密码等。"
            "OpenAI 会锁死账号以防止被盗。"
        ),
        risk_level=RiskLevel.MEDIUM,
        common_patterns=[
            "暴力破解式登录失败",
            "从从未登录过的国家登录",
            "使用公开泄露的密码",
            "短时间内多次密码重置",
        ],
        prevention_tips=[
            "开启双因素认证 (2FA)",
            "使用强密码 + 密码管理器",
            "检查 haveibeenpwned.com 确认密码没有泄露",
        ],
        appeal_success_rate="高（提供身份验证后通常可快速恢复）",
    ),
    BanReason(
        id="multiple-accounts",
        title_zh="批量注册 / 多账号",
        title_en="Mass Registration / Multi-account",
        description_zh=(
            "同一设备/IP/支付卡注册多个免费账号，"
            "被判定为批量注册滥用免费额度。"
            "单人多号也可能触发此规则。"
        ),
        risk_level=RiskLevel.HIGH,
        common_patterns=[
            "用同一张卡注册多个账号",
            "同一 IP 注册大量免费账号",
            "使用临时邮箱注册",
            "用小号薅免费 API 额度",
        ],
        prevention_tips=[
            "一人一号，不要批量注册",
            "不要使用临时邮箱",
            "使用真实手机号验证",
        ],
        appeal_success_rate="低（批量注册行为明确违反 ToS）",
    ),
]


@dataclass
class AppealTemplate:
    lang: str
    subject: str
    body: str


APPEAL_TEMPLATES = {
    "en": AppealTemplate(
        lang="en",
        subject="Account Access Appeal - Unable to Access OpenAI Account",
        body="""Dear OpenAI Support Team,

I am writing to appeal the suspension/lock of my OpenAI account associated with this email address.

I am a legitimate user who has been using OpenAI services for [purpose, e.g., personal coding assistance, research, etc.]. I believe my account may have been flagged in error.

Here are the details of my situation:
- Account email: [your email]
- Last successful login date: [date]
- Payment method: [e.g., personal credit card from XX country]
- I have not violated any terms of service to my knowledge.
- I have enabled two-factor authentication.
- My IP/location is consistent with my payment region.

If there is any additional verification you require, I am happy to provide it (identity verification, payment confirmation, etc.).

I kindly request a review of my account status. Thank you for your time.

Sincerely,
[Your Name]""",
    ),
    "zh": AppealTemplate(
        lang="zh",
        subject="账户申诉 - 无法访问 OpenAI 账户",
        body="""尊敬的 OpenAI 支持团队：

我想对我被暂停/锁定的 OpenAI 账户提出申诉（账户邮箱：[你的邮箱]）。

我是一名正常用户，使用 OpenAI 服务的目的是[如：个人编程辅助、研究等]。我认为我的账户可能被系统误判。

以下是我的使用情况：
- 账户邮箱：[你的邮箱]
- 最后成功登录日期：[日期]
- 支付方式：[如：XX 国家的个人信用卡]
- 就我所知，我没有违反任何服务条款。
- 我已开启双因素认证。
- 我的 IP 地址/登录地区与我的支付地区一致。

如果你们需要额外的验证信息（身份验证、支付确认等），我乐意提供。

请重新审核我的账户状态。感谢你的时间。

此致
[你的名字]""",
    ),
}


@dataclass
class RiskQuestion:
    id: str
    question: str
    weight: float  # how much this affects risk score
    yes_risk: RiskLevel
    no_risk: RiskLevel


RISK_QUESTIONS: List[RiskQuestion] = [
    RiskQuestion(
        id="shared", question="你是否和别人合租/共享 OpenAI 账号？",
        weight=25, yes_risk=RiskLevel.CRITICAL, no_risk=RiskLevel.SAFE,
    ),
    RiskQuestion(
        id="topup", question="你是否使用过淘宝/闲鱼等平台的代充服务？",
        weight=25, yes_risk=RiskLevel.CRITICAL, no_risk=RiskLevel.SAFE,
    ),
    RiskQuestion(
        id="vpn", question="你是否使用过公共 VPN/机场节点访问 OpenAI？",
        weight=15, yes_risk=RiskLevel.HIGH, no_risk=RiskLevel.SAFE,
    ),
    RiskQuestion(
        id="region", question="你的支付卡地区、注册地区、登录 IP 地区是否一致？",
        weight=10, yes_risk=RiskLevel.SAFE, no_risk=RiskLevel.HIGH,
    ),
    RiskQuestion(
        id="chargeback", question="你是否对 OpenAI 发起过银行卡拒付/退单？",
        weight=20, yes_risk=RiskLevel.CRITICAL, no_risk=RiskLevel.SAFE,
    ),
    RiskQuestion(
        id="multi", question="你是否用同一支付方式注册了多个账号？",
        weight=10, yes_risk=RiskLevel.HIGH, no_risk=RiskLevel.SAFE,
    ),
    RiskQuestion(
        id="api_abuse", question="你是否使用 API 做过违规操作（绕过限制、生成违禁内容等）？",
        weight=15, yes_risk=RiskLevel.HIGH, no_risk=RiskLevel.SAFE,
    ),
    RiskQuestion(
        id="2fa", question="你是否开启了双因素认证 (2FA)？",
        weight=5, yes_risk=RiskLevel.SAFE, no_risk=RiskLevel.LOW,
    ),
    RiskQuestion(
        id="abnormal_login", question="你的账号近期是否有异常登录（新地区、多次失败等）？",
        weight=10, yes_risk=RiskLevel.MEDIUM, no_risk=RiskLevel.SAFE,
    ),
]


# Latest community signals (updated from V2EX/other community scans)
# Format: (date, title, replies, severity)
COMMUNITY_SIGNALS = [
    ("2026-06-06", "总结 OpenAI 封号问题：代充/共享是主要原因", 23, "critical"),
    ("2026-06-06", "OpenAI 陆续开始主动解封部分账号", 18, "info"),
    ("2026-06-05", "Codex 用户突然被封号（可能与 API 滥用有关）", 3, "warning"),
    ("2026-06-05", "部分被封账户解封后 API 额度被重置", 3, "info"),
    ("2026-06-04", "GPT代充封号风险警告", 3, "warning"),
    ("2026-05-28", "共享 ChatGPT Plus 被封后申诉失败", 12, "critical"),
    ("2026-05-20", "尼区礼品卡充值被封事件汇总", 8, "critical"),
]


def calculate_risk_score(answers: dict) -> tuple:
    """Calculate risk score from answers to RISK_QUESTIONS.
    
    Returns: (score, level, details)
    """
    total_weight = 0
    risky_weight = 0
    details = []
    
    for q in RISK_QUESTIONS:
        answer = answers.get(q.id)
        if answer is None:
            continue
        total_weight += q.weight
        if answer:  # answered "yes" → check yes_risk
            risk = q.yes_risk
        else:
            risk = q.no_risk
            
        if risk in (RiskLevel.CRITICAL, RiskLevel.HIGH):
            risky_weight += q.weight
        elif risk == RiskLevel.MEDIUM:
            risky_weight += q.weight * 0.5
            
        details.append((q.question, risk))
    
    if total_weight == 0:
        return 0, RiskLevel.SAFE, details
    
    score = (risky_weight / total_weight) * 100
    
    if score >= 70:
        level = RiskLevel.CRITICAL
    elif score >= 40:
        level = RiskLevel.HIGH
    elif score >= 20:
        level = RiskLevel.MEDIUM
    elif score >= 5:
        level = RiskLevel.LOW
    else:
        level = RiskLevel.SAFE
    
    return score, level, details
