#!/usr/bin/env python3
"""
CLI para consulta processual via DataJud
Uso: python cli.py <comando> [opções]
"""
import argparse
import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datajud_client import DataJudClient
from cnj_number import normalizar_cnj, formatar_cnj, infer_tribunal
from monitor import monitor_add, monitor_remove, monitor_check, monitor_list
from formatters import (formatar_processo, formatar_busca, formatar_monitor, 
                       formatar_atualizacoes, formatar_json)


def cmd_consultar(args, client):
    """Consulta processo por número CNJ"""
    numero = normalizar_cnj(args.numero)
    
    if len(numero) != 20:
        print("Erro: Número CNJ deve ter 20 dígitos", file=sys.stderr)
        sys.exit(1)
    
    try:
        dados = client.consultar(
            numero, 
            tribunal=args.tribunal,
            max_movimentos=args.max_movimentos
        )
        
        if args.json:
            print(formatar_json(dados))
        else:
            print(formatar_processo(dados))
            
    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_buscar(args, client):
    """Busca processos por filtros"""
    try:
        resultado = client.buscar(
            tribunal=args.tribunal,
            parte=args.parte,
            classe=args.classe,
            orgao=args.orgao,
            grau=args.grau,
            ajuizamento_de=args.ajuizamento_de,
            ajuizamento_ate=args.ajuizamento_ate,
            size=args.size
        )
        
        if args.json:
            print(formatar_json(resultado))
        else:
            print(formatar_busca(resultado))
            
    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_monitor_add(args, client):
    """Adiciona processo ao monitoramento"""
    numero = normalizar_cnj(args.numero)
    print(monitor_add(numero, args.tribunal))


def cmd_monitor_remove(args, client):
    """Remove processo do monitoramento"""
    numero = normalizar_cnj(args.numero)
    print(monitor_remove(numero))


def cmd_monitor_check(args, client):
    """Verifica atualizações"""
    atualizados = monitor_check(client)
    print(formatar_atualizacoes(atualizados))


def cmd_monitor_list(args, client):
    """Lista processos monitorados"""
    processos = monitor_list()
    print(formatar_monitor(processos))


def cmd_inferir(args, client):
    """Infere tribunal a partir do número CNJ"""
    numero = normalizar_cnj(args.numero)
    
    if len(numero) != 20:
        print("Erro: Número CNJ deve ter 20 dígitos", file=sys.stderr)
        sys.exit(1)
    
    alias = infer_tribunal(numero)
    if alias:
        print(f"Tribunal inferido: {alias}")
    else:
        print("Não foi possível inferir o tribunal. Forneça --tribunal.")


def main():
    parser = argparse.ArgumentParser(
        description="Consulta processos judiciais via API DataJud (CNJ)"
    )
    subparsers = parser.add_subparsers(dest="comando", help="Comandos disponíveis")
    
    # Comando: consultar
    p_consultar = subparsers.add_parser("consultar", help="Consulta processo por número CNJ")
    p_consultar.add_argument("--numero", required=True, help="Número do processo (CNJ)")
    p_consultar.add_argument("--tribunal", help="Alias do tribunal (ex: tjsp, trf1)")
    p_consultar.add_argument("--max-movimentos", type=int, default=50, help="Máximo de movimentos")
    p_consultar.add_argument("--json", action="store_true", help="Saída em JSON")
    
    # Comando: buscar
    p_buscar = subparsers.add_parser("buscar", help="Busca processos por filtros")
    p_buscar.add_argument("--tribunal", required=True, help="Alias do tribunal")
    p_buscar.add_argument("--parte", help="Nome da parte (autor/réu)")
    p_buscar.add_argument("--classe", help="Código da classe")
    p_buscar.add_argument("--orgao", help="Código do órgão julgador")
    p_buscar.add_argument("--grau", help="Grau (G1, G2, JE)")
    p_buscar.add_argument("--ajuizamento-de", help="Data inicial (YYYY-MM-DD)")
    p_buscar.add_argument("--ajuizamento-ate", help="Data final (YYYY-MM-DD)")
    p_buscar.add_argument("--size", type=int, default=10, help="Quantidade de resultados")
    p_buscar.add_argument("--json", action="store_true", help="Saída em JSON")
    
    # Comando: monitor-add
    p_mon_add = subparsers.add_parser("monitor-add", help="Adiciona processo ao monitoramento")
    p_mon_add.add_argument("--numero", required=True, help="Número do processo")
    p_mon_add.add_argument("--tribunal", help="Alias do tribunal")
    
    # Comando: monitor-remove
    p_mon_rem = subparsers.add_parser("monitor-remove", help="Remove processo do monitoramento")
    p_mon_rem.add_argument("--numero", required=True, help="Número do processo")
    
    # Comando: monitor-check
    subparsers.add_parser("monitor-check", help="Verifica atualizações")
    
    # Comando: monitor-list
    subparsers.add_parser("monitor-list", help="Lista processos monitorados")
    
    # Comando: inferir
    p_inferir = subparsers.add_parser("inferir", help="Infere tribunal pelo número CNJ")
    p_inferir.add_argument("--numero", required=True, help="Número do processo")
    
    # Parser global
    parser.add_argument("--dry-run", action="store_true", help="Imprime query sem executar")
    
    args = parser.parse_args()
    
    if not args.comando:
        parser.print_help()
        sys.exit(1)
    
    # Inicializa cliente
    client = DataJudClient()
    
    # Dry run para consultar
    if args.comando == "consultar" and args.dry_run:
        numero = normalizar_cnj(args.numero)
        tribunal = args.tribunal or infer_tribunal(numero) or "?"
        url = f"https://api-publica.datajud.cnj.jus.br/api_publica_{tribunal}/_search"
        query = {"query": {"match": {"numeroProcesso": numero}}, "size": 10}
        
        print("=== DRY RUN ===")
        print(f"URL: {url}")
        print(f"Headers: {client._headers()}")
        print(f"Payload: {query}")
        sys.exit(0)
    
    # Executa comando
    commands = {
        "consultar": cmd_consultar,
        "buscar": cmd_buscar,
        "monitor-add": cmd_monitor_add,
        "monitor-remove": cmd_monitor_remove,
        "monitor-check": cmd_monitor_check,
        "monitor-list": cmd_monitor_list,
        "inferir": cmd_inferir,
    }
    
    commands[args.comando](args, client)


if __name__ == "__main__":
    main()
