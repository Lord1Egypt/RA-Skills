# 2.0：平台只读观察

本模块是未启用扩展：v2.0.3 导出报表正式版的 platform_api_read=not_enabled。常规报表任务不运行本模块，不要求用户申请 API；以下仅保留未来独立授权与验收的技术规范。

需要从平台接口读取店铺对象时使用本文。`scripts/platform_read_guard.py` 是独立只读入口，只产生 `omni-ecom.platform-read-observation@2.0`，不包含任何写入方法，也不会解析或输出密钥。

## 两类证据不能混用

- mock 连接器只能用于合成测试，结果固定为 `synthetic_mock_read`、`simulated=true`、`platform_connection_verified=false`，且只能使用 `acceptance_mode=synthetic`。
- 真实 API 连接器必须绑定宿主预先建立的 `ExecutionStore`、固定客户/平台/账号/店铺/连接器范围、有效的只读权限引用，并声明 `read_only_verified` 或 `write_ready`。通过后只记录为 `native_platform_api_observation`，仍明确 `independently_authenticated=false`、`formal_acceptance_completed=false`。
- 单次 API 返回不是独立第三方认证，也不是完整发布验收。只有真实 WorkBuddy/Codex 运行、真实来源、报告与 PDF、多人协作和完成链全部通过后，才能更新候选状态。

## 调用边界

可信宿主先创建本次运行并固定 binding，再构造仅含 `request_id / run_id / client_scope / platform / account_id / store_id / team_version / resource / platform_id / acceptance_mode` 的请求。权限对象只能是凭证引用，必须匹配同一客户和店铺、未过期，并包含 `<resource>.get`；请求或凭证中出现明文 token、密码、cookie、API key 时立即拒绝且不调用连接器。

读取返回必须匹配连接器、平台、资源和平台对象 ID，读取时间不超过 60 秒，并能从 `resource + platform_id + data` 重新算出来源指纹。观察凭证保存数据、数据指纹、返回指纹、连接器描述指纹和请求指纹，但不保存凭证 ID、`secret_ref` 或异常原文。同一 `request_id` 重放只返回原记录，不再次访问平台；若请求内容变化则阻断。

动作执行仍必须另走 [动作网关](action-gateway-v2.md)。平台读取凭证没有审批权或执行权，不能作为“动作已完成”的证据。

合成边界测试见 `scripts/platform_read_smoke.py`。它不会访问真实店铺，不能计入 `platform_read_acceptance`。
