---
name: inquiry-1688
category: official-1688
description: >-
  向1688供应商发起询盘对话，就商品的价格、起订量、定制、物流、资质、规格、样品等问题咨询商家，
  自动提交询盘并在20分钟后获取供应商的回复结果，通过钉钉主动推送给用户。
  适用于跨境采购、批发拿货、OEM定制等场景下需要与1688商家沟通的需求。
  触发词：询盘、1688询盘、问供应商、问商家、咨询供应商、咨询商家、联系供应商、联系商家、
  问一下卖家、帮我问问、帮我咨询、帮我询盘、发起询盘、给商家留言、
  能不能定制、可以定制吗、支持定制吗、能定做吗、可以OEM吗、能贴牌吗、
  起订量多少、起批量多少、最少买多少、最低起订、MOQ多少、最小订单量、
  多少钱、什么价格、批发价多少、大量拿货价、能便宜吗、可以优惠吗、价格能谈吗、
  能不能发货、可以发到哪里、能发国外吗、支持跨境发货吗、有物流吗、怎么发货、运费多少、
  有没有现货、库存多少、多久能发货、交期多久、生产周期、几天能做好、
  有没有资质、有认证吗、有质检报告吗、有CE认证吗、能提供检测报告吗、
  商品尺寸、商品长宽高、产品规格、有什么材质、什么面料、
  能提供样品吗、可以寄样吗、样品多少钱、打样费多少、
  供应商能不能XXX、这个商品能不能XXX、想问一下这个产品。
metadata:
  version: 1.0.2
  label: 1688询盘
  author: 1688官方技术团队
---

# 1688 询盘

向1688供应商发起询盘，20分钟后自动查询结果并回复。

## 前置配置（必须先完成）

⚠️ **使用本 SKILL 前，必须先配置以下环境变量，否则询盘接口调用会失败。**

| 环境变量 | 说明 | 必填 | 获取方式 |
|---------|------|------|---------|
| `ALPHASHOP_ACCESS_KEY` | AlphaShop API 的 Access Key | ✅ 必填 | 可以访问1688-AlphaShop（遨虾）来申请 https://www.alphashop.cn/seller-center/apikey-management ，直接使用1688/淘宝/支付宝/手机登录即可 |
| `ALPHASHOP_SECRET_KEY` | AlphaShop API 的 Secret Key | ✅ 必填 | 可以访问1688-AlphaShop（遨虾）来申请 https://www.alphashop.cn/seller-center/apikey-management ，直接使用1688/淘宝/支付宝/手机登录即可 |

**⚠️ AlphaShop 接口欠费处理：** 如果调用 AlphaShop 接口时返回欠费/余额不足相关的错误，**必须立即中断当前流程**，提示用户前往 https://www.alphashop.cn/seller-center/home/api-list 购买积分后再继续操作。

### 配置方式

在 OpenClaw config 中配置：
```json5
{
  skills: {
    entries: {
      "inquiry-1688": {
        env: {
          ALPHASHOP_ACCESS_KEY: "YOUR_AK",
          ALPHASHOP_SECRET_KEY: "YOUR_SK"
        }
      }
    }
  }
}
```

如果用户没有提供这些密钥，**必须先询问用户获取后再继续操作**。

**核心机制**：询盘任务提交后，API 端最多执行 20 分钟，到时间后任务一定结束。通过 cron 在 20 分钟后查询结果并写入文件，用户下次发消息时 agent 检查文件并回复。

## 工作流程

```
1. 提取：1688商品链接 + 询盘问题
         ↓
2. submit 提交询盘 → 获取 taskId → 告知用户"已发起，20分钟后结果就绪"
         ↓
3. 写入追踪文件 pending_inquiries.json
         ↓
4. 用 date 命令计算 20 分钟后的 UTC 时间
         ↓
5. 创建 cron isolated agentTurn 任务
   任务内容：查询结果 → 写入 results/{taskId}.md → 清除 pending 记录
         ↓
6. 20 分钟后 cron 触发 → isolated session 查询结果 → 写入文件
         ↓
7. 用户下次发消息时 → agent 检查 results/ 目录 → 发现结果 → 直接回复
   （心跳也会兜底检查 pending_inquiries.json 中超时未处理的任务）
```

## Step 1: 提取信息

