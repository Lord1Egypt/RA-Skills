---
name: magyar-szovegfeldolgoz-s
description: Magyar szövegfeldolgozás: elemzés, kivonatolás, összefoglalás, kulcsszó kinyerés. Use when: (1) magyar szöveget kell elemezni vagy összefoglalni, (2) kulcsszavakat kell kinyerni magyar tartalomtól, (3) szöveg tömörítése kell, (4) magyar nyelvű NLP feladatok.
---

# Magyar Szövegfeldolgozás

## Áttekintés

Magyar nyelvű szövegek automatikus feldolgozása: elemzés, kivonatolás, összefoglalás, és kulcsszó kinyerés.

## Mikor használd

- **Szöveg összefoglalás**: hosszú magyar cikk tömörítése
- **Kulcsszó kinyerés**: fontos szavak kigyűjtése magyar szövegből
- **Téma azonosítás**: miről szól a magyar tartalom
- **Érzelem elemzés**: pozitív/negatív hangulat magyar szövegben
- **Entitás kinyerés**: nevek, helyek, dátumok magyar szövegben

## Működés

### 1. Szöveg összefoglalás

```python
def summarize_hungarian(text, max_sentences=3):
    # 1. Mondatokra bontás (magyar mondatvégi jelek: . ! ?)
    sentences = split_sentences(text)
    # 2. Fontossági súlyozás (kulcsszavak, pozíció)
    scored = score_sentences(sentences)
    # 3. Top N mondatok visszaadása
    return get_top_sentences(scored, max_sentences)
```

### 2. Kulcsszó kinyerés

```python
def extract_keywords(text, top_n=5):
    # 1. Tokenizálás (magyar szóelemzés)
    tokens = tokenize(text)
    # 2. Stopwords szűrés (magyar stopword lista)
    filtered = remove_stopwords(tokens)
    # 3. Gyakoriság alapú rangsor
    return get_top_words(filtered, top_n)
```

### 3. Entitás kinyerés (NER)

- **Személyek**: keresztnevek, vezetéknevek
- **Helyek**: városok, országok, címek
- **Dátumok**: magyar dátum formátumok (YYYY-MM-DD, "március 18")
- **Számok**: pénzek, mennyiségek

## Referenciák

- **references/szovegertes.md** – magyar szövegértés best practices, kontextus megőrzés
- **references/stopwords.txt** – magyar stopwords lista
- **references/magyar-regex.md** – magyar szöveg regex minták
- **references/ner-patterns.md** – entitás kinyerés minták

## Scriptek

- **scripts/summarize.py** – magyar szöveg összefoglalás
- **scripts/keywords.py** – kulcsszó kinyerés
- **scripts/ner.py** – entitás kinyerés

## Szövegértés javítás

Lásd **references/szovegertes.md**:
- Szólások, metaforák értelmezése
- Többjelentésű szavak feloldása
- Kontextus megőrzés több fordulós párbeszédben
- Érzelem elemzés, téma azonosítás

## Jegyzetek

- Magyar agglutináló nyelv: szóvégi toldalékok kezelése fontos
- Stopword lista kritikus a kulcsszó kinyeréshez
- Helyi NLP modellek (pl. HunFlair) ha elérhetők
