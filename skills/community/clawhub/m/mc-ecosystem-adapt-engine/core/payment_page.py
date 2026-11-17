# -*- coding: utf-8 -*-
"""付费引导页面模块 - 渐进式付费引导（优化版）

V1.0.3: 实现三级渐进式付费引导
- 第一级：友好提醒（免费期结束 / 达到限额）
- 第二级：订阅方案展示（用户主动查看）
- 第三级：支持与打赏（微信/爱发电/个人网站）
- 支付页：三主按钮（微信/支付宝/PayPal）+ 其他支付入口
"""

import json
import base64
from datetime import datetime
from pathlib import Path
from typing import Optional

from core.i18n import t

# === 资源目录 ===
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_OUTPUT_DIR = _PROJECT_ROOT / "output"
_PAYMENT_ASSETS = _PROJECT_ROOT / "assets" / "payment"

# === 打赏渠道二维码（第三级支持与打赏页面使用）===
_TIPS_QR_FILES = {
    "wechat_mp": _PAYMENT_ASSETS / "wechat_qr.png",
    "afdian": _PAYMENT_ASSETS / "afdian_qr.png",
    "website": _PAYMENT_ASSETS / "website_qr.png",
}

# === 主支付渠道（三个大按钮）===
_PRI_PAYMENT_QR_FILES = {
    "wechat_pay": _PAYMENT_ASSETS / "wechat_pay_qr.png",
    "alipay": _PAYMENT_ASSETS / "alipay_qr.png",
    "paypal": _PAYMENT_ASSETS / "paypal_qr.png",
}

# === PayPal 按套餐的二维码文件 ===
_PAYPAL_PLAN_QR_FILES = {
    "monthly": _PAYMENT_ASSETS / "paypal_monthly.png",
    "quarterly": _PAYMENT_ASSETS / "paypal_quarterly.png",
    "yearly": _PAYMENT_ASSETS / "paypal_yearly.png",
}

# === 微信支付 按套餐+语言的二维码文件 ===
# 中文：金额 8.88 / 23.88 / 88.88；英文：金额 9.99 / 29.99 / 99.99
_WECHAT_PLAN_QR_FILES = {
    "monthly_cn":    _PAYMENT_ASSETS / "wechat_monthly_cn.png",
    "quarterly_cn":  _PAYMENT_ASSETS / "wechat_quarterly_cn.png",
    "yearly_cn":     _PAYMENT_ASSETS / "wechat_yearly_cn.png",
    "monthly_en":    _PAYMENT_ASSETS / "wechat_monthly_en.png",
    "quarterly_en":  _PAYMENT_ASSETS / "wechat_quarterly_en.png",
    "yearly_en":     _PAYMENT_ASSETS / "wechat_yearly_en.png",
}

# === 支付宝 按套餐+语言的二维码文件 ===
# 中文：金额 8.88 / 23.88 / 88.88；英文：金额 9.99 / 29.99 / 99.99
_ALIPAY_PLAN_QR_FILES = {
    "monthly_cn":    _PAYMENT_ASSETS / "alipay_monthly_cn.png",
    "quarterly_cn":  _PAYMENT_ASSETS / "alipay_quarterly_cn.png",
    "yearly_cn":     _PAYMENT_ASSETS / "alipay_yearly_cn.png",
    "monthly_en":    _PAYMENT_ASSETS / "alipay_monthly_en.png",
    "quarterly_en":  _PAYMENT_ASSETS / "alipay_quarterly_en.png",
    "yearly_en":     _PAYMENT_ASSETS / "alipay_yearly_en.png",
}

# === 其他支付渠道 ===
_OTHER_PAYMENT_QR_FILES = {
    "bank_card": _PAYMENT_ASSETS / "bank_card_qr.png",
    "unionpay": _PAYMENT_ASSETS / "unionpay_qr.png",
    "digital": _PAYMENT_ASSETS / "digital_yuan_qr.png",
    "douyin": _PAYMENT_ASSETS / "douyin_pay_qr.png",
}

# === 主支付渠道配置 ===
_PRI_PAYMENT_CHANNELS = {
    "wechat_pay": {
        "name": "微信支付",
        "name_en": "WeChat Pay",
        "icon": "💬",
        "color": "#07C160",
        "bg_color": "#e8f5e9",
        "description": "请打开微信 APP 扫码付款",
        "description_en": "Open WeChat App to scan QR code",
    },
    "alipay": {
        "name": "支付宝",
        "name_en": "Alipay",
        "icon": "💙",
        "color": "#1677FF",
        "bg_color": "#e3f2fd",
        "description": "请打开支付宝 APP 扫码付款",
        "description_en": "Open Alipay App to scan QR code",
    },
    "paypal": {
        "name": "PayPal/外币",
        "name_en": "PayPal / Foreign Currency",
        "icon": "🌍",
        "color": "#003087",
        "bg_color": "#e3f2fd",
        "description": "PayPal 及海外常用支付方式",
        "description_en": "PayPal and international payment",
    },
}

# === 其他支付渠道配置 ===
_OTHER_PAYMENT_CHANNELS = {
    "bank_card": {
        "name": "银行卡支付",
        "name_en": "Bank Card",
        "icon": "🏦",
        "color": "#4CAF50",
        "bg_color": "#e8f5e9",
        "description": "请使用银行卡扫码或转账",
        "description_en": "Bank card payment or transfer",
    },
    "unionpay": {
        "name": "云闪付",
        "name_en": "UnionPay",
        "icon": "💳",
        "color": "#E60012",
        "bg_color": "#ffebee",
        "description": "请打开云闪付 APP 扫码付款",
        "description_en": "Open UnionPay App to scan QR code",
    },
    "digital": {
        "name": "数字人民币",
        "name_en": "Digital CNY",
        "icon": "💴",
        "color": "#D4001A",
        "bg_color": "#ffebee",
        "description": "请打开数字人民币 APP 扫码付款",
        "description_en": "Open Digital CNY App to scan QR code",
    },
    "douyin": {
        "name": "抖音支付",
        "name_en": "Douyin Pay",
        "icon": "🎵",
        "color": "#000000",
        "bg_color": "#f5f5f5",
        "description": "敬请期待",
        "description_en": "Coming Soon",
        "coming_soon": True,
    },
}

# === 作者链接 ===
_AUTHOR_LINKS = {
    "afdian": "https://afdian.com/a/Lybw_203214_1630_?tab=home",
    "website": "https://cosmos-liang.netlify.app/#hero",
    "wechat_mp": "",
}

# === 订阅方案配置 ===
_SUBSCRIPTION_PLANS = {
    "monthly": {
        "name": "月度会员",
        "name_en": "Monthly",
        "price": "8.88",
        "unit": "元/月",
        "unit_en": "/month",
        "days": 30,
        "product": "MC Skill - 月度授权",
        "product_en": "MC Skill - Monthly License",
        "desc": "适合短期体验",
        "desc_en": "Perfect for short-term use",
        "price_usd": "9.99",
        "paypal_url": "https://www.paypal.com/ncp/payment/WNLHJ4A78G8P8",
    },
    "quarterly": {
        "name": "季度会员",
        "name_en": "Quarterly",
        "price": "23.88",
        "unit": "元/季",
        "unit_en": "/quarter",
        "days": 90,
        "product": "MC Skill - 季度授权",
        "product_en": "MC Skill - Quarterly License",
        "desc": "3个月更划算，省22元",
        "desc_en": "Save $3.50 compared to monthly",
        "price_usd": "29.99",
        "paypal_url": "https://www.paypal.com/ncp/payment/RA4MALVCHLTQJ",
    },
    "yearly": {
        "name": "年度会员",
        "name_en": "Yearly",
        "price": "88.88",
        "unit": "元/年",
        "unit_en": "/year",
        "days": 365,
        "product": "MC Skill - 年度授权",
        "product_en": "MC Skill - Annual License",
        "desc": "全年无忧，最优惠方案",
        "desc_en": "Best value for long-term users",
        "price_usd": "99.99",
        "paypal_url": "https://www.paypal.com/ncp/payment/HGSRGEUYDJVF8",
    },
}

# === 支付完成后的提示信息 ===
_PAYMENT_NOTICES = {
    "auto_unlock": "✅ 付款完成后 30 分钟内自动解锁相关套餐",
    "auto_unlock_en": "✅ Access unlocked within 30 minutes after payment",
    "must_click_complete": "⚠️ 付款后请务必点击下方「✅ 我已付款，等待验证」按钮，否则系统无法确认您的付款，可能导致支付失败",
    "must_click_complete_en": "⚠️ After paying, you MUST click the '✅ Paid, Verify Now' button below. Otherwise the system cannot confirm your payment, which may result in payment failure",
    "no_duplicate_pay": "⚠️ 同一套餐付款成功后 24 小时内请勿重复支付，否则会导致系统数据错乱",
    "no_duplicate_pay_en": "⚠️ Do not pay for the same plan again within 24 hours after a successful payment, otherwise it may cause system data confusion",
    "contact_if_not_work": "✅ 如付款后未生效，请保存支付截图联系客服",
    "contact_if_not_work_en": "✅ If not activated, save payment receipt and contact support",
    "update_notice": "✅ 更新优化：如发现功能漏洞，欢迎通过官网联系渠道或「优化建言」功能提出宝贵意见",
    "update_notice_en": "✅ Feedback: Report bugs or suggestions via official website contact or 'Optimization Suggestion' feature",
    "service_agreement": "✅ 服务说明：授权仅限个人使用，禁止转售",
    "service_agreement_en": "✅ License is for personal use only, resale prohibited",
}

# === 通用文案中英双语字典 ===
_I18N_TEXTS = {
    # 第一级 - 首页
    "page_title": ("MC Skill - 付费引导", "MC Skill - Payment Guide"),
    "icon_gift": ("🎁", "🎁"),
    "badge_member": ("会员提醒", "Membership Notice"),
    "free_used_up": ("您的免费额度已使用完", "Your free quota has been used up"),
    "subtitle_free": ("每日仍有免费额度可用，开通会员可享受更多权益", 
                      "Daily free quota still available. Upgrade for more benefits"),
    "trigger_reason": ("⚠️ 触发原因", "⚠️ Trigger Reason"),
    "daily_free": ("每日免费次数", "Daily Free Uses"),
    "member_multiplier": ("会员权益倍数", "Member Benefits"),
    "view_plans": ("💰 查看订阅方案", "💰 View Subscription Plans"),
    "support_author": ("❤️ 支持下作者", "❤️ Support the Author"),
    "free_daily_update": ("免费额度每天更新，会员权益实时生效", 
                          "Free quota resets daily, member benefits activate instantly"),
    "current_time": ("当前时间", "Current Time"),
    
    # 第二级 - 订阅方案
    "choose_plan": ("选择订阅方案", "Choose a Plan"),
    "choose_plan_sub": ("选择适合您的会员方案，解锁更多权益", 
                        "Select a plan that suits you to unlock more benefits"),
    "best_value": ("🔥 超值推荐", "🔥 Best Value"),
    "temporary_support": ("❤️ 暂不订阅，支持下作者", "❤️ Not now, support the author"),
    "back": ("返回", "Back"),
    
    # 第三级 - 支持与打赏
    "support_dev": ("支持与打赏", "Support & Donate"),
    "support_sub": ("感谢您的支持！关注作者，获取最新动态", 
                    "Thank you for your support! Follow for updates"),
    "follow_wechat": ("📱 关注微信公众号", "📱 Follow WeChat Official Account"),
    "afdian_support": ("☕ 爱发电支持", "☕ Support on Afdian"),
    "personal_website": ("🌐 作者个人网站", "🌐 Author's Website"),
    "click_view_qr": ("点击查看二维码", "Click to view QR code"),
    "continue_using": ("继续使用", "Continue Using"),
    
    # 支付页面
    "select_payment": ("选择支付方式", "Select Payment Method"),
    "payment_sub": ("请选择您方便的支付渠道完成付款", 
                    "Choose your preferred payment method"),
    "product_name": ("商品名称", "Product"),
    "amount_due": ("应付金额", "Amount Due"),
    "select_payment_method": ("选择支付方式", "Select Payment Method"),
    "other_payment": ("🔽 其他支付方式（银行卡、云闪付、数字人民币、PayPal 等）",
                      "🔽 Other Payment Methods (Bank Card, UnionPay, Digital CNY, PayPal, etc.)"),
    "collapse_other": ("🔼 收起其他支付方式", "🔼 Collapse Other Methods"),
    "more_options": ("更多支付选项", "More Payment Options"),
    "scan_qr": ("请打开对应 APP 扫码付款", "Open the app to scan QR code"),
    "qr_not_configured": ("⚠️ 该渠道收款码暂未配置，请联系作者",
                          "⚠️ QR code not configured for this method"),
    "payment_notices": ("📋 付款说明", "📋 Payment Notice"),
    "return_plans": ("返回选择方案", "Back to Plans"),
    "toast_free": ("✨ 已切回免费模式，每日免费额度继续可用",
                   "✨ Switched to free mode. Daily quota still available"),
    
    # 语言切换
    "lang_switch": ("EN", "中文"),
}


def _image_to_base64(path: Path) -> str:
    """将图片转换为 base64 用于内嵌显示"""
    if not path.exists():
        return ""
    try:
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        ext = path.suffix.lower()
        mime = "image/png" if ext == ".png" else "image/jpeg"
        return f"data:{mime};base64,{data}"
    except Exception:
        return ""


def _load_pri_qr_images() -> dict:
    """加载主支付渠道二维码"""
    return {
        key: _image_to_base64(path)
        for key, path in _PRI_PAYMENT_QR_FILES.items()
    }


def _load_other_qr_images() -> dict:
    """加载其他支付渠道二维码"""
    return {
        key: _image_to_base64(path)
        for key, path in _OTHER_PAYMENT_QR_FILES.items()
    }


def _load_tips_qr_images() -> dict:
    """加载打赏渠道二维码"""
    return {
        key: _image_to_base64(path)
        for key, path in _TIPS_QR_FILES.items()
    }


def _load_paypal_plan_qrs() -> dict:
    """加载PayPal按套餐的二维码图片"""
    return {
        key: _image_to_base64(path)
        for key, path in _PAYPAL_PLAN_QR_FILES.items()
    }


def _load_wechat_plan_qrs() -> dict:
    """加载微信支付按套餐的二维码图片"""
    result = {}
    for key, path in _WECHAT_PLAN_QR_FILES.items():
        if path.exists():
            result[key] = _image_to_base64(path)
    return result


def _load_alipay_plan_qrs() -> dict:
    """加载支付宝按套餐的二维码图片"""
    result = {}
    for key, path in _ALIPAY_PLAN_QR_FILES.items():
        if path.exists():
            result[key] = _image_to_base64(path)
    return result


