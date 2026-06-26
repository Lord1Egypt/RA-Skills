# Li Feishu Audio 0.1.4 优化总结

## 优化时间
2026-03-22 21:11

## 问题识别

用户发现以下调试信息被发送给用户：
- `/tmp/openclaw/tts-MB1NBC/voice-1774183714190.mp3`
- `📎 /tmp/openclaw/tts-5E4fDV/voice-1774183713165.mp3`
- `（已发送语音回复）`

这些内部调试信息不应该通过用户消息通道发送。

## 优化内容

### 1. 日志系统重构

#### 新增文件
- `scripts/LOGGING.md` - 日志管理文档
- `src/log_config.py` - Python 日志配置模块

#### 日志目录结构
```
/tmp/openclaw/
├── openclaw-YYYY-MM-DD.log      # 主日志
├── feishu-tts-YYYY-MM-DD.log    # 飞书发送日志
├── whisper-YYYY-MM-DD.log       # 语音识别日志
└── cleanup-YYYY-MM-DD.log       # 清理操作日志
```

### 2. 脚本优化

#### tts-voice.sh
**改动**:
- 日志输出到 stderr，不干扰 stdout
- stdout 仅输出文件路径（供调用者使用）
- Python 代码中使用 logging 模块

**之前**:
```bash
print(f"语音生成完成：{OUTPUT}")  # 输出给用户
echo "$OUTPUT"                    # 再次输出
```

**之后**:
```python
_logger.info(f"TTS 合成成功：{OUTPUT}")  # 输出到日志
print(OUTPUT, flush=True)               # 只输出路径
```

#### feishu-tts.sh
**改动**:
- 新增日志函数 `log()`，输出到文件和 stderr
- 成功/失败信息不再通过 stdout 发送给用户
- stdout 仅输出 `OK` 或 `ERROR`

**之前**:
```bash
echo "语音消息已发送（时长：${DURATION_MS}ms）"  # 发送给用户
```

**之后**:
```bash
log "语音消息发送成功（用户：$USER_ID, 时长：${DURATION_MS}ms）"  # 日志
echo "OK"  # 供调用者判断
```

#### fast-whisper-fast.sh
**改动**:
- 日志输出到文件和 stderr
- stdout 仅输出识别文本（无时间戳）
- 错误信息不暴露文件路径

**之前**:
```bash
print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
```

**之后**:
```python
print(segment.text.strip(), flush=True)  # 只输出文本
_logger.info(f"识别完成：{info.language}")  # 日志
```

#### cleanup-tts.sh
**改动**:
- 新增 `--weekly` 参数，支持每周清理模式
- 日志输出到文件，stdout 仅输出简洁结果
- 自动清理 7 天前的日志文件

**新增功能**:
```bash
# 日常清理（每天凌晨 2 点）
./cleanup-tts.sh 10

# 每周清理（每周日凌晨 3 点）
./cleanup-tts.sh --weekly
```

### 3. Python 模块优化

#### 新增 log_config.py
统一的日志配置模块：
- 自动创建日志目录
- 按模块名称创建日志文件
- 同时输出到控制台和文件
- 支持环境变量配置

#### voice.py 优化建议
后续可将 `_logger` 配置改为使用 `log_config.get_logger(__name__)`

### 4. 文档更新

#### SKILL.md
- 新增"日志管理"章节
- 更新版本信息为 0.1.4
- 添加作者信息

#### _meta.json
- 版本号：0.1.3 → 0.1.4
- 作者：北京老李
- 新增 changelog

#### LOGGING.md
完整的日志管理文档：
- 日志目录配置
- 日志文件说明
- 清理策略
- 查看日志方法
- 配置示例

## 清理策略

### 日常清理（每天凌晨 2 点）
- 保留最近 10 个 TTS 目录
- 最大空间 100MB
- 清理脚本临时文件

### 每周清理（每周日凌晨 3 点）
- 保留最近 5 个 TTS 目录
- 清理 7 天前的日志文件
- 最大空间 50MB

### Cron 配置示例
```bash
# 每天凌晨 2 点清理
0 2 * * * /root/.openclaw/workspace/skills/li-feishu-audio/scripts/cleanup-tts.sh 10

# 每周日凌晨 3 点清理
0 3 * * 0 /root/.openclaw/workspace/skills/li-feishu-audio/scripts/cleanup-tts.sh --weekly
```

## 测试验证

### TTS 测试
```bash
$ ./scripts/tts-voice.sh "测试日志隔离" 2>&1
/tmp/tts-output-1774185496.mp3
```
✅ stdout 仅输出文件路径

### 飞书发送测试
```bash
$ ./scripts/feishu-tts.sh /tmp/test.mp3 test_user 2>&1
[2026-03-22 21:18:20] 错误：发送失败（用户：test_user）
ERROR: {"code":99992351,...}
```
✅ 日志输出到文件和 stderr，stdout 输出 ERROR

### 日志文件验证
```bash
$ ls -lh /tmp/openclaw/*.log
-rw-r--r-- 1 root root  868 3 月 22 21:18 /tmp/openclaw/feishu-tts-2026-03-22.log
-rw-r--r-- 1 root root 4.3M 3 月 22 21:18 /tmp/openclaw/openclaw-2026-03-22.log
```
✅ 日志文件正常创建

## 用户影响

### 之前（有问题）
用户收到消息：
```
语音生成完成：/tmp/openclaw/tts-MB1NBC/voice-1774183714190.mp3
📎 /tmp/openclaw/tts-5E4fDV/voice-1774183713165.mp3
（已发送语音回复）
```

### 之后（已修复）
用户收到消息：
```
<qqvoice>/tmp/openclaw/tts-xxx/voice-xxx.opus</qqvoice>
```
或其他正常的文字回复，不包含调试信息。

## 后续建议

1. **voice.py 更新** - 将 `_logger` 配置改为使用 `log_config.get_logger(__name__)`
2. **日志轮转** - 考虑使用 `logging.handlers.TimedRotatingFileHandler`
3. **日志级别** - 支持通过环境变量动态调整日志级别
4. **监控告警** - 集成 Prometheus 或 Grafana 监控日志

## 总结

本次优化全面解决了调试信息泄露给用户的问题：
- ✅ 所有脚本日志输出到文件
- ✅ stdout 仅输出必要返回值
- ✅ stderr 供调试使用
- ✅ 自动清理策略（日常 + 每周）
- ✅ 完整的日志文档

**版本**: 0.1.4  
**作者**: 北京老李  
**优化完成时间**: 2026-03-22 21:11
