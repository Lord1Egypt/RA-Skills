# 数据模型参考

## 核心实体

### 学生 (Student)
```
studentId       string   # 学号
name            string   # 姓名
grade           int      # 年级 (1-9)
classId         string   # 班级ID
enrolledSubjects []string # 就读学科列表
```

### 班级 (Class)
```
classId         string
grade           int
className       string    # 如"三年级二班"
headTeacher     string    # 班主任教师ID
subjectTeachers map[string]string  # {科目: 教师ID}
```

### 学科 (Subject)
```
subjectId       string    # 如 "math", "chinese", "english"
subjectName     string    # 科目名称
gradeLevel      int       # 适用年级
knowledgePoints []KP      # 该学科包含的知识点列表
```

### 知识点 (KnowledgePoint)
```
kpId            string    # 知识点ID，如 "math-g3-01"
kpName          string    # 知识点名称，如 "两位数加减法"
subjectId       string    # 所属学科
parentId        string    # 父知识点ID（用于层次结构）
level           int       # 层级深度
weight          float     # 在学科中的权重 (0-1)
tags            []string  # 标签，如 ["计算", "基础"]
```

### 作业记录 (HomeworkRecord)
```
recordId        string    # 记录ID
studentId       string
subjectId       string
classId         string
submitTime      datetime
questions       []QuestionResult
totalScore      float
fullScore       float
accuracy        float     # 正确率 (0-1)
teacherNote     string    # 教师备注（可选）
```

### 题目结果 (QuestionResult)
```
questionId      string
questionType    string    # choice | fill-blank | short-answer | essay
correct         bool
score           float
fullScore       float
errorType       string    # concept | calculation | carelessness | expression | other
relatedKps      []string  # 关联的知识点ID列表
aiHint          string    # 自动生成的提示（错在哪、思路引导）
teacherComment  string    # 教师批注（可选）
```

## 掌握度计算

掌握度 = 该知识点关联题目的加权正确率

```
KP_mastery(student, kp) = Σ(question_score * weight) / Σ(question_fullScore * weight)
```

分级标准：
- ≥ 80% — **掌握 (Mastered)**
- 60%-80% — **需巩固 (Needs Review)**
- < 60% — **薄弱 (Weak)**
