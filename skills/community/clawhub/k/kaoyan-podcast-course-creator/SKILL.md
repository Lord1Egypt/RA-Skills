---
name: "kaoyan-podcast-course-creator"
description: "大学数学智慧课程全流程：五维设计→五场景→四阶段→质量审计，含弹题/题型扩展/部署"
---

# 大学数学智慧课程全流程制作指南

> 代老师 × 小墨 · v4.0 · 从考研播课到大学数学智慧课堂
> 核心原则：结构化优先、渐进增强、审计自动化、教师可控

---

## 一、课程架构：五级粒度模型

### 知识粒度
```
课程 (Course) → 章 (Chapter) → 节 (Section) → 知识点 (Keypoint) → 卡片/练习 (Card/Quiz)
```

| 粒度 | 示例 | 可做的智能操作 |
|------|------|-------------|
| 课程 | 高等数学 | 跨课程知识图谱关联 |
| 章 | 无穷级数 | 学习进度追踪、章末综合诊断 |
| 节 | 幂级数 | 课前预习推送、课后作业布置 |
| 知识点 | 阿贝尔定理 | 精准搜索、关联推荐、错题溯源 |
| 卡片 | 定理条件/结论/反例 | 闪卡复习、公式速查、AI答疑引用 |
| 练习题 | 收敛半径计算 | 形成性评价、自适应推题、错因分析 |

### 范围
- 高等数学（上/下，11学分）
- 线性代数（3-4学分）
- 概率论与数理统计（3-4学分）
- 考研强化复习（一稿两用）

---

## 二、数据模板

### 每节数据文件结构（完整 schema）
```javascript
window.EP_DATA = {
  id: "ch08_s03", title: "幂级数", subtitle: "阿贝尔定理与收敛半径",
  course: "高等数学", chapter: "无穷级数", section: "幂级数",
  textbook: "同济七版·下册·第十一章第三节",
  audioFile: "podcast_ch08_s03.mp3",
  totalDuration: 2700,
  segments: [ /* {speaker, text, start, end} */ ],
  chapters: [ /* {title, start, cls, icon} */ ],
  keypoints: [ /* {id, title, formulas, textbookRef, prerequisites, crossRefs} */ ],
  methodTree: { root: "...", children: [ /* {name, when} */ ] },
  sceneColors: ["#...", "#...", "#...", "#..."],
  cards: [ /* {icon, title, tag, label, body} */ ],
  cardMap: [ /* {cardIdx, segIndices} */ ],
  formulaMap: [ /* {r, v, sub} */ ],
  quizzes: [ /* {type, q, options?, ans?, hints?, cardId?, triggerTime?} */ ],
  teachingFlow: { /* 教学场景标注 */ }
};
```

---

## 三、题型设计（6种）

| 题型 | type | 数据字段 | 弹出 UI | 检查方式 |
|------|------|---------|---------|---------|
| 选择题 | `choice` | `options:[...], ans:N` | 点击选项 | `ans === 选择索引` |
| 简答题 | `text` | `a:"答案"` | 文本框 | fuzzyMatch |
| 判断题 | `tf` | `ans:'T'/'F'` | ✅正确/❌错误 | 精确匹配 |
| 填空题 | `fill` | `ans:"单空"` 或 `ans:[...,...]` | 输入框替换 `___` | fuzzyMatch（支持多空） |
| 判断改错 | `judge` | `ans:bool, correction:"..."` | 判断+改错框 | 两级检查 |
| 证明题 | `proof` | `rubric:"采分点1\|2\|3"` | AI辅助评分 | 人工审阅+AI |

### 分层提示（3层）
```
hints: ["概念提示 → 检查定义条件",
        "方法提示 → 尝试比值审敛法",
        "步骤提示 → 先求极限 lim|a_{n+1}/a_n|"]
```
系统记录提示使用层级 → 判断题目难度与学生掌握程度。

---

## 四、五大教学场景

1. **课前预习**：推送 segments[0:1] + 前测题 + 前置知识检查
2. **课堂教学（7环节）**：引入→讲授→例题→归纳→练习→总结→作业
3. **课后复习**：错题重做 + 关联卡片 + 自适应推题
4. **阶段诊断**：章末热力图 + 个人/班级报告
5. **跨课程关联**：知识点图谱连接高数/线代/概率

---

## 五、弹题弹出系统（核心）

### 播放器弹题流程
```
timeupdate/setInterval → checkQuizTriggers(t)
  → 匹配 triggerTime ± 2.0s
  → shouldTriggerQuiz(epId, qi) 检查是否已触发
  → triggerQuizPopup(i, q) → 显示底部弹出窗口
  → markQuizTriggered + audio.pause()
```

### 关键参数
- **触发容差**: 2.0s（避免 audio.currentTime 跳过窗口）
- **轮询间隔**: 250ms（setInterval 独立于 timeupdate 事件）
- **触发持久化**: localStorage `popup_triggered_{id}` 避免重复弹题

### 调试手段
| 工具 | 用法 |
|------|------|
| `?reset_q=1` | URL参数清除触发记录 |
| `forceFirstQuiz()` | Console手动触发首题 |
| `toggleQuizDebug()` | 底部调试状态栏 |
| `[Quiz]` 日志 | checkQuizTriggers实时检查 |
| `[QuizPopup]` 日志 | popup显示确认 |

