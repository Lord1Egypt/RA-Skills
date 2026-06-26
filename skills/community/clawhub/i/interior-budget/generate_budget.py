#!/usr/bin/env python3
"""
室内设计工程预算自动生成工具
基于隐室空间设计标准模板生成
"""

import argparse
import openpyxl

# 默认分项模板 - 标准空间分项（家装）
HOME_SPACES = {
    "一、客餐厅": [
        ("轻钢龙骨石膏板吊顶", "1、轻钢龙骨及辅材 2、石膏板 3、人工", "m²", None),
        ("天花专用腻子批荡", "1、腻子批荡 2、打砂纸 3、人工", "m²", None),
        ("天花乳胶漆喷涂", "定做", "m²", None),
        ("反光灯槽制作", "1、轻钢龙骨 2、木工板 3、人工", "m", None),
        ("地面瓷砖", "1、瓷砖；2、水泥砂浆 3、美缝 4、人工", "m²", None),
        ("墙面专用腻子批荡", "1、腻子批荡 2、打砂纸 3、人工", "m²", None),
        ("墙面乳胶漆/艺术漆", "定做", "m²", None),
        ("电视背景基础", "1、木工基层；2、辅材 3、人工", "m²", None),
        ("背景大理石/石材", "1、石材；2、加工费 3、辅材 4、人工", "m²", None),
        ("木饰面及暗门", "1、木饰面；2、辅材 3、五金 4、人工", "m²", None),
        ("背景柜体", "定制", "m²", None),
        ("酒柜", "定制", "m²", None),
        ("鞋柜（室内）", "定制", "m²", None),
        ("鞋柜（室外）", "现场制作", "m²", None),
        ("墙面砖", "1、墙砖；2、水泥砂浆 3、美缝 4、人工", "m²", None),
    ],
    "二、主卧室": [
        ("地面实木地板", "1、地板；2、龙骨；3、人工 4、辅材", "m²", None),
        ("天花腻子批荡", "1、腻子批荡 2、打砂纸 3、人工", "m²", None),
        ("天花乳胶漆", "定做", "m²", None),
        ("墙面腻子批荡", "1、腻子批荡 2、打砂纸 3、人工", "m²", None),
        ("墙面乳胶漆", "定做", "m²", None),
        ("石膏线", "1、石膏线；2、人工", "m", None),
        ("衣柜", "定制", "m²", None),
        ("床头背景", "定做", "m²", None),
    ],
    "三、次卧室/小孩房": [
        ("地面实木地板", "1、地板；2、龙骨；3、人工 4、辅材", "m²", None),
        ("天花腻子批荡", "1、腻子批荡 2、打砂纸 3、人工", "m²", None),
        ("天花乳胶漆", "定做", "m²", None),
        ("墙面腻子批荡", "1、腻子批荡 2、打砂纸 3、人工", "m²", None),
        ("墙面乳胶漆", "定做", "m²", None),
        ("石膏线", "1、石膏线；2、人工", "m", None),
        ("衣柜", "定制", "m²", None),
    ],
    "四、书房": [
        ("地面地砖/地板", "定做", "m²", None),
        ("天花腻子批荡", "1、腻子批荡 2、打砂纸 3、人工", "m²", None),
        ("天花乳胶漆", "定做", "m²", None),
        ("墙面腻子批荡", "1、腻子批荡 2、打砂纸 3、人工", "m²", None),
        ("墙面乳胶漆", "定做", "m²", None),
        ("书柜", "定制", "m²", None),
    ],
    "五、厨房": [
        ("地面瓷砖", "1、瓷砖；2、水泥砂浆 3、美缝 4、人工", "m²", None),
        ("墙面瓷砖", "1、瓷砖；2、水泥砂浆 3、美缝 4、人工", "m²", None),
        ("天花铝扣板吊顶", "含辅料及人工", "m²", None),
        ("整体橱柜", "定制（地柜+吊柜）", "m", None),
        ("门槛石", "1、石材；2、安装", "块", None),
        ("防水处理", "1、防水涂料 2、人工", "m²", None),
        ("包下水管", "红砖砌筑", "项", None),
    ],
    "六、卫生间": [
        ("地面瓷砖", "1、瓷砖；2、水泥砂浆 3、美缝 4、人工", "m²", None),
        ("墙面瓷砖", "1、瓷砖；2、水泥砂浆 3、美缝 4、人工", "m²", None),
        ("天花铝扣板吊顶", "含辅料及人工", "m²", None),
        ("防水处理", "1、防水涂料 2、人工", "m²", None),
        ("门槛石", "1、石材；2、安装", "块", None),
        ("包下水管", "红砖砌筑", "项", 1),
        ("门及门套安装", "成品门含安装", "套", 1),
        ("淋浴房底盘", "定做含安装", "套", 1),
        ("洁具安装", "含安装", "项", 1),
        ("浴室柜", "定制含安装", "套", 1),
        ("五金挂件", "定做含安装", "套", 1),
    ],
    "七、阳台": [
        ("地面瓷砖", "1、瓷砖；2、水泥砂浆 3、美缝 4、人工", "m²", None),
        ("墙面瓷砖/乳胶漆", "定做", "m²", None),
        ("天花腻子+乳胶漆", "1、腻子 2、乳胶漆 3、人工", "m²", None),
        ("阳台柜", "定制", "m²", None),
        ("门槛石", "1、石材；2、安装", "块", None),
        ("防水", "1、防水涂料 2、人工", "m²", None),
    ],
}

