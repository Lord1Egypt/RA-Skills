# Reclamos y centro de ayuda

## Uso principal

Usar para:
- entrar al módulo de reclamos
- identificar el punto correcto de ingreso o búsqueda
- entender si el flujo permanece en el portal privado o redirige al centro de ayuda
- explicar al usuario cómo seguir sin ejecutar envíos no confirmados

## Hallazgo principal

El módulo de reclamos parece estar parcialmente acoplado al Centro de Ayuda.

## Implicaciones

- No asumir que todo el flujo de reclamo vive dentro del shell legacy.
- Verificar si el botón o acceso:
  - abre formulario interno
  - redirige a ayuda.mercadopublico.cl
  - o requiere contexto adicional

## Estrategia recomendada

1. Entrar desde `Menu.aspx`.
2. Inspeccionar los controles visibles del módulo.
3. Si redirige a ayuda, seguir el flujo con cautela y explicar la transición.
4. No enviar reclamos definitivos sin confirmación explícita.

## Salidas útiles

- dónde se inicia realmente el reclamo
- qué tipo de información pide el sistema
- si el flujo está completo o truncado
- cómo continuar de forma segura
