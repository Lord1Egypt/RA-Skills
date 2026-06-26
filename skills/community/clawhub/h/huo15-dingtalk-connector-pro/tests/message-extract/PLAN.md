# 消息内容提取模块（extractMessageContent）测试方案

## 1. 模块划分与职责

- **extractMessageContent(data: any): ExtractedMessage**
  - 职责：从钉钉 Stream 回调的 `data` 中根据 `msgtype` 提取统一结构 `ExtractedMessage`，供后续会话、Gateway 等使用。
  - 输入：钉钉消息体（含 `msgtype`、`text`、`content` 等）。
  - 输出：`{ text, messageType, imageUrls, downloadCodes, fileNames, atDingtalkIds, atMobiles }`。

## 2. 分支与用例矩阵（全覆盖）

### 2.1 msgtype 缺失或非预期

| 序号 | 输入 data | 期望 messageType | 期望 text | 期望 imageUrls | 期望 downloadCodes | 期望 fileNames | 期望 atDingtalkIds | 期望 atMobiles | 说明 |
|------|-----------|------------------|-----------|----------------|--------------------|----------------|--------------------|----------------|------|
| 1 | `{}` | `'text'` | `''` | `[]` | `[]` | `[]` | `[]` | `[]` | 空对象，msgtype 默认 'text' |
| 2 | `{ msgtype: undefined }` | `'text'` | `''` | `[]` | `[]` | `[]` | `[]` | `[]` | msgtype 缺失按 text 处理 |
| 3 | `{ msgtype: 'unknownType' }` | `'unknownType'` | `'[unknownType消息]'` | `[]` | `[]` | `[]` | `[]` | `[]` | default 分支 |
| 4 | `{ msgtype: null }` | `'text'` | `''` | `[]` | `[]` | `[]` | `[]` | `[]` | null 被 || 成 'text' |

### 2.2 msgtype === 'text'

| 序号 | 输入 data | 期望 text | 期望 atDingtalkIds | 期望 atMobiles | 说明 |
|------|-----------|-----------|--------------------|----------------|------|
| 5 | `{ msgtype: 'text' }` | `''` | `[]` | `[]` | 无 text.content |
| 6 | `{ msgtype: 'text', text: {} }` | `''` | `[]` | `[]` | text 无 content |
| 7 | `{ msgtype: 'text', text: { content: ' hello ' } }` | `'hello'` | `[]` | `[]` | trim 生效 |
| 8 | `{ msgtype: 'text', text: { content: 'hi', at: {} } }` | `'hi'` | `[]` | `[]` | at 为空对象 |
| 9 | `{ msgtype: 'text', text: { content: 'hi', at: { atDingtalkIds: ['id1'], atMobiles: ['13800138000'] } } }` | `'hi'` | `['id1']` | `['13800138000']` | at 完整 |
| 10 | `{ msgtype: 'text', text: { content: 'x', at: { atDingtalkIds: ['a','b'], atMobiles: [] } } }` | `'x'` | `['a','b']` | `[]` | 多个 at 用户 |
| 11 | `{ msgtype: 'text', text: { content: '' } }` | `''` | `[]` | `[]` | 空字符串 content |

### 2.3 msgtype === 'richText'

| 序号 | 输入 data | 期望 text | 期望 imageUrls | 说明 |
|------|-----------|-----------|----------------|------|
| 12 | `{ msgtype: 'richText' }` | `'[富文本消息]'` | `[]` | 无 content.richText |
| 13 | `{ msgtype: 'richText', content: {} }` | `'[富文本消息]'` | `[]` | content 空 |
| 14 | `{ msgtype: 'richText', content: { richText: [] } }` | `'[富文本消息]'` | `[]` | 空数组 |
| 15 | `{ msgtype: 'richText', content: { richText: [{ text: 'a' }, { text: 'b' }] } }` | `'ab'` | `[]` | 纯文本拼接 |
| 16 | `{ msgtype: 'richText', content: { richText: [{ pictureUrl: 'http://x/y.png' }] } }` | `'[图片]'` | `['http://x/y.png']` | 仅图片无文字 |
| 17 | `{ msgtype: 'richText', content: { richText: [{ text: 'x', pictureUrl: 'u' }] } }` | `'x'` | `['u']` | 文本+图片 |
| 18 | `{ msgtype: 'richText', content: { richText: [{ type: 'picture', downloadCode: 'code1' }] } }` | `'[图片]'` | `['downloadCode:code1']` | downloadCode 形式 |
| 19 | `{ msgtype: 'richText', content: { richText: [{ text: 't', type: 'picture', downloadCode: 'c' }] } }` | `'t'` | `['downloadCode:c']` | 文本+downloadCode 图片 |

### 2.4 msgtype === 'picture'

| 序号 | 输入 data | 期望 text | 期望 imageUrls | 期望 downloadCodes | 说明 |
|------|-----------|-----------|----------------|--------------------|------|
| 20 | `{ msgtype: 'picture' }` | `'[图片]'` | `[]` | `[]` | 无 content |
| 21 | `{ msgtype: 'picture', content: { pictureUrl: 'http://p.png' } }` | `'[图片]'` | `['http://p.png']` | `[]` | 仅 pictureUrl |
| 22 | `{ msgtype: 'picture', content: { downloadCode: 'dc1' } }` | `'[图片]'` | `[]` | `['dc1']` | 仅 downloadCode |
| 23 | `{ msgtype: 'picture', content: { pictureUrl: 'u', downloadCode: 'c' } }` | `'[图片]'` | `['u']` | `['c']` | 两者都有 |

### 2.5 msgtype === 'audio'

| 序号 | 输入 data | 期望 text | 期望 messageType | 说明 |
|------|-----------|-----------|------------------|------|
| 24 | `{ msgtype: 'audio' }` | `'[语音消息]'` | `'audio'` | 无 content.recognition |
| 25 | `{ msgtype: 'audio', content: { recognition: '转写文字' } }` | `'转写文字'` | `'audio'` | 有识别结果 |

### 2.6 msgtype === 'video'

| 序号 | 输入 data | 期望 text | 期望 messageType | 说明 |
|------|-----------|-----------|------------------|------|
| 26 | `{ msgtype: 'video' }` | `'[视频]'` | `'video'` | 无额外字段 |

### 2.7 msgtype === 'file'

| 序号 | 输入 data | 期望 text | 期望 downloadCodes | 期望 fileNames | 说明 |
|------|-----------|-----------|--------------------|----------------|------|
| 27 | `{ msgtype: 'file' }` | `'[文件: 文件]'` | `[]` | `[]` | 无 content，fileName 默认 '文件' |
| 28 | `{ msgtype: 'file', content: { fileName: 'a.pdf' } }` | `'[文件: a.pdf]'` | `[]` | `[]` | 无 downloadCode |
| 29 | `{ msgtype: 'file', content: { fileName: 'b.docx', downloadCode: 'fc1' } }` | `'[文件: b.docx]'` | `['fc1']` | `['b.docx']` | 完整 |

## 3. 预期正确输出与潜在错误

- **正确输出**：所有分支返回结构完整的 `ExtractedMessage`，无 undefined 必填字段；text 为字符串；数组均为数组类型。
- **潜在错误原因**：
  - 未对 `data.text?.content` 做 trim，导致首尾空格进入下游。
  - richText 中漏处理 `type === 'picture' && downloadCode`，导致图片未加入 imageUrls。
  - file 类型未同时 push downloadCode 与 fileName，导致下标错位。
  - default 分支未使用 msgtype 导致显示为 `[undefined消息]`。
