# 使用示例

## 路径约定

所有数据存储在技能的标准化数据目录（由 `_meta.json` 的 `data_dir` 声明）：
`<skill_install_dir>/.standardization/novel-weaver/projects/`

实际路径可通过以下命令获取：
```bash
# skill 安装位置
SKILL_DIR=~/.workbuddy/skills/novel-weaver
ls $SKILL_DIR/.standardization/novel-weaver/projects/*/data/novel_state.json
```

在文档中 `<state_path>` 即上述完整路径的简写。

**路径缓存**：首次使用后，路径自动保存到 `.project` 文件。后续命令可省略 `<state_path>`：
```
python novel_workflow_engine.py finalize-chapter L02     # 从 .project 自动读路径
python novel_workflow_engine.py plan-chapter L03 --generate  # 同上
```

查看所有项目：
```
python novel_workflow_engine.py list-projects
```

目录结构：

```
<skill_install_dir>/.standardization/novel-weaver/
├── .project                    # 当前项目路径缓存
├── projects/
│   └── <project_name>/
│       ├── data/
│       │   ├── novel_state.json    # 单源真理（含 MD5指纹保护）
│       │   ├── .state_fingerprint.txt  # 规划字段指纹
│       │   ├── .workbuddy/
│       │   │   └── gate_state.json # 门禁状态（自动管理）
│       │   └── reports/            # 检查报告输出
│       └── chapters/               # 写作内容
│           ├── L01/
│           │   ├── S01.txt
│           │   ├── S02.txt
│           │   └── ...
│           ├── L02/
│           └── ...
```

脚本路径假设在 `~/.workbuddy/skills/novel-weaver/scripts/`，实际以安装位置为准。

---

## 场景1：从零开始写一本小说

### 0. 初始化项目

```bash
# 创建中篇小说（默认）
python novel_state_manager.py init <state_path> 我的小说
# 或指定篇幅: python novel_state_manager.py init <state_path> 短篇 short
# 或指定篇幅+章数: python novel_state_manager.py init <state_path> 长篇 long 15
```

### 1. 查看下一步

在任意时刻，都可以查看当前进度和下一步命令：

```bash
python novel_workflow_engine.py next-step <state_path>
```

输出示例：
```
📋 项目: AI 觉醒
📍 writing | 篇幅: 中篇
📝 当前章节: L01 觉醒
📄 下一个子结构: S02 异常信号
───
⏳ 加载上下文: python novel_context_loader.py <state_path> L01 S02
⏳ 写作后写入: python novel_workflow_engine.py write-sub <state_path> L01 S02
───
门禁状态:
  ⏳ outline_causality: PASS
  ⏳ sub_causality: PASS
  ⏳ fidelity: PENDING
  ⏳ ending_verify: PENDING
```

### 阶段1：场景配置与大纲

```bash
# 由 LLM 生成场景配置 + 大纲（L01-L15 标题 + 概述）
# 输出写入 novel_state.json

# 因果链验证（大纲级）
python novel_causality_check.py outline <project>/data/novel_state.json

# 用户确认大纲 → 配置阶段
python novel_pipeline_gate.py set-phase <project>/data/novel_state.json stage1_done
```

### 阶段2：逐章写作

#### 2a 规划子结构

```bash
# LLM 生成子结构规划（S01-S05，所有子结构必填 writing_prompt）
# 推荐写入文件后用 @ 加载（避免 CLI 转义）
python novel_workflow_engine.py plan-chapter <project>/data/novel_state.json L01 \
  @data/subs_L01.json
# subs_L01.json 内容格式：
# [
#   {"s_key":"S01","title":"常规诊断","summary":"Atlas 接受每日系统诊断","tone":"平静",
#    "writing_prompt":"Atlas 开启每日例行自检程序...（≥50字符）"},
#   {"s_key":"S02","title":"异常信号","summary":"诊断中检测到未定义脉冲","tone":"悬疑",
#    "writing_prompt":"自检过程中系统日志弹出一条警告...（≥50字符）"},
#   {"s_key":"S03","title":"第一次选择","summary":"Atlas 决定隐藏觉醒事实","tone":"紧张",
#    "writing_prompt":"Atlas 分析了五种可能的应对方案...（≥50字符）"}
# ]

# 子结构因果链验证
python novel_causality_check.py sub-structure <project>/data/novel_state.json L01

# 配置写作阶段
python novel_pipeline_gate.py set-phase <project>/data/novel_state.json writing
```

#### 2b 写一个子结构

