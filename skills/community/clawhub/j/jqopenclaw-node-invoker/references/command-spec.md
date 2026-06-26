# JQOpenClawNode 调用规范

## 1. 通用调用骨架

统一走 `node.invoke`：

```json
{
  "method": "node.invoke",
  "params": {
    "nodeId": "<node-id>",
    "command": "<command-name>",
    "params": {},
    "timeoutMs": 30000,
    "idempotencyKey": "<uuid>"
  }
}
```

约束：
- `nodeId`、`command`、`idempotencyKey` 必填。
- `params` 可省略，省略时等价空对象。
- 每次请求使用新 UUID 作为 `idempotencyKey`。
- 节点侧接收 `node.invoke.request` 时仅解析 `paramsJSON`，且 `paramsJSON` 必须为对象 JSON。
- `paramsJSON` 缺失或 `null` 时按空对象处理；若存在但不是字符串、为空字符串、或解析后不是对象，返回 `INVALID_PARAMS`。
- `node.invoke.params.timeoutMs` 可省略；若传入，必须为非负整数（毫秒），否则返回 `INVALID_PARAMS`。其中 `0` 视为立即超时。
- `node.invoke.params.timeoutMs` 会参与请求预算裁剪。当前节点内部会将 `system.run.params.timeoutMs`、`process.exec.params.timeoutMs`（`detached=false`）与 `file.read(operation=rg)` 的内部执行超时裁剪到该预算内（取更小值）。
- 即便省略 `node.invoke.params.timeoutMs`，网关/调用端仍存在等待超时（当前 OpenClaw 侧常见默认约 `30000ms`，CLI `openclaw nodes invoke` 默认 `15000ms`）。
- 实际可用执行时长取决于最先触发的超时层：调用端/网关等待超时、`node.invoke.params.timeoutMs`（若传入）、能力内部超时。

## 2. file.read

用途：读取文件内容、按行区间、目录遍历、元信息、计算文件 MD5，或执行 `rg` 搜索。

`params`：
- `path`：字符串，必填。
- `operation`：字符串，可选，默认 `read`。可选值：`read` / `lines` / `list` / `rg` / `stat` / `md5`。
- `read` 模式参数：
  - `encoding`：字符串，可选，`utf8`（默认）或 `base64`。
  - `maxBytes`：整数，可选，默认 `1048576`，范围 `[1, 2097152]`。
  - `offsetBytes`（或 `offset`）：整数，可选，默认 `0`。用于分块读取起始偏移量，范围 `[0, sizeBytes]`。
- `lines` 模式参数：
  - `startLine`（或 `fromLine`）：整数，必填，1-based 起始行号。
  - `endLine`（或 `toLine`）：整数，必填，1-based 结束行号（含）。
  - `encoding`：仅支持 `utf8`（默认）。
  - 行区间跨度限制：`endLine - startLine + 1` 需在 `[1, 50000]`。
- `list` 模式参数：
  - `includeEntries`：布尔，可选，默认 `true`。是否返回目录项列表。
  - `maxEntries`：整数，可选，默认 `200`，范围 `[1, 5000]`。仅在 `includeEntries=true` 时生效。
  - `recursive`：布尔，可选，默认 `false`。是否递归遍历子目录。
  - `includeHidden`：布尔，可选，默认 `true`。是否包含隐藏/系统项。
  - `glob`：字符串或字符串数组，可选。按文件名或相对路径通配过滤（支持 `*`、`?`）。
- `rg` 模式参数：
  - `pattern`：字符串，必填。
  - `maxMatches`：整数，可选，默认 `200`，范围 `[1, 5000]`。
  - `caseSensitive`：布尔，可选，默认 `false`。
  - `includeHidden`：布尔，可选，默认 `false`。
  - `literal`：布尔，可选，默认 `false`（固定字符串匹配）。
  - 内部执行超时：默认 `60000ms`，若设置了 `node.invoke.timeoutMs`（含 `0`），实际超时为二者较小值。
- `stat` 模式参数：
  - 无额外必填参数。
- `md5` 模式参数：
  - 无额外必填参数。

示例：

