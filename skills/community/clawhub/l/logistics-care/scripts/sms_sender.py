#!/usr/bin/env python3
"""
电商安抚短信发送引擎
- AI生成个性化安抚话术
- 阿里云/腾讯云短信发送
- Dry-run预览模式
- HTML短信预览报告生成
"""

import json
import os
import sys
import argparse
import time
from datetime import datetime
from typing import Optional

# ============ 安抚话术模板 ============

MESSAGE_TEMPLATES = {
    "shipping_timeout": {
        "style": "致歉+解释+补偿",
        "templates": [
            "【{shop_name}】亲爱的{customer_name}，您的订单{order_id}因仓库爆单延迟发货，我们非常抱歉！预计{new_eta}前发出，为您准备了一张{compensation}元优惠券，请查收。如有问题随时联系{contact_phone}。退订回T",
            "【{shop_name}】{customer_name}您好，您购买的{product_name}因供应商备货延迟，预计{new_eta}发出。为表歉意，已为您升级{compensation}。客服{contact_phone}，退订回T",
        ],
    },
    "transit_stuck": {
        "style": "安抚+催促+感谢",
        "templates": [
            "【{shop_name}】{customer_name}您好，我们注意到您的包裹{tracking_number}物流更新稍有延迟，已联系快递公司加急处理。预计{new_eta}送达，感谢您的耐心等待！有问题联系{contact_phone}。退订回T",
            "【{shop_name}】亲爱的{customer_name}，您的{product_name}已催促快递优先派送，最新物流显示预计{new_eta}到达。为您带来的不便深表歉意！客服{contact_phone}，退订回T",
        ],
    },
    "delivery_problem": {
        "style": "紧急通知+方案+致歉",
        "templates": [
            "【{shop_name}】{customer_name}您好，非常抱歉通知您订单{order_id}的包裹在运输中出现异常，我们已紧急联系快递核实。若{deadline}未解决将为您补发或全额退款。客服{contact_phone}，退订回T",
            "【{shop_name}】紧急通知：您的{product_name}物流异常，我们已启动应急流程，将在{deadline}前给出解决方案。如需退款请回复客服{contact_phone}。给您添麻烦了！退订回T",
        ],
    },
    "estimated_late": {
        "style": "温和提醒+更新+服务",
        "templates": [
            "【{shop_name}】{customer_name}您好，您的包裹{tracking_number}因{cause}可能延迟{delay_days}天到达，最新预计{new_eta}。我们持续为您跟进物流，随时可联系{contact_phone}查询。感谢理解！退订回T",
            "【{shop_name}】温馨提醒：您购买的{product_name}因{cause}，预计{cause}天送达。如有急需可联系客服{contact_phone}协调。感谢您的支持！退订回T",
        ],
    },
    "no_tracking": {
        "style": "解释+确认+跟进",
        "templates": [
            "【{shop_name}】{customer_name}您好，您订单{order_id}的物流信息暂未更新，我们正在核实发货情况，确认后第一时间通知您。如有疑问联系{contact_phone}。退订回T",
        ],
    },
    "api_failed": {
        "style": "通用提醒",
        "templates": [
            "【{shop_name}】{customer_name}您好，关于您的订单{order_id}，我们注意到物流可能存在延迟。已安排专人跟进处理，稍后客服会主动联系您。客服电话{contact_phone}，退订回T",
        ],
    },
}

# 默认店铺配置
DEFAULT_SHOP_CONFIG = {
    "shop_name": "小店",
    "contact_phone": "400-000-0000",
    "compensation": "5",
    "deadline": "48小时",
    "delay_days": "1-2",
    "cause": "物流高峰",
}


# ============ AI 话术生成（利用 LLM） ============

def generate_message_ai(delay_info: dict, order: dict, shop_config: dict) -> str:
    """
    使用规则+模板生成安抚短信，可在WorkBuddy上下文中进一步增强
    返回格式化的短信文本
    """
    rule = delay_info.get("rule", "api_failed")
    templates = MESSAGE_TEMPLATES.get(rule, MESSAGE_TEMPLATES["api_failed"])
    
    # 填充变量
    vars_dict = {**shop_config, **order}
    template = templates["templates"][0]  # 使用第一个模板
    
    try:
        message = template.format(**vars_dict)
    except KeyError:
        # 回退到基础模板
        message = f"【{shop_config['shop_name']}】{order.get('customer_name', '尊敬的客户')}您好，关于您的订单{order.get('order_id', '')}，物流可能有延迟，我们会尽快处理。客服{shop_config['contact_phone']}，退订回T"
    
    # 确保70字以内
    if len(message) > 70:
        message = message[:67] + "..."
    
    return message


