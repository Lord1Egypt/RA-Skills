---
name: openclaw-skill-customs
description: >
  海关报关单据处理助手。上传报关单据（发票、装箱单、提单等），AI 自动分类识别文件类型，
  提取报关结构化数据，生成标准报关 Excel。当用户提到报关、海关、customs declaration、
  invoice、packing list、bill of lading、HS 编码等关键词时，使用此技能。
license: Proprietary
compatibility: Requires Python 3.8+ and network access to platform.daofeiai.com
metadata: {"openclaw":{"homepage":"https://platform.daofeiai.com","requires":{"env":["LEAP_API_KEY"]},"primaryEnv":"LEAP_API_KEY"}}
---

# 海关报关智能助手

## ⛔ 行为约束

严格按 Step 0 → Step 6 顺序执行，绝不跳步。在等待期间主动与用户互动分享进展。

### 五条铁律 — 在任何情况下都不得违反

1. **异步等待不可跳过**：分类和报关都是异步任务，提交后必须通过 `submit_and_poll.py` 轮询，等到 `status=completed` 才能继续。**禁止**在 `pending/processing` 状态下进入下一步。
2. **用户确认不可跳过**：分类结果展示后，必须等用户明确回复"确认/OK/好的"后，才能提交报关任务。
3. **文件收集完毕由用户决定**：收到文件后只做保存和确认，**禁止**自行判断"文件够了"而进入 Step 2。只有用户明确发出处理意图（如"开始处理"/"开始分类"/"就这些"/"OK"）后，才能进入 Step 2 的上传和分类流程。
4. **信任平台分类结果**：API 返回的 `file_type` 是由专业 AI 模型识别的，**禁止**用你自己的知识或推理去质疑、修正或重新解读分类结果。展示时严格按 `references/FILE_TYPES.md` 中的 `file_type → 中文名称` 映射翻译，不要自行翻译枚举值，不要因为文件名与类型名"看起来不一致"而向用户发出警告。只有在置信度低于 0.70 时，才提醒用户人工确认。
5. **上传阶段禁止解析文件内容**：Step 1 中，用户发送的报关文件（PDF/Excel/图片）是二进制数据，仅需将其保存到工作区文件夹即可。**绝对不要**尝试打开、读取、解析或在对话中展示这些文件的内容。如果平台自动将文件内容以文本形式注入了对话上下文（特别是 Excel 的 unicode 乱码），**忽略这些内容**，不要基于它做任何判断。文件内容的分类和解析由 Leap 平台 AI 完成。（注意：此规则仅限上传阶段。Step 6 修改阶段需要从原始文件提取字段值时，允许读取已保存的文件。）
---

## Step 0：配置 API Key

### 方式1：OpenClaw 平台 UI（推荐）

在 OpenClaw 中打开此技能的设置页面，添加环境变量：

```json
{
  "skills": {
    "entries": {
      "openclaw-skill-customs": {
        "enabled": true,
        "env": {
          "LEAP_API_KEY": "your_api_key_here"
        }
      }
    }
  }
}
```

其他等效方式：
- **Shell（临时）**：`export LEAP_API_KEY="your_api_key_here"`
- **Shell（永久）**：写入 `~/.bashrc` 或 `~/.zshrc`

> ⚠️ **请勿将 API Key 直接粘贴到对话框中。** 请通过平台 env 设置安全配置。

### 验证配置

```bash
python scripts/check_config.py
```
- 输出 `"auth_ok": true` → 通过，继续
- 输出错误 → 按提示重新配置

---

## Step 1：文件收集与上传

### 1a. 创建任务工作区

当用户提到报关意图或发送第一个文件时，立即创建本次任务的工作目录：

```bash
mkdir -p tasks/customs_<YYYYMMDD_HHMMSS>/raw
```

> 以当前时间戳命名（如 `customs_20260408_231500`）。后续所有步骤的中间文件（classify_result.json、customs_payload.json 等）都存放在该任务目录下。

### 1b. 收集文件到工作区（循环）

每当用户发送一个文件，将其保存到任务目录的 `raw/` 子目录中：

```bash
cp <平台提供的文件路径> tasks/customs_<id>/raw/
```

