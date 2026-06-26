# notebooklm-distiller — 功能验证测试用例

> 所有功能在合并到 main 前必须通过以下测试。
> 测试环境要求：已完成 `notebooklm login`，至少存在 1 个有内容的 NotebookLM notebook。

---

## 前置准备

```bash
# 确认 CLI 可用
notebooklm list

# 记录一个有内容的 notebook 名称和 ID，用于后续测试
# 例：KB: MyResearch  →  ID: xxxxxxxx
```

---

## Case 1：`distill --mode qa`

**目标**：从已有 notebook 生成深度 Q&A，每题附常见误解块，写入 Obsidian。

```bash
python3 scripts/distill.py distill \
  --keywords "<已知 notebook 关键词>" \
  --topic "TestTopic" \
  --vault-dir "/tmp/test-vault" \
  --mode qa
```

**验证点：**
- [ ] 成功找到匹配 notebook，日志输出 `Found 1 notebook(s)`
- [ ] 生成 15-20 个问题（日志：`Generated N questions`）
- [ ] 输出文件存在：`/tmp/test-vault/TestTopic/<NotebookName>_QA.md`
- [ ] 文件包含 YAML frontmatter（`---` 开头，含 `title` / `date` / `author` 字段）
- [ ] 每个 Q&A 块包含 `> [!question]` callout
- [ ] 每个 Q&A 块包含 `> [!warning] Common Misconception` callout
- [ ] `author: notebooklm-distiller`（无个人信息）

---

## Case 2：`distill --mode summary`

**目标**：生成五节专家知识地图。

```bash
python3 scripts/distill.py distill \
  --keywords "<已知 notebook 关键词>" \
  --topic "TestTopic" \
  --vault-dir "/tmp/test-vault" \
  --mode summary
```

**验证点：**
- [ ] 输出文件：`<NotebookName>_Summary.md`
- [ ] 包含五个 `##` 节：`Core Mental Models` / `Consensus Map` / `Debate Map` / `Trade-offs` / `Open Frontier`
- [ ] 各节内容非空（不是"No answer returned"）
- [ ] Debate Map 节包含至少两个不同观点

---

## Case 3：`distill --mode glossary`

**目标**：生成术语表，含专家 vs 新手用法对比。

```bash
python3 scripts/distill.py distill \
  --keywords "<已知 notebook 关键词>" \
  --topic "TestTopic" \
  --vault-dir "/tmp/test-vault" \
  --mode glossary
```

**验证点：**
- [ ] 输出文件：`<NotebookName>_Glossary.md`
- [ ] 至少包含 10 个术语条目
- [ ] 每个条目含定义 + 专家/新手用法区别描述
- [ ] 包含"容易混淆的相关概念"说明

---

## Case 4：`research`

**目标**：发起网络调研，新建 notebook，等待完成。

```bash
python3 scripts/distill.py research \
  --topic "Test Research Topic 2026" \
  --mode fast
```

**验证点：**
- [ ] 打印 `Notebook : Research: Test Research Topic 2026`
- [ ] 打印 `ID       : <notebook_id>`
- [ ] 打印 Next step 提示（含 distill 命令示例）
- [ ] `notebooklm list` 中可找到新建的 notebook

---

## Case 5：`persist`

**目标**：将内容直接写入 Obsidian vault，自动附 frontmatter。

```bash
mkdir -p /tmp/test-vault/Notes

python3 scripts/distill.py persist \
  --vault-dir "/tmp/test-vault" \
  --path "Notes/test-persist.md" \
  --title "Persist Test Note" \
  --content "This is a test note for validation." \
  --tags "test,validation"
```

**验证点：**
- [ ] 打印 `Persisted → /tmp/test-vault/Notes/test-persist.md`
- [ ] 文件存在且包含 YAML frontmatter
- [ ] `title: "Persist Test Note"` 正确
- [ ] `tags: ["test", "validation"]` 正确
- [ ] `author: notebooklm-distiller`

```bash
# 从文件写入
echo "# Draft\nSome content." > /tmp/draft.md
python3 scripts/distill.py persist \
  --vault-dir "/tmp/test-vault" \
  --path "Notes/test-from-file.md" \
  --file /tmp/draft.md
```

- [ ] 文件内容与源文件一致

---

## Case 6：`quiz`（Discord 互动测验第一步）

**目标**：生成问题列表，输出合法 JSON。

```bash
python3 scripts/distill.py quiz \
  --keywords "<已知 notebook 关键词>" \
  --count 5
```

**验证点：**
- [ ] 输出为合法 JSON（`python3 -c "import json,sys; json.load(sys.stdin)" < output.json`）
- [ ] JSON 包含字段：`notebook_id` / `notebook_name` / `questions` / `total`
- [ ] `questions` 为数组，长度 ≤ 5
- [ ] 每个问题为字符串，长度 > 10
- [ ] 问题不是事实性回忆题（需人工判断：问题要求推理或解释 WHY）

---

## Case 7：`evaluate`（Discord 互动测验第二步）

**目标**：对给定答案进行评估，输出结构化 JSON 反馈。

```bash
# 先从 Case 6 拿到 notebook_id 和一个问题
python3 scripts/distill.py evaluate \
  --notebook-id "<Case 6 的 notebook_id>" \
  --question "<Case 6 的某个问题>" \
  --answer "我的测试答案，故意不完整"
```

**验证点：**
- [ ] 输出为合法 JSON
- [ ] JSON 包含字段：`question` / `user_answer` / `feedback`
- [ ] `feedback` 非空，包含对答案的具体评价
- [ ] feedback 中能识别"答对的部分"和"遗漏的点"（人工判断）

---

## Case 8：错误处理

```bash
# 关键词不匹配
python3 scripts/distill.py distill \
  --keywords "xyzzy-nonexistent-notebook-99999" \
  --topic "Test" \
  --vault-dir "/tmp/test-vault" \
  --mode qa
```
- [ ] 退出码非 0
- [ ] 日志输出 `[FATAL] No notebooks matched`

```bash
# vault-dir 不存在
python3 scripts/distill.py distill \
  --keywords "<关键词>" \
  --topic "Test" \
  --vault-dir "/nonexistent/path" \
  --mode qa
```
- [ ] 退出码非 0
- [ ] 日志输出 `[FATAL] vault-dir does not exist`

---

## Case 9：个人信息扫描

```bash
# 扫描所有文件，确认无个人信息
grep -rn "/Users/[a-z]\+\|your-name\|your-email\|my-notebook" \
  scripts/ SKILL.md README.md README_zh.md requirements.txt
```

- [ ] 输出为空（无匹配）

---

## 测试结果记录

| Case | 功能 | 状态 | 备注 |
|---|---|---|---|
| 1 | distill qa + misconception | ⬜ 待测 | |
| 2 | distill summary（新 prompt） | ⬜ 待测 | |
| 3 | distill glossary（新 prompt） | ⬜ 待测 | |
| 4 | research | ⬜ 待测 | |
| 5 | persist（inline + file） | ⬜ 待测 | |
| 6 | quiz（JSON 输出） | ⬜ 待测 | |
| 7 | evaluate（答案评估） | ⬜ 待测 | |
| 8 | 错误处理 | ⬜ 待测 | |
| 9 | 个人信息扫描 | ⬜ 待测 | |

全部通过后，将 `dev/full-features` 合并到 `main` 并公开发布。
