# /novel write - 执行章节写作

## 触发方式

```
/novel write [章节编号或任务ID]
```

或对话式:
```
请写第3章
继续写第3章
```

---

## ⚠️ 前置条件检查(强制)

**在开始写作前,必须确认以下步骤已完成**:

| 步骤 | 命令 | 产出文件 |
|------|------|---------|
| 1 | `/novel init` | 项目目录 + `.claude/` |
| 2 | `/novel constitution` | `memory/constitution.md` |
| 3 | `/novel specify` | `stories/*/specification.md` |
| 4 | `/novel clarify` | `stories/*/clarify-answers.md` |
| 5 | `/novel plan` | `stories/*/creative-plan.md` |
| 6 | `/novel timeline` | `stories/*/timeline.md` |
| 7 | `/novel track-init` | `spec/tracking/*.json`(填充追踪系统) |
| 8 | `/novel tasks` | `stories/*/tasks.md` + `stories/*/tasks-volume-*.md` |

**如果任何步骤未完成,禁止执行写作!**

### 强制检查逻辑

执行 `/novel write` 时,**必须**先运行以下检查:

```bash
# 检查前置文件是否存在
REQUIRED_FILES=(
  "memory/constitution.md"
  "stories/*/specification.md"
  "stories/*/clarify-answers.md"
  "stories/*/creative-plan.md"
  "stories/*/timeline.md"
  "stories/*/tasks.md"
)

# 检查 track-init 是否已运行(tracking JSON 必须存在且非空)
REQUIRED_DIRS=(
  "spec/tracking"
)

for f in "${REQUIRED_FILES[@]}"; do
  if ! ls $f &>/dev/null; then
    echo "❌ 错误:缺少前置文件或步骤未完成"
    echo ""
    echo "当前需要但缺失:$f"
    echo ""
    echo "请按顺序完成以下步骤:"
    echo "  1. /novel init [项目名]"
    echo "  2. /novel constitution"
    echo "  3. /novel specify"
    echo "  4. /novel clarify"
    echo "  5. /novel plan"
    echo "  6. /novel timeline"
    echo "  7. /novel track-init"
    echo "  8. /novel tasks"
    echo ""
    echo "必须全部完成后才能执行 /novel write"
    exit 1
  fi
done

# 检查 tracking 目录是否存在(track-init 验证)
for d in "${REQUIRED_DIRS[@]}"; do
  if [ ! -d "$d" ] || [ -z "$(ls -A $d/*.json 2>/dev/null)" ]; then
    echo "❌ 错误:追踪系统未初始化"
    echo "请先执行 /novel track-init"
    exit 1
  fi
done
```

**检查通过后**才会加载上下文并开始写作。

---

## 执行流程

### 1. 查询上下文(按优先级)

**先查(最高优先级)**:
- `memory/constitution.md` - 创作宪法
- `memory/style-reference.md` - 风格参考(如有)

**再查(规格和计划)**:
- `stories/*/specification.md` - 故事规格
- `stories/*/creative-plan.md` - 创作计划
- `stories/*/timeline.md` - 时间线(写作前必须对照)
- `stories/*/tasks.md` - 当前任务

**自动加载写作风格和规范**:
```yaml
# 检查 specification.md 的 YAML frontmatter
writing-style: natural-voice
writing-requirements:
  - anti-ai-v4
  - fast-paced
```
如配置了,加载对应文件:
- `.claude/knowledge-base/styles/natural-voice.md`
- `.claude/knowledge-base/requirements/anti-ai-v4.md`

**再查(状态和数据)**:
- `spec/tracking/character-state.json` - 角色状态
- `spec/tracking/relationships.json` - 关系网络
- `spec/tracking/plot-tracker.json` - 情节追踪
- `spec/tracking/validation-rules.json` - 验证规则

**再查(知识库)**:
- `spec/knowledge/` - 世界观、角色档案等
- `stories/*/content/` - 前文内容

**再查(写作规范)**:
- `memory/personal-voice.md` - 个人语料(如有)
- `spec/knowledge/natural-expression.md` - 自然化表达

**条件查询(前三章专用)**:
- 如果章节编号 ≤ 3 或总字数 < 10000字:
  - 读取 `spec/presets/golden-opening.md`(黄金开篇法则)

---

### 2. 选择写作任务

从 `tasks.md` 中选择状态为 `pending` 的任务,标记为 `in_progress`。

验证前置条件:
- 相关依赖任务是否完成
- 必要设定是否就绪
- 前序章节是否完成

---

### 3. 六阶段写作流程

