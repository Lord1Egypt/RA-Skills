#!/usr/bin/env python3
"""
DataJud Client - Consulta processos judiciais via API Pública do CNJ
"""
import os
import sys
import json
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional

# Configuração
BASE_URL = "https://api-publica.datajud.cnj.jus.br"
DEFAULT_API_KEY = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="

class DataJudClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("DATAJUD_API_KEY", DEFAULT_API_KEY)
        self.last_request_time = 0
        self.min_interval = 0.5  # 2 req/s max
    
    def _headers(self) -> dict:
        return {
            "Authorization": f"APIKey {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _rate_limit(self):
        """Rate limiting - mínimo 0.5s entre requisições"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_request_time = time.time()
    
    def _request(self, method: str, url: str, data: Optional[dict] = None, 
                 retry: int = 3) -> Optional[dict]:
        self._rate_limit()
        
        body = json.dumps(data).encode() if data else None
        req = urllib.request.Request(url, data=body, headers=self._headers(), method=method)
        
        for attempt in range(retry):
            try:
                with urllib.request.urlopen(req, timeout=30) as response:
                    return json.loads(response.read().decode())
            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt < retry - 1:
                    time.sleep(2 ** attempt)  # Backoff exponencial
                    continue
                elif e.code >= 500 and attempt < retry - 1:
                    time.sleep(2 ** attempt)
                    continue
                else:
                    raise Exception(f"HTTP {e.code}: {e.read().decode()}")
            except Exception as e:
                if attempt < retry - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise
        
        return None
    
    def consultar(self, numero: str, tribunal: Optional[str] = None, 
                  max_movimentos: int = 50) -> dict:
        """Consulta processo por número CNJ"""
        # Normaliza número CNJ
        numero_normalizado = "".join(c for c in numero if c.isdigit())
        
        if len(numero_normalizado) != 20:
            raise ValueError("Número CNJ deve ter 20 dígitos")
        
        # Infere tribunal se não informado
        if not tribunal:
            from cnj_number import infer_tribunal
            tribunal = infer_tribunal(numero_normalizado)
            if not tribunal:
                raise ValueError("Não foi possível inferir o tribunal. Forneça --tribunal.")
        
        url = f"{BASE_URL}/api_publica_{tribunal}/_search"
        
        query = {
            "query": {"match": {"numeroProcesso": numero_normalizado}},
            "size": 10,
            "sort": [{"movimentos.dataHora": {"order": "desc"}}]
        }
        
        result = self._request("POST", url, query)
        
        if not result or result.get("hits", {}).get("total", {}).get("value", 0) == 0:
            raise ValueError("Processo não encontrado ou sigiloso")
        
        hit = result["hits"]["hits"][0]["_source"]
        
        # Limita movimentos
        movimentos = hit.get("movimentos", [])[:max_movimentos]
        
        return {
            "numero": hit.get("numeroProcesso"),
            "tribunal": tribunal,
            "classe": hit.get("classe", {}).get("descricao"),
            "assuntos": [a.get("descricao") for a in hit.get("assuntos", [])],
            "orgaoJulgador": hit.get("orgaoJulgador", {}).get("descricao"),
            "grau": hit.get("grau"),
            "dataAjuizamento": hit.get("dataAjuizamento"),
            "dataUltimaAtualizacao": hit.get("dataHoraUltimaAtualizacao"),
            "movimentos": movimentos,
            "formato": hit.get("formato"),
            "sigilo": hit.get("sigilo", False)
        }
    
    def buscar(self, tribunal: str, classe: Optional[str] = None,
               orgao: Optional[str] = None, grau: Optional[str] = None,
               ajuizamento_de: Optional[str] = None, ajuizamento_ate: Optional[str] = None,
               parte: Optional[str] = None, size: int = 10) -> dict:
        """Busca processos por filtros"""
        url = f"{BASE_URL}/api_publica_{tribunal}/_search"
        
        must_clauses = []
        
        if parte:
            # Busca por nome de parte (autor, réu, etc)
            # Nota: nem todos os tribunais indexam este campo
            must_clauses.append({
                "match": {
                    "nomeParte": {
                        "query": parte,
                        "fuzziness": "AUTO"
                    }
                }
            })
        
        if classe:
            must_clauses.append({"match": {"classe.codigo": classe}})
        if orgao:
            must_clauses.append({"match": {"orgaoJulgador.codigo": orgao}})
        if grau:
            must_clauses.append({"match": {"grau": grau}})
        
        # Range de data
        if ajuizamento_de or ajuizamento_ate:
            range_dict = {}
            if ajuizamento_de:
                range_dict["gte"] = ajuizamento_de
            if ajuizamento_ate:
                range_dict["lte"] = ajuizamento_ate
            must_clauses.append({"range": {"dataAjuizamento": range_dict}})
        
        query = {"query": {"bool": {"must": must_clauses}}, "size": size}
        
        result = self._request("POST", url, query)
        
        hits = result.get("hits", {}).get("hits", [])
        return {"total": result.get("hits", {}).get("total", {}).get("value", 0), 
                "processos": [h["_source"] for h in hits]}


if __name__ == "__main__":
    from cli import main
    main()
