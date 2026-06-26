# Circuit Blocks

Use this for reusable schematic topologies.

## USB-C Sink

- Tie receptacle VBUS pins to `VBUS`.
- Tie receptacle GND pins and shield/EP to `GND` unless a special shield scheme is requested.
- Tie duplicated D+ pins to `USB_DP`, duplicated D- pins to `USB_DN`.
- Add `5.1k` pulldown from `CC1` to `GND` and `5.1k` pulldown from `CC2` to `GND`.
- Add ESD protection when the request includes robustness, productization, or PCB-ready production.

## 3.3 V LDO Rail

- `VIN/VBUS -> LDO VIN`.
- `LDO VOUT -> 3V3`.
- Input and output capacitors to `GND`.
- Local `100nF` near each IC/module power pin.
- Check dropout and current. Avoid AMS1117 for high current or battery-low dropout designs unless explicitly acceptable.

## MCU / Module Minimum System

- Connect every VDD/VSS/GND pin.
- Add reset/enable pullups and boot-mode resistors.
- Add local decoupling and bulk capacitance.
- Expose UART/SWD/JTAG/programming pins.
- Break out useful GPIOs to headers with readable labels.

## UART Bridge

- Cross TX/RX: bridge `TXD` to MCU `RXD`, bridge `RXD` to MCU `TXD`.
- Power the bridge at the logic level used by the MCU unless datasheet says otherwise.
- Expose `DTR_N`/`RTS_N` when auto-reset/auto-boot is expected.

## I2C

- Add pullups to the target logic rail unless already on the module.
- Label `I2C_SCL` and `I2C_SDA`.
- Add connector power and ground.

## SPI

- Label `SPI_MOSI`, `SPI_MISO`, `SPI_SCK`, and `SPI_CS`.
- Use active-low `CS_N` naming when the target datasheet names chip select active-low.
- Keep high-speed or display buses visually grouped.

## Indicators

- Use `rail -> resistor -> LED -> GND` for power LEDs unless active-low indication is desired.
- Choose resistor values based on rail voltage and LED current; default `1k` for simple low-current indicators.
