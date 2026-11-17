#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract plain text from a legacy binary .doc (Word 97-2003 / OLE2).

`python-docx` only reads .docx, so this helper covers the .doc drafts the skill
claims to support. It parses the FIB and piece table directly (needs `olefile`).

Usage:
    python scripts/read_doc_text.py input.doc            # print text to stdout
    python scripts/read_doc_text.py input.doc out.txt    # write text to a file
"""

from __future__ import annotations

import struct
import sys

import olefile


def extract(path: str) -> str:
    ole = olefile.OleFileIO(path)
    try:
        doc = ole.openstream("WordDocument").read()

        # FibBase flags at 0x0A: bit 0x0200 selects 1Table vs 0Table.
        flags = struct.unpack_from("<H", doc, 0x0A)[0]
        table_name = "1Table" if (flags & 0x0200) else "0Table"
        if not ole.exists(table_name):
            table_name = "0Table" if table_name == "1Table" else "1Table"
        table = ole.openstream(table_name).read()

        # fcClx / lcbClx live at fixed offsets in the classic FIB.
        fc_clx = struct.unpack_from("<I", doc, 0x01A2)[0]
        lcb_clx = struct.unpack_from("<I", doc, 0x01A6)[0]
        clx = table[fc_clx:fc_clx + lcb_clx]

        # Walk the Clx: skip Prc entries (0x01) and find the Pcdt (0x02).
        i = 0
        pcdt = None
        while i < len(clx):
            kind = clx[i]
            if kind == 0x01:
                cb = struct.unpack_from("<H", clx, i + 1)[0]
                i += 3 + cb
            elif kind == 0x02:
                lcb = struct.unpack_from("<I", clx, i + 1)[0]
                pcdt = clx[i + 5:i + 5 + lcb]
                break
            else:
                break

        if pcdt is None:
            raise RuntimeError("piece table (Pcdt) not found")

        n = (len(pcdt) - 4) // 12
        cps = [struct.unpack_from("<I", pcdt, k * 4)[0] for k in range(n + 1)]
        pcd_off = (n + 1) * 4

        parts = []
        for k in range(n):
            length = cps[k + 1] - cps[k]
            fc = struct.unpack_from("<I", pcdt, pcd_off + k * 8 + 2)[0]
            compressed = bool(fc & 0x40000000)
            base = fc & 0x3FFFFFFF
            if compressed:  # 8-bit CP1252 text
                raw = doc[base // 2:base // 2 + length]
                parts.append(raw.decode("cp1252", errors="replace"))
            else:  # UTF-16LE text
                raw = doc[base:base + length * 2]
                parts.append(raw.decode("utf-16-le", errors="replace"))
    finally:
        ole.close()

    text = "".join(parts)
    text = text.replace("\r", "\n").replace("\x07", "\t").replace("\x0b", "\n")
    text = text.replace("\x0c", "\n").replace("\x02", "")
    return text


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("usage: python scripts/read_doc_text.py input.doc [output.txt]")
    text = extract(sys.argv[1])
    if len(sys.argv) >= 3:
        with open(sys.argv[2], "w", encoding="utf-8") as handle:
            handle.write(text)
        print(f"extracted {len(text)} chars -> {sys.argv[2]}")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