```json
{
  "method": "node.invoke",
  "params": {
    "nodeId": "<node-id>",
    "command": "file.read",
    "params": {
      "operation": "read",
      "path": "C:/Windows/win.ini",
      "encoding": "utf8",
      "offsetBytes": 0,
      "maxBytes": 8192
    },
    "timeoutMs": 15000,
    "idempotencyKey": "<uuid>"
  }
}
```

示例（list 模式）：

```json
{
  "method": "node.invoke",
  "params": {
    "nodeId": "<node-id>",
    "command": "file.read",
    "params": {
      "operation": "list",
      "path": "C:/Temp",
      "recursive": true,
      "glob": ["*.log", "logs/*"],
      "includeHidden": false,
      "includeEntries": true,
      "maxEntries": 200
    },
    "timeoutMs": 15000,
    "idempotencyKey": "<uuid>"
  }
}
```

示例（lines 模式）：

```json
{
  "method": "node.invoke",
  "params": {
    "nodeId": "<node-id>",
    "command": "file.read",
    "params": {
      "operation": "lines",
      "path": "C:/Repos/project/src/main.cpp",
      "startLine": 120,
      "endLine": 160
    },
    "timeoutMs": 15000,
    "idempotencyKey": "<uuid>"
  }
}
```

示例（rg 模式）：

```json
{
  "method": "node.invoke",
  "params": {
    "nodeId": "<node-id>",
    "command": "file.read",
    "params": {
      "operation": "rg",
      "path": "C:/Repos/project",
      "pattern": "TODO",
      "maxMatches": 200
    },
    "timeoutMs": 30000,
    "idempotencyKey": "<uuid>"
  }
}
```

示例（stat 模式）：

```json
{
  "method": "node.invoke",
  "params": {
    "nodeId": "<node-id>",
    "command": "file.read",
    "params": {
      "operation": "stat",
      "path": "C:/Temp/app.log"
    },
    "timeoutMs": 15000,
    "idempotencyKey": "<uuid>"
  }
}
```

示例（md5 模式）：

```json
{
  "method": "node.invoke",
  "params": {
    "nodeId": "<node-id>",
    "command": "file.read",
    "params": {
      "operation": "md5",
      "path": "C:/Temp/app.log"
    },
    "timeoutMs": 15000,
    "idempotencyKey": "<uuid>"
  }
}
```

返回重点（payload）：
- 公共字段：
  - `path`
  - `operation`
  - `targetType`：`file` 或 `directory`
- `read` 模式字段：
  - `encoding`
  - `sizeBytes`
  - `offsetBytes`
  - `nextOffsetBytes`
  - `readBytes`
  - `hasMore`
  - `eof`
  - `truncated`
  - `content`
- `lines` 模式字段：
  - `encoding`（固定 `utf8`）
  - `startLine`
  - `endLine`
  - `returnedLineCount`
  - `hasMore`
  - `eof`
  - `content`（按 `\n` 拼接）
  - `lines`（数组元素字段：`lineNumber`、`text`）
- `list` 模式字段：
  - `recursive`
  - `includeHidden`
  - `glob`（可选，数组）
  - `directoryCount`
  - `fileCount`
  - `otherCount`
  - `totalCount`
  - `includeEntries`
  - `maxEntries`（仅 `includeEntries=true` 返回）
  - `truncated`（仅 `includeEntries=true` 返回）
  - `entries`（仅 `includeEntries=true` 返回，元素字段：`name`、`path`、`relativePath`、`type`、`isSymLink`、`sizeBytes`[文件项才有]）
- `rg` 模式字段：
  - `pattern`
  - `caseSensitive`
  - `includeHidden`
  - `literal`
  - `maxMatches`
  - `matchCount`
  - `fileCount`
  - `truncated`
  - `searchBackend`（`rg` 或 `powershell.select-string`）
  - `searchExitCode`
  - `stderr`（可选）
  - `matches`（数组元素字段：`path`、`lineNumber`、`columnStart`、`columnEnd`、`lineText`、`matchText`）
