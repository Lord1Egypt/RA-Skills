# 团队配置模板（复制后填写）

## 1) VPN 配置
复制 `vpn_config.yaml`，填写：
- `server`
- `username`
- `password`
- `psk`

## 2) 白名单
复制 `whitelist.yaml`，填写：
- `allowed_hosts`：仅允许后台域名
- `allowed_host_suffixes`：一般留空
- `host_overrides`：仅在网络线路异常时使用

## 3) 命令路由
复制 `menu_map.yaml`，按你们后台菜单文字维护：
- 中文命令 -> clicks 序列
- assert_text 页面校验文字

## 4) 运行示例
```bash
STAFF_USERNAME='后台账号' \
STAFF_PASSWORD='后台密码' \
GOOGLE_OTP='动态码' \
AUTO_VPN=1 FORCE_IPV4=1 \
LOGIN_URL='https://your-admin.example.com/admin/login/index' \
.venv/bin/python scripts/run.py --command "进入文章管理->文章列表"
```
