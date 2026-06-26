---
name: magyar-api-docs
description: Magyar nyelvű API dokumentációk, fejlesztői útmutatók, és technikai referenciák kezelése. Use when: (1) magyar API dokumentumot kell olvasni vagy keresni, (2) fejlesztői útmutató magyar nyelven kell, (3) magyar technikai szakkifejezések magyarázata, (4) API endpointok magyar leírása.
---

# Magyar API Dokumentáció

## Áttekintés

Magyar nyelvű API dokumentációk, fejlesztői útmutatók, és technikai referenciák tárolása és keresése.

## Mikor használd

- **API keresés**: magyar leírású endpointok keresése
- **Dokumentáció olvasás**: fejlesztői útmutatók magyarul
- **Szakkifejezések**: technikai magyar szakkifejezések magyarázata
- **Példakód**: magyar kommentárral ellátott kódminták
- **Hibakeresés**: magyar hibaüzenetek, stack trace elemzése

## Dokumentáció szerkezet

```
references/
├── api-auth.md        – hitelesítés magyarul
├── api-endpoints.md   – endpoint leírások
├── hibauzenetek.md    – gyakori hibák magyarul
└── peldakod.md       – magyar kommentárral
```

## Magyar szakkifejezések

| Angol | Magyar |
|-------|--------|
| endpoint | végpont |
| authentication | hitelesítés |
| response | válasz |
| request | kérés |
| payload | adatterhelés |
| token | azonosító |
| callback | visszahívás |
| webhook | webhívás |

## Kód példák (magyar kommentárral)

```python
# Hitelesítés kérés
response = api.login(felhasznalonev, jelszo)

# Adatok lekérése
adatok = api.get_endpoint("users")

# Hiba kezelés
if response.hiba:
    print(f"Hiba történt: {response.hiba_uzenet}")
```

## Referenciák

- **references/api-glossary.md** – angol-magyar technikai szótár
- **references/hungarian-docs/** – magyar API dokumentumok
- **references/error-messages.md** – magyar hibaüzenet katalogus

## Jegyzetek

- Mindig őrizd meg az eredeti angol terminológiát zárójelben
- Magyar kommentárok segítik a helyi fejlesztőket
- API változásoknál frissítsd a magyar leírást is
