# 知识库导出/导入模块

> 当用户请求导出或导入知识库时，加载本模块。

---

## 1. 导出知识库

### 触发

用户说"导出项目"/"导出知识库"/"分享项目"/"备份项目"。

### 流程

```
1. 读取 projects.yaml，列出所有项目供用户选择
   - 如果用户指定了项目名 → 直接选
   - 如果用户说"全部" → 逐个导出
   - 如果当前有活跃项目 → 默认选中

2. 对每个选中项目：
   a. 读取 PROJECT-STATUS.md
   b. 读取 requirements/README.md（需求索引）
   c. 读取前 3 条活跃需求的完整 README.md（含优先级+标签+会话记录）
   d. 收集 public/ 目录下的文件列表

3. 生成导出包目录：
   {项目名}/
   ├── README.md           ← 导出说明
   ├── PROJECT-STATUS.md   ← 项目状态快照
   ├── requirements/
   │   ├── README.md       ← 需求索引
   │   ├── {REQ-001}/
   │   │   └── README.md   ← 需求详情
   │   ├── {REQ-002}/
   │   │   └── README.md   ← 需求详情
   │   └── {REQ-003}/
   │       └── README.md   ← 需求详情
   └── INSTALL-GUIDE.md    ← 导入指引

4. 打包为 zip：
   - 默认位置：~/.myknowledge/exports/{项目名}-{日期}.zip
   - 用户指定路径 → 先检查路径是否在 ~/.myknowledge/ 目录下
      · 如果是 → 直接使用
      · 如果不是 → 询问用户确认：
        ```
        ⚠️ 注意：导出文件将保存到 ~/.myknowledge/ 之外的路径。
        
        导出位置：{用户指定路径}
        
        1 — 继续（我确认要导出到这里）
        2 — 改用默认位置（~/.myknowledge/exports/）
        3 — 重新指定路径
        ```

5. 告知用户：
   📦 已导出「{项目名}」→ {导出路径}
   📋 包含：项目状态 + 需求索引 + {N}条需求详情 + 导入指引
   
   > 💡 提示：导出文件位于 {导出路径}，你可以手动复制到需要的位置。
```

### 导出包 README.md 模板

```markdown
# {项目名} — 知识库导出

> 导出日期：{date}
> 导出工具：MyKnowledge Skill
> 包含：项目状态、需求索引

## 如何导入？

**已安装 MyKnowledge**：
对 AI 说「导入知识库」，然后提供此 zip 文件路径。

**未安装 MyKnowledge**：
查看 INSTALL-GUIDE.md，安装后即可导入。
```

### INSTALL-GUIDE.md 模板

```markdown
# MyKnowledge 安装指引

MyKnowledge 是一个 AI 知识库管理 Skill。

## 安装（选一种）

1. **SkillHub（推荐，无需终端）**：对 AI 说「安装 my-knowledge 技能」
2. **Atomgit**：`git clone https://atomgit.com/CoderMoray/MyKnowledge.git ~/.codebuddy/skills/myknowledge/`
3. **GitHub**：`git clone https://github.com/CoderMoray/MyKnowledge.git ~/.codebuddy/skills/myknowledge/`

安装后对 AI 说「导入知识库」并提供此 zip 文件。

> 支持平台：CodeBuddy / WorkBuddy / OpenClaw / Claude
```

---

## 2. 导入知识库

### 触发

用户说"导入知识库"/"导入项目"，并提供 zip 文件路径。

### 流程

```
1. 确认 zip 文件路径
2. 读取 zip 内的 README.md，确认是 MyKnowledge 导出包
3. 提取项目名（从 README.md 或目录名）
4. 检查是否已存在同名项目：
   - 不存在 → 直接导入
   - 存在 → 展示对比信息，询问用户

5. 导入：
   - 解压到 ~/.myknowledge/global/{项目名}/
   - 追加到 projects.yaml
   - 告知用户导入完成
```

### 同名项目处理

```
⚠️ 已存在同名项目「{项目名}」

| | 现有项目 | 导入包 |
|------|----------|--------|
| 需求数 | {N} | {M} |
| 最后更新 | {date1} | {date2} |
| 完成率 | {done}/{N} | {done}/{M} |

1 — 覆盖（用导入内容替换现有）
2 — 重命名（导入为「{项目名}-导入」）
3 — 我不确定，帮我对比分析给建议
```

**选项 3 的 AI 响应**：
```
对比分析：
- 现有项目需求更多（{N} vs {M}），但可能有已完成/废弃需求
- 导入包更新（{date2} > {date1}），可能是对方的最新版本
- 建议：
  · 如果导入包是对方主动发给你的 → 选 2（重命名），保留两份按需合并
  · 如果你想同步覆盖 → 选 1（覆盖）
  · 建议先选 2，查看导入内容后再决定是否合并
```

---

## 3. 错误处理

| 错误 | 处理 |
|------|------|
| 导出时项目不存在 | 提示用户选择其他项目或先创建 |
| 导入 zip 无效（无 README.md） | 按以下格式提示： |
| | ⚠️ 导入失败：这不是有效的 MyKnowledge 导出包 |
| | |
| | 有效的导出包必须满足： |
| |   • 是 .zip 格式 |
| |   • 包含 README.md 文件 |
| |   • 是由 MyKnowledge 的"导出项目"功能生成的 |
| | |
| | 你可以： |
| |  1 — 重新导出一次（推荐） |
| |  2 — 手动解压后，把文件夹放到 .myknowledge/projects/ 下 |
| |  回复数字即可 |
| 导入时路径无写入权限 | 提示用户换一个有写入权限的目录 |
| 用户取消导入 | 不操作，回复"好的，已取消" |
