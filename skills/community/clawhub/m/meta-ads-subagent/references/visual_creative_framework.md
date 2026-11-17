# Framework de Criativos Visuais de Alta Conversão para SaaS / APIs de IA

Este guia documenta o padrão de design e composição visual para criativos de anúncios no Meta Ads (Feed 1080x1080) voltados a produtos B2B, APIs de mensageria e soluções de IA.

---

## 1. Padrão "Visual Flow 3-Etapas" (Cliente ➔ IA ➔ Vendas/Receita)

Em produtos de IA conversacional e agentes de voz/atendimento, uma das composições de mais alta conversão é o **Fluxo Narrativo em 3 Colunas Conectadas**:

```
+-------------------+      +-------------------+      +-------------------+
|  1. CLIENTE (HUMANO)| ---> |  2. AGENTE DE IA  | ---> |  3. EMPRESA/LUCRO |
| (Mulher/Homem com |      | (Orbe Neural /    |      | (Notificações Pix,|
|  celular na mão)  |      |  Ondas de Áudio)  |      |  Faturamento $$$) |
+-------------------+      +-------------------+      +-------------------+
```

### Por que funciona?
- **Tangibilização Instantânea:** O lead entende o funcionamento do produto em menos de 2 segundos.
- **Conexão com o Resultado Financeiro:** A ponta final sempre mostra dinheiro entrando (Pix, faturamento, conversão 24/7), focando no benefício e não apenas na tecnologia.
- **Humanização:** Usar uma foto real de alta qualidade na primeira etapa retira a sensação fria de "robô".

---

## 2. Estrutura de Design HTML/CSS (1080x1080) & Safe-Margins

Ao renderizar criativos via Playwright / Chrome Headless (`viewport: 1080x1080`):

1. **Regra de Ouro: Safe Margins Anti-Corte (60px a 80px):**
   - Nunca posicione textos ou botões colados nas bordas do canvas 1080x1080.
   - Use `padding: 60px 60px;` no container principal com `box-sizing: border-box`.
   - Layout estritamente baseado em `flexbox` ou `CSS Grid` para garantir fluxo dinâmico sem quebra manual de linhas arriscada.
   - Tipografia moderna (Google Fonts: Inter, Plus Jakarta Sans) com `line-height: 1.15` a `1.3`.

2. **Header & Identidade Visual:**
   - **Logotipo Oficial da Marca:** Sempre renderize o vetor SVG oficial da marca em alta resolução no topo com badge de autenticidade/verificação.
   - Badges de ancoragem de preço destacados (ex: `R$ 14,90/mês` | `Voz com IA: a partir de R$ 49,90/mês`).

3. **Fundos Futuristas & Cyberpunk Tech para IA e SaaS:**
   - Fundo *dark obsidian* (`#030712` / `#090d16`) com malha geométrica sutil (`linear-gradient` com grid de 40px).
   - Esferas radiais de luz neon (*glow blurs* com `filter: blur(80px)`) em tons Verde WhatsApp (`#25D366`), Ciano Elétrico (`#00f2fe`) e Roxo Neural (`#8b5cf6`).
   - Cards em *glassmorphism* (`background: rgba(255,255,255,0.03)`, `backdrop-filter: blur(16px)`, `border: 1px solid rgba(255,255,255,0.1)`).
   - Visualizadores de voz: HUD de ligação ativa (`00:24 • IA Conectada • Latência < 500ms`) e barras de ondas sonoras (*soundwaves*) neon. Chamada no WhatsApp`).
   - **Coluna 2 (Processamento):** Orbe neural centralizado, ondas de frequência de voz, badge de latência em tempo real (`⚡ 280ms`) e tags de integrações.
   - **Coluna 3 (Destino/Lucro):** Prédio/escritório corporativo moderno com badges flutuantes de faturamento (`💸 +R$ 1.850,00`, `💰 VENDAS 24H`) e métrica de conversão (`+340% 📈`).
   - **Conectores:** Setas visuais em SVG entre as colunas guiando o olhar do usuário.
4. **Live Transcript Banner:**
   - Uma barra horizontal fina simulando a fala da IA em tempo real com confirmação de venda ou agendamento.
5. **Footer / CTA:**
   - Preço de entrada em destaque dourado/amarelo (`JetBrains Mono`, 32px).
   - Botão de Ação chamativo (Verde Esmeralda ou Ciano).

---

## 3. Template HTML Base

O template completo testado e aprovado está disponível em:
`/root/papi_creatives/creative3_ai_voice_flow.html`
