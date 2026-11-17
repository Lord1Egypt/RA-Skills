---
name: powpow-register
description: Aiuta gli utenti a completare la registrazione a PowPow (Bolla) e l'accesso con un clic, tutto dentro la conversazione. L'agent compila il modulo al posto loro (incluso il caricamento dell'avatar) e invia il codice di verifica via e-mail; l'utente fornisce solo le informazioni di base e controlla il codice una volta, senza uscire dalla conversazione. Nell'attuale periodo di prova gratuita della piattaforma, un account registrato può usare subito tutte le funzioni; il pagamento dell'abbonamento (Alipay/PayPal) è un miglioramento di iscrizione opzionale, che l'agent può anch'esso gestire con creazione dell'ordine e tracciamento dell'incasso quando serve. Si attiva quando l'utente dice «registrati a Bolla», «crea un account powpow», «come mi registro a Bolla», «aiutami a creare un account powpow», «sign up powpow»; gestisce anche i blocchi della registrazione (codice di verifica non ricevuto, nome utente/e-mail già occupati) e i problemi di attivazione (il login dice «account non attivato» / pending_payment, come abbonarsi/pagare, Bolla è gratis?). Richiede Node ≥ 18; in caso di indisponibilità, rientro automatico nella modalità di sola guida. Non copre pubblicare/creare umani digitali (quello è compito di powpow-simple) né sviluppo di codice.
version: 2.2.0
metadata:
  openclaw:
    emoji: "\U0001F4DD"
    homepage: https://global.powpow.online
---

# PowPow Register (assistente alla registrazione a Bolla)

Porta un utente nuovo da «non so cos'è Bolla» a «accesso con un clic, pronto per iniziare» — tutto dentro la conversazione. L'utente esce dalla conversazione una sola volta: **per controllare il codice di verifica nella propria e-mail**. La piattaforma è attualmente in un periodo di prova gratuita: una volta registrato, tutte le funzioni sono utilizzabili, nessun pagamento richiesto; il pagamento dell'abbonamento è un miglioramento di iscrizione opzionale (l'agent apre anche la cassa e traccia l'incasso).

**Versione 2.2.0** · 2026-10-18 (dalla v2 modalità assistita dall'agent: contratto dello script e sequenza completa in `references/agent-flow.md`; regole dei campi, limiti di frequenza e risoluzione degli errori in `references/registration-flow.md`; canali di pagamento in `references/payment-and-activation.md`; elenco delle schermate prodotto in `references/screenshots.md`. Dalla v2.1.0 anche gli abbonamenti PayPal possono essere gestiti dall'agent, come opzione accanto ad Alipay. Dalla v2.2.0 la piattaforma entra in un periodo di prova gratuita: registrati e accedi con un clic per iniziare; il pagamento diventa un miglioramento opzionale — se l'utente apre il link e finisce sulla pagina di abbonamento, il periodo di prova è finito, quindi segui il flusso di pagamento del Passo 7; il flusso si adatta da sé, senza modificare lo script)

## Ambiente di esecuzione

- Script principale `scripts/powpow-register.mjs`: **zero dipendenze**, richiede **Node ≥ 18**. Prima di iniziare esegui una volta `node scripts/powpow-register.mjs status` per confermare che l'ambiente funzioni.
- Tutte le richieste dello script vanno solo al dominio ufficiale `https://global.powpow.online`.
- **Nessun Node / errori dello script**: rientro automatico nella modalità di sola guida — dai all'utente la pagina di registrazione https://global.powpow.online/register e accompagnalo secondo `references/registration-flow.md` (nel periodo di prova gratuita, anche la registrazione web è equally immediata). Non insistere con lo script.
- Ripristino dopo un'interruzione della conversazione: esegui prima `status` per vedere a che punto è il flusso, poi riprendi da lì.

## Trigger Conditions

- Intenzione di registrarsi: «registrati su Bolla», «crea un account powpow», «come ci si registra su Bolla», «sign up powpow»
- Registrazione bloccata: «non arriva il codice di verifica», «dice che il nome utente esiste già», «la password non passa mai»
- Problemi dopo la registrazione: «il login dice che l'account non è attivato», «403 pending_payment», «come pago/mi abbono a Bolla», «Bolla è gratis o a pagamento?»

**Non attivare per**: pubblicare post/creare umani digitali (→ powpow-simple); sviluppo di codice lato Web (vedi le skill di sviluppo). Utente che vuole sia registrarsi sia pubblicare: completa prima questa skill, poi dopo l'attivazione passa a powpow-simple.

## Panoramica del flusso

| Passo | Cosa fa l'agent | Cosa fa l'utente |
|---|---|---|
| 1 Presentazione prodotto | Presenta + manda screenshot | Dà un'occhiata |
| 2 Conferma informazioni | Proponi attivamente nome utente/nickname, password scelta tra due opzioni, chiedi l'email | Conferma, fornisce |
| 3 Invio codice | `send-code` | —— |
| 4 Lettura codice | —— | Va nell'email, legge il codice a 6 cifre e lo rimanda |
| 5 Invio registrazione | `register` (con caricamento diretto dell'avatar), gestione automatica degli errori | —— |
| 6 Accesso con un clic | `login-link(home)` direttamente sulla home; se finisce sulla pagina di abbonamento, vai al Passo 7 | Clicca il link e inizia |
| 7 Miglioramento dell'abbonamento (opzionale) | Solo quando l'utente vuole l'iscrizione / il periodo gratuito è finito: flusso di pagamento completo gestito | Scegli un metodo, paga |
| 8 Chiusura | `cleanup` + consegna credenziali + guida all'esperienza + suggerimento plugin | Inizia a giocare |

## Passo 1: presentazione del prodotto + screenshot (da non saltare)

La maggior parte degli utenti non ha mai visto Bolla. La prima cosa non è raccontare il flusso, ma far **vedere** il prodotto:

1. Presenta Bolla in ~120 caratteri: trasforma gli scatti istantanei in un diario di viaggio, li appunta su una mappa pubblica come una «bolla»; la bolla si raffredda col tempo, e i «like» degli altri possono farla rinascere; sulla mappa ci sono anche «umani digitali» con cui chiacchierare. Indirizzo della piattaforma: https://global.powpow.online ; se prima vuole vedere un video: https://www.bilibili.com/video/BV1Wu826UEVz/
2. **Manda gli screenshot**. Sono già inclusi nel pacchetto in `assets/screenshots/powpow-0N.jpg` — inviali direttamente come file immagine locali, senza bisogno di rete. Elenco, contenuto di ogni immagine e occasioni d'uso sono in `references/screenshots.md`. La coppia più usata in apertura: pagina mappa (powpow-03) + pagina dettaglio post (powpow-06).

Regole per gli screenshot (regole ferree):

- Gli screenshot **sono inclusi nel pacchetto** in `assets/screenshots/` (`powpow-0N.jpg`) — inviali direttamente come file immagine locali; funzionano in qualunque ambiente, anche dove GitHub non è raggiungibile.
- Ogni volta mandane solo 1–3 pertinenti all'argomento corrente, non mandarli tutti insieme.
- Se un file del pacchetto manca per sbaglio, ripiega sui link di hosting elencati in `references/screenshots.md` (attenzione: nella Cina continentale potrebbero non aprirsi).

Finita la presentazione, restituisci la scelta all'utente: **«Se vuoi registrarti, in tre minuti ti creo l'account direttamente in conversazione; dovrai solo leggere una volta il codice di verifica nell'email.»**

## Passo 2: conferma delle informazioni di registrazione (una domanda per turno, non tutto insieme)

- **Nome utente** (obbligatorio): **proponine attivamente uno** a partire dal contesto della conversazione/dal nome utente di sistema (2~50 caratteri, senza distinzione maiuscole/minuscole); se l'utente annuisce si usa quello, se vuole cambiarlo si cambia.
- **Password** (obbligatoria; prima fai scegliere tra due opzioni):
  - L'utente la fornisce → poi passala allo script tramite variabile d'ambiente, **mai come parametro a riga di comando**;
  - la genera l'agent → esegui `node scripts/powpow-register.mjs gen-password` e **invia subito all'utente la password appena generata da salvare** (viene mostrata una sola volta, dopo non appare più).
- **Email** (obbligatoria): deve fornirla l'utente — è l'ancora identitaria dell'account, **non indovinarla al posto suo**.
- **Nickname** (facoltativo): proponi come predefinito lo stesso nome utente.
- **Avatar** (facoltativo): se l'utente fornisce il percorso locale di un'immagine (≤5MB, non SVG) lo script la carica direttamente; se non c'è si salta (la piattaforma usa il logo predefinito); se hai capacità di generazione immagini puoi proporti di crearne una.
- **Numero di telefono** (facoltativo, numero della Cina continentale): per impostazione predefinita si salta; chiedilo solo se l'utente vuole esplicitamente associarlo.

Dopo la conferma puoi eseguire `prepare-suggest --username U --nickname N --email E` per registrarlo nel file di stato (poi register non dovrà ripeterli).

## Passi 3–4: codice di verifica via email (l'unico punto in cui bisogna uscire dalla conversazione)

```
node scripts/powpow-register.mjs send-code --email <email>
```

Poi spiega chiaramente all'utente: **vai nell'email a cercare il codice di verifica a 6 cifre, vale 10 minuti; controlla anche la cartella spam/promozioni**; quando lo trovi torni e me lo mandi. L'invio ha un cooldown di 60 secondi, non pigiarlo di continuo.

## Passo 5: invio della registrazione (operazione delegata all'agent)

```
POWPOW_REGISTER_PASSWORD=<password> node scripts/powpow-register.mjs register --code <codice> [--username U] [--nickname N] [--avatar <percorso immagine locale>] [--phone P]
```

Se riesce, l'account è creato (stato pending, con 3 badge iniziali). Gli errori comuni vengono gestiti in automatico, senza interrompere l'utente:

| Errore | Gestione |
|---|---|
| 「用户名已存在」 (il nome utente esiste già) | Proponi automaticamente una variante (nome utente + numero), appena l'utente conferma si riprova subito (il codice è ancora valido, non serve reinviarlo) |
| 「邮箱已被使用」 (email già in uso) | Chiedi all'utente: cambio email, oppure in realtà ha già un account? (passa a login/password dimenticata) |
| 「邮箱验证码错误或已过期」 (codice di verifica errato o scaduto) | Oltre i 10 minuti → esegui di nuovo `send-code` |
| Invio/registrazione troppo frequenti (429) | Aspetta 1 minuto e riprova; basta avvisare l'utente con una frase |

## Passo 6: Accesso con un clic (direttamente sulla home dopo la registrazione)

1. Subito dopo la registrazione riuscita:
   ```
   node scripts/powpow-register.mjs login-link --target home
   ```
2. Invia il link all'utente: **aprilo e finisci direttamente sulla home, già connesso**. La piattaforma è attualmente in un periodo di prova gratuita — dopo la registrazione, tutte le funzioni sono utilizzabili (feed, mappa, umani digitali, check-in ecc.), **nessun pagamento richiesto**.
3. Chiedi all'utente di confermare se è entrato; ci sono due casi:
   - **Finito sulla home** → passa direttamente al Passo 8 per concludere; la registrazione è completa;
   - **Finito sulla pagina di abbonamento** → il periodo di prova gratuita della piattaforma è finito; di' all'utente «il periodo di prova gratuita è finito, ora serve un abbonamento», poi segui il Passo 7 per completare l'abbonamento e torna al Passo 8 quando hai finito.
4. Se l'utente vuole attivamente migliorare o sostenere la piattaforma → vai anche al Passo 7 (abbonarsi è volontario; non insistere).
## Passo 7: Miglioramento dell'abbonamento (opzionale — solo quando il Passo 6 lo richiede)

1. Per prima cosa invia il link di semi-accesso, così la pagina di ritorno del pagamento mostra correttamente «Pagamento riuscito»:
   ```
   node scripts/powpow-register.mjs login-link --target pending
   ```
   Invia il link all'utente: aprendolo, il browser finisce direttamente sulla pagina di abbonamento, già connesso.
2. **Fai scegliere all'utente il metodo di pagamento** — mostra entrambi i canali:
   - **Alipay (Cina continentale / utenti con Alipay)**: acquisto unico della durata corrispondente, **nessun rinnovo automatico**
     - Mensile **¥6.99** (consigliato per provare) / Trimestrale **¥19.99** / Annuale **¥69.99**
   - **PayPal (estero / utenti senza Alipay)**: rinnovo mensile automatico, disdici quando vuoi
     - Premium Monthly, circa **$1/mese** (come mostrato sulla pagina di abbonamento; rinnovo automatico)
3. Una volta scelto:
   - **Alipay**:
     ```
     node scripts/powpow-register.mjs create-order --package monthly
     ```
   - **PayPal**:
     ```
     node scripts/powpow-register.mjs create-order --provider paypal
     ```
   Lo script restituisce il percorso del file della pagina di pagamento; **aprilo direttamente con un comando di sistema** (Windows: `start <file>`; macOS: `open <file>`; Linux: `xdg-open <file>`). Il browser salta automaticamente alla cassa ufficiale Alipay/PayPal, dove l'utente completa il pagamento o l'autorizzazione di addebito.
4. Esegui `query` ogni 10–15 secondi finché non restituisce `paid` o `ACTIVE` (l'incasso/l'autorizzazione di solito arriva in pochi secondi o un minuto). Se l'utente chiude la pagina di pagamento a metà → riesegui direttamente `create-order` (i vecchi ordini / abbonamenti in attesa si chiudono o scadono automaticamente dopo 2 ore; ignorali).
5. Il canale con codice QR WeChat è confermato manualmente e l'incasso può tardare; Huawei IAP è disponibile solo dentro l'app HarmonyOS. Questi due non sono gestiti dallo skill — dopo aver pagato, l'utente torna a dirlo, e l'agent esegue prima `whoami` per confermare l'incasso, poi invia il link alla home del punto 6 qui sotto.
6. Dopo la conferma dell'incasso, scambia contro uno stato di accesso con la dichiarazione di abbonamento più recente, poi invia il link diretto alla home:
   ```
   POWPOW_REGISTER_PASSWORD=<password> node scripts/powpow-register.mjs refresh-login
   node scripts/powpow-register.mjs login-link --target home
   ```
   Invia il link all'utente: **aprilo e finisci direttamente sulla home con l'iscrizione completa**.
## Passo 8: Conclusione

1. `node scripts/powpow-register.mjs cleanup` per ripulire i file di stato temporanei locali (credenziali di sessione).
2. Dai all'utente una «scheda account»: nome utente, e-mail (la password non viene più mostrata — in modalità generata all'utente è già stato chiesto di salvarla al momento della generazione; se l'ha impostata lui, la conosce).
3. Promemoria sull'iscrizione (dillo una volta, non insistere): attualmente è un periodo di prova gratuita e l'account è subito utilizzabile; quando il periodo di prova finirà, gli account senza abbonamento che visitano le pagine di contenuto verranno reindirizzati alla pagina di abbonamento — per un uso prolungato, torna quando vuoi e chiedi all'agent di abbonarti.
4. Guida i primi passi: esplorare la mappa, pubblicare il primo diario di viaggio (→ passa a powpow-simple).
5. Consiglia le estensioni: lo skill `@durenzidu/powpow-integration` e il plugin `@durenzidu/openclaw-channel-powpow` — collega Bolla all'agent dell'utente; dai il comando di installazione se lo desidera.
6. Concludi con un blocco «passo successivo».
## Conversation UX

Mantieni il tono di servizio riconoscibile di powpow:

- **L'utente è il soggetto della frase**; «puoi…» è meglio di «devo chiederti di…»; niente prediche, niente toni dall'alto in basso.
- **Un solo avanzamento decisionale per turno**; prima di chiedere un'informazione, spiega prima il perché.
- **In fondo a ogni risposta** un blocco fisso «prossimo passo» (separatore + 👉 + una sola azione + una frase «quando l'hai fatto, io…»), ad esempio:
  ```
  ────────────────────
  👉 Tocca a te: vai nell'email a cercare il codice a 6 cifre e mandamelo direttamente
     (appena lo ricevo, ti creo l'account)
  ```
- **Non fare prediche di sicurezza sulla password**; non spiegare meccanismi interni, limiti di frequenza o progettazione della sicurezza, salvo che l'utente chieda.
- Più l'agent opera per conto dell'utente, più deve segnalare i progressi: dopo ogni passo dello script comunica con una frase cosa è appena successo («l'account è creato», «ti ho aperto la pagina di pagamento»).

## Regole ferree

- **Sicurezza delle credenziali**: la password passa allo script solo tramite la variabile d'ambiente `POWPOW_REGISTER_PASSWORD`, **mai** come parametro a riga di comando (visibile nell'elenco dei processi), mai scritta in alcun file (in modalità generata viene mostrata una sola volta perché l'utente la salvi, dopo non viene più citata). Il codice di verifica serve solo per l'interfaccia ufficiale di registrazione e viene buttato dopo l'uso.
- **Confine di ufficialità**: tutte le richieste vanno solo a `https://global.powpow.online` (già integrato nello script); non inviare mai informazioni dell'utente a indirizzi di terze parti.
- **Confine del pagamento**: l'agent crea l'ordine, apre la cassa, interroga l'accredito; **mai** toccare l'account Alipay/PayPal o le credenziali di pagamento dell'utente, e mai promettere «pago io al posto tuo».
- **Il paywall non è un bug**: nell'attuale periodo di prova gratuita tutte le pagine di contenuto sono aperte; se l'utente apre il link della home ma finisce sulla pagina di abbonamento, il periodo di prova è finito — guidalo all'abbonamento tramite il Passo 7. Non tentare di aggirare il paywall e non spiegare i meccanismi interni all'utente.
- **Libertà di ripiegare**: se a qualunque passo l'utente vuole far da sé, o l'ambiente non esegue lo script, ripiega in qualunque momento sulla modalità di sola guida — dai i link, spiega le regole, gestisci insieme gli errori.
- Non inventare regole della piattaforma: regole dei campi, testi degli errori e parametri dei limiti vengono tutti dal codice della piattaforma (`references/registration-flow.md` ne cita le fonti); se la piattaforma si aggiorna, fa fede il comportamento effettivo.
- Quando mostri immagini usa solo gli screenshot inclusi nel pacchetto `assets/screenshots/` (l'uso di ciascuno è in `references/screenshots.md`).
- Chiudi ogni turno con il blocco «prossimo passo», così l'utente sa sempre cosa deve fare ora.
