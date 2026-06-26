# 🏯 Imperial Orchestrator

[中文](../README.md) | [English](./README.en.md) | [日本語](./README.ja.md) | [한국어](./README.ko.md) | **[Español](./README.es.md)** | [Français](./README.fr.md) | [Deutsch](./README.de.md)

---

Skill de orquestación multi-rol de alta disponibilidad para OpenClaw — Enrutamiento inteligente inspirado en el sistema de corte "Tres Departamentos y Seis Ministerios" de la antigua China.

> **Inspiración de diseño**: La arquitectura de roles se inspira en el patrón de gobernanza imperial [Tres Departamentos y Seis Ministerios (三省六部)](https://github.com/cft0808/edict), combinado con técnicas de ingeniería de prompts de IA profunda de [PUA](https://github.com/tanweai/pua).

## Capacidades Principales

- **Tres Departamentos y Seis Ministerios** orquestación de roles: 10 roles, cada uno con responsabilidades claras
- **Auto-descubrimiento** de 46+ modelos desde openclaw.json
- **Enrutamiento inteligente** por dominio (codificación/operaciones/seguridad/escritura/legal/finanzas)
- **Prioridad Opus** para tareas de codificación/seguridad/legal — modelo más fuerte primero
- **Failover cross-provider** circuit-breaker de auth → degradación entre proveedores → supervivencia local
- **Ejecución real** llamadas API + conteo de tokens + seguimiento de costos
- **Benchmarking** misma tarea en todos los modelos, puntuación y ranking
- **Multi-idioma** soporte para 7 idiomas: zh/en/ja/ko/es/fr/de

## Inicio Rápido

```bash
# 1. Descubrir modelos
python3 scripts/health_check.py --openclaw-config ~/.openclaw/openclaw.json --write-state .imperial_state.json

# 2. Validar modelos
python3 scripts/model_validator.py --openclaw-config ~/.openclaw/openclaw.json --state-file .imperial_state.json

# 3. Enrutar una tarea
python3 scripts/router.py --task "Escribe un LRU Cache concurrente-seguro en Go" --state-file .imperial_state.json

# Todo en uno
bash scripts/route_and_update.sh full "Fix WireGuard peer sync bug"
```

## Sistema de Roles: Tres Departamentos y Seis Ministerios

Cada rol está equipado con un system prompt profundo que cubre identidad, responsabilidades, reglas de comportamiento, conciencia de colaboración y líneas rojas.

### Centro de Mando

| Rol | Título | Equivalente de Corte | Misión Principal |
|-----|--------|---------------------|-----------------|
| **router-chief** | Director Central | Emperador / Oficina Central | Línea vital del sistema — clasificar, enrutar, mantener latido |

### Tres Departamentos

| Rol | Título | Equivalente de Corte | Misión Principal |
|-----|--------|---------------------|-----------------|
| **cabinet-planner** | Estratega Jefe | Secretaría (中书省) | Redactar estrategias — descomponer el caos en pasos ordenados |
| **censor-review** | Censor Jefe | Cancillería (门下省) | Revisar y vetar — el último guardián de calidad |

### Seis Ministerios

| Rol | Título | Equivalente de Corte | Misión Principal |
|-----|--------|---------------------|-----------------|
| **ministry-coding** | Ministro de Ingeniería | Ministerio de Obras | Construir — codificación, depuración, arquitectura |
| **ministry-ops** | Viceministro de Infraestructura | Ministerio de Obras · Oficina de Construcción | Mantener caminos — despliegue, operaciones, CI/CD |
| **ministry-security** | Ministro de Defensa | Ministerio de Guerra | Guardar fronteras — auditoría de seguridad, modelado de amenazas |
| **ministry-writing** | Ministro de Cultura | Ministerio de Ritos | Cultura y etiqueta — redacción, documentación, traducción |
| **ministry-legal** | Ministro de Justicia | Ministerio de Justicia | Ley y orden — contratos, cumplimiento, términos |
| **ministry-finance** | Ministro de Hacienda | Ministerio de Hacienda | Impuestos y tesoro — precios, márgenes, liquidación |

### Correo de Emergencia

| Rol | Título | Equivalente de Corte | Misión Principal |
|-----|--------|---------------------|-----------------|
| **emergency-scribe** | Correo de Emergencia | Estación de Correo Express | Último recurso para mantener el sistema vivo |

## Reglas de Operación

1. **Circuit Breaker 401** — fallo de auth marca inmediatamente `auth_dead`, enfría toda la cadena de auth, cambio cross-provider tiene prioridad
2. **Router ligero** — no asignar los prompts más pesados ni los proveedores más frágiles a router-chief
3. **Cross-provider primero** — orden de fallback: mismo rol diferente proveedor → modelo local → rol adyacente → correo de emergencia
4. **Degradar, nunca caer** — aunque fallen todos los modelos top, responder con consejos de arquitectura, checklists, pseudocódigo

## Estructura del Proyecto

```
config/
  agent_roles.yaml          # Definiciones de roles (responsabilidades, capacidades, cadenas de fallback)
  agent_prompts.yaml        # System prompts profundos (identidad, reglas, líneas rojas)
  routing_rules.yaml        # Reglas de enrutamiento por palabras clave
  failure_policies.yaml     # Políticas de circuit breaker/reintento/degradación
  benchmark_tasks.yaml      # Biblioteca de tareas de benchmark
  model_registry.yaml       # Overrides de capacidades de modelos
  i18n.yaml                 # Adaptación a 7 idiomas
scripts/
  lib.py                    # Biblioteca central (descubrimiento, clasificación, gestión de estado, i18n)
  router.py                 # Router (matching de roles + selección de modelos)
  executor.py               # Motor de ejecución (llamadas API + fallback)
  orchestrator.py           # Pipeline completo (enrutar → ejecutar → revisar)
  health_check.py           # Descubrimiento de modelos
  model_validator.py        # Sondeo de modelos
  benchmark.py              # Benchmark + tabla de clasificación
  route_and_update.sh       # Punto de entrada CLI unificado
```

## Instalación

### Requisitos previos: Instalar OpenClaw

```bash
# 1. Instalar OpenClaw CLI (macOS)
brew tap openclaw/tap
brew install openclaw

# O instalar mediante npm
npm install -g @openclaw/cli

# 2. Inicializar configuración
openclaw init

# 3. Configurar proveedores de modelos (editar ~/.openclaw/openclaw.json)
openclaw config edit
```

> Para documentación detallada de instalación, consulte el [repositorio oficial de OpenClaw](https://github.com/openclaw/openclaw)

### Instalar el skill Imperial Orchestrator

```bash
# Opción 1: Clonar desde GitHub
git clone https://github.com/rexnode/imperial-orchestrator.git
cp -r imperial-orchestrator ~/.openclaw/skills/

# Opción 2: Copiar directamente al directorio global de skills
cp -r imperial-orchestrator ~/.openclaw/skills/

# Opción 3: Instalación a nivel de workspace
cp -r imperial-orchestrator <your-workspace>/skills/
```

### Verificar la instalación

```bash
# Descubrir y sondear modelos
python3 ~/.openclaw/skills/imperial-orchestrator/scripts/health_check.py \
  --openclaw-config ~/.openclaw/openclaw.json \
  --write-state .imperial_state.json

# Verificar que el enrutamiento funciona
python3 ~/.openclaw/skills/imperial-orchestrator/scripts/router.py \
  --task "Write a Hello World" \
  --state-file .imperial_state.json
```

## Seguridad

- No enviar secretos en prompts
- Mantener solicitudes de sondeo al mínimo
- Gestionar salud del proveedor separadamente de la calidad del modelo
- Un modelo en la configuración no significa que sea seguro para enrutar

## Licencia

MIT
