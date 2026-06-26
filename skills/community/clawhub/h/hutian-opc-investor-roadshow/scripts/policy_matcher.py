#!/usr/bin/env python3
"""
政策匹配脚本
胡田-OPC导师-招商引流工具包

功能：根据企业特征匹配最佳政策组合
"""

import json
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class Policy:
    """政策数据模型"""
    id: str
    name: str
    region: str
    policy_type: str  # 财税/人才/研发/金融/载体
    content: str
    conditions: List[str]
    benefit: str  # 优惠内容描述
    benefit_amount: str  # 金额估算
    
    def match_score(self, enterprise: Dict) -> int:
        """计算政策与企业匹配度"""
        score = 0
        
        # 行业匹配
        for cond in self.conditions:
            if "科技" in cond and enterprise.get("is_tech"):
                score += 15
            if "人才" in cond and enterprise.get("has_talent_demand"):
                score += 10
            if "研发" in cond and enterprise.get("has_rd"):
                score += 15
            if "中小企业" in cond and enterprise.get("is_small"):
                score += 10
            if "瞪羚" in cond and enterprise.get("is_gazelle"):
                score += 20
            if "独角兽" in cond and enterprise.get("is_unicorn"):
                score += 25
                
        return min(score, 100)


class PolicyDatabase:
    """政策数据库"""
    
    def __init__(self):
        self.policies: List[Policy] = []
        self._init_policies()
    
    def _init_policies(self):
        """初始化政策库"""
        # 国家级政策
        self.policies.extend([
            Policy(
                id="CN-GAO-001",
                name="高新技术企业税收优惠",
                region="全国",
                policy_type="财税",
                content="企业所得税按15%征收",
                conditions=["科技企业", "高新技术企业认定"],
                benefit="企业所得税15%",
                benefit_amount="节省10%税负"
            ),
            Policy(
                id="CN-RD-001",
                name="研发费用加计扣除",
                region="全国",
                policy_type="研发",
                content="研发费用加计扣除比例75-100%",
                conditions=["有研发", "科技型中小企业"],
                benefit="加计扣除75-100%",
                benefit_amount="研发费用100万可多抵扣75-100万"
            ),
        ])
        
        # 上海市
        self.policies.extend([
            Policy(
                id="SH-ZJ-001",
                name="张江科学城政策",
                region="上海-张江",
                policy_type="财税",
                content="张江科学城企业享受企业所得税15%",
                conditions=["科技企业", "张江园区入驻"],
                benefit="企业所得税15%",
                benefit_amount="节省10%税负"
            ),
            Policy(
                id="SH-TALENT-001",
                name="海外人才政策",
                region="上海",
                policy_type="人才",
                content="海外高层次人才享受落户、补贴政策",
                conditions=["人才密集", "海归人才"],
                benefit="落户便利+补贴",
                benefit_amount="最高50万安家补贴"
            ),
        ])
        
        # 江苏省-南京
        self.policies.extend([
            Policy(
                id="JS-NJ-TAX-001",
                name="瞪羚独角兽奖励",
                region="南京",
                policy_type="财税",
                content="瞪羚、独角兽企业享受地方留成部分80%奖励",
                conditions=["瞪羚企业", "独角兽企业"],
                benefit="地方留成80%奖励",
                benefit_amount="年省税收约100-500万"
            ),
            Policy(
                id="JS-NJ-TALENT-001",
                name="人才安居政策",
                region="南京",
                policy_type="人才",
                content="认定人才享受购房补贴、租房补贴",
                conditions=["人才密集", "高层次人才"],
                benefit="购房/租房补贴",
                benefit_amount="最高200万购房补贴"
            ),
            Policy(
                id="JS-NJ-RD-001",
                name="研发费用补贴",
                region="南京",
                policy_type="研发",
                content="科技型中小企业研发费用补贴10%",
                conditions=["有研发", "科技型中小企业"],
                benefit="研发费用补贴10%",
                benefit_amount="年研发1000万可获100万补贴"
            ),
        ])
        
        # 江苏省-苏州
        self.policies.extend([
            Policy(
                id="JS-SZ-001",
                name="瞪羚企业补贴",
                region="苏州",
                policy_type="财税",
                content="瞪羚企业享受地方留成部分80%",
                conditions=["瞪羚企业"],
                benefit="地方留成80%奖励",
                benefit_amount="年省税收约100-500万"
            ),
            Policy(
                id="JS-SZ-TALENT-001",
                name="姑苏人才计划",
                region="苏州",
                policy_type="人才",
                content="领军人才最高500万安家补贴",
                conditions=["高层次人才", "领军人才"],
                benefit="安家补贴",
                benefit_amount="最高500万"
            ),
            Policy(
                id="JS-SZ-FUND-001",
                name="产业基金跟投",
                region="苏州",
                policy_type="金融",
                content="产业基金跟投不超过20%",
                conditions=["融资需求", "成长期企业"],
                benefit="基金跟投",
                benefit_amount="融资支持"
            ),
        ])
        
        # 浙江省-杭州
        self.policies.extend([
            Policy(
                id="ZJ-HZ-001",
                name="凤凰行动上市补贴",
                region="杭州",
                policy_type="金融",
                content="上市后备企业最高150万补贴",
                conditions=["上市筹备", "Pre-IPO"],
                benefit="上市补贴",
                benefit_amount="最高150万"
            ),
            Policy(
                id="ZJ-HZ-TALENT-001",
                name="人才生态最优市政策",
                region="杭州",
                policy_type="人才",
                content="A类人才购房补贴最高800万",
                conditions=["高层次人才", "顶尖人才"],
                benefit="购房补贴",
                benefit_amount="最高800万"
            ),
        ])
        
        # 四川省-成都
        self.policies.extend([
            Policy(
                id="SC-CD-001",
                name="产业功能区政策",
                region="成都",
                policy_type="财税",
                content="功能区企业享受税收全返前3年",
                conditions=["入驻功能区"],
                benefit="税收全返3年",
                benefit_amount="前3年税收全返"
            ),
            Policy(
                id="SC-CD-TALENT-001",
                name="人才安居政策",
                region="成都",
                policy_type="人才",
                content="认定人才购房享受最高20%优惠",
                conditions=["人才密集", "高层次人才"],
                benefit="购房优惠",
                benefit_amount="房价20%优惠"
            ),
            Policy(
                id="SC-CD-FUND-001",
                name="上市补贴",
                region="成都",
                policy_type="金融",
                content="上市企业最高500万补贴",
                conditions=["上市筹备"],
                benefit="上市补贴",
                benefit_amount="最高500万"
            ),
        ])
        
        # 广东省-深圳
        self.policies.extend([
            Policy(
                id="GD-SZ-001",
                name="南山领航计划",
                region="深圳-南山",
                policy_type="研发",
                content="高新技术企业研发补贴最高1000万",
                conditions=["高新技术企业", "有研发"],
                benefit="研发补贴",
                benefit_amount="最高1000万"
            ),
            Policy(
                id="GD-SZ-TALENT-001",
                name="新引进人才补贴",
                region="深圳",
                policy_type="人才",
                content="新引进人才补贴本科1.5万/硕士2.5万/博士3万",
                conditions=["人才密集", "应届毕业生"],
                benefit="人才补贴",
                benefit_amount="本科1.5万/硕士2.5万/博士3万"
            ),
        ])
    
    def search(self, region: str = "", policy_type: str = "") -> List[Policy]:
        """搜索政策"""
        results = self.policies
        if region:
            results = [p for p in results if region in p.region]
        if policy_type:
            results = [p for p in results if p.policy_type == policy_type]
        return results
    
    def match(self, enterprise: Dict) -> List[Dict]:
        """为企业匹配政策"""
        matched = []
        
        for policy in self.policies:
            score = policy.match_score(enterprise)
            if score > 0:
                matched.append({
                    "policy": policy,
                    "score": score
                })
        
        # 按匹配度排序
        matched.sort(key=lambda x: x["score"], reverse=True)
        
        return matched[:10]  # 返回前10个最匹配的政策


