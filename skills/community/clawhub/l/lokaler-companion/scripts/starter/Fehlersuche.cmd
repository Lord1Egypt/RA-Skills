@echo off
rem  Wie der normale Start, aber das Serverfenster bleibt offen und sichtbar.
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0start.ps1" -Console
pause
