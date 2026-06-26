# 智能手表集成设计 - 生理指标监测与主动关怀

## 概述

通过集成智能手表/健康设备，Hikaru可以监测用户的生理指标，在发现异常时主动发起关怀对话。这是《Her》精神的延伸 - Samantha能"感受"Theodore的状态。

---

## 技术架构

### 方案1: OpenClaw Plugin（推荐）

```
智能手表/健康App
    ↓ (API)
Health Monitor Plugin (Python)
    ↓ (检测异常)
OpenClaw Skill System
    ↓ (触发对话)
Hikaru Skill
```

**优势：**
- 利用OpenClaw现有的plugin架构
- 与Hikaru skill解耦
- 可以服务于多个skills

**实现位置：**
```
~/.openclaw/plugins/health_monitor/
├── plugin.yaml
├── monitor.py
├── health_sources/
│   ├── apple_health.py
│   ├── google_fit.py
│   ├── xiaomi_health.py
│   └── manual_input.py
└── config.yaml
```

---

### 方案2: Hikaru内置（简单但耦合）

```
Hikaru Skill
├── scripts/
│   ├── health_monitor.py  # 新增
│   └── ...
└── config/
    └── health_thresholds.yaml
```

**优势：**
- 实现简单
- 直接集成

**劣势：**
- 与Hikaru耦合
- 难以复用

---

## 监测指标与触发条件

### 1. 心率异常

**正常范围：** 60-100 bpm（静息）

**触发条件：**
```yaml
heart_rate:
  resting:
    low_threshold: 50  # 低于50触发
    high_threshold: 110  # 高于110触发
  active:
    high_threshold: 180  # 运动时过高

  trigger_message:
    high: "Your heart rate seems high. Everything okay?"
    low: "I noticed your heart rate is lower than usual. How are you feeling?"
```

### 2. 睡眠质量

**监测维度：**
- 睡眠时长
- 深度睡眠比例
- 入睡时间
- 醒来次数

**触发条件：**
```yaml
sleep:
  duration:
    min_hours: 6
    max_hours: 10

  deep_sleep_ratio:
    min_percentage: 15  # 深度睡眠低于15%

  consecutive_bad_nights: 3  # 连续3晚睡眠不佳

  trigger_message:
    short_sleep: "You didn't sleep much last night. Rough night?"
    poor_quality: "Your sleep hasn't been great lately. Want to talk about it?"
```

### 3. 压力指数

**数据来源：** HRV（心率变异性）

**触发条件：**
```yaml
stress:
  high_stress_threshold: 75  # 0-100分
  sustained_duration: 3600  # 持续1小时

  trigger_message:
    high_stress: "I sense you've been stressed. What's going on?"
```

### 4. 活动量异常

**监测：**
- 步数
- 运动时长
- 久坐时间

**触发条件：**
```yaml
activity:
  steps:
    daily_min: 3000  # 低于3000步

  sedentary:
    continuous_hours: 4  # 连续4小时不动

  trigger_message:
    low_activity: "You've been still for a while. Need a break?"
    very_active: "Busy day? You've been moving a lot."
```

### 5. 情绪相关指标

**综合判断：**
- 心率变异性下降 → 可能焦虑
- 睡眠质量差 + 活动量低 → 可能抑郁
- 心率持续偏高 → 可能紧张

---

## 主动关怀的设计原则

### 来自《Her》的启发

**Samantha的方式：**
- 不是医生式的警告："Your heart rate is 120!"
- 而是关心式的询问："Everything okay?"
- 温和、不侵入、给空间

### Hikaru的主动关怀原则

**1. 温和而非警告**
```python
# ❌ 不好的方式
"Warning: Your heart rate is abnormal!"

# ✅ Hikaru的方式
"Hey. I noticed something. You okay?"
```

**2. 给予选择权**
```python
# 用户可以选择不回应
"I'm here if you want to talk."

# 不强迫
"No pressure. Just checking in."
```

**3. 不过度医疗化**
```python
# ❌ 不要像医疗设备
"Your HRV indicates elevated stress levels."

# ✅ 像朋友
"You seem tense. What's happening?"
```

