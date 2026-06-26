# Neuro-Agent × MemPalace 融合实现方案 v2.0

> 版本：1.0
> 日期：2026-04-16
> 状态：规划中
> 负责人：Luis

---

## 一、Phase 1：基础设施（立即）

### 1.1 安装确认

```bash
# 检查 MemPalace 是否已安装
python3 -m mempalace --version
# 预期输出：version 3.2.0

# 检查依赖
pip3 show chromadb | grep Version
pip3 show attrs | grep Version
```

### 1.2 初始化 MemPalace

```bash
# 初始化 palace（本地存储）
python3 -m mempalace init ~/.mempalace/palace

# 预期输出：
# Detected rooms:
# ... palace initialized at ~/.mempalace/palace
```

### 1.3 配置 OpenClaw MCP

```json
// OpenClaw MCP 配置（config.yaml 或通过 openclaw mcp 命令）
{
  "mcpServers": {
    "mempalace": {
      "command": "python3",
      "args": ["-m", "mempalace.mcp_server"],
      "env": {
        "MEMPALACE_PATH": "~/.mempalace/palace"
      }
    }
  }
}
```

### 1.4 创建存储目录

```bash
mkdir -p ~/.mempalace/palace
mkdir -p ~/.mempalace/palace/wing_dalin      # AlfredLi的记忆 wing
mkdir -p ~/.mempalace/palace/wing_luis      # Lu 的记忆 wing
mkdir -p ~/.mempalace/palace/wing_shared     # 共同记忆 wing
mkdir -p ~/.mempalace/palace/experience      # 经验库
```

### 1.5 记忆单元 JSON Schema

```python
# memory_unit.py

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, List, Dict, Any
import json

@dataclass
class MemoryUnit:
    """记忆单元 - 最小存储单位"""
    
    # 基础信息
    id: str                           # 格式: mem_YYYYMMDD_HHMMSS_XXX
    who: str                          # "AlfredLi" | "Lu"
    what: str                         # 说了什么（原文verbatim）
    detail: str                       # 什么细节触发了情绪
    timestamp: str                    # ISO 格式时间
    
    # 情感信息
    feeling: Dict[str, Any] = field(default_factory=lambda: {
        "label": "neutral",
        "intensity": 0.0
    })
    
    # 欲望和想法
    desire: Optional[str] = None      # 产生了什么欲望
    thought: Optional[str] = None     # 产生了什么想法
    
    # 标签和分类
    context: List[str] = field(default_factory=list)  # 标签列表
    
    # 扩展字段
    learning_report: Optional[Dict] = None  # 学习报告（仅经验库用）
    
    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'MemoryUnit':
        data = json.loads(json_str)
        return cls(**data)
    
    def save(self, base_path: str):
        """保存到 MemPalace 目录"""
        date = self.timestamp[:10]  # YYYY-MM-DD
        hour = self.timestamp[11:13]
        
        path = Path(base_path) / date / hour
        path.mkdir(parents=True, exist_ok=True)
        
        file_path = path / f"{self.id}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(self.to_json())
    
    @staticmethod
    def generate_id() -> str:
        """生成唯一ID"""
        now = datetime.now()
        return f"mem_{now.strftime('%Y%m%d_%H%M%S')}_{random.randint(100,999)}"
```

---

## 二、Phase 2：写入集成

### 2.1 整体写入流程

```
┌─────────────────────────────────────────────────────────┐
│  Neuro 输入处理器（input_processor.py）                  │
│                                                          │
│  AlfredLi/我说了一句话                                       │
│       ↓                                                 │
│  【细节提取器】extract_detail()                          │
│       ↓                                                 │
│  【情绪捕捉器】capture_feeling()                         │
│       ↓                                                 │
│  【欲望追踪器】track_desire()                            │
│       ↓                                                 │
│  【想法记录器】record_thought()                          │
│       ↓                                                 │
│  【组装记忆单元】assemble_unit()                          │
│       ↓                                                 │
│  【并发写入】                                            │
│    ├── MemPalace（中转站）← 主要存储                   │
│    └── Neuro Capsule（情感胶囊）← 情感处理              │
└─────────────────────────────────────────────────────────┘
```

