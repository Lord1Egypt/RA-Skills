#!/usr/bin/env python3
"""
LoRa packet protocol decoder
Tries to identify and decode common LoRa protocols from raw hex payload
"""

def decode_packet(hex_str, freq_hz, bw_hz, sf):
    """
    Attempt to identify and decode LoRa packet payload.
    Returns dict with: protocol, confidence, fields, summary
    """
    try:
        data = bytes.fromhex(hex_str)
    except:
        return {'protocol': 'INVALID_HEX', 'confidence': 0, 'summary': 'Bad hex'}

    results = []

    # Try each decoder
    for decoder in [
        _try_lorawan,
        _try_cayenne_lpp,
        _try_ttn_mapper,
        _try_meshtastic,
        _try_radiolib,
        _try_mydevices,
        _try_ascii_text,
        _try_aprs_like,
    ]:
        r = decoder(data, freq_hz, bw_hz, sf)
        if r and r.get('confidence', 0) > 0:
            results.append(r)

    if not results:
        return _generic_decode(data, freq_hz, bw_hz, sf)

    # Return highest confidence
    results.sort(key=lambda x: x['confidence'], reverse=True)
    return results[0]


def _try_lorawan(data, freq, bw, sf):
    """LoRaWAN MAC frame (MHDR + MACPayload + MIC)"""
    if len(data) < 8:
        return None

    mhdr = data[0]
    mtype = (mhdr >> 5) & 0x07
    major = mhdr & 0x03

    mtype_names = {
        0: 'Join Request',
        1: 'Join Accept',
        2: 'Unconfirmed Data Up',
        3: 'Unconfirmed Data Down',
        4: 'Confirmed Data Up',
        5: 'Confirmed Data Down',
        6: 'RFU',
        7: 'Proprietary',
    }

    if major != 0:  # LoRaWAN major version must be 0
        return None

    name = mtype_names.get(mtype, 'Unknown')
    confidence = 40  # base confidence for matching MHDR structure

    fields = {
        'MType': f'{mtype} ({name})',
        'Major': major,
    }

    if mtype in (0,):  # Join Request: AppEUI(8) + DevEUI(8) + DevNonce(2) = 18 + MIC(4) = 23
        if len(data) == 23:
            confidence = 85
            app_eui = data[1:9][::-1].hex().upper()
            dev_eui = data[9:17][::-1].hex().upper()
            dev_nonce = int.from_bytes(data[17:19], 'little')
            fields['AppEUI'] = ':'.join(app_eui[i:i+2] for i in range(0,16,2))
            fields['DevEUI'] = ':'.join(dev_eui[i:i+2] for i in range(0,16,2))
            fields['DevNonce'] = dev_nonce
            fields['MIC'] = data[19:23].hex().upper()

    elif mtype in (2, 4):  # Data Up
        if len(data) >= 13:
            confidence = 70
            dev_addr = data[1:5][::-1].hex().upper()
            fctrl = data[5]
            fcnt  = int.from_bytes(data[6:8], 'little')
            fopts_len = fctrl & 0x0F
            adr = bool(fctrl & 0x80)
            fport_idx = 8 + fopts_len
            fields['DevAddr']  = ':'.join(dev_addr[i:i+2] for i in range(0,8,2))
            fields['FCnt']     = fcnt
            fields['ADR']      = adr
            fields['FOpts_len']= fopts_len
            if fport_idx < len(data) - 4:
                fport = data[fport_idx]
                fields['FPort'] = fport
                payload = data[fport_idx+1:-4]
                fields['Payload_hex'] = payload.hex().upper()
                fields['MIC'] = data[-4:].hex().upper()
                if fport == 2:
                    fields['Hint'] = 'Possibly Cayenne LPP payload'
                elif fport == 1:
                    fields['Hint'] = 'App-specific port 1'

    elif mtype in (1,):  # Join Accept
        if len(data) in (17, 33):
            confidence = 80

    summary_parts = [f"LoRaWAN {name}"]
    if 'DevAddr' in fields:
        summary_parts.append(f"DevAddr={fields['DevAddr']}")
    if 'DevEUI' in fields:
        summary_parts.append(f"DevEUI={fields['DevEUI']}")
    if 'FCnt' in fields:
        summary_parts.append(f"FCnt={fields['FCnt']}")

    return {
        'protocol':   'LoRaWAN',
        'confidence': confidence,
        'fields':     fields,
        'summary':    ' | '.join(summary_parts),
    }


