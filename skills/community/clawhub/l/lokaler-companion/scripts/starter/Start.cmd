@echo off
rem  Doppelklick-Einstieg. -ExecutionPolicy Bypass gilt nur fuer diesen einen
rem  Aufruf und aendert nichts an den Einstellungen des Rechners.
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0start.ps1" %*
if errorlevel 1 pause
