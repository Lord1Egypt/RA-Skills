<div align="center">

# MediaSync-Claw: Servidor Multimedia P2P Remoto y Skill de Streaming para OpenClaw

[English](README.md) | [简体中文](README_ZH.md) | [日本語](README_JA.md) | [Deutsch](README_DE.md) | [Español](README_ES.md)

</div>

---

## 📖 Descripción General y Valor Principal

**MediaSync-Claw** es un **Skill de OpenClaw** y un **Servidor Multimedia P2P Remoto** diseñado para compartir y reproducir archivos de video y audio personales.

Su objetivo principal es permitir a los usuarios acceder, indexar y transmitir su biblioteca multimedia local **en cualquier momento y lugar a través de WhatsApp** mediante el agente de IA OpenClaw. La lista multimedia generada es compatible con la reproducción de alta velocidad en **AIpollo Player** mediante conexiones P2P.

---

## ⚙️ Requisitos Previos

* **OpenClaw**: Asegúrate de tener OpenClaw instalado y en ejecución localmente.
* **Excepción de Firewall / Antivirus**: Agrega una regla de confianza para `frpc.exe` en Windows Defender o tu software de seguridad. *Garantizamos que `frpc.exe` es completamente seguro y original.*

---

## 🚀 Guía de Instalación y Uso

1. **Descarga e Instalación**: Descarga o clona este repositorio dentro del directorio de skills de OpenClaw.
2. **Configura la Carpeta de Videos**: Crea una carpeta llamada `videos` dentro del directorio del skill y coloca los archivos MP4 que deseas reproducir.
3. **Conecta WhatsApp**: Configura e integra tu canal de WhatsApp en OpenClaw.
4. **Ejecuta el Skill**: Inicia el skill MediaSync-Claw en OpenClaw.
5. **Comandos Remotos por WhatsApp**: En tu chat de WhatsApp, escribe comandos en lenguaje natural (por ejemplo, para listar, buscar o reproducir videos de tu biblioteca local) para obtener la lista de medios.
6. **Reproducción Inmediata**: Haz clic en el enlace generado para comenzar la transmisión en AIpollo Player.

---

## 🔒 Divulgación de Seguridad y Gestión de Riesgos

### Riesgo 1: Enrutamiento Público mediante Proxy Inverso FRP
Para facilitar la transmisión fuera de tu red local, este skill establece un túnel de salida mediante el cliente FRP (`frpc`) hacia un servidor de retransmisión (`frps`), permitiendo el acceso a través del dominio `*.yunfrp.net`.

### Riesgo 2: Transmisión HTTP y Arquitectura P2P
La transmisión de video real se realiza mediante **conexiones directas P2P**. El protocolo HTTP se utiliza exclusivamente para recibir instrucciones ligeras de control y no transmite datos personales sensibles.

### Riesgo 3: Descarga de Binarios `frpc.exe`
Para garantizar la máxima seguridad en la cadena de suministro, el ejecutable `frpc.exe` se descarga directamente desde los Releases oficiales de GitHub.

---

## 🛡️ Recomendaciones de Seguridad

* **Servidor Dedicado / Máquina Virtual**: Para una seguridad óptima, se recomienda ejecutar este servicio en un dispositivo secundario o dentro de una Máquina Virtual (VM) aislada.
* **Mantenimiento Periódico**: Mantén actualizados tu sistema operativo y el entorno OpenClaw con los últimos parches de seguridad.

---

## 💻 Compatibilidad de Plataforma

* **Soporte Actual**: Windows (x64)
* **Próximamente**: Soporte para Linux y macOS en desarrollo.

*Si necesitas soporte para otras plataformas o tienes dudas, abre un Issue en GitHub. ¡Gracias por tu confianza y apoyo!*