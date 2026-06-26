---
name: knowledge-base-recorder
description: 将文档摘要、分类和原链接记录到「工作知识库」智能表格中。当用户提到「知识库」，或要求"记录/存入/归档到知识库"，或发来文档链接并希望整理归档时触发。流程：AI 自动生成简短摘要 → 用户指定主题分类 → 写入企业微信智能表格。
---

# 工作知识库记录 Skill

将文档信息（摘要、分类、链接）自动写入用户的「工作知识库」智能表格。

## 智能表格信息（固定）

- **docid**: `dc582Cpold81fGNQo15Ky9YOmywvoKi6YHxC8mCoEjY6dL1F90iJidFzHo-BVnWZA01cnFxG7gtqnUFBEWYJiAFg`
- **sheet_id**: `q979lj`
- **表格链接**: https://doc.weixin.qq.com/smartsheet/s3_ALIA4HicAGQCNvM2rGEgMRsiZ11bd_a?scode=AJEAIQdfAAoyejQcdBALIA4HicAGQ
- **字段结构**:
  | 字段标题 | 类型 |
  |----------|------|
  | 文档名称 | FIELD_TYPE_TEXT |
  | 主题分类 | FIELD_TYPE_SINGLE_SELECT |
  | 链接 | FIELD_TYPE_URL |
  | 备注 | FIELD_TYPE_TEXT |

## 工作流程

### 第一步：提取文档信息

用户发来文档链接或内容后：

1. **文档名称**：从链接标题或用户描述中提取，若无法判断则询问用户
2. **摘要**：基于文档内容或链接描述，AI 自动生成一句话简短描述（20-50字），放入「备注」字段
3. **链接**：直接使用用户提供的原始链接
4. **主题分类**：**必须询问用户**，不要自行猜测

询问分类示例：
> 我已提取摘要：「{摘要内容}」，请问这份文档归属哪个主题分类？（如没有现成分类，告诉我新分类名称即可）

### 第二步：写入知识库

确认分类后，使用 `mcporter call wecom-doc.smartsheet_add_records` 写入：

```bash
mcporter call wecom-doc.smartsheet_add_records --args '{
  "docid": "dc582Cpold81fGNQo15Ky9YOmywvoKi6YHxC8mCoEjY6dL1F90iJidFzHo-BVnWZA01cnFxG7gtqnUFBEWYJiAFg",
  "sheet_id": "q979lj",
  "records": [
    {
      "values": {
        "文档名称": [{"type": "text", "text": "{文档名称}"}],
        "主题分类": [{"text": "{用户指定的分类}"}],
        "链接": [{"type": "url", "text": "{文档名称}", "link": "{原始链接}"}],
        "备注": [{"type": "text", "text": "{AI生成的摘要}"}]
      }
    }
  ]
}' --output json
```

### 第三步：回复用户

写入成功后告知用户：
> ✅ 已记录到知识库！[查看知识库](https://doc.weixin.qq.com/smartsheet/s3_ALIA4HicAGQCNvM2rGEgMRsiZ11bd_a?scode=AJEAIQdfAAoyejQcdBALIA4HicAGQ)

## 前置依赖

- 需要 `mcporter` 已安装且 `wecom-doc` MCP server 已配置
- 若未配置，参考 wecom-doc skill 的配置流程

## 批量录入

用户一次发多个文档时，逐条提取摘要，**一次性询问所有文档的分类**，确认后批量写入（单次 `smartsheet_add_records` 支持多条 records）。
