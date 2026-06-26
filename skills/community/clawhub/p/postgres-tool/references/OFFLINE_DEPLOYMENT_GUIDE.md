# PostgreSQL Tool 内网部署指南

## 内网环境特点

1. **无法访问互联网** - 不能使用 pip 在线安装包
2. **PATH 可能不完整** - pip 等工具可能不在系统 PATH 中
3. **Python 版本固定** - 通常使用固定的 Python 版本（如 3.12）
4. **安全限制严格** - 可能需要管理员权限才能安装包

## 完整部署流程

### 步骤 1：在外网机器准备依赖包

在有网络的机器上执行：

```bash
# 1. 创建临时目录
mkdir temp-deps
cd temp-deps

# 2. 下载所有必需的 wheel 文件
# 注意：需要指定与目标机器相同的 Python 版本
pip download psycopg2-binary pandas openpyxl numpy python-dateutil tzdata et-xmlfile -d .

# 3. 验证下载的文件
dir *.whl

# 4. 将整个 postgres-tool 目录复制到 U 盘或网络共享
# 将 temp-deps 中的内容复制到 postgres-tool/scripts/dependencies/
copy *.whl X:\path\to\postgres-tool\scripts\dependencies\
```

### 步骤 2：在内网机器安装

#### 方法 A：使用批处理脚本（推荐 - Windows）

``batch
@echo off
REM 内网一键安装脚本

set SCRIPT_DIR=%~dp0
set PYTHON_CMD=python

echo ========================================
echo PostgreSQL Tool - 内网依赖安装
echo ========================================
echo.

REM 检查 Python 是否可用
%PYTHON_CMD% --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请确认已安装 Python 3.12+
    pause
    exit /b 1
)

echo Python 版本：
%PYTHON_CMD% --version
echo.

REM 使用 python -m pip 确保即使 pip 不在 PATH 中也能工作
echo 正在安装依赖...
%PYTHON_CMD% -m pip install --no-index --find-links="%SCRIPT_DIR%scripts\dependencies" -r "%SCRIPT_DIR%scripts\requirements.txt"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo 安装成功！
    echo ========================================
    echo.
    echo 测试运行：
    echo   cd "%SCRIPT_DIR%"
    echo   python scripts\postgres_tool.py --list-tables
    echo.
) else (
    echo.
    echo ========================================
    echo 安装失败！
    echo ========================================
    echo.
    echo 可能的原因：
    echo 1. dependencies 目录中的 wheel 文件与 Python 版本不匹配
    echo 2. wheel 文件不完整或损坏
    echo 3. 权限问题（尝试以管理员身份运行）
    echo.
    echo 解决方案：
    echo 1. 重新下载与当前 Python 版本匹配的 wheel 文件
    echo 2. 确保所有 wheel 文件都已复制到 dependencies 目录
    echo 3. 右键点击此脚本，选择"以管理员身份运行"
)

pause
```

保存为 `scripts/install-offline.bat`，放在 postgres-tool 目录。

#### 方法 B：使用 PowerShell 脚本

``powershell
# 内网一键安装脚本 (PowerShell)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonCmd = "python"

Write-Host "========================================"
Write-Host "PostgreSQL Tool - 内网依赖安装"
Write-Host "========================================"
Write-Host ""

# 检查 Python
try {
    $pythonVersion = & $PythonCmd --version
    Write-Host "Python 版本：$pythonVersion"
} catch {
    Write-Host "[错误] 未找到 Python，请确认已安装 Python 3.12+"
    pause
    exit 1
}

Write-Host ""
Write-Host "正在安装依赖..."

# 使用 python -m pip
try {
    & $PythonCmd -m pip install --no-index --find-links="$ScriptDir\scripts\dependencies" -r "$ScriptDir\scripts\requirements.txt"
    
    Write-Host ""
    Write-Host "========================================"
    Write-Host "安装成功！"
    Write-Host "========================================"
    Write-Host ""
    Write-Host "测试运行："
    Write-Host "  cd `"$ScriptDir`""
    Write-Host "  python scripts\postgres_tool.py --list-tables"
    Write-Host ""
} catch {
    Write-Host ""
    Write-Host "========================================"
    Write-Host "安装失败！"
    Write-Host "========================================"
    Write-Host ""
    Write-Host "错误信息：$_"
    Write-Host ""
    Write-Host "解决方案："
    Write-Host "1. 检查 wheel 文件版本是否匹配"
    Write-Host "2. 确保所有依赖文件都已复制"
    Write-Host "3. 以管理员身份运行 PowerShell"
}

