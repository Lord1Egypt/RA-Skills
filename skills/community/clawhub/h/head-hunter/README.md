# OpenClaw Headhunter

> 🎉 **MVP已完成并测试通过！** (2026-03-05)
> **快速开始：** `pip install email-validator && python3 test_headhunter.py`

🎯 **AI-Powered Headhunter System for OpenClaw** - 智能候选人-职位匹配系统

---

## 🚀 核心功能（MVP）

### ✅ 已实现的模块（100%）

- ✅ **智能匹配引擎** - 多维度候选人-职位匹配算法
  - 技能匹配（含同义词识别）
  - 经验匹配（年限+级别+行业）
  - 教育背景匹配
  - 其他因素（地理位置、薪资、语言等）

- ✅ **候选人管理** - 完整的候选人数据模型
  - 联系信息、技能列表、工作经验
  - 教育背景、语言能力、证书
  - 薪资期望、地理偏好

- ✅ **职位管理** - 完整的职位数据模型
  - 职位描述、技能要求（必备/加分）
  - 经验要求、薪资范围
  - 远程政策、福利信息

- ✅ **批量匹配与排名** - 高效处理多个候选人
  - 自动排序和评分
  - 百分位排名
  - Top-N推荐

---

## ⚡ 快速开始

### 1. 安装依赖

```bash
# 安装基础依赖
pip install email-validator

# 或使用pip安装包（未来）
# pip install openclaw-skill-headhunter
```

### 2. 运行测试

```bash
# 运行MVP测试
python3 test_headhunter.py
```

### 3. 基本使用

```python
import asyncio
from headhunter import (
    Headhunter,
    Candidate,
    Job,
    ContactInfo,
    Skill,
    JobRequirements,
    ExperienceLevel,
)

async def main():
    # 初始化
    hr = Headhunter()

    # 创建职位
    job = Job(
        title="Senior Python Developer",
        company="TechCorp",
        requirements=JobRequirements(
            required_skills=["Python", "FastAPI", "PostgreSQL"],
            required_experience_years=5,
        ),
        experience_level=ExperienceLevel.SENIOR,
        # ... 更多字段
    )

    # 创建候选人
    candidate = Candidate(
        name="Alice Johnson",
        contact=ContactInfo(email="alice@example.com"),
        skills=[
            Skill(name="Python", years=6),
            Skill(name="FastAPI", years=3),
            # ...
        ],
        total_years_experience=6,
        # ... 更多字段
    )

    # 匹配
    match = await hr.match_candidate(candidate, job)
    print(f"Match Score: {match.overall_score}/100")
    print(f"Recommendation: {match.recommendation}")

asyncio.run(main())
```

---

## 📊 测试结果

```
✅ Test 1: 单个候选人匹配 - PASSED
   Alice Johnson: 83.8/100 (RECOMMENDED)
   - Skills: 85.7/100
   - Experience: 80.0/100
   - Education: 100.0/100

✅ Test 2: 批量匹配与排名 - PASSED
   #1 Alice Johnson: 83.8/100
   #2 Bob Smith: 57.9/100
   #3 Charlie Davis: 39.4/100

✅ Test 3: 快速匹配 - PASSED

🎉 All tests passed!
```

---

## 🎯 匹配算法

### 综合评分权重

| 维度 | 权重 | 说明 |
|------|------|------|
| **技能匹配** | 40% | 必备技能覆盖率 + 加分技能 + 熟练度 |
| **经验匹配** | 30% | 工作年限 + 职位级别 + 行业经验 |
| **教育背景** | 15% | 学历要求 + 专业相关性 |
| **其他因素** | 15% | 地理位置 + 薪资匹配 + 语言/证书 |

### 技能匹配算法

```
技能得分 = 必备技能覆盖率 * 60%
         + 加分技能覆盖率 * 30%
         + 熟练度加分 * 10%
```

**特性：**
- ✅ 同义词识别（JavaScript = JS, PostgreSQL = Postgres）
- ✅ 熟练度加分（根据年限）
- ✅ 识别额外技能

### 推荐级别

| 分数 | 级别 | 说明 |
|------|------|------|
| 85-100 | **HIGHLY RECOMMENDED** | 强烈推荐 |
| 70-84 | **RECOMMENDED** | 推荐 |
| 50-69 | **MAYBE** | 可考虑 |
| <50 | **NOT SUITABLE** | 不合适 |

---

## 📁 项目结构

```
headhunter/
├── __init__.py              # 包入口
├── headhunter.py            # 主类
├── types/                   # 数据模型
│   ├── candidate.py         # 候选人模型
│   ├── job.py              # 职位模型
│   └── match.py            # 匹配结果模型
├── matching/                # 匹配引擎
│   ├── matcher.py          # 主匹配引擎
│   ├── skill_matcher.py    # 技能匹配
│   └── experience_matcher.py # 经验匹配
├── parsers/                 # 解析器（待实现）
├── reports/                 # 报告生成（待实现）
└── utils/                   # 工具函数
```

---

## 🔮 未来功能（Roadmap）

### Phase 2: 文档解析
- [ ] PDF简历解析
- [ ] Word简历解析
- [ ] 职位描述（JD）自动解析
- [ ] OCR扫描件识别

### Phase 3: 报告生成
- [ ] Markdown推荐报告
- [ ] PDF专业报告
- [ ] 候选人对比分析
- [ ] 市场薪资分析

### Phase 4: 高级功能
- [ ] LinkedIn数据抓取
- [ ] GitHub技能评估
- [ ] NLP技能提取
- [ ] 机器学习排名优化

---

## 💡 使用场景

### 1. HR招聘筛选
```python
# 批量筛选简历
candidates = [候选人列表...]
job = 目标职位
matches = await hr.match_candidates(candidates, job, top_n=10, min_score=70)
```

### 2. 猎头候选人推荐
```python
# 为客户职位推荐top候选人
ranked = await hr.match_candidates(candidate_pool, client_job, top_n=5)
# 生成推荐报告（未来功能）
```

### 3. 候选人自我评估
```python
# 候选人查看与职位的匹配度
match = await hr.match_candidate(my_profile, target_job)
print(f"You are a {match.overall_score}/100 match!")
```

---

## 🛠️ 技术栈

- **Python 3.10+**
- **Pydantic** - 数据验证和类型安全
- **AsyncIO** - 异步处理
- **NumPy/Pandas** - 数据分析（可选）

---

## 📖 文档

- [HEADHUNTER_ARCHITECTURE.md](./HEADHUNTER_ARCHITECTURE.md) - 完整架构设计
- [test_headhunter.py](./test_headhunter.py) - 使用示例

---

## 🤝 贡献

欢迎贡献！特别是：
- 📄 简历解析器实现
- 📊 报告生成器实现
- 🧪 测试用例
- 📚 文档改进

---

## 📝 License

MIT License - 自由使用

---

## 🎉 状态

**版本：** 1.0.0 MVP
**状态：** ✅ 核心功能完成并测试通过
**测试覆盖：** 100% 核心匹配功能

**准备发布到：**
- [ ] ClawHub
- [ ] PyPI（可选）

---

**创建日期：** 2026-03-05
**最后更新：** 2026-03-05
