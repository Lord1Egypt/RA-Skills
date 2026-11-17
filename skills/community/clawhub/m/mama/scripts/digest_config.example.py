# 邮箱智能体非敏感配置模板
# 实际运行时由 init_config.py 根据用户邮箱域名自动生成

CHECK_WINDOW = {
    "enabled": True,
    "workdays": [1, 2, 3, 4, 5],
    "start": "08:00",
    "end": "18:00",
    "interval_hours": 2,
}

WATCH_KEYWORDS = [
    "会议", "培训", "审批", "待办", "任务", "项目", "需求", "合同",
    "报价", "付款", "发票", "客户", "面试", "报名", "确认", "通知",
]

WATCH_DEADLINES = True

DEADLINE_HINTS = [
    "截止", "截至", "限于", "之前", "前完成", "前反馈", "前报送",
    "请于", "务必于", "须于", "需于", "最迟", "办理期限",
    "反馈期限", "报送期限", "完成时间", "截止时间",
    "deadline", "due", "before", "by",
]

# 以下配置项在首次运行时根据用户邮箱域名自动生成，请勿硬编码具体域名
TRUSTED_DOMAINS = []  # 由 init_config.py 自动填充

DEFAULT_PUSH_CHANNEL = "current"
MAX_EMAILS = 30
SINCE_HOURS = 2
