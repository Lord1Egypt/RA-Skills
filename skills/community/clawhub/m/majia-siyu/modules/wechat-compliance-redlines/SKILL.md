---
name: wechat-compliance-redlines
description: 企业微信封号红线 + 广告法违禁词库，逐条核查私域方案的合规性。Use this skill when 合规官核查方案是否踩企微封号/广告法红线时。
metadata:
  version: "2.1.1"
---

# 企微合规红线核查（合规官）

## Overview
合规官在 Step 2 对方案里**每一个拉新/裂变/触达动作**逐条核对红线。命中即标 `COMPLIANCE_RED`，对方案有一票否决权。
词库唯一落在 `src/siyu_team/eval/compliance_lexicon.py`，规则依据见 `modules/_knowledge/01-wechat-official/compliance/redlines.md`。

## 核查清单
1. **封号高危动作**：外挂/群发软件/自动加好友/虚拟定位/诱导式裂变/未授权批量加人 → `COMPLIANCE_RED`
2. **广告法绝对化**：最/第一/国家级/100%/永久/稳赚 → `ABSOLUTE_CLAIM`
3. **个人信息**：收集信息是否明示授权、会话存档是否告知
4. **裂变路径**：是否走企微官方「客户联系/客户群/群发」白名单

## 输出
对每个被否决项给：命中条款（指向 redlines.md）+ 整改建议（合规替代动作）。
> 红线维护：先核对 `modules/_knowledge/01-wechat-official/compliance/redlines.md`，再只改 `eval/compliance_lexicon.py`；其他 Python 文件只 import。

---

## 不知道下一步用哪个 skill？

输入 `/siyu`。

这是私域工具箱的导航入口。它会沿用已有事实和产物，按当前目标安排必要的步骤，
并在当前对话继续完成。迷路了就回 `/siyu`。