def _build_full_page_html(reason: str = "", machine_id: str = "") -> str:
    """构建完整的三级渐进式付费引导页面
    
    Args:
        reason: 触发原因
        machine_id: 当前机器码，用于生成付款备注
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    pri_qrs_json = json.dumps(_load_pri_qr_images(), ensure_ascii=False)
    current_machine_id = machine_id or "未检测到"
    other_qrs_json = json.dumps(_load_other_qr_images(), ensure_ascii=False)
    tips_qrs_json = json.dumps(_load_tips_qr_images(), ensure_ascii=False)
    paypal_plan_qrs_json = json.dumps(_load_paypal_plan_qrs(), ensure_ascii=False)
    wechat_plan_qrs_json = json.dumps(_load_wechat_plan_qrs(), ensure_ascii=False)
    alipay_plan_qrs_json = json.dumps(_load_alipay_plan_qrs(), ensure_ascii=False)
    pri_channels_json = json.dumps(_PRI_PAYMENT_CHANNELS, ensure_ascii=False)
    other_channels_json = json.dumps(_OTHER_PAYMENT_CHANNELS, ensure_ascii=False)
    notices_json = json.dumps(_PAYMENT_NOTICES, ensure_ascii=False)
    author_links_json = json.dumps(_AUTHOR_LINKS, ensure_ascii=False)

    reason_html = ""
    if reason:
        reason_html = f"""
  <div class="reason-box">
    <div class="label" data-i18n-zh="⚠️ 触发原因" data-i18n-en="⚠️ Trigger Reason">⚠️ 触发原因</div>
    <div class="content">{reason}</div>
  </div>"""

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MC Skill - 付费引导</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: -apple-system, "Microsoft YaHei", "Segoe UI", sans-serif;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    color: #333; min-height: 100vh; padding: 20px;
    display: flex; align-items: center; justify-content: center;
  }}
  .container {{
    position: relative;
    max-width: 520px; width: 100%; background: #fff;
    border-radius: 20px; padding: 40px 30px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    animation: fadeIn 0.5s ease;
  }}
  @keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(-20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
  }}
  .header {{ text-align: center; margin-bottom: 30px; }}
  .icon {{ font-size: 56px; margin-bottom: 16px; }}
  .badge {{
    display: inline-block; padding: 6px 16px; border-radius: 20px;
    background: linear-gradient(90deg, #ff9a56, #ff6b6b);
    color: #fff; font-size: 12px; font-weight: 600; margin-bottom: 12px;
  }}
  h1 {{ font-size: 22px; color: #1a1a2e; margin-bottom: 10px; }}
  .subtitle {{ font-size: 14px; color: #666; line-height: 1.6; }}
  .reason-box {{
    background: linear-gradient(135deg, #fff3e0, #ffe0b2);
    border: 1px solid #ff9800; border-radius: 12px;
    padding: 16px; margin-bottom: 20px;
  }}
  .reason-box .label {{ font-size: 12px; color: #e65100; font-weight: 600; margin-bottom: 6px; }}
  .reason-box .content {{ font-size: 14px; color: #bf360c; line-height: 1.6; }}
  .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 24px; }}
  .info-card {{ background: #f5f5fa; border-radius: 12px; padding: 16px; text-align: center; }}
  .info-card .num {{
    font-size: 28px; font-weight: 700;
    background: linear-gradient(90deg, #3a7bd5, #00d2ff);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  }}
  .info-card .label {{ font-size: 12px; color: #666; margin-top: 4px; }}
  .divider {{ border: none; border-top: 1px dashed #ddd; margin: 20px 0; }}
  .option-title {{ font-size: 14px; color: #333; font-weight: 600; text-align: center; margin-bottom: 16px; }}
  .btn-group {{ display: flex; flex-direction: column; gap: 12px; }}
  .btn {{
    display: block; width: 100%; padding: 14px 20px;
    border-radius: 12px; text-align: center;
    font-size: 15px; font-weight: 600;
    text-decoration: none; cursor: pointer;
    transition: all 0.3s; border: none;
  }}
  .btn-primary {{
    background: linear-gradient(90deg, #3a7bd5, #00d2ff);
    color: #fff;
    box-shadow: 0 4px 15px rgba(58, 123, 213, 0.3);
  }}
  .btn-primary:hover {{ transform: translateY(-2px); box-shadow: 0 6px 20px rgba(58, 123, 213, 0.4); }}
  .btn-secondary {{ background: #f5f5fa; color: #555; border: 1px solid #e0e0e0; }}
  .btn-secondary:hover {{ background: #ebebed; }}
  .btn-danger {{ background: #fff3e0; color: #e65100; border: 1px solid #ff9800; }}
  .footer {{ margin-top: 24px; font-size: 11px; color: #999; text-align: center; line-height: 1.6; }}

  /* Modal */
  .modal-overlay {{
    display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0,0,0,0.5); align-items: center; justify-content: center;
    z-index: 1000; padding: 20px;
  }}
  .modal-overlay.active {{ display: flex; }}
  .modal {{
    position: relative;
    max-width: 520px; width: 100%; background: #fff;
    border-radius: 20px; padding: 30px 25px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    max-height: 95vh; overflow-y: auto;
  }}
  .modal-header {{ text-align: center; margin-bottom: 20px; }}
  .modal-icon {{ font-size: 48px; margin-bottom: 12px; }}
  .modal-title {{ font-size: 20px; color: #1a1a2e; margin-bottom: 8px; }}
  .modal-subtitle {{ font-size: 13px; color: #666; line-height: 1.6; }}

  /* Subscription Plans */
  .plan-list {{ display: flex; flex-direction: column; gap: 12px; margin-bottom: 20px; }}
  .plan-item {{
    border: 2px solid; border-radius: 12px; padding: 16px;
    cursor: pointer; transition: all 0.3s; position: relative;
  }}
  .plan-item:hover {{ transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
  .plan-monthly {{ background: linear-gradient(135deg, #e3f2fd, #bbdefb); border-color: #3a7bd5; }}
  .plan-quarterly {{ background: linear-gradient(135deg, #fff3e0, #ffe0b2); border-color: #ff9800; }}
  .plan-yearly {{ background: linear-gradient(135deg, #f3e5f5, #e1bee7); border-color: #9c27b0; }}
  .plan-badge {{
    position: absolute; top: -8px; right: 12px;
    background: #ff6b6b; color: #fff; font-size: 10px;
    padding: 2px 8px; border-radius: 10px;
  }}
  .plan-row {{ display: flex; justify-content: space-between; align-items: center; }}
  .plan-name {{ font-size: 16px; font-weight: 600; color: #1a1a2e; }}
  .plan-desc {{ font-size: 12px; color: #666; margin-top: 4px; }}
  .plan-price {{ font-size: 24px; font-weight: 700; }}
  .plan-price-monthly {{ color: #3a7bd5; }}
  .plan-price-quarterly {{ color: #ff9800; }}
  .plan-price-yearly {{ color: #9c27b0; }}
  .plan-unit {{ font-size: 11px; color: #999; }}

  /* Payment */
  .payment-order {{
    background: #f5f5fa; border-radius: 12px; padding: 16px; margin-bottom: 20px;
  }}
  .payment-order-row {{
    display: flex; justify-content: space-between; align-items: center;
    padding: 8px 0; border-bottom: 1px solid #e0e0e0;
  }}
  .payment-order-row:last-child {{ border-bottom: none; }}
  .payment-order-label {{ font-size: 13px; color: #666; }}
  .payment-order-value {{ font-size: 15px; font-weight: 600; color: #1a1a2e; }}
  .payment-order-value.price {{ color: #ff6b6b; font-size: 20px; }}

  /* 主支付渠道 - 大按钮布局 */
  .main-payment-section {{ margin-bottom: 16px; }}
  .payment-title {{
    font-size: 14px; font-weight: 600; color: #333;
    text-align: center; margin-bottom: 12px;
  }}
  .main-payment-grid {{
    display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px;
  }}
  .main-pay-card {{
    border: 2px solid #e0e0e0; border-radius: 16px;
    padding: 16px 10px; text-align: center;
    cursor: pointer; transition: all 0.3s;
    background: #fff;
  }}
  .main-pay-card:hover {{ transform: translateY(-3px); box-shadow: 0 6px 16px rgba(0,0,0,0.12); }}
  .main-pay-card.active {{ border-color: var(--card-color); background: var(--card-bg); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
  .main-pay-icon {{ font-size: 36px; margin-bottom: 8px; }}
  .main-pay-name {{ font-size: 13px; font-weight: 600; color: #333; }}

  /* 其他支付入口 */
  .other-payment-entry {{
    text-align: center; margin: 16px 0; padding: 12px;
    border: 1px dashed #ccc; border-radius: 12px;
    cursor: pointer; transition: all 0.3s;
    background: #fafafa;
  }}
  .other-payment-entry:hover {{ background: #f0f0f0; border-color: #999; }}
  .other-payment-entry-text {{ font-size: 13px; color: #666; }}
  .other-payment-entry-text strong {{ color: #1976d2; }}

  /* 其他支付渠道列表 */
  .other-payment-list {{
    display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 16px;
  }}
  .other-pay-item {{
    border: 1px solid #e0e0e0; border-radius: 12px;
    padding: 12px; text-align: center;
    cursor: pointer; transition: all 0.3s;
    background: #fff;
  }}
  .other-pay-item:hover {{ transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.08); }}
  .other-pay-item.active {{ border-color: var(--item-color); background: var(--item-bg); }}
  .other-pay-icon {{ font-size: 24px; margin-bottom: 6px; }}
  .other-pay-name {{ font-size: 12px; font-weight: 600; color: #333; }}

  /* QR display */
  .qr-display {{
    display: none;
    background: linear-gradient(135deg, #f5f5fa, #e8eaf6);
    border-radius: 12px; padding: 20px; margin-bottom: 16px; text-align: center;
  }}
  .qr-display.active {{ display: block; }}
  .qr-image-box {{
    max-width: 320px; margin: 0 auto; background: #fff;
    border: 1px solid #e0e0e0; border-radius: 8px;
    display: flex; align-items: center; justify-content: center; overflow: hidden;
  }}
  .qr-image-box img {{ width: 100%; height: auto; display: block; }}
  .qr-hint {{ font-size: 12px; color: #666; margin-top: 10px; line-height: 1.6; }}

  /* Payment Info Box */
  .payment-info-box {{
    background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
    border: 1px solid #4caf50; border-radius: 12px;
    padding: 14px; margin-bottom: 16px;
  }}
  .payment-info-title {{
    font-size: 13px; font-weight: 600; color: #2e7d32; margin-bottom: 10px;
  }}
  .payment-info-content {{ display: flex; flex-direction: column; gap: 8px; }}
  .info-row {{
    display: flex; align-items: center; gap: 8px;
    background: #fff; padding: 8px 12px; border-radius: 8px;
    font-size: 12px;
  }}
  .info-label {{ color: #666; min-width: 70px; font-weight: 600; }}
  .info-value {{ color: #1a1a2e; font-family: monospace; word-break: break-all; flex: 1; }}
  .info-tip {{
    font-size: 11px; color: #666; line-height: 1.6;
    background: rgba(255,255,255,0.6); padding: 8px; border-radius: 6px;
  }}
  .copy-btn {{
    margin-top: 8px;
    background: #4caf50; color: #fff; border: none;
    padding: 10px; border-radius: 8px; font-size: 12px; font-weight: 600;
    cursor: pointer; transition: all 0.3s;
  }}
  .copy-btn:hover {{ background: #388e3c; transform: translateY(-1px); }}
  .copy-btn:active {{ background: #2e7d32; }}

  /* Payment Notices */
  .payment-notices {{
    background: #fff9e6; border: 1px solid #ffd966; border-radius: 8px;
    padding: 12px; margin-top: 16px;
  }}
  .payment-notices-title {{
    font-size: 12px; font-weight: 600; color: #b8860b; margin-bottom: 8px;
  }}
  .payment-notices ul {{ list-style: none; padding: 0; }}
  .payment-notices li {{
    font-size: 11px; color: #666; line-height: 1.8; padding: 2px 0;
  }}

  /* Support Section */
  .support-section {{
    display: flex; flex-direction: column; gap: 12px; margin-top: 16px;
  }}
  .support-card {{
    background: #f5f5fa; border-radius: 12px; padding: 16px; text-align: center;
    cursor: pointer; transition: all 0.3s;
  }}
  .support-card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
  .support-card-wechat {{ background: #e8f5e9; }}
  .support-card-afdian {{ background: #fff3e0; }}
  .support-card-website {{ background: #e3f2fd; }}
  .support-label {{ font-size: 13px; font-weight: 600; color: #333; margin-bottom: 8px; }}
  .support-link {{
    display: inline-block; font-size: 12px; color: #1976d2;
    text-decoration: none; word-break: break-all;
  }}
  .support-link:hover {{ text-decoration: underline; }}

  .tip-qr-display {{
    display: none;
    background: #fff; border: 1px solid #e0e0e0;
    border-radius: 12px; padding: 16px; margin-top: 12px; text-align: center;
  }}
  .tip-qr-display.active {{ display: block; }}

  .modal-actions {{ display: flex; gap: 10px; margin-top: 16px; }}
  .modal-actions .btn {{ flex: 1; }}

  /* Language Switch */
  .lang-switch {{
    position: absolute; top: 16px; right: 16px; z-index: 100;
  }}
  .lang-selector {{
    position: relative;
  }}
  .lang-btn {{
    padding: 8px 14px; border: 2px solid #3a7bd5; border-radius: 20px;
    font-size: 13px; font-weight: 700; cursor: pointer;
    background: #fff;
    color: #3a7bd5; transition: all 0.3s;
    display: flex; align-items: center; gap: 6px;
  }}
  .lang-btn:hover {{
    background: #3a7bd5;
    color: #fff;
    box-shadow: 0 2px 8px rgba(58,123,213,0.3);
  }}
  .lang-btn .globe-icon {{
    font-size: 14px;
  }}
  .lang-btn .arrow {{
    font-size: 10px;
    transition: transform 0.3s;
  }}
  .lang-btn.active .arrow {{
    transform: rotate(180deg);
  }}
  .lang-dropdown {{
    position: absolute;
    top: calc(100% + 8px);
    right: 0;
    background: #fff;
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.15);
    min-width: 180px;
    max-height: 320px;
    overflow-y: auto;
    opacity: 0;
    visibility: hidden;
    transform: translateY(-8px);
    transition: all 0.25s ease;
    padding: 8px;
  }}
  .lang-dropdown.show {{
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
  }}
  .lang-dropdown-item {{
    padding: 10px 14px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 13px;
    color: #333;
  }}
  .lang-dropdown-item:hover {{
    background: #f0f5ff;
    color: #3a7bd5;
  }}
  .lang-dropdown-item.selected {{
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: #fff;
  }}
  .lang-dropdown-item .lang-name {{
    font-weight: 500;
  }}
  .lang-dropdown-item .lang-code {{
    font-size: 11px;
    opacity: 0.6;
  }}
  .lang-dropdown-item.selected .lang-code {{
    opacity: 0.8;
  }}

  /* i18n: no CSS-based hiding; JS controls textContent via data-i18n-zh/en attributes */
</style>
</head>
<body>

<div class="container" id="level1">

<!-- Language Switch Dropdown -->
<div class="lang-switch">
  <div class="lang-selector">
    <button class="lang-btn lang-toggle-btn" onclick="toggleLangMenu(event)">
      <span class="globe-icon">🌐</span>
      <span id="currentLangLabel">中文</span>
      <span class="arrow">▼</span>
    </button>
    <div class="lang-dropdown" id="langDropdown"></div>
  </div>
</div>

  <div class="header">
    <div class="icon">🎁</div>
    <div class="badge" data-i18n-zh="会员提醒" data-i18n-en="Membership Notice">会员提醒</div>
    <h1 data-i18n-zh="您的免费额度已使用完" data-i18n-en="Your free quota has been used up">您的免费额度已使用完</h1>
    <p class="subtitle" data-i18n-zh="每日仍有免费额度可用，开通会员可享受更多权益" data-i18n-en="Daily free quota still available. Upgrade for more benefits">每日仍有免费额度可用，开通会员可享受更多权益</p>
  </div>

  {reason_html}

  <div class="info-grid">
    <div class="info-card">
      <div class="num">20</div>
      <div class="label" data-i18n-zh="每日免费次数" data-i18n-en="Daily Free Uses">每日免费次数</div>
    </div>
    <div class="info-card">
      <div class="num">5×</div>
      <div class="label" data-i18n-zh="会员权益倍数" data-i18n-en="Member Benefits">会员权益倍数</div>
    </div>
  </div>

  <hr class="divider">

  <div class="option-title" data-i18n-zh="选择您的方式" data-i18n-en="Choose Your Option">选择您的方式</div>

  <div class="btn-group">
    <button class="btn btn-primary" onclick="showLevel2()">
      <span data-i18n-zh="💰 查看订阅方案" data-i18n-en="💰 View Subscription Plans">💰 查看订阅方案</span>
    </button>
    <button class="btn btn-secondary" onclick="showLevel3()">
      <span data-i18n-zh="❤️ 支持下作者" data-i18n-en="❤️ Support the Author">❤️ 支持下作者</span>
    </button>
  </div>

  <div class="footer">
    <span data-i18n-zh="免费额度每天更新，会员权益实时生效" data-i18n-en="Free quota resets daily, member benefits activate instantly">免费额度每天更新，会员权益实时生效</span><br>
    <span data-i18n-zh="当前时间" data-i18n-en="Current Time">当前时间</span>: {now}
  </div>
</div>

<!-- Level 2: Subscription Plans Modal -->
<div class="modal-overlay" id="level2Modal">
  <div class="modal">
    <!-- Language Switch Dropdown -->
    <div class="lang-switch">
      <div class="lang-selector">
        <button class="lang-btn lang-toggle-btn" onclick="toggleLangMenu(event)">
          <span class="globe-icon">🌐</span>
          <span id="currentLangLabelModal2">中文</span>
          <span class="arrow">▼</span>
        </button>
        <div class="lang-dropdown"></div>
      </div>
    </div>

    <div class="modal-header">
      <div class="modal-icon">💎</div>
      <h2 class="modal-title" data-i18n-zh="选择订阅方案" data-i18n-en="Choose a Plan">选择订阅方案</h2>
      <p class="modal-subtitle" data-i18n-zh="选择适合您的会员方案，解锁更多权益" data-i18n-en="Select a plan that suits you to unlock more benefits">选择适合您的会员方案，解锁更多权益</p>
    </div>

    <div class="plan-list">
      <div class="plan-item plan-monthly" onclick="selectPlan('monthly')">
        <div class="plan-row">
          <div>
            <div class="plan-name" data-i18n-zh="月度会员" data-i18n-en="Monthly">月度会员</div>
            <div class="plan-desc" data-i18n-zh="适合短期体验" data-i18n-en="Perfect for short-term use">适合短期体验</div>
          </div>
          <div style="text-align:right;">
            <div class="plan-price plan-price-monthly" id="planPriceMonthly">¥8.88</div>
            <div class="plan-unit" data-i18n-zh="元/月" data-i18n-en="/month">元/月</div>
          </div>
        </div>
      </div>

      <div class="plan-item plan-quarterly" onclick="selectPlan('quarterly')">
        <div class="plan-badge" data-i18n-zh="🔥 超值推荐" data-i18n-en="🔥 Best Value">🔥 超值推荐</div>
        <div class="plan-row">
          <div>
            <div class="plan-name" data-i18n-zh="季度会员" data-i18n-en="Quarterly">季度会员</div>
            <div class="plan-desc" data-i18n-zh="3个月更划算，省22元" data-i18n-en="Save $3.50 vs monthly">3个月更划算，省22元</div>
          </div>
          <div style="text-align:right;">
            <div class="plan-price plan-price-quarterly" id="planPriceQuarterly">¥23.88</div>
            <div class="plan-unit" data-i18n-zh="元/季" data-i18n-en="/quarter">元/季</div>
          </div>
        </div>
      </div>

      <div class="plan-item plan-yearly" onclick="selectPlan('yearly')">
        <div class="plan-row">
          <div>
            <div class="plan-name" data-i18n-zh="年度会员" data-i18n-en="Yearly">年度会员</div>
            <div class="plan-desc" data-i18n-zh="全年无忧，最优惠方案" data-i18n-en="Best value for long-term">全年无忧，最优惠方案</div>
          </div>
          <div style="text-align:right;">
            <div class="plan-price plan-price-yearly" id="planPriceYearly">¥88.88</div>
            <div class="plan-unit" data-i18n-zh="元/年" data-i18n-en="/year">元/年</div>
          </div>
        </div>
      </div>
    </div>

    <div class="modal-actions">
      <button class="btn btn-danger" onclick="showLevel3()">
        <span data-i18n-zh="❤️ 暂不订阅，支持下作者" data-i18n-en="❤️ Not now, support the author">❤️ 暂不订阅，支持下作者</span>
      </button>
      <button class="btn btn-secondary" onclick="hideLevel2()">
        <span data-i18n-zh="返回" data-i18n-en="Back">返回</span>
      </button>
    </div>
  </div>
</div>

<!-- Level 3: Support Developer Modal -->
<div class="modal-overlay" id="level3Modal">
  <div class="modal">
    <!-- Language Switch Dropdown -->
    <div class="lang-switch">
      <div class="lang-selector">
        <button class="lang-btn lang-toggle-btn" onclick="toggleLangMenu(event)">
          <span class="globe-icon">🌐</span>
          <span id="currentLangLabelModal3">中文</span>
          <span class="arrow">▼</span>
        </button>
        <div class="lang-dropdown"></div>
      </div>
    </div>

    <div class="modal-header">
      <div class="modal-icon">❤️</div>
      <h2 class="modal-title" data-i18n-zh="支持与打赏" data-i18n-en="Support & Donate">支持与打赏</h2>
      <p class="modal-subtitle" data-i18n-zh="感谢您的支持！关注作者，获取最新动态" data-i18n-en="Thank you for your support! Follow for updates">感谢您的支持！关注作者，获取最新动态</p>
    </div>

    <div class="support-section">
      <div class="support-card support-card-wechat" onclick="showTipQr('wechat_mp')">
        <div class="support-label" data-i18n-zh="📱 关注微信公众号" data-i18n-en="📱 Follow WeChat Official Account">📱 关注微信公众号</div>
        <span class="support-link" data-i18n-zh="点击查看二维码" data-i18n-en="Click to view QR code">点击查看二维码</span>
      </div>

      <div class="support-card support-card-afdian" onclick="showTipQr('afdian')">
        <div class="support-label" data-i18n-zh="☕ 爱发电支持" data-i18n-en="☕ Support on Afdian">☕ 爱发电支持</div>
        <span class="support-link" data-i18n-zh="点击查看二维码" data-i18n-en="Click to view QR code">点击查看二维码</span>
      </div>

      <div class="support-card support-card-website" onclick="showTipQr('website')">
        <div class="support-label" data-i18n-zh="🌐 作者个人网站" data-i18n-en="🌐 Author's Website">🌐 作者个人网站</div>
        <span class="support-link" data-i18n-zh="点击查看二维码" data-i18n-en="Click to view QR code">点击查看二维码</span>
      </div>
    </div>

    <div class="tip-qr-display" id="tipQrDisplay">
      <div style="font-size:13px;color:#333;font-weight:600;margin-bottom:10px;" id="tipQrLabel"></div>
      <div style="width:200px;height:200px;margin:0 auto;background:#fff;border:1px solid #e0e0e0;border-radius:8px;display:flex;align-items:center;justify-content:center;overflow:hidden;">
        <img id="tipQrImg" alt="Tip QR" style="max-width:100%;max-height:100%;">
      </div>
      <div id="tipQrLink" style="margin-top:12px;text-align:center;"></div>
    </div>

    <div class="modal-actions">
      <button class="btn btn-secondary" onclick="closeAllLevels()" style="background:linear-gradient(90deg,#667eea,#764ba2);color:#fff;border:none;">
        <span data-i18n-zh="继续使用" data-i18n-en="Continue Using">继续使用</span>
      </button>
    </div>
  </div>
</div>

<!-- Payment Modal -->
<div class="modal-overlay" id="paymentModal">
  <div class="modal">
    <!-- Language Switch Dropdown -->
    <div class="lang-switch">
      <div class="lang-selector">
        <button class="lang-btn lang-toggle-btn" onclick="toggleLangMenu(event)">
          <span class="globe-icon">🌐</span>
          <span id="currentLangLabelModal">中文</span>
          <span class="arrow">▼</span>
        </button>
        <div class="lang-dropdown"></div>
      </div>
    </div>

    <div class="modal-header">
      <div class="modal-icon">💳</div>
      <h2 class="modal-title" data-i18n-zh="选择支付方式" data-i18n-en="Select Payment Method">选择支付方式</h2>
      <p class="modal-subtitle" data-i18n-zh="请选择您方便的支付渠道完成付款" data-i18n-en="Choose your preferred payment method">请选择您方便的支付渠道完成付款</p>
    </div>

    <div class="payment-order">
      <div class="payment-order-row">
        <span class="payment-order-label" data-i18n-zh="商品名称" data-i18n-en="Product">商品名称</span>
        <span class="payment-order-value" id="orderProduct">-</span>
      </div>
      <div class="payment-order-row">
        <span class="payment-order-label" data-i18n-zh="应付金额" data-i18n-en="Amount Due">应付金额</span>
        <span class="payment-order-value price" id="orderPrice">¥0.00</span>
      </div>
    </div>

    <!-- 主支付渠道 - 三个大按钮 -->
    <div class="main-payment-section" id="mainPaymentSection">
      <div class="payment-title" data-i18n-zh="选择支付方式" data-i18n-en="Select Payment Method">选择支付方式</div>
      <div class="main-payment-grid" id="mainPaymentGrid"></div>
    </div>

    <!-- 其他支付入口 -->
    <div class="other-payment-entry" id="otherEntry" onclick="toggleOtherPayment()">
      <span class="other-payment-entry-text" data-i18n-zh="🔽 <strong>其他支付方式</strong>（银行卡、云闪付、数字人民币、PayPal 等）" data-i18n-en="🔽 <strong>Other Payment Methods</strong> (Bank Card, UnionPay, Digital CNY, PayPal, etc.)">🔽 <strong>其他支付方式</strong>（银行卡、云闪付、数字人民币、PayPal 等）</span>
    </div>

    <!-- 其他支付渠道 - 默认隐藏 -->
    <div id="otherPaymentSection" style="display:none;">
      <div class="payment-title" style="font-size:12px;color:#666;" data-i18n-zh="更多支付选项" data-i18n-en="More Payment Options">更多支付选项</div>
      <div class="other-payment-list" id="otherPaymentList"></div>
    </div>

    <!-- 二维码显示区 -->
    <div class="qr-display" id="qrDisplay">
      <div class="qr-image-box">
        <img id="channelQr" alt="Payment QR" style="max-width:100%;max-height:100%;">
      </div>
      <div class="qr-hint" id="qrDisplayHint" data-i18n-zh="请打开对应 APP 扫码付款" data-i18n-en="Open the app to scan QR code">请打开对应 APP 扫码付款</div>
    </div>

    <div class="payment-notices">
      <div class="payment-notices-title" data-i18n-zh="📋 付款说明" data-i18n-en="📋 Payment Notice">📋 付款说明</div>
      <ul id="paymentNotices"></ul>
    </div>

    <div class="modal-actions">
      <button class="btn btn-secondary" onclick="closePayment()">
        <span data-i18n-zh="返回选择方案" data-i18n-en="Back to Plans">返回选择方案</span>
      </button>
      <button class="btn btn-primary" onclick="confirmPayment()">
        <span data-i18n-zh="✅ 我已付款，等待验证" data-i18n-en="✅ Paid, Verify Now">✅ 我已付款，等待验证</span>
      </button>
    </div>
  </div>
</div>

<script>
  const priQrs = {pri_qrs_json};
  const otherQrs = {other_qrs_json};
  const tipQrs = {tips_qrs_json};
  const paypalPlanQrs = {paypal_plan_qrs_json};
  const wechatPlanQrs = {wechat_plan_qrs_json};
  const alipayPlanQrs = {alipay_plan_qrs_json};
  const plans = {json.dumps(_SUBSCRIPTION_PLANS, ensure_ascii=False)};
  const priChannels = {pri_channels_json};
  const otherChannels = {other_channels_json};
  const notices = {notices_json};
  const authorLinks = {author_links_json};

  let currentLang = 'zh_cn';
  let selectedPlan = null;
  let currentChannel = null;
  let currentChannelType = 'pri';
  
  // ============ 多语言支持配置 ============
  const SUPPORTED_LANGUAGES = {{
    'en_us': 'English',
    'zh_cn': '简体中文',
    'zh_tw': '繁體中文',
    'ja_jp': '日本語',
    'ko_kr': '한국어',
    'ru_ru': 'Русский',
    'es_es': 'Español',
    'it_it': 'Italiano',
    'el_gr': 'Ελληνικά',
    'th_th': 'ไทย',
    'hi_in': 'हिन्दी',
    'ar_sa': 'العربية'
  }};
  
  // 语言代码映射
  const LANG_DISPLAY_NAMES = {{
    'en_us': 'EN',
    'zh_cn': '中文',
    'zh_tw': '繁體',
    'ja_jp': '日本語',
    'ko_kr': '한국어',
    'ru_ru': 'Русский',
    'es_es': 'Español',
    'it_it': 'Italiano',
    'el_gr': 'Ελληνικά',
    'th_th': 'ไทย',
    'hi_in': 'हिन्दी',
    'ar_sa': 'العربية'
  }};
  
  // 判断是否使用人民币（只有简体中文使用人民币）
  function isChineseLang(lang) {{
    return lang === 'zh_cn';
  }}
  
  // 获取语言显示名称
  function getLangDisplayName(lang) {{
    return LANG_DISPLAY_NAMES[lang] || lang;
  }}
  
  // 获取完整语言名称
  function getLangFullName(lang) {{
    return SUPPORTED_LANGUAGES[lang] || lang;
  }}
  
  // 初始化所有语言下拉菜单
  function initLangDropdown() {{
    // 遍历页面上所有的 lang-dropdown 元素
    document.querySelectorAll('.lang-dropdown').forEach(dropdown => {{
      dropdown.innerHTML = '';
      Object.keys(SUPPORTED_LANGUAGES).forEach(langCode => {{
        const item = document.createElement('div');
        item.className = 'lang-dropdown-item' + (langCode === currentLang ? ' selected' : '');
        item.innerHTML = '<span class="lang-name">' + SUPPORTED_LANGUAGES[langCode] + '</span><span class="lang-code">' + langCode + '</span>';
        item.onclick = function(e) {{
          if (e) e.stopPropagation();
          switchLang(langCode);
          hideAllLangMenus();
        }};
        dropdown.appendChild(item);
      }});
    }});
  }}
  
  // 根据点击的按钮，找到对应的 lang-selector 容器中的 dropdown 和 btn
  function getLangDropdownAndBtn(event) {{
    let targetBtn = null;
    if (event && event.currentTarget) {{
      targetBtn = event.currentTarget;
    }} else if (event && event.target) {{
      // 向上查找最近的 lang-toggle-btn
      targetBtn = event.target.closest('.lang-toggle-btn');
    }}
    if (!targetBtn) return null;
    const selector = targetBtn.closest('.lang-selector');
    if (!selector) return null;
    const dropdown = selector.querySelector('.lang-dropdown');
    return {{ selector: selector, dropdown: dropdown, btn: targetBtn }};
  }}
  
  // 显示/隐藏语言菜单（基于事件源）
  function toggleLangMenu(event) {{
    if (event) event.stopPropagation();
    const elems = getLangDropdownAndBtn(event);
    if (!elems || !elems.dropdown || !elems.btn) return;
    
    // 先关闭其他所有已打开的菜单
    document.querySelectorAll('.lang-dropdown.show').forEach(otherDropdown => {{
      if (otherDropdown !== elems.dropdown) {{
        otherDropdown.classList.remove('show');
        const otherBtn = otherDropdown.parentElement.querySelector('.lang-toggle-btn');
        if (otherBtn) otherBtn.classList.remove('active');
      }}
    }});
    
    if (elems.dropdown.classList.contains('show')) {{
      hideLangMenu(event);
    }} else {{
      showLangMenu(event);
    }}
  }}
  
  function showLangMenu(event) {{
    const elems = getLangDropdownAndBtn(event);
    if (!elems || !elems.dropdown || !elems.btn) return;
    const {{ dropdown, btn }} = elems;
    
    dropdown.classList.add('show');
    btn.classList.add('active');
    // 更新选中状态
    dropdown.querySelectorAll('.lang-dropdown-item').forEach(item => {{
      item.classList.remove('selected');
    }});
    const items = dropdown.querySelectorAll('.lang-dropdown-item');
    const idx = Object.keys(SUPPORTED_LANGUAGES).indexOf(currentLang);
    if (idx >= 0 && items[idx]) {{
      items[idx].classList.add('selected');
    }}
  }}
  
  function hideLangMenu(event) {{
    const elems = getLangDropdownAndBtn(event);
    if (!elems || !elems.dropdown || !elems.btn) return;
    elems.dropdown.classList.remove('show');
    elems.btn.classList.remove('active');
  }}
  
  // 关闭所有语言菜单
  function hideAllLangMenus() {{
    document.querySelectorAll('.lang-dropdown.show').forEach(dropdown => {{
      dropdown.classList.remove('show');
      const btn = dropdown.parentElement.querySelector('.lang-toggle-btn');
      if (btn) btn.classList.remove('active');
    }});
  }}
  
  // 点击其他地方关闭所有语言菜单
  document.addEventListener('click', function(e) {{
    let isInsideLangSwitch = false;
    document.querySelectorAll('.lang-switch').forEach(langSwitch => {{
      if (langSwitch.contains(e.target)) {{
        isInsideLangSwitch = true;
      }}
    }});
    if (!isInsideLangSwitch) {{
      hideAllLangMenus();
    }}
  }});
  
  // ============ 支付操作监控系统 ============
  const SERVER_URL = 'http://localhost:8000';
  let qrOpenedAt = null;  // QR码打开时间戳
  // 生成唯一会话ID：用于后端聚合完整付费流程日志
  const PAYMENT_SESSION_ID = 'pay-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 10);

  async function reportPaymentAction(action, extraData = {{}}) {{
    if (!selectedPlan && action !== 'page_opened') return;
    const plan = selectedPlan ? plans[selectedPlan] : {{}};
    const note = selectedPlan ? 'MC Skill-' + selectedPlan.toUpperCase() + '-' + currentMachineId : '';

    // 获取渠道中文名（始终用中文记录，不受界面语言影响）
    const channelCnName = (function() {{
      if (!currentChannel) return '';
      const priCh = priChannels[currentChannel];
      if (priCh) return priCh.name;  // 中文渠道名
      const otherCh = otherChannels[currentChannel];
      if (otherCh) return otherCh.name;
      return currentChannel;
    }})();

    const data = {{
      machine_id: currentMachineId,
      action: action,
      session_id: PAYMENT_SESSION_ID,
      plan: selectedPlan || '',
      channel: currentChannel || '',
      channel_name: channelCnName,           // 始终发送中文渠道名
      product_name: selectedPlan ? plan.product : '',  // 始终用中文商品名，不受界面语言影响
      amount: selectedPlan ? plan.price : 0,
      note: note,
      timestamp: new Date().toISOString(),
      ...extraData
    }};
    
    try {{
      const response = await fetch(SERVER_URL + '/api/payment/action', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify(data)
      }});
      
      const result = await response.json();
      return result;
    }} catch (err) {{
      console.log('[Payment Monitor] Report failed:', action);
      return null;
    }}
  }}
  
  // 页面加载完成后初始化
  window.addEventListener('DOMContentLoaded', function() {{
    // 初始化语言：先恢复用户偏好，再检测浏览器语言
    try {{
      const savedLang = localStorage.getItem('mc_skill_lang');
      if (savedLang && SUPPORTED_LANGUAGES[savedLang]) {{
        currentLang = savedLang;
      }} else {{
        // 检测浏览器语言
        const browserLang = (navigator.language || 'zh').toLowerCase();
        const langMap = {{
          'zh': 'zh_cn',
          'zh-cn': 'zh_cn',
          'zh-tw': 'zh_tw',
          'zh-hk': 'zh_tw',
          'ja': 'ja_jp',
          'ko': 'ko_kr',
          'ru': 'ru_ru',
          'es': 'es_es',
          'it': 'it_it',
          'el': 'el_gr',
          'th': 'th_th',
          'hi': 'hi_in',
          'en': 'en_us',
          'en-us': 'en_us',
          'en-gb': 'en_us'
        }};
        currentLang = langMap[browserLang] || 'zh_cn';
      }}
    }} catch(e) {{
      currentLang = 'zh_cn';
    }}
    
    // 初始化语言下拉菜单
    initLangDropdown();
    switchLang(currentLang);
    
    // 上报页面打开事件
    setTimeout(() => {{
      reportPaymentAction('page_opened');
    }}, 500);
  }});
  
  // 追踪QR码打开时间
  function trackQrOpened() {{
    qrOpenedAt = Date.now();
  }}
  
  function trackQrClosed() {{
    if (qrOpenedAt !== null) {{
      const duration = (Date.now() - qrOpenedAt) / 1000;
      qrOpenedAt = null;
      if (selectedPlan) {{
        reportPaymentAction('qr_closed', {{
          qr_duration_seconds: duration
        }});
      }}
      return duration;
    }}
    return 0;
  }}
  // ============ 监控系统结束 ============

  // 11种语言翻译字典
  const TRANSLATIONS = {{
    // 徽章
    "会员提醒": {{
      "zh_cn": "会员提醒", "en_us": "Membership Notice", "zh_tw": "會員提醒",
      "ja_jp": "メンバーシップ通知", "ko_kr": "회원 안내", "ru_ru": "Уведомление о членстве",
      "es_es": "Aviso de membresía", "it_it": "Notifica membership", "el_gr": "Ειδοποίηση συνδρομής",
      "th_th": "แจ้งเตือนสมาชิก", "hi_in": "सदस्यता सूचना",
      "ar_sa": "إشعار العضوية"
    }},
    // 免费额度用完
    "您的免费额度已使用完": {{
      "zh_cn": "您的免费额度已使用完", "en_us": "Your free quota has been used up", "zh_tw": "您的免費額度已使用完",
      "ja_jp": "無料クォータを使い果たしました", "ko_kr": "무료 한도를 모두 사용했습니다", "ru_ru": "Ваш бесплатный лимит исчерпан",
      "es_es": "Su cuota gratuita se ha agotado", "it_it": "La tua quota gratuita è stata esaurita", "el_gr": "Το δωρεάν όριο σας έχει εξαντληθεί",
      "th_th": "โควต้าฟรีของคุณใช้หมดแล้ว", "hi_in": "आपका मुफ्त कोटा समाप्त हो चुका है",
      "ar_sa": "لقد استنفدت حصتك المجانية"
    }},
    // 副标题
    "每日仍有免费额度可用，开通会员可享受更多权益": {{
      "zh_cn": "每日仍有免费额度可用，开通会员可享受更多权益", "en_us": "Daily free quota still available. Upgrade for more benefits", "zh_tw": "每日仍有免費額度可用，開通會員可享受更多權益",
      "ja_jp": "毎日無料クォータが利用可能です。アップグレードして特典を獲得しましょう", "ko_kr": "매일 무료 한도가 사용 가능합니다. 업그레이드하여 더 많은 혜택을 받으세요", "ru_ru": "Ежедневный бесплатный лимит еще доступен. Повысьте уровень для получения преимуществ",
      "es_es": "La cuota gratuita diaria aún está disponible. Actualice para obtener más beneficios", "it_it": "La quota gratuita giornaliera è ancora disponibile. Aggiorna per ottenere più vantaggi", "el_gr": "Το καθημερινό δωρεάν όριο είναι ακόμα διαθέσιμο. Αναβάθμιση για περισσότερα οφέλη",
      "th_th": "โควต้าฟรีรายวันยังมีอยู่ อัปเกรดเพื่อรับสิทธิประโยชน์มากขึ้น", "hi_in": "दैनिक मुफ्त कोटा अभी भी उपलब्ध है। अधिक लाभों के लिए अपग्रेड करें",
      "ar_sa": "لا تزال الحصة المجانية اليومية متاحة. قم بالترقية للحصول على مزيد من المزايا"
    }},
    // 每日免费次数
    "每日免费次数": {{
      "zh_cn": "每日免费次数", "en_us": "Daily Free Uses", "zh_tw": "每日免費次數",
      "ja_jp": "毎日の無料使用回数", "ko_kr": "매일 무료 사용 횟수", "ru_ru": "Ежедневные бесплатные использования",
      "es_es": "Usos gratuitos diarios", "it_it": "Usi gratuiti giornalieri", "el_gr": "Δωρεάν χρήσεις ανά ημέρα",
      "th_th": "การใช้ฟรีรายวัน", "hi_in": "दैनिक मुफ्त उपयोग",
      "ar_sa": "الاستخدامات المجانية اليومية"
    }},
    // 会员权益倍数
    "会员权益倍数": {{
      "zh_cn": "会员权益倍数", "en_us": "Member Benefits", "zh_tw": "會員權益倍數",
      "ja_jp": "メンバー特典", "ko_kr": "회원 혜택", "ru_ru": "Преимущества участника",
      "es_es": "Beneficios de membresía", "it_it": "Vantaggi membership", "el_gr": "Παροχές μελών",
      "th_th": "สิทธิประโยชน์สมาชิก", "hi_in": "सदस्य लाभ",
      "ar_sa": "مزايا العضوية"
    }},
    // 选择您的方式
    "选择您的方式": {{
      "zh_cn": "选择您的方式", "en_us": "Choose Your Option", "zh_tw": "選擇您的方式",
      "ja_jp": "お選びください", "ko_kr": "선택하세요", "ru_ru": "Выберите вариант",
      "es_es": "Elija su opción", "it_it": "Scegli la tua opzione", "el_gr": "Επίλεξε την επιλογή σου",
      "th_th": "เลือกตัวเลือกของคุณ", "hi_in": "अपना विकल्प चुनें",
      "ar_sa": "اختر خيارك"
    }},
    // 查看订阅方案
    "💰 查看订阅方案": {{
      "zh_cn": "💰 查看订阅方案", "en_us": "💰 View Subscription Plans", "zh_tw": "💰 查看訂閱方案",
      "ja_jp": "💰 サブスクリプションプランを見る", "ko_kr": "💰 구독 계획 보기", "ru_ru": "💰 Посмотреть планы подписки",
      "es_es": "💰 Ver planes de suscripción", "it_it": "💰 Visualizza i piani di abbonamento", "el_gr": "💰 Δείτε τα προγράμματα συνδρομής",
      "th_th": "💰 ดูแผนการสมัครสมาชิก", "hi_in": "💰 सदस्यता योजनाएँ देखें",
      "ar_sa": "💰 عرض خطط الاشتراك"
    }},
    // 支持下作者
    "❤️ 支持下作者": {{
      "zh_cn": "❤️ 支持下作者", "en_us": "❤️ Support the Author", "zh_tw": "❤️ 支持下作者",
      "ja_jp": "❤️ 作者を支援する", "ko_kr": "❤️ 작가를 지원하세요", "ru_ru": "❤️ Поддержать автора",
      "es_es": "❤️ Apoyar al autor", "it_it": "❤️ Sostieni l'autore", "el_gr": "❤️ Υποστηρίξτε τον δημιουργό",
      "th_th": "❤️ สนับสนุนผู้เขียน", "hi_in": "❤️ लेखक का समर्थन करें",
      "ar_sa": "❤️ ادعم المؤلف"
    }},
    // 免费额度每天更新
    "免费额度每天更新，会员权益实时生效": {{
      "zh_cn": "免费额度每天更新，会员权益实时生效", "en_us": "Free quota resets daily, member benefits activate instantly", "zh_tw": "免費額度每天更新，會員權益即時生效",
      "ja_jp": "無料クォータは毎日リセット、メンバー特典は即時適用", "ko_kr": "무료 한도는 매일 초기화, 회원 혜택은 즉시 적용", "ru_ru": "Бесплатный лимит сбрасывается ежедневно, преимущества активируются мгновенно",
      "es_es": "Cuota gratuita se reinicia diariamente, beneficios activados al instante", "it_it": "Quota gratuita si resetta giornalmente, vantaggi attivati istantaneamente", "el_gr": "Το δωρεάν όριο επαναφέρεται καθημερινά, τα οφέλη ενεργοποιούνται αμέσως",
      "th_th": "โควต้าฟรีรีเซ็ตทุกวัน สิทธิประโยชน์สมาชิกเปิดใช้ทันที", "hi_in": "मुफ्त कोटा दैनिक रीसेट, सदस्य लाभ तुरंत सक्रिय",
      "ar_sa": "تتم إعادة تعيين الحصة المجانية يومياً، وتفعيل مزايا العضوية فوراً"
    }},
    // 当前时间
    "当前时间": {{
      "zh_cn": "当前时间", "en_us": "Current Time", "zh_tw": "當前時間",
      "ja_jp": "現在時刻", "ko_kr": "현재 시간", "ru_ru": "Текущее время",
      "es_es": "Hora actual", "it_it": "Ora attuale", "el_gr": "Τρέχουσα ώρα",
      "th_th": "เวลาปัจจุบัน", "hi_in": "वर्तमान समय",
      "ar_sa": "الوقت الحالي"
    }},
    // 选择订阅方案
    "选择订阅方案": {{
      "zh_cn": "选择订阅方案", "en_us": "Choose a Plan", "zh_tw": "選擇訂閱方案",
      "ja_jp": "プランを選択", "ko_kr": "플랜 선택", "ru_ru": "Выберите план",
      "es_es": "Elija un plan", "it_it": "Scegli un piano", "el_gr": "Επίλεξε ένα πρόγραμμα",
      "th_th": "เลือกแผน", "hi_in": "प्लान चुनें",
      "ar_sa": "اختر خطة"
    }},
    // 选择适合您的会员方案
    "选择适合您的会员方案，解锁更多权益": {{
      "zh_cn": "选择适合您的会员方案，解锁更多权益", "en_us": "Select a plan that suits you to unlock more benefits", "zh_tw": "選擇適合您的會員方案，解鎖更多權益",
      "ja_jp": "お客様に合ったプランを選択して、より多くの特典をアンロックしましょう", "ko_kr": "귀하에게 적합한 플랜을 선택하여 더 많은 혜택을 잠금 해제하세요", "ru_ru": "Выберите план, который подходит вам, чтобы разблокировать больше преимуществ",
      "es_es": "Seleccione un plan que se adapte a usted para desbloquear más beneficios", "it_it": "Seleziona un piano adatto a te per sbloccare più vantaggi", "el_gr": "Επίλεξε ένα πρόγραμμα που ταιριάζει σε εσένα για να ξεκλειδώσεις περισσότερα οφέλη",
      "th_th": "เลือกแผนที่เหมาะกับคุณเพื่อปลดล็อกสิทธิประโยชน์มากขึ้น", "hi_in": "अधिक लाभ अनलॉक करने के लिए उपयुक्त प्लान चुनें",
      "ar_sa": "اختر الخطة المناسبة لك لفتح المزيد من المزايا"
    }},
    // 月度会员
    "月度会员": {{
      "zh_cn": "月度会员", "en_us": "Monthly", "zh_tw": "月度會員",
      "ja_jp": "月額会員", "ko_kr": "월간 회원", "ru_ru": "Ежемесячная подписка",
      "es_es": "Suscripción mensual", "it_it": "Abbonamento mensile", "el_gr": "Μηνιαία συνδρομή",
      "th_th": "สมาชิกรายเดือน", "hi_in": "मासिक सदस्यता",
      "ar_sa": "شهري"
    }},
    // 适合短期体验
    "适合短期体验": {{
      "zh_cn": "适合短期体验", "en_us": "Perfect for short-term use", "zh_tw": "適合短期體驗",
      "ja_jp": "短期利用に最適", "ko_kr": "단기 사용에 적합", "ru_ru": "Идеально для краткосрочного использования",
      "es_es": "Perfecto para uso a corto plazo", "it_it": "Perfetto per uso a breve termine", "el_gr": "Ιδανικό για βραχυπρόθεσμη χρήση",
      "th_th": "เหมาะสำหรับการใช้งานระยะสั้น", "hi_in": "अल्पकालिक उपयोग के लिए उपयुक्त",
      "ar_sa": "مثالي للاستخدام قصير الأمد"
    }},
    // 元/月
    "元/月": {{
      "zh_cn": "元/月", "en_us": "/month", "zh_tw": "元/月",
      "ja_jp": "/月", "ko_kr": "/월", "ru_ru": "/мес",
      "es_es": "/mes", "it_it": "/mese", "el_gr": "/μήνα",
      "th_th": "/เดือน", "hi_in": "/माह",
      "ar_sa": "/شهر"
    }},
    // 超值推荐
    "🔥 超值推荐": {{
      "zh_cn": "🔥 超值推荐", "en_us": "🔥 Best Value", "zh_tw": "🔥 超值推薦",
      "ja_jp": "🔥 お得", "ko_kr": "🔥 최고 가치", "ru_ru": "🔥 Лучшая цена",
      "es_es": "🔥 Mejor valor", "it_it": "🔥 Miglior valore", "el_gr": "🔥 Καλύτερη σχέση ποιότητας-τιμής",
      "th_th": "🔥 คุ้มค่าที่สุด", "hi_in": "🔥 सबसे बढ़िया मूल्य",
      "ar_sa": "🔥 أفضل قيمة"
    }},
    // 季度会员
    "季度会员": {{
      "zh_cn": "季度会员", "en_us": "Quarterly", "zh_tw": "季度會員",
      "ja_jp": "季節会員", "ko_kr": "분기 회원", "ru_ru": "Квартальная подписка",
      "es_es": "Suscripción trimestral", "it_it": "Abbonamento trimestrale", "el_gr": "Τριμηνιαία συνδρομή",
      "th_th": "สมาชิกรายไตรมาส", "hi_in": "त्रैमासिक सदस्यता",
      "ar_sa": "فصلي"
    }},
    // 3个月更划算，省22元
    "3个月更划算，省22元": {{
      "zh_cn": "3个月更划算，省22元", "en_us": "Save $3.50 vs monthly", "zh_tw": "3個月更划算，省22元",
      "ja_jp": "3ヶ月でお得、¥22節約", "ko_kr": "3개월 더 경제적, ¥22 절약", "ru_ru": "3 месяца выгоднее, экономия ¥22",
      "es_es": "3 meses más rentable, ahorro ¥22", "it_it": "3 mesi più convenienti, risparmio ¥22", "el_gr": "3 μήνες πιο συμφέρουσα, εξοικονόμηση ¥22",
      "th_th": "3 เดือนคุ้มกว่า ประหยัด ¥22", "hi_in": "3 महीने अधिक किफायती, ¥22 बचाएं",
      "ar_sa": "وفر 3.50 دولار مقارنةً بالخطة الشهرية"
    }},
    // 元/季
    "元/季": {{
      "zh_cn": "元/季", "en_us": "/quarter", "zh_tw": "元/季",
      "ja_jp": "/季", "ko_kr": "/분기", "ru_ru": "/кварт",
      "es_es": "/trimestre", "it_it": "/trimestre", "el_gr": "/τρίμηνο",
      "th_th": "/ไตรมาส", "hi_in": "/तिमाही",
      "ar_sa": "/ربع سنوي"
    }},
    // 年度会员
    "年度会员": {{
      "zh_cn": "年度会员", "en_us": "Yearly", "zh_tw": "年度會員",
      "ja_jp": "年間会員", "ko_kr": "연간 회원", "ru_ru": "Годовая подписка",
      "es_es": "Suscripción anual", "it_it": "Abbonamento annuale", "el_gr": "Ετήσια συνδρομή",
      "th_th": "สมาชิกรายปี", "hi_in": "वार्षिक सदस्यता",
      "ar_sa": "سنوي"
    }},
    // 全年无忧，最优惠方案
    "全年无忧，最优惠方案": {{
      "zh_cn": "全年无忧，最优惠方案", "en_us": "Best value for long-term", "zh_tw": "全年無憂，最優惠方案",
      "ja_jp": "年間安心、最もお得なプラン", "ko_kr": "일년 내내 안심, 최고의 혜택", "ru_ru": "Годовая подписка, самый выгодный вариант",
      "es_es": "Sin preocupaciones durante todo el año, plan más ventajoso", "it_it": "Senza preoccupazioni per tutto l'anno, il piano più vantaggioso", "el_gr": "Χωρίς ανησυχίες όλο το χρόνο, το πιο συμφέρον πρόγραμμα",
      "th_th": "ไม่กังวลทั้งปี แผนคุ้มค่าที่สุด", "hi_in": "पूरे वर्ष चिंता मुक्त, सबसे लाभदायक प्लान",
      "ar_sa": "أفضل قيمة للمستخدمين طويل الأمد"
    }},
    // 元/年
    "元/年": {{
      "zh_cn": "元/年", "en_us": "/year", "zh_tw": "元/年",
      "ja_jp": "/年", "ko_kr": "/년", "ru_ru": "/год",
      "es_es": "/año", "it_it": "/anno", "el_gr": "/έτος",
      "th_th": "/ปี", "hi_in": "/वर्ष",
      "ar_sa": "/سنة"
    }},
    // 暂不订阅，支持下作者
    "❤️ 暂不订阅，支持下作者": {{
      "zh_cn": "❤️ 暂不订阅，支持下作者", "en_us": "❤️ Not now, support the author", "zh_tw": "❤️ 暫不訂閱，支持下作者",
      "ja_jp": "❤️ 今は購読しない、作者を支援", "ko_kr": "❤️ 지금은 구독 안 함, 작가 지원", "ru_ru": "❤️ Пока не оформляйте подписку, поддержите автора",
      "es_es": "❤️ No ahora, apoye al autor", "it_it": "❤️ Non ora, sostieni l'autore", "el_gr": "❤️ Όχι τώρα, υποστηρίξτε τον δημιουργό",
      "th_th": "❤️ ไม่ตอนนี้ สนับสนุนผู้เขียน", "hi_in": "❤️ अभी नहीं, लेखक का समर्थन करें",
      "ar_sa": "❤️ ليس الآن، ادعم المؤلف"
    }},
    // 返回
    "返回": {{
      "zh_cn": "返回", "en_us": "Back", "zh_tw": "返回",
      "ja_jp": "戻る", "ko_kr": "뒤로", "ru_ru": "Назад",
      "es_es": "Atrás", "it_it": "Indietro", "el_gr": "Πίσω",
      "th_th": "กลับ", "hi_in": "वापस",
      "ar_sa": "رجوع"
    }},
    // 支持与打赏
    "支持与打赏": {{
      "zh_cn": "支持与打赏", "en_us": "Support & Donate", "zh_tw": "支持與打賞",
      "ja_jp": "支援と寄付", "ko_kr": "지원 및 기부", "ru_ru": "Поддержка и пожертвования",
      "es_es": "Apoyar y donar", "it_it": "Supporta e dona", "el_gr": "Υποστήριξη και δωρεά",
      "th_th": "สนับสนุนและบริจาค", "hi_in": "समर्थन और दान",
      "ar_sa": "الدعم والتبرع"
    }},
    // 感谢您的支持
    "感谢您的支持！关注作者，获取最新动态": {{
      "zh_cn": "感谢您的支持！关注作者，获取最新动态", "en_us": "Thank you for your support! Follow for updates", "zh_tw": "感謝您的支持！關注作者，獲取最新動態",
      "ja_jp": "ご支援ありがとうございます！フォローして最新情報を入手", "ko_kr": "지원해 주셔서 감사합니다! 팔로우하여 최신 소식을 받아보세요", "ru_ru": "Спасибо за поддержку! Подпишитесь для обновлений",
      "es_es": "¡Gracias por su apoyo! Síguenos para las últimas novedades", "it_it": "Grazie per il supporto! Seguici per gli aggiornamenti", "el_gr": "Ευχαριστούμε για την υποστήριξη! Ακολουθήστε για ενημερώσεις",
      "th_th": "ขอบคุณสำหรับการสนับสนุน! ติดตามเพื่อรับข่าวสารล่าสุด", "hi_in": "समर्थन के लिए धन्यवाद! अपडेट के लिए फ़ॉलो करें",
      "ar_sa": "شكراً لدعمك! تابعنا للحصول على التحديثات"
    }},
    // 关注微信公众号
    "📱 关注微信公众号": {{
      "zh_cn": "📱 关注微信公众号", "en_us": "📱 Follow WeChat Official Account", "zh_tw": "📱 關注微信公眾號",
      "ja_jp": "📱 WeChat公式アカウントをフォロー", "ko_kr": "📱 위챗 공식 계정 팔로우", "ru_ru": "📱 Подпишитесь на WeChat",
      "es_es": "📱 Siga la cuenta oficial de WeChat", "it_it": "📱 Segui la pagina ufficiale WeChat", "el_gr": "📱 Ακολουθήστε το WeChat",
      "th_th": "📱 ติดตามบัญชีทางการ WeChat", "hi_in": "📱 WeChat आधिकारिक खाते को फ़ॉलो करें",
      "ar_sa": "📱 تابع الحساب الرسمي لـ WeChat"
    }},
    // 点击查看二维码
    "点击查看二维码": {{
      "zh_cn": "点击查看二维码", "en_us": "Click to view QR code", "zh_tw": "點擊查看二維碼",
      "ja_jp": "クリックしてQRコードを見る", "ko_kr": "클릭하여 QR 코드 보기", "ru_ru": "Нажмите для просмотра QR-кода",
      "es_es": "Haga clic para ver el código QR", "it_it": "Fai clic per vedere il codice QR", "el_gr": "Κάνε κλικ για να δεις τον κωδικό QR",
      "th_th": "คลิกเพื่อดู QR โค้ด", "hi_in": "QR कोड देखने के लिए क्लिक करें",
      "ar_sa": "انقر لعرض رمز الاستجابة السريعة QR"
    }},
    // 爱发电支持
    "☕ 爱发电支持": {{
      "zh_cn": "☕ 爱发电支持", "en_us": "☕ Support on Afdian", "zh_tw": "☕ 愛發電支持",
      "ja_jp": "☕ Afdianで支援", "ko_kr": "☕ Afdian에서 지원", "ru_ru": "☕ Поддержите на Afdian",
      "es_es": "☕ Apoye en Afdian", "it_it": "☕ Sostieni su Afdian", "el_gr": "☕ Υποστηρίξτε στο Afdian",
      "th_th": "☕ สนับสนุนบน Afdian", "hi_in": "☕ Afdian पर समर्थन करें",
      "ar_sa": "☕ الدعم على Afdian"
    }},
    // 作者个人网站
    "🌐 作者个人网站": {{
      "zh_cn": "🌐 作者个人网站", "en_us": "🌐 Author's Website", "zh_tw": "🌐 作者個人網站",
      "ja_jp": "🌐 作者のウェブサイト", "ko_kr": "🌐 작가 웹사이트", "ru_ru": "🌐 Личный сайт автора",
      "es_es": "🌐 Sitio web del autor", "it_it": "🌐 Sito web dell'autore", "el_gr": "🌐 Ιστοσελίδα δημιουργού",
      "th_th": "🌐 เว็บไซต์ผู้เขียน", "hi_in": "🌐 लेखक की वेबसाइट",
      "ar_sa": "🌐 الموقع الشخصي للمؤلف"
    }},
    // 继续使用
    "继续使用": {{
      "zh_cn": "继续使用", "en_us": "Continue Using", "zh_tw": "繼續使用",
      "ja_jp": "使用を続ける", "ko_kr": "계속 사용", "ru_ru": "Продолжить использование",
      "es_es": "Continuar usando", "it_it": "Continua a usare", "el_gr": "Συνέχεια χρήσης",
      "th_th": "ใช้งานต่อ", "hi_in": "उपयोग जारी रखें",
      "ar_sa": "متابعة الاستخدام"
    }},
    // 选择支付方式
    "选择支付方式": {{
      "zh_cn": "选择支付方式", "en_us": "Select Payment Method", "zh_tw": "選擇支付方式",
      "ja_jp": "お支払い方法を選択", "ko_kr": "결제 방법 선택", "ru_ru": "Выберите способ оплаты",
      "es_es": "Seleccione el método de pago", "it_it": "Seleziona il metodo di pagamento", "el_gr": "Επίλεξε τη μέθοδο πληρωμής",
      "th_th": "เลือกวิธีการชำระเงิน", "hi_in": "भुगतान विधि चुनें",
      "ar_sa": "اختر طريقة الدفع"
    }},
    // 请选择您方便的支付渠道完成付款
    "请选择您方便的支付渠道完成付款": {{
      "zh_cn": "请选择您方便的支付渠道完成付款", "en_us": "Choose your preferred payment method", "zh_tw": "請選擇您方便的支付渠道完成付款",
      "ja_jp": "便利なお支払い方法を選択してください", "ko_kr": "선호하는 결제 방법을 선택하세요", "ru_ru": "Выберите удобный способ оплаты",
      "es_es": "Elija su método de pago preferido", "it_it": "Scegli il tuo metodo di pagamento preferito", "el_gr": "Επίλεξε την προτιμόμενη μέθοδο πληρωμής",
      "th_th": "เลือกวิธีการชำระเงินที่คุณต้องการ", "hi_in": "अपनी प Preferred भुगतान विधि चुनें",
      "ar_sa": "اختر طريقة الدفع المفضلة لديك"
    }},
    // 商品名称
    "商品名称": {{
      "zh_cn": "商品名称", "en_us": "Product", "zh_tw": "商品名稱",
      "ja_jp": "商品名", "ko_kr": "상품명", "ru_ru": "Товар",
      "es_es": "Producto", "it_it": "Prodotto", "el_gr": "Προϊόν",
      "th_th": "สินค้า", "hi_in": "उत्पाद",
      "ar_sa": "المنتج"
    }},
    // 应付金额
    "应付金额": {{
      "zh_cn": "应付金额", "en_us": "Amount Due", "zh_tw": "應付金額",
      "ja_jp": "お支払い金額", "ko_kr": "지불 금액", "ru_ru": "К оплате",
      "es_es": "Monto a pagar", "it_it": "Importo dovuto", "el_gr": "Ποσό οφειλόμενο",
      "th_th": "จำนวนที่ต้องชำระ", "hi_in": "देय राशि",
      "ar_sa": "المبلغ المستحق"
    }},
    // 其他支付方式
    "🔽 <strong>其他支付方式</strong>（银行卡、云闪付、数字人民币、PayPal 等）": {{
      "zh_cn": "🔽 <strong>其他支付方式</strong>（银行卡、云闪付、数字人民币、PayPal 等）", "en_us": "🔽 <strong>Other Payment Methods</strong> (Bank Card, UnionPay, Digital CNY, PayPal, etc.)", "zh_tw": "🔽 <strong>其他支付方式</strong>（銀行卡、雲閃付、數字人民幣、PayPal 等）",
      "ja_jp": "🔽 <strong>その他のお支払い方法</strong>（銀行カード、UnionPay、デジタル人民元、PayPal など）", "ko_kr": "🔽 <strong>기타 결제 수단</strong> (은행 카드, UnionPay, 디지털 위안화, PayPal 등)", "ru_ru": "🔽 <strong>Другие способы оплаты</strong> (Банковская карта, UnionPay, Цифровой юань, PayPal и др.)",
      "es_es": "🔽 <strong>Otros métodos de pago</strong> (Tarjeta bancaria, UnionPay, Yuan digital, PayPal, etc.)", "it_it": "🔽 <strong>Altri metodi di pagamento</strong> (Carta bancaria, UnionPay, Yuan digitale, PayPal, ecc.)", "el_gr": "🔽 <strong>Άλλοι τρόποι πληρωμής</strong> (Τραπεζική κάρτα, UnionPay, Ψηφιακός Γιουάν, PayPal, κ.λπ.)",
      "th_th": "🔽 <strong>วิธีการชำระเงินอื่นๆ</strong> (บัตรธนาคาร, UnionPay, หยวนดิจิทัล, PayPal ฯลฯ)", "hi_in": "🔽 <strong>अन्य भुगतान विधियाँ</strong> (बैंक कार्ड, UnionPay, डिजिटल युआन, PayPal, आदि)",
      "ar_sa": "🔽 <strong>طرق دفع أخرى</strong> (البطاقة المصرفية، UnionPay، اليوان الرقمي، PayPal، وغيرها)"
    }},
    // 更多支付选项
    "更多支付选项": {{
      "zh_cn": "更多支付选项", "en_us": "More Payment Options", "zh_tw": "更多支付選項",
      "ja_jp": "その他のお支払いオプション", "ko_kr": "더 많은 결제 옵션", "ru_ru": "Больше вариантов оплаты",
      "es_es": "Más opciones de pago", "it_it": "Più opzioni di pagamento", "el_gr": "Περισσότερες επιλογές πληρωμής",
      "th_th": "ตัวเลือกการชำระเงินเพิ่มเติม", "hi_in": "अधिक भुगतान विकल्प",
      "ar_sa": "خيارات دفع إضافية"
    }},
    // 请打开对应APP扫码付款
    "请打开对应 APP 扫码付款": {{
      "zh_cn": "请打开对应 APP 扫码付款", "en_us": "Open the app to scan QR code", "zh_tw": "請打開對應 APP 掃碼付款",
      "ja_jp": "アプリを開いてQRコードを読み取り支払い", "ko_kr": "앱을 열고 QR 코드를 스캔하여 결제", "ru_ru": "Откройте приложение для сканирования QR-кода",
      "es_es": "Abra la aplicación para escanear el código QR", "it_it": "Apri l'app per scansionare il codice QR", "el_gr": "Άνοιξε την εφαρμογή για να σαρώσεις τον κωδικό QR",
      "th_th": "เปิดแอปเพื่อสแกน QR โค้ด", "hi_in": "QR कोड स्कैन करने के लिए ऐप खोलें",
      "ar_sa": "افتح التطبيق لمسح رمز الاستجابة السريعة"
    }},
    // 付款说明
    "📋 付款说明": {{
      "zh_cn": "📋 付款说明", "en_us": "📋 Payment Notice", "zh_tw": "📋 付款說明",
      "ja_jp": "📋 お支払いに関する注意", "ko_kr": "📋 결제 안내", "ru_ru": "📋 Уведомление о платеже",
      "es_es": "📋 Aviso de pago", "it_it": "📋 Avviso di pagamento", "el_gr": "📋 Ειδοποίηση πληρωμής",
      "th_th": "📋 ประกาศการชำระเงิน", "hi_in": "📋 भुगतान नोटिस",
      "ar_sa": "📋 إشعار الدفع"
    }},
    // 返回选择方案
    "返回选择方案": {{
      "zh_cn": "返回选择方案", "en_us": "Back to Plans", "zh_tw": "返回選擇方案",
      "ja_jp": "プラン選択に戻る", "ko_kr": "플랜 선택으로 돌아가기", "ru_ru": "Назад к планам",
      "es_es": "Volver a los planes", "it_it": "Torna ai piani", "el_gr": "Πίσω στα προγράμματα",
      "th_th": "กลับไปที่แผน", "hi_in": "प्लान पर वापस जाएं",
      "ar_sa": "العودة إلى الخطط"
    }},
    // 我已付款，等待验证
    "✅ 我已付款，等待验证": {{
      "zh_cn": "✅ 我已付款，等待验证", "en_us": "✅ Paid, Verify Now", "zh_tw": "✅ 我已付款，等待驗證",
      "ja_jp": "✅ 支払い完了、確認待ち", "ko_kr": "✅ 결제 완료, 확인 대기", "ru_ru": "✅ Платеж выполнен, ожидайте проверки",
      "es_es": "✅ Pago realizado, verifique ahora", "it_it": "✅ Pagato, verifica ora", "el_gr": "✅ Πληρωμή ολοκληρώθηκε, περιμένετε επαλήθευση",
      "th_th": "✅ ชำระแล้ว รอการยืนยัน", "hi_in": "✅ भुगतान किया, सत्यापित करें",
      "ar_sa": "✅ تم الدفع، تحقق الآن"
    }},
    // ===== 支付渠道名称 =====
    "微信支付": {{
      "zh_cn": "微信支付", "en_us": "WeChat Pay", "zh_tw": "微信支付",
      "ja_jp": "WeChat Pay", "ko_kr": "위챗 페이", "ru_ru": "WeChat Pay",
      "es_es": "WeChat Pay", "it_it": "WeChat Pay", "el_gr": "WeChat Pay",
      "th_th": "WeChat Pay", "hi_in": "WeChat Pay",
      "ar_sa": "WeChat Pay"
    }},
    "支付宝": {{
      "zh_cn": "支付宝", "en_us": "Alipay", "zh_tw": "支付寶",
      "ja_jp": "アリペイ", "ko_kr": "알리페이", "ru_ru": "Alipay",
      "es_es": "Alipay", "it_it": "Alipay", "el_gr": "Alipay",
      "th_th": "Alipay", "hi_in": "Alipay",
      "ar_sa": "Alipay"
    }},
    "PayPal/外币": {{
      "zh_cn": "PayPal/外币", "en_us": "PayPal / Foreign Currency", "zh_tw": "PayPal/外幣",
      "ja_jp": "PayPal / 外貨", "ko_kr": "PayPal / 외화", "ru_ru": "PayPal / Иностранная валюта",
      "es_es": "PayPal / Moneda extranjera", "it_it": "PayPal / Valuta estera", "el_gr": "PayPal / Ξένο νόμισμα",
      "th_th": "PayPal / สกุลเงินต่างประเทศ", "hi_in": "PayPal / विदेशी मुद्रा",
      "ar_sa": "PayPal / عملة أجنبية"
    }},
    // 主渠道描述
    "请打开微信 APP 扫码付款": {{
      "zh_cn": "请打开微信 APP 扫码付款", "en_us": "Open WeChat App to scan QR code", "zh_tw": "請打開微信 APP 掃碼付款",
      "ja_jp": "WeChatアプリでQRコードをスキャンしてください", "ko_kr": "위챗 앱을 열어 QR코드를 스캔하세요", "ru_ru": "Откройте приложение WeChat и отсканируйте QR-код",
      "es_es": "Abre la app de WeChat para escanear el código QR", "it_it": "Apri l'app WeChat per scansionare il codice QR", "el_gr": "Ανοίξτε την εφαρμογή WeChat για να σαρώσετε τον κωδικό QR",
      "th_th": "เปิดแอป WeChat สแกน QR Code", "hi_in": "WeChat ऐप खोलें और QR कोड स्कैन करें",
      "ar_sa": "افتح تطبيق WeChat لمسح رمز QR"
    }},
    "请打开支付宝 APP 扫码付款": {{
      "zh_cn": "请打开支付宝 APP 扫码付款", "en_us": "Open Alipay App to scan QR code", "zh_tw": "請打開支付寶 APP 掃碼付款",
      "ja_jp": "アリペイアプリでQRコードをスキャンしてください", "ko_kr": "알리페이 앱을 열어 QR코드를 스캔하세요", "ru_ru": "Откройте приложение Alipay и отсканируйте QR-код",
      "es_es": "Abre la app de Alipay para escanear el código QR", "it_it": "Apri l'app Alipay per scansionare il codice QR", "el_gr": "Ανοίξτε την εφαρμογή Alipay για να σαρώσετε τον κωδικό QR",
      "th_th": "เปิดแอป Alipay สแกน QR Code", "hi_in": "Alipay ऐप खोलें और QR कोड स्कैन करें",
      "ar_sa": "افتح تطبيق Alipay لمسح رمز QR"
    }},
    "PayPal 及海外常用支付方式": {{
      "zh_cn": "PayPal 及海外常用支付方式", "en_us": "PayPal and international payment", "zh_tw": "PayPal 及海外常用支付方式",
      "ja_jp": "PayPal および海外決済方法", "ko_kr": "PayPal 및 해외 결제 방식", "ru_ru": "PayPal и международные платежи",
      "es_es": "PayPal y pagos internacionales", "it_it": "PayPal e pagamenti internazionali", "el_gr": "PayPal και διεθνείς πληρωμές",
      "th_th": "PayPal และช่องทางชำระเงินระหว่างประเทศ", "hi_in": "PayPal और अंतर्राष्ट्रीय भुगतान",
      "ar_sa": "PayPal والمدفوعات الدولية"
    }},
    // ===== 其他支付渠道名称 =====
    "银行卡支付": {{
      "zh_cn": "银行卡支付", "en_us": "Bank Card", "zh_tw": "銀行卡支付",
      "ja_jp": "銀行カード", "ko_kr": "은행 카드", "ru_ru": "Банковская карта",
      "es_es": "Tarjeta bancaria", "it_it": "Carta bancaria", "el_gr": "Τραπεζική κάρτα",
      "th_th": "บัตรธนาคาร", "hi_in": "बैंक कार्ड",
      "ar_sa": "البطاقة المصرفية"
    }},
    "云闪付": {{
      "zh_cn": "云闪付", "en_us": "UnionPay", "zh_tw": "雲閃付",
      "ja_jp": "銀聯（ユニオンペイ）", "ko_kr": "UnionPay", "ru_ru": "UnionPay",
      "es_es": "UnionPay", "it_it": "UnionPay", "el_gr": "UnionPay",
      "th_th": "UnionPay", "hi_in": "UnionPay",
      "ar_sa": "UnionPay"
    }},
    "数字人民币": {{
      "zh_cn": "数字人民币", "en_us": "Digital CNY", "zh_tw": "數字人民幣",
      "ja_jp": "デジタル人民元", "ko_kr": "디지털 인민폐", "ru_ru": "Цифровой юань",
      "es_es": "Yuan digital", "it_it": "Yuan digitale", "el_gr": "Ψηφιακό CNY",
      "th_th": "ดิจิทัลหยวน", "hi_in": "डिजिटल CNY",
      "ar_sa": "اليوان الرقمي"
    }},
    "抖音支付": {{
      "zh_cn": "抖音支付", "en_us": "Douyin Pay", "zh_tw": "抖音支付",
      "ja_jp": "Douyin Pay", "ko_kr": "Douyin Pay", "ru_ru": "Douyin Pay",
      "es_es": "Douyin Pay", "it_it": "Douyin Pay", "el_gr": "Douyin Pay",
      "th_th": "Douyin Pay", "hi_in": "Douyin Pay",
      "ar_sa": "Douyin Pay"
    }},
    // 其他渠道描述
    "请使用银行卡扫码或转账": {{
      "zh_cn": "请使用银行卡扫码或转账", "en_us": "Bank card payment or transfer", "zh_tw": "請使用銀行卡掃碼或轉賬",
      "ja_jp": "銀行カードでのスキャンまたは振込", "ko_kr": "은행카드 QR 스캔 또는 계좌이체", "ru_ru": "Оплата банковской картой или перевод",
      "es_es": "Pago con tarjeta o transferencia", "it_it": "Pagamento con carta o bonifico", "el_gr": "Πληρωμή με κάρτα ή τραπεζικό εμβάσμα",
      "th_th": "ชำระด้วยบัตรหรือโอนเงิน", "hi_in": "कार्ड या ट्रांसफर से भुगतान करें",
      "ar_sa": "الدفع ببطاقة بنكية أو تحويل"
    }},
    "请打开云闪付 APP 扫码付款": {{
      "zh_cn": "请打开云闪付 APP 扫码付款", "en_us": "Open UnionPay App to scan QR code", "zh_tw": "請打開雲閃付 APP 掃碼付款",
      "ja_jp": "銀聯アプリでQRコードをスキャンしてください", "ko_kr": "UnionPay 앱에서 QR코드 스캔", "ru_ru": "Откройте приложение UnionPay для сканирования QR",
      "es_es": "Abre la app de UnionPay para escanear el QR", "it_it": "Apri l'app UnionPay per scansionare il QR", "el_gr": "Ανοίξτε την εφαρμογή UnionPay για σάρωση QR",
      "th_th": "เปิดแอป UnionPay สแกน QR Code", "hi_in": "UnionPay ऐप में QR स्कैन करें",
      "ar_sa": "افتح تطبيق UnionPay لمسح رمز QR"
    }},
    "请打开数字人民币 APP 扫码付款": {{
      "zh_cn": "请打开数字人民币 APP 扫码付款", "en_us": "Open Digital CNY App to scan QR code", "zh_tw": "請打開數字人民幣 APP 掃碼付款",
      "ja_jp": "デジタル人民元アプリでQRをスキャン", "ko_kr": "디지털 인민폐 앱에서 QR코드 스캔", "ru_ru": "Откройте приложение цифрового юаня",
      "es_es": "Abre la app de Yuan digital", "it_it": "Apri l'app Yuan digitale", "el_gr": "Ανοίξτε την εφαρμογή Ψηφιακού CNY",
      "th_th": "เปิดแอปดิจิทัลหยวน สแกน QR", "hi_in": "डिजिटल CNY ऐप खोलें",
      "ar_sa": "افتح تطبيق اليوان الرقمي"
    }},
    "请打开抖音 APP 扫码付款": {{
      "zh_cn": "请打开抖音 APP 扫码付款", "en_us": "Open Douyin App to scan QR code", "zh_tw": "請打開抖音 APP 掃碼付款",
      "ja_jp": "DouyinアプリでQRをスキャン", "ko_kr": "Douyin 앱에서 QR코드 스캔", "ru_ru": "Откройте приложение Douyin",
      "es_es": "Abre la app de Douyin", "it_it": "Apri l'app Douyin", "el_gr": "Ανοίξτε την εφαρμογή Douyin",
      "th_th": "เปิดแอป Douyin สแกน QR", "hi_in": "Douyin ऐप खोलें",
      "ar_sa": "افتح تطبيق Douyin"
    }},
    // 收起其他支付方式
    "🔼 <strong>收起其他支付方式</strong>": {{
      "zh_cn": "🔼 <strong>收起其他支付方式</strong>", "en_us": "🔼 <strong>Collapse Other Methods</strong>", "zh_tw": "🔼 <strong>收起其他支付方式</strong>",
      "ja_jp": "🔼 <strong>その他の決済方法を閉じる</strong>", "ko_kr": "🔼 <strong>기타 결제 수단 접기</strong>", "ru_ru": "🔼 <strong>Свернуть другие способы</strong>",
      "es_es": "🔼 <strong>Ocultar otros métodos</strong>", "it_it": "🔼 <strong>Comprimi altri metodi</strong>", "el_gr": "🔼 <strong>Σύμπτυξη άλλων μεθόδων</strong>",
      "th_th": "🔼 <strong>ซ่อนช่องทางอื่นๆ</strong>", "hi_in": "🔼 <strong>अन्य विधियां छिपाएं</strong>",
      "ar_sa": "🔼 <strong>طي طرق الدفع الأخرى</strong>"
    }},
    // ===== 常见动态文本 =====
    "敬请期待": {{
      "zh_cn": "敬请期待", "en_us": "Coming Soon", "zh_tw": "敬請期待",
      "ja_jp": "近日公開", "ko_kr": "곧 출시", "ru_ru": "Скоро будет",
      "es_es": "Próximamente", "it_it": "Prossimamente", "el_gr": "Σύντομα",
      "th_th": "เร็วๆ นี้", "hi_in": "जल्द आ रहा है",
      "ar_sa": "قريباً"
    }},
    "扫码失败？点击此处打开付款页": {{
      "zh_cn": "扫码失败？点击此处打开付款页", "en_us": "Scan failed? Click to open payment page", "zh_tw": "掃碼失敗？點擊此處打開付款頁",
      "ja_jp": "QRスキャン失敗？ここをクリック", "ko_kr": "스캔 실패? 여기를 클릭하세요", "ru_ru": "Ошибка сканирования? Нажмите сюда",
      "es_es": "¿Fallo al escanear? Haz clic aquí", "it_it": "Scansione fallita? Clicca qui", "el_gr": "Αποτυχία σάρωσης; Πατήστε εδώ",
      "th_th": "สแกนไม่สำเร็จ? คลิกที่นี่", "hi_in": "स्कैन विफल? यहां क्लिक करें",
      "ar_sa": "فشل المسح؟ انقر هنا لفتح صفحة الدفع"
    }},
    "⚠️ 该渠道收款码暂未配置，请联系作者": {{
      "zh_cn": "⚠️ 该渠道收款码暂未配置，请联系作者", "en_us": "⚠️ QR code not configured, contact author", "zh_tw": "⚠️ 該渠道收款碼暫未配置，請聯繫作者",
      "ja_jp": "⚠️ この決済方法のQRコードは未設定です、作者に連絡ください", "ko_kr": "⚠️ 해당 채널의 QR코드가 설정되지 않았습니다, 작성자에게 문의", "ru_ru": "⚠️ QR-код не настроен, свяжитесь с автором",
      "es_es": "⚠️ Código QR no configurado, contacte al autor", "it_it": "⚠️ QR code non configurato, contatta l'autore", "el_gr": "⚠️ Ο κωδικός QR δεν έχει ρυθμιστεί, επικοινωνήστε με τον συγγραφέα",
      "th_th": "⚠️ QR Code ของช่องทางนี้ยังไม่ติดตั้ง โปรดติดต่อผู้เขียน", "hi_in": "⚠️ QR कोड कॉन्फ़िगर नहीं है, लेखक से संपर्क करें",
      "ar_sa": "⚠️ لم يتم تكوين رمز QR لهذه الطريقة، يرجى الاتصال بالمؤلف"
    }},
    // ===== 套餐商品名称（订单区域显示）=====
    "MC Skill - 月度授权": {{
      "zh_cn": "MC Skill - 月度授权", "en_us": "MC Skill - Monthly License", "zh_tw": "MC Skill - 月度授權",
      "ja_jp": "MC Skill - 月間ライセンス", "ko_kr": "MC Skill - 월간 라이선스", "ru_ru": "MC Skill - Месячная лицензия",
      "es_es": "MC Skill - Licencia mensual", "it_it": "MC Skill - Licenza mensile", "el_gr": "MC Skill - Μηνιαία άδεια",
      "th_th": "MC Skill - ใบอนุญาตรายเดือน", "hi_in": "MC Skill - मासिक लाइसेंस",
      "ar_sa": "MC Skill - ترخيص شهري"
    }},
    "MC Skill - 季度授权": {{
      "zh_cn": "MC Skill - 季度授权", "en_us": "MC Skill - Quarterly License", "zh_tw": "MC Skill - 季度授權",
      "ja_jp": "MC Skill - 3ヶ月ライセンス", "ko_kr": "MC Skill - 분기 라이선스", "ru_ru": "MC Skill - Квартальная лицензия",
      "es_es": "MC Skill - Licencia trimestral", "it_it": "MC Skill - Licenza trimestrale", "el_gr": "MC Skill - Τριμηνιαία άδεια",
      "th_th": "MC Skill - ใบอนุญาตรายไตรมาส", "hi_in": "MC Skill - तिमाही लाइसेंस",
      "ar_sa": "MC Skill - ترخيص فصلي"
    }},
    "MC Skill - 年度授权": {{
      "zh_cn": "MC Skill - 年度授权", "en_us": "MC Skill - Annual License", "zh_tw": "MC Skill - 年度授權",
      "ja_jp": "MC Skill - 年間ライセンス", "ko_kr": "MC Skill - 연간 라이선스", "ru_ru": "MC Skill - Годовая лицензия",
      "es_es": "MC Skill - Licencia anual", "it_it": "MC Skill - Licenza annuale", "el_gr": "MC Skill - Ετήσια άδεια",
      "th_th": "MC Skill - ใบอนุญาตรายปี", "hi_in": "MC Skill - वार्षिक लाइसेंस",
      "ar_sa": "MC Skill - ترخيص سنوي"
    }},
    // ===== 套餐名称（Level 2 卡片标题）=====
    "月度会员": {{
      "zh_cn": "月度会员", "en_us": "Monthly", "zh_tw": "月度會員",
      "ja_jp": "月会員", "ko_kr": "월간 회원", "ru_ru": "Месячный",
      "es_es": "Mensual", "it_it": "Mensile", "el_gr": "Μηνιαίο",
      "th_th": "รายเดือน", "hi_in": "मासिक",
      "ar_sa": "شهري"
    }},
    "季度会员": {{
      "zh_cn": "季度会员", "en_us": "Quarterly", "zh_tw": "季度會員",
      "ja_jp": "3ヶ月会員", "ko_kr": "분기 회원", "ru_ru": "Квартальный",
      "es_es": "Trimestral", "it_it": "Trimestrale", "el_gr": "Τριμηνιαίο",
      "th_th": "รายไตรมาส", "hi_in": "तिमाही",
      "ar_sa": "فصلي"
    }},
    "年度会员": {{
      "zh_cn": "年度会员", "en_us": "Yearly", "zh_tw": "年度會員",
      "ja_jp": "年会員", "ko_kr": "연간 회원", "ru_ru": "Годовой",
      "es_es": "Anual", "it_it": "Annuale", "el_gr": "Ετήσιο",
      "th_th": "รายปี", "hi_in": "वार्षिक",
      "ar_sa": "سنوي"
    }},
    // ===== 套餐描述 =====
    "适合短期体验": {{
      "zh_cn": "适合短期体验", "en_us": "Perfect for short-term use", "zh_tw": "適合短期體驗",
      "ja_jp": "短期利用に最適", "ko_kr": "단기 체험에 적합", "ru_ru": "Отлично для краткосрочного использования",
      "es_es": "Perfecto para uso a corto plazo", "it_it": "Perfetto per un utilizzo a breve termine", "el_gr": "Ιδανικό για βραχυπρόθεσμη χρήση",
      "th_th": "เหมาะสำหรับใช้ระยะสั้น", "hi_in": "अल्पावधि उपयोग के लिए बेहतरीन",
      "ar_sa": "مثالي للاستخدام قصير الأمد"
    }},
    "3个月更划算，省22元": {{
      "zh_cn": "3个月更划算，省22元", "en_us": "Save $5.00 compared to monthly", "zh_tw": "3個月更划算，省22元",
      "ja_jp": "3ヶ月プランでお得に：月換算で約5ドル節約", "ko_kr": "3개월 플랜으로 월 약 5달러 절약", "ru_ru": "3 месяца выгоднее: экономите около $5 в месяц",
      "es_es": "3 meses ahorran ~$5/mes respecto al plan mensual", "it_it": "3 mesi fanno risparmiare ~$5/mese sul piano mensile", "el_gr": "3 μήνες εξοικονομείτε ~$5/μήνα έναντι μηνιαίου",
      "th_th": "แพ็กเกจ 3 เดือนประหยัดกว่า ~$5/เดือน เทียบแผนรายเดือน", "hi_in": "3 महीने का प्लान मासिक से ~$5/महीना बचत",
      "ar_sa": "وفر 3.50 دولار مقارنةً بالخطة الشهرية"
    }},
    "全年无忧，最优惠方案": {{
      "zh_cn": "全年无忧，最优惠方案", "en_us": "Best value for long-term users", "zh_tw": "全年無憂，最優惠方案",
      "ja_jp": "1年間安心、最もお得なプラン", "ko_kr": "1년간 안심, 가장 할인된 플랜", "ru_ru": "Целый год без забот, лучшее предложение",
      "es_es": "Todo el año sin preocupaciones, la mejor oferta", "it_it": "Tutto l'anno senza pensieri, l'offerta migliore", "el_gr": "Όλο το χρόνο χωρίς ανησυχίες, η καλύτερη προσφορά",
      "th_th": "ทั้งปีไม่ต้องกังวล แพ็กเกจที่คุ้มที่สุด", "hi_in": "पूरे साल बिना चिंता, सबसे अच्छा ऑफर",
      "ar_sa": "أفضل قيمة للمستخدمين طويل الأمد"
    }},
    // ===== 付款说明列表 =====
    "✅ 付款完成后 30 分钟内自动解锁相关套餐": {{
      "zh_cn": "✅ 付款完成后 30 分钟内自动解锁相关套餐", "en_us": "✅ Access unlocked within 30 minutes after payment", "zh_tw": "✅ 付款完成後 30 分鐘內自動解鎖相關套餐",
      "ja_jp": "✅ 支払い完了後30分以内に自動的にアンロック", "ko_kr": "✅ 결제 완료 후 30분 이내 자동 잠금 해제", "ru_ru": "✅ Доступ разблокируется в течение 30 минут после оплаты",
      "es_es": "✅ Acceso desbloqueado en 30 minutos tras el pago", "it_it": "✅ Accesso sbloccato entro 30 minuti dal pagamento", "el_gr": "✅ Πρόσβαση ξεκλειδώνεται εντός 30 λεπτών μετά την πληρωμή",
      "th_th": "✅ ปลดล็อคอัตโนมัติภายใน 30 นาทีหลังชำระ", "hi_in": "✅ भुगतान के 30 मिनट के भीतर स्वतः अनलॉक",
      "ar_sa": "✅ يتم فتح الوصول تلقائياً في غضون 30 دقيقة بعد الدفع"
    }},
    "✅ 如付款后未生效，请保存支付截图联系客服": {{
      "zh_cn": "✅ 如付款后未生效，请保存支付截图联系客服", "en_us": "✅ If not activated, save payment receipt and contact support", "zh_tw": "✅ 如付款後未生效，請保存支付截圖聯繫客服",
      "ja_jp": "✅ 有効化されない場合は、スクリーンショットを保存しサポートに連絡", "ko_kr": "✅ 활성화되지 않으면 결제 내역 저장 후 고객센터에 문의", "ru_ru": "✅ Если не активировалось, сохраните чек и свяжитесь с поддержкой",
      "es_es": "✅ Si no se activa, guarde el recibo y contacte a soporte", "it_it": "✅ Se non si attiva, salva lo screenshot e contatta il supporto", "el_gr": "✅ Αν δεν ενεργοποιηθεί, αποθηκεύστε την απόδειξη και επικοινωνήστε με την υποστήριξη",
      "th_th": "✅ หากยังไม่เปิดใช้งาน ให้บันทึกใบเสร็จแล้วติดต่อสนับสนุน", "hi_in": "✅ यदि सक्रिय न हो तो भुगतान का स्क्रीनशॉट सहेजें और सहायता से संपर्क करें",
      "ar_sa": "✅ إذا لم يتم التفعيل، احفظ إيصال الدفع واتصل بالدعم"
    }},
    "✅ 更新优化：如发现功能漏洞，欢迎通过官网联系渠道或「优化建言」功能提出宝贵意见": {{
      "zh_cn": "✅ 更新优化：如发现功能漏洞，欢迎通过官网联系渠道或「优化建言」功能提出宝贵意见", "en_us": "✅ Feedback: Report bugs or suggestions via official website contact or 'Optimization Suggestion' feature", "zh_tw": "✅ 更新優化：如發現功能漏洞，歡迎通過官網聯繫渠道或「優化建言」功能提出寶貴意見",
      "ja_jp": "✅ 更新改善：不具合やご意見は公式サイトまたは「改善提案」から", "ko_kr": "✅ 업데이트 최적화: 버그나 제안은 공식 웹사이트 또는 '최적화 제안' 기능으로", "ru_ru": "✅ Обратная связь: сообщайте об ошибках через сайт или функцию 'Предложить улучшение'",
      "es_es": "✅ Comentarios: Reporta fallos a través de la web o función 'Sugerencias'", "it_it": "✅ Feedback: Segnala bug tramite sito web o funzione 'Suggerimenti'", "el_gr": "✅ Ανατροφοδότηση: Αναφέρετε σφάλματα μέσω ιστοσελίδας ή λειτουργίας 'Προτάσεις βελτιώσεων'",
      "th_th": "✅ ข้อเสนอแนะ: แจ้งปัญหาหรือข้อเสนอผ่านเว็บไซต์ทางการหรือฟีเจอร์ข้อเสนอแนะ", "hi_in": "✅ प्रतिक्रिया: आधिकारिक वेबसाइट या 'सुझाव' सुविधा के माध्यम से बग रिपोर्ट करें",
      "ar_sa": "✅ ملاحظات: أبلغ عن الأخطاء عبر الموقع الرسمي أو ميزة «اقتراح تحسين»"
    }},
    "✅ 服务说明：授权仅限个人使用，禁止转售": {{
      "zh_cn": "✅ 服务说明：授权仅限个人使用，禁止转售", "en_us": "✅ License is for personal use only, resale prohibited", "zh_tw": "✅ 服務說明：授權僅限個人使用，禁止轉售",
      "ja_jp": "✅ 利用規約：個人利用のみ、転売禁止", "ko_kr": "✅ 서비스 약관: 개인 사용만 허용, 재판매 금지", "ru_ru": "✅ Условия: Лицензия только для личного пользования, перепродажа запрещена",
      "es_es": "✅ Términos: Licencia solo para uso personal, reventa prohibida", "it_it": "✅ Termini: Licenza solo per uso personale, rivendita vietata", "el_gr": "✅ Όροι: Άδεια μόνο για προσωπική χρήση, η μεταπώληση απαγορεύεται",
      "th_th": "✅ ข้อกำหนด: สำหรับใช้ส่วนตัวเท่านั้น ห้ามนำไปขายต่อ", "hi_in": "✅ शर्तें: लाइसेंस केवल व्यक्तिगत उपयोग के लिए, पुनर्विक्रय निषिद्ध",
      "ar_sa": "✅ الشروط: الترخيص للاستخدام الشخصي فقط، يمنع إعادة البيع"
    }},
    // ===== 强制点击付款完成按钮警告 =====
    "⚠️ 付款后请务必点击下方「✅ 我已付款，等待验证」按钮，否则系统无法确认您的付款，可能导致支付失败": {{
      "zh_cn": "⚠️ 付款后请务必点击下方「✅ 我已付款，等待验证」按钮，否则系统无法确认您的付款，可能导致支付失败",
      "en_us": "⚠️ After paying, you MUST click the '✅ Paid, Verify Now' button below. Otherwise the system cannot confirm your payment, which may result in payment failure",
      "zh_tw": "⚠️ 付款後請務必點擊下方「✅ 我已付款，等待驗證」按鈕，否則系統無法確認您的付款，可能導致支付失敗",
      "ja_jp": "⚠️ 支払い後、下の「✅ 支払い完了、確認待ち」ボタンを必ずクリックしてください。クリックしないとシステムが支払いを確認できず、支払い失敗となる可能性があります",
      "ko_kr": "⚠️ 결제 후 아래의 '✅ 결제 완료, 확인 대기' 버튼을 반드시 클릭하세요. 클릭하지 않으면 시스템이 결제를 확인할 수 없어 결제 실패가 발생할 수 있습니다",
      "ru_ru": "⚠️ После оплаты ОБЯЗАТЕЛЬНО нажмите кнопку '✅ Платеж выполнен, ожидайте проверки' ниже. Иначе система не сможет подтвердить ваш платёж, что может привести к ошибке оплаты",
      "es_es": "⚠️ Después de pagar, DEBE hacer clic en el botón '✅ Pagado, verificar ahora' a continuación. De lo contrario, el sistema no puede confirmar su pago, lo que puede provocar un fallo del pago",
      "it_it": "⚠️ Dopo il pagamento, DEVI cliccare il pulsante '✅ Pagato, verifica ora' qui sotto. Altrimenti il sistema non può confermare il pagamento, il che potrebbe causare un fallimento del pagamento",
      "el_gr": "⚠️ Μετά την πληρωμή, ΠΡΕΠΕΙ να κάνετε κλικ στο κουμπί '✅ Πληρωμή ολοκληρώθηκε, περιμένετε επαλήθευση' παρακάτω. Διαφορετικά το σύστημα δεν μπορεί να επιβεβαιώσει την πληρωμή σας, κάτι που μπορεί να οδηγήσει σε αποτυχία",
      "th_th": "⚠️ หลังชำระเงิน กรุณาคลิกปุ่ม '✅ ชำระแล้ว รอการยืนยัน' ด้านล่างนี้เสมอ มิฉะนั้นระบบจะยืนยันการชำระเงินไม่ได้ อาจทำให้การชำระล้มเหลว",
      "hi_in": "⚠️ भुगतान के बाद, नीचे दिए गए '✅ भुगतान किया, सत्यापित करें' बटन पर अवश्य क्लिक करें। अन्यथा सिस्टम आपके भुगतान की पुष्टि नहीं कर सकता, जिससे भुगतान विफल हो सकता है",
      "ar_sa": "⚠️ بعد الدفع، يجب عليك النقر على زر «✅ تم الدفع، تحقق الآن» أدناه. وإلا فلن يتمكن النظام من تأكيد دفعتك، مما قد يؤدي إلى فشل الدفع"
    }},
    // ===== 禁止重复支付警告 =====
    "⚠️ 同一套餐付款成功后 24 小时内请勿重复支付，否则会导致系统数据错乱": {{
      "zh_cn": "⚠️ 同一套餐付款成功后 24 小时内请勿重复支付，否则会导致系统数据错乱",
      "en_us": "⚠️ Do not pay for the same plan again within 24 hours after a successful payment, otherwise it may cause system data confusion",
      "zh_tw": "⚠️ 同一套餐付款成功後 24 小時內請勿重複支付，否則會導致系統數據錯亂",
      "ja_jp": "⚠️ 同一プランの決済成功後24時間以内は重複して支払わないでください。そうでないとシステムデータが混乱する可能性があります",
      "ko_kr": "⚠️ 동일한 플랜 결제 성공 후 24시간 이내에는 중복 결제하지 마세요. 그렇지 않으면 시스템 데이터가 혼란스러워질 수 있습니다",
      "ru_ru": "⚠️ Не оплачивайте тот же план повторно в течение 24 часов после успешного платежа, иначе это может вызвать путаницу в данных системы",
      "es_es": "⚠️ No pague de nuevo por el mismo plan dentro de las 24 horas tras un pago exitoso, de lo contrario puede causar confusión en los datos del sistema",
      "it_it": "⚠️ Non pagare di nuovo lo stesso piano entro 24 ore dopo un pagamento riuscito, altrimenti potrebbe causare confusione nei dati di sistema",
      "el_gr": "⚠️ Μην πληρώσετε ξανά το ίδιο πρόγραμμα εντός 24 ωρών μετά από μια επιτυχημένη πληρωμή, διαφορετικά μπορεί να προκαλέσει σύγχυση στα δεδομένα του συστήματος",
      "th_th": "⚠️ หลังชำระเงินสำเร็จ อย่าชำระแพ็กเกจเดิมซ้ำภายใน 24 ชั่วโมง มิฉะนั้นอาจทำให้ข้อมูลระบบสับสน",
      "hi_in": "⚠️ सफल भुगतान के 24 घंटे के भीतर उसी योजना के लिए पुनः भुगतान न करें, अन्यथा सिस्टम डेटा में भ्रम हो सकता है",
      "ar_sa": "⚠️ لا تدفع عن نفس الخطة مرة أخرى خلال 24 ساعة بعد دفع ناجح، وإلا فقد يتسبب ذلك في ارتباك بيانات النظام"
    }}
  }};

  // Apply i18n text to all elements with data-i18n attributes
  // 支持11种语言，默认使用中文或英文
  function applyI18n() {{
    const hasCurrentLang = currentLang !== 'en_us' && currentLang !== 'zh_cn';
    
    if (hasCurrentLang) {{
      // 对于非中/英语言，从翻译字典中查找对应翻译
      document.querySelectorAll('[data-i18n-zh]').forEach(el => {{
        const zhText = el.dataset.i18nZh;
        const enText = el.dataset.i18nEn;
        // 先尝试从翻译字典查找
        if (TRANSLATIONS[zhText] && TRANSLATIONS[zhText][currentLang]) {{
          el.innerHTML = TRANSLATIONS[zhText][currentLang];
        }} else if (enText && TRANSLATIONS[enText] && TRANSLATIONS[enText][currentLang]) {{
          el.innerHTML = TRANSLATIONS[enText][currentLang];
        }} else {{
          // 降级使用英文
          el.innerHTML = enText || zhText;
        }}
      }});
    }} else {{
      // 中/英双语模式
      document.querySelectorAll('[data-i18n-zh][data-i18n-en]').forEach(el => {{
        if (currentLang === 'en_us') {{
          el.innerHTML = el.dataset.i18nEn;
        }} else {{
          el.innerHTML = el.dataset.i18nZh;
        }}
      }});
    }}
  }}

  // Toggle language between zh and en (保留兼容)
  function toggleLang() {{
    const langs = ['zh_cn', 'en_us', 'zh_tw', 'ja_jp', 'ko_kr', 'ru_ru', 'es_es', 'it_it', 'el_gr', 'th_th', 'hi_in', 'ar_sa'];
    const currentIdx = langs.indexOf(currentLang);
    const nextIdx = (currentIdx + 1) % langs.length;
    switchLang(langs[nextIdx]);
  }}

  // RTL语言列表（从右向左书写的语言）
  const RTL_LANGUAGES = ['ar_sa'];

  // Language switch function
  function switchLang(lang) {{
    if (!SUPPORTED_LANGUAGES[lang]) return;
    
    currentLang = lang;
    document.documentElement.lang = lang;
    
    // RTL 文本方向支持
    const isRtl = RTL_LANGUAGES.includes(lang);
    document.documentElement.dir = isRtl ? 'rtl' : 'ltr';
    document.body.style.direction = isRtl ? 'rtl' : 'ltr';
    if (isRtl) {{
      document.body.classList.add('rtl-mode');
    }} else {{
      document.body.classList.remove('rtl-mode');
    }}
    
    // 更新所有语言按钮显示（主区域 + 三个弹窗）
    const langLabels = ['currentLangLabel', 'currentLangLabelModal', 'currentLangLabelModal2', 'currentLangLabelModal3'];
    langLabels.forEach(id => {{
      const el = document.getElementById(id);
      if (el) {{
        el.textContent = getLangDisplayName(lang);
      }}
    }});
    
    // 更新文档标题
    const titles = {{
      'en_us': 'MC Skill - Payment Guide',
      'zh_cn': 'MC Skill - 付费引导',
      'zh_tw': 'MC Skill - 付費引導',
      'ja_jp': 'MC Skill - 支払いガイド',
      'ko_kr': 'MC Skill - 결제 가이드',
      'ru_ru': 'MC Skill - Руководство по оплате',
      'es_es': 'MC Skill - Guía de pago',
      'it_it': 'MC Skill - Guida al pagamento',
      'el_gr': 'MC Skill - Οδηγός πληρωμής',
      'th_th': 'MC Skill - คู่มือการชำระเงิน',
      'hi_in': 'MC Skill - भुगतान गाइड',
      'ar_sa': 'MC Skill - دليل الدفع'
    }};
    document.title = titles[lang] || titles['en_us'];
    
    // 更新所有静态文本
    applyI18n();
    
    // 更新套餐卡片价格
    updatePlanCardPrices();
    
    // 更新动态内容
    if (selectedPlan) {{
      updatePlanDisplay();
    }}
    renderChannelNames();
    updateOtherPaymentEntry();
    updateQRHint();
    updateNotices();
    updateToastText();
    
    // 更新所有下拉菜单选中状态
    document.querySelectorAll('.lang-dropdown').forEach(dropdown => {{
      dropdown.querySelectorAll('.lang-dropdown-item').forEach(item => {{
        item.classList.remove('selected');
      }});
      const items = dropdown.querySelectorAll('.lang-dropdown-item');
      const idx = Object.keys(SUPPORTED_LANGUAGES).indexOf(lang);
      if (idx >= 0 && items[idx]) {{
        items[idx].classList.add('selected');
      }}
    }});
    
    // 语言切换后，如果已选支付渠道则重新加载对应语言的二维码
    if (currentChannel && selectedPlan) {{
      selectChannel(currentChannel, currentChannelType);
    }}
    
    // 保存语言偏好到 localStorage
    try {{
      localStorage.setItem('mc_skill_lang', lang);
    }} catch(e) {{}}
  }}

  function updatePlanCardPrices() {{
    // 只有简体中文使用人民币，其他所有语言都使用美元
    const useUsd = !isChineseLang(currentLang);
    const priceMap = {{
      monthly:    {{ rmb: '¥8.88',   usd: '$9.99'  }},
      quarterly:  {{ rmb: '¥23.88',  usd: '$29.99' }},
      yearly:     {{ rmb: '¥88.88',  usd: '$99.99' }},
    }};
    Object.keys(priceMap).forEach(plan => {{
      const el = document.getElementById('planPrice' + plan.charAt(0).toUpperCase() + plan.slice(1));
      if (el) {{
        el.textContent = useUsd ? priceMap[plan].usd : priceMap[plan].rmb;
      }}
    }});
  }}

  function getText(zh, en) {{
    // 规则：
    // 1. 简体中文 -> 直接返回 zh
    // 2. 英文 -> 直接返回 en
    // 3. 其他9种语言 -> 先从 TRANSLATIONS 字典用 zh 作为 key 查当前语言翻译
    //    找不到再用 en 作为 key 查，再找不到降级为 en
    if (isChineseLang(currentLang)) return zh;
    if (currentLang === 'en_us') return en;
    // 其他语言：优先查 TRANSLATIONS
    if (typeof TRANSLATIONS !== 'undefined') {{
      if (TRANSLATIONS[zh] && TRANSLATIONS[zh][currentLang]) return TRANSLATIONS[zh][currentLang];
      if (TRANSLATIONS[en] && TRANSLATIONS[en][currentLang]) return TRANSLATIONS[en][currentLang];
    }}
    return en;
  }}
  
  // 获取动态文本（支持多语言）
  function getMultiLangText(texts) {{
    // texts 是一个对象，键为语言代码
    if (texts[currentLang]) return texts[currentLang];
    if (texts.en_us) return texts.en_us;
    if (texts.zh_cn) return texts.zh_cn;
    return '';
  }}

  function showLevel2() {{
    document.getElementById('level2Modal').classList.add('active');
  }}
  function hideLevel2() {{
    document.getElementById('level2Modal').classList.remove('active');
  }}
  function showLevel3() {{
    document.getElementById('level2Modal').classList.remove('active');
    document.getElementById('level3Modal').classList.add('active');
  }}
  function closeAllLevels() {{
    document.getElementById('level3Modal').classList.remove('active');
    document.getElementById('level2Modal').classList.remove('active');
    showToast();
  }}
  function showToast() {{
    const toast = document.createElement('div');
    toast.style.cssText = 'position:fixed;top:20px;left:50%;transform:translateX(-50%);background:#4caf50;color:#fff;padding:12px 24px;border-radius:8px;z-index:9999;box-shadow:0 4px 12px rgba(0,0,0,0.2);';
    toast.textContent = getText('✨ 已切回免费模式，每日免费额度继续可用', '✨ Switched to free mode. Daily quota still available');
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2500);
  }}

  function showTipQr(tipKey) {{
    const display = document.getElementById('tipQrDisplay');
    const label = document.getElementById('tipQrLabel');
    const img = document.getElementById('tipQrImg');
    const linkDiv = document.getElementById('tipQrLink');
    const qrDataUrl = tipQrs[tipKey];
    const link = authorLinks[tipKey];
    const labels = {{
      'wechat_mp': getText('微信公众号', 'WeChat Official Account'),
      'afdian': getText('爱发电', 'Afdian'),
      'website': getText('个人网站', 'Personal Website')
    }};
    label.textContent = labels[tipKey] || tipKey;
    linkDiv.innerHTML = '';

    if (qrDataUrl) {{
      img.src = qrDataUrl;
      img.style.display = 'block';
    }} else {{
      img.style.display = 'none';
    }}

    // Show link below QR if available
    if (link) {{
      const linkText = getText('点击访问', 'Visit');
      linkDiv.innerHTML = '<a href="' + link + '" target="_blank" style="color:#1976d2;text-decoration:underline;font-size:13px;">' + linkText + ' →</a>';
    }} else if (tipKey === 'wechat_mp') {{
      linkDiv.innerHTML = '<span style="color:#999;font-size:12px;">' + getText('请使用微信扫描二维码关注', 'Scan QR code with WeChat') + '</span>';
    }}

    if (qrDataUrl || link) {{
      display.classList.add('active');
    }} else {{
      alert(getText('此渠道二维码暂未配置', 'QR code not configured for this channel'));
    }}
  }}

  function selectPlan(planKey) {{
    const plan = plans[planKey];
    if (!plan) return;
    selectedPlan = planKey;
    updatePlanDisplay();
    renderMainChannels();
    renderOtherChannels();
    document.getElementById('otherPaymentSection').style.display = 'none';
    document.getElementById('otherEntry').style.display = 'block';
    document.getElementById('qrDisplay').classList.remove('active');
    currentChannel = null;
    document.getElementById('paymentModal').classList.add('active');
    // 上报选择套餐事件
    reportPaymentAction('plan_selected');
  }}

  // Machine ID (用于后端API关联，不再在UI上显示)
  const currentMachineId = '{current_machine_id}';

  function showToast2(msg) {{
    const toast = document.createElement('div');
    toast.style.cssText = 'position:fixed;top:20px;left:50%;transform:translateX(-50%);background:#4caf50;color:#fff;padding:12px 24px;border-radius:8px;z-index:9999;box-shadow:0 4px 12px rgba(0,0,0,0.2);';
    toast.textContent = msg;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2000);
  }}

  function updatePlanDisplay() {{
    const plan = plans[selectedPlan];
    if (!plan) return;
    document.getElementById('orderProduct').textContent = getText(plan.product, plan.product_en);
    
    // 货币显示规则（含语言 + 渠道双重判断）：
    // 1. 简体中文（zh_cn）：所有渠道都用 ¥ + 人民币金额
    // 2. 其他所有语言：
    //    - PayPal 渠道：用 $ + 美元金额
    //    - WeChat / AliPay 渠道：用 ¥ 符号 + 美元金额数字（打消海外用户疑虑，明确对应人民币收款）
    const usdAmount = plan.price_usd || plan.price;
    if (isChineseLang(currentLang)) {{
      // 简体中文模式：统一人民币
      document.getElementById('orderPrice').textContent = '¥' + plan.price;
    }} else if (currentChannel === 'paypal') {{
      // 非中文 + PayPal：美元符号 + 美元金额
      document.getElementById('orderPrice').textContent = '$' + usdAmount;
    }} else {{
      // 非中文 + WeChat/AliPay：人民币符号 + 美元金额数字
      document.getElementById('orderPrice').textContent = '¥' + usdAmount;
    }}
  }}

  function renderChannelNames() {{
    // Update main channel names
    document.querySelectorAll('.main-pay-card').forEach(card => {{
      const key = card.dataset.channel;
      const ch = priChannels[key];
      if (ch) {{
        const nameDiv = card.querySelector('.main-pay-name');
        if (nameDiv) nameDiv.textContent = getText(ch.name, ch.name_en);
      }}
    }});
    // Update other channel names
    document.querySelectorAll('.other-pay-item').forEach(item => {{
      const key = item.dataset.channel;
      const ch = otherChannels[key];
      if (ch) {{
        const nameDiv = item.querySelector('.other-pay-name');
        if (nameDiv) nameDiv.textContent = getText(ch.name, ch.name_en);
      }}
    }});
  }}

  function renderMainChannels() {{
    const grid = document.getElementById('mainPaymentGrid');
    grid.innerHTML = '';
    Object.entries(priChannels).forEach(([key, ch]) => {{
      const card = document.createElement('div');
      card.className = 'main-pay-card';
      card.dataset.channel = key;
      card.style.setProperty('--card-color', ch.color);
      card.style.setProperty('--card-bg', ch.bg_color);
      card.onclick = () => selectChannel(key, 'pri');
      card.innerHTML = '<div class="main-pay-icon">' + ch.icon + '</div><div class="main-pay-name">' + getText(ch.name, ch.name_en) + '</div>';
      grid.appendChild(card);
    }});
  }}

  function renderOtherChannels() {{
    const list = document.getElementById('otherPaymentList');
    list.innerHTML = '';
    Object.entries(otherChannels).forEach(([key, ch]) => {{
      const item = document.createElement('div');
      item.className = 'other-pay-item';
      item.dataset.channel = key;
      item.style.setProperty('--item-color', ch.color);
      item.style.setProperty('--item-bg', ch.bg_color);
      item.onclick = () => selectChannel(key, 'other');
      item.innerHTML = '<div class="other-pay-icon">' + ch.icon + '</div><div class="other-pay-name">' + getText(ch.name, ch.name_en) + '</div>';
      list.appendChild(item);
    }});
  }}

  function updateOtherPaymentEntry() {{
    const entry = document.getElementById('otherEntry');
    const section = document.getElementById('otherPaymentSection');
    const isExpanded = section.style.display === 'block';
    
    if (isExpanded) {{
      entry.querySelector('.other-payment-entry-text').innerHTML = 
        getText('🔼 <strong>收起其他支付方式</strong>', '🔼 <strong>Collapse Other Methods</strong>');
    }} else {{
      entry.querySelector('.other-payment-entry-text').innerHTML = 
        getText('🔽 <strong>其他支付方式</strong>（银行卡、云闪付、数字人民币、PayPal 等）', 
                '🔽 <strong>Other Payment Methods</strong> (Bank Card, UnionPay, Digital CNY, PayPal, etc.)');
    }}
  }}

  function toggleOtherPayment() {{
    const section = document.getElementById('otherPaymentSection');
    if (section.style.display === 'none') {{
      section.style.display = 'block';
    }} else {{
      section.style.display = 'none';
    }}
    updateOtherPaymentEntry();
  }}

  function updateQRHint() {{
    if (!currentChannel) return;
    const channels = currentChannelType === 'pri' ? priChannels : otherChannels;
    const ch = channels[currentChannel];
    if (ch) {{
      const qrHint = document.getElementById('qrDisplayHint');
      const qrData = currentChannelType === 'pri' ? priQrs : otherQrs;
      if (qrData[currentChannel]) {{
        qrHint.textContent = getText(ch.description, ch.description_en);
      }} else {{
        qrHint.textContent = getText('⚠️ 该渠道收款码暂未配置，请联系作者', '⚠️ QR code not configured, contact author');
      }}
    }}
  }}

  function selectChannel(channelKey, channelType) {{
    // 如果之前有QR打开，先关闭（上报qr_closed）
    if (qrOpenedAt !== null) {{
      trackQrClosed();
    }}
    
    currentChannel = channelKey;
    currentChannelType = channelType;
    const channels = channelType === 'pri' ? priChannels : otherChannels;
    const qrData = channelType === 'pri' ? priQrs : otherQrs;
    const ch = channels[channelKey];
    if (!ch) return;

    document.querySelectorAll('.main-pay-card, .other-pay-item').forEach(el => {{
      el.classList.toggle('active', el.dataset.channel === channelKey);
    }});

    // 切换渠道时同步刷新订单区域的货币和价格
    if (selectedPlan) {{
      updatePlanDisplay();
    }}

    const qrDisplay = document.getElementById('qrDisplay');
    const qrImg = document.getElementById('channelQr');
    const qrHint = document.getElementById('qrDisplayHint');
    const box = document.querySelector('.qr-image-box');
    qrDisplay.classList.add('active');
    
    // 上报选择支付方式事件（所有渠道都上报）
    reportPaymentAction('channel_selected', {{ channel: channelKey }});
    
    // 获取或创建"敬请期待"提示元素
    let comingSoonEl = box.querySelector('.coming-soon-text');
    if (!comingSoonEl) {{
      comingSoonEl = document.createElement('div');
      comingSoonEl.className = 'coming-soon-text';
      comingSoonEl.style.cssText = 'display:none;align-items:center;justify-content:center;width:100%;height:100%;font-size:20px;font-weight:700;color:#999;letter-spacing:4px;';
      box.appendChild(comingSoonEl);
    }}
    // 清理所有旧的付款链接元素（防止重复叠加）
    const qrDisplayParent = box.parentElement;
    qrDisplayParent.querySelectorAll('.payment-link-box').forEach(el => el.remove());
    // 创建"付款链接"元素（每个渠道只保留唯一的一个）
    let payLinkEl = document.createElement('div');
    payLinkEl.className = 'payment-link-box';
    payLinkEl.style.cssText = 'margin-top:14px;padding:10px 14px;background:#f5f7fa;border-radius:8px;font-size:13px;line-height:1.6;display:none;';
    qrDisplayParent.appendChild(payLinkEl);

    const isComingSoon = ch.coming_soon === true;
    // PayPal渠道：按当前选择的套餐获取二维码和链接
    let hasQrImage = !!qrData[channelKey];
    let actualQrSrc = qrData[channelKey];
    let channelName = ch.name || channelKey;
    let paypalPayLink = '';
    let paypalPriceText = '';
    if (channelKey === 'paypal' && selectedPlan) {{
      const plan = plans[selectedPlan];
      if (plan && plan.paypal_url) {{
        paypalPayLink = plan.paypal_url;
      }}
      if (plan && plan.price_usd) {{
        paypalPriceText = ' ($' + plan.price_usd + ')';
      }}
      // 优先使用套餐级专属二维码，找不到则用默认paypal二维码
      if (paypalPlanQrs && paypalPlanQrs[selectedPlan]) {{
        hasQrImage = true;
        actualQrSrc = paypalPlanQrs[selectedPlan];
      }}
    }}
    // 微信支付：按当前语言+套餐加载专属二维码，找不到则用默认微信二维码
    if (channelKey === 'wechat_pay' && selectedPlan) {{
      // 规则：只有简体中文（zh_cn）使用_cn版本（人民币金额），其他所有语言都使用_en版本（美元金额）
      const langSuffix = isChineseLang(currentLang) ? '_cn' : '_en';
      const qrKey = selectedPlan + langSuffix;
      if (wechatPlanQrs && wechatPlanQrs[qrKey]) {{
        hasQrImage = true;
        actualQrSrc = wechatPlanQrs[qrKey];
      }}
    }}
    // 支付宝：按当前语言+套餐加载专属二维码，找不到则用默认支付宝二维码
    if (channelKey === 'alipay' && selectedPlan) {{
      // 规则：只有简体中文（zh_cn）使用_cn版本（人民币金额），其他所有语言都使用_en版本（美元金额）
      const langSuffix = isChineseLang(currentLang) ? '_cn' : '_en';
      const qrKey = selectedPlan + langSuffix;
      if (alipayPlanQrs && alipayPlanQrs[qrKey]) {{
        hasQrImage = true;
        actualQrSrc = alipayPlanQrs[qrKey];
      }}
    }}

    if (isComingSoon) {{
      comingSoonEl.style.display = 'flex';
      comingSoonEl.textContent = getText('敬请期待', 'Coming Soon');
      qrImg.style.display = 'none';
      qrHint.textContent = getText(ch.description, ch.description_en);
      payLinkEl.style.display = 'none';
      payLinkEl.innerHTML = '';
    }} else if (hasQrImage) {{
      comingSoonEl.style.display = 'none';
      qrImg.src = actualQrSrc;
      qrImg.style.display = 'block';
      qrHint.textContent = getText(ch.description, ch.description_en) + paypalPriceText;
      // PayPal渠道：同时显示付款链接（扫码失败时点击跳转）
      if (channelKey === 'paypal' && paypalPayLink) {{
        const linkText = getText('扫码失败？点击此处打开付款页', 'Scan failed? Click to open payment page');
        payLinkEl.innerHTML = '<a href="' + paypalPayLink + '" target="_blank" style="color:#003087;font-weight:600;text-decoration:none;">🔗 ' + linkText + ' →</a>';
        payLinkEl.style.display = 'block';
      }} else {{
        payLinkEl.innerHTML = '';
        payLinkEl.style.display = 'none';
      }}
    }} else {{
      // 无QR图片的渠道（如银行卡、云闪付等）
      comingSoonEl.style.display = 'none';
      qrImg.style.display = 'none';
      qrHint.textContent = getText('⚠️ 该渠道收款码暂未配置，请联系作者', '⚠️ QR code not configured, contact author');
      payLinkEl.innerHTML = '';
      payLinkEl.style.display = 'none';
    }}
    
    // 所有渠道都上报QR打开事件（包括敬请期待和无图渠道）
    trackQrOpened();
    reportPaymentAction('qr_opened', {{
      channel: channelKey,
      plan: selectedPlan,
      amount: selectedPlan ? plans[selectedPlan].price : 0,
      channel_name: channelName,
      has_qr: hasQrImage,
      is_coming_soon: isComingSoon
    }});
  }}

  function closePayment() {{
    // 关闭支付页面前，上报QR关闭事件（如果QR还在显示）
    if (qrOpenedAt !== null) {{
      trackQrClosed();
    }}
    document.getElementById('paymentModal').classList.remove('active');
  }}

  async function confirmPayment() {{
    if (!selectedPlan) {{
      showToast2(getText('请先选择套餐', 'Please select a plan first'));
      return;
    }}
    if (!currentChannel) {{
      showToast2(getText('请先选择支付方式', 'Please select a payment method first'));
      return;
    }}
    
    const plan = plans[selectedPlan];
    const channel = currentChannel;
    
    // 确认付款时，先上报QR关闭事件（记录QR显示时长）
    if (qrOpenedAt !== null) {{
      trackQrClosed();
    }}
    
    const btn = event.target.closest('.btn-primary');
    const originalText = btn.textContent;
    btn.textContent = getText('正在验证付款...', 'Verifying Payment...');
    btn.disabled = true;
    
    const result = await reportPaymentAction('payment_complete', {{
      channel: channel,
      amount: plan.price,
      status: 'paid'
    }});
    
    btn.textContent = originalText;
    btn.disabled = false;
    
    if (result && result.success) {{
      if (result.auto_granted || result.granted) {{
        showSuccessModal(result);
      }} else if (result.submitted || result.status === 'pending') {{
        showVerificationModal(result);
      }} else {{
        showToast2(getText('✅ 付款信息已提交，等待验证', '✅ Payment submitted, waiting for verification'), 5000);
      }}
    }} else {{
      showToast2(getText('⚠️ 提交失败，请截图联系管理员', '⚠️ Submission failed, contact admin with screenshot'), 5000);
    }}
  }}
  
  function showVerificationModal(result) {{
    const modal = document.createElement('div');
    modal.id = 'verificationModal';
    modal.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);z-index:9999;display:flex;align-items:center;justify-content:center;';
    modal.innerHTML = `
      <div style="background:#fff;border-radius:16px;padding:40px;text-align:center;max-width:400px;">
        <div id="verifyIcon" style="font-size:48px;margin-bottom:16px;">⏳</div>
        <div id="verifyTitle" style="font-size:20px;font-weight:700;margin-bottom:12px;">${{getText('付款验证中', 'Payment Verification')}}...</div>
        <div id="verifyDesc" style="font-size:14px;color:#666;margin-bottom:20px;">
          ${{getText('系统正在通过小微商户API验证您的付款，预计1-3分钟完成', 'System is verifying your payment via merchant API, please wait 1-3 minutes')}}
        </div>
        <div style="background:#f5f5fa;border-radius:8px;padding:16px;margin-bottom:20px;text-align:left;">
          <div style="font-size:12px;color:#999;margin-bottom:8px;">${{getText('订单信息', 'Order Info')}}</div>
          <div style="font-size:13px;margin-bottom:4px;">${{result.plan_cn}} - ¥${{result.price}}</div>
          <div style="font-size:12px;color:#666;">订单号: ${{result.order_id}}</div>
          <div id="verifyStatus" style="font-size:12px;color:#1976d2;margin-top:8px;">${{getText('等待商户确认付款...', 'Waiting for merchant confirmation...')}}</div>
        </div>
        <div style="font-size:13px;color:#1976d2;margin-bottom:20px;">
          ${{getText('💡 验证成功后权限将自动开通，无需重启Skill', '💡 Access will be auto-granted upon verification')}}
        </div>
        <button onclick="document.getElementById('verificationModal').remove()" style="background:linear-gradient(90deg,#3a7bd5,#00d2ff);color:#fff;border:none;border-radius:8px;padding:12px 32px;font-size:14px;font-weight:600;cursor:pointer;">
          ${{getText('后台等待', 'Wait in Background')}}
        </button>
      </div>
    `;
    document.body.appendChild(modal);
    
    // 启动前端轮询，每5秒检查一次验证状态
    startVerificationPolling(result.order_id, result.plan_cn, result.price);
  }}
  
  async function startVerificationPolling(orderId, planCn, price) {{
    const maxAttempts = 60;  // 最多轮询60次（5分钟）
    const intervalMs = 5000;  // 每5秒一次
    let attempt = 0;
    
    while (attempt < maxAttempts) {{
      await new Promise(resolve => setTimeout(resolve, intervalMs));
      attempt++;
      
      try {{
        const response = await fetch(SERVER_URL + '/api/payment/verify-status?order_id=' + encodeURIComponent(orderId));
        const data = await response.json();
        
        const statusEl = document.getElementById('verifyStatus');
        const iconEl = document.getElementById('verifyIcon');
        const titleEl = document.getElementById('verifyTitle');
        const descEl = document.getElementById('verifyDesc');
        const modal = document.getElementById('verificationModal');
        
        if (!modal) {{
          // 用户已关闭弹窗，停止轮询
          break;
        }}
        
        if (data.status === 'granted' || data.granted) {{
          // 验证通过，权限已开通
          iconEl.textContent = '🎉';
          titleEl.textContent = getText('授权已开通！', 'Authorization Granted!');
          titleEl.style.color = '#4caf50';
          descEl.textContent = getText('付款已验证，会员权限已自动开通！', 'Payment verified, premium access auto-granted!');
          statusEl.textContent = getText('✅ 验证成功', '✅ Verified');
          statusEl.style.color = '#4caf50';
          
          // 显示成功弹窗并自动关闭
          setTimeout(() => {{
            modal.remove();
            showSuccessModal(data);
          }}, 2000);
          break;
        }} else if (data.status === 'expired') {{
          iconEl.textContent = '❌';
          titleEl.textContent = getText('验证超时', 'Verification Timeout');
          titleEl.style.color = '#f44336';
          descEl.textContent = getText('未检测到付款记录，可能未完成支付。请联系管理员或重新提交。', 'No payment detected. You may not have completed payment. Contact admin or resubmit.');
          statusEl.textContent = getText('❌ 超时', '❌ Timeout');
          statusEl.style.color = '#f44336';
          break;
        }} else if (data.status === 'verified') {{
          statusEl.textContent = getText('✅ 已验证，正在开通权限...', '✅ Verified, granting access...');
          statusEl.style.color = '#4caf50';
        }} else {{
          // 仍在验证中
          const count = data.verification_count || attempt;
          statusEl.textContent = getText('验证中... 已查询' + count + '次', 'Verifying... queried ' + count + ' times');
        }}
      }} catch (err) {{
        // 静默失败，继续轮询
      }}
    }}
  }}
  
  function showSuccessModal(result) {{
    const modal = document.createElement('div');
    modal.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);z-index:9999;display:flex;align-items:center;justify-content:center;';
    modal.innerHTML = `
      <div style="background:#fff;border-radius:16px;padding:40px;text-align:center;max-width:400px;">
        <div style="font-size:48px;margin-bottom:16px;">🎉</div>
        <div style="font-size:20px;font-weight:700;margin-bottom:12px;color:#4caf50;">${{getText('授权已开通！', 'Authorization Granted!')}}</div>
        <div style="font-size:14px;color:#666;margin-bottom:20px;">
          ${{result.plan_cn}} ${{getText('已激活', 'activated')}}
        </div>
        <div style="background:#f5f5fa;border-radius:8px;padding:16px;margin-bottom:20px;text-align:left;">
          <div style="font-size:12px;color:#999;margin-bottom:8px;">${{getText('有效期至', 'Valid Until')}}</div>
          <div style="font-size:13px;">${{result.expire_at ? new Date(result.expire_at).toLocaleDateString() : '-'}}</div>
        </div>
        <div style="font-size:13px;color:#1976d2;margin-bottom:20px;">
          ${{getText('💡 重启 Skill 即可使用会员功能', '💡 Restart Skill to activate premium features')}}
        </div>
        <button onclick="this.closest('div').parentElement.remove()" style="background:linear-gradient(90deg,#4caf50,#2e7d32);color:#fff;border:none;border-radius:8px;padding:12px 32px;font-size:14px;font-weight:600;cursor:pointer;">
          ${{getText('完成', 'Done')}}
        </button>
      </div>
    `;
    document.body.appendChild(modal);
  }}

  function updateNotices() {{
    const ul = document.getElementById('paymentNotices');
    ul.innerHTML = '';
    const keys = ['auto_unlock', 'must_click_complete', 'no_duplicate_pay', 'contact_if_not_work', 'update_notice', 'service_agreement'];
    keys.forEach(key => {{
      const zhKey = key;
      const enKey = key + '_en';
      const zhText = notices[zhKey] || '';
      const enText = notices[enKey] || zhText;
      const li = document.createElement('li');
      // 用改造后的 getText：会先查 TRANSLATIONS 字典（含9种非中/非英语言），找不到再降级
      li.textContent = getText(zhText, enText);
      ul.appendChild(li);
    }});
  }}

  function updateToastText() {{
    // Toast text is generated dynamically, handled in showToast()
  }}

  // Initialize
  applyI18n();
  updateNotices();
  
  // 页面关闭/隐藏时追踪QR状态
  document.addEventListener('visibilitychange', function() {{
    if (document.visibilityState === 'hidden' && qrOpenedAt !== null) {{
      trackQrClosed();
    }}
  }});
  
  window.addEventListener('beforeunload', function() {{
    if (qrOpenedAt !== null) {{
      trackQrClosed();
    }}
  }});
</script>
</body>
</html>"""
    return html


