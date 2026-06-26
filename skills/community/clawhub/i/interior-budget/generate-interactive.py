#!/usr/bin/env python3
"""交互式生成预算表"""

import generate_budget

def main():
    print("🏠 隐室空间设计 预算表自动生成")
    print("-" * 40)
    name = input("工程名称: ").strip()
    client = input("客户姓名: ").strip()
    address = input("项目地址: ").strip()
    area_str = input("套内面积(㎡): ").strip()
    area = float(area_str)
    print("\n项目类型: [1]家装  [2]办公  [3]餐饮")
    type_choice = input("选择(1/2/3，默认1): ").strip() or "1"
    type_map = {"1": "home", "2": "office", "3": "fnb"}
    ptype = type_map.get(type_choice, "home")
    output = input("输出文件路径: ").strip()
    if not output:
        output = f"/Users/laobaobei/Desktop/{name}_{client}预算.xlsx"
    
    print("\n生成中...")
    generate_budget.generate_budget(name, client, address, area, ptype, output)

if __name__ == "__main__":
    main()
