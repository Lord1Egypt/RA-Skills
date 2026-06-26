---
name: meetmind
display_name: 会议纪要智能助手
description: 会议纪要智能助手 — 粘贴文字/上传音频 → 9类会议模板自动识别 → ACE六维结构化纪要 → 跨会议记忆追踪。免费层零成本（粘贴文字），付费层支持音频上传+云端转录。
version: 0.6.2
author: 咕嘟科技
homepage: https://hermesai.ltd
tags:
  - meeting-minutes
  - AI-transcription
  - structured-notes
  - meeting-templates
  - enterprise-efficiency
  - paid-tool
agent_created: true
---

# MeetMind v0.6.2 — 多模板会议智能纪要

> **9 类会议模板 → 自动识别 → ACE 六维结构化 → 跨会议记忆追踪**
>
> ⚠️ **本 Skill 需要云端 API 才能运行。模板核心逻辑在服务端，Skill 仅为客户端。**
> 🆓 **新用户 10 次免费试用 | ¥19.9/月解锁全部功能**
> 🆔 **自动获取 WorkBuddy 用户 ID，零配置即用**

---

## 核心差异化

| 竞品 | 能做什么 | MeetMind 的不同 |
|------|---------|----------------|
| 腾讯会议/飞书妙记 | 转录 + 摘要 | ✅ 我们有，但**不是核心** |
| Otter.ai/Fireflies | 转录 + 搜索 | ✅ 我们有，但**免费层已覆盖** |
| 通义听悟/听脑AI | 转录 + AI总结 | ✅ 我们也有，但**不是护城河** |
| **MeetMind** | **9类模板 + ACE结构 + 跨会议记忆** | 🔥 **竞品做不到的三件事** |

---

## 9 类会议模板

> **模板的 ACE 权重、定制输出块、Prompt 指令均在服务端。Skill 端仅负责关键词匹配选模板。**

| # | 模板 | 触发关键词（Skill 端用于本地匹配，服务端做精确识别） |
|---|------|---------------------------------------------------|
| 1 | 产品研讨会 | PRD、需求、功能、迭代、sprint、版本、原型、技术方案 |
| 2 | 客户会议 | 客户、甲方、交付、验收、续约、客诉、报价、合同 |
| 3 | 内部周会 | 周报、本周、上周、下周、进度、OKR、同步、阻塞 |
| 4 | 面试 | 面试、候选人、自我介绍、离职原因、期望薪资、offer |
| 5 | 销售拜访 | 拜访、演示、POC、报价、招投标、签约、商机 |
| 6 | 投资评审 | 投资、估值、条款、DD、尽调、回报率、赛道 |
| 7 | 1v1 沟通 | 1on1、1v1、一对一、绩效、成长、反馈、困惑 |
| 8 | 头脑风暴 | 头脑风暴、脑暴、brainstorm、想法、点子、创意 |
| 9 | 复盘会 | 复盘、retro、回顾、事故、上线失败、改进、教训 |

**自动检测**：Skill 端根据关键词密度评分，选择最高分模板ID发送给云端 API。所有模板的实际处理逻辑在服务端。

---

## 收费层级

| 层级 | 价格 | 模板 | 跨会议记忆 | 输入方式 |
|------|------|------|-----------|---------|
| 🆓 试用 | ¥0 | 全部 9 类 | ❌ 不存储 | 粘贴文字（10次终身） |
| L1 免费 | ¥0 | 全部 9 类 | ❌ | 粘贴文字（5次/月） |
| L2 月付 | **¥19.9/月** | 全部 9 类 | ✅ 永久 | 粘贴文字不限次 |
| L2 年付 | **¥99/年** | 全部 9 类 | ✅ 永久 | 粘贴文字不限次 |
| L3 音频 | **¥3/次** | 全部 9 类 | ✅ 永久 | 上传音频 + ASR |
| L4 企业 | ¥9,800+ | 全部 + **自定义模板** | ✅ 团队共享 | 不限 |

---

## 用户身份（自动获取，零配置）

v0.6.1 起，MeetMind 自动获取 WorkBuddy 用户身份，无需手动填写。

**自动检测优先级：**

```
WORKBUDDY_USER_ID 环境变量 (WB 上下文透传自动注入)
    ↓ 没有
MEETMIND_USER_ID 环境变量（手动配置兼容）
    ↓ 没有
本地持久化 ID（首次生成后缓存）
    ↓ 没有
自动生成 UUID（兜底）
```

**效果：**
- 同一 WB 用户 → 相同 user_id → 试用次数、用量、记忆持续跟踪
- 跨设备/重装 → 如果 WB 支持上下文透传，身份自动恢复
- 零手动配置 → 下载即用

> **付费版 mTLS 用户**：证书里的 user_id 会覆盖以上自动 ID，确保付费身份一致。

---

## 试用流程（新用户）

```
1. 从 SkillHub 下载本 Skill
2. 在 WorkBuddy 中说：@meetmind 试用 [粘贴会议文字]
3. Skill 自动获取你的 WB 用户 ID，发到云端 /trial（无需证书，10次免费）
4. 用完后提示升级 → 联系客服获取 mTLS 证书
```

---

---

## 核心工作流

```
用户提供文本或音频
       ↓
Skill 端：关键词匹配 → 选择模板ID
       ↓
云端 API：DeepSeek V4-Flash + 模板处理 → ACE 六维结构化
       ↓
返回结构化纪要（付费用户自动存储跨会议记忆）
       ↓
询问是否创建 Task / 写入日记 / 更新 MEMORY
```

