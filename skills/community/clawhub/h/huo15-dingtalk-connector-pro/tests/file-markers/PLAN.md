# 文件标记与音频类型模块测试方案

## 1. 模块划分与职责

- **extractFileMarkers(content: string, log?: any): { cleanedContent: string; fileInfos: FileInfo[] }**
  - 职责：从 AI 回复内容中匹配 `[DINGTALK_FILE]{...}[/DINGTALK_FILE]`，解析 JSON 得到 `{ path, fileName, fileType }`，校验 path 与 fileName 存在后收集到 fileInfos，并移除标记得到 cleanedContent。
- **isAudioFile(fileType: string): boolean**
  - 职责：判断扩展名是否为支持的音频类型（mp3, wav, amr, ogg, aac, flac, m4a），大小写不敏感。

## 2. 用例矩阵（全覆盖）

### 2.1 isAudioFile

| 序号 | 输入 fileType | 期望 | 说明 |
|------|----------------|------|------|
| 1 | `'mp3'` | true | 小写 |
| 2 | `'MP3'` | true | 大写 |
| 3 | `'Mp3'` | true | 混合 |
| 4 | `'wav'` / `'amr'` / `'ogg'` / `'aac'` / `'flac'` / `'m4a'` | true | 其余支持格式 |
| 5 | `'txt'` | false | 非音频 |
| 6 | `''` | false | 空字符串 |
| 7 | `'mp4'` | false | 视频格式 |
| 8 | `'.mp3'` | false | 带点号（代码用 includes(fileType.toLowerCase())，未 strip 点） |

### 2.2 extractFileMarkers — 无标记

| 序号 | 输入 content | 期望 cleanedContent | 期望 fileInfos | 说明 |
|------|--------------|---------------------|----------------|------|
| 9 | `''` | `''` | `[]` | 空字符串 |
| 10 | `'plain text'` | `'plain text'` | `[]` | 无标记 |
| 11 | `'[DINGTALK_FILE]'` | 原样（无闭合） | `[]` | 不匹配正则 |

### 2.3 extractFileMarkers — 合法单个标记

| 序号 | 输入 content | 期望 fileInfos[0] | 期望 cleanedContent | 说明 |
|------|--------------|-------------------|---------------------|------|
| 12 | `'hi [DINGTALK_FILE]{"path":"/tmp/a.pdf","fileName":"a.pdf","fileType":"pdf"}[/DINGTALK_FILE] end'` | path=/tmp/a.pdf, fileName=a.pdf, fileType=pdf | 'hi  end'（中间标记被移除，保留空格） | 标准格式 |
| 13 | `'[DINGTALK_FILE]{"path":"C:\\\\x.docx","fileName":"文档.docx","fileType":"docx"}[/DINGTALK_FILE]'` | path=C:\\x.docx, fileName=文档.docx, fileType=docx | '' | 反斜杠与中文文件名 |

### 2.4 extractFileMarkers — 缺 path 或 fileName 不收集

| 序号 | 输入 content | 期望 fileInfos | 说明 |
|------|--------------|----------------|------|
| 14 | `'[DINGTALK_FILE]{"path":"/x.pdf","fileName":""}[/DINGTALK_FILE]'` | `[]` | fileName 空不满足 fileInfo.path && fileInfo.fileName |
| 15 | `'[DINGTALK_FILE]{"path":"","fileName":"a.pdf"}[/DINGTALK_FILE]'` | `[]` | path 空不收集 |
| 16 | `'[DINGTALK_FILE]{"fileName":"a.pdf"}[/DINGTALK_FILE]'` | `[]` | 缺 path |
| 17 | `'[DINGTALK_FILE]{"path":"/a.pdf"}[/DINGTALK_FILE]'` | `[]` | 缺 fileName |

### 2.5 extractFileMarkers — 非法 JSON

| 序号 | 输入 content | 期望 fileInfos | 期望 cleanedContent | 说明 |
|------|--------------|----------------|---------------------|------|
| 18 | `'[DINGTALK_FILE]{invalid-json}[/DINGTALK_FILE]'` | `[]` | ''（标记仍被 replace 掉） | JSON.parse 抛错，log.warn 调用 |
| 19 | `'[DINGTALK_FILE]{}[/DINGTALK_FILE]'` | `[]` | '' | 空对象缺 path/fileName |
| 20 | `'[DINGTALK_FILE]{ "path": "/x", "fileName": "x" }[/DINGTALK_FILE]'` | `[{ path: '/x', fileName: 'x', fileType: undefined }]` | '' | 合法 JSON，fileType 可缺 |

### 2.6 extractFileMarkers — 多个标记

| 序号 | 输入 content | 期望 fileInfos.length | 期望 cleanedContent | 说明 |
|------|--------------|------------------------|---------------------|------|
| 21 | 两段合法 [DINGTALK_FILE]...[/DINGTALK_FILE] | 2 | 中间文本保留、两处标记移除 | 多文件 |
| 22 | 一段合法 + 一段非法 JSON | 1 | 两段标记都被移除 | 混合 |

### 2.7 extractFileMarkers — 边界与 trim

| 序号 | 输入 content | 期望 cleanedContent | 说明 |
|------|--------------|---------------------|------|
| 23 | `'  [DINGTALK_FILE]{"path":"/a","fileName":"a"}[/DINGTALK_FILE]  '` | `''` | 前后空格被 trim |
| 24 | `'x[DINGTALK_FILE]{"path":"/a","fileName":"a"}[/DINGTALK_FILE]y'` | `'xy'` | 中间无空格 |

## 3. 预期正确输出与潜在错误

- **正确输出**：fileInfos 仅包含 path 与 fileName 均非空的项；cleanedContent 为移除所有 FILE_MARKER 后 trim 的结果；log.info/warn 按实现调用。
- **潜在错误原因**：正则贪婪/非贪婪错误导致多匹配或少匹配；JSON.parse 未 try-catch 导致整函数抛错；校验写成 path || fileName 导致只填一个也通过；replace 后未 trim。
