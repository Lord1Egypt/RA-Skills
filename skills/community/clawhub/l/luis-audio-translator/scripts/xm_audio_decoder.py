#!/usr/bin/env python3
import argparse
import base64
import json
import os
import sys
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


AES_FILL = b"123456781234567812345678"
XM_STAGE1_KEY = b"ximalayaximalayaximalayaximalaya"


def emit(obj, code=0):
    print(json.dumps(obj, ensure_ascii=False, indent=2))
    raise SystemExit(code)


def xtime(value):
    value <<= 1
    if value & 0x100:
        value ^= 0x11B
    return value & 0xFF


def gf_mul(a, b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        a = xtime(a)
        b >>= 1
    return result


def gf_pow(a, n):
    result = 1
    while n:
        if n & 1:
            result = gf_mul(result, a)
        a = gf_mul(a, a)
        n >>= 1
    return result


def rotl8(value, shift):
    return ((value << shift) | (value >> (8 - shift))) & 0xFF


def build_sboxes():
    sbox = [0] * 256
    inv_sbox = [0] * 256
    for i in range(256):
        inv = 0 if i == 0 else gf_pow(i, 254)
        value = inv ^ rotl8(inv, 1) ^ rotl8(inv, 2) ^ rotl8(inv, 3) ^ rotl8(inv, 4) ^ 0x63
        sbox[i] = value
        inv_sbox[value] = i
    return sbox, inv_sbox


SBOX, INV_SBOX = build_sboxes()


def rcon(index):
    value = 1
    for _ in range(index - 1):
        value = xtime(value)
    return value


def key_expansion(key):
    if len(key) not in (16, 24, 32):
        raise ValueError("AES key must be 16, 24, or 32 bytes")
    nk = len(key) // 4
    nr = nk + 6
    words = [list(key[i:i + 4]) for i in range(0, len(key), 4)]
    for i in range(nk, 4 * (nr + 1)):
        temp = words[i - 1][:]
        if i % nk == 0:
            temp = temp[1:] + temp[:1]
            temp = [SBOX[x] for x in temp]
            temp[0] ^= rcon(i // nk)
        elif nk > 6 and i % nk == 4:
            temp = [SBOX[x] for x in temp]
        words.append([a ^ b for a, b in zip(words[i - nk], temp)])
    return [bytes(sum(words[i:i + 4], [])) for i in range(0, len(words), 4)]


def add_round_key(state, round_key):
    for i in range(16):
        state[i] ^= round_key[i]


def inv_shift_rows(state):
    old = state[:]
    for row in range(4):
        for col in range(4):
            state[4 * col + row] = old[4 * ((col - row) % 4) + row]


def inv_sub_bytes(state):
    for i in range(16):
        state[i] = INV_SBOX[state[i]]


def inv_mix_columns(state):
    for col in range(4):
        offset = 4 * col
        a0, a1, a2, a3 = state[offset:offset + 4]
        state[offset] = gf_mul(a0, 14) ^ gf_mul(a1, 11) ^ gf_mul(a2, 13) ^ gf_mul(a3, 9)
        state[offset + 1] = gf_mul(a0, 9) ^ gf_mul(a1, 14) ^ gf_mul(a2, 11) ^ gf_mul(a3, 13)
        state[offset + 2] = gf_mul(a0, 13) ^ gf_mul(a1, 9) ^ gf_mul(a2, 14) ^ gf_mul(a3, 11)
        state[offset + 3] = gf_mul(a0, 11) ^ gf_mul(a1, 13) ^ gf_mul(a2, 9) ^ gf_mul(a3, 14)


def aes_decrypt_block(block, round_keys):
    state = list(block)
    nr = len(round_keys) - 1
    add_round_key(state, round_keys[nr])
    for round_index in range(nr - 1, 0, -1):
        inv_shift_rows(state)
        inv_sub_bytes(state)
        add_round_key(state, round_keys[round_index])
        inv_mix_columns(state)
    inv_shift_rows(state)
    inv_sub_bytes(state)
    add_round_key(state, round_keys[0])
    return bytes(state)


def pkcs7_pad(data, block_size=16):
    padding = block_size - (len(data) % block_size)
    return data + bytes([padding]) * padding


def pkcs7_unpad(data, block_size=16):
    if not data:
        return data
    padding = data[-1]
    if padding < 1 or padding > block_size or padding > len(data):
        return data
    if data[-padding:] != bytes([padding]) * padding:
        return data
    return data[:-padding]


def aes_cbc_decrypt(data, key, iv, unpad=True):
    if len(data) % 16 != 0:
        raise ValueError("AES-CBC input length must be a multiple of 16")
    round_keys = key_expansion(key)
    previous = iv
    output = bytearray()
    for offset in range(0, len(data), 16):
        block = data[offset:offset + 16]
        plain = aes_decrypt_block(block, round_keys)
        output.extend(a ^ b for a, b in zip(plain, previous))
        previous = block
    result = bytes(output)
    return pkcs7_unpad(result) if unpad else result


def syncsafe_int(data):
    return ((data[0] & 0x7F) << 21) | ((data[1] & 0x7F) << 14) | ((data[2] & 0x7F) << 7) | (data[3] & 0x7F)


def decode_text_frame(payload):
    if not payload:
        return ""
    encoding = payload[0]
    body = payload[1:]
    if encoding == 0:
        return body.decode("latin1", "ignore").rstrip("\x00")
    if encoding == 1:
        if body.startswith(b"\xff\xfe"):
            return body[2:].decode("utf-16le", "ignore").rstrip("\x00")
        if body.startswith(b"\xfe\xff"):
            return body[2:].decode("utf-16be", "ignore").rstrip("\x00")
        return body.decode("utf-16", "ignore").rstrip("\x00")
    return body.decode("utf-8", "ignore").rstrip("\x00")


def read_id3(path):
    data = Path(path).read_bytes()
    if len(data) < 10 or data[:3] != b"ID3":
        emit({"ok": False, "error": "input does not have an ID3v2 header"}, 2)
    major = data[3]
    if major not in (3, 4):
        emit({"ok": False, "error": f"unsupported ID3 version: 2.{major}"}, 2)
    tag_size = syncsafe_int(data[6:10])
    tag_end = 10 + tag_size
    if tag_end > len(data):
        emit({"ok": False, "error": "invalid ID3 tag size", "tag_size": tag_size, "file_size": len(data)}, 2)

    tags = {}
    offset = 10
    wanted = {"TIT2", "TALB", "TPE1", "TRCK", "TSRC", "TENC", "TSIZ", "TSSE"}
    while offset + 10 <= tag_end:
        frame_id = data[offset:offset + 4].decode("latin1", "ignore")
        if not frame_id.isalnum() or frame_id == "\x00\x00\x00\x00":
            break
        size_data = data[offset + 4:offset + 8]
        frame_size = syncsafe_int(size_data) if major == 4 else int.from_bytes(size_data, "big")
        if frame_size <= 0 or offset + 10 + frame_size > tag_end:
            break
        payload = data[offset + 10:offset + 10 + frame_size]
        if frame_id in wanted:
            tags[frame_id] = decode_text_frame(payload)
        offset += 10 + frame_size
    return tags, data[tag_end:]


def printable_prefix(data):
    end = 0
    for value in data:
        if value in (9, 10, 13) or 32 <= value <= 126:
            end += 1
        else:
            break
    return data[:end]


def file_type_ext(data):
    if data.startswith(b"fLaC"):
        return "flac"
    if data.startswith(b"ID3") or (len(data) >= 2 and data[0] == 0xFF and (data[1] & 0xE0) == 0xE0):
        return "mp3"
    if data.startswith(b"OggS"):
        return "ogg"
    if len(data) >= 12 and data[4:8] == b"ftyp":
        return "m4a"
    if len(data) >= 12 and data[8:12] == b"WAVE":
        return "wav"
    return "bin"


def decode_xm(input_path, output_dir):
    tags, audio = read_id3(input_path)
    try:
        encrypted_size = int(tags.get("TSIZ", "0"))
    except ValueError:
        encrypted_size = 0
    if encrypted_size <= 0 or encrypted_size > len(audio):
        emit({"ok": False, "error": "missing or invalid TSIZ encrypted payload size", "TSIZ": tags.get("TSIZ")}, 2)

    iv_hex = tags.get("TSRC") or tags.get("TENC") or ""
    try:
        iv = bytes.fromhex(iv_hex)
    except ValueError:
        iv = b""
    if len(iv) != 16:
        emit({"ok": False, "error": "missing valid 16-byte IV in TSRC or TENC", "TSRC": tags.get("TSRC"), "TENC": tags.get("TENC")}, 2)

    track = str(int(tags.get("TRCK") or "0")).encode("utf-8")
    if len(track) > 24:
        track = track[-24:]
    stage2_key = AES_FILL[:24 - len(track)] + track
    stage2_iv = stage2_key[:16]

    encrypted_block = audio[:encrypted_size]
    stage1 = aes_cbc_decrypt(pkcs7_pad(encrypted_block), XM_STAGE1_KEY, iv, unpad=False)
    stage1_text = printable_prefix(stage1)
    if not stage1_text:
        emit({"ok": False, "error": "xm stage 1 did not produce printable payload"}, 2)

    try:
        stage2_encrypted = base64.b64decode(stage1_text, validate=False)
    except ValueError as exc:
        emit({"ok": False, "error": f"xm stage 1 payload is not base64: {exc}"}, 2)
    stage2_text = aes_cbc_decrypt(stage2_encrypted, stage2_key, stage2_iv, unpad=True).decode("utf-8", "ignore")

    try:
        header = base64.b64decode((tags.get("TSSE") or "") + stage2_text, validate=False)
    except ValueError as exc:
        emit({"ok": False, "error": f"xm decoded header is not base64: {exc}"}, 2)
    if not header:
        emit({"ok": False, "error": "xm decoded header is empty"}, 2)

    decoded = header + audio[encrypted_size:]
    ext = file_type_ext(decoded)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"{Path(input_path).stem}.{ext}"
    output.write_bytes(decoded)
    emit({"ok": True, "input": str(input_path), "output": str(output), "detected_format": ext})


def self_test():
    cases = [
        (
            bytes.fromhex("00112233445566778899aabbccddeeff"),
            bytes.fromhex("000102030405060708090a0b0c0d0e0f"),
            bytes.fromhex("69c4e0d86a7b0430d8cdb78070b4c55a"),
        ),
        (
            bytes.fromhex("00112233445566778899aabbccddeeff"),
            bytes.fromhex("000102030405060708090a0b0c0d0e0f1011121314151617"),
            bytes.fromhex("dda97ca4864cdfe06eaf70a0ec0d7191"),
        ),
        (
            bytes.fromhex("00112233445566778899aabbccddeeff"),
            bytes.fromhex("000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f"),
            bytes.fromhex("8ea2b7ca516745bfeafc49904b496089"),
        ),
    ]
    for plain, key, cipher in cases:
        actual = aes_cbc_decrypt(cipher, key, bytes(16), unpad=False)
        if actual != plain:
            emit({"ok": False, "error": "AES self-test failed", "key_size": len(key) * 8, "actual": actual.hex()}, 1)
    emit({"ok": True, "self_test": "passed"})


def main():
    parser = argparse.ArgumentParser(description="Decode Ximalaya .xm audio without external helpers")
    parser.add_argument("input", nargs="?")
    parser.add_argument("--output-dir")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    if not args.input or not args.output_dir:
        emit({"ok": False, "error": "usage: python xm_audio_decoder.py <input.xm> --output-dir <dir>"}, 2)
    decode_xm(args.input, args.output_dir)


if __name__ == "__main__":
    main()
