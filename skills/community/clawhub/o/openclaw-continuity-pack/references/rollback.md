# 回滚说明

如果部署后出现任一关键问题，不要在线混修，先最小回滚。

## 建议优先回滚的内容

1. `<OPENCLAW_INSTALL_ROOT>/dist/`
2. `<OPENCLAW_INSTALL_ROOT>/dist/control-ui/`

如果你是源码型部署，再额外回滚本次替换过的正式运行时代码文件。

## 最小回滚流程

```bash
systemctl stop <SERVICE_NAME>
rsync -aiv --delete <BACKUP_DIST_DIR>/ <OPENCLAW_INSTALL_ROOT>/dist/
systemctl start <SERVICE_NAME>
```

如果 `control-ui` 是单独备份的，也恢复：

```bash
rsync -aiv --delete <BACKUP_CONTROL_UI_DIR>/ <OPENCLAW_INSTALL_ROOT>/dist/control-ui/
```

## 回滚后立刻确认

1. `openclaw config validate --json`
2. `systemctl is-active <SERVICE_NAME>`
3. 打开 `<LIVE_GATEWAY_URL>`，确认根页面返回 `200`

## 何时必须回滚

出现下面任一项就建议立即回滚：
- 根页面打不开
- `Control UI assets not found`
- service 起不来
- disposable thread 最小验收失败，且你不能在几分钟内明确定位为“仅脚本假阴性”

## 不建议的做法

- 在 live 上边部署边改源码
- 一边在线 patch 一边继续跑真实用户流量
- 跳过备份直接替换
