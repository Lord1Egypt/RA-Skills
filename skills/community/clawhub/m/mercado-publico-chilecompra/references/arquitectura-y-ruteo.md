# Arquitectura y ruteo del portal

## Modelo mental

El portal es híbrido:
- shell legacy en `Menu.aspx`
- muchos módulos cargados en iframe `fraDetalle`
- otros módulos más nuevos viven en rutas separadas o integradas parcialmente

## Regla principal

Preferir partir desde:
- `https://www.mercadopublico.cl/Portal/Modules/Menu/Menu.aspx`

Antes de concluir que un módulo está roto:
1. intentar desde el menú
2. revisar si debe cargarse en `fraDetalle`
3. recién después probar/descartar una URL directa

## Patrón de navegación recomendado

1. Abrir o enfocar `Menu.aspx` autenticado.
2. Inspeccionar `iframe#fraDetalle`.
3. Cargar el módulo en `fraDetalle` cuando corresponda.
4. Si el módulo abre en ruta externa/moderna, seguir ese flujo y verificar que mantiene sesión.

## Problemas observados

- Algunas rutas del menú abiertas directamente devuelven 404.
- Algunos módulos legacy dependen de postbacks y contexto interno.
- Algunos módulos nuevos pueden mostrar errores servidor si entran sin el estado esperado.
- Puede haber CAPTCHA o validaciones externas en ciertos flujos.
- Abrir ciertos módulos en pestañas nuevas o fuera del shell autenticado puede redirigir a la home pública, incluso si la sesión parecía viva en `Menu.aspx`.

## Señales útiles

- 404 directo no siempre significa módulo inexistente; puede ser problema de contexto.
- `NullReferenceException` o errores .NET pueden indicar bug real del portal o estado incompleto.
- Si `fraDetalle` cambia y el shell permanece estable, normalmente el flujo correcto es interno.
