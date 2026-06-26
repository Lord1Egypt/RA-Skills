---
name: institutional-site
description: >
  Cria sites institucionais profissionais em React (Vite + TypeScript + Tailwind CSS 4)
  a partir de materiais de referência do cliente (logos, imagens, apresentações, PDFs, identidade visual).
  Use esta skill SEMPRE que o usuário quiser criar um site, landing page, página institucional,
  site de produto, ou one-pager web. Também deve disparar quando o usuário mencionar "site React",
  "landing page", "página web", "site institucional", "site de produto", "criar site",
  "montar website", ou fornecer materiais visuais (logos, paleta de cores, apresentações)
  pedindo para transformar em site. Serve tanto para sites em português quanto inglês.
  Se o usuário tiver uma pasta com materiais de referência (imagens, logos, PDFs, PPTs),
  esta skill sabe como organizar e transformar tudo em um site de alta qualidade.
---

# Institutional Site Builder

Skill especializada em criar sites institucionais de alta qualidade a partir de materiais
de referência do cliente. O workflow é projetado para extrair o máximo dos materiais fornecidos
(logos, identidade visual, apresentações, PDFs) e transformá-los em um site React profissional
com animações, responsividade e performance otimizada.

## Stack Tecnológico

O projeto SEMPRE usa:
- **Vite** (v6+) como bundler
- **React 19** + **TypeScript**
- **Tailwind CSS 4** via `@tailwindcss/vite`
- **Framer Motion** para animações
- **Lucide React** para ícones

Dependências opcionais (instalar conforme necessidade):
- `three` + `@types/three` — backgrounds 3D animados (DottedSurface, shader backgrounds)
- `react-use-measure` — para o InfiniteSlider (logo cloud, marquee)

## Workflow em 6 Fases

### Fase 1: Exploração e Inventário de Materiais

Antes de escrever qualquer código, explore TUDO que o usuário forneceu. Esta fase é crítica
porque os materiais definem o tom, as cores, o conteúdo e as imagens do site.

**Organize os materiais em categorias mentais:**

| Categoria | O que procurar | Como usar |
|-----------|---------------|-----------|
| **Identidade Visual** | Paleta de cores (hex), tipografia, guidelines | Define `@theme` no CSS, cores de accent, gradientes |
| **Logos** | Variantes claro/escuro, horizontal/vertical, SVG/PNG | Navbar (horizontal, claro), Footer (horizontal, claro), Favicon (ícone escuro) |
| **Imagens de Produto** | Screenshots, mockups, fotos operacionais | Feature cards, hero background, timeline, scroll media |
| **Apresentações** | PPTs, PDFs com slides | EXTRAIR textos, headlines, bullet points, estrutura de seções |
| **Componentes UI** | Arquivos .txt com código React de referência | Adaptar para o projeto (remover deps de shadcn, Next.js) |
| **Dados de Contato** | E-mails, telefones, redes sociais, endereços | Footer, seção contato, WhatsApp flutuante |
| **Logos de Clientes** | Logos de empresas parceiras/clientes | Seção de social proof com InfiniteSlider |

**Checklist de exploração:**
1. `ls -la` recursivo em toda a pasta do usuário
2. Ler TODAS as imagens com o Read tool (logos, identidade visual, slides-chave)
3. Ler PDFs/PPTs para extrair conteúdo textual
4. Identificar paleta de cores exata (hex codes)
5. Mapear quais imagens servem para quais seções
6. Anotar dados de contato, nomes de produtos, taglines

### Fase 2: Planejamento do Site

Após inventariar, pergunte ao usuário usando AskUserQuestion:

1. **Idioma** — PT-BR, EN, ou bilíngue?
2. **Seções** — Completo (Hero, Problema, Solução, Features, Benefícios, Clientes, CTA, Contato, Footer) ou simplificado?
3. **Estilo visual** — Dark premium, Light/clean, ou Híbrido?
4. **Contato** — Formulário + WhatsApp, apenas links, ou formulário completo?

A maioria dos sites institucionais B2B segue esta ordem de seções (ajustar conforme necessidade):

```
1. Navbar (fixa, com blur no scroll)
2. Hero (proposta de valor + CTA)
3. Contexto/Problema (por que o produto existe)
4. Solução (o que o produto faz)
5. Pipeline/Processo (como funciona, passo a passo)
6. Funcionalidades (feature cards com imagens)
7. Detalhes técnicos (IoT, integrações, etc.)
8. Benefícios (cards por categoria)
9. Canais de Entrega (integrações multicanal)
10. Clientes (logo cloud com social proof) ← antes do CTA
11. CTA Final (frase de impacto + botão)
12. Contato (formulário + dados)
13. Footer (links, logo, copyright)
14. WhatsApp Flutuante
```

### Fase 3: Setup do Projeto

```bash
npm create vite@latest <nome-site> -- --template react-ts
cd <nome-site>
npm install
npm install -D tailwindcss @tailwindcss/vite --legacy-peer-deps
npm install framer-motion lucide-react
```

**Configurar `vite.config.ts`:**
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          // Adicionar conforme libs pesadas são usadas
          'framer-motion': ['framer-motion'],
        },
      },
    },
  },
})
```

**Configurar `src/index.css` com a paleta do cliente:**
```css
@import "tailwindcss";

