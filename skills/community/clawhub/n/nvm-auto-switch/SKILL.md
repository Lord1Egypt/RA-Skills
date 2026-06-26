---
name: nvm-auto-switch
description: 根据 package.json 中的 engines 字段自动检测 Node.js 版本要求，如未安装 nvm 则自动安装，并切换到正确的 Node 版本。支持 Windows、macOS 和 Linux。在开发 Node.js 项目、切换 Node 版本或设置开发环境时使用。
---

# NVM 自动切换

根据 package.json 的 engines 字段自动切换到正确的 Node.js 版本。

## 使用场景

- 进入 Node.js 项目目录
- 设置新的开发环境
- Node 版本不匹配错误
- CI/CD 流水线设置

## 快速开始

### Windows
```powershell
# 自动获取当前目录
.\scripts\nvm-auto-switch.ps1

# 或指定项目路径
.\scripts\nvm-auto-switch.ps1 [项目路径]
```

### macOS / Linux
```bash
# 自动获取当前目录
./scripts/nvm-auto-switch.sh

# 或指定项目路径
./scripts/nvm-auto-switch.sh [项目路径]
```

## 工作原理

1. **检测操作系统** - 识别 Windows、macOS 或 Linux
2. **自动获取项目路径** - 如未提供路径，自动使用当前工作目录
3. **检查当前 Node 版本** - 获取当前激活的 Node.js 版本
4. **检查/安装 NVM** - 如未安装则自动安装
5. **读取 package.json** - 解析 engines.node 字段
6. **对比版本** - 如果当前版本已满足要求，跳过切换
7. **查找/安装 Node** - 使用现有版本或下载匹配版本
8. **切换版本** - 激活正确的 Node 版本

## 工作流程

```
获取项目路径（参数或当前目录）
↓
检查当前 Node 版本
↓
读取 package.json engines.node
解析版本要求 (例如 >=14.0.0)
↓
当前版本已满足要求？
├── 是 → 跳过切换，提示当前版本兼容
│
└── 否 → 继续
    ↓
    检查 NVM 是否已安装？
    ├── 否 → 自动安装 NVM
    │   ├── Windows: 下载 nvm-setup.exe
    │   └── macOS/Linux: 运行安装脚本
    │
    └── 是 → 继续
        ↓
        查找匹配的已安装版本？
        ├── 是 → nvm use <版本号>
        │
        └── 否 → nvm install <最新匹配版本>
            nvm use <版本号>
```

## 脚本

`scripts/` 目录下的工具脚本：

| 脚本 | 平台 | 用途 |
|------|------|------|
| `nvm-auto-switch.ps1` | Windows | PowerShell 实现 |
| `nvm-auto-switch.sh` | macOS/Linux | Bash 实现 |

## 示例

**当前目录（自动获取）：**
```bash
./scripts/nvm-auto-switch.sh
```

```powershell
.\scripts\nvm-auto-switch.ps1
```

**指定项目：**
```bash
./scripts/nvm-auto-switch.sh /path/to/project
```

```powershell
.\scripts\nvm-auto-switch.ps1 "C:\projects\my-app"
```

## 注意事项

- Windows 需要管理员权限来安装 nvm
- macOS/Linux 需要 curl 来安装 nvm
- 支持版本前缀：`^`, `~`, `>=`, `<=` 等
- 安装 nvm 后可能需要重启终端
- 不提供路径参数时，自动使用当前工作目录