- `stat` 模式字段：
  - `name`
  - `isFile` / `isDir` / `isSymLink` / `isHidden`
  - `isReadable` / `isWritable` / `isExecutable`
  - `sizeBytes`（文件时返回）
  - `owner`（`name`、`id`、`group`、`groupId`）
  - `permissions`（owner/group/other 的 read/write/execute）
  - `timestamps`（`accessTime`、`birthTime`、`modificationTime`、`metadataChangeTime`，各含 `iso8601`、`epochMs`）
- `md5` 模式字段：
  - `algorithm`：固定 `md5`
  - `sizeBytes`
  - `md5`（32 位小写十六进制摘要）

## 3. file.write

用途：写入文件内容，或执行移动（剪切）/删除/目录增删操作。

`params`：
- `path`：字符串，必填。
- `allowWrite`：布尔，可选，默认 `false`。必须显式传 `true` 才允许执行 `file.write`。
- `operation`：字符串，可选，默认 `write`。可选值：`write` / `move`（或 `cut`）/ `delete`（或 `remove`）/ `mkdir`（或 `createDir`）/ `rmdir`（或 `removeDir`）。
- `write` 模式参数：
  - `content`：字符串，必填。
  - `encoding`：字符串，可选，`utf8`（默认）或 `base64`。
  - `append`：布尔，可选，默认 `false`。
  - `createDirs`：布尔，可选，默认 `true`。
- `move` 模式参数：
  - `destinationPath` 或 `toPath`：字符串，必填（目标路径）。
  - `overwrite`：布尔，可选，默认 `false`（目标存在时是否覆盖）。
  - `createDirs`：布尔，可选，默认 `true`（自动创建目标父目录）。
- `delete` 模式参数：
  - 无额外必填参数。删除行为固定为移动到回收站（`QFile::moveToTrash`）。
- `mkdir` 模式参数：
  - `createDirs`：布尔，可选，默认 `true`（是否递归创建父目录）。
- `rmdir` 模式参数：
  - 无额外必填参数。仅允许删除目录，删除行为固定为移动到回收站（`QFile::moveToTrash`）。

示例：

```json
{
  "method": "node.invoke",
  "params": {
    "nodeId": "<node-id>",
    "command": "file.write",
    "params": {
      "allowWrite": true,
      "operation": "write",
      "path": "C:/Temp/jqopenclaw-output.txt",
      "content": "hello from node",
      "encoding": "utf8",
      "append": false,
      "createDirs": true
    },
    "timeoutMs": 15000,
    "idempotencyKey": "<uuid>"
  }
}
```

示例（move 模式）：

```json
{
  "method": "node.invoke",
  "params": {
    "nodeId": "<node-id>",
    "command": "file.write",
    "params": {
      "allowWrite": true,
      "operation": "move",
      "path": "C:/Temp/a.txt",
      "destinationPath": "C:/Temp/archive/a.txt",
      "overwrite": true
    },
    "timeoutMs": 15000,
    "idempotencyKey": "<uuid>"
  }
}
```

示例（delete 模式）：

```json
{
  "method": "node.invoke",
  "params": {
    "nodeId": "<node-id>",
    "command": "file.write",
    "params": {
      "allowWrite": true,
      "operation": "delete",
      "path": "C:/Temp/old-data"
    },
    "timeoutMs": 15000,
    "idempotencyKey": "<uuid>"
  }
}
```

返回重点（payload）：
- 公共字段：
  - `operation`
  - `path`
- `write` 模式字段：
  - `encoding`
  - `appended`
  - `bytesWritten`
  - `sizeBytes`
- `move` 模式字段：
  - `fromPath`
  - `toPath`
  - `targetType`：`file` 或 `directory`
  - `overwritten`
  - `moved`
- `delete` 模式字段：
  - `targetType`：`file` 或 `directory`
  - `deleted`
  - `deleteMode`：固定 `trash`
- `mkdir` 模式字段：
  - `targetType`：固定 `directory`
  - `created`
  - `existed`
- `rmdir` 模式字段：
  - `targetType`：固定 `directory`
  - `deleted`
  - `deleteMode`：固定 `trash`

## 4. process.exec

用途：兼容历史调用方的进程执行能力，使用 `program + arguments` 参数模型（支持 `detached`）。