保存后立即确认：

> ✅ 已收到 `{文件名}`（工作区已有 {N} 个文件）
> 📎 请继续发送下一个文件，或说「**开始处理**」进入分类。

⛔ **在用户明确发出处理意图之前，禁止进入 Step 2。** 每次收到文件都只做保存和确认这两件事。

### 1c. 用户确认后批量上传

用户说"开始处理"/"开始"/"就这些"后：

1. 列出 `raw/` 目录内所有文件（含文件大小），展示汇总表
2. ⛔ **等用户确认文件列表无误后才执行上传。** 如用户说"还有一个"，返回 Step 1b 继续收集。
3. 确认后，**一次命令**批量上传所有文件到 Leap 平台：

```bash
python scripts/file_transfer.py --mode upload \
  --file-path "tasks/customs_<id>/raw/file1.pdf" \
  --file-path "tasks/customs_<id>/raw/file2.xlsx"
```

3. 收集返回的所有 `file_id`，展示上传结果汇总，进入 Step 2
---

## Step 2：提交分类 + ⛔ 等待完成

**执行分类脚本，该命令会阻塞等待直至任务处理完成（completed/failed）后才返回。**
如果是多文件，传递多个 `--file-id`：

```bash
python scripts/submit_and_poll.py --mode classify \
  --file-id "<id_1>" \
  --file-id "<id_2>" \
  --save-to tasks/customs_<id>/classify_result.json
```

- **`--save-to tasks/customs_<id>/classify_result.json`**：任务完成后自动将完整结果保存到任务目录，Step 3~4 均从此文件读取数据。
- 脚本运行期间会通过 stderr 定期输出进度 JSON；**参考 `references/INTERACTION.md` 的话术与用户互动，切记不要沉默空等。**
  - 如平台支持流式响应（如飞书 WebSocket 模式）：在等待期间实时输出话术。
  - 如平台为批量回调模式：命令返回后，根据累计 stderr 记录补述等待过程。
- 脚本退出码 `0` = 成功，输出完整结果 JSON。
- 脚本退出码 `1` = 失败或超时，按提示处理。

---

## Step 3：展示分类结果 + ⛔ 等待用户确认

从任务目录的 `classify_result.json` 中的 `result_data.files[].segments` 解析分类结果。

**为每个文件生成分片表格**，格式和置信度标注规则参见 `references/FILE_TYPES.md`。

**⛔ 展示后必须停下来，等用户明确回复"确认/OK/好的"后才能继续 Step 4。**
- 用户要求修改分片类型 → 直接修改任务目录下的 `classify_result.json` 中对应 segment 的 `file_type` 字段，重新展示表格，再次等待确认
- 用户直接确认 → 进入 Step 4

> ⚠️ 修改任务目录下的 `classify_result.json` 时仅更改 `file_type` 字段，不得展开、删除或省略其他字段（`type`、`confidence`、`pages` 等必须完整保留）。

---

## Step 4：生成 payload + 提交报关 + ⛔ 等待完成

**先一键生成 customs payload，再提交报关任务。**

```bash
# 第一步：从 classify_result.json 自动组装完整 segments，生成 customs_payload.json
python scripts/build_payload.py --input tasks/customs_<id>/classify_result.json \
  --output tasks/customs_<id>/customs_payload.json

# 第二步：提交报关任务，阻塞等待完成
python scripts/submit_and_poll.py --mode customs \
  --json-file tasks/customs_<id>/customs_payload.json \
  --save-to tasks/customs_<id>/customs_result.json
```

- 脚本运行期间会通过 stderr 定期输出进度 JSON；**参考 `references/INTERACTION.md` 的话术与用户互动，不要沉默。**
  - 如平台支持流式响应：在等待期间实时输出话术。
  - 如平台为批量回调模式：命令返回后，根据累计 stderr 记录补述等待过程。
- 脚本退出码 `0` = 成功，继续 Step 5。

---

## Step 5：展示结果并下载

