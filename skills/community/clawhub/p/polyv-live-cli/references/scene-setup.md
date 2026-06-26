# 场景初始化

`setup` 用于按预定义场景创建资源。npm 版当前内置场景为 `e-commerce`。

## 查看可用场景

```bash
<CLI> setup --list
<CLI> setup --list --detailed
<CLI> setup --list -o json
```

## 预览初始化内容

```bash
<CLI> setup e-commerce --dry-run
<CLI> setup e-commerce --dry-run -o json
```

`--dry-run` 只预览将创建的资源，不实际变更账号或频道资源。

## 初始化电商场景

```bash
<CLI> setup e-commerce
<CLI> setup e-commerce -o json
```

## 命令选项

| 选项 | 说明 |
| --- | --- |
| `-l, --list` | 列出可用场景 |
| `--detailed` | 配合 `--list` 显示详细场景信息 |
| `--dry-run` | 预览资源创建计划 |
| `-o, --output` | `table` 或 `json` |

## 自定义场景

CLI 帮助提示支持在 `~/.polyv/scenes/` 目录放置自定义场景配置。使用自定义场景前，先运行：

```bash
<CLI> setup --list --detailed
```

确认 CLI 是否已经识别到目标场景，再执行初始化。

## 初始化后常见检查

```bash
<CLI> channel list -o json
<CLI> product list -c <频道ID> -o json
<CLI> coupon list -o json
<CLI> stream get-key -c <频道ID>
```

## 使用注意

- `setup e-commerce` 会创建或配置实际资源，执行前确认当前账号和默认账号。
- 生产账号上建议先运行 `--dry-run`。
- 目前不要把 `education`、`event`、`webinar` 写成内置场景，除非新的 npm 帮助输出已经列出这些场景。
