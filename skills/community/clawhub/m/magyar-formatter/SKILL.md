---
name: magyar-formatter
description: Magyar dátum, szám, pénz formázás: helyi formátumok alkalmazása (YYYY. MM. DD., tizedesvessző, Ft). Use when: (1) magyar dátum formátum kell, (2) számok magyar formázása (tizedesvessző), (3) pénz összegek Ft-ban, (4) magyar telefonszám, cím formátum.
---

# Magyar Formázás

## Áttekintés

Magyar helyi formátumok alkalmazása: dátum, számok, pénzek, telefonszámok, és címek.

## Mikor használd

- **Dátum formázás**: magyar dátum (YYYY. MM. DD.)
- **Szám formázás**: tizedesvessző, ezres elválasztó
- **Pénz formázás**: Ft szimbólum, helyi valuta
- **Telefonszám**: +36 XX XXX XXXX formátum
- **Cím formátum**: magyar cím szerkezet

## Formátum szabályok

### 1. Dátum

```
Magyar: 2026. március 18.
Rövid: 2026. 03. 18.
ISO: 2026-03-18 (konvertáld magyarra)
```

### 2. Számok

```
Angol: 1,234.56
Magyar: 1 234,56 (ezres szóköz, tizedesvessző)
```

### 3. Pénz

```
Angol: $1,234.56
Magyar: 1 234,56 Ft
Nagy összeg: 1,2 millió Ft
```

### 4. Telefonszám

```
Nemzetközi: +36 30 123 4567
Helyi: (30) 123-4567
```

### 5. Cím

```
1234 Budapest, Petőfi utca 12. fsz. 3.
irányítószám város, utca házszám emelet ajtó
```

## Scriptek

- **scripts/format_date.py** – dátum magyar formázás
- **scripts/format_number.py** – számok formázása
- **scripts/format_currency.py** – pénz Ft-ban
- **scripts/format_phone.py** – telefonszám formázás

## Példakód

```python
def format_hungarian_date(date):
    return f"{date.year}. {date.month:02d}. {date.day:02d}."

def format_hungarian_number(num):
    return f"{int(num):,}".replace(',', ' ') + f",{abs(num - int(num)):.2f}"[2:]

def format_forint(amount):
    return f"{format_hungarian_number(amount)} Ft"
```

## Referenciák

- **references/date-formats.md** – dátum formátumok részletesen
- **references/currency.md** – Ft konverziók, váltások
- **references/address-format.md** – magyar cím szerkezet

## Jegyzetek

- Tizedesvessző kritikus (nem pont!)
- Ezres elválasztó: szóköz vagy keskeny szóköz
- Ft mindig szám után, szóközzel
- Dátum pontok kötelezőek