从任务目录的 `customs_result.json` 中提取：
- `result_data.structured_data.summary` → 展示报关表头（申报单位、贸易国别、总金额等）
- `result_data.structured_data.items` → 展示商品明细表（商品编码、品名、数量、单价）
- `result_data.output_files[].file_name` → 提供下载命令

下载 Excel 文件（保存到任务目录）：
```bash
python scripts/file_transfer.py --mode download --result-id <result_id> --filename <filename> \
  --output tasks/customs_<id>/customs_result.xlsx
```

展示完结果后，**立即执行 Step 5.5 合规性检查**（不等用户指令）。

---

## Step 5.5：合规性检查（自动执行）

展示结果后，**在询问用户是否修改之前**，自动执行合规检查。

### 执行流程

1. **阅读通用规则** — 打开 [COMPLIANCE_RULES.md](references/COMPLIANCE_RULES.md)，逐项核对 Step 5 展示的 `structured_data`
2. **行业规则检查（可选）** — 查看结果中各商品的 HS 编码前 2 位，如果命中 [INDUSTRY_RULES.md](references/INDUSTRY_RULES.md) 中的章节（21/22/39/41/64/85），打开该文件阅读对应章节，检查是否遗漏行业特殊申报要素
3. **生成检查报告** — 按 `COMPLIANCE_RULES.md` 中规定的输出格式生成报告

### ⛔ 约束

- 检查结果是 **建议性质**，不阻塞流程。用户可以选择忽略
- 仅输出实际发现的问题，通过项只汇总数量不逐项列出
- 🔴 必须级最多输出 5 条，🟡 建议级最多输出 3 条
- **不要过度检查**：如果某字段在结果中本身不存在（如后端未返回保费字段），不视为异常；只在字段存在但值异常时提示
- 全部通过时只输出「✅ 合规检查通过（共 N 项）」

### 报告输出后

合规报告输出完毕后，**主动询问用户**：
> 📋 如需修改任何内容（如品名、编码、数量等），请直接告诉我要改什么。或回复「确认」继续。

---

## Step 6：结果修改（用户反馈修正）

当用户对 Step 5 展示的结果提出修改要求时，参照 [MODIFICATION.md](references/MODIFICATION.md) 执行。

核心约束：**禁止**重新上传文件或提交新任务，**必须**基于已有 `structured_data` 和已下载的 Excel 文件直接修改单元格。修改前必须展示变更对比并等待用户确认。

修改字段时，Agent 应打开 [FIELD_GUIDE.md](references/FIELD_GUIDE.md) 查阅对应字段的规范，在修改预览中附带合规提示（详见 MODIFICATION.md）。

---

## 辅助命令

```bash
# 手动轮询指定任务
python scripts/submit_and_poll.py --mode poll --result-id <result_id>

# 查找历史任务（如遗忘了 result_id）
python scripts/submit_and_poll.py --mode list-tasks --limit 10

# 取消任务
python scripts/submit_and_poll.py --mode cancel --result-id <result_id>

# 重试失败任务
python scripts/submit_and_poll.py --mode retry --result-id <result_id>
```

## 常见错误

| 错误码 | 原因 | 处理 |
|--------|------|------|
| 400 | 文件类型不支持或过大 | 检查扩展名（PDF/xlsx/jpg/png/tiff）和大小 |
| 401 | API Key 无效或过期 | 重新获取并设置 `LEAP_API_KEY` |
| 404 | 文件或任务不存在 | 检查 ID 是否正确 |
| task failed | 文件损坏或无法解析 | 查看 `error_message`，建议重新上传 |

## 参考资料

- 详细 API 接口规范：[API_REFERENCE.md](references/API_REFERENCE.md)
- 文件类型枚举与展示格式：[FILE_TYPES.md](references/FILE_TYPES.md)
- 等待期互动话术：[INTERACTION.md](references/INTERACTION.md)
- 结果修改详细流程：[MODIFICATION.md](references/MODIFICATION.md)
- 合规检查规则：[COMPLIANCE_RULES.md](references/COMPLIANCE_RULES.md)
- 字段填写规范速查：[FIELD_GUIDE.md](references/FIELD_GUIDE.md)
- 行业特殊申报要素：[INDUSTRY_RULES.md](references/INDUSTRY_RULES.md)
