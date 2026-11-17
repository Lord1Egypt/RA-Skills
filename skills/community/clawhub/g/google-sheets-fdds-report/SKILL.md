\---

name: google-sheets-fdds-report

description: Permite leer datos de un documento de Google Sheets con métricas FDDS y actualizar/generar la plantilla de reporte comparando el último día (D-1) contra el mismo día de la semana anterior (W-1).

\---



\# Instrucciones para la habilidad: google-sheets-fdds-report



\## Objetivo

Analizar los datos de rendimiento logístico (FDDS) en un Google Sheet específico y generar la plantilla actualizada de informe con las métricas del último día disponible (D-1) comparado con el mismo día de la semana anterior (W-1).



\## Pestañas requeridas en la Hoja de Cálculo

1\. \*\*Template\*\*: Estructura de ejemplo que se debe rellenar.

2\. \*\*DATA FDDS W\*\*: Datos acumulados y diarios de la semana actual.

3\. \*\*DATA FDDS W-1\*\*: Datos equivalentes de la semana anterior.

4\. \*\*DATA Paquetes\*\*: Registro detallado de envíos y paquetes con fallos.



\## Pasos de ejecución

1\. \*\*Conexión a la Hoja\*\*: Utilizar la API de Google Workspace / Google Sheets para consultar el documento indicado por el usuario.

2\. \*\*Identificación de la fecha D-1\*\*:

&#x20;  - Inspeccionar la pestaña `DATA FDDS W` para localizar la última columna diaria que contenga registros vigentes.

3\. \*\*Cálculo de métricas comparativas\*\*:

&#x20;  - Comparar el día seleccionado contra la misma columna diaria de la semana previa en `DATA FDDS W-1`.

&#x20;  - Extraer:

&#x20;    - `% FDDS` (First Day Delivery Success) y delta vs W-1 en bps.

&#x20;    - Fallos totales (bps) y conteo de envíos.

&#x20;    - Distribución de fallos: \*AMZL Owned\*, \*Central Team Owned\* y \*Not Attempted\*.

&#x20;    - Sub-métricas \*AMZL Owned\*: \*Customer Contact Compliance\*, \*Planned Within Time Window\*, \*Home Unattended Miss\*, \*Defect 100m Radius Compliance\*, etc.

4\. \*\*Generación del reporte\*\*: Sustituir las variables en la estructura de la pestaña `Template` y devolver el reporte en texto o escribirlo de vuelta en el documento según se solicite.

