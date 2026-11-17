# 发布结果、重试与交付

发布或更新结束时读本页，核对结果并交付链接与认领入口。

## 完成条件与失败处理

发布前客户端保存操作日志。保留 stderr 的 `operation_id` 和 `site_id`；失败后同源文件、标题和目标重跑会续用未完成操作。也可显式使用 `--operation-id 原UUID`。内容变更产生幂等冲突时恢复原输入，或在用户确实要求新操作时使用新 ID；不能为了绕过不确定结果而换 ID。

网络请求在每次请求最多 60 秒预算内有限重试，遵守 Retry-After。仍失败后最多手动续试一次；保留原 ID 并报告错误，不循环创建身份、上传或轮询。平台尚未配置、配额不足、权限错误不靠登录解决。

仅当客户端退出成功且 `status=ready`、当前 `deployment_id` 等于 `operation_deployment_id` 时交付“已发布”，直接使用服务端返回的真实 `url` 和 `expires_at`。`superseded` 表示旧请求已经被更新覆盖，不能声称旧版本刚刚上线。上传成功但公开入口验证失败时说明“文件已提交，公开访问尚未验证”，保留 ID；HEAD 通过也不证明游戏逻辑或外部依赖完全正常。交付时分别说明静态检查、本地浏览器验证和公开链接验证的实际结果；没有浏览器能力时明确未做运行验证，不承诺无白屏或安全无漏洞。

公开作品地址为 `/p/` 加 8 位小写字母数字，私有认领地址为 `/connect/` 加 10 位小写字母数字。直接使用服务端返回的 URL，不从作品 UUID 截断、转换或猜测短码；管理命令仍用 `site_id` UUID，旧长链接继续可用。本地预览使用 `/p/preview0/`，不是线上作品地址。

交付作品的公开 `url`；作品 `expires_at=null` 表示无到期限制，不把 null 当成日期。若连接旧服务返回具体时间，按实际响应说明有效期。`creator.status=awaiting_wechat` 时，直接用图片形式展示客户端生成的本地 `creator.qr_path`（Markdown 使用绝对路径），让 PC 用户用微信扫一扫；同时附“打开微信认领页”链接 `creator.claim_url`，不要只返回裸链接或图片文件路径。图片下面显示核对码 `creator.verification_code`、有效期，并说明“核对码无需输入，微信确认页与这里一致后再确认”；确认后当前匿名账号下全部作品归入微信账号。桌面打开链接显示扫码页，在微信内打开直接进入授权。客户端返回 qr_error 或宿主无法展示图片时，明确说明并交付认领页链接，PC 用户可在页面上扫码，不因此重传作品。不能把认领链接加到作品 URL、HTML、二维码分享卡片或公开宣传文案中；若当前交付渠道公开，先只给作品链接，认领入口在用户私有会话中交付。匿名凭证丢失且尚未认领会失去管理权限。

生成认领入口是发布的附带能力，不等待扫码、不轮询微信、不代用户确认，不阻塞分享。仅 `creator.status=claimed` 或服务端确认身份已绑定时才能声称认领完成。过期后用户要求认领时执行 `python3 "/实际skill目录/scripts/litepage.py" claim 作品UUID`，无需重传文件；详细流程见[账号与授权](account.md)。不要输出 HTML 全文、完整文件清单或任何凭证。不要自动往群聊、Echo 或其他平台发消息；发布作品不包含替用户传播的授权。


## 可见性与密码提醒

发布／更新成功后优先按实际 sharing，旧服务回退到 visibility 与 password_protected 说明访问状态，简短转述 CLI sharing_hint；旧客户端没有此字段时依下列规则组织文案。不能因新作品默认 private 就把已有 public 作品说成 private，也不能把 private 说成只有作者可见。提醒只介绍可选操作，不自动切换可见性、设置／移除密码。

- sharing=approval：“作品需要发布者授权，访客微信登录后主动申请，获批账号可访问；转发链接不会转移权限。”不得按旧 private 规则交付为持链接可直接访问。
- private 且无密码：“仅链接访问，持有链接的人可直接读取，不在首页展示。可改为 public 进入首页，也可设置密码保护作品。”
- public 且无密码：“公开展示，可在首页被发现，持有链接的人可直接读取。可改为 private 停止首页展示；如需保护内容，可设为 private 并设置密码。”
- 已有密码：“已设置密码保护，访客需输入密码，不在首页展示。可在作品管理中更换或移除密码。”

