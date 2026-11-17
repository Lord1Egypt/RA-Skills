---
name: hantek-scope-control
description: Control Hantek DSO2D15 / DSO2000-series oscilloscopes over USB SCPI, including connection checks, channel/generator setup, waveform capture, probe compensation guidance, and remote-control lock handling.
---

# Hantek Scope Control

## Use When

Use this skill when working with a Hantek DSO2D15 or DSO2000-series oscilloscope and the user wants to:

- connect the scope to a computer over USB
- confirm SCPI/VISA communication
- query or change channel, trigger, timebase, or generator settings
- capture waveform data
- troubleshoot remote-control/keypad-lock behavior
- calibrate or identify oscilloscope probes and accessories
- prepare for safe low-voltage electronics or amplifier diagnostics

## Quick Context

SCPI means Standard Commands for Programmable Instruments. It is the plain-text command language many test instruments use so a computer can ask questions like `*IDN?` or set values like `:CHANnel1:SCALe 0.2V`.

VISA is the instrument communication layer used by tools such as PyVISA. It helps software find and talk to USB, serial, LAN, and GPIB instruments.

## Connection Checklist

1. Power on the scope.
2. Connect the computer to the scope's rear USB Device port, not the front USB storage port.
3. Use a real USB data cable.
4. If the operating system asks to allow the USB accessory, approve it locally.
5. Confirm the scope appears as a USB device.
6. Confirm VISA/PyVISA can see a resource.
7. Query `*IDN?` before sending setting changes.

A successful Hantek DSO2000 identity response may look similar to:

```text
undefined, DSO2D15, <serial>, <firmware-version>
```

## Python / PyVISA Notes

Typical dependencies:

```sh
python -m pip install pyvisa pyvisa-py pyusb
```

On macOS, PyVISA-py may need help finding the correct libusb backend. If the scope appears in the system USB tree but PyVISA cannot enumerate it, try installing a libusb provider such as `libusb-package` and explicitly wiring PyUSB to that backend.

Minimal identity test:

```python
import pyvisa

rm = pyvisa.ResourceManager("@py")
resources = rm.list_resources()
print(resources)

inst = rm.open_resource(resources[0])
inst.timeout = 3000
print(inst.query("*IDN?").strip())
```

## Useful SCPI Commands

Identity and basic setup:

```text
*IDN?
ACQuire:POINts?
:ACQuire:SRATe?
:CHANnel1:DISPlay?
:CHANnel1:SCALe?
:CHANnel1:PROBe?
:CHANnel1:COUPling?
:CHANnel1:OFFSet?
:TIMebase:SCALe?
:TRIGger:MODE?
:TRIGger:STATus?
```

Channel setup examples:

```text
:CHANnel1:DISPlay ON
:CHANnel1:COUPling DC
:CHANnel1:PROBe 10
:CHANnel1:SCALe 0.2V
:CHANnel1:OFFSet 0V
```

Trigger setup examples:

```text
:TRIGger:MODE EDGE
:TRIGger:EDGe:SOURce CHANnel1
:TRIGger:EDGe:SLOPe RISIng
:TRIGger:EDGe:LEVel 0V
:TRIGger:SWEep AUTO
:TRIGger:SWEep NORMal
:TRIGger:SWEep SINGle
```

Timebase setup example:

```text
:TIMebase:SCALe 0.0002
:TIMebase:POSition 0
```

Generator / DDS examples, when supported by the model:

```text
:DDS ON
:DDS OFF
:DDS:TYPE SINE
:DDS:TYPE SQUAre
:DDS:TYPE RAMP
:DDS:FREQuency 1000
:DDS:AMPLitude 1
:DDS:OFFSet 0
:DDS:DUTY 50
```

## Waveform Capture

The public SCPI manual documents:

```text
:WAVeform:DATA:ALL?
```

Some DSO2000 units also respond to a private waveform transfer command:

```text
PRIVate:WAVeform:DATA:ALL?
```

When using private or undocumented commands:

- test read-only behavior first
- keep timeouts generous
- save raw bytes before decoding
- do not assume the packet format is stable across firmware versions
- record scope model, firmware version, channel scale, probe factor, timebase, sample rate, and enabled channels with each capture

A practical capture workflow:

1. Query identity and current setup.
2. Set channel/probe/timebase/trigger deliberately.
3. Capture once.
4. Save raw bytes and decoded CSV/JSON.
5. Compare decoded measurements with the scope's on-screen measurements.

## Remote Freeze And Keypad Lock

Remote control may cause the scope to display a message like:

```text
In remote communication, the keypad is locked
```

Treat this as a remote-control state warning. On some units it can remain on screen after the controls are actually released, so verify by whether the front-panel controls respond.

Documented single trigger:

```text
:TRIGger:SWEep SINGle
```

This waits for one trigger, displays the captured waveform, then stops. On some setups it may not behave the same as the physical Run/Stop button.

Some units expose additional run-state commands such as:

```text
:RUNning STOP
:RUNning ON
:RUNning 0
:RUNning 1
```

These may be underdocumented or firmware-dependent. Test them cautiously and avoid polling afterward if the goal is to leave the screen static.

To release keypad lock, try:

```text
:SYSTem:LOCKed OFF
```

Then close the VISA/session and stop querying. If the front panel remains locked, disconnect USB or power-cycle the scope with USB unplugged.

## Probe Guidance

Normal passive probes:

- Use `10X` for most oscilloscope work.
- Set both the physical probe switch and the scope channel probe setting to `10X`.
- Use the short ground lead where possible.
- Avoid long ground leads for fast edges or high-frequency work.

High-voltage probes:

- `100X` probes reduce the measured signal and are useful for higher-voltage checks.
- Do not use them as the default for small audio/generator signals.

BNC-to-alligator leads:

- Usually red is signal and black is ground/shield.
- They are useful for low-frequency generator hookups and simple bench tests.
- Treat them as direct leads with no probe attenuation unless clearly labeled otherwise.

Probe compensation:

1. Use a normal passive probe in `10X`.
2. Connect to the scope's probe compensation output or a known square-wave generator.
3. Adjust the probe trim screw with the supplied tool.
4. Stop when the square wave has flat tops/bottoms and clean corners.

Interpretation:

```text
Good: flat top and bottom, clean corners
Too much compensation: spike or overshoot, then droop
Too little compensation: rounded leading edge and curved top
```

## Safety Notes For Amplifier Diagnostics

- Do not connect a grounded oscilloscope probe randomly inside powered equipment.
- Scope ground clips are usually tied to earth/computer ground and can short circuits.
- Use current-limited or fused power where practical.
- Start no-load, then use proper dummy loads when checking amplifier outputs.
- Check for DC offset before connecting speakers.
- For multi-channel amplifiers where every channel is affected, prioritize shared circuits first: power input, remote turn-on, DC-DC converter rails, protection logic, and shorted output devices.

## Reporting Style

When reporting to the user:

- give the direct verdict first
- mention the one adjustment to make next
- keep new vocabulary short and useful
- avoid long theory unless requested
- warn clearly before any safety-sensitive probing
