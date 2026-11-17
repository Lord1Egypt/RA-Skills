# 一次性邮箱：真实注册与收验证邮件

用一次性邮箱 API 给每个 persona 注册一个全新账号，收验证邮件。下面以 [mail.tm](https://docs.mail.tm)
为例；它没有官方 SLA，取不到域名或收不到信时换同类服务（方法相同），并在报告里注明。

## 规则

- 一个 persona 一个邮箱，不复用。地址前缀带 `audit`，例如 `audit-novelist-20261008`。
- 邮箱密码与产品密码都随机生成，存 `~/.config/product-audit/<产品>-<环境>.json`，权限 `0600`，
  按 persona 分键合并写入（不覆盖其他 persona），不进任何仓库、不进报告。
- 一次性邮箱是公开服务：**验证邮件里的链接/验证码只用于本次注册**，不要贴进报告或日志。
- 有的产品会拦截一次性邮箱域名——这本身就是一条发现（记录拦截文案是否清楚），然后改用操作者
  提供的测试邮箱。
- 轮询收件箱：每 5–10 秒一次，最多 5 分钟；记录从提交注册到收到邮件的耗时。

## mail.tm 接口

基地址 `https://api.mail.tm`，JSON 请求需带 `Content-Type: application/json`。

| 步骤 | 请求 | 说明 |
|---|---|---|
| 1 取域名 | `GET /domains` | 返回 `hydra:member[]`，取一个 `isActive` 的 `domain` |
| 2 建邮箱 | `POST /accounts` `{"address","password"}` | 成功 201；地址被占用返回 422，换前缀重试 |
| 3 取令牌 | `POST /token` `{"address","password"}` | 返回 `{"token"}`，后续请求带 `Authorization: Bearer <token>` |
| 4 列邮件 | `GET /messages` | 返回 `hydra:member[]`，含 `id`、`from`、`subject`、`createdAt` |
| 5 读邮件 | `GET /messages/{id}` | 含 `text` 与 `html`；从中提取验证链接或验证码 |

## 示例脚本

宿主的 shell 状态不跨命令保留，而且 `set -e` 失败时会结束当前 shell。所以下面两段**各自是
一条独立命令**：用 `bash <<'SH' … SH` 在子 shell 里跑，开头 source 开跑时写好的
`$RUN/env.sh`（见 SKILL.md 第 2 节，路径换成当时打印的字面值），persona 显式写在脚本里。

第一段：为一个 persona 建邮箱并**合并写入**凭据文件（文件按 persona 分键，多个 persona 共用
一个文件；不要整体覆盖，否则前一个 persona 的凭据会丢，它就无法在「离开再回来」阶段重新登录）。

```bash
bash <<'SH'
set -euo pipefail
umask 077                                                  # 新建文件默认 0600
. ~/audit-runs/20261008-1400-zenstory-staging/env.sh       # 提供 RUN / PRODUCT / TARGET
PERSONA=novelist
CRED=~/.config/product-audit/$PRODUCT-$TARGET.json         # 运行目录与仓库之外
API=https://api.mail.tm
mkdir -p "$(dirname "$CRED")"
[ -f "$CRED" ] || echo '{}' > "$CRED"
if jq -e --arg p "$PERSONA" 'has($p)' "$CRED" >/dev/null; then
  echo "凭据文件里已有 ${PERSONA}，换一个 persona 名，或确认旧账号不再使用后再删该键" >&2; exit 1
fi
DOMAIN=$(curl -fsS "$API/domains" | jq -r '[.["hydra:member"][] | select(.isActive)][0].domain')
ADDR="audit-$PERSONA-$(date +%Y%m%d)-$RANDOM@$DOMAIN"
MAILPW=$(openssl rand -base64 18)
APPPW="Au$(openssl rand -hex 8)!9"                         # 满足常见密码规则
curl -fsS -X POST "$API/accounts" -H 'Content-Type: application/json' \
  -d "$(jq -n --arg a "$ADDR" --arg p "$MAILPW" '{address:$a,password:$p}')" >/dev/null
jq --arg p "$PERSONA" --arg a "$ADDR" --arg m "$MAILPW" --arg w "$APPPW" \
  '. + {($p): {email:$a, mail_password:$m, app_password:$w}}' "$CRED" > "$CRED.tmp"
mv "$CRED.tmp" "$CRED" && chmod 600 "$CRED"
echo "注册邮箱: $ADDR"                                       # 只打印邮箱，不打印密码
SH
```

浏览器里用该邮箱和 `app_password` 完成注册（密码从凭据文件读进表单，不要回显）后，第二段收信。
`FROM_HINT` 是发件人或标题里应出现的词，用来避开同一邮箱里的其他邮件；5 分钟没收到就明确失败：

```bash
bash <<'SH'
set -euo pipefail
umask 077
. ~/audit-runs/20261008-1400-zenstory-staging/env.sh
PERSONA=novelist; FROM_HINT=zenstory
CRED=~/.config/product-audit/$PRODUCT-$TARGET.json
API=https://api.mail.tm
ADDR=$(jq -r --arg p "$PERSONA" '.[$p].email' "$CRED")
MAILPW=$(jq -r --arg p "$PERSONA" '.[$p].mail_password' "$CRED")
TOKEN=$(curl -fsS -X POST "$API/token" -H 'Content-Type: application/json' \
  -d "$(jq -n --arg a "$ADDR" --arg p "$MAILPW" '{address:$a,password:$p}')" | jq -r .token)
ID=""
for i in $(seq 1 30); do                                   # 每 10 秒一次，最多 5 分钟
  ID=$(curl -fsS "$API/messages" -H "Authorization: Bearer $TOKEN" | jq -r --arg h "$FROM_HINT" '
    [.["hydra:member"][]
     | select(((.from.address // "") + " " + (.from.name // "") + " " + (.subject // ""))
              | ascii_downcase | contains($h | ascii_downcase))]
    | sort_by(.createdAt) | last | .id // empty')
  [ -n "$ID" ] && break
  sleep 10
done
if [ -z "$ID" ]; then
  echo "5 分钟内没有收到含“${FROM_HINT}”的验证邮件——这本身是一条发现，记进报告" >&2; exit 2
fi
curl -fsS "$API/messages/$ID" -H "Authorization: Bearer $TOKEN" \
  | jq -r '.text' > "$RUN/logs/$PERSONA-verify-mail.txt"   # 检查完内容后删除此文件
echo "已收到，内容在 $RUN/logs/$PERSONA-verify-mail.txt"
SH
```

从邮件中取出验证链接，在**同一个 persona 的浏览器 session** 里打开（`agent-browser --session <persona> open <链接>`），
而不是用 curl 访问——验证后的落地页也是体验的一部分。

邮件本身也要评估：发件人名称是否可信、标题是否说清用途、正文语言是否与注册时一致、链接是否
可点、有效期是否说明、会不会进垃圾箱（一次性邮箱无法判断这一点，报告中注明）。

收尾：报告附录只写邮箱地址；运行结束后删除 `logs/<persona>-verify-mail.txt`。