`params`：
- `program`：字符串，必填。
- `arguments`：字符串数组，可选。
- `workingDirectory`：字符串，可选。
- `environment`：对象，可选。
- `inheritEnvironment`：布尔，可选，默认 `true`。
- `timeoutMs`：数字，可选，默认 `30000`，范围 `[100, 300000]`。
- `stdin`：字符串，可选。
- `mergeChannels`：布尔，可选，默认 `false`。
- `detached`：布尔，可选，默认 `false`。
- 约束：`detached=true` 时不支持 `stdin` 与 `mergeChannels=true`。
- 超时裁剪：若设置了 `node.invoke.timeoutMs`（含 `0`），且 `detached=false`，实际执行超时为 `min(process.exec.params.timeoutMs, node.invoke.timeoutMs)`。

示例：

```json
{
  "method": "node.invoke",
  "params": {
    "nodeId": "<node-id>",
    "command": "process.exec",
    "params": {
      "program": "cmd.exe",
      "arguments": ["/c", "echo", "hello"],
      "detached": false,
      "timeoutMs": 15000
    },
    "timeoutMs": 20000,
    "idempotencyKey": "<uuid>"
  }
}
```

返回重点（payload）：
- `program`
- `arguments`
- `workingDirectory`
- `timeoutMs`
- `elapsedMs`
- `detached`
- `timedOut`
- `exitCode`
- `exitStatus`
- `stdout`
- `stderr`
- `ok`
- `resultClass`：`ok` / `non_zero_exit` / `crash` / `timeout` / `detached`

## 4.1 system.run

用途：对齐 OpenClaw 的 `system.run` 参数模型（command-first）。

`params`：
- `command`：字符串数组，必填。首元素为程序名，后续元素为参数。
- `rawCommand`：字符串，可选（展示/审批文本）。
- `cwd`：字符串，可选。
- `env`：对象，可选。
- `timeoutMs`：数字，可选，默认 `30000`，范围 `[100, 300000]`。
- `needsScreenRecording`：布尔，可选，默认 `false`。
- 超时裁剪：若设置了 `node.invoke.timeoutMs`（含 `0`），实际执行超时为 `min(system.run.params.timeoutMs, node.invoke.timeoutMs)`。

说明：
- 不再支持 `program` / `arguments` / `detached` / `commandTimeoutMs` / `workingDirectory` / `environment` 参数写法。

示例：

```json
{
  "method": "node.invoke",
  "params": {
    "nodeId": "<node-id>",
    "command": "system.run",
    "params": {
      "command": ["ping", "127.0.0.1", "-n", "2"],
      "rawCommand": "ping 127.0.0.1 -n 2",
      "cwd": "C:/",
      "timeoutMs": 15000
    },
    "timeoutMs": 20000,
    "idempotencyKey": "<uuid>"
  }
}
```

返回重点（payload）：
- `program`
- `arguments`
- `rawCommand`
- `workingDirectory`
- `timeoutMs`
- `elapsedMs`
- `needsScreenRecording`
- `timedOut`
- `exitCode`
- `exitStatus`
- `stdout`
- `stderr`
- `ok`
- `resultClass`：`ok` / `non_zero_exit` / `crash` / `timeout`

## 5. process.which

用途：探测命令在节点环境中是否可执行，并返回可用路径。

`params`：
- `program`：字符串，可选。单个命令名。
- `programs`：字符串数组，可选。批量命令名列表。
- 约束：
  - `program` 与 `programs` 至少提供一个。
  - `programs` 长度范围 `[1, 200]`。
  - 若同时提供，节点会合并去重后统一探测。

示例：

```json
{
  "method": "node.invoke",
  "params": {
    "nodeId": "<node-id>",
    "command": "process.which",
    "params": {
      "programs": ["git", "python", "ffmpeg"]
    },
    "timeoutMs": 15000,
    "idempotencyKey": "<uuid>"
  }
}
```

返回重点（payload）：
- `operation`：固定 `which`
- `requestedCount` / `foundCount` / `allFound`
- `results`：数组元素字段：
  - `program`
  - `backend`（`where` / `which` / `qt.findExecutable`）
  - `found`
  - `path`（仅命中时返回）
  - `allPaths`

