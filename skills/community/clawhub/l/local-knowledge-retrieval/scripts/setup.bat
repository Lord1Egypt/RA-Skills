@echo off
chcp 65001 >nul
title Knowledge Retrieval Skill Setup
echo ========================================
echo   Knowledge Retrieval Skill - Setup
echo ========================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

python -c "import sys; exit(0 if sys.version_info >= (3,8) else 1)"
if errorlevel 1 (
    echo [ERROR] Python 3.8+ is required. Current version:
    python --version
    pause
    exit /b 1
)

echo [OK] Python detected
python --version
echo.

:: Install dependencies
echo Installing dependencies - this may take a minute...
echo.

pip install bm25s==0.3.8 pdfminer.six==20260107 python-pptx==1.0.2
if errorlevel 1 (
    echo.
    echo [WARNING] Some dependencies failed to install.
    echo The skill will still work without full functionality.
    echo To fix, try: pip install bm25s==0.3.8 pdfminer.six==20260107 python-pptx==1.0.2
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] All dependencies installed successfully.
echo.
pause
