#!/usr/bin/env python3
"""
会前简报自动生成脚本（简化版）
基于企业名称，自动生成会前简报
"""

import json
import os
import sys
from datetime import datetime

# 配置路径
WORKSPACE_DIR = os.path.expanduser("~/.workbuddy/workspace/investment-assistant")
CUSTOMERS_DIR = os.path.join(WORKSPACE_DIR, "customers")
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "../templates")

def load_customer_data(enterprise_name):
    """从客户档案.json加载客户数据"""
    try:
        with open(os.path.join(CUSTOMERS_DIR, "客户档案.json"), "r", encoding="utf-8") as f:
            data = json.load(f)
            
        # 在所有等级中查找企业
        for grade in ["A级（高意向）", "B级（有意向）", "C级（潜在）", "D级（观望流失）"]:
            if grade not in data:
                continue
            for customer in data[grade]:
                if customer.get("enterprise") == enterprise_name:
                    customer["grade"] = grade[0]  # A/B/C/D
                    return customer
                    
        print(f"⚠️ 未找到企业 {enterprise_name} 的客户档案")
        return None
        
    except Exception as e:
        print(f"❌ 加载客户档案失败: {e}")
        return None

def generate_briefing(enterprise_name, contact_name=None):
    """生成会前简报"""
    print(f"🚀 开始生成 {enterprise_name} 的会前简报...")
    print("=" * 50)
    
    # 加载客户数据
    customer_data = load_customer_data(enterprise_name)
    
    # 获取企业数据（模拟）
    enterprise = {
        "name": enterprise_name,
        "founded": "2015-03-12",
        "scale": "150人",
        "funding_round": "B轮",
        "funding_amount": "5亿元",
        "business": "人工智能解决方案",
        "industry_rank": "细分领域Top5"
    }
    
    # 扩张信号
    expansion_signals = [
        "✅ 招聘信号：近3个月招聘30人，团队扩容50%",
        "✅ 融资信号：完成B轮5亿元融资，有资金扩租",
        "✅ 扩张信号：新设华东研发中心，场地需求迫切"
    ]
    
    # 决策人画像
    decision_maker = {
        "name": contact_name if contact_name else "张总",
        "position": "CEO",
        "background": "清华本科+斯坦福硕士，连续创业者",
        "style": "技术驱动，关注人才供给和产业生态"
    }
    
    # 生成简报内容
    now = datetime.now()
    briefing = f"""# 📋 会前简报 - {enterprise_name}

**生成时间：** {now.strftime('%Y-%m-%d %H:%M:%S')}
**会见时间：** [请填写]  
**招商负责人：** [请填写]  

---

## 一、企业背景深度分析

### 1.1 企业基本信息

| 项目 | 内容 |
|------|------|
| 企业全称 | {enterprise['name']} |
| 成立时间 | {enterprise['founded']} |
| 企业规模 | {enterprise['scale']} |
| 融资轮次 | {enterprise['funding_round']} |
| 融资金额 | {enterprise['funding_amount']} |
| 主营业务 | {enterprise['business']} |
| 行业地位 | {enterprise['industry_rank']} |

### 1.2 企业发展动态（近1年）

| 动态类型 | 具体内容 | 时间 |
|----------|----------|------|
| 招聘动态 | 近3个月招聘研发人员30人 | 2026-05 |
| 融资事件 | 完成B轮5亿元融资 | 2026-03 |
| 新设机构 | 设立华东研发中心 | 2026-01 |
| 专利/资质 | 新增发明专利15项 | 2026-04 |

### 1.3 决策人画像

| 决策人 | 职位 | 背景 | 决策风格 | 关注重点 |
|---------|------|------|----------|----------|
| {decision_maker['name']} | {decision_maker['position']} | {decision_maker['background']} | {decision_maker['style']} | 人才供给、产业政策、扩租灵活性 |

---

## 二、扩张信号识别

### 2.1 明确扩张信号

{chr(10).join(['- ' + signal for signal in expansion_signals])}

### 2.2 现有场地分析

| 项目 | 内容 |
|------|------|
| 现有场地 | XX园区A栋12楼，500㎡ |
| 租约到期 | 2026-09-30 |
| 扩租计划 | 计划扩租至800-1000㎡ |
| 搬迁意向 | 现有场地无法满足研发需求，考虑搬迁 |

### 2.3 决策时间窗口

- **决策周期**：1-2个月
- **关键节点**：7月前必须确定，9月前完成装修入驻
- **决策流程**：CEO决策 → 董事会审批 → 签约

---

## 三、对话剧本（针对CEO/创始人）

### 3.1 破冰话题

- 「Congratulations on your Series B funding! 我看了你们的最新专利，在 [领域] 很有突破性…」
- 「你们最近招聘的 [岗位] 人，是不是业务扩张很快？」

### 3.2 关键问题

1. 「未来3年的战略重心是什么？人才扩招计划如何？」
2. 「现有场地有哪些痛点？是否满足研发/测试需求？」
3. 「选址最看重哪些因素？成本、配套、还是产业生态？」

### 3.3 价值传递

- **产业生态优势**：园区已入驻50家同产业链企业，协同效应强
- **人才供给优势**：周边10所高校，年输送毕业生2000人
- **政策优势**：100万元/年的补贴，3年可节省300万元

### 3.4 可能的异议 + 应对

**❓ 「租金太贵」**  
→ 「我们算一下TCO，3年综合成本其实比 [竞品] 低15%，而且我们的政策补贴可以抵扣100元/年…」

**❓ 「位置有点远」**  
→ 「我们提供3条班车路线，到地铁站5分钟，而且周边配套完善，员工生活成本低…」

---

## 四、竞品对比分析

### 4.1 可能对比的竞品园区

| 竞品园区 | 距离 | 租金（元/㎡/天） | 优势 | 劣势 |
|----------|------|------------------|------|------|
| 竞品园区A | 5 km | 2.8 | 知名度高、配套成熟 | 租金高、无政策 |
| 竞品园区B | 8 km | 2.2 | 租金低 | 毛坯交付、配套不足、无产业生态 |

### 4.2 我方差异化优势

**VS 竞品园区A：**
- ✅ 价格优势：租金低20%，3年节省150万元
- ✅ 政策优势：我们有100万元/年补贴，竞品无
- ✅ 产业优势：我们园区有50家同产业链企业，竞品无产业协同

**VS 竞品园区B：**
- ✅ 交付优势：我们精装交付即租即用，竞品毛坯需装修3个月
- ✅ 配套优势：我们有食堂/公寓/会议中心，竞品配套不足
- ✅ 服务优势：我们有C+运营服务体系，竞品仅基础物业

### 4.3 截流话术

**如果客户说：「竞品园区A 知名度更高…」**  
→ 「知名度确实高，但您算过TCO吗？我们3年综合成本比他们低15%，而且我们的政策补贴可以抵扣100元/年，实际…」

**如果客户说：「竞品园区B 租金更便宜…」**  
→ 「租金确实低0.6元，但他们是毛坯交付，装修需要3个月，时间成本50万元，而且没有政策补贴，3年综合成本其实比我们高10%…」

---

## 五、会见准备清单

### 5.1 需要携带的材料

- [ ] 园区宣传册（最新版）
- [ ] 房源销控表（实时更新）
- [ ] TCO成本对比报告（针对该企业定制）
- [ ] 政策文件汇编（宝山区+上海市）
- [ ] 产业链地图（园区主导产业生态图）
- [ ] 成功案例集（同行业企业入驻案例）
- [ ] 名片（足够数量）

### 5.2 需要提前确认的事项

- [ ] 确认会见时间、地点、参与人员
- [ ] 确认企业决策人姓名、职位、背景
- [ ] 确认企业需求面积、楼层、交付标准
- [ ] 准备3套推荐房源（备选方案）
- [ ] 准备竞品对比分析（针对该企业可能对比的竞品）
- [ ] 预约带看（如需要，提前预约样板间）

---

## 六、会后跟进计划

### 6.1 24小时内

- [ ] 发送跟进邮件（附会面摘要 + 定制方案）
- [ ] 更新客户档案（`customers/客户档案.json`）
- [ ] 写入跟进记录（`customers/跟进记录/{now.strftime('%Y-%m-%d')}_{enterprise_name}.md`）

### 6.2 3天内

- [ ] 电话跟进，确认客户反馈和顾虑
- [ ] 如需，安排第二次会面或带看
- [ ] 准备方案细化（如客户有意向）

### 6.3 7天内

- [ ] 出具正式报价单（如客户有意向）
- [ ] 安排高层会面（如需要，邀请招商总监/总经理）
- [ ] 启动内部审批流程（如涉及折扣优惠）

---

**📞 紧急联系方式**

**招商负责人：** [招商人员姓名] [电话]  
**招商总监：** [总监姓名] [电话]  

---

*本会前简报由招商助手自动生成*  
*生成时间：{now.strftime('%Y-%m-%d %H:%M:%S')}*  
*有效期：本次会议前24小时*
"""
    
    # 保存简报
    output_file = os.path.join(WORKSPACE_DIR, f"会前简报_{enterprise_name}_{now.strftime('%Y%m%d')}.md")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(briefing)
        
    print(f"✅ 会前简报已生成: {output_file}")
    print("=" * 50)
    print(f"📋 简报内容摘要:")
    print(f"   企业名称: {enterprise_name}")
    print(f"   生成时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   简报文件: {output_file}")
    print(f"\n💡 使用建议:")
    print(f"   1. 打印简报，会见前阅读")
    print(f"   2. 根据实际情况调整对话剧本")
    print(f"   3. 携带简报参加会见，随时查阅")
    
    return output_file

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python3 generate_briefing_simple.py <企业名称> [联系人姓名]")
        print("示例: python3 generate_briefing_simple.py \"XX科技公司\" \"张总\"")
        sys.exit(1)
    
    enterprise_name = sys.argv[1]
    contact_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    output_file = generate_briefing(enterprise_name, contact_name)
    
    if output_file:
        print(f"\n🎉 会前简报生成完成！")
        return 0
    else:
        print(f"\n❌ 会前简报生成失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())
