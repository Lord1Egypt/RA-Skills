#!/usr/bin/env python3
"""
需求诊断系统：从模糊需求推荐人物/主题
"""

import json
from typing import Dict, List


class DemandDiagnostic:
    """需求诊断器"""

    # 需求维度映射
    DEMAND_DIMENSIONS = {
        'decision': {
            'keywords': ['决策', '判断', '选择', '做决定', 'decision', 'choice'],
            'candidates': ['charlie-munger', 'daniel-kahneman', 'ray-dalio'],
            'themes': ['decision-making', 'probabilistic-thinking', 'mental-models']
        },
        'expression': {
            'keywords': ['表达', '写作', '说话', '演讲', 'communication', 'writing'],
            'candidates': ['richard-feynman', 'george-orwell', 'yuval-noah-harari'],
            'themes': ['writing', 'storytelling', 'public-speaking']
        },
        'startup': {
            'keywords': ['创业', '产品', '商业模式', 'startup', 'business'],
            'candidates': ['paul-graham', 'elad-gil', 'peter-thiel'],
            'themes': ['startup', 'product-market-fit', 'entrepreneurship']
        },
        'teaching': {
            'keywords': ['教学', '传播', '讲课', 'teaching', 'education'],
            'candidates': ['richard-feynman', 'joshua-waitzkin'],
            'themes': ['teaching', 'knowledge-transfer', 'learning']
        },
        'critical_thinking': {
            'keywords': ['批判', '识别', '不靠谱', 'critical', 'skeptic'],
            'candidates': ['charlie-munger', 'daniel-kahneman', 'michael-shermer'],
            'themes': ['critical-thinking', 'cognitive-biases', 'skepticism']
        },
        'creativity': {
            'keywords': ['创作', '内容', '视频', '流量', 'creativity', 'content'],
            'candidates': ['james-clear', 'seth-godin', 'ryan-holiday'],
            'themes': ['creativity', 'content-creation', 'attention-economy']
        },
        'life_strategy': {
            'keywords': ['职业', '人生', '方向', 'career', 'life'],
            'candidates': ['naval-ravikant', 'tim-ferriss', 'cal-newport'],
            'themes': ['life-strategy', 'career-planning', 'productivity']
        },
        'risk': {
            'keywords': ['风险', '不确定性', '投资', 'risk', 'uncertainty'],
            'candidates': ['nasim-taleb', 'howard-marks', 'michael-mauboussin'],
            'themes': ['risk-management', 'antifragility', 'investing']
        },
        'design': {
            'keywords': ['设计', '产品', '用户体验', 'design', 'ux', 'product'],
            'candidates': ['don-norman', 'steve-jobs', 'dieter-rams'],
            'themes': ['design-thinking', 'minimalism', 'product-design']
        },
        'humor': {
            'keywords': ['幽默', '有趣', '表达力', 'humor', 'expression'],
            'candidates': ['david-sedaris', 'conan-obrien', 'john-mulaney'],
            'themes': ['humor', 'wit', 'satire']
        }
    }

    # 候选人物/主题数据库
    CANDIDATE_DATABASE = {
        'charlie-munger': {
            'name': '查理·芒格',
            'core_lens': '多元思维模型 + 逆向思考',
            'why_suitable': '擅长用跨学科思维模型做决策，特别适合复杂商业判断',
            'limitations': '过于理性，可能忽略情感因素；需要大量背景知识',
            'type': 'human'
        },
        'richard-feynman': {
            'name': '理查德·费曼',
            'core_lens': '第一性原理 + 费曼技巧',
            'why_suitable': '擅长将复杂概念简化为可理解的形式',
            'limitations': '过于强调简化，可能丢失细节；适合教学但未必适合复杂决策',
            'type': 'human'
        },
        'naval-ravikant': {
            'name': '纳瓦尔',
            'core_lens': '杠杆思维 + 长期主义',
            'why_suitable': '现代财富和幸福的哲学框架，适合职业和人生规划',
            'limitations': '过于理想化，实际执行难度大；更适合战略而非具体操作',
            'type': 'human'
        },
        'nasim-taleb': {
            'name': '纳西姆·塔勒布',
            'core_lens': '反脆弱 + 凸性策略',
            'why_suitable': '应对不确定性和黑天鹅事件的顶级策略',
            'limitations': '过于激进，不适合保守决策；需要高度自律',
            'type': 'human'
        },
        'paul-graham': {
            'name': '保罗·格雷厄姆',
            'core_lens': '第一性原理 + 创业智慧',
            'why_suitable': '创业和产品思维的权威，适合早期创业者',
            'limitations': '过于专注早期创业，不适合成熟企业；需要技术背景',
            'type': 'human'
        },
        # 主题型候选
        'decision-making': {
            'name': '决策科学',
            'core_lens': '概率思维 + 贝叶斯更新',
            'why_suitable': '系统性的决策方法论，融合心理学和经济学',
            'limitations': '过于理性化，实际应用需要适应；不适合快速直觉决策',
            'type': 'theme'
        },
        'antifragility': {
            'name': '反脆弱系统',
            'core_lens': '从波动中获益 + 杠杆选择',
            'why_suitable': '应对不确定性系统的设计原则',
            'limitations': '需要高度自律和长期视角；不适合所有情境',
            'type': 'theme'
        },
        'minimalism': {
            'name': '极简主义',
            'core_lens': '少即是多 + 约束即创意',
            'why_suitable': '设计和产品思维的核心原则',
            'limitations': '可能导致过度简化；不适合需要复杂性的情境',
            'type': 'theme'
        }
    }

    def __init__(self):
        self.diagnostic_history = []

    def diagnose_demand(self, user_input: str) -> Dict:
        """诊断用户需求并推荐候选"""

        # Step 1: 识别需求维度
        dimensions = self._identify_dimensions(user_input)

        # Step 2: 评估是否需要追问
        needs_clarification = self._needs_clarification(user_input, dimensions)

        if needs_clarification:
            return {
                'needs_clarification': True,
                'clarification_question': self._generate_clarification_question(dimensions)
            }

        # Step 3: 生成候选推荐
        candidates = self._generate_candidates(dimensions)

        return {
            'needs_clarification': False,
            'identified_dimensions': dimensions,
            'candidates': candidates
        }

    def _identify_dimensions(self, user_input: str) -> List[str]:
        """识别需求维度"""

        identified = []
        user_input_lower = user_input.lower()

        for dimension_name, dimension_info in self.DEMAND_DIMENSIONS.items():
            for keyword in dimension_info['keywords']:
                if keyword in user_input_lower:
                    if dimension_name not in identified:
                        identified.append(dimension_name)
                    break

        return identified

    def _needs_clarification(self, user_input: str, dimensions: List[str]) -> bool:
        """判断是否需要澄清"""

        # 如果用户表达非常模糊（少于10个字），需要澄清
        if len(user_input) < 10:
            return True

        # 如果没有识别到任何维度，需要澄清
        if not dimensions:
            return True

        # 如果识别到多个维度但用户没有明确偏好，可能需要澄清
        if len(dimensions) > 1 and '主要' not in user_input and '核心' not in user_input:
            return True

        return False

    def _generate_clarification_question(self, dimensions: List[str]) -> str:
        """生成澄清问题"""

        if not dimensions:
            return "你主要想提升哪个方面的能力？比如决策质量、表达能力、创业思维、教学能力、批判思维等？"

        if len(dimensions) == 1:
            dimension = dimensions[0]
            dimension_info = self.DEMAND_DIMENSIONS[dimension]

            # 根据维度生成具体问题
            if dimension == 'decision':
                return "你说的决策主要是哪种场景？比如商业/投资决策，还是职业/人生方向的选择？"
            elif dimension == 'startup':
                return "你是处于创业的哪个阶段？比如想法验证、产品开发、市场扩张？"
            elif dimension == 'life_strategy':
                return "你主要关注职业生涯规划，还是整体人生策略（包括财富、幸福、健康等）？"
            else:
                return f"能具体说一下你在{dimension_info['keywords'][0]}方面遇到的困惑吗？"

        # 多个维度
        dimension_names = [self.DEMAND_DIMENSIONS[d]['keywords'][0] for d in dimensions[:2]]
        return f"你提到的{dimension_names[0]}和{dimension_names[1]}，哪个是更核心的需求？"

    def _generate_candidates(self, dimensions: List[str]) -> List[Dict]:
        """生成候选推荐"""

        candidates = []

        for dimension_name in dimensions:
            dimension_info = self.DEMAND_DIMENSIONS[dimension_name]

            # 从维度获取候选
            for candidate_key in dimension_info['candidates']:
                if candidate_key in self.CANDIDATE_DATABASE:
                    candidate_info = self.CANDIDATE_DATABASE[candidate_key]

                    candidates.append({
                        'candidate_id': candidate_key,
                        'name': candidate_info['name'],
                        'core_lens': candidate_info['core_lens'],
                        'why_suitable': candidate_info['why_suitable'],
                        'limitations': candidate_info['limitations'],
                        'type': candidate_info['type'],
                        'matched_dimension': dimension_name
                    })

        # 去重
        seen = set()
        unique_candidates = []
        for candidate in candidates:
            if candidate['candidate_id'] not in seen:
                seen.add(candidate['candidate_id'])
                unique_candidates.append(candidate)

        # 限制最多3个
        return unique_candidates[:3]

    def clarify_user_response(self, original_input: str, user_response: str) -> Dict:
        """处理用户的澄清响应"""

        # 合并原始输入和响应
        combined_input = f"{original_input} {user_response}"

        # 重新诊断
        return self.diagnose_demand(combined_input)

    def check_existing_skills(self, skills_dir: str) -> List[Dict]:
        """检查已有的Skill"""

        # 简化处理，实际应该扫描目录
        existing_skills = []

        # 模拟检查结果
        return existing_skills


def main():
    import argparse

    parser = argparse.ArgumentParser(description='需求诊断')
    parser.add_argument('--input', type=str, required=True,
                       help='用户输入')
    parser.add_argument('--clarify', type=str,
                       help='用户的澄清响应（如有）')

    args = parser.parse_args()

    diagnostic = DemandDiagnostic()

    if args.clarify:
        result = diagnostic.clarify_user_response(args.input, args.clarify)
    else:
        result = diagnostic.diagnose_demand(args.input)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