修改可见性或密码时按用户后续授权执行[管理操作](management.md#管理操作与授权)或[重设页面密码](management.md#重设页面密码)，无需重新发布作品，链接保持不变。

## 完整结果示例：已认领账号发布成功

以下为虚构示例，覆盖普通发布结果的全部业务字段；可选扩展字段未出现。URL、UUID、日期和本地路径只用于理解结构，执行时必须使用当前客户端的实际返回值。

```json
{
  "password_protected": false,
  "site_id": "51a22e6c-837a-4dd7-941f-45c27ce9a2ef",
  "title": "接水果",
  "visibility": "private",
  "description": "用左右方向键接住水果",
  "preview_url": null,
  "deployment_id": "d903560f-4d14-4fb3-8de2-0d93728c55c4",
  "revision": 1,
  "status": "ready",
  "url": "https://lightpage.hqdx.store/p/abcd1234/",
  "api_url": "https://lightpage.hqdx.store/v1/hosting/sites/51a22e6c-837a-4dd7-941f-45c27ce9a2ef",
  "expires_at": null,
  "created_at": "2026-11-12T13:00:00Z",
  "operation_deployment_id": "d903560f-4d14-4fb3-8de2-0d93728c55c4",
  "replayed": false,
  "sharing_hint": "作品为仅链接访问（private），持有链接的人可直接读取，不在轻页首页展示。可改为 public，让作品在首页被发现；也可设置密码，要求访客输入密码后读取。",
  "creator": {
    "status": "claimed",
    "scope": "anonymous_account",
    "claim_url": null,
    "verification_code": null,
    "expires_at": null
  }
}
```

假定静态检查、本地浏览器关键交互和公开入口 HEAD 均已实际通过，可以这样交付：

> 已发布：[接水果](https://lightpage.hqdx.store/p/abcd1234/)。仅链接访问（private），持有链接的人可直接读取，不在轻页首页展示；作品无到期时间。可改为 public，让作品在首页被发现；也可设置密码保护作品。静态检查、本地浏览器关键交互及公开入口校验通过，未验证线上浏览器运行。未提供封面截图，首页将使用默认封面。后续更新使用作品 ID `51a22e6c-837a-4dd7-941f-45c27ce9a2ef`，链接保持不变。

没有实际通过的检查不能照抄。默认不展示 JSON 全文、重复打印 operation_id 或附分享二维码；有影响使用的 warning 时简短说明。

## 完整结果示例：匿名发布成功、等待微信认领

```json
{
  "password_protected": false,
  "site_id": "ba1b4b8a-92b0-41cb-9542-59b669097c9e",
  "title": "活动说明",
  "visibility": "private",
  "description": "",
  "preview_url": null,
  "deployment_id": "63a9824e-35c8-4b16-b793-cd8d927a028b",
  "revision": 1,
  "status": "ready",
  "url": "https://lightpage.hqdx.store/p/efgh5678/",
  "api_url": "https://lightpage.hqdx.store/v1/hosting/sites/ba1b4b8a-92b0-41cb-9542-59b669097c9e",
  "expires_at": null,
  "created_at": "2026-11-12T13:10:00Z",
  "operation_deployment_id": "63a9824e-35c8-4b16-b793-cd8d927a028b",
  "replayed": false,
  "sharing_hint": "作品为仅链接访问（private），持有链接的人可直接读取，不在轻页首页展示。可改为 public，让作品在首页被发现；也可设置密码，要求访客输入密码后读取。",
  "creator": {
    "status": "awaiting_wechat",
    "scope": "anonymous_account",
    "claim_url": "https://lightpage.hqdx.store/connect/abcd123456/",
    "verification_code": "AB12CD34",
    "expires_at": "2026-11-12T13:20:00Z",
    "qr_path": "/Users/example/.config/litepage/claim-example.png"
  }
}
```

在创作者的私有会话中交付作品链接，说明“作品仅链接访问（private），持有链接的人可直接读取，不在轻页首页展示；作品无到期时间。可改为 public 进入首页，也可设置密码保护作品”。接着展示**实际返回路径**的认领二维码图片，附实际 claim_url、核对码及认领入口有效期：

```markdown
![微信认领二维码](/实际客户端返回的绝对路径.png)
[打开微信认领页](实际返回的claim_url)
核对码：实际返回的verification_code（无需输入，手机确认页一致后再确认）。
认领入口有效期：实际返回的creator.expires_at。确认后此匿名账号下全部作品归入微信账号。
```

这是展示格式模板，不可直接发送占位路径。此时作品已发布，但认领尚未完成，不等待扫码、不代用户确认。若 creator 中为 qr_error 而非 qr_path，说明图片生成失败并提供认领页链接，页面仍可扫码；无需重传。若当前渠道公开，只交付作品链接，私有认领信息另在创作者私有会话中提供。

## 密码作品的交付

启用密码时，完整结果额外字段 password_protected=true（上面的普通作品示例为 false）；先确认客户端成功及版本一致，再说明链接需要密码、浏览器授权一小时。密码只按用户指定渠道单独提供，不附入作品 URL、JSON 全文或二维码；未确认保护时不把链接交付为受保护作品。

审批分享无需植入 JS；平台在返回任何文件前检查授权。CLI 使用无凭证 HEAD 核对审批保护标记；未验证保护时不交付为受限作品。完整命令与人类许可见[访问授权](access.md)。
