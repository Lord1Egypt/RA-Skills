---
name: magyar-nyelvtan
description: Magyar helyesírási és nyelvtani ellenőrzés, ragozási szabályok, nyelvtani tanácsadás. Use when: (1) magyar szöveg helyesírását kell ellenőrizni, (2) igei ragozás vagy névszóragozás kell, (3) nyelvtani szabály magyarázat, (4) magyar mondat szerkezet elemzése.
---

# Magyar Nyelvtan

## Áttekintés

Magyar helyesírási ellenőrzés, nyelvtani szabályok alkalmazása, ragozási minták, és nyelvtani tanácsadás.

## Mikor használd

- **Helyesírás ellenőrzés**: magyar szöveg elírásainak javítása
- **Ragozás**: igei és névszói ragozási formák
- **Nyelvtani magyarázat**: szabályok, kivételek magyarázata
- **Mondeelemek azonosítása**: alany, állítmány, tárgy
- **Szófaj meghatározás**: főnév, ige, melléknév stb.

## Helyesírási szabályok

### 1. Egybeírás vs különírás

```
- egybe: hozzáad, beleír, rámutat (igei előtag + ige)
- külön: oda megy, le ír (határozószó + ige)
```

### 2. Toldalékok

- **Birtokos jelek**: -m, -d, -ja/-je, -nk, -tok/-tek/-tök
- **Többes szám**: -k, -ak/-ek/-ok
- **Esetjelek**: -t (tárgyas), -nak/-nek (részes), -ban/-ben (inesszív)

### 3. Igeragozás

```
határozott: olvasom, olvasod, olvoosja
határozatlan: olvasok, olvasz, olvas
```

## Ellenőrzési workflow

```python
def check_hungarian_spelling(text):
    # 1. Tokenizálás
    tokens = tokenize(text)
    # 2. Szótár ellenőrzés
    errors = []
    for token in tokens:
        if not in_dict(token):
            errors.append(suggest_correction(token))
    # 3. Nyelvtani egyezőség
    check_agreement(errors)
    return errors
```

## Referenciák

- **references/akh12.md** – MTA A magyar helyesírás szabályai (12. kiadás)
- **references/fogalmazas.md** – pontos magyar fogalmazás, idegen szavak kerülése
- **references/ragozas.md** – teljes ragozási táblázatok
- **references/szofajok.md** – szófajok és jellemzőik
- **references/peldak.md** – helyes/hibás példamondeaok

## Hivatalos forrás

**MTA Helyesírás**: https://helyesiras.mta.hu/helyesiras/default/akh12

## Fogalmazás javítás

Lásd **references/f1ogalmazas.md**:
- Idegen szavak kerülése (implementál → megvalósít)
- Tükörfordítások javítása
- Mondatszerkezet optimalizálás
- Stílus ajánlások

## Scriptek

- **scripts/spellcheck.py** – helyesírás ellenőrző
- **scripts/conjugate.py** – igeragozás generátor
- **scripts/grammar_check.py** – nyelvtani egyezőség ellenőrzés

## Jegyzetek

- Magyar agglutináló nyelv: sok toldalék
- Hangrendi illeszkedés: mély/magas hangrend
- Deflexion: határozott/határozatlan ragozás