def generate_message_advanced(order_result: dict, shop_config: dict) -> dict:
    """
    高级话术生成：根据延迟类型和严重程度选择最佳模板
    
    Returns:
        {
            "message": str,
            "delay_type": str,
            "style": str,
            "char_count": int,
        }
    """
    delays = order_result.get("delays", [])
    order = {
        "order_id": order_result.get("order_id", ""),
        "customer_name": order_result.get("customer_name", "尊敬的客户"),
        "tracking_number": order_result.get("tracking_number", ""),
        "product_name": order_result.get("product_name", "商品"),
    }
    
    if not delays:
        return {
            "message": "",
            "delay_type": "normal",
            "style": "无需发送",
            "char_count": 0,
        }
    
    # 取最严重的延迟
    primary_delay = delays[0]
    
    # 根据延迟类型动态生成变量
    tracking = order_result.get("tracking", {})
    new_eta = tracking.get("estimated_delivery", "近日")
    
    enhanced_vars = {
        **shop_config,
        **order,
        "new_eta": new_eta,
        "tracking_number": order.get("tracking_number", ""),
    }
    
    message = generate_message_ai(primary_delay, enhanced_vars, shop_config)
    
    return {
        "message": message,
        "delay_type": primary_delay.get("rule", "unknown"),
        "delay_name": primary_delay.get("name", "未知"),
        "style": MESSAGE_TEMPLATES.get(primary_delay.get("rule", ""), {}).get("style", "通用"),
        "char_count": len(message),
        "severity": primary_delay.get("severity", "low"),
    }


# ============ 短信发送 ============

def send_sms_aliyun(phone: str, message: str, config: dict) -> dict:
    """
    通过阿里云短信发送
    
    Args:
        phone: 手机号
        message: 短信内容（模板变量方式）
        config: {"access_key_id": "", "access_key_secret": "", "sign_name": "", "template_code": ""}
    
    Returns:
        {"success": bool, "message_id": str, "error": str}
    """
    try:
        from alibabacloud_dysmsapi20170525.client import Client as DysmsapiClient
        from alibabacloud_dysmsapi20170525 import models as dysmsapi_models
        from alibabacloud_tea_openapi import models as open_api_models
    except ImportError:
        return {
            "success": False,
            "message_id": "",
            "error": "未安装阿里云短信SDK。安装: pip install alibabacloud_dysmsapi20170525",
        }
    
    required = ["access_key_id", "access_key_secret", "sign_name", "template_code"]
    missing = [k for k in required if not config.get(k)]
    if missing:
        return {"success": False, "message_id": "", "error": f"缺少配置: {', '.join(missing)}"}
    
    try:
        client_config = open_api_models.Config(
            access_key_id=config["access_key_id"],
            access_key_secret=config["access_key_secret"],
        )
        client_config.endpoint = "dysmsapi.aliyuncs.com"
        client = DysmsapiClient(client_config)
        
        request = dysmsapi_models.SendSmsRequest(
            phone_numbers=phone,
            sign_name=config["sign_name"],
            template_code=config["template_code"],
            template_param=json.dumps({"content": message}),
        )
        
        response = client.send_sms(request)
        if response.body.code == "OK":
            return {"success": True, "message_id": response.body.biz_id, "error": None}
        else:
            return {"success": False, "message_id": "", "error": f"{response.body.code}: {response.body.message}"}
    
    except Exception as e:
        return {"success": False, "message_id": "", "error": str(e)}


