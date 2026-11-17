# Plantilla del título de portada (overlay transparente)

Guarda esto como `overlay.html` en la carpeta `recursos/` del carrusel. El `omitBackground`
del script `overlay_export.js` recorta todo lo que no sea texto, así que el fondo DEBE ser transparente.

- Posiciona el título en el **tercio superior** (la zona de cielo/espacio libre de la foto).
- Pesos mezclados estilo @vaibhavsisinty: línea pequeña 300 / título 800 grande / línea pequeña 300.
- Sub en mono verde lima (acento): `Space Mono` 700, color `#C6F24E`.
- Sombra fuerte para legibilidad sobre el video.
- El `.slide` mide lo mismo que el video final (por defecto 1080×1350).

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;800&family=Space+Mono:wght@700&display=swap" rel="stylesheet">
<style>
  *{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;}
  html,body{background:transparent;}                 /* OBLIGATORIO */
  .slide{ position:relative; width:1080px; height:1350px; background:transparent; overflow:hidden; }
  .titlewrap{ position:absolute; top:120px; left:0; right:0; text-align:center; color:#fff;
        text-shadow:0 4px 30px rgba(15,55,95,.55); padding:0 60px; }
  .t-sm{ font-family:'Poppins'; font-weight:300; font-size:48px; letter-spacing:.3px; }
  .t-big{ font-family:'Poppins'; font-weight:800; font-size:104px; line-height:.98; letter-spacing:-2px; margin:6px 0; }
  .t-sm2{ font-family:'Poppins'; font-weight:300; font-size:46px; }
  .swipe{ margin-top:30px; font-family:'Space Mono'; font-weight:700; font-size:30px; letter-spacing:3px;
        color:#C6F24E; text-shadow:0 2px 12px rgba(0,0,0,.4); }
</style>
</head>
<body>
<section class="slide">
  <div class="titlewrap">
    <div class="t-sm">LÍNEA PEQUEÑA DE ARRIBA</div>
    <div class="t-big">TÍTULO GRANDE</div>
    <div class="t-sm2">línea pequeña de cierre</div>
    <div class="swipe">DESLIZA PARA VER →</div>
  </div>
</section>
</body>
</html>
```

> Ajusta `top`, `font-size` y el número de líneas según la foto. Si el sujeto está muy arriba,
> baja el título o súbelo a `top:90px`. La regla: el texto vive donde la foto tiene cielo/espacio vacío.

## Variante de paleta
La paleta del estilo espejo (cielo + repisa naranja) usa lima `#C6F24E` de acento. Si el carrusel
tiene otra marca, cambia el color del `.swipe` y el `text-shadow` al color de marca del usuario.