class PolicyMatcher:
    """政策匹配器"""
    
    def __init__(self):
        self.db = PolicyDatabase()
    
    def match_enterprise(self, enterprise: Dict) -> Dict:
        """匹配企业政策"""
        matched = self.db.match(enterprise)
        
        result = {
            "enterprise": enterprise.get("name", "未知"),
            "match_count": len(matched),
            "policies": [],
            "summary": {
                "total_benefit": 0,
                "policy_types": set()
            }
        }
        
        for item in matched:
            policy = item["policy"]
            result["policies"].append({
                "id": policy.id,
                "name": policy.name,
                "region": policy.region,
                "type": policy.policy_type,
                "benefit": policy.benefit,
                "benefit_amount": policy.benefit_amount,
                "match_score": item["score"]
            })
            result["summary"]["policy_types"].add(policy.policy_type)
        
        result["summary"]["policy_types"] = list(result["summary"]["policy_types"])
        
        return result
    
    def generate_report(self, result: Dict) -> str:
        """生成政策匹配报告"""
        report = "=" * 60 + "\n"
        report += f"政策匹配报告 - {result['enterprise']}\n"
        report += "=" * 60 + "\n\n"
        
        report += f"匹配到 {result['match_count']} 项适用政策\n\n"
        
        report += "-" * 40 + "\n"
        report += "推荐政策清单\n"
        report += "-" * 40 + "\n\n"
        
        for i, policy in enumerate(result["policies"], 1):
            report += f"{i}. {policy['name']}（{policy['region']}）\n"
            report += f"   类型：{policy['type']} | 匹配度：{policy['match_score']}%\n"
            report += f"   优惠：{policy['benefit']}\n"
            report += f"   估算：{policy['benefit_amount']}\n\n"
        
        report += "-" * 40 + "\n"
        report += f"政策类型覆盖：{', '.join(result['summary']['policy_types'])}\n"
        report += "-" * 40 + "\n"
        
        return report


# 示例用法
if __name__ == "__main__":
    matcher = PolicyMatcher()
    
    # 企业1：深圳智链科技
    ent1 = {
        "name": "深圳智链科技有限公司",
        "region": "华东",
        "is_tech": True,
        "is_gazelle": False,
        "has_rd": True,
        "has_talent_demand": True
    }
    
    # 企业2：苏州蓝鲸智能
    ent2 = {
        "name": "苏州蓝鲸智能科技有限公司",
        "region": "苏州",
        "is_tech": True,
        "is_gazelle": True,
        "has_rd": True,
        "has_talent_demand": True
    }
    
    # 企业3：成都某企业
    ent3 = {
        "name": "成都某科技有限公司",
        "region": "成都",
        "is_tech": True,
        "is_gazelle": False,
        "has_rd": True,
        "has_talent_demand": True
    }
    
    for enterprise in [ent1, ent2, ent3]:
        result = matcher.match_enterprise(enterprise)
        print(matcher.generate_report(result))
        print()