# 办公空间分项
OFFICE_SPACES = {
    "一、大堂/接待区": [
        ("轻钢龙骨石膏板吊顶", "1、轻钢龙骨机辅料 2、石膏板 3、人工", "m²", None),
        ("天花腻子批荡+乳胶漆", "1、腻子 2、乳胶漆 3、人工", "m²", None),
        ("地面地砖", "1、地砖 2、水泥砂浆 3、美缝 4、人工", "m²", None),
        ("墙面腻子+艺术漆/乳胶漆", "定做", "m²", None),
        ("接待台", "定制", "m", None),
    ],
    "二、开放办公区": [
        ("轻钢龙骨石膏板吊顶", "1、轻钢龙骨机辅料 2、石膏板 3、人工", "m²", None),
        ("天花腻子批荡+乳胶漆", "1、腻子 2、乳胶漆 3、人工", "m²", None),
        ("地面地砖/地板", "定做", "m²", None),
        ("墙面腻子+乳胶漆", "1、腻子 2、乳胶漆 3、人工", "m²", None),
        ("轻质隔墙", "1、轻钢龙骨 2、石膏板 3、人工", "m²", None),
    ],
    "三、总经理办公室": [
        ("轻钢龙骨石膏板吊顶", "1、轻钢龙骨机辅料 2、石膏板 3、人工", "m²", None),
        ("天花腻子批荡+乳胶漆", "1、腻子 2、乳胶漆 3、人工", "m²", None),
        ("地面地砖/地板", "定做", "m²", None),
        ("墙面木饰面/乳胶漆", "定做", "m²", None),
        ("背景柜/书柜", "定制", "m²", None),
    ],
    "四、会议室": [
        ("轻钢龙骨石膏板吊顶", "1、轻钢龙骨机辅料 2、石膏板 3、人工", "m²", None),
        ("天花腻子批荡+乳胶漆", "1、腻子 2、乳胶漆 3、人工", "m²", None),
        ("地面地砖", "1、地砖 2、水泥砂浆 3、美缝 4、人工", "m²", None),
        ("墙面腻子+乳胶漆", "1、腻子 2、乳胶漆 3、人工", "m²", None),
    ],
}

