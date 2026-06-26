import socket, time, struct

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(5)
sock.connect(('192.168.1.13', 5891))
sock.send(bytearray([0x01, 0x00, 0x00, 0x00, 0x00]))
time.sleep(0.3)
data = sock.recv(8192)
sock.close()

body = data[data.index(b'\n')+1:]

# Parse all variables
pos = 0
results = {}
while pos < len(body) - 4:
    # Skip nulls
    while pos < len(body) and body[pos] == 0:
        pos += 1
    if pos >= len(body) - 4:
        break
    
    # Read name
    name_start = pos
    while pos < len(body) and body[pos] != 0:
        pos += 1
    name = body[name_start:pos].decode('ascii', errors='replace')
    pos += 1  # skip null after name
    
    if len(name) < 2 or not name[0].isalpha():
        continue
    
    # Read type
    if pos >= len(body):
        break
    type_code = body[pos]
    pos += 1
    
    # Skip null padding
    if pos < len(body) and body[pos] == 0:
        pos += 1
    
    # Read data based on type
    value = None
    data_len = 0
    if type_code == 0x01:  # bool
        value = body[pos] != 0 if pos < len(body) else False
        data_len = 1
    elif type_code == 0x04:  # int32
        if pos + 4 <= len(body):
            value = int.from_bytes(body[pos:pos+4], 'little')
            data_len = 4
    elif type_code == 0x18:  # 6 floats
        if pos + 24 <= len(body):
            value = struct.unpack('<6f', body[pos:pos+24])
            data_len = 24
    elif type_code == 0x08:  # string
        str_start = pos
        while pos < len(body) and body[pos] != 0:
            pos += 1
        value = body[str_start:pos].decode('ascii', errors='replace')
        data_len = pos - str_start
    elif type_code == 0x24:  # 9 floats (Coord_Base_Flange etc.)
        if pos + 36 <= len(body):
            value = struct.unpack('<9f', body[pos:pos+36])
            data_len = 36
    elif type_code >= 0x10:  # other float arrays
        n_floats = type_code // 4
        if pos + type_code <= len(body):
            try:
                value = struct.unpack(f'<{n_floats}f', body[pos:pos+type_code])
                data_len = type_code
            except:
                pass  # Skip invalid data
    
    if value is not None:
        results[name] = value
    
    # Advance past data
    pos += data_len
    
    # Skip the 2-byte marker after data
    if pos + 1 < len(body) and body[pos+1] == 0:
        pos += 2

# Show results
print('Parsed variables:')
for k in ['Error_Code', 'Robot_Error', 'Project_Run', 'Project_Pause',
          'Joint_Angle', 'Coord_Robot_Flange', 'Coord_Base_Flange',
          'TCP_Force', 'Joint_Torque', 'Robot_Light', 'Ctrl_DO0']:
    if k in results:
        print(f'{k:25s} = {results[k]}')
    else:
        print(f'{k:25s} = NOT FOUND')
