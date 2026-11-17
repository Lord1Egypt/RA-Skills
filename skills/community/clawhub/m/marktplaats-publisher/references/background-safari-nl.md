# Rustige Safari En Background-Flow

Gebruik deze reference wanneer `marktplaats-publisher` een ingelogde Safari-context nodig heeft voor formulierinspectie, foto-upload of live controle.

## Doel

Gebruik Safari als sessiedrager zonder de gebruiker onnodig te storen. Background-first betekent: geen vensters naar voren halen, geen coordinate-clicks en geen zichtbare UI tenzij de Marktplaats-flow dat echt vereist.

## Voorkeursvolgorde

1. Gebruik gewone HTTP/API/zoek-CLI voor publieke informatie.
2. Gebruik `marktplaats-place-probe --browser-fetch --url ...` voor authenticated HTML/formulierinspectie vanuit Safari-context.
3. Gebruik `marktplaats-place-probe --browser --open-background ...` om een plaatsings- of bewerkpagina in Safari te openen zonder Safari te activeren.
4. Gebruik zichtbare UI alleen voor stappen die niet betrouwbaar via DOM/fetch kunnen: foto-upload, contenteditable tekstcontrole of expliciete visuele bevestiging.

## Niet Storen-Regels

- Activeer Safari niet wanneer background-probe of browser-fetch voldoende is.
- Open geen extra vensters of schermen bovenop het werk van de gebruiker.
- Kies Safari-tabs/documenten op URL, categoriepad of advertentie-id, niet op schermpositie.
- Laat de gebruiker zijn actieve app en tab houden waar dat kan.
- Gebruik snapshots in `housekeeping/marktplaats-snapshots/` voor bewijs en debugging.
- Bij foreground UI: meld kort waarom foreground nodig is en doe zo weinig mogelijk.

## Privacyregels

- Cookies, sessietokens, XSRF/auth-waarden, contactgegevens en browserprofielinformatie nooit printen of opslaan.
- Safari mag credentials gebruiken via normale browsercontext, maar de skill mag die credentials niet exporteren.
- Geen Marktplaats-wachtwoorden vragen of opslaan.

## Stopmomenten

Stop en rapporteer bij:

- login/captcha/MFA/WAF;
- betaalpagina of promotieroute;
- onduidelijke formulierstructuur;
- foto-upload of fototeller die niet te verifieren is;
- Safari-hang of browser-UI die niet betrouwbaar te herstellen is.

Bij een vastgelopen automationproces: stop alleen het vastzittende helperproces waar mogelijk, niet heel Safari.
