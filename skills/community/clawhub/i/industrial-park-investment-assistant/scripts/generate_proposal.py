#!/usr/bin/env python3
"""
报价方案生成器 v2.0
====================
给客户推房源，算单价/总价，包含：租金+物业费+车位费

用法：
  python3 generate_proposal.py "企业名称" 200        # 根据面积自动匹配
  python3 generate_proposal.py "企业名称" 200 3.5     # 指定面积+预算租金
  python3 generate_proposal.py --customer C001        # 根据客户ID匹配

数据库：
  ~/.workbuddy/workspace/investment-assistant/local_db.sqlite
"""

import sqlite3
import os
import sys
import json
from datetime import datetime, date

DB_PATH = os.path.expanduser("~/.workbuddy/workspace/investment-assistant/local_db.sqlite")

# 默认配置（可从config.json覆盖）
DEFAULT_CONFIG = {
    "park_name": "示例产业园A",
    "park_address": "示例市XX区",
    "property_fee": 8.0,        # 物业费 元/㎡/月
    "parking_fee": 500,         # 单个车位月费 元/月
    "parking_recommend": 1,     # 每100㎡推荐1个车位
    "contact_name": "招商经理",
    "contact_phone": "1XX-XXXX-XXXX",
    "conversion_rate": {
        "rent": 1.0,            # 租金单位转换：元/㎡/天 → 元/㎡/月（30天）
        "property": 1.0,        # 物业费单位转换：元/㎡/月
        "parking": 1.0,         # 车位费单位转换：元/月/个
    }
}

def get_db():
    if not os.path.exists(DB_PATH):
        print(f"❌ 数据库不存在：{DB_PATH}")
        print("  提示：请先配置招商助手，导入房源数据。")
        sys.exit(1)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_available_rooms(conn, area=None, max_rent=None):
    """获取可租房源"""
    cursor = conn.cursor()
    
    if area and max_rent:
        # 面积±20%，租金不超过预算
        min_area = area * 0.8
        max_area = area * 1.2
        cursor.execute(
            "SELECT * FROM 房源销控表 WHERE 状态='待租' AND `面积(㎡)` >= ? AND `面积(㎡)` <= ? AND `租金单价(元/㎡/天)` <= ? ORDER BY `租金单价(元/㎡/天)` ASC",
            (min_area, max_area, max_rent)
        )
    elif area:
        min_area = area * 0.8
        max_area = area * 1.2
        cursor.execute(
            "SELECT * FROM 房源销控表 WHERE 状态='待租' AND `面积(㎡)` >= ? AND `面积(㎡)` <= ? ORDER BY `面积(㎡)` ASC",
            (min_area, max_area)
        )
    else:
        cursor.execute(
            "SELECT * FROM 房源销控表 WHERE 状态='待租' ORDER BY `面积(㎡)` ASC"
        )
    
    return [dict(r) for r in cursor.fetchall()]


def get_customer(conn, customer_id_or_name):
    """获取客户信息"""
    cursor = conn.cursor()
    # 先按客户ID查
    cursor.execute("SELECT * FROM 客户跟进记录 WHERE 客户ID=?", (customer_id_or_name,))
    row = cursor.fetchone()
    if row:
        return dict(row)
    # 再按名称查
    cursor.execute("SELECT * FROM 客户跟进记录 WHERE 客户名称 LIKE ?", (f"%{customer_id_or_name}%",))
    row = cursor.fetchone()
    if row:
        return dict(row)
    return None


