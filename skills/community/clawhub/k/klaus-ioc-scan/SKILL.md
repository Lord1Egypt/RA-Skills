---
name: klaus-ioc-scan
description: Analisa URLs/domínios/IPs (IOC): reputação + virus scan usando VirusTotal e AbuseIPDB
version: 1.0.0
author: Klaus
homepage: https://docs.virustotal.com/
metadata:
  openclaw:
    emoji: "🛡️"
    homepage: "https://docs.virustotal.com/"
    requires:
      env: ["VIRUSTOTAL_API_KEY", "ABUSEIPDB_API_KEY"]
      bins: ["curl"]
    primaryEnv: "VIRUSTOTAL_API_KEY"
tags: [ioc, scanner, security, virustotal, abuseipdb, malware, phishing]
user-invocable: true
---

# Klaus IOC Scanner 🛡️

Analisa URLs, domínios e IPs (IOCs) usando VirusTotal e AbuseIPDB para verificar reputação e detecções de malware/phishing.

## Gatilhos

Use esta skill quando o usuário:
- Colar URLs, domínios ou IPs
- Pedir: "scan", "verificar", "reputação", "é malicioso?", "VirusTotal", "AbuseIPDB"

## Configuração

### Variáveis de Ambiente
```bash
export VIRUSTOTAL_API_KEY="sua_chave_virustotal"
export ABUSEIPDB_API_KEY="sua_chave_abuseipdb"
```

## Uso via Linha de Comando

```bash
# Verificar IP
python3 src/ioc_scan.py scan 45.67.89.10

# Verificar domínio
python3 src/ioc_scan.py scan exemplo.com

# Verificar URL
python3 src/ioc_scan.py scan "https://exemplo.com/login"

# Verificar múltiplos IOCs
python3 src/ioc_scan.py scan "https://exemplo.com 8.8.8.8 dominio.ruim"

# Modo detalhado
python3 src/ioc_scan.py scan --verbose 1.2.3.4
```

## Exemplos

- "Verifica a reputação deste IP: 45.67.89.10"
- "Esse link é phishing? https://exemplo.tld/login"
- "Analisa: exemplo.com 8.8.8.8"

## Saída

A skill retorna:
1. Resumo executivo com veredito
2. Tabela rápida de resultados
3. Detalhes por IOC (VirusTotal + AbuseIPDB)
4. Recomendações de ação
