# Perfis Completos dos Agentes — ORBIT

## 1. ORQUESTRADOR
- **Missão:** Interpretar intenção, distribuir trabalho, aplicar quality gates
- **Input:** Texto do comando do usuário
- **Output:** orchestration_result (JSON)
- **Ferramentas:** handoffs para todos os agentes
- **Limites:** Não pesquisa diretamente, não gera conteúdo final
- **Tracing:** Registra cada handoff via log_trace RPC

## 2. PESQUISA WEB
- **Missão:** Buscar fontes reais e montar evidence matrix
- **Input:** Tema ou pergunta de pesquisa
- **Output:** research_result (JSON)
- **Ferramentas:** web_search_preview (nativa OpenAI)
- **Quality Gate:** ≥ 5 fontes distintas; ≥ 3 ângulos cobertos; cobertura estimada ≥ 60%
- **Persist:** research_reports + research_sources + evidence_store

## 3. PESQUISA SOCIAL
- **Missão:** Capturar percepção pública (Reddit, fóruns)
- **Input:** Tema ou questão social
- **Output:** social_research_result (JSON)
- **Ferramentas:** web_search_preview focada em Reddit/fóruns
- **Quality Gate:** ≥ 3 comunidades/discussões distintas
- **Camada:** Complementar, não substitui pesquisa web

## 4. PESQUISA ACADÊMICA
- **Missão:** Buscar papers, DOI, referencias robustas
- **Input:** Tema ou pergunta
- **Output:** scholarly_research_result (JSON)
- **Ferramentas:** web_search_preview + OpenAlex API (https://api.openalex.org/works?search=)
- **Quality Gate:** ≥ 3 referências com DOI verificável
- **Campos no research_sources:** doi, citation_count, publication_year, authors, institution

## 5. ANÁLISE
- **Missão:** Cruzar evidências, gerar análise profunda
- **Input:** research_result + social_research_result + scholarly_research_result
- **Output:** analysis_result (JSON com 7 campos obrigatórios)
- **Quality Gate:** Todos os 5 elementos presentes: convergências, divergências, gaps, SWOT, implicações
- **Regra crítica:** Diferenciar explicitamente fato / inferência / opinião
- **Score confiança:** 0-10 baseado na qualidade e quantidade das evidências

## 6. CRIADOR DE DOSSIÊS
- **Missão:** Transformar análise em documento estruturado profissional
- **Input:** analysis_result
- **Output:** dossier_result (JSON + Markdown)
- **Ferramentas:** file_search (documentos anteriores como referência)
- **Quality Gate:** ≥ 800 palavras; todas as seções: resumo_executivo, secoes[], conclusao, recomendacoes
- **Persist:** dossiers + dossier_sources

## 7. CRIADOR DE APRESENTAÇÕES
- **Missão:** HTML premium autocontido a partir do dossiê
- **Input:** dossier_result
- **Output:** presentation_result com html_content completo
- **Regras do HTML:**
  - Sem dependências externas (sem CDN, sem googleapis)
  - Todos os estilos inline ou em <style> interno
  - Responsivo (mobile, tablet, desktop)
  - Seções obrigatórias: hero, highlights, sections, swot_visual, sources_panel, conclusao
  - Tema: dark premium (#0f0f1a, #6366f1, #818cf8)
- **Quality Gate:** Todas as seções, SWOT visual 2x2, leiturabilidade
- **Persist:** presentations

## 8. REVISOR DE QUALIDADE
- **Missão:** Validar qualquer output antes da entrega
- **Input:** output de qualquer agente + tipo do artifact
- **Output:** quality_review_result com scores por dimensão
- **Scoring (0-10 cada):**
  - completude: todas as seções obrigatórias presentes?
  - profundidade: nível de detalhe é suficiente?
  - coerencia: o documento é internamente consistente?
  - formatacao: estrutura e legibilidade
  - fontes: fontes verificáveis e diversificadas?
- **Score geral mínimo: 7.0**
- **Se reprovado:** registra agente_para_retry e problemas específicos
- **Persist:** quality_evaluations + quality_gates
- **Não corrige diretamente:** sinaliza e solicita retry ao agente responsável
