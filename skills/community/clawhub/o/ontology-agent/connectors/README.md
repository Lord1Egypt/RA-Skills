# 连接器（connectors）· 对接真实 IM 与资料库

本目录是**数字公司（专家团）对接真实系统的端口层**。当前为 **stub（桩）实现**：
未配置任何 API 凭证时，所有方法只打印提示、**绝不发起真实网络请求**；
填入凭证并补全 `TODO` 后即可启用真实对接。

## 一、IM 连接器（钉钉 / 企业微信 / 飞书）

数字公司未来可经 IM 推消息、收事件、给真实员工分配角色视图。

| 文件 | 平台 | 凭证字段（占位，需替换） |
|---|---|---|
| `dingtalk.py` | 钉钉 | `app_key` / `app_secret` |
| `wecom.py` | 企业微信 | `corpid` / `corpsecret` / `agentid` |
| `feishu.py` | 飞书 | `app_id` / `app_secret` |

统一接口（`BaseIMConnector`）：
- `send_message(to, text)` — 推送消息
- `receive_events()` — 拉取/订阅事件（@消息、审批等）
- `get_users()` — 拉取组织成员（用于真实员工角色视图）

### 启用步骤
1. 打开对应平台文件，把 `CREDENTIALS` 的"填入…"替换成真实凭证。
2. 在对应方法的 `TODO` 处接入真实开放 API（已给出接口路径与调用顺序）。
3. 通过工厂调用：
   ```python
   from connectors import get_connector
   im = get_connector("dingtalk")   # / "wecom" / "feishu"
   im.send_message("userid123", "今日运营日报已生成")
   ```
> 未配置时 `im.status()["configured"] == False`，调用方法会打印 `[stub]` 提示并安全返回 None。

## 二、资料库连接器（本地 SQLite → 在线主库）

本地数据层见 `scripts/ops_db.py`（`OpsDB`）。在线主库对接端口见其中的
`RemoteDatasource` 类：把 `CREDENTIALS`（space_id / api_token / endpoint）
替换为真实 WorkBuddy 资料库信息，并补全 `push` / `pull` 的 `TODO` 即可实现双写。

## 设计原则
- **默认不联网**：任何凭证缺失都走 stub，保证装包即用、不泄漏、不误发。
- **端口清晰**：每处外部对接都是显式 `CREDENTIALS` + `TODO`，便于后续逐一接真。
- **厂商中立**：钉钉/企微/飞书并列，新增平台只需加一个子类并在 `__init__.py` 注册。
