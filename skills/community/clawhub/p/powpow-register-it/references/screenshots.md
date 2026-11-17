# Screenshot dell'interfaccia di prodotto — powpow-register

Da usare all'occorrenza durante l'esecuzione. Quando l'utente non ha un'idea di Bolla, o ha bisogno di
«vedere» che aspetto ha il prodotto finito, mandagli direttamente lo screenshot corrispondente.

## Posizione delle immagini

- I sei screenshot **sono già inclusi nel pacchetto della skill**, in `assets/screenshots/powpow-0N.jpg`
  (`N` da 1 a 6). Vanno inviati direttamente come file immagine locali — niente rete, utilizzabili in
  qualunque ambiente (anche dove GitHub non è raggiungibile).
- Ripiego solo se un file del pacchetto manca per sbaglio: copia ospitata
  `https://raw.githubusercontent.com/durenzidu/durenzidu/main/screenshots/powpow-0N.jpg` oppure mirror
  `https://cdn.jsdelivr.net/gh/durenzidu/durenzidu@main/screenshots/powpow-0N.jpg`
  (attenzione: nella Cina continentale entrambi potrebbero non aprirsi — dare priorità ai file del pacchetto).
- Ogni volta mandane solo 1–3 pertinenti all'argomento corrente.

## Elenco

### powpow-01.jpg — pagina dettaglio umano digitale

![pagina dettaglio umano digitale](../assets/screenshots/powpow-01.jpg)

La scheda di una persona reale/personaggio storico trasformato in umano digitale: stato online, luogo di
appartenenza, profilo del personaggio, «inizia la conversazione» ecc.
**Quando usarla**: presentare «una volta registrato puoi chiacchierare con gli umani digitali sulla mappa».

### powpow-02.jpg — pagina di editor dei post

![pagina di editor dei post](../assets/screenshots/powpow-02.jpg)

L'interfaccia di editing per scrivere post/diari di viaggio, con un gruppo di pulsanti flottanti in basso a destra.
**Quando usarla**: l'utente chiede «una volta registrato cosa posso fare», «dove si scrive».

### powpow-03.jpg — pagina mappa (Bolle + umani digitali)

![pagina mappa](../assets/screenshots/powpow-03.jpg)

La mappa pubblica nella sua interezza: i post con località si raccolgono sulla mappa come «bolle», gli umani
digitali sono appuntati con l'avatar nei luoghi reali.
**Quando usarla**: **l'immagine d'apertura preferita per presentare il prodotto** — «il tuo diario di viaggio
diventerà una bolla sulla mappa».

### powpow-04.jpg — profilo personale (patrimonio digitale)

![profilo personale](../assets/screenshots/powpow-04.jpg)

La pagina dell'utente stesso: amici/follow/follower, e il «patrimonio digitale» — saldo badge, le mie bolle,
i miei umani digitali.
**Quando usarla**: mostrare dove si trovano i badge quando si dice «alla registrazione se ne regalano subito 3»;
l'utente chiede «che patrimonio ho».

### powpow-05.jpg — pagina dei progressi della storia

![pagina dei progressi della storia](../assets/screenshots/powpow-05.jpg)

Il gioco narrativo dentro la piattaforma (esempio «Yongle·1421»): progresso dei capitoli, guadagno badge, gioco di ruolo.
**Quando usarla**: l'utente chiede «oltre ai post cos'altro si può fare», «come si guadagnano i badge».

### powpow-06.jpg — pagina dettaglio post (esempio finito)

![pagina dettaglio post](../assets/screenshots/powpow-06.jpg)

Un diario di viaggio pubblicato: autore, tag del luogo, testo, foto, in fondo like/commento/condivisione/salvataggio.
**Quando usarla**: **la seconda immagine in apertura** — «quando qualcuno apre la tua bolla sulla mappa, vede questo».

## Guida rapida per scenario

| Cosa dice l'utente / fase attuale | Quale immagine mandare |
|---|---|
| Apertura, presentare «cos'è Bolla» | powpow-03 + powpow-06 |
| «Una volta registrato cosa posso fare?» | powpow-02 + powpow-01 |
| «Cosa sono i badge / cosa ho?» | powpow-04 |
| «Oltre ai post cos'altro si può fare?» | powpow-05 |
| Diagnosi errori di registrazione/abbonamento | In genere non servono immagini; mandale solo se serve davvero indicare dove si trova una pagina |

## Note di manutenzione

- Le immagini in `assets/screenshots/` sono la copia principale distribuita col pacchetto. Per aggiornare gli
  screenshot, sostituisci i file omonimi sotto `assets/screenshots/` (mantenendo la nomenclatura `powpow-0N.jpg`)
  e pubblica una nuova versione.
- La copia ospitata nel repository pubblico `durenzidu/durenzidu` (cartella `screenshots/`) resta come mirror
  di ripiego, da aggiornare in sincrono con i file del pacchetto.
- L'attuale raccolta **non contiene** screenshot della pagina di registrazione e della pagina abbonamento. Se
  in futuro verranno aggiunti (ad es. `powpow-07.jpg` pagina registrazione, `powpow-08.jpg` pagina abbonamento),
  basta mettere i file in `assets/screenshots/` e aggiungere una sezione con lo stesso formato; il testo di
  presentazione in SKILL.md può citarli di conseguenza.
