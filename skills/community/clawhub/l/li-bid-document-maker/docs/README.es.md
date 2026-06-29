# li-bid-document-maker — Guía de uso

> **Experto en licitaciones** — Convierte automáticamente documentos de licitación en respuestas profesionales orientadas a los criterios de puntuación

## Instalación

```bash
clawhub install li-bid-document-maker
```

## Inicio rápido

Después de instalar, active la habilidad diciendo cualquiera de las siguientes frases a su asistente de IA:

- "Crear una respuesta a una licitación"
- "Analizar esta licitación y generar una propuesta"
- "Ayúdame a preparar una oferta"
- "Generar una respuesta a esta RFP"

La IA ejecutará automáticamente un flujo de trabajo de 6 etapas: **Analizar licitación → Análisis estratégico → Generar esquema → Redactar capítulos → Control de calidad → Mejora PDCA**

## Uso

### Método 1: Subir archivo

Arrastre y suelte el documento de licitación (PDF o Word) en el chat, luego diga:
> "Usa li-bid-document-maker para analizar este documento"

### Método 2: Especificar ruta del archivo

> "Usa li-bid-document-maker, el archivo de licitación está en /projects/tender.pdf"

## Requisitos del sistema

| Elemento | Requisito |
|----------|-----------|
| SO | Windows 10/11, macOS, Ubuntu 20.04+ |
| Plataforma IA | Claude, OpenClaw, Hermes, o cualquier LLM Agent con soporte de E/S de archivos |
| Formato de archivo | PDF (preferiblemente con búsqueda) o Word (.docx) |
| Dependencias | `python-docx`, `PyPDF2` (para procesamiento de archivos, opcional) |

## Resultado

- Documento de propuesta completo (estructura estándar de 16 capítulos)
- Informe de mejora de calidad PDCA
- Mapeo de criterios de puntuación con valores

## Flujo de trabajo

```
Etapa 1: Analizar licitación      → Extraer información del proyecto, especificaciones técnicas, criterios
Etapa 2: Análisis estratégico     → Análisis de ponderación, estrategia competitiva
Etapa 3: Generar esquema          → Esquema orientado a puntuación (requiere confirmación del usuario)
Etapa 4: Redactar capítulos       → Escribir contenido sección por sección
Etapa 5: Control de calidad       → Verificación completa de 6 dimensiones
Etapa 6: Mejora PDCA              → 3 rondas de mejora automática, luego entrega
```

## Licencia

MIT-0
