# Attivazione dell'abbonamento e pagamento — powpow-register

## Conclusione (prima la risposta)
> **Periodo di prova gratuita (a partire dal 2026-10-18; vale il comportamento reale della piattaforma)**: in questo periodo un account registrato può usare direttamente tutte le funzioni, e **abbonarsi è un miglioramento opzionale e non un requisito** — segui il flusso di questo file solo quando l'utente vuole attivamente l'iscrizione. Quando il periodo di prova finirà, gli account senza abbonamento che visitano le pagine di contenuto verranno reindirizzati alla pagina di abbonamento; basta completare l'abbonamento secondo questo file.


**Sia gli abbonamenti con Alipay sia quelli con PayPal possono essere gestiti dall'agent — creazione dell'ordine e tracciamento dell'accredito inclusi.**
Alipay è un acquisto una tantum senza rinnovo automatico, per gli utenti in Cina continentale e chi ha Alipay; PayPal si rinnova automaticamente ogni mese e si può disdire in qualsiasi momento,
per gli utenti all'estero e senza Alipay. Il QR WeChat (conferma manuale) e Huawei IAP restano disponibili, ma la skill non li gestisce.

Confine di responsabilità nel pagamento: l'agent **crea l'ordine, apre la cassa, interroga l'accredito**; non
tocca mai l'account Alipay/PayPal o le credenziali di pagamento dell'utente, e non promette mai «pago al posto tuo».
L'atto del pagamento avviene sempre tra l'utente e la cassa ufficiale.

## Canale Alipay (vibepay, principale)

Modello di acquisto una tantum: si paga una volta e si apre il periodo corrispondente, **senza rinnovo
automatico**. I pacchetti sono definiti in `src/lib/alipay-vibepay.ts` (`ALIPAY_PACKAGES`):

| key | planId | Nome | Prezzo | Durata |
|---|---|---|---|---|
| `monthly` | alipay-monthly | Membro mensile | ¥6.99 | 30 giorni |
| `quarterly` | alipay-quarterly | Membro trimestrale | ¥19.99 | 90 giorni |
| `yearly` | alipay-yearly | Membro annuale | ¥69.99 | 365 giorni |

### Contratto delle interfacce (già incapsulato nello script della skill, l'agent non costruisce richieste per conto proprio)

| Interfaccia | Metodo | Descrizione |
|---|---|---|
| `/api/payment/alipay/create-order` | POST | Richiede `Authorization: Bearer <JWT>` (va bene anche per l'utente pending). body `{package}` → restituisce `{paymentHtml, outTradeNo, amount, planName}`; `paymentHtml` è la pagina con un form che si sottomette da solo al gateway Alipay |
| `/api/payment/alipay/query` | GET `?outTradeNo=` | Stesso Bearer. Restituisce `paid` / `pending` / `closed` / `unknown` |
| `/api/payment/alipay/notify` | POST (callback dal server Alipay) | Verifica della firma su cinque versanti (firma, app_id, coincidenza dell'importo, TRADE_SUCCESS/TRADE_FINISHED, unicità del numero d'ordine commerciante) → aggiornamento dell'ordine **idempotente** + creazione dell'abbonamento + attivazione dell'account. La skill non tocca mai questa interfaccia |
| `/payment/alipay/return` | Pagina di ritorno del browser | Percorso pubblico, dopo il pagamento mostra 「支付成功」, e la pagina fa polling dello stato reale dal backend |

- Gli ordini non pagati **si chiudono automaticamente dopo 2 ore**; se l'utente abbandona a metà → esegui subito
  di nuovo `create-order`, del vecchio ordine non preoccuparti.
- Lo script scrive `paymentHtml` in un file HTML temporaneo, l'agent lo apre con un comando di sistema e si
  arriva dritti alla cassa Alipay (si scannerizza il QR oppure si accede ad Alipay per pagare).

### Catena di attivazione (automatica, nessun lavoro manuale)

La firma del notify passa → l'ordine in `paymentOrders` viene marcato pagato → `user_subscriptions` viene
creata/prorogata (`planId`, `currentPeriodEnd` calcolato da durationDays; il rinnovo si somma solo sulla scadenza
originaria) → `users.accountStatus: active` + `subscriptionStatus: ACTIVE` → la pagina di ritorno intercetta paid
e mostra il successo.

## Dopo il pagamento serve un nuovo stato di accesso (importante)

Nel JWT è incorporata la dichiarazione dell'abbonamento (per l'account pending vale `NONE`). **L'accredito del
pagamento aggiorna solo il database, il JWT già emesso non cambia** — la dichiarazione del vecchio token resta
NONE, e usarlo per generare il link di accesso darebbe l'impressione «nessun abbonamento». Per questo, confermato
il `paid` o lo `ACTIVE` di PayPal, la skill esegue prima `refresh-login` (nuovo login, nuovo JWT, dichiarazione ACTIVE) e solo poi genera
il link 2. È un comportamento voluto dal progetto, non un bug da correggere.

## Canale di abbonamento PayPal (gestito dalla skill; web, non HarmonyOS)

Esiste un solo piano, Premium Monthly (circa $1/mese, secondo quanto restituito da `/api/subscription/plans`); **si rinnova automaticamente ogni mese**
e l'utente può disdirlo quando vuole dal proprio account PayPal.

### Contratto delle interfacce (già incapsulato nello script della skill; l'agent non costruisce richieste per conto proprio)

