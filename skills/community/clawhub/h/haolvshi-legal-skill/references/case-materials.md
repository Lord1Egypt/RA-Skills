# 案件材料识别与复用

法律咨询报告、法律计算器、起诉状和答辩状遇到用户在当前任务上传文件时，先处理材料，再选择项目、回答题目或提取文书字段。不得因为聊天文字已经足够启动流程而忽略附件。材料证据范围仅限当前任务：禁止从全局记忆、其他任务、其他线程、旧案例、旧报告、示例、评测、交接文档、测试记录或日志补充材料内容。

## 支持范围

- `TXT`、`Markdown`、`CSV`、`JSON`、`HTML`、`XML`：脚本可直接提取文字。
- `PDF`、`DOC`、`DOCX`、`RTF`、`XLS`、`XLSX`：先使用当前宿主真实可用的 PDF、文档或表格阅读工具提取文字。
- `JPG`、`JPEG`、`PNG`：咨询和计算器先使用宿主图像理解或文字识别工具提取内容；起诉状和答辩状可以直接交给后端视觉提取，也可以同时提供宿主识别文字。
- 单个文件不超过 10MB，一次最多二十个案件材料文件。

不要根据宿主名称假设文件能力。先检查实际工具列表；宿主能读取时直接读取，不能读取时再请用户提供可复制文字或转换后的文件。禁止静默跳过无法解析的附件。

## 通用提取命令

纯文本材料可直接调用：

```json
{
  "capability":"consultation",
  "filePaths":["/绝对路径/事故经过.txt"]
}
```

传给 `case-materials`。返回的 `data.caseContext.text` 是内部案情上下文，不向用户整段复述。

PDF、Word、表格或图片由宿主读取后，把忠实提取结果随原文件路径提交：

```json
{
  "capability":"calculator",
  "filePaths":["/绝对路径/病历.pdf","/绝对路径/医疗费票据.png"],
  "extractedTexts":[
    {"filePath":"/绝对路径/病历.pdf","text":"宿主从病历中提取的原文信息"},
    {"filePath":"/绝对路径/医疗费票据.png","text":"宿主从票据图片识别的文字和金额"}
  ]
}
```

如果返回 `stage=needs_material_extraction`，根据 `data.unresolvedFiles` 使用宿主相应工具提取，然后将结果放入 `extractedTexts` 重试原命令。只有宿主确实无法读取时才询问用户转换文件。

## 咨询和计算器

`catalog` 和 `question-start` 都接受当前任务的 `filePaths`、`extractedTexts`、`materialText`。项目选择时只结合当前任务原始问题和当前任务材料内容；任务创建后，材料文字保存在当前 `sessionId` 的私有任务状态，并出现在每道题的 `interaction.caseContext` 中。不得把其他任务生成的 `caseContext` 传入本任务。

每道题都按以下顺序处理：

1. 只对照当前任务的 `interaction.caseContext.text`、当前任务用户陈述和当前 `sessionId` 已保存答案。
2. 材料中有直接且唯一的答案时，自动组装 `answers` 调用 `question-reply`。
3. 材料没有答案、材料之间冲突或无法唯一映射到选项时，无论字段是否标记必填，都必须向用户提问并等待本人选择或填写；不得留空跳过，也不得自动选择“不清楚”、其他兜底选项、否定选项或任意默认值。
4. 不把“材料没有记载”解释为“否”“无”或零；材料与用户后来明确更正冲突时，以用户更正为准。

## 起诉状和答辩状

`pleading-extract` 接受普通案情描述、`filePaths`、兼容旧调用的 `imagePaths`，以及宿主生成的 `extractedTexts`。

- 文本类材料由脚本提取后与 `content` 合并，一起发送给 `/indictment/aiExtractsInfo`。
- 图片先上传 `/indictment/uploadImage`，再由同一个文书要素接口识别。
- PDF、Word、表格由宿主读取后，其 `extractedTexts` 与用户描述一起进入文书要素提取。
- 提取后的材料上下文只保存在当前 `sessionId` 中，后续字段页和恢复流程只能继续使用同一任务状态；不得用其他任务编号恢复或复用；生成前仍须通过完整摘要让用户确认。

不得把材料原文未经筛选地铺到聊天回复中，也不得在最终回复中展示身份证号等敏感信息。
