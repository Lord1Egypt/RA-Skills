---
name: long-task-handler-v2
description: |
  升级版长任务处理技能。整合 frankieway/long-task-handler 和 chrislawyeryounger-spec/long-task-checkin 的优点。
  触发场景：编译、部署、训练、数据处理、搜索爬虫、多步骤写作、调用外部API等预计超过60秒的任务。
---

# Long Task Handler V2 - 升级版长任务处理技能

## 核心升级点

- **双阶段反馈机制**：任务开始前预判 + 执行中定期汇报
- **智能时间预估**：结合任务类型和数据量给出合理估算
- **更细致的进度量化**：明确当前步骤/总步骤
- **优雅的错误处理**：问题主动报告，不假装没事

## 触发条件

满足以下任一条件时激活：
- 预计耗时 > 60 秒的任务
- 用户明确要求"后台运行"、"别等我"
- 包含已知慢命令：ffmpeg, docker, webpack, tsc, npm build, git push 等
- 数据量 > 1GB 或文件数 > 100
- 编译/部署/训练/迁移场景

## 执行流程

### Phase 1: 任务预判（收到任务 5 秒内）

```javascript
// 任务评估
function assessTask(command, context) {
  const indicators = {
    duration: estimateBasedOnCommand(command),
    background: /--timeout|-t|nohup|background/.test(command),
    isLongTask: /compile|build|deploy|train|migration|export|process/i.test(command)
  };
  
  return {
    estimatedMinutes: indicators.duration,
    shouldBackground: indicators.duration > 1 || indicators.background,
    notifyInterval: indicators.duration > 5 ? 120 : 60  // >5分钟每2分钟，否则每1分钟
  };
}

// 立即反馈格式
const confirmTemplate = `🫡 收到！

任务：{taskName}
预计耗时：{X-Y} 分钟
通知方式：每 {interval} 秒报告进展

你可以继续问我其他问题，不用等这个任务完成~`;
```

### Phase 2: 执行中反馈（每 2 分钟）

```javascript
// 进度汇报格式（严格遵守）
const progressTemplate = `📋 进度更新（已运行约 {seconds} 秒）

✅ 当前状态：{正在做什么}
📍 进度：{current}/{total} - {percentage}%
⏱ 预计还需：{估算时间}

[继续执行...]`;

// 监控循环
async function monitorTask(sessionId, options) {
  const { pollIntervalMs = 120000, maxSilentMs = 300000 } = options;
  let lastOutput = '';
  let silentSince = Date.now();
  
  setInterval(async () => {
    const result = await process({ action: 'poll', sessionId });
    
    // 有新输出时记录
    if (result.output !== lastOutput) {
      silentSince = Date.now();
      lastOutput = result.output;
    }
    
    // 每2分钟强制报告（即使无新输出）
    await sendProgressReport(result);
    
    // 静默超过5分钟发送警告
    if (Date.now() - silentSince > maxSilentMs) {
      await message({ message: `⚠️ 任务已静默运行 5 分钟，仍在进行中...` });
      silentSince = Date.now();
    }
    
    // 检查完成
    if (result.exitCode !== null) {
      await notifyCompletion(result);
    }
  }, pollIntervalMs);
}
```

### Phase 3: 完成通知

```javascript
const completionTemplate = `{status} **任务完成!**

耗时：{duration}
退出码：{exitCode}
{message}`;

// status: ✅ 成功 / ❌ 失败 / ⏰ 超时
```

## 任务分级处理

| 级别 | 预估时间 | 处理方式 | 反馈频率 |
|------|---------|---------|---------|
| 短任务 | <30s | 直接执行 | 无需汇报 |
| 中任务 | 30s-2min | 后台执行 | 无需汇报（完成后通知） |
| 长任务 | 2-10min | 后台执行 | 每2分钟汇报进度 |
| 超长任务 | >10min | 子代理隔离 | 每2分钟汇报 + 完成通知 |

## 智能预判规则

```javascript
// 编译类
if (/npm build|npm run build|gradle build|mvn compile/i) 
  → 预估 3-10 分钟，标记为长任务

// 部署类
if (/docker build|kubectl deploy|terraform apply/i) 
  → 预估 5-15 分钟，标记为超长任务

// 训练类
if (/train|fine-tune|model.fit|torchrun/i) 
  → 预估 30分钟-数小时，标记为超长任务，使用子代理

// 数据处理
if (/process.*data|migration|export.*csv|backup/i) 
  → 预估时间 = 数据量/处理速度，标记为长任务

// 搜索爬虫
if (/crawl|scrape|search.*multiple|fetch.*all/i) 
  → 预估时间 = 目标数 × 平均响应时间，标记为长任务
```

## 进度量化标准

```javascript
// ✅ 当前状态：通俗说明在做什么
// 好：正在搜索8个平台的热榜信息
// 差：正在执行web_search工具

// 📍 进度：必须量化
// 好：已完成5/8个平台 (62.5%)
// 好：第3步，共5步 (60%)
// 好：已处理230/500条数据 (46%)

// ⏱ 预计还需：保守估算
// 好：约2-3分钟
// 好：约1分钟
// 好：不确定，等待下一个平台响应
```

## 错误处理升级

```javascript
// 遇到问题主动报告，不假装没事
async function handleTaskIssue(sessionId, error) {
  const issueTypes = {
    RATE_LIMIT: '⚠️ 遇到限流，等待恢复...',
    TIMEOUT: '⏰ 任务响应超时，正在重试...',
    NETWORK: '🌐 网络波动，任务继续执行中...',
    MEMORY: '💾 内存使用较高，优化处理中...'
  };
  
  await message({ 
    message: `📋 进度更新（任务遇到小问题）

✅ 当前状态：${issueTypes[error.type]}
📍 进度：${error.progress}
⏱ 预计还需：等待恢复后约 X 分钟

[任务自动恢复中...]` 
  });
}
```

## 配置参数

```yaml
skills:
  long-task-handler-v2:
    enabled: true
    defaultTimeoutSeconds: 3600
    progressReportInterval: 120  # 每2分钟
    silentWarningThreshold: 300  # 5分钟静默警告
    maxConcurrentLongTasks: 3
    notifyOnExit: true
    autoArchive: true
    archiveAfterMinutes: 60
```

## 激活检查清单

收到任务时快速判断（3个✅激活）：

- [ ] 任务涉及编译/部署/迁移/训练？
- [ ] 数据量 > 1GB 或文件数 > 100？
- [ ] 包含慢命令（docker, ffmpeg, webpack, tsc）？
- [ ] 用户要求"后台运行"、"慢慢跑"？
- [ ] 预计耗时 > 2 分钟？

## 最佳实践

### ✅ 推荐

1. **5秒内预判**：收到任务立即评估并反馈
2. **保守估算**：时间预估宁可多说不少说
3. **量化进度**：必须包含 "X/Y" 格式的进度
4. **通俗语言**：说"搜索8个平台"而不是"执行web_search"
5. **问题透明**：遇到限流/错误主动报告

### ❌ 避免

1. 沉默运行 - 超过2分钟无反馈
2. 预估乐观 - 说"1分钟"结果跑了10分钟
3. 技术术语 - 用户不需要知道你在调用什么工具
4. 假装没事 - 出了问题要主动说

## 技能元数据

- 名称: Long Task Handler V2
- 版本: 2.0.0
- 作者: 乌索普（整合 frankieway + chrislawyeryounger-spec）
- 创建日期: 2026-05-05
- 依赖: exec, process, message, sessions_spawn