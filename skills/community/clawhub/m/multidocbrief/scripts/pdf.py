"""
Чтение PDF без сторонних PDF-библиотек (только стандартная библиотека; Pillow — для картинок,
cryptography — для зашифрованных PDF, fontTools — для редких PDF без таблицы ToUnicode;
все три есть в Anaconda). PyMuPDF / pdftoppm / Ghostscript используются, ТОЛЬКО если они есть.

Что умеет:
  - таблицы xref (классические и потоковые), объектные потоки, /Prev-цепочки, восстановление
    повреждённой xref сканированием файла;
  - фильтры Flate (с PNG/TIFF-предикторами), LZW, ASCIIHex, ASCII85, RunLength;
  - шифрование стандартным обработчиком с пустым паролем пользователя (RC4 40–128, AES-128, AES-256) —
    так защищены PDF «только для чтения»;
  - текст: ToUnicode CMap, Identity-H, WinAnsi/MacRoman/Standard + /Differences (включая
    кириллические имена глифов afii100xx), ширины глифов; строки собираются по координатам,
    поэтому таблицы и PDF из PowerPoint/Excel читаются в правильном порядке;
  - признаки «графической» страницы (сканы, крупные картинки, векторные графики) и извлечение
    растровых картинок страницы (JPEG, JPEG 2000, CCITT G3/G4, Flate RGB/Gray/CMYK/Indexed).
"""
from __future__ import annotations

import base64
import hashlib
import io
import math
import re
import shutil
import struct
import subprocess
import tempfile
import zlib
from pathlib import Path

# =============================================================================== базовые типы


class PDFError(Exception):
    pass


class Name(str):
    """Имя PDF (/Type) — отличается от строк (bytes)."""


class Ref:
    __slots__ = ("num", "gen")

    def __init__(self, num: int, gen: int):
        self.num, self.gen = num, gen

    def __eq__(self, other):
        return isinstance(other, Ref) and other.num == self.num and other.gen == self.gen

    def __hash__(self):
        return hash((self.num, self.gen))

    def __repr__(self):
        return f"{self.num} {self.gen} R"


class Stream:
    __slots__ = ("dict", "raw", "objnum", "gen", "_decoded")

    def __init__(self, d: dict, raw: bytes, objnum: int = 0, gen: int = 0):
        self.dict, self.raw, self.objnum, self.gen, self._decoded = d, raw, objnum, gen, None

    def get(self, k, default=None):
        return self.dict.get(k, default)


class Keyword(bytes):
    """Оператор/ключевое слово (obj, R, Tj, BT …)."""


# =============================================================================== лексер

_WS = b" \t\r\n\x0c\x00"
_TOKEN = re.compile(
    rb"(?P<ws>[\x00\t\n\x0c\r ]+|%[^\r\n]*)"
    rb"|(?P<num>[+-]?(?:\d+\.?\d*|\.\d+))(?![^\x00\t\n\x0c\r ()<>\[\]{}/%])"
    rb"|(?P<name>/[^\x00\t\n\x0c\r ()<>\[\]{}/%]*)"
    rb"|(?P<dopen><<)|(?P<dclose>>>)"
    rb"|(?P<hstr><[0-9A-Fa-f\x00\t\n\x0c\r ]*>)"
    rb"|(?P<aopen>\[)|(?P<aclose>\])"
    rb"|(?P<lstr>\()"
    rb"|(?P<bopen>\{)|(?P<bclose>\})"
    rb"|(?P<kw>[^\x00\t\n\x0c\r ()<>\[\]{}/%]+)"
    rb"|(?P<junk>.)", re.S)
_NAME_ESC = re.compile(rb"#([0-9A-Fa-f]{2})")
_STR_ESC = {b"n": b"\n", b"r": b"\r", b"t": b"\t", b"b": b"\b", b"f": b"\f", b"(": b"(", b")": b")", b"\\": b"\\"}
_LSTR_PART = re.compile(rb"[()\\]")


def _read_lstr(data: bytes, pos: int) -> tuple[bytes, int]:
    """pos — сразу после '('. Возвращает (строку, позицию после ')')."""
    depth, out, i, n = 1, bytearray(), pos, len(data)
    while i < n:
        m = _LSTR_PART.search(data, i)
        if not m:
            out += data[i:]
            return bytes(out), n
        out += data[i:m.start()]
        ch = m.group(0)
        i = m.end()
        if ch == b"\\":
            if i >= n:
                break
            c = data[i:i + 1]
            if c in _STR_ESC:
                out += _STR_ESC[c]
                i += 1
            elif c in b"01234567":
                j = i
                while j < n and j - i < 3 and data[j:j + 1] in b"01234567":
                    j += 1
                out.append(int(data[i:j], 8) & 0xFF)
                i = j
            elif c == b"\r":
                i += 2 if data[i + 1:i + 2] == b"\n" else 1
            elif c == b"\n":
                i += 1
            else:
                out += c
                i += 1
        elif ch == b"(":
            depth += 1
            out += b"("
        else:
            depth -= 1
            if depth == 0:
                return bytes(out), i
            out += b")"
    return bytes(out), n


def _hex(b: bytes) -> bytes:
    h = re.sub(rb"[^0-9A-Fa-f]", b"", b)
    if len(h) % 2:
        h += b"0"
    return bytes.fromhex(h.decode())


def tokenize(data: bytes, pos: int = 0, end: int | None = None):
    """Генератор (тип, значение, позиция_после)."""
    end = len(data) if end is None else end
    while pos < end:
        m = _TOKEN.match(data, pos, end)
        if not m:
            return
        kind = m.lastgroup
        pos = m.end()
        if kind == "ws" or kind == "junk":
            continue
        val = m.group(kind)
        if kind == "num":
            yield "obj", (float(val) if b"." in val else int(val)), pos
        elif kind == "name":
            raw = _NAME_ESC.sub(lambda x: bytes([int(x.group(1), 16)]), val[1:])
            yield "obj", Name(raw.decode("latin-1")), pos
        elif kind == "hstr":
            yield "obj", _hex(val[1:-1]), pos
        elif kind == "lstr":
            s, pos = _read_lstr(data, pos)
            yield "obj", s, pos
        elif kind in ("dopen", "dclose", "aopen", "aclose", "bopen", "bclose"):
            yield kind, None, pos
        else:  # kw
            if val == b"true":
                yield "obj", True, pos
            elif val == b"false":
                yield "obj", False, pos
            elif val == b"null":
                yield "obj", None, pos
            else:
                yield "kw", Keyword(val), pos


def parse_object(data: bytes, pos: int, end: int | None = None):
    """Разбирает один объект с позиции pos. Возвращает (объект, позиция_после)."""
    stack: list = [[]]
    kinds: list = ["root"]
    for kind, val, p in tokenize(data, pos, end):
        if kind == "obj":
            stack[-1].append(val)
        elif kind == "kw":
            if val in (b"endobj", b"stream", b"endstream", b"obj") and len(stack) > 1:
                return None, p  # незакрытый словарь/массив — объект повреждён
            if val == b"R" and len(stack[-1]) >= 2 and isinstance(stack[-1][-1], int) \
                    and isinstance(stack[-1][-2], int):
                gen = stack[-1].pop()
                num = stack[-1].pop()
                stack[-1].append(Ref(num, gen))
            else:
                stack[-1].append(val)
        elif kind in ("aopen", "dopen"):
            stack.append([])
            kinds.append(kind)
        elif kind in ("aclose", "dclose") and len(stack) > 1:
            items = stack.pop()
            k = kinds.pop()
            if k == "dopen":
                d = {}
                it = iter(range(0, len(items) - 1, 2))
                for i in it:
                    if isinstance(items[i], Name):
                        d[items[i]] = items[i + 1]
                stack[-1].append(d)
            else:
                stack[-1].append(items)
        else:
            continue
        if len(stack) == 1 and stack[0]:
            # число может оказаться началом ссылки «N G R» — дочитываем, если это так
            if isinstance(stack[0][0], int) and len(stack[0]) == 1:
                m = re.match(rb"\s+(\d+)\s+R\b", data[p:p + 24])
                if m:
                    return Ref(stack[0][0], int(m.group(1))), p + m.end()
            return stack[0][0], p
    return (stack[0][0] if stack[0] else None), len(data)


# =============================================================================== фильтры

def _png_chunk(kind: bytes, payload: bytes) -> bytes:
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)


def _png_fast(data: bytes, colors: int, columns: int) -> bytes | None:
    """Снятие PNG-фильтров силами libpng (Pillow): строки PDF-потока упаковываются в PNG.
    Цвет не важен — нужны только «расфильтрованные» байты.
    """
    ctype = {1: 0, 2: 4, 3: 2, 4: 6}.get(colors)
    rowlen = colors * columns
    h = len(data) // (rowlen + 1) if rowlen else 0
    if ctype is None or not h or columns <= 0:
        return None
    try:
        from PIL import Image
        png = (b"\x89PNG\r\n\x1a\n" + _png_chunk(b"IHDR", struct.pack(">IIBBBBB", columns, h, 8, ctype, 0, 0, 0))
               + _png_chunk(b"IDAT", zlib.compress(data[: h * (rowlen + 1)], 1)) + _png_chunk(b"IEND", b""))
        im = Image.open(io.BytesIO(png))
        im.load()
        return im.tobytes()
    except Exception:  # noqa: BLE001
        return None


