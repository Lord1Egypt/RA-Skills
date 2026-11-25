# 认证
<!-- reference-type: business -->

> **范围**：验证、保存或清除本机 API Key；不创建、撤销平台 Key，不管理多账号档案。
<!-- slot: 范围 -->

## 命令一览

| 命令 | 作用 |
|---|---|
| `nextrap-cli auth set` | 验证输入的 Key 后保存本机配置 |
| `nextrap-cli auth clear` | 仅清除本机已保存的 Key |
<!-- slot: 命令清单 -->

### nextrap-cli auth set

```bash
nextrap-cli auth set --api-key -
```
<!-- slot: 示例 -->

| 输入或行为 | 约束 |
|---|---|
| 标准输入 | 在交互终端由用户粘贴 Key、回车后按 Ctrl+D；代理自动执行时通过工具的 stdin 传入，不拼入 argv 或 shell 历史。不支持 stdin 的工具由用户在本机完成认证。 |
| Key 来源 | 在 Nextrap 平台个人中心创建；本命令不创建 Key。不要让用户把 Key 粘进聊天。 |
| 验证与写入 | 必须有非空 Key，最多读取 65536 字节；验证成功后才保存相同服务地址，验证失败不覆盖旧文件。 |
| 本机配置 | `~/.nextrap-cli/config.yml`；保留其他配置，不自动迁移其他目录的凭证。 |
| 优先级 | Key：`NEXTRAP_API_KEY` 高于文件；业务地址：`--endpoint` 高于 `NEXTRAP_ENDPOINT`、文件、默认服务地址。保存 Key 时验证的是本次 stdin 输入，而不是环境中的旧 Key。 |
<!-- slot: 参数 -->

### nextrap-cli auth clear

```bash
nextrap-cli auth clear -o json
```
<!-- slot: 示例 -->

| 行为 | 约束 |
|---|---|
| 清除范围 | 删除本机配置中的 Key，保留地址及其他设置；不撤销平台 Key，不修改父进程环境变量。 |
| 环境变量 | `NEXTRAP_API_KEY` 若仍存在，清除文件后它继续生效；需要用户在原终端自行取消，不读取其值。 |
<!-- slot: 参数 -->

## 注意事项

- [ ] 已确认服务地址，且任务包含本机认证修改；不为通过验证自动更换服务。
- [ ] Key 没有进入命令参数、日志、截图、报告或仓库；配置内容不复制给用户或其他服务。
<!-- slot: 注意事项 -->
