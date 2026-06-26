---
name: inr-sender
description: "Envoie le résultat de l'INR (International Normalized Ratio) à un centre de télémédecine spécialisé ou pour un test. Utilise ce skill lorsque Gilles souhaite transmettre son INR, en spécifiant la valeur et si c'est un test."
---

# INR Sender Skill

Ce skill permet d'envoyer votre valeur INR à une adresse e-mail prédéfinie ou à une adresse de test.

## Utilisation

Pour envoyer votre INR :
`inr-sender <valeur_inr> [--test]`

- `<valeur_inr>` : La valeur numérique de votre INR (ex: 2.5).
- `--test` (optionnel) : Si présent, l'e-mail sera envoyé à `harpoutian@gmail.com` pour un test. Sinon, il sera envoyé à `creatif.lrb@aphp.fr`.

## Message envoyé

Le message aura le format suivant :
"Bonjour, aujourd'hui (date du jour) mon INR était de [valeur_inr] (automesure). Merci et bonne journée, Gilles Harpoutian né le 16/07/1974"

## Script (`scripts/send_inr.sh`)

Le skill utilise le script `scripts/send_inr.sh` pour formater et envoyer l'e-mail.
