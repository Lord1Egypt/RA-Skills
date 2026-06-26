# CSS Patterns & Visual Guidelines

## index.css Base Template

```css
@import "tailwindcss";

@theme {
  /* SUBSTITUIR pela paleta do cliente */
  --color-primary-900: #101D22;
  --color-primary-50: #F3FAFA;
  --color-accent: #3DDBAB;
  --color-accent-light: #5BEECC;
  --font-sans: 'Inter', system-ui, sans-serif;
}

@layer base {
  html { scroll-behavior: smooth; }
  body {
    margin: 0;
    background-color: var(--color-primary-900);
    color: var(--color-primary-50);
    -webkit-font-smoothing: antialiased;
  }
  #root { width: 100%; max-width: 100%; margin: 0; }
}

/* Scrollbar */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: var(--color-primary-900); }
::-webkit-scrollbar-thumb { background: var(--color-primary-500); border-radius: 4px; }

/* Animations */
@keyframes glow-pulse {
  0%, 100% { box-shadow: 0 0 20px rgba(var(--accent-rgb), 0.1); }
  50% { box-shadow: 0 0 40px rgba(var(--accent-rgb), 0.25); }
}
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.animate-float { animation: float 6s ease-in-out infinite; }

/* Glass morphism */
.glass-card {
  background: rgba(16, 29, 34, 0.7);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(59, 102, 109, 0.3);
}

/* Gradient text */
.gradient-text {
  background: linear-gradient(135deg, currentColor, var(--color-accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Gradient border (pseudo-element) */
.gradient-border { position: relative; }
.gradient-border::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1px;
  background: linear-gradient(135deg, var(--color-accent), var(--color-primary-500), transparent);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}
```

## Google Fonts — Non-Render-Blocking Pattern

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" media="print" onload="this.media='all'" />
<noscript><link href="..." rel="stylesheet" /></noscript>
```

## Image Optimization Script

```python
from PIL import Image
import glob, os

for f in glob.glob("public/images/**/*.png", recursive=True) + glob.glob("public/images/**/*.jpg", recursive=True):
    if os.path.getsize(f) > 100_000:
        img = Image.open(f)
        if hasattr(img, 'mode') and img.mode == 'RGBA':
            img = img.convert('RGBA')
        if img.width > 1200:
            ratio = 1200 / img.width
            img = img.resize((1200, int(img.height * ratio)), Image.LANCZOS)
        webp = f.rsplit('.', 1)[0] + '.webp'
        img.save(webp, 'WEBP', quality=80, method=6)
        old_kb = os.path.getsize(f) // 1024
        new_kb = os.path.getsize(webp) // 1024
        print(f"{f}: {old_kb}KB -> {webp}: {new_kb}KB")
```

## Section Ordering — B2B Best Practices

Standard B2B institutional site ordering based on conversion optimization:

1. **Hero** — proposta de valor em 5 segundos
2. **Social proof #1** (opcional) — logos de clientes right after hero
3. **Problema** — criar empatia com a dor do cliente
4. **Solução** — posicionar o produto como resposta
5. **Como funciona** — pipeline/processo em etapas
6. **Funcionalidades** — cards detalhados com imagens
7. **Detalhes técnicos** — especificações, IoT, integrações
8. **Benefícios** — resultados organizados por categoria
9. **Social proof #2** — logos de clientes antes do CTA ("trust before action")
10. **CTA Final** — frase de impacto + botão de ação
11. **Contato** — formulário + dados comerciais
12. **Footer** — links, logo, copyright