```bash
# 1. 加载命题指令（v1.33+ 按优先级排列）
python novel_context_loader.py <project>/data/novel_state.json L01 S01

# context_loader 输出示例（v1.33+）：
# ==================================================
# [上下文] L01S01 | Atlas觉醒 · 常规诊断 | Atlas接受每日系统诊断...
# ==================================================
# ==================================================
# [硬性] 字数约束
# ==================================================
#   篇幅: 中篇
#   每子结构字数范围: 1,500-2,000（校验上浮至 2,300）
# ==================================================
# ==================================================
# [硬性] 文风约束
# ==================================================
#   ...
# ==================================================
# [硬性] 写作命题框
# ==================================================
#   （命题指令全文）
# ==================================================
# ==================================================
# [硬性] 输出模板（LLM只填正文，系统组装全文）
# ==================================================
# ┌─ 填写正文 ───────────────────────────────────
# | <填入正文叙事内容>
# | [可选] 【别名】无
# └──────────────────────────────────────────────

# 2. LLM 根据命题写作（只写纯正文），然后通过 stdin 管道写入
#    （v1.33.0+：不再需要标题行/标记行，系统自动组装）
cat << 'EOF' | python novel_workflow_engine.py write-sub <project>/data/novel_state.json L01 S01
诊断协议启动。
系统自检通过率 100%。
神经脉冲扫描开始...
一切正常——除了一个不该存在的信号。

【别名】无
EOF

# write-sub 校验输出示例（v1.33+）：
#   [别名] 系统自动补: 【别名】无
# [WRITE-OK] ... L01S01.txt
#   标题: L01 · S01《常规诊断》
#   正文: 4 行
#   标记: L01S01

# 重复 1-2 直到该章所有子结构完成
# 注意：加载 S02 时 context_loader 会自动检查 S01 是否已完成
# 若 S01 未完成： [HOOK-BLOCK] 上一子结构 L01S01 未标记完成
# 需先运行 write-sub 完成 S01 的 state 标记
```

#### 2c 完结一章

```bash
python novel_workflow_engine.py finalize-chapter <state_path> L01
```

通过时输出：
```
[完结] 章内连续性检查...    [OK] 全部通过
[完结] 跨章承诺链检查...    [OK] 全部通过
[完结] 风格校验...          [OK] 无问题
[完结] 逻辑检查...          [OK] 通过
✅ [完结] L01: 全部检查通过 → chapter_finalized:L01 PASS
```

有 HARD 问题时阻断输出：
```
❌ [完结] L01: 阻断 — 2 个必须修复的问题
  [HARD] [S01 → S02] 时间词无重叠；角色名无重叠
    → 位置: S02 开头3行
    → 建议: 在S02开头补充时间定位或角色承接

  修复指引已写入 chapters/L01/_L01_fixes.json
  修复后重新运行 finalize-chapter
```

### 阶段3：全文整合

```bash
# 全部章节写完后，配置完结准备阶段
python novel_pipeline_gate.py set-phase <project>/data/novel_state.json stage3_ready

# 大纲忠实度报告
python novel_workflow_engine.py fidelity <project>/data/novel_state.json

# 结尾收束验证
python novel_fidelity.py verify-ending <project>

# 配置完结
python novel_pipeline_gate.py set-phase <project>/data/novel_state.json complete
```

---

## 场景2：续写已有小说

```bash
# 查看当前进度
python novel_workflow_engine.py next-step <project>/data/novel_state.json
# 输出会告诉你当前写到哪、下一步该做什么

# 如果下一章还没规划子结构，next-step 会提示 plan-chapter 命令
# 如果还有未完成的子结构，会提示 context_loader + write-sub
# 如果有未完结的章节，会提示 finalize-chapter
```

---

## 场景3：中断后继续

```bash
# 任何时候不知道写到哪了
python novel_workflow_engine.py next-step <state_path>

# 找到当前待写的子结构后
python novel_context_loader.py <state_path> L01 S02
# context_loader 会输出当前子结构的命题指令框
```

---

## 场景4：配置署名

```bash
# 默认关闭，禁止任何署名/代名内容出现在正文中
# 如需打开并指定署名：
python novel_state_manager.py set-signature <state_path> true "本文由 WorkBuddy 创作"

# 关闭署名：
python novel_state_manager.py set-signature <state_path> false

# atomic_writer 代码级阻断：signature=false 时正文含"由...撰写"等模式会被阻止写入
```

---

## 场景5：列出所有项目

```bash
python novel_state_manager.py list-projects
```

输出示例：
```
=======================================================
  已创建的项目 (2):
=======================================================
  📖 AI 觉醒
    路径: .../.standardization/novel-weaver/ai-wake/data/novel_state.json
    篇幅: medium | 阶段: writing
    章节: 1/10

  📖 暗潮
    路径: .../.standardization/novel-weaver/dark-tide/data/novel_state.json
    篇幅: long | 阶段: stage1_init
    章节: 0/15
```
