# QQBot 调试信息修复脚本 - 使用说明

## 🎯 功能说明

此脚本用于修复 QQBot 扩展中语音消息文件路径泄露给 LLM 的问题。

**修复前**，用户会看到：
```
📎 /tmp/openclaw/tts-xxx/voice-xxx.mp3
（已发送语音回复）🎙️
```

**修复后**，这些调试信息将不再出现。

---

## 📦 使用方法

### 方式 1：直接执行（推荐）

```bash
# 进入 QQBot 扩展目录
cd /root/.openclaw/extensions/qqbot

# 执行修复脚本
./scripts/fix-debug-leak.sh
```

### 方式 2：完整路径执行

```bash
/root/.openclaw/extensions/qqbot/scripts/fix-debug-leak.sh
```

---

## 🔧 脚本功能

脚本会自动执行以下操作：

1. **检查环境**
   - 验证 QQBot 扩展目录是否存在
   - 检查需要修复的文件

2. **修复文件**
   - `src/ref-index-store.ts` - 引用消息格式化函数
   - `src/gateway.ts` - 出站消息缓存回调

3. **备份原文件**
   - 修改前自动备份为 `*.bak.时间戳`
   - 如需恢复，可以使用备份文件

4. **清理旧缓存**
   - 删除 `~/.openclaw/qqbot/data/ref-index.jsonl`
   - 清除包含旧路径信息的缓存

5. **提示重启**
   - 显示重启命令
   - 说明修复效果

---

## ✅ 执行后操作

脚本执行完成后，**必须重启 OpenClaw**：

```bash
openclaw gateway restart
```

---

## 📝 修复内容详情

### ref-index-store.ts

**修复函数**：`formatRefEntryForAgent()`

**修复前**：
```typescript
const sourceHint = att.localPath ? ` (${att.localPath})` : att.url ? ` (${att.url})` : "";
parts.push(`[语音消息（内容: "${att.transcript}"${sourceTag}）${sourceHint}]`);
```

**修复后**：
```typescript
// 移除 localPath 避免调试信息泄露给 LLM
// const sourceHint = att.localPath ? ` (${att.localPath})` : att.url ? ` (${att.url})` : "";
parts.push(`[语音消息（内容: "${att.transcript}"${sourceTag}）]`);
```

### gateway.ts

**修复位置**：`onMessageSent` 回调

**修复前**：
```typescript
const localPath = meta.mediaLocalPath;
const attachment: RefAttachmentSummary = {
  type: meta.mediaType,
  ...(localPath ? { localPath } : {}),
  ...
};
```

**修复后**：
```typescript
// 移除 localPath 避免调试信息泄露给 LLM
// const localPath = meta.mediaLocalPath;
const attachment: RefAttachmentSummary = {
  type: meta.mediaType,
  // 移除 localPath: localPath ? { localPath } : {},
  ...
};
```

---

## 🔍 验证修复

重启后，发送一条语音消息，检查 AI 回复：

**修复前**：
```
[语音]
📎 /tmp/openclaw/tts-xxx/voice-xxx.mp3
好，继续学词汇！
```

**修复后**：
```
[语音]
好，继续学词汇！
```

---

## 🛠️ 故障排查

### 脚本执行失败

**错误**：`QQBot 扩展目录不存在`

**解决**：
```bash
# 检查目录
ls -la /root/.openclaw/extensions/qqbot/

# 如果不存在，检查 OpenClaw 安装
openclaw status
```

### 文件不存在

**错误**：`文件不存在：src/ref-index-store.ts`

**解决**：
```bash
# 检查文件
ls -la /root/.openclaw/extensions/qqbot/src/

# 如果是 TypeScript 项目，可能需要先编译
cd /root/.openclaw/extensions/qqbot
npm install
npm run build
```

### 修复后仍有调试信息

**原因**：旧缓存未清理或 OpenClaw 未重启

**解决**：
```bash
# 1. 手动清理缓存
rm ~/.openclaw/qqbot/data/ref-index.jsonl

# 2. 重启 OpenClaw
openclaw gateway restart

# 3. 开始新对话
/new
```

---

## 📞 支持

- **修复报告**：`/root/.openclaw/extensions/qqbot/FIX_DEBUG_INFO_LEAK.md`
- **脚本目录**：`/root/.openclaw/extensions/qqbot/scripts/`
- **OpenClaw 文档**：https://docs.openclaw.ai

---

## 📋 版本信息

**脚本版本**：1.0  
**作者**：北京老李 (BeijingLL)  
**日期**：2026-03-22  
**适用版本**：QQBot 扩展（任意版本）
