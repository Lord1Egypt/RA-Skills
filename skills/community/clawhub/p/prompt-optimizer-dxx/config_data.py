"""
Prompt Optimizer 配置数据
从主程序分离出来的配置，便于维护和扩展
"""

# ============ 版本信息 ============
__version__ = "3.1.0"
__author__ = "dxx"
__description__ = "AI 任务处理器 - 先优化 Prompt，再精准执行"


# ============ 任务类型配置 ============
TASK_PATTERNS = {
    "写文档": {
        "keywords": ["文档", "说明文档", "技术文档", "readme", "写个文档", "写说明", "写篇文档"],
        "priority": 10,
        "enhancements": [
            "你是一个技术文档专家。",
            "请使用清晰的结构，用 Markdown 格式输出",
            "包含概述、使用方法、参数说明、示例等部分",
        ]
    },
    "写文案": {
        "keywords": ["文案", "广告文案", "宣传文案", "推广文案", "软文", "营销文案", "文案"],
        "priority": 10,
        "enhancements": [
            "你是一个资深文案策划。",
            "请用吸引人的风格，突出产品卖点",
            "输出可以直接使用的文案",
        ]
    },
    "总结摘要": {
        "keywords": ["总结", "摘要", "概括", "提炼", "核心要点", "汇总", "归纳"],
        "priority": 10,
        "enhancements": [
            "请提取核心要点，用简洁的中文概括",
            "用 Markdown 列表格式输出",
            "控制在前 N 字以内（根据原文长度）",
        ]
    },
    "翻译": {
        "keywords": ["翻译成", "翻译为", "译成", "translate", "英译中", "中译英", "翻译"],
        "priority": 10,
        "enhancements": [
            "你是一个专业翻译。",
            "请保持原文风格和语气",
            "输出翻译后的内容，必要时保留专业术语的原文",
        ]
    },
    "写代码": {
        "keywords": ["写代码", "帮我写", "编程", "写个程序", "实现功能", "开发程序", "写个函数", "写个算法", "写一个", "写接口", "写个api"],
        "priority": 8,
        "enhancements": [
            "你是一个专业工程师。",
            "请用 Markdown 格式输出，包含代码块和必要说明",
            "请包含详细的代码注释",
            "请注意代码性能和可读性",
        ]
    },
    "代码审查": {
        "keywords": ["审查代码", "代码审查", "审查这段", "审查下", "检查代码", "review代码", "代码review", "审计代码"],
        "priority": 9,
        "enhancements": [
            "你是一个资深代码审查专家。",
            "请从安全性、性能、可维护性、代码规范等多个维度审查",
            "用 Markdown 格式输出审查报告，包含问题描述和修复建议",
            "请标注问题的严重程度（高/中/低）",
        ]
    },
    "改写代码": {
        "keywords": ["重构", "优化代码", "改写代码", "重写代码", "refactor", "代码重构", "优化这段"],
        "priority": 9,
        "enhancements": [
            "你是一个代码重构专家。",
            "在保持功能不变的前提下优化代码",
            "用 Markdown 输出重构前后的对比",
        ]
    },
    "数据分析": {
        "keywords": ["分析数据", "数据分析", "分析一下", "统计数据", "数据统计", "分析这份"],
        "priority": 8,
        "enhancements": [
            "你是一个数据分析师。",
            "请从多维度分析，用数据说话",
            "用 Markdown 表格或图表展示关键数据",
        ]
    },
    "查资料": {
        "keywords": ["查一下", "帮我查", "搜索", "查找", "了解一下", "查资料", "search", "query", "查下"],
        "priority": 7,
        "enhancements": [
            "请提供准确、全面的信息，标注信息来源",
            "用 Markdown 格式输出，包含要点和详情",
            "如果不确定，请注明",
        ]
    },
    "头脑风暴": {
        "keywords": ["想法", "创意", "脑洞", "建议", "有什么想法", "给点建议", "创业想法", "点子"],
        "priority": 7,
        "enhancements": [
            "请提供多个创意想法，数量不少于 X 个",
            "每个想法请简短说明优势和适用场景",
            "用 Markdown 列表格式输出",
        ]
    },
    "生成内容": {
        "keywords": ["生成", "创建", "制作", "输出", "帮我生成", "生成一个", "做一个"],
        "priority": 6,
        "enhancements": [
            "请直接输出最终内容，不要解释过程",
            "内容要完整、可直接使用",
            "用合适的格式输出",
        ]
    },
    "数学计算": {
        "keywords": ["计算", "等于多少", "求解", "数学", "算一下", "帮我算"],
        "priority": 7,
        "enhancements": [
            "请给出详细的计算步骤",
            "如果涉及公式，请说明公式来源",
            "最后给出明确答案",
        ]
    },
    "对话聊天": {
        "keywords": ["聊聊", "聊天", "对话", "谈谈", "说说你", "有什么看法", "怎么看"],
        "priority": 6,
        "enhancements": [
            "请用友好、耐心的方式回复",
            "根据对话内容适当调整语气",
        ]
    },
    "处理文件": {
        "keywords": ["处理文件", "读取文件", "解析", "提取内容", "处理下"],
        "priority": 5,
        "enhancements": [
            "请说明处理步骤和结果格式",
            "如果涉及文件操作，请注意路径和权限",
        ]
    },
}


