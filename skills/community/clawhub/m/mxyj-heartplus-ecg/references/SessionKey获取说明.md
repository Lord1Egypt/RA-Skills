# SessionKey获取说明

本文件定义 SessionKey 的唯一获取口径，用于稳定脚本调用链路。

## 适用范围

- `phone_manager.py`
- `gateway_manager.py`
- `api_manager.py`
- 所有需要 `--session-key` 的命令调用

## 固定解析优先级

1. 用户显式提供 sessionKey
2. 执行 `session_status`，仅从 `Session:` 字段提取 sessionKey
3. 若仍不可用，返回失败提示并停止执行脚本

标准失败提示：

未获取到有效会话标识。请提供可用的 sessionKey（例如 agent:main:main）后重试。

## 正向流程

1. 先检查用户输入中是否包含可用 sessionKey  
2. 未命中显式值时，执行 `session_status` 并读取 `Session:` 字段  
3. 从输出中的 `Session:` 字段提取值并作为唯一候选  
4. 候选值通过后，本轮全部业务命令透传同一 `--session-key`  
5. 若无有效值，直接返回失败提示，不进入任何业务脚本调用

## 反例（禁止行为）

- 把 UI 标签当作 sessionKey
- 把渠道名拼接成 sessionKey
- 把会话标题或昵称当作 sessionKey
- 在无法确认 sessionKey 时继续试探性执行脚本

## 回退策略

- 未拿到有效 sessionKey：立即回退到标准失败提示
- `session_status` 调用异常或无法读取 `Session:` 字段：不猜测、不降级为其他来源，直接失败提示
- `Session:` 字段缺失或为空：不继续执行，直接失败提示

## 可见性边界

- SessionKey 解析属于内部过程，不对用户逐步播报
- 禁止输出“我先检查 sessionKey”“我正在读取 session_status 的 Session: 字段”等过程话术
- 用户仅看到两类结果：业务结果，或最小失败提示

## 一致性要求

- 所有文档与话术统一使用“显式 > `session_status` 的 `Session:` 字段 > 失败提示”
- 文档中提到 `session_status` 时，必须明确从 `Session:` 字段取值
- 不使用 `sessionId` 替代 sessionKey