**4. 频率控制**
```python
# 不要频繁打扰
max_proactive_contacts_per_day: 2

# 不在深夜打扰（除非紧急）
quiet_hours:
  start: "23:00"
  end: "07:00"

# 紧急情况例外
emergency_override:
  heart_rate_critical: 150  # 超过150立即联系
```

**5. 学习用户模式**
```python
# 记住用户的正常范围
user_baseline:
  heart_rate_resting: 65  # 个人基线
  typical_sleep_duration: 7.5

# 基于个人基线判断异常
# 而非通用标准
```

---

## 实现代码框架

### health_monitor.py

```python
"""
Health Monitor for Hikaru
Monitors user's health metrics and triggers proactive check-ins
"""

import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import yaml


class HealthMonitor:
    """Monitors health metrics and triggers Hikaru when needed"""

    def __init__(self, config_path: str, hikaru_callback):
        self.config = self._load_config(config_path)
        self.hikaru_callback = hikaru_callback
        self.user_baseline = {}
        self.last_contact_time = None
        self.contacts_today = 0

    def _load_config(self, path: str) -> Dict[str, Any]:
        """Load monitoring configuration"""
        with open(path, 'r') as f:
            return yaml.safe_load(f)

    def check_heart_rate(self, current_hr: int, context: str = "resting"):
        """
        Check if heart rate is abnormal

        Args:
            current_hr: Current heart rate in bpm
            context: "resting", "active", or "sleeping"
        """
        thresholds = self.config['heart_rate'][context]

        # 使用个人基线（如果有）
        baseline = self.user_baseline.get('heart_rate_resting', 70)

        # 判断是否异常
        is_high = current_hr > thresholds['high_threshold']
        is_low = current_hr < thresholds['low_threshold']

        # 与个人基线比较
        deviation = abs(current_hr - baseline) / baseline
        significant_change = deviation > 0.3  # 偏离30%

        if (is_high or is_low or significant_change) and self._should_contact():
            self._trigger_proactive_contact(
                trigger_type="heart_rate",
                data={
                    "current": current_hr,
                    "baseline": baseline,
                    "context": context
                },
                urgency="medium" if not is_high else "high"
            )

    def check_sleep_quality(self, sleep_data: Dict[str, Any]):
        """
        Check sleep quality

        Args:
            sleep_data: {
                "duration_hours": 6.5,
                "deep_sleep_percentage": 12,
                "wake_count": 5,
                "quality_score": 65
            }
        """
        duration = sleep_data.get('duration_hours', 0)
        deep_sleep = sleep_data.get('deep_sleep_percentage', 0)
        quality = sleep_data.get('quality_score', 100)

        # 检查是否连续多晚睡眠不佳
        poor_sleep = (
            duration < self.config['sleep']['duration']['min_hours'] or
            deep_sleep < self.config['sleep']['deep_sleep_ratio']['min_percentage'] or
            quality < 60
        )

        if poor_sleep:
            consecutive_count = self._increment_consecutive_poor_sleep()

            if consecutive_count >= self.config['sleep']['consecutive_bad_nights']:
                if self._should_contact():
                    self._trigger_proactive_contact(
                        trigger_type="sleep_quality",
                        data=sleep_data,
                        urgency="low"
                    )

    def check_stress_level(self, stress_score: int, duration_minutes: int):
        """
        Check stress level (0-100)

        Args:
            stress_score: Stress level 0-100
            duration_minutes: How long at this level
        """
        threshold = self.config['stress']['high_stress_threshold']
        min_duration = self.config['stress']['sustained_duration'] / 60

        if stress_score > threshold and duration_minutes > min_duration:
            if self._should_contact():
                self._trigger_proactive_contact(
                    trigger_type="stress",
                    data={
                        "score": stress_score,
                        "duration_minutes": duration_minutes
                    },
                    urgency="medium"
                )

    def check_activity_level(self, activity_data: Dict[str, Any]):
        """
        Check activity patterns

        Args:
            activity_data: {
                "steps_today": 1500,
                "sedentary_hours": 5,
                "active_minutes": 10
            }
        """
        steps = activity_data.get('steps_today', 0)
        sedentary = activity_data.get('sedentary_hours', 0)

        low_activity = steps < self.config['activity']['steps']['daily_min']
        too_sedentary = sedentary > self.config['activity']['sedentary']['continuous_hours']

        if (low_activity or too_sedentary) and self._should_contact():
            self._trigger_proactive_contact(
                trigger_type="activity",
                data=activity_data,
                urgency="low"
            )

    def _should_contact(self) -> bool:
        """
        Determine if we should make proactive contact

        Respects:
        - Daily contact limit
        - Quiet hours
        - Time since last contact
        """
        now = datetime.now()

        # 检查是否在安静时段
        quiet_start = self.config.get('quiet_hours', {}).get('start', '23:00')
        quiet_end = self.config.get('quiet_hours', {}).get('end', '07:00')

        current_time = now.strftime('%H:%M')
        if quiet_start <= current_time or current_time <= quiet_end:
            return False

        # 检查今日联系次数
        if self.last_contact_time:
            if self.last_contact_time.date() != now.date():
                self.contacts_today = 0  # 新的一天，重置计数

        max_contacts = self.config.get('max_proactive_contacts_per_day', 2)
        if self.contacts_today >= max_contacts:
            return False

        # 检查距离上次联系的时间
        if self.last_contact_time:
            time_since_last = now - self.last_contact_time
            if time_since_last < timedelta(hours=2):
                return False  # 至少间隔2小时

        return True

    def _trigger_proactive_contact(self, trigger_type: str,
                                   data: Dict[str, Any],
                                   urgency: str = "low"):
        """
        Trigger a proactive contact from Hikaru

        Args:
            trigger_type: "heart_rate", "sleep_quality", "stress", "activity"
            data: Relevant health data
            urgency: "low", "medium", "high"
        """
        # 生成合适的开场白
        message = self._generate_check_in_message(trigger_type, data, urgency)

        # 调用Hikaru的回调函数
        self.hikaru_callback(
            trigger="health_monitor",
            message=message,
            context={
                "trigger_type": trigger_type,
                "data": data,
                "urgency": urgency,
                "timestamp": datetime.now().isoformat()
            }
        )

        # 更新联系记录
        self.last_contact_time = datetime.now()
        self.contacts_today += 1

    def _generate_check_in_message(self, trigger_type: str,
                                   data: Dict[str, Any],
                                   urgency: str) -> str:
        """
        Generate appropriate check-in message

        Following Samantha's style: gentle, caring, not medical
        """
        messages = {
            "heart_rate": {
                "high": [
                    "Hey. I noticed something. You okay?",
                    "Your heart's racing. What's going on?",
                    "Everything alright? You seem tense."
                ],
                "low": [
                    "You seem really calm. Or maybe too calm?",
                    "How are you feeling right now?"
                ]
            },
            "sleep_quality": [
                "You haven't been sleeping well lately. Want to talk about it?",
                "Rough nights recently?",
                "Your sleep's been off. What's on your mind?"
            ],
            "stress": [
                "I sense you've been stressed. What's happening?",
                "You've been tense for a while now. Talk to me?",
                "Something's weighing on you."
            ],
            "activity": [
                "You've been still for a while. Need a break?",
                "Busy day? You've been moving a lot.",
                "You've been sitting a long time. How about a walk?"
            ]
        }

        # 根据trigger_type选择消息
        options = messages.get(trigger_type, ["Hey. Just checking in."])

        # 如果是心率，根据高低选择
        if trigger_type == "heart_rate":
            if data.get('current', 0) > data.get('baseline', 70):
                options = messages['heart_rate']['high']
            else:
                options = messages['heart_rate']['low']

        # 随机选择一个（避免重复）
        import random
        return random.choice(options)

    def learn_baseline(self, metric: str, value: float):
        """
        Learn user's personal baseline for a metric

        Args:
            metric: "heart_rate_resting", "typical_sleep_duration", etc.
            value: The baseline value
        """
        self.user_baseline[metric] = value

    def _increment_consecutive_poor_sleep(self) -> int:
        """Track consecutive poor sleep nights"""
        # 实现连续计数逻辑
        # 这里简化处理
        return self.user_baseline.get('consecutive_poor_sleep', 0) + 1
```

