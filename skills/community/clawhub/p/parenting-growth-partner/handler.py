"""
Parenting Growth Partner - Main Handler
"""
import json
from typing import Dict, Any
from engine.milestones import MilestoneEngine
from engine.activities import ActivityEngine
from engine.communication import CommunicationEngine
from engine.behavior import BehaviorEngine

class ParentingGrowthPartner:
    def __init__(self):
        self.milestone_engine = MilestoneEngine()
        self.activity_engine = ActivityEngine()
        self.communication_engine = CommunicationEngine()
        self.behavior_engine = BehaviorEngine()
    
    def handle_milestone_assessment(self, age_months: int, observations: Dict = None) -> Dict:
        """处理发展里程碑评估"""
        try:
            assessment = self.milestone_engine.assess_milestones(age_months, observations)
            recommendations = self.milestone_engine.generate_recommendations(assessment)
            
            return {
                'success': True,
                'assessment': assessment,
                'recommendations': recommendations,
                'summary': {
                    'development_status': assessment['summary']['development_status'],
                    'milestones_checked': assessment['total_milestones_checked'],
                    'milestones_achieved': assessment['summary']['milestones_achieved_count']
                }
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def handle_activity_recommendation(self, age_months: int, available_time: int = 30, 
                                       preferred_domains: list = None) -> Dict:
        """处理活动推荐"""
        try:
            recommendations = self.activity_engine.recommend_activities(
                age_months, available_time, preferred_domains
            )
            
            return {
                'success': True,
                'recommendations': recommendations,
                'summary': recommendations['summary']
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def handle_communication_guidance(self, scenario: str, child_age_months: int = None) -> Dict:
        """处理沟通指导"""
        try:
            guidance = self.communication_engine.get_guidance(scenario, child_age_months)
            
            return {
                'success': True,
                'scenario': scenario,
                'guidance': guidance,
                'quick_tips': [
                    '保持冷静，先处理情绪再处理问题',
                    '蹲下与孩子平视交流',
                    '使用“我”语句表达感受'
                ]
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def handle_behavior_analysis(self, behavior_description: str, frequency: str, 
                                 context: str, child_age_months: int = None) -> Dict:
        """处理行为分析"""
        try:
            analysis = self.behavior_engine.analyze_behavior(behavior_description, frequency, context)
            
            if child_age_months and analysis['possible_patterns']:
                pattern_name = analysis['possible_patterns'][0]['pattern']
                discipline_plan = self.behavior_engine.get_positive_discipline_plan(
                    pattern_name, child_age_months
                )
                analysis['discipline_plan'] = discipline_plan
            
            return {
                'success': True,
                'analysis': analysis,
                'next_steps': [
                    '尝试1-2个推荐技巧',
                    '观察一周记录变化',
                    '根据效果调整策略'
                ]
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def handle_daily_routine_suggestion(self, child_age_months: int) -> Dict:
        """处理日常作息建议"""
        try:
            # Age-based routine suggestions
            if child_age_months < 12:
                routine = {
                    'wake_up': '7:00-8:00',
                    'naps': '2-3次小睡',
                    'meals': '母乳/配方奶 + 辅食2-3次',
                    'active_play': '多次短时间活动',
                    'bedtime': '19:00-20:00'
                }
                tips = ['保持喂养和睡眠规律', '白天充分活动促进夜间睡眠']
            elif child_age_months < 36:
                routine = {
                    'wake_up': '7:00-8:00',
                    'naps': '1次午睡（2-3小时）',
                    'meals': '3餐 + 2次点心',
                    'active_play': '上午和下午各1小时',
                    'quiet_time': '午睡前30分钟',
                    'bedtime': '20:00-21:00'
                }
                tips = ['建立固定的睡前程序', '确保白天充足户外活动']
            else:
                routine = {
                    'wake_up': '7:00-8:00',
                    'meals': '3餐 + 1次点心',
                    'active_play': '至少2小时',
                    'learning_time': '30-60分钟',
                    'family_time': '晚餐后30分钟',
                    'bedtime': '20:30-21:30'
                }
                tips = ['让孩子参与制定作息表', '使用视觉提示帮助孩子理解']
            
            return {
                'success': True,
                'age_months': child_age_months,
                'suggested_routine': routine,
                'tips': tips,
                'flexibility_note': '根据孩子实际情况调整，保持大致规律即可'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

def handler(event, context):
    """Main handler function for OpenClaw skill"""
    partner = ParentingGrowthPartner()
    
    # Parse input
    action = event.get('action', 'milestone_assessment')
    params = event.get('params', {})
    
    # Route to appropriate handler
    if action == 'milestone_assessment':
        age_months = params.get('age_months', 24)
        observations = params.get('observations')
        result = partner.handle_milestone_assessment(age_months, observations)
    
    elif action == 'activity_recommendation':
        age_months = params.get('age_months', 24)
        available_time = params.get('available_time', 30)
        preferred_domains = params.get('preferred_domains')
        result = partner.handle_activity_recommendation(age_months, available_time, preferred_domains)
    
    elif action == 'communication_guidance':
        scenario = params.get('scenario', 'tantrum')
        child_age_months = params.get('child_age_months')
        result = partner.handle_communication_guidance(scenario, child_age_months)
    
    elif action == 'behavior_analysis':
        behavior_description = params.get('behavior_description', '')
        frequency = params.get('frequency', 'occasional')
        context = params.get('context', '')
        child_age_months = params.get('child_age_months')
        result = partner.handle_behavior_analysis(behavior_description, frequency, context, child_age_months)
    
    elif action == 'daily_routine':
        child_age_months = params.get('child_age_months', 24)
        result = partner.handle_daily_routine_suggestion(child_age_months)
    
    else:
        result = {'success': False, 'error': f'Unknown action: {action}'}
    
    return result

if __name__ == '__main__':
    """Self-test when run directly"""
    print('=== Parenting Growth Partner Self-Test ===')
    
    partner = ParentingGrowthPartner()
    
    # Test 1: Milestone assessment
    print('
1. Testing milestone assessment (24 months):')
    result1 = partner.handle_milestone_assessment(24)
    print(f'   Success: {result1["success"]}')
    print(f'   Development status: {result1["assessment"]["summary"]["development_status"]}')
    
    # Test 2: Activity recommendation
    print('
2. Testing activity recommendation (24 months, 30 min):')
    result2 = partner.handle_activity_recommendation(24, 30)
    print(f'   Success: {result2["success"]}')
    print(f'   Activities available: {result2["summary"]["total_available"]}')
    
    # Test 3: Communication guidance
    print('
3. Testing communication guidance (tantrum scenario):')
    result3 = partner.handle_communication_guidance('tantrum', 24)
    print(f'   Success: {result3["success"]}')
    print(f'   Techniques: {len(result3["guidance"]["techniques"])}')
    
    # Test 4: Behavior analysis
    print('
4. Testing behavior analysis:')
    result4 = partner.handle_behavior_analysis('经常说“不”，拖延', 'frequent', '被要求做事时', 24)
    print(f'   Success: {result4["success"]}')
    print(f'   Possible patterns: {len(result4["analysis"]["possible_patterns"])}')
    
    # Test 5: Daily routine
    print('
5. Testing daily routine suggestion (24 months):')
    result5 = partner.handle_daily_routine_suggestion(24)
    print(f'   Success: {result5["success"]}')
    print(f'   Bedtime suggestion: {result5["suggested_routine"]["bedtime"]}')
    
    print('
=== Self-test completed ===')
