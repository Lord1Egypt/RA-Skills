#!/usr/bin/env python3
"""
异议处理脚本
查询异议应对话术和成功案例
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# 异议数据库（实际应存储在JSON文件中）
OBJECTION_DB = {
    "太贵了": {
        "frequency": "★★★★★",
        "success_rate": "78%",
        "responses": [
            "理解您的考虑。让我帮您算一下TCO（总拥有成本）：租金+物业费+停车费，我们园区比竞品低15%。",
            "而且我们有人才补贴政策，本科1万/硕士3万/博士5万，实际成本更低。",
            "这是TCO对比表，您可以看一眼（递上对比表）。",
        ],
        "cases": [
            "案例1：XX科技公司，最初嫌贵，算完TCO后当场签约",
            "案例2：YY贸易公司，对比3个园区后，还是选了我们（总成本最低）",
        ],
        "follow_up": "发送TCO对比表 → 3天后再跟进 → 邀请来看高区景观",
    },
    "位置有点远": {
        "frequency": "★★★★",
        "success_rate": "65%",
        "responses": [
            "确实，我们位置不算中心。但您看，地铁5号线步行8分钟，班车15分钟一班。",
            "而且这里租金比市中心低40%，员工租房成本也低，实际综合成本更优。",
            "很多客户一开始也觉得远，入驻后发现配套齐全，反而节省了通勤时间。",
        ],
        "cases": [
            "案例1：ZZ物流公司，起初嫌远，后来员工反映配套好，反而更稳定",
            "案例2：AA电商公司，对比后选择我们（员工租房成本节省30%）",
        ],
        "follow_up": "发送配套地图 → 安排班车体验 → 邀请员工代表来看",
    },
    "要考虑一下": {
        "frequency": "★★★★",
        "success_rate": "58%",
        "responses": [
            "完全理解，这是重要决策。请问您主要考虑哪些方面？是租金、位置还是配套？",
            "这样吧，我先给您发一份详细的对比资料，您和团队讨论后，我再来拜访。",
            "另外，这周我们有个限时优惠（免租期延长1个月），如果您本周内能确定，我可以帮您申请。",
        ],
        "cases": [
            "案例1：BB咨询公司，考虑1周后签约，因限时优惠提前决定",
            "案例2：CC设计公司，考虑2周，期间竞品降价，但我们以服务胜出",
        ],
        "follow_up": "发送对比资料 → 3天后跟进 → 强调稀缺性+限时优惠",
    },
    "竞品更便宜": {
        "frequency": "★★★",
        "success_rate": "72%",
        "responses": [
            "您说的竞品我也了解，确实租金低一些。但让我帮您算一下全成本：",
            "租金+物业费+停车费+装修成本+时间成本，我们实际3年能省12万。",
            "而且我们有产业生态优势，园区内就有您的上下游企业，这个价值很难用租金衡量。",
        ],
        "cases": [
            "案例1：DD制造公司，竞品便宜0.3元/㎡/天，但算完全成本选了我们",
            "案例2：EE科技公司，起初选竞品，后来因产业生态不足又换回我们",
        ],
        "follow_up": "发送全成本对比 → 强调产业生态 → 邀请参加园区活动",
    },
    "装修要3个月": {
        "frequency": "★★★",
        "success_rate": "85%",
        "responses": [
            "理解您的顾虑。我们有精装交付的房源，空调、网络、隔断都做好，拎包入驻。",
            "如果您需要定制化装修，我们也有合作装修公司，45天交付，比市场快一半。",
            "这是精装房源的照片和装修案例，您看看是否符合需求？",
        ],
        "cases": [
            "案例1：FF贸易公司，选精装房源，签约后7天入驻",
            "案例2：GG科技公司，定制装修，45天交付，比计划提前1个月",
        ],
        "follow_up": "推荐精装房源 → 安排装修公司对接 → 提供装修案例",
    },
}

def query_objection(objection_type):
    """查询异议处理话术"""
    if objection_type not in OBJECTION_DB:
        return None, f"❌ 未找到异议类型: {objection_type}"
    
    return OBJECTION_DB[objection_type], None

def format_objection_response(objection_type, data):
    """格式化异议处理输出"""
    output = f"# 🗣️ 异议处理 - {objection_type}\n\n"
    
    output += f"## 基本信息\n"
    output += f"- **出现频率**：{data['frequency']}\n"
    output += f"- **处理成功率**：{data['success_rate']}\n\n"
    
    output += f"## 应对话术（推荐顺序）\n"
    for i, response in enumerate(data["responses"], 1):
        output += f"{i}. {response}\n"
    output += "\n"
    
    output += f"## 成功案例\n"
    for case in data["cases"]:
        output += f"- {case}\n"
    output += "\n"
    
    output += f"## 后续跟进建议\n"
    output += f"{data['follow_up']}\n\n"
    
    output += f"## 使用提示\n"
    output += f"- 先倾听客户完整顾虑，不要打断\n"
    output += f"- 使用'理解+算账+案例'三步法\n"
    output += f"- 避免直接反驳，用数据说话\n"
    output += f"- 3天内必须跟进，保持热度\n"
    
    return output

def save_to_file(content, objection_type, output_dir=None):
    """保存异议处理到文件"""
    if output_dir is None:
        output_dir = os.path.expanduser("~/.workbuddy/workspace/investment-assistant")
    
    os.makedirs(output_dir, exist_ok=True)
    
    date_str = datetime.now().strftime("%Y%m%d")
    output_file = os.path.join(output_dir, f"异议处理_{date_str}.md")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
        f.write(f"\n\n---\n*本异议处理方案由招商助手自动生成 @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    
    return output_file

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python3 objection_handler.py <异议类型>")
        print("示例: python3 objection_handler.py \"太贵了\"")
        print("支持异议类型：太贵了/位置有点远/要考虑一下/竞品更便宜/装修要3个月")
        sys.exit(1)
    
    objection_type = sys.argv[1]
    
    print(f"🗣️ 开始查询异议处理: {objection_type}")
    
    # 查询异议处理
    data, error = query_objection(objection_type)
    
    if error:
        print(error)
        sys.exit(1)
    
    # 格式化输出
    content = format_objection_response(objection_type, data)
    print(content)
    
    # 保存文件
    output_file = save_to_file(content, objection_type)
    print(f"\n✅ 异议处理方案已保存: {output_file}")
    
    return output_file

if __name__ == "__main__":
    main()
