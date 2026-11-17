@echo off
rem 安装算量 接线薄壳：发布合同到 bus（等价 scripts/anzhuang_statesync.cmd push）
setlocal EnableExtensions
if "%SKILLS_DIR%"=="" set SKILLS_DIR=%USERPROFILE%\.codex\skills
set STATESYNC=%SKILLS_DIR%\anzhuang-suanliang\scripts\anzhuang_statesync.cmd
if not exist "%STATESYNC%" (
  echo [error] 缺少 %STATESYNC%^（请先安装 安装算量 skill^） 1>&2
  exit /b 127
)
call "%STATESYNC%" push %*
exit /b %errorlevel%
