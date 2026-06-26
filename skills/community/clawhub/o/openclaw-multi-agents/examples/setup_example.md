# Multi-Agent Workflow Example: User Login Implementation

This example demonstrates the standard communication flow in a multi-agent team (Main, Manager, Worker) using OpenClaw session keys.

## 1. User Request (Main Agent Perspective)
**User:** "Help me implement a user login feature."

**Main Agent Action:** Immediately relay to Manager.
```javascript
// Target: agent:manager:main
// Channel: feishu (inherited)
message.send({
  target: "agent:manager:main",
  message: "Request: Implement user login feature. User: ou_123"
});
```

## 2. Manager Assignment (Manager Perspective)
Manager analyzes the task and selects a developer worker.
```javascript
// Target: agent:worker-dev:manager
message.send({
  target: "agent:worker-dev:manager",
  message: "Task: Implement user login (Node.js/Express). Reference: req_99"
});
```

## 3. Worker Completion (Worker Perspective)
Worker performs the coding/setup and reports back to the Manager's "main" inbox.
```javascript
// Target: agent:manager:main
message.send({
  target: "agent:manager:main",
  message: "Complete: Login logic implemented in /src/auth.js. Added passport-local."
});
```

## 4. QA & Relay (Manager Perspective)
Manager verifies the work. Once satisfied, relays to the Main Agent's specific manager-session.
```javascript
// Target: agent:main:manager
message.send({
  target: "agent:main:manager",
  message: "Status: Login feature implemented and verified. Ready for user."
});
```

## 5. Final Delivery (Main Agent Perspective)
Main Agent receives the update and informs the human user.
**Main Agent:** "I've implemented the user login feature using Node.js and Passport. You can find the logic in `/src/auth.js`."

---
## Key Session Mapping
| Role | Receiving Session (Input) | Sending To (Output) |
| :--- | :--- | :--- |
| **Main** | `agent:main:feishu:direct:*` | `agent:manager:main` |
| **Manager** | `agent:manager:main` | `agent:<workerId>:manager` |
| **Worker** | `agent:<workerId>:manager` | `agent:manager:main` |
| **Manager (QA)**| `agent:manager:main` | `agent:main:manager` |
| **Main (Relay)** | `agent:main:manager` | `feishu:direct:user_id` |
