"""
报告生成模块
负责组装 Prompt 并调用 NotebookLM 生成健康建议
"""

import subprocess
import json
from typing import Dict, List, Optional
from datetime import datetime
from src.prompts.base import format_base_prompt, PRIVACY_RULES
from src.config import UserConfig

class ReportGenerator:
    """健康报告生成器"""
    
    def __init__(self, user_config: UserConfig):
        self.user_config = user_config

    def _format_concerns(self) -> str:
        """格式化健康关切"""
        concerns = self.user_config.health_concerns
        conditions = [c['condition'] for c in self.user_config.specific_conditions]
        all_concerns = list(set(concerns + conditions))
        return "\n".join([f"- {c}" for c in all_concerns])

    def _format_history(self, history: List[Dict]) -> str:
        """格式化历史数据（简略版）"""
        if not history:
            return "No historical data available yet."
        
        lines = []
        for record in history[-7:]:  # 最近7天
            date = record.get('date', 'Unknown')
            sleep_score = record.get('sleep', {}).get('score', 'N/A')
            steps = record.get('steps', {}).get('total_steps', 'N/A')
            lines.append(f"- {date}: Sleep Score {sleep_score}, Steps {steps}")
        return "\n".join(lines)

    def generate_prompt(self, daily_data: Dict, history: List[Dict]) -> str:
        """生成完整的 AI Prompt"""
        
        # 提取各项数据，处理缺失值
        sleep = daily_data.get('sleep') or {}
        steps = daily_data.get('steps') or {}
        hrv = daily_data.get('hrv') or {}
        bb = daily_data.get('body_battery') or {}
        stress = daily_data.get('stress') or {}
        intensity = daily_data.get('intensity') or {}

        # 这里的模块化逻辑可以根据 PRD 进一步扩展，目前先用基础模板
        analysis_modules = """
### 1. Data Insights
Analyze the correlations between sleep, HRV, and stress. Highlight any metrics that are exceptionally good or visibly off.

### 2. Targeted Daily Actions
Based on the user's health concerns (e.g., sleep, stress, uric acid), provide 3-4 highly specific and actionable recommendations for today.

### 3. Wellness Tip of the Day
Share one bite-sized piece of knowledge based on functional medicine principles.
"""

        prompt = format_base_prompt(
            USER_CONCERNS=self._format_concerns(),
            HISTORY_DATA=self._format_history(history),
            DATE=daily_data.get('date', datetime.now().strftime('%Y-%m-%d')),
            SLEEP_TOTAL_HOURS=sleep.get('total_hours', 'N/A'),
            SLEEP_DEEP_HOURS=sleep.get('deep_hours', 'N/A'),
            SLEEP_DEEP_PERCENT=sleep.get('deep_percent', 'N/A'),
            SLEEP_LIGHT_HOURS=sleep.get('light_hours', 'N/A'),
            SLEEP_REM_HOURS=sleep.get('rem_hours', 'N/A'),
            SLEEP_SCORE=sleep.get('score', 'N/A'),
            STEPS_TOTAL=steps.get('total_steps', 'N/A'),
            STEPS_DISTANCE=steps.get('distance_km', 'N/A'),
            STEPS_COMPLETION=steps.get('completion_percent', 'N/A'),
            HRV_LAST_NIGHT=hrv.get('last_night_avg', 'N/A'),
            HRV_WEEKLY=hrv.get('weekly_avg', 'N/A'),
            HRV_STATUS=hrv.get('status', 'N/A'),
            BODY_BATTERY_CURRENT=bb.get('current', 'N/A'),
            BODY_BATTERY_MAX=bb.get('max', 'N/A'),
            STRESS_OVERALL=stress.get('overall', 'N/A'),
            STRESS_LOW=stress.get('low_duration', 'N/A'),
            STRESS_MEDIUM=stress.get('medium_duration', 'N/A'),
            STRESS_HIGH=stress.get('high_duration', 'N/A'),
            STRESS_REST=stress.get('rest_duration', 'N/A'),
            INTENSITY_MODERATE=intensity.get('moderate', 'N/A'),
            INTENSITY_VIGOROUS=intensity.get('vigorous', 'N/A'),
            INTENSITY_GOAL=intensity.get('weekly_goal', 'N/A'),
            ANALYSIS_MODULES=analysis_modules
        )
        
        return prompt

    def call_notebooklm(self, prompt: str) -> Optional[str]:
        """调用 NotebookLM CLI 获取建议"""
        import tempfile
        import os
        try:
            # 安全改进：禁止将 prompt 直接作为命令行参数传递以防进程列表数据泄漏
            # 建立一个受保护的临时文件并存储敏感的健康数据文本，通过 stdin 管道喂给 notebooklm
            with tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8') as temp_file:
                # 严控临时文件权限，仅生成者可读写
                os.chmod(temp_file.name, 0o600)
                temp_file.write(prompt)
                temp_file.close()

                try:
                    with open(temp_file.name, 'r', encoding='utf-8') as f:
                        # CLI 执行 (兼容其参数方式或通过管道获取)：如果是支持 stdin 则可获取，如果是必须带参可通过读取解决
                        # 根据安全意见，更推荐使用管道
                        process = subprocess.Popen(
                            ['notebooklm', 'ask'],
                            stdin=f,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True
                        )
                        stdout, stderr = process.communicate(timeout=60)
                finally:
                    # 获取结束后始终清理受保护的临时文件
                    if os.path.exists(temp_file.name):
                        os.unlink(temp_file.name)
            
            if process.returncode == 0:
                return stdout.strip()
            else:
                print(f"❌ NotebookLM 调用失败 (错误或不兼容 stdin，需评估): {stderr}")
                return None
        except Exception as e:
            print(f"❌ 调用 NotebookLM 异常: {e}")
            return None

    def format_final_report(self, daily_data: Dict, ai_suggestion: str) -> str:
        """格式化最终发送的消息报告"""
        date_str = daily_data.get('date', datetime.now().strftime('%Y-%m-%d'))
        sleep = daily_data.get('sleep') or {}
        steps = daily_data.get('steps') or {}
        hrv = daily_data.get('hrv') or {}
        bb = daily_data.get('body_battery') or {}
        
        report = f"""📊 Daily Health Report | {date_str}

💤 Sleep
• Total: {sleep.get('total_hours', 'N/A')} hrs
• Deep Sleep: {sleep.get('deep_hours', 'N/A')} hrs ({sleep.get('deep_percent', 0)}%)
• Score: {sleep.get('score', 'N/A')}/100

👟 Activity
• Total Steps: {steps.get('total_steps', 'N/A')} steps
• Goal Completion: {steps.get('completion_percent', 'N/A')}%

❤️ Body Status
• Last Night HRV: {hrv.get('last_night_avg', 'N/A')}
• Status: {hrv.get('status', 'N/A')}

🔋 Body Battery
• Current: {bb.get('current', 'N/A')}

💡 Today's Recommendations
{ai_suggestion}

---
Generated by 🦞 Health Assistant
"""
        return report
