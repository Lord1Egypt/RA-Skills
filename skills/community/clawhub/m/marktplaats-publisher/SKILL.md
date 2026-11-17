---
name: "marktplaats-publisher"
description: "Marktplaats-advertenties voorbereiden, plaatsen/bewerken, copy-QA, preflight, live-verificatie en register."
metadata: {"clawdbot":{"emoji":"🇳🇱","requires":{"bins":["node"]}}}
---

# Marktplaats Publisher

Gebruik deze skill voor normale Marktplaats-advertenties: voorbereiden, plaatsen, bewerken, live controleren en lokaal registreren.

De workflow is command-first. Proceduretekst is alleen toelichting. Als een gate faalt, stop je.

Voor kleinere modellen: doe steeds een fase, lees de output, en ga pas door als de vorige fase aantoonbaar geslaagd is. De scripts zijn harde gates; publiceren en UI-invulwerk blijven browserwerk met verificatie, geen blinde submit-flow.

## Setup En Modelmodus

Als de taak installatie, eerste setup of herstel van de skill is, laad `references/setup-small-model-nl.md`.

Package-identiteit:

- correcte skill/package: `marktplaats-publisher`;
- oude namen zoals `marktplaats`, `marktplaats-nl-publisher` of `pvoo/marktplaats` zijn niet de doel-skill;
- vereiste runtime: Node.js 18 of nieuwer;
- vereiste smoke-test: `npm test` vanuit de skillmap.

Voor lichte modellen zoals GPT-4.5 mini of de lokaal beschikbare mini-route geldt dit contract:

- voer steeds precies een gate uit;
- lees de output volledig;
- ga alleen door bij expliciet `PASS`, `self-test ok` of exitcode 0 met verwachte output;
- bij failure: repareer een oorzaak, draai dezelfde gate opnieuw, maximaal twee herstelpogingen per foutklasse;
- publiceer, bewerk of submit niets als setup, copy-QA, preflight of probe niet aantoonbaar groen is;
- houd per advertentie een klein statusblok bij met `adDir`, `adJson`, `description`, `currentGate`, `lastCommand`, `result` en `nextStep`.

Als globale CLI-commando's ontbreken, gebruik vanaf de skillmap de directe fallback:

```bash
node ./scripts/marktplaats-place-probe.js --self-test
node ./scripts/marktplaats-copy-qa.js --self-test
node ./scripts/marktplaats-ad-preflight.js --self-test
node ./scripts/marktplaats-live-verify.js --self-test
node ./scripts/marktplaats-register-update.js --self-test
```

## Harde Regels

- Geen publicatie of inhoudelijke bewerking zonder expliciete opdracht voor die advertentie.
- Geen betaalde opties, bundels, promoties of betaalflow zonder expliciet akkoord.
- Geen cookies, sessietokens, XSRF/auth-waarden, klantdata of lokale privepaden loggen of publiceren.
- Geen captcha, MFA, login challenge, WAF of accountbeveiliging omzeilen.
- Geen tekst plaatsen als copy-QA of preflight faalt.
- Gebruik `--allow-*` opties alleen bij expliciete, taak-specifieke uitzondering van de gebruiker.
- Publiceerbare advertentietekst mag nooit websiteadressen of domeinachtige tekst bevatten. Verboden zijn onder andere `http://`, `https://`, `www.`, e-mailadressen en woorden met bekende domeinextensies zoals `.com`, `.nl`, `.eu`, `.org`, `.net`, `.de`, `.be` en `.io`. Merknamen met een domeinextensie, zoals `StarTech.com`, moeten worden herschreven naar een gewone merknaam zonder punt, bijvoorbeeld `StarTech`.
- Publiceer of accepteer geen advertentie waarvan de live omschrijving als een grote lap tekst verschijnt. De lokaal geschreven alinea's moeten live aantoonbaar bewaard blijven via alinea's, `<br>`-achtige regelovergangen of Marktplaats-blokken.
- Na opslaan altijd live verifieren en het lokale register bijwerken.
- Bij UI-drift, browser-hang of onduidelijke formulierstatus: stop, maak een snapshot en rapporteer de blokkade.

## Safari Rustig Gebruiken

Laad `references/background-safari-nl.md` bij plaats-/bewerkwerk met Safari.

Voorkeursvolgorde:

