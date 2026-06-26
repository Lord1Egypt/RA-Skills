# Prompt-Router 集成方案

## 当前架构

```
用户消息 → LLM 推理 → using-superpowers 判断 → Skill 工具调用 → 执行 → 回复
                      ↑
                  主观判断（1% 可能性）
```

**问题：**
- 每次都需要 LLM 推理（500ms-2s）
- 依赖 LLM 主观判断
- 简单任务也消耗 Token

## 目标架构

```
用户消息 → Prompt-Router → {高置信度 → 直接调用技能}
                          ↓
                    {低置信度 → LLM 推理 → using-superpowers → Skill 工具}
```

**收益：**
- 60% 简单任务走快速路径（<5ms，¥0 成本）
- 40% 复杂任务降级到 LLM（保持灵活性）

---

## 集成方案

### 方案 1：修改 using-superpowers（推荐）

**优点：**
- 最小改动
- 保持向后兼容
- 所有 Agent 自动受益

**实现：**
1. 在 using-superpowers 开头添加 Prompt-Router 调用逻辑
2. 高置信度匹配直接调用 Skill 工具
3. 低置信度继续原有流程

### 方案 2：创建 wrapper 技能

**优点：**
- 不修改现有技能
- 可独立启用/禁用

**缺点：**
- 需要修改所有 Agent 配置
- 增加一层调用开销

### 方案 3：OpenClaw 核心层集成

**优点：**
- 性能最优
- 系统级支持

**缺点：**
- 需要修改 OpenClaw 源码
- 升级可能覆盖

---

## 推荐：方案 1

### 实施步骤

#### Step 1: 创建 Prompt-Router 调用脚本

```python
# scripts/integration.py
"""
Prompt-Router 集成脚本
供 using-superpowers 调用
"""

import json
import sys
from pathlib import Path

# 导入路由器
sys.path.insert(0, str(Path(__file__).parent))
from router import PromptRouter

def route_prompt(user_message: str) -> dict:
    """
    路由用户消息
    
    Returns:
        {
            "matched": bool,
            "skill_name": str | None,
            "confidence": float,
            "confidence_level": str,
        }
    """
    router = PromptRouter(
        skills_dir='C:/Users/User/.openclaw/workspace/skills',
        confidence_threshold=0.25,
        high_confidence_threshold=0.8,
    )
    
    try:
        router.load_skills()
        result = router.route(user_message)
        
        return {
            "matched": result.match is not None,
            "skill_name": result.match['name'] if result.match else None,
            "confidence": result.confidence,
            "confidence_level": result.confidence_level,
            "score": result.score,
        }
    except Exception as e:
        return {
            "matched": False,
            "skill_name": None,
            "error": str(e),
        }

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No message provided"}))
        sys.exit(1)
    
    message = sys.argv[1]
    result = route_prompt(message)
    print(json.dumps(result, ensure_ascii=False))
```

#### Step 2: 修改 using-superpowers

在 using-superpowers 开头添加：

```markdown
## 🚀 Prompt-Router 快速路径

在判断是否需要调用技能前，先调用 Prompt-Router 进行快速匹配：

```bash
python ~/.openclaw/workspace/skills/prompt-router/scripts/integration.py "用户消息"
```

**如果返回高置信度匹配（confidence >= 0.5）：**
- 直接调用 Skill 工具加载匹配的技能
- 跳过主观判断步骤

**如果返回低置信度匹配（confidence < 0.5）：**
- 继续原有流程（主观判断是否有技能适用）
```

#### Step 3: 测试集成

1. 发送简单消息："搜索 Python 教程"
2. 验证 Prompt-Router 匹配到 multi-search-engine
3. 验证直接调用 Skill 工具
4. 检查延迟和 Token 消耗

---

## 替代方案：Agent 系统提示集成

如果无法修改 using-superpowers，可以在每个 Agent 的系统提示中添加：

```
## Prompt-Router 指令

在收到用户消息后， FIRST 调用 Prompt-Router 技能进行快速匹配。

如果 Prompt-Router 返回高置信度技能匹配，直接调用该技能。
否则，继续正常流程判断是否有技能适用。
```

---

## 监控指标

集成后需要监控：

1. **路由成功率** - 匹配成功/总请求数
2. **平均延迟** - Prompt-Router vs LLM 路由
3. **Token 节省** - 快速路径 vs 完整流程
4. **用户满意度** - 匹配准确率

---

*创建时间：2026-04-05 23:35*
