# Template: Comentario de Review

Usa este template para cada comentario individual en un code review.
Copia y adapta según el tipo de hallazgo.

---

## Formato Estándar

[SEVERIDAD] Categoría: Título breve

**Archivo:** `ruta/al/archivo.ext` línea(s) X-Y

**Hallazgo:**
Descripción clara y concisa de lo que se encontró.

**Por qué importa:**
Explicación del impacto: seguridad, performance, mantenibilidad, etc.

**Sugerencia:**
Código o descripción de cómo resolverlo.

**Referencia:**
Link a documentación, regla o estándar que respalda el comentario.

---

## Ejemplos por Severidad

### 🔴 BLOCKER

🔴 **Seguridad: SQL Injection en búsqueda de usuarios**

**Archivo:** `src/repositories/user.repository.ts` líneas 45-48

**Hallazgo:**

  // Código actual
  const users = await db.query(
    `SELECT * FROM users WHERE name LIKE '%${searchTerm}%'`
  );

**Por qué importa:**
El parámetro `searchTerm` viene directamente del input del usuario sin sanitizar.
Un atacante puede inyectar SQL arbitrario para leer, modificar o eliminar datos
de la base de datos. Esto es una vulnerabilidad crítica.

**Sugerencia:**

  // Usar parámetros preparados
  const users = await db.query(
    'SELECT * FROM users WHERE name LIKE $1',
    [`%${searchTerm}%`]
  );

**Referencia:** rules/security.md → SQL Injection | OWASP Top 10 A03:2021

---

### 🔴 BLOCKER

🔴 **Credenciales: API key hardcodeada en código fuente**

**Archivo:** `src/services/payment.service.ts` línea 12

**Hallazgo:**

  const STRIPE_KEY = 'sk_live_abc123xyz789...';

**Por qué importa:**
La API key de Stripe en modo producción está expuesta en el código fuente.
Cualquier persona con acceso al repositorio puede usarla para realizar cargos
o acceder a información financiera de los clientes.

**Sugerencia:**

  const STRIPE_KEY = process.env.STRIPE_SECRET_KEY;

  if (!STRIPE_KEY) {
    throw new Error('STRIPE_SECRET_KEY environment variable is required');
  }

Además:
1. Rotar la key comprometida inmediatamente en el dashboard de Stripe
2. Agregar `STRIPE_SECRET_KEY` al `.env.example` sin valor
3. Verificar que `.env` está en `.gitignore`
4. Revisar el historial de git para eliminar la key de commits anteriores

**Referencia:** rules/security.md → Secrets y Credenciales | rules/general.md → Secrets

---

### 🟡 WARNING

🟡 **Complejidad: Función con nesting excesivo y múltiples responsabilidades**

**Archivo:** `src/services/order.service.ts` líneas 78-142

**Hallazgo:**
La función `processOrder` tiene 64 líneas, 6 niveles de nesting y maneja
validación, cálculo de precios, aplicación de descuentos, verificación de
inventario y envío de notificaciones.

**Por qué importa:**
La función es difícil de entender, testear y modificar. Cualquier cambio en
una responsabilidad requiere entender y arriesgar todas las demás.

**Sugerencia:**
Extraer en funciones con responsabilidad única:

  async function processOrder(order: Order): Promise<ProcessedOrder> {
    const validatedOrder = validateOrder(order);
    const pricedOrder = calculatePricing(validatedOrder);
    const discountedOrder = applyDiscounts(pricedOrder);

    await verifyInventory(discountedOrder);
    const confirmedOrder = await confirmOrder(discountedOrder);

    await notifyOrderConfirmation(confirmedOrder);

    return confirmedOrder;
  }

**Referencia:** rules/general.md → Complejidad | SOLID → Single Responsibility

---

### 🟡 WARNING

🟡 **Error Handling: Errores silenciados en llamada a servicio externo**

**Archivo:** `src/services/notification.service.ts` líneas 23-30

**Hallazgo:**

  async function sendEmail(to: string, template: string) {
    try {
      await emailProvider.send(to, template);
    } catch (error) {
      // TODO: handle this
    }
  }

**Por qué importa:**
Si el envío de email falla, nadie se entera. No hay logging, no hay retry,
no hay alerta. Los usuarios podrían no recibir emails críticos (confirmación
de compra, reset de password) sin que el equipo lo detecte.

**Sugerencia:**

  async function sendEmail(to: string, template: string): Promise<void> {
    try {
      await emailProvider.send(to, template);
      logger.info('Email sent successfully', { to: maskEmail(to), template });
    } catch (error) {
      logger.error('Failed to send email', {
        to: maskEmail(to),
        template,
        error: error.message,
      });
      // Dependiendo de la criticidad:
      // Opción A: Re-throw para que el caller decida
      throw new EmailDeliveryError(
        `Failed to send ${template} email`,
        { cause: error }
      );
      // Opción B: Encolar para retry
      // await emailQueue.add({ to, template, retryCount: 0 });
    }
  }

