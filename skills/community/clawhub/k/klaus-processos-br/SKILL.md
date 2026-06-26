---
name: klaus_processos_br
description: Consulta processos judiciais brasileiros (Brasil) via API Pública do DataJud (CNJ)
---

# Skill: klaus_processos_br

Consultas de processos judiciais brasileiros usando a API Pública do DataJud (CNJ).

## Quando usar

Use esta skill quando o usuário pedir:
- Consultar processo judicial por número CNJ
- Buscar processos por filtros (classe, órgão, data)
- Monitorar atualizações de processos
- Verificar andamento de processo

## Como usar

### Consultar processo por número CNJ

```
python3 ~/.openclaw/workspace/skills/klaus-processos-br/src/cli.py consultar --numero <NUMERO_CNJ>
```

Exemplo:
```bash
python3 ~/.openclaw/workspace/skills/klaus-processos-br/src/cli.py consultar --numero "0000000-00.2025.4.01.3300"
```

Opções:
- `--numero` (obrigatório): Número CNJ com ou sem máscara
- `--tribunal` (opcional): Alias do tribunal (ex: tjsp, trf1, stj). Se omitido, infere automaticamente.
- `--max-movimentos` (opcional, default: 50): Quantidade máxima de movimentações
- `--json` (opcional): Saída em JSON em vez de texto

### Inferir tribunal

Se não souber o tribunal, pode primeiro inferir:
```bash
python3 ~/.openclaw/workspace/skills/klaus-processos-br/src/cli.py inferir --numero <NUMERO_CNJ>
```

### Buscar processos por filtros

```bash
python3 ~/.openclaw/workspace/skills/klaus-processos-br/src/cli.py buscar --tribunal <ALIAS> [opções]
```

Opções:
- `--tribunal` (obrigatório): Alias do tribunal
- `--classe`: Código da classe processual
- `--orgao`: Código do órgão julgador
- `--grau`: G1, G2, JE
- `--ajuizamento-de`: Data inicial (YYYY-MM-DD)
- `--ajuizamento-ate`: Data final (YYYY-MM-DD)
- `--size`: Quantidade de resultados (default: 10)
- `--json`: Saída em JSON

### Monitoramento de processos

**Adicionar processo ao monitoramento:**
```bash
python3 ~/.openclaw/workspace/skills/klaus-processos-br/src/cli.py monitor-add --numero <NUMERO_CNJ> [--tribunal <ALIAS>]
```

**Verificar atualizações:**
```bash
python3 ~/.openclaw/workspace/skills/klaus-processos-br/src/cli.py monitor-check
```

**Listar processos monitorados:**
```bash
python3 ~/.openclaw/workspace/skills/klaus-processos-br/src/cli.py monitor-list
```

**Remover processo:**
```bash
python3 ~/.openclaw/workspace/skills/klaus-processos-br/src/cli.py monitor-remove --numero <NUMERO_CNJ>
```

##Aliases de tribunais comuns

| Justiça | Alias | Exemplo |
|---------|-------|---------|
| STJ | stj | - |
| Justiça Federal | trf1 a trf6 | trf1 |
| TRT | trt1 a trt24 | trt3 |
| TJ | tj<UF> | tjsp, tjmg, tjdf (use tjdft) |
| TRE | tre-<UF> | tre-sp |
| Justiça Militar MG | tjmmg | - |
| Justiça Militar RS | tjmrs | - |
| Justiça Militar SP | tjmsp | - |

## Formato do número CNJ

O número CNJ tem 20 dígitos: `NNNNNNN-DD.AAAA.J.TR.OOOO`

- 7 dígitos: número sequencial
- 2 dígitos: dígito verificador
- 4 dígitos: ano
- 1 dígito: segmento (3=STJ, 4= JF, 5=JT, 6=JE, 8=JE, 9=JME)
- 2 dígitos: código do tribunal
- 4 dígitos: código do órgão

## Configuração

A API Key pública do DataJud já está configurada por padrão. Opcionalmente, pode-se definir via variável de ambiente:
```
DATAJUD_API_KEY=cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RvnFKZGRQdw==
```

## Limitações

- Apenas processos públicos (sigilosos não retornam dados)
- Rate limit: máximo 2 requisições/segundo
- Nem todos os tribunais estão cobertos (91 tribunais disponíveis)
- STF não está disponível na API pública
