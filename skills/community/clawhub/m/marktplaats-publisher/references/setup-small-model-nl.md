# Setup Voor Kleine Modellen

Gebruik deze reference wanneer een licht model, zoals GPT-4.5 mini of de lokaal beschikbare mini-route, `marktplaats-publisher` moet installeren, herstellen of klaarzetten.

## Doel

Setup is pas klaar wanneer de juiste package is gevonden en de CLI-gates aantoonbaar werken. Een geslaagde setup plaatst of bewerkt nog geen advertentie.

## Identiteit

Verwachte skill/package:

```text
marktplaats-publisher
```

Niet verwarren met:

- `marktplaats`
- `marktplaats-nl-publisher`
- `pvoo/marktplaats`
- alleen een losse Marktplaats zoekskill

Controle:

```bash
node -p "require('./package.json').name + '@' + require('./package.json').version"
```

Stop als de package-naam niet `marktplaats-publisher` is.

## Vereisten

- Node.js 18 of nieuwer.
- Toegang tot de skillmap.
- Schrijfrechten in `~/Documents/OpenClaw/Data/marktplaats/` voor advertentiedata.
- Voor publiceren/bewerken later: een bestaande ingelogde Safari-sessie. Setup zelf vraagt nooit om Marktplaats-wachtwoorden.

Controle:

```bash
node --version
npm --version
```

## Installatie En Smoke-Test

Vanuit de skillmap:

```bash
npm install -g .
npm test
```

`npm test` moet groen zijn. Als globale commands niet beschikbaar zijn, gebruik directe scriptcalls vanuit de skillmap:

```bash
node ./bin/marktplaats-search.js --help
node ./bin/marktplaats-categories.js --help
node ./scripts/marktplaats-place-probe.js --self-test
node ./scripts/marktplaats-copy-qa.js --self-test
node ./scripts/marktplaats-ad-preflight.js --self-test
node ./scripts/marktplaats-live-verify.js --self-test
node ./scripts/marktplaats-register-update.js --self-test
```

Een licht model mag setup alleen als geslaagd rapporteren wanneer deze tests slagen.

## Data-Mappen

Gebruik voor advertentiedata:

```text
~/Documents/OpenClaw/Data/marktplaats/<slug>/ad.json
~/Documents/OpenClaw/Data/marktplaats/<slug>/description.md
~/Documents/OpenClaw/Data/marktplaats/<slug>/photos/
```

Gebruik voor tijdelijke snapshots:

```text
housekeeping/marktplaats-snapshots/
```

Laat geen advertentiedata los in de workspace-root achter.

## Mini-Model Contract

Werk altijd lineair:

1. bepaal de huidige gate;
2. draai precies een command;
3. lees output en exitstatus;
4. noteer `PASS` of `FAIL`;
5. ga alleen door bij bewijs;
6. bij failure: herstel een concrete oorzaak en draai dezelfde gate opnieuw;
7. na twee mislukte herstelpogingen per foutklasse stoppen en rapporteren.

Statusblok per advertentie:

```text
adDir: ...
adJson: ...
description: ...
currentGate: setup | copy-qa | preflight | probe | ui-fill | live-verify | register
lastCommand: ...
result: PASS | FAIL | blocked
nextStep: ...
```

## Stopmomenten

Stop bij:

- verkeerde package-naam;
- Node.js ouder dan 18;
- falende self-test;
- ontbrekende globale CLI zonder werkende directe scriptfallback;
- login, captcha, MFA, WAF of betaalpagina;
- verzoek om cookies, sessietokens of wachtwoorden te exporteren;
- onduidelijke formulierstatus of UI-drift.

## Wat Setup Niet Doet

- Geen echte advertentie publiceren.
- Geen bestaande advertentie bewerken.
- Geen betaalde optie kiezen.
- Geen Marktplaats-login automatiseren.
- Geen koperberichten sturen.

Setup eindigt met een korte status: package, versie, tests, beschikbare commando's en eventuele blokkade.
