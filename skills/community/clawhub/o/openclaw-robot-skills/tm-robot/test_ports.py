import socket

# Test port 5891 (SVR)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(3)
result = sock.connect_ex(('192.168.1.13', 5891))
sock.close()
print(f'Port 5891 (SVR): {"OPEN" if result == 0 else "CLOSED"} ({result})')

# Test port 5890 (SCT)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(3)
result = sock.connect_ex(('192.168.1.13', 5890))
sock.close()
print(f'Port 5890 (SCT): {"OPEN" if result == 0 else "CLOSED"} ({result})')
