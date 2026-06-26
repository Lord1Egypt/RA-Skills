# Marktplaats Verkoopassistent - Nederlandse Handleiding

## Naam

**Marktplaats Verkoopassistent**

Technische skill-key: `marktplaats`.

Deze naam is bewust breder dan alleen zoeken. De skill helpt bij het volledige verkoopproces: categorie kiezen, velden bepalen, foto's voorbereiden/uploaden, lokaal bijhouden, herplaatsing voorbereiden, dry-run maken en pas na akkoord publiceren.

## Doel

De skill helpt een gebruiker of agent om Marktplaats-advertenties betrouwbaar en veilig voor te bereiden, te plaatsen en later terug te vinden voor controle of herplaatsing. De belangrijkste verbetering ten opzichte van handmatig werken is dat de agent eerst de actuele categorievelden uitleest en daarna pas een advertentie invult. Daarnaast houdt de skill lokaal bij wat geplaatst is, met welke foto's en tekst, zodat verlopen advertenties later opnieuw voorbereid kunnen worden.

## Wat De Skill Kan

- Marktplaats doorzoeken op vergelijkbare advertenties.
- Categorieën en subcategorieën ophalen.
- Een beste categorie voorstellen voor een item.
- Een live plaatsingsformulier uitlezen via de browser.
- Categorie-specifieke velden verzamelen, zoals conditie, merk, type, maat, levering, prijs en extra opties.
- Foto's verkleinen en metadata-arm maken waar mogelijk.
- Foto's uploaden via de ingelogde Marktplaats-browsercontext.
- Advertentiedata invullen in het formulier.
- Betaalde opties standaard uitschakelen.
- Een dry-run samenvatting tonen.
- Na expliciet akkoord een advertentie publiceren.
- Na publicatie de success-URL of foutmelding rapporteren.
- Geplaatste advertenties lokaal administreren.
- Verlopen of verwijderde advertenties markeren voor herplaatsing.
- Foto's en korte omschrijvingen uit WhatsApp/iMessage als advertentie-intake gebruiken wanneer de gebruiker daarom vraagt.
- Advertentieteksten vóór publicatie verplicht controleren met de Copy Quality Gate.

## Wat De Skill Niet Zelfstandig Mag

- Geen advertentie publiceren of herplaatsen zonder expliciet akkoord per advertentie.
- Geen betaalde plaatsing of promotie inschakelen zonder apart akkoord.
- Geen prijs verzinnen als de gebruiker geen prijs heeft gegeven.
- Geen conditie kiezen als die onzeker is.
- Geen captcha, login, WAF of beveiligingscontrole omzeilen.
- Geen berichten beantwoorden aan kopers zonder aparte toestemming.
- Geen cookies, XSRF-tokens of sessiegegevens delen.

## Benodigde Rechten

Voor zoeken:

- Netwerktoegang naar Marktplaats.
- Node.js voor de CLI-tools.

Voor advertentievoorbereiding:

- Leesrechten op lokale fotobestanden.
- Leesrechten op relevante WhatsApp/iMessage-bijlagen wanneer de gebruiker vraagt die te gebruiken.
- Schrijfrechten voor advertentiegegevens, foto's en snapshots, bij voorkeur:
  - `~/Documents/OpenClaw/Data/marktplaats/`
  - `housekeeping/marktplaats-snapshots/`
  - `housekeeping/marktplaats-test/`

Voor plaatsen:

- Een browser waarin de gebruiker al is ingelogd op Marktplaats.
- macOS automation via AppleScript of Peekaboo om de browsercontext te gebruiken.
- Toegang tot de Marktplaats plaatsingspagina.

Belangrijk: de skill heeft geen Marktplaats-wachtwoord nodig. Login blijft bij de gebruiker/browser.

## Lokale Advertentieadministratie

Centrale administratie:

```text
~/Documents/OpenClaw/Data/marktplaats/advertenties.json
```

Per advertentie kan een eigen map worden gebruikt:

```text
~/Documents/OpenClaw/Data/marktplaats/<slug>/
```

Aanbevolen inhoud:

- `ad.json`: advertentie-id, URL, status, prijs, categorie, bron en herplaatsinformatie.
- `description.md`: laatst gebruikte advertentietekst.
- `photos/originals/`: bronfoto's.
- `photos/processed/`: verkleinde/metadata-arme publicatiefoto's.
- `snapshots/`: formulier- of submit-snapshots.

Belangrijke statussen:

- `draft`
- `pending_approval`
- `active`
- `removed`
- `expired`
- `needs_repost`
- `reposted`
- `test`

Na elke plaatsing, foutmelding, verwijdering, statuscheck of herplaatsing wordt het register bijgewerkt.

## Herplaatsing Na Verlopen

Marktplaats kan regels wijzigen. Controleer daarom de actuele looptijd of advertentiestatus voordat je automatisch conclusies trekt.

Standaardflow:

1. Lees `advertenties.json`.
2. Zoek actieve advertenties met verlopen `renewAfter`/`expiresAt` of advertenties die niet meer zichtbaar lijken.
3. Controleer de advertentiestatus.
4. Zet ze op `needs_repost` als herplaatsing zinvol is.
5. Maak een nieuwe dry-run op basis van de bestaande tekst/foto's, met verse categorie- en formuliercheck.
6. Publiceer pas na expliciet akkoord van de gebruiker.
7. Voeg de nieuwe advertentie-id toe aan het register en bewaar de oude in `repostHistory`.

Een cron/heartbeat mag melden dat advertenties herplaatst moeten worden, maar mag niet zelfstandig publiceren.

## Intake Vanuit WhatsApp Of iMessage

Wanneer de gebruiker foto's stuurt en zegt wat het is:

1. Lees alleen de relevante berichten/bijlagen.
2. Sla de foto's lokaal op in de advertentiemap.
3. Maak veilige publicatiekopieën.
4. Leg de bron vast, zoals kanaal, chat-id, message-id en tijdstip.
5. Herken item, merk/model en zichtbare details.
6. Vraag ontbrekende kerngegevens: prijs, conditie, ophalen/verzenden, gebreken, missende onderdelen.
7. Zoek productinformatie online.
8. Kies categorie en inspecteer het actuele formulier.
9. Schrijf een sterke SEO-advertentie van circa 3200-3500 tekens.
10. Draai `marktplaats-copy-qa` met producttermen en een natuurlijke zoekvariant.
11. Toon dry-run.
12. Plaats alleen na expliciet akkoord.

Voor WhatsApp/iMessage geldt: lezen/analyseren mag als de gebruiker daarom vraagt; antwoorden naar anderen of kopers sturen alleen na aparte toestemming.

## Standaard Stappenplan

### 1. Item Begrijpen

Bepaal:

- wat het item is;
- merk/type/model;
- conditie;
- gewenste prijs;
- ophalen/verzenden;
- meegeleverde onderdelen;
- gebreken of bijzonderheden;
- beschikbare foto's.

Als prijs, conditie of essentieel detail ontbreekt: vraag de gebruiker.

### 2. Categorie-Kandidaten Zoeken

Gebruik:

```bash
marktplaats-categories --json
marktplaats-categories <parent-id> --json
marktplaats-search "<productnaam>" --json -n 10
```

Kies de categorie op basis van:

- bestaande vergelijkbare advertenties;
- passende attributen;
- gratis plaatsingsmogelijkheid;
- logische vindbaarheid voor kopers.

Motiveer de keuze in de dry-run.

### 3. Copy Quality Gate

Voordat Marktplaats wordt ingevuld:

```bash
marktplaats-copy-qa ./description.md \
  --require "<merk-of-type>" \
  --require "<productsoort>" \
  --variant "<natuurlijke zoekvariant>" \
  --ad-json ./ad.json
```

Stop als de command faalt of als `ad.json.copyQuality.passed` niet `true` is.

Harde eisen:

- standaard 3200-3500 tekens;
- absolute ondergrens 2800 tekens;
- minimaal 7 substantiële secties/alinea's;
- geen `Zoektermen:`, `Keywords:` of keyworddump;
- natuurlijke SEO-termen in lopende tekst;
- minimaal één subtiele spelfout/schrijfvariant in context.

### 4. Live Plaatsingsformulier Inspecteren

Open de plaatsingspagina voor de gekozen categorie en maak een snapshot met de probe:

```bash
node scripts/marktplaats-place-probe.js --browser --save housekeeping/marktplaats-snapshots/current.json
```

Controleer:

- `form.action` (meestal `https://www.marktplaats.nl/plaats/ads`);
- categorievelden (`l1`, `l2`, `bucket`);
- aanwezigheid van een XSRF-token, niet de waarde;
- hidden formulierwaarden;
- titel/omschrijving;
- prijsvelden;
- conditievelden;
- categorie-attributen;
- leveringsvelden;
- postcode/contact;
- betaalde opties;
- geselecteerde bundle.

Een `curl`-probe op `/plaats` kan `401` geven als er geen sessiecookie wordt meegegeven. Dat is normaal: gebruik in dat geval de ingelogde browser-DOM als bron van waarheid, niet handmatige UI-kliks.

Gebruik voor authenticated requests zonder cookies te exporteren:

```bash
node scripts/marktplaats-place-probe.js --browser-fetch --url https://www.marktplaats.nl/plaats
```

Deze route gebruikt Safari's bestaande sessie via `XMLHttpRequest` met credentials. Cookies en sessietokens blijven in Safari en worden niet gelogd.

### 5. Velden Invullen

Gebruik conservatieve mapping:

- Titel kort en specifiek.
- Beschrijving feitelijk, geen overdreven verkooppraat.
- Conditie alleen invullen als redelijk zeker.
- Prijs alleen van de gebruiker of expliciet akkoord.
- Multi-selects alleen aanvinken als zeker passend.
- Levering standaard ophalen, tenzij de gebruiker verzending wil.

### 6. Gratis Advertentie Afdwingen

Controleer vóór publicatie:

- gratis bundle geselecteerd;
- geen urgent/etalage/homepage/promotie;
- geen betaalpagina;
- geen onverwachte kosten.

Als Marktplaats toch kosten toont: stoppen en rapporteren.

### 7. Foto's Voorbereiden

Maak bij voorkeur tijdelijke kopieën:

```bash
mkdir -p housekeeping/marktplaats-test
sips -Z 1600 -s format jpeg input.jpg --out housekeeping/marktplaats-test/photo-1.jpg
```

Controleer waar mogelijk of GPS/EXIF niet meer zichtbaar is.

### 8. Foto's Uploaden

Gebruik de bewezen browsercontext-route. De Marktplaats frontend verwacht:

- endpoint: `/plaats/api/image/upload`
- method: `POST`
- FormData velden:
  - `name`
  - `imageData`
- header:
  - `x-mp-xsrf`

Upload de foto's in de live flow en lees daarna de gegenereerde `images.ids`/hidden fields terug uit de probe. Gebruik de browser alleen als sessiedrager, niet om handmatig een uploadpad te raden.

### 9. Dry-Run Tonen

Altijd tonen vóór publiceren:

```text
Categorie: ...
Waarom deze categorie: ...
Titel: ...
Prijs: ...
Conditie: ...
Levering: ...
Foto's: ...
Gratis advertentie: ja/nee
Betaalde opties: geen
Onzekere velden: ...
Na akkoord: publiceren op Marktplaats
```

### 9. Publiceren

Alleen na expliciet akkoord. Na submit:

- success-redirect rapporteren;
- advertentie-id/link rapporteren;
- validatiefouten kort samenvatten;
- bij betaalpagina stoppen;
- lokale advertentieadministratie bijwerken.

## Testprotocol

Aanbevolen testperiode:

1. Begin met 1 dummy/testadvertentie.
2. Test daarna 2-3 echte goedkope advertenties.
3. Controleer of categorie, prijs, foto's en gratis opties kloppen.
4. Controleer of advertenties makkelijk te verwijderen zijn.
5. Noteer welke categorieën/velden lastig zijn.
6. Test daarna herplaatsing vanuit het lokale register.
7. Test daarna intake vanuit WhatsApp/iMessage-foto's.
8. Pas daarna publicatie op ClawHub overwegen.

## Publicatie Op ClawHub

Voor publicatie moet de skill duidelijk vermelden:

- dat publiceren en herplaatsen alleen na expliciet akkoord mag;
- dat de gebruiker zelf ingelogd moet zijn;
- dat de skill geen login/captcha omzeilt;
- dat betaalde opties standaard uit staan;
- dat lokaal advertentiebeheer persoonsgegevens/foto's kan bevatten en dus privé behandeld moet worden;
- welke lokale tools nodig zijn;
- dat Marktplaats-flows kunnen wijzigen;
- dat de gebruiker verantwoordelijk blijft voor advertentie-inhoud en platformregels.