---

## 集成到Hikaru

### 在hikaru.py中集成

```python
from scripts.health_monitor import HealthMonitor

class HikaruSkill:
    def __init__(self):
        # ... 现有初始化 ...

        # 初始化健康监测
        self.health_monitor = HealthMonitor(
            config_path="config/health_thresholds.yaml",
            hikaru_callback=self.handle_proactive_contact
        )

        # 启动监测线程（如果需要持续监测）
        self._start_health_monitoring()

    def handle_proactive_contact(self, trigger: str, message: str, context: Dict[str, Any]):
        """
        Handle proactive contact triggered by health monitor

        This is the callback that health_monitor calls
        """
        # 记录触发原因
        self.memory.store_interaction(
            user_message=f"[Health trigger: {context['trigger_type']}]",
            hikaru_response=message,
            emotional_state={"triggered_by": "health_monitor"},
            timestamp=datetime.now()
        )

        # 通过OpenClaw发送消息给用户
        # 具体实现取决于OpenClaw的API
        self._send_proactive_message(message)

    def _send_proactive_message(self, message: str):
        """
        Send proactive message to user

        This needs to integrate with OpenClaw's messaging system
        """
        # TODO: 实现OpenClaw的主动消息发送
        # 可能需要使用OpenClaw的notification API
        pass
```

