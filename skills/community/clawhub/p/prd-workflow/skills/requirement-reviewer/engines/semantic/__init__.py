# Semantic Package - 内容检查层
# 基于AI理解的PRD内容质量检查
#
# 检查项：
# - 核心：流程描述、异常处理
# - 完善：改造内容标注、元素完整性、交互逻辑、算法公式、查询关联、GWT验收标准、系统对接描述
# - 优化：分项描述、界面细节、改造类型、原型附件

from .check_items import CHECK_ITEMS, CheckItem, Priority
from .section_parser import SectionParser
from .section_matcher import SectionMatcher
from .ai_checker import AIContentChecker

__all__ = [
    "CHECK_ITEMS",
    "CheckItem",
    "Priority",
    "SectionParser",
    "SectionMatcher",
    "AIContentChecker"
]