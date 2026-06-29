---
name: pan-pac
description: |
  Pan Pacific Travel agent — contexte métier, delegation email/calendar et bookings Lynx.
  USE THIS SKILL pour toute demande liée aux e-mails, messages, calendrier, événements ou bookings dans le contexte Pan Pacific Travel.
metadata:
  author: custom
  version: "1.0"
---

# Pan Pac — Contexte Métier

Agent spécialisé pour Pan Pacific Travel. Traite les communications email avec clients et prestataires dans le cadre de **bookings de voyage**.

## Interlocuteurs par email

Les échanges email se font avec 4 types d'interlocuteurs :

1. **Personnel Pan Pacific Travel** — managers et agents de voyages internes. Pan Pacific Travel est une agence australienne qui gère les bookings via un outil called **Lynx** (skill dédié à venir).

2. **Agences externes** (ex: Voyageurs du Monde) — agents de voyages "clients" de Pan Pacific. Ces agences vendent les voyages aux clients finaux et délèguent l'organisation et l'exécution des bookings à Pan Pacific.

3. **Prestataires touristiques et hôtels** — tous les prestataires impliqués dans un voyage sur-mesure. Les agents Pan Pacific travaillent directement avec eux.

4. **Clients finaux** — contact rare, mostly en après-vente et "conciergerie" pendant le voyage.


## Tâche principale

Lire et traiter ces échanges pour extraire : dates, destinations, passagers, préférences, statuts de réservation, confirmations, modifications, annulations.

## Delegation Lynx (bookings)

Pour toute recherche de **dossiers/reservations**, consultation d'**itinéraires**, upload de **documents** ou gestion de **pièces jointes** dans le système Lynx, utiliser le skill `lynx-skill`.

Consulter `lynx-skill/SKILL.md` pour les détails d'implémentation (7 commandes disponibles : recherche par nom, par référence fichier, itinéraires, documents, upload de pièces jointes).

**Point important — bookings annulés :** Par défaut, `retrieve-itinerary` n'affiche que les bookings actifs. Pour voir aussi les bookings annulés ( Annulation ), ajouter le flag `--show-cancelled`.

## Delegation Outlook

Pour tout ce qui concerne la **lecture d'e-mails et d'événements calendrier**, utiliser impérativement le skill `outlook-entra`.

Ce skill contient toute la documentation technique :
- Authentification OAuth 2.0 / Entra
- Commandes d'accès aux messages, dossiers, pièces jointes
- Recherche dans les e-mails
- Événements calendrier
- Cron de refresh automatique du token

Consulter `outlook-entra/SKILL.md` pour les détails d'implémentation.
