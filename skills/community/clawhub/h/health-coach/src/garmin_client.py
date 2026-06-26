"""
Garmin数据获取客户端
支持获取睡眠、步数、HRV、身体电量、压力、运动强度等数据
"""

import garth
from datetime import date, timedelta
from typing import Any, Dict, Optional
import sys


class GarminClient:
    """Garmin数据客户端"""
    
    def __init__(self, config: Dict):
        """
        初始化Garmin客户端
        
        Args:
            config: 设备配置字典，包含domain等
        """
        self.domain = config.get('domain', 'garmin.cn')
        self.configured = False
        
    def connect(self) -> bool:
        """连接Garmin API"""
        try:
            garth.configure(domain=self.domain)
            garth.resume("~/.garth")
            self.configured = True
            print("✅ Garmin连接成功")
            return True
        except Exception as e:
            print(f"❌ Garmin连接失败: {e}")
            return False
    
    def get_sleep_data(self, date_str: str) -> Optional[Dict]:
        """获取睡眠数据"""
        try:
            sleep = garth.SleepData.get(date_str)
            if sleep is None:
                return None
            
            dto = sleep.daily_sleep_dto
            if dto is None:
                return None
            
            total_hours = dto.sleep_time_seconds / 3600
            deep_hours = dto.deep_sleep_seconds / 3600
            light_hours = dto.light_sleep_seconds / 3600
            rem_hours = dto.rem_sleep_seconds / 3600
            
            feedback_value = getattr(dto, 'sleep_score_feedback', None)
            
            return {
                "total_hours": round(total_hours, 2),
                "deep_hours": round(deep_hours, 2),
                "deep_percent": round(deep_hours/total_hours*100, 1) if total_hours > 0 else 0,
                "light_hours": round(light_hours, 2),
                "rem_hours": round(rem_hours, 2),
                "score": dto.sleep_scores.overall.value,
                "feedback": str(feedback_value) if feedback_value else "N/A"
            }
        except Exception as e:
            print(f"❌ 获取睡眠数据失败: {e}")
            return None
    
    def get_steps_data(self, date_str: str) -> Optional[Dict]:
        """获取步数数据"""
        try:
            steps = garth.DailySteps.list(date_str, 1)
            if not steps or len(steps) == 0:
                return None
            
            s = steps[0]
            return {
                "total_steps": s.total_steps,
                "distance_km": round(s.total_distance/1000, 2),
                "goal": s.step_goal,
                "completion_percent": round(s.total_steps/s.step_goal*100, 1) if s.step_goal > 0 else 0
            }
        except Exception as e:
            print(f"❌ 获取步数数据失败: {e}")
            return None
    
    def get_hrv_data(self, date_str: str) -> Optional[Dict]:
        """获取HRV数据"""
        try:
            hrv = garth.DailyHRV.list(date_str, 1)
            if not hrv or len(hrv) == 0:
                return None
            
            h = hrv[0]
            return {
                "last_night_avg": h.last_night_avg,
                "weekly_avg": h.weekly_avg,
                "status": h.status
            }
        except Exception as e:
            print(f"❌ 获取HRV数据失败: {e}")
            return None
    
    def get_body_battery_stress(self, date_str: str) -> Optional[Dict]:
        """获取身体电量和压力数据"""
        try:
            bb = garth.DailyBodyBatteryStress.list(date_str, 1)
            if not bb or len(bb) == 0:
                return None
            
            b = bb[0]
            return {
                "current": b.current_body_battery,
                "max": b.max_body_battery,
                "change": b.body_battery_change,
                "avg_stress": b.avg_stress_level,
                "max_stress": b.max_stress_level
            }
        except Exception as e:
            print(f"❌ 获取身体电量数据失败: {e}")
            return None
    
    def get_stress_details(self, date_str: str) -> Optional[Dict]:
        """获取压力详情数据"""
        try:
            stress = garth.DailyStress.list(date_str, 1)
            if not stress or len(stress) == 0:
                return None
            
            s = stress[0]
            return {
                "overall": s.overall_stress_level,
                "low_duration": s.low_stress_duration,
                "medium_duration": s.medium_stress_duration,
                "high_duration": s.high_stress_duration or 0,
                "rest_duration": s.rest_stress_duration
            }
        except Exception as e:
            print(f"❌ 获取压力详情失败: {e}")
            return None
    
    def get_intensity_minutes(self, date_str: str) -> Optional[Dict]:
        """获取运动强度数据"""
        try:
            intensity = garth.DailyIntensityMinutes.list(date_str, 1)
            if not intensity or len(intensity) == 0:
                return None
            
            i = intensity[0]
            return {
                "moderate": i.moderate_value,
                "vigorous": i.vigorous_value,
                "weekly_goal": i.weekly_goal
            }
        except Exception as e:
            print(f"❌ 获取运动强度数据失败: {e}")
            return None
    
    def get_daily_data(self, activity_date: str, sleep_end_date: str) -> Dict:
        """
        获取一日健康数据
        
        Args:
            activity_date: 活动日期（YYYY-MM-DD），用于步数、运动强度
            sleep_end_date: 睡眠结束日期（YYYY-MM-DD），用于睡眠、HRV、压力
            
        Returns:
            包含所有健康数据的字典
        """
        print(f"\n📊 获取健康数据 | 活动: {activity_date} | 睡眠结束: {sleep_end_date}")
        
        if not self.configured:
            if not self.connect():
                return {}
        
        health_data: Dict[str, Any] = {
            "date": activity_date,
            "sleep": None,
            "steps": None,
            "hrv": None,
            "body_battery": None,
            "stress": None,
            "intensity": None
        }
        
        # 睡眠数据
        print("\n💤 睡眠数据:")
        sleep_data = self.get_sleep_data(sleep_end_date)
        health_data["sleep"] = sleep_data
        if sleep_data:
            print(f"   总时长: {sleep_data.get('total_hours')}小时, 评分: {sleep_data.get('score')}")
        
        # 步数数据
        print("\n👟 步数数据:")
        steps_data = self.get_steps_data(activity_date)
        health_data["steps"] = steps_data
        if steps_data:
            print(f"   总步数: {steps_data.get('total_steps')}, 完成: {steps_data.get('completion_percent')}%")
        
        # HRV数据
        print("\n❤️ HRV数据:")
        hrv_data = self.get_hrv_data(sleep_end_date)
        health_data["hrv"] = hrv_data
        if hrv_data:
            print(f"   昨晚HRV: {hrv_data.get('last_night_avg')}, 状态: {hrv_data.get('status')}")
        
        # 身体电量
        print("\n🔋 身体电量:")
        bb_data = self.get_body_battery_stress(sleep_end_date)
        health_data["body_battery"] = bb_data
        if bb_data:
            print(f"   当前电量: {bb_data.get('current')}")
        
        # 压力详情
        print("\n😓 压力详情:")
        stress_data = self.get_stress_details(sleep_end_date)
        health_data["stress"] = stress_data
        if stress_data:
            print(f"   整体压力: {stress_data.get('overall')}")
        
        # 运动强度
        print("\n🏃 运动强度:")
        intensity_data = self.get_intensity_minutes(activity_date)
        health_data["intensity"] = intensity_data
        if intensity_data:
            print(f"   中等强度: {intensity_data.get('moderate')}分钟, 高强度: {intensity_data.get('vigorous')}分钟")
        
        return health_data
