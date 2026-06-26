# hivulseAI

自动化技术文档生成工具，通过API接口将指定目录的文件上传并生成各种技术文档。

## 功能特性

- 🔍 自动扫描目录文件，过滤无关目录（node_modules、venv等）
- 📤 批量文件上传到API接口
- 📄 支持13种技术文档类型生成
- 🚀 完整的自动化流程
- 💻 支持命令行和交互式两种使用方式

## 支持的文档类型

| 编号 | 文档类型 |
|------|----------|
| 19 | 用户需求说明书 |
| 2 | 需求规格说明书 |
| 4 | 系统概要设计说明 |
| 5 | 系统详细设计说明 |
| 8 | 软件单元测试计划 |
| 9 | 软件单元测试用例 |
| 10 | 软件单元测试报告 |
| 1 | 系统测试计划 |
| 12 | 系统测试用例 |
| 15 | 系统测试报告 |
| 13 | 网络安全漏洞自评报告 |
| 20 | 软件用户测试用例 |
| 21 | 软件用户测试报告 |

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 交互式使用

```bash
python interactive.py
```

按照提示：
1. 输入项目目录路径
2. 选择文档类型编号
3. 确认开始处理

### 命令行使用

```bash
python hivulseAI.py <目录路径> <文档类型编号> [--task-name 任务名称] [--base-url API地址]
```

示例：
```bash
python hivulseAI.py /path/to/project 4 --task-name "我的项目系统设计"
```


## 过滤目录

系统会自动过滤以下目录：
- node_modules
- venv
- .git
- __pycache__
- .idea
- .vscode

## 文件结构

```
hivulseAI/
├── SKILL.md          # Skill说明文档
├── hivulseAI.py      # 主程序
├── interactive.py    # 交互式界面
├── requirements.txt  # 依赖包
└── README.md         # 使用说明
```

## 错误处理

- 目录不存在或无法访问时会提示错误
- 文件上传失败会中断流程
- API连接失败会有详细错误信息
- 支持键盘中断操作

## 开发说明

主要类：`HivulseAI`

核心方法：
- `get_directory_files()` - 获取目录文件
- `upload_file()` - 上传单个文件
- `upload_all_files()` - 批量上传
- `check_upload_status()` - 检查上传状态
- `generate_document()` - 生成文档
- `run()` - 完整流程执行

## 注意事项

1. 确保API服务正常运行
2. 目录需要有读取权限
3. 网络连接稳定
4. 文件大小不要超过API限制
