@echo off
rem lis-skill-bus 安装脚本（Windows，纯文本、可回滚、幂等）
rem 用法: install_skillbus.cmd [--dry-run|--apply|--uninstall]
rem 环境: USERPROFILE\.codex; SKIP_MCP_REG=1 只复制不注册 MCP
setlocal EnableExtensions
set MODE=%1
if "%MODE%"=="" set MODE=--help
if "%CODEX_HOME%"=="" set CODEX_HOME=%USERPROFILE%\.codex
set BUS_DIR=%CODEX_HOME%\mcp_servers\lis-skill-bus
set CONFIG=%CODEX_HOME%\config.toml
set SCRIPT_DIR=%~dp0
set SECTION_LINE=[mcp_servers.lis-skill-bus]

if /I "%MODE%"=="--help" goto :help
if /I "%MODE%"=="-h"     goto :help
if /I "%MODE%"=="--dry-run"   goto :dryrun
if /I "%MODE%"=="--apply"     goto :apply
if /I "%MODE%"=="--uninstall" goto :uninstall
echo [error] 未知模式: %MODE%
exit /b 64

:help
echo 用法: install_skillbus.cmd [--dry-run^|--apply^|--uninstall]
echo   --dry-run   只预览将写入的路径与 config 变更，不写盘
echo   --apply     复制 runtime 到 USERPROFILE\.codex\mcp_servers 并注册 MCP（先备份 config）
echo   --uninstall 移除 config 中的 MCP 注册（保留 mcp_servers 文件）
echo   环境: SKIP_MCP_REG=1 时只复制不注册
exit /b 0

:dryrun
echo 将安装到: %BUS_DIR%
echo 将复制: skillbus.py / skillbus_client.py / README / SKILL / BENEFITS / mcp-config / schemas / integration / example_pilot
echo 将注册: %SECTION_LINE% -^> %CONFIG%
echo （Windows CI 已覆盖 --dry-run 冒烟）
exit /b 0

:apply
if not exist "%CODEX_HOME%" (
  echo [error] 未找到 CODEX_HOME=%CODEX_HOME%
  exit /b 127
)
if not exist "%BUS_DIR%\schemas" mkdir "%BUS_DIR%\schemas"
if not exist "%BUS_DIR%\integration" mkdir "%BUS_DIR%\integration"
if not exist "%BUS_DIR%\example_pilot" mkdir "%BUS_DIR%\example_pilot"
copy /Y "%SCRIPT_DIR%skillbus.py" "%BUS_DIR%\skillbus.py" >nul
copy /Y "%SCRIPT_DIR%skillbus_client.py" "%BUS_DIR%\skillbus_client.py" >nul
copy /Y "%SCRIPT_DIR%skillbus_client.cmd" "%BUS_DIR%\skillbus_client.cmd" >nul
for %%F in (README.md SKILL.md BENEFITS.md mcp-config.example.json) do @copy /Y "%SCRIPT_DIR%%%F" "%BUS_DIR%\%%F" >nul 2>nul
copy /Y "%SCRIPT_DIR%schemas\*.json" "%BUS_DIR%\schemas" >nul 2>nul
copy /Y "%SCRIPT_DIR%integration\*.sh" "%BUS_DIR%\integration" >nul 2>nul
copy /Y "%SCRIPT_DIR%integration\*.cmd" "%BUS_DIR%\integration" >nul 2>nul
copy /Y "%SCRIPT_DIR%example_pilot\*" "%BUS_DIR%\example_pilot" >nul 2>nul
echo 已复制 runtime 到 %BUS_DIR%
if "%SKIP_MCP_REG%"=="1" (
  echo SKIP_MCP_REG=1，跳过 MCP 注册
  exit /b 0
)
set "CODEX_HOME=%CODEX_HOME%"
set "SECTION_LINE=%SECTION_LINE%"
set PY=python
where py >nul 2>nul
if not errorlevel 1 set PY=py
if not "%PYTHON%"=="" set PY=%PYTHON%
if not "%CODEX_PYTHON%"=="" set PY=%CODEX_PYTHON%
"%PY%" "%SCRIPT_DIR%install_py.py" --apply
exit /b %errorlevel%

:uninstall
set "CODEX_HOME=%CODEX_HOME%"
set "SECTION_LINE=%SECTION_LINE%"
set PY=python
where py >nul 2>nul
if not errorlevel 1 set PY=py
if not "%PYTHON%"=="" set PY=%PYTHON%
if not "%CODEX_PYTHON%"=="" set PY=%CODEX_PYTHON%
"%PY%" "%SCRIPT_DIR%install_py.py" --uninstall
exit /b %errorlevel%
