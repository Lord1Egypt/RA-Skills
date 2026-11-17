@echo off
rem cad-file-reader 接线：发布 cad-contract/v1 到 lis-skill-bus。
setlocal EnableExtensions
call "%~dp0..\skillbus_client.cmd" push %*
exit /b %errorlevel%
