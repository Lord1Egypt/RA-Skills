# pathway-score-guide-pro

一个面向 **专升本、保本、保研、考研、留学、读博、评职称** 的综合评分与指引 skill。

## 设计目标

这个 skill 不是“泛泛建议工具”，而是一个 **规则映射 + 综测评分 + 差距分析 + 材料清单 + 时间线** 的综合助手。

它适合这些场景：

- 我能不能专升本 / 保研 / 考研 / 读博？
- 按我学校 / 单位规则，我现在能打多少分？
- 我缺哪些硬门槛、竞争项、材料项？
- 我应该冲哪条路，保哪条路？
- 评职称到底看什么，论文 / 课题 / 资历哪个最关键？

## 能力边界

### 能做

- 读取用户上传的 **学校 / 单位正式文件** 并结构化成评分表
- 在没有本地文件时，基于 **国家政策 + 代表性院校 / 单位公开规则** 做保守估算
- 生成：
  - 资格核验
  - 综测评分
  - 差距分析
  - 材料清单
  - 时间线
  - 补强建议

### 不能保证

- 不能保证收录“所有学校 / 所有单位”的实时最新内部规则
- 不能替代学校、学院、单位、人事部门、研究生院的正式审核
- 不能承诺录取 / 通过 / 晋升结果

## 目录结构

```text
pathway-score-guide-pro/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── references/
├── resources/
├── scripts/
└── examples/
```

## 运行自检

```bash
python3 scripts/self_check.py .
```

## 示例评分

```bash
python3 scripts/score_engine.py \
  --scorecard resources/scorecards/baoyan.json \
  --profile examples/baoyan_profile_example.json
```

## 扩展方式

把你的学校 / 单位最新文件或规则结构化后放入：

- `resources/templates/`
- `resources/institution_registry_template.csv`

再用：

- `scripts/policy_normalizer.py`
- `scripts/score_engine.py`

做统一整理和估算评分。