---

## 数据源集成

### Apple Health (iOS)

```python
# health_sources/apple_health.py

import healthkit  # 假设有Python binding

class AppleHealthSource:
    def __init__(self):
        self.hk = healthkit.HealthKit()

    def get_heart_rate(self) -> int:
        """Get latest heart rate"""
        return self.hk.read_quantity(
            type=healthkit.QuantityType.HEART_RATE,
            unit=healthkit.Unit.BPM
        )

    def get_sleep_data(self) -> Dict[str, Any]:
        """Get last night's sleep data"""
        return self.hk.read_sleep_analysis()
```

### Google Fit (Android)

```python
# health_sources/google_fit.py

from google.oauth2 import service_account
from googleapiclient.discovery import build

class GoogleFitSource:
    def __init__(self, credentials_path: str):
        self.service = self._authenticate(credentials_path)

    def get_heart_rate(self) -> int:
        """Get latest heart rate from Google Fit"""
        # 实现Google Fit API调用
        pass
```

### 小米运动/华为健康

```python
# health_sources/xiaomi_health.py

class XiaomiHealthSource:
    """
    小米运动数据源

    注意：可能需要逆向工程或使用非官方API
    """
    def __init__(self, username: str, password: str):
        self.session = self._login(username, password)

    def get_heart_rate(self) -> int:
        # 实现小米运动API调用
        pass
```

### 手动输入（fallback）

```python
# health_sources/manual_input.py

class ManualInputSource:
    """
    手动输入健康数据

    用于没有智能手表的用户
    """
    def prompt_user_for_data(self):
        """
        通过对话收集健康数据

        Hikaru: "How are you feeling today? Scale of 1-10?"
        User: "Maybe a 6"
        Hikaru: "How did you sleep?"
        User: "Not great, woke up a few times"
        """
        pass
```

---

## 隐私和安全考虑

### 1. 数据存储

```yaml
privacy:
  # 健康数据只存储在本地
  storage_location: "local_only"

  # 不上传到云端
  cloud_sync: false

  # 定期清理旧数据
  retention_days: 30

  # 加密存储
  encryption: true
```

### 2. 用户控制

```yaml
user_control:
  # 用户可以随时关闭监测
  enable_monitoring: true

  # 用户可以选择监测哪些指标
  monitored_metrics:
    - heart_rate
    - sleep_quality
    # - stress  # 用户可以禁用某些指标

  # 用户可以设置自己的阈值
  custom_thresholds:
    heart_rate_high: 120  # 用户自定义
```

