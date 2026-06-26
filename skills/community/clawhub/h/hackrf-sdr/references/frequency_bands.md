# Frequency Band Reference

Common allocations in the 3.2-3.4 GHz (S-band) range:

| Range (MHz) | Typical Use |
|---|---|
| 3100-3300 | Radar (S-band, meteorological, air traffic control) |
| 3200-3300 | Satellite downlink (S-band, e.g. LEO comms) |
| 3300-3400 | 5G NR n78 band (3400-3800), WiMAX |
| 3300-3400 | Radio astronomy (protected in some regions) |
| 3400-3600 | 5G NR n78 / fixed satellite service |

## Signal Classification Cheat Sheet

| Modulation | Amplitude CV | Phase std | IQ Constellation |
|---|---|---|---|
| CW | <0.02 | <0.05 deg | Single point |
| AM | >0.15 | <0.1 deg | Line along I axis |
| FM/FSK | <0.05 | >2 deg | Circle |
| PSK (BPSK) | <0.05 | <0.5 deg | 2 points |
| PSK (QPSK) | <0.05 | <0.5 deg | 4 points |
| QAM | 0.05-0.15 | 0.5-2 deg | Grid pattern |
| OFDM | >0.2 | >5 deg | Diffuse cloud |

## HackRF One Specs

- Frequency: 1 MHz - 6 GHz
- Sample rate: 2-20 MSPS
- Bandwidth: up to 20 MHz
- Resolution: 8-bit I/Q
- Modes: RX, TX, full duplex
- LNA gain: 0-40 dB (8 dB steps)
- VGA gain: 0-62 dB (2 dB steps)