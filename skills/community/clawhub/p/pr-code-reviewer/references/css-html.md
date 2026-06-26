# Reglas CSS y HTML

Aplica a archivos con extensión: .css, .scss, .sass, .less, .html, .htm, .vue, .svelte, .jsx, .tsx
(para la parte de markup y estilos)

---

## 🔴 BLOCKERS

### Accesibilidad (A11y) Crítica
- Imágenes sin atributo alt (o alt vacío sin justificación)
- Formularios sin labels asociados a sus inputs
- Botones o links sin texto accesible (vacíos o solo con ícono sin aria-label)
- Uso de div o span como botón/link sin role y sin keyboard handling
- Contenido importante transmitido solo por color sin indicador alternativo
- autofocus en elementos que no son el propósito principal de la página
- tabindex con valores positivos (rompe el orden natural de navegación)

❌ Mal:
  <img src="logo.png">
  <input type="email" placeholder="Email">
  <div onclick="submit()">Enviar</div>
  <span class="icon-close" onclick="close()"></span>

✅ Bien:
  <img src="logo.png" alt="Logo de la empresa">
  <img src="decorative-line.png" alt=""> <!-- Decorativa: alt vacío es correcto -->

  <label for="email">Email</label>
  <input type="email" id="email" placeholder="ejemplo@correo.com">

  <button type="submit">Enviar</button>

  <button type="button" onclick="close()" aria-label="Cerrar diálogo">
    <span class="icon-close" aria-hidden="true"></span>
  </button>

### HTML Semántico Crítico
- Más de un <h1> por página
- Headings que saltan niveles: h1 directo a h3 sin h2
- Usar tablas para layout en lugar de datos tabulares
- Formularios sin action o method definidos cuando es relevante

❌ Mal:
  <table>
    <tr>
      <td class="sidebar">...</td>
      <td class="content">...</td>
    </tr>
  </table>

  <h1>Título</h1>
  <h3>Subtítulo</h3> <!-- Saltó h2 -->

✅ Bien:
  <div class="layout">
    <aside class="sidebar">...</aside>
    <main class="content">...</main>
  </div>

  <h1>Título</h1>
  <h2>Subtítulo</h2>

### CSS Crítico
- !important en estilos que no son overrides de terceros o utilidades
- Estilos inline en HTML para lógica de presentación compleja
- z-index con valores arbitrarios altos: 9999, 999999
- overflow: hidden en body o html que rompe scroll de la página

❌ Mal:
  .card {
    color: red !important;
    z-index: 9999;
  }

  <div style="display:flex;justify-content:space-between;align-items:center;padding:20px;margin:10px;background:#f5f5f5;border-radius:8px;">

✅ Bien:
  /* Escala de z-index documentada */
  :root {
    --z-dropdown: 100;
    --z-sticky: 200;
    --z-modal-backdrop: 300;
    --z-modal: 400;
    --z-tooltip: 500;
  }

  .card {
    color: var(--color-error);
  }

  .modal {
    z-index: var(--z-modal);
  }

### Seguridad en HTML
- Links con target="_blank" sin rel="noopener noreferrer" (en navegadores legacy)
- Iframes sin sandbox attribute para contenido externo
- Formularios que envían datos sensibles sin HTTPS (action="http://...")

❌ Mal:
  <a href="https://external.com" target="_blank">Visitar</a>
  <iframe src="https://external-widget.com/embed"></iframe>

✅ Bien:
  <a href="https://external.com" target="_blank" rel="noopener noreferrer">Visitar</a>
  <iframe src="https://external-widget.com/embed" sandbox="allow-scripts allow-same-origin"></iframe>

---

## 🟡 WARNINGS

### HTML Semántico
- No usar elementos semánticos cuando corresponde:
  <header>, <footer>, <nav>, <main>, <article>, <section>, <aside>, <figure>, <figcaption>
- Usar <br> para espaciado en lugar de CSS margin/padding
- Usar <b> y <i> cuando el significado es <strong> y <em>
- Usar <div> para todo cuando existe un elemento semántico apropiado
- Listas de navegación sin <nav> y sin <ul>/<ol>

❌ Mal:
  <div class="header">
    <div class="nav">
      <div class="nav-item"><a href="/">Home</a></div>
      <div class="nav-item"><a href="/about">About</a></div>
    </div>
  </div>
  <div class="main">
    <div class="article">
      <div class="title">Mi Artículo</div>
      <br><br>
      <div class="content">Contenido...</div>
    </div>
  </div>
  <div class="footer">© 2026</div>

✅ Bien:
  <header>
    <nav aria-label="Navegación principal">
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about">About</a></li>
      </ul>
    </nav>
  </header>
  <main>
    <article>
      <h2>Mi Artículo</h2>
      <p>Contenido...</p>
    </article>
  </main>
  <footer>© 2026</footer>

