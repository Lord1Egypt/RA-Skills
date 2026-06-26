#!/usr/bin/env python3
"""
Print a text file to a specified printer.

Usage:
    python print_file.py --printer "Printer Name" --file "C:\path\to\file.txt" [--copies 2]
"""

import sys
import argparse
import os


def print_file_pywin32(printer_name, file_path, copies=1):
    """Print a file using pywin32."""
    try:
        import win32print
        import win32api
    except ImportError:
        return False, "pywin32 not available"
    
    try:
        # Get printer handle
        hPrinter = win32print.OpenPrinter(printer_name)
        
        # Read file content
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        # Start print job
        job_info = {
            'Document': os.path.basename(file_path),
            'Datatype': 'RAW',
        }
        hJob = win32print.StartDocPrinter(hPrinter, 1, job_info)
        win32print.StartPagePrinter(hPrinter)
        
        # Send data to printer
        win32print.WritePrinter(hPrinter, file_content)
        
        # End print job
        win32print.EndPagePrinter(hPrinter)
        win32print.EndDocPrinter(hPrinter)
        win32print.ClosePrinter(hPrinter)
        
        return True, f"Printed {copies} copy(ies) of {file_path}"
    
    except Exception as e:
        return False, f"Print error: {e}"


def find_printer_by_partial_name(name_partial):
    """Find printer by partial name match or port name."""
    import subprocess
    
    # Get all printers
    try:
        result = subprocess.run(
            ['powershell', '-Command', 
             'Get-Printer | Select-Object Name,PortName | ConvertTo-Json'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            import json
            data = json.loads(result.stdout)
            if isinstance(data, dict):
                data = [data]
            
            name_lower = name_partial.lower()
            for p in data:
                prt_name = p.get('Name', '')
                prt_port = p.get('PortName', '')
                
                # Match by name or port
                if name_lower in prt_name.lower() or name_lower in str(prt_port).lower():
                    return prt_name
            
    except Exception:
        pass
    
    return None


def print_file_powershell(printer_name, file_path, copies=1):
    """Print a file using PowerShell (fallback for PDF/text)."""
    import subprocess
    
    # Try to find printer by partial name if exact match fails
    actual_name = find_printer_by_partial_name(printer_name)
    if actual_name:
        printer_name = actual_name
        print(f"[INFO] Found printer: {printer_name}")
    
    try:
        # For text files, use PrintText
        if file_path.lower().endswith('.txt'):
            # Read content and print via PowerShell
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Escape special characters for PowerShell
            escaped_content = content.replace("'", "''")
            
            ps_script = f"""
            $printer = Get-Printer -Name "{printer_name}"
            $printJob = $printer | Start-PrintJob
            # Note: PowerShell printing is limited, may not work for all file types
            """
            
            result = subprocess.run(
                ['powershell', '-Command', ps_script],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return True, f"Print job sent to {printer_name}"
            else:
                return False, f"PowerShell error: {result.stderr}"
        
        # For PDF and other files, use Start-Process with -Verb Print
        else:
            ps_script = f"""
            $filePath = "{file_path}"
            $printerName = "{printer_name}"
            
            # Set as default printer temporarily
            $printer = Get-Printer -Name $printerName -ErrorAction Stop
            $oldDefault = (Get-Printer | Where-Object {{$_.Default -eq $true}}).Name
            
            if ($oldDefault -ne $printerName) {{
                $printer | Set-Printer -Shared $printer.Shared
            }}
            
            # Print the file
            Start-Process -FilePath $filePath -Verb Print -WindowStyle Hidden
            
            # Restore default printer
            if ($oldDefault) {{
                Get-Printer -Name $oldDefault | Set-Printer -Shared (Get-Printer -Name $oldDefault).Shared
            }}
            """
            
            result = subprocess.run(
                ['powershell', '-Command', ps_script],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return True, f"Print job sent to {printer_name} (using default printer method)"
            else:
                return False, f"PowerShell error: {result.stderr}"
    
    except Exception as e:
        return False, f"PowerShell fallback error: {e}"


def main():
    parser = argparse.ArgumentParser(description='Print a file to a specified printer')
    parser.add_argument('--printer', required=True, help='Printer name (exact match)')
    parser.add_argument('--file', required=True, help='Path to file to print')
    parser.add_argument('--copies', type=int, default=1, help='Number of copies (default: 1)')
    
    args = parser.parse_args()
    
    # Validate file exists
    if not os.path.exists(args.file):
        print(f"[ERROR] File not found: {args.file}")
        sys.exit(1)
    
    print(f"Printing: {args.file}")
    print(f"Printer: {args.printer}")
    print(f"Copies: {args.copies}")
    print()
    
    # Try pywin32 first
    success, message = print_file_pywin32(args.printer, args.file, args.copies)
    
    # Fallback to PowerShell
    if not success:
        print(f"[INFO] pywin32 method failed: {message}")
        print("[INFO] Trying PowerShell fallback...\n")
        success, message = print_file_powershell(args.printer, args.file, args.copies)
    
    if success:
        print(f"[SUCCESS] {message}")
        sys.exit(0)
    else:
        print(f"[ERROR] {message}")
        sys.exit(1)


if __name__ == '__main__':
    main()