兼容字段（仅单命令时返回）：
- `program` / `backend` / `found` / `path` / `allPaths`

## 6. process.manage

用途：进程管理（当前仅支持 Windows），支持进程列表、搜索和终止。

`params`：
- `operation`：字符串，可选，默认 `list`。可选值：`list` / `search` / `kill`。
- `list` 与 `search` 通用参数：
  - `query`：字符串，可选。搜索关键字。
  - `keyword`：字符串，可选。`query` 的兼容别名（仅在 `query` 为空时生效）。
  - `pid`：数字，可选，范围 `[1, 2147483647]`。作为 PID 精确过滤条件。
  - `caseSensitive`：布尔，可选，默认 `false`。
  - `limit`：数字，可选，默认 `300`，范围 `[1, 5000]`。
  - `includePath`：布尔，可选，默认 `false`。是否返回进程路径，并允许 `query` 匹配路径。
  - `includeArchitecture`：布尔，可选，默认 `false`。是否返回 `isWow64` 字段（Windows）。
- `search` 额外约束：
  - 必须提供 `query`（或 `keyword`）与 `pid` 之一，否则返回 `INVALID_PARAMS`。
- `kill` 参数：
  - `pid`：数字，必填，范围 `[1, 2147483647]`。
  - `waitMs`：数字，可选，默认 `3000`，范围 `[0, 30000]`。
  - `force`：布尔，可选，默认 `true`。`true` 表示强制终止；`false` 表示发送非强杀退出请求（仅对具有顶层窗口的进程生效）。
  - 注意：`waitMs` 当前不会被 `node.invoke.timeoutMs` 二次裁剪，调用端应自行保证请求预算充足。
  - 默认拒绝终止关键进程（critical process）；仅当 `pid` 等于当前节点进程 PID 时允许。

示例（search 模式）：

```json
{
  "method": "node.invoke",
  "params": {
    "nodeId": "<node-id>",
    "command": "process.manage",
    "params": {
      "operation": "search",
      "query": "chrome",
      "limit": 20,
      "includePath": true
    },
    "timeoutMs": 15000,
    "idempotencyKey": "<uuid>"
  }
}
```

示例（kill 模式）：

```json
{
  "method": "node.invoke",
  "params": {
    "nodeId": "<node-id>",
    "command": "process.manage",
    "params": {
      "operation": "kill",
      "pid": 12345,
      "waitMs": 5000,
      "force": true
    },
    "timeoutMs": 10000,
    "idempotencyKey": "<uuid>"
  }
}
```

返回重点（payload）：
- `list` / `search` 返回字段：
  - `operation` / `query`（可选）/ `pid`（可选）/ `caseSensitive` / `limit`
  - `includePath` / `includeArchitecture`
  - `returnedCount` / `totalMatched` / `truncated`
  - `processes`：数组元素字段包含
    - `pid`
    - `name`
    - `sessionId`（可选）
    - `path`（可选）
    - `isWow64`（可选）
- `kill` 返回字段：
  - `operation` / `pid`
  - `name`（可选）/ `path`（可选）/ `isWow64`（可选）
  - `force` / `waitMs` / `waitResult` / `terminated` / `exited` / `resultClass`
  - `exitCode`（可选）
  - `waitResult` 取值：`signaled` / `timeout` / `abandoned` / `unknown`。

## 7. system.screenshot

用途：采集全部屏幕截图并返回上传后的 URL 信息。

返回重点（payload 数组元素）：
- `format`
- `mimeType`
- `url`
- `width`
- `height`
- `screenIndex`
- `screenName`（可选）

## 8. system.info

用途：采集系统基础信息。

返回重点（payload）：
- `cpuName`
- `cpuCores`
- `cpuThreads`
- `computerName`
- `hostName`
- `osName`
- `osVersion`
- `userName`
- `memory`
- `gpuNames`
- `ip`
- `disks`

## 9. system.notify

用途：弹出系统消息提示框。参数校验通过后会异步投递弹窗请求，`node.invoke` 会立即返回。

