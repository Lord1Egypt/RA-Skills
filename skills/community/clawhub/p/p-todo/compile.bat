@echo off
cd /d "%~dp0"
mvn compile -q
echo EXIT_CODE=%ERRORLEVEL%
