# JEP-Guard Audit 2.0.1 上传说明

1. 解压 jep-guard-audit-2.0.1.zip。解压后的目录内可直接看到 SKILL.md、manifest.json 和 skill 文件夹。
2. 打开原 jep-guard-audit 的更新页，选择这个目录；保留原名称 jep-guard-audit，版本填 2.0.1。
3. 不要上传到 claw-hub-upload-folders 重复条目，也不要把本文件包当作浏览器插件。
4. 更新说明可填：Fix cross-tenant storage exhaustion with operator-controlled event/byte reservations, atomic quota checks, and restart-safe policy enforcement.
5. 发布后仍需等待 ClawHub 对 2.0.1 重新审查；本包尚未声称平台审查通过。

本次修复：租户事件条数和正文 UTF-8 字节数独立保留额度；各租户合计额度不可超出存储总上限；满额租户不占用其他租户预留空间；拒绝未配置租户、冲突工作进程配置和超额历史迁移；失败批次回滚，不删除历史或重放标识。
验证：20 项新增容量回归、7 项原有包内测试、19 项共享安全测试通过（共 46 项）。测试覆盖跨会话、独立数据库连接并发、重启、旧库迁移、字节限额和认证 API 的 429 响应。

若升级实际运行的服务：先停止所有 2.0.0 写入进程并备份数据库，按 SECURITY.md 为已有租户及可写租户配置 JEP_AUDIT_TENANT_QUOTAS。它默认只给 local 租户分配 10,000 条和 16 MiB，不会自动为其他租户分配容量。此限额不替代网关限流或操作系统磁盘管理。
