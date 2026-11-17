# headhunter-pro WorkBuddy Skill

AI 驱动的端到端招聘工作流 — 猎头候选人筛选、推荐报告、触达话术、面试评估、客户管理、入职护航

**版本：** 28.0.0  
**格式：** WorkBuddy Skill Package  
**来源：** headhunter-pro 发布线（v27.0 起以 WorkBuddy 12 阶段架构为主线）

---

## 适用场景

| 场景 | 说明 |
|---|---|
| 简历筛选 | 基于 JD 对候选人进行 9+1 维度评分和推荐判断 |
| 推荐报告 | 生成五段式深度推荐报告（非简历罗列） |
| 触达话术 | 生成个性化冷/暖触达消息，支持三分法策略 |
| 面试评估 | BEI/STAR 框架面试评估 + 情景模拟设计 |
| 客户管理 | 四阶段客户维护流程 + Talent Gap Analysis |
| 人才地图 | 三合一能力模型人才地图 + 季度更新 |

## 快速开始

### 输入格式

```json
{
  "task_type": "resume_screen",
  "candidate_info": {
    "name": "候选人姓名",
    "experience_years": 8,
    "current_company": "当前公司",
    "current_title": "当前职位",
    "education": "教育背景",
    "key_skills": ["技能1", "技能2"]
  },
  "job_description": "职位描述文本",
  "industry": "医疗"
}
```

### task_type 枚举

- `resume_screen` — 简历筛选
- `write_recommendation` — 写推荐报告
- `generate_outreach` — 生成触达话术
- `interview_assess` — 面试评估
- `client_manage` — 客户管理
- `talent_mapping` — 人才地图

### 输出示例

参见 `fixtures/normal_case/expected-output.md`

## 目录结构

```
headhunter-pro-workbuddy/
├── skill.yml                      # 核心配置：输入/输出契约、权限边界
├── README.md                      # 使用说明
├── implementation/
│   └── prompt-template.md         # 核心可执行指令（路由、评分、报告结构等）
├── references/
│   ├── nine-dimension.md          # 9+1 维度评分标准表 + 评分规则
│   ├── outreach-scripts.md        # 触达话术库（冷/暖/跟进/中间阶层）
│   ├── pipeline-states.md         # Pipeline 状态机 + SLA + 转化率基准
│   └── onboarding-silver-medalist.md # 6 个月融合支持 + 回访话术 + 风险预警
├── fixtures/
│   ├── normal_case/               # 正常输入 → 期望输出
│   ├── missing_input/             # 缺失输入 → 期望行为（请求补充）
│   └── conflicting_input/         # 冲突输入 → 期望行为（低评分+不推荐）
└── CHANGELOG.md                   # 版本历史
```

## 已知限制

- 无法访问外部招聘平台（LinkedIn/猎聘/Boss直聘）的实时数据
- 候选人联系方式需由用户手动提供
- 行业趋势数据需联网搜索支持
- 背调需人工执行，AI 仅提供检查清单

## 权限边界

- **文件读访问：** `workspace/candidates/**`, `workspace/memory/*.md`
- **文件写访问：** `workspace/candidates/*/profile.md`, `workspace/candidates/*/recommendation.md`
- **外部 API：** 无
- **连接器：** 无

## 版本历史

详见 `CHANGELOG.md`
