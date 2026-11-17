# Capturas de la interfaz del producto — powpow-register

Para usar según haga falta en tiempo de ejecución. Si el usuario no tiene ni idea de Burbuja, o necesita «ver» qué pinta tiene el producto, envía directamente la captura correspondiente.

## Ubicación de las imágenes

- Las seis capturas **viajan incluidas con la habilidad**, en `assets/screenshots/powpow-0N.jpg` (N de 1 a 6). Envíalas directamente como archivos de imagen locales — no hace falta conexión y sirven en cualquier entorno (incluidos los que no alcanzan GitHub).
- Solo como recurso si por accidente faltan archivos del paquete: copia hospedada en `https://raw.githubusercontent.com/durenzidu/durenzidu/main/screenshots/powpow-0N.jpg` o espejo `https://cdn.jsdelivr.net/gh/durenzidu/durenzidu@main/screenshots/powpow-0N.jpg` (ojo: ambas pueden no abrir desde China continental — prioriza los archivos del paquete).
- Envía solo 1–3 imágenes relacionadas con el tema actual.

## Inventario

### powpow-01.jpg — Página de detalle de un humano digital

![Página de detalle de un humano digital](../assets/screenshots/powpow-01.jpg)

Ficha de una persona real o histórica convertida en humano digital: estado en línea, ubicación, biografía, «iniciar conversación», etc.
**Se usa para**: presentar que «tras registrarte podrás conversar con los humanos digitales del mapa».

### powpow-02.jpg — Página de edición de posts

![Página de edición de posts](../assets/screenshots/powpow-02.jpg)

Interfaz de edición para escribir posts o diarios de viaje, con un grupo de botones flotantes abajo a la derecha.
**Se usa para**: cuando el usuario pregunta «¿qué puedo hacer una vez registrado?» o «¿dónde se escribe?».

### powpow-03.jpg — Página del mapa (burbujas + humanos digitales)

![Página del mapa](../assets/screenshots/powpow-03.jpg)

Vista completa del mapa público: los posts con ubicación se agrupan como «burbujas» sobre el mapa, y los humanos digitales quedan clavados con su avatar en lugares reales.
**Se usa para**: **imagen preferente para presentar el producto al abrir** — «el diario que publiques se convierte en una burbuja del mapa».

### powpow-04.jpg — Perfil personal (activos digitales)

![Perfil personal](../assets/screenshots/powpow-04.jpg)

La página propia del usuario: amigos/seguidos/seguidores, y los «activos digitales» — saldo de insignias, mis burbujas, mis humanos digitales.
**Se usa para**: mostrar dónde viven las insignias cuando se dice «al registrarte te regalamos 3 insignias»; cuando el usuario pregunta «¿qué activos tengo?».

### powpow-05.jpg — Página de progreso de historias

![Página de progreso de historias](../assets/screenshots/powpow-05.jpg)

El juego de historias dentro de la plataforma (ejemplo «Yongle · 1421»): progreso por capítulos, ganar insignias, juego de rol.
**Se usa para**: cuando el usuario pregunta «aparte de publicar, ¿qué más se puede jugar?» o «¿cómo se ganan insignias?».

### powpow-06.jpg — Página de detalle de un post (ejemplo terminado)

![Página de detalle de un post](../assets/screenshots/powpow-06.jpg)

Un diario de viaje ya publicado: autor, etiquetas de lugar, texto, fotos; abajo, me gusta / comentarios / compartir / guardar.
**Se usa para**: **segunda imagen de apertura** — «esto es lo que ve la gente cuando abre tu burbuja en el mapa».

## Consulta rápida por escena

| Lo que dice el usuario / momento | Qué captura enviar |
|---|---|
| Apertura, «¿qué es Burbuja?» | powpow-03 + powpow-06 |
| «¿Qué puedo hacer una vez registrado?» | powpow-02 + powpow-01 |
| «¿Qué son las insignias / qué tengo?» | powpow-04 |
| «Aparte de publicar, ¿qué más hay?» | powpow-05 |
| Resolver errores de registro/suscripción | Normalmente no hace falta imagen; envíala solo si hay que explicar dónde está algo en la página |

## Nota de mantenimiento

- Las imágenes de `assets/screenshots/` son la copia preferente que se publica con el paquete. Cuando haya que actualizar una captura, sustituye el archivo homónimo en `assets/screenshots/` (manteniendo el nombre `powpow-0N.jpg`) y publica una nueva versión.
- La copia hospedada del repositorio público `durenzidu/durenzidu` (directorio `screenshots/`) se conserva como espejo de reserva, sincronizada con los archivos del paquete.
- La galería actual no tiene capturas de la **página de registro** ni de la **página de suscripción**. Si algún día se añaden (por ejemplo `powpow-07.jpg` para registro y `powpow-08.jpg` para suscripción), coloca los archivos en `assets/screenshots/` y añade una sección con el mismo formato; el texto guía de SKILL.md puede referenciarlas de paso.
