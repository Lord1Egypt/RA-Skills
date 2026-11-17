#!/usr/bin/env python3
"""
产业项目综合评分卡与投资决策工具
🐴 本工具为用户开发，2026年5月

功能：
1. 多维度项目评分（8大维度×权重）
2. 自动匹配对标投资机构框架
3. 投资建议和交易结构推荐
4. 输出评分报告

用法：python3 project_scoring_card.py
"""

import json
import os
from datetime import datetime

class ProjectScoringCard:
    """
    产业项目综合评分卡
    总分100分，8大维度
    """
    
    # 评分标准定义
    CRITERIA = {
        '市场/赛道': {
            'weight': 0.20,
            'sub_items': {
                'tam_size': {'weight': 0.05, 'name': 'TAM规模', 'descriptions': {
                    1: '<¥1亿', 3: '¥1-10亿', 5: '¥10-50亿', 
                    7: '¥50-200亿', 10: '>¥200亿'
                }},
                'growth_rate': {'weight': 0.05, 'name': '市场增长率', 'descriptions': {
                    1: '<5%', 3: '5-10%', 5: '10-20%', 
                    7: '20-30%', 10: '>30%'
                }},
                'lifecycle_stage': {'weight': 0.05, 'name': '产业生命周期', 'descriptions': {
                    1: '衰退期', 3: '导入期', 5: '导入期偏成熟',
                    7: '成长期', 10: '成长期偏成熟'
                }},
                'competitive_landscape': {'weight': 0.05, 'name': '竞争格局', 'descriptions': {
                    1: '完全竞争/红海', 3: '分散竞争', 5: '寡头竞争',
                    7: '少量寡头', 10: '垄断/蓝海'
                }}
            }
        },
        '商业模式': {
            'weight': 0.15,
            'sub_items': {
                'revenue_model': {'weight': 0.04, 'name': '收入模式', 'descriptions': {
                    1: '一次性收入', 3: '低频交易', 5: '混合模式',
                    7: '高频复购', 10: '订阅式/经常性收入'
                }},
                'gross_margin': {'weight': 0.04, 'name': '毛利率', 'descriptions': {
                    1: '<10%', 3: '10-20%', 5: '20-35%',
                    7: '35-50%', 10: '>50%'
                }},
                'cash_flow': {'weight': 0.04, 'name': '现金流模式', 'descriptions': {
                    1: '重度负现金流', 3: '轻度负现金流', 5: '接近平衡',
                    7: '轻度正现金流', 10: '强正现金流'
                }},
                'scalability': {'weight': 0.03, 'name': '可扩展性', 'descriptions': {
                    1: '线性增长', 3: '弱规模效应', 5: '中度规模效应',
                    7: '强规模效应', 10: '指数级网络效应'
                }}
            }
        },
        '团队': {
            'weight': 0.15,
            'sub_items': {
                'founder_exp': {'weight': 0.05, 'name': '创始人经验', 'descriptions': {
                    1: '首次创业/外行', 3: '相关行业经验', 5: '5年+行业经验',
                    7: '连续创业者', 10: '成功退出经历'
                }},
                'team_completeness': {'weight': 0.05, 'name': '团队完整度', 'descriptions': {
                    1: '只有创始人', 3: '2-3人核心', 5: '有核心部门',
                    7: '完整管理团队', 10: '全明星阵容'
                }},
                'track_record': {'weight': 0.05, 'name': '过往执行力', 'descriptions': {
                    1: '无记录', 3: '有项目但延期', 5: '按时交付',
                    7: '超预期交付', 10: '行业标杆'
                }}
            }
        },
        '技术/壁垒': {
            'weight': 0.15,
            'sub_items': {
                'tech_uniqueness': {'weight': 0.05, 'name': '技术独特性', 'descriptions': {
                    1: '完全复制', 3: '微创新', 5: '差异化',
                    7: '显著领先', 10: '颠覆性创新'
                }},
                'ip_protection': {'weight': 0.05, 'name': 'IP保护', 'descriptions': {
                    1: '无IP', 3: '申请中', 5: '已授权专利',
                    7: '核心专利群', 10: '专利护城河'
                }},
                'moat_durability': {'weight': 0.05, 'name': '壁垒持久性', 'descriptions': {
                    1: '1年内被复制', 3: '1-2年', 5: '2-3年',
                    7: '3-5年', 10: '5年以上'
                }}
            }
        },
        '财务预测': {
            'weight': 0.10,
            'sub_items': {
                'assumption_reasonableness': {'weight': 0.04, 'name': '假设合理性', 'descriptions': {
                    1: '拍脑袋', 3: '有依据但乐观', 5: '合理',
                    7: '保守稳健', 10: '极度保守'
                }},
                'profit_path': {'weight': 0.03, 'name': '盈利路径', 'descriptions': {
                    1: '持续亏损无明确路径', 3: '2-3年后可能盈亏平衡',
                    5: '1-2年盈亏平衡', 7: '已盈亏平衡', 10: '已盈利并增长'
                }},
                'capex_efficiency': {'weight': 0.03, 'name': '资本效率', 'descriptions': {
                    1: '极高Capex要求', 3: '较高Capex', 5: '中等Capex',
                    7: '低Capex', 10: '轻资产模型'
                }}
            }
        },
        '风险/回报': {
            'weight': 0.15,
            'sub_items': {
                'irr_achievement': {'weight': 0.05, 'name': 'IRR达标', 'descriptions': {
                    1: '<10%', 3: '10-15%', 5: '15-20%',
                    7: '20-30%', 10: '>30%'
                }},
                'downside_protection': {'weight': 0.05, 'name': '下行保护', 'descriptions': {
                    1: '无保护', 3: '弱(股权无抵押)', 5: '中等(资产抵押部分)',
                    7: '良好(资产足值抵押)', 10: '强(多种保护机制)'
                }},
                'exit_certainty': {'weight': 0.05, 'name': '退出确定性', 'descriptions': {
                    1: '无明确退出路径', 3: '退出路径不清晰',
                    5: '有1-2种退出可能', 7: '退出路径明确',
                    10: '已锁定退出渠道'
                }}
            }
        },
        '公司治理/ESG': {
            'weight': 0.05,
            'sub_items': {
                'governance': {'weight': 0.02, 'name': '公司治理', 'descriptions': {
                    1: '家族式管理', 3: '有董事会但形式', 5: '规范治理',
                    7: '独立董事制度', 10: '上市公司治理标准'
                }},
                'esg': {'weight': 0.02, 'name': 'ESG达标', 'descriptions': {
                    1: '严重环保问题', 3: '有瑕疵', 5: '基本达标',
                    7: '良好ESG表现', 10: 'ESG标杆企业'
                }},
                'regulatory': {'weight': 0.01, 'name': '监管合规', 'descriptions': {
                    1: '严重违规', 3: '有违规风险', 5: '基本合规',
                    7: '良好合规记录', 10: '零违规记录'
                }}
            }
        }
    }
    
    # 对标机构映射
    FIRM_MAPPING = {
        (85, 100): {
            'firm': '高瓴资本/红杉资本',
            'action': '立即推进，争取领投/独家投资',
            'dd_depth': '标准尽调（4-6周）',
            'valuation': '接受10-20%溢价',
            'structure': '普通股或优先股+1x清算'
        },
        (70, 84): {
            'firm': '红杉资本/某大型集团',
            'action': '有序推进，获得跟投或联合投资权',
            'dd_depth': '深度尽调（6-8周）',
            'valuation': '市场估值区间',
            'structure': '优先股+参与权'
        },
        (55, 69): {
            'firm': '黑石/某大型集团',
            'action': '有条件推进，设立里程碑，分阶段投资',
            'dd_depth': '深度尽调（8-10周）',
            'valuation': '要求15-20%折价',
            'structure': '可转债+对赌条款'
        },
        (40, 54): {
            'firm': '—',
            'action': '暂时搁置，关注动态，保持联系',
            'dd_depth': '快速扫调（2周）',
            'valuation': '仅考虑大幅折价',
            'structure': '先签TS观望'
        },
        (0, 39): {
            'firm': '—',
            'action': '放弃，但记录原因供未来参考',
            'dd_depth': '无需尽调',
            'valuation': '不适用',
            'structure': '不适用'
        }
    }
    
    def __init__(self, project_name="未命名项目"):
        self.project_name = project_name
        self.scores = {}
        self.total_score = 0
        self.raw_input = {}
        
    def score(self, dimension, sub_item, value):
        """
        给某个子项打分
        value: 1-10 之间的整数
        """
        if dimension not in self.raw_input:
            self.raw_input[dimension] = {}
            self.scores[dimension] = {}
        
        self.raw_input[dimension][sub_item] = value
        self.scores[dimension][sub_item] = value
        
        return self
    
    def score_dimension_from_dict(self, dimension, score_dict):
        """
        从字典批量打分
        score_dict: {sub_item_name: score_value}
        """
        if dimension not in self.scores:
            self.scores[dimension] = {}
            self.raw_input[dimension] = {}
        
        for sub_item, value in score_dict.items():
            self.scores[dimension][sub_item] = value
            self.raw_input[dimension][sub_item] = value
        
        return self
    
    def quick_score(self, **kwargs):
        """
        快速打分：直接传维度名=子项得分字典
        示例：quick_score(市场=..., 团队=...)
        """
        dimension_mapping = {
            '市场': '市场/赛道',
            '商业模式': '商业模式',
            '团队': '团队',
            '技术': '技术/壁垒',
            '财务': '财务预测',
            '风险': '风险/回报',
            '治理': '公司治理/ESG'
        }
        
        for dim_key, scores in kwargs.items():
            real_dim = dimension_mapping.get(dim_key, dim_key)
            if real_dim in self.CRITERIA:
                self.score_dimension_from_dict(real_dim, scores)
        
        return self
    
    def calculate(self):
        """
        计算总分
        """
        total = 0
        dimension_details = []
        
        for dimension, config in self.CRITERIA.items():
            dim_weight = config['weight']
            dim_score = 0
            dim_max = 0
            sub_details = []
            
            for sub_name, sub_config in config['sub_items'].items():
                sub_weight = sub_config['weight']
                sub_score = self.scores.get(dimension, {}).get(sub_name, 5)  # 默认给5分
                
                weighted_sub = sub_score * sub_weight
                dim_score += weighted_sub
                dim_max += 10 * sub_weight
                
                sub_details.append({
                    'name': sub_config['name'],
                    'score': sub_score,
                    'weight': sub_weight,
                    'weighted': weighted_sub,
                    'description': sub_config['descriptions'].get(sub_score, '')
                })
            
            # 归一化到维度权重
            dim_final = dim_score / dim_max * 100 * dim_weight
            total += dim_final
            
            dimension_details.append({
                'name': dimension,
                'weight': dim_weight,
                'raw_score': dim_score,
                'max_score': dim_max,
                'pct': dim_score / dim_max * 100 if dim_max > 0 else 0,
                'weighted_contribution': dim_final / total * 100 if total > 0 else 0,
                'sub_items': sub_details
            })
        
        self.total_score = min(total, 100)  # 上限100
        self.dimension_details = dimension_details
        
        # 判断评级
        for (low, high), mapping in sorted(self.FIRM_MAPPING.items(), reverse=True):
            if low <= self.total_score <= high:
                self.rating = mapping
                self.rating_name = {
                    (85, 100): '⭐⭐⭐⭐⭐ 极力推荐',
                    (70, 84): '⭐⭐⭐⭐ 推荐',
                    (55, 69): '⭐⭐⭐ 有条件',
                    (40, 54): '⭐⭐ 观望',
                    (0, 39): '⭐ 放弃'
                }[(low, high)]
                self.rating_range = (low, high)
                break
        
        return self
    
    def print_report(self):
        """打印评分报告"""
        print(f"\n{'='*60}")
        print(f"📊 项目综合评分报告: {self.project_name}")
        print(f"{'='*60}")
        
        # 总分
        print(f"\n  总分: {self.total_score:.1f}/100  |  评级: {self.rating_name}")
        print(f"  对标机构: {self.rating['firm']}")
        print(f"  建议行动: {self.rating['action']}")
        print(f"{'='*60}")
        
        # 各维度分析
        print(f"\n--- 各维度评分详情 ---")
        for dim in self.dimension_details:
            bar = "█" * int(dim['pct'] / 5)
            print(f"\n{dim['name']} ({dim['weight']*100:.0f}%)")
            print(f"  维度得分: {dim['raw_score']:.1f}/{dim['max_score']:.1f} ({dim['pct']:.0f}%) {bar}")
            for sub in dim['sub_items']:
                sub_bar = "▌" * sub['score']
                print(f"    ├─ {sub['name']:20s} {sub['score']:3d}/10 {sub_bar}")
                if sub['description']:
                    print(f"    │  ({sub['description']})")
        
        # 综合建议
        print(f"\n--- 投资建议 ---")
        print(f"  🏢 对标机构: {self.rating['firm']}")
        print(f"  🎯 行动: {self.rating['action']}")
        print(f"  🔍 尽调深度: {self.rating['dd_depth']}")
        print(f"  💰 估值建议: {self.rating['valuation']}")
        print(f"  📝 建议结构: {self.rating['structure']}")
        
        # 优劣势分析
        print(f"\n--- 优劣势分析 ---")
        sorted_dims = sorted(self.dimension_details, key=lambda x: x['pct'])
        strengths = [d for d in sorted_dims if d['pct'] >= 70]
        weaknesses = [d for d in sorted_dims if d['pct'] < 50]
        
        if strengths:
            print(f"  ✅ 优势维度:")
            for s in strengths:
                print(f"    - {s['name']}: {s['pct']:.0f}%")
        if weaknesses:
            print(f"  ⚠️ 需关注维度:")
            for w in weaknesses:
                print(f"    - {w['name']}: {w['pct']:.0f}%")
                # 找出具体低分子项
                for sub in w['sub_items']:
                    if sub['score'] < 5:
                        print(f"      └ {sub['name']}: {sub['score']}/10 ({sub['description']})")
        
        print(f"\n{'='*60}\n")
        
        return self
    
    def to_dict(self):
        """输出为字典"""
        return {
            'project_name': self.project_name,
            'total_score': self.total_score,
            'rating_name': self.rating_name,
            'firm': self.rating['firm'],
            'action': self.rating['action'],
            'dimensions': self.dimension_details,
            'score_range': self.rating_range
        }