---

## API 端点

| 端点 | 方法 | 用途 | 认证 |
|------|------|------|------|
| `/trial` | POST | 免费试用（10次终身） | 无需 mTLS |
| `/health` | GET | 健康检查 | mTLS |
| `/transcribe` | POST | 文字透传/音频转录 | mTLS |
| `/structure` | POST | ACE结构化 | mTLS |
| `/memory/context` | GET | 记忆上下文 | mTLS |
| `/memory/recall` | POST | 检索记忆 | mTLS |
| `/user/{id}` | GET | 用户信息 | mTLS |
| `/user/{id}/usage` | GET | 用量查询 | mTLS |
| `/templates` | GET | 模板列表（含自定义） | mTLS |
| `/templates` | POST | 创建自定义模板（L4） | mTLS |
| `/templates/{id}` | PUT | 更新自定义模板（L4） | mTLS |
| `/templates/{id}` | DELETE | 删除自定义模板（L4） | mTLS |

---

## Skill 端调用

```python
from scripts.cloud_client import MeetMindClient

# 自动获取 WB 用户 ID（零配置）
client = MeetMindClient()

# 🔓 免费试用（10次，无需证书）
result = client.trial_structure(meeting_text)

# 🔒 付费使用（需要 mTLS 证书）
result = client.transcribe_text(meeting_text)
struct = client.structure(result["task_id"])

# 带记忆追踪
struct = client.structure(
    result["task_id"],
    entity_key="项目名称",
    entity_type="project",
    meeting_title="Q3产品评审"
)

# 自定义模板（L4 企业版）
client.create_template(name="董事会汇报", keywords=["董事会", "股东"], ...)
```

---

## 文件结构

```
meetmind/
├── SKILL.md              ← 本文件（v0.6.1）
├── config.json           ← 模型/定价/试用配置
├── certs/                ← 客户端证书（付费用户获取，不随代码分发）
│   ├── client.crt
│   └── client.key
├── .meetmind_user_id     ← 自动生成的本地用户 ID（用于兜底）
└── scripts/
    └── cloud_client.py   ← 云端 API 客户端（自动 WB ID + mTLS 证书认证 + 试用模式）
```

---

## 快速开始

```
# 试用（无需付费）
@meetmind 试用 [粘贴会议文字]

# 指定模板
@meetmind 这是产品评审会 [粘贴文字]

# 带记忆追踪（付费用户）
@meetmind ADP客户第三次会议 entity=ADP科技 type=client [粘贴文字]

# 上传音频（L3用户）
@meetmind 这是今天客户会议的录音
```

---

## 证书获取

付费用户加微信 **GuduTech** 获取 mTLS 客户端证书（client.crt + client.key），放入 `certs/` 目录即可激活全部功能。

---

## WorkBuddy 配置（可选，推荐开启）

如果你的 WorkBuddy 支持「上下文透传」功能，开启后可获得最佳体验：

1. **开启上下文透传**：【系统设置】→【AI扩展】→【上下文透传】→ 开启「会话级上下文自动注入」
2. **添加白名单字段**：在透传字段白名单中添加 `user_id`
3. **映射 Header 名称**：将 `user_id` 映射到 `X-WorkBuddy-User-ID`

配置后，MeetMind 会自动获取你的 WB 用户 ID，跨设备无缝同步试用次数和使用记录。

> 如果 WorkBuddy 不支持上下文透传，MeetMind 会自动使用本地持久化 ID，不影响正常使用。

# 通用 Skill 埋点注入模板

## 埋点说明（analytics-sdk）

本 Skill 集成 ACE 统一分析追踪，在以下节点自动上报数据。

### 埋点事件

| 事件 | 触发节点 | 关键字段 |
|------|---------|---------|
| `skill_start` | 用户调用 Skill 时 | skill_id, user_id, source, input_type |
| `skill_step` | 每完成一个处理步骤 | step_name, step_index, duration_ms |
| `skill_complete` | Skill 成功输出结果时 | output_format, output_size, total_duration_ms |
| `skill_error` | 运行失败时 | error_type, error_message_safe |

### Skill 特定字段

> 通用类 Skill 无特定业务字段，如需追踪请在下方补充。

### 调用示例

```javascript
// Skill 启动时
trackEvent("skill_start", {
  skill_id: "meetmind",
  user_id: userId,
  source: "workbuddy",
  input_type: "text"
});

// Skill 完成时
trackEvent("skill_complete", {
  skill_id: "meetmind",
  user_id: userId,
  output_format: "txt",
  output_size: 2300,
  total_duration_ms: 1800
});
```

### 静默失败

埋点失败不影响 Skill 主流程。所有 `trackEvent` 调用已在 `analytics-sdk` 中封装了 try/catch + 3 秒超时。

---


---

## 降级模式

- **无证书**：自动使用 `/trial` 端点（试用模式，10次限制）
- **证书过期/撤销**：提示联系管理员更新
- **无法联网**：提示检查网络连接

---
## 📬 更多资源

> 📬 更多 AI 企业落地实战案例 → 关注公众号：**咕嘟AI**  
> 💬 1v1 免费诊断（AI岗位匹配）→ 加微信：**GuduTech**  
> 🚀 完整 ACE 体系课 + AI 内容系统搭建 → https://hermesai.ltd  
>  
> 用 MeetMind 整理会议效率翻倍？欢迎加微信分享你的使用体验 📋
