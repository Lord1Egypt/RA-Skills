# Gongwen Formatting Guidelines

This file summarizes the requirements extracted from `公文标准格式.doc` (`GB/T 9704-2012 党政机关公文格式`).

## 1. Page Setup

- Paper: A4, `210 mm x 297 mm`
- Top margin (`天头`): `37 mm +/- 1 mm`
- Left margin / binding side (`订口`): `28 mm +/- 1 mm`
- Right margin: `26 mm` (ensures core text area width of `156 mm`)
- Bottom margin: `35 mm` (ensures core text area height of `225 mm`)
- Core text area (`版心`): `156 mm x 225 mm`
- Default text color: black
- Default layout density: `22` lines per page, `28` characters per line

## 2. Default Fonts

- General rule: `3号仿宋`
- Issuing authority mark: red `小标宋`, centered
- Secret level / urgency: `3号黑体`
- Signatory label `签发人`: `3号仿宋`
- Signatory name: `3号楷体`
- Title: `2号小标宋`
- Page numbers: `4号半角宋体` Arabic numerals

## 3. Header (`版头`)

- Optional sequence number `份号`: 6-digit `3号` Arabic numerals, top-left first line
- Optional secret level / retention period: top-left second line
- Optional urgency: arranged below in order `份号 -> 密级和保密期限 -> 紧急程度`
- Issuing authority mark:
  - centered
  - top edge to core text top edge: `35 mm`
  - usually `发文机关全称/简称 + 文件`
- Document number (`发文字号`):
  - centered, two lines below issuing authority mark
  - default font `3号仿宋`
  - year uses full-width hex brackets `〔〕`
  - sequence number omits the word `第` and drops leading zeros (write `1`, not `第1` or `01`)
  - ends with `号`
  - for upward reports (`上行文`), it is left-aligned one character from the left edge, on the same line as the last signatory
- Signatory (`签发人`) for upward reports:
  - same line as document number
  - right side, one character space from right
- Red separator line:
  - `4 mm` below the document number
  - centered
  - same width as the core text area

## 4. Body (`主体`)

### Title

- two lines below the header red separator line (`7.2.7`)
- centered
- use trapezoid or diamond-like balanced line breaks for multi-line titles
- font: `2号小标宋`

> Note: GB/T 9704-2012 places exactly **one** red separator line in a standard document — the header line 4 mm below the document number (`7.2.7`). There is **no** red line between the title and the recipient/body, and no rule about leaving blank lines in place of one. The only other red rules are the letter format's red double lines (see section 7).

### Main recipient (`主送机关`)

- one line below title
- left aligned, top grid (`顶格`); wrapped lines stay top grid
- ends with a full-width colon `：`
- if the recipient list is so long the first page cannot show body text, move it to the footer record (`版记`) per `7.4.2`

### Main text (`正文`)

- starts one line below main recipient
- first page must contain body text
- each paragraph starts with two-character indent
- wrapped lines align to the grid
- hierarchy markers follow GB/T 9704-2012:
  - Level 1: `一、`, `二、`, `三、`... (Chinese numerals followed by顿号)
  - Level 2: `（一）`, `（二）`, `（三）`... (parenthesized Chinese numerals)
  - Level 3: `1.`, `2.`, `3.`... (Arabic numerals followed by period)
  - Level 4: `（1）`, `（2）`, `（3）`... (parenthesized Arabic numerals)
- required fonts by level:
  - Level 1: `3号黑体` (Heiti)
  - Level 2: `3号楷体` (Kai)
  - Level 3 and 4: `3号仿宋` (Fangsong)

### Attachment note (`附件说明`)

- if present, one line below body text
- left indent: two characters
- format: `附件：...`
- multiple attachments use Arabic numbering, for example `附件：1. XXX`
- no punctuation after the attachment name; wrapped lines align to the first character of the name

## 5. Signature, Date, Seal

### With seal

- date generally right-aligned with four-character space on the right
- issuing authority name usually centered above date
- seal is red and centered over authority name and date
- seal top should be within one line of the body text or attachment note

### Without seal

- one line below body or attachment note
- issuing authority signature on the right with two-character space
- date on the next line, shifted two characters to the right of the authority name

### Signed by approver

- two lines below body or attachment note
- approver signature seal on the right with four-character space
- job title placed two characters to the left of the signature seal
- date one line below the signature seal

### Date format

- use Arabic numerals for year, month, day
- year written in full
- month and day do not use leading zero

## 6. Notes, Attachments, Footer

### Note (`附注`)

- if present, place one line below the date
- left indent: two characters
- use parentheses

### Attachment page

- attachment starts on a new page
- top-left first line: `附件` plus attachment number in `3号黑体`
- attachment title centered on the third line
- attachment numbering must match the attachment note

### Footer record (`版记`)

- separator lines are full core-width
- first and last lines are thick; middle line is thin
- `抄送` line uses `4号仿宋`, left/right one-character space
- last copied unit ends with `。`
- `印发机关` on left, `印发日期` on right
- date ends with `印发`

### Page numbers

- use `4号半角宋体` Arabic numerals
- format: `— 1 —` (em-dash + page number + em-dash)
- positioned below the core text area bottom edge; the dash line sits `7 mm` below that edge
- single pages right aligned (`居右空一字`), double pages left aligned (`居左空一字`)
- blank pages before the footer record page do not show page numbers
- attachments bound with body use continuous pagination

## 7. Special Formats

### Letter (`信函格式`)

- issuing authority mark top edge to page top: `30 mm`
- top and bottom both use centered red double lines, each `170 mm`
- first page does not show page number
- footer record does not include `印发机关/印发日期` or separator lines

### Order (`命令/令`)

- issuing authority mark top edge to core text top edge: `20 mm`
- authority mark is `发文机关 + 命令` or `令`
- order number centered two lines below
- body starts two lines below order number

### Minutes (`纪要`)

- header mark is `XXXXX纪要`
- attendee / leave / observer lists can be added below body or attachment note
- labels `出席` / `请假` / `列席` use `3号黑体`
- names and units use `3号仿宋`

## 8. Common Review Checklist

- Is the first page showing body text?
- Are page margins and text area compliant?
- Is the title `2号小标宋` and centered correctly?
- Are recipient, body, attachment note, signature, date, and footer in the right order?
- Is the date written as full year + non-zero-padded month/day?
- Are document number, signatory, secret level, urgency, and copied units present only when known?