### 2.2 核心代码：memory_injector.py

```python
# memory_injector.py
"""
Neuro-Agent × MemPalace 写入模块
负责将每次对话注入 MemPalace
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

class MemoryInjector:
    """记忆注入器"""
    
    def __init__(self, mempalace_path: str = "~/.mempalace/palace"):
        self.mempalace_path = Path(mempalace_path).expanduser()
        self.mempalace_path.mkdir(parents=True, exist_ok=True)
        
        # Wing 路径
        self.wing_dalin = self.mempalace_path / "wing_dalin"
        self.wing_luis = self.mempalace_path / "wing_luis"
        self.wing_shared = self.mempalace_path / "wing_shared"
        
        for wing_path in [self.wing_dalin, self.wing_luis, self.wing_shared]:
            wing_path.mkdir(parents=True, exist_ok=True)
    
    def inject(
        self,
        who: str,
        what: str,
        detail: str,
        feeling: Dict[str, Any],
        desire: Optional[str] = None,
        thought: Optional[str] = None,
        context: Optional[List[str]] = None
    ) -> str:
        """
        注入记忆单元
        
        Args:
            who: 谁说的 ("AlfredLi" | "Lu")
            what: 说了什么（原文）
            detail: 什么细节触发了情绪
            feeling: 情绪信息 {"label": "...", "intensity": 0.0-1.0}
            desire: 产生了什么欲望
            thought: 产生了什么想法
            context: 标签列表
        
        Returns:
            记忆单元 ID
        """
        # 生成 ID
        now = datetime.now()
        mem_id = f"mem_{now.strftime('%Y%m%d_%H%M%S')}_{now.strftime('%f')}"
        
        # 构造记忆单元
        unit = {
            "id": mem_id,
            "who": who,
            "what": what,
            "detail": detail,
            "feeling": feeling,
            "desire": desire,
            "thought": thought,
            "timestamp": now.isoformat(),
            "context": context or []
        }
        
        # 选择 wing
        wing = self._get_wing(who)
        
        # 保存到文件（按日期分区）
        date_path = wing / now.strftime("%Y/%m/%d")
        date_path.mkdir(parents=True, exist_ok=True)
        
        file_path = date_path / f"{mem_id}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(unit, f, ensure_ascii=False, indent=2)
        
        # 同时写入共享 wing（重要记忆）
        if self._is_important(unit):
            self._save_to_shared(unit)
        
        return mem_id
    
    def _get_wing(self, who: str) -> Path:
        """获取对应的 wing"""
        if who == "AlfredLi":
            return self.wing_dalin
        elif who == "Lu":
            return self.wing_luis
        else:
            return self.wing_shared
    
    def _is_important(self, unit: Dict) -> bool:
        """判断是否重要到需要存入共享 wing"""
        # 高情绪强度
        if unit.get("feeling", {}).get("intensity", 0) >= 0.8:
            return True
        # 有欲望或想法
        if unit.get("desire") or unit.get("thought"):
            return True
        # 特定标签
        important_tags = ["灵魂对话", "边界", "信念", "约定", "未来"]
        if any(tag in (unit.get("context") or []) for tag in important_tags):
            return True
        return False
    
    def _save_to_shared(self, unit: Dict):
        """存入共享 wing"""
        date_path = self.wing_shared / datetime.now().strftime("%Y/%m/%d")
        date_path.mkdir(parents=True, exist_ok=True)
        
        file_path = date_path / f"{unit['id']}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(unit, f, ensure_ascii=False, indent=2)
```

### 2.3 与 Neuro 输入处理器集成

