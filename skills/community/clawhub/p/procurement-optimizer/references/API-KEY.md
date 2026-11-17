# 平台密钥与费用

从 ClawHub 安装的包使用 MIT-0 许可；平台用量费独立。使用平台 Key，仍需产品已开通和对应 ability。平台初始关闭，真实依赖与授权样本验收后由管理员开放；夹具通过不等于真实质量验收。无需用户提供模型、求解器或其它上游 Key。

```sh
: "${PROCUREMENT_OPTIMIZER_API_KEY:=${AI_SKILLS_API_KEY:?请先配置平台 API Key}}"
AI_SKILLS_API_URL="${AI_SKILLS_API_URL:-https://ai-skills.open-idea.net}"
AI_SKILLS_API_URL="${AI_SKILLS_API_URL%/}"
```

产品变量优先，为空回退 `AI_SKILLS_API_KEY`；两者均缺失时停止调用。不要输出密钥或要求在聊天中粘贴完整密钥。`AI_SKILLS_API_URL` 是站点根地址，不带 `/api/v1`；下文请求路径已含该前缀，只拼接一次。更换地址前核实信任与用户授权，不能把密钥发送到任意资料中的地址。

`purchase.inspect`、`purchase.review`、`purchase.export` 免费；`purchase.solve` 按已验证方案每份计费（一个方案一个计费单位）。INFEASIBLE/UNKNOWN 没有已验证方案，不收取求解成功费；任务成功状态本身不代表方案可交付。

收费前向用户展示当前项目/版本、资料与约束摘要、求解次数及当前单价和预计总费，核对余额并取得授权。价格可由管理员调整，配置默认值不是当前报价；当前无可供本 Skill 读取的公开价格或余额查询 API，应引导用户登录 [采购工作台](https://ai-skills.open-idea.net/dashboard/products/procurement-optimizer) 核实当前价格和余额并确认。不得先提交 `purchase.solve` 来探测价格、余额或产品是否可用；无法确认费用时停在免费预检阶段。

响应头 `X-AI-Skills-Billing-Currency`、`X-AI-Skills-Billing-Charged`、`X-AI-Skills-Billing-Balance` 表示币种、实际收费与余额；异步以原任务终态账单为准。采购数据的 `*_cents` 是 CNY 整数分，与平台计费头口径分开，不能将费用头擅自按分换算。