@theme {
  /* Cores extraídas da identidade visual do cliente */
  --color-primary-900: #XXXXXX;
  --color-primary-800: #XXXXXX;
  /* ... mapear toda a paleta ... */
  --color-accent: #XXXXXX;
  --font-sans: 'Inter', system-ui, sans-serif;
}
```

**Configurar `index.html`:**
- `lang` correto (pt-BR ou en)
- Meta description com o produto
- Google Fonts com defer (NÃO render-blocking):
  ```html
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" />
  <link href="..." rel="stylesheet" media="print" onload="this.media='all'" />
  ```

**Copiar assets:**
- Criar `public/images/` e copiar todas as imagens do produto
- Criar `public/images/clientes/` se houver logos de clientes
- Copiar logos (preferir variante horizontal para navbar)

### Fase 4: Construção do Site

Construir o site inteiro em um único `App.tsx` (para sites de até ~800 linhas).
Para sites maiores, criar componentes em `src/components/`.

**Padrões obrigatórios em TODAS as imagens:**
```tsx
<img src="..." alt="Descrição" width={N} height={N} loading="lazy" />
```

**Componentes utilitários a incluir:**
- `useInView()` — Intersection Observer para animações de entrada
- `Section` — wrapper que anima opacity+translateY no scroll
- `TextCycle` — texto que alterna entre palavras com animação slideUp

**Para cada seção, consultar `references/components.md`** que contém templates
prontos adaptados para o stack (sem dependências de shadcn, Next.js, ou cn()).

### Fase 5: Otimização de Performance (OBRIGATÓRIA)

Esta fase é executada ANTES de entregar o site ao usuário.

**5.1 Imagens — Converter para WebP:**
```python
from PIL import Image
import glob, os
for f in glob.glob("public/images/*.png") + glob.glob("public/images/*.jpg"):
    if os.path.getsize(f) > 100_000:
        img = Image.open(f)
        if img.width > 1200:
            ratio = 1200 / img.width
            img = img.resize((1200, int(img.height * ratio)), Image.LANCZOS)
        img.save(f.rsplit('.', 1)[0] + '.webp', 'WEBP', quality=80)
```
Atualizar todas as referências no código para .webp.

**5.2 Fontes — Eliminar render-blocking:**
Usar o pattern `media="print" onload="this.media='all'"` no index.html.

**5.3 JavaScript — Code splitting:**
- Libs pesadas (Three.js) em lazy import + Suspense
- manualChunks no vite.config.ts
- O bundle JS principal deve ficar abaixo de 300KB

**5.4 Acessibilidade mínima:**
- `role="main"` no container principal
- `alt` em todas as imagens
- `width` e `height` explícitos em todas as `<img>`
- Headings em ordem sequencial (h1 → h2 → h3)
- Contraste suficiente entre texto e fundo

**5.5 SEO básico:**
- `<title>` descritivo
- `<meta name="description">` com o produto
- `lang` correto no `<html>`

### Fase 6: Entrega

1. Fazer `npm run build` e verificar que compila sem erros
2. Copiar o projeto completo para a pasta do usuário
3. Apresentar link `computer:///path/to/project`
4. Instruir: `cd nome-site && npm install && npm run dev`

## Referências

- `references/components.md` — Catálogo completo dos 23 componentes com tabela por categoria, cheat sheet de adaptação Next.js→Vite, e templates inline prontos
- `references/components/` — Os 23 arquivos .txt originais com código TSX completo, demo e dependências de cada componente
- `references/patterns.md` — Padrões de CSS, animações, glass morphism, gradients, otimização de imagens

### Componentes Disponíveis (31 — 23 originais + 8 do 21st.dev)

**Heroes:** Glassmorphism Trust Hero, 3D Hero (Spline), Scroll Expand Media
**Backgrounds:** Animated Shader (GLSL Aurora), Flow Field (Canvas 2D), Dotted Surface (Three.js)
**Navigation:** Tubelight Navbar, Limelight Nav (dark mode)
**Cards:** Glowing Effect Border, Bauhaus Card, Bento Grid
**Content:** Timeline (scroll-based), Vertical Tabs, DB/API Diagram, Global Map, Logo Cloud (InfiniteSlider)
**Animations:** Text Cycle, Loading Skeleton, Container Scroll 3D, Notification Alert
**Utility:** Page 404, Footer, Password Confirmation

**21st.dev Extras:** Starfall Portfolio Landing, Parallax Feature Section, Metaball Hero, Rotating Prompts, Collapsible Header, Image Card, Spotlight, Accordion

Para usar qualquer componente, leia `references/components.md` para o catálogo e depois
leia o `.txt` correspondente em `references/components/` (originais) ou `references/components/21st-dev/` (extras).

Para buscar mais componentes do 21st.dev, use a API: `POST /api/prompts` com `{"prompt_type":"extended","demo_id":<ID>}`. Ver instruções completas em `references/components.md`.

## Organização de Pasta Esperada do Usuário

Quando o usuário fornecer materiais, a skill espera (ou sugere) esta organização:

```
materiais-projeto/
├── logos/              ← Variantes do logo (claro, escuro, horizontal, vertical)
├── identidade-visual/  ← Paleta de cores, guidelines, tipografia
├── imagens/            ← Fotos, screenshots, mockups do produto
├── apresentacoes/      ← PPTs, PDFs com conteúdo do produto
├── clientes/           ← Logos de empresas clientes/parceiras
├── components/         ← Componentes UI de referência (.txt com código React)
└── copy/               ← Textos, taglines, descrições (se houver separado)
```

Se os materiais estiverem desorganizados, a skill navega e cataloga tudo mesmo assim.
Mas se o usuário perguntar "como organizar?", sugira esta estrutura.
