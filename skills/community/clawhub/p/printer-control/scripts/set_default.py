#!/usr/bin/env python3
"""
Set the default printer on the system.

Usage:
    python set_default.py --printer "Printer Name"
"""

import sys
import argparse


def set_default_pywin32(printer_name):
    """Set default printer using pywin32."""
    try:
        import win32print
    except ImportError:
        return False, "pywin32 not available"
    
    try:
        win32print.SetDefaultPrinter(printer_name)
        return True, f"Default printer set to: {printer_name}"
    except Exception as e:
        return False, f"Error: {e}"


def set_default_powershell(printer_name):
    """Set default printer using PowerShell (fallback)."""
    import subprocess
    
    try:
        ps_script = f"""
        $printer = Get-Printer -Name "{printer_name}" -ErrorAction Stop
        $printer | Set-Printer -Default
        """
        
        result = subprocess.run(
            ['powershell', '-Command', ps_script],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            return True, f"Default printer set to: {printer_name}"
        else:
            return False, f"PowerShell error: {result.stderr}"
    
    except Exception as e:
        return False, f"PowerShell fallback error: {e}"


def get_default_printer():
    """Get current default printer."""
    try:
        import win32print
        return win32print.GetDefaultPrinter()
    except:
        pass
    
    try:
        import subprocess
        result = subprocess.run(
            ['powershell', '-Command', '(Get-Printer | Where-Object {$_.Default -eq $true}).Name'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except:
        pass
    
    return None


def main():
    parser = argparse.ArgumentParser(description='Set the default printer')
    parser.add_argument('--printer', required=True, help='Printer name (exact match)')
    
    args = parser.parse_args()
    
    # Show current default
    current_default = get_default_printer()
    if current_default:
        print(f"Current default printer: {current_default}")
    else:
        print("Current default printer: Unknown")
    
    print(f"Setting default to: {args.printer}")
    print()
    
    # Try pywin32 first
    success, message = set_default_pywin32(args.printer)
    
    # Fallback to PowerShell
    if not success:
        print(f"[INFO] pywin32 method failed: {message}")
        print("[INFO] Trying PowerShell fallback...\n")
        success, message = set_default_powershell(args.printer)
    
    if success:
        print(f"[SUCCESS] {message}")
        sys.exit(0)
    else:
        print(f"[ERROR] {message}")
        sys.exit(1)


if __name__ == '__main__':
    main()
