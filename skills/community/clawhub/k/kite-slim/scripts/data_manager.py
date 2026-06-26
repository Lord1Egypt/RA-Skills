#!/usr/bin/env python3
"""
AI陪伴减肥 - 数据持久化管理模块
功能: 用户档案存储、每日记录、设置管理
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path


# ==================== 数据来源标注常量 ====================
class DataSource:
    """数据来源标识"""
    REAL_RECORD = "【真实记录】"      # 来自 data/user_records.json
    EXAMPLE = "【示例】"             # 对话中的假设场景，非真实
    ESTIMATED = "【估算】"           # AI根据常识的推算
    USER_INPUT = "【用户输入】"       # 用户明确告知的数据


def mark_data_source(data_type: str, data: Any, source: str) -> Dict:
    """
    标记数据来源
    用于确保所有展示的数据都有明确的来源标识
    """
    return {
        "value": data,
        "source": source,
        "timestamp": datetime.now().isoformat(),
        "type": data_type
    }


class DataManager:
    """数据持久化管理器"""
    
    def __init__(self, base_dir: str = "./data"):
        self.base_dir = Path(base_dir)
        self.profile_file = self.base_dir / "user_profile.json"
        self.records_dir = self.base_dir / "daily_records"
        self._ensure_dirs()
    
    def _ensure_dirs(self):
        """确保目录存在"""
        self.base_dir.mkdir(exist_ok=True)
        self.records_dir.mkdir(exist_ok=True)
    
    # ==================== 用户档案 ====================
    
    def get_profile(self) -> Optional[Dict]:
        """获取用户档案"""
        if self.profile_file.exists():
            with open(self.profile_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def save_profile(self, profile: Dict) -> bool:
        """保存用户档案"""
        try:
            with open(self.profile_file, 'w', encoding='utf-8') as f:
                json.dump(profile, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存档案失败: {e}")
            return False
    
    def update_profile(self, updates: Dict) -> bool:
        """更新用户档案部分字段"""
        profile = self.get_profile() or {}
        profile.update(updates)
        profile['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M")
        return self.save_profile(profile)
    
    # ==================== 每日记录 ====================
    
    def _get_record_path(self, date: str) -> Path:
        """获取指定日期的记录文件路径"""
        return self.records_dir / f"{date}.json"
    
    def save_daily_record(self, date: str, record: Dict) -> bool:
        """保存每日记录"""
        try:
            record_path = self._get_record_path(date)
            with open(record_path, 'w', encoding='utf-8') as f:
                json.dump(record, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存记录失败: {e}")
            return False
    
    def save_user_record(self, record: Dict) -> bool:
        """保存用户记录（自动使用当天日期）
        
        兼容接口，支持两种调用方式:
        1. save_user_record({'date': '2024-01-01', ...})
        2. save_daily_record('2024-01-01', {...})
        """
        # 优先使用record中的date字段，否则使用今天
        date = record.get('date', datetime.now().strftime('%Y-%m-%d'))
        return self.save_daily_record(date, record)
    
    def get_daily_record(self, date: str) -> Optional[Dict]:
        """获取指定日期的记录"""
        record_path = self._get_record_path(date)
        if record_path.exists():
            with open(record_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def get_records_range(self, start_date: str, end_date: str) -> List[Dict]:
        """获取日期范围内的所有记录"""
        records = []
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        current = start
        while current <= end:
            date_str = current.strftime("%Y-%m-%d")
            record = self.get_daily_record(date_str)
            if record:
                records.append(record)
            current += timedelta(days=1)
        
        return records
    
    def get_recent_records(self, days: int = 7) -> List[Dict]:
        """获取最近N天的记录"""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days-1)).strftime("%Y-%m-%d")
        return self.get_records_range(start_date, end_date)
    
    # ==================== 连续达标计算 ====================
    
    def calculate_streak(self) -> int:
        """计算连续达标天数"""
        streak = 0
        current_date = datetime.now()
        
        while True:
            date_str = current_date.strftime("%Y-%m-%d")
            record = self.get_daily_record(date_str)
            
            if record and record.get('target_achieved', False):
                streak += 1
                current_date -= timedelta(days=1)
            else:
                break
        
        return streak
    
    # ==================== 历史分析 ====================
    
    def get_weight_trend(self, days: int = 30) -> Dict:
        """获取体重趋势"""
        records = self.get_recent_records(days)
        
        weights = []
        dates = []
        for record in records:
            if record.get('weight_morning'):
                weights.append(record['weight_morning'])
                dates.append(record.get('date', ''))
        
        if not weights:
            return {'trend': 'neutral', 'change': 0, 'data': []}
        
        change = weights[-1] - weights[0] if len(weights) > 1 else 0
        
        if change < -0.5:
            trend = 'down'
        elif change > 0.5:
            trend = 'up'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'change': round(change, 1),
            'start': weights[0],
            'end': weights[-1],
            'avg': round(sum(weights) / len(weights), 1),
            'data': [{'date': d, 'weight': w} for d, w in zip(dates, weights)]
        }
    
    def get_calorie_trend(self, days: int = 7) -> Dict:
        """获取热量趋势"""
        records = self.get_recent_records(days)
        
        calories = []
        dates = []
        for record in records:
            calories.append(record.get('total_calories', 0))
            dates.append(record.get('date', ''))
        
        return {
            'avg': round(sum(calories) / len(calories)) if calories else 0,
            'total': sum(calories),
            'data': [{'date': d, 'calories': c} for d, c in zip(dates, calories)]
        }
    
    def get_weekly_report(self) -> Dict:
        """生成周报"""
        records = self.get_recent_records(7)
        
        if not records:
            return {'available': False}
        
        # 基本统计
        total_days = len(records)
        achieved_days = sum(1 for r in records if r.get('target_achieved', False))
        avg_steps = sum(r.get('actual_steps', 0) for r in records) / total_days
        avg_score = sum(r.get('score', 0) for r in records) / total_days
        
        # 体重变化
        weights = [r.get('weight_morning') for r in records if r.get('weight_morning')]
        weight_change = weights[-1] - weights[0] if len(weights) > 1 else 0
        
        # 热量平衡
        total_cal = sum(r.get('total_calories', 0) for r in records)
        avg_bmr = 1400  # 需要从profile获取
        expected_cal = avg_bmr * total_days
        calorie_balance = total_cal - expected_cal
        
        # 最佳/最差日
        scored_records = [(r.get('score', 0), r.get('date', '')) for r in records]
        scored_records.sort(reverse=True)
        best_day = scored_records[0][1] if scored_records else ''
        worst_day = scored_records[-1][1] if scored_records else ''
        
        return {
            'available': True,
            'period': f"{(datetime.now() - timedelta(days=6)).strftime('%m.%d')}-{(datetime.now()).strftime('%m.%d')}",
            'stats': {
                'days': total_days,
                'achieved': achieved_days,
                'achieved_rate': f"{achieved_days}/{total_days}",
                'avg_steps': int(avg_steps),
                'avg_score': round(avg_score, 1),
                'weight_change': round(weight_change, 1),
                'calorie_balance': int(calorie_balance)
            },
            'best_day': best_day,
            'worst_day': worst_day,
            'records': records
        }
    
    def get_monthly_report(self) -> Dict:
        """生成月报"""
        records = self.get_recent_records(30)
        
        if not records:
            return {'available': False}
        
        # 计算月度统计
        total_days = len(records)
        achieved_days = sum(1 for r in records if r.get('target_achieved', False))
        
        # 体重统计
        weights = [r.get('weight_morning') for r in records if r.get('weight_morning')]
        weight_change = weights[-1] - weights[0] if len(weights) > 1 else 0
        
        # 计算连续达标
        streak = self.calculate_streak()
        
        # 月度里程碑
        milestones = []
        if achieved_days >= 20:
            milestones.append("🏅 月度达标达人")
        if weight_change < -2:
            milestones.append("💪 月度减重明星")
        if streak >= 7:
            milestones.append(f"🔥 连续达标{streak}天")
        
        return {
            'available': True,
            'period': datetime.now().strftime('%Y年%m月'),
            'stats': {
                'days': total_days,
                'achieved': achieved_days,
                'achieved_rate': f"{achieved_days}/{total_days}",
                'weight_change': round(weight_change, 1),
                'start_weight': weights[0] if weights else 0,
                'end_weight': weights[-1] if weights else 0,
                'current_streak': streak
            },
            'milestones': milestones,
            'records': records
        }
    
    # ==================== 设置管理 ====================
    
    def get_settings(self) -> Dict:
        """获取用户设置"""
        profile = self.get_profile()
        if profile and 'settings' in profile:
            return profile['settings']
        return self._default_settings()
    
    def update_settings(self, settings: Dict) -> bool:
        """更新用户设置"""
        return self.update_profile({'settings': settings})
    
    def _default_settings(self) -> Dict:
        """默认设置"""
        return {
            'reminder_enabled': True,
            'reminder_morning': '07:00',
            'reminder_lunch': '12:00',
            'reminder_evening': '20:00',
            'reminder_style': 'normal',  # normal, simple, encouraging
            'weight_unit': 'kg',
            'active_goals': True
        }
    
    # ==================== 断点续传 ====================
    
    def save_conversation_state(self, state: Dict) -> bool:
        """
        保存对话状态，用于断点续传
        
        Args:
            state: 对话状态字典，包含：
                - current_phase: 当前阶段(weight_reminder/breakfast/lunch/dinner/summary)
                - pending_data: 待确认数据
                - missing_fields: 缺失字段列表
                - context: 上下文信息
                - last_update: 最后更新时间
        """
        state['last_update'] = datetime.now().isoformat()
        state_file = self.base_dir / "conversation_state.json"
        try:
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存对话状态失败: {e}")
            return False
    
    def get_conversation_state(self) -> Optional[Dict]:
        """获取对话状态"""
        state_file = self.base_dir / "conversation_state.json"
        if state_file.exists():
            try:
                with open(state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return None
        return None
    
    def clear_conversation_state(self) -> bool:
        """清除对话状态"""
        state_file = self.base_dir / "conversation_state.json"
        try:
            if state_file.exists():
                state_file.unlink()
            return True
        except:
            return False
    
    def is_state_expired(self, state: Dict, max_hours: int = 24) -> bool:
        """检查对话状态是否过期"""
        if not state or 'last_update' not in state:
            return True
        last_update = datetime.fromisoformat(state['last_update'])
        return (datetime.now() - last_update).total_seconds() > max_hours * 3600
    
    def get_resume_prompt(self, state: Dict) -> str:
        """生成断点续传提示"""
        phase = state.get('current_phase', 'unknown')
        pending = state.get('pending_data', {})
        missing = state.get('missing_fields', [])
        
        prompts = {
            'weight_reminder': "📝 上次提醒你称体重，还没收到数据哦~",
            'breakfast': "🍳 早餐还没打卡呢，今天吃了什么呀？",
            'lunch': "🌞 午餐打卡还没收到，中午吃了啥？",
            'dinner': "🌙 晚餐还没记录，今晚吃了什么？",
            'steps_check': "🚶 步数目标完成了吗？告诉我走了多少步~",
            'summary': "📊 今天的总结还差一些数据..."
        }
        
        base = prompts.get(phase, "我们继续之前的话题~")
        
        if missing:
            base += f"\n还需要：{', '.join(missing)}"
        
        return base
    
    # ==================== 体重趋势预测 ====================
    
    def predict_weight_trend(self, weeks: int = 4) -> Dict:
        """
        预测体重趋势
        
        Args:
            weeks: 预测周数，默认4周
            
        Returns:
            预测结果，包含：
            - has_enough_data: 是否有足够数据
            - weekly_prediction: 每周预测体重
            - estimated_goal_date: 预计达到目标体重的日期
            - confidence: 预测置信度
            - advice: 建议
        """
        records = self.get_recent_records(30)  # 获取30天数据
        
        if len(records) < 7:
            return {
                'has_enough_data': False,
                'message': '数据不足7天，无法进行趋势预测，请继续记录~'
            }
        
        profile = self.get_profile()
        goal_weight = profile.get('goal_weight', profile.get('weight', 60) - 5) if profile else 60
        current_weight = profile.get('weight', 60) if profile else 60
        
        # 提取体重数据
        weights = []
        for r in records:
            if r.get('weight_morning'):
                weights.append({
                    'date': r.get('date'),
                    'weight': r['weight_morning']
                })
        
        if len(weights) < 7:
            return {
                'has_enough_data': False,
                'message': '体重记录不足，无法预测趋势~'
            }
        
        # 简单线性回归计算趋势
        n = len(weights)
        x_vals = list(range(n))
        y_vals = [w['weight'] for w in weights]
        
        x_mean = sum(x_vals) / n
        y_mean = sum(y_vals) / n
        
        # 计算斜率
        numerator = sum((x_vals[i] - x_mean) * (y_vals[i] - y_mean) for i in range(n))
        denominator = sum((x_vals[i] - x_mean) ** 2 for i in range(n))
        
        slope = numerator / denominator if denominator != 0 else 0
        
        # 预测未来体重
        weekly_predictions = []
        last_weight = y_vals[-1]
        last_date = datetime.strptime(weights[-1]['date'], "%Y-%m-%d")
        
        for week in range(1, weeks + 1):
            future_weight = last_weight + slope * 7 * week
            future_date = last_date + timedelta(weeks=week)
            weekly_predictions.append({
                'week': f"第{week}周",
                'date': future_date.strftime("%m.%d"),
                'weight': round(future_weight, 1)
            })
        
        # 计算预计达成目标日期
        weight_to_lose = current_weight - goal_weight
        if slope < 0:
            days_to_goal = weight_to_lose / abs(slope) if abs(slope) > 0.001 else 365
            goal_date = last_date + timedelta(days=int(days_to_goal))
            estimated_goal_date = goal_date.strftime("%Y年%m月%d日")
        else:
            estimated_goal_date = None
        
        # 置信度评估
        if len(weights) >= 21:
            confidence = 'high'
        elif len(weights) >= 14:
            confidence = 'medium'
        else:
            confidence = 'low'
        
        # 生成建议
        if slope < -0.3:
            advice = "📈 减重趋势良好！继续保持当前节奏，胜利在望~"
        elif slope < 0:
            advice = "📉 体重在慢慢下降，但速度较慢。建议适当增加运动或稍微控制饮食~"
        elif slope == 0:
            advice = "⚖️ 体重目前处于平台期。可以尝试变换运动方式或调整饮食结构打破僵局~"
        else:
            advice = "📊 体重有上升趋势。建议回顾近期饮食和运动情况，适当调整~"
        
        return {
            'has_enough_data': True,
            'current_weight': last_weight,
            'goal_weight': goal_weight,
            'weekly_prediction': weekly_predictions,
            'estimated_goal_date': estimated_goal_date,
            'confidence': confidence,
            'advice': advice,
            'trend': 'down' if slope < 0 else ('stable' if slope == 0 else 'up'),
            'weekly_change': round(slope * 7, 2)
        }
    
    def get_weight_prediction_card(self) -> str:
        """生成体重预测卡片"""
        prediction = self.predict_weight_trend()
        
        if not prediction.get('has_enough_data', False):
            return f"🤔 {prediction.get('message', '数据不足')}"
        
        card = f"""
