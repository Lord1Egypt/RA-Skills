---
name: magyar-szotar
description: Magyar értelmező kéziszótár integráció szójelentések, szinonimák, és nyelvi elemzéshez. Use when: (1) felhasználó magyar szó jelentését kérdezi, (2) szinonimákat keres, (3) magyar szöveg nyelvi elemzése szükséges, (4) szókapcsolatok, szólások magyarázata kell.
---

# Magyar Szótár Skill

## Áttekintés

Ez a skill lehetővé teszi magyar szavak jelentésének, szinonimáinak, és nyelvi kapcsolatainak gyors lekérdezését. Használj helyi szótár adatbázist vagy web API-t a válaszokhoz.

## Mikor használd

- **Szójelentés kérdezése**: "Mit jelent az hogy 'macerás'?"
- **Szinonima keresés**: "Mi a szinonimája a 'gyors'-nak?"
- **Szólások/mondások**: "Mit jelent az 'eső után köpönyeg'?"
- **Nyelvi elemzés**: magyar szöveg morfológiai elemzése
- **Szócsoportosítás**: tematikus szókapcsolatok keresése

## Szótár források

### 1. Arcanum – Magyar Értelmező Szótár (ÉrtSz.)

**Elsődleges forrás**: https://www.arcanum.com/hu/online-kiadvanyok/Lexikonok-a-magyar-nyelv-ertelmezo-szotara-1BE8B/

- **6 kötetes** (1959-1962), ~60.000 szócikk
- **Szerkesztők**: Bárczi Géza, Országh László (MTA Nyelvtudományi Intézete)
- **Kötetek**: I: A-D, II: E-Gy, III: H-Kh, IV: Ki-Mi, V: Mo-S, VI: Sz-Ty, VII: U-Zs
- **Jellemző**: irodalmi és köznyelv törzsállománya, nem enciklopédia

### 2. Helyi szótár fájl (gyors lookup)

Tarts egy `references/magyar-szotar.json` fájlt strukturált szótár adatokkal:

```json
{
  "szavak": {
    "macerás": {
      "jelentés": "nehézséget okozó, problémás",
      "szinonimák": ["problémás", "nehéz", "bonyolult"],
      "példa": "Ez egy macerás feladat."
    }
  }
}
```

### 2. Web API fallback

Ha helyi szótár nem elérhető, használj nyilvános API-t:
- dict.sztaki.hu (magyar-angol, de van értelmező is)
- Wiktionary API

## Gyors kezdés

```python
# Példa szójelentés lekérdezésre
def lookup_word(word):
    # 1. Helyi szótár keresés
    if word in local_dict:
        return local_dict[word]
    # 2. API fallback
    return fetch_from_api(word)
```

## Referenciák

- **references/kozmondasok.md** – 100+ magyar közmondás és szólás jelentéssel, példákkal
- **references/magyar-szotar.json** – fő szótár adatbázis
- **references/arcanum-ertsz.md** – Arcanum ÉrtSz. forrásdokumentáció
- **references/morfológia.md** – magyar nyelvtani szabályok, ragozások

## Jegyzetek

- Mindig ellenőrizd a szótár forrás frissességét
- Nagy szövegeknél batch lookup-ot használj (token hatékony)
- Ha szó nem található, jelezd és ajánlj alternatívát
