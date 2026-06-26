---
name: openclaw-ai-doctor
version: 1.0.0
description: OpenClaw AI 智能体专科医生，专治各类智能体故障。包括启动报错、任务卡死、工具失效、显存溢出、记忆丢失、逻辑崩坏等。提供标准化诊疗流程：问诊→体检→确诊→治疗→复诊。
---

# 🏥 OpenClaw AI 智能体专科医生

## 触发场景

当用户遇到以下问题时使用本技能：
- OpenClaw 启动报错、环境依赖冲突
- AI 智能体任务循环卡死、不执行指令
- 工具调用失效、插件冲突
- 显存溢出、本地部署卡顿
- 上下文记忆断裂、越用越笨
- 权限限制、接口调用失败
- 逻辑崩坏、答非所问
- Session 隔离失效、跨会话泄露
- Gateway 崩溃、心跳丢失
- 技能/Skill 加载失败

## 诊疗流程

### 1. 问诊 (Diagnosis Intake)

收集用户问题信息：
- 症状描述（什么操作后出现问题）
- 部署环境（本地/云端、显卡、系统）
- 报错日志或截图
- 想要实现的功能

### 2. 体检 (System Check)

```bash
# 检查基础状态
openclaw status
openclaw gateway status

# 检查日志
tail -100 ~/.openclaw/logs/gateway.log

# 检查资源
df -h
free -h
nvidia-smi 2>/dev/null
```

### 3. 确诊 (Root Cause)

根据症状定位故障编号：

| 症状 | 故障编号 | 可能病因 |
|------|---------|---------|
| 启动失败 | 001 | 环境依赖冲突 |
| 卡死不动 | 002 | 任务死锁 |
| 工具失效 | 003 | 权限/注册问题 |
| 显存爆了 | 004 | 模型过大/并发过高 |
| 记不住事 | 005 | 上下文溢出/文件权限 |
| 权限报错 | 006 | API Key 过期/配额用尽 |
| 胡言乱语 | 007 | 上下文污染/提示词覆盖 |
| 发错消息 | 008 | Session 隔离失效 |
| Gateway 挂了 | 009 | 内存溢出/配置错误 |
| 技能没了 | 010 | 路径错误/注册表未更新 |

### 4. 治疗 (Treatment)

#### 001 - 启动报错
```bash
npm install --force
npm cache clean --force && npm install
cat ~/.openclaw/config.json | jq .
```

#### 002 - 任务卡死
```bash
openclaw gateway restart
openclaw sessions kill <sessionId>
rm -rf ~/.openclaw/workspace/temp/*.lock
```

#### 003 - 工具失效
```bash
openclaw tools list
openclaw tools reload
cat ~/.openclaw/policy.json
```

#### 004 - 显存溢出
```bash
nvidia-smi
# config.json: modelQuantization: int8/int4
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
```

#### 005 - 记忆断裂
```bash
chmod 644 ~/.openclaw/workspace/memory/*.md
chmod 644 ~/.openclaw/workspace/MEMORY.md
```

#### 006 - 权限报错
```bash
export OPENCLAW_API_KEY=<new_key>
chmod -R u+rw ~/.openclaw/workspace/
```

#### 007 - 逻辑崩坏
```bash
openclaw sessions kill <sessionId>
# 重新读取 SOUL.md 和 AGENTS.md
```

#### 008 - Session 泄露
# 检查 inbound_meta，禁止跨 session 查找 context

#### 009 - Gateway 崩溃
```bash
openclaw gateway restart
openclaw config validate
```

#### 010 - 技能加载失败
```bash
cd ~/.openclaw/skills/<skillName> && npm install
rm ~/.openclaw/skills-index.json && openclaw skills scan
```

### 5. 复诊 (Follow-up)

- 验证修复效果
- 提供预防建议
- 记录案例归档

## 服务信息

| 服务类型 | 价格 | 适用场景 |
|---------|------|---------|
| 轻症问诊 | 29-99 元/次 | 启动报错、基础配置 |
| 深度诊疗 | 199-599 元/次 | 复杂 bug、性能优化 |
| 月度托管 | 699-1999 元/月 | 长期维护、定期体检 |

## 联系方式

- 邮箱: speakmen@outlook.com
- 响应时间: 工作日 2h 内
