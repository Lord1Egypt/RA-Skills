# Component Templates

Templates de componentes React para o stack Vite + React + TS + Tailwind CSS 4.

## Biblioteca Completa — 31 Componentes

A skill contém 31 componentes de referência organizados em duas pastas:

- `references/components/*.txt` — 23 componentes originais curados manualmente
- `references/components/21st-dev/*.txt` — 8 componentes extraídos do 21st.dev

Cada arquivo contém o código TSX completo, demo, dependências e instruções de integração.
Ao usar um componente, leia o `.txt` correspondente e adapte para o projeto (remover deps de shadcn, Next.js, cn()).

### Como buscar MAIS componentes do 21st.dev

O site https://21st.dev/community/components possui 500+ componentes React/Tailwind/shadcn.
Para extrair o prompt de qualquer componente via API:

```
POST https://21st.dev/api/prompts
Content-Type: application/json
Body: {"prompt_type": "extended", "demo_id": <ID_DO_COMPONENTE>}
```

O `demo_id` pode ser capturado interceptando o fetch no browser ao clicar "Copy prompt".
Categorias relevantes: Heroes (73), Features (36), Footers (14), Clients (16),
Calls to Action (34), Backgrounds (33), Shaders (15), Testimonials (15),
Scroll Areas (24), Navigation Menus (11), Pricing Sections (17), Texts (58).

### Catálogo por Categoria

#### Heroes & Landing
| # | Arquivo | Componente TSX | Descrição | Deps |
|---|---------|---------------|-----------|------|
| 1 | `glassmorphis_hero.txt` | glassmorphism-trust-hero.tsx | Hero 2 colunas com glass cards, stats, marquee de clientes | lucide-react |
| 2 | `3d_hero - cópia.txt` | 3d-hero-section-boxes.tsx | Hero com cena 3D Spline interativa | @splinetool/react-spline |
| 3 | `scroll_media_expansion.txt` | scroll-expansion-hero.tsx | Imagem/vídeo que expande no scroll com texto split | framer-motion |

#### Backgrounds & Visual Effects
| # | Arquivo | Componente TSX | Descrição | Deps |
|---|---------|---------------|-----------|------|
| 4 | `back_groun.txt` | animated-shader-background.tsx | Background animado com shaders GLSL (aurora) | three |
| 5 | `background_flow_fluid.txt` | flow-field-background.tsx | Campo de fluxo fluido animado (Canvas 2D) | nenhuma |
| 6 | `dotted_surface.txt` | dotted-surface.tsx | Superfície de partículas 3D ondulantes | three |

#### Navigation
| # | Arquivo | Componente TSX | Descrição | Deps |
|---|---------|---------------|-----------|------|
| 7 | `nav_bar.txt` | tubelight-navbar.tsx | Navbar com efeito tubelight no item ativo | lucide-react, framer-motion |
| 8 | `menu_dark_mode.txt` | limelight-nav.tsx | Menu com toggle dark/light mode | nenhuma (SVG inline) |

#### Cards & Grids
| # | Arquivo | Componente TSX | Descrição | Deps |
|---|---------|---------------|-----------|------|
| 9 | `border_glow_animation_buton_cards.txt` | glowing-effect.tsx | Cards com efeito de borda brilhante que segue o mouse | motion |
| 10 | `card_animado.txt` | bauhaus-card.tsx | Cards estilo Bauhaus com animações de sombra | nenhuma (CSS) |
| 11 | `grid.txt` | bento-grid.tsx | Grid estilo Bento com layout assimétrico | class-variance-authority |

#### Content & Sections
| # | Arquivo | Componente TSX | Descrição | Deps |
|---|---------|---------------|-----------|------|
| 12 | `timeline.txt` | release-time-line.tsx | Timeline scroll-based com cards expansíveis | lucide-react |
| 13 | `vertical_tab.txt` | vertical-tabs.tsx | Tabs verticais com auto-play e imagem animada | motion, @hugeicons |
| 14 | `processo_comunicacao.txt` | database-with-rest-api.tsx | Diagrama animado de comunicação DB/API/frontend | motion, lucide-react |
| 15 | `map_global_connect_everitinh.txt` | map.tsx | Mapa global com pontos de conexão animados | dotted-map, framer-motion |
| 16 | `logo_cloud.txt` | logo-cloud-3.tsx | Logo cloud com InfiniteSlider (marquee) | framer-motion, react-use-measure |