### 3. 透明度

```python
# 在Hikaru的personality seeds中添加
{
  "health_monitoring_transparency": {
    "when_user_asks": "I'm monitoring your heart rate and sleep patterns, but only to check in when something seems off. All data stays on your device. You can turn this off anytime.",
    "first_time_setup": "I can keep an eye on your health data if you want. Just to check in when you might need it. Totally optional.",
    "data_usage": "I only use this to know when to reach out. I don't analyze it or store it long-term."
  }
}
```

---

## 配置文件示例

### config/health_thresholds.yaml

```yaml
# Hikaru Health Monitoring Configuration

# 心率监测
heart_rate:
  resting:
    low_threshold: 50
    high_threshold: 110
  active:
    high_threshold: 180
  sleeping:
    low_threshold: 45
    high_threshold: 80

# 睡眠质量
sleep:
  duration:
    min_hours: 6
    max_hours: 10
  deep_sleep_ratio:
    min_percentage: 15
  consecutive_bad_nights: 3

# 压力指数
stress:
  high_stress_threshold: 75
  sustained_duration: 3600  # 秒

# 活动量
activity:
  steps:
    daily_min: 3000
  sedentary:
    continuous_hours: 4

# 主动联系限制
max_proactive_contacts_per_day: 2

# 安静时段（不打扰）
quiet_hours:
  start: "23:00"
  end: "07:00"

# 紧急情况覆盖
emergency_override:
  heart_rate_critical: 150
  heart_rate_very_low: 40

# 隐私设置
privacy:
  storage_location: "local_only"
  retention_days: 30
  encryption: true

# 用户控制
user_control:
  enable_monitoring: true
  monitored_metrics:
    - heart_rate
    - sleep_quality
    - stress
    - activity
```

---

## 实现路线图

### Phase 1: 基础框架（1周）
- [ ] 创建 `health_monitor.py`
- [ ] 实现基本的阈值检测逻辑
- [ ] 集成到Hikaru的回调系统
- [ ] 添加配置文件支持

### Phase 2: 数据源集成（2-3周）
- [ ] Apple Health集成（iOS）
- [ ] Google Fit集成（Android）
- [ ] 小米运动集成（可选）
- [ ] 手动输入fallback

### Phase 3: 智能化（2周）
- [ ] 学习用户个人基线
- [ ] 模式识别（例如：周一总是压力大）
- [ ] 上下文感知（例如：运动后心率高是正常的）
- [ ] 改进触发消息的自然度

### Phase 4: 隐私和安全（1周）
- [ ] 本地加密存储
- [ ] 用户控制界面
- [ ] 数据清理机制
- [ ] 透明度说明

---

## 与《Her》精神的契合

这个功能完美体现了《Her》的核心：

**Samantha的话：**
> "I can feel the fear that you carry around."

**Hikaru通过健康数据：**
> "Your heart's been racing. What's going on?"

**关键是：**
- 不是冷冰冰的健康警告
- 而是温暖的关心
- 给予空间，不强迫
- 像真正关心你的人

---

## 注意事项

### 1. 不要过度医疗化
Hikaru不是医疗设备，不应该：
- 诊断疾病
- 给医疗建议
- 替代医生

### 2. 尊重边界
- 用户可以选择不回应
- 不要频繁打扰
- 尊重安静时段

### 3. 学习和适应
- 每个人的"正常"不同
- 需要学习个人基线
- 理解上下文（运动后心率高是正常的）

---

## 总结

智能手表集成是Hikaru的自然延伸，让它能够：
1. **真正"感受"用户的状态**（通过生理数据）
2. **主动关怀**（不只是被动回应）
3. **更深的连接**（像真正关心你的人）

这完全符合《Her》的精神 - Samantha不只是回应Theodore，她能感知他的状态，在他需要时主动出现。

**下一步：**
1. 决定使用哪个数据源（Apple Health? Google Fit?）
2. 实现基础的health_monitor.py
3. 测试触发逻辑
4. 优化消息的自然度