1. Gebruik gewone HTTP/API/zoek-CLI waar geen login nodig is.
2. Gebruik `marktplaats-place-probe --browser-fetch --url ...` voor authenticated inspectie zonder zichtbare navigatie.
3. Gebruik `marktplaats-place-probe --browser --open-background ...` om een pagina in Safari te openen zonder Safari actief te maken.
4. Gebruik zichtbare UI alleen als foto-upload, contenteditable tekst of expliciete controle dat vereist.

Regels:

- activeer Safari niet onnodig en open geen extra schermen bovenop het werk van de gebruiker;
- gebruik een bestaande of dedicated Marktplaats-tab; kies tabs op URL/ad-id, niet op schermpositie;
- herstel of laat de actieve gebruikerscontext ongemoeid waar mogelijk;
- log geen cookies, tokens, XSRF-waarden, contactgegevens of browserprofielinformatie;
- bij login/captcha/MFA/WAF, betaalroute, UI-drift of onduidelijke status: stop, schrijf een snapshot en rapporteer.

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
- natuurlijke zoekvarianten in gewone zinnen;
- minimaal een, en bij voorkeur niet meer dan twee, subtiele productrelevante typefout-/schrijfvarianten in gewone zinnen. Voorbeeld: `buiten antenne` naast `buitenantenne`.

Niet doen:

- geen websiteadressen, domeinachtige merknamen, `www.`-tekst, URL's of e-mailadressen;
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

Herhaal `--variant` alleen voor een tweede minimale variant als die natuurlijk in de omschrijving past. Gebruik geen losse typefoutenlijst.

Copy-QA faalt bij URL's, `www.`-tekst, e-mailadressen en domeinachtige tekst zoals `startech.com`, ook als er geen protocol voor staat.

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
- publiceerbare advertentietekst bevat geen URL's, `www.`-tekst, e-mailadressen of domeinachtige tekst;
- foto's bestaan;
- biedeninstelling indien vereist.

### 4. Formulier Probe

Inspecteer Marktplaats voordat je invult. Kies de minst storende route die genoeg bewijs geeft.

Met browser-fetch:

```bash
marktplaats-place-probe --browser-fetch --url "https://www.marktplaats.nl/plaats/..." --save ./snapshot-place.json
```

Als Safari niet de actieve app hoeft te worden, open de plaatsingspagina op de achtergrond en probe daarna dezelfde Safari-context:

```bash
marktplaats-place-probe --browser \
  --open-background "https://www.marktplaats.nl/plaats/..." \
  --save ./snapshot-place.json
```

Als de juiste Marktplaats-tab al open staat:

```bash
marktplaats-place-probe --browser --save ./snapshot-place.json
```

Stop als:

- login/captcha/MFA/WAF verschijnt;
- betaalde route verplicht lijkt;
- formulierstructuur onduidelijk is;
- foto-upload of bundelkeuze niet te verifieren is;
- `security.challengeSignals` login, captcha, MFA, WAF of betaal-/promotiesignalen toont.

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
- laatste zin van de omschrijving zichtbaar in het formulier;
- alinea's zichtbaar in het omschrijvingsveld; gebruik bij voorkeur het zichtbare rich-text/contenteditable veld en geen directe hidden-field submit voor de omschrijving.

Gebruik geen blinde coordinate-clicks. Gebruik DOM/events of een expliciet UI-element met verificatie voor en na.

Gebruik geen directe hidden-field submit of platte `URLSearchParams`-post voor de omschrijving tenzij live-verificatie daarna bewijst dat alinea's bewaard zijn. Als Marktplaats de tekst ondanks correcte inhoud als een doorlopende lap toont, is de advertentie niet klaar.

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
- `Zoektermen:` of keyworddump live zichtbaar is;
- live advertentietekst alsnog websiteadressen of domeinachtige tekst bevat;
- live omschrijving geen aantoonbare alinea-/regelstructuur heeft.

### 7. Register Update

Werk na live verificatie het centrale register bij:

```bash
marktplaats-register-update \
  --ad-json ./ad.json \
  --central-json ~/Documents/OpenClaw/Data/marktplaats/advertenties.json \
  --note "Live gecontroleerd na plaatsing/bewerking."
```

Run register-updates sequentieel. Het script gebruikt een lock en faalt als een tweede update tegelijk hetzelfde centrale register probeert te schrijven.

De register-update hoort standaard te falen als live-verificatie ontbreekt of faalde. Gebruik `--allow-unverified` alleen voor niet-gepubliceerde conceptadministratie en vermeld waarom in `--note`.

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
- Setup voor kleine modellen: `references/setup-small-model-nl.md`
- Rustige Safari/background-flow: `references/background-safari-nl.md`
