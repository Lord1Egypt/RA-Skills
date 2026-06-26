# pixcake-skills

本地 PixCake skill 包，供 OpenClaw / 龙虾直接读取。

当前只暴露一个公开 skill：`pixcake`，覆盖三条工作流：

- 项目管理
- 预设修图
- 导出任务

## 环境要求

| 项目 | 要求 |
|------|------|
| 支持平台 | macOS、Windows |
| PixCake 客户端 | `9.0.0` 及以上 |
| 运行时 | `mcporter`（脚本自动安装） |
| 配置文件 | `~/.openclaw/workspace/config/mcporter.json`（脚本自动写入） |

## 快速开始

1. 放到本地 skills 目录：

```
~/.openclaw/skills/pixcake-skills
```

2. 确认 PixCake 客户端已安装并启动（启动客户端会自动带起 `pixcake-mcp`）

3. Windows 如果目录里当前是 `scripts/setup.ps1.txt`，必须先重命名为 `setup.ps1`，否则后续命令无法执行：

```powershell
Rename-Item .\scripts\setup.ps1.txt setup.ps1
```

4. 运行环境检查：

```bash
# macOS
./scripts/setup.sh --check-only

# Windows PowerShell
.\scripts\setup.ps1 -CheckOnly
```

5. 如果检查显示配置缺失，运行自动设置：

```bash
# macOS
./scripts/setup.sh

# Windows PowerShell
.\scripts\setup.ps1
```

如果自动定位失败，可显式传路径（macOS 示例）：

```bash
./scripts/setup.sh --pixcake-app "/Applications/pixcake.app/Contents/MacOS/pixcake" --pixcake-mcp "/Applications/pixcake.app/Contents/MacOS/pixcake-mcp"
```

6. 验证连接：

```bash
mcporter --config ~/.openclaw/workspace/config/mcporter.json list pixcake --json
```

## 工具面

| 领域 | 工具 | 说明 |
|------|------|------|
| 项目 | `get_project_list`、`create_projects`、`import_images_to_projects`、`get_project_images` | 创建 / 查找项目、导入 / 读取图片 |
| 修图 | `get_preset_suit_list`、`apply_preset_suit` | 预设修图 |
| 导出 | `get_project_images`、`batch_export_images`、`get_task_status` | 提交批量导出任务，并查询任务状态与进度 |

## 调用示例

macOS：

```bash
# 标量参数用 key=value
mcporter --config ~/.openclaw/workspace/config/mcporter.json call pixcake.get_project_list sort_by=created limit=20 --output json

# 对象 / 数组参数用 function-call
mcporter --config ~/.openclaw/workspace/config/mcporter.json call "pixcake.create_projects(projects: [{ project_name: '春日外景', image_paths: ['/Users/xxx/Photos/spring/001.jpg'] }])" --output json
```

Windows：

```powershell
# 标量参数用 key=value
mcporter --config C:\Users\<用户名>\.openclaw\workspace\config\mcporter.json call pixcake.get_project_list sort_by=created limit=20 --output json

# 对象 / 数组参数用 function-call
mcporter --config C:\Users\<用户名>\.openclaw\workspace\config\mcporter.json call "pixcake.create_projects(projects: [{ project_name: '春日外景', image_paths: ['D:\\Photos\\spring\\001.jpg'] }])" --output json
```

> Windows 下不要用 `--args '{...}'` 传复杂 JSON，容易被 PowerShell 引号转义破坏。

## 不支持

- 联机拍摄、AI 挑图、AI 修图、AI 追色
- 滤镜 / 换背景 / 去路人、智能裁剪

## 兼容性策略

以下情况按客户端版本不匹配处理：

- `list pixcake` 无法拿到可用 server
- `list pixcake` 缺少必需工具
- `call pixcake.<tool>` 返回 `tool not found` 或 `method not found`

处理顺序：提示升级到 `9.0.0`+ → 用户要求时重试一次 → 仍失败则引导联系工作人员。

## 目录结构

```
pixcake-skills/
├── SKILL.md
├── README.md
├── manifest.json
├── references/
│   ├── capabilities.md
│   ├── compatibility.md
│   ├── export.md
│   ├── mcp-setup.md
│   ├── projects.md
│   ├── response-policy.md
│   └── retouch.md
└── scripts/
    ├── setup.sh
    └── setup.ps1.txt
```
