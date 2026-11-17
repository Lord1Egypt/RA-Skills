# Lazarillo

**Una habilidad de [OpenClaw](https://openclaw.ai) que actúa en nombre de una persona con baja
visión: manda sus mensajes y sus notas de voz, le lee documentos y correo, y le redacta textos.**

No describe la pantalla. Hace las cosas.

## Para quién es

Para alguien que **ve, pero muy poco**: necesita letras enormes, acerca la cara a la pantalla y usa
magnificación, no lector de pantalla. A ese nivel de zoom se ven tres o cuatro palabras a la vez, así
que **buscar** algo —un contacto, un botón— cuesta mucho más que leerlo.

La idea es quitarle esa búsqueda: entra a **un solo chat** y desde ahí manda lo que sea a quien sea.

## Lo que NO hace

Está arriba a propósito, porque es la parte que importa.

- **No manda nada sin confirmación hablada.** Nunca, ni con prisa.
- **No manda a nadie que no esté en la libreta**, y no adivina números.
- **No toca dinero**, no entra a bancos, no paga, no transfiere.
- **No guarda contraseñas ni códigos.**
- **No habla por ella con nadie**: todo lo que sale lleva su visto bueno.

## Cómo protege

El diseño parte de un hecho: **ella no puede revisar la pantalla para comprobar qué pasó.** Solo
escucha lo que el agente le cuenta. Eso invalida casi todas las salvaguardas normales, que terminan
en "el usuario confirma viendo".

- **Libreta cerrada.** Los números salen de un solo archivo. Sin coincidencia exacta, no se manda.
- **Sándwich de destinatario.** Se dice a quién antes y después del contenido, con los últimos cuatro
  dígitos. Es la única verificación que entra por el oído.
- **Un cuello de botella único.** Todo envío pasa por `scripts/enviar.py`, que **falla cerrado**: si
  el modo no se puede leer, si el contacto es ambiguo, si el número no trae lada, si el contenido
  trae una clave — no manda y explica por qué.
- **Portón de confirmación en código**, con coincidencia de enunciado completo. Comparar con
  "contiene" en vez de la frase entera multiplica por once los falsos positivos.
- **Registro de todo lo enviado**, con hash del contenido y solo los últimos cuatro dígitos del
  número, pensado para copiarse fuera del alcance del agente.

Detalle en [`references/seguridad.md`](references/seguridad.md).

## Instalar

```bash
openclaw skills install git:kapitecsoluciones/lazarillo
```

Después hay que crear la configuración privada —la libreta y el perfil de la persona— siguiendo
[`references/montaje.md`](references/montaje.md). El repositorio trae solo plantillas de ejemplo:
**ningún dato real vive aquí.**

## Estado

**0.2.0.** En uso con una persona real, en español de México. El reenvío de nota de voz todavía no se
ha ejercitado de punta a punta contra un canal en producción: por eso no es 1.0.

Dos límites que conviene saber antes de confiarle algo:

- El agente corre con acceso a shell, así que **puede saltarse su propio cuello de botella**. Estas
  barreras protegen contra el error honesto, no contra un agente comprometido.
- "Cualquier mensaje frena el envío" y "el silencio nunca manda" están descritas en la habilidad y
  las obedece el modelo: **no hay un mecanismo que las imponga**.

## Origen

Nació en el hackathon **Dev Racing · Release Before Ready (Guadalajara, 2026)** como demostración.
La landing de aquel proyecto vive en la rama [`gh-pages`](../../tree/gh-pages).

Se diseñó con una persona real con baja visión, actor de teatro, que la usa todos los días.
No se publica su nombre ni ningún dato suyo.

*Lazarillo* es el nombre común en español de quien guía a una persona ciega, de *El Lazarillo de
Tormes*. Existen otros proyectos que lo usan —entre ellos [lazarillo.app](https://lazarillo.app), una
app de navegación accesible—; son cosas distintas y sin relación con esta habilidad.

Hecho por [Kapitec Soluciones](https://kapitec.pro). MIT.
