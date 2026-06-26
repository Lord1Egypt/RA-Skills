# Design Standards

Use this before substantial schematic work or reviews.

## Intake

Move decisively when the request is clear. Ask one concise question only when a decision changes the circuit materially:

- Input/output voltage or current is unknown for power designs.
- MCU/module variant is ambiguous and affects pins or footprint.
- Connector, package, or mounting style matters mechanically.
- Safety, mains voltage, battery charging, RF, high current, or precision analog is involved.

Otherwise choose conservative defaults and state assumptions at the end.

## Schematic Standard

Every generated schematic should have:

- A named page for the circuit or block.
- A title note describing function, input, output, and revision assumptions.
- Real library components with symbols and footprints when PCB-ready output is implied.
- Clear functional blocks: power, controller, interfaces, connectors, protection, indicators.
- Short wires plus net labels for long connections.
- Consistent net names and power rails.
- Decoupling capacitors near IC/module power pins.
- Pullups/pulldowns on boot, reset, enable, I2C, and configuration pins as needed.
- Programming/debug access for MCUs when relevant.
- Connector pin labels that match net names.

Avoid:

- Hand-drawn fake components when a real part is available.
- Long crossing wires across the sheet.
- Unlabelled power rails.
- Floating configuration pins.
- Creating PCB primitives while a schematic document is active, or schematic primitives while a PCB document is active.

## Net Naming

Use semantic names:

- Power: `VBUS`, `VIN`, `5V`, `3V3`, `1V8`, `GND`, `AGND`, `PGND`, `VBAT`
- USB: `USB_DP`, `USB_DN`, `CC1`, `CC2`, `VBUS`
- UART: `U0TXD`, `U0RXD`, `TXD`, `RXD`, `RTS_N`, `DTR_N`
- I2C: `I2C_SCL`, `I2C_SDA`
- SPI: `SPI_MOSI`, `SPI_MISO`, `SPI_SCK`, `SPI_CS`
- Control: `EN`, `RESET_N`, `BOOT`, `WAKE`, `INT_N`, `CS_N`
- LEDs: `LED_PWR`, `LED_STATUS`, `LED_TX`, `LED_RX`

Use `_N` suffix for active-low signals.

## Quality Gate

Before final response, verify:

- Correct page/document is active.
- Components were actually placed, not only text.
- Critical nets exist by sampling recent wires with `getState_Net()`.
- Power rails and grounds are labelled.
- IC power pins have nearby decoupling or documented assumptions.
- Connectors expose labelled nets.
- The schematic is zoomed to all primitives.

Final response should include page name, main blocks, real parts or substitutions, verification performed, and important electrical assumptions.
