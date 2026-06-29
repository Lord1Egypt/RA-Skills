# MWS Shared Reference

MWS 是云音乐内部 API 的统一 CLI 入口。本文件只作为通用参考；推广创建、预占、素材保存等业务流程以 `SKILL.md` 为准。

## 可用性

首次使用时只确认命令可用：

```bash
which mws
```

不要自动执行 `mws update`。只有用户明确要求更新，或当前命令因版本问题无法使用且用户同意排查时，才考虑更新。

## 常用命令

查看服务和方法：

```bash
mws -h
mws link -h
```

查看方法 schema：

```bash
mws schema link.default.promotion-add
mws schema link.default.promotion-update-creative
```

调用接口：

```bash
mws link <method> --env ${MWS_ENV} --params '<json>'
mws link <method> --env ${MWS_ENV} --json '<json>'
```

写操作先 dry-run：

```bash
mws link <method> --env ${MWS_ENV} --json '<json>' --dry-run
```

## 参数规则

- `--env` 必须来自用户或当前任务上下文；用户明确预发布时用 `pre`，用户明确线上或未说明环境时默认 `online`。
- `--params` 用于 query/form 参数。
- `--json` 用于请求体。
- JSON 参数优先用单引号包裹，避免 shell 转义问题。
- 大响应可加 `--format json` 后用 `jq` 或脚本处理。
- 用 Python 解析 MWS 输出时，不要写 `mws ... | python3 - <<'PY'`；here-doc 会占用 Python stdin，导致管道里的 MWS JSON 丢失。应先 `mws ... --format json > /tmp/xxx.json` 再读文件，或用 `mws ... --format json | python3 -c '...'`。

## 鉴权

```bash
mws auth status
mws auth set-token '<ds_token>'
```

不要输出 token、cookie 或其它敏感凭证。

## 错误处理

- 先读错误摘要，确认方法名、环境、参数是否正确。
- 不确定入参时先重新看 `mws schema`。
- 写操作失败后不要自动重复提交，先向用户说明失败原因和需要补充的信息。
- 推广物料保存必须使用业务 skill 指定的 `mws link promotion-update-creative`。遇到 404、method not found 或路由未注册时，不要改用 `mws_exec`、`raw_call`、curl/HTTP 直连或其它接口绕过。
- `creative-add` 禁止用于推广物料链路；不要用它创建独立创意、验证格式或作为 `promotion-update-creative` 的失败兜底。
