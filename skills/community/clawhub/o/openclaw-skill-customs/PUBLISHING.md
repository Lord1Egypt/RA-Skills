# Publishing / provenance notes

- Publisher: DaoFei AI
- Service homepage: https://platform.daofeiai.com
- Skill purpose: 海关报关智能助手 — 上传单据、智能分类、提取报关数据、生成报关 Excel。

## Required credential

This skill requires exactly one credential:

- `LEAP_API_KEY` — required

Do not paste the API key into chat. Configure it through the platform's secure environment-variable setting for this skill.

API Key 获取方式：在 Leap 开放平台「API Key 管理」页面创建。

## Safety / usage notes

- 此技能仅处理用户主动上传的报关单据文件，不会访问用户系统中的其他文件。
- 所有文件数据均通过 HTTPS 加密传输至 Leap 平台处理。
- 处理结果中可能包含商业敏感信息（金额、商品编码等），请注意信息安全。
- 此技能不会请求与报关业务无关的任何凭证。
