# Magyar Szövegértés – Best Practices

## Áttekintés

Ez a referencia segít a magyar szövegek pontos megértésében és feldolgozásában.

## Szövegértés szintek

### 1. Felületi megértés

- **Szavak jelentése**: szótár használat
- **Mondeelemek**: alany, állítmány, tárgy azonosítása
- **Szófajok**: főnév, ige, melléknév stb.

### 2. Mélyebb megértés

- **Összefüggések**: ok-okozat, cél-eszköz
- **Rejtett jelentés**: átvitt értelmű kifejezések
- **Hangnem**: formális / informális, ironikus / komoly

### 3. Kontextus megértés

- **Környezet**: miről szól a téma
- **Cél**: mi a szöveg célja (tájékoztatás, meggyőzés, kérés)
- **Célközönség**: kinek szól

## Gyakori magyar kifejezések értelmezése

### 1. Szólások

| Kifejezés | Jelentés |
|-----------|----------|
| "eső után köpönyeg" | későn cselekszik |
| "kutya ugat, karaván halad" | nem zavarja a kritika |
| "sűrűje" | központi rész, lényeg |
| "kivágja a rezet" | sikeresen teljesít |
| "töri a fejét" | gondolkodik, keresi a megoldást |
| "kivágja magát" | ügyesen kijut a helyzetből |
| "földbe áll a szeme" | nagyon fáradt |
| "két tűz között van" | nehéz helyzetben van |
| "ujja köré csavar" | manipulál |
| "szót fordít" | félreért, rosszul értelmez |

### 2. Metaforikus kifejezések

| Kifejezés | Jelentés |
|-----------|----------|
| "híd" | kapcsolat, összeköttetés |
| "hídfőállás" | kiindulópont, bázis |
| "sarok" | fontos pont, kulcshely |
| "gerinc" | alapvető rész, váz |
| "mag" | központi rész, lényeg |
| "héj" | külső réteg, felület |
| "gyökér" | eredet, forrás |
| "virág" | eredmény, kibontakozás |
| "fény" | tudás, megértés |
| "árnyék" | bizonytalanság, homály |

### 3. Irodalmi hivatkozások

| Kifejezés | Forrás | Jelentés |
|-----------|--------|----------|
| "bölcselő" | Petőfi | gondolkodó, filozófus |
| "vörös telkek" | Ady | Magyarország |
| "újhold" | Babits | megújulás |
| "csillogó éj" | Vörösmarty | szép este |

## Szövegelemzés technikák

### 1. Kulcsszó kinyerés

```python
def extract_keywords(text):
    # 1. Tokenizálás
    tokens = tokenize(text)
    # 2. Stopwords szűrés
    filtered = remove_stopwords(tokens)
    # 3. Gyakoriság
    freq = count_frequency(filtered)
    # 4. TF-IDF súly
    weighted = apply_tfidf(freq)
    # 5. Top N visszaadás
    return get_top_words(weighted, n=5)
```

### 2. Téma azonosítás

```python
def identify_topic(text):
    # 1. Kulcsszavak
    keywords = extract_keywords(text)
    # 2. Szemantikus csoportosítás
    groups = cluster_keywords(keywords)
    # 3. Domin téma
    return get_dominant_topic(groups)
```

### 3. Érzelem elemzés

```python
def analyze_sentiment(text):
    # 1. Pozitív szavak
    pos_words = count_positive_words(text)
    # 2. Negatív szavak
    neg_words = count_negative_words(text)
    # 3. Semleges
    neutral = len(text.split()) - pos_words - neg_words
    # 4. Arány
    score = (pos_words - neg_words) / len(text.split())
    return classify(score)  # pozitív/negatív/semleges
```

### 4. Entitás kinyerés (NER)

```python
def extract_entities(text):
    entities = {
        'személy': [],
        'hely': [],
        'szervezet': [],
        'dátum': [],
        'pénz': []
    }
    # 1. Név minták
    entities['személy'] = extract_names(text)
    # 2. Hely minták
    entities['hely'] = extract_locations(text)
    # 3. Szervezet minták
    entities['szervezet'] = extract_organizations(text)
    # 4. Dátum minták
    entities['dátum'] = extract_dates(text)
    # 5. Pénz minták
    entities['pénz'] = extract_money(text)
    return entities
```

