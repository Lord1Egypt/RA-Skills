# Parts Strategy

Use this when choosing real EasyEDA/JLC/LCSC library components.

Search exact part names first, then generic descriptions.

| Function | Preferred queries |
| --- | --- |
| 0603 1 k resistor | `0603WAF1001T5E`, `1k 0603 resistor` |
| 0603 10 k resistor | `0603WAF1002T5E`, `10k 0603 resistor` |
| 0603 5.1 k resistor | `0603WAF5101T5E`, `5.1k 0603` |
| 0603 100 nF capacitor | `CC0603KRX7R9BB104`, `100nF 0603` |
| 0603 10 uF capacitor | `CL10A106KP8NNNC`, `10uF 0603` |
| Indicator LED | `KT-0603R`, `LED 0603 red` |
| USB-C receptacle | `USB Type-C 16P` |
| USB-UART | `CH340C`, `CH343P`, `CP2102` |
| LDO | `AMS1117-3.3`, `ME6211`, `XC6206` |
| Buck converter | exact regulator IC, then `buck converter` |
| Tact switch | `TS-1102S`, `tact switch 4P` |
| Headers | `HDR-M-2.54`, `2.54 header` |
| ESP32 | `ESP32-WROOM-32`, `ESP32-C3` |
| STM32 | exact STM32 part, e.g. `STM32F103C8T6` |

Prefer parts that have:

- Symbol and footprint.
- Correct value/package.
- LCSC supplier part metadata.
- Basic Part status when suitable.
- Datasheet link or reputable manufacturer.

If a preferred part is unavailable, choose the closest result with symbol and footprint and label the value clearly.