def send_sms_tencent(phone: str, message: str, config: dict) -> dict:
    """
    通过腾讯云短信发送
    
    Args:
        config: {"secret_id": "", "secret_key": "", "sdk_app_id": "", "template_id": "", "sign_name": ""}
    """
    try:
        from tencentcloud.common import credential
        from tencentcloud.sms.v20210111 import sms_client, models
    except ImportError:
        return {
            "success": False, "message_id": "",
            "error": "未安装腾讯云短信SDK。安装: pip install tencentcloud-sdk-python",
        }
    
    required = ["secret_id", "secret_key", "sdk_app_id", "template_id", "sign_name"]
    missing = [k for k in required if not config.get(k)]
    if missing:
        return {"success": False, "message_id": "", "error": f"缺少配置: {', '.join(missing)}"}
    
    try:
        cred = credential.Credential(config["secret_id"], config["secret_key"])
        client = sms_client.SmsClient(cred, "ap-guangzhou")
        
        req = models.SendSmsRequest()
        req.SmsSdkAppId = config["sdk_app_id"]
        req.SignName = config["sign_name"]
        req.TemplateId = config["template_id"]
        req.TemplateParamSet = [message]
        req.PhoneNumberSet = [f"+86{phone}"]
        
        resp = client.SendSms(req)
        result = json.loads(resp.to_json_string())
        
        if result["SendStatusSet"][0]["Code"] == "Ok":
            return {"success": True, "message_id": result["SendStatusSet"][0].get("SerialNo", ""), "error": None}
        else:
            return {"success": False, "message_id": "", "error": result["SendStatusSet"][0].get("Message", "未知错误")}
    
    except Exception as e:
        return {"success": False, "message_id": "", "error": str(e)}


# ============ HTML 预览报告 ============

