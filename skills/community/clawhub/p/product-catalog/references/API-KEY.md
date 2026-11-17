# API密钥与计费

用户只需平台 Key，不提供模型或 S3 凭证。优先 `PRODUCT_CATALOG_API_KEY`，为空使用 `AI_SKILLS_API_KEY`，两者均缺失时停止。不要记录、输出或要求对话中粘贴完整密钥。

`catalog.translate` 按已验证的实际输入/输出Token收费，已批准且源文未变的译文可复用而不调用模型。`catalog.generate` 使用 canonical data，每语言每100个启用SKU向上取整，1–100为1单元，101–200为2单元；只有完整PDF、页图和清单质量通过并成功保存后计成功生成费。其余四个操作、上传、管理、导出、下载免费并限流；同任务幂等重放不重复扣款。页面显示当前人民币价格，使用前核对报价。

响应计费头为 `X-AI-Skills-Billing-Currency`、`X-AI-Skills-Billing-Charged` 和 `X-AI-Skills-Billing-Balance`。失败与不确定上游状态遵循平台对账，不能另建任务试图重复执行。

## 费用确认的实际入口

目前没有对 OpenClaw 开放的价格查询、余额查询或翻译预留试算 API。让用户在登录后的产品工作台取得当前单价/翻译预留上限与余额，并明确授权；无法取得当前价格依据时停在免费资料整理阶段。不能提交一次收费任务来探价，不能虚构 `/quote` 或 `/balance` 接口。

生成前展示语言、已确认版本、产品数、计费单元及当前单价；翻译前展示将传输的文字范围、Token 单价、预留上限及按实际用量结算方式。英文目录的翻译与生成是两次不同收费，确认译文不等于授权生成费。工作台的费用确认表单不是 Bearer API；通用任务 API 没有 `generation_fee`、`translation_maximum_fee` 等网页字段，不能夹带到 API 请求或宣称 API 已强制限制用户预算。