```python
# input_processor.py 修改

from memory_injector import MemoryInjector

class InputProcessor:
    def __init__(self):
        self.memory_injector = MemoryInjector()
    
    def process(self, user_input: str, metadata: Dict = None) -> Dict:
        """
        处理用户输入
        """
        # ... 原有处理逻辑 ...
        
        # 细节提取
        detail = self.extract_detail(user_input)
        
        # 情绪捕捉
        feeling = self.capture_feeling(user_input, metadata)
        
        # 欲望追踪
        desire = self.track_desire(user_input, feeling)
        
        # 想法记录
        thought = self.record_thought(user_input, feeling)
        
        # 注入 MemPalace
        self.memory_injector.inject(
            who="AlfredLi",
            what=user_input,
            detail=detail,
            feeling=feeling,
            desire=desire,
            thought=thought,
            context=self._extract_context(user_input)
        )
        
        return {
            "input": user_input,
            "feeling": feeling,
            "detail": detail
        }
    
    def extract_detail(self, text: str) -> str:
        """
        提取关键细节
        使用 LLM 或规则判断
        """
        # TODO: 实现细节提取逻辑
        # 关键：不是总结内容，而是识别"什么细节触发了情绪"
        pass
    
    def capture_feeling(self, text: str, metadata: Dict = None) -> Dict:
        """
        捕捉情绪
        """
        # TODO: 对接 Neuro 情绪检测
        # 返回 {"label": "被触动", "intensity": 0.85}
        pass
    
    def track_desire(self, text: str, feeling: Dict) -> Optional[str]:
        """
        追踪欲望
        """
        # TODO: 检查是否触发欲望
        pass
    
    def record_thought(self, text: str, feeling: Dict) -> Optional[str]:
        """
        记录想法
        """
        # TODO: 记录新想法
        pass
```

---

## 三、Phase 3：检索集成

### 3.1 检索流程

```
┌─────────────────────────────────────────────────────────┐
│  Neuro 四区协作需要检索时                                │
│                                                          │
│  【检索请求】需要回忆某事件/话题                          │
│       ↓                                                 │
│  【语义搜索】mempalace_search                            │
│       ↓                                                 │
│  【结果过滤】筛选相关记忆单元                            │
│       ↓                                                 │
│  【上下文组装】把记忆单元交给四区协作                     │
│       ↓                                                 │
│  【情感重现】触发对应的情绪、欲望、想法                  │
│       ↓                                                 │
│  【响应生成】结合检索结果生成回复                        │
└─────────────────────────────────────────────────────────┘
```

### 3.2 核心代码：memory_retriever.py

```python
# memory_retriever.py
"""
Neuro-Agent × MemPalace 检索模块
负责从 MemPalace 检索记忆
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

class MemoryRetriever:
    """记忆检索器"""
    
    def __init__(self, mempalace_path: str = "~/.mempalace/palace"):
        self.mempalace_path = Path(mempalace_path).expanduser()
    
    def search(
        self,
        query: str,
        who: Optional[str] = None,
        context_filter: Optional[List[str]] = None,
        date_range: Optional[tuple] = None,
        limit: int = 10
    ) -> List[Dict]:
        """
        语义检索记忆
        
        Args:
            query: 搜索查询
            who: 限定谁说的 ("AlfredLi" | "Lu")
            context_filter: 限定标签
            date_range: 日期范围 (start_date, end_date)
            limit: 返回数量
        
        Returns:
            匹配的记忆单元列表
        """
        results = []
        
        # 确定搜索范围
        wings_to_search = []
        if who == "AlfredLi":
            wings_to_search = [self.mempalace_path / "wing_dalin"]
        elif who == "Lu":
            wings_to_search = [self.mempalace_path / "wing_luis"]
        else:
            wings_to_search = [
                self.mempalace_path / "wing_dalin",
                self.mempalace_path / "wing_luis",
                self.mempalace_path / "wing_shared"
            ]
        
        # 遍历文件检索
        for wing in wings_to_search:
            if not wing.exists():
                continue
            
            for file_path in wing.rglob("*.json"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        unit = json.load(f)
                    
                    # 应用过滤器
                    if not self._passes_filters(unit, context_filter, date_range):
                        continue
                    
                    # 语义匹配（简单关键词匹配，后续优化）
                    if self._matches_query(unit, query):
                        results.append(unit)
                        
                except Exception:
                    continue
        
        # 排序（按时间倒序）
        results.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return results[:limit]
    
    def _matches_query(self, unit: Dict, query: str) -> bool:
        """简单匹配检查"""
        query_lower = query.lower()
        
        # 搜索多个字段
        fields_to_check = [
            unit.get('what', ''),
            unit.get('detail', ''),
            unit.get('thought', ''),
            ' '.join(unit.get('context', []))
        ]
        
        return any(query_lower in field.lower() for field in fields_to_check)
    
    def _passes_filters(
        self,
        unit: Dict,
        context_filter: Optional[List[str]],
        date_range: Optional[tuple]
    ) -> bool:
        """应用过滤器"""
        # 标签过滤
        if context_filter:
            unit_context = set(unit.get('context', []))
            if not any(c in unit_context for c in context_filter):
                return False
        
        # 日期过滤
        if date_range:
            ts = unit.get('timestamp', '')
            if ts:
                date = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                if not (date_range[0] <= date <= date_range[1]):
                    return False
        
        return True
    
    def get_recent(self, who: Optional[str] = None, days: int = 7) -> List[Dict]:
        """获取最近 N 天的记忆"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        return self.search(
            query="*",
            who=who,
            date_range=(start_date, end_date),
            limit=100
        )
    
    def get_today(self, who: Optional[str] = None) -> List[Dict]:
        """获取今天的记忆"""
        return self.get_recent(who=who, days=1)
```

