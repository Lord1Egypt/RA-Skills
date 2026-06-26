# Recon & Pentest Methodology

## Phase 1: Passive Reconnaissance

Gather intel without touching the target.

```bash
# Domain/subdomain enumeration
amass enum -passive -d <DOMAIN> -o amass_passive.txt
subfinder -d <DOMAIN> -silent -o subfinder.txt
assetfinder <DOMAIN> | sort -u > assetfinder.txt

# Merge and deduplicate
cat amass_passive.txt subfinder.txt assetfinder.txt | sort -u > all_subs.txt

# Historical URL discovery
cat all_subs.txt | waybackurls > wayback.txt
cat all_subs.txt | gau > gau.txt
cat wayback.txt gau.txt | sort -u | uro > all_urls.txt

# DNS records
dig <DOMAIN> any +noall +answer
dig <DOMAIN> axfr  # Zone transfer attempt
dnsrecon -d <DOMAIN> -t std,brt,axfr
fierce --domain <DOMAIN>
dnsenum <DOMAIN>

# WHOIS
whois <DOMAIN>

# Certificate transparency
curl -s "https://crt.sh/?q=%.<DOMAIN>&output=json" | jq -r '.[].name_value' | sort -u

# Email harvesting
theHarvester -d <DOMAIN> -b all -l 500
```

## Phase 2: Active Reconnaissance

### Port Scanning
```bash
# Fast initial scan
rustscan -a <TARGET> --ulimit 5000 -- -sV -sC -oN rustscan.txt
# OR
masscan <TARGET> -p1-65535 --rate 1000 -oG masscan.txt

# Targeted follow-up with nmap
nmap -sV -sC -p <PORTS> -oA nmap_detailed <TARGET>

# Full comprehensive
nmap -sV -sC -A -T4 -p- -oA nmap_full <TARGET>

# UDP scan (top ports)
nmap -sU --top-ports 50 -sV <TARGET>

# Vulnerability scan
nmap --script vuln -p <PORTS> <TARGET>
```

### Service-Specific Enumeration

**HTTP/HTTPS (80, 443, 8080, 8443)**
```bash
httpx -u <TARGET> -probe -tech-detect -status-code -title -content-length -follow-redirects
whatweb -v -a 3 <URL>
wafw00f <URL>  # WAF detection
nuclei -u <URL> -severity critical,high -t cves/ -t exposures/ -t misconfiguration/
```

**SMB (445)**
```bash
enum4linux-ng <TARGET> -A
smbmap -H <TARGET>
smbmap -H <TARGET> -u '' -p ''  # Null session
smbclient -L //<TARGET>/ -N  # List shares
netexec smb <TARGET> -u '' -p '' --shares
```

**LDAP (389, 636)**
```bash
ldapsearch -x -H ldap://<TARGET> -b "dc=<DOMAIN>" -s base namingcontexts
ldapsearch -x -H ldap://<TARGET> -b "dc=<DOMAIN>" "(objectClass=*)"
```

**SSH (22)**
```bash
nmap --script ssh-auth-methods,ssh-hostkey -p 22 <TARGET>
# Brute: hydra -l <USER> -P /usr/share/wordlists/rockyou.txt ssh://<TARGET>
```

**FTP (21)**
```bash
nmap --script ftp-anon,ftp-bounce,ftp-vuln* -p 21 <TARGET>
# Anonymous: ftp <TARGET> → user: anonymous, pass: (blank)
```

**DNS (53)**
```bash
dig axfr @<TARGET> <DOMAIN>  # Zone transfer
dnsrecon -d <DOMAIN> -n <TARGET> -t axfr
```

**SNMP (161)**
```bash
snmpwalk -v2c -c public <TARGET>
onesixtyone -c /usr/share/seclists/Discovery/SNMP/common-snmp-community-strings.txt <TARGET>
```

**MySQL (3306)**
```bash
nmap --script mysql-info,mysql-enum -p 3306 <TARGET>
mysql -h <TARGET> -u root -p  # Try empty/common passwords
```

**RDP (3389)**
```bash
nmap --script rdp-enum-encryption,rdp-vuln-ms12-020 -p 3389 <TARGET>
```

## Phase 3: Vulnerability Scanning

```bash
# Nuclei — template-based vulnerability scanning
nuclei -u <URL> -severity critical,high,medium -o nuclei_results.txt
nuclei -u <URL> -tags cve,rce,sqli,xss,ssrf,lfi -o nuclei_tagged.txt

# Nikto — web server misconfigurations
nikto -h <URL> -C all -o nikto.txt

# SSL/TLS
testssl --quiet --sneaky <HOST>:443
sslscan <HOST>:443
```

## Phase 4: Web Application Testing

```bash
# Directory brute-forcing
gobuster dir -u <URL> -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt \
  -x php,html,txt,js,bak,zip,config -t 50 -o gobuster.txt
ffuf -u <URL>/FUZZ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt \
  -mc 200,204,301,302,307,401,403 -o ffuf.txt

# Spider/crawl
katana -u <URL> -depth 3 -js-crawl -form-extraction -o katana.txt

# Parameter discovery
arjun -u <URL> --get --post --stable
paramspider -d <DOMAIN>

# SQL injection
sqlmap -u "<URL>?param=1" --batch --level 5 --risk 3 --threads 10 --dbs

# XSS
dalfox url "<URL>?param=test" --mining-dom --mining-dict

# CMS-specific
wpscan --url <URL> --enumerate ap,at,cb,dbe --api-token <TOKEN>
```

## Phase 5: Credential Attacks

```bash
# HTTP form brute-force
hydra -l <USER> -P /usr/share/wordlists/rockyou.txt <TARGET> http-post-form \
  "/login:user=^USER^&pass=^PASS^:F=incorrect"

# SSH brute-force
hydra -l <USER> -P /usr/share/wordlists/rockyou.txt ssh://<TARGET>

# SMB
netexec smb <TARGET> -u users.txt -p passwords.txt --continue-on-success

# Hash cracking
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt
hashcat -m <MODE> -a 0 hashes.txt /usr/share/wordlists/rockyou.txt
```

## Useful Wordlists

| Purpose | Path |
|---------|------|
| General dirs | `/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt` |
| Common passwords | `/usr/share/wordlists/rockyou.txt` |
| Common dirs/files | `/usr/share/wordlists/dirb/common.txt` |
| SecLists (if installed) | `/usr/share/seclists/` |
| Common usernames | `/usr/share/seclists/Usernames/top-usernames-shortlist.txt` |
| Web extensions | `php,html,txt,js,bak,zip,xml,json,config,env,log` |

## Cloud Security Assessment

```bash
# AWS
prowler aws --profile <PROFILE> --region <REGION> -M json
scout-suite aws --profile <PROFILE>

# Container/K8s
trivy image <IMAGE>  # Container vulnerability scan
trivy fs /path/to/project  # Filesystem scan
kube-hunter --remote <TARGET>  # K8s pentest
kube-bench  # CIS benchmark

# IaC scanning
checkov -d /path/to/terraform/
terrascan scan -i terraform -d /path/to/terraform/
```
