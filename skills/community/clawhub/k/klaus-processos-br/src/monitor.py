#!/usr/bin/env python3
"""
Módulo de monitoramento de processos
"""
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Optional

STATE_FILE = Path(__file__).parent.parent / "state" / "monitor.json"

def ensure_state_file():
    """Garante que o arquivo de estado existe"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not STATE_FILE.exists():
        STATE_FILE.write_text("[]")

def load_monitor() -> List[dict]:
    """Carrega lista de processos monitorados"""
    ensure_state_file()
    try:
        return json.loads(STATE_FILE.read_text())
    except:
        return []

def save_monitor(processos: List[dict]):
    """Salva lista de processos monitorados"""
    STATE_FILE.write_text(json.dumps(processos, indent=2, ensure_ascii=False))

def hash_movimentos(movimentos: List[dict]) -> str:
    """Gera hash simples dos movimentos"""
    if not movimentos:
        return ""
    # Pega os 5 últimos movimentos como assinatura
    recent = movimentos[:5]
    data = json.dumps([{
        "c": m.get("codigo"),
        "d": m.get("dataHora")
    } for m in recent], sort_keys=True)
    return hashlib.md5(data.encode()).hexdigest()

def monitor_add(numero: str, tribunal: Optional[str] = None) -> str:
    """Adiciona processo ao monitoramento"""
    processos = load_monitor()
    
    # Verifica se já existe
    for p in processos:
        if p["numeroProcesso"] == numero:
            return f"Processo {numero} já está monitorado"
    
    processos.append({
        "numeroProcesso": numero,
        "tribunal": tribunal,
        "hash": "",
        "ultimaAtualizacao": None
    })
    
    save_monitor(processos)
    return f"Processo {numero} adicionado ao monitoramento"

def monitor_remove(numero: str) -> str:
    """Remove processo do monitoramento"""
    processos = load_monitor()
    inicial = len(processos)
    processos = [p for p in processos if p["numeroProcesso"] != numero]
    
    if len(processos) == inicial:
        return f"Processo {numero} não estava monitorado"
    
    save_monitor(processos)
    return f"Processo {numero} removido do monitoramento"

def monitor_check(client) -> List[dict]:
    """Verifica atualizações nos processos monitorados"""
    processos = load_monitor()
    atualizados = []
    
    for p in processos:
        numero = p["numeroProcesso"]
        tribunal = p.get("tribunal")
        
        try:
            dados = client.consultar(numero, tribunal)
            novo_hash = hash_movimentos(dados.get("movimentos", []))
            
            if p.get("hash") and novo_hash != p["hash"]:
                # Detectar movimentos novos
                movimentos_antigos = p.get("movimentos", [])
                movimentos_atuais = dados.get("movimentos", [])
                
                # Simplificado: marca como atualizado
                atualizados.append({
                    "numeroProcesso": numero,
                    "tribunal": dados.get("tribunal"),
                    "dataAtualizacao": dados.get("dataUltimaAtualizacao"),
                    "novo": True
                })
            
            # Atualiza hash
            p["hash"] = novo_hash
            p["ultimaAtualizacao"] = dados.get("dataUltimaAtualizacao")
            p["movimentos"] = dados.get("movimentos", [])[:10]  # Mantém snapshot
            
        except Exception as e:
            atualizados.append({
                "numeroProcesso": numero,
                "erro": str(e)
            })
    
    save_monitor(processos)
    return atualizados

def monitor_list() -> List[dict]:
    """Lista processos monitorados"""
    return load_monitor()
