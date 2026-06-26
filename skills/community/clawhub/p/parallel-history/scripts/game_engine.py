#!/usr/bin/env python3
"""
平行历史游戏引擎 - 辅助工具
用于生成历史背景、推演历史演变
"""

import json
import random
from datetime import datetime
from pathlib import Path

class ParallelHistoryEngine:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data"
        self.state_file = self.data_dir / "state.json"
        self.state = self.load_state()
    
    def load_state(self):
        """加载游戏状态"""
        if self.state_file.exists():
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_state(self):
        """保存游戏状态"""
        self.state['metadata']['last_updated'] = datetime.now().isoformat()
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)
    
    def calculate_success_rate(self, base_rate, faction_strength, historical_trend, player_reputation):
        """计算决策成功率"""
        rate = base_rate * faction_strength * historical_trend * player_reputation
        return max(0.1, min(0.95, rate))  # 限制在10%-95%
    
    def evolve_organization(self, org, years):
        """推演组织演变"""
        influence_change = random.uniform(-10, 15)
        stability_change = random.uniform(-15, 10)
        member_growth = random.uniform(0.95, 1.10)  # -5% to +10%
        
        org['influence'] = max(0, min(100, org['influence'] + influence_change))
        org['stability'] = max(0, min(100, org['stability'] + stability_change))
        org['members'] = int(org['members'] * member_growth)
        
        # 判断组织状态
        if org['influence'] < 30 or org['stability'] < 40:
            org['status'] = 'underground'
        elif org['members'] < 100 or org['influence'] == 0:
            org['status'] = 'extinct'
        else:
            org['status'] = 'active'
        
        return org
    
    def evolve_sect(self, sect, years):
        """推演教派演变"""
        believer_growth = random.uniform(0.90, 1.20)  # -10% to +20%
        doctrine_purity_change = random.uniform(-5, 2)
        institutionalization_change = random.uniform(1, 5)
        
        sect['believers'] = int(sect['believers'] * believer_growth)
        sect['doctrine_purity'] = max(0, min(100, sect['doctrine_purity'] + doctrine_purity_change))
        sect['institutionalization'] = max(0, min(100, sect['institutionalization'] + institutionalization_change))
        
        # 判断教派状态
        if sect['believers'] < 1000:
            sect['status'] = 'extinct'
        elif believer_growth < 1.03:
            sect['status'] = 'declining'
        elif believer_growth < 1.10:
            sect['status'] = 'stable'
        else:
            sect['status'] = 'growing'
        
        return sect
    
    def generate_historical_event(self, year, region):
        """生成历史事件（简化版）"""
        events = {
            'europe_1918': [
                "德国爆发十一月革命",
                "《凡尔赛条约》签订",
                "魏玛共和国成立",
                "希特勒啤酒馆暴动",
                "德国加入国际联盟"
            ],
            'china_1840': [
                "鸦片战争爆发",
                "《南京条约》签订",
                "太平天国运动",
                "第二次鸦片战争",
                "洋务运动开始"
            ]
        }
        
        key = f"{region}_{year // 100 * 100}"
        if key in events:
            return random.choice(events[key])
        return f"{year}年历史演变"
    
    def calculate_legacy_score(self, organization, sect, decisions):
        """计算遗产分数"""
        score = 0
        
        # 组织贡献
        if organization:
            score += organization['influence'] * 0.3
            score += organization['stability'] * 0.2
            if organization['status'] == 'active':
                score += 20
        
        # 教派贡献
        if sect:
            score += sect['doctrine_purity'] * 0.2
            score += min(30, sect['believers'] / 10000)
            if sect['status'] == 'growing':
                score += 15
        
        # 决策影响
        for decision in decisions:
            score += decision.get('impact', 0)
        
        return max(-100, min(100, score))
    
    def calculate_historical_evaluation(self, legacy_score, organization, sect):
        """计算历史评价"""
        evaluation = legacy_score
        
        # 额外修正
        if organization and organization['status'] == 'extinct':
            evaluation -= 20
        if sect and sect['status'] == 'extinct':
            evaluation -= 15
        
        return max(-100, min(100, evaluation))
    
    def determine_ending(self, historical_evaluation):
        """判定结局"""
        if historical_evaluation >= 60:
            return 'glory', self.get_glory_level(historical_evaluation)
        elif historical_evaluation <= -60:
            return 'shame', self.get_shame_level(historical_evaluation)
        else:
            return 'neutral', 'ordinary'
    
    def get_glory_level(self, score):
        """获取荣耀等级"""
        if score >= 90:
            return 'legendary'
        elif score >= 80:
            return 'great'
        elif score >= 70:
            return 'outstanding'
        else:
            return 'excellent'
    
    def get_shame_level(self, score):
        """获取耻辱等级"""
        if score <= -90:
            return 'demonic'
        elif score <= -80:
            return 'sinner'
        elif score <= -70:
            return 'shameful'
        else:
            return 'failure'

# 使用示例
if __name__ == '__main__':
    engine = ParallelHistoryEngine()
    
    # 示例：计算成功率
    rate = engine.calculate_success_rate(
        base_rate=0.6,
        faction_strength=0.8,
        historical_trend=0.7,
        player_reputation=1.0
    )
    print(f"决策成功率: {rate * 100:.1f}%")
    
    # 示例：组织演变
    org = {
        'name': '魏玛民主联盟',
        'members': 50000,
        'influence': 60,
        'stability': 70,
        'status': 'active'
    }
    evolved_org = engine.evolve_organization(org, 5)
    print(f"组织演变: {evolved_org}")