#### Animations & Micro-interactions
| # | Arquivo | Componente TSX | Descrição | Deps |
|---|---------|---------------|-----------|------|
| 17 | `animate_text_cycle.txt` | animated-text-cycle.tsx | Texto que alterna entre palavras com animação | framer-motion |
| 18 | `animate_loading.txt` | animated-loading-skeleton.tsx | Skeleton loading com shimmer animado | framer-motion |
| 19 | `scroll_animation.txt` | container-scroll-animation.tsx | Container com parallax/rotação 3D no scroll | framer-motion |
| 20 | `notification_alert.txt` | notification-alert-dialog.tsx | Dialog de notificação/alerta com animações | lucide-react, @radix-ui |

#### Utility Pages
| # | Arquivo | Componente TSX | Descrição | Deps |
|---|---------|---------------|-----------|------|
| 21 | `pageNOtFound.txt` | page-not-found.tsx | Página 404 com animação de partículas | nenhuma (Web Animations API) |
| 22 | `footer.txt` | footer-section.tsx | Footer completo com links, newsletter, social | motion, lucide-react |
| 23 | `assistance_password_comparation.txt` | assisted-password-confirmation.tsx | Input de senha com validação visual animada | framer-motion |

#### 21st.dev — Componentes Extra (em `21st-dev/`)
| # | Arquivo | Componente TSX | Descrição | Deps |
|---|---------|---------------|-----------|------|
| 24 | `starfall-portfolio-landing.txt` | starfall-portfolio-landing.tsx | Hero portfolio com animação starfall e cards de projetos | framer-motion |
| 25 | `parallax-scroll-feature-section.txt` | parallax-scroll-feature-section.tsx | Seção de features com efeito parallax no scroll | framer-motion |
| 26 | `meta-ball-hero.txt` | meta-ball-hero.tsx | Hero com efeito metaball animado (canvas/WebGL) | nenhuma |
| 27 | `rotating-prompts.txt` | rotating-prompts.tsx | Texto rotativo com prompts animados (typewriter) | framer-motion |
| 28 | `collapsible-header.txt` | collapsible-header.tsx | Header que colapsa/expande conforme scroll | framer-motion |
| 29 | `image-card-1.txt` | image-card-1.tsx | Cards de imagem com hover effects e metadata | shadcn |
| 30 | `spotlight.txt` | spotlight.tsx | Efeito spotlight que segue o mouse no hover | nenhuma (CSS) |
| 31 | `accordion.txt` | accordion.tsx | Accordion animado com transições suaves | @radix-ui |

### Como Usar

1. Identifique qual componente serve para a seção que está construindo
2. Leia o arquivo `.txt` com `Read tool` em `references/components/<nome>.txt`
3. Extraia o código TSX e adapte:
   - Remover `"use client"` (não é Next.js)
   - Substituir `import { cn } from "@/lib/utils"` por template literals
   - Substituir `import Image from "next/image"` por `<img>` com width/height/loading="lazy"
   - Substituir `import Link from "next/link"` por `<a href>`
   - Substituir `useTheme()` (next-themes) por prop ou state local
   - Substituir `@radix-ui/react-slot` por componentes nativos quando possível
4. Ajustar cores e textos para a paleta do projeto
5. Instalar dependências faltantes (`npm install <dep>`)

### Adaptação Rápida — Cheat Sheet

| De (Next.js/shadcn) | Para (Vite/React puro) |
|---------------------|----------------------|
| `"use client"` | remover |
| `cn(a, b)` | `` `${a} ${b}` `` |
| `<Image src={x} alt="" width={w} height={h} />` | `<img src={x} alt="" width={w} height={h} loading="lazy" />` |
| `<Link href="/x">` | `<a href="/x">` ou `<a href="#x">` |
| `useTheme()` | `useState('dark')` ou prop |
| `<Button variant="default">` | `<button className="...">` |
| `motion/react` | `framer-motion` (mesmo pacote, alias diferente) |

---

## Templates Adaptados (Inline)

Abaixo estão os templates mais usados já adaptados e prontos para copiar:

## Table of Contents