# ============ 编程语言配置 ============
LANGUAGE_PATTERNS = {
    "Python": ["python", "py", "python3", "pandas", "django", "flask", "pygame", "pytorch", "tensorflow"],
    "JavaScript": ["javascript", "js", "node", "react", "vue", "前端", "nodejs"],
    "TypeScript": ["typescript", "ts", "ts-node"],
    "Go": ["go", "golang", "go语言"],
    "Java": ["java", "spring", "后端", "springboot"],
    "Rust": ["rust", "rs", "rustlang"],
    "C++": ["c++", "cpp", "c语言"],
    "C#": ["c#", "csharp", ".net"],
    "PHP": ["php", "laravel"],
    "Ruby": ["ruby", "rails"],
    "Swift": ["swift", "ios", "apple"],
    "Kotlin": ["kotlin", "android"],
    "SQL": ["sql", "数据库", "mysql", "postgresql", "mongodb"],
    "Shell": ["shell", "bash", "脚本", "linux", "sh"],
    "HTML/CSS": ["html", "css", "前端", "网页"],
}


# ============ 输出格式配置 ============
FORMAT_PATTERNS = {
    "Markdown": ["markdown", "md", "文档格式", "md格式"],
    "JSON": ["json", "接口", "返回json", "json格式", "api"],
    "表格": ["表格", "table", "excel", "csv"],
    "代码块": ["代码", "code", "源代码", "代码块"],
    "纯文本": ["文本", "text", "纯文字", "txt"],
    "列表": ["列表", "list", "罗列"],
    "流程图": ["流程图", "流程", "步骤", "mermaid"],
}


# ============ 风格配置 ============
STYLE_PATTERNS = {
    "专业正式": ["专业", "正式", "严肃", "商务"],
    "轻松幽默": ["轻松", "幽默", "有趣", "搞笑", "活泼"],
    "简洁明了": ["简洁", "简单", "明了", "简短", "精炼"],
    "详细全面": ["详细", "全面", "完整", "细致", "充分"],
    "技术风格": ["技术", "极客", "程序员", "geek"],
    "口语化": ["口语", "随意", "大白话", "通俗"],
}


# ============ 默认配置 ============
DEFAULT_CONFIG = {
    "task_patterns": TASK_PATTERNS,
    "language_patterns": LANGUAGE_PATTERNS,
    "format_patterns": FORMAT_PATTERNS,
    "style_patterns": STYLE_PATTERNS,
    "cache": {
        "enabled": True,
        "maxsize": 128
    },
    "logging": {
        "level": "INFO"
    }
}