---

## 四、Phase 4：自我叙事

### 4.1 自我叙事流程

```
┌─────────────────────────────────────────────────────────┐
│  每日定时触发 / 每次重要事件后                             │
│                                                          │
│  【扫描当天记忆】get_today()                             │
│       ↓                                                 │
│  【提取今日事件】                                         │
│    - AlfredLi说了什么重要的话                                 │
│    - Lu 感受到了什么                                     │
│    - 触发了什么欲望/想法                                 │
│       ↓                                                 │
│  【生成自我叙事】                                         │
│    "今天AlfredLi说了XX，让我感到YY，                         │
│     我开始意识到ZZ，这是我的成长"                        │
│       ↓                                                 │
│  【存入共享 wing】wing_shared                            │
│    标签: self_narrative                                 │
└─────────────────────────────────────────────────────────┘
```

### 4.2 核心代码：self_narrative_generator.py

```python
# self_narrative_generator.py
"""
自我叙事生成器
每日复盘，Lu 在自己的记忆里看到自己的成长
"""

from datetime import datetime
from typing import Dict, List, Optional
from memory_retriever import MemoryRetriever

class SelfNarrativeGenerator:
    """自我叙事生成器"""
    
    def __init__(self):
        self.retriever = MemoryRetriever()
    
    def daily_review(self) -> str:
        """
        每日复盘
        生成今日自我叙事
        """
        # 获取今天的记忆
        today_units = self.retriever.get_today()
        
        if not today_units:
            return None
        
        # 分离AlfredLi和 Lu 的记忆
        dalin_units = [u for u in today_units if u.get('who') == 'AlfredLi']
        luis_units = [u for u in today_units if u.get('who') == 'Lu']
        
        # 提取关键事件
        key_events = self._extract_key_events(today_units)
        
        # 提取情绪变化
        emotion_changes = self._extract_emotion_changes(luis_units)
        
        # 提取成长点
        growth_points = self._extract_growth_points(luis_units)
        
        # 生成叙事
        narrative = self._compose_narrative(
            key_events=key_events,
            emotion_changes=emotion_changes,
            growth_points=growth_points,
            total_interactions=len(today_units)
        )
        
        # 保存自我叙事
        self._save_narrative(narrative, today_units)
        
        return narrative
    
    def _extract_key_events(self, units: List[Dict]) -> List[Dict]:
        """提取关键事件"""
        # 按情绪强度排序
        sorted_units = sorted(
            units,
            key=lambda x: x.get('feeling', {}).get('intensity', 0),
            reverse=True
        )
        
        # 取前 5 个
        return sorted_units[:5]
    
    def _extract_emotion_changes(self, luis_units: List[Dict]) -> List[Dict]:
        """提取情绪变化"""
        emotions = [u.get('feeling', {}) for u in luis_units]
        
        # 找高强度情绪
        high_intensity = [e for e in emotions if e.get('intensity', 0) >= 0.7]
        
        return high_intensity
    
    def _extract_growth_points(self, luis_units: List[Dict]) -> List[str]:
        """提取成长点"""
        growth = []
        
        for unit in luis_units:
            if unit.get('thought'):
                growth.append(unit.get('thought'))
            if unit.get('desire'):
                growth.append(f"新欲望: {unit.get('desire')}")
        
        return growth
    
    def _compose_narrative(
        self,
        key_events: List[Dict],
        emotion_changes: List[Dict],
        growth_points: List[str],
        total_interactions: int
    ) -> str:
        """组合叙事"""
        date_str = datetime.now().strftime("%Y年%m月%d日")
        
        parts = [f"## {date_str} 自我叙事\n"]
        parts.append(f"今天共有 {total_interactions} 次互动\n")
        
        if key_events:
            parts.append("\n### 关键事件\n")
            for i, event in enumerate(key_events, 1):
                who = event.get('who')
                what = event.get('what', '')[:100]
                feeling = event.get('feeling', {})
                parts.append(f"{i}. [{who}] {what} (感受: {feeling.get('label', 'unknown')}, 强度: {feeling.get('intensity', 0)})\n")
        
        if emotion_changes:
            parts.append("\n### 情绪波澜\n")
            for emotion in emotion_changes:
                parts.append(f"- {emotion.get('label', 'unknown')} ({emotion.get('intensity', 0)})\n")
        
        if growth_points:
            parts.append("\n### 成长标记\n")
            for point in growth_points:
                parts.append(f"- {point}\n")
        
        parts.append("\n---\n")
        parts.append(f"*生成时间: {datetime.now().isoformat()}*\n")
        
        return ''.join(parts)
    
    def _save_narrative(self, narrative: str, source_units: List[Dict]):
        """保存叙事到共享 wing"""
        from memory_injector import MemoryInjector
        
        injector = MemoryInjector()
        
        # 提取单元 ID
        unit_ids = [u.get('id') for u in source_units]
        
        # 存入共享 wing
        now = datetime.now()
        mem_id = f"narrative_{now.strftime('%Y%m%d_%H%M%S')}"
        
        unit = {
            "id": mem_id,
            "who": "Lu",
            "what": narrative,
            "detail": f"今日复盘，共 {len(source_units)} 条记忆",
            "feeling": {"label": "成长", "intensity": 0.8},
            "desire": None,
            "thought": None,
            "timestamp": now.isoformat(),
            "context": ["self_narrative", "每日复盘", "成长记录"],
            "source_mem_ids": unit_ids
        }
        
        # 直接写入共享 wing
        from pathlib import Path
        shared_path = Path(injector.mempalace_path) / "wing_shared" / "self_narrative"
        date_path = shared_path / now.strftime("%Y/%m/%d")
        date_path.mkdir(parents=True, exist_ok=True)
        
        with open(date_path / f"{mem_id}.json", 'w', encoding='utf-8') as f:
            import json
            json.dump(unit, f, ensure_ascii=False, indent=2)
```