**Referencia:** rules/general.md → Error Handling

---

### 🔵 SUGGESTION

🔵 **Legibilidad: Extraer magic numbers a constantes con nombre descriptivo**

**Archivo:** `src/services/pricing.service.ts` líneas 15, 23, 31

**Hallazgo:**

  if (order.total > 1000) { ... }
  const discount = order.total * 0.15;
  if (items.length > 50) { ... }

**Por qué importa:**
Los números mágicos no comunican intención. Otro desarrollador (o tú en 3 meses)
no sabrá por qué 1000, 0.15 o 50 son esos valores específicos.

**Sugerencia:**

  const FREE_SHIPPING_THRESHOLD = 1000;
  const BULK_DISCOUNT_RATE = 0.15;
  const BULK_ORDER_MIN_ITEMS = 50;

  if (order.total > FREE_SHIPPING_THRESHOLD) { ... }
  const discount = order.total * BULK_DISCOUNT_RATE;
  if (items.length > BULK_ORDER_MIN_ITEMS) { ... }

**Referencia:** rules/general.md → DRY

---

### 🔵 SUGGESTION

🔵 **Testing: Agregar tests para los nuevos edge cases**

**Archivo:** `src/services/order.service.ts`

**Hallazgo:**
La nueva lógica de descuentos por volumen no tiene tests para:
- Exactamente 50 items (boundary)
- Descuento combinado con cupón (¿se acumulan? ¿cuál tiene prioridad?)
- Orden con items de precio 0

**Por qué importa:**
Los edge cases son donde más bugs ocurren. Sin tests, cualquier refactor
futuro podría romper estos escenarios sin que nadie lo note.

**Sugerencia:**

  describe('applyDiscounts', () => {
    it('should apply bulk discount at exactly 50 items', () => {
      const order = createOrder({ itemCount: 50, total: 5000 });
      const result = applyDiscounts(order);
      expect(result.discount).toBe(750); // 5000 * 0.15
    });

    it('should not stack bulk discount with coupon beyond max', () => {
      const order = createOrder({
        itemCount: 100,
        total: 10000,
        coupon: 'SAVE20',
      });
      const result = applyDiscounts(order);
      expect(result.discount).toBeLessThanOrEqual(
        order.total * MAX_DISCOUNT_RATE
      );
    });

    it('should handle items with zero price gracefully', () => {
      const order = createOrder({ items: [{ price: 0, qty: 5 }] });
      const result = applyDiscounts(order);
      expect(result.total).toBe(0);
      expect(result.discount).toBe(0);
    });
  });

**Referencia:** rules/team-conventions.md → Testing

---

### 💡 NIT

💡 **Formato: Import no utilizado**

**Archivo:** `src/controllers/user.controller.ts` línea 3

**Hallazgo:**

  import { Logger, Formatter, Validator } from '../utils';
  // Formatter no se usa en ninguna parte del archivo

**Sugerencia:**

  import { Logger, Validator } from '../utils';

**Referencia:** rules/general.md → Imports/Dependencies

---

### 💡 NIT

💡 **Naming: Nombre de variable no refleja su contenido**

**Archivo:** `src/services/report.service.ts` línea 45

**Hallazgo:**

  const data = await fetchMonthlySalesReport(startDate, endDate);

**Sugerencia:**

  const monthlySalesReport = await fetchMonthlySalesReport(startDate, endDate);

**Referencia:** rules/general.md → Naming

---

## Guía de Tono

### ✅ Tono Correcto
- Constructivo y respetuoso
- Enfocado en el código, no en la persona
- Ofrece solución, no solo señala el problema
- Reconoce cuando es preferencia vs requisito
- Usa "podríamos", "sugiero", "considera" para suggestions/nits
- Usa lenguaje directo pero no agresivo para blockers

### ❌ Tono Incorrecto
- "¿Por qué hiciste esto?" → "Este approach tiene el riesgo de..."
- "Esto está mal" → "Esto podría causar [problema específico]"
- "Obvio que debería ser..." → "Considera usar X porque..."
- "No entiendo por qué..." → "¿Podrías explicar la razón detrás de...?"
- Sarcasmo, condescendencia o referencias a seniority

### Cuándo Pedir Contexto
A veces el código tiene una razón no obvia. Antes de marcar como error, preguntar:

  "Veo que [descripción]. ¿Hay alguna razón específica para este approach?
  Mi concern es [explicar preocupación]. Si no hay restricción, sugeriría
  [alternativa] porque [beneficio]."