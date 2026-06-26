# 最小验证步骤

## A. 基础验证

部署后先确认：

1. 配置校验通过

```bash
openclaw config validate --json
```

2. service 正常

```bash
systemctl is-active <SERVICE_NAME>
```

3. 根页面可打开

访问：
- `<LIVE_GATEWAY_URL>`

应看到 Control UI 正常加载。

---

## B. disposable thread 最小验收

### 目标

验证：
- visible thread 不变
- successor rollover 真实发生
- hidden handoff 不外露
- 普通聊天页**不出现 continuity/context 提示**
- 高 context 轮次仍返回完整回答，而不是明显先缩短再切换

### 步骤

1. 打开一个 disposable thread  
   例如使用新的 session key 或新的测试会话。

2. 发第一条 seed 消息  
   示例：
   - `Please reply with READY only.`

3. 等第一轮 session store settled  
   注意：不要在第一轮仍是 `status=running` 时就去改 token。

4. 把这个 disposable thread 的 `totalTokens/contextTokens` 压到 rollover 区间  
   例如构造让下一轮进入 90% 左右上下文使用率。

5. 再发第二条复杂消息  
   示例：
   - 排错 / 比较 / 多步骤问题

6. 验证以下结果：
   - root session 上存在 `continuityThreadId`
   - `threadActiveSessionKey` 指向 successor
   - `successorSessionKey` 存在
   - `gateway-thread-index.json` 里有完整 thread record
   - successor transcript 里有 hidden handoff
   - 用户可见历史里看不到 hidden handoff
   - `visibleThreadUnchanged = true`
   - `visibleContainsHiddenHandoff = false`
   - `noticeSeen = false`
   - `compactPrepareHintSeen = false`
   - `contextUsedHintSeen = false`
   - 第二条复杂消息仍保持正常回答质量，不依赖“先缩短/先敷衍”来换 rollover

---

## C. 验收通过的最低标准

simple / happy path 至少要满足：
- visible thread 不变
- successor 已创建
- hidden handoff 不外露
- 普通聊天页不显示 continuity/context 提示
- rollover 附近的复杂回答质量保持正常

如果这些都通过，才算 continuity / rollover 在当前环境里真正落地。
