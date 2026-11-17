# 授权与调用前检查

1. 安装并加载 `linkfox-amazon-store-auth`。
2. 运行 `python scripts/check_auth_dependency.py`。
3. 通过 auth Skill 的 authorized stores 能力让用户选择店铺，取得 `sellerId` 和 `region`。
4. 设置 `LINKFOX_AGENT_API_KEY`，或使用兼容变量 `LINKFOXAGENT_API_KEY`。
5. 不读取、不显示、不传递 Amazon access/refresh token。

常见失败：

- 网关 401/403：检查 LinkFox API key 和用户权限。
- Amazon 401/403：检查店铺授权、区域及角色。
- 网关提示路径白名单或模块不存在：确认当前部署已开放 `fulfillment/outbound/2026-07-04`；不要改用旧路径掩盖部署问题。
- 沙箱 operation：沿用 Amazon Store Skill 的统一网关配置；`updateOrderStatus`、`updatePackage` 只能用于 sandbox 测试数据。
