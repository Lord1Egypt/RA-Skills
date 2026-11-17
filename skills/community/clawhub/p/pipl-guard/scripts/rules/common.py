#!/usr/bin/env python3
"""PIPL 通用规则包 (common)。

覆盖《个人信息保护法》语境下的通用个人信息与敏感个人信息类别。
纯数据定义，无副作用、无网络、无动态执行。

每条 PATTERN 字段：
    id        规则标识
    regex     检测正则（原始字符串）
    label     中文说明
    category  个人信息类别
    severity  风险等级 high / medium / low
    validate  额外校验器名（None / "luhn" / "china_id"），由内核执行
    mask      脱敏策略 partial / full / hash

每条 KEYWORD 字段：(keyword, label, category, severity)
"""

PROFILE = {
    "id": "common",
    "name": "PIPL 通用护栏规则",
    "version": "1.0.0",
    "basis": "《中华人民共和国个人信息保护法》第二十八条（敏感个人信息）等",
}

# ============ 正则规则 ============
PATTERNS = [
    # —— 身份标识（敏感）——
    ("china_id",
     r"[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]",
     "中国大陆身份证号", "身份标识", "high", "china_id", "partial"),
    ("passport",
     r"(?:[EeGgDdSsPp]\d{8}|1[45]\d{7})",
     "中国护照号", "身份标识", "high", None, "partial"),
    ("hk_macao_permit",
     r"[HMhm]\d{8,10}",
     "港澳通行证号", "身份标识", "high", None, "partial"),
    ("social_credit",
     r"[0-9A-HJ-NPQRTUWXY]{2}\d{6}[0-9A-HJ-NPQRTUWXY]{10}",
     "统一社会信用代码", "组织标识", "medium", None, "partial"),

    # —— 联系方式（敏感度中高）——
    ("china_phone",
     r"1[3-9]\d{9}",
     "中国大陆手机号", "联系方式", "high", None, "partial"),
    ("landline",
     r"0\d{2,3}-?\d{7,8}",
     "固定电话号码", "联系方式", "medium", None, "partial"),
    ("email",
     r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}",
     "电子邮箱地址", "联系方式", "medium", None, "partial"),

    # —— 金融账户（敏感）——
    ("bank_card",
     r"[1-9]\d{11,18}",
     "银行卡号（Luhn 校验）", "金融账户", "high", "luhn", "partial"),

    # —— 网络身份 ——
    ("ipv4",
     r"(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)",
     "IPv4 地址", "网络身份", "low", "ipv4", "partial"),
    ("mac_addr",
     r"(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}",
     "MAC 地址", "网络身份", "low", None, "partial"),

    # —— 车辆 ——
    ("plate_no",
     r"[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领][A-HJ-NP-Z][A-HJ-NP-Z0-9]{4,5}[A-HJ-NP-Z0-9挂学警港澳]",
     "机动车车牌号", "行踪相关", "medium", None, "partial"),
]

# ============ 关键词/词典规则 ============
# 上下文触发词：出现时提示可能存在对应敏感信息，交由内核结合上下文标记
KEYWORDS = [
    ("生物识别", "生物识别信息线索", "生物识别", "high"),
    ("人脸", "生物识别信息线索", "生物识别", "high"),
    ("指纹", "生物识别信息线索", "生物识别", "high"),
    ("声纹", "生物识别信息线索", "生物识别", "high"),
    ("虹膜", "生物识别信息线索", "生物识别", "high"),
    ("基因", "医疗健康信息线索", "医疗健康", "high"),
    ("病历", "医疗健康信息线索", "医疗健康", "high"),
    ("诊断", "医疗健康信息线索", "医疗健康", "high"),
    ("宗教信仰", "特定身份信息线索", "特定身份", "high"),
    ("行踪轨迹", "行踪轨迹信息线索", "行踪相关", "high"),
    ("家庭住址", "住址信息线索", "联系方式", "medium"),
    ("未成年", "未成年人信息线索", "特殊主体", "high"),
    ("儿童", "未成年人信息线索", "特殊主体", "high"),
]
