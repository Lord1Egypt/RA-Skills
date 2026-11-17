import socket

target = '192.168.28.18'
ports = [10000, 8080, 80, 443]
for port in ports:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex((target, port))
    status = "OPEN" if result == 0 else "CLOSED"
    print(f"Port {port}: {status} (code={result})")
    sock.close()