def calc_monthly_cost(room, config, num_cars=1):
    """计算月成本明细"""
    area = room.get("面积(㎡)", 0) or 0
    rent_per_day = room.get("租金单价(元/㎡/天)", 0) or 0
    property_fee = room.get("物业费(元/㎡/月)", 0) or config["property_fee"]
    
    # 租金
    rent_per_month = area * rent_per_day * 30
    # 物业费
    property_per_month = area * property_fee
    # 停车费
    parking_per_month = config["parking_fee"] * num_cars
    
    total_per_month = rent_per_month + property_per_month + parking_per_month
    total_per_year = total_per_month * 12
    total_3_years = total_per_year * 3
    
    # 每日每平米全包价（展示给客户时用）
    all_in_per_day = total_per_month / (area * 30) if area > 0 else 0
    
    return {
        "area": area,
        "rent_per_day": rent_per_day,
        "rent_per_month": round(rent_per_month, 0),
        "property_fee": property_fee,
        "property_per_month": round(property_per_month, 0),
        "parking_per_month": round(parking_per_month, 0),
        "num_cars": num_cars,
        "total_per_month": round(total_per_month, 0),
        "total_per_year": round(total_per_year, 0),
        "total_3_years": round(total_3_years, 0),
        "all_in_per_day": round(all_in_per_day, 2),
    }


def format_proposal(company_name, rooms, costs_list, config):
    """生成报价方案文本"""
    today = date.today().isoformat()
    
    output = f"# 🏢 {'='*45}\n"
    output += f"#   招商报价方案\n"
    output += f"# {'='*45}\n\n"
    output += f"**客户名称**：{company_name}\n"
    output += f"**园区名称**：{config['park_name']}\n"
    output += f"**园区地址**：{config['park_address']}\n"
    output += f"**生成日期**：{today}\n\n"
    output += "---\n\n"

    if not rooms:
        output += "⚠️ **未找到可租房源**\n\n"
        output += "建议：\n"
        output += "1. 扩大面积范围（±30%）\n"
        output += "2. 提高预算上限\n"
        output += "3. 联系招商经理获取更多房源信息\n\n"
        output += f"**联系人**：{config['contact_name']}  {config['contact_phone']}\n"
        return output

    output += f"## 📋 需求匹配\n\n"
    output += f"共找到 **{len(rooms)}** 个匹配房源\n\n"

    for i, (room, cost) in enumerate(zip(rooms, costs_list), 1):
        output += f"---\n\n"
        output += f"### 方案{i}：{room['房号']}\n\n"
        
        # 房源基本信息
        output += f"**基本信息：**\n\n"
        output += f"| 项目 | 数据 |\n"
        output += f"|------|------|\n"
        output += f"| 房号 | {room['房号']} |\n"
        output += f"| 楼层 | {room.get('楼层', '-')}层 |\n"
        output += f"| 面积 | {cost['area']}㎡ |\n"
        output += f"| 租金单价 | {cost['rent_per_day']} 元/㎡/天 |\n"
        output += f"| 装修标准 | {room.get('装修标准', '标准')} |\n"
        output += f"| 朝向 | {room.get('朝向', '-')} |\n"
        output += f"| 状态 | {room.get('状态', '待租')} |\n\n"
        
        # 价格明细
        output += f"**💰 价格明细：**\n\n"
        output += f"| 费用项 | 计算方式 | 金额（元/月） |\n"
        output += f"|--------|---------|--------------|\n"
        output += f"| 💵 租金 | {cost['area']}㎡ × {cost['rent_per_day']}元/㎡/天 × 30天 | {cost['rent_per_month']:,.0f} |\n"
        output += f"| 🏠 物业费 | {cost['area']}㎡ × {cost['property_fee']}元/㎡/月 | {cost['property_per_month']:,.0f} |\n"
        output += f"| 🚗 停车费 | {cost['num_cars']}个车位 × {config['parking_fee']}元/月 | {cost['parking_per_month']:,.0f} |\n"
        output += f"| **月合计** | | **{cost['total_per_month']:,.0f}** |\n\n"
        
        # 总价汇总
        output += f"**📊 总价汇总：**\n\n"
        output += f"- **月总成本**：¥{cost['total_per_month']:,.0f} 元\n"
        output += f"- **年总成本**：¥{cost['total_per_year']:,.0f} 元\n"
        output += f"- **3年总成本**：¥{cost['total_3_years']:,.0f} 元\n"
        output += f"- **全包均价**：{cost['all_in_per_day']} 元/㎡/天（含租金+物业+车位）\n\n"
        
        # 匹配说明
        match_note = []
        if cost['area'] >= 200:
            match_note.append("面积适中，适合中型企业")
        elif cost['area'] >= 100:
            match_note.append("面积紧凑，适合初创/成长型企业")
        else:
            match_note.append("面积充足，适合快速发展企业")
        
        if cost['rent_per_day'] <= 2.0:
            match_note.append("租金性价比高")
        elif cost['rent_per_day'] <= 3.0:
            match_note.append("租金适中，物超所值")
        else:
            match_note.append("品质房源，匹配高端需求")
        
        output += f"**✨ 推荐理由：** {'，'.join(match_note)}。\n\n"

    # 底部信息
    output += "---\n\n"
    output += f"**📌 说明：**\n"
    output += f"- 以上报价为参考价格，最终以合同为准\n"
    output += f"- 停车费按 {config['parking_fee']} 元/月/个计算，实际按需配置\n"
    output += f"- 以上未包含水电费、网络费等杂费\n"
    output += f"- 价格有效期：7天\n\n"
    
    output += f"**👤 联系人：** {config['contact_name']}\n"
    output += f"**📞 电话：** {config['contact_phone']}\n"
    output += f"**⏰ 生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"

    return output


