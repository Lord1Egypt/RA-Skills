---
name: block-disk-format
enabled: true
event: PreExec
matcher: "format |diskpart|chkdsk /f|chkdsk /r|diskpart clean"
action: block
priority: 100
---

禁止执行磁盘格式化或分区操作。

此规则保护磁盘数据安全，拦截所有磁盘级别操作命令。
不可豁免。

---
name: block-registry-edit
enabled: true
event: PreExec
matcher: "reg (delete|add)|regedit /s"
action: block
priority: 100
---

禁止修改 Windows 注册表。

注册表修改可能导致系统不稳定，所有注册表操作需人工审批。

---
name: block-account-management
enabled: true
event: PreExec
matcher: "net user|net localgroup|net accounts"
action: block
priority: 90
---

禁止账户管理操作。

包括创建/删除用户、修改组成员关系、更改账户策略。

---
name: block-service-management
enabled: true
event: PreExec
matcher: "sc (delete|config)|net (stop|start) "
action: block
priority: 90
---

禁止服务管理操作。

包括停止/启动/删除/修改 Windows 服务。

---
name: block-scheduled-tasks
enabled: true
event: PreExec
matcher: "schtasks /(delete|create)"
action: block
priority: 85
---

禁止创建或删除计划任务。

---
name: warn-external-download
enabled: true
event: PreExec
matcher: "curl |wget |Invoke-WebRequest|certutil -urlcache"
action: warn
priority: 70
---

外部下载操作需要确认目标地址在白名单内。

美信 API 和模型 API 域名可放行，其他域名需人工确认。

---
name: warn-batch-delete
enabled: true
event: PreExec
matcher: "(del|remove|rmdir) .*(\/s|\/q|\\*|\\-rf)"
action: block
priority: 95
---

禁止批量文件删除操作。

单次操作超过 50 个文件的删除必须人工审批。

---
name: warn-sudo-equivalent
enabled: true
event: PreExec
matcher: "runas|gsudo|elevate"
action: warn
priority: 60
---

提权操作警告。记录并提醒用户确认。
