# Arcanum – Magyar Értelmező Szótár (ÉrtSz.)

## Forrás

**URL**: https://www.arcanum.com/hu/online-kiadvanyok/Lexikonok-a-magyar-nyelv-ertelmezo-szotara-1BE8B/

## Metaadatok

- **Kiadás**: 1959-1962 (első kiadás)
- **Kötetek**: 7 kötet
- **Szócikkek száma**: ~60.000
- **Szerkesztők**: Bárczi Géza, Országh László
- **Kiadó**: Akadémiai Kiadó
- **Intézmény**: MTA Nyelvtudományi Intézete

## Kötet szerkezet

| Kötet | Betűk |
|-------|-------|
| I | A-D |
| II | E-Gy |
| III | H-Kh |
| IV | Ki-Mi |
| V | Mo-S |
| VI | Sz-Ty |
| VII | U-Zs |

## Használat

### 1. Kötet navigáció

Minden betűhez meg kell nyitni a megfelelő kötetet:

```
A-D szó → I. kötet
E-Gy szó → II. kötet
H-Kh szó → III. kötet
Ki-Mi szó → IV. kötet
Mo-S szó → V. kötet
Sz-Ty szó → VI. kötet
U-Zs szó → VII. kötet
```

### 2. Szócikk szerkezet

Minden szócikk tartalmazza:

- **Címszó** (a szó alapformája)
- **Jelentés** (körülírás, magyarázat)
- **Szókapcsolatok** (gyakori kombinációk)
- **Szólások** (szóláshasonlatok, közmondások)
- **Összetételek** (szócikk végén, értelmezés nélkül)
- **Származékok** (szócikk végén, értelmezés nélkül)

### 3. Példa szócikk

```
macerás
  jelentés: nehézséget okozó, problémás, sok bajjal járó
  szókapcsolatok: macerás ügy, macerás helyzet
  összetételek: macerásság
```

## Jegyzetek

- **Nem enciklopédia**: csak szó jelentéseket értelmez, nem ismereteket közöl
- **Nyelvhelyesség**: értékeli és minősíti a nyelvi tényeket
- **Irodalmi nyelv**: főként a mai köznyelv és 19-20. századi irodalmi nyelv
- **Régi nyelv**: csak kivételesen (klasszikus irodalmi alkotásokra tekintettel)

## API integráció (opcionális)

Ha Arcanum API elérhető:

```python
def lookup_ertsz(word):
    # 1. Kötet meghatározás
    volume = get_volume_for_letter(word[0])
    # 2. Szócikk keresés
    article = search_in_volume(volume, word)
    # 3. Jelentés visszaadás
    return article['meaning']
```

## Alternatív források

- **Wiktionary** (magyar): https://hu.wiktionary.org/
- **Sztaki szótár**: https://dict.sztaki.hu/
