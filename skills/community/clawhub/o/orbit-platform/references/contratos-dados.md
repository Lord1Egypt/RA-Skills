# Contratos de Dados — ORBIT

## orchestration_result
```json
{
  "job_id": "uuid",
  "intent": "string — intenção interpretada",
  "plan": ["passo 1", "passo 2"],
  "agents_triggered": ["research", "analysis", "dossier"],
  "status": "pending|running|completed|failed",
  "final_output_ref": "uuid do artifact final",
  "metadata": {
    "started_at": "ISO timestamp",
    "completed_at": "ISO timestamp",
    "total_tokens": 1500
  }
}
```

## research_result
```json
{
  "query": "string",
  "subconsultas": ["string"],
  "fontes": [{
    "url": "string",
    "titulo": "string",
    "trecho": "string",
    "relevancia": "alta|média|baixa",
    "data": "string",
    "conflito": false
  }],
  "cobertura": 75,
  "conflitos_detectados": ["string"],
  "total_fontes": 8
}
```

## social_research_result
```json
{
  "query": "string",
  "plataformas_consultadas": ["Reddit"],
  "discussoes": [{
    "plataforma": "Reddit",
    "url": "string",
    "resumo": "string",
    "sentimento": "positivo|negativo|neutro|misto",
    "engajamento": "alto|médio|baixo"
  }],
  "sentimento_geral": "string",
  "temas_recorrentes": ["string"]
}
```

## scholarly_research_result
```json
{
  "query": "string",
  "referencias": [{
    "titulo": "string",
    "autores": ["string"],
    "ano": 2024,
    "doi": "string",
    "fonte": "OpenAlex",
    "abstract": "string",
    "relevancia": "alta|média|baixa"
  }],
  "total_referencias": 4
}
```

## analysis_result
```json
{
  "tema": "string",
  "convergencias": ["string"],
  "divergencias": ["string"],
  "gaps": ["string"],
  "implicacoes": ["string"],
  "swot": {
    "forcas": ["string"],
    "fraquezas": ["string"],
    "oportunidades": ["string"],
    "ameacas": ["string"]
  },
  "fatos_verificados": ["string"],
  "inferencias": ["string"],
  "opiniao": ["string"],
  "score_confianca": 8
}
```

## dossier_result
```json
{
  "titulo": "string",
  "data_geracao": "ISO timestamp",
  "resumo_executivo": "string (200-400 palavras)",
  "secoes": [{
    "titulo": "string",
    "conteudo": "string (markdown)"
  }],
  "conclusao": "string (100-200 palavras)",
  "recomendacoes": ["string"],
  "fontes_utilizadas": ["URL ou referência"],
  "total_palavras": 1200
}
```

## presentation_result
```json
{
  "titulo": "string",
  "html_content": "string (HTML completo autocontido)",
  "arquivo_path": "string (Supabase Storage)",
  "secoes_incluidas": ["hero", "highlights", "swot", "timeline", "fontes", "conclusao"],
  "responsivo": true,
  "data_geracao": "ISO timestamp"
}
```

## quality_review_result
```json
{
  "artifact_id": "uuid",
  "artifact_tipo": "research|analysis|dossier|presentation",
  "status": "aprovado|reprovado",
  "scores": {
    "completude": 8,
    "profundidade": 7,
    "coerencia": 9,
    "formatacao": 8,
    "fontes": 7
  },
  "score_geral": 7.8,
  "problemas_encontrados": ["string"],
  "recomendacoes": ["string"],
  "requer_retry": false,
  "agente_para_retry": null
}
```
