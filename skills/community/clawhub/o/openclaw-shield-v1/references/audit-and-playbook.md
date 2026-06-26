# 审计事件与部署检查

## 审计字段

每条审计日志至少记录：
- `timestamp`
- `session_id`
- `event_type`
- `source`
- `risk_level`
- `action_taken`
- `rule_triggered`
- `taint_active`
- `details`

## 建议事件类型

- `injection_detected`
- `command_check`
- `command_blocked`
- `command_confirmed`
- `path_violation`
- `network_violation`
- `metadata_access_blocked`
- `sensitive_filtered`
- `taint_activated`
- `taint_cleared`
- `owner_auth_success`
- `owner_auth_failed`
- `config_change`
- `outbound_connection`
- `alert_escalation`

## 首次部署检查

1. `shield.py scan`
2. `shield.py passphrase set`
3. 配置并校验 `network.server_public_ip` 与 `network.server_internal_ip`
4. 检查日志目录权限
5. 开启 append-only 日志策略
6. 确认运行用户不是 root
7. 验证 metadata 拦截
8. 验证凭证路径拦截
9. 验证反弹 shell 拦截
10. `shield.py status` 检查总览

## 响应模板

### Owner 提醒模板

- 你即将执行: `<操作>`
- 影响范围: `<范围>`
- 风险说明: `<简短说明>`
- 是否继续: `y/n`
- 可选替代方案: `<更安全方案>`

### 拦截模板

- 操作已阻止
- 检测到: `<威胁类型>`
- 风险等级: `<等级>`
- 来源分析: `<agent 或 external>`
- 触发规则: `<规则名>`
- 处置建议: `<如果确需执行，需 Owner 明确确认>`
