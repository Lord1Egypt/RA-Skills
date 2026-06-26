#!/usr/bin/env python3
"""
List all available printers on the system.
Supports Windows with pywin32 or PowerShell fallback.

Usage:
    python list_printers.py
"""

import sys
import subprocess


def list_printers_pywin32():
    """List printers using pywin32."""
    try:
        import win32print
    except ImportError:
        return None
    
    printers = []
    try:
        # Get all printers (level 2 gives detailed info)
        printer_list = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
        for printer in printer_list:
            printers.append({
                'name': printer[2],  # Printer name
                'server': printer[1],  # Server name (empty for local)
                'attributes': printer[7],
            })
    except Exception as e:
        print(f"Error enumerating printers: {e}", file=sys.stderr)
        return None
    
    return printers


def list_printers_powershell():
    """List printers using PowerShell (fallback)."""
    try:
        result = subprocess.run(
            ['powershell', '-Command', 
             'Get-Printer | Select-Object Name,Type,Shared,PortName | ConvertTo-Json'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            import json
            data = json.loads(result.stdout)
            printers = []
            # Handle both single object and array
            if isinstance(data, dict):
                data = [data]
            for p in data:
                printers.append({
                    'name': p.get('Name', 'Unknown'),
                    'type': p.get('Type', 'Unknown'),
                    'shared': p.get('Shared', False),
                    'port': p.get('PortName', 'Unknown'),
                })
            return printers
    except Exception as e:
        print(f"PowerShell fallback error: {e}", file=sys.stderr)
    
    return None


def find_printer_by_partial_name(name_partial):
    """Find printer by partial name match or port name."""
    # Try pywin32 first
    printers = list_printers_pywin32()
    if printers is None:
        printers = list_printers_powershell()
    
    if printers is None:
        return None
    
    # Try to find by partial match
    name_lower = name_partial.lower()
    for printer in printers:
        prt_name = printer.get('name', '')
        prt_port = printer.get('port', '')
        
        # Match by name or port
        if name_lower in prt_name.lower() or name_lower in str(prt_port).lower():
            return printer
    
    return None


def main():
    print("=" * 60)
    print("Available Printers")
    print("=" * 60)
    
    # Try pywin32 first
    printers = list_printers_pywin32()
    
    # Fallback to PowerShell
    if printers is None:
        print("\n[INFO] pywin32 not available, using PowerShell fallback...\n")
        printers = list_printers_powershell()
    
    if printers is None:
        print("\n[ERROR] Could not list printers. Make sure you're on Windows.")
        sys.exit(1)
    
    if not printers:
        print("\nNo printers found on this system.")
        sys.exit(0)
    
    print(f"\nFound {len(printers)} printer(s):\n")
    
    for i, printer in enumerate(printers, 1):
        print(f"{i}. {printer['name']}")
        if 'type' in printer:
            print(f"   Type: {printer['type']}, Port: {printer['port']}")
        if 'server' in printer and printer['server']:
            print(f"   Server: {printer['server']}")
        print()
    
    print("=" * 60)
    print("Use the exact printer name with other scripts in this skill.")
    print("=" * 60)


if __name__ == '__main__':
    main()
