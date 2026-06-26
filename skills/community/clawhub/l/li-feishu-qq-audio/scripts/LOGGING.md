# 日志管理文档

## 日志配置

### 日志目录
- **默认位置**: `/tmp/openclaw/`
- **可配置**: 通过 `.env` 文件设置 `LOG_DIR` 环境变量

### 日志文件

| 脚本 | 日志文件 | 说明 |
|------|----------|------|
| `tts-voice.sh` | `/tmp/openclaw/openclaw-YYYY-MM-DD.log` | TTS 合成日志 |
| `feishu-tts.sh` | `/tmp/openclaw/feishu-tts-YYYY-MM-DD.log` | 飞书语音发送日志 |
| `cleanup-tts.sh` | `/tmp/openclaw/cleanup-YYYY-MM-DD.log` | 清理操作日志 |
| `fast-whisper-fast.sh` | `/tmp/openclaw/whisper-YYYY-MM-DD.log` | 语音识别日志 |

## 日志级别

- **INFO**: 正常操作流程
- **WARN**: 警告信息（不影响功能）
- **ERROR**: 错误信息（需要关注）

## 清理策略

### 自动清理

1. **日常清理**（每天凌晨 2 点）
   ```bash
   ./scripts/cleanup-tts.sh 10
   ```
   - 保留最近 10 个 TTS 目录
   - 最大空间 100MB

2. **每周清理**（每周日凌晨 3 点）
   ```bash
   ./scripts/cleanup-tts.sh --weekly
   ```
   - 保留最近 5 个 TTS 目录
   - 清理 7 天前的日志文件
   - 最大空间 50MB

### 手动清理

```bash
# 清理所有临时文件
./scripts/cleanup-tts.sh 0

# 清理并查看日志
./scripts/cleanup-tts.sh --weekly
cat /tmp/openclaw/cleanup-$(date +%Y-%m-%d).log
```

## 日志格式

```
[YYYY-MM-DD HH:MM:SS] [LEVEL] 消息内容
```

示例：
```
[2026-03-22 21:14:37] [INFO] TTS 合成成功：/tmp/tts-output-1774185280.mp3
[2026-03-22 21:14:38] [INFO] 语音消息发送成功（用户：xxx, 时长：2000ms）
[2026-03-22 21:15:00] [WARN] psutil 未安装，系统资源监控将使用降级方案
```

## 调试信息隔离

所有调试信息（文件路径、临时目录、内部状态）**不会**通过 stdout 输出给用户，而是：

1. **日志文件**: 写入 `/tmp/openclaw/*.log`
2. **stderr**: 供脚本调用者调试使用
3. **stdout**: 仅输出必要的返回值（如文件路径、OK/ERROR）

## 查看日志

```bash
# 查看今日日志
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log

# 查看所有日志文件
ls -lh /tmp/openclaw/*.log

# 搜索错误
grep "ERROR" /tmp/openclaw/*.log
```

## 配置示例

在 `scripts/.env` 中添加：

```bash
# 自定义日志目录
LOG_DIR=/var/log/li-feishu-audio

# 自定义临时目录
TEMP_DIR=/tmp

# 飞书凭证
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=xxx
```

## 注意事项

1. **不要删除正在使用的日志文件** - 可能导致日志丢失
2. **定期清理** - 避免日志文件占用过多磁盘空间
3. **敏感信息** - 日志中不包含用户隐私数据
4. **日志轮转** - 每日自动创建新日志文件
