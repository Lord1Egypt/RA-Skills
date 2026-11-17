# powpow-register

Assistente alla registrazione PowPow Bolla (versione OpenClaw): porta un nuovo utente da «non so cos'è Bolla» a
«account attivato, accesso con un clic, si comincia a giocare» — presentazione del prodotto (con screenshot
dell'interfaccia), registrazione delegata all'agent (caricamento avatar incluso), ordine e accredito
dell'abbonamento Alipay/PayPal, accesso con un clic a doppio link, risoluzione degli errori.

**Dalla v2.0.0 modalità assistita dall'agent, e dalla v2.2.0 adattamento al periodo di prova gratuita della piattaforma**: lo script centrale `scripts/powpow-register.mjs` è a zero dipendenze
(Node ≥ 18); l'utente esce dalla conversazione una sola volta: per controllare il codice di verifica nella propria e-mail. Nell'attuale periodo di prova gratuita, un account registrato può usare subito tutte le funzioni — il pagamento dell'abbonamento è un miglioramento opzionale; se il periodo di prova finisce e l'utente finisce sulla pagina di abbonamento, il flusso passa automaticamente al percorso di pagamento. Senza Node, o quando l'utente preferisce fare da sé, rientro automatico nella modalità di sola guida.

## Installazione

```
openclaw skills install @durenzidu/powpow-register
```

## Funzionalità

1. **Presentazione del prodotto**: apertura di ~120 caratteri + screenshot dell'interfaccia inclusi nel pacchetto
   (`assets/screenshots/`, 6 immagini: pagina mappa, pagina dettaglio post ecc., da scegliere 1–3 per scenario;
   senza hosting esterno, utilizzabili offline).
2. **Registrazione delegata**: l'agent propone attivamente nome utente/nickname, password con doppia scelta
   (fornita dall'utente o generata dall'agent), invio e inserimento del codice di verifica, caricamento diretto
   dell'avatar (≤5MB non SVG), gestione automatica degli errori comuni (occupato/scaduto/limiti di frequenza).
3. **Accesso con un clic (doppio link)**: subito dopo la registrazione riuscita, un link di accesso porta l'utente direttamente sulla home (nel periodo di prova gratuita, un clic ed è utilizzabile);
   se finisce sulla pagina di abbonamento (periodo di prova finito) o l'utente vuole migliorare, segui il flusso di abbonamento — dopo l'incasso, scambia contro un nuovo stato di accesso e il link di iscrizione completa lo porta sulla home
   (attraverso il ponte ufficiale `me?token=` della piattaforma, che pianta il cookie HttpOnly automaticamente).
   pianta automaticamente il cookie HttpOnly).
4. **Pagamento dell'abbonamento**: sia Alipay (mese ¥6.99 / trimestre ¥19.99 /
   anno ¥69.99, acquisto una tantum senza rinnovo automatico) sia PayPal (Premium Monthly, circa $1/mese, rinnovo automatico, disdica quando vuoi) sono gestiti dall'agent: ordine + interrogazione dell'accredito;
   per QR WeChat/Huawei IAP solo indicazioni.
5. **Risoluzione degli errori**: codice di verifica che non arriva, nome utente/email occupati, 403 non attivato,
   account bloccato e altri problemi comuni, tutti tratti dal codice sorgente della piattaforma con fonte citata.

## Struttura dei file

```
powpow-register/
├── SKILL.md                            # Guida principale (condizioni di attivazione, flusso in 8 passi, tono, regole ferree)
├── README.md
├── .clawhubignore
├── assets/
│   └── screenshots/                    # Screenshot di prodotto inclusi nel pacchetto (powpow-01~06.jpg)
├── scripts/
│   └── powpow-register.mjs             # Script principale (zero dipendenze, Node≥18, 11 sottocomandi)
└── references/
    ├── agent-flow.md                   # Contratto dello script, sequenza completa, meccanismo del doppio link, sicurezza
    ├── registration-flow.md            # Regole dei campi, limiti di frequenza, tabella errori (con fonti dal codice)
    ├── payment-and-activation.md       # Contratto Alipay vibepay, catena di attivazione, diagnosi per canale
    └── screenshots.md                  # Elenco screenshot del pacchetto + guida rapida per scenario
```

## Sicurezza

- La **password** entra nel processo dello script solo tramite variabile d'ambiente, mai come parametro a riga
  di comando, mai scritta su disco, mai nei file di stato; la password generata dall'agent viene mostrata una
  sola volta perché l'utente la salvi.
- Il **codice di verifica** serve solo per l'interfaccia ufficiale di registrazione e viene buttato dopo l'uso;
  il file di stato (email/nome utente/token/numero d'ordine) sta nella cartella temporanea di sistema, e a fine
  flusso `cleanup` la ripulisce con un solo comando.
- **Pagamento**: l'agent crea l'ordine, apre la cassa, interroga l'accredito; non tocca mai l'account Alipay/PayPal o
  le credenziali di pagamento dell'utente, non paga mai al posto suo. Il pagamento avviene sempre tra l'utente
  e la cassa ufficiale.
- Tutte le richieste vanno solo al dominio ufficiale `https://global.powpow.online`; nessuna chiave inclusa.

## Licenza

MIT-0 (licenza unificata ClawHub).

## Collegamenti

- Sito ufficiale: https://global.powpow.online
- Registrazione: https://global.powpow.online/register
- Conoscere Bolla (video): https://www.bilibili.com/video/BV1Wu826UEVz/
