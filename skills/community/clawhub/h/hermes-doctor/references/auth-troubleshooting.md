# Auth / 401 排查

## 类型 1:占位符注入(`Bearer no-key-required` / 字面单词)

**症状**:request_dump 里 `request.headers.Authorization` 是 `Bearer no-key-required` 或 `Bearer expired` 之类的**字面字符串**,而不是真 key。

**根因**:hermes 的 provider 解析链没找到该 provider 的凭证,fallback 到了占位符。

**确认方法**:
```bash
HOME_DIR="$(reg query "HKCU\Environment" /v HERMES_HOME 2>/dev/null | awk '/HERMES_HOME/{print $NF}')"
[ -z "$HOME_DIR" ] && HOME_DIR="$HOME/.hermes"
ls -t "$HOME_DIR/sessions/request_dump_*.json" 2>/dev/null | head -1 | xargs grep -A1 "Authorization"
```
看到 `no-key-r****ired` 就锁定。

**修复路径 A(优先,v2026.4.3+ 版本)**:
```bash
hermes auth add deepseek --type api-key --api-key sk-NEWKEY
hermes auth list                  # 验证
# 重启 hermes
```

但**目前主流版本(0.10.x 及之前)仍命中 issue #15914** — `hermes_cli/auth.py` 中 `_resolve_api_key_provider_secret()` 只读 `os.getenv()`,不读 credential_pool。所以即便 `hermes auth add` 成功,启动时 env 里没对应 KEY 仍然 fallback 到占位符。**这种版本统一改用路径 B**。

**修复路径 B(手工 .env + auth.json 双写,标准修法)**:
1. 备份:`cp "$HOME_DIR/auth.json" "$HOME_DIR/auth.json.broken-$(date +%Y%m%d-%H%M%S)"` 同时备 .env
2. 编辑 `auth.json`,在 `credential_pool.<provider>` 下加一个对象:
   ```json
   {
     "id": "<6位随机十六进制>",
     "label": "<PROVIDER>_API_KEY",
     "auth_type": "api_key",
     "priority": 0,
     "source": "manual_repair",
     "access_token": "<可用的 key>",
     "last_status": null, "last_status_at": null,
     "last_error_code": null, "last_error_reason": null,
     "last_error_message": null, "last_error_reset_at": null,
     "base_url": "<provider 的 base_url,如 https://api.deepseek.com/v1>",
     "request_count": 0
   }
   ```
3. 同时把 `<HOME_DIR>/.env` 加上 `<PROVIDER>_API_KEY=<key>` 兜底(**因为 #15914,这一步在 0.10.x 及之前的版本是必须**)
4. **必须重启 hermes 进程** — auth 是启动时加载的
5. 验证:再发一次请求,看 `<HOME_DIR>/sessions/request_dump_*.json` 里 Authorization 已变成真 key 前 8 位 + `****`

**实战记录**:实地修过一例 — `auth.json.credential_pool.deepseek` 数组缺失 + 命中 #15914,hermes 启动后会自动从 .env 读取 DEEPSEEK_API_KEY 补全 pool,ping → pong。所以**双写最稳**。

## 类型 2:`hermes setup` 静默跳过 API key 输入(issue #16394)

**症状**:`hermes setup` 走到 provider 配置步骤,直接显示绿色 ✓ 不让你输入 key。

**根因**:`<HOME_DIR>/.env` 里已有该 provider 的 KEY 行(无论是否有效都跳过)。

**修复**:
```bash
cp "$HOME_DIR/.env" "$HOME_DIR/.env.broken-$(date +%Y%m%d-%H%M%S)"
# 编辑 .env,删掉 DEEPSEEK_API_KEY=... 那一行(或注释掉)
hermes setup           # 这次会弹输入框
```

参考:https://github.com/NousResearch/hermes-agent/issues/16394

## 类型 3:`****ired` 误读为 expired

**辨析**:`your api key: ****ired is invalid` 中 `ired` 不一定是过期 key 的末 4 位。看 hermes 日志的 mask 规则 — 如果实际 key 是 `no-key-required`,前 9 字符 `no-key-r` 显示,中间 4 个 `*` 替代,末 4 位 `ired` 露出。所以 `****ired` 极可能是字面 `no-key-required` 或 `expired`(server 可读文案)被替换。

**判断流程**:
1. 翻 `<HOME_DIR>/sessions/request_dump_*.json`,看 Authorization 完整原文(被 hermes 部分脱敏,但中间 `*` 数 + 头尾字符可还原)
2. 如果末位是 `ired` 头部是 `no-key-r` → **类型 1**(占位符)
3. 如果末位是 `ired` 头部是真 key 头部(如 `sk-12345`) → 真过期 key,去服务商重续
4. 都不是 → 看 server 返回的 `code` 字段,可能是 `invalid_request_error` / `authentication_error` 的语义提示

## provider env 变量优先级

源码 `hermes_cli/auth.py:95-260`,每个 provider 有 `api_key_env_vars` 元组,**靠前的变量优先**。常见:

| Provider | env 变量(顺序敏感) |
|---|---|
| copilot | COPILOT_GITHUB_TOKEN, GH_TOKEN, GITHUB_TOKEN |
| gemini | GOOGLE_API_KEY, GEMINI_API_KEY |
| zai | GLM_API_KEY, ZAI_API_KEY, Z_AI_API_KEY |
| anthropic | ANTHROPIC_API_KEY, ANTHROPIC_TOKEN, CLAUDE_CODE_OAUTH_TOKEN |
| deepseek | DEEPSEEK_API_KEY |
| alibaba (DashScope) | DASHSCOPE_API_KEY |
| xai | XAI_API_KEY |
| nvidia | NVIDIA_API_KEY |
| ai-gateway | AI_GATEWAY_API_KEY |

如果环境同时有 `GH_TOKEN` 和 `COPILOT_GITHUB_TOKEN`,前者会被后者覆盖。

## credential_pool 结构 cheat sheet

`<HOME_DIR>/auth.json`:
```json
{
  "version": 1,
  "providers": {},               // 高级:per-provider 全局策略,通常空
  "credential_pool": {
    "<provider-name>": [
      { "id": "...", "label": "...", "auth_type": "api_key|oauth_device_code",
        "priority": 0, "source": "...", "access_token": "...",
        "base_url": "...", "request_count": 0,
        "last_status": null, "last_status_at": null,
        "last_error_code": null, "last_error_reason": null,
        "last_error_message": null, "last_error_reset_at": null }
    ]
  },
  "updated_at": "ISO-8601"
}
```

每个 provider 数组可有多条,priority 数字小的优先。`source` 字段记录这条凭证从哪来(`env:DEEPSEEK_API_KEY` / `gh_cli` / `oauth` / `manual_repair`)。
