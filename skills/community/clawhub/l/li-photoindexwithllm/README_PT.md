# 📸 PhotoIndexWithLLM — Português

## Visão Geral

PhotoIndexWithLLM é um sistema inteligente de indexação, análise e busca de fotos alimentado por grandes modelos de Visão-Linguagem (VL).

## Início Rápido

```bash
# Instalar dependências
pip install requests

# Escanear fotos
python skill.py scan --dir /home/user/Photos

# Buscar fotos
python skill.py search "praia pôr do sol"

# Saída JSON
python skill.py search "praia" --format json
```

## Plataformas Suportadas

- ✅ Windows 10/11
- ✅ Ubuntu 20.04/22.04/24.04
- ✅ Linux
- ✅ macOS 12+

## Formatos de Imagem Suportados (17 tipos)

| Tipo | Formatos |
|------|----------|
| Comuns | `.jpg` `.jpeg` `.png` `.webp` `.bmp` `.tiff` `.gif` |
| iPhone/Apple | `.heic` `.heif` |
| Canon DSLR | `.cr2` |
| Nikon DSLR | `.nef` |
| Sony DSLR | `.arw` |
| Outros RAW | `.orf` `.raf` `.dng` `.rw2` `.pef` `.sr2` |

## Proteção de Privacidade

- Apenas local por padrão
- As fotos nunca saem do seu computador
- Transferência remota requer consentimento do usuário

## Comandos Completos

```bash
# Escanear fotos
python skill.py scan --dir /home/user/Photos

# Buscar fotos
python skill.py search "praia pôr do sol"

# Escanear e buscar
python skill.py scan_and_search --dir /home/user/Photos --query "praia"

# Anotar
python skill.py annotate --photo /photos/img001.jpg --type person --name João

# Treinar modelo
python skill.py train

# Ver estatísticas
python skill.py stats

# Testar conexão
python skill.py test
```

## Contato

**Autor**: Beijing Lao Li (beijingLL)
**ClawHub ID**: 43622283