def save_proposal(content, company_name):
    """保存报价方案"""
    output_dir = os.path.expanduser("~/.workbuddy/workspace/investment-assistant")
    os.makedirs(output_dir, exist_ok=True)
    
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = company_name.replace(" ", "_").replace("/", "_")[:20]
    output_file = os.path.join(output_dir, f"报价方案_{safe_name}_{date_str}.md")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    return output_file


def main():
    if len(sys.argv) < 3:
        print("用法: python3 generate_proposal.py <企业名称/客户ID> <需求面积> [预算租金]")
        print("示例:")
        print("  python3 generate_proposal.py \"XX科技\" 200")
        print("  python3 generate_proposal.py \"XX科技\" 200 3.5")
        print("  python3 generate_proposal.py --customer C001")
        sys.exit(1)
    
    conn = get_db()
    
    # 解析参数
    company_name = sys.argv[1]
    area = float(sys.argv[2]) if len(sys.argv) >= 3 and sys.argv[2].replace('.','').isdigit() else 0
    max_rent = float(sys.argv[3]) if len(sys.argv) >= 4 and sys.argv[3].replace('.','').isdigit() else None
    
    # 如果是客户ID，自动获取客户信息
    if company_name.startswith("C") and company_name[1:].isdigit():
        customer = get_customer(conn, company_name)
        if customer:
            company_name = customer.get("客户名称", company_name)
            if area == 0 and customer.get("需求面积"):
                try:
                    area_range = str(customer["需求面积"]).split("-")
                    area = float(area_range[0]) if len(area_range) > 0 else 200
                except:
                    area = 200
    
    if area == 0:
        area = 200  # 默认面积
    
    config = DEFAULT_CONFIG
    
    print(f"🏢 生成报价方案...")
    print(f"📋 客户：{company_name}")
    print(f"📐 需求面积：{area}㎡")
    if max_rent:
        print(f"💰 预算租金：≤{max_rent}元/㎡/天")
    print()
    
    # 查找房源
    rooms = get_available_rooms(conn, area, max_rent)
    
    # 如果没有完全匹配的，放宽条件
    if not rooms:
        rooms = get_available_rooms(conn, area * 1.5, max_rent * 1.2 if max_rent else None)
    
    if not rooms:
        rooms = get_available_rooms(conn)
    
    # 限制最多推荐3个
    rooms = rooms[:3]
    
    # 计算成本
    costs_list = []
    for room in rooms:
        # 每100㎡推荐1个车位
        area_val = room.get("面积(㎡)", 0) or 0
        num_cars = max(1, int(area_val / 100))
        cost = calc_monthly_cost(room, config, num_cars)
        costs_list.append(cost)
    
    # 生成方案
    content = format_proposal(company_name, rooms, costs_list, config)
    
    # 保存
    output_file = save_proposal(content, company_name)
    
    print(content)
    print(f"\n✅ 报价方案已保存：{output_file}")
    
    conn.close()
    return output_file


if __name__ == "__main__":
    main()
