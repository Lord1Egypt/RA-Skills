# Step 4 — 分析

**目的**：LLM 逐条分析 S3 输出，生成摘要、打标签、判断适用性。

## 前置检查

```
检查 gxpcode_data/s3/.done 是否存在 → 不存在则等待 S3
```

## 输入

- `gxpcode_data/s3/`：S3 每条含 `title` + `detail_text` + `attachment`
- `resources/config.yaml`：企业类型 + 关注领域
- `s4_prompt.md`：LLM 分析 Prompt 模板（含适用性判断标准、输出格式）

## 核心规则

仅追加 `summary` / `tags` / `applicability` / `reason` / `needs_manual_review` 五个字段，**严禁修改** S3 传入的 `title`、`url`、`source`、`date`、`detail_text`、`attachment` 等原始字段。

## 执行逻辑

分两阶段：**LLM 分析** → **脚本合并写入**。

### 阶段 1：LLM 分析

```
遍历 s3/ 下所有 .json 文件:
  └─ 每个文件内每 5 条一批:
       └─ 读 title + detail_text + source + date + url + attachment
       └─ 使用 `s4_prompt.md` 模板，填入 enterprise_type / focus_areas / input_json
       └─ LLM 逐条分析，输出 JSON 数组（每条保留 S3 全部原始字段 + 5 个分析字段）
       └─ 写入临时 analysis.json
```

### 阶段 2：合并写入

```bash
python "${SKILL_DIR}/scripts/step4_merge.py" gxpcode_data analysis.json
```

`step4_merge.py` 负责：
- 校验每条是否包含 5 个必填分析字段
- 按 source 分组写入 s4/s4_{源名}.json
- 写入 s4/.done

## LLM 分析规则

对每条输入（title + detail_text），LLM 输出以下 5 个字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `summary` | string | 2-3 句中文摘要，概括法规核心内容 |
| `tags` | array | 从 `config.yaml` 的关注领域列表中选择匹配的标签，如 `["GMP","临床试验"]` |
| `applicability` | enum | `high` \| `medium` \| `low` \| `none`，对照 `config.yaml` 的企业类型判断 |
| `reason` | string | 一句话说明适用性判断依据 |
| `needs_manual_review` | bool | 仅当 `detail_text` 为 `[PDF document]`（无正文）时设为 `true`，否则为 `false` |

### detail_text 为 [PDF document] 的特殊处理

仅根据 `title` 字段进行分析，`summary` 末尾追加"（正文为PDF附件，分析仅供参考）"，`needs_manual_review` 设为 `true`。

## 输出

- `gxpcode_data/s4/s4_{源名}.json`：每条追加 5 个分析字段
- `gxpcode_data/s4/.done`：标记完成

## 格式示例

```json
{
  "source": "CDE-指导原则",
  "title": "国家药监局药审中心关于发布...",
  "url": "https://...",
  "date": "2026-06-01",
  "detail_text": "...",
  "attachment": "...",
  "summary": "CDE发布mRNA疫苗临床试验指导原则...",
  "tags": ["临床试验", "疫苗"],
  "applicability": "high",
  "reason": "涉及生物制品临床试验，企业有相关管线",
  "needs_manual_review": false
}
```
