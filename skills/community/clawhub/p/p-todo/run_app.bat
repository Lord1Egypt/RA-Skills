@echo off
cd /d "%~dp0"
java -jar target\P-Todo-1.0.0.jar > tmp_run.log 2>&1
echo EXIT_CODE=%ERRORLEVEL% >> tmp_run.log
