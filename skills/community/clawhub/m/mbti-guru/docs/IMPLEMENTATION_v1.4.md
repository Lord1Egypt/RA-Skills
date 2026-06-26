# MBTI Guru v1.4 详细更新迭代方案

---

## 一、当前进度

### 已完成 ✅
| 功能 | 状态 | 说明 |
|------|------|------|
| 题库系统 | ✅ | 160题（EI/SN/TF/JP各40题） |
| 随机抽取 | ✅ | 每次测试随机抽题，保证多样性 |
| PDF第二页 | ✅ | 认知功能+成长建议+职场人际+情侣匹配 |

### 进行中 🔄
| 功能 | 状态 | 说明 |
|------|------|------|
| 进度保存 | 🔄 | session.py 已创建 |
| 历史记录 | 🔄 | history.py 已创建 |
| 实时反馈 | ⏳ | 待实现 |
| 进度条 | ⏳ | 待实现 |

### 待开始 ⏳
| 功能 | 说明 |
|------|------|
| 题库扩充至600+ | 每个维度100+题目 |
| 用户交互界面 | Telegram 交互优化 |

---

## 二、已完成功能详解

### 2.1 题库扩充系统

**现状：**
- 题库总量：160题
- 每维度题数：40题
- 抽取方式：每次随机抽取指定数量

**目标：**
- 题库总量：600+题
- 每维度题数：150+题
- 题库质量：去除模糊题、平衡难度

**代码结构：**
```python
# lib/question_pool.py
EI_QUESTIONS = [...]  # 40题
SN_QUESTIONS = [...]  # 40题
TF_QUESTIONS = [...]  # 40题
JP_QUESTIONS = [...]  # 40题

def sample_questions(version):
    # 随机抽取指定数量
    # 确保每次测试题目不同
```

### 2.2 PDF第二页内容

**已包含内容：**

1. **认知功能 (Cognitive Functions)**
   - 主功能 (Dominant)
   - 辅助功能 (Auxiliary)
   - 第三功能 (Tertiary)
   - 劣势功能 (Inferior)
   - 每个功能包含：名称、描述、优势

2. **成长建议 (Growth Suggestions)**
   - 4条个性化成长建议
   - 基于认知功能弱点制定

3. **职场人际 (Workplace Relationships)**
   - 最佳工作环境
   - 团队角色定位
   - 协作建议（4条）

4. **情侣匹配 (Relationship Compatibility)**
   - 最佳匹配类型
   - 挑战类型
   - 关系建议（3条）

---

## 三、待实现功能详解

### 3.1 进度保存/恢复

**实现方案：**
```python
# lib/session.py
def save_session(chat_id, version, current_index, answers):
    # 保存到 data/sessions/{chat_id}_{timestamp}.json
    
def load_session(session_id):
    # 恢复会话
    
def get_incomplete_session(chat_id):
    # 检查是否有未完成会话
```

**用户交互：**
```
用户：/start
Bot：检测到您有未完成的测试，是否继续？
用户：继续
Bot：（恢复测试）
```

### 3.2 历史记录

**实现方案：**
```python
# lib/history.py
def save_test_result(chat_id, type_code, scores, clarity):
    # 保存到 data/history/{chat_id}/tests.json
    
def get_test_history(chat_id, limit=10):
    # 获取最近N次测试
    
def compare_tests(test1, test2):
    # 对比两次测试结果
```

**用户交互：**
```
用户：/history
Bot：您的测试历史：
1. INFP - 2026-03-27
2. ENFP - 2026-03-26
3. INTJ - 2026-03-25
```

### 3.3 实时反馈

**实现方案：**
- 每完成10题，发送简要分析
- 基于已答题目，预测维度倾向

**用户交互：**
```
Bot：📊 已完成 10/70
   能量倾向：I (55%)
   信息倾向：N (60%)
   继续加油！
```

### 3.4 进度条

**实现方案：**
- Unicode 方块字符显示进度
- 每答一题更新

**显示效果：**
```
████████████░░░░░░░░░ 60% (42/70)
```

---

## 四、题库扩充计划

### 4.1 需要新增题目

| 维度 | 现有 | 目标 | 需新增 |
|------|------|------|--------|
| EI | 40 | 150 | 110 |
| SN | 40 | 150 | 110 |
| TF | 40 | 150 | 110 |
| JP | 40 | 150 | 110 |
| **总计** | 160 | **600** | **440** |

### 4.2 题目质量标准

- ✅ 双向陈述清晰
- ✅ 选项长度一致
- ✅ 无文化特定内容
- ✅ 难度适中（中低难度为主）
- ✅ 无双重否定
- ✅ 中英双语对照

---

## 五、技术架构

### 文件结构
```
mbti-guru/
├── lib/
│   ├── questions.py       # 兼容旧版本
│   ├── question_pool.py   # 新题库系统 (160题)
│   ├── scorer.py          # 评分系统
│   ├── mbti_types.py      # 类型数据库
│   ├── cognitive.py       # 认知功能数据 ✅
│   ├── relationships.py   # 职场+情侣数据 ✅
│   ├── session.py         # 会话管理 ✅
│   ├── history.py         # 历史记录 ✅
│   ├── pdf_generator.py   # PDF双页生成 ✅
│   └── reports.py         # 终端报告
├── data/
│   ├── sessions/          # 进度保存 ⏳
│   └── history/           # 历史记录 ⏳
└── SKILL.md
```

### 数据流
```
用户答题 → session.py (保存进度) 
        → scorer.py (计算得分)
        → history.py (保存历史)
        → pdf_generator.py (生成报告)
        → Telegram (发送PDF)
```

---

## 六、测试计划

### 单元测试
- [ ] 题库随机抽取一致性
- [ ] 进度保存/恢复
- [ ] 历史记录读写
- [ ] PDF双页生成

### 集成测试
- [ ] 全流程测试（70/93/144/200题）
- [ ] 多用户并发测试
- [ ] PDF内容验证

---

## 七、发布计划

| 版本 | 内容 | 状态 |
|------|------|------|
| v1.4 | 用户体验 + 题库 + PDF第二页 | **测试中** |
| v1.4.1 | 修复已知问题 | 待定 |
| v1.5 | 深色模式 + 题库扩充完成 | 待定 |

---

_Last updated: 2026-03-27_
