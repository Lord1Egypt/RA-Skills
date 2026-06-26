#!/usr/bin/env python3
"""
Módulo para normalizar e parsear números CNJ
"""
import re
from typing import Optional

def normalizar_cnj(numero: str) -> str:
    """Remove tudo que não é dígito"""
    return "".join(c for c in numero if c.isdigit())

def parse_cnj(numero: str) -> dict:
    """Parse do número CNJ: NNNNNNN-DD.AAAA.J.TR.OOOO"""
    digits = normalizar_cnj(numero)
    
    if len(digits) != 20:
        raise ValueError(f"Número CNJ deve ter 20 dígitos, received {len(digits)}")
    
    # Formato sem máscara: NNNNNNNDDAAA AJ.TROOOO
    # 0-6 = número seq (7)
    # 7-8 = dígito (2)
    # 9-12 = ano (4)
    # 13 = segmento J (1)
    # 14-15 = tribunal TR (2)
    # 16-19 = órgão OOOO (4)
    return {
        "numero": digits[:7],
        "digito": digits[7:9],
        "ano": digits[9:13],
        "segmento": digits[13],  # J
        "tribunal": digits[14:16],  # TR
        "orgao": digits[16:20]  # OOOO
    }

# Mapa UF para código (justiça eleitoral)
UF_MAP = {
    "ac": "01", "al": "02", "am": "03", "ap": "04", "ba": "05",
    "ce": "06", "df": "07", "es": "08", "go": "09", "ma": "10",
    "mg": "11", "ms": "12", "mt": "13", "pa": "14", "pb": "15",
    "pe": "16", "pi": "17", "pr": "18", "rn": "19", "ro": "20",
    "rr": "21", "rs": "22", "sc": "23", "se": "24", "sp": "25", "to": "26"
}

# Mapa reverso: código -> UF
CODIGO_UF = {v: k for k, v in UF_MAP.items()}

def infer_tribunal(numero: str) -> Optional[str]:
    """Infere o alias do tribunal a partir do número CNJ"""
    parsed = parse_cnj(numero)
    segmento = parsed["segmento"]
    tribunal = parsed["tribunal"]
    
    # STJ
    if segmento == "3" and tribunal == "00":
        return "stj"
    
    # Justiça Federal (J=4)
    if segmento == "4":
        tr = int(tribunal)
        if 1 <= tr <= 6:
            return f"trf{tr}"
    
    # Justiça do Trabalho (J=5)
    if segmento == "5":
        tr = int(tribunal)
        if 1 <= tr <= 24:
            return f"trt{tr}"
        if tribunal == "00":
            return "tst"  # TST precisa de --tribunal explícito na verdade
    
    # Justiça Eleitoral (J=6)
    if segmento == "6":
        tr = int(tribunal)
        if 1 <= tr <= 27:
            uf = CODIGO_UF.get(f"{tr:02d}")
            if uf:
                return f"tre-{uf}"
    
    # Justiça Estadual (J=8)
    if segmento == "8":
        tr = int(tribunal)
        if 1 <= tr <= 26:
            uf = CODIGO_UF.get(f"{tr:02d}")
            if uf:
                if uf == "df":
                    return "tjdft"
                return f"tj{uf}"
    
    # Justiça Militar Estadual (J=9)
    if segmento == "9":
        if tribunal == "13":  # MG
            return "tjmmg"
        if tribunal == "21":  # RS
            return "tjmrs"
        if tribunal == "26":  # SP
            return "tjmsp"
    
    return None


def formatar_cnj(numero: str) -> str:
    """Formata número CNJ com máscara"""
    digits = normalizar_cnj(numero)
    if len(digits) == 20:
        return f"{digits[:7]}-{digits[7:9]}.{digits[9:13]}.{digits[13]}.{digits[14:16]}.{digits[16:20]}"
    return numero


if __name__ == "__main__":
    # Teste
    test_cases = [
        "0000000-00.2025.4.01.3300",  # JF
        "0000001-00.2025.5.03.0000",  # TRT
        "0000002-00.2025.8.26.0000",  # TJSP
        "0000003-00.2025.3.00.0000",  # STJ
    ]
    
    for tc in test_cases:
        try:
            alias = infer_tribunal(tc)
            print(f"{tc} -> {alias}")
        except Exception as e:
            print(f"{tc} -> ERROR: {e}")