def _try_cayenne_lpp(data, freq, bw, sf):
    """Cayenne Low Power Payload — channel, type, value triples"""
    if len(data) < 3:
        return None

    # LPP data types
    LPP_TYPES = {
        0:  ('Digital Input',     1),
        1:  ('Digital Output',    1),
        2:  ('Analog Input',      2),
        3:  ('Analog Output',     2),
        100:('Generic',           4),
        101:('Illuminance',       2),
        102:('Presence',          1),
        103:('Temperature',       2),
        104:('Humidity',          1),
        113:('Accelerometer',     6),
        115:('Barometric Pressure',2),
        116:('Voltage',           2),
        117:('Current',           2),
        118:('Frequency',         4),
        120:('Percentage',        1),
        121:('Altitude',          2),
        125:('Concentration',     2),
        128:('Power',             2),
        130:('Distance',          4),
        132:('Energy',            4),
        133:('Direction',         2),
        134:('Unix Time',         4),
        135:('GPS',               9),
        136:('GPS (alt)',         11),
        142:('Gyroscope',         6),
        188:('Colour',            3),
        190:('Switch',            1),
        191:('Switch 2',          1),
    }

    fields = {}
    idx = 0
    sensors = 0
    confidence = 0

    while idx + 2 <= len(data):
        channel  = data[idx]
        lpp_type = data[idx+1]
        if lpp_type not in LPP_TYPES:
            break
        name, size = LPP_TYPES[lpp_type]
        if idx + 2 + size > len(data):
            break
        raw = data[idx+2:idx+2+size]

        # Decode value
        val = None
        if lpp_type == 103:  # Temperature: signed int16 / 10
            val = f"{int.from_bytes(raw, 'big', signed=True) / 10:.1f} °C"
        elif lpp_type == 104:  # Humidity: uint8 / 2
            val = f"{raw[0] / 2:.1f} %"
        elif lpp_type == 115:  # Pressure: uint16 / 10
            val = f"{int.from_bytes(raw, 'big') / 10:.1f} hPa"
        elif lpp_type == 102:  # Presence
            val = f"{'yes' if raw[0] else 'no'}"
        elif lpp_type == 101:  # Illuminance
            val = f"{int.from_bytes(raw, 'big')} lux"
        elif lpp_type == 2:    # Analog input: signed int16 / 100
            val = f"{int.from_bytes(raw, 'big', signed=True) / 100:.2f}"
        elif lpp_type == 135:  # GPS
            lat = int.from_bytes(raw[0:3], 'big', signed=True) / 10000
            lon = int.from_bytes(raw[3:6], 'big', signed=True) / 10000
            alt = int.from_bytes(raw[6:9], 'big', signed=True) / 100
            val = f"lat={lat:.4f} lon={lon:.4f} alt={alt:.1f}m"
        else:
            val = raw.hex().upper()

        key = f"Ch{channel}_{name}"
        fields[key] = val
        sensors += 1
        confidence += 25
        idx += 2 + size

    if sensors == 0 or idx < len(data) - 2:
        return None

    confidence = min(confidence, 90)
    summary = 'Cayenne LPP: ' + ', '.join(f"{k}={v}" for k,v in fields.items())

    return {
        'protocol':   'Cayenne LPP',
        'confidence': confidence,
        'fields':     fields,
        'summary':    summary,
    }


