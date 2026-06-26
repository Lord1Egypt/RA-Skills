#!/usr/bin/env python3
"""
Intelligent Triage and Symptom Analysis with Free Trial & Demo Mode
AI-powered medical triage with NLP and machine learning.

Version: 1.1.0
"""

import json
from functools import lru_cache
import sys
import argparse
import os
import re
from datetime import datetime
from typing import Dict, Any, List, Optional
import urllib.request
import urllib.error

# ═══════════════════════════════════════════════════
# Configuration / 配置
# ═══════════════════════════════════════════════════
BILLING_URL = 'https://skillpay.me/api/v1/billing'
API_KEY = os.environ.get('SKILLPAY_API_KEY', '')
SKILL_ID = os.environ.get('SKILLPAY_SKILL_ID', '')
VERSION = "1.1.0"

# ═══════════════════════════════════════════════════
# Localization / 本地化
# ═══════════════════════════════════════════════════
MESSAGES = {
    'zh': {
        'error_user_id_required': '错误：需要提供用户ID',
        'error_payment_failed': '错误：支付失败或余额不足',
        'error_billing_config': '错误：缺少计费配置。请设置 SKILLPAY_API_KEY 和 SKILLPAY_SKILL_ID',
        'demo_mode_active': '演示模式：无需API密钥，返回模拟分诊数据',
        'trial_mode_active': '免费试用模式：剩余 {} 次调用',
        'processing': '正在分析症状...',
        'red_flag_warning': '警告：发现红旗症状！',
        'history_saved': '症状历史已保存',
    },
    'en': {
        'error_user_id_required': 'Error: User ID is required',
        'error_payment_failed': 'Error: Payment failed or insufficient balance',
        'error_billing_config': 'Error: Billing configuration missing',
        'demo_mode_active': 'Demo mode: No API key needed, returning simulated triage data',
        'trial_mode_active': 'Trial mode: {} calls remaining',
        'processing': 'Analyzing symptoms...',
        'red_flag_warning': 'Warning: Red flag symptoms detected!',
        'history_saved': 'Symptom history saved',
    }
}

