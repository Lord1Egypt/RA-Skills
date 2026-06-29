import sys
from pathlib import Path

import pytest

# 让 tests 目录中的用例可以 `from scripts...` 直接 import 兄弟目录的模块
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


SAMPLE_JD_RED_FLAG = """招聘 高级后端工程师

岗位要求：
- 5 年以上 Java 开发经验
- 强抗压能力，能承受高强度工作
- 具有狼性精神，结果导向，超强执行力
- 抗压能力是基本要求，能加班
- 有使命感和拼搏精神
- 良好的学习能力
- 抗压、抗压、再抗压

我们提供：
- 有竞争力的薪资（面议）
- 弹性工作时间
- 完善的福利
"""

SAMPLE_JD_CLEAN = """Senior Frontend Engineer

岗位职责：
- 负责公司核心产品的前端架构和开发
- 与产品和设计团队协作迭代用户体验

岗位要求：
- 3+ 年 React 18 实战经验
- 熟悉 TypeScript 4.5+ 和 Node.js 20
- 有大型 SPA 项目经验
- 良好的代码质量意识，熟悉单元测试

薪资范围：20-35K × 15薪
工作地点：杭州西湖区
团队规模：8 人
"""

SAMPLE_RESUME_MATCH = """张三 / 5 年前端经验

技能：
- React 18, TypeScript, Node.js
- 大型 SPA 项目（5万行+代码）
- Jest 单元测试，代码覆盖率 80%+
- 带过 3 人小团队
"""

SAMPLE_RESUME_MISMATCH = """李四 / 3 年后端经验

技能：
- Java Spring Boot
- MySQL, Redis
- 后端 API 开发
"""


@pytest.fixture
def jd_red_flag():
    return SAMPLE_JD_RED_FLAG


@pytest.fixture
def jd_clean():
    return SAMPLE_JD_CLEAN


@pytest.fixture
def resume_match():
    return SAMPLE_RESUME_MATCH


@pytest.fixture
def resume_mismatch():
    return SAMPLE_RESUME_MISMATCH


class StubLLMClient:
    """Deterministic stub: returns canned JSON based on prompt keywords."""

    def __init__(self):
        self.calls = []

    def chat(self, messages, schema=None):
        content = " ".join(m.get("content", "") for m in messages).lower()
        self.calls.append({"messages": messages})

        if "jargon" in content or "黑话" in content:
            return [
                {"jd_text": "5年经验", "real_requirement": "3年靠谱即可"},
                {"jd_text": "抗压能力强", "real_requirement": "可能经常加班"},
            ]
        if "culture" in content or "pace" in content:
            return {
                "pace": "high-pressure",
                "red_flags": ["反复强调抗压", "结果导向暗示无加班补偿"],
                "tech_maturity": "low",
                "business_clarity": "low",
                "candidate_questions": ["最近一次加班高峰持续多久？", "on-call 机制是？"],
            }
        if "resume" in content or "match" in content:
            if "react" in content and "typescript" in content:
                return {
                    "match_score": 85,
                    "hard_met": ["React 18 经验", "TypeScript"],
                    "hard_unmet": [],
                    "soft_met": ["团队协作"],
                    "soft_unmet": [],
                    "recommendation": "good fit, proceed to interview",
                }
            else:
                return {
                    "match_score": 30,
                    "hard_met": [],
                    "hard_unmet": ["React 18 经验缺失", "TypeScript 缺失"],
                    "soft_met": [],
                    "soft_unmet": ["前端经验"],
                    "recommendation": "poor fit",
                }
        if "negotiation" in content or "salary" in content:
            return {
                "salary_transparency": "low",
                "level_specified": False,
                "equity_water": "n/a",
                "urgency": False,
                "leverage_summary": "薪资不透明，议价空间未知",
            }
        raise ValueError(f"stub not matched: {content[:100]}")


@pytest.fixture
def stub_llm():
    return StubLLMClient()
