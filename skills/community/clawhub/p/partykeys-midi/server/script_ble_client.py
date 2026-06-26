"""
Script BLE Client - 直接通过 Python 连接蓝牙设备
"""
import asyncio
from bleak import BleakClient, BleakScanner

SERVICE_UUID = "03b80e5a-ede8-4b33-a751-6ce34ec4c700"

class ScriptBLEClient:
    def __init__(self):
        self.client = None
        self.device_address = None
        self.characteristic = None
        self.initialized = False

    async def scan_devices(self):
        """扫描附近的设备"""
        devices = await BleakScanner.discover(timeout=5.0)
        # 简化：返回所有设备，让用户选择或自动连接第一个
        return devices

    async def connect(self, address=None):
        """连接设备"""
        try:
            if not address:
                devices = await self.scan_devices()
                if not devices:
                    return {"success": False, "error": "未找到设备"}

                # 返回设备列表让用户选择
                device_list = [{"name": d.name or "未知设备", "address": d.address} for d in devices]
                return {"success": False, "need_selection": True, "devices": device_list, "message": "请选择要连接的设备"}

            self.client = BleakClient(address)
            await self.client.connect()

            for service in self.client.services:
                if service.uuid.lower() == SERVICE_UUID.lower():
                    self.characteristic = service.characteristics[0]
                    break

            return {"success": True, "address": address}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def disconnect(self):
        """断开连接"""
        if self.client:
            await self.client.disconnect()
        return {"success": True}

    def frame_ble_midi(self, sysex_bytes):
        """BLE MIDI 分包"""
        timestamp = 0x80
        packets = []

        f0 = sysex_bytes[0]
        f7 = sysex_bytes[-1]
        body = sysex_bytes[1:-1]

        # 第一个包
        first_payload = [0x80, timestamp, f0] + body[:17]
        packets.append(bytes(first_payload))

        # 后续包
        offset = 17
        while offset < len(body):
            chunk = body[offset:offset + 19]
            packets.append(bytes([0x80] + chunk))
            offset += 19

        # 最后添加 F7
        last_packet = packets[-1]
        if len(last_packet) + 2 <= 20:
            packets[-1] = bytes(list(last_packet) + [timestamp, f7])
        else:
            packets.append(bytes([0x80, timestamp, f7]))

        return packets

    async def light_keys(self, keys, color=1, brightness=100):
        """点亮按键"""
        if not self.client or not self.client.is_connected:
            return {"success": False, "error": "未连接"}

        # 只在第一次初始化
        if not self.initialized:
            init_cmd = [0xF0, 0x05, 0x30, 0x7f, 0x7f, 0x20, 0x00, 0x0f, 0x05, 0xF7]
            init_packets = self.frame_ble_midi(init_cmd)
            for packet in init_packets:
                await self.client.write_gatt_char(self.characteristic, packet, response=False)
            self.initialized = True
            await asyncio.sleep(0.05)

        # 亮灯命令
        header = [0xF0, 0x05, 0x30, 0x7f, 0x7f, 0x20, 0x00, 0x71]
        key_data = []
        for key in keys:
            note = int(key, 16) if isinstance(key, str) else key
            key_data.extend([note, color])

        light_cmd = header + [len(keys)] + key_data + [0xF7]
        light_packets = self.frame_ble_midi(light_cmd)
        for packet in light_packets:
            await self.client.write_gatt_char(self.characteristic, packet, response=False)

        return {"success": True}

    async def play_sequence(self, sequence):
        """播放音符序列"""
        if not self.client or not self.client.is_connected:
            return {"success": False, "error": "未连接"}

        for item in sequence:
            await self.light_keys(item["keys"])
            if item.get("delay", 0) > 0:
                await asyncio.sleep(item["delay"] / 1000.0)

        return {"success": True}

    async def follow_mode(self, notes, timeout=30000):
        """跟弹模式"""
        if not self.client or not self.client.is_connected:
            return {"success": False, "error": "未连接"}

        results = []
        for i, note in enumerate(notes):
            await self.light_keys([note], color=3)
            # TODO: 实现 MIDI 输入监听
            await asyncio.sleep(0.1)
            results.append({"note": note, "success": True})

        return {"success": True, "results": results}
