#!/usr/bin/env python3
"""
会前简报自动生成脚本 - 主程序
基于企业名称，自动生成完整的会前简报（含企业背景、扩张信号、对话剧本、竞品分析）
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta

# 配置路径
WORKSPACE_DIR = os.path.expanduser("~/.workbuddy/workspace/investment-assistant")
CUSTOMERS_DIR = os.path.join(WORKSPACE_DIR, "customers")
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "../templates")

class BriefingGenerator:
    def __init__(self, enterprise_name, contact_name=None):
        self.enterprise_name = enterprise_name
        self.contact_name = contact_name
        self.customer_data = None
        self.briefing_data = {}
        
    def load_customer_data(self):
        """从客户档案.json加载客户数据"""
        try:
            with open(os.path.join(CUSTOMERS_DIR, "客户档案.json"), "r", encoding="utf-8") as f:
                data = json.load(f)
                
            # 在所有等级中查找企业
            for grade in ["A级（高意向）", "B级（有意向）", "C级（潜在）", "D级（观望流失）"]:
                if grade not in data:
                    continue
                for customer in data[grade]:
                    if customer.get("enterprise") == self.enterprise_name:
                        self.customer_data = customer
                        self.customer_data["grade"] = grade[0]  # A/B/C/D
                        return True
                        
            print(f"⚠️ 未找到企业 {self.enterprise_name} 的客户档案")
            return False
            
        except Exception as e:
            print(f"❌ 加载客户档案失败: {e}")
            return False
    
    def fetch_enterprise_data(self):
        """获取企业实时数据（模拟企查查API）"""
        print(f"🔍 正在获取 {self.enterprise_name} 的实时数据...")
        
        # 模拟API调用延迟
        time.sleep(1)
        
        # 模拟返回数据
        self.briefing_data["enterprise"] = {
            "name": self.enterprise_name,
            "founded": "2015-03-12",
            "registered_capital": "1000万元",
            "scale": "150人",
            "revenue_2025": "2.5亿元（估算）",
            "funding_round": "B轮",
            "funding_amount": "5亿元",
            "business": "人工智能解决方案",
            "industry_rank": "细分领域Top5"
        }
        
        self.briefing_data["dynamics"] = {
            "recruitment": "近3个月招聘研发人员30人",
            "funding": "2026年3月完成B轮5亿元融资",
            "new_office": "2026年1月设立华东研发中心",
            "patents": "新增发明专利15项"
        }
        
        self.briefing_data["decision_maker"] = {
            "name": "张总",
            "position": "CEO",
            "background": "清华本科+斯坦福硕士，连续创业者",
            "style": "技术驱动，关注人才供给和产业生态",
            "focus": "人才供给、产业政策、扩租灵活性"
        }
        
        print(f"✅ 企业数据获取完成")
        return True
    
    def analyze_expansion_signals(self):
        """分析扩张信号"""
        print(f"📈 正在分析扩张信号...")
        
        # 基于客户数据和实时数据分析
        signals = []
        
        # 招聘信号
        if "招聘" in self.briefing_data.get("dynamics", {}).get("recruitment", ""):
            signals.append("✅ 招聘信号：近3个月招聘30人，团队扩容50%")
            
        # 融资信号
        if "融资" in self.briefing_data.get("dynamics", {}).get("funding", ""):
            signals.append("✅ 融资信号：完成B轮5亿元融资，有资金扩租")
            
        # 新设机构信号
        if "设立" in self.briefing_data.get("dynamics", {}).get("new_office", ""):
            signals.append("✅ 扩张信号：新设华东研发中心，场地需求迫切")
            
        # 现有场地分析
        self.briefing_data["current_site"] = {
            "address": "XX园区A栋12楼，500㎡",
            "lease_expire": "2026-09-30",
            "expansion_plan": "计划扩租至800-1000㎡",
            "move_intention": "现有场地无法满足研发需求，考虑搬迁"
        }
        
        self.briefing_data["expansion_signals"] = signals
        print(f"✅ 扩张信号分析完成")
        return True
    
    def generate_dialogue_script(self):
        """生成对话剧本（针对不同决策人）"""
        print(f"🎯 正在生成对话剧本...")
        
        decision_maker = self.briefing_data.get("decision_maker", {})
        position = decision_maker.get("position", "CEO")
        
        scripts = {}
        
        # CEO/创始人剧本
        scripts["CEO"] = {
            "ice_breaking": [
                f"Congratulations on your Series B funding! 我看了你们的最新专利，在 [领域] 很有突破性…",
                f"你们最近招聘的 [岗位] 人，是不是业务扩张很快？"
            ],
            "key_questions": [
                "未来3年的战略重心是什么？人才扩招计划如何？",
                "现有场地有哪些痛点？是否满足研发/测试需求？",
                "选址最看重哪些因素？成本、配套、还是产业生态？"
            ],
            "value_proposition": [
                f"园区产业生态：已入驻 [X] 家同产业链企业，协同效应强",
                f"人才供给优势：周边 [X] 高校，年输送毕业生 [X] 人",
                f"政策支持：[X] 万元/年的补贴，3年可节省 [X] 万元"
            ],
            "objection_handling": {
                "租金太贵": "我们算一下TCO，3年综合成本其实比 [竞品] 低 [X]%，而且我们的政策补贴可以抵扣 [X] 元/年…",
                "位置有点远": "我们提供 [X] 班车路线，到地铁站 [X] 分钟，而且周边配套完善，员工生活成本低…"
            }
        }
        
        # COO/运营负责人剧本
        scripts["COO"] = {
            "ice_breaking": [
                "你们现在的场地，听说交付标准不太满足研发需求？",
                "我看了你们的团队规模，扩张很快啊，现有场地还够用吗？"
            ],
            "key_questions": [
                "现有场地的交付标准有哪些不满足的地方？",
                "计算过搬迁的时间成本和装修成本吗？",
                "对园区的配套服务（食堂/公寓/会议）有哪些要求？"
            ],
            "value_proposition": [
                "精装交付：即租即用，0装修成本，0时间成本",
                "配套完善：食堂/人才公寓/会议中心/路演厅，降低企业运营成本 [X]%",
                "TCO优势：3年综合成本比毛坯交付园区低 [X]%"
            ],
            "objection_handling": {
                "物业费太高": "物业费包含 [X] 项服务（安保/清洁/绿化/设施维护），折算下来实际 [X] 元/㎡/月，而且…",
                "精装交付的装修标准如何": "我们提供3种装修标准，可以满足研发/办公/展示等不同需求，而且…"
            }
        }
        
        # CFO/财务负责人剧本
        scripts["CFO"] = {
            "ice_breaking": [
                "你们财务测算过搬迁的成本吗？除了租金，还有哪些隐形成本？",
                "我们园区有专门的财务咨询服务平台，可以帮企业做税务筹划…"
            ],
            "key_questions": [
                "除了租金和物业费，企业选址还会考虑哪些成本？",
                "了解过上海市和宝山区的产业政策吗？补贴力度很大…",
                "对园区提供的金融服务（产业基金/融资对接）有兴趣吗？"
            ],
            "value_proposition": [
                f"TCO透明：3年综合成本 [X] 万元，竞品 [X] 万元，节省 [X] 万元",
                f"政策收益：[X] 万元/年的补贴（人才+税收+专项），直接抵扣租金",
                f"金融服务：园区产业基金 [X] 亿元，可跟投优质企业 [X] 万元"
            ],
            "objection_handling": {
                "我们需要详细的成本测算对比": "我这就给您出一份TCO成本对比报告，包含租金、物业费、停车费、装修分摊、政策收益、时间成本，3年综合对比…",
                "政策补贴能否兑现": "这是宝山区和中集产城的官方协议，已经有很多企业成功申报，补贴按时到账…"
            }
        }
        
        # CTO/技术负责人剧本
        scripts["CTO"] = {
            "ice_breaking": [
                "你们研发实验室对层高和承重有什么要求？我们园区有 [X] 米层高、[X] kg/㎡承重的房源…",
                "听说你们需要做 [X] 测试，对电力负荷要求很高？我们园区可以做到 [X] KW/层…"
            ],
            "key_questions": [
                "研发实验室/测试中心对场地有哪些特殊要求？",
                "现有场地的电力、网络、通风是否满足需求？",
                "对园区的技术服务（算力平台/测试平台）有需求吗？"
            ],
            "value_proposition": [
                "硬件优势：层高 [X] m、承重 [X] kg/㎡、电力 [X] KW/层，满足研发需求",
                "技术服务：人工智能算力平台、公共测试平台，降低企业研发成本 [X]%",
                "智慧园区：5G全覆盖、物联网平台，提升研发效率 [X]%"
            ],
            "objection_handling": {
                "我们需要 [X] KW的电力增容，能做到吗": "园区电力冗余充足，增容申请 [X] 天内可批复，而且…",
                "网络带宽和稳定性如何": "园区接入 [X] 条光纤，带宽可达 [X] Gbps，而且有备用线路，保证99.9%可用性…"
            }
        }
        
        self.briefing_data["dialogue_scripts"] = scripts
        print(f"✅ 对话剧本生成完成（CEO/COO/CFO/CTO）")
        return True
    
    def analyze_competitors(self):
        """分析竞品对比"""
        print(f"🏢 正在分析竞品对比...")
        
        # 模拟竞品数据
        competitors = [
            {
                "name": "竞品园区A",
                "distance": "5 km",
                "rent": "2.8元/㎡/天",
                "advantages": "知名度高、配套成熟",
                "disadvantages": "租金高、无政策"
            },
            {
                "name": "竞品园区B",
                "distance": "8 km",
                "rent": "2.2元/㎡/天",
                "advantages": "租金低",
                "disadvantages": "毛坯交付、配套不足、无产业生态"
            }
        ]
        
        self.briefing_data["competitors"] = competitors
        
        # 生成截流话术
        self.briefing_data["interception_scripts"] = [
            f"如果客户说：『{competitors[0]['name']} 知名度更高…』→ 「知名度确实高，但您算过TCO吗？我们3年综合成本比他们低 [X]%，而且我们的政策补贴可以抵扣 [X] 元/年，实际…」",
            f"如果客户说：『{competitors[1]['name']} 租金更便宜…』→ 「租金确实低 [X] 元，但他们是毛坯交付，装修需要 [X] 个月，时间成本 [X] 万元，而且没有政策补贴，3年综合成本其实比我们高 [X]%…」"
        ]
        
        print(f"✅ 竞品对比分析完成")
        return True
    
    def generate_briefing_document(self):
        """生成会前简报文档"""
        print(f"📄 正在生成会前简报文档...")
        
        # 读取模板
        template_path = os.path.join(TEMPLATES_DIR, "会前简报模板.md")
        if not os.path.exists(template_path):
            print(f"❌ 模板文件不存在: {template_path}")
            return False
            
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
        
        # 填充数据（简化版，实际应该完整填充所有[X]占位符）
        now = datetime.now()
        briefing = template.replace("[企业名称]", self.enterprise_name)
        briefing = briefing.replace("[日期]", now.strftime("%Y年%m月%d日"))
        briefing = briefing.replace("[YYYY年MM月DD日]", now.strftime("%Y年%m月%d日"))
        briefing = briefing.replace("[YYYY-MM-DD HH:mm:ss]", now.strftime("%Y-%m-%d %H:%M:%S"))
        
        # 填充企业数据
        enterprise = self.briefing_data.get("enterprise", {})
        briefing = briefing.replace("[X]（如：细分领域Top3/快速成长/初创企业）", enterprise.get("industry_rank", "细分领域Top5"))
        briefing = briefing.replace("[X]（如：招聘研发人员20人/扩招销售团队）", self.briefing_data.get("dynamics", {}).get("recruitment", ""))
        
        # 填充决策人数据
        decision_maker = self.briefing_data.get("decision_maker", {})
        briefing = briefing.replace("[姓名/职位/背景/决策风格]", f"{decision_maker.get('name', '')} / {decision_maker.get('position', '')} / {decision_maker.get('background', '')} / {decision_maker.get('style', '')}")
        
        # 保存生成的简报
        output_file = os.path.join(WORKSPACE_DIR, f"会前简报_{self.enterprise_name}_{now.strftime('%Y%m%d')}.md")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(briefing)
            
        print(f"✅ 会前简报已生成: {output_file}")
        return output_file
    
    def generate(self):
        """生成完整的会前简报"""
        print(f"🚀 开始生成 {self.enterprise_name} 的会前简报...")
        print(f"=" * 50)
        
        # 步骤1：加载客户数据
        if not self.load_customer_data():
            print(f"⚠️ 未找到客户档案，将仅使用企业名称生成简报")
            # 继续执行，使用默认值
            
        # 步骤2：获取企业实时数据
        self.fetch_enterprise_data()
        
        # 步骤3：分析扩张信号
        self.analyze_expansion_signals()
        
        # 步骤4：生成对话剧本
        self.generate_dialogue_script()
        
        # 步骤5：分析竞品对比
        self.analyze_competitors()
        
        # 步骤6：生成简报文档
        output_file = self.generate_briefing_document()
        
        print(f"=" * 50)
        print(f"🎉 会前简报生成完成！")
        print(f"📋 简报文件: {output_file}")
        print(f"⏰ 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return output_file

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python3 generate_briefing.py <企业名称> [联系人姓名]")
        print("示例: python3 generate_briefing.py \"XX科技公司\" \"张总\"")
        sys.exit(1)
    
    enterprise_name = sys.argv[1]
    contact_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    generator = BriefingGenerator(enterprise_name, contact_name)
    output_file = generator.generate()
    
    if output_file:
        print(f"\n📊 简报内容摘要:")
        print(f"   企业名称: {enterprise_name}")
        print(f"   生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   简报文件: {output_file}")
        print(f"\n💡 使用建议:")
        print(f"   1. 打印简报，会见前阅读")
        print(f"   2. 使用语音播报功能（需配置TTS）")
        print(f"   3. 根据实际情况调整对话剧本")
    else:
        print(f"❌ 会前简报生成失败")
        sys.exit(1)

if __name__ == "__main__":
    main()