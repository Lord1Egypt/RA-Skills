# config.json 示例（路由 A 邮箱 + B/C 线上 API）

将下列字段合并进本 Skill 目录下的 `config.json`。**勿**把真实 Key 提交到公开仓库。

```json
{
  "hifleet_api_key": "在 HiFleet / mytonnages 网站获取的 API Key（与账号绑定、按次计费）",
  "hifleet_liner_api_base": "https://api.hifleet.com/openclaw/vessel/charter/liner",
  "hifleet_charter_api_base": "https://api.hifleet.com/openclaw/vessel/charter",
  "charter_enrich_url": "https://api.hifleet.com/openclaw/vessel/charter/enrich-row",
  "mail_parse_interval_minutes": 10,
  "imap_host": "imap.example.com",
  "imap_port": 993,
  "email": "user@example.com",
  "email_password": "第三方客户端密码（本地存储，勿提交仓库）"
}
```

- **`hifleet_api_key`**：**路由 B（班轮）、C（预抵）必填**；路由 A 补充船舶信息也需要。或 **`HIFLEET_API_KEY`**。见 **`FIRST_SETUP.md` §C**。  
- **邮箱字段**：**仅路由 A**；见 **`WORKFLOW_1_MAIL.md`**。  
- **`hifleet_liner_api_base`**：路由 B；班轮解锁 `POST …/liner/unlock`。  
- **`hifleet_charter_api_base`**：路由 A 档案/portid、**路由 C** 预抵查询根路径。  
- **`charter_enrich_url`**：路由 A 单行补充信息（IMO/tags/档案），默认公网 **`…/enrich-row`**。  
- **`mail_parse_interval_minutes`**：邮件定时解析，默认 **10** 分钟（**`MAIL_PARSE_SCHEDULE.md`**）。