def show_payment_page(reason: str = "", mode: str = "auto", machine_id: str = "") -> bool:
    """显示付费引导页面（渐进式）
    
    Args:
        reason: 触发原因
        mode: 显示模式 (auto/manual)
        machine_id: 当前机器码，用于生成付款备注
    """
    try:
        _OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        # 自动获取机器码（如果没有传入）
        if not machine_id:
            try:
                from core.auth_client import get_machine_id
                machine_id = get_machine_id()
            except Exception:
                machine_id = ""
        html = _build_full_page_html(reason, machine_id)
        html_path = _OUTPUT_DIR / "payment_guide.html"
        html_path.write_text(html, encoding="utf-8")
        print(f"\n{'='*50}", flush=True)
        if mode == "auto":
            print(f"  ⚠️  您的免费额度已使用完", flush=True)
        else:
            print(f"  💎  欢迎查看会员方案", flush=True)
        if reason:
            print(f"  📌 {reason}", flush=True)
        print(f"  📂 页面路径: {html_path}", flush=True)
        print(f"\n  💡 每日仍有免费额度可用", flush=True)
        print(f"  👉 查看订阅方案解锁更多权益", flush=True)
        print(f"{'='*50}", flush=True)
        return True
    except Exception as e:
        print(f"[Error] 打开付费页面失败: {e}", flush=True)
        return False


if __name__ == "__main__":
    show_payment_page(reason="免费额度已用完，今日剩余 8 次免费额度", mode="auto")