**【阶段1】预写分析 → 【阶段2】初稿生成 → 【阶段3】自检 → 【阶段4】文笔润色 → 【阶段5】修订 → 【阶段6】元数据输出**

#### 阶段1:预写分析

读取并输出:
1. **本章时间点**:从 timeline.md 找到本章对应的事件
2. **本章任务**:tasks 中本章的任务描述
3. **角色状态**:character-state.json 中相关角色当前状态
4. **待揭晓伏笔**:plot-tracker.json 中状态为 foreshadowing 的伏笔
5. **前文摘要**:前1-2章的关键情节(防矛盾)
6. **记忆库**(.learnings/):检查与本章相关的角色/地点/情节记忆,确保新设定不遗忘

输出:
```
📋 预写分析：第X章
- 时间点：第X年X月 - 事件名称
- 核心任务：...
- 相关角色状态：...（标注关键变化）
- 本章需揭晓伏笔：F-XX / 无
- 继续埋设伏笔：F-XX（线索：...）
- 记忆库引用：.learnings/ 中相关记忆（如有）
- 前文摘要：...
```

---

#### 阶段2:初稿生成

基于阶段1的上下文,生成章节初稿。

**保存路径**:`stories/*/content/volumeX/chapter-XX-draft.md`

---


#### 阶段3:自检

对照阶段1的分析,逐项检查:

| 检查项 | 标准 | 未达标处理 |
|--------|------|-----------|
| 时间线一致性 | 事件顺序符合 timeline.md | 停止,修正 |
| 伏笔揭晓检测 | 应揭晓的伏笔正文有对应内容 | 停止,补全 |
| 角色一致性 | character-state.json 的状态无矛盾 | 停止,修正 |
| 前文连贯 | 与前1-2章情节衔接无断裂 | 停止,修正 |

**通过**:进入阶段4
**失败**:停在阶段3,输出具体问题,修正后重跑阶段2

---

#### 阶段4:文笔润色

按 `writing-style` 和 `writing-requirements` 调整:
- 替换 AI 高频禁用词
- 调整单句成段比例(30%-50%)
- 具象化抽象描写
- 标点符号规范

**保存路径**:`stories/*/content/volumeX/chapter-XX-polished.md`

---

#### 阶段5:修订

阅读润色后正文,做最终检查:
- 节奏是否流畅
- 对话是否自然
- 有无冗余重复
- 章末钩子是否有效

如有问题直接修改。

---

#### 阶段6:元数据输出

- **重命名**:`chapter-XX-draft.md` 和 `chapter-XX-polished.md` 删除中间文件,只保留最终版 `chapter-XX.md`
- **更新 tracking**:
  - character-state.json(角色状态变化)
  - plot-tracker.json(伏笔揭晓更新)
  - progress.json(字数、章节进度)
- **记录完成时间**


### 5. 写作前提醒


**基于宪法原则**:
- 核心价值观要点
- 质量标准要求
- 风格一致性准则

**基于规格要求**:
- P0 必须包含的元素
- 目标读者特征
- 内容红线提醒

**基于写作风格和规范(如已配置)**:

```
🎨 当前写作配置:
- 风格:natural-voice(自然人声)
  - 口语化优先,对话推动情节
  - 行为>心理,具体>抽象

- 规范:anti-ai-v4 + fast-paced
  - 200+禁用词,形容词限制
  - 每章至少2个爽点,节奏紧凑

组合效果:自然流畅的快节奏爽文
```

---

### 6. 分段格式规范

- ⛔ **禁止使用**:"一"、"二"、"三"等数字标记分段
- ✅ **使用方式**:场景转换时用两个空行分隔
- 📖 **原因**:数字标记过于生硬,破坏阅读沉浸感
- ⛔ **行间非必要不添加空行**:段落之间除非场景转换,否则不插空行

---

### 7. 反AI检测写作规范

**单句成段比例**:30%-50%的段落应为单句成段

**每段字数**:50-100字

**重点信息独立成段**

#### AI高频词黑名单

| ❌ 禁用 | ✅ 替换 |
|---------|---------|
| 唯一的 | 这个、那个 |
| 直到 | 一直到、直到...才 |
| 弥漫着 | 有股、飘着 |
| 摇摇欲坠的 | 旧的、快坏的 |
| 空气凝固 | 沉默、没人说话 |
| 话音未落 | 他话没说完 |
| 猛地 | 突然、一把 |
| 心中暗想 | 他想、寻思 |
| 皱起眉头 | 眉头一皱 |
| 叹了口气 | 叹了一声 |

#### 具象化原则

**时间抽象** ❌ → **具体化** ✅
- "最近" → "上周三"
- "很久以前" → "三年前的秋天"
- "过了一会儿" → "等了半个小时"