pause
```

保存为 `scripts/install-offline.ps1`。

#### 方法 C：手动命令行安装

如果自动脚本失败，可以手动执行：

```
# 1. 打开命令提示符（CMD）或 PowerShell
# 2. 进入技能目录
cd d:\biz-evn-dev\workspace\node-debug-mservice\.qoder\skills\postgres-tool

# 3. 使用 python -m pip 安装（即使 pip 不在 PATH 中）
python -m pip install --no-index --find-links=./scripts/dependencies -r scripts/requirements.txt

# 4. 验证安装
python scripts/postgres_tool.py --list-tables
```

### 步骤 3：配置数据库连接

编辑 `db_config.json`（用户自行创建）：

```

```


```

### 步骤 4：测试运行

```
# 列出所有表
python scripts/postgres_tool.py --list-tables

# 查询数据
python scripts/postgres_tool.py "SELECT COUNT(*) FROM your_table;"
```

## 常见问题与解决方案

### 问题 1：pip 命令找不到

**错误：**
```
pip : 无法将"pip"项识别为 cmdlet、函数、脚本文件或可运行程序的名称
```

**解决方案：**

使用 `python -m pip` 替代 `pip`：

```bash
# 错误方式
pip install ...

# 正确方式
python -m pip install ...
```

### 问题 2：psycopg2 模块找不到

**错误：**
```
ModuleNotFoundError: No module named 'psycopg2'
```

**原因：**
- 依赖未安装
- 或者安装到了错误的 Python 环境

**解决方案：**

1. 确认 Python 版本：
```bash
python --version
```

2. 检查 wheel 文件是否匹配：
```bash
# 查看 dependencies 目录中的文件名
dir scripts\dependencies\*.whl

# cp312 表示 Python 3.12
# cp313 表示 Python 3.13
```

3. 重新安装：
```bash
python -m pip install --no-index --find-links=./scripts/dependencies -r scripts/requirements.txt
```

### 问题 3：wheel 文件版本不匹配

**症状：**
```
ERROR: psycopg2_binary-2.9.11-cp313-cp313-win_amd64.whl is not a supported wheel on this platform.
```

**解决方案：**

重新下载与当前 Python 版本匹配的 wheel 文件：

```bash
# 在外网机器执行（确保 Python 版本与内网相同）
pip download psycopg2-binary pandas openpyxl numpy python-dateutil tzdata et-xmlfile -d dependencies
```

### 问题 4：权限问题

**症状：**
```
PermissionError: [Errno 13] Permission denied
```

**解决方案：**

**Windows：**
- 右键点击安装脚本，选择"以管理员身份运行"
- 或者安装到用户目录：
```bash
python -m pip install --user --no-index --find-links=./scripts/dependencies -r scripts/requirements.txt
```

**Linux/Mac：**
```bash
sudo ./scripts/install-dependencies.sh
```

### 问题 5：依赖文件不完整

**症状：**
```
ERROR: Could not find a version that satisfies the requirement numpy
```

**解决方案：**

检查 `scripts/dependencies` 目录中是否有所有必需的文件：

必需文件列表：
- ✅ psycopg2_binary-*.whl
- ✅ pandas-*.whl
- ✅ numpy-*.whl
- ✅ openpyxl-*.whl
- ✅ python_dateutil-*.whl
- ✅ tzdata-*.whl
- ✅ et_xmlfile-*.whl

如果有缺失，在外网机器重新下载：
```bash
pip download psycopg2-binary pandas openpyxl numpy python-dateutil tzdata et-xmlfile -d scripts/dependencies
```

## 快速参考卡片

打印此部分供快速参考：

```
========================================
PostgreSQL Tool 内网安装 - 快速参考
========================================

1. 检查 Python 版本
   python --version

2. 安装依赖（三种方式任选其一）
   
   方式 A：使用批处理脚本
   .\scripts\install-offline.bat
   
   方式 B：使用 PowerShell
   .\scripts\install-offline.ps1
   
   方式 C：手动命令行
   python -m pip install --no-index --find-links=./scripts/dependencies -r scripts/requirements.txt

3. 配置数据库
   编辑 db_config.json

4. 测试运行
   python scripts/postgres_tool.py --list-tables
   python scripts/postgres_tool.py "SELECT * FROM your_table LIMIT 10;"

5. 诊断问题
   python scripts/diagnose_deps.py

========================================
```

## 联系支持

如果以上方法都无法解决问题：

1. 运行诊断工具：
```bash
python scripts/diagnose_deps.py
```

2. 记录错误信息

3. 联系技术支持，提供以下信息：
   - Python 版本
   - 操作系统版本
   - 完整的错误日志
   - diagnose_deps.py 的输出结果
