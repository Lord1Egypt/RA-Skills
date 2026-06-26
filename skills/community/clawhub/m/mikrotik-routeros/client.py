import socket
import select
import hashlib
import binascii

"""
MikroTik RouterOS API Client - Core Connection Module
Author: Xiage
Translator/Maintainer: drodecker
"""

class RouterOSApi:
    """MikroTik RouterOS API Client"""
    
    def __init__(self, host, username='admin', password='', port=8728, timeout=5):
        """
        Initialize API Client
        
        Args:
            host: RouterOS device IP address
            username: Username (default: admin)
            password: Password (default: empty)
            port: API port (default: 8728, use 8729 for SSL)
            timeout: Connection timeout (seconds)
        """
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.timeout = timeout
        self.sock = None

    def connect(self):
        """Establish connection to RouterOS"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(self.timeout)
            self.sock.connect((self.host, self.port))
            self.sock.setblocking(0)  # Non-blocking mode (select handles timeout)
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False

    def disconnect(self):
        """Disconnect"""
        if self.sock:
            try:
                self.sock.close()
            except:
                pass
            self.sock = None

    def _send_word(self, word):
        """Send an API word"""
        if not self.sock:
            raise ConnectionError("Not connected to RouterOS")
            
        b_word = word.encode('utf-8')
        length = len(b_word)
        
        # Encode length prefix
        if length < 0x80:
            header = bytes([length])
        elif length < 0x4000:
            length |= 0x8000
            header = bytes([(length >> 8) & 0xFF, length & 0xFF])
        elif length < 0x200000:
            length |= 0xC00000
            header = bytes([(length >> 16) & 0xFF, (length >> 8) & 0xFF, length & 0xFF])
        elif length < 0x10000000:
            length |= 0xE0000000
            header = bytes([(length >> 24) & 0xFF, (length >> 16) & 0xFF, (length >> 8) & 0xFF, length & 0xFF])
        else:
            header = bytes([0xF0, (length >> 24) & 0xFF, (length >> 16) & 0xFF, (length >> 8) & 0xFF, length & 0xFF])
            
        self.sock.sendall(header + b_word)

    def _recv_word(self):
        """
        Receive an API word
        
        RouterOS API uses length-prefixed format:
        - 1st byte: length marker
        - Subsequent bytes: actual length (calculated based on marker)
        - Finally: actual data
        
        Returns:
            Decoded string, or None (timeout/error)
        """
        try:
            # Wait for data
            ready = select.select([self.sock], [], [], self.timeout)
            if not ready[0]:
                return None
                
            # Read length prefix (1st byte)
            b = self.sock.recv(1)
            if not b:
                return None
            
            length = b[0]
            
            # Calculate actual length based on bits
            if (length & 0x80) == 0:
                pass # length < 0x80
            elif (length & 0xC0) == 0x80:
                # 2 bytes: 10xxxxxx + 1 byte length
                b = self.sock.recv(1)
                length = ((length & 0x3F) << 8) + b[0]
            elif (length & 0xE0) == 0xC0:
                # 3 bytes: 110xxxxx + 2 bytes length
                b = self.sock.recv(2)
                length = ((length & 0x1F) << 16) + (b[0] << 8) + b[1]
            elif (length & 0xF0) == 0xE0:
                # 4 bytes: 1110xxxx + 3 bytes length
                b = self.sock.recv(3)
                length = ((length & 0x0F) << 24) + (b[0] << 16) + (b[1] << 8) + b[2]
            elif (length & 0xF8) == 0xF0:
                # 5 bytes: 11110xxx + 4 bytes length
                b = self.sock.recv(4)
                length = (b[0] << 24) + (b[1] << 16) + (b[2] << 8) + b[3]
                
            # Read actual data
            data = b""
            while len(data) < length:
                chunk = self.sock.recv(length - len(data))
                if not chunk:
                    break
                data += chunk
                
            return data.decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"⚠️ Failed to receive word: {e}")
            return None

    def _recv_response(self):
        """
        Receive complete API response
        
        RouterOS API response format:
        - !re (record/entry)
        - !done (completed)
        - !trap (error)
        - !halt (stopped)
        
        Each message followed by multiple =key=value, ending with an empty string.
        
        Returns:
            List of parsed entries
        """
        results = []
        entry = {}
        
        try:
            current_timeout = self.timeout
            while True:
                word = self._recv_word()
                
                if word is None:
                    # Timeout, return received data
                    break
                    
                if word == "":
                    # Empty word indicates end of current message
                    if entry:
                        results.append(entry)
                        entry = {}
                    if word_type in ['!done', '!trap', '!halt']:
                        # Completion/error message, return results
                        break
                    continue
                
                # Message type
                if word.startswith('!'):
                    word_type = word
                    continue
                
                # =key=value format
                if word.startswith('='):
                    parts = word.split('=', 2)
                    if len(parts) >= 3:
                        entry[parts[1]] = parts[2]
                
                # Reduce subsequent timeout
                current_timeout = 0.5
                
            return results
        except Exception as e:
            print(f"⚠️ Failed to receive response: {e}")
            return results

    def _parse_response(self, response):
        """Parse API response data (backward compatible, deprecated)"""
        # Use _recv_response() instead
        return response

    def login(self):
        """Login to RouterOS"""
        if not self.sock:
            return False
            
        try:
            # Send login command
            self._send_word('/login')
            self._send_word(f'=name={self.username}')
            self._send_word(f'=password={self.password}')
            self._send_word('')  # End marker
            
            # Receive response
            res = self._recv_response()
            
            # Check for !done response (login success marker)
            # res might look like [{'ret': '...'}, {}] or just []
            if res is not None:
                return True
                
            # If no !done but has data, also consider success (compatible with old versions)
            if res:
                return True
                
            # No response at all, might be a connection issue
            return False
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False

    def run_command(self, command, args=None):
        """
        Execute API command
        
        Args:
            command: Command path (e.g., '/system/resource/print')
            args: Extra argument list (e.g., ['=detail=', '=active='])
            
        Returns:
            List of parsed response data (supports multiple entries)
        """
        if not self.sock:
            raise ConnectionError("Not connected to RouterOS")
            
        try:
            # Send command
            self._send_word(command)
            if args:
                for arg in args:
                    self._send_word(arg)
            self._send_word('')  # End marker
            
            # Receive and parse response
            return self._recv_response()
        except Exception as e:
            print(f"❌ Command execution failed: {e}")
            return []

    def __enter__(self):
        """Context manager entry"""
        if self.connect():
            if self.login():
                return self
        return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()
