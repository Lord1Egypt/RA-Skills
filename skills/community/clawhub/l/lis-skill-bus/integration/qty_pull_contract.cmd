@echo off
rem 土建算量接线：从 lis-skill-bus 拉取 cad-contract/v1。
setlocal EnableExtensions
call "%~dp0..\skillbus_client.cmd" pull %*
exit /b %errorlevel%