**人物抽象** ❌ → **具体化** ✅
- "很多人" → "村里人都"
- "有人说" → "隔壁老王说"

**数量抽象** ❌ → **具体化** ✅
- "效果很好" → "多收了三石粮"
- "很贵" → "一顿饭花了三百块"

---

### 8. 章节结构

```
### 开场
- 吸引读者
- 承接前文
- 建立氛围

### 发展
- 推进情节
- 深化人物
- 埋设伏笔

### 转折
- 制造冲突或悬念
- 打破预期

### 收尾
- 适当收束
- 章末钩子(引出下一章)
```

---

### 9. 保存和更新

- 章节内容保存到 `stories/*/content/volumeX/chapter-XX.md`
- **必须等第8步全部检查通过后**才更新任务状态为 `completed`
- 记录完成时间和字数
- ⚠️ **章节正文内不得包含质量追踪结果、分析报告等元数据**,只输出纯小说内容

---

### 10. 完成后行动(强制检查)

**必须按顺序执行,全部通过才算章节完成。任一失败则章节标记为未完成,阻断后续写作。**

#### 8.1 字数验证

```bash
bash <skill>/scripts/bash/count-chinese-words.sh <文件路径>
```

**字数要求**:通常 2000-4000字(来自 `spec/tracking/validation-rules.json`)

**失败处理**:字数不符合要求 → 阻断 → 提示用户修改章节内容 → 重跑 `/novel write`

#### 8.2 追踪验证(每章强制)

**after_each_chapter**:
```
/novel track --check
```

**检查内容**:角色一致性、情节进度、线索推进

**失败处理**:
```
❌ 追踪验证失败:角色"林晚"人设前后不一致
   - 第2章设定她"性格内向"
   - 第3章却写她"主动搭话陌生人"

请修复后再执行 /novel write 第3章
```

**通过条件**:角色状态一致、情节逻辑连贯、线索推进正确

#### 8.3 质量分析(每5章强制)

**every_5_chapters**(当完成章节数是5的倍数时):
```
/novel analyze
```

**检查内容**:一致性、节奏、视角、对话质量

**失败处理**:
```
❌ 质量分析失败:
   - 第2章节奏偏慢(建议删除冗余描写)
   - 第4章对话比例过高(占65%,建议≤50%)
   - 第3章出现未预期情节转折

请修复后再执行 /novel write 第5章
```

**通过条件**:节奏达标、无重大质量问题、符合规格要求

#### 检查流程图

```
章节写作完成
    ↓
字数验证 → ❌ 失败 → 阻断 → 提示修改
    ↓ 通过
追踪验证 → ❌ 失败 → 阻断 → 提示修复
    ↓ 通过
伏笔回收检查 → ❌ 失败 → 阻断 → 提示修复
    ↓ 通过
5章倍数? → 是 → 质量分析 → ❌ 失败 → 阻断 → 提示修复
    ↓ 通过(或直接继续)
    ↓
✅ 章节完成 → 更新任务状态为 completed
```

---

### 11. 输出完成报告

```
✅ 章节写作完成

📄 已保存:stories/她是我唯一的异常值/content/volume1/chapter-03.md
📊 实际字数:3,256字
📊 字数要求:3,000-3,500字
📊 字数状态:✅ 符合要求

🔍 强制检查:
   1. 字数验证 → ✅ 通过
   2. 追踪验证 → ✅ 通过
      - 角色一致性:✅
      - 情节进度:✅
      - 线索推进:✅
   3. 伏笔回收检查 → ✅ 通过
      - F-01 已揭晓 → resolved
      - F-03 继续埋设

📦 任务状态:✅ 已更新为 completed

📌 提醒:第3章不是5的倍数,跳过质量分析
   (每5章需执行 /novel analyze)
```

**每5章提醒**(章节编号 % 5 == 0 时输出):

```
📌 第5章完成!

   🔍 质量分析提醒:
      - 已完成章节数:5(5的倍数)
      - 建议执行 /novel analyze 进行质量分析
      - 分析通过后才能继续写作

   请执行:/novel analyze
```

---

## 与七步方法论的关系

```
/novel constitution → 提供创作原则
         ↓
/novel specify → 定义故事需求
         ↓
/novel clarify → 澄清关键决策
         ↓
/novel plan → 制定技术方案
         ↓
/novel tasks → 分解执行任务
         ↓
/novel write → 【当前】执行写作
         ↓
/novel analyze → 验证质量一致
```

**写作是执行层,要严格遵循上层的规格和计划。**
