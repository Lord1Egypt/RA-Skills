# Halo CLI 运维操作 — 主题、插件、附件、备份、瞬间

## 主题（Theme）

```bash
halo theme list
halo theme list --uninstalled          # 包含已卸载主题
halo theme current
halo theme get <name>
halo theme activate <name>
halo theme reload <name>
halo theme delete <name> --force
```

### 安装主题

```bash
halo theme install --file ./theme.zip
halo theme install --url https://example.com/theme.zip
```

第三方 URL 会提示确认，非交互模式下用 `--yes` 跳过。

### 升级主题

```bash
halo theme upgrade <name> --online     # 从 Halo 应用商店升级
halo theme upgrade <name> --url https://example.com/theme.zip
halo theme upgrade <name> --file ./theme.zip
halo theme upgrade --all               # 批量升级所有应用商店主题
```

## 插件（Plugin）

```bash
halo plugin list
halo plugin list --enabled true
halo plugin get <name>
halo plugin enable <name>
halo plugin disable <name> --force
halo plugin uninstall <name> --force
```

### 安装插件

```bash
halo plugin install --file ./plugin.jar
halo plugin install --url https://example.com/plugin.jar
halo plugin install --app-id app-SnwWD
```

### 升级插件

```bash
halo plugin upgrade <name> --online
halo plugin upgrade <name> --url https://example.com/plugin.jar
halo plugin upgrade <name> --file ./plugin.jar
halo plugin upgrade --all --yes        # 批量升级并跳过确认
```

## 附件（Attachment）

```bash
halo attachment list
halo attachment get <name>
halo attachment upload --file ./image.png
halo attachment upload --url https://example.com/image.png
halo attachment download <name> --output ./downloads/image.png
halo attachment delete <name> --force
```

## 备份（Backup）

```bash
halo backup list
halo backup get <name>
halo backup create
halo backup create --wait              # 等待完成
halo backup create --wait --wait-timeout 300
halo backup download <name> --output ./backup.zip
halo backup delete <name> --force
```

## 瞬间（Moment）

```bash
halo moment list
halo moment get <name>
halo moment create --content "Hello from Halo CLI"
halo moment update <name> --content "Updated content"
halo moment delete <name> --force
```

可用选项包括 `--visible`、`--tags` 和发布时间相关参数。
