#!/usr/bin/env python3
"""
Print raw text string to a specified printer.

Usage:
    python print_text.py --printer "Printer Name" --text "Hello, World!"
"""

import sys
import argparse


def print_text_pywin32(printer_name, text, copies=1):
    """Print text using pywin32."""
    try:
        import win32print
    except ImportError:
        return False, "pywin32 not available"
    
    try:
        # Get printer handle
        hPrinter = win32print.OpenPrinter(printer_name)
        
        # Prepare text with line endings
        text_bytes = (text + '\n').encode('utf-8')
        
        # Start print job
        job_info = {
            'Document': 'Print Text Job',
            'Datatype': 'RAW',
        }
        hJob = win32print.StartDocPrinter(hPrinter, 1, job_info)
        win32print.StartPagePrinter(hPrinter)
        
        # Send text to printer
        win32print.WritePrinter(hPrinter, text_bytes)
        
        # End print job
        win32print.EndPagePrinter(hPrinter)
        win32print.EndDocPrinter(hPrinter)
        win32print.ClosePrinter(hPrinter)
        
        return True, f"Printed text to {printer_name}"
    
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


def print_text_powershell(printer_name, text):
    """Print text using PowerShell (fallback)."""
    import subprocess
    
    # Try to find printer by partial name if exact match fails
    actual_name = find_printer_by_partial_name(printer_name)
    if actual_name:
        printer_name = actual_name
        print(f"[INFO] Found printer: {printer_name}")
    
    try:
        # Escape special characters for PowerShell
        escaped_text = text.replace("'", "''").replace('$', '`$').replace('"', '`"')
        
        ps_script = f"""
        $printer = Get-Printer -Name "{printer_name}" -ErrorAction Stop
        
        # Create a temporary text file
        $tempFile = [System.IO.Path]::GetTempFileName()
        "{escaped_text}" | Out-File -FilePath $tempFile -Encoding UTF8
        
        # Print the file using Notepad
        $notepad = Start-Process notepad.exe -ArgumentList "/p $tempFile" -PassThru -WindowStyle Hidden
        $notepad.WaitForExit(5000)
        
        # Clean up temp file after a short delay
        Start-Sleep -Seconds 2
        Remove-Item $tempFile -Force
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
    
    except Exception as e:
        return False, f"PowerShell fallback error: {e}"


def main():
    parser = argparse.ArgumentParser(description='Print raw text to a specified printer')
    parser.add_argument('--printer', required=True, help='Printer name (exact match)')
    parser.add_argument('--text', required=True, help='Text to print')
    parser.add_argument('--copies', type=int, default=1, help='Number of copies (default: 1)')
    
    args = parser.parse_args()
    
    print(f"Printing text: {args.text[:50]}{'...' if len(args.text) > 50 else ''}")
    print(f"Printer: {args.printer}")
    print(f"Copies: {args.copies}")
    print()
    
    # Try pywin32 first
    success, message = print_text_pywin32(args.printer, args.text, args.copies)
    
    # Fallback to PowerShell
    if not success:
        print(f"[INFO] pywin32 method failed: {message}")
        print("[INFO] Trying PowerShell fallback...\n")
        success, message = print_text_powershell(args.printer, args.text)
    
    if success:
        print(f"[SUCCESS] {message}")
        sys.exit(0)
    else:
        print(f"[ERROR] {message}")
        sys.exit(1)


if __name__ == '__main__':
    main()
