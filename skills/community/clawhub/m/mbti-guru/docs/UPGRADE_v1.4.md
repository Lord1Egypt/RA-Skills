# MBTI Guru v1.4-v1.5 升级方案

## 一、当前状态
- 版本: v1.0.3
- 题库: 200题/4版本，每个维度约50题
- PDF: 单页精简版
- 用户体验: 基础交互

---

## 二、v1.4 升级计划

### 2.1 用户体验模块 (Priority 1)

#### A. 进度保存
- **机制:** 用户中途退出可保存进度
- **存储:** `data/sessions/{user_id}_{timestamp}.json`
- **数据:** `{user_id, version, current_index, answers[], timestamp}`
- **恢复:** 下次启动检测未完成session，询问是否继续

#### B. 历史记录
- **存储:** `data/history/{user_id}/`
- **数据:** `{test_id, type_code, scores, clarity, version, date, answers_count}`
- **展示:** 最近10次测试，支持查看详情
- **对比:** 可选两个结果对比分析

#### C. 实时反馈
- **时机:** 每10题完成后显示简要分析
- **内容:** 当前维度倾向 + 剩余题数
- **方式:** Telegram消息推送

#### D. 进度条
- **显示:** `████████░░░░ 65% (65/100)`
- **更新:** 每答一题更新
- **格式:** Unicode方块 + 百分比 + 题数

---

### 2.2 题库扩充模块 (Priority 2)

#### A. 题库目标
| 维度 | 现有题数 | 目标题数 | 需新增 |
|------|---------|---------|--------|
| EI | ~50 | 150+ | ~100 |
| SN | ~50 | 150+ | ~100 |
| TF | ~50 | 150+ | ~100 |
| JP | ~50 | 150+ | ~100 |
| **总计** | ~200 | **600+** | **~400** |

#### B. 题库结构优化
```python
# 题目分级
question_pool = {
    "EI": {
        "E": [...],  # 偏向Extravert的题目
        "I": [...]   # 偏向Introvert的题目
    },
    ...
}

# 每次测试随机抽取，确保多样性
selected = random.sample(pool[dimension], 50)
```

#### C. 题目质量优化
- 去除双重否定题
- 去除文化特定题
- 平衡题目难度（中低难度为主）
- 确保选项长度一致

---

### 2.3 PDF第二页 (Priority 1)

#### 内容结构
```
┌─────────────────────────────────────────┐
│  Page 2: 深度分析 / Deep Analysis      │
├─────────────────────────────────────────┤
│                                         │
│  🧠 认知功能 / Cognitive Functions      │
│     - 主功能 / Auxiliary / Tertiary...   │
│                                         │
│  📈 成长建议 / Growth Suggestions       │
│     - 个人成长路径                       │
│     - 潜在优势发挥                       │
│                                         │
│  💼 职场人际 / Workplace Relationships │
│     - 最佳工作环境                       │
│     - 团队协作建议                       │
│                                         │
│  💕 情侣匹配 / Relationship Compatibility│
│     - 最佳匹配类型                       │
│     - 关系发展建议                       │
│                                         │
└─────────────────────────────────────────┘
```

---

## 三、v1.5 计划（待定）

### 3.1 PDF增强
- 添加深色模式选项（用户可选）
- 更多版式定制

### 3.2 数据分析
- 类型分布统计
- 变化趋势追踪

---

## 四、技术实现

### 文件结构
```
mbti-guru/
├── lib/
│   ├── questions.py      # 题库系统（含大题库）
│   ├── question_pool.py  # 600+题库（新增）
│   ├── scorer.py         # 评分系统
│   ├── mbti_types.py     # 类型数据库
│   ├── cognitive.py      # 认知功能数据（新增）
│   ├── growth.py         # 成长建议数据（新增）
│   ├── careers.py        # 职场人际数据（新增）
│   ├── relationships.py  # 情侣匹配数据（新增）
│   ├── session.py        # 会话管理（新增）
│   ├── history.py        # 历史记录（新增）
│   ├── pdf_generator.py  # PDF生成
│   └── reports.py        # 终端报告
├── data/
│   ├── sessions/         # 进度保存
│   └── history/          # 历史记录
└── SKILL.md
```

### 数据存储
- **会话:** JSON文件，`data/sessions/{chat_id}_{timestamp}.json`
- **历史:** JSON文件，`data/history/{chat_id}/tests.json`

---

## 五、版本计划

| 版本 | 内容 | 优先级 |
|------|------|--------|
| v1.4 | 用户体验 + 题库扩充 + PDF第二页 | 当前 |
| v1.5 | 深色模式 + 数据分析 | 待定 |

---

## 六、测试计划

- [ ] 进度保存/恢复测试
- [ ] 历史记录读写测试
- [ ] 600+题库随机抽取测试
- [ ] PDF双页生成测试
- [ ] 全流程用户测试

---

_Last updated: 2026-03-27_
