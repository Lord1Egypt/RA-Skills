# 起诉状和答辩状流程

## 选择模板

起诉状：

```json
{"capability":"complaint","query":"离婚起诉状"}
```

答辩状：

```json
{"capability":"defense","query":"离婚答辩状"}
```

传给 `catalog`。选择模板后调用 `pleading-start`：

```json
{
  "capability":"complaint",
  "templateId":"模板编号",
  "query":"离婚起诉状"
}
```

## 提取案件信息

优先把当前任务/当前线程中用户已经提供的全部案件事实忠实汇总成一段案情描述，并连同当前任务中的案件材料文件提交；不得要求用户把本任务中已经说过的内容再描述一遍。`content`、`query`、当事人、请求、事实理由、法院和材料路径都禁止读取或混入 WorkBuddy/宿主全局记忆、长期记忆、用户画像、其他任务、其他线程、旧案例、旧报告、旧合同、旧文书、示例、评测、交接文档、测试记录或日志。文本文件由脚本直接读取，图片由文书后端视觉提取，PDF、Word和表格先按 `references/case-materials.md` 使用宿主工具读取并放入 `extractedTexts`。只有当前任务消息和材料中都没有可提取的案件事实时才向用户索要：

```json
{
  "sessionId":"任务编号",
  "content":"用户案情描述",
  "filePaths":["/绝对路径/起诉材料.pdf","/绝对路径/材料1.jpg"],
  "extractedTexts":[
    {"filePath":"/绝对路径/起诉材料.pdf","text":"从PDF忠实提取的文字"}
  ]
}
```

传给 `pleading-extract`。旧调用中的 `imagePaths` 仍兼容。脚本把当前任务文本材料和当前任务 `content` 合并后送入 `/indictment/aiExtractsInfo`，图片先上传 `/indictment/uploadImage` 再由同一流程识别。AI 提取结果是当前 `sessionId` 的预填内容；逐字段只对照当前任务用户陈述、当前任务材料、当前 `sessionId` 已有值和当前任务更正，有明确依据的值可以自动接受，不逐项重复询问，缺失、冲突、无法唯一判断或会实质影响文书的内容才让用户补充。生成前仍须通过完整摘要一次性确认。

## 分步骤核对

每次收到当前步骤的 `interaction` 后，先执行 `references/interaction.md` 的“当前任务证据匹配”：

- 当前任务证据可可靠补全的字段通过 `patches` 或 `partyAction` 直接写入。
- 当前字段页已经可靠完成时，直接切换到下一 `fieldPage`；当前步骤的所有页完成后再使用 `direction=next`。
- 多当事人字段依次用 `focus` 检查各类当事人卡片；已有值且与当前任务消息或材料一致时不再询问。
- 当前视图仍有没有匹配答案、冲突或实质性未决字段时，只询问这些字段并等待用户本人填写或选择。无论字段是否标记必填，只要可填写且没有当前任务依据，就不能由 AI 保持空白或跳过；只读字段除外。
- 不得把未提及某事实当成否定回答，也不得为了走完表单而虚构姓名、金额、日期、法院或诉讼请求；“不清楚”“不知道”“不确定”“其他”“无”“否”“不适用”等值也不能作为无匹配时的自动默认答案，只有用户明确表达或亲自选择时才能写入。

使用 `pleading-update` 更新普通字段：

```json
{
  "sessionId":"任务编号",
  "patches":{
    "plaintiffs[0].plaintiffName":"张某",
    "plaintiffs[0].plaintiffContact":"13800000000"
  },
  "direction":"next"
}
```

维护多个当事人：

```json
{
  "sessionId":"任务编号",
  "partyAction":{
    "type":"add",
    "collection":"defendants",
    "value":{"defendantName":"李某"}
  }
}
```

修改或删除时传 `type=update` 或 `type=remove`，并使用从零开始的 `index`。向用户显示时把序号加一。

字段较多时，脚本不会把整份表单铺满大模型窗口：

- 文书始终只显示当前步骤。
- “当事人信息”一次只展开一类当事人的一张卡片，其他当事人仅显示姓名等摘要。
- 普通字段每页最多八项。
- 当事人超过二十位时只返回前二十条摘要，并给出剩余数量。

切换当事人卡片：

```json
{
  "sessionId":"任务编号",
  "focus":{"collection":"defendants","index":1}
}
```

切换当前步骤中的普通字段页：

```json
{"sessionId":"任务编号","fieldPage":1}
```

## 确认并生成

进入“确认生成”步骤后，向用户汇总：

- 所有当事人
- 诉讼请求或答辩意见
- 事实与理由
- 证据材料
- 法院和管辖信息

用户明确确认后调用：

```json
{"sessionId":"任务编号","confirmed":true}
```

传给 `pleading-generate`，最后展示文书摘要并在同一轮原样输出 `data.delivery.markdown`，起诉状固定显示为 `[起诉状（Word）](链接地址)`，答辩状固定显示为 `[答辩状（Word）](链接地址)`。最终摘要和法律依据只能来自已生成文书及文书内已经列出的法规、案例和其他依据；不得在生成后搜索、查询或补充文书外内容。该链接必须在文书生成当轮出现，不得等用户再次索取。文书为下载链接，`data.delivery.autoOpen=false`，不自动打开、预览或导航；它使用后端 `/indictment/download/{recordId}.docx` 接口，由用户主动点击下载，不再提供 `/indictment/report/{recordId}` 在线文书页面。
