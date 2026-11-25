# 琉璃金山桥 · 接入与凭证配置说明

> 本文件**不含任何明文密钥**，只描述配置方法。AppSecret / token / code 明文严禁写入本目录或任何分发文件。

## 一、需要的前置（一次性，由掌握 WPS 后台者完成）
1. **企业自建应用**：在 WPS 开放平台用大陆企业主体建成自建应用，拿到 `AppID(client_id)` 与 `AppSecret(client_secret)`。
2. **权限 scope**：Permission Management 申请并通过多维表 `kso.dbsheet.read` / `kso.dbsheet.readwrite`（**user 态**也要激活）。
3. **OAuth 回调**：Security Settings 填入一个 **https、公网可达**的回调地址（本项目用 `https://wps.hu5.cn/`，由 Cloudflare Worker 承接 code，存 KV 15 分钟，回显可复制，并提供 `/latest` 带外取回）。
4. **建版本 → 提审 → 企业超管审批 → 发版**：user scope 随发版生效。

## 二、获取 user token（authorization_code）
授权 URL 模板（state 用随机值，redirect_uri 与后台完全一致含尾斜杠）：
```
GET https://openapi.wps.cn/oauth2/auth?response_type=code&client_id=<AppID>&redirect_uri=https%3A%2F%2Fwps.hu5.cn%2F&scope=kso.dbsheet.read%2Ckso.dbsheet.readwrite&state=<随机>
```
用户同意 → 302 回调带 `code` → 用 code 换 token：
```
POST https://openapi.wps.cn/oauth2/token
  grant_type=authorization_code
  client_id=<AppID>
  client_secret=<AppSecret>   # 带外注入，仅内存/命令内联，不落明文
  code=<授权code>             # 一次性，10 分钟有效
  redirect_uri=https://wps.hu5.cn/   # 必须与授权时一致
```
返回 `access_token`（约 2 小时）与 `refresh_token`（约 365 天）。

## 三、本地凭证目录（600）
`~/.config/wps-openapi/`（权限 `700`）：
| 文件 | 内容 |
|---|---|
| `client_id` | AppID |
| `client_secret` | AppSecret（带外注入，勿外传） |
| `access_token` | 短时令牌（脚本自动维护） |
| `refresh_token` | 长效刷新令牌（脚本自动轮换维护） |

```bash
mkdir -p ~/.config/wps-openapi && chmod 700 ~/.config/wps-openapi
# 由各凭据以 600 写入；切勿 echo 明文到对话/日志
```

## 四、运行期自动刷新
`wps_auth.cjs` 的 `ensureToken()`：access_token 临期(≤5min)或缺失时，自动用 refresh_token 换新的并把新 access/refresh 落回 600（refresh 轮换，旧 refresh 作废）。因此日常读写**无需重复授权**，refresh 一年内有效。

## 五、调用接口
- 读结构：`GET /v7/coop/dbsheet/<file_id>/schema`
- 写记录：`POST /v7/coop/dbsheet/<file_id>/sheets/<sheet_id>/records/create`
  - body：`{"records":[{"fields_value":"{\"<主字段>\":\"<值>\"}"}]}`（字段值是 JSON 字符串）
- 鉴权头：`Authorization: Bearer <access_token>`；未开启接口签名时无需 KSO-1 头。

## 六、常见错误码
| code | 含义 | 排查 |
|---|---|---|
| 401 40100008 invalid_client | client_id/secret 不匹配 | 确认 AppID 与 AppSecret 属同一应用 |
| 401 40100009 invalid_grant | code 过期/已用/OCR错、refresh 失效 | 重新授权拿新 code；核对 redirect_uri |
| 403 403000001 PermissionDenied | scope 不足（app token 缺文件级 scope） | 走 user token；或确认 user scope 已发版生效 |
| 401000001 header not found | 缺 Authorization 头 | 确认带 Bearer token |

## 七、给下载者的分发说明（必读·凭证各配各的）

**本技能包零明文密钥，下载后 NOT 开箱即用——每位使用者须配自己的一把钥匙。**

### 为什么不给统一钥匙
- `client_secret` 是应用级凭证，公开分发＝把应用钥匙散出去，**红线禁止**；
- `refresh_token` 是**用户个人授权**，且 refresh 每次刷新会作废旧 token——**多人共用必然互相顶掉**（本项目洲/玉共用曾触发 `invalid_grant`，已按"各自独立授权"解耦）；
- 因此：玉的钥匙给不了别人、也不该给；别人也用不了玉的表（那是用他的账号授权的空间）。

### 别人下载后三步自用
1. **自建应用**：在 WPS 开放平台用**自己的企业主体**建自建应用，拿自己的 AppID／AppSecret；
2. **自己授权**：用**自己的 WPS 账号**走本文件第二节的 OAuth 流程，拿自己的 `refresh_token`（约 365 天）；
3. **本地落盘**：在本机 `~/.config/wps-openapi/`（700 目录／600 文件）写好四项凭证，之后脚本自动续期，日常无需再管。

### 边界与责任
- 谁授权谁负责：凭证安全、授权范围、所读写表格的内容合规，均由使用者自负；
- 本技能只提供"接入方法＋脚本"，不代建应用、不代授权、不保管任何人的凭证；
- 若希望省去自建应用的门槛，可另行约定**代配置服务**（属服务层，不属本技能包，需单独授权与定价）。

## 八、安全红线（不可破）
- 明文 secret/token/code：不入对话、信箱、代码、日志，**不打进技能分发包**。
- 带外密钥邮件"即用即焚"；凭证只存活于 600 文件。
- 多端共用同一 refresh 须约定单一持有方轮换；并发写同表须错开时间。
