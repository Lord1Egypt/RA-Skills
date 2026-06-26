# 🔍 li_sentry_check - Habilidad de Inspección de Servidores

> Habilidad multiplataforma de inspección y verificación de salud de servidores. Acceso SSH a servidores Linux remotos mediante autenticación por clave, ejecución de comandos de inspección de solo lectura y generación de informes estructurados en Markdown.

[![Versión](https://img.shields.io/badge/versión-0.1.0-blue.svg)](https://clawhub.ai/skills/li_sentry_check)
[![Plataformas](https://img.shields.io/badge/plataformas-nanobot%20%7C%20OpenClaw%20%7C%20Hermes-green.svg)]()
[![Licencia](https://img.shields.io/badge/licencia-MIT-green.svg)](LICENSE)

## 📋 Resumen

`li_sentry_check` es una habilidad de inspección de servidores multiplataforma que soporta **nanobot**, **OpenClaw** y **Hermes agent**. Se conecta a servidores Linux remotos mediante autenticación por clave SSH, ejecuta comandos de inspección de solo lectura (CPU, memoria, disco, red, servicios, seguridad) y genera informes Markdown estructurados con resaltado automático de anomalías.

## ✨ Funcionalidades Principales

| Funcionalidad | Descripción |
|---------------|-------------|
| 🔐 Autenticación por Clave SSH | Solo autenticación por clave, acceso con contraseña deshabilitado, seguridad reforzada |
| 📊 Inspección de Hardware | CPU, memoria, disco, uso de red |
| 🖥️ Inspección de Servicios | Estado de servicios clave, registros de errores |
| 🛡️ Inspección de Seguridad | Inicios de sesión SSH anómalos, alertas de firewall, errores del kernel |
| 📝 Informes Estructurados | Formato Markdown/JSON, anomalías prioritarias |
| 🌐 Multiplataforma | Soporta nanobot, OpenClaw, Hermes |

## 🚀 Inicio Rápido

### 1. Instalar la Habilidad

```bash
# nanobot
./manage.sh skill install li_sentry_check

# OpenClaw
npx clawhub@latest install li_sentry_check

# Hermes
hermes skill install li_sentry_check
```

### 2. Configurar Claves SSH

```bash
# Generar par de claves
ssh-keygen -t rsa -b 4096 -f ~/.ssh/li_sentry_check -N ""

# Copiar clave pública al servidor remoto
ssh-copy-id -i ~/.ssh/li_sentry_check.pub inspector@<IP_SERVIDOR>

# Probar conexión
ssh -i ~/.ssh/li_sentry_check inspector@<IP_SERVIDOR>
```

### 3. Configurar Servidores Objetivo

Editar `references/targets.yaml`:

```yaml
targets:
  producción-web:
    host: TU_IP_SERVIDOR
    port: 22
    user: inspector
    keyPath: ~/.ssh/li_sentry_check
    services:
      - nginx
      - docker
      - sshd
```

### 4. Ejecutar Inspección

```bash
# Inspección básica (recursos de hardware)
python3 scripts/inspect.py --target producción-web --checks basic

# Inspección de servicios
python3 scripts/inspect.py --target producción-web --checks services

# Inspección completa (básica + servicios + seguridad + registros)
python3 scripts/inspect.py --target producción-web --checks daily

# Salida en formato JSON
python3 scripts/inspect.py --target producción-web --checks daily --format json

# Salida a archivo
python3 scripts/inspect.py --target producción-web --checks daily --output informe.md
```

## 📖 Grupos de Verificación de Inspección

| Grupo | Contenido | Comandos |
|-------|-----------|----------|
| `basic` | CPU, memoria, disco, red | 8 |
| `services` | Estado de servicios + registros de errores (dinámico) | 3×N |
| `daily` | Inspección completa (básica + servicios + seguridad + registros) | 26 |

## 📊 Ejemplo de Informe

```markdown
# 🔍 Informe de Inspección de Servidor

- Objetivo: producción-web
- Host: TU_IP_SERVIDOR
- Usuario: inspector
- Verificaciones: daily
- Iniciado: 2026-04-26T09:00:00+00:00
- Total verificaciones: 26
- ⚠️ Anomalías: 3

## Estado General: ⚠️ ADVERTENCIA

## ⚠️ Anomalías (Prioridad)

### ⚠️ systemd_failed_units
Comando: `systemctl --failed --no-pager`
Estado: OK (contiene anomalías)

Salida:
```
UNIT          LOAD   ACTIVE SUB    DESCRIPTION
mcelog.service loaded failed failed Machine Check Exception Logging Daemon
```
```

## 🔧 Opciones de Línea de Comandos

| Opción | Descripción | Predeterminado |
|--------|-------------|----------------|
| `--target` | Nombre del servidor objetivo (definido en targets.yaml) | (obligatorio) |
| `--checks` | Grupo de verificación: `basic`, `services`, `daily` | `basic` |
| `--format` | Formato de salida: `markdown`, `json` | `markdown` |
| `--output` | Salida a archivo (predeterminado: stdout) | stdout |

## 🌐 Soporte Multiplataforma

| Plataforma | Entorno | Script | Comando |
|------------|---------|--------|---------|
| **OpenClaw** | Node.js 24+ | `scripts/inspect.mjs` | `node scripts/inspect.mjs --target bogon --checks daily` |
| **NanoBot** | Python 3.10+ | `scripts/inspect.py` | `python3 scripts/inspect.py --target bogon --checks daily` |
| **Hermes** | Python 3.10+ | `scripts/inspect.py` | `python3 scripts/inspect.py --target bogon --checks daily` |

## 📁 Estructura de Archivos

```
li_sentry_check/
├── SKILL.md                  # Documentación de la habilidad
├── _meta.json                # Metadatos de la habilidad
├── design.md                 # Documentación de diseño
├── references/
│   ├── targets.yaml          # Configuración de servidores objetivo
│   └── checks.yaml           # Lista blanca de comandos de inspección
└── scripts/
    ├── inspect.mjs           # Implementación Node.js (OpenClaw)
    └── inspect.py            # Implementación Python (NanoBot/Hermes)
```

## 🔒 Mejores Prácticas de Seguridad

- **Permisos de clave**: `chmod 600 ~/.ssh/li_sentry_check`
- **Verificación de host**: Para producción, pre-rellenar `known_hosts` en lugar de usar `accept-new`
- **Nombres de servicios**: Solo alfanumérico, guiones, guiones bajos permitidos (validados antes del uso)
- **Lista blanca de comandos**: Nunca modificar `checks.yaml` con comandos que cambien el estado
- **Manejo de informes**: Los informes pueden contener datos del sistema — no compartir públicamente

## 🔧 Guía de Extensión

### Agregar un Nuevo Servidor Objetivo

Editar `references/targets.yaml`:

```yaml
targets:
  servidor-base-datos:
    host: TU_IP_SERVIDOR
    port: 22
    user: inspector
    keyPath: ~/.ssh/li_sentry_check
    services:
      - mysql
      - redis
```

### Agregar un Nuevo Grupo de Verificación

Editar `references/checks.yaml`:

```yaml
checks:
  base-datos:
    description: Inspección de base de datos
    commands:
      - id: mysql_status
        cmd: "systemctl status mysql --no-pager | sed -n '1,20p'"
        timeoutSec: 10
      - id: mysql_connections
        cmd: "mysql -e 'SHOW STATUS LIKE \"Threads_connected\"' || true"
        timeoutSec: 15
```

## 📝 Historial de Versiones

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 0.1.0 | 2026-04-26 | Versión inicial: inspección básica, de servicios y completa |

## 📄 Licencia

Licencia MIT
