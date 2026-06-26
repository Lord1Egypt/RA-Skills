#!/usr/bin/env python3
"""Serial Communication - cross-platform."""
import json, sys, os, argparse, time, serial

def list_ports():
    """List all serial ports."""
    try:
        import serial.tools.list_ports
        ports = [{"port": p.device, "desc": p.description} for p in serial.tools.list_ports.comports()]
        return json.dumps({"ports": ports}, indent=2)
    except ImportError:
        return json.dumps({"error": "Install pyserial"}, indent=2)

def detect_baudrate(port):
    """Auto-detect baudrate."""
    try:
        ser = serial.Serial(port)
        ser.baudrate = 9600
        return json.dumps({"port": port, "baudrate": 9600}, indent=2)
    except:
        return json.dumps({"error": f"Failed to open {port}"}, indent=2)

def send_data(port, data, baud=9600):
    """Send data to serial port."""
    try:
        ser = serial.Serial(port, baud)
        ser.write(data.encode())
        ser.close()
        return json.dumps({"success": True, "sent": data}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def receive_data(port, baud=9600, timeout=5):
    """Receive data from serial port."""
    try:
        ser = serial.Serial(port, baud, timeout=timeout)
        data = ser.read_all().decode('utf-8', errors='ignore')
        ser.close()
        return json.dumps({"received": data}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def chat(port, data, baud=9600):
    """Send data and wait for response."""
    try:
        ser = serial.Serial(port, baud, timeout=5)
        ser.write(data.encode())
        time.sleep(0.5)
        response = ser.read_all().decode('utf-8', errors='ignore')
        ser.close()
        return json.dumps({"sent": data, "received": response}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def monitor(port, baud=9600, duration=30):
    """Monitor serial port in real-time."""
    try:
        ser = serial.Serial(port, baud)
        results = []
        end_time = time.time() + duration
        while time.time() < end_time:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
                results.append({"time": time.time(), "data": data})
            time.sleep(0.1)
        ser.close()
        return json.dumps({"monitor_results": results}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Serial Communication')
    subparsers = parser.add_subparsers(dest='command')

    # list command
    subparsers.add_parser('list')

    # detect command
    detect_parser = subparsers.add_parser('detect')
    detect_parser.add_argument('--port', required=True)

    # send command
    send_parser = subparsers.add_parser('send')
    send_parser.add_argument('--port', required=True)
    send_parser.add_argument('--data', required=True)
    send_parser.add_argument('--baud', type=int, default=9600)

    # receive command
    recv_parser = subparsers.add_parser('receive')
    recv_parser.add_argument('--port', required=True)
    recv_parser.add_argument('--baud', type=int, default=9600)
    recv_parser.add_argument('--timeout', type=int, default=5)

    # chat command
    chat_parser = subparsers.add_parser('chat')
    chat_parser.add_argument('--port', required=True)
    chat_parser.add_argument('--data', required=True)
    chat_parser.add_argument('--baud', type=int, default=9600)

    # monitor command
    monitor_parser = subparsers.add_parser('monitor')
    monitor_parser.add_argument('--port', required=True)
    monitor_parser.add_argument('--baud', type=int, default=9600)
    monitor_parser.add_argument('--duration', type=int, default=30)

    args = parser.parse_args()

    if args.command == 'list':
        print(list_ports())
    elif args.command == 'detect':
        print(detect_baudrate(args.port))
    elif args.command == 'send':
        print(send_data(args.port, args.data, args.baud))
    elif args.command == 'receive':
        print(receive_data(args.port, args.baud, args.timeout))
    elif args.command == 'chat':
        print(chat(args.port, args.data, args.baud))
    elif args.command == 'monitor':
        print(monitor(args.port, args.baud, args.duration))

if __name__ == '__main__':
    main()
