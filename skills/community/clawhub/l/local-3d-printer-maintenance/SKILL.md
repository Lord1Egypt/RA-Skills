# Local-Only 3D Printer Maintenance Assistant

## Overview
A fully offline diagnostic and maintenance assistant for FDM 3D printers.  
Runs entirely on local LLMs through OpenClaw with zero cloud dependencies.

## Capabilities
- Text-based troubleshooting for print failures  
- Step-by-step maintenance protocols  
- Premium image-based failure analysis (LLaVA)  
- Automatic calibration G-code generation  
- Tuning profile save/load system  
- Maintenance log export to CSV  

## Workflows
- `troubleshoot` — Diagnose print issues using text input  
- `maintenance` — Provide guided maintenance procedures  
- `vision_analysis` — Analyze print failures from images (premium)  
- `generate_gcode` — Create calibration G-code (premium)  
- `manage_profiles` — Save/load tuning profiles  
- `export_logs` — Export maintenance logs  

## Actions
- `local_llm_text` — Runs text prompts through local Llama3  
- `local_llm_vision` — Runs image prompts through LLaVA  
- `gcode_generator` — Generates calibration G-code  
- `profile_manager` — Manages tuning profiles  
- `log_exporter` — Outputs CSV maintenance logs  

## Requirements
- OpenClaw v1.2.0+  
- Ollama installed  
- Models: `llama3`, `llava`  

## Tiers
- **Free:** Troubleshooting, maintenance, basic guidance  
- **Premium:** Vision analysis, G-code generation, profile manager, log export  

## Notes
This skill does **not** control printers or hardware.  
All operations are informational and file‑based only.
