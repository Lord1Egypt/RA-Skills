#!/usr/bin/env python3
"""Hexdump Tool - Binary to hex."""

import argparse
import sys


def hexdump(data: bytes, offset: int = 0, length: int = None):
    """Display hexdump."""
    if length:
        data = data[:length]
    
    for i in range(0, len(data), 16):
        chunk = data[i:i+16]
        
        # Offset
        addr = offset + i
        
        # Hex part
        hex_part = ' '.join(f'{b:02x}' for b in chunk)
        hex_part = hex_part.ljust(48)
        
        # ASCII part
        ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        
        print(f'{addr:08x}  {hex_part}  |{ascii_part}|')


def string_to_hex(s: str) -> str:
    """Convert string to hex."""
    return s.encode('utf-8').hex()


def hex_to_string(h: str) -> str:
    """Convert hex to string."""
    return bytes.fromhex(h).decode('utf-8')


def main():
    parser = argparse.ArgumentParser(description='Hexdump tool')
    parser.add_argument('file', nargs='?', help='File to dump')
    parser.add_argument('-s', '--string', help='String to convert')
    parser.add_argument('-e', '--encode', help='Encode string to hex')
    parser.add_argument('-d', '--decode', help='Decode hex to string')
    parser.add_argument('-n', '--length', type=int, help='Bytes to show')
    parser.add_argument('-o', '--offset', type=int, default=0, help='Starting offset')
    
    args = parser.parse_args()
    
    if args.encode:
        print(string_to_hex(args.encode))
    elif args.decode:
        print(hex_to_string(args.decode))
    elif args.string:
        print(string_to_hex(args.string))
    elif args.file:
        try:
            with open(args.file, 'rb') as f:
                data = f.read()
            hexdump(data, args.offset, args.length)
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
    else:
        # Read from stdin
        data = sys.stdin.buffer.read()
        hexdump(data)


if __name__ == '__main__':
    main()