def _png_unpredict(data: bytes, predictor: int, colors: int, bpc: int, columns: int) -> bytes:
    if predictor >= 10 and bpc == 8:
        fast = _png_fast(data, colors, columns)
        if fast is not None:
            return fast
    if predictor < 10:
        if predictor == 2 and bpc == 8:  # TIFF predictor
            bpp, row = colors, colors * columns
            out = bytearray(data)
            for r in range(0, len(out), row):
                for i in range(r + bpp, min(r + row, len(out))):
                    out[i] = (out[i] + out[i - bpp]) & 0xFF
            return bytes(out)
        return data
    bpp = max(1, colors * bpc // 8)
    rowlen = (colors * bpc * columns + 7) // 8
    out = bytearray()
    prev = bytearray(rowlen)
    i = 0
    while i < len(data):
        ft = data[i]
        row = bytearray(data[i + 1:i + 1 + rowlen])
        if len(row) < rowlen:
            row += bytes(rowlen - len(row))
        i += rowlen + 1
        if ft == 1:
            for x in range(bpp, rowlen):
                row[x] = (row[x] + row[x - bpp]) & 0xFF
        elif ft == 2:
            for x in range(rowlen):
                row[x] = (row[x] + prev[x]) & 0xFF
        elif ft == 3:
            for x in range(rowlen):
                left = row[x - bpp] if x >= bpp else 0
                row[x] = (row[x] + ((left + prev[x]) >> 1)) & 0xFF
        elif ft == 4:
            for x in range(rowlen):
                a = row[x - bpp] if x >= bpp else 0
                b = prev[x]
                c = prev[x - bpp] if x >= bpp else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if pa <= pb and pa <= pc else (b if pb <= pc else c)
                row[x] = (row[x] + pr) & 0xFF
        out += row
        prev = row
    return bytes(out)


def _flate(data: bytes) -> bytes:
    for wbits, chunk in ((15, data), (-15, data[2:])):
        d = zlib.decompressobj(wbits)
        try:
            return d.decompress(chunk, MAX_STREAM)  # обрезанный поток — берём, что распаковалось
        except zlib.error:
            continue
    return b""


def _lzw(data: bytes, early: int = 1) -> bytes:
    out = bytearray()
    table = [bytes([i]) for i in range(256)] + [b"", b""]
    bits, buf, nbits, prev = 9, 0, 0, None
    for byte in data:
        buf = (buf << 8) | byte
        nbits += 8
        while nbits >= bits:
            nbits -= bits
            code = (buf >> nbits) & ((1 << bits) - 1)
            if code == 256:
                table = table[:258]
                bits, prev = 9, None
                continue
            if code == 257:
                return bytes(out)
            if prev is None:
                entry = table[code] if code < len(table) else b""
            elif code < len(table):
                entry = table[code]
                if len(table) < 4096:
                    table.append(prev + entry[:1])
            else:
                entry = prev + prev[:1]
                if len(table) < 4096:
                    table.append(entry)
            out += entry
            prev = entry
            if len(out) > MAX_STREAM:
                return bytes(out)
            if len(table) + early >= (1 << bits) and bits < 12:
                bits += 1
    return bytes(out)


def _a85(data: bytes) -> bytes:
    data = re.sub(rb"\s", b"", data)
    if data.startswith(b"<~"):
        data = data[2:]
    end = data.find(b"~>")
    if end >= 0:
        data = data[:end]
    try:
        return base64.a85decode(data)
    except ValueError:
        return b""


def _rle(data: bytes) -> bytes:
    out, i = bytearray(), 0
    while i < len(data):
        n = data[i]
        if n == 128:
            break
        if n < 128:
            out += data[i + 1:i + 2 + n]
            i += n + 2
        else:
            out += data[i + 1:i + 2] * (257 - n)
            i += 2
    return bytes(out)


MAX_STREAM = 256 << 20   # не распаковываем поток больше 256 МБ (защита от «zip-бомб»)
IMAGE_FILTERS = {"DCTDecode", "DCT", "JPXDecode", "CCITTFaxDecode", "CCF", "JBIG2Decode"}


# =============================================================================== шифрование

_PAD = bytes.fromhex("28BF4E5E4E758A4164004E56FFFA01082E2E00B6D0683E802F0CA9FE6453697A")


def _rc4(key: bytes, data: bytes) -> bytes:
    s = list(range(256))
    j = 0
    for i in range(256):
        j = (j + s[i] + key[i % len(key)]) & 0xFF
        s[i], s[j] = s[j], s[i]
    out = bytearray(len(data))
    i = j = 0
    for n, b in enumerate(data):
        i = (i + 1) & 0xFF
        j = (j + s[i]) & 0xFF
        s[i], s[j] = s[j], s[i]
        out[n] = b ^ s[(s[i] + s[j]) & 0xFF]
    return bytes(out)


def _aes_cbc(key: bytes, data: bytes, decrypt: bool = True, iv: bytes | None = None, unpad: bool = True) -> bytes:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    if iv is None:
        iv, data = data[:16], data[16:]
    if not data:
        return b""
    data = data[: len(data) - len(data) % 16]
    c = Cipher(algorithms.AES(key), modes.CBC(iv))
    op = c.decryptor() if decrypt else c.encryptor()
    out = op.update(data) + op.finalize()
    if decrypt and unpad and out and 1 <= out[-1] <= 16:
        out = out[: -out[-1]]
    return out


class _Crypt:
    def __init__(self, enc: dict, file_id: bytes, resolve):
        self.v = int(resolve(enc.get("V", 0)) or 0)
        self.r = int(resolve(enc.get("R", 2)) or 2)
        self.method = "RC4"
        length = int(resolve(enc.get("Length", 40)) or 40)
        if self.v >= 4:
            cf = resolve(enc.get("CF")) or {}
            stmf = resolve(enc.get("StmF", Name("Identity")))
            cfd = resolve(cf.get(stmf, {})) if isinstance(cf, dict) else {}
            cfm = str(resolve(cfd.get("CFM", "V2"))) if cfd else "None"
            self.method = {"AESV2": "AES", "AESV3": "AES256", "V2": "RC4"}.get(cfm, "NONE")
            if cfd and cfd.get("Length"):
                ln = int(resolve(cfd.get("Length")))
                length = ln * 8 if ln <= 32 else ln
        o, u = resolve(enc.get("O", b"")), resolve(enc.get("U", b""))
        p = int(resolve(enc.get("P", 0)) or 0)
        encrypt_meta = resolve(enc.get("EncryptMetadata", True)) is not False
        if self.r >= 5:
            self.method = "AES256"
            ue = resolve(enc.get("UE", b""))
            if self.r == 5:
                ikey = hashlib.sha256(b"" + u[40:48]).digest()
            else:
                ikey = self._hash_r6(b"", u[40:48], b"")
            check = hashlib.sha256(b"" + u[32:40]).digest() if self.r == 5 else self._hash_r6(b"", u[32:40], b"")
            if check != u[:32]:
                raise PDFError("PDF защищён паролем на открытие — без пароля не читается")
            self.key = _aes_cbc(ikey, ue[:32], iv=bytes(16), unpad=False)
        else:
            n = 5 if self.r == 2 else max(5, length // 8)
            h = hashlib.md5(_PAD + o[:32] + struct.pack("<i", p) + (file_id or b""))
            if self.r >= 4 and not encrypt_meta:
                h.update(b"\xff\xff\xff\xff")
            key = h.digest()[:n]
            if self.r >= 3:
                for _ in range(50):
                    key = hashlib.md5(key).digest()[:n]
            self.key = key
            # пустой ли пароль пользователя (иначе расшифровка даст мусор)
            if self.r == 2:
                ok = _rc4(key, _PAD) == u[:32]
            else:
                x = _rc4(key, hashlib.md5(_PAD + (file_id or b"")).digest())
                for i in range(1, 20):
                    x = _rc4(bytes(b ^ i for b in key), x)
                ok = x == u[:16]
            if not ok:
                raise PDFError("PDF защищён паролем на открытие — без пароля не читается")

    @staticmethod
    def _hash_r6(password: bytes, salt: bytes, udata: bytes) -> bytes:
        k = hashlib.sha256(password + salt + udata).digest()
        i = 0
        while True:
            k1 = (password + k + udata) * 64
            e = _aes_cbc(k[:16], k1, decrypt=False, iv=k[16:32], unpad=False)
            mod = sum(e[:16]) % 3
            k = (hashlib.sha256, hashlib.sha384, hashlib.sha512)[mod](e).digest()
            i += 1
            if i >= 64 and e[-1] <= i - 32:
                break
        return k[:32]

    def decrypt(self, data: bytes, num: int, gen: int) -> bytes:
        if self.method == "NONE" or not data:
            return data
        if self.method == "AES256":
            return _aes_cbc(self.key, data)
        salt = b"sAlT" if self.method == "AES" else b""
        k = hashlib.md5(self.key + struct.pack("<i", num)[:3] + struct.pack("<i", gen)[:2] + salt).digest()
        k = k[: min(len(self.key) + 5, 16)]
        return _aes_cbc(k, data) if self.method == "AES" else _rc4(k, data)


# =============================================================================== документ

_OBJ_HEAD = re.compile(rb"(?<!\d)(\d{1,10})[\x00\t\n\x0c\r ]+(\d{1,5})[\x00\t\n\x0c\r ]+obj\b")


class PDFDocument:
    def __init__(self, data: bytes):
        if not data.lstrip()[:5].startswith(b"%PDF") and b"%PDF" not in data[:1024]:
            raise PDFError("это не PDF")
        self.data = data
        self.xref: dict[int, tuple] = {}
        self.trailer: dict = {}
        self._cache: dict[int, object] = {}
        self._objstm: dict[int, dict[int, object]] = {}
        self._scan: dict[int, int] | None = None
        self.crypt: _Crypt | None = None
        self.warnings: list[str] = []
        self._xref_broken = False
        try:
            self._load_xref()
        except Exception as e:  # noqa: BLE001
            self._xref_broken = True
            self.warnings.append(f"xref повреждена ({type(e).__name__}) — восстанавливаю сканированием")
        if not self.trailer.get("Root") or not self.xref or self._xref_broken:
            self._rebuild()
        enc = self.trailer.get("Encrypt")
        if enc is not None:
            ids = self.resolve(self.trailer.get("ID")) or [b""]
            try:
                fid = self.resolve(ids[0]) if isinstance(ids, list) and ids else b""
                self.crypt = _Crypt(self.resolve(enc), fid if isinstance(fid, bytes) else b"", self.resolve)
                self._encrypt_ref = enc.num if isinstance(enc, Ref) else None
            except PDFError:
                raise
            except Exception as e:  # noqa: BLE001
                raise PDFError(f"PDF зашифрован и не открывается без пароля ({type(e).__name__})")
        self.pages = self._collect_pages()

    # ------------------------------------------------------------------ xref
    def _load_xref(self):
        d = self.data
        sx = d.rfind(b"startxref")
        if sx < 0:
            raise PDFError("нет startxref")
        m = re.match(rb"startxref\s+(\d+)", d[sx:sx + 40])
        pos = int(m.group(1))
        seen = set()
        while pos is not None and pos not in seen and 0 <= pos < len(d):
            seen.add(pos)
            p = pos
            while p < len(d) and d[p:p + 1] in _WS:
                p += 1
            try:
                if d[p:p + 4] == b"xref":
                    trailer = self._read_xref_table(p + 4)
                else:
                    trailer = self._read_xref_stream(p)
            except Exception:  # noqa: BLE001  — битая (старая) секция: остальное восстановим сканированием
                self._xref_broken = True
                break
            for k, v in trailer.items():
                self.trailer.setdefault(k, v)
            if "XRefStm" in trailer:
                try:
                    self._read_xref_stream(int(trailer["XRefStm"]))
                except Exception:  # noqa: BLE001
                    pass
            prev = trailer.get("Prev")
            pos = int(prev) if isinstance(prev, (int, float)) else None

    def _read_xref_table(self, p: int) -> dict:
        d = self.data
        sub = re.compile(rb"\s*(\d+)\s+(\d+)[ \t]*\r?\n?")
        ent = re.compile(rb"\s*(\d{1,10})\s+(\d{1,5})\s+([nf])")
        while True:
            m = sub.match(d, p)
            if not m or d[m.start():m.end()].strip().startswith(b"trailer"):
                break
            start, count = int(m.group(1)), int(m.group(2))
            p = m.end()
            for i in range(count):
                e = ent.match(d, p)
                if not e:
                    break
                p = e.end()
                num = start + i
                if e.group(3) == b"n" and num not in self.xref:
                    self.xref[num] = (1, int(e.group(1)), int(e.group(2)))
                elif num not in self.xref:
                    self.xref[num] = (0, 0, 0)
        t = d.find(b"trailer", p)
        if t < 0:
            return {}
        obj, _ = parse_object(d, t + 7)
        return obj if isinstance(obj, dict) else {}

    def _read_xref_stream(self, p: int) -> dict:
        m = _OBJ_HEAD.match(self.data, p)
        if not m:
            raise PDFError("ожидался объект xref-потока")
        obj = self._parse_indirect_at(p, int(m.group(1)), int(m.group(2)), decrypt=False)
        if not isinstance(obj, Stream):
            raise PDFError("xref не поток")
        sd = obj.dict
        w = [int(x) for x in sd.get("W", [1, 2, 1])]
        size = int(sd.get("Size", 0))
        index = sd.get("Index", [0, size])
        data = self.stream_bytes(obj, decrypt=False)
        rec = sum(w)
        if rec <= 0 or any(x < 0 or x > 8 for x in w):
            raise PDFError("некорректный /W в xref-потоке")
        i = 0
        for k in range(0, len(index) - 1, 2):
            start, count = int(index[k]), int(index[k + 1])
            for j in range(count):
                if i + rec > len(data):
                    break
                fields, q = [], i
                for width in w:
                    fields.append(int.from_bytes(data[q:q + width], "big") if width else None)
                    q += width
                i += rec
                t = fields[0] if w[0] else 1
                num = start + j
                if num in self.xref:
                    continue
                if t == 1:
                    self.xref[num] = (1, fields[1], fields[2] or 0)
                elif t == 2:
                    self.xref[num] = (2, fields[1], fields[2])
                else:
                    self.xref[num] = (0, 0, 0)
        return sd

    def _rebuild(self):
        """Восстановление: объекты, найденные сканированием файла, дополняют то, что прочитано из xref;
        члены объектных потоков (/ObjStm) тоже попадают в таблицу.
        """
        self._scan_objects()
        for n, off in self._scan.items():
            if n not in self.xref or self.xref[n][0] == 0:
                self.xref[n] = (1, off, 0)
        for n, off in sorted(self._scan.items(), key=lambda t: t[1]):
            head = self.data[off:off + 400]
            if re.search(rb"/Type\s*/XRef\b", head):
                try:
                    t = self._read_xref_stream(off)
                    for k, v in t.items():
                        if k in ("Root", "Encrypt", "ID", "Info"):
                            self.trailer.setdefault(k, v)
                except Exception:  # noqa: BLE001
                    pass
            if re.search(rb"/Type\s*/ObjStm\b", head):
                stm = self.get(n)
                if isinstance(stm, Stream):
                    try:
                        data = self.stream_bytes(stm)
                        cnt, first = int(stm.dict.get("N", 0)), int(stm.dict.get("First", 0))
                        nums = [t[1] for t in tokenize(data, 0, first) if t[0] == "obj"]
                        for k in range(0, min(len(nums), 2 * cnt) - 1, 2):
                            member = int(nums[k])
                            if member not in self.xref or self.xref[member][0] == 0:
                                self.xref[member] = (2, n, k // 2)
                    except Exception:  # noqa: BLE001
                        pass
        for m in re.finditer(rb"trailer\s*<<", self.data):
            t, _ = parse_object(self.data, m.start() + 7)
            if isinstance(t, dict):
                for k, v in t.items():
                    self.trailer.setdefault(k, v)
        if "Root" not in self.trailer:
            for num in self._scan:
                head = self.data[self._scan[num]:self._scan[num] + 300]
                if re.search(rb"/Type\s*/Catalog\b", head):
                    self.trailer["Root"] = Ref(num, 0)
                    break
        if "Root" not in self.trailer:
            raise PDFError("не найден каталог документа")

    def _scan_objects(self):
        if self._scan is None:
            self._scan = {}
            for m in _OBJ_HEAD.finditer(self.data):
                self._scan[int(m.group(1))] = m.start()  # последнее вхождение — самое новое

    # ------------------------------------------------------------------ объекты
    def resolve(self, obj, depth: int = 0):
        while isinstance(obj, Ref) and depth < 32:
            obj = self.get(obj.num)
            depth += 1
        return obj

    def get(self, num: int):
        if num in self._cache:
            return self._cache[num]
        self._cache[num] = None  # защита от циклов
        entry = self.xref.get(num)
        obj = None
        try:
            if entry and entry[0] == 1:
                obj = self._parse_indirect_at(entry[1], num, entry[2])
            elif entry and entry[0] == 2:
                obj = self._from_objstm(entry[1], entry[2], num)
            else:
                self._scan_objects()
                if num in self._scan:
                    obj = self._parse_indirect_at(self._scan[num], num, 0)
        except Exception:  # noqa: BLE001
            self._scan_objects()
            if num in self._scan:
                try:
                    obj = self._parse_indirect_at(self._scan[num], num, 0)
                except Exception:  # noqa: BLE001
                    obj = None
        self._cache[num] = obj
        return obj

    def _parse_indirect_at(self, pos: int, num: int, gen: int, decrypt: bool = True):
        d = self.data
        m = _OBJ_HEAD.match(d, pos)
        if not m or int(m.group(1)) != num:
            # смещение в xref неточное — ищем заголовок рядом, иначе по скану файла
            win = d[max(0, pos - 64):pos + 64]
            mm = re.search(rb"(?<!\d)" + str(num).encode() + rb"\s+\d+\s+obj\b", win)
            if mm:
                pos = max(0, pos - 64) + mm.start()
            else:
                self._scan_objects()
                if num not in self._scan:
                    raise PDFError(f"объект {num} не найден")
                pos = self._scan[num]
            m = _OBJ_HEAD.match(d, pos)
            if not m:
                raise PDFError(f"объект {num} повреждён")
        gen = int(m.group(2))
        obj, p = parse_object(d, m.end())
        crypt = self.crypt if decrypt and getattr(self, "_encrypt_ref", None) != num else None
        if isinstance(obj, dict):
            k = re.match(rb"\s*stream\r?\n?", d[p:p + 12])
            if k:
                start = p + k.end()
                length = obj.get("Length")
                if isinstance(length, Ref):
                    length = self.resolve(length)
                raw = None
                if isinstance(length, int) and 0 <= length and d[start + length:start + length + 30].lstrip()[:9] == b"endstream":
                    raw = d[start:start + length]
                if raw is None:
                    e = d.find(b"endstream", start)
                    raw = d[start:e if e >= 0 else len(d)]
                    raw = raw[:-2] if raw.endswith(b"\r\n") else raw[:-1] if raw.endswith((b"\n", b"\r")) else raw
                if crypt and obj.get("Type") != "XRef":
                    raw = crypt.decrypt(raw, num, gen)
                if crypt:
                    obj = self._decrypt_strings(obj, crypt, num, gen)
                return Stream(obj, raw, num, gen)
        if crypt:
            obj = self._decrypt_strings(obj, crypt, num, gen)
        return obj

    def _decrypt_strings(self, obj, crypt, num, gen):
        if isinstance(obj, bytes) and not isinstance(obj, Keyword):
            return crypt.decrypt(obj, num, gen)
        if isinstance(obj, list):
            return [self._decrypt_strings(x, crypt, num, gen) for x in obj]
        if isinstance(obj, dict):
            return {k: self._decrypt_strings(v, crypt, num, gen) for k, v in obj.items()}
        return obj

    def _from_objstm(self, stm_num: int, idx: int, num: int):
        if stm_num not in self._objstm:
            stm = self.get(stm_num)
            table: dict[int, object] = {}
            if isinstance(stm, Stream):
                data = self.stream_bytes(stm)
                n, first = int(stm.dict.get("N", 0)), int(stm.dict.get("First", 0))
                head = [t[1] for t in tokenize(data, 0, first) if t[0] == "obj"]
                pairs = [(int(head[i]), int(head[i + 1])) for i in range(0, min(len(head), 2 * n) - 1, 2)]
                for k, (onum, off) in enumerate(pairs):
                    end = first + pairs[k + 1][1] if k + 1 < len(pairs) else len(data)
                    try:
                        table[onum] = parse_object(data, first + off, end)[0]
                    except Exception:  # noqa: BLE001
                        table[onum] = None
            self._objstm[stm_num] = table
        return self._objstm[stm_num].get(num)

    # ------------------------------------------------------------------ потоки
    def stream_bytes(self, stm: Stream, decrypt: bool = True, stop_at_image: bool = False):
        """Распакованные данные потока. stop_at_image=True → (data, имя_картинного_фильтра, параметры)."""
        if stm._decoded is not None and not stop_at_image:
            return stm._decoded
        filters = self.resolve(stm.dict.get("Filter"))
        parms = self.resolve(stm.dict.get("DecodeParms", stm.dict.get("DP")))
        if not isinstance(filters, list):
            filters = [filters] if filters else []
        if not isinstance(parms, list):
            parms = [parms] * len(filters)
        data = stm.raw
        for i, f in enumerate(filters):
            f = str(self.resolve(f))
            p = self.resolve(parms[i]) if i < len(parms) else None
            p = p if isinstance(p, dict) else {}
            if f in IMAGE_FILTERS:
                if stop_at_image:
                    return data, f, {k: self.resolve(v) for k, v in p.items()}
                break
            if f in ("FlateDecode", "Fl"):
                data = _flate(data)
            elif f in ("LZWDecode", "LZW"):
                data = _lzw(data, int(p.get("EarlyChange", 1)))
            elif f in ("ASCIIHexDecode", "AHx"):
                data = _hex(data.split(b">")[0])
                continue
            elif f in ("ASCII85Decode", "A85"):
                data = _a85(data)
                continue
            elif f in ("RunLengthDecode", "RL"):
                data = _rle(data)
                continue
            elif f == "Crypt":
                continue
            else:
                break
            pred = int(self.resolve(p.get("Predictor", 1)) or 1)
            if pred > 1:
                data = _png_unpredict(data, pred, int(p.get("Colors", 1)), int(p.get("BitsPerComponent", 8)),
                                      int(p.get("Columns", 1)))
        if stop_at_image:
            return data, None, {}
        stm._decoded = data
        return data

    # ------------------------------------------------------------------ страницы
    def _collect_pages(self) -> list[dict]:
        root = self.resolve(self.trailer.get("Root"))
        pages_root = self.resolve(root.get("Pages")) if isinstance(root, dict) else None
        out: list[dict] = []
        inherit_keys = ("Resources", "MediaBox", "CropBox", "Rotate")

        def walk(node, inherited, depth=0, seen=None):
            seen = seen if seen is not None else set()
            if depth > 64 or not isinstance(node, dict) or id(node) in seen:
                return
            seen.add(id(node))
            inh = dict(inherited)
            for k in inherit_keys:
                if k in node:
                    inh[k] = node[k]
            kids = self.resolve(node.get("Kids"))
            if not isinstance(kids, list):
                kids = [kids] if isinstance(kids, (dict, Ref)) else []
            if node.get("Type") == "Pages" or (kids and node.get("Type") != "Page"):
                for kid in kids or []:
                    walk(self.resolve(kid), inh, depth + 1, seen)
            else:
                page = dict(node)
                for k, v in inh.items():
                    page.setdefault(k, v)
                out.append(page)

        walk(pages_root, {})
        if not out:  # дерево страниц сломано — собираем объекты /Type /Page
            self._scan_objects()
            for num in sorted(self._scan):
                o = self.get(num)
                if isinstance(o, dict) and o.get("Type") == "Page":
                    out.append(o)
        return out

    @property
    def page_count(self) -> int:
        return len(self.pages)


def count_pages(path: str | Path) -> int:
    return PDFDocument(Path(path).read_bytes()).page_count


# =============================================================================== шрифты и CMap

_STD_GLYPHS = {
    "space": " ", "exclam": "!", "quotedbl": '"', "numbersign": "#", "dollar": "$", "percent": "%",
    "ampersand": "&", "quotesingle": "'", "parenleft": "(", "parenright": ")", "asterisk": "*", "plus": "+",
    "comma": ",", "hyphen": "-", "period": ".", "slash": "/", "colon": ":", "semicolon": ";", "less": "<",
    "equal": "=", "greater": ">", "question": "?", "at": "@", "bracketleft": "[", "backslash": "\\",
    "bracketright": "]", "asciicircum": "^", "underscore": "_", "grave": "`", "braceleft": "{", "bar": "|",
    "braceright": "}", "asciitilde": "~", "bullet": "•", "endash": "–", "emdash": "—", "quotedblleft": "“",
    "quotedblright": "”", "quoteleft": "‘", "quoteright": "’", "quotesinglbase": "‚", "quotedblbase": "„",
    "guillemotleft": "«", "guillemotright": "»", "guilsinglleft": "‹", "guilsinglright": "›", "ellipsis": "…",
    "degree": "°", "section": "§", "copyright": "©", "registered": "®", "trademark": "™", "afii61352": "№",
    "nbspace": " ", "uni00A0": " ", "minus": "−", "multiply": "×", "divide": "÷", "plusminus": "±",
    "Euro": "€", "sterling": "£", "yen": "¥", "cent": "¢", "periodcentered": "·", "dagger": "†",
    "daggerdbl": "‡", "fi": "fi", "fl": "fl", "paragraph": "¶", "mu": "µ", "onehalf": "½", "onequarter": "¼",
    "threequarters": "¾", "arrowright": "→", "arrowleft": "←", "lessequal": "≤", "greaterequal": "≥",
    "notequal": "≠", "approxequal": "≈", "infinity": "∞", "perthousand": "‰", "germandbls": "ß",
    "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7",
    "eight": "8", "nine": "9", "afii10023": "Ё", "afii10071": "ё", "afii10055": "Ґ", "afii10103": "ґ",
    "afii10053": "Є", "afii10101": "є", "afii10056": "І", "afii10104": "і", "afii10057": "Ї", "afii10105": "ї",
}
for _i, _c in enumerate(list("АБВГДЕ")):
    _STD_GLYPHS[f"afii{10017 + _i}"] = _c
for _i, _c in enumerate(list("ЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")):
    _STD_GLYPHS[f"afii{10024 + _i}"] = _c
for _i, _c in enumerate(list("абвгде")):
    _STD_GLYPHS[f"afii{10065 + _i}"] = _c
for _i, _c in enumerate(list("жзийклмнопрстуфхцчшщъыьэюя")):
    _STD_GLYPHS[f"afii{10072 + _i}"] = _c
for _c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
    _STD_GLYPHS[_c] = _c


def _safe_chr(cp: int) -> str:
    """chr без одиночных суррогатов и недопустимых кодов (иначе запись в UTF-8 падает)."""
    if 0 <= cp < 0x110000 and not 0xD800 <= cp <= 0xDFFF:
        return chr(cp)
    return ""


def glyph_to_unicode(name: str) -> str:
    if name in _STD_GLYPHS:
        return _STD_GLYPHS[name]
    base = name.split(".")[0].split("_")[0]
    if base in _STD_GLYPHS:
        return _STD_GLYPHS[base]
    m = re.fullmatch(r"uni([0-9A-Fa-f]{4})+", base)
    if m:
        h = base[3:]
        return "".join(_safe_chr(int(h[i:i + 4], 16)) for i in range(0, len(h), 4))
    m = re.fullmatch(r"u([0-9A-Fa-f]{4,6})", base)
    if m:
        return _safe_chr(int(m.group(1), 16))
    try:  # полный Adobe Glyph List — из fontTools (есть в Anaconda)
        from fontTools.agl import toUnicode
        u = toUnicode(name)
        return "".join(c for c in u if not 0xD800 <= ord(c) <= 0xDFFF)
    except Exception:  # noqa: BLE001
        return ""


# Adobe StandardEncoding: коды 0x80–0xFF, отличные от Latin-1 (PDF 1.7, приложение D)
_STANDARD_HIGH = dict(zip(
    [0xA1, 0xA2, 0xA3, 0xA4, 0xA5, 0xA6, 0xA7, 0xA8, 0xA9, 0xAA, 0xAB, 0xAC, 0xAD, 0xAE, 0xAF, 0xB1, 0xB2, 0xB3,
     0xB4, 0xB6, 0xB7, 0xB8, 0xB9, 0xBA, 0xBB, 0xBC, 0xBD, 0xBF, 0xC1, 0xC2, 0xC3, 0xC4, 0xC5, 0xC6, 0xC7, 0xC8,
     0xCA, 0xCB, 0xCD, 0xCE, 0xCF, 0xD0, 0xE1, 0xE3, 0xE8, 0xE9, 0xEA, 0xEB, 0xF1, 0xF5, 0xF8, 0xF9, 0xFA, 0xFB],
    "¡¢£⁄¥ƒ§¤'“«‹›ﬁﬂ–†‡·¶•‚„”»…‰¿`´ˆ˜¯˘˙¨˚¸˝˛ˇ—ÆªŁØŒºæıłøœß"))


def _base_table(name: str) -> list[str]:
    codec = {"WinAnsiEncoding": "cp1252", "MacRomanEncoding": "mac_roman"}.get(name, "latin-1")
    table = []
    for i in range(256):
        try:
            ch = bytes([i]).decode(codec)
        except UnicodeDecodeError:
            ch = ""
        table.append("" if 0x80 <= ord(ch or "a") <= 0x9F else ch)  # управляющие C1 — не текст
    if name == "StandardEncoding":
        table[0x27], table[0x60] = "’", "‘"
        for code in range(0x80, 0x100):
            table[code] = _STANDARD_HIGH.get(code, "")
    return table


_AFM_CACHE: dict[str, dict[str, float]] = {}
_BASE14 = {"helvetica": "Helvetica", "arial": "Helvetica", "times": "Times-Roman", "timesnewroman": "Times-Roman",
           "courier": "Courier", "couriernew": "Courier", "symbol": "Symbol", "zapfdingbats": "ZapfDingbats"}


def _afm_widths(base_font: str) -> dict[str, float]:
    """Ширины 14 стандартных шрифтов (для PDF без /Widths) из AFM-файлов matplotlib: символ → ширина."""
    name = re.sub(r"^[A-Z]{6}\+", "", base_font or "")
    low = re.sub(r"[^a-z]", "", name.lower())
    fam = next((v for k, v in _BASE14.items() if low.startswith(k)), None)
    if fam is None:
        return {}
    bold = "bold" in low
    ital = "italic" in low or "oblique" in low
    if fam == "Helvetica":
        fname = "Helvetica" + ("-BoldOblique" if bold and ital else "-Bold" if bold else "-Oblique" if ital else "")
    elif fam == "Times-Roman":
        fname = "Times-" + ("BoldItalic" if bold and ital else "Bold" if bold else "Italic" if ital else "Roman")
    elif fam == "Courier":
        fname = "Courier" + ("-BoldOblique" if bold and ital else "-Bold" if bold else "-Oblique" if ital else "")
    else:
        fname = fam
    if fname in _AFM_CACHE:
        return _AFM_CACHE[fname]
    widths: dict[str, float] = {}
    try:
        import matplotlib
        path = Path(matplotlib.get_data_path()) / "fonts" / "pdfcorefonts" / (fname + ".afm")
        for line in path.read_text(encoding="latin-1").splitlines():
            m = re.match(r"C\s+-?\d+\s*;\s*WX\s+([\d.]+)\s*;\s*N\s+(\S+)", line)
            if m:
                u = glyph_to_unicode(m.group(2))
                if u:
                    widths.setdefault(u, float(m.group(1)))
    except Exception:  # noqa: BLE001
        widths = {}
    _AFM_CACHE[fname] = widths
    return widths


class CMap:
    """ToUnicode CMap: длины кодов (codespace) + код → строка."""

    def __init__(self, data: bytes):
        self.ranges: list[tuple[int, int, int]] = []  # (длина, начало, конец)
        self.map: dict[tuple[int, int], str] = {}
        toks = [t for t in tokenize(data)]
        i, n = 0, len(toks)

        def u16(b: bytes) -> str:
            try:
                return b.decode("utf-16-be")
            except UnicodeDecodeError:
                return b.decode("latin-1")

        while i < n:
            kind, val, _ = toks[i]
            if kind == "kw" and val == b"begincodespacerange":
                i += 1
                while i + 1 < n and not (toks[i][0] == "kw" and toks[i][1] == b"endcodespacerange"):
                    a, b = toks[i][1], toks[i + 1][1]
                    if isinstance(a, bytes) and isinstance(b, bytes):
                        self.ranges.append((len(a), int.from_bytes(a, "big"), int.from_bytes(b, "big")))
                    i += 2
            elif kind == "kw" and val == b"beginbfchar":
                i += 1
                while i + 1 < n and not (toks[i][0] == "kw" and toks[i][1] == b"endbfchar"):
                    a, b = toks[i][1], toks[i + 1][1]
                    if isinstance(a, bytes) and isinstance(b, (bytes, Name)):
                        self.map[(len(a), int.from_bytes(a, "big"))] = u16(b) if isinstance(b, bytes) \
                            else glyph_to_unicode(str(b))
                    i += 2
            elif kind == "kw" and val == b"beginbfrange":
                i += 1
                while i + 2 < n and not (toks[i][0] == "kw" and toks[i][1] == b"endbfrange"):
                    a, b = toks[i][1], toks[i + 1][1]
                    if toks[i + 2][0] == "aopen":
                        j = i + 3
                        arr = []
                        while j < n and toks[j][0] != "aclose":
                            arr.append(toks[j][1])
                            j += 1
                        if isinstance(a, bytes) and isinstance(b, bytes):
                            s = int.from_bytes(a, "big")
                            for k, dst in enumerate(arr):
                                if isinstance(dst, bytes):
                                    self.map[(len(a), s + k)] = u16(dst)
                        i = j + 1
                        continue
                    dst = toks[i + 2][1]
                    if isinstance(a, bytes) and isinstance(b, bytes) and isinstance(dst, bytes):
                        s, e = int.from_bytes(a, "big"), int.from_bytes(b, "big")
                        if e - s < 65536:
                            base = int.from_bytes(dst, "big") if dst else 0
                            prefix = dst[:-2] if len(dst) > 2 else b""
                            for k in range(e - s + 1):
                                if len(dst) <= 2:
                                    self.map[(len(a), s + k)] = _safe_chr((base + k) & 0xFFFF)
                                else:
                                    last = int.from_bytes(dst[-2:], "big") + k
                                    self.map[(len(a), s + k)] = u16(prefix + (last & 0xFFFF).to_bytes(2, "big"))
                    i += 3
            else:
                i += 1
        if not self.ranges:
            lens = {k[0] for k in self.map} or {2}
            self.ranges = [(ln, 0, (1 << (8 * ln)) - 1) for ln in sorted(lens)]

    def split(self, data: bytes) -> list[tuple[int, int]]:
        """Байты → [(длина, код)] по диапазонам codespace."""
        out, i = [], 0
        lens = sorted({r[0] for r in self.ranges})
        while i < len(data):
            for ln in lens:
                code = int.from_bytes(data[i:i + ln], "big")
                if len(data) - i >= ln and any(r[0] == ln and r[1] <= code <= r[2] for r in self.ranges):
                    out.append((ln, code))
                    i += ln
                    break
            else:
                ln = lens[0]
                out.append((ln, int.from_bytes(data[i:i + ln], "big")))
                i += ln
        return out


class Font:
    def __init__(self, doc: PDFDocument, fd: dict):
        r = doc.resolve
        self.subtype = str(r(fd.get("Subtype", "")))
        self.cid = self.subtype == "Type0"
        self.fm0 = 0.001
        if self.subtype == "Type3":
            fm = r(fd.get("FontMatrix")) or [0.001]
            self.fm0 = float(r(fm[0])) if fm else 0.001
        self.cmap: CMap | None = None
        tu = r(fd.get("ToUnicode"))
        if isinstance(tu, Stream):
            try:
                self.cmap = CMap(doc.stream_bytes(tu))
            except Exception:  # noqa: BLE001
                self.cmap = None
        self.widths: dict[int, float] = {}
        self.default_w = 500.0
        self.gid_uni: dict[int, str] = {}
        self.identity = False
        if self.cid:
            enc = r(fd.get("Encoding"))
            self.identity = not isinstance(enc, Name) or "Identity" in str(enc)
            descs = r(fd.get("DescendantFonts"))
            desc = r(descs[0]) if isinstance(descs, list) and descs else {}
            desc = desc if isinstance(desc, dict) else {}
            self.default_w = float(r(desc.get("DW", 1000)))
            w = r(desc.get("W")) or []
            i = 0
            while i < len(w):
                first = r(w[i])
                nxt = r(w[i + 1]) if i + 1 < len(w) else None
                if isinstance(nxt, list):
                    for k, val in enumerate(nxt):
                        self.widths[int(first) + k] = float(r(val))
                    i += 2
                elif i + 2 < len(w):
                    if 0 <= int(nxt) - int(first) <= 65535:  # защита от «/W [0 300000000 500]»
                        for c in range(int(first), int(nxt) + 1):
                            self.widths[c] = float(r(w[i + 2]))
                    i += 3
                else:
                    break
            if self.cmap is None:
                self._load_font_cmap(doc, r(desc.get("FontDescriptor")) or {}, desc)
        else:
            first = int(r(fd.get("FirstChar", 0)) or 0)
            for k, val in enumerate(r(fd.get("Widths")) or []):
                try:
                    self.widths[first + k] = float(r(val))
                except (TypeError, ValueError):
                    pass
            fdesc = r(fd.get("FontDescriptor")) or {}
            if isinstance(fdesc, dict) and fdesc.get("MissingWidth"):
                self.default_w = float(r(fdesc["MissingWidth"]))
            enc = r(fd.get("Encoding"))
            base = "StandardEncoding"
            diffs = []
            if isinstance(enc, Name):
                base = str(enc)
            elif isinstance(enc, dict):
                base = str(r(enc.get("BaseEncoding", "StandardEncoding")))
                diffs = r(enc.get("Differences")) or []
            elif "Symbol" in str(fd.get("BaseFont", "")) or (isinstance(fdesc, dict) and
                                                              int(r(fdesc.get("Flags", 0)) or 0) & 4):
                base = "StandardEncoding"
            if base not in ("WinAnsiEncoding", "MacRomanEncoding", "StandardEncoding"):
                base = "StandardEncoding"
            self.table = _base_table(base if base != "StandardEncoding" or not self.cmap else "WinAnsiEncoding")
            if base == "StandardEncoding" and not diffs and self.subtype == "TrueType":
                self.table = _base_table("WinAnsiEncoding")
            code = 0
            for d in diffs:
                d = r(d)
                if isinstance(d, (int, float)):
                    code = int(d)
                elif isinstance(d, Name):
                    if 0 <= code < 256:
                        self.table[code] = glyph_to_unicode(str(d))
                    code += 1
            if not self.widths:  # стандартный шрифт без /Widths: ширины из AFM (иначе слова слипаются)
                afm = _afm_widths(str(r(fd.get("BaseFont", ""))))
                for code in range(256):
                    u = self.cmap.map.get((1, code)) if self.cmap else None
                    u = u or self.table[code]
                    if u in afm:
                        self.widths[code] = afm[u]

    def _load_font_cmap(self, doc, fdesc: dict, desc: dict):
        """Нет ToUnicode: пробуем таблицу cmap встроенного TrueType/OpenType-шрифта (fontTools)."""
        r = doc.resolve
        ff = r(fdesc.get("FontFile2")) or r(fdesc.get("FontFile3"))
        if not isinstance(ff, Stream):
            return
        try:
            from fontTools.ttLib import TTFont
            font = TTFont(io.BytesIO(doc.stream_bytes(ff)), lazy=True)
            best = font.getBestCmap() or {}
            order = font.getGlyphOrder()
            gid = {name: i for i, name in enumerate(order)}
            cid2gid = None
            c2g = r(desc.get("CIDToGIDMap"))
            if isinstance(c2g, Stream):
                raw = doc.stream_bytes(c2g)
                cid2gid = {i // 2: int.from_bytes(raw[i:i + 2], "big") for i in range(0, len(raw) - 1, 2)}
            rev = {}
            for uni, name in best.items():
                g = gid.get(name)
                if g is not None and g not in rev:
                    rev[g] = _safe_chr(uni)
            if cid2gid:
                self.gid_uni = {cid: rev[g] for cid, g in cid2gid.items() if g in rev}
            else:
                self.gid_uni = rev
        except Exception:  # noqa: BLE001
            self.gid_uni = {}

    def decode(self, s: bytes) -> list[tuple[str, float, bool]]:
        """→ [(текст, ширина в ед. текста, это_пробел_кода_32)]"""
        out = []
        if self.cid:
            if self.cmap and not self.identity:
                codes = self.cmap.split(s)
            else:  # Identity-H/V — всегда 2-байтовые коды, что бы ни заявлял codespace в ToUnicode
                codes = [(2, int.from_bytes(s[i:i + 2], "big")) for i in range(0, len(s) - 1, 2)]
            for ln, code in codes:
                if self.cmap:
                    u = self.cmap.map.get((ln, code)) or (self.cmap.map.get((1, code), "") if code < 256 else "")
                else:
                    u = self.gid_uni.get(code, "")
                w = self.widths.get(code, self.default_w) * self.fm0
                out.append((u, w, False))
        else:
            for b in s:
                if self.cmap and (1, b) in self.cmap.map:
                    u = self.cmap.map[(1, b)]
                else:
                    u = self.table[b]
                w = self.widths.get(b, self.default_w) * self.fm0
                out.append((u, w, b == 32))
        return out


# =============================================================================== содержимое страницы

def _mul(a, b):
    return [a[0] * b[0] + a[1] * b[2], a[0] * b[1] + a[1] * b[3],
            a[2] * b[0] + a[3] * b[2], a[2] * b[1] + a[3] * b[3],
            a[4] * b[0] + a[5] * b[2] + b[4], a[4] * b[1] + a[5] * b[3] + b[5]]


_PATH_OPS = {b"m", b"l", b"c", b"v", b"y", b"re"}
_PAINT_OPS = {b"S", b"s", b"f", b"F", b"f*", b"B", b"B*", b"b", b"b*"}


class PageReader:
    """Интерпретатор потока содержимого: текстовые фрагменты с координатами + статистика графики."""

    def __init__(self, doc: PDFDocument, page: dict):
        self.doc = doc
        self.page = page
        r = doc.resolve
        box = r(page.get("CropBox")) or r(page.get("MediaBox")) or [0, 0, 612, 792]
        try:
            box = [float(r(x)) for x in box][:4]
        except (TypeError, ValueError):
            box = [0, 0, 612, 792]
        if len(box) < 4:
            box = [0, 0, 612, 792]
        self.box = box
        self.width, self.height = abs(box[2] - box[0]), abs(box[3] - box[1])
        try:
            self.rotate = int(r(page.get("Rotate", 0)) or 0) % 360
        except (TypeError, ValueError):
            self.rotate = 0
        self.spans: list[tuple[float, float, float, float, float, str]] = []  # x0, y0, x1, y1, size, text
        self.image_area = 0.0
        self.images: list[tuple[float, Stream]] = []
        self.path_ops = 0
        self.paint_ops = 0
        self._fonts: dict = {}
        self._forms_seen = 0

    @property
    def page_area(self) -> float:
        return max(self.width * self.height, 1.0)

    def run(self):
        contents = self.doc.resolve(self.page.get("Contents"))
        if not isinstance(contents, list):
            contents = [contents] if contents is not None else []
        streams = [self.doc.resolve(x) for x in contents]
        data = b"\n".join(self.doc.stream_bytes(c) for c in streams if isinstance(c, Stream))
        res = self.doc.resolve(self.page.get("Resources")) or {}
        self._exec(data, res if isinstance(res, dict) else {}, [1, 0, 0, 1, 0, 0], 0)
        self._annotations(res if isinstance(res, dict) else {})
        return self

    def _annotations(self, page_res: dict):
        """Видимые аннотации с внешним видом (/AP /N): значения полей форм, выноски FreeText, штампы."""
        r = self.doc.resolve
        annots = r(self.page.get("Annots"))
        if not isinstance(annots, list):
            return
        for a in annots[:500]:
            a = r(a)
            if not isinstance(a, dict) or a.get("Subtype") in ("Link", "Popup"):
                continue
            try:
                flags = int(r(a.get("F", 0)) or 0)
                if flags & (2 | 32):  # Hidden / NoView
                    continue
                ap = r(a.get("AP"))
                n = r(ap.get("N")) if isinstance(ap, dict) else None
                if isinstance(n, dict) and not isinstance(n, Stream):  # состояния (флажки) — выбранное /AS
                    n = r(n.get(r(a.get("AS")))) if a.get("AS") is not None else None
                rect = [float(r(x)) for x in (r(a.get("Rect")) or [])][:4]
                if not isinstance(n, Stream) or len(rect) < 4:
                    continue
                bbox = [float(r(x)) for x in (r(n.dict.get("BBox")) or rect)][:4]
                bw, bh = (bbox[2] - bbox[0]) or 1.0, (bbox[3] - bbox[1]) or 1.0
                rx0, ry0 = min(rect[0], rect[2]), min(rect[1], rect[3])
                sx, sy = abs(rect[2] - rect[0]) / abs(bw), abs(rect[3] - rect[1]) / abs(bh)
                m = [sx, 0, 0, sy, rx0 - min(bbox[0], bbox[2]) * sx, ry0 - min(bbox[1], bbox[3]) * sy]
                fm = r(n.dict.get("Matrix")) or [1, 0, 0, 1, 0, 0]
                ares = r(n.dict.get("Resources")) or page_res
                self._exec(self.doc.stream_bytes(n), ares if isinstance(ares, dict) else page_res,
                           _mul([float(r(x)) for x in fm], m), 1)
            except Exception:  # noqa: BLE001
                continue

    def _font(self, res: dict, name) -> Font | None:
        fonts = self.doc.resolve(res.get("Font")) or {}
        ref = fonts.get(name) if isinstance(fonts, dict) else None
        key = ref.num if isinstance(ref, Ref) else (id(ref), name)
        if key not in self._fonts:
            fd = self.doc.resolve(ref)
            try:
                self._fonts[key] = Font(self.doc, fd) if isinstance(fd, dict) else None
            except Exception:  # noqa: BLE001
                self._fonts[key] = None
        return self._fonts[key]

    def _exec(self, data: bytes, res: dict, ctm: list, depth: int):
        ops: list = []
        arrays: list = []
        gstack: list = []
        tm = lm = [1, 0, 0, 1, 0, 0]
        font, fsize, tc, tw, th, tl, rise = None, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0
        gen = tokenize(data)
        while True:
            try:
                kind, val, pos = next(gen)
            except StopIteration:
                break
            if kind == "obj":
                (arrays[-1] if arrays else ops).append(val)
                continue
            if kind == "aopen":
                arrays.append([])
                continue
            if kind == "aclose":
                if arrays:
                    a = arrays.pop()
                    (arrays[-1] if arrays else ops).append(a)
                continue
            if kind != "kw":
                continue  # словари в операндах (BDC) и прочее нам не нужны
            op = bytes(val)
            try:
                if op == b"BI":  # встроенная картинка: учитываем площадь и пропускаем данные до EI
                    m = re.compile(rb"\sID[\s]").search(data, pos)
                    if m:
                        e = re.compile(rb"\sEI(?=[\s]|$)").search(data, m.end())
                        self.image_area += min(abs(ctm[0] * ctm[3] - ctm[1] * ctm[2]), self.page_area)
                        gen = tokenize(data, e.end() if e else len(data))
                elif op == b"q":
                    gstack.append((ctm, font, fsize, tc, tw, th, tl, rise))
                elif op == b"Q":
                    if gstack:
                        ctm, font, fsize, tc, tw, th, tl, rise = gstack.pop()
                elif op == b"cm" and len(ops) >= 6:
                    ctm = _mul([float(x) for x in ops[-6:]], ctm)
                elif op == b"BT":
                    tm = lm = [1, 0, 0, 1, 0, 0]
                elif op == b"Tf" and len(ops) >= 2:
                    font, fsize = self._font(res, ops[-2]), float(ops[-1])
                elif op == b"Tc" and ops:
                    tc = float(ops[-1])
                elif op == b"Tw" and ops:
                    tw = float(ops[-1])
                elif op == b"Tz" and ops:
                    th = float(ops[-1]) / 100.0
                elif op == b"TL" and ops:
                    tl = float(ops[-1])
                elif op == b"Ts" and ops:
                    rise = float(ops[-1])
                elif op in (b"Td", b"TD") and len(ops) >= 2:
                    tx, ty = float(ops[-2]), float(ops[-1])
                    if op == b"TD":
                        tl = -ty
                    lm = _mul([1, 0, 0, 1, tx, ty], lm)
                    tm = lm
                elif op == b"Tm" and len(ops) >= 6:
                    lm = tm = [float(x) for x in ops[-6:]]
                elif op == b"T*":
                    lm = _mul([1, 0, 0, 1, 0, -tl], lm)
                    tm = lm
                elif op in (b"Tj", b"'", b'"', b"TJ") and ops:
                    if op in (b"'", b'"'):
                        if op == b'"' and len(ops) >= 3:
                            tw, tc = float(ops[-3]), float(ops[-2])
                        lm = _mul([1, 0, 0, 1, 0, -tl], lm)
                        tm = lm
                    items = ops[-1] if op == b"TJ" else [ops[-1]]
                    if font is not None and isinstance(items, list):
                        tm = self._show(items, font, fsize, tc, tw, th, tm, ctm)
                elif op == b"Do" and ops:
                    self._do(res, ops[-1], ctm, depth)
                elif op in _PATH_OPS:
                    self.path_ops += 1
                elif op in _PAINT_OPS:
                    self.paint_ops += 1
            except (TypeError, ValueError, IndexError, ZeroDivisionError, AttributeError):
                pass
            ops = []

    def _show(self, items, font: Font, fsize, tc, tw, th, tm, ctm):
        """Вывод строки. TJ с крупными сдвигами (так LibreOffice/Word «перепрыгивают» через слова,
        набранные другим шрифтом) режется на отдельные фрагменты со своими координатами.
        """
        trm = _mul(tm, ctm)
        sy = (trm[2] ** 2 + trm[3] ** 2) ** 0.5
        sx = (trm[0] ** 2 + trm[1] ** 2) ** 0.5
        size = abs(fsize) * (sy or sx or 1.0)
        adv, run_start, run = 0.0, 0.0, []

        def flush():
            txt = "".join(run)
            if txt.strip():
                a = _mul(_mul([1, 0, 0, 1, run_start, 0], tm), ctm)
                b = _mul(_mul([1, 0, 0, 1, adv, 0], tm), ctm)
                if all(math.isfinite(v) for v in (a[4], a[5], b[4], b[5], size)) and len(self.spans) < 500_000:
                    self.spans.append((a[4], a[5], b[4], b[5], size, txt))

        for it in items:
            if isinstance(it, (int, float)):
                num = float(it)
                if abs(num) > 120 and run:
                    flush()
                    run = []
                adv += -num / 1000.0 * fsize * th
                if not run:
                    run_start = adv
                continue
            if not isinstance(it, bytes):
                continue
            if not run:
                run_start = adv
            for u, w, is_space in font.decode(it):
                if u == " " and run:  # слово = отдельный фрагмент: между словами бывают глифы другого шрифта
                    flush()
                    run = []
                adv += (w * fsize + tc + (tw if is_space else 0.0)) * th
                if u == " ":
                    run_start = adv
                    continue
                if not run:
                    run_start = adv - (w * fsize + tc) * th
                run.append(u)
        flush()
        return _mul([1, 0, 0, 1, adv, 0], tm)

    def _do(self, res: dict, name, ctm, depth: int):
        xobjs = self.doc.resolve(res.get("XObject")) or {}
        xo = self.doc.resolve(xobjs.get(name)) if isinstance(xobjs, dict) else None
        if not isinstance(xo, Stream):
            return
        st = xo.dict.get("Subtype")
        if st == "Image":
            area = min(abs(ctm[0] * ctm[3] - ctm[1] * ctm[2]), self.page_area)
            self.image_area += area
            self.images.append((area / self.page_area, xo))
        elif st == "Form" and depth < 12 and self._forms_seen < 2000:
            self._forms_seen += 1
            m = self.doc.resolve(xo.dict.get("Matrix")) or [1, 0, 0, 1, 0, 0]
            fres = self.doc.resolve(xo.dict.get("Resources")) or res
            try:
                self._exec(self.doc.stream_bytes(xo), fres if isinstance(fres, dict) else res,
                           _mul([float(self.doc.resolve(x)) for x in m], ctm), depth + 1)
            except Exception:  # noqa: BLE001
                pass

    # ------------------------------------------------------------------ сборка текста
    def _merged_spans(self) -> list[list]:
        """Склеивает фрагменты, идущие друг за другом по направлению письма (текст, выведенный
        по букве, подписи под углом). Возвращает [x0, y0, x1, y1, size, text, dx, dy].
        """
        out: list[list] = []
        for x0, y0, x1, y1, size, s in self.spans:
            dx, dy = x1 - x0, y1 - y0
            ln = (dx * dx + dy * dy) ** 0.5
            if ln < 1e-6:
                dx, dy = 1.0, 0.0
            else:
                dx, dy = dx / ln, dy / ln
            diagonal = abs(dx) > 0.1 and abs(dy) > 0.1  # подписи под углом; горизонталь соберёт сортировка
            if out and diagonal:
                p = out[-1]
                if p[6] * dx + p[7] * dy > 0.99 and abs(p[4] - size) < 0.25 * max(size, 1):
                    rx, ry = x0 - p[2], y0 - p[3]
                    along = rx * dx + ry * dy
                    perp = abs(-rx * dy + ry * dx)
                    if perp < 0.3 * size and -0.5 * size < along < 1.0 * size:
                        if along > 0.18 * size and not p[5].endswith(" ") and not s.startswith(" "):
                            p[5] += " "
                        p[5] += s
                        p[2], p[3] = x1, y1
                        continue
            out.append([x0, y0, x1, y1, size, s, dx, dy])
        return out

    def text(self) -> str:
        if not self.spans:
            return ""
        spans = self._merged_spans()
        # преобладающее направление письма (повёрнутые страницы и слайды)
        votes = {0: 0, 90: 0, 180: 0, 270: 0}
        for sp in spans:
            dx, dy = sp[6], sp[7]
            ang = 0 if abs(dx) >= abs(dy) and dx >= 0 else 180 if abs(dx) >= abs(dy) else 90 if dy > 0 else 270
            votes[ang] += len(sp[5])
        dom = max(votes, key=votes.get)

        def rot(x, y):
            if dom == 90:
                return y, -x
            if dom == 180:
                return -x, -y
            if dom == 270:
                return -y, x
            return x, y

        items, seen = [], set()
        for x0, y0, x1, y1, size, s, _, _ in spans:
            a, b = rot(x0, y0)
            c, _ = rot(x1, y1)
            key = (round(a), round(b), s)
            if key in seen:  # «жирный» двойной печатью и дубли
                continue
            seen.add(key)
            items.append((a, b, max(c, a), size, s))
        items.sort(key=lambda t: (-t[1], t[0]))
        lines: list[list] = []
        for it in items:
            if lines:
                ly, lsize, _ = lines[-1]
                if abs(it[1] - ly) <= max(1.5, 0.45 * min(it[3], lsize)):
                    lines[-1][2].append(it)
                    continue
            lines.append([it[1], it[3], [it]])
        # строка → ячейки (разрыв больше 3 кеглей = граница колонки/ячейки)
        rows = []
        for y, size, sp in lines:
            sp.sort(key=lambda t: t[0])
            cells, buf, last_x1, cell_x = [], "", None, sp[0][0]
            for x0, _, x1, sz, s in sp:
                if last_x1 is not None:
                    gap = x0 - last_x1
                    if gap > 3.0 * sz:
                        cells.append((cell_x, last_x1, buf.strip()))
                        buf, cell_x = "", x0
                    elif gap > 0.15 * sz and not buf.endswith(" ") and not s.startswith(" "):
                        buf += " "
                buf += s
                last_x1 = x1 if last_x1 is None else max(x1, last_x1)
            cells.append((cell_x, last_x1, buf.strip()))
            rows.append((y, size, cells))
        rows = self._split_columns(rows)
        out, prev_y, prev_size = [], None, None
        for y, size, cells in rows:
            if y is None:
                out.append("")
                prev_y = None
                continue
            if prev_y is not None and prev_y - y > 1.9 * max(size, prev_size or size):
                out.append("")
            out.append(" | ".join(c[2] for c in cells if c[2]))
            prev_y, prev_size = y, size
        # управляющие символы — признак шрифта без кодировки (такой текст не читается; страницу посмотрит VLM)
        return re.sub(r"[\x00-\x08\x0b-\x1f\x7f-\x9f\ufffd\ud800-\udfff]", "", "\n".join(out))

    @staticmethod
    def _split_columns(rows: list) -> list:
        """Двухколоночная вёрстка: подряд ≥3 строк с одним разрывом на одном x и длинным текстом
        по обе стороны → сначала левая колонка, потом правая. Таблицы (много коротких ячеек) не трогаем.
        """
        def gutter(row):
            cells = row[2]
            if len(cells) == 2 and len(cells[0][2]) >= 20 and len(cells[1][2]) >= 20:
                return (cells[0][1] + cells[1][0]) / 2
            return None

        out, i = [], 0
        while i < len(rows):
            g = gutter(rows[i])
            j = i
            if g is not None:
                while j + 1 < len(rows):
                    g2 = gutter(rows[j + 1])
                    if g2 is None or abs(g2 - g) > 15:
                        break
                    j += 1
            if g is not None and j - i >= 2:
                block = rows[i:j + 1]
                out += [(y, sz, [c[0]]) for y, sz, c in block]
                out.append((None, 0, []))
                out += [(y, sz, [c[1]]) for y, sz, c in block]
                out.append((None, 0, []))
                i = j + 1
            else:
                out.append(rows[i])
                i += 1
        return out


# =============================================================================== картинки

def image_to_pil(doc: PDFDocument, stm: Stream):
    """Растровая картинка PDF → PIL.Image (RGB/L). None, если формат не поддержан или данные битые."""
    from PIL import Image, ImageFile
    old = ImageFile.LOAD_TRUNCATED_IMAGES
    ImageFile.LOAD_TRUNCATED_IMAGES = True  # слегка обрезанные сканы лучше прочитать, чем потерять
    try:
        return _image_to_pil(doc, stm)
    except Exception:  # noqa: BLE001
        return None
    finally:
        ImageFile.LOAD_TRUNCATED_IMAGES = old


def _image_to_pil(doc: PDFDocument, stm: Stream):
    from PIL import Image, ImageOps
    r = doc.resolve
    d = stm.dict
    data, filt, parms = doc.stream_bytes(stm, stop_at_image=True)
    w, h = int(r(d.get("Width", 0)) or 0), int(r(d.get("Height", 0)) or 0)
    bpc = int(r(d.get("BitsPerComponent", 8)) or 8)
    cs = r(d.get("ColorSpace"))
    if filt in ("DCTDecode", "DCT", "JPXDecode"):
        im = Image.open(io.BytesIO(data))
        im.load()
        if im.mode == "CMYK":
            dec = r(d.get("Decode"))
            if dec and float(r(dec[0])) == 1.0:
                im = Image.eval(im, lambda v: 255 - v)
            im = im.convert("RGB")
        return im
    if filt in ("CCITTFaxDecode", "CCF"):
        k = int(parms.get("K", 0) or 0)
        cols = int(parms.get("Columns", 1728) or 1728)
        rows = int(parms.get("Rows", h) or h)
        black1 = bool(parms.get("BlackIs1", False))
        comp = 4 if k < 0 else 3
        t4opt = 0 if k <= 0 else 1
        tags = [(256, 4, cols), (257, 4, rows), (258, 3, 1), (259, 3, comp), (262, 3, 1 if black1 else 0),
                (273, 4, 0), (277, 3, 1), (278, 4, rows), (279, 4, len(data))]
        if comp == 3:
            tags.append((292, 4, t4opt))
        tags.sort()
        ifd_off = 8
        n = len(tags)
        data_off = ifd_off + 2 + n * 12 + 4
        ifd = struct.pack("<H", n)
        for tag, typ, val in tags:
            if tag == 273:
                val = data_off
            if typ == 3:
                ifd += struct.pack("<HHIHH", tag, typ, 1, val, 0)
            else:
                ifd += struct.pack("<HHII", tag, typ, 1, val)
        tiff = b"II*\x00" + struct.pack("<I", ifd_off) + ifd + b"\x00\x00\x00\x00" + data
        im = Image.open(io.BytesIO(tiff))
        im.load()
        return im.convert("L")
    if filt == "JBIG2Decode" or w <= 0 or h <= 0 or w * h > Image.MAX_IMAGE_PIXELS:
        return None
    # несжатые пиксели (после Flate/LZW)
    cs_name, palette, ncomp = cs, None, 1
    if isinstance(cs, list) and cs:
        cs_name = r(cs[0])
        if cs_name == "ICCBased" and len(cs) > 1:
            icc = r(cs[1])
            ncomp = int(r(icc.get("N", 3))) if isinstance(icc, Stream) else 3
            cs_name = {1: "DeviceGray", 3: "DeviceRGB", 4: "DeviceCMYK"}.get(ncomp, "DeviceRGB")
        elif cs_name in ("Indexed", "I") and len(cs) >= 4:
            base = r(cs[1])
            if isinstance(base, list):
                base = r(base[0])
                if base == "ICCBased":
                    base = "DeviceRGB"
            lookup = r(cs[3])
            lut = doc.stream_bytes(lookup) if isinstance(lookup, Stream) else (lookup or b"")
            if base in ("DeviceGray", "CalGray", "G"):
                palette = b"".join(bytes([v, v, v]) for v in lut)
            elif base in ("DeviceCMYK", "CMYK"):
                pal = bytearray()
                for i in range(0, len(lut) - 3, 4):
                    c, m, y, kk = lut[i:i + 4]
                    pal += bytes([255 - min(255, c + kk), 255 - min(255, m + kk), 255 - min(255, y + kk)])
                palette = bytes(pal)
            else:
                palette = bytes(lut)
            cs_name = "Indexed"
        elif cs_name in ("CalRGB",):
            cs_name = "DeviceRGB"
        elif cs_name in ("CalGray",):
            cs_name = "DeviceGray"
        elif cs_name in ("Separation", "DeviceN"):
            cs_name = "DeviceGray"
    if r(d.get("ImageMask")) is True:
        cs_name, bpc = "DeviceGray", 1
    ncomp = {"DeviceRGB": 3, "RGB": 3, "DeviceCMYK": 4, "CMYK": 4}.get(cs_name, 1)
    if len(data) < ((w * ncomp * bpc + 7) // 8) * h:  # данных меньше, чем заявлено размерами — не выделяем память
        return None
    try:
        if cs_name == "Indexed":
            raw_mode = {8: "P", 4: "P;4", 2: "P;2", 1: "P;1"}.get(bpc, "P")
            im = Image.frombytes("P", (w, h), data, "raw", raw_mode)
            im.putpalette(palette[:768] + bytes(max(0, 768 - len(palette))))
            return im.convert("RGB")
        if cs_name in ("DeviceRGB", "RGB"):
            return Image.frombytes("RGB", (w, h), data[: w * h * 3]) if bpc == 8 else None
        if cs_name in ("DeviceCMYK", "CMYK"):
            return Image.frombytes("CMYK", (w, h), data[: w * h * 4]).convert("RGB") if bpc == 8 else None
        if bpc == 1:
            im = Image.frombytes("1", (w, h), data)
            if r(d.get("ImageMask")) is True:
                im = ImageOps.invert(im.convert("L"))
            return im.convert("L")
        if bpc == 8:
            return Image.frombytes("L", (w, h), data[: w * h])
    except (ValueError, OSError):
        return None
    return None


# =============================================================================== рендереры (опционально)

def renderer() -> str | None:
    """Чем можно растеризовать страницу PDF: pymupdf → pdftoppm → ghostscript → ничем."""
    import os
    if os.environ.get("DOCBRIEF_NO_RASTER"):  # принудительно без растеризатора (тесты)
        return None
    try:
        import pymupdf  # noqa: F401
        return "pymupdf"
    except ImportError:
        try:
            import fitz  # noqa: F401
            return "fitz"
        except ImportError:
            pass
    if shutil.which("pdftoppm"):
        return "pdftoppm"
    for gs in ("gswin64c", "gswin32c", "gs"):
        if shutil.which(gs):
            return gs
    return None


def render_page(path: str | Path, page_no: int, dpi: int = 150):
    """Страница (с 1) → PIL.Image или None, если растеризатора нет."""
    from PIL import Image
    how = renderer()
    path = str(path)
    if how in ("pymupdf", "fitz"):
        mod = __import__(how)
        doc = mod.open(path)
        pix = doc[page_no - 1].get_pixmap(dpi=dpi)
        return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    if how is None:
        return None
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as td:
        out = Path(td) / "p.jpg"
        if how == "pdftoppm":
            cmd = ["pdftoppm", "-f", str(page_no), "-l", str(page_no), "-r", str(dpi), "-jpeg", "-singlefile",
                   path, str(out.with_suffix(""))]
        else:
            cmd = [how, "-q", "-dNOPAUSE", "-dBATCH", "-dSAFER", "-sDEVICE=jpeg", f"-r{dpi}",
                   f"-dFirstPage={page_no}", f"-dLastPage={page_no}", f"-sOutputFile={out}", path]
        try:
            subprocess.run(cmd, check=True, capture_output=True, timeout=120)
            im = Image.open(out)
            im.load()
            return im.convert("RGB")
        except Exception:  # noqa: BLE001
            return None


# =============================================================================== API

def read_pdf(path: str | Path) -> tuple[PDFDocument, list[PageReader]]:
    doc = PDFDocument(Path(path).read_bytes())
    readers = []
    for page in doc.pages:
        try:
            pr = PageReader(doc, page)
        except Exception as e:  # noqa: BLE001
            doc.warnings.append(f"страница {len(readers) + 1}: {type(e).__name__}")
            pr = PageReader(doc, {})
        try:
            pr.run()
        except Exception as e:  # noqa: BLE001
            doc.warnings.append(f"страница {len(readers) + 1}: {type(e).__name__}")
        readers.append(pr)
    return doc, readers
