# 常见问题排查

## 1. AK/SK 未配置

**错误**：`请配置阿里云 AK/SK 环境变量`

**解决**：
```bash
export ALIBABA_CLOUD_ACCESS_KEY_ID="your-key"
export ALIBABA_CLOUD_ACCESS_KEY_SECRET="your-secret"
```

---

## 2. CCAI_APP_ID 未配置

**错误**：`请配置 CCAI_APP_ID 环境变量`

**解决**：Load references/setup.md，引导用户在百炼控制台获取 APP ID。

---

## 3. 权限不足

**错误**：`CCAI.IllegalPermission.NoAuth` 或 `CCAI.TenantPermission.NoAuth`

**可能原因**：
- AK/SK 对应的账号没有 CCAI AIO 服务权限
- 子账号未被授权访问指定业务空间

**解决**：
- 确认使用的是已开通 CCAI AIO 服务的账号的 AK/SK
- 如使用 RAM 子账号，联系主账号管理员授权 `ContactCenterAI:*` 权限

---

## 4. 参数错误

**错误**：`CCAI.InvalidParam.NotExist` 或 `CCAI.ParamInvalid.IllegalParamValue`

**可能原因**：
- `taskType` 不是 `"text"` 或 `"audio"`
- `resultTypes` 为空或包含无效值
- `service_inspection` 类型未提供 `serviceInspection` 配置

**解决**：检查 task.json 的字段格式，参考 references/input-formats.md

---

## 5. 任务超时

**错误**：`任务超时（超过 120 秒）`

**可能原因**：
- 音频文件较大，转写时间较长
- 服务端繁忙

**解决**：
- 语音文件建议控制在 30 分钟以内
- 稍后重试，或联系阿里云技术支持（钉钉群：147535001692）

---

## 6. 任务执行失败

**错误**：`任务执行失败: [taskErrorMessage]`

**可能原因**：
- 语音文件 URL 无法访问（需要公网可访问）
- 对话内容超过 2 万字限制
- 音频格式不支持

**解决**：
- 确认语音 URL 可以在浏览器中直接访问
- 文本内容超长时，分段提交
- 音频转换为 mp3 格式，8k 采样率

---

## 7. 限流错误

**错误**：`CCAI.Throttling.Qps` 或 `CCAI.Throttling.Qpm`

**解决**：
- 付费 API：购买更高 QPS/QPM 配额
- 免费 API：联系钉钉群（62730018475）申请提升
