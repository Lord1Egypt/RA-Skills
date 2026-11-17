<div align="center">

<h1 style="border-bottom: none">
  <b><a href="https://tourmind.com/skills">Hotel Booking AI</a></b><br />
  <strong>Tu asistente personal de IA para buscar y reservar hoteles</strong>
</h1>

<a href="https://auth.journione.ai/">
  <img alt="Hotel Booking AI — busca, compara y reserva hoteles con tu agente de IA" src="https://skilloss.tourmind.com/skills/tourmind-booking/v1/hero/tourmind-booking-skills.png" style="width: 100%" />
</a>

<br />

<p align="center">
  Encuentra una estancia mejor. Compara precios en tiempo real. Reserva con confianza.
</p>

<br />

<div align="center">
  <a href="https://tourmind.com/skills">Página del producto</a> |
  <span>Demostración en vivo</span> |
  <a href="https://tourmind.com">Empresa</a>
</div>

<br />

[![Descargas en ClawHub](https://img.shields.io/badge/ClawHub_downloads-1.6k-F97316)](https://clawhub.ai/tourmind/skills/hotel-booking-ai)
[![Versión del Skill](https://img.shields.io/badge/Skill_version-1.0.8-2563EB)](SKILL.md)
[![Licencia](https://img.shields.io/github/license/tourmind-com/Hotel-Booking-AI)](LICENSE)

</div>

<br />

<div align="center">
  <a href="README.md">English</a> |
  <a href="README.zh-CN.md">简体中文</a> |
  <a href="README.ja.md">日本語</a> |
  <a href="README.es.md">Español</a>
</div>

<br />

Convierte tu agente de IA en un asistente personal de reservas de hotel. Hotel Booking AI busca hoteles en todo el mundo, compara tarifas de habitaciones en tiempo real entre las principales OTA y proveedores hoteleros, muestra fotos y condiciones de cancelación, verifica el precio final y te ayuda a reservar, pagar, cancelar o consultar pedidos en una sola conversación.

La búsqueda de hoteles, los detalles de hoteles y habitaciones, las tarifas en tiempo real y la verificación de disponibilidad son públicos: no necesitas una cuenta ni iniciar sesión hasta que quieras reservar.

## Demostración

### 1. Descubre hoteles con disponibilidad en tiempo real

<div align="center">
  <a href="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/search-en.gif">
    <img src="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/search-en.gif" alt="Demostración de búsqueda de hoteles en tiempo real con Hotel Booking AI" width="720" />
  </a>
</div>

### 2. Compara habitaciones, fotos y precios

<div align="center">
  <a href="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/detail-en.gif">
    <img src="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/detail-en.gif" alt="Demostración de comparación de habitaciones y precios con Hotel Booking AI" width="720" />
  </a>
</div>

### 3. Vuelve a verificar la tarifa y paga de forma segura

<div align="center">
  <a href="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/pay-en.gif">
    <img src="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/pay-en.gif" alt="Demostración de reserva y pago con Hotel Booking AI" width="720" />
  </a>
</div>

## Planifica y reserva tu estancia en un solo chat

- Busca por ciudad, hotel, lugar de interés, estación, dirección, zona de esquí u otro punto de interés sin inventar coordenadas.
- Compara hasta 20 hoteles candidatos y recibe las cinco mejores opciones con habitaciones verificadas en tiempo real.
- Consulta precios reales por noche y por estancia, fotos del hotel y la habitación, camas, comidas, impuestos, cancelación y estado del inventario.
- Filtra por presupuesto, distancia, estrellas, desayuno, instalaciones, tipo de habitación o cancelación gratuita.
- Entiende por qué cada hotel se ajusta a tu viaje, en lugar de recibir recomendaciones genéricas.
- Vuelve a verificar el precio exacto y la disponibilidad antes de confirmar la reserva.
- Reserva, paga con Stripe, WeChat Pay o Alipay, consulta un pedido o cancela una reserva elegible en la misma conversación.

## Clientes de IA compatibles

| Cliente | Cómo usar Hotel Booking AI |
|---|---|
| OpenClaw | Instala directamente desde ClawHub o clona este repositorio en tu directorio personal de Skills |
| WorkBuddy | Instala o importa este repositorio como Skill de usuario |
| OpenAI Codex | Instala desde la interfaz de Skills o un directorio local compatible con tu versión |
| Claude Code | Instala como Skill personal en `~/.claude/skills` |
| Clientes compatibles con Agent Skills | Disponibles cuando el cliente puede cargar un `SKILL.md` en la raíz y realizar solicitudes HTTPS `POST` |
| Clientes de IA compatibles con MCP | Utiliza el paquete complementario [Hotel Booking AI MCP](https://github.com/tourmind-com/Hotel-Booking-AI-MCP) |

## Instalación en 1 minuto

### Opción 1: instalar desde ClawHub

```bash
openclaw skills install @tourmind/hotel-booking-ai
openclaw gateway restart
```

### Opción 2: importar desde GitHub

En la interfaz de Skills de tu cliente de IA, instala o importa este repositorio:

```text
https://github.com/tourmind-com/Hotel-Booking-AI.git
```

Si el cliente carga Skills desde el sistema de archivos, clona el repositorio en su directorio personal de Skills:

```bash
CLIENT_SKILLS_DIR="<directorio-de-skills-del-cliente>"
mkdir -p "$CLIENT_SKILLS_DIR"
git clone https://github.com/tourmind-com/Hotel-Booking-AI.git "$CLIENT_SKILLS_DIR/hotel-booking-ai"
```

Directorios personales habituales:

| Cliente | Directorio |
|---|---|
| OpenClaw | `~/.openclaw/skills` |
| WorkBuddy | `~/.workbuddy/skills` |
| OpenAI Codex | Usa la interfaz de Skills o el directorio local compatible con tu versión de Codex |
| Claude Code | `~/.claude/skills` |

Recarga los Skills o reinicia tu cliente de IA y pide un hotel. No necesitas un servidor MCP local; Hotel Booking AI llama directamente a la API de TourMind mediante HTTPS.

## Busca primero e inicia sesión solo cuando reserves

Puedes buscar hoteles, consultar detalles, comparar tarifas en tiempo real y verificar disponibilidad sin `user_key`.

Cuando quieras crear, consultar, cancelar o pagar una reserva:

1. Inicia sesión con Google en [auth.journione.ai](https://auth.journione.ai).
2. Copia tu `user_key` y guárdalo como `user_key.txt` en la carpeta `hotel-booking-ai` instalada. Tu agente de IA también puede guiarte cuando inicies una operación de pedido.
3. En macOS o Linux, restringe el acceso al archivo:

   ```bash
   chmod 600 user_key.txt
   ```

Nunca añadas `user_key.txt` a un commit de Git. Está excluido por `.gitignore` y debe permanecer únicamente en tu dispositivo.

## Prompts de ejemplo

```text
Viajaré a Tokio con mi familia de cuatro personas del 3 al 7 de abril de 2027. Busca una habitación cerca de una estación, con buen acceso a Tokyo Disneyland, desayuno, cancelación gratuita y un precio total inferior a JPY 120.000. Compara los cinco mejores hoteles disponibles con fotos, tipo de habitación, camas, precio por noche y total, diferencias de transporte y plazos de cancelación. Todavía no reserves.
```

```text
Muéstrame las habitaciones disponibles en el segundo hotel. Incluye fotos, camas, comidas, política de cancelación, precio por noche, total de la estancia y si cada habitación puede confirmarse de inmediato. Recomienda la mejor relación calidad-precio, pero espera a que yo elija.
```

```text
Elige la habitación king con desayuno. Vuelve a verificar el precio exacto, la disponibilidad, los impuestos, la cancelación y cualquier cargo que pueda cobrar el hotel. Muéstrame el resumen final y espera mi confirmación explícita antes de crear la reserva o iniciar el pago.
```

## Cómo funciona Hotel Booking AI

```text
Destino, fechas y huéspedes
  → resolver la ciudad, el hotel o el punto de interés
  → buscar hasta 20 hoteles candidatos
  → consultar habitaciones en tiempo real que coincidan
  → clasificar y mostrar los cinco mejores hoteles verificados
  → mostrar detalles, fotos de habitaciones y tarifas actuales
  → volver a verificar el precio y la disponibilidad elegidos
  → crear la reserva solo tras tu confirmación explícita
  → pagar, consultar o cancelar cuando lo solicites
```

El precio de la búsqueda inicial es solo una señal para seleccionar candidatos. Los precios comparados proceden de productos de habitación en tiempo real y la reserva final utiliza la tarifa más reciente devuelta por la verificación de disponibilidad.

## Privacidad, reservas y pagos

- La búsqueda pública y la comparación de tarifas en tiempo real no requieren iniciar sesión.
- Las operaciones de pedidos usan el `user_key` guardado localmente en `user_key.txt`; no lo incluyas en prompts, capturas, registros, URL, commits ni incidencias.
- Hotel Booking AI solicita el nombre legal completo del huésped y un correo de contacto solo cuando se va a crear una reserva confirmada. No recopila un número de teléfono.
- La reserva, la cancelación y el pago son acciones explícitas. El agente debe mostrar los detalles y esperar tu confirmación.
- Los precios de TourMind incluyen impuestos. Algunos destinos pueden exigir que el hotel cobre una tasa turística o municipal al llegar; los cargos obligatorios devueltos se muestran por separado.
- Stripe añade una comisión de procesamiento del 3,5 %. También se admiten WeChat Pay y Alipay.
- Los enlaces de resultados de solo lectura muestran información de hoteles y habitaciones, pero no permiten reservar, pagar, cancelar ni acceder a páginas de cuenta o finanzas.

## Elige la integración de TourMind adecuada

| Audiencia | Integración | Modelo de autenticación | Producto y repositorio |
|---|---|---|---|
| Consumidor / ToC | Skill HTTP directo | Búsqueda y disponibilidad públicas; `user_key` solo para pedidos | **[Hotel-booking-ai](https://github.com/tourmind-com/Hotel-Booking-AI)** |
| Empresa / ToB | Skill HTTP directo | Skill Token obligatorio en cada llamada a la API | [Tourmind-booking-skill](https://github.com/tourmind-com/Tourmind-Booking-Skills) |
| Consumidor / ToC | MCP + Skill complementario | Conexión MCP pública; `user_key` solo para pedidos | [Hotel Booking AI MCP](https://github.com/tourmind-com/Hotel-Booking-AI-MCP) |
| Empresa / ToB | MCP + Skill complementario | Conexión MCP autenticada mediante Bearer | [TourMind Booking MCP](https://github.com/tourmind-com/Tourmind-Booking-MCP) |

## API y soporte

**URL base de la API:** `https://api.tourmind.com`

| Endpoint | Propósito | Inicio de sesión |
|---|---|---|
| `POST /skill/toc/check_skill_update` | Comprobar actualizaciones del Skill | No |
| `POST /skill/toc/search_location` | Resolver una región, un POI o un hotel | No |
| `POST /skill/toc/search_hotels` | Buscar hoteles candidatos | No |
| `POST /skill/toc/get_hotel_detail` | Obtener detalles e imágenes del hotel | No |
| `POST /skill/toc/query_room_rates` | Obtener habitaciones y tarifas en tiempo real | No |
| `POST /skill/toc/check_room_availability` | Volver a verificar la tarifa y el inventario | No |
| `POST /skill/toc/create_booking` | Crear una reserva tras confirmación | Sí |
| `POST /skill/toc/query_booking` | Consultar un pedido | Sí |
| `POST /skill/toc/cancel_booking` | Cancelar un pedido elegible tras confirmación | Sí |
| `POST /skill/toc/pay_order` | Iniciar el pago tras confirmación | Sí |

- Campos, contratos de respuesta, clasificación, imágenes, impuestos y reglas de reserva: [references/parameter_guide.md](references/parameter_guide.md)
- Instalación desde ClawHub: [Hotel Booking AI](https://clawhub.ai/tourmind/skills/hotel-booking-ai)
- Soporte en GitHub: [abrir una incidencia](https://github.com/tourmind-com/Hotel-Booking-AI/issues)
- Atención al cliente de TourMind: `+86-755 3665 4666`
- Soporte hotelero: `hotel@tourmind.com`
- Colaboración en productos de IA: `ai@tourmind.com`

## Licencia

[MIT](LICENSE) © 2026 TourMind
