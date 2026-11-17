@echo off
rem lis-skill-bus 客户端 Windows 薄壳（逻辑在 skillbus_client.py）。
setlocal EnableExtensions
set PY=python
where py >nul 2>nul
if not errorlevel 1 set PY=py
if not "%PYTHON%"=="" set PY=%PYTHON%
if not "%CODEX_PYTHON%"=="" set PY=%CODEX_PYTHON%
"%PY%" "%~dp0skillbus_client.py" %*
exit /b %errorlevel%
