#!/usr/bin/env python3
"""
本地通推荐 → 飞书卡片格式化
将搜索结果格式化为飞书原生卡片
"""
import json
import sys
import os

# 使用技能目录下的本地模块
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
from feishu_card import send_card

def build_guide_card(items, location, item_type, sources):
    """构建本地通推荐卡片"""
    
    elements = []
    
    # 停车场类型使用不同的标题
    if item_type == "停车":
        title_text = f"🚗 {location} 停车场推荐"
        intro_text = f"根据官方信息和本地车主反馈，为您整理以下停车选择："
    else:
        title_text = f"🎯 {location} 本地通推荐 - {item_type}"
        intro_text = f"根据官方推荐（{sources}）和本地口碑，为您精选以下地道{item_type}："
    
    # 说明段
    elements.append({
        "tag": "div",
        "text": {"tag": "lark_md", "content": intro_text}
    })
    elements.append({"tag": "hr"})
    
    # 按分类组织推荐
    categories = {}
    for item in items:
        cat = item.get("category", "其他推荐")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)
    
    # 渲染每个分类
    for category, category_items in categories.items():
        # 分类标题
        emoji = "🏆" if "官方" in category else "🏅" if "口碑" in category else "📍"
        elements.append({
            "tag": "div",
            "text": {"tag": "lark_md", "content": f"**{emoji} {category}**"}
        })
        
        # 每个推荐
        for idx, item in enumerate(category_items, 1):
            # 名称和星级
            stars = "⭐" * item.get("stars", 2)
            elements.append({
                "tag": "div",
                "text": {"tag": "lark_md", "content": f"**{idx}. {item['name']}** {stars}"}
            })
            
            # 基本信息
            info_lines = []
            if item.get("address"):
                info_lines.append(f"📍 **位置**：{item['address']}")
            if item.get("phone"):
                info_lines.append(f"📞 **电话**：{item['phone']}")
            if item.get("navigation"):
                info_lines.append(f"🗺️ **导航**：{item['navigation']}")
            
            # 停车场专用字段
            if item_type == "停车":
                if item.get("spaces"):
                    info_lines.append(f"🅿️ **车位数量**：{item['spaces']}")
                if item.get("hour_rate"):
                    info_lines.append(f"💰 **每小时费用**：{item['hour_rate']}")
                if item.get("first_hour") and item.get("after_hour"):
                    info_lines.append(f"📋 **收费标准**：首小时{item['first_hour']}，后续{item['after_hour']}")
                elif item.get("hour_rate"):
                    info_lines.append(f"📋 **收费标准**：{item['hour_rate']}")
                if item.get("daily_cap"):
                    info_lines.append(f"📊 **全天封顶**：{item['daily_cap']}")
                if item.get("free_time"):
                    info_lines.append(f"🎁 **免费时长**：{item['free_time']}")
                if item.get("charging"):
                    info_lines.append(f"🔌 **充电桩**：{item['charging']}")
            
            # 通用字段
            if item.get("hours"):
                info_lines.append(f"⏰ **营业时间**：{item['hours']}")
            if item.get("price"):
                info_lines.append(f"💰 **人均消费**：{item['price']}")
            
            if info_lines:
                elements.append({
                    "tag": "div",
                    "text": {"tag": "lark_md", "content": "\n".join(info_lines)}
                })
            
            # 推荐理由
            if item.get("reasons"):
                reasons_text = "\n".join([f"• {r}" for r in item["reasons"]])
                elements.append({
                    "tag": "div",
                    "text": {"tag": "lark_md", "content": f"✨ **推荐理由**：\n{reasons_text}"}
                })
            
            # 避雷参考
            if item.get("warnings"):
                warnings_text = "\n".join([f"• {w}" for w in item["warnings"]])
                elements.append({
                    "tag": "div",
                    "text": {"tag": "lark_md", "content": f"⚠️ **避雷参考**：\n{warnings_text}"}
                })
            
            # 分隔线（最后一个不加）
            if idx < len(category_items):
                elements.append({"tag": "hr"})
        
        # 分类之间的分隔
        elements.append({"tag": "hr"})
    
    # 温馨提示
    elements.append({
        "tag": "div",
        "text": {"tag": "lark_md", "content": "**📝 温馨提示**"}
    })
    
    tips = [
        "**官方认证优先**：优先推荐政府文旅、旅游局认证的地方",
        "**避开高峰**：建议避开周末和节假日高峰期",
        "**提前确认**：建议前往前电话确认营业状态",
        "**交通建议**：建议自驾或打车，部分地方位置较偏",
        "**支付方式**：建议提前确认支付方式，部分老店只收现金"
    ]
    
    for tip in tips:
        elements.append({
            "tag": "div",
            "text": {"tag": "lark_md", "content": tip}
        })
    
    elements.append({"tag": "hr"})
    
    # 来源说明
    elements.append({
        "tag": "note",
        "elements": [{
            "tag": "plain_text",
            "content": f"搜索来源：{sources}（已排除大众点评、美团、携程等商业平台）"
        }]
    })
    
    # 构建完整卡片
    card = {
        "config": {"wide_screen_mode": True},
        "header": {
            "template": "blue",
            "title": {
                "tag": "plain_text",
                "content": f"🎯 {location} 本地通推荐 - {item_type}"
            }
        },
        "elements": elements
    }
    
    return card


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: send_feishu_card.py <receive_id> [reply_to]", file=sys.stderr)
        sys.exit(1)
    
    receive_id = sys.argv[1]
    reply_to = sys.argv[2] if len(sys.argv) > 2 else None
    
    # 从 stdin 读取 JSON 数据
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析错误: {e}", file=sys.stderr)
        sys.exit(1)
    
    location = data.get("location", "未知地点")
    item_type = data.get("type", "推荐")
    sources = data.get("sources", "本地口碑")
    items = data.get("items", [])
    
    if not items:
        print("❌ 没有推荐数据", file=sys.stderr)
        sys.exit(1)
    
    # 构建卡片
    card = build_guide_card(items, location, item_type, sources)
    
    # 发送卡片
    result = send_card(receive_id, card, reply_to=reply_to)
    
    if result:
        print(f"OK:{result}")
        print("✅ 卡片发送成功")
    else:
        print("❌ 卡片发送失败", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
