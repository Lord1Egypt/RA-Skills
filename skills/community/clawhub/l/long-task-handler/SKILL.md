# Long Task Handler - 长任务处理技能

## 触发条件

当用户任务符合以下特征时激活此技能：

1. **预计耗时 > 30 秒** 的任务（编译、部署、大数据处理、模型训练等）
2. **需要进度反馈** 的任务（用户需要知道进展）
3. **可能阻塞队列** 的任务（会影响其他用户请求）
4. 用户明确要求"后台运行"、"别阻塞"、"慢慢跑"等

触发关键词：
- "长任务"、"耗时"、"后台运行"、"别等我"
- "跑完告诉我"、"有进展通知我"
- 编译、部署、训练、处理大量数据等场景

## 核心机制

### 1. 任务分流架构

```
用户请求 → 立即确认 → 后台 exec → 定期轮询 → 进展推送 → 完成通知
            ↓           ↓          ↓          ↓          ↓
         (1 秒内)   (不阻塞)   (30 秒间隔)  (实时)    (自动)
```

### 2. 三层处理策略

| 任务类型 | 处理方式 | 工具 |
|----------|----------|------|
| 短任务 (<30 秒) | 直接执行 | `exec` 前台 |
| 中长任务 (30 秒 -5 分) | 后台执行 + 定期轮询 | `exec background` + `process poll` |
| 长任务 (>5 分) | 子代理隔离 + 进度推送 | `sessions_spawn` + `message` |

## 执行流程

### Step 1: 任务评估

```javascript
function assessTask(command) {
  // 预估耗时因素
  const longTaskIndicators = [
    /compile|build|deploy/i,
    /train|fine-tune/i,
    /process.*data|migration/i,
    /export|backup.*large/i,
    /\b(ffmpeg|docker|webpack|tsc)\b/,
    /test.*--coverage|--all/i,
  ];
  
  // 检查是否有超时/后台标记
  const hasTimeout = /--timeout|-t\s*\d+/.test(command);
  const isBackground = /&$|nohup|background/.test(command);
  
  // 返回评估结果
  return {
    estimatedDuration: 'short' | 'medium' | 'long',
    shouldBackground: boolean,
    needsProgressReporting: boolean
  };
}
```

### Step 2: 立即确认

**必须**在 5 秒内给用户确认回复：

```
🫡 收到！这个任务预计需要 X 分钟，我会在后台运行。

任务：[任务简述]
预计耗时：X 分钟
通知方式：每 30 秒报告进展，完成后立即通知

你可以继续问我其他问题，不用等这个任务完成~
```

### Step 3: 后台启动

```javascript
const { sessionId } = await exec({
  command: taskCommand,
  background: true,
  yieldMs: 2000,      // 2 秒后切到后台
  timeout: timeoutSeconds || 3600,  // 默认 1 小时超时
  workdir: workspaceDir
});
```

### Step 4: 进度监控循环

```javascript
const monitorProgress = async (sessionId, options = {}) => {
  const {
    pollIntervalMs = 30000,  // 30 秒轮询
    reportNoChange = false,   // 无变化是否报告
    maxSilentMinutes = 5      // 最大静默时间
  } = options;
  
  let lastOutput = '';
  let silentSince = Date.now();
  
  const interval = setInterval(async () => {
    const result = await process({
      action: 'poll',
      sessionId
    });
    
    // 检查是否有新输出
    if (result.output && result.output !== lastOutput) {
      const newLines = result.output.slice(lastOutput.length);
      if (newLines.trim()) {
        await message({
          channel: 'feishu',
          message: `📊 任务进展:\n\`\`\`\n${newLines.slice(-500)}\n\`\`\``
        });
        lastOutput = result.output;
        silentSince = Date.now();
      }
    }
    
    // 检查静默超时
    if (Date.now() - silentSince > maxSilentMinutes * 60000) {
      await message({
        message: `⚠️ 任务已静默运行 ${maxSilentMinutes} 分钟，仍在进行中...`
      });
      silentSince = Date.now();  // 重置计时
    }
    
    // 检查是否完成
    if (result.exitCode !== null) {
      clearInterval(interval);
      await notifyCompletion(sessionId, result);
    }
  }, pollIntervalMs);
  
  return interval;
};
```

### Step 5: 完成通知

```javascript
const notifyCompletion = async (sessionId, result) => {
  const fullLog = await process({
    action: 'log',
    sessionId,
    limit: 100
  });
  
  const status = result.exitCode === 0 ? '✅' : '❌';
  const duration = formatDuration(result.durationMs);
  
  await message({
    channel: 'feishu',
    message: `${status} **任务完成!**
    
耗时：${duration}
退出码：${result.exitCode}

${result.exitCode === 0 ? '🎉 一切顺利!' : '⚠️ 任务失败，请检查日志'}

${fullLog.output ? '最近输出:\n```\n' + fullLog.output.slice(-1000) + '\n```' : ''}`
  });
};
```

## 配置参数

在 `openclaw.json` 中添加:

```json5
{
  skills: {
    "long-task-handler": {
      enabled: true,
      defaultTimeoutSeconds: 3600,    // 默认 1 小时超时
      pollIntervalSeconds: 30,        // 轮询间隔
      progressReportThreshold: 30,    // 超过 30 秒的任务才报告进展
      maxConcurrentLongTasks: 3,      // 最多并行长任务数
      notifyOnExit: true,             // 完成时自动通知
      autoArchive: true,              // 完成后归档日志
      archiveAfterMinutes: 60         // 多少分钟后归档
    }
  },
  tools: {
    exec: {
      backgroundMs: 5000,
      timeoutSec: 3600,
      notifyOnExit: true,
      notifyOnExitEmptySuccess: false
    }
  }
}
```

## 使用示例

### 示例 1: 编译项目

```
用户：编译整个项目，有点大

