# 配置灵犀API

## 环境变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| LYK_API_KEY | 灵犀API认证密钥（格式：`lyk-xxx`） | `lyk-xxx` |
| LYK_API_URL | API基础URL | `https://aiapi.szyldata.com` |

---

## API Key 存储位置

API Key 不是存在系统环境变量，而是存在 OpenClaw 配置文件：

```
~/.openclaw/openclaw.json
```

路径：`skills.entries.lingxiai.env.LYK_API_KEY`

**查看当前 Key：**
```bash
cat ~/.openclaw/openclaw.json | grep LYK_API_KEY
```

**修改 Key：** 直接编辑 `~/.openclaw/openclaw.json`，找到 `LYK_API_KEY` 字段更新值即可。

---

## 配置命令

用户说「配置灵犀」或「连接灵犀」时，提示输入 API Key：

```
请提供您的灵犀API Key（格式：lyk-xxx），您可以在灵犀AI设置页面获取。
```

获取后保存到 `~/.openclaw/openclaw.json` 的 `skills.entries.lingxiai.env.LYK_API_KEY` 字段。

---

## 验证配置

调用录音列表接口验证（无参请求）：

```bash
# 销售录音（无参）
curl -X GET "https://aiapi.szyldata.com/api/api/apiKeyConfig/innerApi/userRecordingQuery" \
  -H "AuthorizationLyk: 您的API_KEY" \
  -H "Accept: */*"

# 会议录音（无参）
curl -X GET "https://aiapi.szyldata.com/api/api/apiKeyConfig/innerApi/userRecordingMeetingQuery" \
  -H "AuthorizationLyk: 您的API_KEY" \
  -H "Accept: */*"
```

返回 `code: 200` 且有 `data` 数组即配置成功。

---

## URL 路径说明

> ⚠️ 完整路径为 `/api/api/apiKeyConfig/innerApi/...`（双 `/api`），拼接结果：`https://aiapi.szyldata.com/api/api/apiKeyConfig/innerApi/...`