---
name: "progress-report"
description: "Transforma notas diárias e atividades em relatórios de progresso profissionais (semanal, mensal ou executivo)."
metadata:
  - report
  - productivity
  - business
  - management
  - writing
  - career
allowed-tools:
  - read
  - write
  - memory_search
  - memory_get
user-invocable: true
---

# Progress Report Generator 📈✍️

Transforma anotações soltas, bullets e lembretes em relatórios de progresso profissionais, prontos para enviar para seu chefe, cliente ou equipe.

## Público-Alvo

Profissionais CLT, estagiários, trainees, freelancers, PJs, gerentes de projeto — qualquer um que precise reportar seu progresso regularmente.

## Trigger

Invocar quando o usuário:
- Pedir "gerar relatório de progresso"
- Falar "relatório semanal/mensal"
- Pedir "status report"
- Dizer "preciso reportar o que fiz essa semana"
- Enviar uma lista de atividades

## Diferenciais

1. **3 estilos de relatório** — Semanal (detalhado), Mensal (estratégico) e Executivo (pitch de 5 linhas).
2. **De notas para linguagem profissional** — Aceita frases soltas ("terminei o layout", "reunião com cliente X") e expande em linguagem corporativa.
3. **Destaque automático de entregas** — Identifica o que é "entrega" vs "tarefa corriqueira" e destaca as entregas.
4. **Geração de Next Steps** — Com base nas atividades, sugere automaticamente os próximos passos.
5. **Templates por papel** — Estilos otimizados para: Dev, Designer, Marketing, Vendas, Gerente, Estagiário, Freelancer.
6. **Tonalidade ajustável** — Formal (corporativo), Casual (startup), Técnico (dev/engenharia).
7. **Memória de relatórios anteriores** — Se usado com frequência, consulta relatórios passados pra não repetir e mostrar evolução.

## Workflow

### Passo 1: Coletar entradas

O usuário pode fornecer:

**Notas soltas:**
```
- terminei o novo layout do site
- reunião com cliente sobre orçamento
- corrigi 3 bugs no sistema
- apresentei proposta pra João
- fiz code review do PR #42
```

**Lista de tarefas concluídas:**
```
✅ Layout site — Concluído
✅ Correção bugs — 3 resolvidos
✅ Reunião cliente orçamento — OK
✅ Code review PR #42 — Aprovado
```

**Pode ser vazio (perguntar passo a passo):**
Nesse caso, a skill pergunta: "O que você fez? Pode mandar uma lista simples."

### Passo 2: Escolher o estilo

| Estilo | Ideal pra... | Tamanho |
|--------|-------------|---------|
| **Semanal** | Estágio, CLT, freelancer com cliente | Médio (10-15 linhas) |
| **Mensal** | Gerente, coordenação, resultados | Longo (15-25 linhas) |
| **Executivo** | Pitch rápido, reunião de alinhamento | Curto (5-8 linhas) |

Se o usuário não especificar, perguntar: "Semanal, mensal ou executivo?"

### Passo 3: Escolher papel (opcional)

Perguntar se quer template para um papel específico. Se o usuário não sabe, detectar automaticamente pelo contexto.

| Papel | Foco do relatório |
|-------|------------------|
| 💻 Dev | Features entregues, bugs corrigidos, PRs, débito técnico |
| 🎨 Designer | Entregas visuais, protótipos, feedbacks, revisões |
| 📢 Marketing | Campanhas, métricas, conteúdo, redes sociais |
| 💰 Vendas | Leads, reuniões, propostas, fechamentos |
| 👔 Gerente | Equipe, entregas do time, riscos, decisões |
| 📚 Estagiário | Aprendizados, tarefas, mentorias, dúvidas |
| 🔧 Freelancer | Projetos, entregas, prazos, faturamento |

### Passo 4: Gerar relatório

#### Modelo Semanal (para WhatsApp)

```
📈 *RELATÓRIO SEMANAL*
👤 [Nome] | 📅 Semana de [data]
🎯 Papel: [papel]

✅ *Entregas*
• Layout do site finalizado — versão responsiva aprovada pelo cliente
• 3 bugs críticos corrigidos no módulo de pagamentos
• Proposta comercial apresentada para João (empresa X)
• Code review do PR #42 aprovado e mergeado

📋 *Tarefas em Andamento*
• Integração com gateway de pagamento (70%)
• Documentação técnica do módulo de usuários

📌 *Próximos Passos*
• Finalizar integração com gateway (prazo: 18/06)
• Iniciar testes de carga
• Reunião com cliente Y para alinhamento

⚠️ *Impedimentos*
• Aguardando acesso ao servidor de homologação
```

#### Modelo Executivo (5 linhas)

```
📈 *STATUS EXECUTIVO — Semana [data]*
• 💥 Entregue: Layout do site finalizado, 3 bugs críticos corrigidos, proposta apresentada
• 🔄 Andamento: Integração gateway (70%), docs
• 🎯 Próximo: Finalizar gateway + testes de carga
• ⚠️ Bloqueio: Acesso ao servidor de homologação pendente
```

## Regras de Formatação

- **Entregas:** sempre começam com verbo no passado (finalizei, corrigi, apresentei). A skill deve transformar "layout" em "Layout do site finalizado".
- **Próximos passos:** sempre com prazo quando possível.
- **Impedimentos:** destacar com ⚠️ e manter visível.
- **Tonalidade técnica:** usar linguagem específica da área (PR, deploy, merge, protótipo, lead, etc.)
- **Se for primeiro relatório do usuário:** perguntar preferências de estilo e salvar em memória.

## Notes

- Se o usuário não especificar período, considerar a semana atual (segunda a domingo).
- Se as notas forem muito vagas ("fiz coisas"), perguntar especificamente: "Pode dar mais detalhes do que fez?"
- Para freelancers, incluir campo de horas trabalhadas se informado.
- Se houver relatório anterior (memória), comparar e destacar progresso.
- WhatsApp-friendly: bullet lists, sem tabelas markdown.

---
⭐ *Gostou desta skill?* Deixe uma estrela no [ClawHub](https://clawhub.ai) para ajudar outros a encontrá-la!