参数（`params`）：
- `message`：字符串，必填，非空，长度范围 `[1, 4000]`
- `title`：字符串，可选，默认 `JQOpenClaw`，长度上限 `120`

返回（`payload`）：
- `operation`：固定 `notify`
- `title`
- `message`
- `shown`：固定 `true`
- `async`：固定 `true`
- `ok`：固定 `true`

## 10. system.clipboard

用途：读取当前系统剪贴板文本，或写入文本到系统剪贴板。建议 `timeoutMs` 取值 `5000-15000`。

参数（`params`）：
- `operation`：字符串，可选，`read|write`，默认 `read`
- `text`：字符串，当 `operation=write` 时必填（可为空字符串）

返回（`payload`）：
- `operation=read`：
  - `operation`：固定 `read`
  - `text`
  - `length`
  - `hasText`
  - `ok`：固定 `true`
- `operation=write`：
  - `operation`：固定 `write`
  - `written`：固定 `true`
  - `length`
  - `hasText`
  - `ok`：固定 `true`

示例（读取剪贴板）：

```json
{
  "method": "node.invoke",
  "params": {
    "nodeId": "<node-id>",
    "command": "system.clipboard",
    "params": {
      "operation": "read"
    },
    "timeoutMs": 10000,
    "idempotencyKey": "<uuid>"
  }
}
```

示例（写入剪贴板）：

```json
{
  "method": "node.invoke",
  "params": {
    "nodeId": "<node-id>",
    "command": "system.clipboard",
    "params": {
      "operation": "write",
      "text": "hello from openclaw"
    },
    "timeoutMs": 10000,
    "idempotencyKey": "<uuid>"
  }
}
```

## 11. node.selfUpdate

用途：执行节点自更新。流程为参数校验 -> 当前程序 MD5 比对 -> HTTP 下载 -> 下载包 MD5 比对 -> 写入临时文件 -> 生成并启动更新 bat -> `node.invoke` 回包后延迟退出当前节点。

`params`：
- `downloadUrl`：字符串，必填。新版本程序完整下载地址（仅支持 `http/https`）。
- `md5`：字符串，必填。32 位十六进制 MD5；若与当前程序一致，返回无需更新。

返回重点（`payload`）：
- 无需更新：
  - `operation=selfUpdate`
  - `updated=false`
  - `reason=md5_unchanged`
  - `currentMd5`
  - `expectedMd5`
- 进入更新流程：
  - `operation=selfUpdate`
  - `updated=true`
  - `downloadUrl`
  - `downloadedMd5`
  - `expectedMd5`
  - `willExit=true`
  - `status=exiting_for_self_update`

注意：
- 下载临时文件使用 UUID 文件名，不带 `.exe` 后缀。
- 更新 bat 会自动删除临时文件和 bat 本身。

## 12. 常见错误与处理

- `INVALID_PARAMS`
  - 参数缺失、类型不匹配或超出范围（含 `file.read` / `file.write` / `process.exec` / `process.manage` / `system.run` / `process.which` / `system.notify` / `system.clipboard` / `system.input` / `node.selfUpdate` 参数校验失败，例如 `node.selfUpdate` 缺失必填 `md5`）。
  - 修正字段后重试。

- `FILE_READ_FAILED` / `FILE_WRITE_FAILED`
  - 常见原因：路径错误、权限不足、父目录不存在、移动目标已存在、系统回收站不可用或拒绝接收目标。
  - 优先检查路径、权限、目录状态、回收站状态等执行环境问题。

- `PROCESS_EXEC_FAILED`
  - 常见原因：程序不存在、权限不足、启动失败等无法产出结构化执行结果。
  - 优先检查 `program`、`workingDirectory`、权限、运行环境。

- `PROCESS_MANAGE_FAILED`
  - 常见原因：目标进程不存在、权限不足、非 Windows 平台、命中关键进程保护、终止失败或等待失败。
  - 优先检查 `pid`、节点运行权限、平台类型与目标进程存活状态。

- `SYSTEM_RUN_FAILED`
  - 常见原因：命令数组非法、程序不存在、权限不足、启动失败等无法产出结构化执行结果。
  - 优先检查 `command`、`cwd`、权限、运行环境。