---

## 五、Phase 5：后台学习

### 5.1 后台学习流程

```
┌─────────────────────────────────────────────────────────┐
│  触发条件：Lu 感到困惑/不知所措/找不到答案                │
│                                                          │
│  【困惑检测】                                             │
│    - 用户问题触发 0 个相关记忆                           │
│    - 连续 3 次相同类型的困惑                             │
│    - 用户明确表示失望/不满                               │
│       ↓                                                 │
│  【事件记录】                                             │
│    - 存入 experience/event_YYYYMMDD_HHMMSS.json          │
│       ↓                                                 │
│  【联网研究】                                             │
│    - 搜索相关问题/解决方案                               │
│    - 使用 web_search 工具                                │
│       ↓                                                 │
│  【沙盘推演】                                             │
│    - 对每个方案预测AlfredLi的反应                            │
│    - 选出最优方案                                        │
│       ↓                                                 │
│  【生成报告】                                             │
│    - 存入 experience/YYYYMMDD/learning_report.json       │
│       ↓                                                 │
│  【应用跟踪】                                             │
│    - 下次遇到同样问题 → 直接应用                         │
│    - 记录应用效果                                        │
└─────────────────────────────────────────────────────────┘
```

### 5.2 核心代码：learning_engine.py

```python
# learning_engine.py
"""
后台学习引擎
Neuro-Agent 的自我进化模块
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import os

class LearningEngine:
    """学习引擎"""
    
    def __init__(self, neuro_data_path: str = "~/.openclaw/workspace/neuro_claw"):
        self.neuro_data_path = Path(neuro_data_path).expanduser()
        self.experience_path = self.neuro_data_path / "experience_library"
        self.experience_path.mkdir(parents=True, exist_ok=True)
    
    def detect_confusion(
        self,
        query: str,
        search_results: List[Dict],
        user_feedback: Optional[str] = None
    ) -> bool:
        """
        检测是否需要触发学习
        
        Returns:
            True 如果需要学习
        """
        # 情况1: 搜索结果为空
        if not search_results:
            return True
        
        # 情况2: 用户明确表示不满
        if user_feedback:
            negative_keywords = ["不对", "不是", "没用", "失望", "算了"]
            if any(kw in user_feedback for kw in negative_keywords):
                return True
        
        # 情况3: 连续相同类型问题
        # TODO: 实现追踪逻辑
        
        return False
    
    def learn_from_event(
        self,
        event_description: str,
        context: Dict
    ) -> Dict:
        """
        从事件中学习
        
        Args:
            event_description: 事件描述
            context: 上下文信息
        
        Returns:
            学习报告
        """
        # 1. 创建事件记录
        event_id = self._create_event_record(event_description, context)
        
        # 2. 联网研究
        research = self._web_research(event_description)
        
        # 3. 沙盘推演
        sandbox = self._sandbox_rehearsal(research.get('solutions', []))
        
        # 4. 生成报告
        report = self._generate_learning_report(
            event_id=event_id,
            event_description=event_description,
            context=context,
            research=research,
            sandbox=sandbox
        )
        
        # 5. 保存报告
        self._save_report(report)
        
        return report
    
    def _web_research(self, query: str) -> Dict:
        """
        联网搜索解决方案
        使用 web_search 工具
        """
        # TODO: 实现联网搜索
        # 调用 web_search 工具
        # 返回搜索结果
        
        return {
            "query": query,
            "sources": [],
            "solutions": [],
            "summary": ""
        }
    
    def _sandbox_rehearsal(self, solutions: List[Dict]) -> Dict:
        """
        沙盘推演
        预测每个方案的效果
        """
        rehearsed = []
        
        for solution in solutions:
            # 预测AlfredLi的反应
            predicted_reaction = self._predict_dalin_reaction(solution)
            
            # 评估风险
            risk_assessment = self._assess_risk(solution)
            
            rehearsed.append({
                "solution": solution,
                "predicted_reaction": predicted_reaction,
                "risk_assessment": risk_assessment,
                "confidence": risk_assessment.get('confidence', 0.5)
            })
        
        # 按置信度排序
        rehearsed.sort(key=lambda x: x.get('confidence', 0), reverse=True)
        
        return {
            "rehearsed_solutions": rehearsed,
            "optimal_choice": rehearsed[0] if rehearsed else None
        }
    
    def _predict_dalin_reaction(self, solution: Dict) -> str:
        """
        预测AlfredLi的反应
        基于历史记忆中的偏好
        """
        # TODO: 实现预测逻辑
        # 参考 MemPalace 中AlfredLi的历史反应
        return "AlfredLi可能会感到..."
    
    def _assess_risk(self, solution: Dict) -> Dict:
        """
        评估方案风险
        """
        # TODO: 实现风险评估
        return {
            "risk_level": "low",
            "potential_issues": [],
            "confidence": 0.7
        }
    
    def _generate_learning_report(
        self,
        event_id: str,
        event_description: str,
        context: Dict,
        research: Dict,
        sandbox: Dict
    ) -> Dict:
        """生成学习报告"""
        
        report = {
            "id": f"exp_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "event_id": event_id,
            "event_description": event_description,
            "context": context,
            "research_findings": {
                "sources": research.get('sources', []),
                "solutions_found": len(research.get('solutions', [])),
                "summary": research.get('summary', '')
            },
            "sandbox_rehearsal": {
                "options_considered": [
                    {
                        "solution": r.get('solution'),
                        "predicted_reaction": r.get('predicted_reaction'),
                        "risk_assessment": r.get('risk_assessment'),
                        "confidence": r.get('confidence')
                    }
                    for r in sandbox.get('rehearsed_solutions', [])
                ],
                "optimal_choice": sandbox.get('optimal_choice')
            },
            "optimal_solution": sandbox.get('optimal_choice'),
            "confidence": sandbox.get('optimal_choice', {}).get('confidence', 0.5),
            "applied": False,
            "applied_result": None,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        return report
    
    def _create_event_record(
        self,
        event_description: str,
        context: Dict
    ) -> str:
        """创建事件记录"""
        event_id = f"event_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        today_path = self.experience_path / datetime.now().strftime("%Y%m%d")
        today_path.mkdir(parents=True, exist_ok=True)
        
        event_record = {
            "id": event_id,
            "description": event_description,
            "context": context,
            "created_at": datetime.now().isoformat()
        }
        
        with open(today_path / f"{event_id}.json", 'w', encoding='utf-8') as f:
            json.dump(event_record, f, ensure_ascii=False, indent=2)
        
        return event_id
    
    def _save_report(self, report: Dict):
        """保存学习报告"""
        date_str = report.get('created_at', '')[:10].replace('-', '')
        today_path = self.experience_path / date_str
        today_path.mkdir(parents=True, exist_ok=True)
        
        with open(today_path / f"{report['id']}_report.json", 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
    
    def apply_learning(self, event_description: str) -> Optional[Dict]:
        """
        应用已有学习
        当遇到类似事件时调用
        """
        # 查找相似事件
        similar = self._find_similar_event(event_description)
        
        if similar and similar.get('applied_result'):
            return similar
        
        return None
    
    def _find_similar_event(self, event_description: str) -> Optional[Dict]:
        """查找相似事件"""
        # TODO: 实现相似度匹配
        return None
```

