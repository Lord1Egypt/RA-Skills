# 视频标记模块测试方案

## 1. 模块划分与职责

- **processVideoMarkers(content, webhook, config, oapiToken, log)**  
  解析并处理文本中的 `[DINGTALK_VIDEO]{...}[/DINGTALK_VIDEO]` 标记：
  - 在 `oapiToken` 为空或不存在合法标记时 **跳过处理并保留原文**（仅记录日志）；
  - 解析出合法 JSON（含 `path`）时，根据实现尝试上传/发送或给出友好提示，再从文本中移除标记。

> 本套件通过 `plugin.__testables.processVideoMarkers` 进行测试。

## 2. 已覆盖用例（与 `video.test.ts` 对齐）

### 2.1 控制流与异常路径

| 序号 | 场景 | 输入 content | oapiToken | 期望 | 说明 |
|------|------|--------------|----------|------|------|
| 1 | 无 token 跳过处理 | `'hello [DINGTALK_VIDEO]{"path":"/tmp/a.mp4"}[/DINGTALK_VIDEO]'` | `null` | 返回原文（含标记），记录 warn | oapiToken 为空直接 bypass |
| 2 | 无标记直接返回 | `'plain text without markers'` | `'token'` | 返回原文 | 无匹配时不做任何修改 |
| 3 | 非法 JSON 标记 | `'text [DINGTALK_VIDEO]{invalid-json}[/DINGTALK_VIDEO]'` | `'token'` | 返回 `'text'`，记录 warn | 解析失败时安全移除标记 |

## 3. 待补充用例（未来可选）

> 以下为尚未在当前 `video.test.ts` 中覆盖、但实现可能支持的场景，供后续扩展使用。

| 序号 | 场景 | 输入 content | 期望 |
|------|------|--------------|------|
| P1 | 多个合法视频标记 | 含 2 个以上 `[DINGTALK_VIDEO]` | 所有标记均被识别并按顺序处理/移除 |
| P2 | JSON 缺少 path 字段 | `'[DINGTALK_VIDEO]{}[/DINGTALK_VIDEO]'` | 不抛异常，记录 warn，并移除标记或原样保留（以实现为准） |

# 视频标记处理模块测试方案（完整设计，单测仅覆盖部分路径）

## 1. 模块划分与职责

- **processVideoMarkers**
  - 从 AI 回复内容中提取 `[DINGTALK_VIDEO]{...}[/DINGTALK_VIDEO]` 片段：
    - 校验视频文件是否存在
    - 使用 ffmpeg 提取视频元数据（时长、分辨率）
    - 生成封面截图并上传
    - 通过会话 webhook 或主动消息 API 发送视频消息
    - 清理临时文件与标记文本，并在原回复后追加状态提示
- **关联辅助函数（在本方案中作为依赖）**
  - `extractVideoMetadata`：调用 ffprobe 获取时长与分辨率
  - `extractVideoThumbnail`：按指定尺寸生成封面图
  - `uploadMediaToDingTalk`：上传视频与封面至钉钉媒体服务
  - `sendVideoMessage` / `sendVideoProactive`：根据配置发送视频消息

## 2. 测试用例覆盖

> 由于视频处理链路涉及 ffmpeg / 文件系统 / 网络调用，当前单元测试主要集中在 **控制流与异常路径**，重 I/O 场景建议在集成测试中验证。

### 2.1 无 Token 情况

- **输入**
  - `content = "hello [DINGTALK_VIDEO]{\"path\":\"/tmp/a.mp4\"}[/DINGTALK_VIDEO]"`
  - `oapiToken = null`
- **期望**
  - 函数检测到无 token 后直接跳过上传逻辑，并返回原始 content（不做替换/删除）：
    - 日志：`warn` 提示“无 oapiToken，跳过视频处理”
    - 返回内容：等于输入（包含原始标记）
- **可能错误输出原因**
  - 若期望“无 token 也要移除标记”，需在实现中调整策略；当前单测按“原样返回”约定。

### 2.2 无标记内容

- **输入**
  - `content = "plain text without markers"`
  - `oapiToken = "token"`
- **期望**
  - `processVideoMarkers` 不进行任何处理，直接返回原文：
    - 输出等于输入
    - 日志：`info` 提示“未检测到视频标记”
- **可能错误输出原因**
  - 错误的正则表达式匹配导致误删普通文本。

### 2.3 非法 JSON 标记

- **输入**
  - `content = "text [DINGTALK_VIDEO]{invalid-json}[/DINGTALK_VIDEO]"`
  - `oapiToken = "token"`
- **期望**
  - 在解析 JSON 失败时：
    - 捕获异常并通过 `log.warn` 记录“解析标记失败”
    - 移除对应标记，保留正常文本部分：`"text"`
- **可能错误输出原因**
  - 对 `JSON.parse` 异常未做捕获，导致整条消息处理失败。

### 2.4 正常处理流程（方案设计，待在集成测试中补充）

1. **文件存在性校验**
   - 若文件不存在：记录 `warn` 并在状态提示中附加 `⚠️ 视频文件不存在: <文件名>`
2. **提取元数据**
   - `extractVideoMetadata` 返回 `duration > 0` 且 `width/height` 合理
3. **生成封面图**
   - 调用 `extractVideoThumbnail`，生成的本地路径随后交给 `uploadMediaToDingTalk`
4. **上传视频与封面**
   - 视频上传超过 `MAX_VIDEO_SIZE` 时，应在状态提示中标记“文件可能超过 20MB 限制”
5. **发送消息**
   - 根据 `useProactiveApi` 与 `target` 分支选择 `sendVideoMessage` 或 `sendVideoProactive`
6. **临时文件清理**
   - 不论成功或失败，在 `finally` 中尝试 `fs.unlinkSync` 删除封面文件，忽略删除失败异常

## 3. 预期正确输出与潜在错误

- **正确输出**
  - 用户只需在回复末尾标记本地视频路径，插件自动完成：
    - 元数据提取
    - 封面生成与上传
    - 视频消息发送
    - 状态提示汇总
  - 当配置或运行环境不满足条件（无 token、文件不存在、ffmpeg 不可用）时，能够优雅降级，仅通过文本提示说明问题，而不会导致整个消息失败。
- **潜在错误输出原因**
  - 正则匹配过于宽松，误匹配其他方括号语法。
  - 异常路径未统一清理临时文件，长期运行产生大量垃圾文件。
  - 对 `useProactiveApi` 与 `target` 参数校验不足，导致主动消息 API 调用失败。

当前 `video.test.ts` 已对 “无 token”、"无标记"、"非法 JSON 标记" 三类核心控制流路径进行了自动化测试，保证在高并发 Stream 回调场景下不会因异常数据导致整条消息管道中断。后续可在本目录继续扩展 I/O 相关用例，覆盖所有成功链路与失败分支。 

