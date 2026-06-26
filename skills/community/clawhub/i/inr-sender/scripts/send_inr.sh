#!/bin/bash

INR_VALUE="$1"
IS_TEST="$2" # --test if present

RECIPIENT="creatif.lrb@aphp.fr"
if [ "$IS_TEST" == "--test" ]; then
    RECIPIENT="harpoutian@gmail.com"
fi

CURRENT_DATE=$(LC_TIME=fr_FR.UTF-8 date +"%A %d %B" | sed -e 's/lundi/Lundi/' -e 's/mardi/Mardi/' -e 's/mercredi/Mercredi/' -e 's/jeudi/Jeudi/' -e 's/vendredi/Vendredi/' -e 's/samedi/Samedi/' -e 's/dimanche/Dimanche/')
MESSAGE="Bonjour,

Aujourd'hui ${CURRENT_DATE} mon INR est de ${INR_VALUE} (automesure).

Merci et bonne journée,

Gilles Harpoutian né le 16/07/1974"
SUBJECT="INR de Gilles Harpoutian - ${CURRENT_DATE}"

# Utilisation de l'outil gog pour envoyer l'e-mail
# gog gmail send --to <recipient> --subject <subject> --body <message> --account <account_email>
/root/go/bin/gog gmail send --to "${RECIPIENT}" --subject "${SUBJECT}" --body "${MESSAGE}" --account harpoutian@gmail.com