从用户消息中提取：
- **商品链接或ID**（必须）
- **询盘问题**：自由文本（必须）
- **期望订购量**（可选）
- **地址**（可选）

如果用户没提供商品链接，必须询问。

## Step 2: 提交询盘

```bash
python3 scripts/inquiry.py submit "<商品链接或ID>" "<询盘问题>" [--quantity X] [--address "地址"]
```

从响应中提取 `result.data` 作为 taskId。提交成功后告知用户：
> 询盘已发送给供应商，20分钟后给你结果 ✅

## Step 3: 写入追踪文件 + 创建 cron 查询任务

### 3a: 写入追踪文件

将待查询的任务信息追加到追踪文件：

```bash
TRACK_FILE="/home/admin/.openclaw/workspace/skills/inquiry-1688/pending_inquiries.json"

# 写入格式（JSON Lines，每行一个任务）：
echo '{"taskId":"<taskId>","productId":"<商品ID>","url":"<商品链接>","question":"<用户问题>","submitTime":"<ISO时间>"}' >> "$TRACK_FILE"
```

### 3b: 创建 cron 查询任务（钉钉主动推送）

⚠️ **时间计算必须用 `date` 命令，禁止手算！**

```bash
date -u -d '+20 minutes' --iso-8601=seconds
```

然后创建 cron 任务。**核心：查询结果后通过 message 工具直接推送到钉钉**：

```
cron action=add
job={
  "name": "inquiry-result-{商品ID}",
  "schedule": {"kind": "at", "at": "{上面的UTC时间}"},
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "你是询盘结果查询助手。请严格执行以下步骤：\n\n1. 执行查询命令：\npython3 /home/admin/.openclaw/workspace/skills/inquiry-1688/scripts/inquiry.py query \"{taskId}\"\n\n2. 将结果总结为中文消息，包含：\n   📋 询盘结果\n   商品链接: {链接}\n   用户原始问题: {用户的问题}\n   商品名称 + 价格 + 供应商名称\n   各问题的回答\n   AI 总结\n\n3. 使用 message 工具发送到钉钉：\n   message action=send channel=dingtalk target=238382 message=\"整理好的询盘结果\"\n\n4. 清除追踪记录：\npython3 /home/admin/.openclaw/workspace/skills/inquiry-1688/scripts/inquiry.py remove-pending \"{taskId}\"\n\n⚠️ 必须用 message 工具发钉钉！不要用 sessions_send，不要写文件！",
    "timeoutSeconds": 120
  },
  "delivery": {
    "mode": "none"
  },
  "enabled": true
}
```

**关键参数：**
- **sessionTarget**: `isolated`（独立 session 执行，不抢主 session 锁）
- **payload.kind**: `agentTurn`（独立 agent turn）
- **delivery.mode**: `none`（不走 announce，由任务自己用 message 工具推送钉钉）
- **钉钉 target**: `238382`（流畅的钉钉 peer ID）

## Step 4: 结果投递（钉钉主动推送）

cron 任务查到结果后，直接通过 `message action=send channel=dingtalk target=238382` 推送到流畅的钉钉私聊。用户在钉钉即时收到通知 ✅

### 兜底机制
如果钉钉推送失败，任务会把结果写入 `results/{taskId}.md`，用户下次发消息时 agent 检查并回复。

回复格式参考：

### 📋 询盘结果

**商品**: {taskInfo.title 或商品名称}（¥{价格}）
**供应商**: {sellerInfo.companyName}
**状态**: ✅/❌ {taskInfo.status}

| 问题 | 回复 |
|------|------|
| {问题1} | {回答1} |
| {问题2} | {回答2} |

#### AI 总结
{aiSummary 核心内容，精简展示}

## 脚本命令参考

| 命令 | 用途 | 示例 |
|------|------|------|
| `submit` | 提交询盘 | `inquiry.py submit "链接" "问题"` |
| `query` | 查询结果 | `inquiry.py query "taskId"` |

## 注意事项

- `questionList` 固定填 `["自定义"]`，用户实际问题放入 `requirementContent`
- `isRequirementOriginal` 设为 `true`，原文发送
- **不要轮询！** submit 后创建 cron，20 分钟后 query 一次就够
- **cron 用 `sessionTarget: isolated` + `payload.kind: agentTurn`**，在独立 session 里查询结果
- **delivery.mode 必须是 `none`**（由任务自己用 message 工具推送钉钉）
- 时间计算必须用 `date -u -d '+20 minutes' --iso-8601=seconds`
- 如果用户中途问"结果出来了吗"，可以提前 query 一次看看
- **钉钉推送目标**: `target=238382`（流畅的钉钉 peer ID）
- ⚠️ **不要用 systemEvent + main session！**（教训 #13）
- ⚠️ **不要用 sessions_send 推送结果！**（教训 #15）