# ========== 使用示例 ==========
if __name__ == "__main__":
    print("🐴 产业项目综合评分卡")
    print("="*60)
    
    card = ProjectScoringCard("示例: AI驱动的工业质检项目")
    
    # 可以通过两种方式打分
    
    # 方式1: 逐项打分
    card.score('市场/赛道', 'tam_size', 8)          # TAM ¥50亿+
    card.score('市场/赛道', 'growth_rate', 9)       # 增长率>30%
    card.score('市场/赛道', 'lifecycle_stage', 7)   # 成长期
    card.score('市场/赛道', 'competitive_landscape', 6)  # 少量寡头
    
    # 方式2: 批量打分
    card.score_dimension_from_dict('商业模式', {
        'revenue_model': 7,    # 高频复购+SaaS
        'gross_margin': 8,     # >50%
        'cash_flow': 6,        # 轻度正现金流
        'scalability': 8       # 强规模效应
    })
    
    card.score_dimension_from_dict('团队', {
        'founder_exp': 8,      # 连续创业者
        'team_completeness': 7, # 完整管理团队
        'track_record': 7      # 超预期交付
    })
    
    card.score_dimension_from_dict('技术/壁垒', {
        'tech_uniqueness': 8,  # 显著领先
        'ip_protection': 7,    # 核心专利群
        'moat_durability': 7   # 3-5年壁垒
    })
    
    card.score_dimension_from_dict('财务预测', {
        'assumption_reasonableness': 6,
        'profit_path': 6,
        'capex_efficiency': 7
    })
    
    card.score_dimension_from_dict('风险/回报', {
        'irr_achievement': 7,
        'downside_protection': 6,
        'exit_certainty': 7
    })
    
    card.score_dimension_from_dict('公司治理/ESG', {
        'governance': 7,
        'esg': 8,
        'regulatory': 8
    })
    
    # 方式3: 快速打分（可用于快速评估）
    # card.quick_score(
    #     市场={'tam_size': 7, 'growth_rate': 8, 'lifecycle_stage': 7, 'competitive_landscape': 6},
    #     团队={'founder_exp': 8, 'team_completeness': 7, 'track_record': 7}
    # )
    
    # 计算总分并输出
    card.calculate()
    card.print_report()