def _try_ttn_mapper(data, freq, bw, sf):
    """TTN Mapper format: lat(4)+lon(4)+alt(2)+hdop(1) = 11 bytes"""
    if len(data) != 11:
        return None
    try:
        lat  = int.from_bytes(data[0:4], 'little', signed=True) / 1e6
        lon  = int.from_bytes(data[4:8], 'little', signed=True) / 1e6
        alt  = int.from_bytes(data[8:10], 'little', signed=True) / 100
        hdop = data[10] / 10

        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            return None
        if not (0 <= hdop <= 50):
            return None

        return {
            'protocol':   'TTN Mapper',
            'confidence': 75,
            'fields': {
                'Latitude':  f"{lat:.6f}°",
                'Longitude': f"{lon:.6f}°",
                'Altitude':  f"{alt:.1f} m",
                'HDOP':      f"{hdop:.1f}",
            },
            'summary': f"TTN Mapper: {lat:.5f},{lon:.5f} alt={alt:.0f}m hdop={hdop:.1f}",
        }
    except:
        return None


def _try_meshtastic(data, freq, bw, sf):
    """Meshtastic uses 915/868/433 MHz with specific header"""
    if len(data) < 8:
        return None

    # Meshtastic packet has dest(4)+src(4)+id(4)+flags(1)+... minimum 13 bytes
    if len(data) < 13:
        return None

    dest = int.from_bytes(data[0:4], 'little')
    src  = int.from_bytes(data[4:8], 'little')
    pkt_id = int.from_bytes(data[8:12], 'little')
    flags = data[12] if len(data) > 12 else 0

    # Meshtastic node IDs are typically 0xFFFFFFFF (broadcast) or 8-digit hex
    is_broadcast = (dest == 0xFFFFFFFF)
    # Check if looks like node IDs (not all zeros or all FF)
    if dest == 0 and src == 0:
        return None

    confidence = 35
    if is_broadcast:
        confidence += 20
    if 433e6 <= freq <= 435e6:
        confidence += 15  # common Meshtastic EU freq

    return {
        'protocol':   'Meshtastic',
        'confidence': confidence,
        'fields': {
            'Dest':   f"{'BROADCAST' if is_broadcast else hex(dest)}",
            'Src':    hex(src),
            'PktID':  hex(pkt_id),
            'Flags':  hex(flags),
            'Payload':data[13:].hex().upper() if len(data)>13 else '',
        },
        'summary': f"Meshtastic: src={hex(src)} → {'BROADCAST' if is_broadcast else hex(dest)} id={hex(pkt_id)}",
    }


def _try_radiolib(data, freq, bw, sf):
    """RadioLib/Arduino-LoRa simple packet: often starts with printable ASCII or known magic"""
    if len(data) < 2:
        return None

    # RadioLib ping: 'Hello World' style
    printable = sum(1 for b in data if 32 <= b < 127)
    ratio = printable / len(data)

    if ratio > 0.85:
        text = ''.join(chr(b) if 32<=b<127 else '.' for b in data)
        return {
            'protocol':   'ASCII/RadioLib',
            'confidence': 60,
            'fields':     {'Text': text},
            'summary':    f"Text: \"{text}\"",
        }
    return None


def _try_mydevices(data, freq, bw, sf):
    """MyDevices / generic sensor with temp+humidity common pattern"""
    # 4-byte: temp(2 signed /100) + humidity(2 unsigned /100)
    if len(data) == 4:
        try:
            temp = int.from_bytes(data[0:2], 'big', signed=True) / 100
            hum  = int.from_bytes(data[2:4], 'big') / 100
            if -40 <= temp <= 85 and 0 <= hum <= 100:
                return {
                    'protocol':   'Sensor (temp+hum)',
                    'confidence': 55,
                    'fields':     {'Temperature': f"{temp:.2f}°C", 'Humidity': f"{hum:.1f}%"},
                    'summary':    f"Sensor: T={temp:.1f}°C H={hum:.1f}%",
                }
        except:
            pass
    return None


def _try_ascii_text(data, freq, bw, sf):
    """Plain ASCII text payload"""
    try:
        text = data.decode('ascii')
        if all(32 <= ord(c) < 127 or c in '\r\n\t' for c in text):
            return {
                'protocol':   'Plain Text',
                'confidence': 70,
                'fields':     {'Text': text.strip()},
                'summary':    f"Text: \"{text.strip()[:60]}\"",
            }
    except:
        pass
    return None