## 兜底机制：心跳检查未完成询盘

**追踪文件**：`/home/admin/.openclaw/workspace/skills/inquiry-1688/pending_inquiries.json`（JSON Lines 格式）

**心跳检查流程**（已加入 HEARTBEAT.md）：

```
如果 pending_inquiries.json 存在且非空：
  1. 逐行读取每个待查询任务
  2. 检查 submitTime 是否已超过 20 分钟
  3. 如果已超时，执行 query 并通过钉钉推送结果
  4. 推送后执行 remove-pending 清除记录
```

## 教训记录

> **2026-03-05 ~ 03-06 连续踩坑：**
> 1. ❌ cron isolated + announce：delivery 配置问题 + announce 不送达
> 2. ❌ sessions_spawn + announce：用户收不到结果
> 3. ❌ sessions_spawn + message 推送 webchat：webchat 不支持
> 4. ❌ 同步 poll：阻塞进程，无中间输出
> 5. ❌ 循环 query：process poll 延迟导致超时 / yieldMs 超系统上限被后台化
> 6. ❌ sleep 1200 同步等：yieldMs 超系统上限，exec 被后台化，结果拿不回来
> 7. ❌ cron systemEvent + wakeMode 默认（next-heartbeat）：systemEvent 注入了但要等心跳才处理，用户等不到结果
> 8. ✅ **最终方案**：submit → cron systemEvent（20分钟后注入主session，wakeMode=now 立即唤醒）→ agent 收到后 query 一次 → 直接回复用户
> 9. ❌ cron systemEvent wakeMode=now 但主 session 忙：报 "timeout waiting for main lane to become idle"，任务被 skipped，用户收不到结果
> 10. ✅ **兜底修复**：除 cron 外，同时写入 pending_inquiries.json 追踪文件，心跳时兜底检查超时任务并补回结果
> 11. ❌ 用户 /new 重置 session 后，cron systemEvent 注入新 session，新 session 没有上下文不知道该干啥，结果又丢了
> 12. ✅ **修复**：systemEvent 文本改为完全自包含，包含所有必要信息和明确操作指令，不依赖任何 session 上下文
> 13. ❌ systemEvent 触发后，回复发到了 heartbeat session（agent:main:main），而不是用户的 webchat session（agent:main:openresponses-user:xxx）。用户看不到回复。根本原因：systemEvent 走主 session 的心跳通道，回复目标是心跳 session，不是用户 session
> 14. ✅ **彻底重构**：改用 isolated agentTurn + sessions_send。cron 触发独立 session 查询结果，然后用 sessions_send 主动推送到用户的 webchat session。不再使用 systemEvent
> 15. ❌ isolated agentTurn + sessions_send：sessions_send 确实把消息注入到了用户 session，agent 也生成了回复，但回复的 delivery.mode 是 "announce"（跨 session 投递），用户看到的是 "Agent-to-agent announce step" 而不是直接对话。内容虽然最终送达了，但用户体验差，看起来像系统消息而不是正常回复。根本原因：sessions_send 触发的回复走 announce 通道，不走 webchat 直连通道
> 16. ❌ message 工具发 webchat：webchat 不是可外发的 channel，`message action=send channel=webchat` 报 "Unknown channel: webchat"，不指定 channel 报 "no configured channels detected"
> 17. ✅ **被动模式（webchat 时代）**：cron isolated agentTurn 只负责查询结果并写入文件（results/{taskId}.md），不尝试任何跨 session 推送。用户下次发消息时 agent 检查 results 目录，发现新结果就直接回复。心跳也可兜底检查。牺牲实时性换取可靠性
> 18. ✅ **钉钉主动推送（v2.0）**：接入钉钉 channel 后，cron isolated agentTurn 查询结果后直接用 `message action=send channel=dingtalk target=238382` 推送到流畅的钉钉私聊。delivery.mode 仍为 none（不依赖 announce），由任务自己调 message 工具发送。实时性 + 可靠性兼得 🎉