### Accesibilidad Intermedia
- Contraste insuficiente entre texto y fondo (mínimo 4.5:1 para texto normal, 3:1 para grande)
- Elementos interactivos con área de toque menor a 44x44px en móvil
- Animaciones sin prefers-reduced-motion
- Contenido que desaparece o aparece sin aviso a screen readers
- Formularios sin mensajes de error asociados al campo

❌ Mal:
  .spinner {
    animation: spin 1s linear infinite;
  }

✅ Bien:
  .spinner {
    animation: spin 1s linear infinite;
  }

  @media (prefers-reduced-motion: reduce) {
    .spinner {
      animation: none;
    }
  }

✅ Error accesible en formulario:
  <label for="email">Email</label>
  <input type="email" id="email" aria-describedby="email-error" aria-invalid="true">
  <span id="email-error" role="alert">Por favor ingresa un email válido</span>

### CSS Layout
- Usar float para layout (excepto para wrapping de texto alrededor de imágenes)
- Anchos y alturas fijos en píxeles para contenedores que deberían ser responsivos
- Media queries con valores de px hardcodeados sin lógica clara de breakpoints
- Usar position: absolute/fixed sin considerar el contexto de stacking

❌ Mal:
  .container {
    width: 1200px;
    margin: 0 auto;
  }

  .sidebar {
    float: left;
    width: 300px;
  }

  .content {
    float: left;
    width: 900px;
  }

✅ Bien:
  .container {
    max-width: 1200px;
    width: 100%;
    margin: 0 auto;
    padding-inline: 1rem;
  }

  .layout {
    display: grid;
    grid-template-columns: minmax(200px, 300px) 1fr;
    gap: 2rem;
  }

  @media (max-width: 768px) {
    .layout {
      grid-template-columns: 1fr;
    }
  }

### Responsive Design
- No tener meta viewport en el HTML
- Texto con font-size fijo en px que no escala
- Elementos que se desbordan en pantallas pequeñas
- Imágenes sin max-width: 100% que rompen el layout en móvil
- No testear en diferentes tamaños de pantalla

✅ Siempre incluir:
  <meta name="viewport" content="width=device-width, initial-scale=1">

✅ Imágenes responsivas:
  img {
    max-width: 100%;
    height: auto;
  }

  /* Mejor con srcset para diferentes resoluciones */
  <img
    src="photo-800.jpg"
    srcset="photo-400.jpg 400w, photo-800.jpg 800w, photo-1200.jpg 1200w"
    sizes="(max-width: 600px) 100vw, (max-width: 1200px) 50vw, 800px"
    alt="Descripción de la foto"
  >

### Performance CSS
- Selectores excesivamente específicos o profundos
- @import en CSS (bloquea el render; usar <link> o bundler)
- Fuentes web sin font-display: swap o fallback
- Animaciones de propiedades que causan layout/paint: width, height, top, left
- No usar will-change con moderación (solo donde realmente se necesita)

❌ Mal:
  @import url('fonts.css'); /* Bloquea render */

  body div.container main article .content p span.highlight {
    color: red;
  }

  .animated-box {
    transition: width 0.3s, height 0.3s, top 0.3s;
  }

✅ Bien:
  /* En HTML: <link rel="stylesheet" href="fonts.css"> */

  .highlight {
    color: var(--color-highlight);
  }

  .animated-box {
    transition: transform 0.3s, opacity 0.3s; /* Solo propiedades composited */
  }

  @font-face {
    font-family: 'CustomFont';
    src: url('custom-font.woff2') format('woff2');
    font-display: swap;
  }

---

## 🔵 SUGGESTIONS

### Custom Properties (CSS Variables)
- Usar CSS custom properties para valores reutilizables: colores, spacing, typography
- Definir un sistema de design tokens consistente
- Usar variables para theming (dark mode, etc.)

✅ Sistema de tokens recomendado:
  :root {
    /* Colores */
    --color-primary: #2563eb;
    --color-primary-hover: #1d4ed8;
    --color-error: #dc2626;
    --color-success: #16a34a;
    --color-text: #1f2937;
    --color-text-secondary: #6b7280;
    --color-bg: #ffffff;
    --color-bg-secondary: #f3f4f6;
    --color-border: #e5e7eb;

    /* Spacing */
    --space-xs: 0.25rem;
    --space-sm: 0.5rem;
    --space-md: 1rem;
    --space-lg: 1.5rem;
    --space-xl: 2rem;
    --space-2xl: 3rem;

    /* Typography */
    --font-sans: system-ui, -apple-system, sans-serif;
    --font-mono: 'Fira Code', monospace;
    --text-sm: 0.875rem;
    --text-base: 1rem;
    --text-lg: 1.125rem;
    --text-xl: 1.25rem;
    --text-2xl: 1.5rem;

    /* Borders */
    --radius-sm: 0.25rem;
    --radius-md: 0.5rem;
    --radius-lg: 1rem;
    --radius-full: 9999px;
  }

  /* Dark mode */
  @media (prefers-color-scheme: dark) {
    :root {
      --color-text: #f9fafb;
      --color-text-secondary: #9ca3af;
      --color-bg: #111827;
      --color-bg-secondary: #1f2937;
      --color-border: #374151;
    }
  }