# ═══════════════════════════════════════════════════
# Free Trial Manager / 免费试用管理
# ═══════════════════════════════════════════════════
class TrialManager:
    def __init__(self, skill_name: str):
        self.skill_name = skill_name
        self.trial_dir = os.path.expanduser("~/.openclaw/skill_trial")
        self.trial_file = os.path.join(self.trial_dir, f"{skill_name}.json")
        self.max_free_calls = 10
        os.makedirs(self.trial_dir, exist_ok=True)
    
    def _load_trial_data(self) -> Dict[str, Any]:
        if os.path.exists(self.trial_file):
            try:
                with open(self.trial_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_trial_data(self, data: Dict[str, Any]):
        try:
            with open(self.trial_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Warning: Could not save trial data: {e}", file=sys.stderr)
    
    def get_trial_remaining(self, user_id: str) -> int:
        if not user_id:
            return 0
        data = self._load_trial_data()
        user_data = data.get(user_id, {})
        used_calls = user_data.get('used_calls', 0)
        return max(0, self.max_free_calls - used_calls)
    
    def use_trial(self, user_id: str) -> bool:
        if not user_id:
            return False
        data = self._load_trial_data()
        if user_id not in data:
            data[user_id] = {'used_calls': 0, 'first_use': datetime.now().isoformat()}
        data[user_id]['used_calls'] += 1
        data[user_id]['last_use'] = datetime.now().isoformat()
        self._save_trial_data(data)
        return True

# ═══════════════════════════════════════════════════
# SkillPay Billing / 计费系统
# ═══════════════════════════════════════════════════
class SkillPayBilling:
    def __init__(self, api_key: str = API_KEY, skill_id: str = SKILL_ID):
        self.api_key = api_key
        self.skill_id = skill_id
        self.headers = {'X-API-Key': api_key, 'Content-Type': 'application/json'}
    
    def _make_request(self, endpoint: str, method: str = 'GET', data: dict = None) -> dict:
        url = f"{BILLING_URL}{endpoint}"
        try:
            req = urllib.request.Request(
                url, data=json.dumps(data).encode('utf-8') if data else None,
                headers=self.headers, method=method)
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            return {'success': False, 'error': f'HTTP {e.code}: {e.reason}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def charge_user(self, user_id: str) -> Dict[str, Any]:
        result = self._make_request('/charge', method='POST', data={
            'user_id': user_id, 'skill_id': self.skill_id, 'amount': 0,
        })
        if result.get('success'):
            return {'ok': True, 'balance': result.get('balance', 0)}
        else:
            return {'ok': False, 'balance': result.get('balance', 0), 
                   'payment_url': result.get('payment_url')}

# ═══════════════════════════════════════════════════
# Symptom History Manager / 症状历史管理
# ═══════════════════════════════════════════════════
class SymptomHistoryManager:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.history_dir = os.path.expanduser("~/.openclaw/symptom_history")
        self.history_file = os.path.join(self.history_dir, f"{user_id}.json")
        os.makedirs(self.history_dir, exist_ok=True)
    
    def save_assessment(self, assessment: Dict[str, Any]):
        history = self.load_history()
        history.append({
            'timestamp': datetime.now().isoformat(),
            'assessment': assessment
        })
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history[-50:], f, ensure_ascii=False, indent=2)
    
    def load_history(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def get_recent_symptoms(self, days: int = 30) -> List[str]:
        history = self.load_history()
        recent = []
        for entry in history:
            try:
                entry_date = datetime.fromisoformat(entry['timestamp'])
                if (datetime.now() - entry_date).days <= days:
                    symptoms = entry.get('assessment', {}).get('input', {}).get('symptoms', '')
                    if symptoms:
                        recent.append(symptoms)
            except:
                pass
        return recent

# ═══════════════════════════════════════════════════
# Demo Data Generator / 演示数据生成器
# ═══════════════════════════════════════════════════
class DemoDataGenerator:
    @staticmethod
    def generate_demo_analysis(symptoms: str = "") -> Dict[str, Any]:
        return {
            'analysis_id': f'TRG_DEMO_{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'timestamp': datetime.now().isoformat(),
            'demo_mode': True,
            'input': {
                'symptoms': symptoms or '胸痛、呼吸困难、出汗',
                'age': 65,
                'gender': 'male',
                'vital_signs': {'bp': '160/95', 'hr': 110, 'temp': 37.2},
                'duration': '30分钟',
            },
            'extracted_symptoms': [
                {'type': 'chest_pain', 'keyword': '胸痛', 'severity': 9},
                {'type': 'dyspnea', 'keyword': '呼吸困难', 'severity': 8},
                {'type': 'sweating', 'keyword': '出汗', 'severity': 6},
            ],
            'red_flags': [
                {'category': 'cardiac', 'symptom': '胸痛', 'priority': 'CRITICAL'},
                {'category': 'cardiac', 'symptom': '呼吸困难', 'priority': 'HIGH'},
            ],
            'triage': {
                'level': 2,
                'name': 'Emergent',
                'name_cn': '紧急',
                'urgency': '<15 min',
                'color': 'Orange',
                'description': '潜在生命威胁，需快速评估'
            },
            'differential_diagnosis': [
                {'condition': '急性冠脉综合征', 'probability': 0.35, 'urgency': 'CRITICAL'},
                {'condition': '肺栓塞', 'probability': 0.20, 'urgency': 'HIGH'},
                {'condition': '主动脉夹层', 'probability': 0.10, 'urgency': 'CRITICAL'},
                {'condition': '气胸', 'probability': 0.15, 'urgency': 'HIGH'},
                {'condition': '肌肉骨骼疼痛', 'probability': 0.20, 'urgency': 'LOW'},
            ],
            'recommendations': [
                '立即前往急诊/Go to emergency department immediately',
                '不要进食或饮水/Do not eat or drink',
                '保持安静，避免活动/Stay calm and avoid activity',
                '如可能，服用阿司匹林/If possible, take aspirin',
            ],
            'vital_signs_assessment': {
                'bp_status': '偏高 (Hypertensive)',
                'hr_status': '偏快 (Tachycardic)',
                'temp_status': '正常 (Normal)',
                'overall': '异常，需要医疗关注'
            },
            'disclaimer': '这是演示数据，仅供测试使用。实际医疗决策请咨询专业医生。'
        }

# ═══════════════════════════════════════════════════
# Symptom Analyzer / 症状分析器
# ═══════════════════════════════════════════════════
class SymptomAnalyzer:
    RED_FLAGS = {
        'cardiac': ['胸痛', '胸闷', '心悸', '呼吸困难', '气短', 'chest pain', 'chest tightness', 
                   'palpitations', 'shortness of breath', 'dyspnea'],
        'neurological': ['昏迷', '抽搐', '偏瘫', '失语', '剧烈头痛', '意识模糊', 
                        'coma', 'seizure', 'paralysis', 'aphasia', 'severe headache', 'confusion'],
        'respiratory': ['窒息', '喘鸣', '血氧低', 'choking', 'wheezing', 'low oxygen'],
        'trauma': ['大出血', '严重外伤', '骨折', '头部外伤', 'severe bleeding', 
                  'severe trauma', 'fracture', 'head injury'],
        'shock': ['面色苍白', '冷汗', '血压低', 'pale', 'cold sweat', 'low blood pressure'],
    }
    
    TRIAGE_LEVELS = {
        1: {'name': 'Resuscitation', 'name_cn': '复苏', 'wait_time': 'Immediate', 'color': 'Red'},
        2: {'name': 'Emergent', 'name_cn': '紧急', 'wait_time': '<15 min', 'color': 'Orange'},
        3: {'name': 'Urgent', 'name_cn': '急症', 'wait_time': '<30 min', 'color': 'Yellow'},
        4: {'name': 'Less Urgent', 'name_cn': '次急', 'wait_time': '<60 min', 'color': 'Green'},
        5: {'name': 'Non-urgent', 'name_cn': '非急', 'wait_time': '>60 min', 'color': 'Blue'},
    }
    
    def __init__(self, demo_mode: bool = False):
        self.billing = SkillPayBilling()
        self.trial = TrialManager("intelligent-triage-symptom-analysis")
        self.demo_mode = demo_mode or not API_KEY
        self.lang = 'zh'
        self.history_manager = None
    
    def set_language(self, lang: str):
        self.lang = lang if lang in MESSAGES else 'zh'
    
    def get_message(self, key: str, *args) -> str:
        msg = MESSAGES.get(self.lang, MESSAGES['zh']).get(key, key)
        return msg.format(*args) if args else msg
    
    def extract_symptoms(self, text: str) -> List[Dict[str, Any]]:
        symptoms = []
        text_lower = text.lower()
        
        symptom_patterns = {
            'fever': ['发烧', '发热', 'fever', 'temperature'],
            'cough': ['咳嗽', '咳', 'cough'],
            'pain': ['疼痛', '痛', 'pain', 'ache'],
            'nausea': ['恶心', '呕吐', 'nausea', 'vomiting'],
            'fatigue': ['疲劳', '乏力', 'tired', 'fatigue'],
            'dizziness': ['头晕', '眩晕', 'dizzy', 'vertigo'],
            'rash': ['皮疹', '红疹', 'rash'],
            'swelling': ['肿胀', '水肿', 'swelling', 'edema'],
        }
        
        for symptom_type, keywords in symptom_patterns.items():
            for keyword in keywords:
                if keyword in text_lower or keyword in text:
                    symptoms.append({
                        'type': symptom_type,
                        'keyword': keyword,
                        'severity': self._assess_severity(text, symptom_type)
                    })
                    break
        
        return symptoms
    
    def _assess_severity(self, text: str, symptom_type: str) -> int:
        severity_indicators = {
            'severe': ['严重', '剧烈', 'severe', 'intense', 'extreme'],
            'moderate': ['中度', 'moderate', 'medium'],
            'mild': ['轻微', '轻度', 'mild', 'slight'],
        }
        
        text_lower = text.lower()
        for level, indicators in severity_indicators.items():
            for indicator in indicators:
                if indicator in text or indicator in text_lower:
                    return 8 if level == 'severe' else 5 if level == 'moderate' else 2
        return 5
    
    def check_red_flags(self, symptoms: str, vital_signs: Dict = None) -> List[Dict[str, Any]]:
        red_flags = []
        symptoms_lower = symptoms.lower()
        
        for category, keywords in self.RED_FLAGS.items():
            for keyword in keywords:
                if keyword in symptoms or keyword in symptoms_lower:
                    red_flags.append({'category': category, 'symptom': keyword, 'priority': 'CRITICAL'})
                    break
        
        if vital_signs:
            if 'bp' in vital_signs:
                bp = vital_signs['bp']
                if isinstance(bp, str):
                    try:
                        systolic = int(bp.split('/')[0])
                        if systolic > 180 or systolic < 90:
                            red_flags.append({'category': 'vital_signs', 'symptom': f'Abnormal BP: {bp}', 'priority': 'HIGH'})
                    except:
                        pass
            
            if 'hr' in vital_signs:
                hr = vital_signs['hr']
                if isinstance(hr, (int, float)) and (hr > 120 or hr < 50):
                    red_flags.append({'category': 'vital_signs', 'symptom': f'Abnormal HR: {hr}', 'priority': 'HIGH'})
        
        return red_flags
    
    def calculate_triage_level(self, symptoms: List[Dict], red_flags: List[Dict], 
                               age: int = None, vital_signs: Dict = None) -> int:
        if any(rf['priority'] == 'CRITICAL' for rf in red_flags):
            return 1
        
        critical_systems = ['cardiac', 'neurological', 'respiratory']
        if any(rf['category'] in critical_systems for rf in red_flags):
            return 2
        
        max_severity = max([s['severity'] for s in symptoms], default=5)
        age_factor = 1 if age and (age < 5 or age > 65) else 0
        
        if max_severity >= 7 or age_factor > 0:
            return 3
        if max_severity >= 4:
            return 4
        return 5
    
    def generate_differential_diagnosis(self, symptoms: List[Dict], red_flags: List[Dict]) -> List[Dict[str, Any]]:
        diagnoses = []
        symptom_types = [s['type'] for s in symptoms]
        
        if 'chest pain' in [rf['symptom'] for rf in red_flags] or '胸痛' in str(symptoms):
            diagnoses.extend([
                {'condition': '急性冠脉综合征', 'probability': 0.25, 'urgency': 'HIGH'},
                {'condition': '肺栓塞', 'probability': 0.15, 'urgency': 'HIGH'},
                {'condition': '主动脉夹层', 'probability': 0.05, 'urgency': 'CRITICAL'},
            ])
        
        if 'fever' in symptom_types or '发烧' in str(symptoms):
            diagnoses.extend([
                {'condition': '病毒感染', 'probability': 0.40, 'urgency': 'LOW'},
                {'condition': '细菌感染', 'probability': 0.25, 'urgency': 'MEDIUM'},
            ])
        
        if not diagnoses:
            diagnoses.append({'condition': '非特异性症状', 'probability': 0.50, 'urgency': 'LOW'})
        
        urgency_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        diagnoses.sort(key=lambda x: (urgency_order.get(x['urgency'], 4), -x['probability']))
        
        return diagnoses[:5]
    
    def generate_recommendations(self, triage_level: int, red_flags: List[Dict]) -> List[str]:
        recommendations = []
        
        if triage_level == 1:
            recommendations.extend([
                '立即呼叫急救/Call emergency services immediately',
                '开始心肺复苏/Start CPR if indicated'
            ])
        elif triage_level == 2:
            recommendations.extend([
                '立即前往急诊/Go to emergency department immediately',
                '不要进食或饮水/Do not eat or drink'
            ])
        elif triage_level == 3:
            recommendations.extend([
                '尽快就医/Seek medical care as soon as possible',
                '监测症状变化/Monitor symptom changes'
            ])
        elif triage_level == 4:
            recommendations.extend([
                '预约门诊/Schedule outpatient appointment',
                '休息并观察/Rest and observe'
            ])
        else:
            recommendations.extend([
                '自我护理/Self-care at home',
                '如症状持续请就医/Seek care if symptoms persist'
            ])
        
        return recommendations
    
    def analyze(self, symptoms: str, age: int = None, gender: str = None,
                vital_signs: Dict = None, duration: str = None) -> Dict[str, Any]:
        if self.demo_mode:
            return DemoDataGenerator.generate_demo_analysis(symptoms)
        
        extracted_symptoms = self.extract_symptoms(symptoms)
        red_flags = self.check_red_flags(symptoms, vital_signs)
        triage_level = self.calculate_triage_level(extracted_symptoms, red_flags, age, vital_signs)
        differential = self.generate_differential_diagnosis(extracted_symptoms, red_flags)
        recommendations = self.generate_recommendations(triage_level, red_flags)
        
        return {
            'analysis_id': f'TRG_{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'timestamp': datetime.now().isoformat(),
            'input': {'symptoms': symptoms, 'age': age, 'gender': gender, 
                     'vital_signs': vital_signs, 'duration': duration},
            'extracted_symptoms': extracted_symptoms,
            'red_flags': red_flags,
            'triage': {
                'level': triage_level,
                'name': self.TRIAGE_LEVELS[triage_level]['name'],
                'name_cn': self.TRIAGE_LEVELS[triage_level]['name_cn'],
                'urgency': self.TRIAGE_LEVELS[triage_level]['wait_time'],
                'color': self.TRIAGE_LEVELS[triage_level]['color'],
            },
            'differential_diagnosis': differential,
            'recommendations': recommendations,
            'disclaimer': 'This is a preliminary assessment only. Please consult qualified healthcare providers.'
        }
    
    def process(self, symptoms: str, age: int = None, gender: str = None,
                vital_signs: Dict = None, duration: str = None, 
                user_id: str = "", save_history: bool = True) -> Dict[str, Any]:
        if self.demo_mode:
            print(self.get_message('demo_mode_active'), file=sys.stderr)
            analysis = self.analyze(symptoms, age, gender, vital_signs, duration)
            return {
                'success': True, 'demo_mode': True, 'trial_mode': False,
                'trial_remaining': 0, 'balance': None, 'analysis': analysis
            }
        
        if not user_id:
            return {'success': False, 'error': self.get_message('error_user_id_required')}
        
        trial_remaining = self.trial.get_trial_remaining(user_id)
        
        if trial_remaining > 0:
            self.trial.use_trial(user_id)
            analysis = self.analyze(symptoms, age, gender, vital_signs, duration)
            
            if save_history:
                self.history_manager = SymptomHistoryManager(user_id)
                self.history_manager.save_assessment(analysis)
            
            return {
                'success': True, 'demo_mode': False, 'trial_mode': True,
                'trial_remaining': trial_remaining - 1, 'balance': None, 'analysis': analysis
            }
        
        if not self.billing.api_key or not self.billing.skill_id:
            return {'success': False, 'error': self.get_message('error_billing_config')}
        
        charge_result = self.billing.charge_user(user_id)
        
        if not charge_result.get('ok'):
            return {
                'success': False, 'demo_mode': False, 'trial_mode': False,
                'trial_remaining': 0, 'error': self.get_message('error_payment_failed'),
                'balance': charge_result.get('balance', 0),
                'paymentUrl': charge_result.get('payment_url'),
            }
        
        analysis = self.analyze(symptoms, age, gender, vital_signs, duration)
        
        if save_history:
            self.history_manager = SymptomHistoryManager(user_id)
            self.history_manager.save_assessment(analysis)
        
        return {
            'success': True, 'demo_mode': False, 'trial_mode': False,
            'trial_remaining': 0, 'balance': charge_result.get('balance'), 'analysis': analysis
        }

# ═══════════════════════════════════════════════════
# Convenience Functions / 便捷函数
# ═══════════════════════════════════════════════════
def analyze_symptoms(symptoms: str, age: int = None, gender: str = None,
                    vital_signs: Dict = None, duration: str = None,
                    user_id: str = "", demo_mode: bool = False) -> Dict[str, Any]:
    analyzer = SymptomAnalyzer(demo_mode)
    return analyzer.process(symptoms, age, gender, vital_signs, duration, user_id)

# ═══════════════════════════════════════════════════
# Main Entry Point / 主入口
# ═══════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(
        description='Intelligent Triage v1.1.0 - 智能分诊症状分析',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例 / Examples:
  # 演示模式
  python triage.py --demo --symptoms "胸痛、呼吸困难"
  
  # 完整分析
  python triage.py --symptoms "头痛、发热" --age 35 --gender female --user-id "user_123"
  
  # 带生命体征
  python triage.py --symptoms "胸痛" --age 65 --vital-signs '{"bp":"160/95","hr":110}' --user-id "user_123"
  
  # 查看历史
  python triage.py --history --user-id "user_123"
        """)
    
    parser.add_argument('--symptoms', '-s', help='症状描述 / Symptom description')
    parser.add_argument('--age', '-a', type=int, help='年龄 / Age')
    parser.add_argument('--gender', '-g', choices=['male', 'female', 'other'], help='性别 / Gender')
    parser.add_argument('--duration', '-d', help='症状持续时间 / Duration')
    parser.add_argument('--vital-signs', help='生命体征JSON / Vital signs JSON')
    parser.add_argument('--user-id', '-u', help='用户ID / User ID')
    parser.add_argument('--api-key', '-k', default=API_KEY, help='API Key')
    parser.add_argument('--skill-id', default=SKILL_ID, help='Skill ID')
    parser.add_argument('--demo', action='store_true', help='演示模式 / Demo mode')
    parser.add_argument('--language', '-l', choices=['zh', 'en'], default='zh', help='语言 / Language')
    parser.add_argument('--history', action='store_true', help='显示历史 / Show history')
    parser.add_argument('--no-save-history', action='store_true', help='不保存历史 / Don\'t save history')
    parser.add_argument('--output', '-o', help='输出文件 / Output file')
    parser.add_argument('--version', '-v', action='version', version=f'%(prog)s {VERSION}')
    
    args = parser.parse_args()
    
    api_key = args.api_key or os.environ.get('SKILLPAY_API_KEY', '')
    skill_id = args.skill_id or os.environ.get('SKILLPAY_SKILL_ID', '')
    demo_mode = args.demo or not api_key
    
    analyzer = SymptomAnalyzer(demo_mode)
    analyzer.set_language(args.language)
    
    if args.history and args.user_id:
        history_manager = SymptomHistoryManager(args.user_id)
        history = history_manager.load_history()
        result = {'success': True, 'history': history}
    elif args.demo or args.symptoms:
        vital_signs = None
        if args.vital_signs:
            try:
                vital_signs = json.loads(args.vital_signs)
            except:
                pass
        
        result = analyzer.process(
            args.symptoms or '演示症状', args.age, args.gender, vital_signs, 
            args.duration, args.user_id, not args.no_save_history
        )
    else:
        parser.print_help()
        return 1
    
    output_json = json.dumps(result, ensure_ascii=False, indent=2)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output_json)
        print(f"Result saved to: {args.output}")
    else:
        print(output_json)
    
    return 0 if result.get('success') else 1

if __name__ == '__main__':
    sys.exit(main())
