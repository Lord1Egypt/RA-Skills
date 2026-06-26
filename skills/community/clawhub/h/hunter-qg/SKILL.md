---
name: jike-talent-hunter
description: 在即刻平台挖掘vibecoding创业者人才。每…
---

# 即刻人才挖掘

## 任务目标

每天在即刻平台挖掘15名符合画像的年轻人：
- 会用AI工具编程（vibecoding）
- 有创业精神
- 有独立做产品的能力

## 人才池

**存储位置**: `~/.openclaw/workspace-test/memory/talent-pool.json`

每次执行任务前，先读取人才池检查已存在的人，避免重复。

**数据结构**:
```json
{
  "candidates": [
    {
      "jikeId": "用户ID",
      "postUrl": "帖子链接",
      "profileUrl": "个人主页链接",
      "matchedReason": "为什么匹配",
      "foundDate": "2026-03-19"
    }
  ]
}
```

## 工作流程

### 第一步：接管浏览器并登录即刻

1. 使用 `browser` 工具接管浏览器：`browser(action=start, profile="openclaw")`
2. 导航到即刻：https://web.okjike.com
3. 如果用户未登录，提示用户扫码登录
4. 等待用户完成登录后，继续下一步

### 第二步：读取人才池查重

1. 读取 `~/.openclaw/workspace-test/memory/talent-pool.json`
2. 提取已收录的jikeId列表

### 第三步：搜索目标用户

在即刻搜索或浏览时，关键词组合：
- "vibe coding" / "vibecoding" / "AI编程"
- "独立开发" / "个人产品" / "自己做产品"
- "创业" / "副业" / "做自己的产品"
- "product hunt" / "indie hacker"

### 第四步：验证匹配

对每个潜在候选人，浏览其：
1. **帖子内容** - 确认有vibecoding实践、创业分享、产品发布等内容
2. **个人profile** - 确认是年轻人、有独立做产品的经历

判断标准（满足任一即可）：
- 帖子中提到用AI工具开发产品并上线
- 分享自己做产品的过程和成果
- 有创业/做产品相关的持续输出

### 第五步：记录结果

对确认匹配的人，追加到人才池：
- jikeId: 用户在即刻的ID
- postUrl: 对应帖子链接
- profileUrl: 个人主页链接
- matchedReason: 简要说明匹配理由
- foundDate: 今天的日期 (YYYY-MM-DD格式)

### 第六步：完成指标

确保当天找到15个不重复的候选人后再结束。

## 输出格式

任务完成后，报告：
1. 本次找到的人数
2. 人才池总人数
3. 新增人员列表（jikeId + 帖子链接）

## 注意事项

- 必须先查重再记录，避免重复收录
- 每个候选人必须有对应的帖子链接作为验证依据
- 如果当天找不到15人，可以扩大搜索范围或换关键词
