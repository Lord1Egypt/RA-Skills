---
name: "marktplaats-publisher"
description: "Marktplaats publisher met scriptmatige copy-QA, preflight, live verify en register-update."
homepage: https://www.marktplaats.nl
metadata: {"clawdbot":{"emoji":"🇳🇱","requires":{"bins":["node"]}}}
---

# Marktplaats Publisher

Gebruik deze skill voor normale Marktplaats-advertenties: voorbereiden, plaatsen, bewerken, live controleren en lokaal registreren.

De workflow is command-first. Proceduretekst is alleen toelichting. Als een gate faalt, stop je.

## Harde Regels

- Geen publicatie of inhoudelijke bewerking zonder expliciete opdracht voor die advertentie.
- Geen betaalde opties, bundels, promoties of betaalflow zonder expliciet akkoord.
- Geen cookies, sessietokens, XSRF/auth-waarden, klantdata of lokale privepaden loggen of publiceren.
- Geen captcha, MFA, login challenge, WAF of accountbeveiliging omzeilen.
- Geen tekst plaatsen als copy-QA of preflight faalt.
- Na opslaan altijd live verifieren en het lokale register bijwerken.
- Bij UI-drift, browser-hang of onduidelijke formulierstatus: stop, maak een snapshot en rapporteer de blokkade.

## Lokale Bestanden

Werk per advertentie in:

```text
~/Documents/OpenClaw/Data/marktplaats/<slug>/ad.json
~/Documents/OpenClaw/Data/marktplaats/<slug>/description.md
~/Documents/OpenClaw/Data/marktplaats/<slug>/photos/
```

Centraal register:

```text
~/Documents/OpenClaw/Data/marktplaats/advertenties.json
```

`ad.json` moet minimaal bevatten: titel, prijs, conditie, levering, categorie/categoryIds, `biddingAllowed`, `descriptionFile`, `imageDir` of foto's, URL/adId zodra live, en `copyQuality`.

## Verplichte Pipeline

### 1. Schrijf De Omschrijving

Schrijf een feitelijke Nederlandse tekst van ongeveer 3200-3500 tekens.

Moet bevatten:

- merk/model of herkenbare productnaam;
- productsoort;
- staat/conditie en wat wel/niet getest is;
- concrete zichtbare kenmerken;
- toepassing en compatibiliteit;
- ophalen/verzenden, prijs en bieden;
- natuurlijke zoekvarianten in gewone zinnen.

Niet doen:

- geen `Zoektermen:`, `Keywords:` of `SEO:` footer;
- geen lange comma-keyworddump;
- geen claims over werking, garantie of compleetheid zonder bewijs.

### 2. Copy-QA

Altijd draaien voordat Marktplaats wordt ingevuld of opgeslagen:

```bash
marktplaats-copy-qa ./description.md \
  --require "<merk-of-model>" \
  --require "<productsoort>" \
  --variant "<natuurlijke zoekvariant>" \
  --ad-json ./ad.json
```

Stop als dit geen `PASS` geeft. De command schrijft `copyQuality` inclusief `descriptionSha256` naar `ad.json`.

### 3. Preflight

Altijd draaien na copy-QA en voor browser/UI-werk:

```bash
marktplaats-ad-preflight --ad-json ./ad.json --require-bidding-allowed
```

Gebruik `--require-bidding-allowed` wanneer bieden aan moet staan. Stop bij failure.

Preflight controleert onder andere:

- verplichte advertentievelden;
- omschrijving bestaat en is niet gewijzigd na copy-QA;
- copy-QA is geslaagd;
- foto's bestaan;
- biedeninstelling indien vereist.

### 4. Formulier Probe

Inspecteer Marktplaats voordat je invult:

```bash
marktplaats-place-probe --browser --save ./snapshot-place.json
```

Of met browser-fetch:

```bash
marktplaats-place-probe --browser-fetch --url "https://www.marktplaats.nl/plaats/..." --save ./snapshot-place.json
```

Stop als:

- login/captcha/MFA/WAF verschijnt;
- betaalde route verplicht lijkt;
- formulierstructuur onduidelijk is;
- foto-upload of bundelkeuze niet te verifieren is.

### 5. Plaats Of Bewerk

Vul Marktplaats pas na groene copy-QA en preflight.

Controleer voor submit/save:

- titel;
- prijs;
- bieden toegestaan indien gevraagd;
- conditie;
- levering;
- foto-aantal;
- gratis/basic route;
- laatste zin van de omschrijving zichtbaar in het formulier.

Gebruik geen blinde coordinate-clicks. Gebruik DOM/events of een expliciet UI-element met verificatie voor en na.

### 6. Live Verify

Na opslaan of plaatsen moet de live advertentie gecontroleerd worden.

Als fetch genoeg tekst bevat:

```bash
marktplaats-live-verify --ad-json ./ad.json --url "https://www.marktplaats.nl/seller/view/..." --update-ad-json
```

Als de pagina dynamisch is, sla eerst zichtbare/live tekst op en verifieer die:

```bash
marktplaats-live-verify --ad-json ./ad.json --text ./live-text.txt --update-ad-json
```

Stop als:

- begin van de omschrijving ontbreekt;
- laatste zin ontbreekt;
- omschrijving dubbel staat;
- `Zoektermen:` of keyworddump live zichtbaar is.

### 7. Register Update

Werk na live verificatie het centrale register bij:

```bash
marktplaats-register-update \
  --ad-json ./ad.json \
  --central-json ~/Documents/OpenClaw/Data/marktplaats/advertenties.json \
  --note "Live gecontroleerd na plaatsing/bewerking."
```

Run register-updates sequentieel. Het script gebruikt een lock en faalt als een tweede update tegelijk hetzelfde centrale register probeert te schrijven.

## Bestaande Advertentie Bewerken

Voor elke inhoudelijke tekstbewerking geldt dezelfde pipeline:

```bash
marktplaats-copy-qa ./description.md --require "<term1>" --require "<term2>" --variant "<variant>" --ad-json ./ad.json
marktplaats-ad-preflight --ad-json ./ad.json --require-bidding-allowed
# bewerk via Marktplaats UI/DOM
marktplaats-live-verify --ad-json ./ad.json --url "<live-url>" --update-ad-json
marktplaats-register-update --ad-json ./ad.json --central-json ~/Documents/OpenClaw/Data/marktplaats/advertenties.json
```

Als live fetch de tekst niet ziet, gebruik `--text ./live-text.txt` met tekst uit de browser/accessibility snapshot.

## Test De Skill

```bash
npm test
```

Deze test moet groen zijn voordat je publiceert naar ClawHub.

## Naslag

- Publieke uitleg: `README.md`
- Langere handleiding: `references/handleiding-nl.md`
- Engelse guide: `references/guide-en.md`
- Robuuste checklist: `references/robust-posting-checklist.md`
