# 2.0 正式发布验收

本文件只用于汇总真实验收结果，不替代实际运行，也不扩大专家团的外部操作权限。

## 核心正式能力

omni-ecom v2.0.3 的正式核心是“用户授权读取的后台导出报表 → 全量识别与口径复算 → WorkBuddy/Codex 真实多专家协作 → 图表化 PDF → 独立交付复核”。发布必须取得两类真实证据：

1. WorkBuddy 原生多专家、PDF 和独立复核完整通过；
2. Codex 原生多专家、PDF 和独立复核完整通过。

两类证据都必须来自真实宿主运行，显示 `status=PASS`、`environment=live`、目标版本、真实任务身份和来源 SHA256。合成测试、mock、fixture、候选自述或仅有报告文件不能替代。

## 可选扩展能力

以下能力不属于报表型专家团正式发布的前置条件：

- `platform_api_read`：平台 API 直接读取；
- `controlled_action_readback`：后台受控动作与结果回读；
- `live_model_route_baseline`：跨模型真实基线与路线建议。

缺少真实验收时，发布回执必须把对应能力标记为 `not_enabled`。专家团不得调用、宣传或暗示它们可用。将来取得真实授权和证据后，可独立验收并在后续版本中启用。天猫等只提供商家后台导出而没有开放 API 的场景，继续使用文件导入主链路，不得把人工导出冒充 API 读取。

## 生成发布回执

把两类核心证据的实际 SHA256 写入 `omni-ecom.release-acceptance-ledger@2.0` 后运行：

```text
python scripts/release_acceptance_guard.py acceptance-ledger.json --target-version 2.0.3 --output release-acceptance.json
```

只有两类核心证据均通过时才写出 `omni-ecom.release-acceptance-receipt@2.0`。回执同时公开三项可选能力的 `enabled/not_enabled` 状态。失败时只输出诊断，不写正式回执。

这张回执只证明报表分析核心达到发布条件，不授予预算、调价、库存、发布、投放或任何平台写入权限。每次外部动作仍须另行接入、验收和明确批准。