## Kontextus megőrzés

### 1. Párbeszéd kontextus

```
Felhasználó: "Milyen az idő?"
Asszisztens: "Budapesten jelenleg 18°C van, napos az idő."

Felhasználó: "És holnap?"
→ Kontextus: időjárás, Budapest, holnapi nap
→ Válasz: "Holnap Budapesten 20°C várható, eső lehetséges."
```

### 2. Több fordulós kontextus

```
1. "Írj egy Python scriptet ami fájlt olvas."
2. "Adj hozzá hibakezelést."
3. "Most pedig írd ki az eredményt konzolra."

→ Mindhárom ugyanarra a scriptre vonatkozik
→ Kontextus: Python, fájlolvasás, hibakezelés, konzol kiírás
```

### 3. Referencia feloldás

```
"A felhasználó elküldte a fájlt. **Ez** hibás volt."
→ "Ez" = a fájl

"A meetinget elhalasztották. **Az** jövő héten lesz."
→ "Az" = a meeting
```

## Gyakori félreértések

### 1. Többjelentésű szavak

| Szó | Jelentés 1 | Jelentés 2 |
|-----|------------|------------|
| "kulcs" | zár kulcs | megoldás kulcs |
| "híd" | építmény | kapcsolat |
| "mag" | növény mag | központi rész |
| "fej" | testrész | vezető |
| "láb" | testrész | bútor lába |
| "szem" | testrész | rügy (növény) |
| "fog" | testrész | fésű foga |
| "kar" | testrész | időkar (karácsony) |
| "has" | testrész | haszon |
| "nyelv" | testrész | beszéd nyelv |

### 2. Hasonló szavak

| Szópár | Különbség |
|--------|-----------|
| "mellék" vs "melléklet" | mellék = oldal, melléklet = csatolmány |
| "terv" vs "tervezet" | terv = koncepció, tervezet = előzetes változat |
| "adat" vs "információ" | adat = nyers, információ = feldolgozott |
| "hiba" vs "hibaüzenet" | hiba = probléma, hibaüzenet = jelzés |
| "kimenet" vs "kimeneti" | kimenet = output, kimeneti = attribútum |

### 3. Tagadás értelmezése

```
"Nem rossz" = jó (két tagadás = állítás)
"Nem feltétlenül" = lehetséges de nem biztos
"Nem soha" = néha (két tagadás)
"Kétségtelenül nem" = biztosan nem
```

## Gyakorlati minták

### 1. Rövid szöveg összefoglalás

```
Eredeti (100 szó):
"A projekt múlt héten indult és a csapat 5 főből áll. 
A cél egy új weboldal fejlesztése ami a cég termékeit mutatja be. 
Az első fázis a tervezés ami 2 hétig tart. 
Ezután jön a fejlesztés 4 hétig. 
Végül a tesztelés 1 hétig. 
A projekt összesen 7 hétig tart és 3 sprintből áll."

Összefoglalás (20 szó):
"7 hetes webfejlesztési projekt: 2 hét tervezés, 4 hét fejlesztés, 1 hét tesztelés. 5 fős csapat, 3 sprint."
```

### 2. Kérdés értelmezés

```
Kérdés: "Mikor készül el a projekt?"
→ Típus: dátum kérés
→ Kontextus: projekt határidő
→ Válasz: "A projekt 7 hét alatt készül el."
```

### 3. Kérés azonosítás

```
"Ki tudnád ezt javítani?"
→ Kérés típus: cselekvés kérés
→ Akció: javítás
→ Objektum: "ez" (kontextusból kell kideríteni)
```

## Jegyzetek

- **Kontextus kritikus**: mindig olvasd vissza az előzményeket
- **Többjelentés**: figyeld a környező szavakat
- **Rejtett jelentés**: keresd az átvitt értelmet
- **Gyakorold**: napi olvasás javítja a megértést