| Interfaccia | Metodo | Descrizione |
|---|---|---|
| `/api/subscription/plans` | GET | Auth Bearer; restituisce l'elenco dei piani disponibili (al momento solo 1) |
| `/api/subscription/create` | POST | body `{planId}` → restituisce `{subscriptionId, approveUrl, status}`; `status` di solito è `APPROVAL_PENDING` |
| `/api/subscription/create` | GET | Auth Bearer; restituisce `{activeSubscription, allSubscriptions}`; l'agent fa polling di `activeSubscription.subscription.status === 'ACTIVE'` |
| `/api/subscription/verify` | POST | La chiama automaticamente la pagina di successo (con il cookie); attiva direttamente tramite l'API PayPal se il webhook non è arrivato |
| `/subscription/success` | Pagina di ritorno del browser | Dove si atterra dopo l'autorizzazione PayPal; fa polling di verify automaticamente e poi torna alla home / pagina originale |
| `/subscription/cancel` | Pagina del browser | Dove si atterra se l'utente annulla o qualcosa fallisce; si può riprovare |

### Flusso delegato

```
create-order --provider paypal  # → restituisce approveUrl, scritto in un file HTML locale
aprire il file HTML             # → il browser salta alla pagina di autorizzazione PayPal
query (ogni 10–15s)             # → fare polling fino ad ACTIVE
refresh-login                   # → scambiare con un JWT nuovo (dichiarazione di abbonamento ACTIVE)
login-link --target home        # → generare il link di accesso definitivo
```

- Gli abbonamenti PENDING non completati entro 1 ora vengono ripuliti automaticamente dal backend; basta ricominciare.
- Se l'utente ripete `create-order`, il backend riutilizza l'abbonamento `APPROVAL_PENDING` ancora valido, evitando un 409.
- Come con Alipay: l'accredito aggiorna solo il database, un JWT vecchio non si rinnova da sé — **bisogna** eseguire `refresh-login` prima di inviare il link alla home.

## I quattro canali della pagina abbonamento

La pagina abbonamento `src/app/(public)/subscription/page.tsx` mostra in base all'ambiente di esecuzione:

| Canale | Ambiente | Meccanismo | Come si attiva |
|---|---|---|---|
| **Alipay (principale)** | Web | `AlipayPaymentSection` agganciata alle interfacce vibepay (tabella sopra) | Attivazione automatica lato server via notify, questione di secondi |
| Abbonamento PayPal | Web (non su HarmonyOS) | `/api/subscription/create` → autorizzazione PayPal; mensile con rinnovo automatico, disdica quando vuoi (`/api/subscription/manage`) | Il Webhook PayPal (`BILLING.SUBSCRIPTION.*`) attiva in automatico |
| Abbonamento QR WeChat | Web (non su HarmonyOS) | In fondo alla pagina 「微信扫码订阅」: trasferimento scannerizzando il QR | **Conferma manuale**, l'accredito può ritardare; non ritenerlo fallito subito dopo aver pagato |
| Acquisto in-app Huawei | Dentro l'app HarmonyOS | Chiamata nativa `NativeBridge.purchaseSubscription()` | `/api/subscription/activate-huawei` verifica l'ordine Huawei e attiva |

Pacchetti e prezzi PayPal arrivano dinamici da `/api/subscription/plans`; testo statico sulla pagina:
Auto-renews. Cancel anytime.

## Stati e reindirizzamenti

- Alipay completato → la pagina di ritorno mostra il successo; PayPal riuscito → `/subscription/success` →
  account attivo → ritorno automatico alla pagina di origine secondo il parametro `next` (se manca, alla home).
- Chi è già membro apre la pagina abbonamento → vede "You're All Set!", e dopo 3 secondi si torna in home da soli.
- Pagamento fallito/annullato (PayPal) → `/subscription/cancel`, si può riprovare.

## Diagnosi

| Sintomo | Rimedio |
|---|---|
| Dopo il pagamento Alipay `query` resta pending | Il ritardo del notify è raro; attendere 30 secondi e ricontrollare. Se ancora niente, far guardare all'utente lo stato sulla pagina di ritorno nel browser; se persiste, contattare l'assistenza della piattaforma (dongtao@outlook.com) fornendo l'`outTradeNo` |
| Alipay ha addebitato, ma col link 2 si viene comunque respinti | `refresh-login` è stato saltato (la dichiarazione del vecchio JWT non è stata aggiornata) — prima `refresh-login`, poi `login-link` |
| Il `query` di PayPal resta PENDING | L'utente non ha completato l'autorizzazione su PayPal; verifica che il link di autorizzazione sia stato aperto nel browser. Se dopo l'autorizzazione resta PENDING, può essere un ritardo del webhook: chiedi all'utente di attendere qualche secondo in più sulla pagina di successo o di ricaricarla |
| Il `query` di PayPal restituisce 409 | Esiste già un abbonamento PENDING non completato; attendi 1 ora perché scada, oppure completa l'autorizzazione del vecchio link nel browser |
| PayPal pagato, ma con il link 2 si viene comunque respinti | Come con Alipay: prima `refresh-login`, poi `login-link` |
| Ancora 403 dopo il pagamento (PayPal) | Il Webhook a volte ritarda; rifare il login per aggiornare lo stato |
| Pagato via WeChat, l'abbonamento non si apre | La conferma manuale è asincrona; se dopo qualche ora non si è aperto, contattare l'assistenza della piattaforma |
| La pagina abbonamento mostra "No subscription plans available" | `/api/subscription/plans` non restituisce pacchetti PayPal, guasto di configurazione lato piattaforma; gli utenti della Cina continentale possono nel frattempo usare Alipay |

## Nota storica

Nel codice esiste anche un **vecchio** set di pagamento web Alipay (`src/lib/alipay.ts`,
`/api/payment/create-order`, una tantum ¥9.90/¥99, con pagamento simulato se manca la chiave sandbox), mai
collegato alla UI della pagina abbonamento e privo di rapporti con vibepay. La skill non lo tocca; il canale
attuale è `alipay-vibepay.ts`.
