## Description:

Designs, implements and reviews Bluetooth Low Energy code in Android, iOS and Flutter apps: Android 12+ permissions, filtered scans, GATT operation queues, MTU, bonding, status 133, CoreBluetooth threading and state restoration, flutter_blue_plus, framing, CRC, safe firmware updates (DFU) and connection state machines. Use when writing or reviewing BLE scan, connect, read, write or notify code, reconnect logic or device protocols.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT-0

## Use Case:

Mobile developers and connected-device engineers use this skill to implement and review BLE scanning, connections, GATT operations, device protocols, reconnect behavior, and firmware update flows in Android, iOS, and Flutter apps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Permission and background-mode changes can affect app behavior and review requirements.

Mitigation: Review generated permission and background-mode changes for the intended platform behavior before release.

Risk: Firmware update failures, incompatible images, or low battery can leave a device unable to update safely.

Mitigation: Test firmware failure and recovery paths on dedicated hardware; confirm incompatible images and low-battery conditions block updates.

Risk: The Flutter BLE dependency may carry licensing obligations and build-time data sharing.

Mitigation: Review the dependency's disclosed license and build-time network behavior before adoption.

## Reference(s):

- [Android BLE guidance](references/android.md)
- [iOS CoreBluetooth guidance](references/ios.md)
- [Flutter BLE guidance](references/flutter.md)
- [Protocol and firmware updates](references/protocol-and-dfu.md)
- [BLE testing guidance](references/testing.md)
- [Mobile BLE on ClawHub](https://clawhub.ai/ahmadhussain0335/skills/mobile-ble)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
