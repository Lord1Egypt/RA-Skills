# Local-Only 3D Printer Maintenance Assistant
A fully offline, privacy‑first diagnostic and maintenance system for FDM 3D printers.  
Powered entirely by local LLMs (Llama3 + LLaVA) through OpenClaw — no cloud, no telemetry, no external dependencies.

## Overview
This skill provides a complete maintenance and troubleshooting toolkit for 3D printers, including:

- Text-based troubleshooting for common print failures  
- Step-by-step maintenance protocols  
- Premium image-based failure analysis (LLaVA)  
- Automatic calibration G-code generation  
- Tuning profile management  
- Maintenance log export to CSV  
- 100% offline execution

Designed for users who want a powerful AI assistant without sacrificing privacy or hardware safety.

---

## Features

### 🔧 Troubleshooting
Diagnose issues like:
- Stringing  
- Under-extrusion  
- Bed adhesion problems  
- Layer shifting  
- Warping  
- Nozzle clogs  

### 🧽 Maintenance
Guided procedures for:
- Hotend cleaning  
- Bed leveling  
- Z-offset calibration  
- PEI sheet care  
- Belt tensioning  
- Extruder inspection  

### 🖼️ Vision Analysis (Premium)
Upload a photo of a failed print and receive:
- Failure classification  
- Root-cause analysis  
- Corrective actions  
- Preventative recommendations  

### 🧪 G-code Generation (Premium)
Generate calibration files for:
- Retraction  
- Flow rate  
- Temperature towers  
- Bed leveling patterns  

### 📁 Profile Manager
Save and load tuning profiles for different materials or printers.

### 📊 Log Export
Export maintenance logs to CSV for tracking long-term printer health.

---

## Requirements
- **Ollama** installed and running  
- Models:
  - `llama3`
  - `llava`
- **OpenClaw v1.2.0+**

---

## Installation
Place the folder into your OpenClaw skills directory:

