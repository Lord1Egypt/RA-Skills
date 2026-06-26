# Marktplaats.nl Verkoopassistent

Deze skill helpt je om een Marktplaats-advertentie netjes voor te bereiden, te plaatsen en achteraf te controleren.

Het belangrijkste doel is simpel: een goede advertentie maken zonder half werk, zonder betaalde opties per ongeluk aan te zetten en zonder dat de tekst weer te kort, kaal of spammerig wordt.

Vanaf versie 0.6.0 is dit vooral een scriptmatige pipeline. De assistent krijgt dus niet alleen lange instructies, maar moet door harde checks heen: copy-QA, preflight, live-verificatie en register-update.

## Wat doet deze skill?

- Zoekt mee naar categorieën en vergelijkbare advertenties.
- Helpt productinformatie te verwerken zonder dingen te verzinnen.
- Schrijft een volle Nederlandse advertentietekst van ongeveer 3200 tot 3500 tekens.
- Controleert de tekst voordat Marktplaats wordt ingevuld.
- Werkt met een bestaande ingelogde Safari-sessie op macOS.
- Uploadt en controleert foto's via de normale Marktplaats-flow.
- Houdt betaalde promoties standaard uit.
- Controleert na het plaatsen of de advertentie echt live goed staat.
- Bewaart lokaal wat er geplaatst is, inclusief tekstcheck en live controle.

Deze skill is bedoeld voor normale verkoopadvertenties. Niet voor bulkposten, omzeilen van beveiliging, captcha's, loginproblemen of betaalflows.

## Waarom is die tekstcheck zo streng?

Omdat korte advertenties steeds terugkwamen als probleem.

Een advertentie van een paar regels is snel gemaakt, maar meestal slecht vindbaar. Daarom zit er een harde controle in: de tekst moet lang genoeg zijn, genoeg inhoud hebben, natuurlijke zoekwoorden bevatten en geen los blok met `Zoektermen:` of keywordspam onderaan zetten.

De standaard is:

- ongeveer 3200 tot 3500 tekens;
- minimaal 7 duidelijke alinea's of onderdelen;
- merk/model en productsoort moeten erin staan;
- een kleine natuurlijke zoekvariant mag, zoals `deur slot` of `buiten antenne`;
- geen losse zoekwoordenlijst;
- de laatste zin moet ook live zichtbaar zijn na opslaan.

Als die check faalt, moet de advertentie eerst beter worden. Niet toch maar plaatsen.

## Copy check draaien

Gebruik dit voordat je Marktplaats opent of een bestaande advertentie opslaat:

```bash
marktplaats-copy-qa ./description.md \
  --require "KFV" \
  --require "motorslot" \
  --variant "deur slot" \
  --ad-json ./ad.json
```

De check schrijft het resultaat in `ad.json`. Alleen als `copyQuality.passed` op `true` staat, mag de tekst door naar Marktplaats.

Voor een snelle test van de tool zelf:

```bash
marktplaats-copy-qa --self-test
```

## Preflight voor het plaatsen

Na de copy check moet de advertentie door preflight:

```bash
marktplaats-ad-preflight --ad-json ./ad.json --require-bidding-allowed
```

Deze check kijkt of `ad.json`, de omschrijving, foto's, bieden-instelling en copy-QA bij elkaar passen. Als de omschrijving na de copy check nog is aangepast, faalt preflight op de tekst-hash.

## Live controleren na opslaan

Na plaatsen of bewerken moet de live advertentie worden gecontroleerd:

```bash
marktplaats-live-verify --ad-json ./ad.json --url "https://www.marktplaats.nl/seller/view/..." --update-ad-json
```

Als Marktplaats de tekst niet goed in de HTML meestuurt, gebruik je tekst uit de browser:

```bash
marktplaats-live-verify --ad-json ./ad.json --text ./live-text.txt --update-ad-json
```

Deze check faalt als het begin van de omschrijving ontbreekt, de laatste zin ontbreekt, de tekst dubbel staat of er toch een `Zoektermen:` blok live zichtbaar is.

## Register bijwerken

Daarna werk je het centrale register bij:

```bash
marktplaats-register-update \
  --ad-json ./ad.json \
  --central-json ~/Documents/OpenClaw/Data/marktplaats/advertenties.json \
  --note "Live gecontroleerd."
```

Voer register-updates niet parallel uit op hetzelfde bestand. De tool gebruikt een lock en stopt als er al een update loopt.

## Advertentie voorbereiden

Een praktische map per advertentie werkt het prettigst:

```text
~/Documents/OpenClaw/Data/marktplaats/<advertentie-slug>/ad.json
~/Documents/OpenClaw/Data/marktplaats/<advertentie-slug>/description.md
~/Documents/OpenClaw/Data/marktplaats/<advertentie-slug>/photos/
```

Zet in `ad.json` in elk geval titel, prijs, categorie, foto's, status, live URL en het resultaat van de copy check. Zo kun je later terugvinden wat er is geplaatst en wanneer het live gecontroleerd is.

## Plaatsen of bewerken

De normale volgorde:

1. Maak lokaal titel, prijs, foto's en omschrijving klaar.
2. Zoek productinformatie op als merk of model bekend is.
3. Schrijf de omschrijving rijk, feitelijk en verkoopbaar.
4. Draai `marktplaats-copy-qa`.
5. Draai `marktplaats-ad-preflight`.
6. Stop als een van de checks niet slaagt.
7. Open pas daarna de Marktplaats plaats- of bewerkpagina.
8. Controleer dat de gratis/basic route actief is.
9. Upload foto's en controleer de fototeller.
10. Controleer titel, prijs, bieden, foto's en laatste zin van de omschrijving.
11. Sla op of plaats pas als de gebruiker daar opdracht voor gaf.
12. Draai `marktplaats-live-verify`.
13. Draai `marktplaats-register-update`.

## Gratis blijft gratis

Deze skill kiest standaard geen betaalde opties.

Als Marktplaats een betaalde promotie, topadvertentie, urgent-optie, bundel of betaalpagina toont, is dat een stopmoment. Alleen doorgaan als de gebruiker voor die specifieke advertentie expliciet zegt dat een betaalde optie mag.

## Safari en privacy

Voor echt plaatsen of bewerken gebruikt de skill een bestaande ingelogde Safari-sessie. Dat is handig, maar privacygevoelig.

Daarom:

- geen cookies printen;
- geen sessietokens opslaan;
- geen XSRF/auth-waarden loggen;
- geen lokale privébestanden of advertentie-id's in voorbeelden zetten;
- geen koperberichten sturen zonder aparte toestemming.

De browser mag als veilige sessiecontext gebruikt worden. De sessie zelf mag niet worden gelekt.

## Zoek- en categoriehulpen

Zoeken:

```bash
marktplaats-search "4G antenne"
```

Categorieën:

```bash
marktplaats-categories
marktplaats-categories <parent-id>
```

Formulier inspecteren via de ingelogde browsercontext:

```bash
marktplaats-place-probe --browser --save housekeeping/marktplaats-snapshots/current.json
```

## Installeren en testen

```bash
npm install -g .
npm test
```

Node.js 18 of nieuwer is nodig.

## Wat deze skill niet doet

- Geen bulkplaatsingen.
- Geen captcha's of loginbeveiliging omzeilen.
- Geen betaalde opties stil aanzetten.
- Geen garanties verzinnen over werking, compleetheid of accessoires.
- Geen privédata publiceren.
- Geen berichten naar kopers sturen zonder expliciete toestemming.

## Licentie

MIT
