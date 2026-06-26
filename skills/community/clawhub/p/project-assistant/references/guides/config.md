# 配置管理详细指南

## 配置命令

| 命令 | 说明 |
|------|------|
| `/set-config <key> <value>` | 设置配置项 |
| `/get-config <key>` | 获取配置项 |
| `/show-config` | 显示所有配置 |
| `/delete-config <key>` | 删除配置项 |

## 预定义配置项

| 配置项 | 说明 | 示例 |
|--------|------|------|
| `workdir` | 工作目录 | `/home/user/project` |
| `build_command` | 构建命令 | `npm run build` |
| `run_command` | 运行命令 | `npm run dev` |
| `test_command` | 测试命令 | `npm test` |
| `preferences.language` | 语言偏好 | `zh` / `en` |
| `preferences.detail_level` | 详细程度 | `brief` / `normal` / `detailed` |
| `feishu.doc_token` | 飞书文档 token | `doccnxxx` |
| `feishu.folder_token` | 飞书文件夹 token | `fldcnxxx` |
| `custom.*` | 自定义配置 | `custom.board_type` |

## 执行命令

```bash
python3 {baseDir}/scripts/config_manager.py {baseDir} <command> [args]
```

## 示例

```bash
# 设置工作目录（替代 /set-workdir）
/set-config workdir /home/user/project

# 设置构建命令
/set-config build_command "make all"

# 设置飞书文档
/set-config feishu.doc_token "doccnxxxxxx"

# 显示所有配置
/show-config
```