📊 体重趋势预测

━━━━━━━━━━━━━━━
📍 当前体重：{prediction['current_weight']}kg
🎯 目标体重：{prediction['goal_weight']}kg
📉 每周变化：{prediction['weekly_change']}kg
━━━━━━━━━━━━━━━

📅 未来预测：
"""
        
        for p in prediction['weekly_prediction']:
            card += f"  {p['week']}({p['date']})：{p['weight']}kg\n"
        
        if prediction['estimated_goal_date']:
            card += f"""
━━━━━━━━━━━━━━━
🎯 预计达成目标：{prediction['estimated_goal_date']}
━━━━━━━━━━━━━━━
"""
        
        card += f"{prediction['advice']}"
        
        return card


def main():
    """命令行测试/交互入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI陪伴减肥 - 数据管理')
    parser.add_argument('--action', default='test', 
                        choices=['init', 'record', 'weekly_report', 'monthly_report', 
                                'save_state', 'get_state', 'clear_state', 'resume_prompt',
                                'predict_trend', 'test'],
                        help='操作类型')
    parser.add_argument('--user_id', default='default_user', help='用户ID')
    parser.add_argument('--phase', help='对话阶段(用于save_state)')
    parser.add_argument('--missing', help='缺失字段(用于save_state)')
    parser.add_argument('--weeks', type=int, default=4, help='预测周数')
    parser.add_argument('--date', help='日期')
    parser.add_argument('--weight', type=float, help='体重')
    parser.add_argument('--steps', type=int, help='步数')
    
    args = parser.parse_args()
    dm = DataManager()
    
    if args.action == 'init':
        # 初始化用户档案
        print("初始化用户档案...")
        profile = {
            'user_id': args.user_id,
            'height': 165,
            'weight': args.weight or 60,
            'age': 25,
            'gender': 'female',
            'activity': 'sedentary',
            'goal_weight': (args.weight or 60) - 5,
            'created_at': datetime.now().strftime("%Y-%m-%d"),
            'settings': dm._default_settings()
        }
        dm.save_profile(profile)
        print("✅ 用户档案已初始化")
        
    elif args.action == 'save_state':
        # 保存对话状态
        state = {
            'current_phase': args.phase or 'unknown',
            'pending_data': {},
            'missing_fields': args.missing.split(',') if args.missing else []
        }
        dm.save_conversation_state(state)
        print(f"✅ 对话状态已保存: {args.phase}")
        
    elif args.action == 'get_state':
        # 获取对话状态
        state = dm.get_conversation_state()
        if state:
            print(f"当前状态: {json.dumps(state, ensure_ascii=False, indent=2)}")
        else:
            print("无对话状态记录")
            
    elif args.action == 'clear_state':
        # 清除对话状态
        dm.clear_conversation_state()
        print("✅ 对话状态已清除")
        
    elif args.action == 'resume_prompt':
        # 获取续传提示
        state = dm.get_conversation_state()
        if state:
            print(dm.get_resume_prompt(state))
        else:
            print("无对话状态记录")
            
    elif args.action == 'predict_trend':
        # 体重趋势预测
        print(dm.get_weight_prediction_card())
        
    elif args.action == 'weekly_report':
        # 周报
        report = dm.get_weekly_report()
        if report['available']:
            print(f"📊 周报 ({report['period']})")
            print(f"达标天数: {report['stats']['achieved_rate']}")
            print(f"体重变化: {report['stats']['weight_change']}kg")
        else:
            print("数据不足，无法生成周报")
            
    else:
        # 默认测试流程
        print("🧪 运行测试流程...\n")
        
        # 保存用户档案
        profile = {
            'user_id': args.user_id,
            'height': 165,
            'weight': 60,
            'age': 25,
            'gender': 'female',
            'activity': 'sedentary',
            'goal_weight': 55,
            'created_at': datetime.now().strftime("%Y-%m-%d"),
            'settings': dm._default_settings()
        }
        dm.save_profile(profile)
        print("✅ 用户档案已保存")
        
        # 保存每日记录
        today = datetime.now().strftime("%Y-%m-%d")
        record = {
            'date': today,
            'weight_morning': 58.5,
            'meals': {
                'breakfast': {'foods': '粥+包子', 'calories': 350},
                'lunch': {'foods': '米饭+鱼', 'calories': 550},
                'dinner': {'foods': '面条', 'calories': 400}
            },
            'total_calories': 1300,
            'target_steps': 8000,
            'actual_steps': 7500,
            'target_achieved': False,
            'score': 7.5,
            'streak_days': 5
        }
        dm.save_daily_record(today, record)
        print("✅ 每日记录已保存")
        
        # 测试体重预测
        print("\n📈 体重趋势预测:")
        print(dm.get_weight_prediction_card())
        
        # 测试断点续传
        print("\n💾 断点续传测试:")
        dm.save_conversation_state({
            'current_phase': 'breakfast',
            'pending_data': {'time': '08:30'},
            'missing_fields': ['breakfast_foods']
        })
        state = dm.get_conversation_state()
        print(f"已保存状态: {state['current_phase']}")
        print(f"续传提示: {dm.get_resume_prompt(state)}")
        dm.clear_conversation_state()
        print("状态已清除")


if __name__ == '__main__':
    main()
