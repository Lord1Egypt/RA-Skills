# HomeKit API Reference

## Device Discovery

HomeKit uses the Bonjour/mDNS protocol to discover devices on the local network.

```python
from homekit.zeroconf_impl import ZeroconfController

controller = ZeroconfController()
devices = controller.discover(timeout=5)
```

## Device Pairing

Pairing requires:
1. The device must be in pairing mode.
2. A valid pairing code (8-digit PIN, format: XXX-XX-XXX).

```python
from homekit import Controller

controller = Controller()
pairing = controller.perform_pairing(
    alias="my-device",
    device_name="Device Name",
    pin="123-45-678",
    address="192.168.1.100",
    port=8080
)
```

## Device Control

### Getting Device List

```python
pairings = controller.get_pairings()
for alias in pairings:
    pairing = pairings[alias]
    accessories = pairing.list_accessories_and_characteristics()
```

### Controlling Switches

```python
# Turn on
pairing.put_characteristics([{
    'aid': 1,  # Accessory ID
    'iid': 9,  # Characteristic ID (On)
    'value': True
}])

# Turn off
pairing.put_characteristics([{
    'aid': 1,
    'iid': 9,
    'value': False
}])
```

### Setting Brightness

```python
pairing.put_characteristics([{
    'aid': 1,
    'iid': 10,  # Brightness characteristic
    'value': 50  # 0-100
}])
```

## Characteristic Types

| Type | UUID | Description |
|------|------|------|
| On | 00000025-0000-1000-8000-0026BB765291 | Power state |
| Brightness | 00000008-0000-1000-8000-0026BB765291 | Brightness (0-100) |
| Hue | 00000013-0000-1000-8000-0026BB765291 | Hue (0-360) |
| Saturation | 0000002F-0000-1000-8000-0026BB765291 | Saturation (0-100) |
| CurrentTemperature | 00000011-0000-1000-8000-0026BB765291 | Current Temp |
| TargetTemperature | 00000035-0000-1000-8000-0026BB765291 | Target Temp |

## Service Types

| Type | Description |
|------|------|
| Lightbulb | Lightbulb |
| Switch | Switch |
| Outlet | Outlet |
| Thermostat | Thermostat |
| Fan | Fan |
| GarageDoorOpener | Garage Door Opener |
| LockManagement | Lock Management |

## Error Handling

Common exceptions:
- `AccessoryNotFoundError`: Device not found.
- `IncorrectPairingIdError`: Invalid pairing ID.
- `UnavailableError`: Device is offline.