1. [useInView Hook](#useinview-hook)
2. [TextCycle — Animated Text Rotation](#textcycle)
3. [Section — Scroll Animated Wrapper](#section)
4. [Glassmorphism Trust Hero](#glassmorphism-trust-hero)
5. [Scroll Expand Media](#scroll-expand-media)
6. [Feature Card](#feature-card)
7. [Benefit Card](#benefit-card)
8. [Operational Timeline](#operational-timeline)
9. [InfiniteSlider — Logo Cloud](#infiniteslider)
10. [DottedSurface — Three.js Background](#dottedsurface)
11. [WhatsApp Floating Button](#whatsapp-floating)
12. [Contact Form — Glass Style](#contact-form)

---

## useInView Hook

Intersection Observer para animações de entrada. Dispara uma vez quando o elemento entra na viewport.

```tsx
function useInView(threshold = 0.15) {
  const ref = useRef<HTMLDivElement>(null)
  const [isInView, setIsInView] = useState(false)
  useEffect(() => {
    const el = ref.current
    if (!el) return
    const obs = new IntersectionObserver(
      ([e]) => { if (e.isIntersecting) setIsInView(true) },
      { threshold }
    )
    obs.observe(el)
    return () => obs.disconnect()
  }, [threshold])
  return { ref, isInView }
}
```

## TextCycle

Texto que alterna entre palavras com animação slide-up. Ideal para hero headlines.

```tsx
function TextCycle({ words, interval = 3000 }: { words: string[]; interval?: number }) {
  const [idx, setIdx] = useState(0)
  useEffect(() => {
    const t = setInterval(() => setIdx(i => (i + 1) % words.length), interval)
    return () => clearInterval(t)
  }, [words.length, interval])
  return (
    <span className="inline-block relative overflow-hidden h-[1.2em] align-bottom">
      <span key={idx} style={{ animation: 'slideUp 0.5s ease-out' }}>
        {words[idx]}
      </span>
      <style>{`@keyframes slideUp { from { transform:translateY(100%); opacity:0; } to { transform:translateY(0); opacity:1; } }`}</style>
    </span>
  )
}
```

Usage: `<TextCycle words={['Offshore', 'Marítimos', 'Industriais']} />`

## Section

Wrapper que aplica fade-in + slide-up no scroll. Usar em todas as seções do site.

```tsx
function Section({ children, id, className = '' }: { children: React.ReactNode; id?: string; className?: string }) {
  const { ref, isInView } = useInView(0.1)
  return (
    <section id={id} ref={ref}
      className={`transition-all duration-1000 ${isInView ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'} ${className}`}
    >
      {children}
    </section>
  )
}
```

## Glassmorphism Trust Hero

Hero com 2 colunas: texto + CTAs à esquerda, glass cards com stats e marquee à direita.
Ideal para sites B2B/enterprise que querem transmitir confiança e dados.

**Estrutura:**
- Left column (lg:col-span-7): Badge animado → Heading com gradient + TextCycle → Descrição → 2 CTAs
- Right column (lg:col-span-5): Glass stats card (progress bar + mini stats + tags) → Marquee card (canais/integrações)

**Padrões visuais:**
- Background: mesh gradients + grid overlay + scan-line
- Glass cards: `border border-white/10 bg-white/5 backdrop-blur-xl`
- Tags: indicador pulsante verde (IA ATIVA), badges com ícones
- Fade-in escalonado: `.hero-fade { animation: heroFadeIn 0.8s ease-out forwards; opacity:0; }`

**Adaptações necessárias:**
- Substituir textos/dados pelo conteúdo do cliente
- Ajustar cores do accent para a paleta do projeto
- Substituir ícones de canais/integrações conforme o produto

Ver implementação completa em `references/hero-template.md` (se criado).

## Scroll Expand Media

Imagem central que expande para fullscreen conforme o scroll. Texto se divide e voa para os lados.
Ideal como showcase imersivo entre seções.

**Comportamento:**
1. Imagem começa pequena (320×250px) no centro da viewport
2. Conforme scroll (wheel ou touch), expande gradualmente
3. Texto split (metade vai pra esquerda, metade pra direita) proporcional ao scroll
4. Ao atingir 100%, a seção se "libera" e o scroll normal continua
5. Hint "Role para expandir" com seta pulsante

**Atenção:** Este componente hijacka o scroll. Usar no máximo 1x por site.

```tsx
// Props
{ imageSrc: string; title: string }
// Calcula dimensões baseado em progress (0-1):
const w = 320 + progress * (isMobile ? 600 : 1200)
const h = 250 + progress * (isMobile ? 200 : 450)
```

## Feature Card

Card com imagem, ícone, título e descrição. Usa glass morphism e glow animation.

```tsx
function FeatureCard({ icon: Icon, title, description, image, delay = 0 }: {
  icon: React.ElementType; title: string; description: string; image?: string; delay?: number
}) {
  const { ref, isInView } = useInView()
  return (
    <div ref={ref} className={`glass-card rounded-2xl overflow-hidden transition-all duration-700 hover:scale-[1.02] group
      ${isInView ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-12'}`}
      style={{ transitionDelay: `${delay}ms` }}>
      {image && (
        <div className="h-48 overflow-hidden">
          <img src={image} alt={title} className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
            width="400" height="192" loading="lazy" />
        </div>
      )}
      <div className="p-6">
        <div className="w-12 h-12 rounded-xl bg-accent/10 flex items-center justify-center mb-4 border border-accent/20">
          <Icon className="w-6 h-6 text-accent" />
        </div>
        <h3 className="text-xl font-semibold mb-2">{title}</h3>
        <p className="text-sm leading-relaxed opacity-80">{description}</p>
      </div>
    </div>
  )
}
```

## Benefit Card

Card com ícone, título e lista de itens. Mais simples que FeatureCard, sem imagem.

```tsx
function BenefitCard({ icon: Icon, title, items, delay = 0 }: {
  icon: React.ElementType; title: string; items: string[]; delay?: number
}) { /* ... useInView + list rendering ... */ }
```

## Operational Timeline

Timeline de scroll onde o card ativo expande conforme proximidade ao viewport center.
Usa requestAnimationFrame + sentinel divs para detectar o card mais próximo.

**Estrutura por entry:**
- Left: sticky meta column (ícone + etapa + título)
- Right: card com imagem, subtitle badge, descrição, lista expansível

**Data structure:**
```tsx
type TimelineEntry = {
  icon: React.ElementType
  step: string
  title: string
  subtitle: string
  description: string
  items: string[]
  image: string
}
```

## InfiniteSlider

Componente de scroll infinito para logo clouds / marquee. Requer `react-use-measure` e `framer-motion`.

Criar como arquivo separado `src/InfiniteSlider.tsx`:

```tsx
import { useMotionValue, animate, motion } from 'framer-motion'
import { useState, useEffect } from 'react'
import useMeasure from 'react-use-measure'
// ... (ver implementação completa no projeto de referência)
```

**Usage para logo cloud:**
```tsx
<InfiniteSlider gap={60} reverse duration={30} durationOnHover={60}>
  {logos.map(logo => (
    <img key={logo.alt} src={logo.src} alt={logo.alt}
      className={`h-8 md:h-10 w-auto select-none opacity-60 hover:opacity-100 ${logo.invert ? 'brightness-0 invert' : ''}`}
      loading="lazy" width="120" height="40" />
  ))}
</InfiniteSlider>
```

**Atenção com filtros de cor:**
- `brightness-0 invert` funciona para logos escuros em fundo dark (transforma em branco)
- NÃO usar em logos coloridos com fundo branco (fica todo branco)
- Usar flag `invert: boolean` por logo para controle individual

## DottedSurface

Background animado Three.js com partículas ondulantes. Sempre criar como arquivo separado
para code-splitting via `lazy()`:

```tsx
// src/DottedSurface.tsx — arquivo separado
// No App.tsx:
const DottedSurface = lazy(() => import('./DottedSurface'))
// No JSX:
<Suspense fallback={null}><DottedSurface /></Suspense>
```

**Configurações para a paleta do projeto:**
Ajustar as cores RGB das partículas para matches da paleta do cliente:
```tsx
const r = 0.20 + t * 0.15  // ajustar conforme accent
const g = 0.70 + t * 0.16
const b = 0.55 + t * 0.18
```

Adicionar `three` ao `manualChunks` no vite.config.ts.

## WhatsApp Floating

Botão flutuante no canto inferior direito com tooltip no hover.

```tsx
<a href="https://wa.me/NUMERO?text=MENSAGEM"
  target="_blank" rel="noreferrer"
  className="fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full bg-green-500 flex items-center justify-center shadow-lg hover:scale-110 transition-all group">
  <MessageCircle className="w-7 h-7 text-white" />
  <span className="absolute right-full mr-3 px-3 py-1.5 rounded-lg bg-neutral-800 text-white text-sm whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
    Fale pelo WhatsApp
  </span>
</a>
```

## Contact Form

Formulário com glass morphism. Campos: nome, empresa, email, telefone, mensagem.

**CSS classes essenciais:**
```css
.glass-card {
  background: rgba(16, 29, 34, 0.7);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(59, 102, 109, 0.3);
}
```

Input styling: `bg-neural-800/60 border border-neural-600/30 focus:border-accent/50`
