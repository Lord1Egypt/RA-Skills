# Maybe Sheet Clickable References

Use this reference when an answer about a Maybe Sheet needs to mention confirmed cells, ranges, or worksheets from the current workbook. The frontend can render `sheet-ref` tags as clickable references.

## Formats

Cell or range:

```html
<sheet-ref kind="cell" docId="DOCUMENT_ID" gid="WORKSHEET_GID" sheet="WORKSHEET_NAME" range="A1_OR_A1:B2">VISIBLE_LABEL</sheet-ref>
```

The tag must be paired and must include visible text. The frontend parser does not recognize self-closing tags.

Worksheet:

```html
<sheet-ref kind="worksheet" docId="DOCUMENT_ID" gid="WORKSHEET_GID" sheet="WORKSHEET_NAME">VISIBLE_LABEL</sheet-ref>
```

## Rules

- Only use `sheet-ref` tags when the task is operating on a Maybe Sheet.
- Only use `sheet-ref` tags for real cells, ranges, or worksheets from the current workbook.
- Only use `sheet-ref` tags for references that were confirmed from the workbook, a tool result, or a reliable Maybe Sheet API response.
- Do not use `sheet-ref` tags for examples, guesses, inferred locations, hypothetical formulas, external workbook references, or uncertain references.
- Include the current workbook document ID in the `docId` attribute. Use the exact document ID from the Maybe Sheet URL or API response.
- Include the target worksheet gid in the `gid` attribute. Use the exact gid from the Maybe Sheet URL, worksheet list, or API response.
- Preserve the exact worksheet name from the workbook or tool result in the `sheet` attribute.
- Use A1 notation in the `range` attribute. For a single cell, either `A1` or `A1:A1` is acceptable; prefer the form returned or required by the active tool.
- Use a concise visible label, usually `SheetName!A1`, `SheetName!A1:B2`, or the worksheet name.
- Always use paired tags with visible text: `<sheet-ref ...>SheetName!A1</sheet-ref>`.
- Never use self-closing tags such as `<sheet-ref kind="cell" docId="abc123" gid="0" sheet="Sheet1" range="A1"/>`; they are not clickable in the current frontend.
- Do not wrap `sheet-ref` tags in code blocks in the final answer.
- Do not put `sheet-ref` tags inside formula code blocks, SQL code blocks, JSON, shell commands, or other literal examples.
- If the task is not about Maybe Sheet, answer normally without `sheet-ref` tags.

## Chinese Rules

- 只在当前任务是 Maybe Sheet 场景时使用 `sheet-ref`。
- 只对当前 Maybe Sheet 工作簿中真实存在的单元格、区域或工作表使用。
- 只对已经从工作簿、工具结果或可信 Maybe Sheet API 响应中确认的位置使用。
- 不要对示例、猜测、推断位置、假设公式、外部工作簿引用或不确定位置使用。
- 必须在 `docId` 属性中包含当前工作簿的文档 ID。使用 Maybe Sheet URL 或 API 响应中的精确 document ID。
- 必须在 `gid` 属性中包含目标工作表 gid。使用 Maybe Sheet URL、worksheet 列表或 API 响应中的精确 gid。
- `sheet` 必须保留工作簿或工具结果里的精确工作表名。
- `range` 使用 A1 表示法。单个单元格可以写成 `A1` 或 `A1:A1`；优先使用当前工具返回或要求的形式。
- 显示文本保持简短，例如 `Sheet1!A1`、`Sheet1!A1:B2` 或工作表名。
- 必须使用带显示文本的成对标签：`<sheet-ref ...>SheetName!A1</sheet-ref>`。
- 禁止使用 `<sheet-ref kind="cell" docId="abc123" gid="0" sheet="Sheet1" range="A1"/>` 这类自闭合标签；当前前端不会把它渲染成可点击链接。
- 不要把 `sheet-ref` 放进最终回答的代码块。
- 不要把 `sheet-ref` 放进公式、SQL、JSON、shell 命令或其他字面量示例中。
- 如果任务不是 Maybe Sheet 场景，正常回答，不要输出 `sheet-ref`。

## Examples

Good:

```md
异常值主要出现在 <sheet-ref kind="cell" docId="6a33b18d091d6b760b093359" gid="2" sheet="订单明细" range="F18">订单明细!F18</sheet-ref>，汇总结果在 <sheet-ref kind="worksheet" docId="6a33b18d091d6b760b093359" gid="3" sheet="汇总">汇总</sheet-ref>。
```

Good:

```md
<sheet-ref kind="cell" docId="6a33b18d091d6b760b093359" gid="3" sheet="利润分析" range="C3:C3">利润分析!C3</sheet-ref> 来自 <sheet-ref kind="cell" docId="6a33b18d091d6b760b093359" gid="18" sheet="利润表-2025Q2" range="D5:D5">利润表-2025Q2!D5</sheet-ref>。
```

Bad:

```md
For example, <sheet-ref kind="cell" docId="6a33b18d091d6b760b093359" gid="0" sheet="Sheet1" range="A1">Sheet1!A1</sheet-ref> could contain revenue.
```

The bad example uses `sheet-ref` for an example, not a confirmed workbook reference.

Bad:

```md
Q2 销售费用在 <sheet-ref kind="cell" docId="6a33b18d091d6b760b093359" gid="3" sheet="利润分析" range="B6"/>
```

The bad example uses a self-closing tag, which the current frontend does not recognize as a clickable reference.

Bad:

```md
<sheet-ref kind="cell" sheet="利润分析" range="C3:C3">利润分析!C3</sheet-ref>
```

The bad example omits the required `docId` attribute.

Bad:

```md
<sheet-ref kind="cell" docId="6a33b18d091d6b760b093359" sheet="利润分析" range="C3:C3">利润分析!C3</sheet-ref>
```

The bad example omits the required `gid` attribute.
