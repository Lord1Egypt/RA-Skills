# internal-admin-playwright

内部后台自动化 Skill（Python + Playwright），支持：

- VPN（L2TP/IPsec）可配置化
- 访问权限白名单可配置化
- 中文命令路由（菜单跳转）
- 可复用给团队

## 1. 目录说明

- `references/vpn_config.yaml`：VPN 参数
- `references/whitelist.yaml`：允许访问域名 + 可选域名解析覆盖
- `references/menu_map.yaml`：中文命令映射
- `scripts/vpn_l2tp.py`：VPN up/down/status
- `scripts/run.py`：主自动化入口

## 2. 安装依赖

```bash
cd internal-admin-playwright
python3 -m venv .venv
.venv/bin/pip install -r scripts/requirements.txt
.venv/bin/python -m playwright install chromium
```

## 3. 配置 VPN

编辑 `references/vpn_config.yaml`：

- `server`
- `username`
- `password`
- `psk`
- `route_all_traffic`
- `xl2tpd_local_port`（建议 0）

手动测试：

```bash
.venv/bin/python scripts/vpn_l2tp.py up
.venv/bin/python scripts/vpn_l2tp.py status
```

## 4. 配置白名单边界

编辑 `references/whitelist.yaml`：

- `allowed_hosts`
- `allowed_host_suffixes`
- `host_overrides`（可选）

## 5. 配置命令

编辑 `references/menu_map.yaml`，示例：

```yaml
commands:
  "进入文章管理->文章列表":
    clicks:
      - "文章管理"
      - "文章列表"
    assert_text: "文章列表"
```

## 6. 运行

```bash
STAFF_USERNAME='xxx' \
STAFF_PASSWORD='xxx' \
GOOGLE_OTP='123456' \
AUTO_VPN=1 \
FORCE_IPV4=1 \
LOGIN_URL='https://staff-mogusp.peach-av.com/admin/login/index' \
.venv/bin/python scripts/run.py --command "进入文章管理->文章列表"
```

## 7. 打包分发

```bash
python3 /usr/lib/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py /root/.openclaw/workspace/skills/internal-admin-playwright /root/.openclaw/workspace/dist
```

产物：`/root/.openclaw/workspace/dist/internal-admin-playwright.skill`

## 8. 团队共享建议

- 不要提交真实账号密码/PSK
- `vpn_config.yaml` 用模板，生产值走环境注入或密钥管理
- 命令映射与白名单走代码评审
