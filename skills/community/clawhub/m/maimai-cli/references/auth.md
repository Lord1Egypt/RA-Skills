# 认证与安全

## 安装与检查

如果未安装：

```bash
uv tool install maimai-cli
```

检查可用性：

```bash
maimai --help
maimai status
```

## 导入 Cookie

推荐用户在自己的终端执行，不要把完整 Cookie 发到聊天里：

```bash
maimai import-cookie-header --cookie '完整 Cookie 头'
```

或：

```bash
export MAIMAI_COOKIE='完整 Cookie 头'
maimai import-cookie-header
```

## 检查登录状态

```bash
maimai status
maimai me
maimai cookies
```

适用场景：
- 用户说“已经登录了，帮我看看能不能用”
- 用户刚导入 Cookie，想确认是否成功
- 用户怀疑本地登录态失效

## 清理登录态

```bash
maimai logout
```

适用场景：
- 用户想切换账号
- 用户怀疑 Cookie 已泄露
- 工具状态异常，需要重新导入

## 强制安全规则

- 不要要求用户把完整 Cookie、`access_token`、`session`、`csrftoken` 贴进聊天
- 不要读取并回显本地保存的 Cookie 文件内容
- 不要在回复里复述用户已泄露的敏感值
- 如果用户已经泄露完整 Cookie，优先建议其退出登录或重新登录，让旧登录态失效
- 只有在用户明确需要完整原始结果时才使用 `--raw`
