# Build specification — implement exactly

1. Write kernel modules P0, P1, P3, P5  
2. Write agent: ollama client, limbs, smart_disk_agent HTTP server  
3. Write portal UI (chat, health, limbs)  
4. Write launchers BOOT/STOP  
5. Write firmware seal  
6. Write tests + self_check  
7. Run tests; fix until green  

**Ports:** agent `9631`, Ollama `11434`  
**Auth:** none on loopback  
**Brand:** LYGO SMART DISK AGENT only  