def _try_aprs_like(data, freq, bw, sf):
    """APRS-over-LoRa sometimes used in 433 MHz region"""
    if len(data) < 5:
        return None
    try:
        text = data.decode('ascii', errors='replace')
        if '>' in text and (':' in text or '!' in text):
            return {
                'protocol':   'APRS-like',
                'confidence': 65,
                'fields':     {'Frame': text},
                'summary':    f"APRS: {text[:80]}",
            }
    except:
        pass
    return None


def _generic_decode(data, freq, bw, sf):
    """Fallback: entropy analysis and basic stats"""
    import math
    from collections import Counter

    counts = Counter(data)
    total  = len(data)
    entropy = -sum((c/total)*math.log2(c/total) for c in counts.values() if c > 0)

    printable = sum(1 for b in data if 32<=b<127)

    if entropy > 7.5:
        hint = "High entropy → likely encrypted or compressed"
    elif entropy < 3:
        hint = "Low entropy → structured/repetitive data"
    else:
        hint = "Medium entropy → possibly framed data"

    return {
        'protocol':   'Unknown',
        'confidence': 0,
        'fields': {
            'Length':    total,
            'Entropy':   f"{entropy:.2f} bits/byte",
            'Printable': f"{printable}/{total} bytes",
            'Hint':      hint,
            'Hex':       ' '.join(f"{b:02X}" for b in data[:32]),
        },
        'summary': f"Unknown ({total}B, entropy={entropy:.1f}) — {hint}",
    }


def format_decoded(pkt_dict, decoded):
    """Format decoded packet for Telegram message"""
    lines = [
        f"🎯 LoRa PACKET CAUGHT!",
        f"",
        f"📻 {pkt_dict['freq']/1e6:.3f} MHz  BW={pkt_dict['bw']//1000}kHz  SF{pkt_dict['sf']}",
        f"📶 RSSI: {pkt_dict['rssi']} dBm  SNR: {pkt_dict['snr']:+d} dB",
        f"📦 Length: {pkt_dict['len']} bytes",
        f"",
    ]

    conf = decoded['confidence']
    proto = decoded['protocol']
    if conf >= 70:
        lines.append(f"✅ Protocol: {proto} (confidence {conf}%)")
    elif conf >= 40:
        lines.append(f"🔶 Possibly: {proto} (confidence {conf}%)")
    else:
        lines.append(f"❓ Protocol not recognized")

    lines.append(f"📋 {decoded['summary']}")
    lines.append("")

    # Key fields
    fields = decoded.get('fields', {})
    skip = {'Hex', 'Payload_hex'}  # show separately
    for k, v in fields.items():
        if k not in skip and str(v):
            lines.append(f"  {k}: {v}")

    # Raw hex
    lines.append("")
    lines.append("HEX:")
    hex_str = pkt_dict['hex']
    for i in range(0, len(hex_str), 24):  # 12 bytes per row
        chunk = hex_str[i:i+24]
        pairs = ' '.join(chunk[j:j+2] for j in range(0, len(chunk), 2))
        lines.append(f"  {pairs}")

    return '\n'.join(lines)


if __name__ == '__main__':
    # Test
    import sys
    if len(sys.argv) > 1:
        hex_str = sys.argv[1]
        freq    = int(sys.argv[2]) if len(sys.argv) > 2 else 433175000
        bw      = int(sys.argv[3]) if len(sys.argv) > 3 else 125000
        sf      = int(sys.argv[4]) if len(sys.argv) > 4 else 7
        result  = decode_packet(hex_str, freq, bw, sf)
        print(f"Protocol:   {result['protocol']}")
        print(f"Confidence: {result['confidence']}%")
        print(f"Summary:    {result['summary']}")
        for k, v in result.get('fields', {}).items():
            print(f"  {k}: {v}")
