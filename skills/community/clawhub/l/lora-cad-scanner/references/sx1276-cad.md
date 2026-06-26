# SX1276 CAD Register Reference

## Key Registers for CAD

| Register | Address | Description |
|---|---|---|
| `REG_OP_MODE` | 0x01 | Operating mode control |
| `REG_IRQ_FLAGS` | 0x12 | IRQ status flags |
| `REG_RSSI_WIDEBAND` | 0x2C | Wideband RSSI (no demodulation) |
| `REG_MODEM_CONFIG_1` | 0x1D | BW [7:4], CodingRate [3:1], ImplicitHdr [0] |
| `REG_MODEM_CONFIG_2` | 0x1E | SF [7:4], TxCont [3], RxCRC [2], SymTimeout [1:0] |
| `REG_VERSION` | 0x42 | Chip version (SX1276 = 0x12) |

## OP_MODE Values (LoRa mode = bit7 set)

| Value | Mode |
|---|---|
| 0x80 | SLEEP |
| 0x81 | STANDBY |
| 0x82 | FSTX |
| 0x83 | TX |
| 0x84 | FSRX |
| 0x85 | RXCONTINUOUS |
| 0x86 | RXSINGLE |
| 0x87 | **CAD** |

## IRQ_FLAGS Bits

| Bit | Name | Description |
|---|---|---|
| 7 | RxTimeout | RX timeout |
| 6 | RxDone | Packet received |
| 5 | PayloadCrcError | CRC error |
| 4 | ValidHeader | Valid header received |
| 3 | TxDone | TX complete |
| 2 | **CadDone** | CAD complete (poll this) |
| 1 | FhssChangeChannel | FHSS hop |
| 0 | **CadDetected** | LoRa preamble detected |

## CAD Sequence

```cpp
// 1. Clear all IRQ flags
writeReg(0x12, 0xFF);

// 2. Trigger CAD mode
writeReg(0x01, 0x87);

// 3. Poll CadDone (bit 2)
while (!(readReg(0x12) & 0x04)) {
    if (timeout) break;
}

// 4. Check CadDetected (bit 0)
bool hit = (readReg(0x12) & 0x01) != 0;

// 5. Return to standby
writeReg(0x12, 0xFF);  // clear flags
writeReg(0x01, 0x81);  // standby
```

## BW Register Values (REG_MODEM_CONFIG_1 bits [7:4])

| Code | Bandwidth |
|---|---|
| 0 | 7.8 kHz |
| 1 | 10.4 kHz |
| 2 | 15.6 kHz |
| 3 | 20.8 kHz |
| 4 | 31.25 kHz |
| 5 | 41.7 kHz |
| 6 | **62.5 kHz** |
| 7 | **125 kHz** |
| 8 | **250 kHz** |
| 9 | **500 kHz** |

## CAD Duration

CAD duration ≈ 2^SF / BW × 2 symbols. Approximate timeouts:

| SF | BW=125kHz | BW=500kHz |
|---|---|---|
| SF6 | ~1 ms | ~0.25 ms |
| SF9 | ~8 ms | ~2 ms |
| SF12 | ~64 ms | ~16 ms |

Use 400 ms timeout as safe upper bound for all SF/BW combos.

## RSSI Calculation

```cpp
// Wideband RSSI (no packet needed, works in any mode after brief RX)
int rssi = -157 + readReg(0x2C);  // SX1276 (HF port)
// For LF port (< 868 MHz): rssi = -164 + readReg(0x2C)
```
