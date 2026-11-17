@echo off
rem 园林算量 接线薄壳：开工前从 bus 拉取合同（等价 scripts/yuanlin_statesync.cmd pull）
setlocal EnableExtensions
if "%SKILLS_DIR%"=="" set SKILLS_DIR=%USERPROFILE%\.codex\skills
set STATESYNC=%SKILLS_DIR%\yuanlin-suanliang\scripts\yuanlin_statesync.cmd
if not exist "%STATESYNC%" (
  echo [error] 缺少 %STATESYNC%^（请先安装 园林算量 skill^） 1>&2
  exit /b 127
)
call "%STATESYNC%" pull %*
exit /b %errorlevel%
