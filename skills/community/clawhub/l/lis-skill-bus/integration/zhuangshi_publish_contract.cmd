@echo off
rem 装饰算量 接线薄壳：发布合同到 bus（等价 scripts/zhuangshi_statesync.cmd push）
setlocal EnableExtensions
if "%SKILLS_DIR%"=="" set SKILLS_DIR=%USERPROFILE%\.codex\skills
set STATESYNC=%SKILLS_DIR%\zhuangshi-suanliang\scripts\zhuangshi_statesync.cmd
if not exist "%STATESYNC%" (
  echo [error] 缺少 %STATESYNC%^（请先安装 装饰算量 skill^） 1>&2
  exit /b 127
)
call "%STATESYNC%" push %*
exit /b %errorlevel%