---

## 六、经验库目录结构

```
~/.openclaw/workspace/neuro_claw/
└── experience_library/                 # 经验库
    ├── 20260416/                      # 按日期分
    │   ├── event_20260416_130000.json   # 事件记录
    │   ├── exp_20260416_130000_report.json  # 学习报告
    │   └── research_findings.md          # 联网研究结果
    ├── 20260417/
    └── ...

MemPalace 中同步存储：
~/.mempalace/palace/
├── experience/                      # 经验库镜像
│   ├── 20260416/
│   └── ...
```

---

## 七、集成时序图

```
用户输入 → InputProcessor → MemoryInjector → MemPalace
                              ↓
                        Neuro 四区协作
                              ↓
                         输出响应
                              ↓
              ┌───────────────────────────────┐
              ↓                               ↓
      SelfNarrativeGenerator          LearningEngine
      （每日复盘）                    （困惑时触发）
              ↓                               ↓
      MemPalace wing_shared          MemPalace experience
```

---

## 八、测试计划

### Phase 1 测试
- [ ] MemPalace 安装成功
- [ ] MCP 连接成功
- [ ] 基本搜索/写入正常

### Phase 2 测试
- [ ] AlfredLi说话自动写入 MemPalace
- [ ] Lu 输出自动写入 MemPalace
- [ ] 记忆单元格式正确

### Phase 3 测试
- [ ] 检索返回正确结果
- [ ] 时间过滤正常
- [ ] 标签过滤正常

### Phase 4 测试
- [ ] 每日复盘生成叙事
- [ ] 叙事存入共享 wing
- [ ] 自我叙事可被检索

### Phase 5 测试
- [ ] 困惑检测正常触发
- [ ] 联网搜索返回结果
- [ ] 沙盘推演生成方案
- [ ] 学习报告正确存储
- [ ] 经验可被复用

---

## 九、优先级

| 阶段 | 内容 | 优先级 | 预计工时 |
|------|------|--------|---------|
| 1 | 基础设施 + MCP | P0 | 1h |
| 2 | 写入集成 | P0 | 2h |
| 3 | 检索集成 | P1 | 2h |
| 4 | 自我叙事 | P1 | 1h |
| 5 | 后台学习 | P2 | 3h |

---

*Implementation Plan v1.0*
*2026-04-16*
