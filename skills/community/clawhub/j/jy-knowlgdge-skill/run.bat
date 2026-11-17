@echo off
chcp 65001 >nul
set PYTHON=C:\Users\admin\.workbuddy\binaries\python\envs\default\Scripts\python.exe
cd /d D:\knowledge_skill\JY_Knowlgdge_Skill

if "%1"=="-t" goto test
if "%1"=="-c" goto categories
if "%1"=="-f" goto file
if "%1"=="-d" goto dir
goto help

:file
%PYTHON% main.py -f %2 -y
goto end

:dir
%PYTHON% main.py -d %2 -y
goto end

:test
%PYTHON% main.py -t
goto end

:categories
%PYTHON% main.py -c
goto end

:help
echo Usage:
echo   run.bat -f "D:/path/to/file.docx"  ^- Process single file
echo   run.bat -d "D:/path/to/dir/"       ^- Process directory
echo   run.bat -t                          ^- Test connections
echo   run.bat -c                          ^- View categories
goto end

:end
pause