# 餐饮空间分项
FnB_SPACES = {
    "一、大厅就餐区": [
        ("轻钢龙骨石膏板吊顶/矿棉板吊顶", "定做", "m²", None),
        ("天花腻子批荡+乳胶漆", "1、腻子 2、乳胶漆 3、人工", "m²", None),
        ("地面防滑地砖", "1、瓷砖 2、水泥砂浆 3、美缝 4、人工", "m²", None),
        ("墙面墙砖/乳胶漆", "定做", "m²", None),
        ("造型背景墙", "定做", "m²", None),
    ],
    "二、包厢": [
        ("轻钢龙骨石膏板吊顶", "1、轻钢龙骨机辅料 2、石膏板 3、人工", "m²", None),
        ("天花腻子批荡+乳胶漆", "1、腻子 2、乳胶漆 3、人工", "m²", None),
        ("地面防滑地砖", "1、瓷砖 2、水泥砂浆 3、美缝 4、人工", "m²", None),
        ("墙面墙砖/乳胶漆", "定做", "m²", None),
    ],
    "三、厨房/操作间": [
        ("地面防滑地砖", "1、防滑砖 2、水泥砂浆 3、美缝 4、人工", "m²", None),
        ("墙面墙砖到顶", "1、墙砖 2、水泥砂浆 3、美缝 4、人工", "m²", None),
        ("天花铝扣板吊顶", "含辅料人工", "m²", None),
        ("防水处理", "1、防水涂料 2、人工", "m²", None),
        ("排水沟", "砖砌+水泥砂浆找坡", "m", None),
    ],
    "四、门头/收银台": [
        ("门头制作安装", "定做含骨架+招牌", "项", 1),
        ("收银台", "现场制作", "m", None),
    ],
}

def generate_budget(project_name, client_name, address, area_m2, project_type, output_path):
    """
    生成预算Excel文件
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "分部分项工程量清单表与计价表"

    # 表头信息
    ws.append(["【表1-2】"])
    ws.append(["地址：温州市鹿城区车站大道神力大厦4栋9楼\n电话：0577-86057756  13706668486"])
    ws.append([f"{client_name}装修工程预算表"])
    ws.append([f"工程名称: {project_name}                     客户姓名 {client_name}             地址：{address}             面积：套内{area_m2}平方米"])
    ws.append(["序号", "项目名称", "项目特征", "计量单位", "工程量", "单价", "合价", "备注（品牌）"])

    current_row = 6
    current_seq = 1

    # 选择空间模板
    if project_type == "home":
        spaces = HOME_SPACES
    elif project_type == "office":
        spaces = OFFICE_SPACES
    elif project_type == "fnb":
        spaces = FnB_SPACES
    else:
        spaces = HOME_SPACES

    # 按空间写
    for space_name, items in spaces.items():
        ws.append([space_name])
        current_row += 1
        for item_name, feature, unit, qty in items:
            row = [
                current_seq,
                item_name,
                feature,
                unit,
                qty if qty is not None else "",
                "",
                "",
                "",
            ]
            ws.append(row)
            current_seq += 1
            current_row += 1

    # 汇总行
    ws.append([])
    ws.append(["", "", "", "", "", "合计：", "", ""])
    ws.append(["", "", "", "", "", "税金（3.14%）", "", ""])
    ws.append(["", "", "", "", "", "总造价：", "", ""])

    # 调整列宽
    ws.column_dimensions['A'].width = 8
    ws.column_dimensions['B'].width = 22
    ws.column_dimensions['C'].width = 30
    ws.column_dimensions['D'].width = 12
    ws.column_dimensions['E'].width = 12
    ws.column_dimensions['F'].width = 10
    ws.column_dimensions['G'].width = 14
    ws.column_dimensions['H'].width = 20

    wb.save(output_path)
    print(f"✓ 预算表已生成: {output_path}")
    print(f"  项目: {project_name}, 面积: {area_m2}㎡, 类型: {project_type}")
    print("  工程量/单价/合价/品牌备注列已留空，直接填入即可")

def main():
    parser = argparse.ArgumentParser(description="生成室内设计工程预算表")
    parser.add_argument("--name", required=True, help="工程名称")
    parser.add_argument("--client", required=True, help="客户姓名")
    parser.add_argument("--address", required=True, help="项目地址")
    parser.add_argument("--area", type=float, required=True, help="套内面积（平方米）")
    parser.add_argument("--type", default="home", choices=["home", "office", "fnb"], 
                        help="项目类型: home(家装)/office(办公)/fnb(餐饮)")
    parser.add_argument("--output", required=True, help="输出文件路径")
    args = parser.parse_args()

    generate_budget(args.name, args.client, args.address, args.area, args.type, args.output)

if __name__ == "__main__":
    main()