助手：🫡 收到！编译大项目预计需要 3-5 分钟，我会在后台运行。

任务：编译项目
预计耗时：3-5 分钟
通知方式：每 30 秒报告进展，完成后立即通知

你可以继续问我其他问题，不用等这个任务完成~

[后台启动 exec: npm run build]
[30 秒后] 📊 任务进展:
```
Building modules...
✓ Compiled 234 files in 45s
```

[60 秒后] 📊 任务进展:
```
Optimizing assets...
✓ Bundle size: 2.3MB
```

[完成] ✅ **任务完成!**
耗时：2 分 34 秒
退出码：0
🎉 一切顺利!
```

### 示例 2: 数据迁移

```
用户：把数据库迁移到新服务器，数据量大概 10GB

助手：🫡 收到！10GB 数据迁移预计需要 15-30 分钟，我会在后台运行。

任务：数据库迁移 (10GB)
预计耗时：15-30 分钟
通知方式：每 60 秒报告进展，完成后立即通知

你可以继续问我其他问题，不用等这个任务完成~

[启动 sessions_spawn 子代理处理]
...
```

### 示例 3: 模型训练

```
用户：用这个数据集 fine-tune 模型，跑 100 个 epoch

助手：🫡 收到！模型训练是长任务，预计需要 2-4 小时，我会用独立子代理运行。

任务：Fine-tune 模型 (100 epochs)
预计耗时：2-4 小时
通知方式：每 5 分钟报告训练进度，完成后立即通知

你可以继续问我其他问题，不用等这个任务完成~

[启动独立子代理，完全隔离]
...
```

## 错误处理

### 任务超时

```javascript
if (result.timedOut) {
  await message({
    message: `⏰ **任务超时!**
    
运行超过 ${timeoutSeconds} 秒，已自动终止。

可能原因:
- 任务确实需要更长时间
- 任务卡死或进入死循环
- 资源不足 (内存/CPU)

建议:
1. 检查日志确认卡在哪里
2. 如需更长时间，用 --timeout 参数指定
3. 考虑优化任务或分批处理`
  });
}
```

### 任务失败

```javascript
if (result.exitCode !== 0) {
  const errorLog = await process({
    action: 'log',
    sessionId,
    offset: -50,  // 最后 50 行
    limit: 50
  });
  
  await message({
    message: `❌ **任务失败!**
    
退出码：${result.exitCode}
错误摘要:\n\`\`\`\n${errorLog.output.slice(-500)}\n\`\`\`

需要我帮你分析问题原因吗？`
  });
}
```

### 队列积压

当检测到多个长任务排队时:

```javascript
const runningTasks = await process({ action: 'list' });
if (runningTasks.length >= maxConcurrentLongTasks) {
  await message({
    message: `⚠️ 当前有 ${runningTasks.length} 个长任务正在运行。
    
新任务已加入队列，会在第 ${runningTasks.length + 1} 顺位执行。

使用 \`/tasks\` 查看队列状态`
  });
}
```

## 相关命令

### `/tasks` - 查看任务列表

```
📋 当前任务列表

运行中:
1. [sessionId: abc123] npm run build - 运行 2 分钟
2. [sessionId: def456] data-migration - 运行 15 分钟

等待中:
1. [queued] model-training - 排队第 1 位

已完成 (最近 1 小时):
1. [✅] test-suite - 耗时 5 分 23 秒
```

### `/task <id> log` - 查看任务日志

```
📄 任务日志 [abc123]

[17:30:00] Starting build...
[17:30:15] Compiled 100 files
[17:30:45] Compiled 234 files
[17:31:00] Optimizing...
[17:32:34] Build complete!
```

### `/task <id> kill` - 终止任务

```
⏹️ 任务 [abc123] 已终止

退出码：SIGTERM
运行时长：2 分 34 秒
```

## 最佳实践

### ✅ 推荐

1. **立即确认** - 5 秒内回复，让用户知道任务已接收
2. **预估时间** - 给出合理的时间预期
3. **定期反馈** - 30-60 秒报告一次，避免用户焦虑
4. **隔离长任务** - >5 分钟的任务用子代理
5. **超时保护** - 设置合理 timeout，避免无限运行
6. **日志归档** - 完成后保留日志供查阅

### ❌ 避免

1. **沉默运行** - 几分钟没反馈，用户不知道在干嘛
2. **阻塞队列** - 长任务占用主线程，其他用户等不了
3. **无超时** - 卡死的任务永远跑不完
4. **日志丢失** - 完成后没地方看输出
5. **过度报告** - 每秒都发，骚扰用户

## 技能元数据

- **名称**: Long Task Handler
- **版本**: 1.0.0
- **作者**: Frankie 助理
- **创建日期**: 2026-03-31
- **依赖工具**: exec, process, message, sessions_spawn
- **适用渠道**: 所有渠道 (feishu, discord, telegram, etc.)

## 激活检查清单

收到任务时快速判断:

- [ ] 任务是否涉及编译/部署/迁移/训练？
- [ ] 数据量是否 > 1GB 或文件数 > 1000？
- [ ] 是否包含已知慢命令 (docker build, webpack, tsc, ffmpeg)？
- [ ] 用户是否暗示"慢慢跑"、"不急"、"后台弄"？
- [ ] 是否有超时/进度参数？

3 个以上 ✅ → 激活长任务处理机制
