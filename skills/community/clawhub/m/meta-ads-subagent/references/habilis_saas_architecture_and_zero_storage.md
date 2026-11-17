# Habilis SaaS MCP Gateway & Zero-Storage Architecture Guide

## 1. Definição e Diferenciação Crítica de Escopo
- **Habilis (`/home/orca/orca/habilis`)**: É a plataforma de inteligência e automação MCP Gateway & Web Dashboard construído em Next.js / TypeScript, servido na porta `3080` (`http://localhost:3080` / `https://xvix.com.br`) e gerenciado pelo serviço `habilis.service`.
  - Destinado a **clientes externos e assinantes** que conectam agentes (Claude Desktop, Cursor, Hermes, n8n) ao Meta Ads, OpenAI Ads, PAPI e outros provedores.
- **Skills Internas do Hermes (`~/.hermes/skills/`)**: São os módulos procedurais do assistente Hermes para execução de tarefas locais e automações do usuário.
- **Regra de Não-Confusão**: Quando o usuário instruir mudanças ou novas funcionalidades no "Habilis", o escopo é estritamente a aplicação web e backend do Habilis (`/home/orca/orca/habilis`), e NÃO a criação ou modificação de skills do Hermes no ambiente local.

---

## 2. Princípio de Zero-Storage & Privacidade Client-Side
- Ao construir ou estender fluxos de Onboarding, parametrização ou exportação de credenciais no frontend do Habilis (`src/components/SkillDownloaderModal.tsx`, `src/lib/onboarding-schema.ts`, etc.):
  1. **Zero Persistência no Backend**: Tokens de acesso, senhas de API, IDs de conta de anúncios, Pixels e Page IDs digitados pelos clientes **NUNCA** devem ser gravados no banco de dados (`data/habilis_db.json`), SQLite, logs ou arquivos no servidor.
  2. **Processamento In-Memory**: O formulário opera exclusivamente em memória volátil do navegador via React State (`useState`).
  3. **Interpolação em Tempo Real**: Os snippets de código (`claude_desktop_config.json`, `.cursor/mcp.json`, comandos cURL, CLI do Hermes) e arquivos para download (`SKILL.md`, `.env`) são gerados client-side utilizando `Blob` e URLs temporárias (`URL.createObjectURL`), sendo liberados imediatamente após o download (`URL.revokeObjectURL`).
  4. **Avisos Transparentes de Segurança**: A interface do modal deve sempre exibir badges e alertas claros de privacidade (`🔒 Zero-Storage Guarantee`) para gerar confiança nos assinantes do SaaS.

---

## 3. Ciclo de Build e Deploy do Habilis
Após qualquer alteração nos componentes, rotas ou esquemas do Habilis:
1. **Validar Build**:
   ```bash
   cd /home/orca/orca/habilis && npm run build
   ```
2. **Reiniciar Serviço**:
   ```bash
   systemctl restart habilis
   ```
3. **Verificar Integridade HTTP**:
   ```bash
   curl -I http://localhost:3080
   ```
