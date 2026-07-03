# analysis.json Schema Reference

生成报告前，将 LLM 分析结果写入 `analysis.json`，格式如下。脚本 `scripts/generate_report.py` 读取此 JSON 渲染 HTML。

## 顶层结构

```json
{
  "module_1_basic_info": {},
  "module_1_responsibilities": [],
  "module_1_hard_skills_required": [],
  "module_1_hard_skills_plus": [],
  "module_1_soft_skills": [],
  "module_1_education": "",
  "module_2_explicit_implicit": [],
  "module_3_weighted_requirements": [],
  "module_4_gap_assessment": [],
  "module_5_interview_questions": [],
  "module_5_reverse_questions": [],
  "module_6_learning_roadmap": [],
  "module_7_ats_keywords": {},
  "module_7_integration_tips": [],
  "module_8_salary_benchmark": null
}
```

## 各模块字段说明

### 模块一：基本信息

```json
{
  "module_1_basic_info": {
    "title": "高级前端开发工程师",
    "company": "某互联网公司 / AI 行业",
    "location": "北京·海淀区",
    "salary": "30K-50K·15薪",
    "type": "全职"
  },
  "module_1_responsibilities": [
    "负责公司核心产品的前端架构设计与开发",
    "参与技术选型和性能优化"
  ],
  "module_1_hard_skills_required": ["React", "TypeScript", "Webpack"],
  "module_1_hard_skills_plus": ["Node.js", "WebAssembly", "Rust"],
  "module_1_soft_skills": ["沟通协作", "自驱力", "技术热情"],
  "module_1_education": "本科及以上 · 3-5年经验"
}
```

### 模块二：显性隐性映射

```json
{
  "module_2_explicit_implicit": [
    {
      "explicit": "抗压能力强，能适应快速迭代",
      "implicit": "团队节奏快，可能有加班文化，需求变更频繁",
      "strength": "高"
    },
    {
      "explicit": "有 owner 意识",
      "implicit": "需要自驱完成目标，可能一人负责多个模块",
      "strength": "高"
    },
    {
      "explicit": "扁平化管理",
      "implicit": "层级少但晋升通道可能不够明确",
      "strength": "低"
    }
  ]
}
```

**strength 取值**: `"高"` | `"中"` | `"低"`

### 模块三：需求权重评分

```json
{
  "module_3_weighted_requirements": [
    {
      "name": "React 精通",
      "category": "硬技能",
      "weight": 5,
      "necessity": "必须",
      "note": "JD 首位要求，核心技术栈"
    },
    {
      "name": "TypeScript 熟悉",
      "category": "硬技能",
      "weight": 4,
      "necessity": "必须",
      "note": "现代前端标配"
    },
    {
      "name": "Node.js 经验",
      "category": "硬技能",
      "weight": 2,
      "necessity": "加分",
      "note": "加分项，非必需"
    }
  ]
}
```

**weight**: 1-5 (对应星级)
**necessity**: `"必须"` | `"重要"` | `"建议"` | `"加分"`

### 模块四：差距自评

```json
{
  "module_4_gap_assessment": [
    {
      "name": "React 精通",
      "self_score": 4,
      "priority": "P1"
    },
    {
      "name": "TypeScript 熟悉",
      "self_score": 2,
      "priority": "P0"
    }
  ]
}
```

**self_score**: 1-5
**priority**: `"P0"` | `"P1"` | `"P2"`
如果无自评数据，设为空数组 `[]`，报告将显示自评引导占位符。

### 模块五：面试考点预测

```json
{
  "module_5_interview_questions": [
    {
      "category": "技术栈深挖",
      "question": "React Hooks 与 Class 组件的本质区别是什么？useEffect 的 cleanup 机制如何工作？",
      "probability": 3
    },
    {
      "category": "项目经验追问",
      "question": "介绍一个你主导的前端架构升级项目，遇到了什么挑战？",
      "probability": 3
    },
    {
      "category": "行为面试",
      "question": "描述一次你与后端工程师在接口设计上产生分歧的经历，你是如何解决的？",
      "probability": 2
    }
  ],
  "module_5_reverse_questions": [
    "团队目前的技术栈和未来演进方向是怎样的？",
    "这个岗位的典型一天是什么样子的？",
    "公司对工程师的成长路径和晋升机制是怎样的？"
  ]
}
```

**probability**: 1-3 (对应 ★/★★/★★★)
**category**: 常见分类 — `"技术栈深挖"` | `"项目经验追问"` | `"行为面试"` | `"系统设计"` | `"案例分析"` | `"其他"`

### 模块六：学习路线图

```json
{
  "module_6_learning_roadmap": [
    {
      "phase": 1,
      "title": "TypeScript 系统学习",
      "duration": "2周",
      "items": [
        "完成 TypeScript 官方 Handbook",
        "练习泛型与高级类型编程",
        "在个人项目中全面迁移到 TS"
      ],
      "projects": "将一个 React 项目从 JS 迁移到 TS 并实现严格模式"
    },
    {
      "phase": 2,
      "title": "React 性能优化深入",
      "duration": "3周",
      "items": [
        "学习 React Profiler 和性能分析工具",
        "掌握 useMemo/useCallback/React.memo 最佳实践",
        "了解 React 18 并发特性"
      ],
      "projects": "优化现有项目的首屏加载时间和交互响应速度"
    }
  ]
}
```

### 模块七：ATS 关键词

```json
{
  "module_7_ats_keywords": {
    "技术关键词": ["React", "TypeScript", "Webpack", "微前端", "性能优化"],
    "业务关键词": ["SaaS", "B端产品", "数据可视化"],
    "软技能关键词": ["跨部门协作", "技术方案设计", "code review"],
    "行动动词": ["主导", "设计", "优化", "搭建", "重构"]
  },
  "module_7_integration_tips": [
    "React 和 TypeScript 必须原样出现在技能列表和项目描述中",
    "在项目描述中使用「主导」「设计」等行动动词开头",
    "将微前端相关经验放在项目经历的前三条中"
  ]
}
```

### 模块八：薪资对标（可选）

```json
{
  "module_8_salary_benchmark": {
    "jd_salary": "30K-50K·15薪",
    "market_range": "25K-45K·14薪 (北京 3-5年 前端)",
    "negotiation_range": "35K-45K·15薪",
    "by_city": [
      {"city": "北京", "range": "25K-45K"},
      {"city": "上海", "range": "23K-42K"},
      {"city": "深圳", "range": "22K-40K"},
      {"city": "杭州", "range": "20K-38K"}
    ],
    "strategy": "JD 标注 30K-50K，范围较宽，实际中间值约 40K 左右。建议在 HR 面时询问薪资结构和年终奖发放规则，技术面表现优异可争取上限。"
  }
}
```

如果不需要此模块，设为 `null`。