def generate_preview_html(results: dict, shop_config: dict) -> str:
    """生成短信预览HTML报告"""
    orders = results.get("orders", [])
    delayed_orders = [o for o in orders if o.get("has_delay")]
    
    # 生成订单行
    order_rows = ""
    for o in orders:
        tracking = o.get("tracking", {})
        delays = o.get("delays", [])
        msg_info = generate_message_advanced(o, shop_config) if o.get("has_delay") else {}
        
        delay_tags = ""
        for d in delays:
            delay_tags += f'<span class="tag tag-{d["severity"]}">{d["icon"]} {d["name"]}</span>'
        
        status_class = {
            "normal": "status-ok",
            "delayed_high": "status-danger",
            "delayed_medium": "status-warn",
            "delayed_low": "status-info",
            "unknown": "status-muted",
        }.get(o.get("overall_status", "unknown"), "status-muted")
        
        status_text = {
            "normal": "✅ 正常",
            "delayed_high": "🔴 高风险延迟",
            "delayed_medium": "🟡 中风险延迟",
            "delayed_low": "🟢 低风险",
            "unknown": "❓ 未知",
        }.get(o.get("overall_status", "unknown"), "❓")
        
        sms_preview = ""
        if msg_info.get("message"):
            sms_preview = f"""
            <div class="sms-preview">
                <strong>📱 短信预览（{msg_info.get('char_count', 0)}字）:</strong>
                <div class="sms-content">{msg_info.get('message', '')}</div>
            </div>"""
        
        order_rows += f"""
        <tr class="{status_class}">
            <td>{o.get('order_id', '')}</td>
            <td>{o.get('customer_name', '-')}</td>
            <td>{o.get('tracking_number', '')}</td>
            <td>{tracking.get('status', '-')}</td>
            <td>{tracking.get('carrier', '-')}</td>
            <td>{delay_tags if delay_tags else '<span class="tag tag-ok">✅ 无异常</span>'}</td>
            <td><span class="badge {status_class}">{status_text}</span></td>
        </tr>
        <tr class="sms-row">
            <td colspan="7">{sms_preview}</td>
        </tr>"""
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>物流延迟检测 & 安抚短信预览</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f5f7fa; color: #333; padding: 20px; }}
.container {{ max-width: 1200px; margin: 0 auto; }}
.header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 12px; margin-bottom: 24px; }}
.header h1 {{ font-size: 24px; margin-bottom: 8px; }}
.header .meta {{ opacity: 0.85; font-size: 14px; }}
.stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-bottom: 24px; }}
.stat-card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); text-align: center; }}
.stat-card .num {{ font-size: 32px; font-weight: 700; }}
.stat-card .label {{ color: #666; font-size: 13px; margin-top: 4px; }}
.stat-card.danger .num {{ color: #e53e3e; }}
.stat-card.warn .num {{ color: #d69e2e; }}
.stat-card.success .num {{ color: #38a169; }}
.section {{ background: white; border-radius: 10px; padding: 24px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
.section h2 {{ font-size: 18px; margin-bottom: 16px; color: #2d3748; }}
table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
th {{ background: #f7fafc; padding: 12px 10px; text-align: left; font-weight: 600; color: #4a5568; border-bottom: 2px solid #e2e8f0; }}
td {{ padding: 10px; border-bottom: 1px solid #edf2f7; }}
tr:hover {{ background: #f7fafc; }}
.tag {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; margin: 2px; }}
.tag-high {{ background: #fed7d7; color: #c53030; }}
.tag-medium {{ background: #fefcbf; color: #975a16; }}
.tag-low {{ background: #c6f6d5; color: #276749; }}
.tag-ok {{ background: #e2e8f0; color: #4a5568; }}
.badge {{ display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; }}
.status-ok {{ }}
.status-danger {{ background: #fff5f5; }}
.status-warn {{ background: #fffff0; }}
.status-info {{ background: #f0fff4; }}
.status-muted {{ background: #f7fafc; color: #a0aec0; }}
.badge.status-ok {{ background: #c6f6d5; color: #276749; }}
.badge.status-danger {{ background: #fed7d7; color: #c53030; }}
.badge.status-warn {{ background: #fefcbf; color: #975a16; }}
.badge.status-info {{ background: #bee3f8; color: #2b6cb0; }}
.sms-preview {{ margin-top: 8px; padding: 12px; background: #f0fff4; border-left: 3px solid #38a169; border-radius: 4px; font-size: 13px; }}
.sms-content {{ margin-top: 6px; padding: 8px 12px; background: white; border: 1px solid #c6f6d5; border-radius: 4px; font-family: monospace; word-break: break-all; }}
.sms-row td {{ padding: 4px 10px 12px; border-bottom: 2px solid #e2e8f0; }}
.footer {{ text-align: center; color: #a0aec0; font-size: 12px; padding: 20px; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>📦 物流延迟检测 & 安抚短信预览</h1>
    <div class="meta">生成时间: {results.get('generated_at', '')} | 店铺: {shop_config.get('shop_name', '')}</div>
  </div>
  
  <div class="stats">
    <div class="stat-card">
      <div class="num">{results.get('total_orders', 0)}</div>
      <div class="label">总订单数</div>
    </div>
    <div class="stat-card success">
      <div class="num">{results.get('success_count', 0)}</div>
      <div class="label">查询成功</div>
    </div>
    <div class="stat-card {'danger' if results.get('delayed_count', 0) > 0 else ''}">
      <div class="num">{results.get('delayed_count', 0)}</div>
      <div class="label">延迟风险</div>
    </div>
    <div class="stat-card">
      <div class="num">{results.get('total_orders', 0) - results.get('delayed_count', 0)}</div>
      <div class="label">正常订单</div>
    </div>
  </div>

  <div class="section">
    <h2>📋 订单详情 & 短信预览</h2>
    <table>
      <thead>
        <tr>
          <th>订单号</th>
          <th>客户</th>
          <th>运单号</th>
          <th>物流状态</th>
          <th>快递公司</th>
          <th>检测结果</th>
          <th>状态</th>
        </tr>
      </thead>
      <tbody>
        {order_rows}
      </tbody>
    </table>
  </div>
  
  <div class="footer">
    物流延迟检测技能 · 数据来源UAPI
  </div>
</div>
</body>
</html>"""
    
    return html


# ============ 主流程 ============

def process_sms(results: dict, mode: str, provider: str, sms_config: dict, shop_config: dict) -> dict:
    """
    处理短信生成和发送
    
    Args:
        results: logistics_checker 的输出结果
        mode: "dry-run" | "send"
        provider: "aliyun" | "tencent"
        sms_config: 短信服务商配置
        shop_config: 店铺信息配置
    
    Returns:
        处理结果
    """
    sms_results = {
        "mode": mode,
        "provider": provider,
        "generated_at": datetime.now().isoformat(),
        "total_delayed": results.get("delayed_count", 0),
        "sent_count": 0,
        "fail_count": 0,
        "messages": [],
    }
    
    orders = results.get("orders", [])
    delayed_orders = [o for o in orders if o.get("has_delay")]
    
    print(f"\n📱 生成安抚短信 ({mode}模式)...")
    print(f"   延迟订单: {len(delayed_orders)} 条")
    
    for order in delayed_orders:
        msg_info = generate_message_advanced(order, shop_config)
        
        if not msg_info.get("message"):
            continue
        
        msg_record = {
            "order_id": order["order_id"],
            "customer_name": order.get("customer_name", ""),
            "customer_phone": order.get("customer_phone", ""),
            "message": msg_info["message"],
            "delay_type": msg_info["delay_type"],
            "char_count": msg_info["char_count"],
            "severity": msg_info["severity"],
            "sent": False,
            "send_result": None,
        }
        
        if mode == "send":
            print(f"\n   → 发送至 {order.get('customer_phone', '')}: {msg_info['message'][:30]}...")
            
            if provider == "aliyun":
                result = send_sms_aliyun(order["customer_phone"], msg_info["message"], sms_config)
            elif provider == "tencent":
                result = send_sms_tencent(order["customer_phone"], msg_info["message"], sms_config)
            else:
                result = {"success": False, "error": f"不支持的短信服务商: {provider}"}
            
            msg_record["sent"] = result["success"]
            msg_record["send_result"] = result
            
            if result["success"]:
                sms_results["sent_count"] += 1
                print(f"   ✅ 发送成功 (ID: {result.get('message_id', 'N/A')})")
            else:
                sms_results["fail_count"] += 1
                print(f"   ❌ 发送失败: {result.get('error', '')}")
            
            # 发送间隔（阿里云限流3000次/秒，保守1秒1条）
            time.sleep(1)
        else:
            print(f"   📝 [{msg_info['severity'].upper()}] {order['order_id']}: {msg_info['message'][:50]}...")
        
        sms_results["messages"].append(msg_record)
    
    # 打印总结
    print(f"\n📊 短信处理完成:")
    print(f"   生成话术: {len(sms_results['messages'])} 条")
    if mode == "send":
        print(f"   发送成功: {sms_results['sent_count']} 条")
        print(f"   发送失败: {sms_results['fail_count']} 条")
    else:
        print(f"   (dry-run模式，未真实发送)")
    
    return sms_results


def main():
    parser = argparse.ArgumentParser(description="电商安抚短信发送引擎")
    parser.add_argument("--input", "-i", required=True, help="物流检测结果JSON文件")
    parser.add_argument("--mode", "-m", choices=["dry-run", "send"], default="dry-run", help="运行模式")
    parser.add_argument("--provider", choices=["aliyun", "tencent"], default="aliyun", help="短信服务商")
    parser.add_argument("--output", "-o", default="sms_preview.html", help="HTML预览报告输出路径")
    parser.add_argument("--config", "-c", help="短信配置JSON文件路径")
    parser.add_argument("--shop-name", default="小店", help="店铺名称")
    parser.add_argument("--contact-phone", default="400-000-0000", help="客服电话")
    parser.add_argument("--compensation", default="5", help="默认补偿金额/类型")
    
    args = parser.parse_args()
    
    # 读取物流检测结果
    with open(args.input, "r", encoding="utf-8") as f:
        results = json.load(f)
    
    # 店铺配置
    shop_config = {
        **DEFAULT_SHOP_CONFIG,
        "shop_name": args.shop_name,
        "contact_phone": args.contact_phone,
        "compensation": args.compensation,
    }
    
    # 短信配置
    sms_config = {}
    if args.config:
        with open(args.config, "r", encoding="utf-8") as f:
            sms_config = json.load(f)
    elif args.mode == "send":
        # 从环境变量读取
        if args.provider == "aliyun":
            sms_config = {
                "access_key_id": os.environ.get("ALIYUN_ACCESS_KEY_ID", ""),
                "access_key_secret": os.environ.get("ALIYUN_ACCESS_KEY_SECRET", ""),
                "sign_name": os.environ.get("SMS_SIGN_NAME", ""),
                "template_code": os.environ.get("SMS_TEMPLATE_CODE", ""),
            }
        else:
            sms_config = {
                "secret_id": os.environ.get("TENCENT_SECRET_ID", ""),
                "secret_key": os.environ.get("TENCENT_SECRET_KEY", ""),
                "sdk_app_id": os.environ.get("TENCENT_SMS_APP_ID", ""),
                "template_id": os.environ.get("TENCENT_SMS_TEMPLATE_ID", ""),
                "sign_name": os.environ.get("SMS_SIGN_NAME", ""),
            }
    
    if args.mode == "send" and not any(sms_config.values()):
        print("❌ 发送模式需要短信配置。请通过 --config 提供JSON配置文件，或设置环境变量。")
        print("   dry-run模式不需要配置，可先预览短信内容。")
        sys.exit(1)
    
    # 处理短信
    sms_results = process_sms(results, args.mode, args.provider, sms_config, shop_config)
    
    # 生成HTML预览
    html = generate_preview_html(results, shop_config)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\n📄 HTML报告已生成: {args.output}")
    
    # 保存短信结果
    sms_output = args.output.replace(".html", "_sms.json")
    with open(sms_output, "w", encoding="utf-8") as f:
        json.dump(sms_results, f, ensure_ascii=False, indent=2)
    print(f"📄 短信结果已保存: {sms_output}")


if __name__ == "__main__":
    main()
