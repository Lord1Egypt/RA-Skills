@echo off
setlocal
set "PAN_SCRIPT=%~dp0pan.py"
if not exist "%PAN_SCRIPT%" (
  echo [pan] 找不到 %PAN_SCRIPT% 1>&2
  exit /b 2
)
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 "%PAN_SCRIPT%" %*
  exit /b %errorlevel%
)
where python >nul 2>nul
if %errorlevel%==0 (
  python "%PAN_SCRIPT%" %*
  exit /b %errorlevel%
)
echo [pan] 未找到 Python 3；请安装 Python 并勾选 Add python.exe to PATH 1>&2
exit /b 127
