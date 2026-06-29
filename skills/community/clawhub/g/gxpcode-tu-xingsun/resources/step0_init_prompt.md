# GxpCode-制药法规跟踪 — Step 0 启动检查 Prompt

> 前置条件：首次使用前需运行 `python scripts/setup.py` 完成环境配置。

读取 `resources/config.yaml`，检查 `enterprise_type` 和 `focus_areas` 的值：

## A. 两者均为空（`[]` 或不存在）→ 执行对话式引导

依次询问：

> 请选择您的企业类型（可多选）：A. 化药  B. 中药  C. 生物制品  D. 原料药  E. 辅料包材

> 请选择重点关注领域（可多选，或输入"全部"）：GMP / 注册 / 变更 / 稳定性 / 工艺验证 / 分析方法 / 杂质 / 临床试验 / 药物警戒

确认后写入 `resources/config.yaml`（覆盖原有的空值），完成后进入 Step 1。

## B. 两者至少有一项非空 → 回显已有配置并确认

```
检测到已有配置：
  企业类型：<enterprise_type>
  重点关注：<focus_areas>
是否按此配置继续？（如需修改请告知）
```

用户确认后进入 Step 1；用户要求修改则先更新 config.yaml 再进入 Step 1。
