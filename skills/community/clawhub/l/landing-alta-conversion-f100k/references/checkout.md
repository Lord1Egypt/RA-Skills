# Integración de checkout — Hotmart / Stripe / GHL

Los 3 CTAs de la plantilla apuntan a `{{CHECKOUT_URL}}`. Elige UNA pasarela y reemplaza el token.

## Modo LINK (recomendado — más simple, funciona en todo)
Reemplaza `{{CHECKOUT_URL}}` por la URL de pago:

| Pasarela | Formato del link |
|----------|------------------|
| **Hotmart** | `https://pay.hotmart.com/XXXXXXXX?checkoutMode=10` (link de "Checkout" del producto) |
| **Stripe**  | `https://buy.stripe.com/XXXXXXXX` (Payment Link creado en el dashboard) |
| **GHL**     | URL del step de pago del funnel (`https://tudominio.com/checkout` o link del order form) |

El botón `.cta` ya es un `<a href>` — con esto queda listo. Los 3 CTAs comparten el mismo link (mantener consistencia).

## Modo EMBED (checkout incrustado en la página)
Solo si el usuario lo pide explícitamente. Sustituye el `<a class="cta">` del bloque final por el embed:

### Hotmart (embed oficial)
```html
<script src="https://checkout.hotmart.com/lib/hotmart-checkout-elements.js"></script>
<a onclick="hotmart.checkout.pay('CODIGO_DE_OFERTA')" class="cta">Comprar ahora</a>
<script>hotmart.checkout.init();</script>
```
> En GHL el `<script>` externo puede bloquearse; usa modo LINK si el embed no carga.

### Stripe (Payment Link como botón — no requiere JS)
Modo LINK ya cubre Stripe. Para checkout embebido real (Stripe.js) hace falta backend → fuera del alcance de una landing estática; usa Payment Link.

### GHL (order form nativo)
Si la landing se sube DENTRO de GHL, lo ideal es que el CTA lleve al order form nativo del funnel (no embeber pasarela externa). Reemplaza `{{CHECKOUT_URL}}` por la ruta relativa del step de pago.

## UTMs y tracking
Añade UTMs al link para atribución de pauta Meta:
```
...checkout?utm_source=ig&utm_medium=paid&utm_campaign=lanzamiento
```
Si hay Pixel de Meta / GA, pega el snippet en el `<head>` (o en GHL, en Tracking Code) — no en el body de la plantilla.

## Orden bump / upsell (opcional)
La plantilla no incluye order bump. Si lo quieren:
- **Hotmart/GHL**: se configuran en la propia pasarela (order bump nativo). La landing solo manda al checkout; el bump aparece allí.
- No intentar simular el bump en HTML estático.
