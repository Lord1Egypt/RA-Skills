#!/usr/bin/env python3
"""
Check printer status (online, paper, toner, errors).

Usage:
    python printer_status.py --printer "Printer Name"
    python printer_status.py --all  # Check all printers
"""

import sys
import argparse


def get_printer_status_pywin32(printer_name):
    """Get printer status using pywin32."""
    try:
        import win32print
    except ImportError:
        return None
    
    try:
        hPrinter = win32print.OpenPrinter(printer_name)
        try:
            info = win32print.GetPrinter(hPrinter, 2)
            
            # Status codes
            status = info[8]  # PRINTER_INFO_2.Status
            
            status_info = {
                'name': printer_name,
                'raw_status': status,
                'flags': [],
            }
            
            # Decode status flags
            if status & 0x00000002:
                status_info['flags'].append('PAPER_OUT')
            if status & 0x00000004:
                status_info['flags'].append('PAPER_PROBLEM')
            if status & 0x00000008:
                status_info['flags'].append('OUT_OF_MEMORY')
            if status & 0x00000010:
                status_info['flags'].append('DOOR_OPEN')
            if status & 0x00000020:
                status_info['flags'].append('JAMMED')
            if status & 0x00000040:
                status_info['flags'].append('NOT_AVAILABLE')
            if status & 0x00000080:
                status_info['flags'].append('MANUAL_FEED')
            if status & 0x00000100:
                status_info['flags'].append('TONER_OUT')
            if status & 0x00000200:
                status_info['flags'].append('PAPER_SMALL')
            if status & 0x00000400:
                status_info['flags'].append('PAPER_SIZE')
            if status & 0x00000800:
                status_info['flags'].append('OFFLINE')
            if status & 0x00001000:
                status_info['flags'].append('IO_ACTIVE')
            if status & 0x00002000:
                status_info['flags'].append('BUSY')
            if status & 0x00004000:
                status_info['flags'].append('PRINTING')
            if status & 0x00008000:
                status_info['flags'].append('OUTPUT_BIN_FULL')
            if status & 0x00010000:
                status_info['flags'].append('NOT_AVAILABLE')
            if status & 0x00020000:
                status_info['flags'].append('WAITING')
            if status & 0x00040000:
                status_info['flags'].append('PROCESSING')
            if status & 0x00080000:
                status_info['flags'].append('INITIALIZING')
            if status & 0x00100000:
                status_info['flags'].append('WARMING_UP')
            if status & 0x00200000:
                status_info['flags'].append('TONER_LOW')
            if status & 0x00400000:
                status_info['flags'].append('NO_TONER')
            if status & 0x00800000:
                status_info['flags'].append('PAGE_PUNT')
            if status & 0x01000000:
                status_info['flags'].append('USER_INTERVENTION')
            
            # Determine overall status
            if not status_info['flags']:
                status_info['overall'] = 'READY'
            elif 'OFFLINE' in status_info['flags'] or 'NOT_AVAILABLE' in status_info['flags']:
                status_info['overall'] = 'OFFLINE'
            elif any(f in status_info['flags'] for f in ['PAPER_OUT', 'TONER_OUT', 'JAMMED']):
                status_info['overall'] = 'ERROR'
            elif 'PRINTING' in status_info['flags']:
                status_info['overall'] = 'PRINTING'
            else:
                status_info['overall'] = 'WARNING'
            
            return status_info
            
        finally:
            win32print.ClosePrinter(hPrinter)
    
    except Exception as e:
        return {'name': printer_name, 'error': str(e)}


def get_printer_status_powershell(printer_name):
    """Get printer status using PowerShell (fallback)."""
    import subprocess
    
    try:
        ps_script = f"""
        $printer = Get-Printer -Name "{printer_name}" -ErrorAction Stop
        [PSCustomObject]@{{
            Name = $printer.Name
            Type = $printer.Type
            PortName = $printer.PortName
            Shared = $printer.Shared
            Default = $printer.Default
            Status = if ($printer.WorkOffline) {{ "Offline" }} else {{ "Online" }}
        }} | ConvertTo-Json
        """
        
        result = subprocess.run(
            ['powershell', '-Command', ps_script],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            import json
            data = json.loads(result.stdout)
            return {
                'name': data.get('Name', printer_name),
                'status': data.get('Status', 'Unknown'),
                'type': data.get('Type', 'Unknown'),
                'port': data.get('PortName', 'Unknown'),
                'overall': 'READY' if data.get('Status') == 'Online' else 'OFFLINE',
                'flags': [] if data.get('Status') == 'Online' else ['OFFLINE'],
            }
        else:
            return {'name': printer_name, 'error': result.stderr}
    
    except Exception as e:
        return {'name': printer_name, 'error': str(e)}


def format_status(status_info):
    """Format status info for display."""
    lines = []
    lines.append(f"Printer: {status_info['name']}")
    
    if 'error' in status_info:
        lines.append(f"  Status: ERROR - {status_info['error']}")
        return '\n'.join(lines)
    
    overall = status_info.get('overall', 'UNKNOWN')
    lines.append(f"  Overall Status: {overall}")
    
    flags = status_info.get('flags', [])
    if flags:
        lines.append(f"  Flags: {', '.join(flags)}")
    
    if 'type' in status_info:
        lines.append(f"  Type: {status_info['type']}")
    if 'port' in status_info:
        lines.append(f"  Port: {status_info['port']}")
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Check printer status')
    parser.add_argument('--printer', help='Printer name (exact match)')
    parser.add_argument('--all', action='store_true', help='Check all printers')
    
    args = parser.parse_args()
    
    if not args.printer and not args.all:
        print("[ERROR] Specify --printer or --all")
        sys.exit(1)
    
    print("=" * 60)
    print("Printer Status")
    print("=" * 60)
    print()
    
    # Get list of printers
    try:
        import win32print
        printer_list = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
        printers = [p[2] for p in printer_list]
    except:
        import subprocess
        result = subprocess.run(
            ['powershell', '-Command', 'Get-Printer | Select-Object -ExpandProperty Name'],
            capture_output=True,
            text=True,
            timeout=10
        )
        printers = [p.strip() for p in result.stdout.strip().split('\n') if p.strip()]
    
    if args.all:
        for printer_name in printers:
            status = get_printer_status_pywin32(printer_name)
            if status is None:
                status = get_printer_status_powershell(printer_name)
            print(format_status(status))
            print()
    else:
        if args.printer not in printers:
            print(f"[ERROR] Printer '{args.printer}' not found.")
            print(f"Available printers: {', '.join(printers)}")
            sys.exit(1)
        
        status = get_printer_status_pywin32(args.printer)
        if status is None:
            status = get_printer_status_powershell(args.printer)
        print(format_status(status))
        print()
    
    print("=" * 60)


if __name__ == '__main__':
    main()