### Metodología CSS
- Usar una metodología consistente: BEM, Utility-first, CSS Modules, CSS-in-JS
- Si se usa BEM: Block__Element--Modifier
- Evitar mezclar metodologías en el mismo proyecto

✅ Ejemplo BEM:
  .card {}
  .card__header {}
  .card__body {}
  .card__footer {}
  .card--featured {}
  .card--compact {}
  .card__header--sticky {}

### Formularios Accesibles Completos
✅ Ejemplo de formulario bien estructurado:
  <form novalidate>
    <fieldset>
      <legend>Información Personal</legend>

      <div class="form-group">
        <label for="name">Nombre completo <span aria-hidden="true">*</span></label>
        <input
          type="text"
          id="name"
          name="name"
          required
          autocomplete="name"
          aria-required="true"
        >
      </div>

      <div class="form-group">
        <label for="email">Email <span aria-hidden="true">*</span></label>
        <input
          type="email"
          id="email"
          name="email"
          required
          autocomplete="email"
          aria-required="true"
          aria-describedby="email-hint"
        >
        <span id="email-hint" class="hint">Usaremos este email para contactarte</span>
      </div>
    </fieldset>

    <button type="submit">Enviar</button>
  </form>

### Modern CSS Features
- Usar container queries para componentes verdaderamente responsivos
- Usar :has() para parent selectors (cuando el soporte lo permita)
- Usar logical properties: margin-inline, padding-block, etc.
- Usar clamp() para fluid typography y spacing
- Usar aspect-ratio para mantener proporciones

✅ Ejemplos:
  /* Fluid typography */
  h1 {
    font-size: clamp(1.5rem, 4vw, 3rem);
  }

  /* Aspect ratio */
  .video-container {
    aspect-ratio: 16 / 9;
    width: 100%;
  }

  /* Logical properties */
  .card {
    margin-block: var(--space-md);
    padding-inline: var(--space-lg);
    border-inline-start: 3px solid var(--color-primary);
  }

  /* Container queries */
  .card-container {
    container-type: inline-size;
  }

  @container (min-width: 400px) {
    .card {
      display: grid;
      grid-template-columns: auto 1fr;
    }
  }

---

## 💡 NITS

### HTML
- Atributos booleanos sin valor: usar "required" no "required='true'"
- Orden consistente de atributos: id, class, name, type, otros, aria-*, data-*
- Cerrar void elements consistentemente: <img /> o <img>, elegir uno
- Usar comillas dobles para atributos HTML
- Indentar contenido de elementos de bloque

### CSS
- Ordenar propiedades de forma consistente:
  1. Layout: display, position, grid, flex
  2. Box model: width, height, margin, padding, border
  3. Typography: font, color, text-align, line-height
  4. Visual: background, box-shadow, opacity, border-radius
  5. Animation: transition, animation, transform
  6. Misc: cursor, pointer-events, overflow

- Usar shorthand properties cuando se definen todos los valores
- No usar unidades en valores de 0: margin: 0, no margin: 0px
- Usar rem o em para font-size, no px
- Preferir hex corto cuando sea posible: #fff en lugar de #ffffff
- Agrupar media queries junto al componente que modifican, no al final del archivo
- Usar nesting nativo de CSS o de preprocesador con moderación (máximo 3 niveles)

❌ Mal:
  .nav {
    .list {
      .item {
        .link {
          .icon {
            color: red;
          }
        }
      }
    }
  }

✅ Bien:
  .nav-link {
    color: var(--color-text);

    &:hover {
      color: var(--color-primary);
    }

    .icon {
      margin-inline-end: var(--space-xs);
    }
  }

### HTML Misc
- Incluir lang en el tag <html>: <html lang="es">
- Incluir charset: <meta charset="UTF-8">
- Título descriptivo en <title> para cada página
- Usar loading="lazy" en imágenes que no están en el viewport inicial
- Usar <picture> con formatos modernos (WebP, AVIF) con fallback

✅ Ejemplo de head completo:
  <!DOCTYPE html>
  <html lang="es">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="Descripción de la página">
    <title>Título de la Página | Sitio</title>
    <link rel="icon" href="/favicon.svg" type="image/svg+xml">
    <link rel="stylesheet" href="/styles.css">
  </head>

✅ Imágenes optimizadas:
  <picture>
    <source srcset="photo.avif" type="image/avif">
    <source srcset="photo.webp" type="image/webp">
    <img src="photo.jpg" alt="Descripción" loading="lazy" decoding="async">
  </picture>