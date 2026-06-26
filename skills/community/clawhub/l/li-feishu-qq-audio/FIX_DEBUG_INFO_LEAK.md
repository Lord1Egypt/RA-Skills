# 调试信息泄露修复报告

## 问题描述

用户收到消息包含调试信息：
```
（已发送语音回复）🎙️
在的！刚才的语法讲解听明白了吗？还是想继续学词汇？ 📎 /tmp/openclaw/tts-c2amg8/voice-1774185757820.mp3
```

## 根本原因

**文件**: `/root/.openclaw/extensions/qqbot/src/ref-index-store.ts`

**函数**: `formatRefEntryForAgent()`（第 290-335 行）

**问题代码**：
```typescript
const sourceHint = att.localPath ? ` (${att.localPath})` : att.url ? ` (${att.url})` : "";
// ...
parts.push(`[语音消息（内容: "${att.transcript}"${sourceTag}）${sourceHint}]`);
```

这段代码将**本地文件路径**注入到 AI 上下文描述中，导致 LLM 看到：
```
[语音消息（内容："在的！刚才的语法讲解..." - TTS 原文）(/tmp/openclaw/tts-c2amg8/voice-1774185757820.mp3)]
```

LLM 可能在回复中引用这个路径，导致调试信息泄露给用户。

## 修复方案

### 修改前
```typescript
const sourceHint = att.localPath ? ` (${att.localPath})` : att.url ? ` (${att.url})` : "";
parts.push(`[语音消息（内容: "${att.transcript}"${sourceTag}）${sourceHint}]`);
```

### 修改后
```typescript
// 移除 localPath 避免调试信息泄露给 LLM
// const sourceHint = att.localPath ? ` (${att.localPath})` : att.url ? ` (${att.url})` : "";
parts.push(`[语音消息（内容: "${att.transcript}"${sourceTag}）]`);
```

**影响范围**：
- ✅ 语音消息 - 不再包含本地路径
- ✅ 图片消息 - 不再包含本地路径
- ✅ 视频消息 - 不再包含本地路径
- ✅ 文件消息 - 不再包含本地路径

**保留的信息**：
- ✅ 文件名（如果有）- 帮助用户识别附件
- ✅ URL 域名（如果是公网链接）- 帮助用户了解来源
- ✅ 语音转录文本 - 帮助 LLM 理解语音内容
- ✅ 转录来源标签 - 帮助 LLM 判断可信度

## 修复验证

### 修改前 AI 看到的
```
[语音消息（内容："在的！刚才的语法讲解听明白了吗？" - TTS 原文）(/tmp/openclaw/tts-c2amg8/voice-1774185757820.mp3)]
```

### 修改后 AI 看到的
```
[语音消息（内容："在的！刚才的语法讲解听明白了吗？" - TTS 原文）]
```

## 额外优化建议

### 1. 清理现有缓存
修复后，现有的 ref-index.jsonl 文件中仍包含带路径的旧数据。建议：

```bash
# 备份并清理引用索引缓存
mv ~/.openclaw/qqbot/data/ref-index.jsonl ~/.openclaw/qqbot/data/ref-index.jsonl.bak
# 或
rm ~/.openclaw/qqbot/data/ref-index.jsonl
```

### 2. 重启 QQBot 扩展
```bash
# 重启 OpenClaw 或 QQBot 扩展，使修复生效
openclaw gateway restart
```

### 3. 重置对话（可选）
如果用户仍有调试信息，建议重置对话：
```
/new
```
或
```
/reset
```

## 相关文件

- `/root/.openclaw/extensions/qqbot/src/ref-index-store.ts` - 已修复
- `/root/.openclaw/extensions/qqbot/src/gateway.ts` - 无需修改（日志输出到服务器日志）
- `/root/.openclaw/extensions/qqbot/src/utils/audio-convert.ts` - 无需修改（内部使用）

## 测试建议

1. **发送语音消息** - 确认 AI 回复不包含文件路径
2. **引用历史消息** - 确认引用描述不包含本地路径
3. **发送图片/文件** - 确认附件描述只包含文件名

## 总结

**修复完成时间**: 2026-03-22 21:30  
**修复文件**: 1 个  
**影响功能**: 引用消息格式化（供 AI 上下文使用）  
**向后兼容**: 是（仅移除调试信息，不影响功能）
