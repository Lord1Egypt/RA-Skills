#!/usr/bin/env python3
"""
Formatters para output amigável
"""
import json
from typing import Dict, List, Optional
from cnj_number import formatar_cnj

def formatar_processo(dados: dict) -> str:
    """Formata dados do processo em texto amigável"""
    linhas = []
    
    linhas.append("=" * 50)
    linhas.append("📋 PROCESSO JUDICIAL")
    linhas.append("=" * 50)
    
    numero = dados.get("numero", "")
    linhas.append(f"**Número:** {formatar_cnj(numero)}")
    linhas.append(f"**Tribunal:** {dados.get('tribunal', 'N/A').upper()}")
    linhas.append(f"**Grau:** {dados.get('grau', 'N/A')}")
    linhas.append(f"**Classe:** {dados.get('classe', 'N/A')}")
    
    if dados.get("assuntos"):
        linhas.append(f"**Assuntos:** {', '.join(dados['assuntos'][:3])}")
    
    linhas.append(f"**Órgão Julgador:** {dados.get('orgaoJulgador', 'N/A')}")
    linhas.append(f"**Data Ajuizamento:** {dados.get('dataAjuizamento', 'N/A')}")
    linhas.append(f"**Última Atualização:** {dados.get('dataUltimaAtualizacao', 'N/A')}")
    linhas.append(f"**Sigilo:** {'Sim' if dados.get('sigilo') else 'Não'}")
    
    # Movimentações
    movimentos = dados.get("movimentos", [])
    if movimentos:
        linhas.append("")
        linhas.append("📜 ÚLTIMAS MOVIMENTAÇÕES")
        linhas.append("-" * 40)
        
        for i, mov in enumerate(movimentos[:15], 1):
            data = mov.get("dataHora", "")[:19] if mov.get("dataHora") else "N/A"
            desc = mov.get("descricao", mov.get("nome", "N/A"))
            # Limita tamanho
            if len(desc) > 80:
                desc = desc[:77] + "..."
            linhas.append(f"{i:2}. [{data}] {desc}")
    
    linhas.append("=" * 50)
    return "\n".join(linhas)

def formatar_busca(resultado: dict) -> str:
    """Formata resultado de busca"""
    linhas = []
    total = resultado.get("total", 0)
    processos = resultado.get("processos", [])
    
    linhas.append(f"📊 Total: {total} processo(s) encontrado(s)")
    linhas.append("")
    
    for i, p in enumerate(processos[:10], 1):
        numero = p.get("numeroProcesso", "")
        classe = p.get("classe", {}).get("descricao", "N/A") if isinstance(p.get("classe"), dict) else p.get("classe", "N/A")
        orgao = p.get("orgaoJulgador", {}).get("descricao", "N/A") if isinstance(p.get("orgaoJulgador"), dict) else p.get("orgaoJulgador", "N/A")
        data = p.get("dataAjuizamento", "N/A")
        
        linhas.append(f"{i}. **{formatar_cnj(numero)}**")
        linhas.append(f"   Classe: {classe}")
        linhas.append(f"   Órgão: {orgao}")
        linhas.append(f"   Data: {data}")
        linhas.append("")
    
    return "\n".join(linhas)

def formatar_monitor(processos: List[dict]) -> str:
    """Formata lista de processos monitorados"""
    if not processos:
        return "Nenhum processo monitorado"
    
    linhas = ["📡 PROCESSOS MONITORADOS", "-" * 40]
    
    for p in processos:
        numero = p.get("numeroProcesso", "")
        tribunal = p.get("tribunal", "N/A")
        ultima = p.get("ultimaAtualizacao", "N/A")
        
        linhas.append(f"• {formatar_cnj(numero)} ({tribunal})")
        linhas.append(f"  Última atualização: {ultima[:19] if ultima and len(ultima) > 19 else ultima}")
        linhas.append("")
    
    return "\n".join(linhas)

def formatar_atualizacoes(atualizados: List[dict]) -> str:
    """Formata atualizações detectadas"""
    if not atualizados:
        return "✅ Nenhuma atualização nos processos monitorados"
    
    linhas = ["🔔 ATUALIZAÇÕES DETECTADAS", "-" * 40]
    
    for p in atualizados:
        if "erro" in p:
            linhas.append(f"❌ {p['numeroProcesso']}: {p['erro']}")
        else:
            linhas.append(f"✅ {p['numeroProcesso']} ({p.get('tribunal', '')})")
            linhas.append(f"   Última: {p.get('dataAtualizacao', 'N/A')}")
    
    return "\n".join(linhas)

def formatar_json(dados: dict) -> str:
    """Formata dados como JSON"""
    return json.dumps(dados, indent=2, ensure_ascii=False)
