# Tool Quick Reference

Condensed syntax for 80+ security tools, organized by category.

## Network Scanning

| Tool | Quick Usage |
|------|------------|
| nmap | `nmap -sV -sC -p- -T4 <TARGET>` |
| rustscan | `rustscan -a <TARGET> --ulimit 5000 -- -sV -sC` |
| masscan | `masscan <TARGET> -p1-65535 --rate 1000` |
| autorecon | `autorecon <TARGET> -o /tmp/autorecon` |

## Subdomain & DNS

| Tool | Quick Usage |
|------|------------|
| amass | `amass enum -d <DOMAIN>` (active) / `-passive` |
| subfinder | `subfinder -d <DOMAIN> -silent` |
| fierce | `fierce --domain <DOMAIN>` |
| dnsenum | `dnsenum <DOMAIN>` |
| dnsrecon | `dnsrecon -d <DOMAIN> -t std,brt,axfr` |
| theHarvester | `theHarvester -d <DOMAIN> -b all -l 500` |

## Web Content Discovery

| Tool | Quick Usage |
|------|------------|
| gobuster | `gobuster dir -u <URL> -w <WORDLIST> -x php,html,txt -t 50` |
| feroxbuster | `feroxbuster -u <URL> -w <WORDLIST> -x php,html,js,txt` |
| ffuf | `ffuf -u <URL>/FUZZ -w <WORDLIST> -mc 200,301,302,403` |
| dirsearch | `dirsearch -u <URL> -e php,html,js -t 50` |
| dirb | `dirb <URL> <WORDLIST>` |

## Web Vulnerability Scanning

| Tool | Quick Usage |
|------|------------|
| nuclei | `nuclei -u <URL> -severity critical,high -o results.txt` |
| nikto | `nikto -h <URL> -C all` |
| sqlmap | `sqlmap -u "<URL>?p=1" --batch --level 3 --risk 2` |
| dalfox | `dalfox url "<URL>?p=test" --mining-dom` |
| wpscan | `wpscan --url <URL> --enumerate ap,at,cb,dbe` |
| wafw00f | `wafw00f <URL>` |

## Web Crawling & Probing

| Tool | Quick Usage |
|------|------------|
| httpx | `httpx -u <URL> -probe -tech-detect -status-code -title` |
| katana | `katana -u <URL> -depth 3 -js-crawl` |
| gau | `gau <DOMAIN>` |
| waybackurls | `echo <DOMAIN> \| waybackurls` |
| whatweb | `whatweb -v -a 3 <URL>` |

## Parameter Discovery

| Tool | Quick Usage |
|------|------------|
| arjun | `arjun -u <URL> --get --post` |
| paramspider | `paramspider -d <DOMAIN>` |
| x8 | `x8 -u <URL> -w <WORDLIST>` |

## SMB/Windows

| Tool | Quick Usage |
|------|------------|
| enum4linux-ng | `enum4linux-ng <TARGET> -A` |
| smbmap | `smbmap -H <TARGET> -u '' -p ''` |
| netexec | `netexec smb <TARGET> -u '' -p '' --shares` |
| rpcclient | `rpcclient -U '' -N <TARGET>` |
| evil-winrm | `evil-winrm -i <TARGET> -u <USER> -p <PASS>` |

## Credential Attacks

| Tool | Quick Usage |
|------|------------|
| hydra | `hydra -l <USER> -P <WORDLIST> <TARGET> <SERVICE>` |
| john | `john --wordlist=<WORDLIST> --format=<FMT> <HASHES>` |
| hashcat | `hashcat -m <MODE> -a 0 <HASHES> <WORDLIST>` |
| medusa | `medusa -h <TARGET> -u <USER> -P <WORDLIST> -M <MODULE>` |
| hash-identifier | `hash-identifier` (interactive) |

## Binary Analysis

| Tool | Quick Usage |
|------|------------|
| checksec | `checksec --file <BIN>` |
| file | `file <BIN>` |
| strings | `strings -n 8 <BIN>` |
| objdump | `objdump -d -M intel <BIN>` |
| readelf | `readelf -a <BIN>` |
| nm | `nm -D <BIN>` |
| ldd | `ldd <BIN>` |
| ltrace | `ltrace ./<BIN>` |
| strace | `strace -f ./<BIN>` |

## Reverse Engineering

| Tool | Quick Usage |
|------|------------|
| radare2 | `r2 -A <BIN>` then `afl` (functions), `pdf @main` (disasm) |
| ghidra | `analyzeHeadless /tmp proj -import <BIN> -postScript <SCRIPT>` |
| ropper | `ropper --file <BIN> --search "pop rdi"` |
| ROPgadget | `ROPgadget --binary <BIN>` |
| one_gadget | `one_gadget <LIBC>` |
| upx | `upx -d <BIN>` (unpack) |
| angr | Python: `import angr; p = angr.Project('<BIN>')` |

## Forensics

| Tool | Quick Usage |
|------|------------|
| binwalk | `binwalk -e <FILE>` (extract embedded) |
| foremost | `foremost -i <FILE> -o /tmp/out` |
| exiftool | `exiftool <FILE>` (metadata) |
| steghide | `steghide extract -sf <IMG> -p "<PASS>"` |
| zsteg | `zsteg -a <PNG>` |
| volatility | `volatility -f <DUMP> --profile=<P> <PLUGIN>` |
| volatility3 | `python3 vol.py -f <DUMP> windows.pslist` |
| tshark | `tshark -r <PCAP> -Y "<FILTER>"` |

## OSINT

| Tool | Quick Usage |
|------|------------|
| sherlock | `sherlock <USERNAME>` |
| whois | `whois <DOMAIN>` |
| shodan | `shodan search "hostname:<DOMAIN>"` |
| dig | `dig <DOMAIN> any +noall +answer` |

## Cloud Security

| Tool | Quick Usage |
|------|------------|
| prowler | `prowler aws --profile <P> -M json` |
| scout-suite | `scout-suite aws --profile <P>` |
| trivy | `trivy image <IMG>` / `trivy fs <PATH>` |
| kube-hunter | `kube-hunter --remote <TARGET>` |
| kube-bench | `kube-bench` |
| checkov | `checkov -d <PATH>` |
| terrascan | `terrascan scan -i terraform -d <PATH>` |

## SSL/TLS

| Tool | Quick Usage |
|------|------------|
| testssl | `testssl --quiet <HOST>:443` |
| sslscan | `sslscan <HOST>:443` |
| sslyze | `sslyze <HOST>` |

## Hashcat Mode Reference

| Hash Type | Mode (-m) |
|-----------|-----------|
| MD5 | 0 |
| SHA1 | 100 |
| SHA256 | 1400 |
| SHA512 | 1700 |
| sha512crypt ($6$) | 1800 |
| bcrypt | 3200 |
| NTLM | 1000 |
| NetNTLMv2 | 5600 |
| WPA/WPA2 | 22000 |
| Kerberos TGS (23) | 13100 |
| Kerberos AS-REP (23) | 18200 |
