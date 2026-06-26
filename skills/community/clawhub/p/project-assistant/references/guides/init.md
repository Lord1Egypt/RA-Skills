# 项目初始化详细指南

## 命令

```
/init [目录] [选项]
```

## 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `目录` | 项目目录 | 当前目录 |
| `--force` | 强制重新扫描 | false |
| `--depth=N` | 扫描深度 | 3 |
| `--quick` | 快速模式 | false |

## 执行流程

```bash
# 1. 探测项目类型
python3 {baseDir}/scripts/detector.py "$PROJECT_DIR"

# 2. 加载子模块
# 根据 project_type 加载 references/templates/ 下对应模板

# 3. 生成文档
# 输出到 .claude/project.md
```

## 项目类型映射

| project_type | 模板 |
|-------------|------|
| `android-app` | `templates/mobile/android.md` |
| `ios` | `templates/mobile/ios.md` |
| `stm32/esp32/pico` | `templates/embedded/mcu.md` |
| `freertos/zephyr` | `templates/embedded/rtos.md` |
| `embedded-linux` | `templates/embedded/linux.md` |
| `qnx` | `templates/embedded/qnx.md` |
| `react/vue/angular` | `templates/web/frontend.md` |
| `django/fastapi` | `templates/web/backend.md` |
| `electron/qt` | `templates/desktop/desktop.md` |
| `cmake/makefile` | `templates/system/native.md` |

## 输出结构

```
.claude/
├── project.md           # L0 项目概览
├── index/               # 数据索引
│   ├── processes.json
│   ├── ipc.json
│   └── structure.json
├── docs/                # 详细文档（按需生成）
└── cache.json           # 缓存
```

## 大型项目处理

文件数 > 10000 时：
- 自动限制扫描深度到 2
- 跳过 `node_modules`, `build` 等
- 只解析顶层配置