### 已知陷阱
1. **onTimeUpdate异常中断**：CARD_MAP.find()空指针、new RegExp(fm.r)非法正则 → 全部 try-catch
2. **`\(` 转义地狱**：`new RegExp('\\(')` 在V8中开启捕获组 → 用 `\x28` 或 `[(]`
3. **loadTriggeredState()** 必须在 `EP_CURRENT = D` 之后调用
4. **MathJax跳过 display:none**：展开时需手动 `typeset(el)`
5. **容差太窄**：0.5s → 2.0s，轮询 500ms → 250ms

---

## 六、题库扩展机制

### 三层题库系统
```
quiz-bank.js                # 基础题库（11专题，100+题）
quiz-bank-expansion-2.js    # 扩展卷一（计算+证明，追加100+题）
quiz-bank-expansion-3.js    # 扩展卷二（判断+填空，追加44题）
```

### 加载顺序
```html
<script src="quiz-bank.js"></script>
<script src="quiz-bank-expansion-2.js"></script>
<script src="quiz-bank-expansion-3.js"></script>
<script src="quiz-widget.js"></script>
```

### 新增一节题库
```javascript
B.t01 = B.t01.concat([
  { type: 'fill', q: '极限 $\\displaystyle\\lim_{x\\to 0}\\frac{\\sin x}{x}=$ ___',
    ans: '$1$', difficulty: 'basic',
    hint: '重要极限', lessonId: 't01-l1' },
  { type: 'tf', q: '可导一定连续。',
    ans: 'T', difficulty: 'basic',
    hint: '可导与连续的关系',
    explanation: '可导⇒连续，反之不成立。', lessonId: 't02-l1' }
]);
```

---

## 七、制作流程（8步）

### Step 1: 课程设计 → 设计稿
```markdown
# 第X章第Y节 设计稿
> 教材：同济七版 | 课时：45min | 前置：... | 易错：...
## 教学环节 & 交互设计
## 对话脚本
```

### Step 2: 提取分段 → segments JSON（含 speaker/timecode）
### Step 3: 生成音视频（edge-tts / NotebookLM / 教师录制）
### Step 4: 构建数据文件（generate_section.py + 手动编辑）
### Step 5: 弹题/交互系统（triggerTime + 分层提示 + 题型选择）
### Step 6: 验证 + 质量审计（`audit_course.js` 全量扫描）
### Step 7: 部署 + 学习数据接入（scp / deploy.py）
### Step 8: 回归测试（弹题触发 + quiz panel + 强制弹题）

---

## 八、技术选型

| 层级 | 技术 | 理由 |
|------|------|------|
| 前端 | 原生JS | 播放器性能优先 |
| 数据 | IndexedDB + localStorage | 离线+触发状态 |
| 公式 | MathJax 3 (tex-chtml) | 成熟LaTeX渲染 |
| 可视化 | Canvas 2D + D3.js | 粒子场景+知识图谱 |
| 部署 | Nginx + SCP | 简单可靠 |
| AI | LLM API | 出题/答疑/分析 |

---

## 九、工具链

| 脚本 | 用途 |
|------|------|
| `generate_section.py` | segments → 完整数据文件 |
| `audit_course.js` | 全课程审计（TT/正则/KP/卡片/编码） |
| `fix_missing_triggers.js` | 批量补 triggerTime |
| `fix_formula_regex.js` | 修复 `\(` 转义 |
| `build_knowledge_graph.py` | 生成跨课程知识图谱 |
| `deploy.py` | 自动化部署 |

### 部署命令
```bash
scp -B -i ~/.ssh/deploy_ode_course player-data/eXX.js root@host:/www/wwwroot/moodle/ode-course/player-data/
scp -B -i ~/.ssh/deploy_ode_course podcast_video_v4.html root@host:/www/wwwroot/moodle/ode-course/
scp -B -i ~/.ssh/deploy_ode_course quiz-bank-expansion-3.js root@host:/www/wwwroot/moodle/
# 验证部署
curl -s -o /dev/null -w "%{http_code}" "http://host/ode-course/podcast_video_v4.html?ep=E01&reset_q=1"
```

---

## 十、快速新增一节

```bash
vim chX_sY_design.md                    # 1. 设计稿
python extract_segments.py > segs.json  # 2. 提取 segments
python generate_section.py              # 3. 构建数据
node --check player-data/chX_sY.js      # 4. 语法验证
node audit_course.js                    # 5. 全量审计
scp -B -i key player-data/chX_sY.js     # 6. 部署
# 浏览器打开 ?ep=EXX 测试弹题触发         # 7. 回归测试
```

---

## 十一、风险与对策

| 风险 | 对策 |
|------|------|
| 结构化数据工作量大 | 生成脚本 + AI辅助初稿 |
| 公式正则转义 | audit自动检测 + 批量修复 |
| 音频文件匹配度 | 测试 triggerTime 在 totalDuration 范围内 |
| AI生成不稳定 | 强制标注AI来源 + 人工审核 |
| 教师使用门槛高 | 设计稿模板 + 一键生成 + 培训 |

---

## 十二、里程碑

| 节点 | 交付标准 |
|------|---------|
| M1: 单章Demo | 数据完整 + 弹题触发 + 审计0warn |
| M2: 教学平台 | 6种题型 + 错题本 + 学习看板 |
| M3: 知识图谱 | 三门课图谱 + 诊断推荐 |
| M4: AI增强 | 出题/答疑/分析可用 |
| M5: 全课程 | 全部章节数据完成 |