- `PROCESS_WHICH_FAILED`
  - 常见原因：探测流程内部异常。
  - 建议检查节点日志并重试。

- `SYSTEM_INFO_FAILED`
  - 系统信息采集失败。

- `SCREENSHOT_CAPTURE_FAILED`
  - 截图采集阶段失败（未进入上传）。

- `SCREENSHOT_UPLOAD_FAILED`
  - 截图已采集但全部上传失败。

- `TIMEOUT`
  - `node.invoke` 请求级超时（网关等待节点结果超时），或显式传入 `timeoutMs=0` 导致立即超时。
  - 增大 `timeoutMs` 或缩小执行范围。

- `COMMAND_NOT_SUPPORTED`
  - 节点未实现该命令。
  - 检查 `node.describe.commands`。
- `SYSTEM_INPUT_FAILED`
  - `system.input` 请求投递失败（例如线程池不可用、平台不支持）。
- `SYSTEM_NOTIFY_FAILED`
  - `system.notify` 请求投递失败（如应用实例不可用、UI 线程分发失败）。
- `SYSTEM_CLIPBOARD_FAILED`
  - `system.clipboard` 执行失败（如应用实例不可用、图形环境缺失、剪贴板访问失败）。
- `NODE_SELF_UPDATE_FAILED`
  - `node.selfUpdate` 执行失败（下载失败、HTTP 状态异常、临时文件写入失败、更新脚本启动失败等）。
- `NODE_SELF_UPDATE_MD5_MISMATCH`
  - `node.selfUpdate` 下载成功但 MD5 校验不匹配。
- `command not allowlisted`
  - 网关策略拦截。
  - 在网关配置 `gateway.nodes.allowCommands` 增加目标命令（如 `file.read`、`file.write`、`process.exec`、`process.manage`、`system.run`、`process.which`、`system.notify`、`system.clipboard`、`system.input`、`node.selfUpdate`）。

## 13. system.input

用途：控制鼠标与键盘输入，支持一个请求内多动作顺序执行。
说明：参数校验通过后请求会异步入队，`node.invoke` 立即返回，不等待动作执行完成。
调度策略：latest-wins。若新请求到达，会取消旧请求尚未完成的剩余动作；已执行动作不会回滚。
建议：`keyboard.down` / `keyboard.up` 尽量在同一请求内闭合配对，或优先使用 `keyboard.tap`。

参数（`params`）：
- `actions`：数组，必填，长度 `[1, 1000]`
- `actions[i].type` 支持：
  - `mouse.move`：`mode=absolute|relative`，`x`，`y`
  - `mouse.click`：`button=left|right`，可选 `count`
  - `mouse.scroll`：`delta|deltaY`（二选一，范围 `[-12000, 12000]`），可选 `deltaX`（范围 `[-12000, 12000]`）
  - `mouse.drag`：`mode=absolute|relative`，`x`，`y`，可选 `button=left|right`
  - `keyboard.down` / `keyboard.up` / `keyboard.tap`：`key`
  - `keyboard.text`：`text`（非空），可选 `intervalMs`
  - `delay`：`ms`

返回（`payload`）：
- `operation`：固定 `input`
- `totalCount`
- `accepted`：固定 `true`
- `async`：固定 `true`
- `ok`：固定 `true`

示例：

```json
{
  "method": "node.invoke",
  "params": {
    "nodeId": "<node-id>",
    "command": "system.input",
    "params": {
      "actions": [
        { "type": "mouse.move", "mode": "absolute", "x": 1200, "y": 700 },
        { "type": "mouse.click", "button": "left" },
        { "type": "mouse.scroll", "deltaY": -120, "deltaX": 0 },
        { "type": "mouse.drag", "mode": "absolute", "x": 1400, "y": 700, "button": "left" },
        { "type": "delay", "ms": 150 },
        { "type": "keyboard.text", "text": "OpenClaw", "intervalMs": 20 }
      ]
    },
    "timeoutMs": 15000,
    "idempotencyKey": "<uuid>"
  }
}
```
