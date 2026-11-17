@echo off
rem Windows launcher: start llama-server in the skill root using a relative model path.
setlocal
cd /d "%~dp0"
if "%MODEL%"=="" set "MODEL=models\Hy-MT2-7B-Q4_K_M.gguf"
if "%PORT%"=="" set "PORT=8001"
if "%API_KEY%"=="" set "API_KEY=llama2025"
llama-server.exe -m "%MODEL%" -ngl -1 --host 127.0.0.1 --port %PORT% --api-key %API_KEY% -c 32768