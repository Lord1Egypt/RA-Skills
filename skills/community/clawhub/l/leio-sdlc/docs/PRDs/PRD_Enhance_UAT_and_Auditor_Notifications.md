---
Affected_Projects: [leio-sdlc]
---

# PRD: Enhance_UAT_and_Auditor_Notifications

## 1. Context & Problem (业务背景与核心痛点)
ISSUE-1099. Currently, the `notification_formatter.py` script within the `leio-sdlc` project lacks specific templates for several critical events, including `auditor_approved`, `auditor_rejected`, `uat_complete`, and `uat_error`. When these events are triggered, the system falls back to a generic and confusing message: `🤖 [SDLC Engine] 未知事件: <event_type>`. This prevents the Manager and the Boss from immediately understanding the result of SDLC pipeline checks in the Slack channel, forcing them to manually parse logs.

## 2. Requirements & User Stories (需求定义)
- **Functional Requirements:**
  - Update `notification_formatter.py` to properly handle and format the `auditor_approved`, `auditor_rejected`, `uat_complete`, and `uat_error` event types.
  - The `uat_complete` event must read the `status` from the context (e.g., "PASS", "NEEDS_FIX", etc.) and clearly output whether the UAT passed or missed.
  - Maintain the existing fallback logic for genuinely unknown events.
- **Non-Functional Requirements:**
  - Fast execution and no broken imports. Ensure strict formatting matching the current emojis.

## 3. Architecture & Technical Strategy (架构设计与技术路线)
- **Target File**: `scripts/notification_formatter.py`
- **Logic**: 
  - Add explicit `elif` blocks for `auditor_approved`, `auditor_rejected`, `uat_complete`, and `uat_error` before the final fallback `return f"🤖 [SDLC Engine] 未知事件: {event_type}"`.
  - For `uat_complete`, extract `status = context.get('status', 'UNKNOWN')` and format the message conditionally.

## 4. Acceptance Criteria (BDD 黑盒验收标准)
- **Scenario 1: Auditor Events**
  - **Given** an `auditor_approved` event is dispatched
  - **When** `format_notification` processes it
  - **Then** it returns the exact string defined in the hardcoded template.
- **Scenario 2: UAT Complete Event (Pass)**
  - **Given** a `uat_complete` event with `status: "PASS"`
  - **When** `format_notification` processes it
  - **Then** it includes "UAT Verification: Passed."
- **Scenario 3: UAT Complete Event (Fail)**
  - **Given** a `uat_complete` event with `status: "NEEDS_FIX"`
  - **When** `format_notification` processes it
  - **Then** it includes "UAT Verification: Missed".

## 5. Overall Test Strategy & Quality Goal (测试策略与质量目标)
- **Unit Testing**: Add unit tests in the `leio-sdlc` test suite to assert the outputs of `format_notification` for each of the newly added event types, verifying that the "未知事件" fallback is no longer triggered for them.

## 6. Framework Modifications (框架防篡改声明)
- `scripts/notification_formatter.py`

## 7. Hardcoded Content (硬编码内容)
> **[CRITICAL INSTRUCTION FOR PM & CODER]**
> **Anti-Hallucination Policy (防幻觉策略):** 
> 凡是本需求涉及需要精确输出的字符串（如 Error Message、正则法则、配置文件等），**PM 必须在此处使用 Markdown 代码块（单行或多行）一字不落地定义清楚**。

- **Formatter Output Strings (For `notification_formatter.py`)**:
```python
# For event_type == "auditor_approved"
return f"✅ [Auditor] PRD 审查通过 (APPROVED)。"

# For event_type == "auditor_rejected"
return f"❌ [Auditor] PRD 审查未通过 (REJECTED)，请根据反馈进行修改并重试。"

# For event_type == "uat_complete" and status == "PASS"
return f"🎉 [{prd_match}] UAT Verification: Passed."

# For event_type == "uat_complete" and status != "PASS"
return f"⚠️ [{prd_match}] UAT Verification: Missed (Needs Fix)."

# For event_type == "uat_error"
return f"❌ [{prd_match}] UAT Verification Error: 测试报告解析失败或发生异常。"
```